"""Tests zur Freischaltung neuer Registrierungen (seit 29.09.2026).

Ausfuehren:  ./.venv/Scripts/python.exe test_freischaltung.py

Eigene DB `data/esg_freischaltung_test.db`, kein Netz, keine echte Mail
(`mailer.send` ist eine Attrappe).

Bloecke:
  1  Bestandskonten bleiben nutzbar (Migration mit Default "freigeschaltet")
  2  Registrierung legt eine gesperrte Anfrage an; Anmeldung wird abgewiesen
  3  Admin-Seite: Anfrage sichtbar, nur fuer Admins, nicht in der Kontenliste
  4  Freischalten: Konto nutzbar, Mail mit Anmeldelink in der Sprache der Anfrage
  5  Ablehnen: Anfrage samt Daten weg, keine Mail; aktive Konten sind geschuetzt
"""
from __future__ import annotations

import os
import sqlite3
import sys
import threading
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_freischaltung_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for _var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_var] = ""
BASIS = "https://test.example"
os.environ["PUBLIC_BASE_URL"] = BASIS

import db  # noqa: E402

assert db.DB_PATH == TEST_DB
db.init_db()

import mailer  # noqa: E402
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


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def ruhe() -> None:
    ende = time.perf_counter() + 5
    while threading.active_count() > BASIS_THREADS and time.perf_counter() < ende:
        time.sleep(0.005)
    time.sleep(0.05)


def client_als(email: str | None):
    c = flaskapp.app.test_client()
    if email:
        uid = db.get_user_by_email(email)["id"]
        with c.session_transaction() as sess:
            sess["user_id"] = uid
            sess["user_email"] = email
            sess["ui_language"] = "de"
    return c


def post(c, path: str, data: dict | None = None):
    # Kein eigenes base_url: die Sitzung aus session_transaction haengt am
    # Standard-Host des Testclients. Die Herkunftspruefung vergleicht den
    # Origin-Kopf mit PUBLIC_BASE_URL, das genuegt.
    return c.post(path, data=data or {}, headers={"Origin": BASIS},
                  environ_base={"REMOTE_ADDR": "203.0.113.9"})


# ---------------------------------------------------------------------------
print("\n1. Bestandskonten bleiben nutzbar")
alt_id = db.create_user("alt@example.org", PW)       # Default: freigeschaltet
admin_id = db.create_user(ADMIN, PW)
with sqlite3.connect(TEST_DB) as c:
    # Ein Konto wie vor der Migration: Spalte approved faellt auf den Default.
    c.execute("INSERT INTO users (email, pw_hash, created_at) VALUES (?, ?, ?)",
              ("vorher@example.org", "x", "2026-01-01T00:00:00"))
    vorher = c.execute("SELECT approved FROM users WHERE email = 'vorher@example.org'").fetchone()[0]
pruefe(vorher == 1, "Konto ohne Angabe gilt als freigeschaltet (Default der Migration)")
db.init_db()   # zweiter Lauf: idempotent
pruefe(db.is_approved(alt_id), "Bestandskonto bleibt nach erneuter Migration freigeschaltet")

# ---------------------------------------------------------------------------
print("\n2. Registrierung wird zur gesperrten Anfrage")
versandt.clear()
anon = flaskapp.app.test_client()
with anon.session_transaction() as sess:
    sess["ui_language"] = "fr"
r = post(anon, "/login", {"action": "signup", "email": "neu@example.org",
                          "password": PW, "password2": PW})
ruhe()
neu = db.get_user_by_email("neu@example.org")
pruefe(r.status_code == 200 and neu is not None, "Anfrage angelegt, Seite antwortet normal")
pruefe(not db.is_approved(neu["id"]), "Anfrage ist gesperrt")
an_person = [m for m in versandt if m["to"] == "neu@example.org"]
an_admin = [m for m in versandt if m["to"] == ADMIN]
pruefe(len(an_person) == 1 and "reçu" in an_person[0]["subject"],
       "Eingangsbestaetigung an die Person, in ihrer Sprache (FR)")
pruefe(len(an_admin) == 1 and "neu@example.org" in an_admin[0]["text"]
       and f"{BASIS}/admin/konten" in an_admin[0]["text"],
       "Admin-Mail mit Adresse und Link in den Admin-Bereich")
pruefe(BASIS + "/login" not in an_person[0]["text"] or "freigeschaltet" not in an_person[0]["text"],
       "Eingangsbestaetigung enthaelt keinen Anmeldelink als Versprechen")

r = post(anon, "/login", {"action": "login", "email": "neu@example.org", "password": PW})
text = r.get_data(as_text=True)
pruefe(r.status_code == 403 and "/dashboard" not in (r.headers.get("Location") or ""),
       "Anmeldung einer offenen Anfrage wird abgewiesen")
with anon.session_transaction() as sess:
    pruefe("user_id" not in sess, "keine Sitzung fuer die offene Anfrage")
r = post(anon, "/login", {"action": "login", "email": "neu@example.org", "password": "falsch-falsch"})
pruefe(r.status_code == 200 and "noch nicht freigeschaltet" not in r.get_data(as_text=True)
       and "pas encore activé" not in r.get_data(as_text=True),
       "falsches Passwort verraet den Freischaltstatus nicht")

# ---------------------------------------------------------------------------
print("\n3. Admin-Seite")
r = client_als(ADMIN).get("/admin/konten")
seite = r.get_data(as_text=True)
pruefe(r.status_code == 200 and "neu@example.org" in seite and "Freischalten" in seite,
       "Anfrage steht mit Knopf 'Freischalten' auf der Admin-Seite")
pruefe(all(k["email"] != "neu@example.org" for k in db.list_accounts()),
       "offene Anfrage zaehlt nicht als Konto")
r = client_als("alt@example.org").get("/admin/konten")
pruefe(r.status_code == 302 and "neu@example.org" not in r.get_data(as_text=True),
       "Nicht-Admin wird umgeleitet, sieht nichts")
r = post(client_als("alt@example.org"), f"/admin/anfragen/{neu['id']}/freischalten")
pruefe(r.status_code == 302 and not db.is_approved(neu["id"]), "Nicht-Admin kann nicht freischalten")
r = post(flaskapp.app.test_client(), f"/admin/anfragen/{neu['id']}/freischalten")
pruefe(not db.is_approved(neu["id"]), "ohne Anmeldung kein Freischalten")
r = flaskapp.app.test_client().post(f"/admin/anfragen/{neu['id']}/freischalten",
                                    headers={"Origin": "https://angreifer.example"})
pruefe(r.status_code in (400, 403) and not db.is_approved(neu["id"]),
       "fremde Herkunft (CSRF) wird abgewiesen")

# ---------------------------------------------------------------------------
print("\n4. Freischalten")
versandt.clear()
r = post(client_als(ADMIN), f"/admin/anfragen/{neu['id']}/freischalten")
ruhe()
pruefe(r.status_code == 302 and db.is_approved(neu["id"]), "Admin schaltet frei")
pruefe(len(versandt) == 1 and versandt[0]["to"] == "neu@example.org"
       and "activé" in versandt[0]["subject"] and f"{BASIS}/login" in versandt[0]["text"],
       "Freischalt-Mail mit Anmeldelink, in der Sprache der Anfrage")
anon2 = flaskapp.app.test_client()
r = post(anon2, "/login", {"action": "login", "email": "neu@example.org", "password": PW})
pruefe(r.status_code == 302 and "/dashboard" in (r.headers.get("Location") or ""),
       "danach klappt die Anmeldung")
versandt.clear()
r = post(client_als(ADMIN), f"/admin/anfragen/{neu['id']}/freischalten")
ruhe()
pruefe(not versandt, "zweites Freischalten schickt keine zweite Mail")

# ---------------------------------------------------------------------------
print("\n5. Ablehnen")
versandt.clear()
post(flaskapp.app.test_client(), "/login", {"action": "signup", "email": "weg@example.org",
                                             "password": PW, "password2": PW})
ruhe()
weg = db.get_user_by_email("weg@example.org")
versandt.clear()
r = post(client_als(ADMIN), f"/admin/anfragen/{weg['id']}/ablehnen")
ruhe()
pruefe(r.status_code == 302 and db.get_user_by_email("weg@example.org") is None,
       "abgelehnte Anfrage ist geloescht")
with sqlite3.connect(TEST_DB) as c:
    rest = c.execute("SELECT COUNT(*) FROM mail_log WHERE lower(recipient) = 'weg@example.org'").fetchone()[0]
pruefe(rest == 0, "auch das Versandprotokoll zur Adresse ist weg")
pruefe(not versandt, "keine Mail an die abgelehnte Person")
r = post(client_als(ADMIN), f"/admin/anfragen/{alt_id}/ablehnen")
pruefe(db.get_user_by_email("alt@example.org") is not None,
       "ein aktives Konto laesst sich ueber 'Ablehnen' nicht loeschen")

print()
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("=" * 62)
print("Alle Pruefungen bestanden.")
