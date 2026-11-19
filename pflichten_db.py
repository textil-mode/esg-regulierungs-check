"""Pflichten-Plan: Datenmodell, Startbestand und Lesezugriffe.

Der Katalog der Schritte (`pflicht_schritte` + Texte je Sprache) loest die
festen ersten Schritte aus `regulations.FIRST_STEPS_BY_REG_KEY` /
`i18n.FIRST_STEPS` ab. Der Startbestand wird einmalig aus dem Code
uebernommen (`seed_aus_code`); `herkunft_key` merkt sich den alten
Schluessel, damit der Abgleich idempotent bleibt.

Nutzerbezogene Tabellen haengen per `ON DELETE CASCADE` am Konto, nur
`pflicht_hinweise` hat laut Datenmodell keinen Fremdschluessel — die loescht
`db._delete_account_rows` selbst per user_id.

Importreihenfolge: `db` importiert dieses Modul erst innerhalb von
`init_db`, damit `import db` allein ohne Kreisimport funktioniert.
"""
from __future__ import annotations

import os
import sqlite3

import db
import i18n
import regulations as regs

SPRACHEN = ("de", "en", "es", "fr", "it", "zh")
TEXTFELDER = ("titel", "beschreibung", "daten")

SCHEMA = """
CREATE TABLE IF NOT EXISTS pflicht_schritte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_key TEXT NOT NULL,
    sortierung INTEGER NOT NULL DEFAULT 0,
    rolle TEXT NOT NULL DEFAULT '',
    frist_typ TEXT NOT NULL DEFAULT 'keine',   -- relativ | fest | jaehrlich | keine
    frist_wert TEXT NOT NULL DEFAULT '',
    link TEXT,
    quelle TEXT,
    aktiv INTEGER NOT NULL DEFAULT 1,
    version INTEGER NOT NULL DEFAULT 1,
    geprueft_am TEXT,
    geaendert_am TEXT,                          -- nur bei wesentlicher Freigabe
    herkunft_key TEXT UNIQUE                    -- alter Schluessel, z. B. eudr_1
);
CREATE INDEX IF NOT EXISTS idx_pflicht_schritte_reg
    ON pflicht_schritte (reg_key, sortierung);
CREATE TABLE IF NOT EXISTS pflicht_schritt_texte (
    schritt_id INTEGER NOT NULL,
    sprache TEXT NOT NULL,
    titel TEXT NOT NULL DEFAULT '',
    beschreibung TEXT NOT NULL DEFAULT '',
    daten TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (schritt_id, sprache),
    FOREIGN KEY(schritt_id) REFERENCES pflicht_schritte(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS pflicht_schritt_versionen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schritt_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    inhalt_json TEXT NOT NULL,
    geaendert_am TEXT NOT NULL,
    geaendert_von TEXT,
    vorschlag_id INTEGER
);
CREATE TABLE IF NOT EXISTS pflicht_vorschlaege (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_key TEXT NOT NULL,
    schritt_id INTEGER,
    art TEXT NOT NULL,              -- neu | aendern | deaktivieren
    ausloeser TEXT NOT NULL,        -- watchdog | anwendungsbeginn | startbestand | hand
    ausloeser_ref TEXT,
    vorher_json TEXT,
    nachher_json TEXT,
    beleg TEXT,
    begruendung TEXT,
    status TEXT NOT NULL DEFAULT 'offen',   -- offen | freigegeben | verworfen
    erstellt_am TEXT NOT NULL,
    entschieden_am TEXT,
    entschieden_von TEXT,
    grund TEXT
);
CREATE INDEX IF NOT EXISTS idx_pflicht_vorschlaege_status
    ON pflicht_vorschlaege (status, reg_key);
CREATE TABLE IF NOT EXISTS nutzer_pflichten (
    user_id INTEGER NOT NULL,
    reg_key TEXT NOT NULL,
    erste_feststellung TEXT,
    entfallen_am TEXT,
    letzter_gilt_ab TEXT,
    PRIMARY KEY (user_id, reg_key),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS nutzer_schritte (
    user_id INTEGER NOT NULL,
    schritt_id INTEGER NOT NULL,
    zustaendig TEXT,
    gesehen_version INTEGER,
    PRIMARY KEY (user_id, schritt_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS nutzer_erledigt (
    user_id INTEGER NOT NULL,
    schritt_id INTEGER NOT NULL,
    periode TEXT NOT NULL DEFAULT '',   -- '' oder Jahr 'YYYY'
    erledigt_am TEXT,
    PRIMARY KEY (user_id, schritt_id, periode),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS pflicht_erinnerungen (
    user_id INTEGER NOT NULL,
    schritt_id INTEGER NOT NULL,
    art TEXT NOT NULL,                  -- 30 | 7
    frist TEXT NOT NULL,
    gesendet_am TEXT,
    PRIMARY KEY (user_id, schritt_id, art, frist),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS pflicht_hinweise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reg_key TEXT NOT NULL,
    art TEXT NOT NULL,                  -- inhalt | datum
    text_de TEXT,
    erstellt_am TEXT NOT NULL,
    gesendet_am TEXT
);
CREATE INDEX IF NOT EXISTS idx_pflicht_hinweise_user
    ON pflicht_hinweise (user_id);
CREATE TABLE IF NOT EXISTS pflicht_einstellungen (
    schluessel TEXT PRIMARY KEY,
    wert TEXT
);
"""


def init_schema(c: sqlite3.Connection) -> None:
    """Legt alle Tabellen des Pflichten-Plans an (idempotent)."""
    c.executescript(SCHEMA)


def seed_aus_code(c: sqlite3.Connection) -> int:
    """Uebernimmt fehlende erste Schritte aus dem Code als Startbestand.

    Je Schluessel aus `FIRST_STEPS_BY_REG_KEY` genau ein Schritt; vorhandene
    (`herkunft_key` bekannt) bleiben unberuehrt, auch wenn sie inzwischen
    bearbeitet oder deaktiviert sind. Rueckgabe: Anzahl neu angelegter.
    """
    vorhanden = {r[0] for r in c.execute(
        "SELECT herkunft_key FROM pflicht_schritte WHERE herkunft_key IS NOT NULL")}
    neu = 0
    for reg_key, keys in regs.FIRST_STEPS_BY_REG_KEY.items():
        link = regs.first_steps_link(reg_key)
        url = link.get("url") if link else None
        for pos, key in enumerate(keys, start=1):
            if key in vorhanden:
                continue
            cur = c.execute(
                "INSERT INTO pflicht_schritte (reg_key, sortierung, rolle, frist_typ,"
                " frist_wert, link, quelle, aktiv, version, geprueft_am, geaendert_am,"
                " herkunft_key) VALUES (?, ?, '', 'keine', '', ?, NULL, 1, 1, NULL, NULL, ?)",
                (reg_key, pos, url, key),
            )
            sid = cur.lastrowid
            for lang, titel in i18n.FIRST_STEPS.get(key, {}).items():
                c.execute(
                    "INSERT INTO pflicht_schritt_texte (schritt_id, sprache, titel,"
                    " beschreibung, daten) VALUES (?, ?, ?, '', '')",
                    (sid, lang, titel),
                )
            neu += 1
    return neu


# ---------- Einstellungen ----------

def einstellung(schluessel: str, standard: str = "") -> str:
    with db._conn() as c:
        row = c.execute("SELECT wert FROM pflicht_einstellungen WHERE schluessel = ?",
                        (schluessel,)).fetchone()
    return row["wert"] if row and row["wert"] is not None else standard


def setze_einstellung(schluessel: str, wert: str) -> None:
    with db._conn() as c:
        c.execute(
            "INSERT INTO pflicht_einstellungen (schluessel, wert) VALUES (?, ?)"
            " ON CONFLICT(schluessel) DO UPDATE SET wert = excluded.wert",
            (schluessel, wert),
        )


def funktion_aktiv() -> bool:
    """Env `PFLICHTEN_PLAN=aus` schaltet die ganze Funktion ab (Legacy-Container)."""
    return os.getenv("PFLICHTEN_PLAN", "").lower() != "aus"


# ---------- Lesen ----------

def _texte(c: sqlite3.Connection, ids: list[int]) -> dict[int, dict[str, dict[str, str]]]:
    if not ids:
        return {}
    marks = ",".join("?" * len(ids))
    out: dict[int, dict[str, dict[str, str]]] = {}
    for r in c.execute(
        f"SELECT schritt_id, sprache, titel, beschreibung, daten FROM pflicht_schritt_texte"
        f" WHERE schritt_id IN ({marks})", ids,
    ):
        out.setdefault(r["schritt_id"], {})[r["sprache"]] = {
            f: r[f] or "" for f in TEXTFELDER}
    return out


def _mit_sprache(zeile: dict, texte: dict[str, dict[str, str]], lang: str) -> dict:
    eigen = texte.get(lang, {})
    de = texte.get("de", {})
    for f in TEXTFELDER:
        zeile[f] = eigen.get(f) or de.get(f, "")
    return zeile


def schritte_fuer(reg_key: str, lang: str, nur_aktiv: bool = True) -> list[dict]:
    """Schritte einer Regulierung in Sortierfolge, Texte in `lang` (Rueckfall `de`)."""
    sql = "SELECT * FROM pflicht_schritte WHERE reg_key = ?"
    if nur_aktiv:
        sql += " AND aktiv = 1"
    sql += " ORDER BY sortierung, id"
    with db._conn() as c:
        rows = [dict(r) for r in c.execute(sql, (reg_key,))]
        texte = _texte(c, [r["id"] for r in rows])
    return [_mit_sprache(r, texte.get(r["id"], {}), lang) for r in rows]


def schritt(schritt_id: int) -> dict | None:
    """Ein Schritt mit allen Texten: `texte = {lang: {titel, beschreibung, daten}}`."""
    with db._conn() as c:
        row = c.execute("SELECT * FROM pflicht_schritte WHERE id = ?",
                        (schritt_id,)).fetchone()
        if not row:
            return None
        out = dict(row)
        out["texte"] = _texte(c, [schritt_id]).get(schritt_id, {})
    return out
