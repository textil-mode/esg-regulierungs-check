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

import json
import os
import sqlite3
from datetime import date

import db
import i18n
import regulations as regs

SPRACHEN = ("de", "en", "es", "fr", "it", "zh")

# Fest hinterlegte Haupt-Admins (Stamm-Admins). Hier statt in app.py, damit
# auch der Watchdog sie ohne Import der Flask-App kennt (KI-Vorschlaege
# melden sich per Mail an genau diese Adressen). app.ADMIN_EMAILS liest von hier.
STAMM_ADMINS = frozenset({"mschuckert@textil-mode.de"})
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


# ---------- Nutzerzustand ----------

ZUSTAENDIG_MAX = 120
_PLAN_JA = ("ja", "moeglich")


def sync_pflichten(user_id: int, aktuelle: dict[str, str], today) -> None:
    """Gleicht `nutzer_pflichten` mit dem letzten Pruefergebnis ab.

    `ja`/`moeglich`: Zeile anlegen oder `entfallen_am` zuruecksetzen;
    `nein`: `entfallen_am = today`, falls noch leer; `error` (und alles
    Unbekannte): Zustand bleibt, wie er ist.
    """
    tag = today.isoformat()[:10]
    with db._conn() as c:
        for reg_key, applies in aktuelle.items():
            if applies in _PLAN_JA:
                c.execute(
                    "INSERT INTO nutzer_pflichten (user_id, reg_key, erste_feststellung,"
                    " entfallen_am) VALUES (?, ?, ?, NULL)"
                    " ON CONFLICT(user_id, reg_key) DO UPDATE SET entfallen_am = NULL",
                    (user_id, reg_key, tag),
                )
            elif applies == "nein":
                c.execute(
                    "UPDATE nutzer_pflichten SET entfallen_am = ?"
                    " WHERE user_id = ? AND reg_key = ? AND entfallen_am IS NULL",
                    (tag, user_id, reg_key),
                )


def nutzer_pflichten(user_id: int) -> list[dict]:
    with db._conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM nutzer_pflichten WHERE user_id = ? ORDER BY reg_key", (user_id,))]


def setze_erledigt(user_id: int, schritt_id: int, periode: str, erledigt: bool, today) -> None:
    """Haekchen setzen (Datum `today`) oder entfernen; `periode` '' oder 'YYYY'."""
    with db._conn() as c:
        if erledigt:
            c.execute(
                "INSERT INTO nutzer_erledigt (user_id, schritt_id, periode, erledigt_am)"
                " VALUES (?, ?, ?, ?) ON CONFLICT(user_id, schritt_id, periode)"
                " DO UPDATE SET erledigt_am = excluded.erledigt_am",
                (user_id, schritt_id, periode or "", today.isoformat()[:10]),
            )
            # Wer abhakt, hat den aktuellen Stand gesehen: "geaendert" erst nach
            # einer spaeteren Freigabe (neue Version).
            c.execute(
                "INSERT INTO nutzer_schritte (user_id, schritt_id, gesehen_version)"
                " SELECT ?, id, version FROM pflicht_schritte WHERE id = ?"
                " ON CONFLICT(user_id, schritt_id) DO UPDATE SET"
                " gesehen_version = excluded.gesehen_version",
                (user_id, schritt_id),
            )
        else:
            c.execute(
                "DELETE FROM nutzer_erledigt WHERE user_id = ? AND schritt_id = ?"
                " AND periode = ?", (user_id, schritt_id, periode or ""))


def setze_zustaendig(user_id: int, schritt_id: int, text: str) -> None:
    """Freitext 'Zustaendig', getrimmt und auf 120 Zeichen gekuerzt; leer = NULL."""
    wert = (text or "").strip()[:ZUSTAENDIG_MAX].strip() or None
    with db._conn() as c:
        c.execute(
            "INSERT INTO nutzer_schritte (user_id, schritt_id, zustaendig) VALUES (?, ?, ?)"
            " ON CONFLICT(user_id, schritt_id) DO UPDATE SET zustaendig = excluded.zustaendig",
            (user_id, schritt_id, wert),
        )


def markiere_gesehen(user_id: int, schritt_id: int, version: int) -> None:
    with db._conn() as c:
        c.execute(
            "INSERT INTO nutzer_schritte (user_id, schritt_id, gesehen_version) VALUES (?, ?, ?)"
            " ON CONFLICT(user_id, schritt_id) DO UPDATE SET"
            " gesehen_version = excluded.gesehen_version",
            (user_id, schritt_id, version),
        )


def nutzer_zustand(user_id: int) -> tuple[dict[int, dict], dict[int, dict[str, str]]]:
    """(`nutzer_schritte` je schritt_id, {schritt_id: {periode: erledigt_am}})."""
    with db._conn() as c:
        schritte = {r["schritt_id"]: dict(r) for r in c.execute(
            "SELECT * FROM nutzer_schritte WHERE user_id = ?", (user_id,))}
        erledigt: dict[int, dict[str, str]] = {}
        for r in c.execute(
            "SELECT schritt_id, periode, erledigt_am FROM nutzer_erledigt WHERE user_id = ?",
            (user_id,),
        ):
            erledigt.setdefault(r["schritt_id"], {})[r["periode"]] = r["erledigt_am"]
    return schritte, erledigt


# ---------- Vorschlaege und Freigabe ----------

FRIST_TYPEN = ("relativ", "fest", "jaehrlich", "keine")
SCHRITT_FELDER = ("rolle", "frist_typ", "frist_wert", "link", "quelle", "sortierung")
VORSCHLAG_ARTEN = ("neu", "aendern", "deaktivieren")
AUSLOESER = ("watchdog", "anwendungsbeginn", "startbestand", "hand")


def pruefe_felder(felder: dict, today) -> list[str]:
    """Prueft Schrittfelder (Admin-Eingabe oder KI-Vorschlag); Rueckgabe: Fehlertexte.

    Nur vorhandene Felder werden geprueft (fehlend = unveraendert). Der
    Frist-Wert wird gegen `pflichten.frist_fuer` gehalten: stuft der ihn als
    `keine` ein, obwohl der Typ etwas anderes sagt, ist er unbrauchbar.
    """
    import pflichten

    fehler = []
    if "rolle" in felder and (felder["rolle"] or "") not in ("", *pflichten.ROLLEN):
        fehler.append(f"Unbekannte Rolle: {felder['rolle']!r}")
    typ = felder.get("frist_typ")
    if "frist_typ" in felder and typ not in FRIST_TYPEN:
        fehler.append(f"Unbekannter Frist-Typ: {typ!r}")
    elif typ and typ != "keine":
        wert = felder.get("frist_wert") or ""
        # Anker weit in der Zukunft, damit 'relativ' nicht als 'laufend' gilt.
        probe = pflichten.frist_fuer(typ, wert, "01.01.2999", today)
        if probe["art"] == "keine":
            fehler.append(f"Frist-Wert {wert!r} passt nicht zum Typ {typ!r}")
    link = (felder.get("link") or "").strip()
    if link and not link.lower().startswith(("http://", "https://")):
        fehler.append("Link muss mit http:// oder https:// beginnen")
    if "sortierung" in felder:
        try:
            int(felder["sortierung"])
        except (TypeError, ValueError):
            fehler.append("Sortierung muss eine Zahl sein")
    return fehler


def _schritt_snapshot(c: sqlite3.Connection, schritt_id: int) -> dict | None:
    row = c.execute("SELECT * FROM pflicht_schritte WHERE id = ?", (schritt_id,)).fetchone()
    if not row:
        return None
    out = {f: row[f] for f in (*SCHRITT_FELDER, "reg_key", "aktiv", "version")}
    out["texte"] = _texte(c, [schritt_id]).get(schritt_id, {})
    return out


def neuer_vorschlag(reg_key: str, art: str, ausloeser: str, nachher: dict, *,
                    schritt_id: int | None = None, ausloeser_ref: str = "",
                    beleg: str = "", begruendung: str = "") -> int:
    """Legt einen offenen Vorschlag an; `vorher_json` = aktueller Stand des Schritts."""
    if art not in VORSCHLAG_ARTEN:
        raise ValueError(f"unbekannte Art: {art!r}")
    if ausloeser not in AUSLOESER:
        raise ValueError(f"unbekannter Ausloeser: {ausloeser!r}")
    if art != "neu" and schritt_id is None:
        raise ValueError("aendern/deaktivieren braucht schritt_id")
    with db._conn() as c:
        vorher = None
        if art != "neu":
            vorher = _schritt_snapshot(c, schritt_id)
            if vorher is None or vorher["reg_key"] != reg_key:
                raise ValueError(f"Schritt {schritt_id} gehoert nicht zu {reg_key}")
        cur = c.execute(
            "INSERT INTO pflicht_vorschlaege (reg_key, schritt_id, art, ausloeser,"
            " ausloeser_ref, vorher_json, nachher_json, beleg, begruendung, status,"
            " erstellt_am) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'offen', ?)",
            (reg_key, None if art == "neu" else schritt_id, art, ausloeser, ausloeser_ref,
             json.dumps(vorher, ensure_ascii=False) if vorher is not None else None,
             json.dumps(nachher or {}, ensure_ascii=False), beleg, begruendung,
             date.today().isoformat()),
        )
        return cur.lastrowid


def ist_bestaetigung(v: dict) -> bool:
    """`aendern` ohne Inhalt: bestaetigt den Schritt unveraendert (Startbestand)."""
    nachher = v.get("nachher") or {}
    return (v.get("art") == "aendern"
            and not any(k in nachher for k in SCHRITT_FELDER)
            and not any(f for f in (nachher.get("texte") or {}).values()))


def _vorschlag_dict(row: sqlite3.Row) -> dict:
    out = dict(row)
    out["vorher"] = json.loads(row["vorher_json"]) if row["vorher_json"] else None
    out["nachher"] = json.loads(row["nachher_json"]) if row["nachher_json"] else {}
    return out


def offene_vorschlaege() -> list[dict]:
    with db._conn() as c:
        return [_vorschlag_dict(r) for r in c.execute(
            "SELECT * FROM pflicht_vorschlaege WHERE status = 'offen'"
            " ORDER BY reg_key, erstellt_am, id")]


def vorschlag(vid: int) -> dict | None:
    with db._conn() as c:
        row = c.execute("SELECT * FROM pflicht_vorschlaege WHERE id = ?", (vid,)).fetchone()
    return _vorschlag_dict(row) if row else None


def _zusammenfuehren(nachher: dict, aenderungen: dict | None) -> dict:
    """`aenderungen` ueberschreibt `nachher`; Texte je Sprache und Feld."""
    out = {k: v for k, v in (nachher or {}).items() if k != "texte"}
    texte = {lang: dict(f or {}) for lang, f in ((nachher or {}).get("texte") or {}).items()}
    for k, v in (aenderungen or {}).items():
        if k == "texte":
            for lang, felder in (v or {}).items():
                texte.setdefault(lang, {}).update(felder or {})
        else:
            out[k] = v
    if texte:
        out["texte"] = texte
    return out


def _schreibe_texte(c: sqlite3.Connection, sid: int, texte: dict) -> None:
    for lang, felder in texte.items():
        if lang not in SPRACHEN:
            continue
        felder = {f: str(felder[f] or "") for f in TEXTFELDER if f in (felder or {})}
        if not felder:
            continue
        c.execute("INSERT OR IGNORE INTO pflicht_schritt_texte (schritt_id, sprache)"
                  " VALUES (?, ?)", (sid, lang))
        sets = ", ".join(f"{f} = ?" for f in felder)
        c.execute(f"UPDATE pflicht_schritt_texte SET {sets} WHERE schritt_id = ? AND sprache = ?",
                  (*felder.values(), sid, lang))


_HINWEIS_TEXT = {"neu": "Neuer Schritt", "aendern": "Schritt geaendert",
                 "deaktivieren": "Schritt entfaellt"}


NICHT_OFFEN = "nicht mehr offen"


def _link_normalisieren(link):
    """Leerzeichen weg, Schema klein (`HTTPS://` -> `https://`); leer -> None."""
    link = (link or "").strip()
    if not link:
        return None
    teil = link.split(":", 1)
    return teil[0].lower() + ":" + teil[1] if len(teil) == 2 else link


def freigeben(vid: int, admin_email: str, aenderungen: dict | None, today) -> bool:
    """Wendet einen offenen Vorschlag an; Kurzform von `freigeben_mit_grund`."""
    return freigeben_mit_grund(vid, admin_email, aenderungen, today)[0]


def freigeben_mit_grund(vid: int, admin_email: str, aenderungen: dict | None,
                        today) -> tuple[bool, str]:
    """Wendet einen offenen Vorschlag an — atomar und hoechstens einmal.

    Alles laeuft in einer Transaktion (`BEGIN IMMEDIATE`), der Status wird
    darin geprueft: ein zweiter Aufruf (Doppelklick, zweiter Tab) liefert
    `(False, NICHT_OFFEN)` und aendert nichts. Ungueltige Felder, ein leerer
    deutscher Titel oder ein verschwundener Schritt liefern `(False,
    "ungueltig: <Grund>")`, ebenfalls mit Rollback. Erfolg: `(True, "")`.
    """
    tag = today.isoformat()[:10]
    c = db._conn()
    c.isolation_level = None  # Transaktion selbst steuern

    def abbruch(grund: str) -> tuple[bool, str]:
        c.execute("ROLLBACK")
        return False, grund

    try:
        c.execute("BEGIN IMMEDIATE")
        row = c.execute("SELECT * FROM pflicht_vorschlaege WHERE id = ? AND status = 'offen'",
                        (vid,)).fetchone()
        if not row:
            return abbruch(NICHT_OFFEN)
        v = _vorschlag_dict(row)
        alt = None
        if v["art"] != "neu":
            alt = _schritt_snapshot(c, v["schritt_id"])
            if alt is None:
                return abbruch("ungültig: Schritt existiert nicht mehr")
        daten = _zusammenfuehren(v["nachher"], aenderungen)
        if ist_bestaetigung({"art": v["art"], "nachher": daten}):
            # Bestaetigung ohne Aenderung: nur geprueft_am — keine Version,
            # kein Versionseintrag, kein geaendert_am, kein Hinweis.
            c.execute("UPDATE pflicht_schritte SET geprueft_am = ? WHERE id = ?",
                      (tag, v["schritt_id"]))
            c.execute(
                "UPDATE pflicht_vorschlaege SET status = 'freigegeben', entschieden_am = ?,"
                " entschieden_von = ? WHERE id = ?", (tag, admin_email, vid))
            c.execute("COMMIT")
            return True, ""
        felder = {k: daten[k] for k in SCHRITT_FELDER if k in daten}
        # Frist-Typ und -Wert nur gemeinsam pruefen: fehlt einer, gilt der
        # aktuelle des Schritts (sonst rutschte z. B. ein neuer Wert ungeprueft durch).
        probe = dict(felder)
        if alt is not None and ("frist_typ" in probe) != ("frist_wert" in probe):
            probe.setdefault("frist_typ", alt.get("frist_typ"))
            probe.setdefault("frist_wert", alt.get("frist_wert"))
        fehler = pruefe_felder(probe, today) if v["art"] != "deaktivieren" else []
        if fehler:
            return abbruch("ungültig: " + "; ".join(fehler))
        if "sortierung" in felder:
            felder["sortierung"] = int(felder["sortierung"])
        if "link" in felder:
            felder["link"] = _link_normalisieren(felder["link"])
        endtyp = felder.get("frist_typ") or (alt or {}).get("frist_typ") or "keine"
        if endtyp == "keine" and ("frist_typ" in felder or "frist_wert" in felder):
            felder["frist_wert"] = ""  # 'keine' hat nie einen Wert

        if v["art"] == "neu":
            if "sortierung" not in felder:
                # ohne Angabe ans Ende der Regulierung
                felder["sortierung"] = c.execute(
                    "SELECT COALESCE(MAX(sortierung), 0) + 1 FROM pflicht_schritte"
                    " WHERE reg_key = ?", (v["reg_key"],)).fetchone()[0]
            basis = {"rolle": "", "frist_typ": "keine", "frist_wert": "", "link": None,
                     "quelle": None, **felder}
            if basis["frist_typ"] == "keine":
                basis["frist_wert"] = ""
            sid = c.execute(
                "INSERT INTO pflicht_schritte (reg_key, sortierung, rolle, frist_typ,"
                " frist_wert, link, quelle, aktiv, version, geprueft_am)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1, ?)",
                (v["reg_key"], basis["sortierung"], basis["rolle"] or "", basis["frist_typ"],
                 basis["frist_wert"] or "", basis["link"] or None, basis["quelle"] or None, tag),
            ).lastrowid
        else:
            sid = v["schritt_id"]
            if v["art"] == "deaktivieren":
                felder = {"aktiv": 0}
            else:
                for k in ("rolle", "frist_wert"):
                    if k in felder:
                        felder[k] = felder[k] or ""
                if "quelle" in felder:
                    felder["quelle"] = felder["quelle"] or None
            sets = "".join(f"{k} = ?, " for k in felder)
            c.execute(f"UPDATE pflicht_schritte SET {sets}version = version + 1,"
                      " geprueft_am = ? WHERE id = ?", (*felder.values(), tag, sid))
        if v["art"] != "deaktivieren":
            _schreibe_texte(c, sid, daten.get("texte") or {})

        stand = _schritt_snapshot(c, sid)
        if v["art"] != "deaktivieren" and not (
                (stand["texte"].get("de") or {}).get("titel") or "").strip():
            return abbruch("ungültig: deutscher Titel ist leer")

        # Schalter in derselben Verbindung lesen (keine zweite waehrend der Sperre).
        schalter = c.execute("SELECT wert FROM pflicht_einstellungen"
                             " WHERE schluessel = 'pflichten_plan_aktiv'").fetchone()
        melden = (v["ausloeser"] != "startbestand"
                  and schalter is not None and schalter[0] == "1")
        if melden:
            c.execute("UPDATE pflicht_schritte SET geaendert_am = ? WHERE id = ?", (tag, sid))
            stand = _schritt_snapshot(c, sid)

        c.execute(
            "INSERT INTO pflicht_schritt_versionen (schritt_id, version, inhalt_json,"
            " geaendert_am, geaendert_von, vorschlag_id) VALUES (?, ?, ?, ?, ?, ?)",
            (sid, stand["version"], json.dumps(stand, ensure_ascii=False), tag,
             admin_email, vid),
        )
        if melden:
            titel = (stand["texte"].get("de") or {}).get("titel", "")
            c.execute(
                "INSERT INTO pflicht_hinweise (user_id, reg_key, art, text_de, erstellt_am)"
                " SELECT user_id, ?, 'inhalt', ?, ? FROM nutzer_pflichten"
                " WHERE reg_key = ? AND entfallen_am IS NULL",
                (v["reg_key"], f"{v['reg_key']}: {_HINWEIS_TEXT[v['art']]}: {titel}", tag,
                 v["reg_key"]),
            )
        c.execute(
            "UPDATE pflicht_vorschlaege SET status = 'freigegeben', schritt_id = ?,"
            " entschieden_am = ?, entschieden_von = ? WHERE id = ?",
            (sid, tag, admin_email, vid),
        )
        c.execute("COMMIT")
        return True, ""
    except Exception:
        if c.in_transaction:
            c.execute("ROLLBACK")
        raise
    finally:
        c.close()


def verwerfen(vid: int, admin_email: str, grund: str, today) -> bool:
    """Nur aus `offen`; der Schritt bleibt, wie er ist."""
    with db._conn() as c:
        cur = c.execute(
            "UPDATE pflicht_vorschlaege SET status = 'verworfen', entschieden_am = ?,"
            " entschieden_von = ?, grund = ? WHERE id = ? AND status = 'offen'",
            (today.isoformat()[:10], admin_email, (grund or "").strip(), vid),
        )
        return cur.rowcount == 1


def katalog_export() -> dict:
    """Alle Schritte (auch deaktivierte) mit allen Texten, fuer den JSON-Download."""
    with db._conn() as c:
        rows = [dict(r) for r in c.execute(
            "SELECT * FROM pflicht_schritte ORDER BY reg_key, sortierung, id")]
        texte = _texte(c, [r["id"] for r in rows])
    for r in rows:
        r["texte"] = texte.get(r["id"], {})
    return {"exportiert_am": date.today().isoformat(), "schritte": rows}
