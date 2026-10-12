"""Tests zum nationalen Medizinprodukterecht (12.10.2026): MPDG, MPAMIV, MPBetreibV.

Ausfuehren:  ./.venv/Scripts/python.exe test_medizinprodukte.py

Kein Netz, kein LLM. Eigene DB `data/esg_medizin_test.db`; die Produktiv-DB
wird nicht beruehrt.

Bloecke:
  A  Regelbasierte Entscheidungen je Profil (inkl. MDR mit Zusatzfrage)
  B  Jeder erreichbare Fall hat Texte in sechs Sprachen (sonst ginge er ans LLM)
  C  Ausblenden: ohne Medizintextilien keine Karte, im PDF ebenso
  D  Profilfeld `medical_activities`: Speichern, Lesen, unbekannte Werte
  E  Formular: Zusatzfrage nur bei der Kategorie, Speichern ueber /save-company
  F  Katalog: Stammdaten, Fristen, erste Schritte, Leitlinien
"""
from __future__ import annotations

import itertools
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_medizin_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
BASIS = "https://test.example"
os.environ["PUBLIC_BASE_URL"] = BASIS
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import deadlines  # noqa: E402
import i18n  # noqa: E402
import llm  # noqa: E402
import regulations as regs  # noqa: E402
import app as flaskapp  # noqa: E402
from pdfexport import render_pdf  # noqa: E402
from views import render_cards_html  # noqa: E402

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


KAT = "Medizin- und Gesundheitstextilien"
HERSTELLER_ROLLE = regs.VALUE_CHAIN_ROLES[0]
ZULIEFERER = "Zulieferer"
NEU = ["MPDG", "MPAMIV", "MPBetreibV"]
H, HA, AUF, KEINE, UNKLAR = (regs.MED_HERSTELLER, regs.MED_HANDEL, regs.MED_AUFBEREITUNG,
                             regs.MED_KEINE, regs.MED_UNKLAR)
LANGS = ["de", "en", "es", "fr", "it", "zh"]


def med(*acts, **extra) -> dict:
    return {"product_categories": [KAT], "medical_activities": list(acts), **extra}


def ausgang(key: str, profile: dict) -> str:
    return regs.coupling_verdict(key, profile)["applies"]


# ---------------------------------------------------------------------------
def block_a() -> None:
    print("\n--- A  Regelbasierte Entscheidungen ---")
    faelle = [
        # Ohne Kategorie: alles nein (und ausgeblendet, siehe C)
        ("MPDG", {"product_categories": ["Schuhe"], "medical_activities": [H]}, "nein"),
        ("MPAMIV", {}, "nein"),
        ("MPBetreibV", {"product_categories": ["Bekleidung und Bekleidungszubehör"]}, "nein"),
        # Hersteller
        ("MPDG", med(H), "ja"),
        ("MPAMIV", med(H), "ja"),
        ("MPBetreibV", med(H), "nein"),
        ("MDR", med(H), "ja"),
        # Import/Handel: MPAMIV verpflichtet sie nicht (Art. 13/14 MDR + § 81 MPDG)
        ("MPDG", med(HA), "ja"),
        ("MPAMIV", med(HA), "nein"),
        ("MPBetreibV", med(HA), "nein"),
        ("MDR", med(HA), "ja"),
        # Aufbereitung (Textilservice, OP-Textilien)
        ("MPDG", med(AUF), "ja"),
        ("MPAMIV", med(AUF), "moeglich"),
        ("MPBetreibV", med(AUF), "ja"),
        ("MDR", med(AUF), "moeglich"),
        # Hersteller UND Aufbereiter: jede Pflicht greift
        ("MPAMIV", med(H, AUF), "ja"),
        ("MPBetreibV", med(H, AUF), "ja"),
        # Keine Zweckbestimmung: alles nein, auch die MDR
        ("MPDG", med(KEINE), "nein"),
        ("MPAMIV", med(KEINE), "nein"),
        ("MPBetreibV", med(KEINE), "nein"),
        ("MDR", med(KEINE), "nein"),
        # "Keine" neben einer Taetigkeit zaehlt nicht als "keine"
        ("MPDG", med(KEINE, HA), "ja"),
        # Unklar / leer (Altprofil): pruefen
        ("MPDG", med(UNKLAR), "moeglich"),
        ("MPAMIV", med(), "moeglich"),
        ("MPBetreibV", med(), "moeglich"),
        ("MDR", med(), "moeglich"),
        ("MDR", med(UNKLAR), "moeglich"),
        # Zulieferer ohne Angabe: pruefen; mit Herstellerangabe: die Angabe zaehlt
        ("MPDG", med(value_chain_roles=[ZULIEFERER]), "moeglich"),
        ("MDR", med(value_chain_roles=[ZULIEFERER]), "moeglich"),
        ("MDR", med(H, value_chain_roles=[ZULIEFERER]), "ja"),
        # Nur ausserhalb EU/EWR: nein — auch fuer die MDR wie bisher
        ("MPDG", med(H, sales_markets=["außerhalb EU/EWR"]), "nein"),
        ("MDR", med(H, sales_markets=["außerhalb EU/EWR"]), "nein"),
        # Bisheriger MDR-Fall (Kategorie + Herstellerrolle, ohne Zusatzfrage) bleibt "moeglich"
        ("MDR", {"product_categories": [KAT], "value_chain_roles": [HERSTELLER_ROLLE]}, "moeglich"),
    ]
    for key, profile, erwartet in faelle:
        ist = ausgang(key, profile)
        check(f"A {key:10s} {sorted(profile.get('medical_activities') or [])!s:.60} -> {erwartet}",
              ist == erwartet, f"ist {ist}")


# ---------------------------------------------------------------------------
def _alle_profile():
    """Kombinationen, die jeden Zweig der vier Statusfunktionen erreichen."""
    akte = [(), (H,), (HA,), (AUF,), (KEINE,), (UNKLAR,), (H, AUF), (HA, AUF)]
    rollen = [[], [ZULIEFERER], [HERSTELLER_ROLLE]]
    maerkte = [[], ["Deutschland"], ["außerhalb EU/EWR"]]
    kategorien = [[], [KAT]]
    for a, r, m, k in itertools.product(akte, rollen, maerkte, kategorien):
        yield {"product_categories": k, "medical_activities": list(a),
               "value_chain_roles": r, "sales_markets": m}


def block_b() -> None:
    print("\n--- B  Texte fuer jeden erreichbaren Fall ---")
    keys = NEU + ["MDR"]
    by_key = {r["key"]: r for r in regs.REGULATIONS}
    luecken = []
    faelle = set()
    for profile in _alle_profile():
        for key in keys:
            v = regs.coupling_verdict(key, profile)
            faelle.add((key, v["fact"], v["conclusion"]))
            for lang in LANGS:
                res = llm.deterministic_result(by_key[key], profile, lang)
                if res is None:
                    luecken.append((key, v["fact"], v["conclusion"], lang))
    check(f"B {len(faelle)} Faelle x 6 Sprachen ohne LLM entschieden", not luecken,
          str(luecken[:5]))
    # Chinesisch ohne Leerzeichen zwischen den Saetzen, die anderen mit
    res_zh = llm.deterministic_result(by_key["MPDG"], med(H), "zh")
    res_de = llm.deterministic_result(by_key["MPDG"], med(H), "de")
    check("B Satztrennung DE mit, ZH ohne Leerzeichen",
          "。 " not in res_zh["reason"] and ". Für" in res_de["reason"])
    # Begruendung nennt keine Pflicht, die das Profil nicht traegt
    res = llm.deterministic_result(by_key["MPAMIV"], med(HA), "de")
    check("B MPAMIV bei Handel verweist auf § 81 MPDG", "§ 81 MPDG" in res["reason"], res["reason"])


# ---------------------------------------------------------------------------
def _lauf(profile: dict, lang: str = "de") -> list[dict]:
    """Ergebnisse wie im Analyse-Lauf — nur die regelbasierten Regulierungen."""
    out = []
    for reg in regs.REGULATIONS:
        res = llm.deterministic_result(reg, profile, lang)
        if res is not None:
            out.append(res)
    return out


def block_c() -> None:
    print("\n--- C  Ausblenden ohne Medizintextilien ---")
    ohne = _lauf({"product_categories": ["Bekleidung und Bekleidungszubehör"]})
    mit = _lauf(med(H))
    versteckt = sorted(r["key"] for r in ohne if r.get("hidden"))
    check("C ohne Kategorie: genau die drei neuen versteckt", versteckt == sorted(NEU), str(versteckt))
    check("C MDR bleibt sichtbar (nicht einschlaegig)",
          any(r["key"] == "MDR" and not r.get("hidden") and r["applies"] == "nein" for r in ohne))
    check("C mit Kategorie: nichts versteckt", not any(r.get("hidden") for r in mit))
    # "keine Zweckbestimmung" bleibt sichtbar: der Nutzer hat die Kategorie gewaehlt
    keine = _lauf(med(KEINE))
    check("C Kategorie + keine Zweckbestimmung: sichtbar", not any(r.get("hidden") for r in keine))

    html_ohne = render_cards_html(ohne, "de")
    html_mit = render_cards_html(mit, "de")
    check("C Karten: MPDG fehlt ohne Kategorie", "MPDG –" not in html_ohne)
    check("C Karten: MPDG, MPAMIV, MPBetreibV mit Kategorie",
          all(n in html_mit for n in ("MPDG –", "MPAMIV –", "MPBetreibV –")))
    # Zaehler: die versteckten Karten zaehlen nicht als "nicht einschlaegig"
    nein_sichtbar = sum(1 for r in ohne if r["applies"] == "nein" and not r.get("hidden"))
    check("C Zaehler ohne die versteckten",
          f'<div class="metric-value">{nein_sichtbar}</div><div class="metric-label">' in html_ohne)
    pdf = render_pdf(ohne, "de", profile={"name": "Test", "product_categories": []})
    check("C PDF entsteht", isinstance(pdf, (bytes, bytearray)) and pdf[:4] == b"%PDF")


# ---------------------------------------------------------------------------
def block_d() -> None:
    print("\n--- D  Profilfeld medical_activities ---")
    uid = db.create_user("medtex@example.org", "ein-gutes-Passwort-2026")
    db.upsert_company(uid, {"name": "X", "employees": 10, "branch": regs.BRANCHES[0],
                            "product_categories": [KAT],
                            "medical_activities": [AUF, "Erfunden", H]})
    c = db.get_company(uid)
    check("D gespeichert in Listenreihenfolge, Unbekanntes verworfen",
          c["medical_activities"] == [H, AUF], str(c["medical_activities"]))
    uid2 = db.create_user("alt@example.org", "ein-gutes-Passwort-2026")
    db.upsert_company(uid2, {"name": "Y", "employees": 10, "branch": regs.BRANCHES[0]})
    check("D Altprofil ohne Angabe -> leere Liste", db.get_company(uid2)["medical_activities"] == [])
    check("D im Prompt beschriftet", "medical_activities" in llm._PROFILE_LABELS
          and "medical_activities" in llm._LIST_FIELDS)
    for key in NEU + ["MDR"]:
        reg = next(r for r in regs.REGULATIONS if r["key"] == key)
        check(f"D {key}: Feld in relevant_fields", "medical_activities" in reg["relevant_fields"])


# ---------------------------------------------------------------------------
def block_e() -> None:
    print("\n--- E  Formular ---")
    uid = db.create_user("formular@example.org", "ein-gutes-Passwort-2026")
    c = flaskapp.app.test_client()
    with c.session_transaction() as sess:
        sess["user_id"] = uid
        sess["ui_language"] = "de"

    def seite() -> str:
        return c.get("/dashboard").get_data(as_text=True)

    db.upsert_company(uid, {"name": "Z", "employees": 10, "branch": regs.BRANCHES[0],
                            "product_categories": ["Schuhe"]})
    html = seite()
    check("E Block vorhanden, aber versteckt ohne Kategorie",
          'id="medical-block"' in html and 'data-category="Medizin- und Gesundheitstextilien" hidden' in html)
    db.upsert_company(uid, {"name": "Z", "employees": 10, "branch": regs.BRANCHES[0],
                            "product_categories": [KAT], "medical_activities": [AUF]})
    html = seite()
    check("E Block sichtbar mit Kategorie, Haken gesetzt",
          'data-category="Medizin- und Gesundheitstextilien" >' in html
          and f'value="{AUF}" id="med_3" checked' in html)
    check("E Ausfuellhilfe und Ueberschrift", "Tätigkeit mit Medizinprodukten" in html)

    r = c.post("/save-company", data={
        "name": "Z", "employees": "10", "branch": regs.BRANCHES[0],
        "product_categories": [KAT], "medical_activities": [H, HA],
    }, headers={"Origin": BASIS})
    gespeichert = db.get_company(uid)["medical_activities"]
    check("E /save-company speichert die Mehrfachauswahl", r.status_code == 302 and gespeichert == [H, HA],
          f"{r.status_code} {gespeichert}")

    with c.session_transaction() as sess:
        sess["ui_language"] = "en"
    html = seite()
    check("E Englische Beschriftung", "Activities involving medical devices" in html
          and "Manufacturer of medical devices" in html)


# ---------------------------------------------------------------------------
def block_f() -> None:
    print("\n--- F  Katalog ---")
    by_key = {r["key"]: r for r in regs.REGULATIONS}
    for key in NEU:
        reg = by_key.get(key)
        check(f"F {key} im Katalog", reg is not None)
        if not reg:
            continue
        check(f"F {key}: Quelle gesetze-im-internet.de (Volltext)",
              reg["text_url"].startswith("https://www.gesetze-im-internet.de/")
              and "/BJNR" in reg["text_url"])
        check(f"F {key}: Veroeffentlichung + Anwendung", regs.published_for(key) != "—"
              and regs.application_for(key)["applies_from"])
        check(f"F {key}: Leitlinien", len(regs.guidelines_for(key)) >= 1)
        steps = regs.first_steps_for(key)
        check(f"F {key}: erste Schritte in 6 Sprachen",
              2 <= len(steps) <= 5 and all(i18n.t_first_step(s, l) for s in steps for l in LANGS))
        check(f"F {key}: Frist ableitbar", deadlines.deadline_for(key, med(H)) is not None)
    check("F MPBetreibV: Neufassung 2025 (nicht die abgeloeste Adresse)",
          "mpbetreibv_2025" in by_key["MPBetreibV"]["text_url"])
    check("F MDR: MPAV-Hinweis als fuenfter Schritt", regs.first_steps_for("MDR")[-1] == "mdr_5"
          and "MPAV" in i18n.t_first_step("mdr_5", "de"))
    check("F Nummern eindeutig", len({r["nr"] for r in regs.REGULATIONS}) == len(regs.REGULATIONS))
    check("F Auswahlliste uebersetzt",
          all(i18n.t_opt(v, i18n.MEDICAL_ACTIVITY_LABELS, l) for v in regs.MEDICAL_ACTIVITIES for l in LANGS)
          and set(i18n.MEDICAL_ACTIVITY_LABELS) == set(regs.MEDICAL_ACTIVITIES))
    check("F Ausfuellhilfe in 6 Sprachen", all(i18n.t_help("medical", l) for l in LANGS))


if __name__ == "__main__":
    for block in (block_a, block_b, block_c, block_d, block_e, block_f):
        block()
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER:")
        for f in _failures:
            print("  -", f)
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
