"""Admin-Rechte ueber die Oberflaeche vergeben (29.09.2026).

  1  Migration: Spalte is_admin, Bestandskonten sind keine Admins
  2  Das fest hinterlegte Konto erteilt Admin-Rechte: Recht in der DB, Mail an die Person
  3  Ein ernannter Admin erreicht alle Admin-Seiten und kann freischalten
  4  ... darf aber keine Rechte vergeben oder entziehen und sieht keine Knoepfe
  5  ... und keinen Reset-Link fuer Admin-Konten erzeugen (Uebernahme des festen Kontos)
  6  Schutz: festes Konto unveraenderbar, offene Anfrage kein Admin, Nicht-Admins abgewiesen,
     POST ohne Herkunft abgewiesen
  7  Registrierungs-Mails gehen an alle Admins
  8  Entziehen wirkt sofort, auch in laufender Sitzung; Doppelklick = eine Mail

Eigene DB data/esg_admin_rollen_test.db, Attrappe statt Mailversand, kein Netz.
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

TEST_DB = Path(__file__).parent / "data" / "esg_admin_rollen_test.db"
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
import regulations  # noqa: E402
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
        with c.session_transaction() as sess:
            sess["user_id"] = db.get_user_by_email(email)["id"]
            sess["user_email"] = email
            sess["ui_language"] = "de"
    return c


def post(c, path: str, data: dict | None = None, origin: str | None = BASIS):
    headers = {"Origin": origin} if origin else {}
    return c.post(path, data=data or {}, headers=headers,
                  environ_base={"REMOTE_ADDR": "203.0.113.9"})


def ist_admin_seite(r) -> bool:
    return r.status_code == 200


def rolle(uid: int) -> int:
    with sqlite3.connect(TEST_DB) as c:
        return c.execute("SELECT is_admin FROM users WHERE id = ?", (uid,)).fetchone()[0]


# ---------------------------------------------------------------------------
print("1. Migration")
admin_id = db.create_user(ADMIN, PW)
berta_id = db.create_user("berta@example.org", PW)
carl_id = db.create_user("carl@example.org", PW)
dora_id = db.create_user("dora@example.org", PW)
offen_id = db.create_user("offen@example.org", None, approved=False, lang="de")
db.init_db()   # zweiter Lauf: idempotent
pruefe(rolle(berta_id) == 0 and rolle(admin_id) == 0,
       "Spalte is_admin vorhanden, Bestandskonten sind keine Admins")
pruefe(not db.admin_emails(), "keine Admins in der Datenbank")

# ---------------------------------------------------------------------------
print("\n2. Festes Admin-Konto erteilt Admin-Rechte")
chef = client_als(ADMIN)
seite = chef.get("/admin/konten").get_data(as_text=True)
pruefe("Zum Admin machen" in seite and "Admin (fest)" in seite,
       "Knopf \"Zum Admin machen\" und Kennzeichnung des festen Kontos sichtbar")
fest_zeile = seite.split(f">{ADMIN}</td>", 1)[1].split("</tr>", 1)[0]
pruefe("Zum Admin machen" not in fest_zeile and "entziehen" not in fest_zeile,
       "am festen Konto selbst steht kein Knopf")
versandt.clear()
r = post(chef, f"/admin/konten/{berta_id}/admin-recht", {"recht": "erteilen"})
ruhe()
pruefe(r.status_code == 302 and rolle(berta_id) == 1, "Berta ist jetzt Admin")
pruefe([m["to"] for m in versandt] == ["berta@example.org"]
       and "Admin-Rechte" in versandt[0]["subject"] and ADMIN in versandt[0]["text"]
       and f"{BASIS}/admin/konten" in versandt[0]["text"],
       "Berta erhaelt eine Mail mit Absender der Vergabe und Link")
pruefe(db.admin_emails() == ["berta@example.org"], "admin_emails() liefert Berta")
seite = chef.get("/admin/konten").get_data(as_text=True)
berta_zeile = seite.split(">berta@example.org</td>", 1)[1].split("</tr>", 1)[0]
pruefe("Admin-Recht entziehen" in berta_zeile and 'data-sort-value="Admin"' in berta_zeile,
       "in der Liste als Admin gekennzeichnet, mit Knopf zum Entziehen")

# ---------------------------------------------------------------------------
print("\n3. Ernannter Admin erreicht alle Admin-Seiten")
berta = client_als("berta@example.org")
for pfad in ("/admin/konten", "/admin/passwort-resets", "/admin/regulierungs-status"):
    r = berta.get(pfad)
    pruefe(ist_admin_seite(r), f"{pfad} -> {r.status_code}")
menue = berta.get("/dashboard").get_data(as_text=True)
pruefe("/admin/konten" in menue, "Admin-Menuepunkte werden angezeigt")
versandt.clear()
r = post(berta, f"/admin/anfragen/{offen_id}/freischalten",
         {"kontotyp": db.ACCOUNT_TYPE_USER})
ruhe()
pruefe(db.is_approved(offen_id) and any(m["to"] == "offen@example.org" for m in versandt),
       "Berta kann eine Anfrage freischalten")
with sqlite3.connect(TEST_DB) as c:
    c.execute("UPDATE users SET approved = 0 WHERE id = ?", (offen_id,))   # fuer Block 6

# ---------------------------------------------------------------------------
print("\n4. Ernannter Admin vergibt keine Rechte")
versandt.clear()
r = post(berta, f"/admin/konten/{carl_id}/admin-recht", {"recht": "erteilen"})
pruefe(rolle(carl_id) == 0, "Berta kann Carl nicht zum Admin machen")
r = post(berta, f"/admin/konten/{berta_id}/admin-recht", {"recht": "entziehen"})
pruefe(rolle(berta_id) == 1, "... und sich selbst nichts aendern")
ruhe()
pruefe(not versandt, "dabei geht keine Mail raus")
seite = berta.get("/admin/konten").get_data(as_text=True)
pruefe("Zum Admin machen" not in seite and "Admin-Recht entziehen" not in seite,
       "Berta sieht keine Knoepfe zur Rechtevergabe")

# ---------------------------------------------------------------------------
print("\n5. Reset-Links fuer Admin-Konten nur durch das feste Konto")
db.set_admin(dora_id, True)
for ziel, name in ((ADMIN, "festes Admin-Konto"), ("dora@example.org", "ernannte Admina")):
    with sqlite3.connect(TEST_DB) as c:
        vorher = c.execute("SELECT COUNT(*) FROM password_resets").fetchone()[0]
    r = post(berta, "/admin/passwort-resets", {"email": ziel})
    text = r.get_data(as_text=True)
    with sqlite3.connect(TEST_DB) as c:
        nachher = c.execute("SELECT COUNT(*) FROM password_resets").fetchone()[0]
    pruefe(nachher == vorher and "/passwort-zuruecksetzen/" not in text,
           f"Berta erzeugt keinen Link fuer das {name}")
r = post(berta, "/admin/passwort-resets", {"email": "carl@example.org"})
pruefe("carl@example.org" in r.get_data(as_text=True) and r.status_code == 200,
       "fuer ein Mitgliederkonto geht es weiterhin")
with sqlite3.connect(TEST_DB) as c:
    vorher = c.execute("SELECT COUNT(*) FROM password_resets").fetchone()[0]
post(chef, "/admin/passwort-resets", {"email": "dora@example.org"})
with sqlite3.connect(TEST_DB) as c:
    nachher = c.execute("SELECT COUNT(*) FROM password_resets").fetchone()[0]
pruefe(nachher == vorher + 1, "das feste Konto kann auch fuer Admin-Konten einen Link erzeugen")
db.set_admin(dora_id, False)

# ---------------------------------------------------------------------------
print("\n6. Schutzregeln")
r = post(chef, f"/admin/konten/{admin_id}/admin-recht", {"recht": "entziehen"})
pruefe(client_als(ADMIN).get("/admin/konten").status_code == 200,
       "festes Konto bleibt Admin, auch nach Versuch des Entziehens")
r = post(chef, f"/admin/konten/{offen_id}/admin-recht", {"recht": "erteilen"})
pruefe(rolle(offen_id) == 0, "eine offene Anfrage wird nicht zum Admin")
r = post(chef, "/admin/konten/99999/admin-recht", {"recht": "erteilen"})
pruefe(r.status_code == 302, "unbekannte Kennung: Umleitung, kein Fehler")
carl = client_als("carl@example.org")
r = post(carl, f"/admin/konten/{carl_id}/admin-recht", {"recht": "erteilen"})
pruefe(rolle(carl_id) == 0 and "/dashboard" in (r.headers.get("Location") or ""),
       "Mitglied ohne Admin-Recht wird abgewiesen")
pruefe(carl.get("/admin/konten").status_code == 302, "... und sieht die Kontenliste nicht")
r = post(chef, f"/admin/konten/{carl_id}/admin-recht", {"recht": "erteilen"}, origin="https://boese.example")
pruefe(rolle(carl_id) == 0 and r.status_code == 403, f"POST von fremder Herkunft abgewiesen ({r.status_code})")
pruefe(client_als(None).post(f"/admin/konten/{carl_id}/admin-recht", data={"recht": "erteilen"},
                             headers={"Origin": BASIS}).status_code == 302 and rolle(carl_id) == 0,
       "ohne Anmeldung: Umleitung zur Anmeldung")

# ---------------------------------------------------------------------------
print("\n7. Registrierungs-Mails gehen an alle Admins")
with sqlite3.connect(TEST_DB) as c:
    c.execute("DELETE FROM login_attempts")
versandt.clear()
post(flaskapp.app.test_client(), "/login", {"action": "signup", "email": "neuling@example.org",
     "association": regulations.MEMBER_ASSOCIATIONS[0]})
ruhe()
an = sorted(m["to"] for m in versandt if "Zugangsanfrage" in m["subject"] and m["to"] != "neuling@example.org")
pruefe(an == sorted([ADMIN, "berta@example.org"]), f"Admin-Mail an festes Konto und Berta ({an})")

# ---------------------------------------------------------------------------
print("\n8. Entziehen")
versandt.clear()
r = post(chef, f"/admin/konten/{berta_id}/admin-recht", {"recht": "entziehen"})
post(chef, f"/admin/konten/{berta_id}/admin-recht", {"recht": "entziehen"})   # Doppelklick
ruhe()
pruefe(rolle(berta_id) == 0, "Berta ist kein Admin mehr")
pruefe([m["to"] for m in versandt] == ["berta@example.org"] and "entzogen" in versandt[0]["subject"],
       "genau eine Mail an Berta, auch beim Doppelklick")
r = berta.get("/admin/konten")
pruefe(r.status_code == 302, "Bertas laufende Sitzung verliert den Zugang sofort")
pruefe(berta.get("/dashboard").status_code == 200, "ihr Konto bleibt nutzbar")

print()
if fehler:
    print(f"{len(fehler)} Pruefung(en) fehlgeschlagen")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
