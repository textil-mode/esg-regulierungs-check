"""Woechentlicher Aktualitaets-Waechter fuer die Gesetzestexte.

Ausfuehren:  python watchdog.py [--language de] [--no-llm]

Der Watchdog laedt alle Regulierungen frisch (force=True, also ohne
ETag-Kurzschluss), vergleicht den SHA-256 des Texts mit der zuletzt in
`law_versions` gespeicherten Fassung und schreibt das Ergebnis in
`watchdog_runs`. Bei einer Abweichung wird der Unterschied kurz vom LLM
zusammengefasst — als **Vorschlag**. Die `criteria` in `regulations.py` werden
nie automatisch veraendert; ueber Rechtsaussagen entscheidet ein Mensch.

Gedacht fuer Cron auf dem VPS, siehe README/CLAUDE.md.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
import traceback
from datetime import datetime

from dotenv import load_dotenv

# VOR den Projekt-Importen: db.py liest `ESG_DB_PATH` beim Import. Stuende der
# Aufruf darunter, schriebe ein Testlauf trotz gesetzter Variable in die
# Produktiv-DB.
load_dotenv(override=True)

import db  # noqa: E402
import lawparse  # noqa: E402
import pflichten_db  # noqa: E402
import pflichten_vorschlag  # noqa: E402
from fetcher import fetch_law_text, version_text  # noqa: E402
from regulations import REGULATIONS  # noqa: E402


# Diff-Auszug liegt in lawparse (auch pflichten_vorschlag braucht ihn);
# die alten Namen bleiben hier erhalten.
DIFF_MAX_CHARS = lawparse.DIFF_MAX_CHARS
_diff_excerpt = lawparse.diff_auszug

_SUMMARY_SYSTEM = (
    "Du bist Jurist und vergleichst zwei Fassungen eines EU- oder Bundesgesetzes. "
    "Antworte auf Deutsch, sachlich, hoechstens 120 Woerter. Nenne nur, was sich "
    "inhaltlich geaendert hat — besonders Schwellenwerte, Anwendungsbereich, "
    "Fristen und Anwendungsdaten. Reine Formatierungs- oder Layout-Unterschiede "
    "nennst du als 'keine inhaltliche Aenderung erkennbar'. Erfinde nichts."
)


async def _summarize(reg: dict, old: str, new: str) -> str:
    from llm import LLMClient
    client = LLMClient()
    user = (
        f"Rechtsakt: {reg.get('full_name') or reg['name']}\n"
        f"Bisher hinterlegte Kriterien: {reg.get('criteria', '')}\n\n"
        f"{_diff_excerpt(old, new)}\n\n"
        "Fasse die inhaltliche Aenderung zusammen und sage, ob die hinterlegten "
        "Kriterien dadurch ueberholt sein koennten."
    )
    return (await client.ask(_SUMMARY_SYSTEM, user, max_tokens=400, json_mode=False)).strip()


def _pflichten_vorschlaege(key: str, old_text: str, new_text: str, run_id: int,
                           entry: dict, errors: list[dict], vorschlaege: dict[str, int]) -> None:
    """KI-Vorschlaege fuer den Pflichten-Katalog; Fehler landen in `errors`."""
    verworfen: list[str] = []
    try:
        ids = asyncio.run(pflichten_vorschlag.vorschlaege_aus_aenderung(
            key, old_text, new_text, ausloeser_ref=str(run_id), verworfen=verworfen))
    except Exception as e:  # noqa: BLE001 — bricht den Lauf nicht ab
        errors.append({"reg_key": key, "error": f"Pflichten-Vorschlaege: {type(e).__name__}: {e}"})
        traceback.print_exc()
        return
    entry["pflichten_vorschlaege"] = len(ids)
    entry["pflichten_verworfen"] = len(verworfen)
    if ids:
        vorschlaege[key] = len(ids)
    print(f"[watchdog] {key}: {len(ids)} Pflichten-Vorschlaege, {len(verworfen)} verworfen",
          flush=True)


def run(language: str = "de", use_llm: bool = True) -> dict:
    run_id = db.start_watchdog_run(language)
    changed: list[dict] = []
    errors: list[dict] = []
    checked = 0
    # Pflichten-Plan: KI-Vorschlaege nur auf der deutschen Fassung (der Katalog
    # ist deutsch gepflegt) und nur, wenn die Funktion nicht abgeschaltet ist.
    pflichten_an = language == "de" and pflichten_db.funktion_aktiv()
    vorschlaege: dict[str, int] = {}

    for reg in REGULATIONS:
        key = reg["key"]
        try:
            res = fetch_law_text(reg, language=language, force=True)
        except Exception as e:  # noqa: BLE001
            errors.append({"reg_key": key, "error": f"{type(e).__name__}: {e}"})
            print(f"[watchdog] {key}: FEHLER {e}", flush=True)
            continue

        checked += 1
        if res.get("error"):
            errors.append({"reg_key": key, "error": str(res["error"])})
        if not (res.get("text") or "").strip():
            errors.append({"reg_key": key, "error": "leerer Text"})
            print(f"[watchdog] {key}: leerer Text", flush=True)
            continue

        if not res.get("version_new"):
            print(f"[watchdog] {key}: unveraendert", flush=True)
            continue

        previous_hash = res.get("previous_hash")
        entry = {
            "reg_key": key,
            "name": reg["name"],
            "previous_hash": previous_hash,
            "text_hash": res.get("text_hash"),
            "summary": "",
        }
        if previous_hash is None:
            # Erste gespeicherte Fassung — kein Vergleich moeglich, keine Aenderung.
            print(f"[watchdog] {key}: erste Fassung aufgenommen", flush=True)
            continue

        print(f"[watchdog] {key}: GEAENDERT", flush=True)
        old_text = ""
        if use_llm:
            try:
                old_text = version_text(key, language, previous_hash)
                entry["summary"] = asyncio.run(_summarize(reg, old_text, res["text"]))
            except Exception as e:  # noqa: BLE001
                entry["summary"] = ""
                errors.append({"reg_key": key, "error": f"LLM-Zusammenfassung: {e}"})
                traceback.print_exc()
        changed.append(entry)
        # Spec 6.4: nur Regulierungen, die schon Schritte im Katalog haben.
        if (use_llm and pflichten_an and (old_text or "").strip()
                and pflichten_db.schritte_fuer(key, "de")):
            _pflichten_vorschlaege(key, old_text, res["text"], run_id, entry, errors,
                                   vorschlaege)

    if vorschlaege:
        try:
            pflichten_vorschlag.benachrichtige_admin(vorschlaege)
        except Exception as e:  # noqa: BLE001
            errors.append({"reg_key": "-", "error": f"Admin-Mail Pflichten-Vorschlaege: {e}"})

    db.finish_watchdog_run(run_id, checked, changed, errors)
    return {"run_id": run_id, "checked": checked, "changed": changed, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Aktualitaets-Waechter fuer Gesetzestexte")
    parser.add_argument("--language", default=os.getenv("WATCHDOG_LANGUAGE", "de"))
    parser.add_argument("--no-llm", action="store_true",
                        help="Aenderungen erfassen, aber nicht zusammenfassen (spart Kosten)")
    args = parser.parse_args()

    started = datetime.now()
    result = run(language=args.language, use_llm=not args.no_llm)
    print(
        f"\n[watchdog] Lauf {result['run_id']} fertig in {(datetime.now() - started).seconds}s: "
        f"{result['checked']} geprueft, {len(result['changed'])} geaendert, "
        f"{len(result['errors'])} Fehler",
        flush=True,
    )
    for entry in result["changed"]:
        print(f"  geaendert: {entry['reg_key']}")
    for entry in result["errors"]:
        print(f"  Fehler:    {entry['reg_key']}: {entry['error']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
