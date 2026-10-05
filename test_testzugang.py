"""Testzugang: 48 Stunden ab Freischaltung (05.10.2026).

  1  Migration: Bestandskonten sind dauerhafte Benutzer
  2  Freischalten verlangt eine Kontoart - ohne Auswahl passiert nichts
  3  Freischaltung als Benutzer: dauerhaft, bisheriger Mailtext
  4  Freischaltung als Testzugang: Frist gesetzt, eigener Mailtext mit Ablauf
  5  Vor Ablauf nutzbar, nach Ablauf gesperrt - mit Nachricht, und nur einer
  6  Gesperrt heisst gesperrt: keine Anmeldung, keine laufende Sitzung,
     und die Anfragenliste zeigt das Konto nicht als offene Anfrage
  7  Admin wechselt die Kontoart in beide Richtungen; Wechsel auf Benutzer
     hebt die Sperre auf, Wechsel auf Testzugang startet neue 48 Stunden
  8  Wer nicht darf, kommt nicht durch; das eigene Konto bleibt aussen vor
  9  Die Oberflaeche: Pflichtauswahl, Spalte "Zugang", Frist bzw. "abgelaufen"

Eigene DB data/esg_testzugang_test.db, Attrappe statt Mailversand, kein Netz.
Aufruf:  ./.venv/Scripts/python.exe test_testzugang.py
"""
from __future__ import annotations

import os
import sqlite3
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_testzugang_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for _var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
             "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_var] = ""
BASIS = "https://test.example"
os.environ["PUBLIC_BASE_URL"] = BASIS

import db  # noqa: E402

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH}!"
db.init_db()

import mailer  # noqa: E402
import regulations  # noqa: E402
import i18n  # noqa: E402
import testzugang  # noqa: E402
import app as flaskapp  # noqa: E402

fehler: list[str] = []
versandt: list[dict] = []
BASIS_THREADS = threading.active_count()


def _attrappe(recipient: str, subject: str, text: str) -> str:
    versandt.append({"to": recipient, "subject": subject, "text": text})
    return "msg_%03d" % len(versandt)


mailer.send = _attrappe
mailer.is_configured = lambda: True

ADMIN = sorted(flaskapp.ADMIN_EMAILS)[0]
PW = "ein-gutes-Passwort-2026"
VERBAND = regulations.MEMBER_ASSOCIATIONS[0]


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def ruhe() -> None:
    """Zweimal ruhig mit Abstand — Threads starten hier eigene Threads."""
    ende = time.perf_counter() + 8
    ruhig = 0
    while ruhig < 2 and time.perf_counter() < ende:
        if threading.active_count() > BASIS_THREADS:
            ruhig = 0
            time.sleep(0.005)
        else:
            ruhig += 1
            time.sleep(0.08)


def client_als(email: str | None):
    c = flaskapp.app.test_client()
    if email:
        with c.session_transaction() as sess:
            sess["user_id"] = db.get_user_by_email(email)["id"]
            sess["user_email"] = email
            sess["ui_language"] = "de"
    return c


def post(c, path: str, data: dict | None = None, origin: str | None = BASIS):
    headers = {"Origin": origin} if origin else {}
    return c.post(path, data=data or {}, headers=headers,
                  environ_base={"REMOTE_ADDR": "203.0.113.9"})


def zustand(uid: int) -> dict:
    with sqlite3.connect(TEST_DB) as c:
        c.row_factory = sqlite3.Row
        r = c.execute("SELECT account_type, test_expires_at, locked, approved"
                      "  FROM users WHERE id = ?", (uid,)).fetchone()
    return dict(r) if r else {}


def anfrage_anlegen(email: str, lang: str = "de") -> int:
    return db.create_user(email, None, approved=False, lang=lang,
                          association=VERBAND)


def frist_setzen(uid: int, stunden: float) -> None:
    """Verschiebt die Frist, um Ablauf zu pruefen, ohne 48 Stunden zu warten."""
    ziel = (datetime.utcnow() + timedelta(hours=stunden)).isoformat()
    with sqlite3.connect(TEST_DB) as c:
        c.execute("UPDATE users SET test_expires_at = ? WHERE id = ?", (ziel, uid))


admin_id = db.create_user(ADMIN, PW)

# ---------------------------------------------------------------------------
print("\n1. Migration: Bestandskonten sind dauerhafte Benutzer")
# ---------------------------------------------------------------------------
alt_id = db.create_user("bestand@example.org", PW)
z = zustand(alt_id)
pruefe(z["account_type"] == db.ACCOUNT_TYPE_USER, "Kontoart ist 'benutzer'")
pruefe(z["test_expires_at"] is None, "keine Frist")
pruefe(z["locked"] == 0, "nicht gesperrt")
pruefe(db.TEST_ACCESS_HOURS == 48, f"Testzeit {db.TEST_ACCESS_HOURS} Stunden")

# ---------------------------------------------------------------------------
print("\n2. Freischalten verlangt eine Kontoart")
# ---------------------------------------------------------------------------
ohne_wahl = anfrage_anlegen("ohne-wahl@example.org")
versandt.clear()
r = post(client_als(ADMIN), f"/admin/anfragen/{ohne_wahl}/freischalten")
ruhe()
pruefe(not db.is_approved(ohne_wahl), "ohne Auswahl wird nicht freigeschaltet")
pruefe(not versandt, "und es geht keine Mail raus")
r = post(client_als(ADMIN), f"/admin/anfragen/{ohne_wahl}/freischalten",
         {"kontotyp": "irgendwas"})
ruhe()
pruefe(not db.is_approved(ohne_wahl), "ein erfundener Wert wird abgewiesen")
try:
    db.approve_user(ohne_wahl, "unsinn")
    pruefe(False, "db.approve_user lehnt eine unbekannte Kontoart ab")
except ValueError:
    pruefe(True, "db.approve_user lehnt eine unbekannte Kontoart ab")

# ---------------------------------------------------------------------------
print("\n3. Freischaltung als Benutzer")
# ---------------------------------------------------------------------------
dauer_id = anfrage_anlegen("dauerhaft@example.org")
versandt.clear()
post(client_als(ADMIN), f"/admin/anfragen/{dauer_id}/freischalten",
     {"kontotyp": db.ACCOUNT_TYPE_USER})
ruhe()
z = zustand(dauer_id)
pruefe(z["approved"] == 1 and z["account_type"] == db.ACCOUNT_TYPE_USER,
       "freigeschaltet als dauerhafter Benutzer")
pruefe(z["test_expires_at"] is None, "ohne Frist")
pruefe(len(versandt) == 1, f"eine Mail ({len(versandt)})")
if versandt:
    pruefe(versandt[0]["subject"] == i18n.t("mail_signup_subject", "de"),
           "mit dem bisherigen Betreff")

# ---------------------------------------------------------------------------
print("\n4. Freischaltung als Testzugang")
# ---------------------------------------------------------------------------
test_id = anfrage_anlegen("probe@example.org")
versandt.clear()
post(client_als(ADMIN), f"/admin/anfragen/{test_id}/freischalten",
     {"kontotyp": db.ACCOUNT_TYPE_TEST})
ruhe()
z = zustand(test_id)
pruefe(z["approved"] == 1 and z["account_type"] == db.ACCOUNT_TYPE_TEST,
       "freigeschaltet als Testzugang")
# Die Uhr laeuft erst mit der ersten Anmeldung. Setzte die Freischaltung schon
# eine Frist, waere die Testzeit verstrichen, bevor die Person ihr Passwort
# ueberhaupt gesetzt hat - der Code gilt 7 Tage, die Testzeit 48 Stunden.
pruefe(z["test_expires_at"] is None,
       "noch ohne Frist - die Uhr startet bei der ersten Anmeldung")
pruefe(z["locked"] == 0, "und nicht gesperrt")
pruefe(testzugang.sperren_und_melden() == [],
       "ein nicht eingeloester Testzugang laeuft nicht von selbst ab")

pruefe(len(versandt) == 1, f"eine Mail ({len(versandt)})")
if versandt:
    pruefe(versandt[0]["subject"] == i18n.t("mail_signup_test_subject", "de"),
           "mit dem eigenen Betreff fuer Testzugaenge")
    pruefe(versandt[0]["subject"] != i18n.t("mail_signup_subject", "de"),
           "also einem anderen als beim dauerhaften Zugang")
    text = versandt[0]["text"]
    pruefe("48" in text, "der Text nennt die 48 Stunden")
    pruefe("anmelden" in text.lower(), "und sagt, dass die Zeit mit der Anmeldung beginnt")
    pruefe(BASIS in text, "samt Link zum Setzen des Passworts")

# Testzugang in einer anderen Sprache
fr_id = anfrage_anlegen("essai@example.org", lang="fr")
versandt.clear()
post(client_als(ADMIN), f"/admin/anfragen/{fr_id}/freischalten",
     {"kontotyp": db.ACCOUNT_TYPE_TEST})
ruhe()
pruefe(bool(versandt) and versandt[0]["subject"] == i18n.t("mail_signup_test_subject", "fr"),
       "die Mail kommt in der Sprache der Registrierung (FR)")

# ---------------------------------------------------------------------------
print("\n5. Die erste Anmeldung startet die Uhr, der Ablauf sperrt")
# ---------------------------------------------------------------------------
db.set_password(test_id, PW)
pruefe(zustand(test_id)["test_expires_at"] is None,
       "Passwort setzen allein startet die Uhr nicht")

vorher = datetime.utcnow()
r = post(flaskapp.app.test_client(), "/login",
         {"action": "login", "email": "probe@example.org", "password": PW})
pruefe(r.status_code in (302, 303), f"die erste Anmeldung gelingt ({r.status_code})")
frist_iso = zustand(test_id)["test_expires_at"]
pruefe(bool(frist_iso), "und setzt die Frist")
if frist_iso:
    stunden = (datetime.fromisoformat(frist_iso) - vorher).total_seconds() / 3600
    pruefe(47.9 < stunden < 48.2, f"auf 48 Stunden ab jetzt ({stunden:.2f} h)")

# Jede weitere Anmeldung darf die Frist NICHT verschieben, sonst liesse sich
# die Testzeit durch Aus- und Einloggen beliebig verlaengern.
post(flaskapp.app.test_client(), "/login",
     {"action": "login", "email": "probe@example.org", "password": PW})
pruefe(zustand(test_id)["test_expires_at"] == frist_iso,
       "eine zweite Anmeldung verschiebt die Frist nicht")
pruefe(db.start_test_clock(test_id) is None,
       "start_test_clock wirkt genau einmal")

seite = client_als("probe@example.org").get("/dashboard")
pruefe(seite.status_code == 200, "vor Ablauf laedt das Dashboard")

frist_setzen(test_id, -0.1)        # Frist liegt 6 Minuten in der Vergangenheit
versandt.clear()
betroffen = testzugang.sperren_und_melden()
pruefe(len(betroffen) == 1 and betroffen[0]["email"] == "probe@example.org",
       f"genau ein Konto gesperrt ({len(betroffen)})")
pruefe(zustand(test_id)["locked"] == 1, "es ist gesperrt")
pruefe(zustand(test_id)["approved"] == 1,
       "aber weiterhin freigeschaltet - also keine offene Anfrage")
with sqlite3.connect(TEST_DB) as c:
    da = c.execute("SELECT 1 FROM users WHERE id = ?", (test_id,)).fetchone()
pruefe(da is not None, "und nicht geloescht (Nutzervorgabe)")
pruefe(len(versandt) == 1, f"eine Nachricht an die Person ({len(versandt)})")
if versandt:
    pruefe(versandt[0]["to"] == "probe@example.org", "an die richtige Adresse")
    pruefe(versandt[0]["subject"] == i18n.t("mail_test_expired_subject", "de"),
           "mit dem Betreff zum Ablauf")
    pruefe("gesperrt" in versandt[0]["text"] and "gelöscht" in versandt[0]["text"],
           "der Text sagt: gesperrt, nicht geloescht")

versandt.clear()
pruefe(testzugang.sperren_und_melden() == [], "ein zweiter Lauf findet nichts mehr")
pruefe(not versandt, "und schickt keine zweite Nachricht")

# ---------------------------------------------------------------------------
print("\n6. Gesperrt heisst gesperrt")
# ---------------------------------------------------------------------------
r = post(flaskapp.app.test_client(), "/login",
         {"action": "login", "email": "probe@example.org", "password": PW})
pruefe(r.status_code == 403, f"Anmeldung mit richtigem Passwort: 403 ({r.status_code})")
pruefe(i18n.t("err_account_test_over", "de")[:40] in r.get_data(as_text=True),
       "mit dem Hinweis auf den abgelaufenen Testzeitraum")

# Eine laufende Sitzung muss ebenfalls enden — sonst arbeitet der Zugang
# weiter, solange das Cookie lebt (bis zu 12 Stunden).
laufend = client_als("probe@example.org")
r = laufend.get("/dashboard")
pruefe(r.status_code in (302, 303), "eine laufende Sitzung wird beendet")
r = laufend.get("/dashboard")
pruefe(r.status_code in (302, 303), "und bleibt beendet")

seite = client_als(ADMIN).get("/admin/konten").get_data(as_text=True)
anfragen = seite.split('id="anfragen"')[1].split("</table>")[0] \
    if 'id="anfragen"' in seite else ""
pruefe("probe@example.org" not in anfragen,
       "das gesperrte Konto steht nicht unter den offenen Anfragen")

# ---------------------------------------------------------------------------
print("\n7. Admin wechselt die Kontoart")
# ---------------------------------------------------------------------------
r = post(client_als(ADMIN), f"/admin/konten/{test_id}/zugang",
         {"kontotyp": db.ACCOUNT_TYPE_USER})
z = zustand(test_id)
pruefe(z["account_type"] == db.ACCOUNT_TYPE_USER, "Wechsel auf Benutzer wirkt")
pruefe(z["locked"] == 0, "und hebt die Sperre auf")
pruefe(z["test_expires_at"] is None, "die Frist ist weg")
pruefe(db.verify_user("probe@example.org", PW) == test_id, "Anmelden geht wieder")
r = client_als("probe@example.org").get("/dashboard")
pruefe(r.status_code == 200, "das Dashboard laedt wieder")

post(client_als(ADMIN), f"/admin/konten/{dauer_id}/zugang",
     {"kontotyp": db.ACCOUNT_TYPE_TEST})
z = zustand(dauer_id)
pruefe(z["account_type"] == db.ACCOUNT_TYPE_TEST, "Wechsel auf Testzugang wirkt")
pruefe(z["test_expires_at"] is None,
       "die Uhr steht auf null - sie startet mit der naechsten Anmeldung")

# Ein zweiter Klick auf einem laufenden Testkonto setzt die Testzeit neu an:
# die Frist faellt weg, die naechste Anmeldung startet 48 frische Stunden.
frist_setzen(dauer_id, 1)
pruefe(zustand(dauer_id)["test_expires_at"] is not None, "Ausgangslage: Frist laeuft")
post(client_als(ADMIN), f"/admin/konten/{dauer_id}/zugang",
     {"kontotyp": db.ACCOUNT_TYPE_TEST})
pruefe(zustand(dauer_id)["test_expires_at"] is None,
       "ein zweiter Klick setzt die Testzeit neu an (Uhr wieder auf null)")

# Und die Uhr laeuft dann wirklich bei der naechsten Anmeldung los.
db.set_password(dauer_id, PW)
vorher = datetime.utcnow()
post(flaskapp.app.test_client(), "/login",
     {"action": "login", "email": "dauerhaft@example.org", "password": PW})
neue_frist = zustand(dauer_id)["test_expires_at"]
pruefe(bool(neue_frist), "die naechste Anmeldung startet sie")
if neue_frist:
    stunden = (datetime.fromisoformat(neue_frist) - vorher).total_seconds() / 3600
    pruefe(47.9 < stunden < 48.2, f"mit frischen 48 Stunden ({stunden:.2f} h)")

r = post(client_als(ADMIN), f"/admin/konten/{dauer_id}/zugang", {"kontotyp": ""})
pruefe(zustand(dauer_id)["account_type"] == db.ACCOUNT_TYPE_TEST,
       "ohne Kontoart aendert sich nichts")
pruefe(db.set_account_type(999999, db.ACCOUNT_TYPE_USER) is None,
       "eine unbekannte Kennung liefert None")

# ---------------------------------------------------------------------------
print("\n8. Wer nicht darf, kommt nicht durch")
# ---------------------------------------------------------------------------
r = post(client_als("bestand@example.org"), f"/admin/konten/{test_id}/zugang",
         {"kontotyp": db.ACCOUNT_TYPE_TEST})
pruefe(zustand(test_id)["account_type"] == db.ACCOUNT_TYPE_USER,
       "ein normales Mitglied wechselt nichts")
r = post(flaskapp.app.test_client(), f"/admin/konten/{test_id}/zugang",
         {"kontotyp": db.ACCOUNT_TYPE_TEST})
pruefe(zustand(test_id)["account_type"] == db.ACCOUNT_TYPE_USER,
       "ohne Anmeldung auch nicht")
r = post(client_als(ADMIN), f"/admin/konten/{test_id}/zugang",
         {"kontotyp": db.ACCOUNT_TYPE_TEST}, origin="https://angreifer.example")
pruefe(r.status_code == 403 and zustand(test_id)["account_type"] == db.ACCOUNT_TYPE_USER,
       "fremde Herkunft (CSRF) wird abgewiesen")

# Das eigene Konto bleibt aussen vor: wer sich selbst einen Testzugang gibt,
# sperrt sich in 48 Stunden aus.
post(client_als(ADMIN), f"/admin/konten/{admin_id}/zugang",
     {"kontotyp": db.ACCOUNT_TYPE_TEST})
pruefe(zustand(admin_id)["account_type"] == db.ACCOUNT_TYPE_USER,
       "der Admin gibt sich selbst keinen Testzugang")

# ---------------------------------------------------------------------------
print("\n9. Die Oberflaeche")
# ---------------------------------------------------------------------------
offen = anfrage_anlegen("neue-anfrage@example.org")
seite = client_als(ADMIN).get("/admin/konten").get_data(as_text=True)
anfragen = seite.split('id="anfragen"')[1].split("</table>")[0]
pruefe('name="kontotyp"' in anfragen and "required" in anfragen,
       "die Anfrage hat ein Pflicht-Auswahlfeld")
pruefe(i18n.t("account_type_choose", "de") in anfragen,
       "mit leerer Vorauswahl (der Admin muss waehlen)")
pruefe(i18n.t("account_type_test", "de") in anfragen, "Testzugang ist waehlbar")
pruefe(i18n.t("account_type_user", "de") in anfragen, "Benutzer ebenso")

tabelle = seite.split('id="konten"')[1]
pruefe(i18n.t("account_type_col", "de") in tabelle, "die Kontenliste hat die Spalte 'Zugang'")
pruefe(f"/admin/konten/{test_id}/zugang" in tabelle, "mit Umschalt-Knopf je Konto")
pruefe(f"/admin/konten/{admin_id}/zugang" not in tabelle,
       "fuer das eigene Konto ohne Knopf")

frist_setzen(dauer_id, 5)
tabelle = client_als(ADMIN).get("/admin/konten").get_data(as_text=True).split('id="konten"')[1]
pruefe(i18n.t("account_type_test", "de") in tabelle, "ein laufender Testzugang ist erkennbar")
frist = zustand(dauer_id)["test_expires_at"]
pruefe(frist[8:10] + "." + frist[5:7] in tabelle, "die Frist steht dabei")

frist_setzen(dauer_id, -1)
versandt.clear()
tabelle = client_als(ADMIN).get("/admin/konten").get_data(as_text=True).split('id="konten"')[1]
ruhe()
pruefe(i18n.t("account_test_locked", "de") in tabelle,
       "ein abgelaufener zeigt 'Testzeit abgelaufen' …")
pruefe(zustand(dauer_id)["locked"] == 1,
       "… weil der Aufruf der Liste faellige Zugaenge mitsperrt")
pruefe(len(versandt) == 1, f"und dabei genau eine Nachricht verschickt ({len(versandt)})")

# ---------------------------------------------------------------------------
ruhe()
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
