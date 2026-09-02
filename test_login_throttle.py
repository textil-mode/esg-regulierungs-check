"""Tests fuer die Login-Bremse (K1) und die gleiche Laufzeit beider Fehlerpfade (H4).

Laeuft ausschliesslich gegen eine eigene Datenbank (`data/esg_login_test.db`),
die zu Beginn frisch angelegt wird — `data/esg.db` wird nie beruehrt.
Kein Netz, kein LLM, keine Kosten.

Aufruf:  ./.venv/Scripts/python.exe test_login_throttle.py
"""
from __future__ import annotations

import os
import sqlite3
import statistics
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

TEST_DB = Path(__file__).parent / "data" / "esg_login_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)

import db  # noqa: E402  (muss NACH dem Setzen von ESG_DB_PATH importiert werden)

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH} statt auf die Kopie!"

db.init_db()

USER_MAIL = "opfer@example.org"
USER_PW = "richtiges-Passwort-2026"
FALSCH = "falsch"
IP_A = "203.0.113.7"
IP_B = "198.51.100.9"


# ---------------------------------------------------------------------------
# Hilfen
# ---------------------------------------------------------------------------
def _leeren() -> None:
    """Alle Fehlversuche loeschen — jeder Test startet sauber."""
    with sqlite3.connect(TEST_DB) as c:
        c.execute("DELETE FROM login_attempts")


def _zurueckdatieren(minuten: int) -> None:
    """Verschiebt alle gespeicherten Fehlversuche um N Minuten in die Vergangenheit.

    So laesst sich der Ablauf einer Sperre pruefen, ohne im Test zu warten.
    """
    with sqlite3.connect(TEST_DB) as c:
        rows = c.execute("SELECT id, attempted_at FROM login_attempts").fetchall()
        for rid, ts in rows:
            neu = (datetime.fromisoformat(ts) - timedelta(minutes=minuten)).isoformat()
            c.execute("UPDATE login_attempts SET attempted_at = ? WHERE id = ?", (neu, rid))


def _pruefe(bedingung: bool, text: str, fehler: list[str]) -> None:
    if bedingung:
        print(f"  ok  {text}")
    else:
        print(f"  FEHLER  {text}")
        fehler.append(text)


# ---------------------------------------------------------------------------
# 1. Legitime Nutzer werden nicht ausgesperrt
# ---------------------------------------------------------------------------
def test_unter_der_schwelle(fehler: list[str]) -> None:
    print("\n[1] Vier Fehlversuche sperren noch nicht")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX - 1):
        db.record_login_failure(USER_MAIL, IP_A)
    frei = db.login_block_seconds(USER_MAIL, IP_A)
    _pruefe(frei == 0, f"nach {db.LOGIN_FAIL_MAX - 1} Fehlversuchen keine Sperre", fehler)
    _pruefe(
        db.verify_user(USER_MAIL, USER_PW) is not None,
        "richtiges Passwort wird danach weiterhin akzeptiert",
        fehler,
    )


# ---------------------------------------------------------------------------
# 2. Die Sperre greift
# ---------------------------------------------------------------------------
def test_sperre_greift(fehler: list[str]) -> None:
    print("\n[2] Der fuenfte Fehlversuch sperrt")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_A)
    gesperrt = db.login_block_seconds(USER_MAIL, IP_A)
    _pruefe(gesperrt > 0, f"Sperre aktiv ({gesperrt} s Restzeit)", fehler)
    _pruefe(
        gesperrt <= db.LOGIN_BLOCK_BASE_SEC,
        f"erste Sperre hoechstens {db.LOGIN_BLOCK_BASE_SEC} s (gemessen {gesperrt} s)",
        fehler,
    )
    # Ein anderes Konto von derselben IP bleibt frei (IP-Schwelle nicht erreicht).
    _pruefe(
        db.login_block_seconds("jemand.anderes@example.org", IP_A) == 0,
        "die Kontosperre trifft nur dieses eine Konto",
        fehler,
    )


# ---------------------------------------------------------------------------
# 3. Gestaffelt: jeder weitere Fehlversuch verdoppelt die Wartezeit
# ---------------------------------------------------------------------------
def test_staffelung(fehler: list[str]) -> None:
    print("\n[3] Die Wartezeit verdoppelt sich, gedeckelt bei 15 Minuten")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_A)
    erste = db.login_block_seconds(USER_MAIL, IP_A)
    db.record_login_failure(USER_MAIL, IP_A)
    zweite = db.login_block_seconds(USER_MAIL, IP_A)
    _pruefe(zweite >= 2 * erste - 2, f"{erste} s -> {zweite} s", fehler)
    for _ in range(12):
        db.record_login_failure(USER_MAIL, IP_A)
    gedeckelt = db.login_block_seconds(USER_MAIL, IP_A)
    _pruefe(
        gedeckelt <= db.LOGIN_BLOCK_MAX_SEC,
        f"Deckel haelt: {gedeckelt} s <= {db.LOGIN_BLOCK_MAX_SEC} s",
        fehler,
    )


# ---------------------------------------------------------------------------
# 4. Nach Ablauf ist der Weg wieder frei (keine Dauersperre)
# ---------------------------------------------------------------------------
def test_sperre_laeuft_ab(fehler: list[str]) -> None:
    print("\n[4] Nach Ablauf des Fensters ist die Anmeldung wieder moeglich")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_A)
    _pruefe(db.login_block_seconds(USER_MAIL, IP_A) > 0, "zunaechst gesperrt", fehler)

    # Kurz vor Ablauf der Sperre (aber noch im Zaehlfenster): immer noch gesperrt.
    _zurueckdatieren(db.LOGIN_BLOCK_BASE_SEC // 60)
    rest = db.login_block_seconds(USER_MAIL, IP_A)
    _pruefe(rest == 0, f"nach {db.LOGIN_BLOCK_BASE_SEC} s Wartezeit wieder frei", fehler)

    # Und nach dem vollen Beobachtungsfenster ist auch der Zaehler leer.
    _zurueckdatieren(db.LOGIN_FAIL_WINDOW_MIN + 1)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_A) == 0,
        f"nach {db.LOGIN_FAIL_WINDOW_MIN} min ohne Versuch faellt der Zaehler auf 0",
        fehler,
    )
    _pruefe(
        db.verify_user(USER_MAIL, USER_PW) is not None,
        "richtiges Passwort wird danach akzeptiert",
        fehler,
    )


# ---------------------------------------------------------------------------
# 5. Erfolgreiche Anmeldung setzt den Kontozaehler zurueck
# ---------------------------------------------------------------------------
def test_erfolg_setzt_zurueck(fehler: list[str]) -> None:
    print("\n[5] Erfolgreiche Anmeldung loescht den Zaehler des Kontos")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX - 1):
        db.record_login_failure(USER_MAIL, IP_A)
    db.clear_login_failures(USER_MAIL)
    with sqlite3.connect(TEST_DB) as c:
        offen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='account' AND subject=?",
            (USER_MAIL,),
        ).fetchone()[0]
    _pruefe(offen == 0, "Kontozaehler steht wieder auf 0", fehler)
    # Vier neue Fehlversuche duerfen jetzt wieder folgen, ohne zu sperren.
    for _ in range(db.LOGIN_FAIL_MAX - 1):
        db.record_login_failure(USER_MAIL, IP_A)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_A) == 0,
        "das Kontingent steht danach wieder voll zur Verfuegung",
        fehler,
    )
    # Die IP-Zaehlung bleibt bewusst bestehen.
    with sqlite3.connect(TEST_DB) as c:
        ip_zeilen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='ip' AND subject=?",
            (IP_A,),
        ).fetchone()[0]
    _pruefe(ip_zeilen > 0, "die IP-Zaehlung wird durch einen Erfolg NICHT geleert", fehler)


# ---------------------------------------------------------------------------
# 6. IP-Bremse: verteilte Versuche auf viele Konten
# ---------------------------------------------------------------------------
def test_ip_bremse(fehler: list[str]) -> None:
    print("\n[6] Die IP-Bremse fasst Versuche ueber viele Konten zusammen")
    _leeren()
    for i in range(db.LOGIN_IP_MAX):
        db.record_login_failure(f"ziel{i}@example.org", IP_A)
    # Jedes einzelne Konto liegt weit unter der Kontoschwelle …
    _pruefe(
        db.login_block_seconds("ziel0@example.org", IP_B) == 0,
        "kein einzelnes Konto ist gesperrt",
        fehler,
    )
    # … die IP aber ist es.
    gesperrt = db.login_block_seconds("ziel99@example.org", IP_A)
    _pruefe(gesperrt > 0, f"IP {IP_A} gesperrt ({gesperrt} s Restzeit)", fehler)
    _pruefe(
        db.login_block_seconds("ziel99@example.org", IP_B) == 0,
        f"eine andere IP ({IP_B}) bleibt unbehelligt",
        fehler,
    )
    _zurueckdatieren(db.LOGIN_IP_BLOCK_SEC // 60 + 1)
    _pruefe(
        db.login_block_seconds("ziel99@example.org", IP_A) == 0,
        "nach Ablauf ist auch die IP wieder frei",
        fehler,
    )


# ---------------------------------------------------------------------------
# 7. Unbekannte Adressen zaehlen mit (sonst verriete die Sperre das Konto)
# ---------------------------------------------------------------------------
def test_unbekanntes_konto(fehler: list[str]) -> None:
    print("\n[7] Auch erfundene Adressen werden gesperrt (kein Rueckschluss moeglich)")
    _leeren()
    erfunden = "gibt-es-nicht@example.org"
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(erfunden, IP_A)
    _pruefe(
        db.login_block_seconds(erfunden, IP_A) > 0,
        "erfundene Adresse wird genauso gesperrt wie eine echte",
        fehler,
    )


# ---------------------------------------------------------------------------
# 8. Bremse am Passwort-Reset-Pfad
# ---------------------------------------------------------------------------
def test_reset_bremse(fehler: list[str]) -> None:
    print("\n[8] Ungueltige Reset-Token lassen sich nicht endlos durchklopfen")
    _leeren()
    for _ in range(db.RESET_IP_MAX - 1):
        db.record_reset_token_failure(IP_A)
    _pruefe(db.reset_token_block_seconds(IP_A) == 0, "unterhalb der Schwelle frei", fehler)
    db.record_reset_token_failure(IP_A)
    _pruefe(db.reset_token_block_seconds(IP_A) > 0, "ab der Schwelle gesperrt", fehler)
    _pruefe(db.reset_token_block_seconds(IP_B) == 0, "andere IP unbetroffen", fehler)


# ---------------------------------------------------------------------------
# 9. Sperre ueberlebt einen Neustart (persistent in SQLite)
# ---------------------------------------------------------------------------
def test_persistenz(fehler: list[str]) -> None:
    print("\n[9] Die Sperre steht in der Datenbank, nicht im Speicher")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_A)
    with sqlite3.connect(TEST_DB) as c:
        zeilen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='account' AND subject=?",
            (USER_MAIL,),
        ).fetchone()[0]
    _pruefe(zeilen == db.LOGIN_FAIL_MAX, f"{zeilen} Zeilen in login_attempts", fehler)
    # init_db erneut aufrufen (wie beim Containerstart) — die Sperre bleibt.
    db.init_db()
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_A) > 0,
        "nach erneutem init_db() weiterhin gesperrt",
        fehler,
    )


# ---------------------------------------------------------------------------
# 10. H4: beide Fehlerpfade brauchen gleich lang
# ---------------------------------------------------------------------------
def test_laufzeit(fehler: list[str]) -> None:
    print("\n[10] Antwortzeit verraet nicht mehr, ob es das Konto gibt (H4)")
    _leeren()
    laeufe = 7

    def messen(mail: str) -> float:
        werte = []
        for _ in range(laeufe):
            start = time.perf_counter()
            db.verify_user(mail, "irgendein-falsches-Passwort")
            werte.append(time.perf_counter() - start)
        return statistics.mean(werte)

    vorhanden = messen(USER_MAIL)
    erfunden = messen("gibt-es-garantiert-nicht@example.org")
    verhaeltnis = erfunden / vorhanden if vorhanden else 0
    print(f"      vorhandenes Konto : {vorhanden * 1000:7.1f} ms (Mittel aus {laeufe})")
    print(f"      erfundene Adresse : {erfunden * 1000:7.1f} ms (Mittel aus {laeufe})")
    print(f"      Verhaeltnis       : {verhaeltnis:.2f}  (1,00 = nicht unterscheidbar)")
    _pruefe(
        0.7 <= verhaeltnis <= 1.4,
        f"Laufzeiten liegen dicht beieinander (Faktor {verhaeltnis:.2f}, vorher ~0,05)",
        fehler,
    )


def main() -> int:
    fehler: list[str] = []
    print(f"Test-Datenbank: {TEST_DB}")
    db.create_user(USER_MAIL, USER_PW)

    test_unter_der_schwelle(fehler)
    test_sperre_greift(fehler)
    test_staffelung(fehler)
    test_sperre_laeuft_ab(fehler)
    test_erfolg_setzt_zurueck(fehler)
    test_ip_bremse(fehler)
    test_unbekanntes_konto(fehler)
    test_reset_bremse(fehler)
    test_persistenz(fehler)
    test_laufzeit(fehler)

    print("\n" + "=" * 70)
    if fehler:
        print(f"FEHLGESCHLAGEN — {len(fehler)} Befund(e):")
        for f in fehler:
            print(f"  - {f}")
        return 1
    print("Alle Tests bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
