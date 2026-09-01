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
import difflib
import os
import sys
import traceback
from datetime import datetime

from dotenv import load_dotenv

import db
from fetcher import fetch_law_text, version_text
from regulations import REGULATIONS

load_dotenv(override=True)


# Wieviel Diff-Umgebung das LLM je Fassung sieht. Bewusst knapp: eine
# Konsolidierung aendert oft hunderte Zeilen, und der Vorschlag soll nur die
# Richtung angeben, nicht den Rechtsakt nacherzaehlen.
DIFF_MAX_CHARS = 15_000

_SUMMARY_SYSTEM = (
    "Du bist Jurist und vergleichst zwei Fassungen eines EU- oder Bundesgesetzes. "
    "Antworte auf Deutsch, sachlich, hoechstens 120 Woerter. Nenne nur, was sich "
    "inhaltlich geaendert hat — besonders Schwellenwerte, Anwendungsbereich, "
    "Fristen und Anwendungsdaten. Reine Formatierungs- oder Layout-Unterschiede "
    "nennst du als 'keine inhaltliche Aenderung erkennbar'. Erfinde nichts."
)


def _diff_excerpt(old: str, new: str) -> str:
    """Unified Diff, auf DIFF_MAX_CHARS je Fassung begrenzt."""
    old_lines = (old or "").splitlines()
    new_lines = (new or "").splitlines()
    diff = difflib.unified_diff(old_lines, new_lines, lineterm="", n=2)
    removed: list[str] = []
    added: list[str] = []
    for line in diff:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("-") and len("\n".join(removed)) < DIFF_MAX_CHARS:
            removed.append(line[1:])
        elif line.startswith("+") and len("\n".join(added)) < DIFF_MAX_CHARS:
            added.append(line[1:])
        if len("\n".join(removed)) >= DIFF_MAX_CHARS and len("\n".join(added)) >= DIFF_MAX_CHARS:
            break
    return (
        "ALTE FASSUNG (entfernte Stellen):\n"
        + "\n".join(removed)[:DIFF_MAX_CHARS]
        + "\n\nNEUE FASSUNG (hinzugekommene Stellen):\n"
        + "\n".join(added)[:DIFF_MAX_CHARS]
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


def run(language: str = "de", use_llm: bool = True) -> dict:
    run_id = db.start_watchdog_run(language)
    changed: list[dict] = []
    errors: list[dict] = []
    checked = 0

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
        if use_llm:
            try:
                old_text = version_text(key, language, previous_hash)
                entry["summary"] = asyncio.run(_summarize(reg, old_text, res["text"]))
            except Exception as e:  # noqa: BLE001
                entry["summary"] = ""
                errors.append({"reg_key": key, "error": f"LLM-Zusammenfassung: {e}"})
                traceback.print_exc()
        changed.append(entry)

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
