# -*- coding: utf-8 -*-
"""Woechentliche Linkpruefung mit Ersatzsuche und Mail an den Admin.

Prueft alle Links aus `regulations.py` (Rechtsquellen, Volltextquellen,
Leitlinien) mit derselben Logik wie `check_links.py`, sucht fuer jeden
defekten Link eine Ersatzadresse, speichert das Ergebnis in `link_checks`
(sichtbar auf /admin/regulierungs-status) und schickt eine Mail, sobald
etwas defekt ist — und einmal Entwarnung, wenn danach wieder alles geht.
Im ersten Lauf jedes Monats kommt ausserdem ein Lebenszeichen, wenn sonst
nichts zu melden ist; bleibt es aus, laeuft die Pruefung nicht.

**Nichts wird automatisch ersetzt.** Die Links stehen im Code
(`regulations.py`); eine falsche Fundstelle in einem Compliance-Werkzeug ist
schlimmer als eine tote. Die Vorschlaege sind gegengeprueft (erreichbar, und
bei der KI-Suche passt der Seiteninhalt zum Titel), uebernommen werden sie von
Hand.

Ersatzsuche, in dieser Reihenfolge:
  1. gesetze-im-internet.de: neues Kuerzel derselben Vorschrift aus der
     amtlichen Teilliste (Fall MPBetreibV: `mpbetreibv/` -> `mpbetreibv_2025/`),
     dann dieselbe Einzelnorm oder der Volltext (`BJNR…html`) darunter.
  2. KI-Suche: Gemini mit Google-Suche nach Titel und bisheriger Adresse.
     Gesendet wird nur Titel und Adresse des Links, nie Nutzerdaten.
     Abschaltbar mit `LINKCHECK_KI=0`.

Cron (montags nach dem Watchdog):
    45 3 * * 1 docker exec esg-ki-textil-mode python linkwaechter.py >> /var/log/esg-linkwaechter.log 2>&1

Von Hand:
    python linkwaechter.py --probe     # pruefen und anzeigen, nichts speichern, keine Mail
"""
from __future__ import annotations

import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit

from dotenv import load_dotenv

# VOR den Projekt-Importen: db.py liest `ESG_DB_PATH` beim Import.
load_dotenv(override=True)

import httpx  # noqa: E402

import db  # noqa: E402
import mailer  # noqa: E402
from check_links import HEADERS, TIMEOUT, Result, check, collect  # noqa: E402

# Nutzervorgabe 12.10.2026: Mail an Michael Schuckert. Bewusst eine eigene
# Angabe statt `app.ADMIN_EMAILS` — der Cron soll die Flask-App nicht laden.
EMPFAENGER = os.getenv("LINKCHECK_MAIL_TO", "mschuckert@textil-mode.de")
ADMIN_PFAD = "/esg/admin/regulierungs-status"
GII = "https://www.gesetze-im-internet.de/"


# ---------------------------------------------------------------------------
# Pruefen
# ---------------------------------------------------------------------------
def pruefen(items: list[tuple[str, str, str]] | None = None,
            pruefer=check) -> list[Result]:
    """Alle Links pruefen — schonend (3 parallel, kurze Pause je Abruf)."""
    items = collect() if items is None else items
    with httpx.Client(timeout=TIMEOUT, http2=False) as client:
        def run(it):
            url, where, label = it
            r = pruefer(url, where, label, client)
            time.sleep(0.4)
            return r
        with ThreadPoolExecutor(max_workers=3) as pool:
            return list(pool.map(run, items))


def _wesentlich_weitergeleitet(r: Result) -> bool:
    """Funktionierender Link, dessen Ziel sich wirklich verschoben hat.

    http->https, ein Schraegstrich am Ende oder angehaengte Parameter auf
    derselben Seite zaehlen nicht — sonst stuende jede zweite Behoerdenseite
    in der Liste.
    """
    if r.status != "OK" or not r.final_url:
        return False
    alt, neu = urlsplit(r.url), urlsplit(r.final_url)
    return (alt.netloc.removeprefix("www.") != neu.netloc.removeprefix("www.")
            or alt.path.rstrip("/") != neu.path.rstrip("/"))


# ---------------------------------------------------------------------------
# Einstufung: nur echte Fehler sind "defekt"
# ---------------------------------------------------------------------------
# Probelauf 12.10.2026: 10 von 109 Links "defekt", davon 8 Fehlalarme — ECHA
# und Legifrance sperren Server-Abrufe (403), Cellar hat REACH nicht als HTML,
# zwei Behoerdenseiten antworteten kurz mit 504. Jede Woche eine Mail mit
# acht Fehlalarmen liest niemand; deshalb:
#   gesperrt     (401/403/429, Bot-Schutz) -> unklar, "im Browser pruefen"
#   voruebergehend (5xx, keine Verbindung) -> nach kurzer Pause erneut; bleibt
#                  es dabei, unklar — und erst defekt, wenn derselbe Link auch
#                  im Lauf davor schon nicht erreichbar war
#   alles andere (404, 410, Fehlerseite)   -> defekt, sofort Mail
GESPERRT = "gesperrt"
VORUEBERGEHEND = "voruebergehend"
WIEDERHOLEN_NACH = float(os.getenv("LINKCHECK_RETRY_SEC", "30"))


def art_des_fehlers(r: Result) -> str | None:
    """`gesperrt`, `voruebergehend` oder None (echter Fehler)."""
    if r.http_status in (401, 403, 429) or "Bot-Schutz" in (r.note or ""):
        return GESPERRT
    if r.http_status is None or r.http_status >= 500:
        return VORUEBERGEHEND
    return None


def einstufen(ergebnisse: list[Result], vorher: dict | None, pruefer=check,
              warten: float = WIEDERHOLEN_NACH) -> tuple[list[Result], list[dict]]:
    """Teilt die BROKEN-Ergebnisse in echte Defekte und unklare Faelle.

    Rueckgabe: (defekte Results, unklare Eintraege fuer Speicherung/Anzeige).
    """
    vorher_weg = {u["url"] for u in (vorher or {}).get("unknown", [])
                  if u.get("kind") == VORUEBERGEHEND}
    vorher_weg |= {b["url"] for b in (vorher or {}).get("broken", [])}
    defekt: list[Result] = []
    unklar: list[dict] = [{"where": r.where, "label": r.label, "url": r.url, "note": r.note,
                           "kind": "unklar"} for r in ergebnisse if r.status == "UNKNOWN"]
    kaputt = [r for r in ergebnisse if r.status == "BROKEN"]
    nochmal = [r for r in kaputt if art_des_fehlers(r) == VORUEBERGEHEND]
    if nochmal and warten:
        time.sleep(warten)
    zweiter = {r.url: r for r in pruefen([(r.url, r.where, r.label) for r in nochmal], pruefer)}         if nochmal else {}
    for r in kaputt:
        art = art_des_fehlers(r)
        if art == VORUEBERGEHEND:
            r2 = zweiter.get(r.url, r)
            if r2.status != "BROKEN":
                continue                      # beim zweiten Versuch erreichbar
            art = art_des_fehlers(r2)
            r = r2
            if art == VORUEBERGEHEND and r.url in vorher_weg:
                r.note = f"seit mindestens einer Woche nicht erreichbar ({r.note})"
                defekt.append(r)
                continue
        if art == GESPERRT:
            unklar.append({"where": r.where, "label": r.label, "url": r.url, "kind": GESPERRT,
                           "note": f"Server-Abruf gesperrt, im Browser prüfen ({r.note})"})
        elif art == VORUEBERGEHEND:
            unklar.append({"where": r.where, "label": r.label, "url": r.url, "kind": VORUEBERGEHEND,
                           "note": f"vorübergehend nicht erreichbar ({r.note})"})
        else:
            defekt.append(r)
    return defekt, unklar


# ---------------------------------------------------------------------------
# Ersatzsuche 1: gesetze-im-internet.de
# ---------------------------------------------------------------------------
_GII_PATH = re.compile(r"^/([a-z0-9_\-]+)/([^/]*)$", re.I)
_TEILLISTE_HREF = re.compile(r'href="\./([a-z0-9_\-]+)/index\.html"', re.I)
_BJNR_HREF = re.compile(r'href="(BJNR[0-9A-Z]+\.html)"')
_JAHR_SUFFIX = re.compile(r"_(\d{4})$")


def _gii_kandidaten_kuerzel(alt: str, teilliste_html: str) -> list[str]:
    """Kuerzel aus der Teilliste, die die abgeloeste Vorschrift fortfuehren.

    `mpbetreibv` -> `mpbetreibv_2025`; `mpbetreibv_2025` -> `mpbetreibv_2031`.
    Juengste zuerst; das alte Kuerzel selbst nie.
    """
    def jahr(k: str) -> int:
        m = _JAHR_SUFFIX.search(k)
        return int(m.group(1)) if m else 0

    alt = alt.lower()
    stamm = _JAHR_SUFFIX.sub("", alt)
    gefunden = {k.lower() for k in _TEILLISTE_HREF.findall(teilliste_html)}
    treffer = [k for k in gefunden
               if k != alt and (k == stamm or (k.startswith(stamm + "_") and jahr(k)))
               # nie zurueck auf eine aeltere Fassung
               and jahr(k) > jahr(alt)]
    return sorted(treffer, key=jahr, reverse=True)


def gii_ersatz(url: str, client: httpx.Client, pruefer=check) -> list[dict]:
    teile = urlsplit(url)
    if teile.netloc.removeprefix("www.") != "gesetze-im-internet.de":
        return []
    m = _GII_PATH.match(teile.path)
    if not m:
        return []
    alt, datei = m.group(1), m.group(2)
    try:
        liste = client.get(f"{GII}Teilliste_{alt[0].upper()}.html", headers=HEADERS,
                           follow_redirects=True)
        liste_html = liste.content.decode("iso-8859-1", errors="replace")
    except Exception:                                       # noqa: BLE001
        return []
    out: list[dict] = []
    for neu in _gii_kandidaten_kuerzel(alt, liste_html)[:2]:
        ziele: list[str] = []
        # Dieselbe Einzelnorm unter dem neuen Kuerzel (z. B. __10a.html) —
        # der Volltext hat bei einer Neufassung eine neue BJNR-Nummer.
        if datei and not datei.startswith("BJNR") and datei != "index.html":
            ziele.append(f"{GII}{neu}/{datei}")
        try:
            index = client.get(f"{GII}{neu}/index.html", headers=HEADERS, follow_redirects=True)
            bjnr = _BJNR_HREF.search(index.content.decode("iso-8859-1", errors="replace"))
            if bjnr:
                ziele.append(urljoin(f"{GII}{neu}/", bjnr.group(1)))
        except Exception:                                   # noqa: BLE001
            pass
        for ziel in ziele:
            r = pruefer(ziel, "", "", client)
            if r.status == "OK":
                out.append({"url": ziel, "source": "gesetze-im-internet.de",
                            "note": f"neues Kürzel „{neu}“ in der amtlichen Gesetzesliste"})
                break
    return out


# ---------------------------------------------------------------------------
# Ersatzsuche 2: KI mit Google-Suche
# ---------------------------------------------------------------------------
_URL_IM_TEXT = re.compile(r"https?://[^\s<>\"')\]]+")
_STOPP = {"und", "der", "die", "das", "für", "fuer", "zur", "zum", "von", "mit", "über",
          "ueber", "the", "and", "for", "des", "den", "dem", "eine", "einer"}


def _woerter(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zäöüß0-9]{4,}", text.lower()) if w not in _STOPP}


def _inhalt_passt(label: str, client: httpx.Client, url: str) -> bool:
    """Mindestens die Haelfte der bedeutungstragenden Titelwoerter steht auf der Seite."""
    woerter = _woerter(label)
    if not woerter:
        return True
    try:
        seite = client.get(url, headers=HEADERS, follow_redirects=True).text[:60000].lower()
    except Exception:                                       # noqa: BLE001
        return False
    return sum(1 for w in woerter if w in seite) * 2 >= len(woerter)


def _gemini_suche(label: str, url: str) -> tuple[str, list[str]]:
    """(Antworttext, Quell-Adressen der Google-Suche). Leer, wenn nicht moeglich."""
    if os.getenv("LINKCHECK_KI", "1") == "0":
        return "", []
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if os.getenv("LLM_PROVIDER", "").lower() != "google" or not key:
        return "", []
    model = os.getenv("GOOGLE_MODEL") or os.getenv("OPENAI_MODEL", "gemini-2.5-flash")
    frage = (
        f"Die Webseite „{label}“ war bisher unter {url} erreichbar; die Adresse liefert jetzt "
        "einen Fehler. Suche die aktuelle offizielle Adresse genau dieser Seite oder ihres "
        "direkten Nachfolgers, bevorzugt auf derselben Website. Antworte nur mit bis zu drei "
        "vollständigen Adressen, eine pro Zeile, ohne weiteren Text."
    )
    body = {"contents": [{"role": "user", "parts": [{"text": frage}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.0, "maxOutputTokens": 400}}
    try:
        r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                       json=body, headers={"x-goog-api-key": key}, timeout=60)
        r.raise_for_status()
        kandidat = (r.json().get("candidates") or [{}])[0]
    except Exception as exc:                                # noqa: BLE001
        # Schluessel steht im Kopf, nicht in der Adresse — die Meldung ist unbedenklich.
        print(f"[linkwaechter] KI-Suche fuer {url}: {type(exc).__name__}", flush=True)
        return "", []
    text = "".join(p.get("text", "") for p in (kandidat.get("content") or {}).get("parts", []))
    quellen = [c.get("web", {}).get("uri", "")
               for c in (kandidat.get("groundingMetadata") or {}).get("groundingChunks", [])]
    return text, [q for q in quellen if q]


def ki_ersatz(url: str, label: str, client: httpx.Client, pruefer=check,
              suche=_gemini_suche) -> list[dict]:
    text, quellen = suche(label, url)
    kandidaten: list[str] = [u.rstrip(".,;") for u in _URL_IM_TEXT.findall(text)]
    # Die Quellen der Google-Suche sind Weiterleitungen (vertexaisearch…) — Ziel aufloesen.
    for q in quellen:
        try:
            kandidaten.append(str(client.get(q, headers=HEADERS, follow_redirects=True).url))
        except Exception:                                   # noqa: BLE001
            continue
    out: list[dict] = []
    gesehen = {url.rstrip("/")}
    for k in kandidaten:
        if k.rstrip("/") in gesehen or "vertexaisearch" in k:
            continue
        gesehen.add(k.rstrip("/"))
        r = pruefer(k, "", label, client)
        if r.status != "OK":
            continue
        passt = _inhalt_passt(label, client, r.final_url or k)
        out.append({"url": r.final_url or k, "source": "KI-Suche",
                    "note": "erreichbar, Inhalt passt zum Titel" if passt
                    else "erreichbar, Inhalt bitte prüfen"})
        if len(out) >= 2:
            break
    # Treffer mit passendem Inhalt zuerst
    return sorted(out, key=lambda s: "prüfen" in s["note"])


def ersatz_suchen(r: Result, client: httpx.Client, pruefer=check, suche=_gemini_suche) -> list[dict]:
    vorschlaege = gii_ersatz(r.url, client, pruefer)
    if not vorschlaege:
        vorschlaege = ki_ersatz(r.url, r.label, client, pruefer, suche)
    return vorschlaege


# ---------------------------------------------------------------------------
# Bericht und Mail
# ---------------------------------------------------------------------------
def _wo(where: str, label: str) -> str:
    """`REGULATIONS[MPDG].url` -> „MPDG – Gesetzeslink“ usw., lesbar fuer die Mail."""
    m = re.match(r"REGULATIONS\[(.+)\]\.(url|text_url)", where)
    if m:
        art = "Link in Liste und Karte" if m.group(2) == "url" else "Volltextquelle"
        return f"{m.group(1)} – {art}"
    m = re.match(r"GUIDELINES\[(.+)\]", where)
    if m:
        return f"{m.group(1)} – Leitlinie „{label}“"
    return where or label


def mail_defekt(lauf: dict) -> tuple[str, str]:
    defekt = lauf["broken"]
    betreff = (f"ESG-Check: {len(defekt)} defekter Link" if len(defekt) == 1
               else f"ESG-Check: {len(defekt)} defekte Links")
    zeilen = [
        "Hallo,",
        "",
        f"die wöchentliche Linkprüfung des ESG-Regulierungs-Checks hat {lauf['checked']} Links "
        f"geprüft; {len(defekt)} davon funktionieren nicht mehr.",
        "",
    ]
    for i, b in enumerate(defekt, 1):
        zeilen += [f"{i}. {_wo(b['where'], b['label'])}",
                   f"   Adresse: {b['url']}",
                   f"   Fehler:  {b['note']}"]
        if b.get("suggestions"):
            for s in b["suggestions"]:
                zeilen.append(f"   Vorschlag ({s['source']}, {s['note']}):")
                zeilen.append(f"   {s['url']}")
        else:
            zeilen.append("   Vorschlag: keine Ersatzadresse gefunden – bitte von Hand suchen.")
        zeilen.append("")
    if lauf["unknown"]:
        zeilen += [f"Nicht mitgezählt: {len(lauf['unknown'])} unklare Fälle (Seiten, die "
                   "automatische Abrufe sperren, oder kurze Störungen) – Einzelheiten auf der "
                   "Admin-Seite.", ""]
    zeilen += [
        "Übernommen wird nichts automatisch: Die Links stehen in regulations.py. Vorschlag "
        "prüfen und dort eintragen – oder Claude Code mit dem Text dieser Mail beauftragen.",
        "",
        f"Admin-Seite: {_admin_link()}",
        "",
        "Diese Nachricht kommt jede Woche, solange ein Link defekt ist.",
    ]
    return betreff, "\n".join(zeilen)


def mail_entwarnung(lauf: dict) -> tuple[str, str]:
    return ("ESG-Check: alle Links wieder erreichbar",
            "Hallo,\n\n"
            f"bei der heutigen Linkprüfung waren alle {lauf['checked']} Links erreichbar. "
            "Die zuletzt gemeldeten Fehler sind damit erledigt.\n\n"
            f"Admin-Seite: {_admin_link()}\n")


def mail_lebenszeichen(lauf: dict) -> tuple[str, str]:
    """Monatliche Bestaetigung, dass die Pruefung laeuft (Nutzerwunsch 12.10.2026).

    Ohne sie hiesse Stille zweierlei: alles in Ordnung — oder die Pruefung
    lief gar nicht (Container, Cron oder Mailversand ausgefallen). Bleibt diese
    Mail am Monatsanfang aus, klemmt etwas.
    """
    unklar = (f" {len(lauf['unknown'])} Seiten sperren automatische Abrufe oder waren kurz "
              "gestört; sie zählen nicht als defekt und stehen auf der Admin-Seite."
              if lauf["unknown"] else "")
    return ("ESG-Check: Linkprüfung läuft – alles in Ordnung",
            "Hallo,\n\n"
            "dies ist das monatliche Lebenszeichen der wöchentlichen Linkprüfung des "
            f"ESG-Regulierungs-Checks: {lauf['checked']} Links geprüft, keiner defekt.{unklar}\n\n"
            "Bleibt diese Nachricht am Anfang eines Monats aus, läuft die Prüfung nicht mehr "
            "(Container, Cron-Eintrag oder Mailversand auf dem Server prüfen).\n\n"
            f"Admin-Seite: {_admin_link()}\n")


def _admin_link() -> str:
    basis = (os.environ.get("PUBLIC_BASE_URL") or "").rstrip("/")
    return f"{basis}{ADMIN_PFAD}" if basis else ADMIN_PFAD


def _senden(betreff: str, text: str, versand=None) -> None:
    if versand is not None:
        versand(EMPFAENGER, betreff, text)
        return
    if not mailer.is_configured():
        print("[linkwaechter] kein Mailversand konfiguriert — Bericht nur gespeichert", flush=True)
        return
    try:
        mid = mailer.send(EMPFAENGER, betreff, text)
        db.log_mail(EMPFAENGER, "link_check", "sent", message_id=mid)
    except Exception as exc:                                # noqa: BLE001
        db.log_mail(EMPFAENGER, "link_check", "failed", error=str(exc)[:300])
        print(f"[linkwaechter] Mail fehlgeschlagen: {exc}", flush=True)


# ---------------------------------------------------------------------------
def lauf(items=None, pruefer=check, suche=_gemini_suche, versand=None,
         speichern: bool = True, warten: float = WIEDERHOLEN_NACH) -> dict:
    """Ein kompletter Durchgang. Parameter erlauben Attrappen im Test."""
    db.init_db()
    gestartet = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    vorher = db.latest_link_check()
    ergebnisse = pruefen(items, pruefer)
    echte, unklar = einstufen(ergebnisse, vorher, pruefer, warten)

    defekt: list[dict] = []
    with httpx.Client(timeout=TIMEOUT, http2=False) as client:
        for r in echte:
            defekt.append({"where": r.where, "label": r.label, "url": r.url, "note": r.note,
                           "http_status": r.http_status,
                           "suggestions": ersatz_suchen(r, client, pruefer, suche)})
    weiter = [{"where": r.where, "label": r.label, "url": r.url, "final_url": r.final_url}
              for r in ergebnisse if _wesentlich_weitergeleitet(r)]
    bericht = {"checked": len(ergebnisse), "broken": defekt, "unknown": unklar,
               "redirected": weiter}
    if not speichern:
        return bericht

    db.save_link_check(gestartet, len(ergebnisse), defekt, unklar, weiter)
    # Erster Lauf eines Kalendermonats (auch nach einem Ausfall): Lebenszeichen,
    # wenn es nichts anderes zu melden gibt — jede Mail ist zugleich eines.
    neuer_monat = not vorher or (vorher.get("started_at") or "")[:7] != gestartet[:7]
    if defekt:
        _senden(*mail_defekt(bericht), versand=versand)
    elif vorher and vorher.get("broken"):
        _senden(*mail_entwarnung(bericht), versand=versand)
    elif neuer_monat:
        _senden(*mail_lebenszeichen(bericht), versand=versand)
    return bericht


def main(argv: list[str]) -> int:
    probe = "--probe" in argv
    start = datetime.now()
    bericht = lauf(speichern=not probe)
    print(f"[linkwaechter] {datetime.now():%d.%m.%Y %H:%M} in {(datetime.now() - start).seconds}s: "
          f"{bericht['checked']} geprueft, {len(bericht['broken'])} defekt, "
          f"{len(bericht['unknown'])} unklar, {len(bericht['redirected'])} weitergeleitet",
          flush=True)
    for b in bericht["broken"]:
        print(f"  DEFEKT {b['where']}: {b['url']} ({b['note']})")
        for s in b["suggestions"]:
            print(f"         -> {s['url']}  [{s['source']}: {s['note']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
