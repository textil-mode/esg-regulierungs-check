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


# ---------- Plan je Konto ----------

ROLLEN = ["gf", "einkauf", "personal", "logistik", "produkt", "nachhaltigkeit", "finanzen"]


def _geaendert(schritt: dict, erledigt_am: str | None, gesehen: int | None) -> bool:
    if not erledigt_am or not schritt.get("geaendert_am"):
        return False
    return (str(schritt["geaendert_am"]) > str(erledigt_am)
            and (gesehen or 0) < int(schritt.get("version") or 1))


def _schritt_im_plan(s: dict, gilt_ab: str, today: date, zustand: dict,
                     erledigungen: dict[str, str]) -> dict:
    frist = frist_fuer(s.get("frist_typ"), s.get("frist_wert"), gilt_ab, today)
    jaehrlich = (s.get("frist_typ") or "").strip() == "jaehrlich"
    periode = frist["periode"] if jaehrlich else ""
    erledigt_am = erledigungen.get(periode)
    erledigt = erledigt_am is not None
    verlauf = []
    if jaehrlich:
        verlauf = [{"periode": p, "erledigt_am": d}
                   for p, d in sorted(erledigungen.items(), reverse=True)
                   if p and p != periode]
    return {
        "id": s["id"], "titel": s.get("titel", ""), "beschreibung": s.get("beschreibung", ""),
        "daten": s.get("daten", ""), "rolle": s.get("rolle", ""), "link": s.get("link"),
        "quelle": s.get("quelle"), "geprueft_am": s.get("geprueft_am"),
        "frist": frist,
        "ueberfaellig": (frist["art"] == "datum" and frist["datum"] < today and not erledigt),
        "erledigt": erledigt, "erledigt_am": erledigt_am,
        "zustaendig": zustand.get("zustaendig"),
        "geaendert": erledigt and _geaendert(s, erledigt_am, zustand.get("gesehen_version")),
        "verlauf": verlauf,
    }


def plan_fuer(user_id: int, lang: str, today: date) -> dict:
    """Plan 'Meine Pflichten' eines Kontos aus dem letzten Pruefergebnis.

    Gleicht vorher `nutzer_pflichten` per `sync_pflichten` ab. Fristen werden
    bei jedem Aufruf neu berechnet (aktuelles Profil, `deadline_for`).
    """
    import db
    import deadlines
    import pflichten_db as pdb
    import regulations as regs

    if isinstance(today, datetime):
        today = today.date()
    company = db.get_company(user_id)
    profil = company or {}
    analyse = db.latest_analysis(user_id)
    plan = {"grundlage": analyse["created_at"] if analyse else None,
            "hat_profil": company is not None, "pflichten": []}
    if not analyse:
        return plan

    karten = {k["key"]: k for k in (analyse.get("result") or [])
              if isinstance(k, dict) and k.get("key")}
    pdb.sync_pflichten(user_id, {k: v.get("applies") for k, v in karten.items()}, today)
    zustaende, erledigt = pdb.nutzer_zustand(user_id)
    namen = {r["key"]: r.get("name", r["key"]) for r in regs.REGULATIONS}

    for zeile in pdb.nutzer_pflichten(user_id):
        reg_key = zeile["reg_key"]
        gilt_ab = ""
        if company is not None:
            info = deadlines.deadline_for(reg_key, profil, today)
            gilt_ab = (info or {}).get("gilt_ab") or ""
        schritte = [
            _schritt_im_plan(s, gilt_ab, today, zustaende.get(s["id"], {}),
                             erledigt.get(s["id"], {}))
            for s in pdb.schritte_fuer(reg_key, lang)
        ]
        offene_daten = [s["frist"]["datum"] for s in schritte
                        if not s["erledigt"] and s["frist"]["art"] == "datum"]
        plan["pflichten"].append({
            "reg_key": reg_key,
            "name": (karten.get(reg_key) or {}).get("name") or namen.get(reg_key, reg_key),
            "gilt_ab": gilt_ab,
            "entfaellt": zeile["entfallen_am"] is not None,
            "entfallen_am": zeile["entfallen_am"],
            "erledigt": sum(1 for s in schritte if s["erledigt"]),
            "gesamt": len(schritte),
            "naechste_frist": min(offene_daten) if offene_daten else None,
            "schritte": schritte,
        })

    plan["pflichten"].sort(key=lambda p: (
        p["entfaellt"],
        not any(s["ueberfaellig"] for s in p["schritte"]),
        p["naechste_frist"] is None,
        p["naechste_frist"] or date.max,
        p["name"].casefold(),
    ))
    return plan
