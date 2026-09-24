# -*- coding: utf-8 -*-
"""Prueft die neue Kontenuebersicht: Inhalt, Rechte, letzte Anmeldung."""
import os
import sys
import time
from pathlib import Path

PROJEKT = Path(r"H:\KI-Projekte\ESG-Plattform\esg_app_v2")
os.chdir(PROJEKT)
sys.path.insert(0, str(PROJEKT))

TEST_DB = PROJEKT / "data" / "esg_konten_seite_test.db"
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    os.environ[v] = ""
os.environ["PUBLIC_BASE_URL"] = "https://test.example"

import db  # noqa: E402
assert db.DB_PATH == TEST_DB, "falsche Datenbank!"
db.init_db()
import app as flaskapp  # noqa: E402

ADMIN = "mschuckert@textil-mode.de"
GAST = "gast@example.org"
PW = "ein-gutes-Passwort-2026"

fehler = []


def pruefe(bedingung, text):
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


admin_id = db.create_user(ADMIN, PW)
gast_id = db.create_user(GAST, PW)
db.upsert_company(gast_id, {"name": "Musterweberei GmbH"})

print("\n1. Die Liste zeigt den Bestand")
konten = db.list_accounts()
pruefe(len(konten) == 2, "beide Konten erscheinen")
adressen = {k["email"] for k in konten}
pruefe(adressen == {ADMIN, GAST}, "mit ihren Adressen")
gast = [k for k in konten if k["email"] == GAST][0]
pruefe(gast["company_name"] == "Musterweberei GmbH", "Firmenname steht dabei")
pruefe(gast["analyses_count"] == 0, "Pruefungen werden gezaehlt (hier 0)")
pruefe("pw_hash" not in gast, "der Passwort-Hash ist NICHT enthalten")
pruefe("employees" not in gast and "revenue_eur" not in gast,
       "Profilzahlen sind NICHT enthalten")

print("\n2. Letzte Anmeldung wird erfasst")
pruefe(gast["last_login_at"] is None, "vor der ersten Anmeldung: leer")
db.verify_user(GAST, PW)
gast = [k for k in db.list_accounts() if k["email"] == GAST][0]
pruefe(bool(gast["last_login_at"]), "nach der Anmeldung: gesetzt")
erster = gast["last_login_at"]
time.sleep(1.1)
db.verify_user(GAST, "falsches-passwort")
gast = [k for k in db.list_accounts() if k["email"] == GAST][0]
pruefe(gast["last_login_at"] == erster, "ein Fehlversuch aendert nichts")
db.verify_user(GAST, PW)
gast = [k for k in db.list_accounts() if k["email"] == GAST][0]
pruefe(gast["last_login_at"] > erster, "die naechste Anmeldung ueberschreibt")

print("\n3. Reihenfolge und Zaehlwerte")
db.save_analysis(gast_id, {"foo": "bar"})
gast = [k for k in db.list_accounts() if k["email"] == GAST][0]
pruefe(gast["analyses_count"] == 1, "Pruefung wird mitgezaehlt")
pruefe(bool(gast["last_analysis"]), "Zeitpunkt der letzten Pruefung steht da")

print("\n4. Die Seite ist nur fuer den Admin")
with flaskapp.app.test_client() as client:
    ohne = client.get("/admin/konten")
    pruefe(ohne.status_code in (302, 303), "ohne Anmeldung: Umleitung")

    with client.session_transaction() as s:
        s["user_id"] = gast_id
        s["user_email"] = GAST
    fremd = client.get("/admin/konten")
    pruefe(fremd.status_code in (302, 303), "als gewoehnlicher Nutzer: Umleitung")
    pruefe(GAST not in fremd.get_data(as_text=True), "und keine Daten im Rumpf")

with flaskapp.app.test_client() as client:
    with client.session_transaction() as s:
        s["user_id"] = admin_id
        s["user_email"] = ADMIN
    seite = client.get("/admin/konten")
    inhalt = seite.get_data(as_text=True)
    pruefe(seite.status_code == 200, "als Admin: die Seite laedt")
    pruefe(GAST in inhalt, "das Gastkonto steht darin")
    pruefe("Musterweberei GmbH" in inhalt, "mit dem Firmennamen")
    pruefe("Konten insgesamt" in inhalt, "die Kennzahlen stehen oben")
    pruefe("$2b$" not in inhalt and "pw_hash" not in inhalt,
           "kein Passwort-Hash auf der Seite")
    pruefe("Konten" in inhalt, "der Menuepunkt ist da")

print("\n5. Bestandskonten ohne Zeitpunkt")
with __import__("sqlite3").connect(TEST_DB) as c:
    c.execute("UPDATE users SET last_login_at = NULL WHERE id = ?", (gast_id,))
with flaskapp.app.test_client() as client:
    with client.session_transaction() as s:
        s["user_id"] = admin_id
        s["user_email"] = ADMIN
    inhalt = client.get("/admin/konten").get_data(as_text=True)
    pruefe("nicht erfasst" in inhalt,
           "zeigt 'nicht erfasst' statt einer erfundenen Angabe")

print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
