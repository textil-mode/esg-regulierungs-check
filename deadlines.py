"""Anwendungsbeginn je Regulierung UND je Unternehmen — deterministisch.

`regulations.APPLICATION_BY_REG_KEY` haelt den Anwendungsbeginn der Norm.
Der Anwendungsbeginn fuer ein KONKRETES Unternehmen kann davon abweichen, wenn
die Norm nach Groesse staffelt (LkSG 3.000/1.000, HinSchG 250/50-249) oder wenn
sie an einer anderen Regulierung haengt (ESRS und Taxonomie-Offenlegung folgen
dem ersten CSRD-pflichtigen Geschaeftsjahr dieses Unternehmens).

Kein LLM, keine Netzzugriffe, kein Cache: `deadline_for()` rechnet aus dem
Profil und laeuft zur Renderzeit. Damit fliesst nichts davon in den
Begruendungs-Cache (`analysis_cache`) ein und loest keine Neuformulierung aus.

Rueckgabe je Regulierung:
    {"gilt_ab": "DD.MM.YYYY" | "", "hinweis": "<Schluessel>"}   oder None

`hinweis` ist ein Schluessel, kein Text — aufgeloest wird er in der UI-Sprache
ueber `i18n.t_deadline_note()` (erst `DEADLINE_NOTES`, dann `APPLIES_NOTES`).
Ein leeres `gilt_ab` heisst: fuer dieses Unternehmen laesst sich der Beginn
nicht aus dem Profil bestimmen (Entwurf, Ruecknahme, Drittland-Sonderregime) —
die Karte zeigt dann den Status statt eines erfundenen Datums.
"""
from __future__ import annotations

from datetime import date

import regulations
from regulations import application_for, csrd_status

# ---------------------------------------------------------------------------
# Schwellen der Groessen-Staffelungen (Fundstelle jeweils daneben).
# ---------------------------------------------------------------------------

# § 1 Abs. 1 Satz 3 LkSG: ab 01.01.2024 gilt 1.000 statt 3.000.
_LKSG_STUFE_3000 = "01.01.2023"
_LKSG_STUFE_1000 = "01.01.2024"

# § 42 Abs. 1 HinSchG: 50-249 Beschaeftigte erst ab 17.12.2023;
# ab 250 Beschaeftigten mit Inkrafttreten des Gesetzes am 02.07.2023.
_HINSCHG_AB_250 = "02.07.2023"
_HINSCHG_AB_50 = "17.12.2023"

# Art. 26 Abs. 1/2 RL (EU) 2019/1937: Umsetzungsfristen der Mitgliedstaaten.
_WHISTLE_AB_250 = "17.12.2021"
_WHISTLE_AB_50 = "17.12.2023"

# Art. 5 Abs. 2 UAbs. 1 lit. a RL (EU) 2022/2464 — Welle 1 (grosse Unternehmen
# von oeffentlichem Interesse mit mehr als 500 Beschaeftigten) berichtet seit
# dem Geschaeftsjahr 2024.
_CSRD_WELLE1 = "01.01.2024"

# Art. 38 Abs. 3 VO (EU) 2023/1115 in der Fassung der Verschiebung.
_EUDR_KLEIN = "30.06.2027"

# Art. 27 Abs. 2 lit. a VO (EU) 2020/852 — Klimaschutz/Anpassung; die
# Offenlegung nach Art. 8 haengt daneben an der CSRD-Pflicht.
_TAXONOMIE_FINANZ = "01.01.2022"


def _pass_through(reg_key: str, today: date | None) -> dict:
    """Anwendungsbeginn der Norm unveraendert durchreichen."""
    info = application_for(reg_key, today)
    return {"gilt_ab": info["applies_from"], "hinweis": info["note"]}


# ---------------------------------------------------------------------------
# Regulierungen mit Staffelung — je eine kleine Funktion.
# Signatur einheitlich: (profile, today) -> {"gilt_ab", "hinweis"}
# ---------------------------------------------------------------------------

def _csddd(profile: dict, today: date | None) -> dict:
    """CSDDD: seit der Aenderung durch RL (EU) 2026/470 KEIN Phase-in mehr.

    Art. 37 Abs. 1 der konsolidierten Fassung 02024L1760 nennt einen einzigen
    Anwendungsbeginn (26.07.2029) fuer alle erfassten Unternehmen; die frueheren
    Stufen 2027/2028/2029 nach Groesse sind entfallen. Die Funktion bleibt
    trotzdem stehen, damit die Herleitung an dieser Stelle dokumentiert ist.
    """
    return _pass_through("CSDDD", today)


def _lksg(profile: dict, today: date | None) -> dict:
    """LkSG: 3.000 Arbeitnehmer im Inland ab 2023, 1.000 ab 2024."""
    emp_de = profile.get("employees_de") or 0
    if emp_de >= 3000:
        return {"gilt_ab": _LKSG_STUFE_3000, "hinweis": "lksg_stufe_3000"}
    return {"gilt_ab": _LKSG_STUFE_1000, "hinweis": "lksg_stufe_1000"}


def _csrd(profile: dict, today: date | None) -> dict:
    """CSRD: neue Schwellen ab dem Geschaeftsjahr 2027, Welle 1 schon ab 2024.

    Die Welle-1-Pruefung steht bewusst VOR `csrd_status()`: ein boersen-
    notiertes Unternehmen mit mehr als 500 Beschaeftigten berichtet seit dem
    Geschaeftsjahr 2024, unabhaengig davon, ob es zusaetzlich die neuen
    Schwellen ueberschreitet. `csrd_status()` beantwortet die Frage OB, nicht
    die Frage AB WANN, und erreicht seinen Welle-1-Zweig nur fuer Unternehmen
    unterhalb der neuen Schwellen.
    Merkmale wie in `csrd_status()`: boersennotiert (grosses Unternehmen von
    oeffentlichem Interesse) und mehr als 500 Beschaeftigte.
    """
    if bool(profile.get("listed")) and (profile.get("employees") or 0) > 500:
        return {"gilt_ab": _CSRD_WELLE1, "hinweis": "csrd_welle1"}
    _applies, fact = csrd_status(profile)
    if fact == "csrd_drittland":
        # Art. 40a der Bilanzrichtlinie hat einen eigenen Anwendungsbeginn fuer
        # Drittland-Konzerne. Er laesst sich aus dem Profil nicht bestimmen —
        # lieber kein Datum als ein falsches.
        return {"gilt_ab": "", "hinweis": "csrd_drittland"}
    return {"gilt_ab": application_for("CSRD", today)["applies_from"],
            "hinweis": "csrd_neue_schwellen"}


def _csrd_de(profile: dict, today: date | None) -> dict:
    """CSRD-Umsetzungsgesetz: Verfahren nicht abgeschlossen, kein Datum."""
    return {"gilt_ab": "", "hinweis": "entwurf_de"}


def _esrs(profile: dict, today: date | None) -> dict:
    """ESRS: gelten mit dem ersten CSRD-pflichtigen Geschaeftsjahr.

    Art. 2 der Del. VO (EU) 2023/2772 nennt 01.01.2024 — das ist der Beginn
    fuer Welle 1. Ein Unternehmen, das erst ab dem Geschaeftsjahr 2027
    berichtspflichtig wird, wendet die Standards auch erst dann an.
    """
    csrd = _csrd(profile, today)
    if not csrd["gilt_ab"]:
        return {"gilt_ab": "", "hinweis": "esrs_folgt_csrd"}
    return {"gilt_ab": csrd["gilt_ab"], "hinweis": "esrs_folgt_csrd"}


def _taxonomie(profile: dict, today: date | None) -> dict:
    """Taxonomie-Offenlegung: an der CSRD-Pflicht, fuer Finanzunternehmen eigenstaendig."""
    if (profile.get("branch") or "") in regulations._FINANCIAL_BRANCHES:
        return {"gilt_ab": _TAXONOMIE_FINANZ, "hinweis": "taxonomie_finanz"}
    csrd = _csrd(profile, today)
    if not csrd["gilt_ab"]:
        return {"gilt_ab": "", "hinweis": "taxonomie_folgt_csrd"}
    return {"gilt_ab": csrd["gilt_ab"], "hinweis": "taxonomie_folgt_csrd"}


def _hinschg(profile: dict, today: date | None) -> dict:
    """HinSchG: interne Meldestelle ab 250 Beschaeftigten frueher als ab 50."""
    emp_de = profile.get("employees_de") or 0
    if emp_de >= 250:
        return {"gilt_ab": _HINSCHG_AB_250, "hinweis": "hinschg_ab_250"}
    return {"gilt_ab": _HINSCHG_AB_50, "hinweis": "hinschg_ab_50"}


def _whistleblower(profile: dict, today: date | None) -> dict:
    """Whistleblower-RL: Umsetzungsfrist gestaffelt wie beim HinSchG."""
    emp_de = profile.get("employees_de") or 0
    if emp_de >= 250:
        return {"gilt_ab": _WHISTLE_AB_250, "hinweis": "whistle_ab_250"}
    return {"gilt_ab": _WHISTLE_AB_50, "hinweis": "whistle_ab_50"}


def _eudr(profile: dict, today: date | None) -> dict:
    """EUDR: Kleinst- und Kleinunternehmen ein halbes Jahr spaeter.

    Art. 38 Abs. 3 stellt auf Kleinst-/Kleinunternehmen im Sinne des Art. 3
    Abs. 1 und 2 der RL 2013/34/EU ab, die am 31.12.2024 bereits als solche
    niedergelassen waren. Aus dem Profil laesst sich davon nur die Groesse
    ablesen: die spaetere Frist wird deshalb nur vergeben, wenn das Unternehmen
    BEIDE ablesbaren Merkmale (bis 50 Beschaeftigte, bis 15 Mio. EUR Umsatz)
    einhaelt. Im Zweifel gilt der fruehere Termin — das ist die Richtung, in
    der ein Irrtum nicht zu einer versaeumten Pflicht fuehrt.
    """
    emp = profile.get("employees") or 0
    rev = profile.get("revenue_eur") or 0
    if emp <= 50 and rev <= 15_000_000:
        return {"gilt_ab": _EUDR_KLEIN, "hinweis": "eudr_klein"}
    return _pass_through("EUDR", today)


def _greenclaims(profile: dict, today: date | None) -> dict:
    """Green Claims: Ruecknahme angekuendigt, kein Anwendungsbeginn."""
    return {"gilt_ab": "", "hinweis": "greenclaims"}


_RULES = {
    "CSDDD": _csddd,
    "LkSG": _lksg,
    "CSRD": _csrd,
    "CSRD_DE": _csrd_de,
    "ESRS": _esrs,
    "TaxonomieVO": _taxonomie,
    "HinSchG": _hinschg,
    "WhistleblowerRL": _whistleblower,
    "EUDR": _eudr,
    "GreenClaims": _greenclaims,
}


def deadline_for(reg_key: str, profile: dict, today: date | None = None) -> dict | None:
    """Anwendungsbeginn dieser Regulierung fuer dieses Unternehmen.

    None, wenn die Regulierung unbekannt ist. Sonst
    {"gilt_ab": "DD.MM.YYYY" oder "", "hinweis": "<Schluessel oder ''>"}.
    """
    if reg_key not in regulations.APPLICATION_BY_REG_KEY:
        return None
    rule = _RULES.get(reg_key)
    if rule is None:
        return _pass_through(reg_key, today)
    return rule(profile or {}, today)


def deadlines_for_profile(profile: dict, today: date | None = None) -> dict[str, dict]:
    """Alle Anwendungsbeginne fuer ein Profil: reg_key -> {gilt_ab, hinweis}."""
    out: dict[str, dict] = {}
    for reg_key in regulations.APPLICATION_BY_REG_KEY:
        result = deadline_for(reg_key, profile, today)
        if result is not None:
            out[reg_key] = result
    return out
