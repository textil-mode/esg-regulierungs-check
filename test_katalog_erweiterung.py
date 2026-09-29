"""Tests zur Katalogerweiterung vom 29.09.2026 (14 Regulierungen, 4 Profilfelder).

Ausfuehren:  ./.venv/Scripts/python.exe test_katalog_erweiterung.py

Kein Netz, kein LLM. Eigene DB `data/esg_katalog_test.db`; die Produktiv-DB
wird nicht beruehrt.

Bloecke:
  A  Regelbasierte Entscheidungen: Ausgang je Profil, Texte in sechs Sprachen
  B  Neue Profilfelder: Speichern/Lesen, Altprofil, Prompt-Darstellung
  C  Abruf: Bildanker bei REACH, Einstiegsmarke (letzte Fundstelle)
  D  Kontext: gezielte Eintraege aus Anhang XVII (focus_entries)
  E  Katalog: Vollstaendigkeit der Stammdaten, Hinweise, Schwellen-Naehe
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_katalog_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import fetcher  # noqa: E402
import i18n  # noqa: E402
import lawparse  # noqa: E402
import llm  # noqa: E402
import regulations as regs  # noqa: E402
import thresholds  # noqa: E402

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


HERSTELLER = regs.VALUE_CHAIN_ROLES[0]
HAENDLER = regs.VALUE_CHAIN_ROLES[2]
ZULIEFERER = "Zulieferer"
NEUE = ["REACH_XVII", "REACH_ART33", "SCIP", "POP", "BPR", "TKVO", "GPSR", "PSA", "MDR",
        "Schuhkennzeichnung", "EnEfG", "AbwV38", "EPR_FR", "EPR_NL"]
REGELBASIERT = ["REACH_ART33", "SCIP", "BPR", "PSA", "MDR", "Schuhkennzeichnung", "EnEfG", "AbwV38",
                "EPR_FR", "EPR_NL"]


def verdict(key: str, **profile) -> tuple[str, str, str]:
    v = regs.coupling_verdict(key, profile)
    return v["applies"], v["fact"], v["conclusion"]


# ---------------------------------------------------------------------------
def block_a() -> None:
    print("\n--- A  Regelbasierte Entscheidungen ---")
    faelle = [
        # (Regulierung, Profil, erwarteter Ausgang)
        ("REACH_ART33", {"svhc_status": "Ja"}, "ja"),
        ("REACH_ART33", {"svhc_status": "Nein"}, "nein"),
        ("REACH_ART33", {"svhc_status": "Nicht bekannt"}, "moeglich"),
        ("REACH_ART33", {}, "moeglich"),
        ("SCIP", {"svhc_status": "Ja", "value_chain_roles": [HERSTELLER]}, "ja"),
        ("SCIP", {"svhc_status": "Ja", "value_chain_roles": [HAENDLER], "b2c": True}, "moeglich"),
        ("SCIP", {"svhc_status": "Ja", "value_chain_roles": [HAENDLER], "b2c": False}, "ja"),
        ("SCIP", {"svhc_status": "Nein"}, "nein"),
        ("BPR", {"materials": ["Antimikrobielle / biozide Ausrüstung"]}, "ja"),
        ("BPR", {"materials": ["Nicht bekannt / kann nicht ausgeschlossen werden"]}, "moeglich"),
        ("BPR", {"materials": ["Baumwolle"]}, "nein"),
        ("BPR", {"materials": ["Antimikrobielle / biozide Ausrüstung"],
                 "sales_markets": ["außerhalb EU/EWR"]}, "nein"),
        ("PSA", {"product_categories": ["Schutztextilien / PSA"], "value_chain_roles": [HERSTELLER]}, "ja"),
        ("PSA", {"product_categories": ["Schutztextilien / PSA"], "value_chain_roles": [ZULIEFERER]}, "moeglich"),
        ("PSA", {"product_categories": ["Bekleidung und Bekleidungszubehör"]}, "nein"),
        ("MDR", {"product_categories": ["Medizin- und Gesundheitstextilien"],
                 "value_chain_roles": [HERSTELLER]}, "moeglich"),
        ("MDR", {"product_categories": ["Schuhe"]}, "nein"),
        ("Schuhkennzeichnung", {"product_categories": ["Schuhe"], "value_chain_roles": [HAENDLER]}, "ja"),
        ("Schuhkennzeichnung", {"product_categories": ["Schuhe"],
                                "sales_markets": ["außerhalb EU/EWR"]}, "nein"),
        # Altprofil ohne Absatzmaerkte: kein Schluss auf "ausserhalb"
        ("Schuhkennzeichnung", {"product_categories": ["Schuhe"], "sales_markets": []}, "ja"),
        # EnEfG: "mehr als" — genau 7,5 bzw. 2,5 reichen nicht
        ("EnEfG", {"energy_gwh": 0}, "moeglich"),
        ("EnEfG", {"energy_gwh": 2.5}, "nein"),
        ("EnEfG", {"energy_gwh": 2.51}, "ja"),
        ("EnEfG", {"energy_gwh": 7.5}, "ja"),
        ("EnEfG", {"energy_gwh": 7.51}, "ja"),
        ("AbwV38", {"wet_processing_de": True}, "ja"),
        ("AbwV38", {"branch": "Veredlung von Textilien und Bekleidung"}, "moeglich"),
        ("AbwV38", {"branch": "Weberei"}, "nein"),
        # Frankreich / Niederlande — der Live-Fehler vom 29.09.2026 (NL-Absatz galt als FR-Pflicht)
        ("EPR_FR", {"sales_markets": ["Deutschland", "Niederlande"], "product_categories": ["Schuhe"],
                    "value_chain_roles": [HAENDLER], "b2c": True}, "nein"),
        ("EPR_FR", {"sales_markets": ["Frankreich"], "product_categories": ["Schuhe"],
                    "value_chain_roles": [HAENDLER], "b2c": True}, "ja"),
        ("EPR_FR", {"sales_markets": ["Frankreich"], "product_categories": ["Bekleidung und Bekleidungszubehör"],
                    "value_chain_roles": [HERSTELLER], "b2c": False}, "moeglich"),
        ("EPR_FR", {"sales_markets": ["andere EU-/EWR-Staaten"], "product_categories": ["Heim- und Haustextilien"],
                    "value_chain_roles": [HERSTELLER], "b2c": True}, "moeglich"),
        ("EPR_FR", {"sales_markets": ["Frankreich"], "product_categories": ["Agrartextilien – Netze, Vliese, Abdeckungen etc."],
                    "b2c": True}, "nein"),
        ("EPR_FR", {"sales_markets": ["Frankreich"], "product_categories": ["Bekleidung und Bekleidungszubehör"],
                    "value_chain_roles": [ZULIEFERER], "b2c": True}, "moeglich"),
        ("EPR_NL", {"sales_markets": ["Niederlande"], "product_categories": ["Schuhe"],
                    "value_chain_roles": [HAENDLER]}, "nein"),
        ("EPR_NL", {"sales_markets": ["Niederlande"], "product_categories": ["Bekleidung und Bekleidungszubehör"],
                    "value_chain_roles": [HERSTELLER], "b2c": False}, "ja"),
        # PSA allein (etwa Sicherheitsschuhe) ist keine Berufskleidung im Sinne des Besluit
        ("EPR_NL", {"sales_markets": ["Niederlande"], "product_categories": ["Schutztextilien / PSA"],
                    "value_chain_roles": [HERSTELLER]}, "nein"),
        ("EPR_NL", {"sales_markets": ["Deutschland", "Frankreich"], "product_categories": ["Bekleidung und Bekleidungszubehör"],
                    "value_chain_roles": [HERSTELLER]}, "nein"),
        ("EPR_NL", {"sales_markets": ["andere EU-/EWR-Staaten"], "product_categories": ["Bekleidung und Bekleidungszubehör"],
                    "value_chain_roles": [HERSTELLER]}, "moeglich"),
    ]
    for key, profile, expected in faelle:
        applies, fact, conclusion = verdict(key, **profile)
        check(f"A {key} {profile} -> {expected}", applies == expected, f"{applies}/{fact}/{conclusion}")

    check("A EnEfG 7,5 GWh = nur Umsetzungsplaene (nicht Managementsystem)",
          verdict("EnEfG", energy_gwh=7.5)[2] == "ja_umsetzungsplan")
    check("A EnEfG 7,51 GWh = Managementsystem",
          verdict("EnEfG", energy_gwh=7.51)[2] == "ja_management")

    # Jeder erreichbare Fall hat Begruendung + Fundstelle in allen Sprachen,
    # und der Zahlenwert steht formatiert drin.
    for key, profile, _ in faelle:
        v = regs.coupling_verdict(key, profile)
        for lang in i18n.LANG_CODES:
            texts = i18n.coupling_texts(key, v, lang)
            if not texts or not texts[0] or not texts[1] or "{" in texts[0]:
                check(f"A Texte {key} {v['fact']}/{v['conclusion']} [{lang}]", False, repr(texts))
                break
        else:
            continue
    de = i18n.coupling_texts("EnEfG", regs.coupling_verdict("EnEfG", {"energy_gwh": 8.25}), "de")[0]
    en = i18n.coupling_texts("EnEfG", regs.coupling_verdict("EnEfG", {"energy_gwh": 8.25}), "en")[0]
    check("A EnEfG-Wert formatiert (DE Komma, EN Punkt)", "8,25 GWh" in de and "8.25 GWh" in en)

    # Regelbasiert heisst: kein LLM-Aufruf
    for key in REGELBASIERT:
        reg = next(r for r in regs.REGULATIONS if r["key"] == key)
        check(f"A {key} ohne LLM", llm.deterministic_result(reg, {}, "de") is not None)
    for key in sorted(set(NEUE) - set(REGELBASIERT)):
        reg = next(r for r in regs.REGULATIONS if r["key"] == key)
        check(f"A {key} ueber das LLM", llm.deterministic_result(reg, {}, "de") is None)


# ---------------------------------------------------------------------------
def block_b() -> None:
    print("\n--- B  Neue Profilfelder ---")
    db.init_db()
    uid = db.create_user("katalogtest@example.invalid", "nur-fuer-den-test")
    db.upsert_company(uid, {
        "name": "Test", "employees": 10, "branch": regs.BRANCHES[0],
        "sales_markets": ["Deutschland", "Frankreich", "Niederlande", "Gibt es nicht"],
        "energy_gwh": 7.5, "wet_processing_de": True, "svhc_status": "Ja",
    })
    c = db.get_company(uid)
    check("B Frankreich/Niederlande gespeichert, Unbekanntes verworfen",
          c["sales_markets"] == ["Deutschland", "Frankreich", "Niederlande"], str(c["sales_markets"]))
    check("B Energieverbrauch als Kommazahl", c["energy_gwh"] == 7.5, str(c["energy_gwh"]))
    check("B Nassveredlung", c["wet_processing_de"] is True)
    check("B SVHC", c["svhc_status"] == "Ja")

    db.upsert_company(uid, {"name": "Test", "employees": 10, "branch": regs.BRANCHES[0],
                            "svhc_status": "Vielleicht"})
    c = db.get_company(uid)
    check("B unbekannter SVHC-Wert -> 'Nicht bekannt'", c["svhc_status"] == "Nicht bekannt")
    check("B fehlende Angaben -> 0 / False", c["energy_gwh"] == 0 and c["wet_processing_de"] is False)

    check("B Prompt zeigt 7,5 GWh nicht als '8'",
          llm._render_field("energy_gwh", 7.5) == "7.50", llm._render_field("energy_gwh", 7.5))
    check("B Nassveredlung im Prompt als yes/no", llm._render_field("wet_processing_de", True) == "yes")
    for field in ("energy_gwh", "wet_processing_de", "svhc_status"):
        check(f"B Prompt-Beschriftung {field}", field in llm._PROFILE_LABELS)
    # Der Cache-Schluessel darf sich an der Typdarstellung nicht stossen.
    reg = next(r for r in regs.REGULATIONS if r["key"] == "EnEfG")
    check("B profile_hash stabil (7.5 vs '7.5' nicht verwechselt, 0 vs None gleich)",
          llm.profile_hash({"energy_gwh": 0}, reg) == llm.profile_hash({"energy_gwh": None}, reg))


# ---------------------------------------------------------------------------
def block_c() -> None:
    print("\n--- C  Abruf ---")
    html = ('<html><body><a id="textofimagelink_1" href="#">Text von Bild</a>'
            '<div id="TexteOnly"><p>Artikel 33</p><p>Jeder Lieferant eines Erzeugnisses</p></div>'
            '</body></html>')
    text = fetcher._extract_html(html)
    check("C Bildanker wird uebersprungen", "Jeder Lieferant" in text and "Text von Bild" not in text,
          text[:80])
    plain = '<html><body><div id="content"><p>Artikel 1</p></div></body></html>'
    check("C ohne Bildanker unveraendert", fetcher._extract_html(plain) == "Artikel 1")

    reg = {"key": "X", "text_from": r"^\s*(?:ANHANG|ANNEX)\s+XVII\s*$"}
    raw = "Inhalt\nANHANG XVII\nTitel I\n...\nANHANG XVII\nVerzeichnis 2\n...\nANHANG XVII\n43.  Azofarbstoffe"
    out = fetcher._apply_text_from(raw, reg)
    check("C Einstiegsmarke: letzte Fundstelle", out.startswith("ANHANG XVII\n43."), out[:30])
    check("C Einstiegsmarke fehlt -> Text unveraendert",
          fetcher._apply_text_from("kein Anhang", reg) == "kein Anhang")
    check("C ohne text_from unveraendert", fetcher._apply_text_from(raw, {"key": "Y"}) == raw)


# ---------------------------------------------------------------------------
def block_d() -> None:
    print("\n--- D  Kontext: Eintraege aus Anhang XVII ---")
    annex = ("ANHANG XVII\n41.  Hexachlorethan\nDarf nicht.\n"
             "43.  Azofarbstoffe\n1.  Azofarbstoffe duerfen nicht ...\n2.  Weitere Regel.\n"
             "46.\na)  Nonylphenol\nDarf nicht.\n"
             "46a.  Nonylphenolethoxylate\nIn waschbaren Textilien nicht ueber 0,01 %.\n"
             "72.  CMR-Stoffe\n1.  Duerfen nach dem 1. November 2020 nicht ...\n"
             "73.  Etwas anderes\nNicht gefragt.\n")
    reg = {"key": "T", "full_name": "Test", "focus_entries": ["43", "46a", "72", "99"],
           "focus_label": "Anhang XVII Nr. {n}"}
    ctx = lawparse.build_context(reg, annex, [], 25000)
    check("D Kopfzeile je Eintrag", all(f"=== Anhang XVII Nr. {n} ===" in ctx for n in ("43", "46a", "72")))
    check("D Eintrag endet vor dem naechsten (Absaetze 1./2. gehoeren dazu)",
          "Weitere Regel." in ctx and "Nonylphenol\nDarf" not in ctx.split("Nr. 43 ===")[1].split("===")[0])
    check("D nicht gefragte Eintraege fehlen", "Hexachlorethan" not in ctx and "Nicht gefragt" not in ctx)
    check("D fehlender Eintrag (99) stoert nicht", "Nr. 99" not in ctx)
    ohne = lawparse.build_context({"key": "U", "full_name": "Test"}, annex, [], 25000)
    check("D ohne focus_entries normaler Ablauf", "Anhang XVII Nr." not in ohne)


# ---------------------------------------------------------------------------
def block_e() -> None:
    print("\n--- E  Katalog ---")
    by_key = {r["key"]: r for r in regs.REGULATIONS}
    check("E 30 Regulierungen, alle neuen vorhanden", len(regs.REGULATIONS) == 30
          and all(k in by_key for k in NEUE), str(len(regs.REGULATIONS)))
    check("E Nummern eindeutig", len({r["nr"] for r in regs.REGULATIONS}) == len(regs.REGULATIONS))
    for key in NEUE:
        r = by_key[key]
        ok = all(r.get(f) for f in ("name", "full_name", "url", "text_url", "scope", "criteria",
                                    "key_article", "relevant_fields"))
        app = regs.application_for(key)
        ok = ok and bool(app["applies_from"]) and regs.published_for(key) != "—"
        check(f"E {key} Stammdaten vollstaendig", ok)
        if app["note"]:
            check(f"E {key} Hinweiszeile in sechs Sprachen",
                  all(i18n.t_applies_note(app["note"], lang) for lang in i18n.LANG_CODES))
        unknown = [f for f in r["relevant_fields"] if f not in llm._PROFILE_LABELS]
        check(f"E {key} relevant_fields bekannt", not unknown, str(unknown))
    ki = [r for r in regs.REGULATIONS if llm.deterministic_result(r, {}, "de") is None]
    most = max(len(r["relevant_fields"]) for r in ki)
    check("E hoechstens sieben Profilmerkmale je KI-Anfrage (Datenschutzerklaerung sagt sieben)", most <= 7, str(most))

    for gwh, key in ((2.2, "enefg_2_5_knapp_darunter"), (2.8, "enefg_2_5_knapp_darueber"),
                     (7.5, "enefg_7_5_knapp_darunter"), (8.5, "enefg_7_5_knapp_darueber")):
        hints = [h["key"] for h in thresholds.near_thresholds({"energy_gwh": gwh})]
        check(f"E Schwellen-Naehe {gwh} GWh -> {key}", hints == [key], str(hints))
    hint = {"key": "enefg_7_5_knapp_darueber", "values": {"energy_gwh": 8.5}}
    check("E Schwellen-Hinweis in sechs Sprachen mit Wert",
          all("8" in i18n.t_threshold_hint(hint, lang) for lang in i18n.LANG_CODES))
    for label_key in ("field_energy_gwh", "field_wet_processing", "field_svhc"):
        check(f"E Beschriftung {label_key} in sechs Sprachen",
              all(i18n.t(label_key, lang) != label_key for lang in i18n.LANG_CODES))
    for help_key in ("energy_gwh", "wet_processing", "svhc"):
        check(f"E Ausfuellhilfe {help_key} in sechs Sprachen",
              all(i18n.t_help(help_key, lang) for lang in i18n.LANG_CODES))


def main() -> int:
    block_a()
    block_b()
    block_c()
    block_d()
    block_e()
    print()
    if _failures:
        print(f"{len(_failures)} Pruefung(en) fehlgeschlagen:")
        for f in _failures:
            print("  -", f)
        return 1
    print("=" * 62)
    print("Alle Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
