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
from datetime import datetime
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

from db import DB_PATH


USER_AGENT = "ESG-Regulierungs-Check/1.0 (+https://localhost)"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
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

# Prozess-Cache: pro Lauf wird jede CELEX-ID hoechstens einmal aufgeloest.
_consolidated_cache: dict[str, str] = {}


def _base_act_celex(celex: str) -> str:
    """`02024L1760` → `32024L1760` (Basisrechtsakt, immer in Cellar vorhanden)."""
    m = _UNDATED_CONSOLIDATED.match(celex)
    return f"3{m.group(1)}" if m else celex


def _latest_consolidated(celex: str, timeout: float) -> str:
    """Juengste konsolidierte Fassung zu einer datumslosen `0…`-CELEX-ID.

    Rueckgabe: `02024L1760-20260318`, oder der Basisrechtsakt (`32024L1760`),
    wenn es keine konsolidierte Fassung gibt oder der Endpunkt nicht antwortet.
    Damit bleibt der Abruf auch ohne SPARQL funktionsfaehig — nur eben auf der
    Ursprungsfassung.
    """
    if celex in _consolidated_cache:
        return _consolidated_cache[celex]
    query = (
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n"
        "SELECT ?celex WHERE {\n"
        "  ?w cdm:resource_legal_id_celex ?celex .\n"
        f'  FILTER(STRSTARTS(STR(?celex), "{celex}-"))\n'
        "}\nORDER BY DESC(?celex) LIMIT 1"
    )
    resolved = _base_act_celex(celex)
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True,
                          headers={"User-Agent": USER_AGENT,
                                   "Accept": "application/sparql-results+json"}) as client:
            resp = client.get(_SPARQL_URL, params={
                "query": query, "format": "application/sparql-results+json"})
        if resp.status_code < 400:
            bindings = resp.json().get("results", {}).get("bindings", [])
            if bindings:
                value = (bindings[0].get("celex") or {}).get("value") or ""
                if _DATED_CELEX.match(value):
                    resolved = value
    except Exception as e:  # noqa: BLE001
        print(f"[cellar] Konsolidierungssuche {celex} fehlgeschlagen: {e}", flush=True)
    _consolidated_cache[celex] = resolved
    return resolved


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


def _cellar_text(url: str, language: str, timeout: float) -> str:
    """Volltext ueber publications.europa.eu zur CELEX-ID in `url`, sonst ''.

    Bei datumsloser konsolidierter ID wird zuerst die juengste konsolidierte
    Fassung versucht, danach der Basisrechtsakt — so bleibt der Abruf auch dann
    erfolgreich, wenn zu einem Rechtsakt (noch) keine Konsolidierung vorliegt.
    """
    celex = _celex_id(url)
    if not celex:
        return ""
    candidates = [celex]
    if _UNDATED_CONSOLIDATED.match(celex):
        candidates = [_latest_consolidated(celex, timeout), _base_act_celex(celex)]
    for cand in dict.fromkeys(candidates):
        text = _cellar_fetch(cand, language, timeout)
        if text:
            return text
    return ""


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
    }


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
            "SELECT text, etag, last_modified, fetched_at FROM law_texts "
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
    # Genau ein Fallback-Versuch — Phase 1 laeuft sequenziell ueber alle 22
    # Regulierungen, ein zweiter Anlauf koennte pro Reg 60 s zusaetzlich kosten.
    used_fallback = False
    if len(text.strip()) < 2000 and "eur-lex.europa.eu" in url:
        alt = _cellar_text(url, language, 60.0)
        if len(alt) > len(text):
            text = alt
            used_fallback = True

    if resp.status_code >= 400 and not text:
        return _cached_result(row, resp.status_code, f"HTTP {resp.status_code}")

    text = text[:_store_limit()]

    # Nach einem Fallback duerfen ETag/Last-Modified der Challenge-Antwort nicht
    # gespeichert werden — sonst quittiert EUR-Lex den naechsten Lauf mit 304.
    etag = "" if used_fallback else (resp.headers.get("etag") or "")
    last_mod = "" if used_fallback else (resp.headers.get("last-modified") or "")
    # Negatives source_status = Text kam nicht von der Primaerquelle, sondern
    # aus dem Fallback; der Betrag ist der Statuscode der Primaerantwort
    # (z. B. -202 = WAF-Challenge von EUR-Lex, Text vom Amt fuer
    # Veroeffentlichungen).
    source_status = -resp.status_code if used_fallback else resp.status_code
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
            (reg["key"], language, url, text, etag, last_mod, now, source_status),
        )
        version_new, previous_hash = _record_version(c, reg["key"], language, url, text, now)

    return {"text": text, "fetched_at": now, "is_new": True, "error": None,
            "status": resp.status_code,
            "text_hash": text_hash(text) if text.strip() else None,
            "version_new": version_new, "previous_hash": previous_hash}


def get_cached_text(reg_key: str, language: str = "de") -> dict | None:
    init_fetcher()
    with _conn() as c:
        row = c.execute(
            "SELECT text, fetched_at, last_modified FROM law_texts WHERE reg_key = ? AND language = ?",
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
