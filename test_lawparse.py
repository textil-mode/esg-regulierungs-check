"""Tests fuer lawparse.build_context gegen echte Gesetzestexte.

Ausfuehren:  ./.venv/Scripts/python.exe test_lawparse.py

Die Texte kommen aus einer KOPIE der lokalen DB (`data/esg.db`), die beim
ersten Lauf unter `data/esg_lawparse_test.db` angelegt und ueber den Fetcher
befuellt wird (`data/` steht in .gitignore). Die Produktiv-DB wird nie
beschrieben.

Abnahmekriterium: fuer CSDDD, CSRD und EUDR enthaelt der gebaute Kontext den
Anwendungsbereichs-Artikel, und die Gesamtlaenge bleibt unter dem Budget.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DIR = BASE / "data"
TEST_DB = TEST_DIR / "esg_lawparse_test.db"

# Live laeuft FULLTEXT_MAX_CHARS=25000 — dagegen wird getestet.
BUDGET = 25000

import fetcher  # noqa: E402
import lawparse  # noqa: E402
from regulations import REGULATIONS  # noqa: E402


def _setup_db() -> None:
    """Test-DB als Kopie anlegen und den Fetcher darauf umbiegen."""
    TEST_DIR.mkdir(exist_ok=True)
    if not TEST_DB.exists():
        src = BASE / "data" / "esg.db"
        if src.exists():
            shutil.copy2(src, TEST_DB)
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
    if len(text) < 5000:
        # Kein brauchbarer Cache -> frisch laden (schreibt nur in die Test-DB).
        os.environ.setdefault("LAW_TEXT_MAX_CHARS", "400000")
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
        "Annex I (ESRS 1, ESRS 2, E1-E5, S1-S4, G1)": ([], ["I"]),
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


def test_all_regulations_fit() -> None:
    print("\n[build_context — alle 22 Regulierungen]")
    for reg in REGULATIONS:
        cached = fetcher.get_cached_text(reg["key"], "de") or {}
        raw = cached.get("text") or ""
        guides = [{"name": "G", "url": "u", "text": "x" * 50000}]
        ctx = lawparse.build_context(reg, raw, guides, BUDGET)
        n_sec = len(lawparse.parse_sections(raw))
        check(len(ctx) <= BUDGET, f"{reg['key']:16s} roh={len(raw):7d} abschnitte={n_sec:3d} "
                                  f"kontext={len(ctx):6d}")


if __name__ == "__main__":
    test_parser_basics()
    test_scope_reaches_llm()
    test_all_regulations_fit()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FEHLER:")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("Alle Tests gruen.")
