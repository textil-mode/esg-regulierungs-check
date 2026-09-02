"""Schwellen-Naehe (Was-waere-wenn) — deterministisch, kein LLM.

Die Karten beantworten "greift / greift nicht" fuer den heutigen Stand. Ein
Unternehmen, das 950 Beschaeftigte in Deutschland hat, faellt heute nicht unter
das LkSG — bei 1.000 aber schon. Dieses Modul macht solche Naehe sichtbar,
BEVOR sie eintritt.

Geprueft werden nur die zahlengebundenen Schwellen, die sich aus dem Profil
ablesen lassen: LkSG (1.000 Arbeitnehmer im Inland), HinSchG (50 Beschaeftigte
im Inland), CSRD (1.000 Beschaeftigte UND 450 Mio. EUR) und CSDDD (5.000
Beschaeftigte UND 1.500 Mio. EUR). Naehe heisst: innerhalb von 20 Prozent
unterhalb oder oberhalb der Schwelle.

Die Vergleichsoperatoren folgen exakt dem Gesetzeswortlaut und damit den
Statusfunktionen in `regulations.py`: LkSG und HinSchG sagen "mindestens"
(>=), CSRD und CSDDD sagen "mehr als" (>).

Rueckgabe: Liste von {"key": "<i18n-Schluessel>", "values": {...}} in fester
Reihenfolge. Der Text steht in `i18n.THRESHOLD_HINTS` in sechs Sprachen.
Berechnung zur Renderzeit — nichts davon beruehrt den Begruendungs-Cache.
"""
from __future__ import annotations

_BAND = 0.20

# Schwellen. Fundstellen: § 1 Abs. 1 Nr. 2 LkSG; § 12 Abs. 1 HinSchG;
# Art. 19a Abs. 1 Bilanz-RL i.d.F. RL (EU) 2026/470; Art. 2 Abs. 1 CSDDD
# i.d.F. RL (EU) 2026/470.
_LKSG_MA = 1000
_HINSCHG_MA = 50
_CSRD_MA = 1000
_CSRD_UMSATZ = 450_000_000
_CSDDD_MA = 5000
_CSDDD_UMSATZ = 1_500_000_000


def _unter(value: float, threshold: float) -> bool:
    """Innerhalb des 20-Prozent-Bandes unterhalb der Schwelle."""
    return threshold * (1 - _BAND) <= value <= threshold


def _ueber(value: float, threshold: float) -> bool:
    """Innerhalb des 20-Prozent-Bandes oberhalb der Schwelle."""
    return threshold <= value <= threshold * (1 + _BAND)


def _zwei_merkmale(emp: float, rev: float, ma_schwelle: int, umsatz_schwelle: int
                   ) -> str:
    """Naehe zu einer Schwelle aus ZWEI kumulativen Merkmalen (CSRD, CSDDD).

    Liefert "unter", "ueber" oder "" (keine Naehe).

    "unter": mindestens ein Merkmal ist noch nicht erfuellt, und jedes nicht
    erfuellte liegt im 20-Prozent-Band darunter — das Unternehmen waere also
    mit einem ueberschaubaren Wachstum erfasst.
    "ueber": beide Merkmale sind erfuellt, mindestens eines aber nur knapp.
    """
    emp_erfuellt = emp > ma_schwelle
    rev_erfuellt = rev > umsatz_schwelle
    if emp_erfuellt and rev_erfuellt:
        if _ueber(emp, ma_schwelle) or _ueber(rev, umsatz_schwelle):
            return "ueber"
        return ""
    emp_nah = emp_erfuellt or _unter(emp, ma_schwelle)
    rev_nah = rev_erfuellt or _unter(rev, umsatz_schwelle)
    return "unter" if (emp_nah and rev_nah) else ""


def near_thresholds(profile: dict) -> list[dict]:
    """Hinweise zur Schwellen-Naehe fuer dieses Profil (ggf. leere Liste)."""
    profile = profile or {}
    emp = profile.get("employees") or 0
    emp_de = profile.get("employees_de") or 0
    rev = profile.get("revenue_eur") or 0

    hints: list[dict] = []
    values = {"employees": emp, "employees_de": emp_de, "revenue_eur": rev}

    # LkSG — § 1 Abs. 1 Nr. 2: "in der Regel mindestens 1 000 Arbeitnehmer".
    if emp_de >= _LKSG_MA:
        if _ueber(emp_de, _LKSG_MA):
            hints.append({"key": "lksg_knapp_darueber", "values": values})
    elif _unter(emp_de, _LKSG_MA):
        hints.append({"key": "lksg_knapp_darunter", "values": values})

    # HinSchG — § 12 Abs. 1: "in der Regel mindestens 50 Beschaeftigte".
    if emp_de >= _HINSCHG_MA:
        if _ueber(emp_de, _HINSCHG_MA):
            hints.append({"key": "hinschg_knapp_darueber", "values": values})
    elif _unter(emp_de, _HINSCHG_MA):
        hints.append({"key": "hinschg_knapp_darunter", "values": values})

    # CSRD — beide Merkmale kumulativ, "mehr als".
    lage = _zwei_merkmale(emp, rev, _CSRD_MA, _CSRD_UMSATZ)
    if lage:
        hints.append({"key": f"csrd_knapp_dar{lage}", "values": values})

    # CSDDD — beide Merkmale kumulativ, "mehr als".
    lage = _zwei_merkmale(emp, rev, _CSDDD_MA, _CSDDD_UMSATZ)
    if lage:
        hints.append({"key": f"csddd_knapp_dar{lage}", "values": values})

    return hints
