"""Sortierbare Tabellen auf /admin/konten (29.09.2026).

Geprueft wird die Serverseite: beide Tabellen tragen die Sortier-Kennzeichen,
jede sortierbare Spalte hat einen Knopf, und die Zellen liefern den
Sortierwert in maschinenlesbarer Form (ISO-Zeitstempel statt Anzeige,
leerer Wert statt "noch nie" / "nicht erfasst" / "—").

Das Sortieren selbst laeuft im Browser. Mit --html <datei> schreibt der Test
die gerenderte Seite weg, damit man sie im Browser durchklicken kann.

Eigene DB data/esg_sortierung_test.db, kein Netz, kein LLM.
"""
from __future__ import annotations

import os
import re
import sqlite3
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_sortierung_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for _var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_var] = ""
os.environ["PUBLIC_BASE_URL"] = "https://test.example"

import db  # noqa: E402

assert db.DB_PATH == TEST_DB
db.init_db()

import app as flaskapp  # noqa: E402

fehler: list[str] = []
ADMIN = sorted(flaskapp.ADMIN_EMAILS)[0]


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


# Testbestand: Werte so gewaehlt, dass jede Spalte eine andere Reihenfolge ergibt.
KONTEN = [
    # email, registriert, letzte Anmeldung, Unternehmen, Pruefungen (Zeitpunkte)
    (ADMIN, "2026-01-05T08:00:00", "2026-09-29T09:00:00", "textil+mode", ["2026-09-28T10:00:00"]),
    ("berta@example.org", "2026-03-10T12:00:00", None, "Zwirnerei Berta", []),
    ("anton@example.org", "2026-06-01T07:30:00", "2026-07-01T11:00:00", None,
     ["2026-06-02T09:00:00", "2026-06-03T09:00:00", "2026-06-20T09:00:00"]),
    ("Carla@example.org", "2026-09-20T16:45:00", "2026-09-21T08:00:00", "Atelier Carla", ["2026-09-21T08:30:00"]),
]
with sqlite3.connect(TEST_DB) as c:
    for email, reg, login, firma, pruefungen in KONTEN:
        uid = c.execute(
            "INSERT INTO users (email, pw_hash, created_at, last_login_at, approved)"
            " VALUES (?, 'x', ?, ?, 1)", (email.lower(), reg, login)).lastrowid
        if firma:
            c.execute("INSERT INTO companies (user_id, name, updated_at) VALUES (?, ?, ?)", (uid, firma, reg))
        for zeit in pruefungen:
            c.execute("INSERT INTO analyses (user_id, created_at, result_json) VALUES (?, ?, '[]')",
                      (uid, zeit))
    c.execute("INSERT INTO users (email, pw_hash, created_at, approved)"
              " VALUES ('offen2@example.org', 'x', '2026-09-29T10:00:00', 0)")
    c.execute("INSERT INTO users (email, pw_hash, created_at, approved)"
              " VALUES ('offen1@example.org', 'x', '2026-09-28T10:00:00', 0)")

client = flaskapp.app.test_client()
with client.session_transaction() as sess:
    sess["user_id"] = db.get_user_by_email(ADMIN)["id"]
    sess["user_email"] = ADMIN
    sess["ui_language"] = "de"

print("1. Seite und Tabellen")
r = client.get("/admin/konten")
html = r.get_data(as_text=True)
pruefe(r.status_code == 200, f"/admin/konten laedt (HTTP {r.status_code})")
pruefe('class="reg-table sortable" id="konten"' in html, "Kontentabelle ist sortierbar")
pruefe('class="reg-table sortable" id="anfragen"' in html, "Anfragentabelle ist sortierbar")

print("\n2. Spaltenkoepfe")
konten_kopf = html.split('id="konten"', 1)[1].split("</thead>", 1)[0]
typen = re.findall(r'<th data-sort="(\w+)"', konten_kopf)
pruefe(typen == ["text", "text", "date", "date", "num", "date", "text"],
       f"sieben sortierbare Spalten mit passender Art ({typen})")
pruefe(konten_kopf.count('class="sort-btn"') == 7, "jede Spalte hat einen Sortierknopf")
pruefe('aria-sort="descending"' in konten_kopf,
       "Ausgangslage gekennzeichnet: Registrierung, neueste zuerst")
pruefe("Nach dieser Spalte sortieren" in konten_kopf, "Hinweis beim Ueberfahren (i18n)")
anfragen_kopf = html.split('id="anfragen"', 1)[1].split("</thead>", 1)[0]
pruefe(re.findall(r'<th data-sort="(\w+)"', anfragen_kopf) == ["text", "text", "date"],
       "Anfragen: nach Adresse, Verband und Eingang sortierbar, Aktionsspalte nicht")

print("\n3. Sortierwerte in den Zellen")
koerper = html.split('id="konten"', 1)[1].split("</tbody>", 1)[0]
zeilen = koerper.split("<tr>")[2:]  # [0] = vor thead, [1] = Kopfzeile
pruefe(len(zeilen) == 4, f"vier freigeschaltete Konten, offene Anfragen nicht darunter ({len(zeilen)})")
berta = next((z for z in zeilen if "berta@example.org" in z), "")
pruefe('data-sort-value="2026-03-10T12:00:00"' in berta, "Registrierung als ISO-Zeitstempel")
pruefe(berta.count('data-sort-value=""') == 3,
       "ohne Anmeldung, ohne Pruefung, ohne Admin-Recht: leerer Sortierwert (steht dann unten)")
pruefe('data-sort-value="0"' in berta, "keine Pruefung: Zahl 0")
anton = next((z for z in zeilen if "anton@example.org" in z), "")
pruefe('data-sort-value="3"' in anton and 'data-sort-value="2026-06-20T09:00:00"' in anton,
       "Anzahl und letzte Pruefung richtig")
pruefe("—" in anton and 'data-sort-value=""' in anton,
       "Anzeige bleibt \"—\", Sortierwert ist leer")
pruefe("<script>" in html and "localeCompare" in html, "Sortierskript eingebunden")

if "--html" in sys.argv:
    ziel = Path(sys.argv[sys.argv.index("--html") + 1])
    ziel.write_text(html, encoding="utf-8")
    print(f"\nSeite geschrieben: {ziel}")

print()
if fehler:
    print(f"{len(fehler)} Pruefung(en) fehlgeschlagen")
    sys.exit(1)
print("alle Pruefungen gruen")
