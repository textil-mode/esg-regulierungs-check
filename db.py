"""SQLite-Persistenz für User, Company und Analysen."""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import bcrypt

from regulations import (MATERIALS, PRODUCT_CATEGORIES, SALES_MARKETS, SITE_TYPES,
                         VALUE_CHAIN_ROLES)


def _configured_db_path() -> Path:
    """Ziel-Datenbank; `ESG_DB_PATH` erlaubt isolierte Laeufe.

    Ohne diesen Schalter schreibt jeder Direktaufruf (z. B. `python watchdog.py`)
    zwangslaeufig in `data/esg.db`; ein Testlauf waere nur ueber Monkey-Patching
    von db UND fetcher moeglich — und genau das wird leicht vergessen.
    `fetcher.py` folgt diesem Pfad automatisch, es reicht also die eine Variable.
    """
    override = (os.getenv("ESG_DB_PATH") or "").strip()
    return Path(override) if override else Path(__file__).parent / "data" / "esg.db"


DB_PATH = _configured_db_path()


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


COMPANY_EXTRA_COLUMNS = [
    ("balance_sheet_eur", "REAL DEFAULT 0"),
    ("legal_form", "TEXT"),
    ("group_role", "TEXT"),
    ("env_claims", "INTEGER DEFAULT 0"),
    ("product_categories_json", "TEXT"),
    ("employees_de", "INTEGER DEFAULT 0"),
    ("language", "TEXT DEFAULT 'de'"),
    ("eu_importer", "INTEGER DEFAULT 0"),
    ("value_chain_roles_json", "TEXT"),
    ("materials_json", "TEXT"),
    # Nettoumsatz in der EU (Art. 40a Bilanzrichtlinie, Art. 2 Abs. 2 CSDDD
    # stellen fuer Drittland-Unternehmen darauf ab, nicht auf den weltweiten).
    ("revenue_eu_eur", "REAL DEFAULT 0"),
    ("sales_markets_json", "TEXT"),
]

# Umbenannte Auswahlwerte: alter Wert -> heutiger Wert. Anders als bei den
# Mehrfachauswahlen wird hier nichts weggefiltert, sondern derselbe Sachverhalt
# unter seinem neuen Namen weitergefuehrt. Nur echte Umbenennungen gehoeren
# hier hinein — keine inhaltliche Umdeutung.
_SITE_TYPE_RENAMES = {"Hauptsitz": SITE_TYPES[0]}


def _rename_sites(sites: list) -> list:
    """Standort-Typen aus Altprofilen auf die heutigen Bezeichnungen heben."""
    out = []
    for s in sites or []:
        s = dict(s)
        s["type"] = _SITE_TYPE_RENAMES.get(s.get("type"), s.get("type"))
        out.append(s)
    return out


def _migrate_companies(c: sqlite3.Connection) -> None:
    cols = {row[1] for row in c.execute("PRAGMA table_info(companies)").fetchall()}
    for col, ddl in COMPANY_EXTRA_COLUMNS:
        if col not in cols:
            c.execute(f"ALTER TABLE companies ADD COLUMN {col} {ddl}")


def _migrate_analysis_cache(c: sqlite3.Connection) -> None:
    """Bringt `analysis_cache` auf das globale, gesetzesstand-feste Schema.

    Der alte Cache haengt am Nutzer und kennt den Gesetzesstand nicht; seine
    Eintraege lassen sich nicht in das neue Schema uebersetzen. Sie verfallen
    deshalb einmalig (die Ergebnisse werden beim naechsten Lauf neu erzeugt).
    Idempotent: laeuft nur, solange eine alte Tabelle vorliegt.
    """
    cols = {row[1] for row in c.execute("PRAGMA table_info(analysis_cache)").fetchall()}
    if cols and ("user_id" in cols or "text_hash" not in cols):
        c.execute("DROP TABLE analysis_cache")


def init_db() -> None:
    with _conn() as c:
        _migrate_analysis_cache(c)
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                pw_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                name TEXT,
                employees INTEGER,
                revenue_eur REAL,
                branch TEXT,
                b2c INTEGER DEFAULT 0,
                listed INTEGER DEFAULT 0,
                sites_json TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                result_json TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                requested_at TEXT NOT NULL,
                token_hash TEXT,
                expires_at TEXT,
                used_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            -- Fehlversuche beim Anmelden; persistent, damit ein Neustart
            -- des Containers keine laufende Sperre aufhebt.
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scope TEXT NOT NULL,        -- 'account' | 'ip' | 'reset_ip'
                subject TEXT NOT NULL,      -- E-Mail (klein) bzw. Quell-IP
                attempted_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_login_attempts_lookup
                ON login_attempts (scope, subject, attempted_at);
            -- Eigener Index fuers Aufraeumen: der Lookup-Index oben beginnt mit
            -- `scope` und hilft einer reinen Altersabfrage nicht.
            CREATE INDEX IF NOT EXISTS idx_login_attempts_age
                ON login_attempts (attempted_at);
            CREATE TABLE IF NOT EXISTS watchdog_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                language TEXT NOT NULL DEFAULT 'de',
                checked INTEGER NOT NULL DEFAULT 0,
                changed_json TEXT NOT NULL DEFAULT '[]',
                errors_json TEXT NOT NULL DEFAULT '[]'
            );
            -- Nutzeruebergreifend: gleiche Ausgangslage -> gleiche Begruendung,
            -- unabhaengig davon, wer sie zuerst angefordert hat.
            CREATE TABLE IF NOT EXISTS analysis_cache (
                reg_key TEXT NOT NULL,
                profile_hash TEXT NOT NULL,
                reg_hash TEXT NOT NULL,
                text_hash TEXT,
                result_json TEXT NOT NULL,
                cached_at TEXT NOT NULL,
                PRIMARY KEY (reg_key, profile_hash, reg_hash)
            );
            """
        )
        _migrate_companies(c)
        # Altlasten der Login-Bremse wegraeumen (idempotent).
        _prune(c)


# ---------- Users ----------
# Kostenfaktor fuer bcrypt. An EINER Stelle definiert, damit der Dummy-Hash
# unten nicht zurueckbleibt, wenn er je erhoeht wird (siehe _DUMMY_PW_HASH).
BCRYPT_ROUNDS = 12


def create_user(email: str, password: str) -> int:
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)).decode()
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO users (email, pw_hash, created_at) VALUES (?, ?, ?)",
            (email.lower().strip(), pw_hash, datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


# bcrypt-Hash eines zufaelligen, nirgends verwendeten Geheimnisses. Er dient
# ausschliesslich dazu, den Pfad "Adresse unbekannt" genauso lange rechnen zu
# lassen wie den Pfad "Adresse bekannt, Passwort falsch". Ohne das verraet die
# Antwortzeit (0,012 s gegen 0,27 s, Faktor 91), welche Adressen registriert sind.
#
# Der Kostenfaktor MUSS zu BCRYPT_ROUNDS passen, sonst rechnen beide Pfade
# wieder unterschiedlich lang und H4 waere still zurueck. Stimmt er nicht,
# wird der Dummy beim Start einmalig passend neu erzeugt (kostet ~0,25 s).
# `test_login_throttle.py` prueft den Gleichlauf zusaetzlich nach.
_DUMMY_PW_HASH = b"$2b$12$LOmoH0iusZ8izgFMaVdbsu5Qm6ftN2eop5FNIcwQRFRYVbhxWFbdG"
if not _DUMMY_PW_HASH.startswith(b"$2b$%02d$" % BCRYPT_ROUNDS):
    _DUMMY_PW_HASH = bcrypt.hashpw(secrets.token_bytes(32), bcrypt.gensalt(BCRYPT_ROUNDS))


def verify_user(email: str, password: str) -> Optional[int]:
    with _conn() as c:
        row = c.execute(
            "SELECT id, pw_hash FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
    if not row:
        # Kein frueher Ausstieg: gegen den Dummy-Hash rechnen, damit beide
        # Faelle gleich lange brauchen (siehe _DUMMY_PW_HASH).
        bcrypt.checkpw(password.encode(), _DUMMY_PW_HASH)
        return None
    if bcrypt.checkpw(password.encode(), row["pw_hash"].encode()):
        return row["id"]
    return None


def email_exists(email: str) -> bool:
    with _conn() as c:
        return c.execute("SELECT 1 FROM users WHERE email = ?", (email.lower().strip(),)).fetchone() is not None


def get_user_by_email(email: str) -> Optional[dict]:
    with _conn() as c:
        row = c.execute(
            "SELECT id, email, created_at FROM users WHERE email = ?",
            (email.lower().strip(),),
        ).fetchone()
    return dict(row) if row else None


def set_password(user_id: int, password: str) -> None:
    """Setzt ein neues Passwort und entwertet alle offenen Reset-Links."""
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)).decode()
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute("UPDATE users SET pw_hash = ? WHERE id = ?", (pw_hash, user_id))
        c.execute(
            "UPDATE password_resets SET used_at = ? WHERE user_id = ? AND used_at IS NULL",
            (now, user_id),
        )


def check_password(user_id: int, password: str) -> bool:
    with _conn() as c:
        row = c.execute("SELECT pw_hash FROM users WHERE id = ?", (user_id,)).fetchone()
    return bool(row) and bcrypt.checkpw(password.encode(), row["pw_hash"].encode())


# ---------- Login-Bremse (Brute-Force) ----------
# Zwei Bremsen, weil jede allein umgehbar waere:
#  * je (Konto, Quell-IP) — bremst das Durchprobieren eines Kontos;
#  * je Quell-IP ueber alle Konten — sonst klappert jemand von einer Adresse
#    aus viele Konten mit je vier Versuchen ab.
#
# Warum das Paar (Konto, IP) und NICHT das Konto allein: Eine kontoweite Sperre
# ist eine Waffe gegen den rechtmaessigen Inhaber. Nachgestellt wurde, dass rund
# 29 Versuche je Stunde — unterhalb der IP-Schwelle — ein Konto dauerhaft
# gesperrt halten; beim Admin-Konto haette das auch den Admin-Bereich zugesperrt,
# ohne Weg zurueck ausser einer Shell im Container. Mit der Bindung an die IP
# sperrt sich ein Angreifer nur selbst aus, waehrend der Inhaber von seiner
# eigenen Adresse unbehelligt hineinkommt.
#
# Restrisiko, bewusst getragen: Wer ueber viele Adressen verfuegt (Botnetz),
# umgeht die Kontobremse, weil je Adresse nur vier Versuche anfallen. Gegen ihn
# wirkt allein die IP-Bremse, die den Durchsatz je Adresse auf 30/Stunde deckelt
# — dieselbe Grenze gilt dann aber auch fuer jedes andere Ziel. Der Preis waere
# die Verfuegbarkeit des Kontos, und die wiegt hier schwerer.
#
# Bewusst KEINE dauerhafte Sperre: die Fenster gleiten, nach Ruhe loest sich
# die Sperre von selbst. Zusaetzlich gibt es einen Notausgang von aussen:
#   docker exec <container> python -m db unlock <email>
LOGIN_FAIL_WINDOW_MIN = 15   # Beobachtungsfenster je (Konto, IP)
LOGIN_FAIL_MAX = 5           # Fehlversuche in diesem Fenster, dann Sperre
LOGIN_BLOCK_BASE_SEC = 60    # erste Sperre; verdoppelt sich je weiterem Fehlversuch
LOGIN_BLOCK_MAX_SEC = 900    # Deckel: 15 Minuten

LOGIN_IP_WINDOW_MIN = 60     # Beobachtungsfenster je Quell-IP
LOGIN_IP_MAX = 30            # Fehlversuche je Stunde und IP
LOGIN_IP_BLOCK_SEC = 900     # danach 15 Minuten Ruhe ab dem letzten Versuch

# Der Reset-Token hat 256 Bit Zufall und ist praktisch nicht erratbar; diese
# Bremse verhindert deshalb kein Durchprobieren, sondern deckelt nur, wie oft
# ein unangemeldeter Endpunkt von einer Adresse aus beklopft werden kann.
# Der Aufrufer prueft den Token ZUERST — ein gueltiger Link laesst sich also
# auch dann einloesen, wenn jemand anderes hinter derselben Adresse gerade
# ungueltige Token verbraucht hat.
RESET_IP_WINDOW_MIN = 60
RESET_IP_MAX = 20
RESET_IP_BLOCK_SEC = 900

# Aelter als das laengste Fenster + laengste Sperre wird nie mehr gebraucht.
ATTEMPT_KEEP_HOURS = 3


def _parse_ts(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _attempt_stats(
    c: sqlite3.Connection, scope: str, subject: str, window_min: int
) -> tuple[int, Optional[datetime]]:
    """(Anzahl, letzter Zeitpunkt) der Fehlversuche im gleitenden Fenster."""
    since = (datetime.utcnow() - timedelta(minutes=window_min)).isoformat()
    row = c.execute(
        """SELECT COUNT(*) AS n, MAX(attempted_at) AS last
           FROM login_attempts
           WHERE scope = ? AND subject = ? AND attempted_at >= ?""",
        (scope, subject, since),
    ).fetchone()
    if not row or not row["n"]:
        return 0, None
    return int(row["n"]), _parse_ts(row["last"] or "")


def _remaining(last: Optional[datetime], block_sec: int) -> int:
    if last is None:
        return 0
    elapsed = (datetime.utcnow() - last).total_seconds()
    return max(0, int(round(block_sec - elapsed)))


def _record_attempt(c: sqlite3.Connection, scope: str, subject: str) -> None:
    c.execute(
        "INSERT INTO login_attempts (scope, subject, attempted_at) VALUES (?, ?, ?)",
        (scope, subject, datetime.utcnow().isoformat()),
    )


def _prune(c: sqlite3.Connection) -> None:
    """Abgelaufene Fehlversuche wegraeumen.

    Nutzt `idx_login_attempts_age`; ohne diesen Index waere es bei jedem
    Fehlversuch ein Volltabellenscan (der Lookup-Index beginnt mit `scope`
    und greift bei einer reinen Altersabfrage nicht).
    """
    cutoff = (datetime.utcnow() - timedelta(hours=ATTEMPT_KEEP_HOURS)).isoformat()
    c.execute("DELETE FROM login_attempts WHERE attempted_at < ?", (cutoff,))


def prune_login_attempts() -> None:
    """Raeumt abgelaufene Fehlversuche weg (idempotent, jederzeit aufrufbar)."""
    with _conn() as c:
        _prune(c)


def _account_subject(email: str, ip: str) -> str:
    """Schluessel der Kontobremse: Konto UND Quell-IP (siehe Kopfkommentar)."""
    return "{}|{}".format((email or "").lower().strip(), ip or "")


def _block_seconds(c: sqlite3.Connection, email: str, ip: str) -> int:
    """Restliche Sperrzeit in Sekunden auf einer bestehenden Verbindung."""
    remaining = 0
    mail = (email or "").lower().strip()
    if mail:
        n, last = _attempt_stats(
            c, "account", _account_subject(mail, ip), LOGIN_FAIL_WINDOW_MIN
        )
        if n >= LOGIN_FAIL_MAX:
            # Exponent gedeckelt, damit ein Ausreisser keine Riesenzahl baut.
            stufe = min(n - LOGIN_FAIL_MAX, 16)
            delay = min(LOGIN_BLOCK_BASE_SEC * (2 ** stufe), LOGIN_BLOCK_MAX_SEC)
            remaining = max(remaining, _remaining(last, delay))
    if ip:
        n, last = _attempt_stats(c, "ip", ip, LOGIN_IP_WINDOW_MIN)
        if n >= LOGIN_IP_MAX:
            remaining = max(remaining, _remaining(last, LOGIN_IP_BLOCK_SEC))
    return remaining


def login_block_seconds(email: str, ip: str) -> int:
    """Nur lesen: restliche Sperrzeit in Sekunden; 0 = Versuch waere erlaubt.

    Fuer Diagnose und Tests. Der Anmeldepfad nimmt `begin_login_attempt`,
    weil dort Pruefen und Verbuchen untrennbar zusammengehoeren.
    """
    with _conn() as c:
        return _block_seconds(c, email, ip)


def begin_login_attempt(email: str, ip: str) -> int:
    """Prueft die Sperre und verbucht den Versuch — in EINER Transaktion.

    Rueckgabe: 0 = weitermachen (der Versuch ist bereits als Fehlversuch
    verbucht), sonst die restliche Sperrzeit in Sekunden.

    Der Fehlversuch wird VOR der Passwortpruefung verbucht, und Lesen und
    Schreiben laufen unter `BEGIN IMMEDIATE`. Sonst klafft zwischen
    Zaehlerlesen und Verbuchen der komplette bcrypt-Durchlauf (~230 ms) — bei
    8 Gunicorn-Threads kamen so pro Runde acht Versuche gleichzeitig durch.
    Eine erfolgreiche Anmeldung raeumt den Eintrag gleich wieder weg
    (`clear_login_failures`), legitime Nutzer merken davon nichts.
    """
    mail = (email or "").lower().strip()
    with _conn() as c:
        c.execute("BEGIN IMMEDIATE")
        blocked = _block_seconds(c, mail, ip)
        if blocked:
            return blocked
        # Auch unbekannte Adressen zaehlen mit — sonst verriete allein das
        # Auftreten einer Sperre, dass es das Konto gibt.
        if mail:
            _record_attempt(c, "account", _account_subject(mail, ip))
        if ip:
            _record_attempt(c, "ip", ip)
        _prune(c)
    return 0


def record_login_failure(email: str, ip: str) -> None:
    """Fehlversuch verbuchen, ohne die Sperre zu pruefen (Tests, Sonderfaelle)."""
    mail = (email or "").lower().strip()
    with _conn() as c:
        if mail:
            _record_attempt(c, "account", _account_subject(mail, ip))
        if ip:
            _record_attempt(c, "ip", ip)
        _prune(c)


def clear_login_failures(email: str, ip: str | None = None) -> int:
    """Zaehler zuruecksetzen. Gibt die Zahl geloeschter Zeilen zurueck.

    Mit `ip`: nur das Paar (Konto, diese IP) — so raeumt eine erfolgreiche
    Anmeldung die eigene Adresse frei, waehrend die Sperre einer fremden
    Adresse (Angreifer) bestehen bleibt.
    Ohne `ip`: alle Adressen dieses Kontos — das ist der Notausgang
    `python -m db unlock <email>`.

    Die IP-Zaehlung ueber alle Konten bleibt in beiden Faellen stehen; wer ein
    gueltiges Konto besitzt, koennte sie sonst jederzeit selbst wegdruecken.
    """
    mail = (email or "").lower().strip()
    if not mail:
        return 0
    with _conn() as c:
        if ip is not None:
            cur = c.execute(
                "DELETE FROM login_attempts WHERE scope = 'account' AND subject = ?",
                (_account_subject(mail, ip),),
            )
        else:
            prefix = mail + "|"
            cur = c.execute(
                """DELETE FROM login_attempts
                   WHERE scope = 'account' AND substr(subject, 1, ?) = ?""",
                (len(prefix), prefix),
            )
        return cur.rowcount


def reset_token_block_seconds(ip: str) -> int:
    if not ip:
        return 0
    with _conn() as c:
        n, last = _attempt_stats(c, "reset_ip", ip, RESET_IP_WINDOW_MIN)
    if n < RESET_IP_MAX:
        return 0
    return _remaining(last, RESET_IP_BLOCK_SEC)


def record_reset_token_failure(ip: str) -> None:
    if not ip:
        return
    with _conn() as c:
        _record_attempt(c, "reset_ip", ip)


# ---------- Passwort-Reset ----------
RESET_TTL_HOURS = 24


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_reset_request(email: str) -> bool:
    """Legt ein Ticket an ('Passwort vergessen'). False, wenn es die E-Mail nicht gibt.

    Pro Nutzer bleibt höchstens ein offenes Ticket bestehen.
    """
    with _conn() as c:
        row = c.execute(
            "SELECT id FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
        if not row:
            return False
        open_ticket = c.execute(
            "SELECT 1 FROM password_resets WHERE user_id = ? AND used_at IS NULL",
            (row["id"],),
        ).fetchone()
        if not open_ticket:
            c.execute(
                "INSERT INTO password_resets (user_id, requested_at) VALUES (?, ?)",
                (row["id"], datetime.utcnow().isoformat()),
            )
        return True


def list_open_resets() -> list[dict]:
    """Offene Reset-Anfragen für die Admin-Seite, neueste zuerst."""
    with _conn() as c:
        rows = c.execute(
            """
            SELECT r.id, r.user_id, r.requested_at, r.expires_at,
                   r.token_hash IS NOT NULL AS link_issued,
                   u.email, c.name AS company
            FROM password_resets r
            JOIN users u ON u.id = r.user_id
            LEFT JOIN companies c ON c.user_id = r.user_id
            WHERE r.used_at IS NULL
            ORDER BY r.requested_at DESC
            """
        ).fetchall()
    return [dict(r) for r in rows]


def issue_reset_token(user_id: int) -> tuple[str, str]:
    """Erzeugt einen einmaligen Reset-Token. Gibt (Klartext-Token, Ablauf-ISO) zurück.

    Der Klartext wird nirgends gespeichert — nur sein SHA-256-Hash.
    """
    token = secrets.token_urlsafe(32)
    now = datetime.utcnow()
    expires = (now + timedelta(hours=RESET_TTL_HOURS)).isoformat()
    with _conn() as c:
        # Ältere offene Links desselben Nutzers entwerten.
        c.execute(
            "UPDATE password_resets SET used_at = ? WHERE user_id = ? AND used_at IS NULL",
            (now.isoformat(), user_id),
        )
        c.execute(
            """INSERT INTO password_resets (user_id, requested_at, token_hash, expires_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, now.isoformat(), _token_hash(token), expires),
        )
    return token, expires


def user_for_reset_token(token: str) -> Optional[dict]:
    """Prüft einen Token. Gibt {id, email} zurück oder None (unbekannt/verbraucht/abgelaufen)."""
    with _conn() as c:
        row = c.execute(
            """
            SELECT r.id, r.expires_at, u.id AS user_id, u.email
            FROM password_resets r
            JOIN users u ON u.id = r.user_id
            WHERE r.token_hash = ? AND r.used_at IS NULL
            """,
            (_token_hash(token),),
        ).fetchone()
    if not row:
        return None
    if datetime.utcnow().isoformat() > (row["expires_at"] or ""):
        return None
    return {"id": row["user_id"], "email": row["email"]}


# ---------- Company ----------
def _known(values, allowed) -> list[str]:
    """Nur Werte, die es in der aktuellen Auswahlliste noch gibt (Reihenfolge der Liste)."""
    chosen = set(values or ())
    return [v for v in allowed if v in chosen]


def get_company(user_id: int) -> Optional[dict]:
    with _conn() as c:
        row = c.execute("SELECT * FROM companies WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        return None
    data = dict(row)
    data["sites"] = _rename_sites(json.loads(data.pop("sites_json") or "[]"))
    # Auswahllisten: nur noch bekannte Werte durchlassen. Die Produkt-
    # kategorien wurden am 02.09.2026 vollstaendig ausgetauscht; aeltere
    # Profile tragen Werte, die es nicht mehr gibt ("Kaffee / Kakao",
    # "Keine physischen Produkte ..."). Wuerden sie durchgereicht, stuenden sie
    # im LLM-Prompt und im Cache-Schluessel, waeren im Formular aber unsichtbar
    # und beim naechsten Speichern verschwunden — der Nutzer saehe also eine
    # Begruendung zu einer Angabe, die er nicht mehr machen kann. Deshalb hier
    # zentral herausfiltern; gespeichert bleiben sie, bis der Nutzer das
    # naechste Mal speichert.
    data["product_categories"] = _known(
        json.loads(data.pop("product_categories_json") or "[]"), PRODUCT_CATEGORIES)
    data["value_chain_roles"] = _known(
        json.loads(data.pop("value_chain_roles_json") or "[]"), VALUE_CHAIN_ROLES)
    data["materials"] = _known(
        json.loads(data.pop("materials_json") or "[]"), MATERIALS)
    data["sales_markets"] = _known(
        json.loads(data.pop("sales_markets_json") or "[]"), SALES_MARKETS)
    data["b2c"] = bool(data.get("b2c"))
    data["listed"] = bool(data.get("listed"))
    data["env_claims"] = bool(data.get("env_claims"))
    data["eu_importer"] = bool(data.get("eu_importer"))
    return data


def upsert_company(user_id: int, data: dict) -> None:
    sites_json = json.dumps(_rename_sites(data.get("sites", [])), ensure_ascii=False)
    products_json = json.dumps(
        _known(data.get("product_categories"), PRODUCT_CATEGORIES), ensure_ascii=False)
    roles_json = json.dumps(
        _known(data.get("value_chain_roles"), VALUE_CHAIN_ROLES), ensure_ascii=False)
    materials_json = json.dumps(
        _known(data.get("materials"), MATERIALS), ensure_ascii=False)
    markets_json = json.dumps(
        _known(data.get("sales_markets"), SALES_MARKETS), ensure_ascii=False)
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute(
            """
            INSERT INTO companies (
                user_id, name, employees, revenue_eur, branch, b2c, listed,
                sites_json, updated_at, balance_sheet_eur, legal_form, group_role,
                env_claims, product_categories_json, employees_de, language,
                eu_importer, value_chain_roles_json, materials_json,
                revenue_eu_eur, sales_markets_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name=excluded.name,
                employees=excluded.employees,
                revenue_eur=excluded.revenue_eur,
                branch=excluded.branch,
                b2c=excluded.b2c,
                listed=excluded.listed,
                sites_json=excluded.sites_json,
                updated_at=excluded.updated_at,
                balance_sheet_eur=excluded.balance_sheet_eur,
                legal_form=excluded.legal_form,
                group_role=excluded.group_role,
                env_claims=excluded.env_claims,
                product_categories_json=excluded.product_categories_json,
                employees_de=excluded.employees_de,
                language=excluded.language,
                eu_importer=excluded.eu_importer,
                value_chain_roles_json=excluded.value_chain_roles_json,
                materials_json=excluded.materials_json,
                revenue_eu_eur=excluded.revenue_eu_eur,
                sales_markets_json=excluded.sales_markets_json
            """,
            (
                user_id,
                data.get("name"),
                int(data.get("employees") or 0),
                float(data.get("revenue_eur") or 0),
                data.get("branch"),
                1 if data.get("b2c") else 0,
                1 if data.get("listed") else 0,
                sites_json,
                now,
                float(data.get("balance_sheet_eur") or 0),
                data.get("legal_form"),
                data.get("group_role"),
                1 if data.get("env_claims") else 0,
                products_json,
                int(data.get("employees_de") or 0),
                data.get("language") or "de",
                1 if data.get("eu_importer") else 0,
                roles_json,
                materials_json,
                float(data.get("revenue_eu_eur") or 0),
                markets_json,
            ),
        )


# ---------- Analyses ----------
def save_analysis(user_id: int, result: list[dict]) -> int:
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO analyses (user_id, created_at, result_json) VALUES (?, ?, ?)",
            (user_id, datetime.utcnow().isoformat(), json.dumps(result, ensure_ascii=False)),
        )
        return cur.lastrowid


# ---------- Cache ----------
def get_cache(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], list[dict]]:
    """Cache-Zeilen zu (reg_key, profile_hash)-Paaren, je Paar neueste zuerst.

    Pro Paar koennen mehrere Zeilen liegen (eine je Gesetzesstand); welche davon
    gilt, entscheidet `llm._cache_hit`.
    """
    out: dict[tuple[str, str], list[dict]] = {}
    with _conn() as c:
        for reg_key, profile_hash in pairs:
            rows = c.execute(
                "SELECT reg_hash, text_hash, result_json, cached_at FROM analysis_cache "
                "WHERE reg_key = ? AND profile_hash = ? ORDER BY cached_at DESC",
                (reg_key, profile_hash),
            ).fetchall()
            out[(reg_key, profile_hash)] = [
                {
                    "reg_hash": row["reg_hash"],
                    "text_hash": row["text_hash"],
                    "cached_at": row["cached_at"],
                    "result": json.loads(row["result_json"]),
                }
                for row in rows
            ]
    return out


def put_cache(profile_hash: str, reg_key: str, reg_hash: str, text_hash: Optional[str],
              result: dict) -> None:
    with _conn() as c:
        c.execute(
            """
            INSERT INTO analysis_cache (reg_key, profile_hash, reg_hash, text_hash,
                                        result_json, cached_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(reg_key, profile_hash, reg_hash) DO UPDATE SET
                text_hash=excluded.text_hash,
                result_json=excluded.result_json,
                cached_at=excluded.cached_at
            """,
            (reg_key, profile_hash, reg_hash, text_hash,
             json.dumps(result, ensure_ascii=False), datetime.utcnow().isoformat()),
        )


# ---------- Watchdog ----------
def start_watchdog_run(language: str = "de") -> int:
    """Legt einen Lauf an und liefert dessen ID."""
    init_db()
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO watchdog_runs (started_at, language) VALUES (?, ?)",
            (datetime.utcnow().isoformat(), language),
        )
        return cur.lastrowid


def finish_watchdog_run(run_id: int, checked: int, changed: list[dict],
                        errors: list[dict]) -> None:
    """Schliesst einen Lauf ab.

    `changed`: [{reg_key, previous_hash, text_hash, summary}]
    `errors`:  [{reg_key, error}]
    """
    with _conn() as c:
        c.execute(
            "UPDATE watchdog_runs SET finished_at = ?, checked = ?, changed_json = ?, "
            "errors_json = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), checked,
             json.dumps(changed, ensure_ascii=False),
             json.dumps(errors, ensure_ascii=False), run_id),
        )


def _watchdog_row(row) -> dict:
    return {
        "id": row["id"],
        "started_at": row["started_at"],
        "finished_at": row["finished_at"],
        "language": row["language"],
        "checked": row["checked"],
        "changed": json.loads(row["changed_json"] or "[]"),
        "errors": json.loads(row["errors_json"] or "[]"),
    }


def latest_watchdog_run() -> Optional[dict]:
    init_db()
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM watchdog_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return _watchdog_row(row) if row else None


def watchdog_changes_by_reg(limit_runs: int = 50) -> dict[str, dict]:
    """Je Regulierung die zuletzt erkannte Aenderung (inkl. LLM-Zusammenfassung)."""
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT id, started_at, changed_json FROM watchdog_runs "
            "ORDER BY id DESC LIMIT ?",
            (limit_runs,),
        ).fetchall()
    out: dict[str, dict] = {}
    for row in rows:  # neueste zuerst — der erste Treffer gewinnt
        for entry in json.loads(row["changed_json"] or "[]"):
            key = entry.get("reg_key")
            if key and key not in out:
                out[key] = {**entry, "run_at": row["started_at"]}
    return out


def latest_analysis(user_id: int) -> Optional[dict]:
    with _conn() as c:
        row = c.execute(
            "SELECT id, created_at, result_json FROM analyses WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "result": json.loads(row["result_json"]),
    }


# ---------------------------------------------------------------------------
# Notausgang von der Kommandozeile
# ---------------------------------------------------------------------------
def _cli(argv: list[str]) -> int:
    """`python -m db unlock <email>` — hebt die Login-Sperre eines Kontos auf.

    Gedacht fuer den Fall, dass niemand mehr hineinkommt:
        docker exec <container> python -m db unlock chef@example.org
    Die Kontobremse haengt am Paar (Konto, IP); der Aufruf raeumt alle
    Adressen dieses Kontos frei. Die IP-Bremse bleibt bestehen.
    """
    if len(argv) != 2 or argv[0] != "unlock":
        print("Aufruf: python -m db unlock <email>")
        return 2
    init_db()
    email = argv[1]
    geloescht = clear_login_failures(email)
    offen = login_block_seconds(email, "")
    print(f"Datenbank: {DB_PATH}")
    print(f"{email}: {geloescht} Fehlversuch-Eintraege geloescht.")
    print("Kontosperre aufgehoben." if offen == 0 else f"Achtung: weiterhin {offen} s gesperrt.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(_cli(sys.argv[1:]))
