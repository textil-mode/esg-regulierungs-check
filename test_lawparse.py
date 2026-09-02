"""Tests fuer die Gesetzestext-Quellen und lawparse.build_context.

Ausfuehren:  ./.venv/Scripts/python.exe test_lawparse.py
             ./.venv/Scripts/python.exe test_lawparse.py --keep   (Cache behalten)

Die Test-DB `data/esg_lawparse_test.db` wird standardmaessig VERWORFEN und neu
aufgebaut: alle 20 Quellen werden frisch geladen. Nur so faellt auf, wenn eine
`text_url` wieder auf eine Inhaltsverzeichnis- oder Portalseite zeigt — ein
mitgeschleppter Cache aus einem frueheren Lauf wuerde genau das verdecken.
Ein voller Lauf dauert dadurch rund eine Minute. Mit `--keep` bleibt die Test-DB
erhalten (schnelle Wiederholung waehrend der Entwicklung an lawparse selbst).

Die Produktiv-DB `data/esg.db` wird nie beschrieben (`data/` steht in
.gitignore).

Abnahmekriterien:
  * jede der 20 Quellen liefert echten Volltext (Mindestlaenge + Artikelstruktur),
  * die fuenf reparierten Quellen liefern nachweislich den RICHTIGEN Rechtsakt,
  * fuer CSDDD, CSRD und EUDR enthaelt der gebaute Kontext den
    Anwendungsbereichs-Artikel, und die Gesamtlaenge bleibt unter dem Budget.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DIR = BASE / "data"
TEST_DB = TEST_DIR / "esg_lawparse_test.db"

# Live laeuft FULLTEXT_MAX_CHARS=25000 — dagegen wird getestet.
BUDGET = 25000

# Unter dieser Laenge ist es kein Gesetzestext, sondern eine Uebersichts-,
# Inhaltsverzeichnis- oder Portalseite. Die kaputten Quellen lagen vor der
# Reparatur bei 556 / 767 / 2 365 / 10 772 Zeichen.
MIN_CHARS = 8000
MIN_SECTIONS = 3

KEEP_CACHE = "--keep" in sys.argv

import fetcher  # noqa: E402
import lawparse  # noqa: E402
from regulations import REGULATIONS  # noqa: E402


def _setup_db() -> None:
    """Test-DB frisch anlegen und den Fetcher darauf umbiegen."""
    TEST_DIR.mkdir(exist_ok=True)
    if TEST_DB.exists() and not KEEP_CACHE:
        TEST_DB.unlink()
    # Voller Text, nicht auf das LLM-Budget gekappt.
    os.environ.setdefault("LAW_TEXT_MAX_CHARS", "400000")
    fetcher.DB_PATH = TEST_DB
    fetcher.init_fetcher()


# Beim Import ausfuehren, nicht erst unter __main__: sonst wuerde ein
# versehentlicher pytest-Lauf (die Datei heisst test_*) mit fetcher.DB_PATH auf
# data/esg.db laufen und _law_text() per force=True in die echte lokale DB
# schreiben.
_setup_db()


def _law_text(reg: dict, language: str = "de") -> str:
    cached = fetcher.get_cached_text(reg["key"], language) or {}
    text = cached.get("text") or ""
    if len(text) < MIN_CHARS:
        # Kein brauchbarer Cache -> frisch laden (schreibt nur in die Test-DB).
        text = fetcher.fetch_law_text(reg, language=language, force=True).get("text") or ""
    return text


def _reg(key: str) -> dict:
    return next(r for r in REGULATIONS if r["key"] == key)


def _old_context(reg: dict, law_text: str, budget: int) -> str:
    """Bisheriges Verhalten: konkatenieren und vorn abschneiden."""
    head = f"=== GESETZESTEXT: {reg.get('full_name') or reg['name']} ==="
    return "\n".join([head, law_text])[:budget]


# Charakteristische Passagen der Anwendungsbereichs-Artikel (DE-Fassung).
SCOPE_MARKERS = {
    "CSDDD": ["Geltungsbereich", "Diese Richtlinie gilt für Unternehmen",
              "weltweiten Nettoumsatz"],
    "CSRD":  ["Konsolidierte Nachhaltigkeitsberichterstattung", "Große Unternehmen"],
    "EUDR":  ["Gegenstand und Anwendungsbereich", "in Verkehr gebracht"],
}

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        FAILURES.append(msg)


def test_parser_basics() -> None:
    print("\n[parse_sections]")
    raw = (
        "Erwaegungsgrund 1 lang lang lang.\n"
        "Erwaegungsgrund 2 lang lang lang.\n"
        "Artikel 1\n"
        "Gegenstand\n" + "A" * 600 + "\n"
        "Artikel 2\n"
        "Anwendungsbereich\n" + "B" * 600 + "\n"
        "Diese Richtlinie gilt gemaess Artikel 2 Absatz 1 auch fuer X.\n"
        "„Artikel 19a\n"
        "Berichterstattung\n" + "C" * 600 + "\n"
        "ANHANG I\n" + "D" * 600 + "\n"
    )
    secs = lawparse.parse_sections(raw)
    labels = [s["label"] for s in secs]
    check(labels == ["Art. 1", "Art. 2", "Art. 19a", "Anhang I"], f"Abschnitte erkannt: {labels}")
    check(all("Erwaegungsgrund" not in s["text"] for s in secs), "Praeambel verworfen")
    check("Absatz" not in " ".join(labels), "Querverweis-Zeile nicht als Ueberschrift gewertet")
    check(secs[1]["title"] == "Anwendungsbereich", "Titel aus Folgezeile (PDF-Artefakt)")
    check(secs[3]["kind"] == "annex", "Anhang als eigener Abschnitt")

    print("\n[article_refs]")
    cases = {
        "Art. 2 (Anwendungsbereich)": (["2"], []),
        "Art. 19a, 29a (aktualisiert)": (["19a", "29a"], []),
        "§ 12 HinSchG": (["12"], []),
        "§§ 289b-289h HGB-E": (["289b", "289c", "289d", "289e", "289f", "289g", "289h"], []),
        "Art. 1, Anhang I": (["1"], ["I"]),
        "Art. 2 (Ausnahmen), Art. 3 (Dokumentation)": (["2", "3"], []),
    }
    for src, expected in cases.items():
        check(lawparse.article_refs(src) == expected, f"{src!r} -> {lawparse.article_refs(src)}")

    print("\n[Fallback ohne Struktur]")
    plain = "Nur Fliesstext ohne jede Gliederung. " * 50
    reg = _reg("CSDDD")
    ctx = lawparse.build_context(reg, plain, [], 5000)
    check(plain[:200] in ctx, "Text ohne Struktur wird unveraendert durchgereicht")
    check(lawparse.parse_sections(plain) == [], "parse_sections liefert [] ohne Struktur")


def test_scope_reaches_llm() -> None:
    print("\n[build_context — Anwendungsbereich erreicht das LLM]")
    for key, markers in SCOPE_MARKERS.items():
        reg = _reg(key)
        raw = _law_text(reg)
        check(len(raw) > 20000, f"{key}: Rohtext geladen ({len(raw)} Zeichen)")
        if len(raw) < 20000:
            continue

        old = _old_context(reg, raw, BUDGET)
        new = lawparse.build_context(reg, raw, [], BUDGET)

        check(len(new) <= BUDGET, f"{key}: Kontext {len(new)} Zeichen <= Budget {BUDGET}")
        for m in markers:
            check(m in new, f"{key}: neuer Kontext enthaelt {m!r}")
        missing_old = [m for m in markers if m not in old]
        first_art = raw.find("Artikel 1")
        print(f"       alt ({len(old)} Zeichen): fehlende Marker {missing_old or 'keine'} "
              f"| 'Artikel 1' steht im Rohtext ab Zeichen {first_art}")

        # Kernartikel laut regulations.py muessen als Abschnitt auftauchen.
        arts, _ = lawparse.article_refs(reg.get("key_article") or "")
        for a in arts:
            check(f"=== Art. {a}" in new or f"=== Art. {a.upper()}" in new,
                  f"{key}: Kernartikel Art. {a} als Abschnitt im Kontext")


# Belege dafuer, dass die Quelle den RICHTIGEN Rechtsakt liefert — nicht nur
# irgendeinen Text. Alle fuenf Eintraege waren vor 09/2026 defekt oder falsch.
SOURCE_MARKERS: dict[str, list[str]] = {
    # zeigte auf eine BAFA-Uebersichtsseite (Pressetext ohne § 1)
    "LkSG":        ["§ 1", "Arbeitnehmer im Inland"],
    # zeigte auf das Inhaltsverzeichnis
    "HinSchG":     ["§ 12", "50 Beschäftigten"],
    # zeigte auf das Inhaltsverzeichnis
    "MinRohSorgG": ["§ 1", "Verordnung (EU) 2017/821"],
    # zeigte auf die bgbl.de-Startseite; jetzt HGB-Gesamtausgabe.
    # § 289b steht bei Zeichen ~259 000 — der Test sichert die Kappungsgrenze ab.
    "CSR-RUG":     ["§ 289b", "500 Arbeitnehmer"],
    # Neu am 02.09.2026; der Volltext kommt ueber Cellar (32026R0296).
    "Vernichtungsverbot": ["2026/296", "acht Wochen"],
}


def test_sources_deliver_fulltext() -> None:
    """Jede Quelle liefert echten Volltext — und die reparierten den richtigen."""
    print("\n[Quellen — Volltext statt Uebersichtsseite]")
    for reg in REGULATIONS:
        raw = _law_text(reg)
        n_sec = len(lawparse.parse_sections(raw))
        check(len(raw) >= MIN_CHARS,
              f"{reg['key']:16s} Volltext {len(raw):7d} Zeichen (>= {MIN_CHARS})")
        check(n_sec >= MIN_SECTIONS,
              f"{reg['key']:16s} {n_sec:3d} Abschnitte erkannt (>= {MIN_SECTIONS})")

    print("\n[Quellen — richtiger Rechtsakt]")
    for key, markers in SOURCE_MARKERS.items():
        raw = _law_text(_reg(key))
        for marker in markers:
            check(marker in raw, f"{key:16s} enthaelt {marker!r}")


def test_all_regulations_fit() -> None:
    print("\n[build_context — alle 20 Regulierungen]")
    for reg in REGULATIONS:
        cached = fetcher.get_cached_text(reg["key"], "de") or {}
        raw = cached.get("text") or ""
        guides = [{"name": "G", "url": "u", "text": "x" * 50000}]
        ctx = lawparse.build_context(reg, raw, guides, BUDGET)
        n_sec = len(lawparse.parse_sections(raw))
        check(len(ctx) <= BUDGET, f"{reg['key']:16s} roh={len(raw):7d} abschnitte={n_sec:3d} "
                                  f"kontext={len(ctx):6d}")


if __name__ == "__main__":
    print(f"Test-DB: {TEST_DB} ({'behalten' if KEEP_CACHE else 'frisch aufgebaut'})")
    test_parser_basics()
    test_sources_deliver_fulltext()
    test_scope_reaches_llm()
    test_all_regulations_fit()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FEHLER:")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("Alle Tests gruen.")
