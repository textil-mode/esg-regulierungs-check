"""Tests zur Pflichtangabe des Mitgliedsverbands bei der Registrierung.

Eigene Datenbank (`data/esg_verband_test.db`), Attrappe statt echtem Versand,
kein Netz. `data/esg.db` wird nie beruehrt.

Aufruf:  ./.venv/Scripts/python.exe test_mitgliedsverband.py
"""
from __future__ import annotations

import os
import sqlite3
import sys
import threading
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEST_DB = Path(__file__).parent / "data" / "esg_verband_test.db"
TEST_DB.parent.mkdir(parents=True, exist_ok=True)
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["ESG_DB_PATH"] = str(TEST_DB)
for _v in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
           "MAIL_FROM", "MAIL_FROM_NAME"):
    os.environ[_v] = ""
os.environ["PUBLIC_BASE_URL"] = "https://test.example"

import db  # noqa: E402

assert db.DB_PATH == TEST_DB, f"Testlauf zeigt auf {db.DB_PATH}!"
db.init_db()

import mailer  # noqa: E402
import regulations  # noqa: E402
import i18n  # noqa: E402
import app as flaskapp  # noqa: E402

VERBAND = regulations.MEMBER_ASSOCIATIONS[0]
KEIN = "Kein Mitglied"
BASIS_THREADS = threading.active_count()

fehler: list[str] = []
versandt: list[dict] = []
mailer.send = lambda to, subj, text: (versandt.append({"to": to, "subject": subj}),
                                      "msg")[1]
mailer.is_configured = lambda: True


def pruefe(bedingung: bool, text: str) -> None:
    print(("  [ok]   " if bedingung else "  [FEHL] ") + text)
    if not bedingung:
        fehler.append(text)


def ruhe(sekunden: float = 5.0) -> None:
    ende = time.perf_counter() + sekunden
    while threading.active_count() > BASIS_THREADS and time.perf_counter() < ende:
        time.sleep(0.005)
    time.sleep(0.05)


def registrieren(email: str, verband, ip: str = "203.0.113.5"):
    daten = {"action": "signup", "email": email}
    if verband is not None:
        daten["association"] = verband
    with flaskapp.app.test_client() as client:
        return client.post("/login", data=daten, environ_base={"REMOTE_ADDR": ip})


def verband_von(email: str):
    with sqlite3.connect(TEST_DB) as c:
        r = c.execute("SELECT association FROM users WHERE email = ?",
                      (email.lower(),)).fetchone()
    return r[0] if r else "(kein Konto)"


# ---------------------------------------------------------------------------
print("\n1. Die Liste stimmt mit der Website ueberein")
# ---------------------------------------------------------------------------
liste = regulations.MEMBER_ASSOCIATIONS
pruefe(len(liste) == 25, f"24 Verbaende + 'Kein Mitglied' ({len(liste)})")
pruefe(liste[-1] == KEIN, "'Kein Mitglied' steht am Ende und ist waehlbar")
pruefe(len(set(liste)) == len(liste), "keine Dubletten")
pruefe(all(v.strip() == v and v for v in liste), "keine leeren Eintraege, kein Rand-Leerzeichen")
pruefe(any("Südwesttextil" in v for v in liste), "Suedwesttextil ist dabei")
pruefe(any("GermanFashion" in v for v in liste), "GermanFashion ist dabei")
pruefe(any("Gesamtmasche" in v for v in liste), "Gesamtmasche ist dabei")
# Die zweite Haelfte der Liste laedt die Website erst per "Weiter laden" nach —
# beim ersten Abruf fehlte sie. Diese Pruefungen fangen den Rueckfall ab.
pruefe(any("intex" in v for v in liste), "intex (Nr. 24) ist dabei")
pruefe(any("BVMed" in v for v in liste), "BVMed ist dabei")
pruefe(any("Kammgarnspinner" in v for v in liste), "Kammgarnspinner ist dabei")
pruefe(any("Plauener Spitze" in v for v in liste), "Plauener Spitze ist dabei")

# ---------------------------------------------------------------------------
print("\n2. Angabe wird gespeichert")
# ---------------------------------------------------------------------------
a = registrieren("mit-verband@example.org", VERBAND)
ruhe()
pruefe(a.status_code == 200, "Registrierung beantwortet mit 200")
pruefe(verband_von("mit-verband@example.org") == VERBAND,
       "der gewaehlte Verband steht am Konto")

b = registrieren("ohne-mitgliedschaft@example.org", KEIN, ip="203.0.113.6")
ruhe()
pruefe(verband_von("ohne-mitgliedschaft@example.org") == KEIN,
       "'Kein Mitglied' wird ebenso gespeichert")

# ---------------------------------------------------------------------------
print("\n3. Pflichtangabe — ohne gueltigen Wert entsteht kein Konto")
# ---------------------------------------------------------------------------
for wert, was in ((None, "Feld fehlt ganz"), ("", "leer"),
                  ("Erfundener Verband e. V.", "nicht aus der Liste"),
                  (" ", "nur Leerzeichen")):
    adresse = f"ohne-{abs(hash(was)) % 10000}@example.org"
    r = registrieren(adresse, wert, ip="203.0.113.7")
    ruhe()
    pruefe(not db.email_exists(adresse), f"{was}: kein Konto angelegt")
    pruefe(r.status_code == 200, f"{was}: Seite bleibt bedienbar")

# ---------------------------------------------------------------------------
print("\n4. Die Antwort verraet weiterhin nichts ueber den Kontobestand")
# ---------------------------------------------------------------------------
versandt.clear()
neu = registrieren("frisch@example.org", VERBAND, ip="203.0.113.8")
ruhe()
seite_neu = neu.get_data(as_text=True)
versandt.clear()
nochmal = registrieren("frisch@example.org", VERBAND, ip="203.0.113.9")
ruhe()
pruefe(nochmal.get_data(as_text=True) == seite_neu,
       "bekannte und neue Adresse liefern dieselbe Seite")
pruefe(nochmal.status_code == neu.status_code, "gleicher HTTP-Status")

# ---------------------------------------------------------------------------
print("\n5. Der Admin sieht den Verband bei den offenen Anfragen")
# ---------------------------------------------------------------------------
offen = db.list_pending()
pruefe(all("association" in a for a in offen),
       "list_pending liefert die Spalte mit")
treffer = [a for a in offen if a["email"] == "mit-verband@example.org"]
pruefe(bool(treffer) and treffer[0]["association"] == VERBAND,
       "der Wert steht an der richtigen Anfrage")

admin = "mschuckert@textil-mode.de"
admin_id = db.create_user(admin, "ein-gutes-Passwort-2026")
with flaskapp.app.test_client() as client:
    with client.session_transaction() as s:
        s["user_id"] = admin_id
        s["user_email"] = admin
    seite = client.get("/admin/konten")
    inhalt = seite.get_data(as_text=True)
    pruefe(seite.status_code == 200, "die Admin-Seite laedt")
    pruefe("Verband" in inhalt, "die Spalte 'Verband' ist da")
    pruefe(VERBAND in inhalt, "der Verband der Anfrage steht darin")

# ---------------------------------------------------------------------------
print("\n6. Das Formular bietet alle Verbaende an")
# ---------------------------------------------------------------------------
with flaskapp.app.test_client() as client:
    formular = client.get("/login").get_data(as_text=True)
pruefe('name="association"' in formular, "das Auswahlfeld ist im Formular")
pruefe("required" in formular.split('name="association"')[1][:60],
       "es ist als Pflichtfeld gekennzeichnet")
fehlend = [v for v in liste if v not in formular]
pruefe(not fehlend, f"alle {len(liste)} Eintraege stehen zur Auswahl")
pruefe(i18n.t("association_choose", "de") in formular,
       "die leere Vorauswahl 'Bitte waehlen' steht davor")

# ---------------------------------------------------------------------------
print("\n7. Texte vollstaendig in allen Sprachen")
# ---------------------------------------------------------------------------
for k in ("field_association", "association_choose", "err_association_missing",
          "admin_pending_association"):
    f = [x for x in i18n.LANG_CODES if not i18n.UI.get(k, {}).get(x)]
    pruefe(not f, f"{k}: alle {len(i18n.LANG_CODES)} Sprachen")
f = [x for x in i18n.LANG_CODES if not i18n.ASSOCIATION_LABELS[KEIN].get(x)]
pruefe(not f, "'Kein Mitglied' ist uebersetzt")
pruefe(i18n.t_opt(VERBAND, i18n.ASSOCIATION_LABELS, "en") == VERBAND,
       "Verbandsnamen bleiben als Eigenname stehen (hier: en)")

# ---------------------------------------------------------------------------
ruhe()
print("\n" + "=" * 62)
if fehler:
    print(f"FEHLGESCHLAGEN: {len(fehler)} Pruefung(en)")
    for f in fehler:
        print("  -", f)
    sys.exit(1)
print("Alle Pruefungen bestanden.")
