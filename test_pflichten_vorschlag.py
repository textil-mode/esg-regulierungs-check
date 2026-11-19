"""Tests zum Pflichten-Plan, Aufgabe 6: KI-Vorschlaege und Uebersetzung.

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_vorschlag.py

Kein Netz, kein LLM (Fake-`ask`), festes `today`. Eigene DB
`data/esg_pflichten_vorschlag_test.db`.

Bloecke:
  A  Watchdog-Aenderung: ein Vorschlag, sechs Sprachen, nur geaenderte Felder
  B  leere Liste -> kein Vorschlag
  C  kaputtes JSON -> VorschlagFehler, nichts angelegt
  D  fremde / unbekannte schritt_id -> verworfen
  E  unbrauchbarer Frist-Wert -> verworfen
  F  keine Firmen- oder Kontodaten im Prompt
  G  Startbestand: je ungeprueftem EUDR-Schritt ein Vorschlag, kein Doppel
  H  uebersetzen: nur die gegebenen Felder, unbrauchbare Antwort -> Fehler
  I  benachrichtige_admin: eine Mail, Link, mail_log
  J  Watchdog: use_llm=False unveraendert; use_llm=True ruft Vorschlaege, Fehler im Lauf
  K  Startbestand-Knopf: Rechte, Hintergrund-Start, kein Doppelstart
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import threading
from datetime import date
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_vorschlag_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
os.environ["PUBLIC_BASE_URL"] = "https://test.example"
os.environ.pop("PFLICHTEN_PLAN", None)
for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[v] = ""
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import pflichten_db as pdb  # noqa: E402
import app as flaskapp  # noqa: E402
import pflichten_vorschlag as pv  # noqa: E402
import watchdog  # noqa: E402

# app.py und watchdog.py laden `.env` mit override=True — danach noch einmal
# die Testwerte setzen, damit nichts in die Produktiv-DB oder ans Netz geht.
os.environ["PUBLIC_BASE_URL"] = "https://test.example"
for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[v] = ""
assert db.DB_PATH == TEST_DB, "falsche Datenbank!"

_failures: list[str] = []
HEUTE = date(2026, 11, 19)
flaskapp._heute = lambda: HEUTE


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


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
FIRMA = "Zwirnerei Geheimname GmbH"
KONTO = "geheimkonto@zwirnerei-geheim.example"
KONTO_ID = db.create_user(KONTO, PW)
with db._conn() as _c:
    _c.execute("UPDATE users SET approved = 1")
db.set_admin(ERNANNT_ID, True)
db.upsert_company(KONTO_ID, {"name": FIRMA, "employees": 120})
assert (db.get_company(KONTO_ID) or {}).get("name") == FIRMA, "Profil fehlt"

# Eine Regulierung ohne (aktive) Schritte (Watchdog darf dafuer nichts vorschlagen).
# Deaktivieren statt loeschen: init_db saet geloeschte Startschritte neu.
OHNE = "AbwV55"
with db._conn() as _c:
    _c.execute("UPDATE pflicht_schritte SET aktiv = 0 WHERE reg_key = ?", (OHNE,))
# Zweite Regulierung fuer Startbestand-Randfaelle (nicht EUDR, nicht CSRD).
ZWEIT = "AbwV38"

EUDR = [s["id"] for s in pdb.schritte_fuer("EUDR", "de")]
assert len(EUDR) >= 2, "Startbestand fehlt"
FREMD = _eins("SELECT id FROM pflicht_schritte WHERE reg_key != 'EUDR' ORDER BY id LIMIT 1")

PROMPTS: list[tuple[str, str]] = []


def _uebersetzung_fake(user: str) -> str:
    texte = json.loads(user[user.index("{"):])
    return json.dumps({lang: {f: f"{t} [{lang}]" for f, t in texte.items()}
                       for lang in pv.ZIELSPRACHEN}, ensure_ascii=False)


def fake_ask(haupt):
    """Fake-LLM: Uebersetzungen automatisch, sonst `haupt` (str oder dict)."""
    async def ask(system: str, user: str) -> str:
        PROMPTS.append((system, user))
        if system == pv.SYSTEM_UEBERSETZUNG:
            return _uebersetzung_fake(user)
        return haupt if isinstance(haupt, str) else json.dumps(haupt, ensure_ascii=False)
    return ask


def _offen() -> int:
    return _eins("SELECT COUNT(*) FROM pflicht_vorschlaege WHERE status = 'offen'")


def run(coro):
    return asyncio.run(coro)


def block_a() -> None:
    print("\n--- A  Watchdog-Aenderung ---")
    s = pdb.schritt(EUDR[0])
    andere_rolle = "finanzen" if s["rolle"] != "finanzen" else "gf"
    antwort = {"aenderungen": [{
        "art": "aendern", "schritt_id": EUDR[0],
        "nachher": {"rolle": andere_rolle, "frist_typ": s["frist_typ"],
                    "frist_wert": s["frist_wert"],
                    "titel": "Neuer Titel laut Art. 9",
                    "beschreibung": s["texte"]["de"]["beschreibung"]},
        "beleg": "Art. 9 Abs. 1: neue Pflicht", "begruendung": "Artikel 9 geaendert"}]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "alter Text\nArt. 9 alt",
                                           "alter Text\nArt. 9 neu", fake_ask(antwort),
                                           ausloeser_ref="77"))
    check("A ein Vorschlag", len(ids) == 1, str(ids))
    if not ids:
        return
    v = pdb.vorschlag(ids[0])
    check("A ausloeser watchdog, art aendern", v["ausloeser"] == "watchdog" and v["art"] == "aendern")
    check("A ausloeser_ref = Lauf", v["ausloeser_ref"] == "77", str(v["ausloeser_ref"]))
    check("A Beleg uebernommen", "Art. 9" in (v["beleg"] or ""))
    n = v["nachher"]
    check("A Rolle im nachher", n.get("rolle") == andere_rolle)
    check("A unveraenderte Frist nicht im nachher",
          "frist_typ" not in n and "frist_wert" not in n, str(n))
    check("A Texte in allen sechs Sprachen", sorted(n.get("texte", {})) == sorted(pdb.SPRACHEN))
    check("A nur geaenderter Text (titel)",
          all(set(t) == {"titel"} for t in n.get("texte", {}).values()), str(n.get("texte")))
    check("A deutscher Titel", n["texte"]["de"]["titel"] == "Neuer Titel laut Art. 9")
    check("A englischer Titel uebersetzt", n["texte"]["en"]["titel"] == "Neuer Titel laut Art. 9 [en]")


def block_b() -> None:
    print("\n--- B  leere Liste ---")
    vorher = _offen()
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask({"aenderungen": []})))
    check("B keine Vorschlaege", ids == [] and _offen() == vorher)


def block_c() -> None:
    print("\n--- C  kaputtes JSON ---")
    vorher = _offen()
    try:
        run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask("das ist kein JSON")))
        check("C VorschlagFehler", False, "keine Ausnahme")
    except pv.VorschlagFehler:
        check("C VorschlagFehler", True)
    check("C nichts angelegt", _offen() == vorher)
    try:
        run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask({"falsch": 1})))
        check("C falsche Form -> VorschlagFehler", False)
    except pv.VorschlagFehler:
        check("C falsche Form -> VorschlagFehler", True)


def block_d() -> None:
    print("\n--- D  fremde schritt_id ---")
    vorher = _offen()
    antwort = {"aenderungen": [
        {"art": "aendern", "schritt_id": FREMD, "nachher": {"rolle": "gf"}, "beleg": "x"},
        {"art": "aendern", "schritt_id": 999999, "nachher": {"rolle": "gf"}, "beleg": "x"},
        {"art": "deaktivieren", "schritt_id": FREMD, "nachher": {}, "beleg": "x"},
    ]}
    protokoll: list[str] = []
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort),
                                           verworfen=protokoll))
    check("D alle verworfen", ids == [] and _offen() == vorher, str(ids))
    check("D Verwerfungen gezaehlt", len(protokoll) == 3, str(protokoll))


def block_e() -> None:
    print("\n--- E  Frist-Wert ---")
    vorher = _offen()
    antwort = {"aenderungen": [
        {"art": "aendern", "schritt_id": EUDR[1],
         "nachher": {"frist_typ": "relativ", "frist_wert": "bald"}, "beleg": "x"},
        {"art": "neu", "schritt_id": None,
         "nachher": {"titel": "Neu", "frist_typ": "fest", "frist_wert": "irgendwann"},
         "beleg": "x"},
        {"art": "aendern", "schritt_id": EUDR[1], "nachher": {"rolle": "chef"}, "beleg": "x"},
    ]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort)))
    check("E verworfen", ids == [] and _offen() == vorher, str(ids))
    antwort = {"aenderungen": [{"art": "aendern", "schritt_id": EUDR[1],
                                "nachher": {"frist_typ": "relativ", "frist_wert": "-6m"},
                                "beleg": "Art. 3"}]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort)))
    s = pdb.schritt(EUDR[1])
    erwartet = 0 if (s["frist_typ"], s["frist_wert"]) == ("relativ", "-6m") else 1
    check("E gueltige Frist angenommen", len(ids) == erwartet, str(ids))
    if ids:
        n = pdb.vorschlag(ids[0])["nachher"]
        check("E ohne Texte keine Uebersetzung", "texte" not in n, str(n))


def block_f() -> None:
    print("\n--- F  keine Kontodaten im Prompt ---")
    check("F Prompts gesammelt", len(PROMPTS) > 0)
    alles = "\n".join(s + "\n" + u for s, u in PROMPTS)
    check("F kein Firmenname", FIRMA not in alles)
    check("F keine Konto-E-Mail", KONTO not in alles)
    check("F kein Stamm-Admin", STAMM not in alles)
    haupt = [s for s, _ in PROMPTS if s == pv.SYSTEM_AENDERUNG]
    check("F System-Prompt deutsch mit Regeln", bool(haupt) and "erfinde nichts" in haupt[0].lower()
          and "relativ" in haupt[0] and "jaehrlich" in haupt[0])


def block_g() -> None:
    print("\n--- G  Startbestand ---")
    # Schritte mit offenem Vorschlag (aus A-E) ueberspringt der Startbestand.
    offen = {v["schritt_id"] for v in pdb.offene_vorschlaege()}
    ungeprueft = [s for s in pdb.schritte_fuer("EUDR", "de")
                  if not s["geprueft_am"] and s["id"] not in offen]
    check("G ungepruefte EUDR-Schritte vorhanden", len(ungeprueft) >= 1, str(len(ungeprueft)))
    geladen = []

    def fake_fetch(reg, *, language="de", force=False):
        geladen.append((reg["key"], language, force))
        return {"text": "Artikel 1\nGegenstand.\nArtikel 9\nSorgfaltserklaerung vor Inverkehrbringen."}

    alt = pv.fetcher.fetch_law_text
    pv.fetcher.fetch_law_text = fake_fetch
    try:
        antwort = {"schritte": [
            {"schritt_id": s["id"], "rolle": "einkauf", "frist_typ": "keine", "frist_wert": "",
             "daten": "Geodaten der Erzeugungsflaechen", "beleg": "Art. 9",
             "begruendung": "Art. 9 verlangt Geodaten"} for s in ungeprueft]
            + [{"schritt_id": FREMD, "rolle": "gf", "beleg": "x"}]
            + [{"schritt_id": sid, "rolle": "gf", "beleg": "x"} for sid in offen if sid]}
        vorher = _offen()
        ids = run(pv.startbestand_vorschlaege("EUDR", fake_ask(antwort)))
        check("G je ungeprueftem Schritt ein Vorschlag", len(ids) == len(ungeprueft),
              f"{len(ids)} / {len(ungeprueft)}")
        check("G angelegt", _offen() == vorher + len(ids))
        vs = [pdb.vorschlag(i) for i in ids]
        check("G ausloeser startbestand, art aendern",
              all(v["ausloeser"] == "startbestand" and v["art"] == "aendern" for v in vs))
        check("G Schritte = ungepruefte",
              sorted(v["schritt_id"] for v in vs) == sorted(s["id"] for s in ungeprueft))
        check("G Gesetz ungezwungen aus Cache", geladen and geladen[0] == ("EUDR", "de", False),
              str(geladen))
        check("G Gesetzestext im Prompt", any("Sorgfaltserklaerung" in u for _, u in PROMPTS))
        geaendert = [v for v in vs if "daten" in (v["nachher"].get("texte") or {}).get("de", {})]
        check("G Daten als Text in sechs Sprachen", geaendert and
              sorted(geaendert[0]["nachher"]["texte"]) == sorted(pdb.SPRACHEN))
        ids2 = run(pv.startbestand_vorschlaege("EUDR", fake_ask(antwort)))
        check("G kein Doppel bei zweitem Lauf", ids2 == [], str(ids2))
    finally:
        pv.fetcher.fetch_law_text = alt


def block_h() -> None:
    print("\n--- H  uebersetzen ---")
    out = run(pv.uebersetzen({"titel": "Titel"}, fake_ask({})))
    check("H alle Zielsprachen", sorted(out) == sorted(pv.ZIELSPRACHEN))
    check("H nur gegebene Felder", all(set(t) == {"titel"} for t in out.values()), str(out))
    out = run(pv.uebersetzen({"titel": "T", "beschreibung": "B", "daten": "D"}, fake_ask({})))
    check("H drei Felder", out["zh"] == {"titel": "T [zh]", "beschreibung": "B [zh]",
                                         "daten": "D [zh]"})

    async def kaputt(system, user):
        return "{\"en\": {\"titel\": \"x\"}}"
    try:
        run(pv.uebersetzen({"titel": "T"}, kaputt))
        check("H fehlende Sprache -> VorschlagFehler", False)
    except pv.VorschlagFehler:
        check("H fehlende Sprache -> VorschlagFehler", True)

    async def muell(system, user):
        return "nope"
    try:
        run(pv.uebersetzen({"titel": "T"}, muell))
        check("H kein JSON -> VorschlagFehler", False)
    except pv.VorschlagFehler:
        check("H kein JSON -> VorschlagFehler", True)
    check("H leere Eingabe ohne LLM", run(pv.uebersetzen({}, muell)) ==
          {lang: {} for lang in pv.ZIELSPRACHEN})


def block_i() -> None:
    print("\n--- I  benachrichtige_admin ---")
    gesendet = []

    def versand(empfaenger, betreff, text):
        gesendet.append((empfaenger, betreff, text))
        return "<id@test>"

    vorher = _eins("SELECT COUNT(*) FROM mail_log WHERE purpose = 'pflichten_vorschlag'")
    pv.benachrichtige_admin({"EUDR": 2, "CSRD": 0}, versand=versand)
    check("I genau eine Mail", len(gesendet) == 1, str(len(gesendet)))
    if gesendet:
        empf, betreff, text = gesendet[0]
        check("I an Stamm-Admin", empf == STAMM, empf)
        check("I Zeile EUDR: 2 Vorschläge", "EUDR: 2 Vorschläge" in text, text)
        check("I CSRD ohne Vorschlag fehlt", "CSRD" not in text)
        check("I Link mit Pfad-Praefix",
              "https://test.example/esg/admin/pflichten/vorschlaege" in text, text)
        check("I Betreff Plural", "2 neue KI-Vorschläge" in betreff, betreff)
    nachher = _eins("SELECT COUNT(*) FROM mail_log WHERE purpose = 'pflichten_vorschlag'")
    check("I mail_log", nachher == vorher + 1)
    gesendet.clear()
    pv.benachrichtige_admin({"EUDR": 0}, versand=versand)
    check("I nichts zu melden -> keine Mail", gesendet == [])

    gesendet.clear()
    pv.benachrichtige_admin({"EUDR": 1}, versand=versand)
    check("I Singular", gesendet and "1 neuer KI-Vorschlag" in gesendet[0][1]
          and "EUDR: 1 Vorschlag\n" in gesendet[0][2], str(gesendet))
    gesendet.clear()
    pv.benachrichtige_admin({"EUDR": 0}, versand=versand, fehler=["CSRD: Timeout", "SBTi: x"])
    check("I 0 Vorschlaege mit Fehlern: Mail",
          len(gesendet) == 1 and "keine neuen Vorschläge, 2 Fehler" in gesendet[0][1]
          and "CSRD: Timeout" in gesendet[0][2] and "EUDR" not in gesendet[0][2],
          str(gesendet))
    gesendet.clear()
    pv.benachrichtige_admin({"EUDR": 3}, versand=versand, fehler=["CSRD: Timeout"])
    check("I Vorschlaege und 1 Fehler", gesendet and
          "3 neue KI-Vorschläge, 1 Fehler" in gesendet[0][1], str(gesendet))

    def kaputt(empfaenger, betreff, text):
        raise RuntimeError("SMTP weg")
    pv.benachrichtige_admin({"EUDR": 1}, versand=kaputt)
    check("I Fehler protokolliert",
          _eins("SELECT COUNT(*) FROM mail_log WHERE purpose = 'pflichten_vorschlag'"
                " AND status = 'failed'") == 1)


def block_j() -> None:
    print("\n--- J  Watchdog ---")
    aufrufe = {"vorschlag": [], "admin": []}

    def fake_fetch(reg, *, language="de", force=False):
        if reg["key"] in ("EUDR", "CSRD", OHNE):
            return {"text": f"neu {reg['key']}", "version_new": True, "previous_hash": "h0",
                    "text_hash": "h1"}
        return {"text": "gleich", "version_new": False}

    async def fake_vorschlaege(reg_key, alt, neu, ask=None, *, ausloeser_ref="", verworfen=None):
        aufrufe["vorschlag"].append((reg_key, alt, neu, ausloeser_ref))
        if reg_key == "CSRD":
            raise pv.VorschlagFehler("kaputt")
        return [101, 102]

    async def fake_summary(reg, old, new):
        return "Zusammenfassung"

    gesichert = (watchdog.fetch_law_text, watchdog.version_text, watchdog._summarize,
                 pv.vorschlaege_aus_aenderung, pv.benachrichtige_admin)
    watchdog.fetch_law_text = fake_fetch
    watchdog.version_text = lambda key, lang, h: f"alt {key}"
    watchdog._summarize = fake_summary
    pv.vorschlaege_aus_aenderung = fake_vorschlaege
    pv.benachrichtige_admin = lambda anzahl, **kw: aufrufe["admin"].append(anzahl)
    try:
        res = watchdog.run(use_llm=False)
        check("J ohne LLM: Aenderungen erkannt",
              sorted(e["reg_key"] for e in res["changed"]) == sorted(["CSRD", "EUDR", OHNE]),
              str(res["changed"]))
        check("J ohne LLM: keine Vorschlaege, keine Mail",
              aufrufe["vorschlag"] == [] and aufrufe["admin"] == [])
        check("J ohne LLM: keine Fehler", res["errors"] == [], str(res["errors"]))
        res = watchdog.run(use_llm=True)
        check("J mit LLM: Vorschlaege je Aenderung", sorted(a[0] for a in aufrufe["vorschlag"])
              == ["CSRD", "EUDR"], str(aufrufe["vorschlag"]))
        eudr = [a for a in aufrufe["vorschlag"] if a[0] == "EUDR"][0]
        check("J alter/neuer Text, Lauf-ID", eudr[1] == "alt EUDR" and eudr[2] == "neu EUDR"
              and eudr[3] == str(res["run_id"]), str(eudr))
        check("J Fehler im Lauf, kein Abbruch",
              any(e["reg_key"] == "CSRD" for e in res["errors"]) and len(res["changed"]) == 3,
              str(res["errors"]))
        check("J Admin-Mail mit Anzahl", aufrufe["admin"] == [{"EUDR": 2}], str(aufrufe["admin"]))
        check("J Zusammenfassung bleibt", all(e["summary"] == "Zusammenfassung"
                                              for e in res["changed"]))
    finally:
        (watchdog.fetch_law_text, watchdog.version_text, watchdog._summarize,
         pv.vorschlaege_aus_aenderung, pv.benachrichtige_admin) = gesichert


def block_k() -> None:
    print("\n--- K  Startbestand-Knopf ---")
    stamm = _client(STAMM_ID, STAMM)
    ernannt = _client(ERNANNT_ID, ERNANNT)
    html = stamm.get("/admin/pflichten").get_data(as_text=True)
    check("K Knopf fuer Stamm-Admin", "/admin/pflichten/startbestand" in html)
    html = ernannt.get("/admin/pflichten").get_data(as_text=True)
    check("K kein Knopf fuer ernannten Admin", "/admin/pflichten/startbestand" not in html)
    check("K ernannt 403", ernannt.post("/admin/pflichten/startbestand").status_code == 403)
    check("K GET nicht erlaubt", stamm.get("/admin/pflichten/startbestand").status_code == 405)

    gestartet = []
    alt = pv.starte_startbestand
    pv.starte_startbestand = lambda **kw: gestartet.append(kw) or True
    try:
        r = stamm.post("/admin/pflichten/startbestand")
        check("K Stamm: Redirect", r.status_code in (302, 303), str(r.status_code))
        check("K Hintergrundlauf gestartet", len(gestartet) == 1)
        r = stamm.post("/admin/pflichten/startbestand",
                       headers={"Origin": "https://boese.example"})
        check("K fremde Herkunft abgewiesen", r.status_code in (400, 403) and len(gestartet) == 1,
              str(r.status_code))
    finally:
        pv.starte_startbestand = alt

    # Echter Starter: zweiter Start waehrend eines Laufs wird abgelehnt.
    freigabe = threading.Event()
    fertig = threading.Event()

    def lauf():
        freigabe.wait(5)
        fertig.set()

    check("K erster Start", pv.starte_startbestand(lauf=lauf) is True)
    check("K zweiter Start abgelehnt", pv.starte_startbestand(lauf=lauf) is False)
    freigabe.set()
    fertig.wait(5)
    for _ in range(50):
        if not pv.startbestand_laeuft():
            break
        threading.Event().wait(0.05)
    check("K nach Ende wieder startbar", not pv.startbestand_laeuft())

    # Gesamtlauf: nur Regulierungen mit ungeprueften Schritten, eine Mail am Ende.
    gesehen, mails = [], []

    async def fake_start(reg_key, ask=None, **kw):
        gesehen.append(reg_key)
        if reg_key == "CSRD":
            raise pv.VorschlagFehler("Antwort kaputt")
        return [1] if reg_key == "EUDR" else []

    alt_sv = pv.startbestand_vorschlaege
    pv.startbestand_vorschlaege = fake_start
    try:
        pv.startbestand_alle(versand=lambda e, b, t: mails.append(t) or "<id>")
    finally:
        pv.startbestand_vorschlaege = alt_sv
    mit_ungeprueft = {r for (r,) in db._conn().execute(
        "SELECT DISTINCT reg_key FROM pflicht_schritte WHERE aktiv = 1 AND geprueft_am IS NULL")}
    check("K nur Regulierungen mit ungeprueften Schritten", set(gesehen) == mit_ungeprueft,
          f"{sorted(gesehen)[:5]} …")
    check("K eine Mail am Ende", len(mails) == 1 and "EUDR: 1 Vorschlag" in mails[0],
          str(mails))
    check("K Fehler unter 'Nicht bearbeitet'", bool(mails) and "Nicht bearbeitet" in mails[0]
          and "CSRD" in mails[0] and "Antwort kaputt" in mails[0], str(mails))


def block_l() -> None:
    print("\n--- L  Typen aus der KI-Antwort ---")
    s = pdb.schritt(EUDR[2])
    alt_daten = s["texte"]["de"]["daten"]
    antwort = {"aenderungen": [
        {"art": "aendern", "schritt_id": EUDR[2],
         "nachher": {"daten": ["Geodaten", "Menge"]}, "beleg": "Art. 9"},
    ]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort)))
    check("L Liste in daten -> verbunden", len(ids) == 1 and
          pdb.vorschlag(ids[0])["nachher"]["texte"]["de"]["daten"] == "Geodaten; Menge",
          str(ids and pdb.vorschlag(ids[0])["nachher"]))
    check("L Liste in daten war Aenderung", alt_daten != "Geodaten; Menge")
    vorher = _offen()
    verworfen: list[str] = []
    antwort = {"aenderungen": [
        {"art": "aendern", "schritt_id": EUDR[2], "nachher": {"titel": {"de": "x"}},
         "beleg": "Art. 9"},
        {"art": "aendern", "schritt_id": True, "nachher": {"rolle": "gf"}, "beleg": "Art. 9"},
        {"art": "aendern", "schritt_id": 3.7, "nachher": {"rolle": "gf"}, "beleg": "Art. 9"},
        {"art": "aendern", "schritt_id": EUDR[2], "nachher": {"rolle": "gf"},
         "beleg": {"text": "Art. 9"}},
        {"art": "aendern", "schritt_id": EUDR[2], "nachher": {"rolle": "gf"},
         "beleg": "Art. 9", "begruendung": 42},
    ]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort),
                                           verworfen=verworfen))
    check("L dict-Titel, True/3.7-Id, dict-Beleg, Zahl-Begruendung verworfen",
          ids == [] and _offen() == vorher and len(verworfen) == 5, f"{ids} {verworfen}")
    antwort = {"aenderungen": [{"art": "aendern", "schritt_id": str(EUDR[2]),
                                "nachher": {"beschreibung": "Neu beschrieben"},
                                "beleg": ["Art. 9", "Abs. 2"]}]}
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", fake_ask(antwort)))
    check("L Ziffern-String als Id, Beleg-Liste verbunden", len(ids) == 1
          and pdb.vorschlag(ids[0])["beleg"] == "Art. 9; Abs. 2", str(ids))


def block_m() -> None:
    print("\n--- M  Startbestand: Beleg und Bestaetigung ---")
    schritte = [x for x in pdb.schritte_fuer(ZWEIT, "de") if not x["geprueft_am"]]
    check("M ungepruefte Schritte", len(schritte) >= 2, str(len(schritte)))
    a, b = schritte[0], schritte[1]
    andere = "finanzen" if a["rolle"] != "finanzen" else "gf"
    antwort = {"schritte": [
        {"schritt_id": a["id"], "rolle": andere, "frist_typ": a["frist_typ"],
         "frist_wert": a["frist_wert"], "daten": a["daten"], "beleg": ""},
        {"schritt_id": b["id"], "rolle": b["rolle"], "frist_typ": b["frist_typ"],
         "frist_wert": b["frist_wert"], "daten": b["daten"], "beleg": "",
         "begruendung": "Passt zum Gesetz"},
    ]}
    alt = pv.fetcher.fetch_law_text
    pv.fetcher.fetch_law_text = lambda reg, **kw: {"text": "§ 1 Anwendungsbereich"}

    def lauf() -> tuple[list[int], list[str], str]:
        verworfen: list[str] = []
        ids = run(pv.startbestand_vorschlaege(ZWEIT, fake_ask(antwort), verworfen=verworfen))
        letzte = [u for sy, u in PROMPTS if sy == pv.SYSTEM_STARTBESTAND][-1]
        return ids, verworfen, letzte

    marke = f'"schritt_id": {b["id"]},'
    try:
        ids, verworfen, _ = lauf()
        check("M Aenderung ohne Beleg verworfen", len(verworfen) == 1, str(verworfen))
        check("M Bestaetigung als Vorschlag", len(ids) == 1, str(ids))
        if len(ids) != 1:
            return
        v = pdb.vorschlag(ids[0])
        check("M Bestaetigung: aendern, leeres nachher, Schritt b, startbestand",
              v["art"] == "aendern" and v["nachher"] == {} and v["schritt_id"] == b["id"]
              and v["ausloeser"] == "startbestand", str(v["nachher"]))
        check("M Begruendung der KI", "Passt zum Gesetz" in (v["begruendung"] or ""))

        stamm = _client(STAMM_ID, STAMM)
        html = stamm.get(f"/admin/pflichten/vorschlag/{ids[0]}").get_data(as_text=True)
        check("M Seite zeigt Bestaetigung", "Bestätigung, keine Änderung" in html)
        html = stamm.get("/admin/pflichten/vorschlaege").get_data(as_text=True)
        check("M Liste zeigt Bestaetigung", "Bestätigung, keine Änderung" in html)

        ids2, _, prompt2 = lauf()
        check("M zweiter Lauf: offener Vorschlag uebersprungen",
              ids2 == [] and marke not in prompt2, str(ids2))

        # Freigabe: nur geprueft_am, keine Version, kein Hinweis, kein geaendert_am.
        pdb.setze_einstellung("pflichten_plan_aktiv", "1")
        with db._conn() as c:
            c.execute("INSERT OR IGNORE INTO nutzer_pflichten (user_id, reg_key,"
                      " erste_feststellung) VALUES (?, ?, '2026-11-01')", (KONTO_ID, ZWEIT))
        vorher = pdb.schritt(b["id"])
        n_versionen = _eins("SELECT COUNT(*) FROM pflicht_schritt_versionen WHERE schritt_id = ?",
                            (b["id"],))
        n_hinweise = _eins("SELECT COUNT(*) FROM pflicht_hinweise")
        ok = pdb.freigeben(ids[0], STAMM, None, HEUTE)
        nach = pdb.schritt(b["id"])
        check("M Freigabe ok", ok is True and pdb.vorschlag(ids[0])["status"] == "freigegeben")
        check("M geprueft_am = heute", nach["geprueft_am"] == "2026-11-19", str(nach["geprueft_am"]))
        check("M Version unveraendert", nach["version"] == vorher["version"])
        check("M kein Versionseintrag", _eins(
            "SELECT COUNT(*) FROM pflicht_schritt_versionen WHERE schritt_id = ?",
            (b["id"],)) == n_versionen)
        check("M geaendert_am unveraendert", nach["geaendert_am"] == vorher["geaendert_am"])
        check("M kein Hinweis", _eins("SELECT COUNT(*) FROM pflicht_hinweise") == n_hinweise)
        check("M Texte/Felder unveraendert", nach["texte"] == vorher["texte"]
              and nach["rolle"] == vorher["rolle"])
        pdb.setze_einstellung("pflichten_plan_aktiv", "0")

        ids3, _, prompt3 = lauf()
        check("M dritter Lauf: geprueft uebersprungen", ids3 == [] and marke not in prompt3,
              str(ids3))
    finally:
        pv.fetcher.fetch_law_text = alt


def block_n() -> None:
    print("\n--- N  Uebersetzung schlaegt fehl ---")

    async def ask(system, user):
        PROMPTS.append((system, user))
        if system == pv.SYSTEM_UEBERSETZUNG:
            return "kaputt"
        return json.dumps({"aenderungen": [{
            "art": "aendern", "schritt_id": EUDR[3],
            "nachher": {"titel": "Titel ohne Uebersetzung"},
            "beleg": "Art. 4", "begruendung": "B" * 3000}]})
    ids = run(pv.vorschlaege_aus_aenderung("EUDR", "a", "b", ask))
    check("N Vorschlag trotzdem angelegt", len(ids) == 1, str(ids))
    if ids:
        v = pdb.vorschlag(ids[0])
        t = v["nachher"]["texte"]
        check("N fremde Sprachen = deutscher Text", sorted(t) == sorted(pdb.SPRACHEN)
              and t["fr"]["titel"] == "Titel ohne Uebersetzung")
        check("N Warnhinweis ueberlebt Kuerzung",
              "Übersetzung fehlgeschlagen" in v["begruendung"]
              and len(v["begruendung"]) <= pv.BEGRUENDUNG_MAX + 300, str(len(v["begruendung"])))


def main() -> int:
    for block in (block_a, block_b, block_c, block_d, block_e, block_f, block_g, block_h,
                  block_i, block_j, block_k, block_l, block_m, block_n):
        try:
            block()
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            check(f"{block.__name__} ohne Ausnahme", False, f"{type(exc).__name__}: {exc}")
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER: {_failures}")
        return 1
    print("Alle Checks gruen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
