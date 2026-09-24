"""Tests fuer den automatischen Versand des Passwort-Reset-Links.

Laeuft ausschliesslich gegen eine eigene Datenbank (`data/esg_mail_test.db`),
die zu Beginn frisch angelegt wird — `data/esg.db` wird nie beruehrt.
**Kein Netz, keine echte Mail:** `mailer.send` wird durch eine Attrappe
ersetzt, die nur mitschreibt.

Aufruf:  ./.venv/Scripts/python.exe test_reset_mail.py
"""
from __future__ import annotations

import os
import sqlite3
import threading
import statistics
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_mail_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
# Sicherstellen, dass kein echter Zugang aus der .env in den Test rutscht.
for _var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
             "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_var] = ""

import db  # noqa: E402

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH} statt auf die Kopie!"
db.init_db()

import mailer  # noqa: E402
import app as flaskapp  # noqa: E402

assert db.DB_PATH == TEST_DB, "app.py hat die Test-Datenbank umgebogen!"

KONTO = "vorhanden@example.org"
ERFUNDEN = "gibtesnicht@example.org"
START_PW = "erstes-Passwort-2026"
IP_A = "203.0.113.5"
IP_B = "198.51.100.11"

USER_ID = db.create_user(KONTO, START_PW)

BASIS_THREADS = threading.active_count()

fehler: list[str] = []
versandt: list[dict] = []   # Attrappe: was waere rausgegangen
versand_fehler = False      # schaltet die Attrappe auf Fehlschlag


# ---------------------------------------------------------------------------
# Attrappe statt echtem Versand
# ---------------------------------------------------------------------------
def _attrappe(recipient: str, subject: str, text: str) -> str:
    if versand_fehler:
        raise mailer.MailError("Anmeldung am Mailserver abgelehnt (SMTP 535)")
    versandt.append({"to": recipient, "subject": subject, "text": text})
    return "msg_%03d" % len(versandt)


_echte_pruefung = mailer.is_configured   # fuer die Gegenprobe in Block 6
mailer.send = _attrappe
_MAIL_AN = True
mailer.is_configured = lambda: _MAIL_AN


def _mit_mail(an: bool) -> None:
    global _MAIL_AN
    _MAIL_AN = an


# ---------------------------------------------------------------------------
# Hilfen
# ---------------------------------------------------------------------------
def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def ruhe(sekunden: float = 5.0) -> bool:
    """Wartet, bis kein Versand-Thread mehr laeuft.

    Ohne das faelscht ein noch laufender Thread aus dem vorigen Block die
    naechste Messung (er schreibt in dieselbe Datenbank) — das ist ein
    Artefakt des Tests, nicht des Produktivpfads.
    """
    ende = time.perf_counter() + sekunden
    while threading.active_count() > BASIS_THREADS and time.perf_counter() < ende:
        time.sleep(0.005)
    return threading.active_count() <= BASIS_THREADS


def _leeren() -> None:
    """Bremse, Protokoll und offene Tickets zuruecksetzen."""
    ruhe()
    with sqlite3.connect(TEST_DB) as c:
        c.execute("DELETE FROM login_attempts")
        c.execute("DELETE FROM mail_log")
        c.execute("DELETE FROM password_resets")
    versandt.clear()


def anfordern(email: str, ip: str = IP_A, https: bool = False, prefix: str = ""):
    """Ein „Passwort vergessen" absetzen. Gibt die Antwort zurueck."""
    kopf = {}
    umgebung = {"REMOTE_ADDR": ip}
    if https:
        # Wie hinter nginx: die Verbindung kommt vom Proxy (privates Netz),
        # erst dann wertet _client_ip/PrefixMiddleware die Header aus.
        umgebung = {"REMOTE_ADDR": "172.18.0.1"}
        kopf["X-Forwarded-Proto"] = "https"
        kopf["X-Real-IP"] = ip
    if prefix:
        kopf["X-Script-Name"] = prefix
    with flaskapp.app.test_client() as client:
        return client.post(
            "/login",
            data={"action": "forgot", "email": email},
            headers=kopf,
            environ_base=umgebung,
        )


def warte_auf(bedingung, sekunden: float = 5.0) -> bool:
    """Wartet, bis der Hintergrund-Thread fertig ist (oder die Zeit ablaeuft)."""
    ende = time.perf_counter() + sekunden
    while time.perf_counter() < ende:
        if bedingung():
            return True
        time.sleep(0.01)
    return bedingung()


def offene_tokens() -> int:
    with sqlite3.connect(TEST_DB) as c:
        return c.execute(
            "SELECT COUNT(*) FROM password_resets WHERE token_hash IS NOT NULL"
        ).fetchone()[0]


# ---------------------------------------------------------------------------
print("\n1. Bekannte Adresse: Token, Mail und gueltiger Link")
# ---------------------------------------------------------------------------
_leeren()
_mit_mail(True)
antwort = anfordern(KONTO)
pruefe(antwort.status_code == 200, "Anmeldeseite antwortet mit 200")
pruefe(warte_auf(lambda: len(versandt) == 1), "genau eine Mail waere rausgegangen")
if versandt:
    text = versandt[0]["text"]
    pruefe(versandt[0]["to"] == KONTO, "Empfaenger ist die angefragte Adresse")
    pruefe("passwort-zuruecksetzen/" in text, "der Link steht in der Mail")
    pruefe("24" in text, "Hinweis auf 24 Stunden Gueltigkeit")
    pruefe(offene_tokens() == 1, "genau ein Token wurde erzeugt")

    marke = "/passwort-zuruecksetzen/"
    token = text.split(marke, 1)[1].split()[0].strip()
    with flaskapp.app.test_client() as client:
        seite = client.get(f"/passwort-zuruecksetzen/{token}")
        pruefe(seite.status_code == 200, "der Link aus der Mail oeffnet die Seite")
        neu = client.post(
            f"/passwort-zuruecksetzen/{token}",
            data={"password": "zweites-Passwort-2026",
                  "password2": "zweites-Passwort-2026"},
        )
        pruefe(neu.status_code in (200, 302), "neues Passwort laesst sich setzen")
    pruefe(db.verify_user(KONTO, "zweites-Passwort-2026") == USER_ID,
           "Anmeldung mit dem neuen Passwort gelingt")
    pruefe(db.verify_user(KONTO, START_PW) is None, "altes Passwort gilt nicht mehr")
    db.set_password(USER_ID, START_PW)  # fuer die folgenden Bloecke

protokoll = db.list_mail_log()
pruefe(len(protokoll) == 1 and protokoll[0]["status"] == "sent",
       "Protokoll vermerkt den Versand als erfolgreich")
pruefe(bool(protokoll and protokoll[0]["message_id"]),
       "die Nachrichtenkennung des Dienstes steht im Protokoll")

# ---------------------------------------------------------------------------
print("\n2. Erfundene Adresse: kein Token, keine Mail, gleiche Seite")
# ---------------------------------------------------------------------------
_leeren()
antwort_bekannt = anfordern(KONTO)
warte_auf(lambda: len(db.list_mail_log()) == 1)
ruhe()
seite_bekannt = antwort_bekannt.get_data(as_text=True)

_leeren()
antwort_unbekannt = anfordern(ERFUNDEN)
ruhe()
pruefe(not versandt, "an die erfundene Adresse geht keine Mail")
pruefe(offene_tokens() == 0, "fuer die erfundene Adresse entsteht kein Token")
pruefe(db.list_mail_log() == [], "kein Protokolleintrag fuer die erfundene Adresse")
seite_unbekannt = antwort_unbekannt.get_data(as_text=True)
pruefe(antwort_bekannt.status_code == antwort_unbekannt.status_code,
       "gleicher HTTP-Status in beiden Faellen")
pruefe(seite_bekannt == seite_unbekannt,
       "die ausgelieferte Seite ist Zeichen fuer Zeichen dieselbe")

# ---------------------------------------------------------------------------
print("\n3. Antwortzeit verraet die Existenz des Kontos nicht")
# ---------------------------------------------------------------------------
_leeren()
# Die Bremse zaehlt je Adresse; fuer die Messung wird sie zwischendurch geleert.
RUNDEN = 20


def _messe(email: str) -> float:
    ruhe()  # keine fremde Hintergrundarbeit waehrend der Messung
    with sqlite3.connect(TEST_DB) as c:
        c.execute("DELETE FROM login_attempts")
    start = time.perf_counter()
    anfordern(email)
    return (time.perf_counter() - start) * 1000


zeiten_bekannt: list[float] = []
zeiten_unbekannt: list[float] = []
for _ in range(RUNDEN):
    zeiten_bekannt.append(_messe(KONTO))
    zeiten_unbekannt.append(_messe(ERFUNDEN))
ruhe(10)

m_bekannt = statistics.median(zeiten_bekannt)
m_unbekannt = statistics.median(zeiten_unbekannt)
faktor = max(m_bekannt, m_unbekannt) / max(0.001, min(m_bekannt, m_unbekannt))
print(f"    bekannt:   Median {m_bekannt:6.1f} ms  "
      f"(min {min(zeiten_bekannt):.1f} / max {max(zeiten_bekannt):.1f})")
print(f"    erfunden:  Median {m_unbekannt:6.1f} ms  "
      f"(min {min(zeiten_unbekannt):.1f} / max {max(zeiten_unbekannt):.1f})")
print(f"    Faktor:    {faktor:.2f}")
pruefe(faktor < 1.35, "beide Pfade brauchen praktisch gleich lang (Faktor < 1,35)")

# ---------------------------------------------------------------------------
print("\n4. Bremse gegen Mail-Fluten")
# ---------------------------------------------------------------------------
_leeren()
erlaubt = db.RESET_MAIL_MAX_PER_ADDRESS
for i in range(erlaubt):
    anfordern(KONTO)
warte_auf(lambda: len(versandt) == erlaubt)
pruefe(len(versandt) == erlaubt,
       f"die ersten {erlaubt} Anfragen loesen je eine Mail aus")

abgewiesen = anfordern(KONTO)
ruhe()
pruefe(abgewiesen.status_code == 429, "die naechste Anfrage wird mit 429 abgewiesen")
pruefe(len(versandt) == erlaubt, "und loest keine weitere Mail aus")

# Zweites Konto, andere Adresse und andere IP — kommt weiter durch.
zweit_mail = "zweiter@example.org"
db.create_user(zweit_mail, "drittes-Passwort-2026")
anfordern(zweit_mail, ip=IP_B)
pruefe(warte_auf(lambda: len(versandt) == erlaubt + 1),
       "ein anderer Nutzer von anderer Adresse kommt weiterhin durch")

# IP-Deckel: viele verschiedene Adressen von derselben Quelle.
_leeren()
for i in range(db.RESET_MAIL_MAX_PER_IP):
    anfordern(f"fremd{i}@example.org", ip=IP_B)
ip_gesperrt = anfordern("noch-einer@example.org", ip=IP_B)
pruefe(ip_gesperrt.status_code == 429,
       f"nach {db.RESET_MAIL_MAX_PER_IP} Anfragen ist auch die Quell-IP gedeckelt")
pruefe(anfordern(KONTO, ip=IP_A).status_code == 200,
       "eine andere Quell-IP ist davon nicht betroffen")

# ---------------------------------------------------------------------------
print("\n5. Der Link stimmt hinter dem Proxy (https und /esg)")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO, https=True, prefix="/esg")
pruefe(warte_auf(lambda: len(versandt) == 1), "Mail wuerde rausgehen")
if versandt:
    zeile = [z for z in versandt[0]["text"].splitlines() if "passwort" in z][0].strip()
    print(f"    Link: {zeile[:60]}…")
    pruefe(zeile.startswith("https://"), "der Link beginnt mit https")
    pruefe("/esg/passwort-zuruecksetzen/" in zeile, "der Pfad traegt den /esg-Prefix")

_leeren()
anfordern(KONTO, https=True, prefix="/regulierungs-check")
warte_auf(lambda: len(versandt) == 1)
if versandt:
    zeile = [z for z in versandt[0]["text"].splitlines() if "passwort" in z][0].strip()
    pruefe("/regulierungs-check/passwort-zuruecksetzen/" in zeile,
           "unter der Legacy-Domain traegt der Link deren Prefix")

# ---------------------------------------------------------------------------
print("\n6. Ohne Zugangsdaten: Anwendung laeuft, Ticket beim Admin")
# ---------------------------------------------------------------------------
_leeren()
_mit_mail(False)
ohne = anfordern(KONTO)
ruhe()
pruefe(ohne.status_code == 200, "die Anmeldeseite antwortet weiterhin mit 200")
pruefe(not versandt, "es wird nichts versendet")
pruefe(offene_tokens() == 0, "es wird kein Token auf Vorrat erzeugt")
offen = db.list_open_resets()
pruefe(len(offen) == 1 and offen[0]["email"] == KONTO,
       "die Anfrage liegt als Ticket unter /admin/passwort-resets")
pruefe(db.list_mail_log() == [], "das Protokoll bleibt leer")
_mit_mail(True)

# Gegenprobe mit dem echten (nicht konfigurierten) mailer:
pruefe(_echte_pruefung() is False,
       "ohne Umgebungsvariablen meldet der Mailer keinen Zugang")

# ---------------------------------------------------------------------------
print("\n7. Versandfehler: Nutzer sieht dasselbe, Admin sieht den Fehler")
# ---------------------------------------------------------------------------
_leeren()
versand_fehler = True
kaputt = anfordern(KONTO)
pruefe(warte_auf(lambda: db.list_mail_log() != []), "der Fehlschlag wird protokolliert")
eintrag = (db.list_mail_log() or [{}])[0]
pruefe(eintrag.get("status") == "failed", "Status im Protokoll ist 'failed'")
pruefe("535" in (eintrag.get("error") or ""), "der Grund steht beim Eintrag")
pruefe(kaputt.get_data(as_text=True) == seite_bekannt,
       "der Nutzer bekommt dieselbe neutrale Seite wie im Erfolgsfall")
versand_fehler = False

# ---------------------------------------------------------------------------
print("\n8. Weder Token noch Link landen im Protokoll")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
warte_auf(lambda: len(versandt) == 1)
token = versandt[0]["text"].split("/passwort-zuruecksetzen/", 1)[1].split()[0].strip()
with sqlite3.connect(TEST_DB) as c:
    inhalt = " ".join(
        str(wert)
        for zeile in c.execute("SELECT * FROM mail_log").fetchall()
        for wert in zeile
    )
    hash_zeilen = c.execute(
        "SELECT token_hash FROM password_resets WHERE token_hash IS NOT NULL"
    ).fetchall()
pruefe(token not in inhalt, "der Token steht nirgends im Protokoll")
pruefe("passwort-zuruecksetzen" not in inhalt, "auch der Link steht nicht darin")
pruefe(all(z[0] != token for z in hash_zeilen),
       "in password_resets liegt nur der Hash, nicht der Token")

# ---------------------------------------------------------------------------
print("\n9. Die Admin-Seite zeigt das Zustellprotokoll")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
warte_auf(lambda: len(db.list_mail_log()) == 1)
admin_mail = sorted(flaskapp.ADMIN_EMAILS)[0]
if not db.email_exists(admin_mail):
    db.create_user(admin_mail, "admin-Passwort-2026")
with flaskapp.app.test_client() as client:
    with client.session_transaction() as sitzung:
        sitzung["user_id"] = db.get_user_by_email(admin_mail)["id"]
        sitzung["user_email"] = admin_mail
    seite = client.get("/admin/passwort-resets")
    inhalt = seite.get_data(as_text=True)
pruefe(seite.status_code == 200, "die Admin-Seite laedt")
pruefe("Mailversand" in inhalt, "der Abschnitt Mailversand ist da")
pruefe("versendet" in inhalt, "der Zustand des Versands steht darin")
pruefe(KONTO in inhalt, "der Empfaenger ist genannt")
pruefe("passwort-zuruecksetzen" not in inhalt.split("Mailversand", 1)[1],
       "im Protokollabschnitt steht kein Link")

# ---------------------------------------------------------------------------
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  - " + f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
