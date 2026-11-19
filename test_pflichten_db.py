"""Tests zum Pflichten-Plan, Aufgabe 1: Datenmodell, Startbestand, Loeschung.

Ausfuehren:  ./.venv/Scripts/python.exe test_pflichten_db.py

Kein Netz, kein LLM. Eigene DB `data/esg_pflichten_db_test.db`.

Bloecke:
  A  Startbestand aus FIRST_STEPS_BY_REG_KEY (einmalig, idempotent)
  B  Texte je Sprache mit Rueckfall auf Deutsch
  C  Einstellungen
  D  Kontoloeschung raeumt alle Nutzer-Tabellen
  E  Neue Spalte users.erinnerungen
  F  Spalte pflicht_schritte.meldung_version (Migration idempotent, Start NULL)
  G  Seed mit INSERT OR IGNORE: Wettlauf um herkunft_key wirft nicht
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_pflichten_db_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import i18n  # noqa: E402
import pflichten_db as pdb  # noqa: E402
import regulations as regs  # noqa: E402

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def block_a() -> None:
    db.init_db()  # legt Schema an und spielt den Startbestand ein
    with db._conn() as c:
        rows = c.execute("SELECT herkunft_key, reg_key FROM pflicht_schritte").fetchall()
        zweiter = pdb.seed_aus_code(c)
    erwartet = {(k, reg) for reg, keys in regs.FIRST_STEPS_BY_REG_KEY.items() for k in keys}
    gefunden = [(r["herkunft_key"], r["reg_key"]) for r in rows]
    check("A je Schluessel genau ein Schritt",
          sorted(gefunden) == sorted(erwartet) and len(gefunden) == len(set(gefunden)),
          f"{len(gefunden)} Zeilen, {len(erwartet)} erwartet")
    check("A zweiter Aufruf legt nichts an", zweiter == 0, f"{zweiter}")
    db.init_db()
    with db._conn() as c:
        n = c.execute("SELECT COUNT(*) FROM pflicht_schritte").fetchone()[0]
    check("A init_db erneut: keine Dubletten", n == len(erwartet), f"{n}")

    eudr = pdb.schritte_fuer("EUDR", "de")
    erster = eudr[0] if eudr else {}
    link = regs.first_steps_link("EUDR")
    check("A Startwerte des Schritts",
          erster.get("frist_typ") == "keine" and erster.get("rolle") == ""
          and erster.get("geprueft_am") is None and erster.get("aktiv") == 1
          and erster.get("beschreibung") == "" and erster.get("daten") == ""
          and erster.get("link") == (link["url"] if link else None),
          f"{ {k: erster.get(k) for k in ('frist_typ', 'rolle', 'geprueft_am', 'link')} }")
    check("A Reihenfolge nach sortierung",
          [s["herkunft_key"] for s in eudr] == regs.FIRST_STEPS_BY_REG_KEY["EUDR"])


def block_b() -> None:
    en = pdb.schritte_fuer("EUDR", "en")
    check("B englischer Titel", bool(en) and en[0]["titel"] == i18n.FIRST_STEPS["eudr_1"]["en"])
    sid = en[0]["id"]
    with db._conn() as c:
        c.execute("DELETE FROM pflicht_schritt_texte WHERE schritt_id = ? AND sprache = 'zh'",
                  (sid,))
    zh = pdb.schritte_fuer("EUDR", "zh")
    check("B fehlende zh-Zeile -> deutscher Titel",
          zh[0]["titel"] == i18n.FIRST_STEPS["eudr_1"]["de"], zh[0]["titel"][:40])
    s = pdb.schritt(sid)
    check("B schritt() mit Texten",
          s is not None and s["texte"]["de"]["titel"] == i18n.FIRST_STEPS["eudr_1"]["de"]
          and "zh" not in s["texte"])
    check("B schritt() unbekannt -> None", pdb.schritt(999999) is None)
    with db._conn() as c:
        c.execute("UPDATE pflicht_schritte SET aktiv = 0 WHERE id = ?", (sid,))
    check("B nur_aktiv blendet aus", sid not in [x["id"] for x in pdb.schritte_fuer("EUDR", "de")])
    check("B nur_aktiv=False zeigt alle",
          sid in [x["id"] for x in pdb.schritte_fuer("EUDR", "de", nur_aktiv=False)])


def block_c() -> None:
    check("C Standardwert", pdb.einstellung("pflichten_plan_aktiv", "0") == "0")
    pdb.setze_einstellung("pflichten_plan_aktiv", "1")
    check("C gesetzt", pdb.einstellung("pflichten_plan_aktiv", "0") == "1")
    pdb.setze_einstellung("pflichten_plan_aktiv", "0")
    check("C ueberschrieben", pdb.einstellung("pflichten_plan_aktiv") == "0")
    alt = os.environ.pop("PFLICHTEN_PLAN", None)
    check("C funktion_aktiv ohne Env", pdb.funktion_aktiv() is True)
    os.environ["PFLICHTEN_PLAN"] = "AUS"
    check("C funktion_aktiv mit Env aus", pdb.funktion_aktiv() is False)
    os.environ.pop("PFLICHTEN_PLAN")
    if alt is not None:
        os.environ["PFLICHTEN_PLAN"] = alt


NUTZER_TABELLEN = ("nutzer_pflichten", "nutzer_schritte", "nutzer_erledigt",
                   "pflicht_erinnerungen", "pflicht_hinweise")


def _zeilen(uid: int) -> dict[str, int]:
    with db._conn() as c:
        return {t: c.execute(f"SELECT COUNT(*) FROM {t} WHERE user_id = ?", (uid,)).fetchone()[0]
                for t in NUTZER_TABELLEN}


def block_d() -> None:
    uid = db.create_user("pflicht-loeschen@test.example", "Sehr-geheim-123")
    andere = db.create_user("pflicht-bleibt@test.example", "Sehr-geheim-123")
    sid = pdb.schritte_fuer("CSRD", "de")[0]["id"]
    with db._conn() as c:
        for u in (uid, andere):
            c.execute("INSERT INTO nutzer_pflichten (user_id, reg_key, erste_feststellung)"
                      " VALUES (?, 'CSRD', '2026-11-19')", (u,))
            c.execute("INSERT INTO nutzer_schritte (user_id, schritt_id, zustaendig,"
                      " gesehen_version) VALUES (?, ?, 'Einkauf', 1)", (u, sid))
            c.execute("INSERT INTO nutzer_erledigt (user_id, schritt_id, periode, erledigt_am)"
                      " VALUES (?, ?, '', '2026-11-19')", (u, sid))
            c.execute("INSERT INTO pflicht_erinnerungen (user_id, schritt_id, art, frist,"
                      " gesendet_am) VALUES (?, ?, '30', '2026-12-31', '2026-12-01')", (u, sid))
            c.execute("INSERT INTO pflicht_hinweise (user_id, reg_key, art, text_de, erstellt_am)"
                      " VALUES (?, 'CSRD', 'inhalt', 'geaendert', '2026-11-19')", (u,))
    vorher = _zeilen(uid)
    check("D vorher je eine Zeile", all(v == 1 for v in vorher.values()), f"{vorher}")
    check("D delete_user", db.delete_user(uid) is True)
    nachher = _zeilen(uid)
    check("D nachher alles leer", all(v == 0 for v in nachher.values()), f"{nachher}")
    check("D anderes Konto unberuehrt", all(v == 1 for v in _zeilen(andere).values()))


def block_e() -> None:
    with db._conn() as c:
        cols = {r[1]: r for r in c.execute("PRAGMA table_info(users)").fetchall()}
    col = cols.get("erinnerungen")
    check("E Spalte users.erinnerungen", col is not None)
    check("E Standard 1", col is not None and str(col[4]) == "1" and col[3] == 1,
          f"{tuple(col) if col else None}")
    uid = db.create_user("pflicht-standard@test.example", "Sehr-geheim-123")
    with db._conn() as c:
        wert = c.execute("SELECT erinnerungen FROM users WHERE id = ?", (uid,)).fetchone()[0]
    check("E neues Konto erinnerungen = 1", wert == 1, f"{wert}")


def block_f() -> None:
    import sqlite3
    with db._conn() as c:
        cols = {r[1] for r in c.execute("PRAGMA table_info(pflicht_schritte)")}
        werte = {r[0] for r in c.execute("SELECT meldung_version FROM pflicht_schritte")} \
            if "meldung_version" in cols else {"fehlt"}
    check("F Spalte meldung_version", "meldung_version" in cols, str(sorted(cols)))
    check("F Startwert NULL", werte == {None}, str(werte))
    # Alte DB ohne Spalte: Migration legt sie an, zweiter Lauf ist ruhig.
    alt = sqlite3.connect(":memory:")
    alt.execute(
        "CREATE TABLE pflicht_schritte (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " reg_key TEXT NOT NULL, sortierung INTEGER NOT NULL DEFAULT 0,"
        " rolle TEXT NOT NULL DEFAULT '', frist_typ TEXT NOT NULL DEFAULT 'keine',"
        " frist_wert TEXT NOT NULL DEFAULT '', link TEXT, quelle TEXT,"
        " aktiv INTEGER NOT NULL DEFAULT 1, version INTEGER NOT NULL DEFAULT 1,"
        " geprueft_am TEXT, geaendert_am TEXT, herkunft_key TEXT UNIQUE)")  # Stand aad2d54
    try:
        pdb.init_schema(alt)
        pdb.init_schema(alt)
        cols = {r[1] for r in alt.execute("PRAGMA table_info(pflicht_schritte)")}
    except Exception as exc:  # noqa: BLE001
        cols = {repr(exc)}
    check("F Migration auf alter Tabelle, idempotent", "meldung_version" in cols, str(cols))


class _OhneVorhandene:
    """Verbindung, die beim Seed 'nichts vorhanden' meldet - wie ein paralleler Prozess,
    der zwischen Lesen und Schreiben dieselben Schritte angelegt hat."""

    def __init__(self, c):
        self.c = c

    def execute(self, sql, *args):
        if sql.startswith("SELECT herkunft_key"):
            return iter([])
        return self.c.execute(sql, *args)


def block_g() -> None:
    with db._conn() as c:
        vorher = c.execute("SELECT COUNT(*) FROM pflicht_schritte").fetchone()[0]
        texte = c.execute("SELECT COUNT(*) FROM pflicht_schritt_texte").fetchone()[0]
        try:
            neu = pdb.seed_aus_code(_OhneVorhandene(c))
            fehler = ""
        except Exception as exc:  # noqa: BLE001
            neu, fehler = None, repr(exc)
        nachher = c.execute("SELECT COUNT(*) FROM pflicht_schritte").fetchone()[0]
        texte2 = c.execute("SELECT COUNT(*) FROM pflicht_schritt_texte").fetchone()[0]
    check("G Wettlauf: kein Fehler, nichts neu", neu == 0, fehler or str(neu))
    check("G keine Dubletten, keine verwaisten Texte", nachher == vorher and texte2 == texte,
          f"{vorher}->{nachher}, {texte}->{texte2}")


if __name__ == "__main__":
    for block in (block_a, block_b, block_c, block_d, block_e, block_f, block_g):
        block()
    print()
    if TEST_DB.exists():
        try:
            TEST_DB.unlink()
        except OSError:
            pass
    if _failures:
        print(f"{len(_failures)} FEHLER:")
        for f in _failures:
            print("  -", f)
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
