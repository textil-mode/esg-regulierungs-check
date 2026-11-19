"""Pflichten-Plan: Fristen-Regeln und Plan-Logik.

Reine Funktionen, keine Importe mit Nebenwirkung.
"""
from __future__ import annotations

import calendar
import re
from datetime import date, datetime, timedelta

_KEINE = {"art": "keine", "datum": None, "periode": ""}


def _keine() -> dict:
    return dict(_KEINE)


def _tag_monat_jahr(text: str) -> date | None:
    m = re.fullmatch(r"\s*(\d{1,2})\.(\d{1,2})\.(\d{4})\s*", text or "")
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def _monate_addieren(d: date, n: int) -> date:
    idx = d.year * 12 + (d.month - 1) + n
    jahr, monat = divmod(idx, 12)
    monat += 1
    return date(jahr, monat, min(d.day, calendar.monthrange(jahr, monat)[1]))


def _stichtag(jahr: int, tag: int, monat: int) -> date:
    return date(jahr, monat, min(tag, calendar.monthrange(jahr, monat)[1]))


def frist_fuer(frist_typ: str, frist_wert: str, gilt_ab: str, today: date) -> dict:
    """Berechnet die Frist einer Pflicht. Wirft nie; ungueltig -> art 'keine'."""
    try:
        if isinstance(today, datetime):
            today = today.date()
        typ = (frist_typ or "").strip()
        wert = (frist_wert or "").strip()
        if typ == "fest":
            d = _tag_monat_jahr(wert)
            if d is None:
                return _keine()
            return {"art": "datum", "datum": d, "periode": ""}
        if typ == "jaehrlich":
            m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.", wert)
            if not m:
                return _keine()
            tag, monat = int(m.group(1)), int(m.group(2))
            if not (1 <= monat <= 12 and 1 <= tag <= calendar.monthrange(2024, monat)[1]):
                return _keine()
            d = _stichtag(today.year, tag, monat)
            if d < today:
                d = _stichtag(today.year + 1, tag, monat)
            return {"art": "datum", "datum": d, "periode": str(d.year)}
        if typ == "relativ":
            m = re.fullmatch(r"([+-])(\d+)([md])", wert)
            if not m:
                return _keine()
            anker_text = (gilt_ab or "").strip()
            if not anker_text:
                return {"art": "offen", "datum": None, "periode": ""}
            anker = _tag_monat_jahr(anker_text)
            if anker is None:
                return _keine()
            n = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
            if m.group(3) == "m":
                d = _monate_addieren(anker, n)
            else:
                d = anker + timedelta(days=n)
            if anker <= today and not (n > 0 and d > today):
                return {"art": "laufend", "datum": None, "periode": ""}
            return {"art": "datum", "datum": d, "periode": ""}
        return _keine()
    except Exception:
        return _keine()
