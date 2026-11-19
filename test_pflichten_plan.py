"""Tests zum Pflichten-Plan, Aufgabe 3: Plan je Konto.

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_plan.py

Kein Netz, kein LLM, festes `today`. Eigene DB `data/esg_pflichten_plan_test.db`.

Bloecke:
  A  Ohne Analyse: leerer Plan
  B  Erste Analyse: ja/moeglich im Plan, nein/error nicht
  C  Zweite Analyse (CSRD nein): entfaellt, Haekchen bleibt
  D  Dritte Analyse (CSRD error): Zustand unveraendert
  E  Ueberfaellig (fest 01.11.2026) und Erledigen
  F  Jaehrlicher Schritt: Periode und Verlauf
  G  Geaendert nach Abhaken, markiere_gesehen
  H  Sortierung: Ueberfaellige zuerst
  I  Zustaendig auf 120 Zeichen gekuerzt
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_plan_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import pflichten  # noqa: E402
import pflichten_db as pdb  # noqa: E402

_failures: list[str] = []

HEUTE = date(2026, 11, 19)


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def _karten(**applies: str) -> list[dict]:
    return [{"key": k, "name": f"{k} – Testname", "applies": v} for k, v in applies.items()]


def _pflicht(plan: dict, reg_key: str) -> dict | None:
    return next((p for p in plan["pflichten"] if p["reg_key"] == reg_key), None)


def _schritt(pflicht: dict, sid: int) -> dict | None:
    return next((s for s in pflicht["schritte"] if s["id"] == sid), None)


def _setze_frist(sid: int, typ: str, wert: str) -> None:
    with db._conn() as c:
        c.execute("UPDATE pflicht_schritte SET frist_typ = ?, frist_wert = ? WHERE id = ?",
                  (typ, wert, sid))


db.init_db()
UID = db.create_user("plan@example.org", "Geheim-Passwort-123")
db.upsert_company(UID, {"name": "Lederwaren Test GmbH", "employees": 120,
                        "materials": ["Leder"]})

EUDR = [s["id"] for s in pdb.schritte_fuer("EUDR", "de")]
CSRD = [s["id"] for s in pdb.schritte_fuer("CSRD", "de")]
assert len(EUDR) >= 2 and CSRD, "Startbestand fehlt"


def block_a() -> None:
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    check("A ohne Analyse: keine Pflichten", plan["pflichten"] == [], str(plan["pflichten"])[:80])
    check("A ohne Analyse: grundlage None", plan["grundlage"] is None)
    check("A Profil vorhanden", plan["hat_profil"] is True)


def block_b() -> None:
    db.save_analysis(UID, _karten(EUDR="ja", LkSG="nein", CSRD="moeglich", GPSR="error"))
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    keys = {p["reg_key"] for p in plan["pflichten"]}
    check("B EUDR und CSRD im Plan", {"EUDR", "CSRD"} <= keys, str(keys))
    check("B LkSG und GPSR nicht im Plan", not keys & {"LkSG", "GPSR"}, str(keys))
    check("B grundlage gesetzt", bool(plan["grundlage"]))
    eudr = _pflicht(plan, "EUDR")
    check("B Name aus der Karte", eudr["name"] == "EUDR – Testname", eudr["name"])
    check("B entfaellt False", eudr["entfaellt"] is False and eudr["entfallen_am"] is None)
    check("B gesamt = Anzahl aktiver Schritte", eudr["gesamt"] == len(EUDR)
          and eudr["erledigt"] == 0, f"{eudr['erledigt']}/{eudr['gesamt']}")
    s = eudr["schritte"][0]
    felder = {"id", "titel", "beschreibung", "daten", "rolle", "link", "quelle", "geprueft_am",
              "frist", "ueberfaellig", "erledigt", "erledigt_am", "zustaendig", "geaendert",
              "verlauf"}
    check("B Schritt-Felder vollstaendig", felder <= set(s), str(felder - set(s)))
    check("B gilt_ab aus deadline_for", isinstance(eudr["gilt_ab"], str))


def block_c() -> None:
    pdb.setze_erledigt(UID, CSRD[0], "", True, HEUTE)
    db.save_analysis(UID, _karten(EUDR="ja", LkSG="nein", CSRD="nein", GPSR="error"))
    spaeter = date(2026, 11, 25)
    plan = pflichten.plan_fuer(UID, "de", spaeter)
    csrd = _pflicht(plan, "CSRD")
    check("C CSRD entfaellt", csrd is not None and csrd["entfaellt"] is True)
    check("C entfallen_am = heute", csrd is not None and csrd["entfallen_am"] == spaeter.isoformat(),
          str(csrd and csrd["entfallen_am"]))
    s = _schritt(csrd, CSRD[0]) if csrd else None
    check("C Haekchen bleibt", bool(s) and s["erledigt"] is True)
    check("C entfallene stehen hinten", plan["pflichten"][-1]["reg_key"] == "CSRD",
          str([p["reg_key"] for p in plan["pflichten"]]))
    # Nochmals 'nein' an spaeterem Tag: Datum bleibt das erste
    plan = pflichten.plan_fuer(UID, "de", date(2026, 12, 1))
    check("C entfallen_am bleibt beim zweiten Lauf",
          _pflicht(plan, "CSRD")["entfallen_am"] == spaeter.isoformat())


def block_d() -> None:
    vorher = pflichten.plan_fuer(UID, "de", HEUTE)
    db.save_analysis(UID, _karten(EUDR="ja", LkSG="nein", CSRD="error", GPSR="error"))
    nachher = pflichten.plan_fuer(UID, "de", HEUTE)
    v, n = _pflicht(vorher, "CSRD"), _pflicht(nachher, "CSRD")
    check("D CSRD bei error unveraendert",
          n is not None and n["entfaellt"] == v["entfaellt"]
          and n["entfallen_am"] == v["entfallen_am"], f"{v and v['entfallen_am']} -> {n and n['entfallen_am']}")
    # error ohne Vorzustand legt nichts an
    check("D GPSR (error) weiter nicht im Plan", _pflicht(nachher, "GPSR") is None)
    # zurueck auf moeglich: entfaellt aufgehoben
    db.save_analysis(UID, _karten(EUDR="ja", LkSG="nein", CSRD="moeglich", GPSR="error"))
    wieder = _pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "CSRD")
    check("D moeglich hebt entfaellt auf", wieder["entfaellt"] is False
          and wieder["entfallen_am"] is None)


def block_e() -> None:
    _setze_frist(EUDR[0], "fest", "01.11.2026")
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), EUDR[0])
    check("E fest 01.11.2026 offen -> ueberfaellig", s["ueberfaellig"] is True,
          str(s["frist"]))
    pdb.setze_erledigt(UID, EUDR[0], "", True, HEUTE)
    p = _pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR")
    s = _schritt(p, EUDR[0])
    check("E nach Erledigen nicht ueberfaellig", s["ueberfaellig"] is False and s["erledigt"] is True)
    check("E erledigt_am gesetzt", s["erledigt_am"] == HEUTE.isoformat(), str(s["erledigt_am"]))
    check("E Zaehler 1 erledigt", p["erledigt"] == 1, str(p["erledigt"]))
    pdb.setze_erledigt(UID, EUDR[0], "", False, HEUTE)
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), EUDR[0])
    check("E Haekchen entfernen -> wieder ueberfaellig", s["erledigt"] is False
          and s["ueberfaellig"] is True and s["erledigt_am"] is None)


def block_f() -> None:
    sid = EUDR[1]
    _setze_frist(sid, "jaehrlich", "31.05.")
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), sid)
    check("F Periode 2027 am 19.11.2026", s["frist"]["periode"] == "2027", str(s["frist"]))
    pdb.setze_erledigt(UID, sid, "2027", True, HEUTE)
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), sid)
    check("F erledigt in Periode 2027", s["erledigt"] is True and s["verlauf"] == [],
          str(s["verlauf"]))
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", date(2027, 6, 1)), "EUDR"), sid)
    check("F am 01.06.2027 wieder offen", s["erledigt"] is False and s["frist"]["periode"] == "2028",
          str(s["frist"]))
    check("F Verlauf enthaelt 2027",
          s["verlauf"] == [{"periode": "2027", "erledigt_am": HEUTE.isoformat()}], str(s["verlauf"]))


def block_g() -> None:
    sid = EUDR[0]
    pdb.setze_erledigt(UID, sid, "", True, HEUTE)
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), sid)
    check("G frisch erledigt: nicht geaendert", s["geaendert"] is False)
    with db._conn() as c:
        c.execute("UPDATE pflicht_schritte SET version = version + 1, geaendert_am = ?"
                  " WHERE id = ?", ("2026-12-01", sid))
        version = c.execute("SELECT version FROM pflicht_schritte WHERE id = ?",
                            (sid,)).fetchone()[0]
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", date(2026, 12, 2)), "EUDR"), sid)
    check("G nach Aenderung: geaendert True", s["geaendert"] is True and s["erledigt"] is True)
    pdb.markiere_gesehen(UID, sid, version)
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", date(2026, 12, 2)), "EUDR"), sid)
    check("G nach markiere_gesehen: False", s["geaendert"] is False)
    # nicht erledigter geaenderter Schritt ist nie 'geaendert'
    with db._conn() as c:
        c.execute("UPDATE pflicht_schritte SET version = version + 1, geaendert_am = ?"
                  " WHERE id = ?", ("2026-12-01", CSRD[-1]))
    pdb.setze_erledigt(UID, CSRD[-1], "", False, HEUTE)
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", date(2026, 12, 2)), "CSRD"), CSRD[-1])
    check("G offener Schritt: geaendert False", s["geaendert"] is False)
    pdb.setze_erledigt(UID, sid, "", False, HEUTE)


def block_h() -> None:
    # EUDR: Schritt 0 ueberfaellig (fest 01.11.2026, offen); CSRD: spaetere Frist
    _setze_frist(CSRD[0], "fest", "31.12.2027")
    pdb.setze_erledigt(UID, CSRD[0], "", False, HEUTE)
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    keys = [p["reg_key"] for p in plan["pflichten"]]
    check("H ueberfaellige Pflicht vor spaeterer Frist",
          keys.index("EUDR") < keys.index("CSRD"), str(keys))
    csrd = _pflicht(plan, "CSRD")
    check("H naechste_frist CSRD = 31.12.2027", csrd["naechste_frist"] == date(2027, 12, 31),
          str(csrd["naechste_frist"]))
    # Ohne ueberfaelligen Schritt: Frist entscheidet; EUDR (31.05.2027) vor CSRD (31.12.2027)
    pdb.setze_erledigt(UID, EUDR[0], "", True, HEUTE)
    pdb.setze_erledigt(UID, EUDR[1], "2027", False, HEUTE)  # jaehrlicher Schritt wieder offen
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    keys = [p["reg_key"] for p in plan["pflichten"]]
    eudr = _pflicht(plan, "EUDR")
    check("H naechste_frist EUDR = jaehrlicher Stichtag 31.05.2027",
          eudr["naechste_frist"] == date(2027, 5, 31), str(eudr["naechste_frist"]))
    check("H fruehere Frist zuerst", keys.index("EUDR") < keys.index("CSRD"), str(keys))
    # Pflicht ohne Frist zuletzt (vor entfallenen)
    db.save_analysis(UID, _karten(EUDR="ja", CSRD="moeglich", LkSG="ja"))
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    lksg = _pflicht(plan, "LkSG")
    keys = [p["reg_key"] for p in plan["pflichten"]]
    check("H Pflicht ohne Frist hinten", lksg["naechste_frist"] is None and keys[-1] == "LkSG",
          str(keys))


def block_i() -> None:
    pdb.setze_zustaendig(UID, EUDR[0], "  " + "x" * 200 + "  ")
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), EUDR[0])
    check("I zustaendig auf 120 Zeichen", s["zustaendig"] == "x" * 120, str(len(s["zustaendig"] or "")))
    pdb.setze_zustaendig(UID, EUDR[0], "   ")
    s = _schritt(_pflicht(pflichten.plan_fuer(UID, "de", HEUTE), "EUDR"), EUDR[0])
    check("I leer -> None", s["zustaendig"] is None)
    check("I ROLLEN", pflichten.ROLLEN == ["gf", "einkauf", "personal", "logistik", "produkt",
                                           "nachhaltigkeit", "finanzen"])


def block_j() -> None:
    uid2 = db.create_user("ohneprofil@example.org", "Geheim-Passwort-123")
    db.save_analysis(uid2, _karten(EUDR="ja"))
    plan = pflichten.plan_fuer(uid2, "en", HEUTE)
    eudr = _pflicht(plan, "EUDR")
    check("J ohne Profil: hat_profil False, Anker leer",
          plan["hat_profil"] is False and eudr is not None and eudr["gilt_ab"] == "",
          str(eudr and eudr["gilt_ab"]))
    check("J Konten getrennt: kein Haekchen von Konto 1",
          all(not s["erledigt"] for s in eudr["schritte"]))


for block in (block_a, block_b, block_c, block_d, block_e, block_f, block_g, block_h,
              block_i, block_j):
    block()

print()
if _failures:
    print(f"{len(_failures)} Fehler: {', '.join(_failures)}")
    sys.exit(1)
print("Alle Pruefungen bestanden.")
