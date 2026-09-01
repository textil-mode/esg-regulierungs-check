"""Tests fuer die Wortstabilitaet der Begruendungen.

Ausfuehren:  ./.venv/Scripts/python.exe test_cache_stability.py
             ./.venv/Scripts/python.exe test_cache_stability.py --live   (echte LLM-Calls)

Nachgewiesen wird die Zusage: **eine Begruendung wird nur dann neu formuliert,
wenn sich die Regulierung oder ein fuer sie relevanter Profilwert geaendert hat.**

Getestet wird der echte Analyse-Pfad (`app._run_analysis_bg`) gegen die Test-DB
`data/esg_cache_test.db`; die Produktiv-DB `data/esg.db` wird nur gelesen (die
gecachten Gesetzestexte werden einmalig kopiert). Die Gesetzesquellen werden
nicht neu geladen: fuer die Cache-Frage zaehlt der gecachte Text, und ein
Netz-Abruf mitten im Test wuerde die Messung verrauschen.

Ohne `--live` antwortet ein Platzhalter statt des LLM — der Test misst dann nur
die Cache-Entscheidungen, kostet nichts und braucht keinen API-Key. Mit `--live`
laufen echte Calls (Szenario 1 formuliert 16 Begruendungen, ca. 0,5 ct).

Szenarien:
  1. Erstlauf                      -> 22 Karten, nur die nicht-gekoppelten ans LLM
  2. Gleiches Profil noch einmal   -> 0 neue Formulierungen, Texte byte-identisch
  3. Firmenname geaendert          -> 0 neue Formulierungen, Texte byte-identisch
  4. employees geaendert           -> nur Regs mit `employees` in relevant_fields
  5. Gesetzestext geaendert        -> nur die betroffene Regulierung
  6. Gesetzestext nicht abrufbar   -> 0 neue Formulierungen (alter Stand gilt weiter)
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_cache_test.db"
SOURCE_DB = BASE / "data" / "esg.db"

LIVE = "--live" in sys.argv

os.environ["ESG_DB_PATH"] = str(TEST_DB)
if not LIVE:
    # Der Platzhalter ersetzt `_analyze_one`; der Client wird nie befragt, darf
    # aber auch nicht schon beim Anlegen einen API-Key verlangen.
    os.environ["LLM_PROVIDER"] = "ollama"

if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import fetcher  # noqa: E402
import llm  # noqa: E402
import app as esg_app  # noqa: E402
from regulations import REGULATIONS, relevant_fields_for  # noqa: E402

PROFILE = {
    "name": "Muster Textil GmbH",
    "employees": 1200,
    "employees_de": 900,
    "revenue_eur": 600_000_000.0,
    "balance_sheet_eur": 300_000_000.0,
    "branch": "Textil / Bekleidung / Leder",
    "b2c": True,
    "listed": False,
    "env_claims": True,
    "eu_importer": True,
    "legal_form": "GmbH",
    "group_role": "Eigenständig (kein Konzern)",
    "sites": [{"type": "Hauptsitz", "location": "Deutschland", "count": 1}],
    "product_categories": ["Textilien / Bekleidung / Leder"],
    "language": "de",
}

# Ohne Textbaustein, also LLM-Faelle
LLM_KEYS = [r["key"] for r in REGULATIONS
            if llm.deterministic_result(r, PROFILE, "de") is None]
TEMPLATE_KEYS = [r["key"] for r in REGULATIONS if r["key"] not in LLM_KEYS]

_calls: list[str] = []
_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


# ---------------------------------------------------------------------------
# Testaufbau: eigene DB, Gesetzestexte aus der Produktiv-DB uebernehmen
# ---------------------------------------------------------------------------
def _setup_db() -> int:
    db.init_db()
    fetcher.init_fetcher()
    if not SOURCE_DB.exists():
        sys.exit(f"{SOURCE_DB} fehlt — ohne gecachte Gesetzestexte ist der Test sinnlos.")
    c = sqlite3.connect(TEST_DB, isolation_level=None, uri=True)
    try:
        # Strikt lesend anhaengen: die Produktiv-DB darf durch einen Testlauf
        # unter keinen Umstaenden angefasst werden.
        c.execute("ATTACH DATABASE ? AS src", (SOURCE_DB.as_uri() + "?mode=ro",))
        # Nur die gemeinsamen Spalten kopieren: die Produktiv-DB kann aelter sein.
        here = {r[1] for r in c.execute("PRAGMA table_info(law_texts)")}
        there = [r[1] for r in c.execute("PRAGMA src.table_info(law_texts)")]
        cols = ", ".join(col for col in there if col in here)
        c.execute(f"INSERT INTO law_texts ({cols}) SELECT {cols} FROM src.law_texts")
        c.execute("DETACH DATABASE src")
    finally:
        c.close()
    return db.create_user("cachetest@example.invalid", "nur-fuer-den-test")


def _offline_law_text(reg: dict, language: str = "de", **_kw) -> dict:
    cached = fetcher.get_cached_text(reg["key"], language) or {}
    return {"text": cached.get("text") or "", "fetched_at": cached.get("fetched_at") or "",
            "last_modified": None, "is_new": False, "error": "", "status": 200}


def _offline_url_text(url: str, **_kw) -> dict:
    return {"text": "", "fetched_at": "", "last_modified": None, "is_new": False,
            "error": "", "status": 304}


_real_analyze_one = llm._analyze_one


async def _counting_analyze_one(client, profile_block, reg, fulltext, language, profile=None):
    """Zaehlt jede Regulierung, die tatsaechlich neu formuliert wird."""
    _calls.append(reg["key"])
    if LIVE:
        return await _real_analyze_one(client, profile_block, reg, fulltext, language, profile)
    return {**llm._enrich(reg, {}), "applies": "nein",
            "reason": f"Platzhalter-Begruendung fuer {reg['key']}.",
            "passage": reg.get("key_article") or "-"}


def run(uid: int, profile: dict) -> tuple[dict[str, dict], list[str]]:
    """Ein Analyse-Lauf. Rueckgabe: (Ergebnisse je reg_key, neu formulierte Keys)."""
    _calls.clear()
    esg_app._analysis_status[uid] = {"phase": "starting", "done": 0,
                                     "total": len(REGULATIONS), "name": ""}
    esg_app._run_analysis_bg(uid, profile, profile.get("language") or "de")
    status = esg_app._analysis_status[uid]
    if status.get("phase") != "done":
        sys.exit(f"Lauf abgebrochen: {status}")
    stored = db.latest_analysis(uid)["result"]
    return {r["key"]: r for r in stored}, sorted(_calls)


def reasons(results: dict[str, dict]) -> dict[str, str]:
    return {k: v.get("reason", "") for k, v in results.items()}


def diff_keys(a: dict[str, str], b: dict[str, str]) -> list[str]:
    return sorted(k for k in a if a[k] != b.get(k))


def main() -> int:
    esg_app.fetch_law_text = _offline_law_text
    esg_app.fetch_url_text = _offline_url_text
    llm._analyze_one = _counting_analyze_one

    uid = _setup_db()
    print(f"Modus: {'LIVE (echte LLM-Calls)' if LIVE else 'Platzhalter (kein LLM)'}")
    print(f"Textbausteine ({len(TEMPLATE_KEYS)}): {', '.join(TEMPLATE_KEYS)}")
    print()

    # --- 1. Erstlauf -------------------------------------------------------
    res1, calls1 = run(uid, PROFILE)
    check("1 Erstlauf: 22 Karten", len(res1) == len(REGULATIONS), f"{len(res1)}/{len(REGULATIONS)}")
    check("1 Erstlauf: keine Fehlerkarte",
          all(r.get("applies") != "error" for r in res1.values()),
          ", ".join(k for k, r in res1.items() if r.get("applies") == "error") or "keine")
    check("1 Erstlauf: Textbausteine kosten keinen Call",
          not set(calls1) & set(TEMPLATE_KEYS), f"{len(calls1)} Calls fuer {len(LLM_KEYS)} LLM-Regs")
    check("1 Erstlauf: jede Begruendung gefuellt",
          all((r.get("reason") or "").strip() for r in res1.values()))

    # --- 2. Identischer Lauf ----------------------------------------------
    res2, calls2 = run(uid, PROFILE)
    check("2 Gleiches Profil: 0 neue Formulierungen", calls2 == [], str(calls2))
    check("2 Gleiches Profil: Begruendungen byte-identisch",
          reasons(res1) == reasons(res2), str(diff_keys(reasons(res1), reasons(res2))))
    check("2 Gleiches Profil: Fundstellen byte-identisch",
          all(res1[k].get("passage") == res2[k].get("passage") for k in res1))

    # --- 3. Irrelevantes Feld (Firmenname) --------------------------------
    res3, calls3 = run(uid, {**PROFILE, "name": "Ganz Anders AG"})
    check("3 Firmenname geaendert: 0 neue Formulierungen", calls3 == [], str(calls3))
    check("3 Firmenname geaendert: Begruendungen byte-identisch",
          reasons(res1) == reasons(res3), str(diff_keys(reasons(res1), reasons(res3))))

    # --- 4. Relevantes Feld (employees) -----------------------------------
    expect4 = sorted(r["key"] for r in REGULATIONS
                     if "employees" in relevant_fields_for(r) and r["key"] in LLM_KEYS)
    res4, calls4 = run(uid, {**PROFILE, "employees": 5200})
    check("4 employees geaendert: nur betroffene Regs neu", calls4 == expect4,
          f"neu={calls4} erwartet={expect4}")
    # Unbeteiligt ist, wer `employees` gar nicht auswertet — die Textbausteine
    # der CSRD-Familie MUESSEN sich mitaendern, sie nennen die Beschaeftigtenzahl.
    unaffected = [r["key"] for r in REGULATIONS if "employees" not in relevant_fields_for(r)]
    moved = [k for k in unaffected if res1[k]["reason"] != res4[k]["reason"]]
    check("4 employees geaendert: uebrige Begruendungen unveraendert", not moved, str(moved))

    # --- 5. Gesetzestext geaendert ----------------------------------------
    victim = "LkSG"
    with sqlite3.connect(TEST_DB) as c:
        c.execute("UPDATE law_texts SET text = text || ? WHERE reg_key = ? AND language = 'de'",
                  ("\n§ 99 Testparagraph.", victim))
    res5, calls5 = run(uid, PROFILE)
    check("5 Gesetzestext geaendert: nur diese Regulierung neu", calls5 == [victim], str(calls5))
    check("5 Gesetzestext geaendert: uebrige Begruendungen unveraendert",
          all(res1[k]["reason"] == res5[k]["reason"] for k in res1 if k != victim),
          str([k for k in res1 if k != victim and res1[k]["reason"] != res5[k]["reason"]]))

    # --- 6. Gesetzestext nicht abrufbar -----------------------------------
    with sqlite3.connect(TEST_DB) as c:
        c.execute("UPDATE law_texts SET text = '' WHERE reg_key = ? AND language = 'de'", (victim,))
    res6, calls6 = run(uid, PROFILE)
    check("6 Quelle nicht abrufbar: 0 neue Formulierungen", calls6 == [], str(calls6))
    check("6 Quelle nicht abrufbar: Begruendung bleibt der letzte gueltige Stand",
          res6[victim]["reason"] == res5[victim]["reason"])

    # --- Stichprobe --------------------------------------------------------
    print()
    print("Stichprobe (DE, Erstlauf):")
    for key in ("CSRD", "HinSchG", "LkSG", "EUDR", "EmpCo"):
        if key in res1:
            print(f"  [{res1[key]['applies']}] {key}: {res1[key]['reason']}")
            print(f"        Fundstelle: {res1[key]['passage']}")

    print()
    if _failures:
        print(f"FEHLGESCHLAGEN: {len(_failures)}")
        for f in _failures:
            print(f"  - {f}")
        return 1
    print("Alle Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
