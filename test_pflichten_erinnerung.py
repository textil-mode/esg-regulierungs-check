"""Tests zum Pflichten-Plan, Aufgabe 7: taeglicher Lauf (pflichten_erinnerung.py).

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_erinnerung.py

Kein Netz, kein LLM, feste Tage. Eigene DB `data/esg_pflichten_erinnerung_test.db`.
Versand ueber eine Attrappe (`versand(empfaenger, betreff, text)`).

Bloecke:
  A  Schalter aus / Funktion aus: nichts, Zaehler 0
  B  Erster Lauf: 30- und 7-Tage-Erinnerung in einer Mail, Protokoll
  C  laufend/offen/erledigt/gesperrt/nicht freigeschaltet/abbestellt: keine Mail
  D  Zwei faellige Schritte + Hinweis: genau eine Mail, Hinweis gesendet
  E  MailError: nichts als gesendet markiert, Lauf laeuft weiter
  F  Zweiter Lauf am selben Tag und am Folgetag: keine Mail
  G  Datumsaenderung (EUDR 120 -> 40 Beschaeftigte): genau ein Hinweis 'datum'
  H  Monatserster: Uebersicht mit Block 'laufend', Sprache en, Lebenszeichen
  I  --probe: nichts gesendet, nichts markiert
  K  30 -> 7 Tage (zweite Mail), geaenderte Frist = neue Erinnerung, Fenstergrenzen
  L  Versand ok, Protokollieren scheitert: trotzdem als gesendet markiert
  J  Monatsuebersicht/Lebenszeichen: erster erfolgreicher Lauf des Monats
     (1. scheitert -> 2. sendet -> 3. nichts)
  M  Monatsuebersicht wiederholt keine Schritte aus "Fristen in den naechsten Tagen"

Vorbedingung: Die November-Uebersicht und das November-Lebenszeichen gelten
als schon verschickt (Marker gesetzt), damit die Bloecke B-G nur Erinnerungen
und Hinweise sehen.
"""
from __future__ import annotations

import io
import os
import sys
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_erinnerung_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
os.environ["PUBLIC_BASE_URL"] = "https://beispiel.test"
os.environ.pop("PFLICHTEN_PLAN", None)
for _k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[_k] = ""          # nie echter Versand, auch nicht aus einer .env
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import mailer  # noqa: E402
import pflichten_db as pdb  # noqa: E402
import pflichten_erinnerung as pe  # noqa: E402
from i18n import t  # noqa: E402

_failures: list[str] = []

HEUTE = date(2026, 11, 19)


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


class Versand:
    """Attrappe: merkt sich jede Mail; Adressen in `fehler` werfen MailError."""

    def __init__(self, fehler: set[str] | None = None):
        self.mails: list[tuple[str, str, str]] = []
        self.fehler = fehler or set()

    def __call__(self, empfaenger: str, betreff: str, text: str):
        if empfaenger in self.fehler:
            raise mailer.MailError("Testfehler")
        self.mails.append((empfaenger, betreff, text))
        return "<test@beispiel.test>"

    def an(self, email: str) -> list[tuple[str, str, str]]:
        return [m for m in self.mails if m[0] == email]


def _karten(**applies: str) -> list[dict]:
    return [{"key": k, "name": f"{k} – Testname", "applies": v} for k, v in applies.items()]


def _setze_frist(sid: int, typ: str, wert: str) -> None:
    with db._conn() as c:
        c.execute("UPDATE pflicht_schritte SET frist_typ = ?, frist_wert = ? WHERE id = ?",
                  (typ, wert, sid))


PROFIL = {"name": "Test GmbH", "employees": 120, "revenue_eur": 10_000_000,
          "materials": ["Leder"]}


def _konto(email: str, regs: dict, *, lang=None, approved=True, locked=0,
           erinnerungen=1, profil=None) -> int:
    uid = db.create_user(email, "Geheim-Passwort-123", approved=approved, lang=lang)
    with db._conn() as c:
        c.execute("UPDATE users SET locked = ?, erinnerungen = ? WHERE id = ?",
                  (locked, erinnerungen, uid))
    db.upsert_company(uid, profil or PROFIL)
    db.save_analysis(uid, _karten(**regs))
    return uid


def _erinnerungen(uid: int, mit_marker: bool = False) -> set[tuple[int, str, str]]:
    """Protokoll eines Kontos; ohne mit_marker nur echte Schritte (keine Monatsmarker)."""
    with db._conn() as c:
        return {(r["schritt_id"], r["art"], r["frist"]) for r in c.execute(
            "SELECT schritt_id, art, frist FROM pflicht_erinnerungen WHERE user_id = ?",
            (uid,)) if mit_marker or r["schritt_id"] != 0}


def _hinweise(uid: int, art: str | None = None) -> list[dict]:
    sql = "SELECT * FROM pflicht_hinweise WHERE user_id = ?"
    args: tuple = (uid,)
    if art:
        sql += " AND art = ?"
        args += (art,)
    with db._conn() as c:
        return [dict(r) for r in c.execute(sql + " ORDER BY id", args)]


db.init_db()

EUDR = pdb.schritte_fuer("EUDR", "de")
GPSR = pdb.schritte_fuer("GPSR", "de")
CSRD_DE = pdb.schritte_fuer("CSRD_DE", "de")
LKSG = pdb.schritte_fuer("LkSG", "de")
assert len(EUDR) >= 4 and GPSR and CSRD_DE and LKSG, "Startbestand fehlt"

_setze_frist(EUDR[0]["id"], "fest", "19.12.2026")   # 30 Tage nach HEUTE
_setze_frist(EUDR[1]["id"], "fest", "24.11.2026")   # 5 Tage nach HEUTE
_setze_frist(GPSR[0]["id"], "relativ", "+0d")       # GPSR gilt seit 2024 -> laufend
_setze_frist(CSRD_DE[0]["id"], "relativ", "-6m")    # Anwendungsbeginn offen
_setze_frist(LKSG[0]["id"], "fest", "19.12.2026")   # wird abgehakt

U1 = _konto("eins@beispiel.test", {"EUDR": "ja"})
U2 = _konto("zwei@beispiel.test", {"EUDR": "moeglich"})
ULO = _konto("lo@beispiel.test", {"GPSR": "ja", "CSRD_DE": "ja"}, lang="en")
UERL = _konto("erledigt@beispiel.test", {"LkSG": "ja"})
ULOCK = _konto("gesperrt@beispiel.test", {"EUDR": "ja"}, locked=1)
UNEU = _konto("neu@beispiel.test", {"EUDR": "ja"}, approved=False)
UAUS = _konto("aus@beispiel.test", {"EUDR": "ja"}, erinnerungen=0)
UDAT = _konto("datum@beispiel.test", {"EUDR": "ja"})
UFEHL = _konto("fehler@beispiel.test", {"EUDR": "ja"})
UEN = _konto("english@beispiel.test", {"EUDR": "ja"}, lang="en")
UMON = _konto("monat@beispiel.test", {"EUDR": "ja"})
# Pflicht entfaellt nach neuer Pruefung; ein Hinweis dazu darf nicht mehr gemailt werden.
UDROP = _konto("entfallen@beispiel.test", {"GPSR": "ja", "CSRD_DE": "ja"})
db.save_analysis(UDROP, _karten(GPSR="ja", CSRD_DE="nein"))
pdb.setze_erledigt(UERL, LKSG[0]["id"], "", True, HEUTE)

with db._conn() as c:
    c.execute(
        "INSERT INTO pflicht_hinweise (user_id, reg_key, art, text_de, erstellt_am)"
        " VALUES (?, 'EUDR', 'inhalt', 'intern', ?)", (U2, HEUTE.isoformat()))
    for _uid, _reg in ((UFEHL, "EUDR"), (UDROP, "CSRD_DE")):
        c.execute(
            "INSERT INTO pflicht_hinweise (user_id, reg_key, art, text_de, erstellt_am)"
            " VALUES (?, ?, 'inhalt', 'intern', ?)", (_uid, _reg, HEUTE.isoformat()))


def _november_erledigt(*uids: int) -> None:
    for _u in uids:
        pdb.merke_erinnerungen(_u, [(0, "monat", "2026-11")], "2026-11-01T06:30:00")


_november_erledigt(U1, U2, ULO, UERL, ULOCK, UNEU, UAUS, UDAT, UFEHL, UEN, UMON, UDROP)
pdb.setze_einstellung("lebenszeichen_monat", "2026-11")

ADMIN = sorted(pdb.STAMM_ADMINS)[0]
LEER = {"erinnerungen": 0, "uebersichten": 0, "hinweise": 0, "konten": 0}


def block_a() -> None:
    v = Versand()
    erg = pe.lauf(HEUTE, versand=v)        # Schalter steht auf Standard (aus)
    check("A Schalter aus: keine Mail", v.mails == [], str(v.mails)[:80])
    check("A Schalter aus: Zaehler 0", erg == LEER, str(erg))
    check("A Schalter aus: kein Protokoll", _erinnerungen(U1) == set())

    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    os.environ["PFLICHTEN_PLAN"] = "aus"
    try:
        v = Versand()
        erg = pe.lauf(HEUTE, versand=v)
        check("A PFLICHTEN_PLAN=aus: keine Mail, Zaehler 0", v.mails == [] and erg == LEER,
              str(erg))
    finally:
        os.environ.pop("PFLICHTEN_PLAN", None)


ERG_B: dict = {}
V_B = Versand({"fehler@beispiel.test"})


def block_b() -> None:
    ERG_B.update(pe.lauf(HEUTE, versand=V_B))
    mails = V_B.an("eins@beispiel.test")
    check("B Konto 1: genau eine Mail", len(mails) == 1, str(len(mails)))
    text = mails[0][2] if mails else ""
    check("B Mail nennt Schritt in 30 Tagen", EUDR[0]["titel"] in text)
    check("B Mail nennt Schritt in 5 Tagen", EUDR[1]["titel"] in text)
    check("B Mail enthaelt Link auf Meine Pflichten",
          "https://beispiel.test/esg/meine-pflichten" in text, text[-300:])
    check("B Mail enthaelt Abbestell-Hinweis mit Kontoseite",
          "https://beispiel.test/esg/passwort-aendern" in text)
    check("B Mail deutsch bei signup_lang NULL",
          mails and mails[0][1] == t("pflichten_mail_betreff", "de"), mails[0][1] if mails else "")
    check("B Protokoll Art 30 und 7",
          _erinnerungen(U1) == {(EUDR[0]["id"], "30", "2026-12-19"),
                                (EUDR[1]["id"], "7", "2026-11-24")}, str(_erinnerungen(U1)))
    en = V_B.an("english@beispiel.test")
    check("B Mail englisch bei signup_lang en",
          len(en) == 1 and en[0][1] == t("pflichten_mail_betreff", "en")
          and en[0][1] != t("pflichten_mail_betreff", "de"), en[0][1] if en else "")
    check("B kein Lebenszeichen (November schon erledigt)", V_B.an(ADMIN) == [])
    with db._conn() as c:
        n = c.execute("SELECT COUNT(*) FROM mail_log WHERE purpose = 'pflichten_erinnerung'"
                      " AND status = 'sent'").fetchone()[0]
    check("B mail_log mit purpose pflichten_erinnerung", n == len(V_B.mails), f"{n}")
    check("B Zaehler konten = versandte Mails", ERG_B["konten"] == len(V_B.mails), str(ERG_B))


def block_c() -> None:
    for email, label in (("lo@beispiel.test", "laufend/offen"),
                         ("erledigt@beispiel.test", "erledigt"),
                         ("gesperrt@beispiel.test", "locked=1"),
                         ("neu@beispiel.test", "approved=0"),
                         ("aus@beispiel.test", "erinnerungen=0")):
        check(f"C {label}: keine Mail", V_B.an(email) == [])
    check("C laufend/offen: kein Protokoll", _erinnerungen(ULO) == set())
    check("C erledigt: kein Protokoll", _erinnerungen(UERL) == set())
    check("C gesperrt: kein Protokoll", _erinnerungen(ULOCK) == set())


def block_d() -> None:
    mails = V_B.an("zwei@beispiel.test")
    check("D zwei Schritte + Hinweis: genau eine Mail", len(mails) == 1, str(len(mails)))
    text = mails[0][2] if mails else ""
    check("D Mail enthaelt beide Schritte",
          EUDR[0]["titel"] in text and EUDR[1]["titel"] in text)
    erwartet = t("pflichten_mail_hinweis_inhalt", "de").format(name="EUDR – Testname")
    check("D Mail enthaelt den Hinweis", erwartet in text, text[:400])
    check("D interner text_de nicht in der Mail", "intern" not in text)
    check("D Hinweis als gesendet markiert",
          all(h["gesendet_am"] for h in _hinweise(U2)), str(_hinweise(U2)))
    check("D Zaehler hinweise >= 1", ERG_B["hinweise"] >= 1, str(ERG_B))
    check("D Hinweis zu entfallener Pflicht: keine Mail", V_B.an("entfallen@beispiel.test") == [])
    check("D Hinweis zu entfallener Pflicht: still als gesendet markiert",
          all(h["gesendet_am"] for h in _hinweise(UDROP)), str(_hinweise(UDROP)))


def block_e() -> None:
    check("E MailError: keine Mail angekommen", V_B.an("fehler@beispiel.test") == [])
    check("E MailError: Erinnerung nicht als gesendet markiert", _erinnerungen(UFEHL) == set(),
          str(_erinnerungen(UFEHL)))
    check("E MailError: Lauf ging weiter (andere Konten bekamen Post)",
          len(V_B.an("eins@beispiel.test")) == 1 and len(V_B.an("datum@beispiel.test")) == 1)
    with db._conn() as c:
        n = c.execute("SELECT COUNT(*) FROM mail_log WHERE purpose = 'pflichten_erinnerung'"
                      " AND status = 'failed' AND recipient = 'fehler@beispiel.test'"
                      ).fetchone()[0]
    check("E MailError protokolliert als failed", n == 1, str(n))
    check("E MailError: Hinweis bleibt ungesendet",
          [h["gesendet_am"] for h in _hinweise(UFEHL)] == [None], str(_hinweise(UFEHL)))


def block_f() -> None:
    v = Versand()
    pe.lauf(HEUTE, versand=v)
    check("F gleicher Tag erneut: keine Mail an Konto 1", v.an("eins@beispiel.test") == [])
    check("F gleicher Tag erneut: keine Mail an Konto 2", v.an("zwei@beispiel.test") == [])
    check("F gleicher Tag erneut: Fehlerkonto versucht es wieder (und nur das)",
          len(v.an("fehler@beispiel.test")) == 1 and len(v.mails) == 1, str(v.mails)[:120])
    check("F nach Erfolg: Fehlerkonto jetzt protokolliert",
          {(EUDR[0]["id"], "30", "2026-12-19"), (EUDR[1]["id"], "7", "2026-11-24")}
          <= _erinnerungen(UFEHL), str(_erinnerungen(UFEHL)))
    check("F nach Erfolg: Hinweis des Fehlerkontos gesendet",
          all(h["gesendet_am"] for h in _hinweise(UFEHL)), str(_hinweise(UFEHL)))
    v = Versand()
    pe.lauf(date(2026, 11, 20), versand=v)
    check("F Folgetag: keine weitere Mail an Konto 1", v.an("eins@beispiel.test") == [])


def block_g() -> None:
    check("G erster Lauf ohne Vorwert: kein Hinweis 'datum'", _hinweise(UDAT, "datum") == [])
    with db._conn() as c:
        alt = c.execute("SELECT letzter_gilt_ab FROM nutzer_pflichten WHERE user_id = ?"
                        " AND reg_key = 'EUDR'", (UDAT,)).fetchone()[0]
    check("G letzter_gilt_ab gespeichert", alt == "30.12.2026", str(alt))
    db.upsert_company(UDAT, {**PROFIL, "employees": 40})
    v = Versand()
    pe.lauf(HEUTE, versand=v)
    hinweise = _hinweise(UDAT, "datum")
    check("G geaendertes Profil: genau ein Hinweis 'datum'", len(hinweise) == 1, str(hinweise))
    mails = v.an("datum@beispiel.test")
    check("G Hinweis in genau einer Mail", len(mails) == 1, str(len(mails)))
    erwartet = t("pflichten_mail_hinweis_datum", "de").format(
        name="EUDR – Testname", datum="30.06.2027")
    check("G Mail nennt neuen Anwendungsbeginn", mails and erwartet in mails[0][2],
          mails[0][2][:400] if mails else "")
    check("G Hinweis gesendet", all(h["gesendet_am"] for h in hinweise))
    v = Versand()
    pe.lauf(HEUTE, versand=v)
    check("G dritter Lauf: kein weiterer Hinweis", len(_hinweise(UDAT, "datum")) == 1)
    check("G dritter Lauf: keine Mail", v.an("datum@beispiel.test") == [])


def block_h() -> None:
    with db._conn() as c:
        gesendet = c.execute("SELECT COUNT(*) FROM mail_log WHERE purpose ="
                             " 'pflichten_erinnerung' AND status = 'sent'").fetchone()[0]
    v = Versand()
    erg = pe.lauf(date(2026, 12, 1), versand=v)
    mails = v.an("lo@beispiel.test")
    check("H Monatserster: Uebersicht an laufend/offen-Konto", len(mails) == 1, str(len(mails)))
    text = mails[0][2] if mails else ""
    gpsr_en = pdb.schritte_fuer("GPSR", "en")[0]["titel"]
    kopf = t("pflichten_mail_laufend", "en")
    check("H Block 'laufend' mit GPSR-Schritt",
          kopf in text and gpsr_en in text.split(kopf, 1)[-1], text[:500])
    check("H Uebersicht englisch", mails and mails[0][1] == t("pflichten_mail_betreff", "en"))
    check("H laufend/offen: keine Schritt-Erinnerung, nur Monatsmarker",
          _erinnerungen(ULO, True) == {(0, "monat", "2026-11"), (0, "monat", "2026-12")},
          str(_erinnerungen(ULO, True)))
    check("H Zaehler uebersichten >= 1", erg["uebersichten"] >= 1, str(erg))
    leb = v.an(ADMIN)
    check("H Lebenszeichen an Admin", len(leb) == 1, str(len(leb)))
    satz = f"In den letzten 30 Tagen gingen {gesendet} Erinnerungsmails an Mitglieder."
    check("H Lebenszeichen nennt Zahl der letzten 30 Tage (exakter Satz)",
          bool(leb) and satz in leb[0][2], (leb[0][2][:300] if leb else "") + f" / {satz}")
    with db._conn() as c:
        zwecke = {r[0] for r in c.execute(
            "SELECT purpose FROM mail_log WHERE recipient = ?", (ADMIN,))}
    check("H Lebenszeichen zaehlt nicht als Erinnerung",
          zwecke == {"pflichten_lebenszeichen"}, str(zwecke))
    v2 = Versand()
    pe.lauf(date(2026, 12, 1), versand=v2)
    check("H zweiter Lauf am Monatsersten: kein zweites Lebenszeichen", v2.an(ADMIN) == [])
    check("H zweiter Lauf am Monatsersten: keine zweite Uebersicht",
          v2.an("lo@beispiel.test") == [])


def block_i() -> None:
    uid = _konto("probe@beispiel.test", {"EUDR": "ja"})
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        rc = pe.main(["--heute", "2026-11-19", "--probe"])
    aus = puffer.getvalue()
    check("I --probe: Rueckgabe 0", rc == 0, str(rc))
    check("I --probe: zeigt die Mail", "probe@beispiel.test" in aus and EUDR[0]["titel"] in aus,
          aus[:300])
    check("I --probe: nichts markiert", _erinnerungen(uid) == set())
    with db._conn() as c:
        n = c.execute("SELECT COUNT(*) FROM mail_log WHERE recipient = 'probe@beispiel.test'"
                      ).fetchone()[0]
        alt = c.execute("SELECT letzter_gilt_ab FROM nutzer_pflichten WHERE user_id = ?",
                        (uid,)).fetchone()[0]
    check("I --probe: kein mail_log", n == 0, str(n))
    check("I --probe: letzter_gilt_ab nicht gespeichert", alt is None, str(alt))


def block_k() -> None:
    v = Versand()
    pe.lauf(date(2026, 12, 12), versand=v)
    mails = v.an("eins@beispiel.test")
    check("K 30 -> 7 Tage: zweite Mail fuer denselben Schritt",
          len(mails) == 1 and EUDR[0]["titel"] in mails[0][2], str(len(mails)))
    check("K Protokoll Art 7 fuer 19.12.",
          (EUDR[0]["id"], "7", "2026-12-19") in _erinnerungen(U1), str(_erinnerungen(U1)))
    v = Versand()
    pe.lauf(date(2026, 12, 12), versand=v)
    check("K gleicher Tag: keine weitere Mail", v.an("eins@beispiel.test") == [])

    _setze_frist(EUDR[0]["id"], "fest", "22.12.2026")
    v = Versand()
    pe.lauf(date(2026, 12, 12), versand=v)
    check("K geaenderte Frist: neue Erinnerung (Art 30, 22.12.)",
          len(v.an("eins@beispiel.test")) == 1
          and (EUDR[0]["id"], "30", "2026-12-22") in _erinnerungen(U1), str(_erinnerungen(U1)))

    tag = date(2027, 3, 10)
    schritte = []
    for i, tage in enumerate((-1, 0, 7, 8, 30, 31)):
        d = date.fromordinal(tag.toordinal() + tage)
        schritte.append({"id": 9000 + i, "titel": f"T{tage}", "erledigt": False,
                         "ueberfaellig": tage < 0,
                         "frist": {"art": "datum", "datum": d, "periode": ""}})
    schritte.append({"id": 9100, "titel": "keine", "erledigt": False, "ueberfaellig": False,
                     "frist": {"art": "keine", "datum": None, "periode": ""}})
    plan = {"pflichten": [{"reg_key": "X", "name": "X", "entfaellt": False,
                           "schritte": schritte}]}
    arten = {e["schritt"]["titel"]: e["art"] for e in pe._faellige(U1, plan, tag)}
    check("K Fenstergrenzen -1/0/7/8/30/31 und 'keine'",
          arten == {"T0": "7", "T7": "7", "T8": "30", "T30": "30"}, str(arten))


def block_l() -> None:
    uid = _konto("logfehler@beispiel.test", {"EUDR": "ja"})
    original = db.log_mail

    def kaputt(recipient, purpose, status, **kw):
        if status == "sent":
            raise RuntimeError("Protokoll kaputt")
        return original(recipient, purpose, status, **kw)

    v = Versand()
    db.log_mail = kaputt
    try:
        pe.lauf(date(2026, 12, 12), versand=v)
    finally:
        db.log_mail = original
    check("L Versand ok, Protokoll scheitert: Mail ging raus",
          len(v.an("logfehler@beispiel.test")) == 1)
    check("L ... und Erinnerung gilt als gesendet",
          (EUDR[0]["id"], "30", "2026-12-22") in _erinnerungen(uid), str(_erinnerungen(uid)))
    with db._conn() as c:
        n = c.execute("SELECT COUNT(*) FROM mail_log WHERE recipient = 'logfehler@beispiel.test'"
                      " AND status = 'failed'").fetchone()[0]
    check("L ... und nicht als failed protokolliert", n == 0, str(n))


def block_j() -> None:
    v = Versand({"monat@beispiel.test", ADMIN})
    pe.lauf(date(2027, 1, 1), versand=v)
    check("J 1.: Uebersicht scheitert -> kein Marker",
          (0, "monat", "2027-01") not in _erinnerungen(UMON, True), str(_erinnerungen(UMON, True)))
    check("J 1.: Lebenszeichen scheitert -> kein Marker",
          pdb.einstellung("lebenszeichen_monat") != "2027-01")
    check("J 1.: andere Konten bekamen ihre Uebersicht trotzdem",
          len(v.an("lo@beispiel.test")) == 1)
    v = Versand()
    pe.lauf(date(2027, 1, 2), versand=v)
    mails = v.an("monat@beispiel.test")
    check("J 2.: Uebersicht nachgeholt", len(mails) == 1
          and t("pflichten_mail_uebersicht", "de") in mails[0][2], str(len(mails)))
    check("J 2.: Lebenszeichen nachgeholt", len(v.an(ADMIN)) == 1)
    check("J 2.: Konten mit Januar-Uebersicht bekommen keine zweite",
          v.an("lo@beispiel.test") == [])
    v = Versand()
    pe.lauf(date(2027, 1, 3), versand=v)
    check("J 3.: keine Uebersicht mehr", v.an("monat@beispiel.test") == [])
    check("J 3.: kein Lebenszeichen mehr", v.an(ADMIN) == [])


def block_m() -> None:
    tag = date(2027, 3, 1)

    def schritt(sid: int, titel: str, tage: int) -> dict:
        d = date.fromordinal(tag.toordinal() + tage)
        return {"id": sid, "titel": titel, "erledigt": False, "ueberfaellig": False,
                "frist": {"art": "datum", "datum": d, "periode": ""}}

    x = schritt(9200, "Bald-in-5-Tagen", 5)
    y = schritt(9201, "Spaeter-in-60-Tagen", 60)
    p = {"reg_key": "X", "name": "Xreg", "entfaellt": False, "schritte": [x, y]}
    faellig = [{"pflicht": p, "schritt": x, "art": "7", "tage": 5}]
    _, text = pe.mailtext("de", faellig, [], {"bald": [(p, x), (p, y)], "ueberfaellig": [],
                                               "laufend": []})
    kopf = t("pflichten_mail_90", "de")
    check("M Schritt aus 'naechste Tage' nur einmal in der Mail",
          text.count("Bald-in-5-Tagen") == 1, text)
    check("M 90-Tage-Block zeigt die uebrigen", "Spaeter-in-60-Tagen" in text.split(kopf, 1)[-1])
    _, text = pe.mailtext("de", faellig, [], {"bald": [(p, x)], "ueberfaellig": [],
                                               "laufend": []})
    check("M nur doppelte: kein leerer 90-Tage-Block, keine leere Uebersicht",
          kopf not in text and t("pflichten_mail_uebersicht", "de") not in text, text)


def main() -> int:
    for blk in (block_a, block_b, block_c, block_d, block_e, block_f, block_g, block_h,
                block_i, block_k, block_l, block_j, block_m):
        try:
            blk()
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            check(f"{blk.__name__} ohne Ausnahme", False, repr(exc))
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER: {_failures}")
        return 1
    print("Alle Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
