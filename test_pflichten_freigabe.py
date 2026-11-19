"""Tests zum Pflichten-Plan, Aufgabe 5: Vorschlaege, Freigabe, Handpflege.

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_freigabe.py

Kein Netz, kein LLM, festes `today`. Eigene DB `data/esg_pflichten_freigabe_test.db`.

Bloecke:
  A  aendern: Rolle, Version +1, Versionseintrag, geprueft_am
  B  zweites freigeben: False, nichts aendert sich
  C  verwerfen: Schritt unveraendert, Status + Grund
  D  Hinweise: Schalter an, EUDR-Konto genau einer, entfallenes Konto keiner
  E  Startbestand: kein Hinweis, geaendert_am unveraendert
  F  Schalter aus: kein Hinweis
  G  deaktivieren: Schritt fehlt in schritte_fuer und im Plan
  H  neu + aenderungen ueberschreiben nachher; Export
  I  Routen-Rechte, Handpflege-Formular, Validierung
  L  'geaendert' ueber meldung_version (Hand-Freigabe, Abhaken, Startbestand am selben Tag)
  M  Freigabe ohne inhaltliche Aenderung: kein Hinweis, keine meldung_version, keine Version
  N  Bestaetigungs-Vorschlag, vom Admin vor der Freigabe geaendert: normale Aenderung
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_freigabe_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
os.environ["PUBLIC_BASE_URL"] = "https://test.example"
os.environ.pop("PFLICHTEN_PLAN", None)
for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[v] = ""
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import pflichten  # noqa: E402
import pflichten_db as pdb  # noqa: E402
import app as flaskapp  # noqa: E402

assert db.DB_PATH == TEST_DB, "falsche Datenbank!"

_failures: list[str] = []
HEUTE = date(2026, 11, 19)
flaskapp._heute = lambda: HEUTE

import pflichten_vorschlag  # noqa: E402


async def _uebersetzen_kopie(texte_de, ask=None):
    """Kein LLM im Test: fremde Sprachen bekommen den deutschen Text (wie der alte Platzhalter)."""
    return {lang: {f: texte_de[f] for f in pdb.TEXTFELDER if f in texte_de}
            for lang in pflichten_vorschlag.ZIELSPRACHEN}


pflichten_vorschlag.uebersetzen = _uebersetzen_kopie


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def _sql(sql: str, params=()) -> None:
    with db._conn() as c:
        c.execute(sql, params)


def _eins(sql: str, params=()):
    with db._conn() as c:
        return c.execute(sql, params).fetchone()[0]


def _client(uid: int, email: str):
    client = flaskapp.app.test_client()
    with client.session_transaction() as s:
        s["user_id"] = uid
        s["user_email"] = email
    return client


PW = "Geheim-Passwort-123"
STAMM = "mschuckert@textil-mode.de"
STAMM_ID = db.create_user(STAMM, PW)
ERNANNT = "ernannt@example.org"
ERNANNT_ID = db.create_user(ERNANNT, PW)
MITGLIED = "mitglied@example.org"
UID = db.create_user(MITGLIED, PW)
WEG = "weg@example.org"
WEG_ID = db.create_user(WEG, PW)
for _u in (STAMM_ID, ERNANNT_ID, UID, WEG_ID):
    _sql("UPDATE users SET approved = 1 WHERE id = ?", (_u,))
db.set_admin(ERNANNT_ID, True)

# UID hat EUDR aktiv, WEG_ID hatte EUDR, ist aber entfallen.
_sql("INSERT INTO nutzer_pflichten (user_id, reg_key, erste_feststellung) VALUES (?, 'EUDR', ?)",
     (UID, "2026-11-01"))
_sql("INSERT INTO nutzer_pflichten (user_id, reg_key, erste_feststellung, entfallen_am)"
     " VALUES (?, 'EUDR', ?, ?)", (WEG_ID, "2026-10-01", "2026-11-02"))

EUDR = [s["id"] for s in pdb.schritte_fuer("EUDR", "de")]
assert len(EUDR) >= 4, "Startbestand fehlt"


def _hinweise() -> int:
    return _eins("SELECT COUNT(*) FROM pflicht_hinweise")


def _versionen(sid: int) -> int:
    return _eins("SELECT COUNT(*) FROM pflicht_schritt_versionen WHERE schritt_id = ?", (sid,))


def block_a() -> None:
    print("\n--- A  aendern + freigeben ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "0")
    vorher = pdb.schritt(EUDR[0])
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "einkauf"},
                              schritt_id=EUDR[0], beleg="Art. 9", begruendung="Test")
    v = pdb.vorschlag(vid)
    check("A Vorschlag offen", v and v["status"] == "offen")
    check("A vorher aus dem Schritt", v and v["vorher"]["rolle"] == vorher["rolle"]
          and v["vorher"]["texte"]["de"]["titel"] == vorher["texte"]["de"]["titel"])
    check("A in offene_vorschlaege", vid in [o["id"] for o in pdb.offene_vorschlaege()])
    ok = pdb.freigeben(vid, STAMM, None, HEUTE)
    nachher = pdb.schritt(EUDR[0])
    check("A freigeben True", ok is True)
    check("A Rolle uebernommen", nachher["rolle"] == "einkauf", nachher["rolle"])
    check("A Version +1", nachher["version"] == vorher["version"] + 1,
          f"{vorher['version']} -> {nachher['version']}")
    check("A ein Versionseintrag", _versionen(EUDR[0]) == 1)
    check("A geprueft_am = heute", nachher["geprueft_am"] == "2026-11-19", str(nachher["geprueft_am"]))
    check("A Texte unveraendert", nachher["texte"]["de"]["titel"] == vorher["texte"]["de"]["titel"])
    v = pdb.vorschlag(vid)
    check("A Status freigegeben", v["status"] == "freigegeben" and v["entschieden_von"] == STAMM)
    check("A nicht mehr offen", vid not in [o["id"] for o in pdb.offene_vorschlaege()])


def block_b() -> None:
    print("\n--- B  zweites freigeben ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "logistik"},
                              schritt_id=EUDR[1])
    check("B erstes freigeben True", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    version = pdb.schritt(EUDR[1])["version"]
    hinweise = _hinweise()
    check("B zweites freigeben False", pdb.freigeben(vid, STAMM, None, HEUTE) is False)
    check("B Version unveraendert", pdb.schritt(EUDR[1])["version"] == version)
    check("B Hinweiszahl unveraendert", _hinweise() == hinweise)
    check("B verwerfen nach Freigabe False", pdb.verwerfen(vid, STAMM, "x", HEUTE) is False)
    check("B unbekannte ID False", pdb.freigeben(999999, STAMM, None, HEUTE) is False)


def block_c() -> None:
    print("\n--- C  verwerfen ---")
    vorher = pdb.schritt(EUDR[2])
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "watchdog", {"rolle": "finanzen"},
                              schritt_id=EUDR[2])
    check("C verwerfen True", pdb.verwerfen(vid, STAMM, "kein Bezug", HEUTE) is True)
    nachher = pdb.schritt(EUDR[2])
    check("C Schritt unveraendert", nachher == vorher)
    v = pdb.vorschlag(vid)
    check("C Status verworfen + Grund", v["status"] == "verworfen" and v["grund"] == "kein Bezug")
    check("C freigeben danach False", pdb.freigeben(vid, STAMM, None, HEUTE) is False)
    check("C Schritt weiter unveraendert", pdb.schritt(EUDR[2]) == vorher)


def block_d() -> None:
    print("\n--- D  Hinweise bei Schalter an ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    _sql("DELETE FROM pflicht_hinweise")
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "watchdog", {"frist_typ": "fest",
                              "frist_wert": "31.12.2027"}, schritt_id=EUDR[2])
    pdb.freigeben(vid, STAMM, None, HEUTE)
    check("D genau ein Hinweis", _hinweise() == 1, str(_hinweise()))
    check("D fuer das EUDR-Konto", _eins("SELECT COUNT(*) FROM pflicht_hinweise WHERE user_id=?"
                                        " AND reg_key='EUDR' AND art='inhalt'", (UID,)) == 1)
    check("D entfallenes Konto keiner",
          _eins("SELECT COUNT(*) FROM pflicht_hinweise WHERE user_id=?", (WEG_ID,)) == 0)
    check("D geaendert_am = heute", pdb.schritt(EUDR[2])["geaendert_am"] == "2026-11-19")
    # Nur ein neuer Frist-Wert, der zum bestehenden Typ 'fest' nicht passt.
    version = pdb.schritt(EUDR[2])["version"]
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "watchdog", {"frist_wert": "-6m"},
                              schritt_id=EUDR[2])
    check("D unpassender Frist-Wert: False", pdb.freigeben(vid, STAMM, None, HEUTE) is False)
    check("D unpassender Frist-Wert: offen, unveraendert",
          pdb.vorschlag(vid)["status"] == "offen" and pdb.schritt(EUDR[2])["version"] == version)
    pdb.verwerfen(vid, STAMM, "Test", HEUTE)


def block_e() -> None:
    print("\n--- E  Startbestand ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    _sql("DELETE FROM pflicht_hinweise")
    _sql("UPDATE pflicht_schritte SET geaendert_am = NULL WHERE id = ?", (EUDR[3],))
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "startbestand", {"rolle": "produkt"},
                              schritt_id=EUDR[3])
    check("E freigeben True", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    check("E kein Hinweis", _hinweise() == 0)
    s = pdb.schritt(EUDR[3])
    check("E geaendert_am unveraendert", s["geaendert_am"] is None, str(s["geaendert_am"]))
    check("E geprueft_am gesetzt", s["geprueft_am"] == "2026-11-19")


def block_f() -> None:
    print("\n--- F  Schalter aus ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "0")
    _sql("DELETE FROM pflicht_hinweise")
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "gf"}, schritt_id=EUDR[0])
    check("F freigeben True", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    check("F kein Hinweis", _hinweise() == 0)


def block_g() -> None:
    print("\n--- G  deaktivieren ---")
    db.upsert_company(UID, {"name": "Leder GmbH", "employees": 120, "materials": ["Leder"]})
    db.save_analysis(UID, [{"key": "EUDR", "name": "EUDR", "applies": "ja"}])
    ziel = EUDR[1]
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    ids = [s["id"] for p in plan["pflichten"] for s in p["schritte"]]
    check("G vorher im Plan", ziel in ids)
    vid = pdb.neuer_vorschlag("EUDR", "deaktivieren", "hand", {}, schritt_id=ziel)
    check("G freigeben True", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    check("G fehlt in schritte_fuer", ziel not in [s["id"] for s in pdb.schritte_fuer("EUDR", "de")])
    check("G noch in schritte_fuer(nur_aktiv=False)",
          ziel in [s["id"] for s in pdb.schritte_fuer("EUDR", "de", nur_aktiv=False)])
    plan = pflichten.plan_fuer(UID, "de", HEUTE)
    ids = [s["id"] for p in plan["pflichten"] for s in p["schritte"]]
    check("G nicht mehr im Plan", ziel not in ids)


def block_h() -> None:
    print("\n--- H  neu, Ueberschreiben, Export ---")
    texte = {lang: {"titel": f"Neu {lang}", "beschreibung": "B", "daten": "D"}
             for lang in pdb.SPRACHEN}
    vid = pdb.neuer_vorschlag("EUDR", "neu", "hand", {"rolle": "einkauf", "frist_typ": "keine",
                              "frist_wert": "", "sortierung": 9, "texte": texte})
    check("H neu: vorher leer", pdb.vorschlag(vid)["vorher"] is None)
    aend = {"rolle": "logistik", "texte": {"de": {"titel": "Neu de korrigiert"}}}
    check("H freigeben True", pdb.freigeben(vid, STAMM, aend, HEUTE) is True)
    v = pdb.vorschlag(vid)
    sid = v["schritt_id"]
    s = pdb.schritt(sid) if sid else None
    check("H Schritt angelegt", s is not None and s["reg_key"] == "EUDR" and s["aktiv"] == 1)
    check("H Aenderung ueberschreibt Rolle", s and s["rolle"] == "logistik")
    check("H Aenderung ueberschreibt Titel, Rest bleibt",
          s and s["texte"]["de"]["titel"] == "Neu de korrigiert"
          and s["texte"]["de"]["beschreibung"] == "B" and s["texte"]["en"]["titel"] == "Neu en")
    check("H Versionseintrag", sid and _versionen(sid) == 1)
    inhalt = json.loads(_eins("SELECT inhalt_json FROM pflicht_schritt_versionen"
                              " WHERE schritt_id = ?", (sid,)))
    check("H Versionsinhalt mit Texten", inhalt.get("texte", {}).get("de", {}).get("titel")
          == "Neu de korrigiert")
    exp = pdb.katalog_export()
    alle = {x["id"]: x for x in exp["schritte"]}
    check("H Export enthaelt neuen Schritt mit Texten",
          sid in alle and alle[sid]["texte"]["en"]["titel"] == "Neu en")
    check("H Export enthaelt deaktivierte", EUDR[1] in alle and alle[EUDR[1]]["aktiv"] == 0)


def block_i() -> None:
    print("\n--- I  Routen ---")
    stamm = _client(STAMM_ID, STAMM)
    ernannt = _client(ERNANNT_ID, ERNANNT)
    mitglied = _client(UID, MITGLIED)

    r = mitglied.get("/admin/pflichten")
    check("I Mitglied GET -> Dashboard", r.status_code in (302, 303)
          and r.headers.get("Location", "").endswith("/dashboard"), r.headers.get("Location", ""))
    r = flaskapp.app.test_client().get("/admin/pflichten")
    check("I ohne Anmeldung -> Umleitung", r.status_code in (302, 303))
    check("I ernannt GET 200", ernannt.get("/admin/pflichten").status_code == 200)
    r = stamm.get("/admin/pflichten")
    check("I Stamm GET 200", r.status_code == 200)
    check("I Export-Link", "/admin/pflichten/export.json" in r.get_data(as_text=True))

    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "personal"},
                              schritt_id=EUDR[0])
    check("I ernannt Vorschlagsseite 200",
          ernannt.get(f"/admin/pflichten/vorschlag/{vid}").status_code == 200)
    check("I ernannt Liste 200", ernannt.get("/admin/pflichten/vorschlaege").status_code == 200)
    r = ernannt.post(f"/admin/pflichten/vorschlag/{vid}/freigeben", data={})
    check("I ernannt freigeben 403", r.status_code == 403, str(r.status_code))
    check("I nach 403 noch offen", pdb.vorschlag(vid)["status"] == "offen")
    check("I ernannt verwerfen 403",
          ernannt.post(f"/admin/pflichten/vorschlag/{vid}/verwerfen",
                       data={"grund": "x"}).status_code == 403)
    check("I ernannt Schalter 403",
          ernannt.post("/admin/pflichten/schalter", data={"aktiv": "1"}).status_code == 403)
    check("I ernannt Handpflege 403",
          ernannt.post(f"/admin/pflichten/schritt/{EUDR[0]}", data={"titel": "x"}).status_code == 403)
    check("I Mitglied freigeben nicht moeglich",
          mitglied.post(f"/admin/pflichten/vorschlag/{vid}/freigeben").status_code in (302, 303, 403)
          and pdb.vorschlag(vid)["status"] == "offen")

    r = stamm.get(f"/admin/pflichten/vorschlag/{vid}")
    check("I Stamm Vorschlagsseite: Freigeben-Knopf",
          f"/admin/pflichten/vorschlag/{vid}/freigeben" in r.get_data(as_text=True))
    r = stamm.post(f"/admin/pflichten/vorschlag/{vid}/freigeben", data={})
    check("I Stamm freigeben Redirect", r.status_code in (302, 303), str(r.status_code))
    check("I Status freigegeben", pdb.vorschlag(vid)["status"] == "freigegeben")
    check("I Rolle personal", pdb.schritt(EUDR[0])["rolle"] == "personal")

    vid2 = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "gf"}, schritt_id=EUDR[0])
    r = stamm.post(f"/admin/pflichten/vorschlag/{vid2}/verwerfen", data={"grund": "doppelt"})
    check("I Stamm verwerfen", r.status_code in (302, 303)
          and pdb.vorschlag(vid2)["status"] == "verworfen" and pdb.vorschlag(vid2)["grund"] == "doppelt")

    r = stamm.post("/admin/pflichten/schalter", data={"aktiv": "0"})
    check("I Schalter aus", r.status_code in (302, 303)
          and pdb.einstellung("pflichten_plan_aktiv") == "0")
    stamm.post("/admin/pflichten/schalter", data={"aktiv": "1"})
    check("I Schalter an", pdb.einstellung("pflichten_plan_aktiv") == "1")

    # Handpflege: Formular -> Vorschlag 'hand' mit allen sechs Sprachen.
    check("I Formular GET", stamm.get(f"/admin/pflichten/schritt/{EUDR[0]}").status_code == 200)
    check("I Formular neu GET", stamm.get("/admin/pflichten/neu/EUDR").status_code == 200)
    check("I Formular neu unbekannte Regulierung 404",
          stamm.get("/admin/pflichten/neu/GIBTSNICHT").status_code == 404)
    vor = {o["id"] for o in pdb.offene_vorschlaege()}
    form = {"titel": "Hand Titel", "beschreibung": "Hand B", "daten": "Hand D",
            "rolle": "einkauf", "frist_typ": "fest", "frist_wert": "31.12.2027",
            "link": "https://example.org/x", "quelle": "Q", "sortierung": "3"}
    r = stamm.post(f"/admin/pflichten/schritt/{EUDR[0]}", data=form)
    neu = [o for o in pdb.offene_vorschlaege() if o["id"] not in vor]
    check("I Handpflege erzeugt einen Vorschlag", len(neu) == 1)
    if neu:
        v = neu[0]
        check("I Redirect auf Vorschlagsseite", r.status_code in (302, 303)
              and r.headers.get("Location", "").endswith(f"/admin/pflichten/vorschlag/{v['id']}"),
              r.headers.get("Location", ""))
        check("I ausloeser hand, art aendern", v["ausloeser"] == "hand" and v["art"] == "aendern")
        check("I alle sechs Sprachen", sorted(v["nachher"]["texte"]) == sorted(pdb.SPRACHEN))
        check("I Platzhalter kopiert Deutsch",
              v["nachher"]["texte"]["fr"]["titel"] == "Hand Titel")
        # Freigabe mit Korrektur aus dem Formular der Vorschlagsseite
        r = stamm.post(f"/admin/pflichten/vorschlag/{v['id']}/freigeben",
                       data={**{k: v["nachher"][k] for k in ("rolle", "frist_typ", "frist_wert",
                                                              "link", "quelle")},
                             "sortierung": "3",
                             **{f"{f}_{lang}": v["nachher"]["texte"][lang][f]
                                for lang in pdb.SPRACHEN for f in pdb.TEXTFELDER},
                             "titel_en": "Hand title"})
        s = pdb.schritt(EUDR[0])
        check("I Freigabe mit Korrektur", s["texte"]["en"]["titel"] == "Hand title"
              and s["texte"]["de"]["titel"] == "Hand Titel" and s["frist_wert"] == "31.12.2027")

    vor = {o["id"] for o in pdb.offene_vorschlaege()}
    r = stamm.post("/admin/pflichten/neu/EUDR", data={**form, "titel": "Ganz neu"})
    neu = [o for o in pdb.offene_vorschlaege() if o["id"] not in vor]
    check("I neu erzeugt Vorschlag art neu", len(neu) == 1 and neu[0]["art"] == "neu"
          and neu[0]["schritt_id"] is None)

    # Validierung
    def _abgelehnt(label: str, data: dict) -> None:
        vor = {o["id"] for o in pdb.offene_vorschlaege()}
        r = stamm.post(f"/admin/pflichten/schritt/{EUDR[0]}", data={**form, **data})
        neu = [o for o in pdb.offene_vorschlaege() if o["id"] not in vor]
        check(f"I abgelehnt: {label}", not neu and r.status_code == 400, str(r.status_code))

    _abgelehnt("Rolle unbekannt", {"rolle": "chef"})
    _abgelehnt("Frist-Typ unbekannt", {"frist_typ": "bald"})
    _abgelehnt("Frist-Wert unbrauchbar", {"frist_typ": "fest", "frist_wert": "32.13.2027"})
    _abgelehnt("relativ ohne Versatz", {"frist_typ": "relativ", "frist_wert": "6 Monate"})
    _abgelehnt("Link javascript:", {"link": "javascript:alert(1)"})
    _abgelehnt("Titel leer", {"titel": "  "})

    vid3 = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "gf"}, schritt_id=EUDR[0])
    r = stamm.post(f"/admin/pflichten/vorschlag/{vid3}/freigeben",
                   data={"rolle": "gf", "frist_typ": "jaehrlich", "frist_wert": "31.02."})
    check("I Freigabe mit ungueltiger Frist abgelehnt",
          pdb.vorschlag(vid3)["status"] == "offen")

    r = stamm.get("/admin/pflichten/export.json")
    check("I Export JSON", r.status_code == 200 and r.is_json
          and any(x["id"] == EUDR[0] for x in r.get_json()["schritte"]))
    check("I Mitglied Export -> Umleitung",
          mitglied.get("/admin/pflichten/export.json").status_code in (302, 303))


class _FormLeser(HTMLParser):
    """Liest die Felder des Freigabe-Formulars so, wie ein Browser sie senden wuerde."""

    def __init__(self, action: str):
        super().__init__()
        self.action, self.drin, self.daten = action, False, {}
        self._select = self._textarea = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form":
            self.drin = a.get("action", "").endswith(self.action)
        elif not self.drin:
            return
        elif tag == "input" and a.get("name"):
            self.daten[a["name"]] = a.get("value") or ""
        elif tag == "select":
            self._select = a.get("name")
            self._gewaehlt = False
            self._erste = None
        elif tag == "option" and self._select:
            if self._erste is None:
                self._erste = a.get("value") or ""
            if "selected" in a:
                self.daten[self._select] = a.get("value") or ""
                self._gewaehlt = True
        elif tag == "textarea":
            self._textarea = a.get("name")
            self.daten[self._textarea] = ""

    def handle_endtag(self, tag):
        if tag == "form":
            self.drin = False
        elif tag == "select":
            # Wie ein Browser: ohne `selected` wird die erste Option gesendet.
            if self._select and not self._gewaehlt and self._erste is not None:
                self.daten[self._select] = self._erste
            self._select = None
        elif tag == "textarea":
            self._textarea = None

    def handle_data(self, data):
        if self._textarea:
            self.daten[self._textarea] += data


def _formular(client, vid: int) -> dict:
    leser = _FormLeser(f"/admin/pflichten/vorschlag/{vid}/freigeben")
    leser.feed(client.get(f"/admin/pflichten/vorschlag/{vid}").get_data(as_text=True))
    return leser.daten


def block_j() -> None:
    print("\n--- J  Korrekturrunde 1: verlorene Aenderung, leerer Titel ---")
    stamm = _client(STAMM_ID, STAMM)
    sid = EUDR[2]
    _sql("UPDATE pflicht_schritte SET rolle = '', quelle = NULL WHERE id = ?", (sid,))
    a = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "gf"}, schritt_id=sid)
    b = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"quelle": "Leitfaden 2027"},
                            schritt_id=sid)
    form_b_alt = _formular(stamm, b)            # B geoeffnet, bevor A freigegeben wird
    stamm.post(f"/admin/pflichten/vorschlag/{a}/freigeben", data=_formular(stamm, a))
    check("J A freigegeben, Rolle gf", pdb.schritt(sid)["rolle"] == "gf")
    html = stamm.get(f"/admin/pflichten/vorschlag/{b}").get_data(as_text=True)
    check("J Warnung: Schritt seit Vorschlag geaendert", "seit diesem Vorschlag geändert" in html)
    form_b_neu = _formular(stamm, b)
    check("J Seite B zeigt aktuelle Rolle", form_b_neu.get("rolle") == "gf",
          repr(form_b_neu.get("rolle")))
    r = stamm.post(f"/admin/pflichten/vorschlag/{b}/freigeben", data=form_b_alt)
    s = pdb.schritt(sid)
    check("J B (altes Formular) freigegeben", r.status_code in (302, 303)
          and pdb.vorschlag(b)["status"] == "freigegeben")
    check("J Rolle bleibt gf", s["rolle"] == "gf", repr(s["rolle"]))
    check("J Quelle aktualisiert", s["quelle"] == "Leitfaden 2027", repr(s["quelle"]))

    # Frisches Formular ohne Eingriff: nur das vorgeschlagene Feld aendert sich.
    c = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"sortierung": 7}, schritt_id=sid)
    stamm.post(f"/admin/pflichten/vorschlag/{c}/freigeben", data=_formular(stamm, c))
    s = pdb.schritt(sid)
    check("J frisches Formular: nur Sortierung", s["sortierung"] == 7 and s["rolle"] == "gf"
          and s["quelle"] == "Leitfaden 2027")

    # Handpflege legt nur abweichende Felder in `nachher`.
    vor = {o["id"] for o in pdb.offene_vorschlaege()}
    de = s["texte"]["de"]
    stamm.post(f"/admin/pflichten/schritt/{sid}", data={
        "titel": de["titel"], "beschreibung": de["beschreibung"], "daten": de["daten"],
        "rolle": "gf", "frist_typ": s["frist_typ"], "frist_wert": s["frist_wert"],
        "link": s["link"] or "", "quelle": "Neue Quelle", "sortierung": str(s["sortierung"])})
    neu = [o for o in pdb.offene_vorschlaege() if o["id"] not in vor]
    check("J Handpflege: nur geaenderte Felder", len(neu) == 1
          and neu[0]["nachher"] == {"quelle": "Neue Quelle"}, repr(neu and neu[0]["nachher"]))
    if neu:
        pdb.verwerfen(neu[0]["id"], STAMM, "Test", HEUTE)

    # Handpflege A aendert nur den Titel, B nur die Beschreibung; beide vor jeder
    # Freigabe angelegt. Nach beiden Freigaben muessen beide Aenderungen stehen.
    basis = {"daten": de["daten"], "rolle": "gf", "frist_typ": s["frist_typ"],
             "frist_wert": s["frist_wert"], "link": s["link"] or "",
             "quelle": s["quelle"] or "", "sortierung": str(s["sortierung"])}
    vor = {o["id"] for o in pdb.offene_vorschlaege()}
    stamm.post(f"/admin/pflichten/schritt/{sid}", data={
        **basis, "titel": "Titel aus A", "beschreibung": de["beschreibung"]})
    stamm.post(f"/admin/pflichten/schritt/{sid}", data={
        **basis, "titel": de["titel"], "beschreibung": "Beschreibung aus B"})
    neu = sorted(o["id"] for o in pdb.offene_vorschlaege() if o["id"] not in vor)
    check("J Text A/B: zwei Vorschlaege", len(neu) == 2, str(neu))
    if len(neu) == 2:
        va, vb = (pdb.vorschlag(x) for x in neu)
        check("J Text A/B: nachher nur das geaenderte Textfeld",
              all(set(t) == {"titel"} for t in va["nachher"]["texte"].values())
              and all(set(t) == {"beschreibung"} for t in vb["nachher"]["texte"].values())
              and len(va["nachher"]["texte"]) == len(pdb.SPRACHEN))
        stamm.post(f"/admin/pflichten/vorschlag/{va['id']}/freigeben",
                   data=_formular(stamm, va["id"]))
        stamm.post(f"/admin/pflichten/vorschlag/{vb['id']}/freigeben",
                   data=_formular(stamm, vb["id"]))
        t = pdb.schritt(sid)["texte"]
        check("J Text A/B: beide Aenderungen bleiben",
              t["de"]["titel"] == "Titel aus A" and t["de"]["beschreibung"] == "Beschreibung aus B"
              and t["fr"]["titel"] == "Titel aus A"
              and t["fr"]["beschreibung"] == "Beschreibung aus B", repr(t["de"]))
        de = t["de"]

    # Leerer deutscher Titel: nie freigebbar (aendern per Formular, neu per Vorschlag).
    d = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": "einkauf"}, schritt_id=sid)
    form = {**_formular(stamm, d), "titel_de": "  "}
    r = stamm.post(f"/admin/pflichten/vorschlag/{d}/freigeben", data=form)
    check("J leerer Titel (aendern): offen, Schritt unveraendert",
          pdb.vorschlag(d)["status"] == "offen" and pdb.schritt(sid)["rolle"] == "gf"
          and pdb.schritt(sid)["texte"]["de"]["titel"] == de["titel"])
    check("J leerer Titel: zurueck auf die Vorschlagsseite",
          r.headers.get("Location", "").endswith(f"/admin/pflichten/vorschlag/{d}"))
    html = stamm.get(f"/admin/pflichten/vorschlag/{d}").get_data(as_text=True)
    check("J Meldung nennt den Grund", "ungültig" in html and "Titel" in html)
    anzahl = _eins("SELECT COUNT(*) FROM pflicht_schritte")
    # Frist-Typ und Sortierung ausdruecklich gesetzt: sonst koennte die Ablehnung
    # an Frist oder Sortierung haengen statt am leeren Titel.
    e = pdb.neuer_vorschlag("EUDR", "neu", "hand", {"frist_typ": "keine", "sortierung": 1,
                            "texte": {"de": {"titel": ""}}})
    r = stamm.post(f"/admin/pflichten/vorschlag/{e}/freigeben", data=_formular(stamm, e))
    check("J leerer Titel (neu): offen, kein Schritt angelegt",
          pdb.vorschlag(e)["status"] == "offen"
          and _eins("SELECT COUNT(*) FROM pflicht_schritte") == anzahl)
    ok, grund = pdb.freigeben_mit_grund(e, STAMM, None, HEUTE)
    check("J Grund leerer Titel", not ok and grund.startswith("ungültig") and "Titel" in grund,
          grund)
    pdb.verwerfen(d, STAMM, "Test", HEUTE)
    pdb.verwerfen(e, STAMM, "Test", HEUTE)
    ok, grund = pdb.freigeben_mit_grund(e, STAMM, None, HEUTE)
    check("J Grund nicht mehr offen", not ok and grund == pdb.NICHT_OFFEN, grund)

    # KI-Vorschlag 'neu' ohne Frist-Typ: Auswahl steht auf 'keine', Freigabe gelingt.
    f = pdb.neuer_vorschlag("EUDR", "neu", "watchdog", {"texte": {"de": {"titel": "Ohne Frist"}}})
    form = _formular(stamm, f)
    check("J neu ohne Frist-Typ: Auswahl 'keine'", form.get("frist_typ") == "keine",
          repr(form.get("frist_typ")))
    stamm.post(f"/admin/pflichten/vorschlag/{f}/freigeben", data=form)
    v = pdb.vorschlag(f)
    check("J neu ohne Frist-Typ: freigegeben, Typ keine", v["status"] == "freigegeben"
          and pdb.schritt(v["schritt_id"])["frist_typ"] == "keine", v["status"])


def block_k() -> None:
    print("\n--- K  Kleinigkeiten: Frist keine, Sortierung, Link, Menue ---")
    sid = EUDR[2]
    v = pdb.neuer_vorschlag("EUDR", "aendern", "hand",
                            {"frist_typ": "keine", "frist_wert": "-6m"}, schritt_id=sid)
    check("K freigeben", pdb.freigeben(v, STAMM, None, HEUTE) is True)
    s = pdb.schritt(sid)
    check("K Frist keine -> Wert leer", s["frist_typ"] == "keine" and s["frist_wert"] == "",
          repr(s["frist_wert"]))
    hoechste = _eins("SELECT MAX(sortierung) FROM pflicht_schritte WHERE reg_key = 'EUDR'")
    v = pdb.neuer_vorschlag("EUDR", "neu", "hand", {"link": "HTTPS://Example.org/Pfad",
                            "texte": {"de": {"titel": "Ans Ende"}}})
    check("K neu ohne Sortierung freigegeben", pdb.freigeben(v, STAMM, None, HEUTE) is True)
    s = pdb.schritt(pdb.vorschlag(v)["schritt_id"])
    check("K neu ans Ende", s["sortierung"] == hoechste + 1, f"{s['sortierung']} vs {hoechste}")
    check("K Link-Schema klein", s["link"] == "https://Example.org/Pfad", s["link"])

    html = _client(STAMM_ID, STAMM).get("/passwort-aendern").get_data(as_text=True)
    check("K Menue: Link fuer Admin", 'href="/admin/pflichten"' in html)
    html = _client(ERNANNT_ID, ERNANNT).get("/passwort-aendern").get_data(as_text=True)
    check("K Menue: Link fuer ernannten Admin", 'href="/admin/pflichten"' in html)
    html = _client(UID, MITGLIED).get("/passwort-aendern").get_data(as_text=True)
    check("K Menue: kein Link fuer Mitglied", "/admin/pflichten" not in html)
    os.environ["PFLICHTEN_PLAN"] = "aus"
    try:
        html = _client(STAMM_ID, STAMM).get("/passwort-aendern").get_data(as_text=True)
        check("K Menue: kein Link bei PFLICHTEN_PLAN=aus", "/admin/pflichten" not in html)
    finally:
        os.environ.pop("PFLICHTEN_PLAN", None)


def _plan_schritt(uid: int, sid: int, tag=HEUTE) -> dict:
    for p in pflichten.plan_fuer(uid, "de", tag)["pflichten"]:
        for s in p["schritte"]:
            if s["id"] == sid:
                return s
    raise AssertionError(f"Schritt {sid} nicht im Plan")


def _meldung(sid: int):
    return _eins("SELECT meldung_version FROM pflicht_schritte WHERE id = ?", (sid,))


def block_l() -> None:
    print("\n--- L  geaendert ueber meldung_version ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    uid = db.create_user("meldung@example.org", PW)
    db.save_analysis(uid, [{"key": "EUDR", "name": "EUDR", "applies": "ja"}])
    sid = EUDR[0]
    rolle = pdb.schritt(sid)["rolle"]
    neu = "finanzen" if rolle != "finanzen" else "personal"
    # (1) meldepflichtige Hand-Freigabe, (2) Abhaken, (3) Startbestand-Freigabe - alles heute
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": neu}, schritt_id=sid)
    check("L Hand-Freigabe", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    version = pdb.schritt(sid)["version"]
    check("L Hand-Freigabe setzt meldung_version = Version", _meldung(sid) == version,
          f"{_meldung(sid)} / {version}")
    pdb.setze_erledigt(uid, sid, "", True, HEUTE)
    check("L nach Abhaken: nicht geaendert", _plan_schritt(uid, sid)["geaendert"] is False)
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "startbestand", {"rolle": rolle or "gf"},
                              schritt_id=sid)
    check("L Startbestand-Freigabe", pdb.freigeben(vid, STAMM, None, HEUTE) is True)
    check("L Startbestand: Version +1, meldung_version bleibt",
          pdb.schritt(sid)["version"] == version + 1 and _meldung(sid) == version,
          f"{pdb.schritt(sid)['version']} / {_meldung(sid)}")
    check("L Startbestand am selben Tag nach Abhaken: nicht geaendert",
          _plan_schritt(uid, sid)["geaendert"] is False)
    # Schalter aus: Freigabe ohne Meldung
    pdb.setze_einstellung("pflichten_plan_aktiv", "0")
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "hand", {"rolle": neu}, schritt_id=sid)
    pdb.freigeben(vid, STAMM, None, HEUTE)
    check("L Schalter aus: meldung_version bleibt", _meldung(sid) == version)
    check("L Schalter aus: nicht geaendert", _plan_schritt(uid, sid)["geaendert"] is False)
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    # meldepflichtige Freigabe nach dem Abhaken -> geaendert; gesehen -> nicht mehr
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "watchdog", {"rolle": rolle or "gf"},
                              schritt_id=sid)
    pdb.freigeben(vid, STAMM, None, HEUTE)
    s = pdb.schritt(sid)
    check("L meldepflichtige Freigabe: meldung_version = neue Version",
          _meldung(sid) == s["version"], f"{_meldung(sid)} / {s['version']}")
    check("L meldepflichtige Freigabe nach Abhaken: geaendert",
          _plan_schritt(uid, sid)["geaendert"] is True)
    pdb.markiere_gesehen(uid, sid, s["version"])
    check("L gesehen: nicht mehr geaendert", _plan_schritt(uid, sid)["geaendert"] is False)
    pdb.setze_erledigt(uid, sid, "", False, HEUTE)


def block_m() -> None:
    print("\n--- M  Freigabe ohne inhaltliche Aenderung ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    _sql("DELETE FROM pflicht_hinweise")
    sid = EUDR[0]
    vorher = pdb.schritt(sid)
    meldung = _meldung(sid)
    versionen = _versionen(sid)
    faelle = [
        ("gleiches Feld", "aendern", sid, {"rolle": vorher["rolle"]}),
        ("Fremdsprache identisch", "aendern", sid,
         {"texte": {"en": {"titel": vorher["texte"]["en"]["titel"]}}}),
    ]
    inaktiv = EUDR[1]
    check("M Vorbedingung: Schritt inaktiv", pdb.schritt(inaktiv)["aktiv"] == 0)
    faelle.append(("schon inaktiven Schritt deaktivieren", "deaktivieren", inaktiv, {}))
    for name, art, ziel, nachher in faelle:
        v_ziel = pdb.schritt(ziel)
        vid = pdb.neuer_vorschlag("EUDR", art, "hand", nachher, schritt_id=ziel)
        check(f"M {name}: freigegeben", pdb.freigeben(vid, STAMM, None, HEUTE) is True
              and pdb.vorschlag(vid)["status"] == "freigegeben")
        danach = pdb.schritt(ziel)
        check(f"M {name}: keine neue Version", danach["version"] == v_ziel["version"],
              f"{v_ziel['version']} -> {danach['version']}")
        check(f"M {name}: kein Hinweis", _hinweise() == 0, str(_hinweise()))
    check("M keine meldung_version", _meldung(sid) == meldung, f"{meldung} -> {_meldung(sid)}")
    check("M kein Versionseintrag", _versionen(sid) == versionen)


def block_n() -> None:
    print("\n--- N  Bestaetigung, vom Admin geaendert ---")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    _sql("DELETE FROM pflicht_hinweise")
    sid = EUDR[2]
    vorher = pdb.schritt(sid)
    vid = pdb.neuer_vorschlag("EUDR", "aendern", "startbestand", {}, schritt_id=sid)
    check("N ist Bestaetigung", pdb.ist_bestaetigung(pdb.vorschlag(vid)))
    neu = "finanzen" if vorher["rolle"] != "finanzen" else "personal"
    check("N freigeben mit Aenderung",
          pdb.freigeben(vid, STAMM, {"rolle": neu}, HEUTE) is True)
    s = pdb.schritt(sid)
    check("N Rolle uebernommen", s["rolle"] == neu, s["rolle"])
    check("N Version +1", s["version"] == vorher["version"] + 1,
          f"{vorher['version']} -> {s['version']}")
    check("N Versionseintrag", _eins("SELECT COUNT(*) FROM pflicht_schritt_versionen"
                                     " WHERE vorschlag_id = ?", (vid,)) == 1)
    check("N Startbestand: kein Hinweis", _hinweise() == 0)


if __name__ == "__main__":
    for block in (block_a, block_b, block_c, block_d, block_e, block_f, block_g, block_h,
                  block_i, block_j, block_k, block_l, block_m, block_n):
        try:
            block()
        except Exception as exc:  # noqa: BLE001 — jeden Block melden, nicht abbrechen
            check(f"{block.__name__} ohne Ausnahme", False, repr(exc))
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER:")
        for f in _failures:
            print("  -", f)
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
