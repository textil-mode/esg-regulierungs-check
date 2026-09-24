"""Mailversand über SMTP — schlank, ohne Warteschlange.

Versendet wird über ein gewöhnliches Postfach (hier: Hostinger,
`noreply@ki-textil-mode.de`) mit `smtplib` aus der Standardbibliothek. Keine
zusätzliche Abhängigkeit, kein Dienstkonto, keine Gebühr für eigene
Absenderdomänen.

Verbindungsweg — bewusst nur dieser eine:

    SMTP auf Port 587  ->  EHLO  ->  STARTTLS (mit Zertifikatsprüfung)
                       ->  EHLO  ->  LOGIN  ->  Nachricht

Bietet der Server kein STARTTLS an, bricht der Versand ab. Es gibt **keinen**
Rückfall auf eine unverschlüsselte Verbindung: darin stünden Postfach-Passwort
und Reset-Link im Klartext auf der Leitung.

Warum hier **keine** Warteschlange mit Wiederholversuchen:

* Die ESG-Anwendung ist ein einzelner Flask-/Gunicorn-Prozess ohne Scheduler.
  Eine Warteschlange bräuchte erst einen Wecker, den es nicht gibt; sie würde
  faktisch nur beim nächsten Reset-Versuch abgearbeitet — also genau dann,
  wenn der Nutzer ohnehin schon einen frischen Link anfordert.
* Eine Warteschlange müsste den **fertigen Mailtext** speichern, und darin
  steht der Reset-Link im Klartext. Das widerspricht der Regel, dass vom Token
  nur der SHA-256-Hash in der Datenbank liegt.
* Der Link gilt 24 Stunden und ist beliebig oft neu anforderbar. Scheitert der
  Versand, ist der richtige Weg „noch einmal anfordern" oder der Admin-Weg
  unter /admin/passwort-resets — beides ist bereits da.

An SMTP ändert das nichts: der Versand ist synchron und dauert deshalb
merklich länger als ein HTTP-Aufruf. Genau darum läuft er im
Hintergrund-Thread (siehe `app._send_reset_mail`) und ist durch
`TIMEOUT_SEC` begrenzt — ohne Zeitgrenze bliebe ein Thread an einem stummen
Mailserver hängen. Es bleibt bei einem Versuch je Anforderung; das Ergebnis
wird protokolliert (`db.log_mail`), damit der Admin sieht, ob es geklappt hat.
"""
from __future__ import annotations

import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid

# Gilt für Verbindungsaufbau und jede einzelne Antwort des Servers. Der
# Versand läuft in einem Hintergrund-Thread, blockiert also keine Anfrage —
# kurz gehalten, damit bei einem stummen Server keine Threads auflaufen.
TIMEOUT_SEC = 15.0

STANDARD_PORT = 587
STANDARD_ANZEIGENAME = "ESG-Regulierungs-Check"


class MailError(RuntimeError):
    """Versand nicht möglich (nicht konfiguriert, Netz-, Anmelde- oder SMTP-Fehler)."""


def _config() -> dict[str, str | int]:
    def wert(name: str) -> str:
        return (os.getenv(name) or "").strip()

    port_roh = wert("SMTP_PORT")
    try:
        port = int(port_roh) if port_roh else STANDARD_PORT
    except ValueError:
        port = STANDARD_PORT

    return {
        "host": wert("SMTP_HOST"),
        "port": port,
        "user": wert("SMTP_USER"),
        "password": os.getenv("SMTP_PASSWORD") or "",
        "from": wert("MAIL_FROM"),
        "from_name": wert("MAIL_FROM_NAME") or STANDARD_ANZEIGENAME,
    }


def is_configured() -> bool:
    """Steht ein vollständiger Postfach-Zugang bereit? Sonst gilt der Admin-Weg."""
    c = _config()
    return bool(c["host"] and c["user"] and c["password"] and c["from"])


def _fehlertext(exc: Exception) -> str:
    """Übersetzt den SMTP-Fehler in einen Satz für das Admin-Protokoll.

    Nie durchgereicht werden Passwort oder Nachrichtentext; die Meldungen der
    Bibliothek nennen nur Antwortcodes und Adressen.
    """
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return f"Anmeldung am Mailserver abgelehnt (SMTP {exc.smtp_code})"
    if isinstance(exc, smtplib.SMTPRecipientsRefused):
        adressen = ", ".join(sorted(exc.recipients)) or "unbekannt"
        return f"Empfaenger abgelehnt: {adressen}"
    if isinstance(exc, smtplib.SMTPSenderRefused):
        return f"Absender abgelehnt (SMTP {exc.smtp_code})"
    if isinstance(exc, smtplib.SMTPNotSupportedError):
        return f"Mailserver unterstuetzt den Schritt nicht: {exc}"
    if isinstance(exc, ssl.SSLError):
        return f"TLS-Fehler: {exc.__class__.__name__}"
    if isinstance(exc, smtplib.SMTPException):
        return f"SMTP-Fehler: {exc.__class__.__name__}: {exc}"
    return f"Mailserver nicht erreichbar: {exc.__class__.__name__}: {exc}"


def send(recipient: str, subject: str, text: str) -> str | None:
    """Verschickt eine Nur-Text-Nachricht über SMTP mit STARTTLS.

    Gibt die selbst vergebene `Message-ID` zurück, damit der Versand im
    Protokoll und im Postausgang zusammenzubringen ist. Wirft `MailError` bei
    jedem Fehlschlag — der Aufrufer protokolliert ihn, zeigt ihn aber nie dem
    anfragenden Nutzer (sonst verriete die Meldung, dass es das Konto gibt).
    """
    c = _config()
    if not is_configured():
        raise MailError("SMTP ist nicht konfiguriert.")

    absender = str(c["from"])
    nachricht = EmailMessage()
    nachricht["From"] = formataddr((str(c["from_name"]), absender))
    nachricht["To"] = recipient
    nachricht["Subject"] = subject
    nachricht["Date"] = formatdate(localtime=True)
    # Eigene Kennung statt einer vom Server vergebenen: sie steht schon vor
    # dem Versand fest und taucht so im Protokoll wie in der Mail auf.
    nachricht["Message-ID"] = make_msgid(domain=absender.rpartition("@")[2] or None)
    # Umlaute: set_content kodiert Text als UTF-8, den Betreff erledigt die
    # Header-Kodierung von EmailMessage (RFC 2047).
    nachricht.set_content(text, subtype="plain", charset="utf-8")

    kontext = ssl.create_default_context()  # prüft Zertifikat und Hostnamen

    try:
        with smtplib.SMTP(str(c["host"]), int(c["port"]), timeout=TIMEOUT_SEC) as server:
            server.ehlo()
            if not server.has_extn("starttls"):
                raise MailError(
                    "Mailserver bietet kein STARTTLS an - es wird nicht "
                    "unverschluesselt versendet."
                )
            server.starttls(context=kontext)
            server.ehlo()
            server.login(str(c["user"]), str(c["password"]))
            server.send_message(nachricht)
    except MailError:
        raise
    except Exception as exc:  # smtplib-, TLS- und Netzwerkfehler
        raise MailError(_fehlertext(exc)) from exc

    return nachricht["Message-ID"]
