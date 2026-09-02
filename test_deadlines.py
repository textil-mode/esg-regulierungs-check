"""Tests fuer die Fristen-Logik (`deadlines.py`) und die Schwellen-Naehe.

Reine Rechenlogik ohne Datenbank, ohne Netz, ohne LLM — der Lauf kostet nichts
und braucht kein `ESG_DB_PATH`.

Aufruf:  ./.venv/Scripts/python.exe test_deadlines.py
"""
from __future__ import annotations

import sys

import i18n
import regulations
from deadlines import deadline_for, deadlines_for_profile
from thresholds import near_thresholds

# ---------------------------------------------------------------------------
# Drei Profile aus dem Auftrag.
# ---------------------------------------------------------------------------

KLEINBETRIEB = {
    "name": "Kleinbetrieb",
    "employees": 35,
    "employees_de": 35,
    "revenue_eur": 4_000_000,
    "branch": "Textil / Bekleidung / Leder",
    "legal_form": "GmbH",
    "group_role": "Eigenständig (kein Konzern)",
    "listed": False,
    "b2c": True,
    "env_claims": True,
    "eu_importer": False,
    "sites": [{"type": "Hauptsitz", "location": "Deutschland", "count": 35}],
    "product_categories": ["Textilien / Bekleidung / Leder"],
    "language": "de",
}

MITTELSTAND_1100 = {
    "name": "Mittelstaendler",
    "employees": 1_100,
    "employees_de": 1_100,
    "revenue_eur": 210_000_000,
    "branch": "Textil / Bekleidung / Leder",
    "legal_form": "GmbH & Co. KG",
    "group_role": "Eigenständig (kein Konzern)",
    "listed": False,
    "b2c": True,
    "env_claims": True,
    "eu_importer": True,
    "sites": [{"type": "Hauptsitz", "location": "Deutschland", "count": 1100}],
    "product_categories": ["Textilien / Bekleidung / Leder"],
    "language": "de",
}

GROSSKONZERN = {
    "name": "Grosskonzern",
    "employees": 12_000,
    "employees_de": 6_500,
    "revenue_eur": 3_200_000_000,
    "branch": "Textil / Bekleidung / Leder",
    "legal_form": "AG / SE",
    "group_role": "Mutterunternehmen mit Sitz in EU",
    "listed": True,
    "b2c": True,
    "env_claims": True,
    "eu_importer": True,
    "sites": [{"type": "Hauptsitz", "location": "Deutschland", "count": 6500}],
    "product_categories": ["Textilien / Bekleidung / Leder"],
    "language": "de",
}

# Fuer den Schwellen-Test aus den Abschlusskriterien.
PROFIL_950_DE = dict(MITTELSTAND_1100, name="950 MA in DE", employees=950, employees_de=950)


# ---------------------------------------------------------------------------
# Erwartete gilt_ab-Werte. Herleitung steht jeweils daneben.
# ---------------------------------------------------------------------------
ERWARTET: list[tuple[str, dict, str, str]] = [
    # (reg_key, profil, erwartetes gilt_ab, Herleitung)
    ("LkSG", KLEINBETRIEB, "01.01.2024",
     "unter 3.000 MA im Inland -> zweite Stufe, § 1 Abs. 1 S. 3 LkSG"),
    ("LkSG", MITTELSTAND_1100, "01.01.2024",
     "1.100 MA im Inland -> zweite Stufe seit 01.01.2024"),
    ("LkSG", GROSSKONZERN, "01.01.2023",
     "6.500 MA im Inland -> erste Stufe ab 3.000, seit 01.01.2023"),

    ("HinSchG", KLEINBETRIEB, "17.12.2023",
     "unter 250 Beschaeftigte -> § 42 HinSchG"),
    ("HinSchG", MITTELSTAND_1100, "02.07.2023",
     "ueber 250 Beschaeftigte -> mit Inkrafttreten"),
    ("HinSchG", GROSSKONZERN, "02.07.2023",
     "ueber 250 Beschaeftigte -> mit Inkrafttreten"),

    ("WhistleblowerRL", KLEINBETRIEB, "17.12.2023", "Art. 26 Abs. 2"),
    ("WhistleblowerRL", GROSSKONZERN, "17.12.2021", "Art. 26 Abs. 1"),

    ("CSRD", KLEINBETRIEB, "01.01.2027", "neue Schwellen, kein Welle-1-Fall"),
    ("CSRD", MITTELSTAND_1100, "01.01.2027", "neue Schwellen, nicht boersennotiert"),
    ("CSRD", GROSSKONZERN, "01.01.2024",
     "boersennotiert mit mehr als 500 MA -> Welle 1"),

    ("ESRS", MITTELSTAND_1100, "01.01.2027", "folgt der CSRD-Frist dieses Unternehmens"),
    ("ESRS", GROSSKONZERN, "01.01.2024", "folgt der CSRD-Frist dieses Unternehmens"),

    ("TaxonomieVO", GROSSKONZERN, "01.01.2024", "folgt der CSRD-Frist"),

    ("EUDR", KLEINBETRIEB, "30.06.2027",
     "bis 50 MA und bis 15 Mio. EUR -> Art. 38 Abs. 3"),
    ("EUDR", MITTELSTAND_1100, "30.12.2026", "kein Kleinunternehmen"),
    ("EUDR", GROSSKONZERN, "30.12.2026", "kein Kleinunternehmen"),

    # Ohne Staffelung: applies_from aus regulations.py wird durchgereicht.
    ("CSDDD", GROSSKONZERN, "26.07.2029", "einstufig seit RL (EU) 2026/470"),
    ("CSDDD", KLEINBETRIEB, "26.07.2029", "einstufig, unabhaengig von der Groesse"),
    ("EmpCo", KLEINBETRIEB, "27.09.2026", "kein groessenabhaengiger Phase-in"),
    ("EmpCo", GROSSKONZERN, "27.09.2026", "kein groessenabhaengiger Phase-in"),
    ("PPWR", MITTELSTAND_1100, "12.08.2026", "Art. 71 VO (EU) 2025/40"),
    ("FLR", GROSSKONZERN, "14.12.2027", "Art. 39 VO (EU) 2024/3015"),
    ("RightToRepair", KLEINBETRIEB, "31.07.2026", "Art. 22 Abs. 1 UAbs. 3"),
    ("Oekodesign", MITTELSTAND_1100, "18.07.2024", "Art. 80 VO (EU) 2024/1781"),
    ("SFDR", GROSSKONZERN, "10.03.2021", "Art. 20 Abs. 2 VO (EU) 2019/2088"),

    # Ohne bestimmbares Datum.
    ("CSRD_DE", GROSSKONZERN, "", "Gesetzgebungsverfahren nicht abgeschlossen"),
    ("GreenClaims", KLEINBETRIEB, "", "Ruecknahme angekuendigt"),
]


def _fail(msg: str, fehler: list[str]) -> None:
    print(f"  FEHLER: {msg}")
    fehler.append(msg)


def test_gilt_ab(fehler: list[str]) -> None:
    print("\n[1] gilt_ab je Regulierung und Profil")
    for reg_key, profil, erwartet, herleitung in ERWARTET:
        info = deadline_for(reg_key, profil)
        if info is None:
            _fail(f"{reg_key}/{profil['name']}: kein Ergebnis", fehler)
            continue
        ist = info["gilt_ab"]
        marke = "ok " if ist == erwartet else "XX "
        print(f"  {marke}{reg_key:<16} {profil['name']:<15} "
              f"{ist or '(kein Datum)':<14} {herleitung}")
        if ist != erwartet:
            _fail(f"{reg_key}/{profil['name']}: erwartet {erwartet!r}, ist {ist!r}", fehler)


def test_vollstaendigkeit(fehler: list[str]) -> None:
    print("\n[2] Jede Regulierung liefert ein Ergebnis, jeder Hinweis ist uebersetzt")
    for profil in (KLEINBETRIEB, MITTELSTAND_1100, GROSSKONZERN):
        alle = deadlines_for_profile(profil)
        if len(alle) != len(regulations.REGULATIONS):
            _fail(f"{profil['name']}: {len(alle)} statt {len(regulations.REGULATIONS)} "
                  f"Regulierungen", fehler)
        for reg_key, info in alle.items():
            hinweis = info["hinweis"]
            if not hinweis:
                continue
            for lang in i18n.LANG_CODES:
                if not i18n.t_deadline_note(hinweis, lang):
                    _fail(f"{reg_key}: Hinweis {hinweis!r} fehlt in {lang}", fehler)
    print(f"  ok  {len(regulations.REGULATIONS)} Regulierungen, "
          f"Hinweise in {len(i18n.LANG_CODES)} Sprachen")


def test_unbekannte_reg(fehler: list[str]) -> None:
    print("\n[3] Unbekannte Regulierung liefert None")
    if deadline_for("GibtsNicht", KLEINBETRIEB) is not None:
        _fail("unbekannter Schluessel liefert kein None", fehler)
    else:
        print("  ok  None")


def test_schwellen_naehe(fehler: list[str]) -> None:
    print("\n[4] Schwellen-Naehe")
    faelle = [
        (PROFIL_950_DE, {"lksg_knapp_darunter"},
         "950 MA in DE: LkSG-Naehe, HinSchG laengst ueberschritten"),
        (KLEINBETRIEB, set(), "35 MA: keine Schwelle in Reichweite"),
        (MITTELSTAND_1100, {"lksg_knapp_darueber"}, "1.100 MA in DE: knapp darueber"),
        (dict(KLEINBETRIEB, employees=45, employees_de=45), {"hinschg_knapp_darunter"},
         "45 MA in DE: knapp unter der HinSchG-Schwelle"),
        (dict(MITTELSTAND_1100, employees=900, employees_de=900,
              revenue_eur=400_000_000), {"lksg_knapp_darunter", "csrd_knapp_darunter"},
         "900 MA / 400 Mio. EUR: LkSG- und CSRD-Naehe"),
        (dict(GROSSKONZERN, employees=4_500, employees_de=1_000,
              revenue_eur=1_400_000_000),
         {"lksg_knapp_darueber", "csddd_knapp_darunter"},
         "4.500 MA / 1,4 Mrd. EUR: CSDDD in Reichweite, CSRD laengst ueberschritten"),
    ]
    for profil, erwartet, beschreibung in faelle:
        keys = {h["key"] for h in near_thresholds(profil)}
        marke = "ok " if keys == erwartet else "XX "
        print(f"  {marke}{beschreibung}")
        if keys != erwartet:
            _fail(f"{beschreibung}: erwartet {sorted(erwartet)}, ist {sorted(keys)}", fehler)
        # Jeder erzeugte Hinweis muss in allen sechs Sprachen formulierbar sein.
        for hint in near_thresholds(profil):
            for lang in i18n.LANG_CODES:
                if not i18n.t_threshold_hint(hint, lang):
                    _fail(f"Hinweis {hint['key']} fehlt in {lang}", fehler)


def test_erste_schritte(fehler: list[str]) -> None:
    print("\n[5] Erste Schritte: 2-4 Stichpunkte je Regulierung, sechs Sprachen")
    for reg in regulations.REGULATIONS:
        steps = regulations.first_steps_for(reg["key"])
        if not 2 <= len(steps) <= 4:
            _fail(f"{reg['key']}: {len(steps)} Stichpunkte (erlaubt 2-4)", fehler)
        for step in steps:
            for lang in i18n.LANG_CODES:
                if not i18n.t_first_step(step, lang):
                    _fail(f"{reg['key']}: Schritt {step!r} fehlt in {lang}", fehler)
        if regulations.first_steps_link(reg["key"]) is None:
            _fail(f"{reg['key']}: keine weiterfuehrende Leitlinie", fehler)
    print(f"  ok  {len(regulations.REGULATIONS)} Regulierungen mit Leitlinien-Link")


def main() -> int:
    fehler: list[str] = []
    test_gilt_ab(fehler)
    test_vollstaendigkeit(fehler)
    test_unbekannte_reg(fehler)
    test_schwellen_naehe(fehler)
    test_erste_schritte(fehler)
    print("\n" + "=" * 70)
    if fehler:
        print(f"FEHLGESCHLAGEN — {len(fehler)} Befund(e):")
        for f in fehler:
            print(f"  - {f}")
        return 1
    print("Alle Tests bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
