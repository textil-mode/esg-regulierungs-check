"""Tests zu den Befunden M1-M5 und N1/N3/N5 des Durchlaufs vom 24.09.2026.

Laeuft ausschliesslich gegen eine eigene Datenbank (`data/esg_konto_test.db`),
die zu Beginn frisch angelegt wird — `data/esg.db` wird nie beruehrt.
**Kein Netz, keine echte Mail:** `mailer.send` wird durch eine Attrappe
ersetzt, die nur mitschreibt.

Aufruf:  ./.venv/Scripts/python.exe test_konto_sicherheit.py
"""
from __future__ import annotations

import os
import sqlite3
import statistics
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_konto_test.db"
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

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH} statt auf die Kopie!"
db.init_db()

import mailer  # noqa: E402
import app as flaskapp  # noqa: E402

assert db.DB_PATH == TEST_DB, "app.py hat die Test-Datenbank umgebogen!"

BEKANNT = "schon-da@example.org"
NEU = "noch-nicht-da@example.org"
PW = "ein-gutes-Passwort-2026"
IP_A = "203.0.113.5"

BEKANNT_ID = db.create_user(BEKANNT, PW)
BASIS_THREADS = threading.active_count()

fehler: list[str] = []
versandt: list[dict] = []


def _attrappe(recipient: str, subject: str, text: str) -> str:
    versandt.append({"to": recipient, "subject": subject, "text": text})
    return "msg_%03d" % len(versandt)


mailer.send = _attrappe
mailer.is_configured = lambda: True


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def ruhe(sekunden: float = 5.0) -> bool:
    ende = time.perf_counter() + sekunden
    while threading.active_count() > BASIS_THREADS and time.perf_counter() < ende:
        time.sleep(0.005)
    time.sleep(0.05)
    return threading.active_count() <= BASIS_THREADS


def _leeren() -> None:
    ruhe()
    with sqlite3.connect(TEST_DB) as c:
        c.execute("DELETE FROM login_attempts")
        c.execute("DELETE FROM mail_log")
    versandt.clear()


def registrieren(email: str, ip: str = IP_A, pw: str = PW):
    with flaskapp.app.test_client() as client:
        return client.post(
            "/login",
            data={"action": "signup", "email": email,
                  "password": pw, "password2": pw},
            environ_base={"REMOTE_ADDR": ip},
        )


# ---------------------------------------------------------------------------
print("\n1. Die Registrierung verraet nicht, welche Adressen es gibt (M1)")
# ---------------------------------------------------------------------------
_leeren()
a = registrieren(BEKANNT)
ruhe()
mails_bekannt = [m["subject"] for m in versandt]
seite_bekannt = a.get_data(as_text=True)

_leeren()
b = registrieren(NEU)
ruhe()
mails_neu = [m["subject"] for m in versandt]
seite_neu = b.get_data(as_text=True)

pruefe(a.status_code == b.status_code,
       f"gleicher HTTP-Status ({a.status_code})")
pruefe(seite_bekannt == seite_neu,
       "die ausgelieferte Seite ist Zeichen fuer Zeichen dieselbe")
pruefe("bereits" not in seite_bekannt.lower()
       and "vergeben" not in seite_bekannt.lower(),
       "kein Hinweis auf ein bestehendes Konto in der Antwort")
pruefe(a.status_code == 200 and "/dashboard" not in (a.headers.get("Location") or ""),
       "niemand wird mehr automatisch angemeldet")
pruefe(len(mails_bekannt) == 1 and len(mails_neu) == 1,
       "in beiden Faellen geht genau eine Mail raus")
if mails_bekannt and mails_neu:
    pruefe(mails_bekannt[0] != mails_neu[0],
           "der Inhaber erfaehrt per Mail, was wirklich war")
pruefe(db.email_exists(NEU), "das neue Konto wurde tatsaechlich angelegt")
neu_id = db.get_user_by_email(NEU)["id"]
pruefe(db.verify_user(NEU, PW) == neu_id, "und laesst sich benutzen")

# Zweiter Versuch auf die nun vergebene Adresse: wieder dieselbe Antwort.
_leeren()
c2 = registrieren(NEU)
ruhe()
pruefe(c2.get_data(as_text=True) == seite_neu,
       "auch beim zweiten Versuch sieht die Seite gleich aus")
pruefe(len(versandt) == 1 and "bereits" in versandt[0]["subject"].lower(),
       "diesmal geht die Nachricht 'Es besteht bereits ein Konto' raus")

# ---------------------------------------------------------------------------
print("\n2. Die Antwortzeit verraet es auch nicht (M1)")
# ---------------------------------------------------------------------------
# Das Anlegen kostet bcrypt-Zeit, das blosse Nachschlagen nicht. Liefe das im
# Vordergrund, waere die Dauer der Verraeter.
_leeren()


def _messe(vorlage: str, runden: int = 5) -> float:
    zeiten = []
    for i in range(runden):
        adresse = vorlage.format(i=i)
        start = time.perf_counter()
        registrieren(adresse, ip=f"198.51.100.{i + 20}")
        zeiten.append((time.perf_counter() - start) * 1000)
        ruhe()
        with sqlite3.connect(TEST_DB) as c:
            c.execute("DELETE FROM login_attempts")
    return statistics.median(zeiten)


m_bekannt = _messe(BEKANNT.replace("@", "{i}@").replace("{i}", ""))
m_neu = _messe("frisch{i}@example.org")
faktor = max(m_bekannt, m_neu) / max(min(m_bekannt, m_neu), 0.001)
print(f"    bestehend: Median {m_bekannt:6.1f} ms")
print(f"    neu:       Median {m_neu:6.1f} ms")
print(f"    Faktor:    {faktor:.2f}")
pruefe(faktor < 1.35, "beide Faelle brauchen praktisch gleich lang (Faktor < 1,35)")

# ---------------------------------------------------------------------------
print("\n3. Bremse gegen massenhaftes Anlegen von Konten (M2)")
# ---------------------------------------------------------------------------
_leeren()
IP_FLUT = "192.0.2.77"
angelegt = 0
for i in range(db.SIGNUP_MAX_PER_IP):
    r = registrieren(f"flut{i}@example.org", ip=IP_FLUT)
    if r.status_code == 200:
        angelegt += 1
ruhe()
pruefe(angelegt == db.SIGNUP_MAX_PER_IP,
       f"die ersten {db.SIGNUP_MAX_PER_IP} Registrierungen gehen durch")
zu_viel = registrieren("flut-zuviel@example.org", ip=IP_FLUT)
ruhe()
pruefe(zu_viel.status_code == 429, "die naechste wird mit 429 abgewiesen")
pruefe(not db.email_exists("flut-zuviel@example.org"),
       "und legt kein Konto an")
anders = registrieren("andere-leitung@example.org", ip="203.0.113.200")
ruhe()
pruefe(anders.status_code == 200 and db.email_exists("andere-leitung@example.org"),
       "von einer anderen Adresse kommt man weiterhin durch")

# ---------------------------------------------------------------------------
print("\n4. Passwortwechsel wird dem Inhaber gemeldet (M3)")
# ---------------------------------------------------------------------------
_leeren()
with flaskapp.app.test_client() as client:
    with client.session_transaction() as sitzung:
        sitzung["user_id"] = BEKANNT_ID
        sitzung["user_email"] = BEKANNT
    client.post("/passwort-aendern", data={
        "current_password": PW,
        "password": "neues-Passwort-2026",
        "password2": "neues-Passwort-2026",
    })
ruhe()
pruefe(len(versandt) == 1, "eine Nachricht geht raus")
if versandt:
    pruefe(versandt[0]["to"] == BEKANNT, "sie geht an den Kontoinhaber")
    pruefe("neues-Passwort-2026" not in versandt[0]["text"],
           "das neue Passwort steht nicht darin")
    pruefe(BASIS in versandt[0]["text"],
           "der enthaltene Link zeigt auf die eigene Adresse")
protokoll = {z["purpose"] for z in db.list_mail_log()}
pruefe("password_changed" in protokoll, "der Versand steht im Protokoll")
db.set_password(BEKANNT_ID, PW)

# ---------------------------------------------------------------------------
print("\n5. Versandprotokoll: Aufbewahrung und Loeschung (M4)")
# ---------------------------------------------------------------------------
_leeren()
db.log_mail(BEKANNT, "password_reset", "sent", message_id="m1")
db.log_mail("fremd@example.org", "password_reset", "sent", message_id="m2")
pruefe(len(db.list_mail_log()) == 2, "zwei Eintraege liegen vor")

db.delete_user(BEKANNT_ID)
rest = db.list_mail_log()
pruefe(all(z["recipient"] != BEKANNT for z in rest),
       "beim Loeschen des Kontos verschwindet die Adresse aus dem Protokoll")
pruefe(any(z["recipient"] == "fremd@example.org" for z in rest),
       "fremde Eintraege bleiben unberuehrt")

# Alteintrag ueber der Aufbewahrungsfrist wird beim naechsten Schreiben entfernt.
alt = (datetime.utcnow() - timedelta(days=db.MAIL_LOG_KEEP_DAYS + 1)).isoformat()
with sqlite3.connect(TEST_DB) as c:
    c.execute("""INSERT INTO mail_log
                     (logged_at, recipient, purpose, status, message_id, error)
                 VALUES (?, 'uralt@example.org', 'password_reset', 'sent', 'm3', NULL)""",
              (alt,))
pruefe(any(z["recipient"] == "uralt@example.org" for z in db.list_mail_log()),
       f"ein {db.MAIL_LOG_KEEP_DAYS + 1} Tage alter Eintrag liegt vor")
db.log_mail("neu@example.org", "password_reset", "sent", message_id="m4")
pruefe(all(z["recipient"] != "uralt@example.org" for z in db.list_mail_log()),
       f"er wird nach {db.MAIL_LOG_KEEP_DAYS} Tagen weggeraeumt")
BEKANNT_ID = db.create_user(BEKANNT, PW)   # fuer die folgenden Bloecke

# ---------------------------------------------------------------------------
print("\n6. POST von einer fremden Seite wird abgewiesen (M5)")
# ---------------------------------------------------------------------------
_leeren()
with flaskapp.app.test_client() as client:
    fremd = client.post("/login", data={"action": "forgot", "email": BEKANNT},
                        headers={"Origin": "https://angreifer.example"})
    pruefe(fremd.status_code == 403, "fremder Origin: 403")

    fremd_ref = client.post("/login", data={"action": "forgot", "email": BEKANNT},
                            headers={"Referer": "https://angreifer.example/falle"})
    pruefe(fremd_ref.status_code == 403, "fremder Referer: 403")

    eigen = client.post("/login", data={"action": "forgot", "email": BEKANNT},
                        headers={"Origin": BASIS})
    pruefe(eigen.status_code in (200, 429), "eigener Origin: kommt durch")

    ohne = client.post("/login", data={"action": "forgot", "email": BEKANNT})
    pruefe(ohne.status_code in (200, 429),
           "ohne Origin und Referer (curl o. ae.): kommt durch")

    lesend = client.get("/login", headers={"Origin": "https://angreifer.example"})
    pruefe(lesend.status_code == 200, "GET bleibt unberuehrt")
ruhe()
_leeren()

# ---------------------------------------------------------------------------
print("\n7. Sprachumschaltung fuehrt nicht auf fremde Seiten (N1)")
# ---------------------------------------------------------------------------
with flaskapp.app.test_client() as client:
    weg = client.post("/set-language", data={"language": "en"},
                      headers={"Referer": "https://test.example/esg/datenschutz",
                               "Origin": BASIS})
    ziel = weg.headers.get("Location") or ""
    pruefe(weg.status_code in (302, 303), "eigene Seite: Umleitung")
    pruefe("angreifer" not in ziel, "und nicht nach draussen")

    fremd = client.post("/set-language", data={"language": "en"},
                        headers={"Referer": "https://angreifer.example/falle",
                                 "Origin": BASIS})
    ziel_fremd = fremd.headers.get("Location") or ""
    pruefe("angreifer.example" not in ziel_fremd,
           f"fremder Referer landet nicht dort (Ziel: {ziel_fremd or '—'})")

# ---------------------------------------------------------------------------
print("\n8. Sitzung: Ablauf und sauberer Start (N3/N5)")
# ---------------------------------------------------------------------------
pruefe(flaskapp.app.config["PERMANENT_SESSION_LIFETIME"] == timedelta(hours=12),
       "die Sitzung laeuft nach 12 Stunden ab")
with flaskapp.app.test_client() as client:
    with client.session_transaction() as sitzung:
        sitzung["altlast"] = "darf nicht ueberleben"
    client.post("/login", data={"action": "login", "email": BEKANNT,
                                "password": PW})
    with client.session_transaction() as sitzung:
        pruefe("altlast" not in sitzung,
               "beim Anmelden wird die vorige Sitzung verworfen")
        pruefe(sitzung.get("user_id") == BEKANNT_ID, "und das Konto gesetzt")
        pruefe(sitzung.permanent, "die Sitzung traegt ein Ablaufdatum")

# ---------------------------------------------------------------------------
ruhe()
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
