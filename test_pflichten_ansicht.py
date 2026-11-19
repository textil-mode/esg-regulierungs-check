"""Tests zum Pflichten-Plan, Aufgabe 4: Ansicht, Kalenderexport, Karten aus der DB.

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_ansicht.py

Kein Netz, kein LLM, festes `today` (app._heute wird ersetzt).
Eigene DB `data/esg_pflichten_ansicht_test.db`.

Bloecke:
  A  Schalter aus: Mitglied 404, Admin 200
  B  Schalter an, Konto ohne Analyse: Verweis auf den Check
  C  Konto mit Analyse: EUDR-Schritt, "laufend" fuer geltende Pflicht
  D  POST-Routen: fremde/inaktive/entfallene Schritte 404, Periode serverseitig
  E  Zustaendigkeit wird escaped
  F  Filter ?rolle=einkauf
  G  .ics: ein VEVENT je datiertem offenem Schritt, Faltung, Escaping
  H  gesehen: Version aus der DB
  I  Erinnerungen an/aus
  J  Env PFLICHTEN_PLAN=aus: 404 auch fuer Admin (auch /admin/pflichten*), Karten aus dem Code
  L  Quelle der ersten Schritte (Karte + Assistent): Schalter aus -> Code, an -> DB
  M  Abbestellen markiert offene Hinweise als gesendet
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_ansicht_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
os.environ["PUBLIC_BASE_URL"] = "https://test.example"
os.environ.pop("PFLICHTEN_PLAN", None)
for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[v] = ""
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import i18n  # noqa: E402
import pflichten  # noqa: E402
import pflichten_db as pdb  # noqa: E402
import app as flaskapp  # noqa: E402
from views import render_cards_html  # noqa: E402
from markupsafe import escape  # noqa: E402

assert db.DB_PATH == TEST_DB, "falsche Datenbank!"

_failures: list[str] = []
HEUTE = date(2026, 11, 19)
flaskapp._heute = lambda: HEUTE


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def _sql(sql: str, params=()) -> None:
    with db._conn() as c:
        c.execute(sql, params)


def _client(uid: int, email: str):
    client = flaskapp.app.test_client()
    with client.session_transaction() as s:
        s["user_id"] = uid
        s["user_email"] = email
    return client


PW = "Geheim-Passwort-123"
ADMIN = "mschuckert@textil-mode.de"
ADMIN_ID = db.create_user(ADMIN, PW)
LEER_ID = db.create_user("leer@example.org", PW)
UID = db.create_user("mitglied@example.org", PW)
PROFIL = {"name": "Lederwaren Test GmbH", "employees": 120, "materials": ["Leder"]}
db.upsert_company(LEER_ID, PROFIL)
db.upsert_company(UID, PROFIL)

EUDR = [s["id"] for s in pdb.schritte_fuer("EUDR", "de")]
TKVO = [s["id"] for s in pdb.schritte_fuer("TKVO", "de")]
LKSG = [s["id"] for s in pdb.schritte_fuer("LkSG", "de")]
CSRD = [s["id"] for s in pdb.schritte_fuer("CSRD", "de")]
assert len(EUDR) >= 4 and len(TKVO) >= 3 and LKSG and CSRD, "Startbestand fehlt"

# Fristen: EUDR gilt ab 30.12.2026 (in der Zukunft), TKVO seit 2012.
_sql("UPDATE pflicht_schritte SET frist_typ='fest', frist_wert='31.12.2026', rolle='einkauf'"
     " WHERE id=?", (EUDR[0],))
_sql("UPDATE pflicht_schritte SET frist_typ='relativ', frist_wert='+0d', rolle='personal'"
     " WHERE id=?", (EUDR[1],))
_sql("UPDATE pflicht_schritte SET frist_typ='jaehrlich', frist_wert='31.05.', rolle='logistik'"
     " WHERE id=?", (EUDR[2],))
_sql("UPDATE pflicht_schritte SET aktiv=0 WHERE id=?", (EUDR[3],))
_sql("UPDATE pflicht_schritte SET frist_typ='relativ', frist_wert='-6m' WHERE id=?", (TKVO[0],))
# TKVO: ein Logistik-Schritt spaet (30.06.2027), ein ueberfaelliger (01.11.2026).
_sql("UPDATE pflicht_schritte SET frist_typ='fest', frist_wert='30.06.2027', rolle='logistik'"
     " WHERE id=?", (TKVO[1],))
_sql("UPDATE pflicht_schritte SET frist_typ='fest', frist_wert='01.11.2026' WHERE id=?", (TKVO[2],))
_sql("UPDATE pflicht_schritte SET frist_typ='fest', frist_wert='01.03.2027' WHERE id=?",
     (CSRD[0],))


def _karten(**applies: str) -> list[dict]:
    return [{"key": k, "name": f"{k} Testname", "applies": v} for k, v in applies.items()]


def _erinnerungen(uid: int) -> int:
    with db._conn() as c:
        return c.execute("SELECT erinnerungen FROM users WHERE id=?", (uid,)).fetchone()[0]


def block_a() -> None:
    print("\n--- A  Schalter aus ---")
    r = _client(UID, "mitglied@example.org").get("/meine-pflichten")
    check("A Mitglied: 404 bei Schalter aus", r.status_code == 404, str(r.status_code))
    r = _client(ADMIN_ID, ADMIN).get("/meine-pflichten")
    check("A Admin: 200 bei Schalter aus", r.status_code == 200, str(r.status_code))
    r = flaskapp.app.test_client().get("/meine-pflichten")
    check("A ohne Anmeldung: Umleitung", r.status_code in (302, 303), str(r.status_code))
    html = _client(UID, "mitglied@example.org").get("/passwort-aendern").get_data(as_text=True)
    check("A Menue: kein Link fuer Mitglied", "/meine-pflichten" not in html)
    html = _client(ADMIN_ID, ADMIN).get("/passwort-aendern").get_data(as_text=True)
    check("A Menue: Link fuer Admin", "/meine-pflichten" in html)
    r = _client(UID, "mitglied@example.org").post("/konto/erinnerungen", data={"an": "0"})
    check("A Erinnerungen-Schalter Mitglied: 404", r.status_code == 404
          and _erinnerungen(UID) == 1, str(r.status_code))
    html = _client(UID, "mitglied@example.org").get("/passwort-aendern").get_data(as_text=True)
    check("A Kontoseite Mitglied: kein Erinnerungsschalter", "/konto/erinnerungen" not in html)


def block_b() -> None:
    print("\n--- B  Ohne Analyse ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    r = _client(LEER_ID, "leer@example.org").get("/meine-pflichten")
    html = r.get_data(as_text=True)
    check("B 200", r.status_code == 200, str(r.status_code))
    check("B Verweis auf den Check", i18n.t("pflichten_ohne_pruefung", "de") in html)
    check("B Haftungshinweis", i18n.t("pflichten_haftung", "de") in html)


def block_c() -> str:
    print("\n--- C  Mit Analyse ---")
    db.save_analysis(UID, _karten(EUDR="ja", TKVO="ja", CSRD="moeglich", LkSG="nein"))
    r = _client(UID, "mitglied@example.org").get("/meine-pflichten")
    html = r.get_data(as_text=True)
    check("C 200", r.status_code == 200, str(r.status_code))
    titel = pdb.schritte_fuer("EUDR", "de")[0]["titel"]
    check("C EUDR-Schritttitel", str(escape(titel)) in html, titel[:40])
    check("C 'laufend' fuer TKVO-Schritt",
          f'id="s-{TKVO[0]}" data-frist="laufend"' in html
          and i18n.t("pflichten_laufend", "de") in html)
    check("C fester Termin mit 'bis 31.12.2026'",
          f'id="s-{EUDR[0]}" data-frist="datum"' in html and "31.12.2026" in html)
    check("C inaktiver Schritt nicht sichtbar", f'id="s-{EUDR[3]}"' not in html)
    check("C LkSG (nein) nicht im Plan", f'id="s-{LKSG[0]}"' not in html)
    check("C Rollenname uebersetzt", i18n.t("rolle_einkauf", "de") in html)
    kopf = html[html.find('id="p-TKVO"'):]
    kopf = kopf[:kopf.find("</summary>")]
    check("C geltende Pflicht: 'gilt (Daueraufgabe)' statt Datum",
          i18n.t("pflichten_gilt_dauer", "de") in kopf and "08.05.2012" not in kopf, " ".join(kopf.split())[:160])
    kopf = html[html.find('id="p-EUDR"'):]
    kopf = kopf[:kopf.find("</summary>")]
    check("C kuenftige Pflicht: 'gilt fuer Sie ab 30.12.2026'",
          i18n.t("pflichten_gilt_ab", "de").format(datum="30.12.2026") in kopf, " ".join(kopf.split())[:160])
    # Faellig in 90 Tagen: EUDR 30.12. und 31.12.2026; nicht TKVO 01.11.2026 (ueberfaellig),
    # nicht CSRD 01.03.2027 / TKVO 30.06.2027 / EUDR 31.05.2027 (spaeter).
    check("C 'faellig in 90 Tagen' ohne Ueberfaellige = 2",
          "· 3 Pflichten · 2 Schritte fällig in 90 Tagen" in html,
          re.search(r"·[^<]*fällig[^<]*", html).group(0) if re.search(r"·[^<]*fällig[^<]*", html) else "")
    return html


def block_d() -> None:
    print("\n--- D  POST-Routen ---")
    c = _client(UID, "mitglied@example.org")
    r = c.post(f"/meine-pflichten/{EUDR[3]}/erledigt", data={"erledigt": "1"})
    check("D inaktiver Schritt: 404", r.status_code == 404, str(r.status_code))
    r = c.post(f"/meine-pflichten/{LKSG[0]}/erledigt", data={"erledigt": "1"})
    check("D fremde Pflicht (LkSG nein): 404", r.status_code == 404, str(r.status_code))
    r = c.post("/meine-pflichten/999999/erledigt", data={"erledigt": "1"})
    check("D unbekannte ID: 404", r.status_code == 404, str(r.status_code))
    r = c.post(f"/meine-pflichten/{LKSG[0]}/zustaendig", data={"zustaendig": "x"})
    check("D zustaendig fremd: 404", r.status_code == 404, str(r.status_code))
    r = c.post(f"/meine-pflichten/{LKSG[0]}/gesehen")
    check("D gesehen fremd: 404", r.status_code == 404, str(r.status_code))

    # Jaehrlich: Periode kommt vom Server (31.05.2027 -> '2027'), nicht aus dem Formular.
    r = c.post(f"/meine-pflichten/{EUDR[2]}/erledigt", data={"erledigt": "1", "periode": "1999"})
    check("D erledigt: Umleitung", r.status_code in (302, 303), str(r.status_code))
    _, erledigt = pdb.nutzer_zustand(UID)
    check("D Periode serverseitig '2027'", set(erledigt.get(EUDR[2], {})) == {"2027"},
          str(erledigt.get(EUDR[2])))
    r = c.post(f"/meine-pflichten/{EUDR[2]}/erledigt", data={"erledigt": "0", "periode": "1999"})
    _, erledigt = pdb.nutzer_zustand(UID)
    check("D Haekchen entfernt", not erledigt.get(EUDR[2]), str(erledigt.get(EUDR[2])))

    # Entfallene Pflicht: CSRD nach neuer Pruefung 'nein'
    db.save_analysis(UID, _karten(EUDR="ja", TKVO="ja", CSRD="nein", LkSG="nein"))
    r = c.post(f"/meine-pflichten/{CSRD[0]}/erledigt", data={"erledigt": "1"})
    check("D entfallene Pflicht: 404", r.status_code == 404, str(r.status_code))
    html = c.get("/meine-pflichten").get_data(as_text=True)
    check("D Entfaellt-Block sichtbar", i18n.t("pflichten_entfaellt", "de") in html)

    # Fremdes Konto darf keine Schritte im Plan eines anderen abhaken
    r = _client(LEER_ID, "leer@example.org").post(f"/meine-pflichten/{EUDR[0]}/erledigt",
                                                  data={"erledigt": "1"})
    check("D Konto ohne Plan: 404", r.status_code == 404, str(r.status_code))


def block_e() -> None:
    print("\n--- E  Escaping ---")
    c = _client(UID, "mitglied@example.org")
    r = c.post(f"/meine-pflichten/{EUDR[0]}/zustaendig",
               data={"zustaendig": "<script>alert(1)</script>"})
    check("E zustaendig: Umleitung", r.status_code in (302, 303), str(r.status_code))
    html = c.get("/meine-pflichten").get_data(as_text=True)
    check("E kein rohes <script>alert", "<script>alert(1)</script>" not in html)
    check("E escaped sichtbar", "&lt;script&gt;alert(1)&lt;/script&gt;" in html)


def block_f() -> None:
    print("\n--- F  Rollenfilter ---")
    html = _client(UID, "mitglied@example.org").get("/meine-pflichten?rolle=einkauf") \
        .get_data(as_text=True)
    check("F Einkauf-Schritt sichtbar", f'id="s-{EUDR[0]}"' in html)
    check("F Personal-Schritt ausgeblendet", f'id="s-{EUDR[1]}"' not in html)
    check("F TKVO (keine Einkauf-Schritte) entfaellt aus der Anzeige", f'id="s-{TKVO[0]}"' not in html)
    html = _client(UID, "mitglied@example.org").get("/meine-pflichten").get_data(as_text=True)
    check("F ohne Filter: TKVO (ueberfaellig) vor EUDR",
          0 < html.find('id="p-TKVO"') < html.find('id="p-EUDR"'))
    html = _client(UID, "mitglied@example.org").get("/meine-pflichten?rolle=logistik")         .get_data(as_text=True)
    check("F Filter logistik sortiert neu: EUDR (31.05.2027) vor TKVO (30.06.2027)",
          0 < html.find('id="p-EUDR"') < html.find('id="p-TKVO"'))
    html = _client(UID, "mitglied@example.org").get("/meine-pflichten?rolle=quatsch") \
        .get_data(as_text=True)
    check("F unbekannte Rolle = alle", f'id="s-{EUDR[1]}"' in html)


def _unfold(text: str) -> list[str]:
    return text.replace("\r\n ", "").split("\r\n")


def block_g() -> None:
    print("\n--- G  Kalender ---")
    c = _client(UID, "mitglied@example.org")
    c.post(f"/meine-pflichten/{EUDR[0]}/zustaendig",
           data={"zustaendig": "Frau Muster; Einkauf, Leder\\Haeute " + "x" * 80})
    r = c.get("/meine-pflichten.ics")
    check("G 200 text/calendar", r.status_code == 200
          and r.mimetype == "text/calendar", f"{r.status_code} {r.mimetype}")
    roh = r.get_data()
    text = roh.decode("utf-8")
    check("G CRLF-Zeilenenden", "\r\n" in text and "\n" not in text.replace("\r\n", ""))
    check("G Zeilen <= 75 Oktette",
          all(len(z.encode("utf-8")) <= 75 for z in text.split("\r\n")))
    zeilen = _unfold(text)
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    erwartet = sorted(
        f"pflicht-{UID}-{s['id']}-{s['frist']['datum'].strftime('%Y%m%d')}@ki-textil-mode.de"
        for p in plan["pflichten"] if not p["entfaellt"]
        for s in p["schritte"] if s["frist"]["art"] == "datum" and not s["erledigt"])
    uids = sorted(z[4:] for z in zeilen if z.startswith("UID:"))
    check("G genau ein VEVENT je datiertem offenem Schritt",
          uids == erwartet and text.count("BEGIN:VEVENT") == len(erwartet) and erwartet,
          f"{uids} vs {erwartet}")
    check("G kein VEVENT fuer laufend (TKVO)", not any(f"-{TKVO[0]}-" in u for u in uids))
    check("G kein VEVENT fuer entfallene CSRD", not any(f"-{CSRD[0]}-" in u for u in uids))
    check("G ganztaegig", "DTSTART;VALUE=DATE:20261231" in zeilen)
    check("G Escaping ; , \\", any("Frau Muster\\; Einkauf\\, Leder\\\\Haeute" in z
                                   for z in zeilen))
    # Erledigt -> kein Termin mehr
    c.post(f"/meine-pflichten/{EUDR[0]}/erledigt", data={"erledigt": "1"})
    text = c.get("/meine-pflichten.ics").get_data(as_text=True)
    check("G erledigter Schritt ohne VEVENT", f"pflicht-{UID}-{EUDR[0]}-" not in text)
    r = _client(LEER_ID, "leer@example.org").get("/meine-pflichten.ics")
    check("G ohne Analyse: leerer Kalender", r.status_code == 200
          and "BEGIN:VCALENDAR" in r.get_data(as_text=True)
          and "BEGIN:VEVENT" not in r.get_data(as_text=True))


def block_h() -> None:
    print("\n--- H  gesehen ---")
    _sql("UPDATE pflicht_schritte SET version=3, meldung_version=3, geaendert_am='2026-11-19'"
         " WHERE id=?",
         (EUDR[0],))
    c = _client(UID, "mitglied@example.org")
    html = c.get("/meine-pflichten").get_data(as_text=True)
    check("H 'geaendert, bitte pruefen' sichtbar",
          i18n.t("pflichten_geaendert", "de").split("{")[0] in html)
    r = c.post(f"/meine-pflichten/{EUDR[0]}/gesehen", data={"version": "99"})
    zustand, _ = pdb.nutzer_zustand(UID)
    check("H Version aus der DB (3), nicht 99",
          r.status_code in (302, 303) and zustand[EUDR[0]]["gesehen_version"] == 3,
          str(zustand.get(EUDR[0])))


def block_i() -> None:
    print("\n--- I  Erinnerungen ---")
    c = _client(UID, "mitglied@example.org")
    html = c.get("/passwort-aendern").get_data(as_text=True)
    check("I Schalter auf der Kontoseite", "/konto/erinnerungen" in html
          and i18n.t("pflichten_erinnerungen_an", "de") in html)
    r = c.post("/konto/erinnerungen", data={"an": "0"})
    check("I aus", r.status_code in (302, 303) and _erinnerungen(UID) == 0)
    html = c.get("/meine-pflichten").get_data(as_text=True)
    check("I Seite zeigt 'aus'", i18n.t("pflichten_erinnerungen_aus", "de") in html)
    c.post("/konto/erinnerungen", data={"an": "1"})
    check("I wieder an", _erinnerungen(UID) == 1)
    r = flaskapp.app.test_client().post("/konto/erinnerungen", data={"an": "0"})
    check("I ohne Anmeldung: Umleitung, nichts geaendert",
          r.status_code in (302, 303) and _erinnerungen(UID) == 1)


def block_j() -> None:
    print("\n--- J  Env PFLICHTEN_PLAN=aus ---")
    _sql("UPDATE pflicht_schritt_texte SET titel='DB-Titel Testschritt' WHERE schritt_id=?"
         " AND sprache='de'", (EUDR[0],))
    karte = [{"nr": 1, "key": "EUDR", "name": "EUDR", "full_name": "x",
              "url": "https://example.org", "applies": "ja", "reason": "r", "passage": "p"}]
    html = render_cards_html(karte, "de", profile=PROFIL)
    check("J Karte liest erste Schritte aus der DB", "DB-Titel Testschritt" in html)
    os.environ["PFLICHTEN_PLAN"] = "aus"
    try:
        r = _client(ADMIN_ID, ADMIN).get("/meine-pflichten")
        check("J Admin: 404", r.status_code == 404, str(r.status_code))
        r = _client(UID, "mitglied@example.org").get("/meine-pflichten.ics")
        check("J .ics: 404", r.status_code == 404, str(r.status_code))
        r = _client(UID, "mitglied@example.org").post(
            f"/meine-pflichten/{EUDR[1]}/erledigt", data={"erledigt": "1"})
        check("J POST: 404", r.status_code == 404, str(r.status_code))
        r = _client(ADMIN_ID, ADMIN).post("/konto/erinnerungen", data={"an": "0"})
        check("J Erinnerungen-Schalter Admin: 404", r.status_code == 404
              and _erinnerungen(ADMIN_ID) == 1, str(r.status_code))
        html = render_cards_html(karte, "de", profile=PROFIL)
        code = i18n.t_first_step("eudr_1", "de")
        check("J Karte aus i18n.FIRST_STEPS", code and code in html
              and "DB-Titel Testschritt" not in html)
        html = _client(ADMIN_ID, ADMIN).get("/passwort-aendern").get_data(as_text=True)
        check("J kein Menuepunkt", "/meine-pflichten" not in html)
        # F3: auch die Admin-Seiten sind aus (lesen und schreiben, beide Admin-Arten)
        admin = _client(ADMIN_ID, ADMIN)
        for pfad in ("/admin/pflichten", "/admin/pflichten/vorschlaege",
                     f"/admin/pflichten/schritt/{EUDR[0]}", "/admin/pflichten/neu/EUDR",
                     "/admin/pflichten/export.json"):
            r = admin.get(pfad)
            check(f"J Admin GET {pfad}: 404", r.status_code == 404, str(r.status_code))
        vorher = pdb.einstellung("pflichten_plan_aktiv", "0")
        r = admin.post("/admin/pflichten/schalter", data={"aktiv": "0"})
        check("J Admin POST Schalter: 404, Schalter unveraendert", r.status_code == 404
              and pdb.einstellung("pflichten_plan_aktiv", "0") == vorher, str(r.status_code))
        n = len(pdb.offene_vorschlaege())
        r = admin.post(f"/admin/pflichten/schritt/{EUDR[0]}", data={"deaktivieren": "1"})
        check("J Admin POST Handpflege: 404, kein Vorschlag",
              r.status_code == 404 and len(pdb.offene_vorschlaege()) == n, str(r.status_code))
        import pflichten_vorschlag
        gestartet = []
        alt_start = pflichten_vorschlag.starte_startbestand
        pflichten_vorschlag.starte_startbestand = lambda **kw: gestartet.append(1) or True
        try:
            r = admin.post("/admin/pflichten/startbestand")
        finally:
            pflichten_vorschlag.starte_startbestand = alt_start
        check("J Admin POST Startbestand: 404, kein Lauf",
              r.status_code == 404 and not gestartet, str(r.status_code))
    finally:
        os.environ.pop("PFLICHTEN_PLAN", None)


def block_k() -> None:
    print("\n--- K  i18n ---")
    schluessel = ["nav_pflichten", "pflichten_titel", "pflichten_grundlage",
                  "pflichten_ohne_pruefung", "pflichten_gilt_ab", "pflichten_laufend",
                  "pflichten_offen", "pflichten_ueberfaellig", "pflichten_bis",
                  "pflichten_daten", "pflichten_zustaendig", "pflichten_geprueft",
                  "pflichten_geaendert", "pflichten_entfaellt", "pflichten_ics",
                  "pflichten_erinnerungen_an", "pflichten_erinnerungen_aus",
                  "pflichten_filter_alle", "pflichten_haftung", "pflichten_gilt_dauer",
                  "pflichten_geaendert_ohne_datum", "pflichten_verlauf_vor_umstellung"]
    schluessel += [f"rolle_{r}" for r in pflichten.ROLLEN]
    fehlt = [f"{k}/{l}" for k in schluessel for l in ("de", "en", "es", "fr", "it", "zh")
             if not i18n.UI.get(k, {}).get(l)]
    check("K alle Schluessel in 6 Sprachen", not fehlt, ", ".join(fehlt[:8]))
    html = _client(UID, "mitglied@example.org").get("/meine-pflichten").get_data(as_text=True)
    check("K keine unaufgeloesten Platzhalter", not re.search(r"\{(datum|anzahl|faellig|erledigt|gesamt|periode)\}", html))


def block_l() -> None:
    print("\n--- L  Quelle der ersten Schritte ---")
    import assistent
    _sql("UPDATE pflicht_schritt_texte SET titel='DB-Titel Quelle' WHERE schritt_id=?"
         " AND sprache='de'", (EUDR[0],))
    karte = [{"nr": 1, "key": "EUDR", "name": "EUDR", "full_name": "x",
              "url": "https://example.org", "applies": "ja", "reason": "r", "passage": "p"}]
    code = i18n.t_first_step("eudr_1", "de")
    vorher = pdb.einstellung("pflichten_plan_aktiv", "0")
    try:
        pdb.setze_einstellung("pflichten_plan_aktiv", "0")
        titel = pdb.erste_schritte_titel("EUDR", "de")
        check("L Schalter aus: Hilfsfunktion liefert Code-Titel",
              code in titel and "DB-Titel Quelle" not in titel, str(titel))
        html = render_cards_html(karte, "de", profile=PROFIL)
        check("L Schalter aus: Karte aus dem Code", code in html and "DB-Titel Quelle" not in html)
        assistent._catalog_cache = None
        text = assistent.catalog_text(HEUTE)
        check("L Schalter aus: Assistent aus dem Code",
              code in text and "DB-Titel Quelle" not in text)
        pdb.setze_einstellung("pflichten_plan_aktiv", "1")
        titel = pdb.erste_schritte_titel("EUDR", "de")
        check("L Schalter an: Hilfsfunktion liefert DB-Titel", "DB-Titel Quelle" in titel,
              str(titel))
        check("L Schalter an: inaktiver Schritt fehlt",
              len(titel) == len(pdb.schritte_fuer("EUDR", "de")), str(titel))
        html = render_cards_html(karte, "de", profile=PROFIL)
        check("L Schalter an: Karte aus der DB", "DB-Titel Quelle" in html)
        text = assistent.catalog_text(HEUTE)
        check("L Schalter an: Assistent aus der DB (Cache folgt dem Schalter)",
              "DB-Titel Quelle" in text)
    finally:
        pdb.setze_einstellung("pflichten_plan_aktiv", vorher)
        assistent._catalog_cache = None


def block_m() -> None:
    print("\n--- M  Abbestellen ---")
    for text in ("eins", "zwei"):
        pdb.neuer_hinweis(UID, "EUDR", "inhalt", text, HEUTE)
    check("M vorher: zwei offene Hinweise", len(pdb.offene_hinweise(UID)) == 2)
    c = _client(UID, "mitglied@example.org")
    r = c.post("/konto/erinnerungen", data={"an": "0"})
    check("M abbestellt", r.status_code in (302, 303) and _erinnerungen(UID) == 0)
    check("M offene Hinweise als gesendet markiert", pdb.offene_hinweise(UID) == [],
          str(pdb.offene_hinweise(UID)))
    pdb.neuer_hinweis(ADMIN_ID, "EUDR", "inhalt", "fremd", HEUTE)
    c.post("/konto/erinnerungen", data={"an": "1"})
    check("M wieder an; Hinweise anderer Konten unberuehrt",
          _erinnerungen(UID) == 1 and len(pdb.offene_hinweise(ADMIN_ID)) == 1)


if __name__ == "__main__":
    for block in (block_a, block_b, block_c, block_d, block_e, block_f, block_g, block_h,
                  block_i, block_j, block_k, block_l, block_m):
        block()
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER:")
        for f in _failures:
            print("  -", f)
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
