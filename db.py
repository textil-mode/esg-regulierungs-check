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
]


def _migrate_companies(c: sqlite3.Connection) -> None:
    cols = {row[1] for row in c.execute("PRAGMA table_info(companies)").fetchall()}
    for col, ddl in COMPANY_EXTRA_COLUMNS:
        if col not in cols:
            c.execute(f"ALTER TABLE companies ADD COLUMN {col} {ddl}")


def init_db() -> None:
    with _conn() as c:
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
            CREATE TABLE IF NOT EXISTS watchdog_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                language TEXT NOT NULL DEFAULT 'de',
                checked INTEGER NOT NULL DEFAULT 0,
                changed_json TEXT NOT NULL DEFAULT '[]',
                errors_json TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS analysis_cache (
                user_id INTEGER NOT NULL,
                profile_hash TEXT NOT NULL,
                reg_key TEXT NOT NULL,
                reg_hash TEXT NOT NULL,
                result_json TEXT NOT NULL,
                cached_at TEXT NOT NULL,
                PRIMARY KEY (user_id, profile_hash, reg_key),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
        _migrate_companies(c)


# ---------- Users ----------
def create_user(email: str, password: str) -> int:
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO users (email, pw_hash, created_at) VALUES (?, ?, ?)",
            (email.lower().strip(), pw_hash, datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


def verify_user(email: str, password: str) -> Optional[int]:
    with _conn() as c:
        row = c.execute(
            "SELECT id, pw_hash FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
    if not row:
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
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
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
def get_company(user_id: int) -> Optional[dict]:
    with _conn() as c:
        row = c.execute("SELECT * FROM companies WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        return None
    data = dict(row)
    data["sites"] = json.loads(data.pop("sites_json") or "[]")
    data["product_categories"] = json.loads(data.pop("product_categories_json") or "[]")
    data["b2c"] = bool(data.get("b2c"))
    data["listed"] = bool(data.get("listed"))
    data["env_claims"] = bool(data.get("env_claims"))
    data["eu_importer"] = bool(data.get("eu_importer"))
    return data


def upsert_company(user_id: int, data: dict) -> None:
    sites_json = json.dumps(data.get("sites", []), ensure_ascii=False)
    products_json = json.dumps(data.get("product_categories", []), ensure_ascii=False)
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute(
            """
            INSERT INTO companies (
                user_id, name, employees, revenue_eur, branch, b2c, listed,
                sites_json, updated_at, balance_sheet_eur, legal_form, group_role,
                env_claims, product_categories_json, employees_de, language,
                eu_importer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                eu_importer=excluded.eu_importer
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
def get_cache(user_id: int, profile_hash: str) -> dict[str, dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT reg_key, reg_hash, result_json, cached_at FROM analysis_cache "
            "WHERE user_id = ? AND profile_hash = ?",
            (user_id, profile_hash),
        ).fetchall()
    return {
        row["reg_key"]: {
            "reg_hash": row["reg_hash"],
            "cached_at": row["cached_at"],
            "result": json.loads(row["result_json"]),
        }
        for row in rows
    }


def put_cache(user_id: int, profile_hash: str, reg_key: str, reg_hash: str, result: dict) -> None:
    with _conn() as c:
        c.execute(
            """
            INSERT INTO analysis_cache (user_id, profile_hash, reg_key, reg_hash, result_json, cached_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, profile_hash, reg_key) DO UPDATE SET
                reg_hash=excluded.reg_hash,
                result_json=excluded.result_json,
                cached_at=excluded.cached_at
            """,
            (user_id, profile_hash, reg_key, reg_hash, json.dumps(result, ensure_ascii=False),
             datetime.utcnow().isoformat()),
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
