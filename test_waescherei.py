"""Tests zur Nutzervorgabe vom 12.10.2026: Waescherei (AbwV Anhang 55),
Geschaeftsmodell / Taetigkeitsbereich, neue Hilfetexte und Beschriftungen,
Hinweis vor dem Pruefergebnis.

Ausfuehren:  ./.venv/Scripts/python.exe test_waescherei.py

Kein Netz, kein LLM. Eigene DB `data/esg_waescherei_test.db`.

Bloecke:
  A  AbwV55: Entscheidungen je Profil
  B  AbwV55: Texte fuer jeden Fall in sechs Sprachen (sonst ginge er ans LLM)
  C  Neue Profilfelder: Speichern, Lesen, unbekannte Werte, Altprofil
  D  Vorgabetexte zeichengenau (Hilfetexte, Beschriftungen, Ergebnis-Hinweis)
  E  Formular und Ergebnisseite
  F  Katalog: Stammdaten, Fristen, erste Schritte, Leitlinien
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_waescherei_test.db"
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
from views import render_cards_html  # noqa: E402

_failures: list[str] = []
LANGS = ["de", "en", "es", "fr", "it", "zh"]
WAESCHEREI = "Gewerbliche Wäscherei / Textilreinigung"
TEXTILSERVICE = "Textilservice / Full-Service-Versorgung"
PRODUKTION = "Produktionsstätte / Werk (Herstellung, Verarbeitung oder Veredelung)"


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


# ---------------------------------------------------------------------------
def block_a() -> None:
    print("\n--- A  AbwV55 ---")
    faelle = [
        ({"laundry_de": True}, "ja"),
        ({"laundry_de": True, "business_activities": ["Herstellung von Textilien oder Bekleidung"]}, "ja"),
        ({"business_activities": [WAESCHEREI]}, "moeglich"),
        ({"business_activities": [TEXTILSERVICE]}, "moeglich"),
        ({"business_activities": ["Vermietung / Leasing von Textilien"]}, "nein"),
        ({"branch": "Wäscherei und chemische Reinigung"}, "moeglich"),
        ({"branch": "Weberei"}, "nein"),
        ({}, "nein"),
        # Anhang 38 (Veredlung) und Anhang 55 sind getrennte Fragen
        ({"wet_processing_de": True}, "nein"),
    ]
    for profil, erwartet in faelle:
        ist = regs.coupling_verdict("AbwV55", profil)["applies"]
        check(f"A {profil} -> {erwartet}", ist == erwartet, f"ist {ist}")
    check("A AbwV38 unberuehrt vom Waescherei-Haekchen",
          regs.coupling_verdict("AbwV38", {"laundry_de": True})["applies"] == "nein")


def block_b() -> None:
    print("\n--- B  Texte ---")
    reg = next(r for r in regs.REGULATIONS if r["key"] == "AbwV55")
    profile = [{"laundry_de": True}, {"business_activities": [WAESCHEREI]},
               {"branch": "Wäscherei und chemische Reinigung"}, {}]
    luecken = [(p, l) for p in profile for l in LANGS if llm.deterministic_result(reg, p, l) is None]
    check("B alle Faelle x 6 Sprachen ohne LLM", not luecken, str(luecken))
    de = llm.deterministic_result(reg, {"laundry_de": True}, "de")
    check("B Begruendung nennt die Ausnahme fuer Hotelwaesche",
          "Hoteltextilien ohne chlorhaltige Waschmittel" in de["reason"], de["reason"])
    en = llm.deterministic_result(reg, {"branch": "Wäscherei und chemische Reinigung"}, "en")
    check("B Branche in der Begruendung wie in der Branchenliste",
          i18n.BRANCH_LABELS["Wäscherei und chemische Reinigung"]["en"] in en["reason"])


# ---------------------------------------------------------------------------
def block_c() -> None:
    print("\n--- C  Profilfelder ---")
    uid = db.create_user("waesche@example.org", "ein-gutes-Passwort-2026")
    db.upsert_company(uid, {"name": "W", "employees": 10, "branch": regs.BRANCHES[0],
                            "laundry_de": True,
                            "business_activities": [TEXTILSERVICE, "Erfunden", WAESCHEREI]})
    c = db.get_company(uid)
    check("C Haekchen gespeichert", c["laundry_de"] is True)
    check("C Taetigkeiten in Listenreihenfolge, Unbekanntes verworfen",
          c["business_activities"] == [WAESCHEREI, TEXTILSERVICE], str(c["business_activities"]))
    uid2 = db.create_user("alt2@example.org", "ein-gutes-Passwort-2026")
    db.upsert_company(uid2, {"name": "A", "employees": 10, "branch": regs.BRANCHES[0]})
    c2 = db.get_company(uid2)
    check("C Altprofil: Haekchen aus, Liste leer",
          c2["laundry_de"] is False and c2["business_activities"] == [])
    check("C im Prompt beschriftet",
          "laundry_de" in llm._BOOL_FIELDS and "business_activities" in llm._LIST_FIELDS
          and {"laundry_de", "business_activities"} <= set(llm._PROFILE_LABELS))
    # Geschaeftsmodell geht in keinen LLM-Prompt (Cache der uebrigen bleibt)
    llm_regs = [r for r in regs.REGULATIONS if r["key"] not in regs._COUPLINGS]
    check("C Geschaeftsmodell in keinem LLM-Prompt",
          not any("business_activities" in r["relevant_fields"] for r in llm_regs))


# ---------------------------------------------------------------------------
# Woertlich aus der Vorgabe des Nutzers vom 12.10.2026.
VORGABE = {
    "laundry": "Setzen Sie den Haken, wenn an einem Standort Ihres Unternehmens in Deutschland bei der gewerblichen Reinigung oder Aufbereitung von Textilien Abwasser entsteht, z. B. in einer industriellen Wäscherei oder einem Textilservicebetrieb. Dies gilt auch bei Einleitung in die öffentliche Kanalisation. Je nach Art der gereinigten Textilien und den eingesetzten Verfahren können besondere abwasserrechtliche Anforderungen gelten.",
    "products": "Kreuzen Sie alle Produktkategorien an, die Ihr Unternehmen herstellt, einführt, vertreibt, vermietet, verleast oder im Rahmen seiner Dienstleistungen bereitstellt – auch wenn sie nur einen kleinen Teil Ihrer Geschäftstätigkeit ausmachen. Produktbezogene regulatorische Anforderungen können für einzelne Warengruppen gelten, unabhängig vom Schwerpunkt Ihrer Geschäftstätigkeit.",
    "business": "Wählen Sie alle Tätigkeitsbereiche aus, in denen Ihr Unternehmen aktiv ist – auch wenn diese nur einen Teil Ihrer Geschäftstätigkeit ausmachen.",
    "materials": "Wählen Sie alle Materialien aus, die in Ihren Produkten oder in den von Ihnen gereinigten, gepflegten, vermieteten oder verleasten Textilien enthalten sind – einschließlich Materialien in zugekauften Bestandteilen. Die Materialzusammensetzung kann für die Prüfung einzelner regulatorischer Anforderungen relevant sein. Ist Ihnen die Zusammensetzung bei Teilen Ihres Sortiments oder der von Ihnen betreuten Textilien nicht bekannt, wählen Sie zusätzlich „Nicht bekannt / kann nicht ausgeschlossen werden“.",
}
VORGABE_ROLLEN = ("Mehrfachauswahl möglich. Wählen Sie alle Rollen aus, die Ihr Unternehmen beim Umgang mit Produkten übernimmt.",
                  "Entscheidend ist beispielsweise, ob Sie Textilien selbst herstellen, aus Nicht-EU-Ländern einführen, unter eigener Marke anbieten oder an andere Unternehmen weitergeben.",
                  "Auch Unternehmen, die Textilien vermieten oder verleasen, können je nach Tätigkeit mehrere Rollen übernehmen.",
                  "Die Auswahl hilft dabei, produktbezogene regulatorische Anforderungen zu ermitteln, etwa aus der EUDR, PPWR oder EmpCo sowie zum Vernichtungsverbot.")
VORGABE_STANDORTE = ("Geben Sie an, welche Arten von Standorten Ihr Unternehmen unterhält, in welcher Region sie liegen und wie viele es jeweils sind.",
                     "Standorte, an denen Textilien gewaschen, gereinigt oder aufbereitet werden, zählen zu den Produktions- bzw. Betriebsstätten. Reine Annahmestellen oder Kundenbüros sind als Filialen bzw. Niederlassungen anzugeben. Die Standortart und der Standort können für die Prüfung einzelner regulatorischer Anforderungen relevant sein.")


def block_d() -> None:
    print("\n--- D  Vorgabetexte ---")
    for k, text in VORGABE.items():
        check(f"D Hilfetext {k} woertlich", i18n.t_help(k, "de") == text)
    check("D Hilfetext Rollen woertlich (Absaetze)", i18n.t_help("roles", "de") == "\n".join(VORGABE_ROLLEN))
    check("D Hilfetext Standorte woertlich", i18n.t_help("sites", "de") == "\n".join(VORGABE_STANDORTE))
    check("D Feld Waescherei", i18n.t("field_laundry", "de") == "Abwasser aus gewerblicher Wäscherei")
    check("D Abschnitt Geschaeftsmodell",
          i18n.t("section_business", "de").endswith("Geschäftsmodell / Tätigkeitsbereich")
          and i18n.t("business_hint", "de") == "Mehrfachauswahl möglich.")
    check("D sechs Taetigkeiten in Vorgabe-Reihenfolge", regs.BUSINESS_ACTIVITIES == [
        "Herstellung von Textilien oder Bekleidung", "Handel / Vertrieb von Textilprodukten",
        "Gewerbliche Wäscherei / Textilreinigung", "Vermietung / Leasing von Textilien",
        "Textilservice / Full-Service-Versorgung", "Sonstige textile Dienstleistungen"])
    rolle = {k: i18n.t_opt(k, i18n.ROLE_LABELS, "de") for k in regs.VALUE_CHAIN_ROLES}
    check("D Rolle Importeur", "Importeur (Bringt Produkte aus einem Nicht-EU-Land erstmals auf den EU-Markt, beispielsweise direkt beschaffte Berufskleidung oder Hotelwäsche.)" in rolle.values())
    check("D Rolle Haendler", "Händler / Vertreiber (Stellt Produkte anderer Unternehmen auf dem Markt bereit, beispielsweise durch Verkauf oder gegebenenfalls Vermietung.)" in rolle.values())
    check("D Rolle Zulieferer", "Zulieferer (Liefert Produkte, Materialien oder Komponenten an andere Unternehmen zur Weiterverarbeitung oder Verwendung.)" in rolle.values())
    check("D gespeicherte Rollenwerte unveraendert (keine Migration, Regeln greifen weiter)",
          "Zulieferer" in regs.VALUE_CHAIN_ROLES and regs._ROLE_HAENDLER in regs.VALUE_CHAIN_ROLES)
    check("D Standortart Produktion",
          i18n.t_opt(PRODUKTION, i18n.SITE_TYPE_LABELS, "de")
          == "Produktions- / Betriebsstätte (Herstellung, Verarbeitung, Reinigung oder Aufbereitung)"
          and PRODUKTION in regs.SITE_TYPES)
    check("D Ergebnis-Hinweis woertlich",
          i18n.t("results_role_title", "de") == "Hinweis zur Einordnung Ihres Ergebnisses"
          and i18n.t("results_role_text", "de") == "Die Begriffe „Hersteller“, „Importeur“ oder „Händler“ können je nach Rechtsvorschrift unterschiedlich definiert sein. Daher können einzelne Anforderungen auch für Unternehmen gelten, die sich selbst nicht diesen Kategorien zuordnen. Entscheidend sind die jeweiligen gesetzlichen Definitionen und die konkrete Tätigkeit Ihres Unternehmens."
          and i18n.t("results_questions_title", "de") == "Fragen zu Ihrem Ergebnis?"
          and i18n.t("results_hint", "de") == "Der ESG-Regulierungs-Check bietet eine erste Orientierung. Für eine vertiefte Einordnung einzelner Regelungen und ihrer Auswirkungen auf Ihr Unternehmen steht Ihnen das Team von textil+mode und seiner Mitgliedsverbände gerne zur Verfügung.")
    fehlend = [k for k in ("field_laundry", "section_business", "business_hint", "results_role_title",
                           "results_role_text", "results_questions_title", "results_hint")
               for l in LANGS if not i18n.UI[k].get(l)]
    fehlend += [k for k in ("laundry", "business", "products", "roles", "materials", "sites")
                for l in LANGS if not i18n.FIELD_HELP[k].get(l)]
    fehlend += [v for v in regs.BUSINESS_ACTIVITIES for l in LANGS
                if not i18n.BUSINESS_ACTIVITY_LABELS.get(v, {}).get(l)]
    check("D alles in sechs Sprachen", not fehlend, str(fehlend[:5]))


# ---------------------------------------------------------------------------
def block_e() -> None:
    print("\n--- E  Formular und Ergebnisseite ---")
    uid = db.create_user("formular2@example.org", "ein-gutes-Passwort-2026")
    db.upsert_company(uid, {"name": "F", "employees": 10, "branch": regs.BRANCHES[0],
                            "business_activities": [WAESCHEREI], "laundry_de": True})
    c = flaskapp.app.test_client()
    with c.session_transaction() as sess:
        sess["user_id"] = uid
        sess["ui_language"] = "de"
    html = c.get("/dashboard").get_data(as_text=True)
    i_nass, i_waesche = html.find('id="wet_processing_de"'), html.find('id="laundry_de"')
    check("E Waescherei-Haekchen direkt nach dem Abwasser-Feld, gesetzt",
          0 < i_nass < i_waesche and 'id="laundry_de" name="laundry_de" checked' in html)
    i_prod, i_biz, i_rollen = (html.find('name="product_categories"'), html.find('name="business_activities"'),
                               html.find('name="value_chain_roles"'))
    check("E Geschaeftsmodell zwischen Produktkategorien und Rollen", 0 < i_prod < i_biz < i_rollen)
    check("E Haken bei der gespeicherten Taetigkeit", f'value="{WAESCHEREI}" id="biz_3" checked' in html)
    check("E neue Beschriftungen im Formular",
          "Produktions- / Betriebsstätte (Herstellung, Verarbeitung, Reinigung oder Aufbereitung)" in html
          and "Zulieferer (Liefert Produkte" in html)
    r = c.post("/save-company", data={"name": "F", "employees": "10", "branch": regs.BRANCHES[0],
                                      "business_activities": [TEXTILSERVICE]},
               headers={"Origin": BASIS})
    neu = db.get_company(uid)
    check("E /save-company speichert Taetigkeit, Haekchen aus wenn nicht gesendet",
          r.status_code == 302 and neu["business_activities"] == [TEXTILSERVICE] and not neu["laundry_de"])

    karten = render_cards_html([{"nr": 34, "key": "AbwV55", "name": "AbwV Anhang 55", "full_name": "x",
                                 "url": "https://example.org", "applies": "ja", "reason": "r", "passage": "p"}],
                               "de")
    i1, i2 = karten.find("Hinweis zur Einordnung Ihres Ergebnisses"), karten.find("Fragen zu Ihrem Ergebnis?")
    check("E Ergebnis-Hinweis vor den Karten, beide Teile mit Ueberschrift",
          0 < i1 < i2 < karten.find("reg-card") and "<h4>" in karten)


# ---------------------------------------------------------------------------
def block_f() -> None:
    print("\n--- F  Katalog ---")
    reg = next((r for r in regs.REGULATIONS if r["key"] == "AbwV55"), None)
    check("F AbwV55 im Katalog, Quelle Anhang 55",
          reg is not None and reg["text_url"].endswith("/abwv/anhang_55.html"))
    check("F Veroeffentlichung + Anwendung + Hinweis",
          regs.published_for("AbwV55") == "17.06.2004"
          and regs.application_for("AbwV55")["note"] == "abwv55"
          and all(i18n.t_applies_note("abwv55", l) for l in LANGS))
    steps = regs.first_steps_for("AbwV55")
    check("F erste Schritte in 6 Sprachen",
          len(steps) == 3 and all(i18n.t_first_step(s, l) for s in steps for l in LANGS))
    check("F Leitlinie", len(regs.guidelines_for("AbwV55")) == 1)
    check("F Frist ableitbar", deadlines.deadline_for("AbwV55", {"laundry_de": True}) is not None)
    check("F Nummern eindeutig", len({r["nr"] for r in regs.REGULATIONS}) == len(regs.REGULATIONS))


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
