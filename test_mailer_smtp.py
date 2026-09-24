"""Tests fuer den SMTP-Versandweg in mailer.py.

**Es geht keine echte Mail raus.** `smtplib.SMTP` wird durch ein Doppel
ersetzt, das nur mitschreibt; fuer die Zeitgrenze laeuft ein stummer
TCP-Server auf 127.0.0.1, der nie ein Banner schickt. Keine Zugangsdaten,
kein Kontakt zu Hostinger.

Aufruf:  ./.venv/Scripts/python.exe test_mailer_smtp.py
"""
from __future__ import annotations

import os
import smtplib
import socket
import ssl
import sys
import threading
import time
from email.header import decode_header, make_header

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

# Kein echter Zugang aus der Umgebung/.env in den Test.
for _var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
             "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ.pop(_var, None)

import mailer  # noqa: E402

fehler: list[str] = []

PASSWORT = "Attrappen-Passwort-nicht-echt"
ZUGANG = {
    "SMTP_HOST": "smtp.example.invalid",
    "SMTP_PORT": "587",
    "SMTP_USER": "noreply@example.invalid",
    "SMTP_PASSWORD": PASSWORT,
    "MAIL_FROM": "noreply@example.invalid",
    "MAIL_FROM_NAME": "ESG-Regulierungs-Check",
}


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def setze_zugang(**abweichung: str | None) -> None:
    werte = dict(ZUGANG)
    werte.update(abweichung)
    for name, wert in werte.items():
        if wert is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = wert


# ---------------------------------------------------------------------------
# Doppel statt echtem smtplib.SMTP
# ---------------------------------------------------------------------------
class SmtpDoppel:
    """Schreibt mit, was der Mailer tut. Klassenweit, damit der Test es sieht."""

    protokoll: list[tuple] = []
    kann_starttls = True
    fehler_bei: dict[str, Exception] = {}
    letzte_nachricht = None

    def __init__(self, host, port, timeout=None):
        SmtpDoppel.protokoll.append(("connect", host, port, timeout))

    def __enter__(self):
        return self

    def __exit__(self, *_):
        SmtpDoppel.protokoll.append(("quit",))
        return False

    def _vielleicht_fehler(self, schritt: str) -> None:
        exc = SmtpDoppel.fehler_bei.get(schritt)
        if exc is not None:
            raise exc

    def ehlo(self):
        SmtpDoppel.protokoll.append(("ehlo",))

    def has_extn(self, name):
        SmtpDoppel.protokoll.append(("has_extn", name))
        return SmtpDoppel.kann_starttls

    def starttls(self, context=None):
        SmtpDoppel.protokoll.append(("starttls", context))
        self._vielleicht_fehler("starttls")

    def login(self, user, password):
        SmtpDoppel.protokoll.append(("login", user, password))
        self._vielleicht_fehler("login")

    def send_message(self, nachricht):
        SmtpDoppel.protokoll.append(("send_message",))
        SmtpDoppel.letzte_nachricht = nachricht
        self._vielleicht_fehler("send_message")


def mit_doppel(**einstellung):
    SmtpDoppel.protokoll = []
    SmtpDoppel.kann_starttls = einstellung.get("kann_starttls", True)
    SmtpDoppel.fehler_bei = einstellung.get("fehler_bei", {})
    SmtpDoppel.letzte_nachricht = None
    mailer.smtplib.SMTP = SmtpDoppel


_ECHTES_SMTP = smtplib.SMTP

BETREFF = "ESG-Regulierungs-Check: Passwort zurücksetzen"
TEXT = ("Guten Tag,\n\nüber den folgenden Link können Sie ein neues Passwort "
        "setzen:\n\nhttps://ki-textil-mode.de/esg/passwort-zuruecksetzen/abc\n\n"
        "Der Link gilt 24 Stunden. Größe, Prüfung, Änderung – öäüßÖÄÜ.\n")

# ---------------------------------------------------------------------------
print("\n1. is_configured() prueft den vollstaendigen Zugang")
# ---------------------------------------------------------------------------
setze_zugang(SMTP_HOST=None, SMTP_USER=None, SMTP_PASSWORD=None, MAIL_FROM=None,
             SMTP_PORT=None, MAIL_FROM_NAME=None)
pruefe(mailer.is_configured() is False, "ohne Variablen: nicht konfiguriert")
for fehlend in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM"):
    setze_zugang(**{fehlend: None})
    pruefe(mailer.is_configured() is False, f"ohne {fehlend}: nicht konfiguriert")
setze_zugang()
pruefe(mailer.is_configured() is True, "mit allen Pflichtwerten: konfiguriert")
setze_zugang(SMTP_PORT=None)
pruefe(mailer._config()["port"] == 587, "ohne SMTP_PORT gilt 587")
setze_zugang(SMTP_PORT="unsinn")
pruefe(mailer._config()["port"] == 587, "bei unbrauchbarem SMTP_PORT gilt 587")
setze_zugang(SMTP_PORT="2525")
pruefe(mailer._config()["port"] == 2525, "SMTP_PORT wird uebernommen")
setze_zugang()

# ---------------------------------------------------------------------------
print("\n2. Verbindungsweg: STARTTLS mit Zertifikatspruefung, dann Anmeldung")
# ---------------------------------------------------------------------------
mit_doppel()
kennung = mailer.send("empfaenger@example.org", BETREFF, TEXT)
schritte = [z[0] for z in SmtpDoppel.protokoll]
print("    Ablauf:", " -> ".join(schritte))
pruefe(schritte == ["connect", "ehlo", "has_extn", "starttls", "ehlo",
                    "login", "send_message", "quit"],
       "Reihenfolge: EHLO, STARTTLS, EHLO, LOGIN, Nachricht")

verbindung = SmtpDoppel.protokoll[0]
pruefe(verbindung[1] == "smtp.example.invalid" and verbindung[2] == 587,
       "Verbindung geht an SMTP_HOST:SMTP_PORT")
pruefe(verbindung[3] == mailer.TIMEOUT_SEC and 0 < mailer.TIMEOUT_SEC <= 30,
       f"Zeitgrenze {mailer.TIMEOUT_SEC} s wird an smtplib durchgereicht")

kontext = [z for z in SmtpDoppel.protokoll if z[0] == "starttls"][0][1]
pruefe(isinstance(kontext, ssl.SSLContext), "STARTTLS bekommt einen SSL-Kontext")
pruefe(kontext.verify_mode == ssl.CERT_REQUIRED, "Zertifikat wird verlangt")
pruefe(kontext.check_hostname is True, "der Hostname wird geprueft")

anmeldung = [z for z in SmtpDoppel.protokoll if z[0] == "login"][0]
pruefe(anmeldung[1] == ZUGANG["SMTP_USER"] and anmeldung[2] == PASSWORT,
       "Anmeldung mit SMTP_USER und SMTP_PASSWORD")
pruefe(bool(kennung) and kennung.startswith("<") and kennung.endswith(">"),
       f"Rueckgabe ist eine Message-ID ({kennung})")

# ---------------------------------------------------------------------------
print("\n3. Ohne STARTTLS wird nicht versendet")
# ---------------------------------------------------------------------------
mit_doppel(kann_starttls=False)
try:
    mailer.send("empfaenger@example.org", BETREFF, TEXT)
    pruefe(False, "Versand ohne STARTTLS bricht ab")
except mailer.MailError as exc:
    pruefe("STARTTLS" in str(exc), f"Versand bricht ab: {exc}")
schritte = [z[0] for z in SmtpDoppel.protokoll]
pruefe("login" not in schritte and "send_message" not in schritte,
       "weder Anmeldung noch Nachricht gehen unverschluesselt raus")

# ---------------------------------------------------------------------------
print("\n4. Kopfzeilen und Umlaute")
# ---------------------------------------------------------------------------
mit_doppel()
mailer.send("empfaenger@example.org", BETREFF, TEXT)
nachricht = SmtpDoppel.letzte_nachricht
roh = nachricht.as_bytes()

pruefe(nachricht["From"] == '"ESG-Regulierungs-Check" <noreply@example.invalid>'
       or nachricht["From"] == 'ESG-Regulierungs-Check <noreply@example.invalid>',
       f"Absender: {nachricht['From']}")
pruefe(nachricht["To"] == "empfaenger@example.org", "Empfaenger steht im To-Feld")
pruefe("Reply-To" not in nachricht, "kein ueberfluessiges Reply-To")
pruefe(nachricht.get_content_type() == "text/plain", "reiner Text, kein HTML")

betreff_zeile = [z for z in roh.decode("ascii", "replace").splitlines()
                 if z.startswith("Subject:")][0]
print("    Betreff auf der Leitung:", betreff_zeile)
pruefe(all(b < 128 for b in betreff_zeile.encode("ascii", "replace")),
       "der Betreff geht 7-bit-sauber ueber die Leitung (RFC 2047)")
zurueck = str(make_header(decode_header(nachricht["Subject"])))
pruefe(zurueck == BETREFF, f"zurueckdekodiert ergibt er wieder: {zurueck}")

pruefe(nachricht.get_content_charset() == "utf-8", "der Text ist als UTF-8 deklariert")
inhalt = nachricht.get_content()
pruefe(inhalt.rstrip("\n") == TEXT.rstrip("\n"),
       "der Text kommt Zeichen fuer Zeichen wieder heraus (öäüß, Größe, –)")
pruefe("öäü".encode("utf-8") in roh or b"=C3=B6" in roh or b"w6TDtsO8" in roh,
       "die Umlaute liegen als UTF-8 in der Nachricht, nicht als Fragezeichen")
pruefe("?" not in inhalt, "kein Umlaut ist zu einem Fragezeichen geworden")

# ---------------------------------------------------------------------------
print("\n5. Fehler werden uebersetzt, nicht verschluckt")
# ---------------------------------------------------------------------------
faelle = [
    ("login", smtplib.SMTPAuthenticationError(535, b"5.7.8 auth failed"),
     "Anmeldung", "Anmeldung abgelehnt"),
    ("send_message", smtplib.SMTPRecipientsRefused(
        {"wer@example.org": (550, b"no such user")}),
     "Empfaenger abgelehnt", "Empfaenger abgelehnt"),
    ("send_message", smtplib.SMTPSenderRefused(
        553, b"sender rejected", "noreply@example.invalid"),
     "Absender abgelehnt", "Absender abgelehnt"),
    ("starttls", ConnectionResetError("connection reset by peer"),
     "nicht erreichbar", "Verbindung abgerissen"),
]
for schritt, exc, erwartet, beschreibung in faelle:
    mit_doppel(fehler_bei={schritt: exc})
    try:
        mailer.send("wer@example.org", BETREFF, TEXT)
        pruefe(False, f"{beschreibung}: Fehler wird gemeldet")
    except mailer.MailError as gemeldet:
        meldung = str(gemeldet)
        pruefe(erwartet in meldung, f"{beschreibung} -> \"{meldung}\"")
        pruefe(PASSWORT not in meldung and "zuruecksetzen" not in meldung,
               f"{beschreibung}: weder Passwort noch Link in der Meldung")

mit_doppel()
setze_zugang(SMTP_PASSWORD=None)
try:
    mailer.send("wer@example.org", BETREFF, TEXT)
    pruefe(False, "ohne Zugang wird gar nicht erst verbunden")
except mailer.MailError as exc:
    pruefe(not SmtpDoppel.protokoll, f"ohne Zugang keine Verbindung: {exc}")
setze_zugang()

# ---------------------------------------------------------------------------
print("\n6. Die Zeitgrenze greift wirklich (stummer Server auf 127.0.0.1)")
# ---------------------------------------------------------------------------
mailer.smtplib.SMTP = _ECHTES_SMTP  # hier soll das echte smtplib laufen

horcher = socket.socket()
horcher.bind(("127.0.0.1", 0))
horcher.listen(1)
stumm_port = horcher.getsockname()[1]
offen: list[socket.socket] = []


def _stumm():
    """Nimmt die Verbindung an und schweigt — kein 220-Banner."""
    try:
        verbindung, _ = horcher.accept()
        offen.append(verbindung)
        time.sleep(8)
    except OSError:
        pass


threading.Thread(target=_stumm, daemon=True).start()

alte_grenze = mailer.TIMEOUT_SEC
mailer.TIMEOUT_SEC = 1.0
setze_zugang(SMTP_HOST="127.0.0.1", SMTP_PORT=str(stumm_port))
start = time.perf_counter()
try:
    mailer.send("wer@example.org", BETREFF, TEXT)
    gedauert = time.perf_counter() - start
    pruefe(False, "der Versand bricht ab, statt zu haengen")
except mailer.MailError as exc:
    gedauert = time.perf_counter() - start
    print(f"    abgebrochen nach {gedauert:.2f} s: {exc}")
    pruefe(gedauert < 3.0,
           f"nach {gedauert:.2f} s abgebrochen (Grenze 1,0 s), nicht haengen geblieben")
    pruefe(isinstance(exc, mailer.MailError), "der Abbruch kommt als MailError heraus")
mailer.TIMEOUT_SEC = alte_grenze
setze_zugang()
for s in offen:
    s.close()
horcher.close()

# ---------------------------------------------------------------------------
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  - " + f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")

# ---------------------------------------------------------------------------
print("\nZusatz: Kein Oeffnungs- und Klick-Tracking (24.09.2026)")
# ---------------------------------------------------------------------------
# Brevo haengt sonst von sich aus einen Zaehl-Link an den Anfang der Mail.
import email as _email  # noqa: E402

_fang: list = []


class _FangSMTP:
    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def ehlo(self):
        return (250, b"ok")

    def has_extn(self, name):
        return True

    def starttls(self, context=None):
        return (220, b"ok")

    def login(self, user, pw):
        return (235, b"ok")

    def send_message(self, nachricht):
        _fang.append(nachricht)


_echtes_smtp = smtplib.SMTP
smtplib.SMTP = _FangSMTP
for _v, _w in (("SMTP_HOST", "mail.example"), ("SMTP_USER", "u"),
               ("SMTP_PASSWORD", "p"), ("MAIL_FROM", "noreply@example.org")):
    os.environ[_v] = _w
try:
    mailer.send("empfaenger@example.org", "Betreff", "Ihr Code lautet: 123456")
finally:
    smtplib.SMTP = _echtes_smtp

pruefe(len(_fang) == 1, "die Nachricht wurde uebergeben")
if _fang:
    kopf = {k.lower(): v for k, v in _fang[0].items()}
    pruefe(kopf.get("x-mailin-track") == "0",
           "der Kopf X-Mailin-Track: 0 ist gesetzt")
    pruefe("sendibt" not in _fang[0].get_content(),
           "im Text steht kein Zaehl-Link")

print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
