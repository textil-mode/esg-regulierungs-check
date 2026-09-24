"""Mailversand über AgentMail — schlank, ohne Warteschlange.

Schnittstelle 1:1 wie im Projekt „Prompt-Katalog" (`app/lib/mail.ts`):

    POST https://api.agentmail.to/v0/inboxes/{INBOX_ID}/messages/send
    Authorization: Bearer {API_KEY}
    Content-Type: application/json
    {"to": "...", "subject": "...", "text": "..."}

Die Antwort trägt bei Erfolg `message_id`, im Fehlerfall ein `message`-Feld.

Warum hier **keine** Warteschlange mit Wiederholversuchen, anders als im
Prompt-Katalog:

* Der Prompt-Katalog ist ein Cloudflare Worker mit Cron-Trigger — dort kostet
  ein späterer Versuch nichts und läuft von selbst an. Die ESG-Anwendung ist
  ein einzelner Flask-/Gunicorn-Prozess ohne Scheduler. Eine Warteschlange
  bräuchte hier erst einen Wecker, den es nicht gibt; sie würde faktisch nur
  beim nächsten Reset-Versuch abgearbeitet — also genau dann, wenn der Nutzer
  ohnehin schon einen frischen Link anfordert.
* Eine Warteschlange müsste den **fertigen Mailtext** speichern, und darin
  steht der Reset-Link im Klartext. Das widerspricht der Regel, dass vom Token
  nur der SHA-256-Hash in der Datenbank liegt.
* Der Link gilt 24 Stunden und ist beliebig oft neu anforderbar. Scheitert der
  Versand, ist der richtige Weg „noch einmal anfordern" oder der Admin-Weg
  unter /admin/passwort-resets — beides ist bereits da.

Es bleibt deshalb bei einem Versuch je Anforderung. Das Ergebnis wird
protokolliert (`db.log_mail`), damit der Admin sieht, ob es geklappt hat.
"""
from __future__ import annotations

import os
from urllib.parse import quote

import httpx

ENDPOINT = "https://api.agentmail.to/v0/inboxes/{inbox}/messages/send"

# Der Versand läuft in einem Hintergrund-Thread; ein hängender Aufruf blockiert
# also keine Anfrage. Trotzdem kurz gehalten, damit Threads nicht auflaufen.
TIMEOUT_SEC = 15.0


class MailError(RuntimeError):
    """Versand nicht möglich (nicht konfiguriert, Netz- oder API-Fehler)."""


def _config() -> tuple[str, str]:
    return (
        (os.getenv("AGENTMAIL_API_KEY") or "").strip(),
        (os.getenv("AGENTMAIL_INBOX_ID") or "").strip(),
    )


def is_configured() -> bool:
    """Sind Schlüssel und Postfach gesetzt? Ohne beides gilt der Admin-Weg."""
    api_key, inbox = _config()
    return bool(api_key and inbox)


def send(recipient: str, subject: str, text: str) -> str | None:
    """Übergibt eine Nur-Text-Nachricht an AgentMail.

    Gibt die `message_id` des Dienstes zurück. Wirft `MailError` bei jedem
    Fehlschlag — der Aufrufer protokolliert ihn, zeigt ihn aber nie dem
    anfragenden Nutzer (sonst verriete die Meldung, dass es das Konto gibt).
    """
    api_key, inbox = _config()
    if not (api_key and inbox):
        raise MailError("AgentMail ist nicht konfiguriert.")

    try:
        antwort = httpx.post(
            ENDPOINT.format(inbox=quote(inbox, safe="")),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"to": recipient, "subject": subject, "text": text},
            timeout=TIMEOUT_SEC,
        )
    except httpx.HTTPError as exc:
        raise MailError(f"Netzwerkfehler: {exc.__class__.__name__}") from exc

    try:
        nutzlast = antwort.json()
    except ValueError:
        nutzlast = {}
    if not isinstance(nutzlast, dict):
        nutzlast = {}

    if antwort.status_code >= 400:
        grund = nutzlast.get("message") or "unbekannter Fehler"
        raise MailError(f"HTTP {antwort.status_code}: {grund}")
    return nutzlast.get("message_id")
