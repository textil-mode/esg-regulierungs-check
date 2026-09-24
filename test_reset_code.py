"""Tests fuer den Passwort-Reset per sechsstelligem Zahlencode.

Laeuft ausschliesslich gegen eine eigene Datenbank (`data/esg_code_test.db`),
die zu Beginn frisch angelegt wird — `data/esg.db` wird nie beruehrt.
**Kein Netz, keine echte Mail:** `mailer.send` wird durch eine Attrappe
ersetzt, die nur mitschreibt.

Aufruf:  ./.venv/Scripts/python.exe test_reset_code.py
"""
from __future__ import annotations

import os
import re
import sqlite3
import statistics
import sys
import threading
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_code_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for _v in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
           "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_v] = ""
os.environ["PUBLIC_BASE_URL"] = "https://test.example"

import db  # noqa: E402

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH} statt auf die Kopie!"
db.init_db()

import mailer  # noqa: E402
import app as flaskapp  # noqa: E402

KONTO = "vorhanden@example.org"
ERFUNDEN = "gibtesnicht@example.org"
START_PW = "erstes-Passwort-2026"
NEU_PW = "zweites-Passwort-2026"
IP_A = "203.0.113.5"

USER_ID = db.create_user(KONTO, START_PW)
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


def anfordern(email: str, ip: str = IP_A):
    with flaskapp.app.test_client() as client:
        return client.post("/login", data={"action": "forgot", "email": email},
                           environ_base={"REMOTE_ADDR": ip})


def code_aus_mail() -> str:
    treffer = re.search(r"\b(\d{6})\b", versandt[-1]["text"])
    return treffer.group(1) if treffer else ""


def einloesen(email: str, code: str, pw: str = NEU_PW, pw2: str | None = None,
              ip: str = IP_A):
    with flaskapp.app.test_client() as client:
        return client.post(
            "/passwort-neu",
            data={"email": email, "code": code, "password": pw,
                  "password2": pw if pw2 is None else pw2},
            environ_base={"REMOTE_ADDR": ip},
        )


# ---------------------------------------------------------------------------
print("\n1. Der gewoehnliche Weg: Code anfordern, Passwort setzen")
# ---------------------------------------------------------------------------
_leeren()
antwort = anfordern(KONTO)
pruefe(antwort.status_code in (302, 303), "Weiterleitung auf die Code-Eingabe")
pruefe("/passwort-neu" in (antwort.headers.get("Location") or ""),
       "und zwar auf /passwort-neu")
pruefe(ruhe() and len(versandt) == 1, "genau eine Mail waere rausgegangen")
if versandt:
    text = versandt[0]["text"]
    code = code_aus_mail()
    pruefe(bool(code), f"ein sechsstelliger Code steht darin ({code[:2]}…)")
    pruefe("http" not in text,
           "KEIN Link in der Mail — genau darum geht es")
    pruefe("30" in text, "Hinweis auf 30 Minuten Gueltigkeit")

    gesetzt = einloesen(KONTO, code)
    pruefe(gesetzt.status_code in (302, 303), "das Setzen leitet weiter")
    pruefe(db.verify_user(KONTO, NEU_PW) == USER_ID,
           "Anmeldung mit dem neuen Passwort gelingt")
    pruefe(db.verify_user(KONTO, START_PW) is None, "altes Passwort gilt nicht mehr")
    db.set_password(USER_ID, START_PW)

# ---------------------------------------------------------------------------
print("\n2. Derselbe Code laesst sich kein zweites Mal verwenden")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
ruhe()
code = code_aus_mail()
einloesen(KONTO, code)
db.set_password(USER_ID, START_PW)
nochmal = einloesen(KONTO, code, pw="drittes-Passwort-2026")
pruefe(nochmal.status_code == 200, "der zweite Versuch bleibt auf der Seite")
pruefe(db.verify_user(KONTO, "drittes-Passwort-2026") is None,
       "und setzt kein Passwort")

# ---------------------------------------------------------------------------
print("\n3. Ein neuer Code entwertet den alten")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
ruhe()
alt = code_aus_mail()
anfordern(KONTO)
ruhe()
neu = code_aus_mail()
pruefe(alt != neu, "der zweite Code ist ein anderer")
einloesen(KONTO, alt, pw="viertes-Passwort-2026")
pruefe(db.verify_user(KONTO, "viertes-Passwort-2026") is None,
       "der alte Code greift nicht mehr")
einloesen(KONTO, neu, pw="fuenftes-Passwort-2026")
pruefe(db.verify_user(KONTO, "fuenftes-Passwort-2026") == USER_ID,
       "der neue Code greift")
db.set_password(USER_ID, START_PW)

# ---------------------------------------------------------------------------
print("\n4. Durchprobieren: nach fuenf Fehlversuchen ist der Code tot")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
ruhe()
echt = code_aus_mail()
falsch = "000000" if echt != "000000" else "111111"
for i in range(db.CODE_MAX_ATTEMPTS):
    einloesen(KONTO, falsch, pw="raten-Passwort-2026")
pruefe(db.verify_user(KONTO, "raten-Passwort-2026") is None,
       f"{db.CODE_MAX_ATTEMPTS} Fehlversuche setzen kein Passwort")
danach = einloesen(KONTO, echt, pw="zu-spaet-Passwort-2026")
pruefe(db.verify_user(KONTO, "zu-spaet-Passwort-2026") is None,
       "auch der RICHTIGE Code greift danach nicht mehr")
pruefe(danach.status_code == 200, "die Seite bleibt bedienbar")

# ---------------------------------------------------------------------------
print("\n5. Ein abgelaufener Code greift nicht")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
ruhe()
code = code_aus_mail()
with sqlite3.connect(TEST_DB) as c:
    c.execute("UPDATE reset_codes SET expires_at = '2020-01-01T00:00:00' "
              "WHERE used_at IS NULL")
einloesen(KONTO, code, pw="abgelaufen-Passwort-2026")
pruefe(db.verify_user(KONTO, "abgelaufen-Passwort-2026") is None,
       "nach Ablauf wird kein Passwort gesetzt")

# ---------------------------------------------------------------------------
print("\n6. Ein Code gilt nur fuer SEIN Konto")
# ---------------------------------------------------------------------------
_leeren()
ZWEITER = "zweiter@example.org"
zweite_id = db.create_user(ZWEITER, START_PW)
anfordern(KONTO)
ruhe()
code_konto1 = code_aus_mail()
einloesen(ZWEITER, code_konto1, pw="fremd-Passwort-2026")
pruefe(db.verify_user(ZWEITER, "fremd-Passwort-2026") is None,
       "der Code des einen Kontos setzt beim anderen nichts")
pruefe(db.verify_user(ZWEITER, START_PW) == zweite_id,
       "dessen Passwort ist unveraendert")

# ---------------------------------------------------------------------------
print("\n7. Erfundene Adresse: kein Code, keine Mail, gleiche Antwort")
# ---------------------------------------------------------------------------
def _codes_gesamt() -> int:
    with sqlite3.connect(TEST_DB) as c:
        return c.execute("SELECT COUNT(*) FROM reset_codes").fetchone()[0]


_leeren()
a = anfordern(KONTO)
ruhe()
mails_bekannt = len(versandt)
_leeren()
vorher = _codes_gesamt()
b = anfordern(ERFUNDEN)
ruhe()
pruefe(a.status_code == b.status_code,
       f"gleicher HTTP-Status ({a.status_code})")
pruefe((a.headers.get("Location") or "") == (b.headers.get("Location") or ""),
       "gleiches Ziel der Weiterleitung")
pruefe(mails_bekannt == 1 and not versandt,
       "fuer die erfundene Adresse geht nichts raus")
# Gemessen wird die Veraenderung: offene Codes der bekannten Adresse aus den
# Bloecken davor duerfen das Ergebnis nicht faelschen.
pruefe(_codes_gesamt() == vorher, "und es entsteht kein Code auf Vorrat")

# ---------------------------------------------------------------------------
print("\n8. Die Antwortzeit verraet die Existenz des Kontos nicht")
# ---------------------------------------------------------------------------
_leeren()


def _messe(email: str, runden: int = 7) -> float:
    zeiten = []
    for i in range(runden):
        with sqlite3.connect(TEST_DB) as c:
            c.execute("DELETE FROM login_attempts")
        start = time.perf_counter()
        anfordern(email, ip=f"198.51.100.{i + 30}")
        zeiten.append((time.perf_counter() - start) * 1000)
        ruhe()
    return statistics.median(zeiten)


m_bekannt = _messe(KONTO)
m_unbekannt = _messe(ERFUNDEN)
faktor = max(m_bekannt, m_unbekannt) / max(min(m_bekannt, m_unbekannt), 0.001)
print(f"    bekannt:   Median {m_bekannt:6.1f} ms")
print(f"    erfunden:  Median {m_unbekannt:6.1f} ms")
print(f"    Faktor:    {faktor:.2f}")
pruefe(faktor < 1.35, "beide Pfade brauchen praktisch gleich lang (Faktor < 1,35)")

# ---------------------------------------------------------------------------
print("\n9. Weder Code noch Passwort landen im Protokoll")
# ---------------------------------------------------------------------------
_leeren()
anfordern(KONTO)
ruhe()
code = code_aus_mail()
einloesen(KONTO, code, pw="protokoll-Passwort-2026")
ruhe()
protokoll = db.list_mail_log()
als_text = repr(protokoll)
pruefe(code not in als_text, "der Code steht nirgends im Protokoll")
pruefe("protokoll-Passwort-2026" not in als_text, "das Passwort ebenso wenig")
with sqlite3.connect(TEST_DB) as c:
    roh = repr(c.execute("SELECT * FROM reset_codes").fetchall())
pruefe(code not in roh, "auch in der Tabelle steht nur der Hash")
db.set_password(USER_ID, START_PW)

# ---------------------------------------------------------------------------
print("\n10. Bremse gegen Mail-Fluten wirkt weiterhin")
# ---------------------------------------------------------------------------
_leeren()
IP_FLUT = "192.0.2.99"
durch = 0
for i in range(db.RESET_MAIL_MAX_PER_ADDRESS):
    if anfordern(KONTO, ip=IP_FLUT).status_code in (302, 303):
        durch += 1
ruhe()
pruefe(durch == db.RESET_MAIL_MAX_PER_ADDRESS,
       f"die ersten {db.RESET_MAIL_MAX_PER_ADDRESS} Anfragen gehen durch")
zu_viel = anfordern(KONTO, ip=IP_FLUT)
pruefe(zu_viel.status_code == 429, "die naechste wird mit 429 abgewiesen")

# ---------------------------------------------------------------------------
print("\n11. Ohne Postfach: alles wie bisher (Ticket beim Admin)")
# ---------------------------------------------------------------------------
_leeren()
mailer.is_configured = lambda: False
ohne = anfordern(KONTO, ip="203.0.113.77")
ruhe()
pruefe(ohne.status_code == 200, "die Anmeldeseite antwortet mit 200")
pruefe(not versandt, "es geht nichts raus")
offen = db.list_open_resets()
pruefe(any(o["email"] == KONTO for o in offen),
       "die Anfrage liegt als Ticket beim Admin")
mailer.is_configured = lambda: True

# ---------------------------------------------------------------------------
print("\n12. Der Admin-Weg mit Einmal-Link besteht weiter")
# ---------------------------------------------------------------------------
# Er ist die Rueckfallebene, wenn der Mailversand klemmt — der Admin erzeugt
# den Link und gibt ihn persoenlich weiter. Diese Pruefungen standen frueher
# in test_reset_mail.py, das mit dem Mail-Link entfallen ist.
_leeren()
token, ablauf = db.issue_reset_token(USER_ID)
pruefe(len(token) > 30, "der Token ist lang und zufaellig")
nutzer = db.user_for_reset_token(token)
pruefe(nutzer is not None and nutzer["email"] == KONTO,
       "der Token gehoert zum richtigen Konto")
with flaskapp.app.test_client() as client:
    seite = client.get(f"/passwort-zuruecksetzen/{token}")
    pruefe(seite.status_code == 200, "der Link oeffnet die Seite")
    gesetzt = client.post(f"/passwort-zuruecksetzen/{token}",
                          data={"password": "adminweg-Passwort-2026",
                                "password2": "adminweg-Passwort-2026"})
    pruefe(gesetzt.status_code in (200, 302), "das Passwort laesst sich setzen")
pruefe(db.verify_user(KONTO, "adminweg-Passwort-2026") == USER_ID,
       "und gilt danach")
pruefe(db.user_for_reset_token(token) is None,
       "der Token ist danach verbraucht")
with sqlite3.connect(TEST_DB) as c:
    roh = repr(c.execute("SELECT * FROM password_resets").fetchall())
pruefe(token not in roh, "gespeichert ist nur der Hash, nicht der Token")
db.set_password(USER_ID, START_PW)

# ---------------------------------------------------------------------------
ruhe()
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
