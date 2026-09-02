"""Prueft alle in `regulations.py` hinterlegten externen Links auf Erreichbarkeit.

Aufruf:
    .venv\\Scripts\\python.exe check_links.py            # alles
    .venv\\Scripts\\python.exe check_links.py --only guidelines
    .venv\\Scripts\\python.exe check_links.py --json bericht.json

Geprueft werden drei Gruppen:
  * ``REGULATIONS[*]["url"]``       — verlinkte Rechtsquelle (Liste + Ergebniskarten)
  * ``REGULATIONS[*]["text_url"]``  — Volltextquelle fuer die Analyse
  * ``GUIDELINES_BY_REG_KEY``       — kuratierte Leitlinien (Liste + "Erste Schritte")

Besonderheiten, die das Skript kennt:
  * **EUR-Lex** blockt Server-Abrufe mit einer AWS-WAF-Challenge (HTTP 202 oder
    403 bei leerem Body). Das ist KEIN kaputter Link. Solche URLs werden ueber
    ``publications.europa.eu/resource/celex/<CELEX>`` gegengeprueft — genau den
    Weg nutzt auch ``fetcher._cellar_text``.
  * Behoerdenseiten liefern "Seite nicht gefunden" haeufig mit HTTP 200 aus.
    Deshalb wird der Seitentext zusaetzlich auf Fehlerfloskeln abgeklopft.

Der Exit-Code ist 1, sobald mindestens ein Link als ``BROKEN`` gilt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict

import httpx

from regulations import REGULATIONS, GUIDELINES_BY_REG_KEY

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
TIMEOUT = httpx.Timeout(45.0, connect=20.0)

# Floskeln, die eine als HTTP 200 ausgelieferte Fehlerseite verraten.
ERROR_PHRASES = [
    "seite nicht gefunden",
    "seite konnte nicht gefunden werden",
    "page not found",
    "page cannot be found",
    "the requested page could not be found",
    "404 - not found",
    "fehler 404",
    "error 404",
    "diese seite existiert nicht",
    "no longer available",
    "nicht mehr verfuegbar",
    "document does not exist",
    "sorry, the page you are looking for",
]

# Der Doppelpunkt steht roh (`CELEX:…`) oder prozentkodiert (`CELEX%3A…`) da.
# Die Alternativen muessen einzeln stehen: eine Zeichenklasse `[%3A:]` wuerde
# auch die fuehrende `3` einer Ursprungsakt-ID (`32024R3005`) verschlucken.
CELEX_RE = re.compile(r"CELEX(?:%3A|:)([0-9A-Z()]+)", re.I)
ELI_RE = re.compile(r"eur-lex\.europa\.eu/eli/(\w+)/(\d{4})/(\d+)/oj", re.I)

# Datumslose konsolidierte CELEX-ID, z. B. 02024L1760 (ohne "-20260318").
# Cellar loest die nicht auf; die juengste Fassung ermittelt derselbe
# SPARQL-Weg, den auch die Anwendung nutzt — deshalb aus fetcher importiert,
# statt die Logik hier ein zweites Mal zu pflegen.
UNDATED_CONSOLIDATED = re.compile(r"^0\d{4}[LRD]\d{4}$", re.I)
from fetcher import _latest_consolidated, RESOLVE_CONSOLIDATED  # noqa: E402


@dataclass
class Result:
    url: str
    where: str
    label: str
    status: str          # OK | OK_VIA_CELLAR | BROKEN | UNKNOWN
    http_status: int | None
    final_url: str | None
    content_type: str | None
    length: int | None
    note: str = ""


def _text_of(resp: httpx.Response) -> str:
    ctype = (resp.headers.get("content-type") or "").lower()
    if "pdf" in ctype or "octet-stream" in ctype:
        return ""
    try:
        return resp.text[:20000].lower()
    except Exception:
        return ""


def _celex_of(url: str) -> str | None:
    m = CELEX_RE.search(url)
    if m:
        return m.group(1)
    m = ELI_RE.search(url)
    if m:
        kind, year, num = m.groups()
        # ELI-Kurzform -> CELEX des Basisrechtsakts (3<Jahr><L|R><4-stellige Nr.>)
        letter = {"reg": "R", "dir": "L", "dec": "D"}.get(kind.lower())
        if letter:
            return f"3{year}{letter}{int(num):04d}"
    return None


def _check_cellar(celex: str, client: httpx.Client) -> tuple[bool, str]:
    """Gegenprobe ueber publications.europa.eu — derselbe Weg wie fetcher._cellar_text.

    Eine datumslose konsolidierte ID (`02024L1760`) liefert in Cellar 404; die
    juengste datierte Fassung wird deshalb — genau wie in `fetcher` — per SPARQL
    aufgeloest, bevor abgerufen wird.
    """
    resolved = celex
    if UNDATED_CONSOLIDATED.match(celex):
        resolved, kind = _latest_consolidated(celex)
        if kind != RESOLVE_CONSOLIDATED:
            return False, (f"Konsolidierung zu {celex} nicht aufloesbar "
                           f"(SPARQL); Basisakt {resolved} wird geprueft")
    target = f"https://publications.europa.eu/resource/celex/{resolved}"
    for accept in ("text/html", "application/xhtml+xml", "text/plain"):
        try:
            r = client.get(
                target,
                headers={**HEADERS, "Accept": accept,
                         "Accept-Language": "eng, deu, fra"},
                follow_redirects=True,
            )
        except Exception as exc:  # noqa: BLE001
            return False, f"Cellar-Fehler: {type(exc).__name__}"
        if r.status_code == 200 and len(r.content) > 2000:
            return True, (f"Cellar-Gegenprobe OK ({celex}, {len(r.content)} Bytes, "
                          f"{r.headers.get('content-type', '?')})")
    return False, f"Cellar-Gegenprobe fehlgeschlagen ({celex}, HTTP {r.status_code})"


def check(url: str, where: str, label: str, client: httpx.Client) -> Result:
    try:
        resp = client.get(url, headers=HEADERS, follow_redirects=True)
    except Exception as exc:  # noqa: BLE001
        return Result(url, where, label, "BROKEN", None, None, None, None,
                      f"Verbindungsfehler: {type(exc).__name__}: {exc}")

    ctype = resp.headers.get("content-type")
    final = str(resp.url)
    length = len(resp.content)
    body = _text_of(resp)

    # --- EUR-Lex-Bot-Schutz -------------------------------------------------
    is_eurlex = "eur-lex.europa.eu" in url
    waf = resp.status_code in (202, 403) or (
        is_eurlex and length < 4000 and "awswaf" in body
    )
    if is_eurlex and waf:
        celex = _celex_of(url)
        if celex:
            ok, note = _check_cellar(celex, client)
            return Result(url, where, label, "OK_VIA_CELLAR" if ok else "BROKEN",
                          resp.status_code, final, ctype, length,
                          f"EUR-Lex-Bot-Schutz (HTTP {resp.status_code}). {note}")
        return Result(url, where, label, "UNKNOWN", resp.status_code, final,
                      ctype, length, "EUR-Lex-Bot-Schutz, kein CELEX ableitbar")

    if resp.status_code >= 400:
        return Result(url, where, label, "BROKEN", resp.status_code, final,
                      ctype, length, f"HTTP {resp.status_code}")

    # --- als 200 getarnte Fehlerseiten --------------------------------------
    hit = next((p for p in ERROR_PHRASES if p in body), None)
    if hit:
        return Result(url, where, label, "BROKEN", resp.status_code, final,
                      ctype, length, f"Fehlerseite trotz HTTP 200 (Fund: '{hit}')")

    if length < 800 and "pdf" not in (ctype or ""):
        return Result(url, where, label, "UNKNOWN", resp.status_code, final,
                      ctype, length, "verdaechtig kurze Antwort")

    note = ""
    if final.rstrip("/") != url.rstrip("/"):
        note = f"weitergeleitet auf {final}"
    if is_eurlex and celex_ok(body):
        note = (note + "; " if note else "") + "EUR-Lex-Inhalt erkannt"
    return Result(url, where, label, "OK", resp.status_code, final, ctype,
                  length, note)


def celex_ok(body: str) -> bool:
    return "eur-lex" in body and ("official journal" in body or "amtsblatt" in body
                                  or "document" in body)


def collect() -> list[tuple[str, str, str]]:
    """(url, wo, label) fuer alle hinterlegten Links."""
    items: list[tuple[str, str, str]] = []
    for reg in REGULATIONS:
        key = reg.get("key") or reg.get("name", "?")
        if reg.get("url"):
            items.append((reg["url"], f"REGULATIONS[{key}].url", key))
        if reg.get("text_url") and reg.get("text_url") != reg.get("url"):
            items.append((reg["text_url"], f"REGULATIONS[{key}].text_url", key))
    for key, guides in GUIDELINES_BY_REG_KEY.items():
        for g in guides:
            items.append((g["url"], f"GUIDELINES[{key}]", g["name"]))
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["regulations", "guidelines"], default=None)
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--workers", type=int, default=3,
                    help="parallele Abrufe (klein halten, Server schonen)")
    args = ap.parse_args()

    items = collect()
    if args.only == "regulations":
        items = [i for i in items if i[1].startswith("REGULATIONS")]
    elif args.only == "guidelines":
        items = [i for i in items if i[1].startswith("GUIDELINES")]

    results: list[Result] = []
    with httpx.Client(timeout=TIMEOUT, http2=False) as client:
        def run(it):
            url, where, label = it
            r = check(url, where, label, client)
            time.sleep(0.4)  # Server nicht ueberfahren
            return r

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for r in pool.map(run, items):
                results.append(r)
                print(f"{r.status:14s} {r.http_status or '-':>4}  {r.where}\n"
                      f"{'':19s} {r.url}"
                      + (f"\n{'':19s} -> {r.note}" if r.note else ""),
                      flush=True)

    broken = [r for r in results if r.status == "BROKEN"]
    unknown = [r for r in results if r.status == "UNKNOWN"]
    print("\n" + "=" * 70)
    print(f"geprueft: {len(results)} | ok: {len(results) - len(broken) - len(unknown)}"
          f" | defekt: {len(broken)} | unklar: {len(unknown)}")
    for r in broken:
        print(f"  DEFEKT  {r.where}: {r.url}  ({r.note})")
    for r in unknown:
        print(f"  UNKLAR  {r.where}: {r.url}  ({r.note})")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump([asdict(r) for r in results], fh, ensure_ascii=False, indent=2)

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
