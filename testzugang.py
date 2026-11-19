# -*- coding: utf-8 -*-
"""Abgelaufene Testzugaenge sperren und die Betroffenen benachrichtigen.

Ein Testzugang gilt `db.TEST_ACCESS_HOURS` = 48 Stunden **ab der Freischaltung**
(Nutzerentscheidung 05.10.2026). Danach sperrt sich das Konto — gesperrt, nicht
geloescht: alle Angaben bleiben, der Admin kann jederzeit auf `benutzer`
umstellen.

Dieser Flask-Prozess hat keinen Wecker (siehe `mailer.py`), deshalb hat die
Sperre drei Ausloeser:

* **Anmeldeversuch** — wirkt sofort, aber nur wenn jemand kommt.
* **Aufruf der Admin-Kontenliste** — damit die Liste nie veraltet aussieht.
* **Cron, stuendlich** — der einzige, der auch im stillen Fall die Nachricht
  verschickt:

      0 * * * * docker exec esg-ki-textil-mode python testzugang.py >> /var/log/esg-testzugang.log 2>&1

Dass niemand zweimal benachrichtigt wird, sichert `db.lock_expired_tests()`:
Lesen und Sperren liegen in einer Transaktion, jede Zeile wird nur einmal
herausgegeben. Zwei gleichzeitige Ausloeser teilen sich also die Arbeit, statt
sie zu verdoppeln.

Aufruf von Hand (zeigt, was passieren wuerde, ohne zu sperren):
    docker exec esg-ki-textil-mode python testzugang.py --probe
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Callable, Optional

import db
import mailer
from i18n import normalize_lang, t

# Wohin der Link in der Nachricht zeigt. Dieselbe Variable wie im Mailversand
# der App — aus dem `Host`-Kopf darf nichts gebaut werden (Befund H1,
# 24.09.2026), und hier gibt es ohnehin keine Anfrage.
def _anmeldelink() -> str:
    basis = (os.environ.get("PUBLIC_BASE_URL") or "").rstrip("/")
    return f"{basis}/login" if basis else ""


def _zeit(iso: Optional[str]) -> str:
    """ISO-Zeitstempel als `TT.MM.JJJJ HH:MM`. Leer bleibt leer."""
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso).strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return iso[:16].replace("T", " ")


def nachricht(konto: dict) -> tuple[str, str, str]:
    """Betreff und Text der Ablauf-Nachricht in der Sprache der Registrierung."""
    lang = normalize_lang(konto.get("signup_lang"))
    return (lang,
            t("mail_test_expired_subject", lang),
            t("mail_test_expired_body", lang).format(link=_anmeldelink()))


def sperren_und_melden(versand: Callable[[str, str, str], None] | None = None
                       ) -> list[dict]:
    """Sperrt faellige Testzugaenge und meldet es den Betroffenen.

    `versand(empfaenger, betreff, text)` uebernimmt das Verschicken — die App
    gibt dort ihren Hintergrund-Thread hinein, der Cron den direkten Weg
    unten. Ohne konfigurierten Mailversand wird nur gesperrt; die Sperre darf
    nicht daran haengen, dass eine Nachricht rausgeht.

    Rueckgabe: die gesperrten Konten (leer, wenn nichts faellig war).
    """
    betroffen = db.lock_expired_tests()
    if not betroffen or not mailer.is_configured():
        return betroffen

    for konto in betroffen:
        _lang, betreff, text = nachricht(konto)
        if versand is not None:
            versand(konto["email"], betreff, text)
        else:
            try:
                message_id = mailer.send(konto["email"], betreff, text)
                db.log_mail(konto["email"], "test_expired", "sent",
                            message_id=message_id)
            except Exception as exc:                      # noqa: BLE001
                db.log_mail(konto["email"], "test_expired", "failed",
                            error=str(exc)[:300])
    return betroffen


def _probe() -> int:
    """Zeigt, was faellig ist, ohne zu sperren oder zu verschicken."""
    jetzt = datetime.utcnow().isoformat()
    with db._conn() as c:                                  # noqa: SLF001
        rows = c.execute(
            "SELECT email, test_expires_at FROM users"
            " WHERE account_type = ? AND locked = 0 AND approved = 1"
            "   AND test_expires_at IS NOT NULL AND test_expires_at <= ?",
            (db.ACCOUNT_TYPE_TEST, jetzt)).fetchall()
        offen = c.execute(
            "SELECT email, test_expires_at FROM users"
            " WHERE account_type = ? AND locked = 0 AND approved = 1"
            "   AND test_expires_at > ? ORDER BY test_expires_at",
            (db.ACCOUNT_TYPE_TEST, jetzt)).fetchall()
    print(f"Datenbank: {db.DB_PATH}")
    print(f"faellig jetzt: {len(rows)}")
    for r in rows:
        print(f"  {r['email']}  (abgelaufen {_zeit(r['test_expires_at'])})")
    print(f"laufende Testzugaenge: {len(offen)}")
    for r in offen:
        print(f"  {r['email']}  (laeuft bis {_zeit(r['test_expires_at'])})")
    return 0


def main(argv: list[str]) -> int:
    db.init_db()
    if "--probe" in argv:
        return _probe()
    betroffen = sperren_und_melden()
    if not betroffen:
        # Stille, wenn nichts zu melden ist: der Lauf kommt stuendlich, und ein
        # Log, in dem 23 von 24 Zeilen "nichts passiert" sagen, liest niemand.
        # Den Stand zeigt `--probe`.
        return 0
    zeit = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
    print(f"[{zeit}] {len(betroffen)} Testzugang/-zugaenge gesperrt:")
    for konto in betroffen:
        print(f"  {konto['email']}")
    if not mailer.is_configured():
        print("  (kein Mailversand konfiguriert — nur gesperrt)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
