"""Konten durch die Administration entfernen (01.10.2026).

  1  Ein Mitgliederkonto wird samt allem entfernt, was daran haengt
  2  Die Person erfaehrt davon; ein zweiter Klick loescht nichts und mailt nicht
  3  Admin-Konten sind geschuetzt (ernannt und fest hinterlegt)
  4  Das eigene Konto geht hier nicht
  5  Offene Anfragen gehen hier nicht (dafuer gibt es "Ablehnen")
  6  Nicht-Admins und Nichtangemeldete kommen nicht durch, POST ohne Herkunft auch nicht
  7  Die Oberflaeche zeigt den Knopf nur dort, wo er wirkt

Eigene DB data/esg_admin_loeschen_test.db, Attrappe statt Mailversand, kein Netz.
Aufruf:  ./.venv/Scripts/python.exe test_admin_loeschen.py
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

TEST_DB = Path(__file__).parent / "data" / "esg_admin_loeschen_test.db"
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


def post(c, path: str, origin: str | None = BASIS):
    headers = {"Origin": origin} if origin else {}
    return c.post(path, data={}, headers=headers,
                  environ_base={"REMOTE_ADDR": "203.0.113.9"})


def zaehle(tabelle: str, spalte: str, wert) -> int:
    with sqlite3.connect(TEST_DB) as c:
        return c.execute(f"SELECT COUNT(*) FROM {tabelle} WHERE {spalte} = ?",
                         (wert,)).fetchone()[0]


def existiert(uid: int) -> bool:
    with sqlite3.connect(TEST_DB) as c:
        return c.execute("SELECT 1 FROM users WHERE id = ?", (uid,)).fetchone() is not None


admin_id = db.create_user(ADMIN, PW)

# ---------------------------------------------------------------------------
print("\n1. Ein Mitgliederkonto wird samt allem entfernt")
# ---------------------------------------------------------------------------
opfer = "mitglied@example.org"
opfer_id = db.create_user(opfer, PW, association=VERBAND)
db.upsert_company(opfer_id, {"name": "Musterweberei GmbH", "employees_total": 120})
db.save_analysis(opfer_id, [{"reg_key": "LkSG", "applies": "nein", "reason": "Probe"}])
db.log_mail(opfer, "signup_request", "sent", message_id="m1")
db.begin_login_attempt(opfer, "203.0.113.50")

pruefe(zaehle("companies", "user_id", opfer_id) == 1, "Ausgangslage: Unternehmensangaben da")
pruefe(zaehle("analyses", "user_id", opfer_id) == 1, "Ausgangslage: eine Pruefung da")
pruefe(zaehle("mail_log", "lower(recipient)", opfer) == 1, "Ausgangslage: Versandprotokoll da")

versandt.clear()
r = post(client_als(ADMIN), f"/admin/konten/{opfer_id}/entfernen")
ruhe()
pruefe(r.status_code in (302, 303), f"Antwort ist eine Umleitung (HTTP {r.status_code})")
pruefe(not existiert(opfer_id), "das Konto ist weg")
pruefe(zaehle("companies", "user_id", opfer_id) == 0, "Unternehmensangaben sind weg")
pruefe(zaehle("analyses", "user_id", opfer_id) == 0, "Pruefungen sind weg")
pruefe(zaehle("mail_log", "lower(recipient)", opfer) <= 1,
       "vom Versandprotokoll bleibt hoechstens die Nachricht ueber die Loeschung")
with sqlite3.connect(TEST_DB) as _c:
    reste = _c.execute(
        "SELECT COUNT(*) FROM login_attempts WHERE subject = ? OR subject LIKE ?",
        (opfer, opfer + "|%")).fetchone()[0]
pruefe(reste == 0, "die Eintraege der Login-Bremse sind weg")

# ---------------------------------------------------------------------------
print("\n2. Nachricht an die Person, und nur eine")
# ---------------------------------------------------------------------------
pruefe(len(versandt) == 1 and versandt[0]["to"] == opfer,
       f"genau eine Nachricht an die betroffene Adresse ({len(versandt)})")
if versandt:
    pruefe(ADMIN in versandt[0]["text"], "sie nennt, wer entfernt hat")
    pruefe(BASIS in versandt[0]["text"], "und den Weg zur Neuregistrierung")

versandt.clear()
r = post(client_als(ADMIN), f"/admin/konten/{opfer_id}/entfernen")
ruhe()
pruefe(not versandt, "der zweite Klick auf dieselbe Kennung mailt nicht noch einmal")

# ---------------------------------------------------------------------------
print("\n3. Admin-Konten sind geschuetzt")
# ---------------------------------------------------------------------------
ernannt = "ernannt@example.org"
ernannt_id = db.create_user(ernannt, PW)
db.set_admin(ernannt_id, True)
versandt.clear()
post(client_als(ADMIN), f"/admin/konten/{ernannt_id}/entfernen")
ruhe()
pruefe(existiert(ernannt_id), "ein ernannter Admin wird nicht entfernt")
pruefe(not versandt, "und es geht keine Nachricht raus")

# Erst nach dem Entzug - sonst koennte ein ernannter Admin das feste Konto
# entfernen und sich so die Rechtevergabe holen.
db.set_admin(ernannt_id, False)
versandt.clear()
post(client_als(ADMIN), f"/admin/konten/{ernannt_id}/entfernen")
ruhe()
pruefe(not existiert(ernannt_id), "nach dem Entzug des Rechts geht es")

zweiter_fest = "fest-zwei@example.org"
if len(flaskapp.ADMIN_EMAILS) > 1:
    zweiter_fest = sorted(flaskapp.ADMIN_EMAILS)[1]
    fest_id = db.create_user(zweiter_fest, PW)
else:
    fest_id = None
if fest_id:
    post(client_als(ADMIN), f"/admin/konten/{fest_id}/entfernen")
    pruefe(existiert(fest_id), "ein fest hinterlegtes Konto wird nicht entfernt")
else:
    print("  [--]   nur eine fest hinterlegte Adresse — Fall nicht pruefbar")

# ---------------------------------------------------------------------------
print("\n4. Das eigene Konto geht hier nicht")
# ---------------------------------------------------------------------------
post(client_als(ADMIN), f"/admin/konten/{admin_id}/entfernen")
pruefe(existiert(admin_id), "der Admin entfernt sich nicht selbst")

nur_admin = "zweiter-admin@example.org"
nur_admin_id = db.create_user(nur_admin, PW)
db.set_admin(nur_admin_id, True)
post(client_als(nur_admin), f"/admin/konten/{nur_admin_id}/entfernen")
pruefe(existiert(nur_admin_id), "auch ein ernannter Admin nicht sich selbst")
db.set_admin(nur_admin_id, False)

# ---------------------------------------------------------------------------
print("\n5. Offene Anfragen gehen hier nicht")
# ---------------------------------------------------------------------------
anfrage = "anfrage@example.org"
anfrage_id = db.create_user(anfrage, None, approved=False, lang="de",
                            association=VERBAND)
versandt.clear()
post(client_als(ADMIN), f"/admin/konten/{anfrage_id}/entfernen")
ruhe()
pruefe(existiert(anfrage_id), "eine offene Anfrage bleibt stehen (dafuer gibt es Ablehnen)")
pruefe(not versandt, "und es geht keine Nachricht raus")
pruefe(db.reject_user(anfrage_id) == anfrage, "Ablehnen raeumt sie weg")
pruefe(not existiert(anfrage_id), "danach ist sie weg")

# ---------------------------------------------------------------------------
print("\n6. Wer nicht darf, kommt nicht durch")
# ---------------------------------------------------------------------------
mitglied = "normal@example.org"
mitglied_id = db.create_user(mitglied, PW, association=VERBAND)
ziel = "ziel@example.org"
ziel_id = db.create_user(ziel, PW, association=VERBAND)

r = post(client_als(mitglied), f"/admin/konten/{ziel_id}/entfernen")
pruefe(existiert(ziel_id), "ein normales Mitglied entfernt niemanden")
pruefe(r.status_code in (302, 303), "es wird umgeleitet, nicht beantwortet")

r = post(client_als(None), f"/admin/konten/{ziel_id}/entfernen")
pruefe(existiert(ziel_id), "ohne Anmeldung geht nichts")

# Herkunftspruefung (app._herkunft_pruefen): Eine fremde Herkunft wird
# abgewiesen - das ist der CSRF-Fall, bei dem der Browser das Sitzungscookie
# einer anderen Seite mitschickt.
r = post(client_als(ADMIN), f"/admin/konten/{ziel_id}/entfernen",
         origin="https://angreifer.example")
pruefe(r.status_code == 403, f"POST mit fremder Herkunft: 403 (war {r.status_code})")
pruefe(existiert(ziel_id), "und das Konto bleibt stehen")

# Fehlen Origin UND Referer, wird bewusst durchgelassen: so verhaelt sich kein
# Browser, sondern ein Werkzeug wie curl - das bringt keine fremden
# Sitzungscookies mit. Entscheidung vom 24.09.2026, hier festgehalten, damit
# eine Aenderung daran auffaellt.
r = post(client_als(ADMIN), f"/admin/konten/{ziel_id}/entfernen", origin=None)
pruefe(not existiert(ziel_id),
       "ohne Origin und Referer wird durchgelassen (dokumentierte Entscheidung)")

# ---------------------------------------------------------------------------
print("\n7. Die Oberflaeche zeigt den Knopf nur dort, wo er wirkt")
# ---------------------------------------------------------------------------
db.set_admin(mitglied_id, True)
knopf = "knopf@example.org"
knopf_id = db.create_user(knopf, PW, association=VERBAND)
seite = client_als(ADMIN).get("/admin/konten").get_data(as_text=True)
tabelle = seite.split('id="konten"')[1] if 'id="konten"' in seite else ""
pruefe(bool(tabelle), "die Kontentabelle wird ausgegeben")
pruefe(f"/admin/konten/{knopf_id}/entfernen" in tabelle,
       "fuer ein gewoehnliches Konto steht der Knopf da")
pruefe(f"/admin/konten/{admin_id}/entfernen" not in tabelle,
       "fuer das eigene Konto nicht")
pruefe(f"/admin/konten/{mitglied_id}/entfernen" not in tabelle,
       "fuer ein Admin-Konto nicht")
pruefe("confirm(" in tabelle, "der Knopf fragt im Browser zurueck")
pruefe(flaskapp.t("admin_delete_btn", "de") in tabelle, "die Beschriftung ist uebersetzt")

seite_mitglied = client_als(knopf).get("/admin/konten")
pruefe(seite_mitglied.status_code in (302, 303),
       "ein Mitglied sieht die Kontenseite ueberhaupt nicht")

# ---------------------------------------------------------------------------
ruhe()
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
