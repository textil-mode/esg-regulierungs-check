"""Lädt Gesetzestexte aus dem Internet, extrahiert Klartext, cached sie in SQLite.

ETag/Last-Modified werden genutzt, um bei erneutem Fetch nur zu aktualisieren
wenn sich wirklich etwas geändert hat. So wird "Aktualitätscheck" billig.
"""
from __future__ import annotations

import hashlib
import io
import os
import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

import db as _db


USER_AGENT = "ESG-Regulierungs-Check/1.0 (+https://localhost)"

# Optionale Modul-Ueberschreibung fuer Tests (`fetcher.DB_PATH = …`).
# None = es gilt der in db.py konfigurierte Pfad, inklusive `ESG_DB_PATH`.
# So genuegt eine einzige Stellschraube, statt beide Module patchen zu muessen.
DB_PATH: Path | None = None


def _db_path() -> Path:
    return Path(DB_PATH) if DB_PATH else Path(_db.DB_PATH)


def _conn() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_fetcher() -> None:
    with _conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS law_texts (
                reg_key TEXT NOT NULL,
                language TEXT NOT NULL DEFAULT 'de',
                url TEXT NOT NULL,
                text TEXT NOT NULL,
                etag TEXT,
                last_modified TEXT,
                fetched_at TEXT NOT NULL,
                source_status INTEGER,
                PRIMARY KEY (reg_key, language)
            )
            """
        )
        # Migration: alte Tabelle ohne language → language='de' setzen (idempotent)
        cols = {row[1] for row in c.execute("PRAGMA table_info(law_texts)").fetchall()}
        if "language" not in cols:
            c.execute("ALTER TABLE law_texts ADD COLUMN language TEXT NOT NULL DEFAULT 'de'")
        # Herkunft des Texts im Klartext (welche CELEX-Fassung, Notbehelf ja/nein).
        # `source_status` allein kann das nicht tragen und waere fuer den
        # Admin-Blick auch nicht lesbar.
        if "source_note" not in cols:
            c.execute("ALTER TABLE law_texts ADD COLUMN source_note TEXT")
        # Historie: je inhaltlich abweichender Fassung eine Zeile. `law_texts`
        # haelt nur den letzten Stand — ohne Historie waere weder erkennbar
        # NOCH belegbar, dass sich ein Gesetzestext geaendert hat.
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS law_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg_key TEXT NOT NULL,
                language TEXT NOT NULL,
                text_hash TEXT NOT NULL,
                text TEXT NOT NULL,
                url TEXT,
                fetched_at TEXT NOT NULL
            )
            """
        )
        c.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS ux_law_versions "
            "ON law_versions (reg_key, language, text_hash)"
        )
        c.execute(
            "CREATE INDEX IF NOT EXISTS ix_law_versions_recent "
            "ON law_versions (reg_key, language, id DESC)"
        )


def _extract_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()
    main = soup.find("main") or soup.find(id=re.compile("content|main|text", re.I)) or soup.body or soup
    text = main.get_text("\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = []
        # max 60 Seiten (reicht für Anwendungsbereich + Kernartikel)
        for i, page in enumerate(reader.pages[:60]):
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                continue
        text = "\n".join(pages)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    except Exception as e:  # noqa: BLE001
        return f"[PDF-Extraktion fehlgeschlagen: {e}]"


_EURLEX_LANG_MAP = {
    "de": ("deu", "DE"),
    "en": ("eng", "EN"),
    "es": ("spa", "ES"),
    "fr": ("fra", "FR"),
    "it": ("ita", "IT"),
    # ZH wird auf EN gemappt (EUR-Lex hat kein Chinesisch)
    "zh": ("eng", "EN"),
}

_ACCEPT_LANG_MAP = {
    "de": "de,en;q=0.7",
    "en": "en,de;q=0.7",
    "es": "es,en;q=0.7,de;q=0.5",
    "fr": "fr,en;q=0.7,de;q=0.5",
    "it": "it,en;q=0.7,de;q=0.5",
    "zh": "en,de;q=0.7",  # ZH → EN-Text
}


def _accept_language(lang: str) -> str:
    return _ACCEPT_LANG_MAP.get(lang, "de,en;q=0.7")


def _store_limit() -> int:
    """Wieviel Text im Cache abgelegt wird.

    Bewusst getrennt von FULLTEXT_MAX_CHARS (= Budget fuer den LLM-Kontext):
    lawparse.build_context waehlt die relevanten Artikel erst aus dem
    vollstaendigen Text aus. Wuerde hier schon auf das LLM-Budget gekappt,
    fehlte der Anwendungsbereich weiterhin (EU-Rechtsakte beginnen mit
    Erwaegungsgruenden).
    """
    return int(os.getenv("LAW_TEXT_MAX_CHARS", "400000"))


# EUR-Lex liefert seit 2026 fuer Server-Clients eine AWS-WAF-Challenge
# (HTTP 202, leerer Body). Der Volltext liegt identisch beim Amt fuer
# Veroeffentlichungen; von dort wird er als Fallback geholt.
_CELEX_FROM_URL = re.compile(r"CELEX[:%]?(?:3A)?([0-9][0-9A-Z\-]+)", re.I)
_ELI_FROM_URL = re.compile(r"/eli/(dir|reg|reg_del|dec)/(\d{4})/(\d+)/oj", re.I)
_ELI_SECTOR = {"dir": "L", "reg": "R", "reg_del": "R", "dec": "D"}


def _celex_id(url: str) -> str | None:
    m = _CELEX_FROM_URL.search(url)
    if m:
        return m.group(1).upper()
    m = _ELI_FROM_URL.search(url)
    if m:
        kind, year, num = m.group(1).lower(), m.group(2), m.group(3)
        return f"3{year}{_ELI_SECTOR.get(kind, 'R')}{int(num):04d}"
    return None


# Cellar loest nur zwei Formen auf: den Basisrechtsakt (`32024L1760`) und eine
# DATIERTE konsolidierte Fassung (`02024L1760-20260318`). Eine datumslose
# konsolidierte ID (`02024L1760`) liefert dort 404 — genau die Form, die in
# `regulations.py` steht, damit die Quelle nicht auf einem Konsolidierungsstand
# einfriert. Die juengste datierte Fassung wird deshalb zur Laufzeit ueber den
# SPARQL-Endpunkt des Amts fuer Veroeffentlichungen ermittelt.
_SPARQL_URL = "https://publications.europa.eu/webapi/rdf/sparql"
_DATED_CELEX = re.compile(r"^0\d{4}[A-Z]\d{4}-\d{8}$")
_UNDATED_CONSOLIDATED = re.compile(r"^0(\d{4}[A-Z]\d{4})$")

# Eigener, KURZER Timeout: die Konsolidierungssuche ist eine Zusatzabfrage vor
# dem eigentlichen Download. Mit dem 60-s-Timeout des Cellar-Abrufs koennte sie
# Phase 1 (sequenziell ueber alle Regulierungen) um Minuten verlaengern.
_SPARQL_TIMEOUT = float(os.getenv("SPARQL_TIMEOUT", "8"))

# Ergebniszustaende der Konsolidierungssuche. Bewusst nur zwei: entweder die
# konsolidierte Fassung steht fest, oder sie steht NICHT fest.
#
# Ein leeres Suchergebnis gilt dabei ebenfalls als "nicht ermittelt" und NICHT
# als "es gibt keine konsolidierte Fassung". Grund: eine `0…`-CELEX-ID existiert
# ueberhaupt nur dann, wenn EUR-Lex eine konsolidierte Fassung fuehrt. Kommt zu
# einer solchen ID keine Trefferzeile zurueck, hat die Abfrage versagt (z. B.
# Drosselung des Endpunkts) — genau dieser Fall ist im Test am 01.09.2026 fuer
# EUDR aufgetreten und haette sonst den Ursprungsrechtsakt legitimiert.
RESOLVE_CONSOLIDATED = "consolidated"
RESOLVE_UNRESOLVED = "unresolved"

# Prozess-Cache: pro Lauf wird jede CELEX-ID hoechstens einmal aufgeloest.
# ACHTUNG: NUR Erfolge werden gecacht. Wuerde auch `unresolved` gecacht,
# vergiftete ein Sekunden-Ausfall des Endpunkts den Gunicorn-Worker bis zum
# Neustart.
_consolidated_cache: dict[str, str] = {}


def _base_act_celex(celex: str) -> str:
    """`02024L1760` → `32024L1760` (Basisrechtsakt, immer in Cellar vorhanden)."""
    m = _UNDATED_CONSOLIDATED.match(celex)
    return f"3{m.group(1)}" if m else celex


def _sparql_latest(celex: str, timeout: float) -> str:
    """Eine SPARQL-Abfrage; liefert die datierte CELEX-ID oder ''."""
    query = (
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n"
        "SELECT ?celex WHERE {\n"
        "  ?w cdm:resource_legal_id_celex ?celex .\n"
        f'  FILTER(STRSTARTS(STR(?celex), "{celex}-"))\n'
        "}\nORDER BY DESC(?celex) LIMIT 1"
    )
    with httpx.Client(timeout=timeout, follow_redirects=True,
                      headers={"User-Agent": USER_AGENT,
                               "Accept": "application/sparql-results+json"}) as client:
        resp = client.get(_SPARQL_URL, params={
            "query": query, "format": "application/sparql-results+json"})
    if resp.status_code >= 400:
        raise RuntimeError(f"HTTP {resp.status_code}")
    bindings = resp.json().get("results", {}).get("bindings", [])
    if not bindings:
        return ""
    value = (bindings[0].get("celex") or {}).get("value") or ""
    return value if _DATED_CELEX.match(value) else ""


def _latest_consolidated(celex: str, timeout: float | None = None) -> tuple[str, str]:
    """Juengste konsolidierte Fassung zu einer datumslosen `0…`-CELEX-ID.

    Rueckgabe `(celex, zustand)`:
      * `("02024L1760-20260318", RESOLVE_CONSOLIDATED)` — Fassung steht fest.
      * `("32024L1760", RESOLVE_UNRESOLVED)` — nicht ermittelbar. Der
        Basisrechtsakt ist dann nur ein Notbehelf und inhaltlich womoeglich
        falsch (bei der CSDDD z. B. die Ursprungsfassung mit 3 000 Beschaeftigten
        und 900 Mio. EUR statt der geltenden 5 000 / 1,5 Mrd.). Der Aufrufer MUSS
        diesen Zustand anders behandeln.

    Ein zweiter Versuch faengt die haeufigste Ursache ab: der Endpunkt drosselt
    bei mehreren Abfragen kurz hintereinander, wie sie ein Analyse- oder
    Watchdog-Lauf ueber alle Regulierungen ausloest.
    """
    if celex in _consolidated_cache:
        return _consolidated_cache[celex], RESOLVE_CONSOLIDATED
    t = timeout or _SPARQL_TIMEOUT
    last_problem = "leeres Ergebnis"
    for attempt in (1, 2):
        try:
            value = _sparql_latest(celex, t)
        except Exception as e:  # noqa: BLE001
            last_problem = f"{type(e).__name__}: {e}"
            value = ""
        if value:
            _consolidated_cache[celex] = value
            return value, RESOLVE_CONSOLIDATED
        if attempt == 1:
            time.sleep(1.5)
    print(f"[cellar] Konsolidierungssuche {celex} ergebnislos ({last_problem}) — "
          f"Ergebnis wird NICHT gecacht", flush=True)
    return _base_act_celex(celex), RESOLVE_UNRESOLVED


def _cellar_fetch(celex: str, language: str, timeout: float) -> str:
    """Volltext einer konkreten CELEX-Resource, sonst ''.

    Die Kette laeuft durchgehend ueber https: der 303-Redirect der
    CELEX-Resource zeigt auf eine `http://…/cellar/…`-URL, deshalb wird jeder
    Redirect selbst verfolgt und vorher auf https hochgestuft. Sonst kaeme der
    Gesetzestext — die Eingabe der LLM-Analyse — unverschluesselt an und waere
    unterwegs manipulierbar.
    """
    three, _ = _EURLEX_LANG_MAP.get(language, ("deu", "DE"))
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/xhtml+xml",
        "Accept-Language": three,
    }
    target = f"https://publications.europa.eu/resource/celex/{celex}"
    try:
        with httpx.Client(timeout=timeout, follow_redirects=False, headers=headers) as client:
            for _ in range(5):
                resp = client.get(target)
                if resp.status_code not in (301, 302, 303, 307, 308):
                    break
                location = resp.headers.get("location") or ""
                if not location:
                    return ""
                target = str(httpx.URL(target).join(location))
                if target.startswith("http://"):
                    target = "https://" + target[len("http://"):]
            else:
                print(f"[cellar] {celex}: zu viele Redirects", flush=True)
                return ""
        if resp.status_code >= 400:
            return ""
        content_type = (resp.headers.get("content-type") or "").lower()
        if "pdf" in content_type or target.lower().endswith(".pdf"):
            return _extract_pdf(resp.content)
        if "html" in content_type or "xml" in content_type:
            return _extract_html(resp.text)
        # Alles andere (RDF/N-Triples/ZIP …) ist kein Gesetzestext.
        print(f"[cellar] {celex}: unerwarteter Content-Type {content_type!r}", flush=True)
        return ""
    except Exception as e:  # noqa: BLE001
        print(f"[cellar] {celex} fehlgeschlagen: {e}", flush=True)
        return ""


class CellarResult(NamedTuple):
    """Ergebnis eines Cellar-Abrufs samt Herkunft des Texts.

    `kind` ist entscheidend fuer die Vertrauenswuerdigkeit:
      * `RESOLVE_CONSOLIDATED` — die geltende konsolidierte Fassung.
      * `RESOLVE_UNRESOLVED` — Basisrechtsakt als Notbehelf, weil die
        Konsolidierung nicht ermittelt oder nicht geladen werden konnte.
        **Inhaltlich verdaechtig — spaetere Aenderungen fehlen.**
      * `""` — die URL nannte direkt einen Ursprungsrechtsakt (`3…`/`5…`),
        es war also gar keine Konsolidierung angefragt.
    """
    text: str
    celex: str
    kind: str
    # Die vom Resolver ermittelte konsolidierte Fassung, auch wenn sie sich
    # nicht laden liess ('' wenn die Aufloesung selbst scheiterte). Erlaubt dem
    # Aufrufer zu unterscheiden, ob eine Konsolidierung fehlt oder nur ihre
    # Textfassung nicht abrufbar war.
    resolved_celex: str = ""


def _is_consolidated_text(text: str, celex: str) -> bool:
    """Traegt der geladene Text die Kopfzeile der konsolidierten Fassung?

    Konsolidierte Fassungen beginnen mit einer Kennungszeile
    `02024L1760 — DE — 18.03.2026 — 002.001`; aeltere Konsolidierungen drucken
    dieselbe Kennung OHNE fuehrende Null (`2014L0095 — DE — 05.12.2014`), daher
    ist sie hier optional. Ursprungsrechtsakte beginnen dagegen mit
    `Amtsblatt der Europaeischen Union …` und haben diese Zeile nicht.

    Diese Pruefung am INHALT ist die eigentliche Absicherung: sie greift auch
    dann, wenn die Konsolidierungssuche faelschlich einen Erfolg meldet oder
    Cellar unter einer konsolidierten Kennung den Ursprungstext ausliefert.
    """
    stem = celex[1:] if celex.startswith("0") else celex
    pattern = rf"\b0?{re.escape(stem)}\s*[—–-]\s*[A-Z]{{2}}\s*[—–-]"
    return re.search(pattern, text[:300]) is not None


def _cellar_text(url: str, language: str, timeout: float) -> CellarResult:
    """Volltext ueber publications.europa.eu zur CELEX-ID in `url`.

    Bei datumsloser konsolidierter ID wird die juengste konsolidierte Fassung
    ermittelt und geladen. Der Basisrechtsakt wird nur als Rueckfallebene
    versucht — und das Ergebnis dann als solches markiert, damit der Aufrufer
    entscheiden kann, ob er ihn ueberhaupt akzeptieren will.
    """
    celex = _celex_id(url)
    if not celex:
        return CellarResult("", "", "")
    if not _UNDATED_CONSOLIDATED.match(celex):
        # Die URL nennt direkt einen Ursprungsrechtsakt — dann ist er auch das
        # Gewuenschte, es gibt nichts zu pruefen.
        return CellarResult(_cellar_fetch(celex, language, timeout), celex, "")

    resolved, state = _latest_consolidated(celex)
    consolidated_id = resolved if state == RESOLVE_CONSOLIDATED else ""
    if state == RESOLVE_CONSOLIDATED:
        text = _cellar_fetch(resolved, language, timeout)
        if text and _is_consolidated_text(text, celex):
            return CellarResult(text, resolved, RESOLVE_CONSOLIDATED, consolidated_id)
        if text:
            print(f"[cellar] {resolved}: geladener Text traegt keine konsolidierte "
                  f"Kopfzeile — als Ursprungsfassung behandelt", flush=True)
            return CellarResult(text, resolved, RESOLVE_UNRESOLVED, consolidated_id)

    # Konsolidierung nicht ermittelbar oder nicht ladbar: Der Basisrechtsakt ist
    # hier zunaechst nur ein Notbehelf. `resolved_celex` sagt dem Aufrufer, ob
    # ueberhaupt eine Konsolidierung existiert — davon haengt ab, ob wirklich
    # etwas fehlt.
    base = _base_act_celex(celex)
    base_text = _cellar_fetch(base, language, timeout)
    return CellarResult(base_text, base, RESOLVE_UNRESOLVED, consolidated_id)


def _localized_url(url: str, lang: str) -> str:
    """EUR-Lex unterstützt /oj/<3-letter> bzw. /legal-content/<2-letter>/.
    Andere URLs (z.B. gesetze-im-internet.de) unverändert.
    """
    three, two = _EURLEX_LANG_MAP.get(lang, ("deu", "DE"))
    if "eur-lex.europa.eu" in url and url.rstrip("/").endswith("/oj"):
        return url.rstrip("/") + f"/{three}"
    if "eur-lex.europa.eu/legal-content/" in url:
        # Ersetze /DE/ bzw. /EN/ / etc. durch Zielsprache
        import re as _re
        return _re.sub(r"/legal-content/[A-Z]{2}/", f"/legal-content/{two}/", url, count=1)
    return url


def _fetch_url(reg: dict) -> str:
    """Welche URL soll der Fetcher laden?

    Bei EU-Regularien zeigt 'url' auf die EUR-Lex-Suche (UI-Verlinkung),
    und 'text_url' enthält den kanonischen ELI/CELEX-Link für den Volltext.
    Fehlt 'text_url', wird 'url' verwendet (z.B. DE-Gesetze).
    """
    return reg.get("text_url") or reg["url"]


# ---------------------------------------------------------------------------
# Textversionierung
# ---------------------------------------------------------------------------
def text_hash(text: str) -> str:
    """SHA-256 des Gesetzestexts (Vergleichsschluessel fuer Versionen)."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def current_text_hash(reg_key: str, language: str = "de") -> str | None:
    """SHA-256 des aktuell gecachten Gesetzestexts, oder None ohne Cache.

    Stabiler Schluessel fuer alles, was am Gesetzesstand haengt (z. B.
    Cache-Invalidierung nachgelagerter Auswertungen): der Hash aendert sich
    genau dann, wenn sich der Text inhaltlich geaendert hat. Ein leerer Text
    (fehlgeschlagener Abruf) liefert ebenfalls None, nicht den Hash des
    leeren Strings.
    """
    init_fetcher()
    with _conn() as c:
        row = c.execute(
            "SELECT text FROM law_texts WHERE reg_key = ? AND language = ?",
            (reg_key, language),
        ).fetchone()
    if not row or not (row["text"] or "").strip():
        return None
    return text_hash(row["text"])


def _record_version(c: sqlite3.Connection, reg_key: str, language: str,
                    url: str, text: str, fetched_at: str) -> tuple[bool, str | None]:
    """Legt bei inhaltlicher Aenderung eine neue Version an.

    Rueckgabe: (ist_neue_version, Hash der Vorgaengerversion).
    Leere Texte werden nicht versioniert — ein gescheiterter Abruf ist keine
    Gesetzesaenderung.
    """
    if not (text or "").strip():
        return False, None
    new_hash = text_hash(text)
    prev = c.execute(
        "SELECT text_hash FROM law_versions WHERE reg_key = ? AND language = ? "
        "ORDER BY id DESC LIMIT 1",
        (reg_key, language),
    ).fetchone()
    prev_hash = prev["text_hash"] if prev else None
    if prev_hash == new_hash:
        return False, prev_hash
    c.execute(
        "INSERT OR IGNORE INTO law_versions (reg_key, language, text_hash, text, url, fetched_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (reg_key, language, new_hash, text, url, fetched_at),
    )
    return True, prev_hash


def list_versions(reg_key: str, language: str = "de", limit: int = 10) -> list[dict]:
    """Versionshistorie (neueste zuerst), ohne den Volltext."""
    init_fetcher()
    with _conn() as c:
        rows = c.execute(
            "SELECT id, text_hash, url, fetched_at, LENGTH(text) AS chars "
            "FROM law_versions WHERE reg_key = ? AND language = ? "
            "ORDER BY id DESC LIMIT ?",
            (reg_key, language, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def version_text(reg_key: str, language: str, text_hash_value: str) -> str:
    """Volltext einer bestimmten Version (leer, wenn unbekannt)."""
    init_fetcher()
    with _conn() as c:
        row = c.execute(
            "SELECT text FROM law_versions WHERE reg_key = ? AND language = ? AND text_hash = ?",
            (reg_key, language, text_hash_value),
        ).fetchone()
    return row["text"] if row else ""


def _is_initial_consolidation(reg: dict, resolved_celex: str) -> bool:
    """Ist die ermittelte Konsolidierung auf den Tag der ABl.-Veroeffentlichung datiert?

    Dann gibt sie den Rechtsakt unveraendert wieder — es existieren keine
    spaeteren Aenderungen, und der Ursprungstext ist der geltende Text. Nur so
    laesst sich "wir vermissen Aenderungen" (echte Warnung) von "es gibt keine
    Aenderungen" (kein Grund zur Warnung) unterscheiden.

    Ohne diese Unterscheidung stuende auf der Admin-Seite dauerhaft eine
    sachlich falsche Warnung, was den Wert aller uebrigen Warnungen zerstoert.
    """
    if not resolved_celex or len(resolved_celex) < 8:
        return False
    # Lokaler Import: `regulations` ist die Inhalts-, `fetcher` die Datenschicht.
    # Ein Import auf Modulebene wuerde die Richtung dauerhaft festschreiben.
    from regulations import published_for
    published = published_for(reg.get("key", ""))
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", published or ""):
        return False
    d, m, y = published.split(".")
    return resolved_celex[-8:] == f"{y}{m}{d}"


def _cached_result(row, status: int, error: str | None) -> dict:
    """Rueckgabe aus dem Cache (304 oder Fehler mit vorhandenem Text)."""
    text = row["text"] if row else ""
    return {
        "text": text,
        "fetched_at": row["fetched_at"] if row else None,
        "is_new": False,
        "error": error,
        "status": status,
        "text_hash": text_hash(text) if (text or "").strip() else None,
        "version_new": False,
        "previous_hash": None,
        "source_note": (row["source_note"] if row and "source_note" in row.keys() else None),
    }


# `source_status` kodiert die Herkunft des gespeicherten Texts:
#   > 0    Primaerquelle hat geantwortet (Wert = HTTP-Status)
#   < 0    Cellar-Fallback benutzt, Betrag = Status der Primaerantwort
#          (z. B. -202 = WAF-Challenge von EUR-Lex)
#   < -1000  wie oben, ABER nur der Basisrechtsakt statt der konsolidierten
#          Fassung — inhaltlich verdaechtig. Betrag - 1000 = Primaerstatus.
SOURCE_STATUS_BASE_ACT_OFFSET = -1000

# Faellt ein Abruf unter diesen Anteil des bisherigen Textumfangs, gilt er als
# gescheitert und der Cache-Stand bleibt stehen. Echte Konsolidierungen kuerzen
# einen Rechtsakt nie um die Haelfte; ein solcher Sprung deutet auf eine
# Fehlerseite oder einen abgebrochenen Download hin.
_MIN_KEEP_RATIO = 0.5


def source_is_base_act_fallback(source_status: int | None) -> bool:
    """True, wenn der gespeicherte Text nur der Ursprungsrechtsakt ist.

    Dann fehlen alle spaeteren Aenderungen — bei der CSDDD beispielsweise die
    Omnibus-Schwellen. Die Admin-Seite weist solche Eintraege deutlich aus.
    """
    return source_status is not None and source_status <= SOURCE_STATUS_BASE_ACT_OFFSET


def fetch_law_text(reg: dict, *, language: str = "de", force: bool = False) -> dict:
    """Lädt den Gesetzestext.

    Liefert {text, fetched_at, is_new, error, status, text_hash, version_new,
    previous_hash}. `version_new` ist True, wenn der Text inhaltlich von der
    zuletzt gespeicherten Fassung abweicht und deshalb eine neue Zeile in
    `law_versions` entstanden ist.

    Nutzt ETag/Last-Modified für conditional-GET. Bei 304 wird der Cache-Text
    zurückgegeben. Bei Fehlern mit vorhandenem Cache: Cache-Text zurück + error.
    """
    init_fetcher()
    url = _localized_url(_fetch_url(reg), language)
    with _conn() as c:
        row = c.execute(
            "SELECT text, url, etag, last_modified, fetched_at, source_note FROM law_texts "
            "WHERE reg_key = ? AND language = ?",
            (reg["key"], language),
        ).fetchone()

    headers = {"User-Agent": USER_AGENT, "Accept-Language": _accept_language(language)}
    if row and not force:
        if row["etag"]:
            headers["If-None-Match"] = row["etag"]
        if row["last_modified"]:
            headers["If-Modified-Since"] = row["last_modified"]

    try:
        with httpx.Client(timeout=30, follow_redirects=True, headers=headers) as client:
            resp = client.get(url)
    except Exception as e:  # noqa: BLE001
        return _cached_result(row, -1, str(e))

    if resp.status_code == 304 and row:
        # Unveraendert laut Quelle — aber die Historie kann noch leer sein
        # (erster Lauf nach Einfuehrung der Versionierung).
        with _conn() as c:
            _record_version(c, reg["key"], language, url, row["text"], row["fetched_at"])
        return _cached_result(row, 304, None)

    if resp.status_code >= 400:
        text = ""
    else:
        content_type = (resp.headers.get("content-type") or "").lower()
        if "pdf" in content_type or url.lower().endswith(".pdf"):
            text = _extract_pdf(resp.content)
        else:
            text = _extract_html(resp.text)

    # EUR-Lex antwortet Server-Clients mit einer WAF-Challenge (HTTP 202,
    # leerer Body). Dann den Volltext beim Amt fuer Veroeffentlichungen holen.
    # Genau ein Fallback-Versuch — Phase 1 laeuft sequenziell ueber alle 20
    # Regulierungen, ein zweiter Anlauf koennte pro Reg 60 s zusaetzlich kosten.
    used_fallback = False
    source_note = f"Primaerquelle HTTP {resp.status_code}"
    base_act_only = False
    initial_consolidation = False
    if len(text.strip()) < 2000 and "eur-lex.europa.eu" in url:
        cellar = _cellar_text(url, language, 60.0)
        if len(cellar.text) > len(text):
            base_act_only = cellar.kind == RESOLVE_UNRESOLVED
            if base_act_only and _is_initial_consolidation(reg, cellar.resolved_celex):
                # Es GIBT eine konsolidierte Fassung, sie liess sich nur nicht
                # abrufen — aber sie ist auf den Tag der Veroeffentlichung im
                # Amtsblatt datiert. Eine solche Erstkonsolidierung gibt den
                # Rechtsakt unveraendert wieder; spaetere Aenderungen existieren
                # nicht. Der Ursprungstext ist damit der geltende Text, und eine
                # Warnung "Nur Ursprungsfassung" waere sachlich falsch.
                # (Fall ESG-Rating-VO: 02024R3005-20241212, ABl. vom 12.12.2024,
                # Cellar liefert dafuer dauerhaft HTTP 404.)
                base_act_only = False
                initial_consolidation = True
                print(f"[fetch] {reg['key']}: konsolidierte Fassung "
                      f"{cellar.resolved_celex} nicht abrufbar, entspricht aber der "
                      f"Erstfassung — Ursprungstext ist der geltende Text", flush=True)
            if base_act_only and row and (row["text"] or "").strip():
                # KERNENTSCHEIDUNG: Die konsolidierte Fassung liess sich nicht
                # ermitteln, und der Ersatz waere die Ursprungsfassung — bei der
                # CSDDD z. B. mit 3 000 Beschaeftigten / 900 Mio. EUR statt der
                # geltenden 5 000 / 1,5 Mrd. Ein bekannter, evtl. etwas aelterer
                # Stand ist besser als ein still falscher: Cache behalten und den
                # Grund als Fehler melden, damit er auf der Admin-Seite auftaucht.
                print(f"[fetch] {reg['key']}: Konsolidierung nicht aufloesbar — "
                      f"Cache-Stand behalten statt Basisrechtsakt {cellar.celex}", flush=True)
                return _cached_result(
                    row, resp.status_code,
                    f"Konsolidierte Fassung nicht ermittelbar (SPARQL); "
                    f"Basisrechtsakt {cellar.celex} verworfen, Cache-Stand behalten",
                )
            text = cellar.text
            used_fallback = True
            source_note = f"Cellar {cellar.celex}" + (
                " (nur Basisrechtsakt — Konsolidierung nicht ermittelbar)"
                if base_act_only else
                f" (= Erstkonsolidierung {cellar.resolved_celex}, keine spaeteren Aenderungen)"
                if initial_consolidation else ""
            )

    if resp.status_code >= 400 and not text:
        return _cached_result(row, resp.status_code, f"HTTP {resp.status_code}")

    text = text[:_store_limit()]

    # --- Schutz vor Datenverlust ------------------------------------------
    # Ein brauchbarer Cache-Text darf NIE durch einen leeren oder drastisch
    # kuerzeren Abruf ersetzt werden. Ohne diese Pruefung ueberschrieb ein
    # Doppelausfall (EUR-Lex antwortet mit der WAF-Challenge UND Cellar liefert
    # nichts) einen vollstaendigen Gesetzestext durch einen Leerstring — ohne
    # Fehlermeldung, weil der bisherige Schutz innerhalb des Cellar-Zweigs sass
    # und bei leerem Cellar-Ergebnis gar nicht erreicht wurde.
    #
    # Die Pruefung greift nur bei UNVERAENDERTER Quelle: wurde `text_url` in
    # regulations.py bewusst umgestellt, ist ein Groessensprung nach unten
    # gewollt (z. B. Gesamtausgabe -> Einzelvorschrift) und wird zugelassen.
    cached_text = (row["text"] if row else "") or ""
    same_source = bool(row) and (row["url"] or "") == url
    if cached_text.strip() and same_source:
        if not text.strip():
            print(f"[fetch] {reg['key']}: Abruf ohne Text — Cache-Stand behalten", flush=True)
            return _cached_result(
                row, resp.status_code,
                "Abruf lieferte keinen Text (Primaerquelle und Fallback leer) — "
                "bisheriger Cache-Stand behalten")
        if len(text) < len(cached_text) * _MIN_KEEP_RATIO:
            share = 100 * len(text) / max(len(cached_text), 1)
            print(f"[fetch] {reg['key']}: Abruf nur {share:.0f}% des bisherigen "
                  f"Umfangs — Cache-Stand behalten", flush=True)
            return _cached_result(
                row, resp.status_code,
                f"Abruf lieferte nur {len(text)} statt bisher {len(cached_text)} Zeichen "
                f"({share:.0f}%) — bisheriger Cache-Stand behalten. Bei absichtlicher "
                f"Quellenaenderung den Cache-Eintrag loeschen.")
    if not text.strip():
        # Kein Cache vorhanden und nichts geladen: keinen Leereintrag anlegen,
        # sonst gilt beim naechsten Lauf ein leerer Text als "Bestand".
        return _cached_result(
            row, resp.status_code,
            "Abruf lieferte keinen Text (Primaerquelle und Fallback leer)")

    # Nach einem Fallback duerfen ETag/Last-Modified der Challenge-Antwort nicht
    # gespeichert werden — sonst quittiert EUR-Lex den naechsten Lauf mit 304.
    etag = "" if used_fallback else (resp.headers.get("etag") or "")
    last_mod = "" if used_fallback else (resp.headers.get("last-modified") or "")
    # Siehe Kommentar bei SOURCE_STATUS_BASE_ACT_OFFSET.
    source_status = -resp.status_code if used_fallback else resp.status_code
    if base_act_only:
        source_status += SOURCE_STATUS_BASE_ACT_OFFSET
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute(
            """
            INSERT INTO law_texts (reg_key, language, url, text, etag, last_modified,
                                   fetched_at, source_status, source_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(reg_key, language) DO UPDATE SET
                url=excluded.url,
                text=excluded.text,
                etag=excluded.etag,
                last_modified=excluded.last_modified,
                fetched_at=excluded.fetched_at,
                source_status=excluded.source_status,
                source_note=excluded.source_note
            """,
            (reg["key"], language, url, text, etag, last_mod, now, source_status, source_note),
        )
        version_new, previous_hash = _record_version(c, reg["key"], language, url, text, now)

    return {"text": text, "fetched_at": now, "is_new": True,
            "error": ("Nur Basisrechtsakt geladen — spaetere Aenderungen fehlen"
                      if base_act_only else None),
            "status": resp.status_code,
            "text_hash": text_hash(text) if text.strip() else None,
            "version_new": version_new, "previous_hash": previous_hash,
            "source_note": source_note, "base_act_only": base_act_only}


def get_cached_text(reg_key: str, language: str = "de") -> dict | None:
    init_fetcher()
    with _conn() as c:
        row = c.execute(
            "SELECT text, fetched_at, last_modified, source_status, source_note "
            "FROM law_texts WHERE reg_key = ? AND language = ?",
            (reg_key, language),
        ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Generisches Fetching beliebiger URLs (z.B. Guidelines)
# ---------------------------------------------------------------------------
import hashlib as _hashlib


def _guideline_key(url: str) -> str:
    """Stabile Cache-Key fuer beliebige URLs (teilt sich die `law_texts`-Tabelle)."""
    return "GUIDE:" + _hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]


def fetch_url_text(url: str, *, language: str = "de", force: bool = False,
                    timeout: float = 30.0) -> dict:
    """Laedt eine beliebige URL (HTML/PDF), cached sie in der `law_texts`-Tabelle.

    Rueckgabe wie bei `fetch_law_text`:
        {text, fetched_at, last_modified, is_new, error, status}.

    Wird u.a. fuer Guidelines verwendet. Nutzt den gleichen ETag/Last-Modified-
    Mechanismus, damit Wiederholungs-Fetches billig bleiben.

    `timeout` (Sekunden) laesst sich fuer sekundaere Quellen (z.B. Guidelines)
    kuerzen, damit ein einzelner langsamer Server nicht die ganze Analyse blockt.
    """
    init_fetcher()
    cache_key = _guideline_key(url)
    with _conn() as c:
        row = c.execute(
            "SELECT text, etag, last_modified, fetched_at FROM law_texts "
            "WHERE reg_key = ? AND language = ?",
            (cache_key, language),
        ).fetchone()

    headers = {"User-Agent": USER_AGENT, "Accept-Language": _accept_language(language)}
    if row and not force:
        if row["etag"]:
            headers["If-None-Match"] = row["etag"]
        if row["last_modified"]:
            headers["If-Modified-Since"] = row["last_modified"]

    try:
        with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
            resp = client.get(url)
    except Exception as e:  # noqa: BLE001
        if row:
            return {"text": row["text"], "fetched_at": row["fetched_at"],
                    "last_modified": row["last_modified"], "is_new": False,
                    "error": str(e), "status": -1}
        return {"text": "", "fetched_at": None, "last_modified": None,
                "is_new": False, "error": str(e), "status": -1}

    if resp.status_code == 304 and row:
        return {"text": row["text"], "fetched_at": row["fetched_at"],
                "last_modified": row["last_modified"], "is_new": False,
                "error": None, "status": 304}

    if resp.status_code >= 400:
        if row:
            return {"text": row["text"], "fetched_at": row["fetched_at"],
                    "last_modified": row["last_modified"], "is_new": False,
                    "error": f"HTTP {resp.status_code}", "status": resp.status_code}
        return {"text": "", "fetched_at": None, "last_modified": None,
                "is_new": False, "error": f"HTTP {resp.status_code}", "status": resp.status_code}

    content_type = (resp.headers.get("content-type") or "").lower()
    if "pdf" in content_type or url.lower().endswith(".pdf"):
        text = _extract_pdf(resp.content)
    else:
        text = _extract_html(resp.text)

    text = text[:_store_limit()]

    etag = resp.headers.get("etag") or ""
    last_mod = resp.headers.get("last-modified") or ""
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute(
            """
            INSERT INTO law_texts (reg_key, language, url, text, etag, last_modified, fetched_at, source_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(reg_key, language) DO UPDATE SET
                url=excluded.url,
                text=excluded.text,
                etag=excluded.etag,
                last_modified=excluded.last_modified,
                fetched_at=excluded.fetched_at,
                source_status=excluded.source_status
            """,
            (cache_key, language, url, text, etag, last_mod, now, resp.status_code),
        )

    return {"text": text, "fetched_at": now, "last_modified": last_mod,
            "is_new": True, "error": None, "status": resp.status_code}


def get_cached_url_text(url: str, language: str = "de") -> dict | None:
    """Cache-Lookup fuer eine durch `fetch_url_text` geladene URL."""
    init_fetcher()
    cache_key = _guideline_key(url)
    with _conn() as c:
        row = c.execute(
            "SELECT text, fetched_at, last_modified FROM law_texts "
            "WHERE reg_key = ? AND language = ?",
            (cache_key, language),
        ).fetchone()
    return dict(row) if row else None
