"""Tests zum Pflichten-Plan, Aufgabe 2: Frist-Regeln (reine Funktion, keine DB).

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_frist.py
"""
from __future__ import annotations

import sys
from datetime import date

from pflichten import frist_fuer

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


TODAY = date(2026, 11, 19)


def case(label, args, art, datum=None, periode=""):
    r = frist_fuer(*args)
    check(label, r["art"] == art and r["datum"] == datum and r["periode"] == periode, repr(r))


case("relativ -6m", ("relativ", "-6m", "30.06.2027", TODAY), "datum", date(2026, 12, 30))
case("relativ +0d", ("relativ", "+0d", "30.06.2027", TODAY), "datum", date(2027, 6, 30))
case("relativ Datum in Vergangenheit, Anker Zukunft", ("relativ", "-6m", "30.12.2026", TODAY), "datum", date(2026, 6, 30))
case("relativ Anker lange vorbei", ("relativ", "-6m", "01.01.2023", TODAY), "laufend")
case("relativ Anker = heute", ("relativ", "-6m", "19.11.2026", TODAY), "laufend")
case("relativ Anker leer", ("relativ", "-6m", "", TODAY), "offen")
case("fest", ("fest", "31.12.2027", "", TODAY), "datum", date(2027, 12, 31))
case("jaehrlich naechster", ("jaehrlich", "31.05.", "", TODAY), "datum", date(2027, 5, 31), "2027")
case("jaehrlich Stichtag selbst", ("jaehrlich", "31.05.", "", date(2027, 5, 31)), "datum", date(2027, 5, 31), "2027")
case("jaehrlich 29.02.", ("jaehrlich", "29.02.", "", TODAY), "datum", date(2027, 2, 28), "2027")
case("keine", ("keine", "", "30.06.2027", TODAY), "keine")
case("relativ quatsch", ("relativ", "quatsch", "30.06.2027", TODAY), "keine")
case("Monatsende -1m", ("relativ", "-1m", "31.03.2027", TODAY), "datum", date(2027, 2, 28))
case("relativ -30d", ("relativ", "-30d", "31.12.2027", TODAY), "datum", date(2027, 12, 1))
case("fest kaputt", ("fest", "99.99.2027", "", TODAY), "keine")
case("jaehrlich kaputt", ("jaehrlich", "xx", "", TODAY), "keine")
case("unbekannter Typ", ("foo", "", "", TODAY), "keine")
case("relativ Anker kaputt", ("relativ", "-6m", "kaputt", TODAY), "keine")

if _failures:
    print(f"\n{len(_failures)} FEHLER")
    sys.exit(1)
print("\nAlle Tests gruen")
