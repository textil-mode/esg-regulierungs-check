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
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

# Die Windows-Konsole faellt sonst ueber die chinesische Meldung (cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_login_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)

import db  # noqa: E402  (muss NACH dem Setzen von ESG_DB_PATH importiert werden)

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH} statt auf die Kopie!"

db.init_db()

import app as flaskapp  # noqa: E402  (importiert db bereits initialisiert)

assert db.DB_PATH == TEST_DB, "app.py hat die Test-Datenbank umgebogen!"

USER_MAIL = "opfer@example.org"
USER_PW = "richtiges-Passwort-2026"
IP_ANGREIFER = "203.0.113.7"
IP_NUTZER = "198.51.100.9"


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


def _ip_bei(remote: str, **headers: str) -> str:
    """`_client_ip()` unter kontrollierten Bedingungen auswerten."""
    with flaskapp.app.test_request_context(
        "/login", headers=headers, environ_base={"REMOTE_ADDR": remote}
    ):
        return flaskapp._client_ip()


# ---------------------------------------------------------------------------
# 1. Legitime Nutzer werden nicht ausgesperrt
# ---------------------------------------------------------------------------
def test_unter_der_schwelle(fehler: list[str]) -> None:
    print("\n[1] Vier Fehlversuche sperren noch nicht")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX - 1):
        db.record_login_failure(USER_MAIL, IP_NUTZER)
    frei = db.login_block_seconds(USER_MAIL, IP_NUTZER)
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
        db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    gesperrt = db.login_block_seconds(USER_MAIL, IP_ANGREIFER)
    _pruefe(gesperrt > 0, f"Sperre aktiv ({gesperrt} s Restzeit)", fehler)
    _pruefe(
        gesperrt <= db.LOGIN_BLOCK_BASE_SEC,
        f"erste Sperre hoechstens {db.LOGIN_BLOCK_BASE_SEC} s (gemessen {gesperrt} s)",
        fehler,
    )
    _pruefe(
        db.login_block_seconds("jemand.anderes@example.org", IP_ANGREIFER) == 0,
        "ein anderes Konto von derselben Adresse ist nicht betroffen",
        fehler,
    )


# ---------------------------------------------------------------------------
# 3. BLOCKER 1: Ein Angreifer kann ein fremdes Konto NICHT aussperren
# ---------------------------------------------------------------------------
def test_kein_aussperren(fehler: list[str]) -> None:
    print("\n[3] Angreifer sperrt nur sich selbst aus, nicht den Kontoinhaber")
    _leeren()
    # Angreifer beschiesst das Konto — deutlich ueber der Kontoschwelle,
    # aber unterhalb der IP-Schwelle (29 < 30 je Stunde), genau wie in der
    # nachgestellten Dauerbelagerung.
    for _ in range(29):
        db.record_login_failure(USER_MAIL, IP_ANGREIFER)

    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_ANGREIFER) > 0,
        "die Adresse des Angreifers ist fuer dieses Konto gesperrt",
        fehler,
    )
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_NUTZER) == 0,
        "der Kontoinhaber kommt von SEINER Adresse weiterhin durch",
        fehler,
    )
    # Und zwar wirklich bis zur Anmeldung — ueber die echte Route.
    c = flaskapp.app.test_client()
    r = c.post(
        "/login",
        data={"action": "login", "email": USER_MAIL, "password": USER_PW},
        headers={"X-Real-IP": IP_NUTZER},
    )
    _pruefe(
        r.status_code == 302 and (r.headers.get("Location") or "").endswith("/dashboard"),
        f"Anmeldung von der eigenen Adresse gelingt (HTTP {r.status_code})",
        fehler,
    )
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_ANGREIFER) > 0,
        "die Sperre des Angreifers bleibt dabei bestehen",
        fehler,
    )


# ---------------------------------------------------------------------------
# 4. Notausgang: python -m db unlock <email>
# ---------------------------------------------------------------------------
def test_notausgang(fehler: list[str]) -> None:
    print("\n[4] Notausgang `python -m db unlock <email>`")
    _leeren()
    for ip in (IP_ANGREIFER, IP_NUTZER):
        for _ in range(db.LOGIN_FAIL_MAX):
            db.record_login_failure(USER_MAIL, ip)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_NUTZER) > 0,
        "beide Adressen sind gesperrt",
        fehler,
    )
    rc = db._cli(["unlock", USER_MAIL])
    _pruefe(rc == 0, "CLI meldet Erfolg (Rueckgabewert 0)", fehler)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_NUTZER) == 0
        and db.login_block_seconds(USER_MAIL, IP_ANGREIFER) == 0,
        "danach ist das Konto von jeder Adresse aus wieder frei",
        fehler,
    )
    _pruefe(db._cli(["quatsch"]) == 2, "unbekannter Befehl gibt 2 zurueck", fehler)


# ---------------------------------------------------------------------------
# 5. BLOCKER 2: Proxy-Header richtig auswerten
# ---------------------------------------------------------------------------
def test_client_ip(fehler: list[str]) -> None:
    print("\n[5] Quell-IP: X-Real-IP zaehlt, gefaelschtes X-Forwarded-For nicht")
    # nginx setzt beides; X-Real-IP hat Vorrang, weil nginx ihn selbst schreibt.
    _pruefe(
        _ip_bei("172.17.0.1", **{"X-Real-IP": "9.9.9.9", "X-Forwarded-For": "1.2.3.4, 9.9.9.9"})
        == "9.9.9.9",
        "X-Real-IP schlaegt X-Forwarded-For",
        fehler,
    )
    # `$proxy_add_x_forwarded_for` haengt die echte Adresse HINTEN an.
    _pruefe(
        _ip_bei("172.17.0.1", **{"X-Forwarded-For": "1.2.3.4, 5.5.5.5, 9.9.9.9"}) == "9.9.9.9",
        "ohne X-Real-IP zaehlt der LETZTE X-Forwarded-For-Eintrag",
        fehler,
    )
    _pruefe(
        _ip_bei("172.17.0.1", **{"X-Forwarded-For": "kein-ip-wert, 9.9.9.9"}) == "9.9.9.9",
        "Muell im Header wird uebersprungen",
        fehler,
    )
    # Direkt am offenen Port: Gegenstelle oeffentlich -> Header ignorieren.
    _pruefe(
        _ip_bei("93.184.216.34", **{"X-Real-IP": "1.2.3.4", "X-Forwarded-For": "1.2.3.4"})
        == "93.184.216.34",
        "am offenen Port werden beide Header ignoriert",
        fehler,
    )
    _pruefe(_ip_bei("172.17.0.1") == "172.17.0.1", "ohne Header bleibt die Gegenstelle", fehler)

    # Und der Angriff selbst: 60 Versuche mit rotierendem, gefaelschtem XFF.
    _leeren()
    c = flaskapp.app.test_client()
    codes = []
    for i in range(60):
        r = c.post(
            "/login",
            data={"action": "login", "email": USER_MAIL, "password": "falsch"},
            headers={"X-Real-IP": IP_ANGREIFER, "X-Forwarded-For": f"10.0.0.{i}, {IP_ANGREIFER}"},
        )
        codes.append(r.status_code)
    _pruefe(
        429 in codes,
        f"rotierendes X-Forwarded-For umgeht die Sperre nicht "
        f"(erste Sperre bei Versuch {codes.index(429) + 1 if 429 in codes else '-'})",
        fehler,
    )
    # Gegenprobe: die behauptete Fremdadresse wurde nicht gesperrt.
    _pruefe(
        db.login_block_seconds(USER_MAIL, "10.0.0.1") == 0,
        "eine im Header behauptete Fremdadresse wird nicht gesperrt",
        fehler,
    )


# ---------------------------------------------------------------------------
# 6. Gestaffelt: jeder weitere Fehlversuch verdoppelt die Wartezeit
# ---------------------------------------------------------------------------
def test_staffelung(fehler: list[str]) -> None:
    print("\n[6] Die Wartezeit verdoppelt sich, gedeckelt bei 15 Minuten")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    erste = db.login_block_seconds(USER_MAIL, IP_ANGREIFER)
    db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    zweite = db.login_block_seconds(USER_MAIL, IP_ANGREIFER)
    _pruefe(zweite >= 2 * erste - 2, f"{erste} s -> {zweite} s", fehler)
    for _ in range(12):
        db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    gedeckelt = db.login_block_seconds(USER_MAIL, IP_ANGREIFER)
    _pruefe(
        gedeckelt <= db.LOGIN_BLOCK_MAX_SEC,
        f"Deckel haelt: {gedeckelt} s <= {db.LOGIN_BLOCK_MAX_SEC} s",
        fehler,
    )


# ---------------------------------------------------------------------------
# 7. Nach Ablauf ist der Weg wieder frei (keine Dauersperre)
# ---------------------------------------------------------------------------
def test_sperre_laeuft_ab(fehler: list[str]) -> None:
    print("\n[7] Nach Ablauf des Fensters ist die Anmeldung wieder moeglich")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_NUTZER)
    _pruefe(db.login_block_seconds(USER_MAIL, IP_NUTZER) > 0, "zunaechst gesperrt", fehler)

    _zurueckdatieren(db.LOGIN_BLOCK_BASE_SEC // 60)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_NUTZER) == 0,
        f"nach {db.LOGIN_BLOCK_BASE_SEC} s Wartezeit wieder frei",
        fehler,
    )

    _zurueckdatieren(db.LOGIN_FAIL_WINDOW_MIN + 1)
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_NUTZER) == 0,
        f"nach {db.LOGIN_FAIL_WINDOW_MIN} min ohne Versuch faellt der Zaehler auf 0",
        fehler,
    )
    _pruefe(
        db.verify_user(USER_MAIL, USER_PW) is not None,
        "richtiges Passwort wird danach akzeptiert",
        fehler,
    )


# ---------------------------------------------------------------------------
# 8. Erfolgreiche Anmeldung setzt den Zaehler der eigenen Adresse zurueck
# ---------------------------------------------------------------------------
def test_erfolg_setzt_zurueck(fehler: list[str]) -> None:
    print("\n[8] Erfolgreiche Anmeldung loescht den Zaehler der eigenen Adresse")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX - 1):
        db.record_login_failure(USER_MAIL, IP_NUTZER)
    db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    db.clear_login_failures(USER_MAIL, IP_NUTZER)
    with sqlite3.connect(TEST_DB) as c:
        eigen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='account' AND subject=?",
            (f"{USER_MAIL}|{IP_NUTZER}",),
        ).fetchone()[0]
        fremd = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='account' AND subject=?",
            (f"{USER_MAIL}|{IP_ANGREIFER}",),
        ).fetchone()[0]
    _pruefe(eigen == 0, "Zaehler der eigenen Adresse steht wieder auf 0", fehler)
    _pruefe(fremd == 1, "der Eintrag der fremden Adresse bleibt bestehen", fehler)

    with sqlite3.connect(TEST_DB) as c:
        ip_zeilen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='ip' AND subject=?",
            (IP_NUTZER,),
        ).fetchone()[0]
    _pruefe(ip_zeilen > 0, "die IP-Zaehlung wird durch einen Erfolg NICHT geleert", fehler)


# ---------------------------------------------------------------------------
# 9. IP-Bremse: verteilte Versuche auf viele Konten
# ---------------------------------------------------------------------------
def test_ip_bremse(fehler: list[str]) -> None:
    print("\n[9] Die IP-Bremse fasst Versuche ueber viele Konten zusammen")
    _leeren()
    for i in range(db.LOGIN_IP_MAX):
        db.record_login_failure(f"ziel{i}@example.org", IP_ANGREIFER)
    _pruefe(
        db.login_block_seconds("ziel0@example.org", IP_NUTZER) == 0,
        "kein einzelnes Konto ist gesperrt",
        fehler,
    )
    gesperrt = db.login_block_seconds("ziel99@example.org", IP_ANGREIFER)
    _pruefe(gesperrt > 0, f"IP {IP_ANGREIFER} gesperrt ({gesperrt} s Restzeit)", fehler)
    _pruefe(
        db.login_block_seconds("ziel99@example.org", IP_NUTZER) == 0,
        f"eine andere IP ({IP_NUTZER}) bleibt unbehelligt",
        fehler,
    )
    _zurueckdatieren(db.LOGIN_IP_BLOCK_SEC // 60 + 1)
    _pruefe(
        db.login_block_seconds("ziel99@example.org", IP_ANGREIFER) == 0,
        "nach Ablauf ist auch die IP wieder frei",
        fehler,
    )


# ---------------------------------------------------------------------------
# 10. Unbekannte Adressen zaehlen mit (sonst verriete die Sperre das Konto)
# ---------------------------------------------------------------------------
def test_unbekanntes_konto(fehler: list[str]) -> None:
    print("\n[10] Auch erfundene Adressen werden gesperrt (kein Rueckschluss moeglich)")
    _leeren()
    erfunden = "gibt-es-nicht@example.org"
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(erfunden, IP_ANGREIFER)
    _pruefe(
        db.login_block_seconds(erfunden, IP_ANGREIFER) > 0,
        "erfundene Adresse wird genauso gesperrt wie eine echte",
        fehler,
    )


# ---------------------------------------------------------------------------
# 11. Gleichzeitige Versuche schluepfen nicht durch
# ---------------------------------------------------------------------------
def test_gleichzeitig(fehler: list[str]) -> None:
    print("\n[11] 20 gleichzeitige Versuche: nur das Kontingent kommt durch")
    _leeren()
    durchgelassen: list[int] = []
    sperre = threading.Lock()

    def versuch() -> None:
        rest = db.begin_login_attempt(USER_MAIL, IP_ANGREIFER)
        if rest == 0:
            with sperre:
                durchgelassen.append(1)

    threads = [threading.Thread(target=versuch) for _ in range(20)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    n = len(durchgelassen)
    _pruefe(
        n == db.LOGIN_FAIL_MAX,
        f"{n} von 20 durchgelassen (erwartet {db.LOGIN_FAIL_MAX}; vorher: alle 20)",
        fehler,
    )


# ---------------------------------------------------------------------------
# 12. Bremse am Passwort-Reset-Pfad — gueltige Links bleiben einloesbar
# ---------------------------------------------------------------------------
def test_reset_bremse(fehler: list[str]) -> None:
    print("\n[12] Reset-Pfad: ungueltige Token gebremst, gueltiger Link geht durch")
    _leeren()
    c = flaskapp.app.test_client()
    codes = [
        c.get(f"/passwort-zuruecksetzen/token-{i}", headers={"X-Real-IP": IP_ANGREIFER}).status_code
        for i in range(db.RESET_IP_MAX + 1)
    ]
    _pruefe(
        codes[: db.RESET_IP_MAX] == [400] * db.RESET_IP_MAX and codes[-1] == 429,
        f"{db.RESET_IP_MAX}x HTTP 400, dann 429",
        fehler,
    )
    # Entscheidend: Der rechtmaessige Nutzer hinter DERSELBEN Adresse
    # (Firmen-NAT) kann seinen gueltigen Link trotzdem einloesen.
    user = db.get_user_by_email(USER_MAIL)
    token, _ = db.issue_reset_token(user["id"])
    r = c.get(f"/passwort-zuruecksetzen/{token}", headers={"X-Real-IP": IP_ANGREIFER})
    _pruefe(
        r.status_code == 200,
        f"gueltiger Link trotz gesperrter Adresse einloesbar (HTTP {r.status_code})",
        fehler,
    )


# ---------------------------------------------------------------------------
# 13. Sperre ueberlebt einen Neustart (persistent in SQLite)
# ---------------------------------------------------------------------------
def test_persistenz(fehler: list[str]) -> None:
    print("\n[13] Die Sperre steht in der Datenbank, nicht im Speicher")
    _leeren()
    for _ in range(db.LOGIN_FAIL_MAX):
        db.record_login_failure(USER_MAIL, IP_ANGREIFER)
    with sqlite3.connect(TEST_DB) as c:
        zeilen = c.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE scope='account' AND subject=?",
            (f"{USER_MAIL}|{IP_ANGREIFER}",),
        ).fetchone()[0]
    _pruefe(zeilen == db.LOGIN_FAIL_MAX, f"{zeilen} Zeilen in login_attempts", fehler)
    db.init_db()
    _pruefe(
        db.login_block_seconds(USER_MAIL, IP_ANGREIFER) > 0,
        "nach erneutem init_db() weiterhin gesperrt",
        fehler,
    )


# ---------------------------------------------------------------------------
# 14. Aufraeumen laeuft ueber einen Index, nicht als Volltabellenscan
# ---------------------------------------------------------------------------
def test_aufraeum_index(fehler: list[str]) -> None:
    print("\n[14] Das Aufraeumen nutzt einen Index")
    with sqlite3.connect(TEST_DB) as c:
        plan = " ".join(
            str(r)
            for r in c.execute(
                "EXPLAIN QUERY PLAN DELETE FROM login_attempts WHERE attempted_at < ?",
                ("2000-01-01",),
            ).fetchall()
        )
    _pruefe("idx_login_attempts_age" in plan, f"Abfrageplan: {plan.strip()}", fehler)


# ---------------------------------------------------------------------------
# 15. H4: beide Fehlerpfade brauchen gleich lang
# ---------------------------------------------------------------------------
def test_laufzeit(fehler: list[str]) -> None:
    print("\n[15] Antwortzeit verraet nicht mehr, ob es das Konto gibt (H4)")
    _leeren()
    # Der Dummy-Hash muss denselben Kostenfaktor tragen wie die echten Hashes —
    # sonst laufen beide Pfade wieder unterschiedlich lang.
    _pruefe(
        db._DUMMY_PW_HASH.startswith(b"$2b$%02d$" % db.BCRYPT_ROUNDS),
        f"Dummy-Hash traegt Kostenfaktor {db.BCRYPT_ROUNDS}",
        fehler,
    )
    with sqlite3.connect(TEST_DB) as c:
        echt = c.execute("SELECT pw_hash FROM users WHERE email = ?", (USER_MAIL,)).fetchone()[0]
    _pruefe(
        echt.startswith(f"$2b${db.BCRYPT_ROUNDS:02d}$"),
        "gespeicherte Passwoerter tragen denselben Kostenfaktor",
        fehler,
    )

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
        f"Laufzeiten liegen dicht beieinander (Faktor {verhaeltnis:.2f}, vorher ~0,01)",
        fehler,
    )


# ---------------------------------------------------------------------------
# 16. Sperrmeldung in allen 6 Sprachen, mit Singular und Plural
# ---------------------------------------------------------------------------
def test_meldung(fehler: list[str]) -> None:
    print("\n[16] Sperrmeldung: 6 Sprachen, Singular und Plural")
    import i18n

    for lang in i18n.LANG_CODES:
        einzahl = flaskapp._locked_message(45, lang)     # -> 1 Minute
        mehrzahl = flaskapp._locked_message(600, lang)   # -> 10 Minuten
        ok = (
            "{minutes}" not in einzahl
            and "{minutes}" not in mehrzahl
            and "10" in mehrzahl
            and einzahl != mehrzahl
            and i18n.UI["err_login_locked_one"].get(lang)
            and i18n.UI["err_login_locked"].get(lang)
        )
        _pruefe(bool(ok), f"{lang}: {einzahl} / {mehrzahl}", fehler)


def main() -> int:
    fehler: list[str] = []
    print(f"Test-Datenbank: {TEST_DB}")
    db.create_user(USER_MAIL, USER_PW)

    test_unter_der_schwelle(fehler)
    test_sperre_greift(fehler)
    test_kein_aussperren(fehler)
    test_notausgang(fehler)
    test_client_ip(fehler)
    test_staffelung(fehler)
    test_sperre_laeuft_ab(fehler)
    test_erfolg_setzt_zurueck(fehler)
    test_ip_bremse(fehler)
    test_unbekanntes_konto(fehler)
    test_gleichzeitig(fehler)
    test_reset_bremse(fehler)
    test_persistenz(fehler)
    test_aufraeum_index(fehler)
    test_laufzeit(fehler)
    test_meldung(fehler)

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
