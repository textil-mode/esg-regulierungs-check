# Pflichten-Plan („Meine Pflichten“) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aus dem letzten Prüfergebnis eine laufende Arbeitsliste je Mitglied bauen (Schritte, Fristen, Rolle, Daten, Häkchen, Zuständigkeit, Erinnerungen), deren Katalog in der Datenbank liegt und nur über Vorschläge mit Admin-Freigabe geändert wird.

**Architecture:** Neuer Katalog in SQLite (`pflichten_db.py`), reine Rechenlogik für Fristen und Plan (`pflichten.py`), KI-Vorschläge und Übersetzungen (`pflichten_vorschlag.py`), täglicher Cron-Lauf für Erinnerungen und Hinweise (`pflichten_erinnerung.py`). Flask-Routen und Templates im bestehenden Stil von `app.py`. Fristen werden nie gespeichert, sondern bei jeder Anzeige aus Regel + `deadlines.deadline_for` berechnet.

**Tech Stack:** Python 3.12, Flask 3, SQLite, Gemini über `llm.LLMClient.ask`, SMTP über `mailer.send`, Cron per `docker exec` auf dem VPS.

**Spec:** `docs/superpowers/specs/2026-11-19-pflichten-plan-design.md` (vor jeder Aufgabe lesen).

## Global Constraints

- Sprachen: `de, en, es, fr, it, zh`. Jeder neue Text für Mitglieder in allen sechs (in `i18n.py`, Muster der vorhandenen Schlüssel).
- Freigabe und Handpflege nur für `app._is_stamm_admin()` (Konten in `ADMIN_EMAILS`); ernannte Admins (`_is_admin()`) nur lesend.
- Keine KI-Änderung wird ohne Freigabe sichtbar; keine Mitgliederdaten im Prompt (nur Gesetzestext und Katalog).
- Schalter `pflichten_plan_aktiv` (DB, Standard `0`): aus = Ansicht nur für Admins, keine Erinnerungen, keine Hinweise an Mitglieder.
- Env `PFLICHTEN_PLAN=aus` (Legacy-Container): Funktion komplett aus, Karten lesen erste Schritte aus dem Code (`regulations.first_steps_for` + `i18n.t_first_step`).
- Frist-Typen exakt: `relativ` (Wert `-6m`, `-30d`, `+0d`), `fest` (`31.12.2027`), `jaehrlich` (`31.05.`), `keine` (`""`).
- Pflicht gilt schon (Anker ≤ heute) → relative Frist ist `laufend`: kein Datum, keine 30/7-Tage-Erinnerung, kein .ics, nie überfällig; eigener Block „laufend“ in der Monatsübersicht.
- Anker leer (`gilt_ab == ""`) → `offen`, keine Erinnerung.
- Erinnerungen 30 und 7 Tage vor Frist (Fenster: Frist − heute ∈ [0, 30] bzw. [0, 7], einmal je Konto/Schritt/Art/Frist); Monatsübersicht am 1. (offen in 90 Tagen, überfällig, laufend).
- Keine Mails an Konten mit `approved = 0` oder `locked = 1` oder `erinnerungen = 0`.
- Mail-Sprache = `users.signup_lang`, sonst `de`.
- Startbestand-Freigaben (`ausloeser = 'startbestand'`) erzeugen keine Hinweise und kein „geändert, bitte prüfen“.
- Tests: Skriptstil wie `test_waescherei.py` (eigene DB über `ESG_DB_PATH`, `check()`, kein Netz, kein LLM, festes `today`); keine Zusicherungen auf die Gesamtzahl der Regulierungen.
- `analyses.result_json`: Liste von Karten mit `key` und `applies` ∈ {`ja`, `nein`, `moeglich`, `error`}. Plan nimmt `ja`/`moeglich`; `error` lässt den vorherigen Zustand der Pflicht unverändert.
- Commits pfadbeschränkt (`git add <dateien>`), Nachricht endet mit `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. Konto ohne Unternehmensprofil oder ohne Prüfung → Seite zeigt Verweis auf den Check, kein Fehler 500 (Test in Task 4).
2. Jährlicher Schritt genau am Stichtag (heute = 31.05.) → Frist ist heute, nicht nächstes Jahr; Häkchen dieser Periode zählt (Test in Task 2/3).
3. Doppelklick auf „Freigeben“ → zweiter Aufruf ändert nichts, keine zweite Version, keine doppelten Hinweise (Test in Task 5).
4. Cron fällt drei Tage aus → 7-Tage-Erinnerung kommt trotzdem, aber nur einmal (Test in Task 7).
5. Konto löschen → alle Zeilen in den neuen Nutzer-Tabellen weg (Test in Task 1).

---

### Task 1: Datenmodell, Startbestand, Löschung

**Files:**
- Create: `pflichten_db.py`
- Modify: `db.py` (`init_db` ruft `pflichten_db.init_schema(c)`; `_migrate_users` ergänzt `erinnerungen INTEGER NOT NULL DEFAULT 1`; `_delete_account_rows` löscht `pflicht_hinweise` per user_id — die übrigen Nutzer-Tabellen per `ON DELETE CASCADE`)
- Test: `test_pflichten_db.py`

**Interfaces:**
- Produces:
  - Tabellen (alle `CREATE TABLE IF NOT EXISTS`):
    - `pflicht_schritte(id INTEGER PK, reg_key TEXT, sortierung INTEGER, rolle TEXT, frist_typ TEXT, frist_wert TEXT, link TEXT, quelle TEXT, aktiv INTEGER DEFAULT 1, version INTEGER DEFAULT 1, geprueft_am TEXT, geaendert_am TEXT, herkunft_key TEXT UNIQUE)` — `herkunft_key` = alter Schlüssel aus `FIRST_STEPS_BY_REG_KEY` (z. B. `eudr_1`), NULL bei neuen Schritten; `geaendert_am` nur bei wesentlicher (nicht Startbestand-)Freigabe.
    - `pflicht_schritt_texte(schritt_id, sprache, titel, beschreibung, daten, PK(schritt_id, sprache))`
    - `pflicht_schritt_versionen(id PK, schritt_id, version, inhalt_json, geaendert_am, geaendert_von, vorschlag_id)`
    - `pflicht_vorschlaege(id PK, reg_key, schritt_id NULL, art TEXT /*neu|aendern|deaktivieren*/, ausloeser TEXT /*watchdog|anwendungsbeginn|startbestand|hand*/, ausloeser_ref TEXT, vorher_json, nachher_json, beleg TEXT, begruendung TEXT, status TEXT DEFAULT 'offen' /*offen|freigegeben|verworfen*/, erstellt_am, entschieden_am, entschieden_von, grund)`
    - `nutzer_pflichten(user_id FK CASCADE, reg_key, erste_feststellung TEXT, entfallen_am TEXT, letzter_gilt_ab TEXT, PK(user_id, reg_key))`
    - `nutzer_schritte(user_id FK CASCADE, schritt_id, zustaendig TEXT, gesehen_version INTEGER, PK(user_id, schritt_id))`
    - `nutzer_erledigt(user_id FK CASCADE, schritt_id, periode TEXT /* '' oder Jahr 'YYYY' */, erledigt_am TEXT, PK(user_id, schritt_id, periode))`
    - `pflicht_erinnerungen(user_id FK CASCADE, schritt_id, art TEXT /*30|7*/, frist TEXT, gesendet_am, PK(user_id, schritt_id, art, frist))`
    - `pflicht_hinweise(id PK, user_id, reg_key, art TEXT /*inhalt|datum*/, text_de TEXT, erstellt_am, gesendet_am)`
    - `pflicht_einstellungen(schluessel TEXT PK, wert TEXT)`
  - `init_schema(c: sqlite3.Connection) -> None`
  - `seed_aus_code(c) -> int` — legt je Eintrag in `FIRST_STEPS_BY_REG_KEY` einen Schritt an, falls `herkunft_key` fehlt (Texte aus `i18n.FIRST_STEPS[key][lang]` als `titel`, `beschreibung`/`daten` leer, `frist_typ='keine'`, `rolle=''`, `link` = `first_steps_link(reg_key)["url"]` falls vorhanden, `geprueft_am` NULL). Gibt Anzahl neu angelegter zurück. Idempotent.
  - `einstellung(schluessel: str, standard: str = "") -> str`, `setze_einstellung(schluessel: str, wert: str) -> None`
  - `schritte_fuer(reg_key: str, lang: str, nur_aktiv: bool = True) -> list[dict]` — Felder der Tabelle + `titel, beschreibung, daten` in `lang`, Rückfall auf `de` je Feld.
  - `schritt(schritt_id: int) -> dict | None` — inkl. `texte: {lang: {titel, beschreibung, daten}}`
  - `funktion_aktiv() -> bool` — `os.getenv("PFLICHTEN_PLAN", "").lower() != "aus"`

- [ ] **Step 1: Write the failing test** `test_pflichten_db.py` mit Checks:
  - `seed_aus_code` legt für jeden Schlüssel aus `regs.FIRST_STEPS_BY_REG_KEY` genau einen Schritt an; zweiter Aufruf gibt `0` zurück.
  - `schritte_fuer("EUDR", "en")[0]["titel"] == i18n.FIRST_STEPS["eudr_1"]["en"]`.
  - Fehlt eine `zh`-Zeile, liefert `schritte_fuer(..., "zh")` den deutschen Titel.
  - `einstellung("pflichten_plan_aktiv", "0") == "0"`; nach `setze_einstellung(..., "1")` → `"1"`.
  - Nach `db.delete_user(uid)` sind `nutzer_pflichten`, `nutzer_schritte`, `nutzer_erledigt`, `pflicht_erinnerungen`, `pflicht_hinweise` für `uid` leer (vorher je eine Zeile eingefügt).
  - Neue Spalte `users.erinnerungen` existiert mit Standard `1`.
- [ ] **Step 2:** `./.venv/Scripts/python.exe test_pflichten_db.py` → FAIL (`ModuleNotFoundError: pflichten_db`).
- [ ] **Step 3:** `pflichten_db.py` und Änderungen in `db.py` umsetzen. `seed_aus_code` wird in `db.init_db` nach `init_schema` aufgerufen.
- [ ] **Step 4:** Test erneut → keine `FAIL`-Zeile, Exit 0. Zusätzlich `test_admin_loeschen.py` und `test_konto_sicherheit.py` grün.
- [ ] **Step 5: Commit** `git add pflichten_db.py db.py test_pflichten_db.py && git commit -m "Pflichten-Plan: Datenmodell und Startbestand aus den ersten Schritten"`

### Task 2: Frist-Regeln

**Files:**
- Create: `pflichten.py`
- Test: `test_pflichten_frist.py`

**Interfaces:**
- Produces: `frist_fuer(frist_typ: str, frist_wert: str, gilt_ab: str, today: date) -> dict` mit `{"art": "datum"|"laufend"|"offen"|"keine", "datum": date|None, "periode": str}`; `periode` ist `"YYYY"` bei `jaehrlich` (Jahr des berechneten Stichtags), sonst `""`. Ungültige Werte → `{"art": "keine", ...}` (nie Ausnahme).

- [ ] **Step 1: Write the failing test** — `today = date(2026, 11, 19)`:
  - `frist_fuer("relativ", "-6m", "30.06.2027", today)` → `art "datum"`, `datum 2026-12-30`.
  - `frist_fuer("relativ", "+0d", "30.06.2027", today)` → `datum 2027-06-30`.
  - `frist_fuer("relativ", "-6m", "30.12.2026", today)` → `datum 2026-06-30` (Datum in der Vergangenheit, Anker in der Zukunft: bleibt `datum`, Anzeige „überfällig“ entscheidet Task 3).
  - `frist_fuer("relativ", "-6m", "01.01.2023", today)` → `art "laufend"`, `datum None`.
  - `frist_fuer("relativ", "-6m", "19.11.2026", today)` → `laufend` (Anker = heute gilt als gilt schon).
  - `frist_fuer("relativ", "-6m", "", today)` → `offen`.
  - `frist_fuer("fest", "31.12.2027", "", today)` → `datum 2027-12-31`.
  - `frist_fuer("jaehrlich", "31.05.", "", today)` → `datum 2027-05-31`, `periode "2027"`.
  - `frist_fuer("jaehrlich", "31.05.", "", date(2027, 5, 31))` → `datum 2027-05-31` (Stichtag selbst).
  - `frist_fuer("jaehrlich", "29.02.", "", today)` → `datum 2027-02-28`.
  - `frist_fuer("keine", "", "30.06.2027", today)` → `keine`; `frist_fuer("relativ", "quatsch", "30.06.2027", today)` → `keine`.
  - Monatsversatz am Monatsende: `frist_fuer("relativ", "-1m", "31.03.2027", today)` → `datum 2027-02-28`.
- [ ] **Step 2:** Test laufen lassen → FAIL.
- [ ] **Step 3:** `frist_fuer` implementieren (Monatsrechnung ohne neue Abhängigkeit, Tag auf Monatsende kappen).
- [ ] **Step 4:** Test → grün.
- [ ] **Step 5: Commit** `git add pflichten.py test_pflichten_frist.py && git commit -m "Pflichten-Plan: Frist-Regeln"`

### Task 3: Plan je Konto

**Files:**
- Modify: `pflichten.py`, `pflichten_db.py`
- Test: `test_pflichten_plan.py`

**Interfaces:**
- Consumes: `frist_fuer`, `schritte_fuer`, `db.latest_analysis(user_id) -> {"id","created_at","result":[{key, name, applies, ...}]}|None`, `db.get_company(user_id)`, `deadlines.deadline_for(reg_key, profile, today)`.
- Produces:
  - `pflichten_db.sync_pflichten(user_id: int, aktuelle: dict[str, str], today: date) -> None` — `aktuelle` = `{reg_key: applies}` aus dem letzten Ergebnis. `ja`/`moeglich`: Zeile anlegen (`erste_feststellung = today`) oder `entfallen_am` auf NULL; `nein`: `entfallen_am = today`, falls noch NULL; `error`: nichts.
  - `pflichten_db.setze_erledigt(user_id, schritt_id, periode: str, erledigt: bool, today: date) -> None`
  - `pflichten_db.setze_zustaendig(user_id, schritt_id, text: str) -> None` (auf 120 Zeichen gekürzt, getrimmt; leer = NULL)
  - `pflichten_db.markiere_gesehen(user_id, schritt_id, version: int) -> None`
  - `pflichten.plan_fuer(user_id: int, lang: str, today: date) -> dict`:
    ```
    {"grundlage": created_at|None, "hat_profil": bool,
     "pflichten": [{"reg_key","name","gilt_ab","entfaellt": bool, "entfallen_am",
                    "erledigt": int, "gesamt": int, "naechste_frist": date|None,
                    "schritte": [{"id","titel","beschreibung","daten","rolle","link","quelle",
                                  "geprueft_am","frist": <frist_fuer-dict>,
                                  "ueberfaellig": bool, "erledigt": bool, "erledigt_am",
                                  "zustaendig", "geaendert": bool, "verlauf": [{"periode","erledigt_am"}]}]}]}
    ```
    Sortierung: nicht entfallene vor entfallenen; darin überfällige zuerst, dann `naechste_frist` aufsteigend, `None` zuletzt, dann Name. `ueberfaellig` = `art == "datum"` und `datum < today` und nicht erledigt. `geaendert` = erledigt und `geaendert_am` > `erledigt_am` und `gesehen_version` < `version`. `erledigt` bei `jaehrlich` nur für die aktuelle `periode`; ältere Perioden in `verlauf`.
  - `pflichten.ROLLEN = ["gf", "einkauf", "personal", "logistik", "produkt", "nachhaltigkeit", "finanzen"]` (Anzeige über i18n `rolle_<schluessel>`).

- [ ] **Step 1: Write the failing test** mit Testkonto, Profil (z. B. 120 Beschäftigte, Leder), gespeicherter Analyse (`db.save_analysis`) mit `EUDR: ja`, `LkSG: nein`, `CSRD: moeglich`, `GPSR: error`; Checks:
  - Ohne Analyse: `plan_fuer(...)["pflichten"] == []`, `grundlage is None`.
  - Mit Analyse: EUDR und CSRD im Plan, LkSG nicht, GPSR nicht.
  - Zweite Analyse mit `CSRD: nein` → CSRD `entfaellt True`, Häkchen eines CSRD-Schritts bleibt erhalten.
  - Dritte Analyse mit `CSRD: error` → CSRD-Zustand unverändert gegenüber vorher.
  - Schritt mit `fest 01.11.2026`, nicht erledigt → `ueberfaellig True`; nach `setze_erledigt` → `False`.
  - Jährlicher Schritt `31.05.`: erledigt in Periode `2027` am `today=2026-11-19`; bei `today=2027-06-01` ist er offen und `verlauf` enthält 2027.
  - `geaendert`: Schritt erledigt, dann `version` erhöht und `geaendert_am` später gesetzt → `True`; nach `markiere_gesehen` → `False`.
  - Sortierung: überfälliger Schritt-Pflicht steht vor Pflicht mit späterer Frist.
  - `setze_zustaendig` mit 200 Zeichen speichert 120.
- [ ] **Step 2:** Test → FAIL.
- [ ] **Step 3:** Implementieren. `plan_fuer` ruft `sync_pflichten` mit dem letzten Ergebnis auf; Profil über `db.get_company` (fehlt es: `hat_profil False`, Anker leer).
- [ ] **Step 4:** Test → grün.
- [ ] **Step 5: Commit** `git add pflichten.py pflichten_db.py test_pflichten_plan.py && git commit -m "Pflichten-Plan: Plan je Konto mit Haekchen, Perioden und Entfaellt"`

### Task 4: Ansicht „Meine Pflichten“, .ics, Karten aus der Datenbank

**Files:**
- Create: `templates/meine_pflichten.html`
- Modify: `app.py` (Routen), `views.py:205-225` (erste Schritte aus DB, wenn `funktion_aktiv()`), `i18n.py` (Schlüssel), Navigationsleiste in `templates/base.html`
- Test: `test_pflichten_ansicht.py`

**Interfaces:**
- Consumes: `plan_fuer`, `setze_erledigt`, `setze_zustaendig`, `markiere_gesehen`, `einstellung`, `funktion_aktiv`.
- Produces (Routen, alle mit `_require_login()`; sichtbar wenn `funktion_aktiv()` und (`einstellung("pflichten_plan_aktiv")=="1"` oder `_is_admin()`), sonst 404):
  - `GET /meine-pflichten` (`?rolle=<schluessel>` filtert Schritte; Pflichten ohne passende Schritte entfallen aus der Anzeige)
  - `POST /meine-pflichten/<int:schritt_id>/erledigt` (Form `erledigt=1|0`, `periode`) → Redirect zurück
  - `POST /meine-pflichten/<int:schritt_id>/zustaendig` (Form `zustaendig`)
  - `POST /meine-pflichten/<int:schritt_id>/gesehen`
  - `GET /meine-pflichten.ics` → `text/calendar`; ein `VEVENT` (ganztägig) je Schritt mit `frist.art == "datum"`, nicht erledigt, nicht entfallen; `UID` = `pflicht-<user_id>-<schritt_id>-<YYYYMMDD>@ki-textil-mode.de`; Zeilen nach RFC 5545 gefaltet/escaped.
  - `POST /konto/erinnerungen` (Form `an=1|0`) setzt `users.erinnerungen`; Schalter auf der Seite „Passwort ändern“/Konto.
  - `views.render_cards_html`: Liste der ersten Schritte aus `schritte_fuer(reg_key, lang)` (nur `titel`), sonst wie bisher aus dem Code.
- i18n-Schlüssel (6 Sprachen): `nav_pflichten, pflichten_titel, pflichten_grundlage, pflichten_ohne_pruefung, pflichten_gilt_ab, pflichten_laufend, pflichten_offen, pflichten_ueberfaellig, pflichten_bis, pflichten_daten, pflichten_zustaendig, pflichten_geprueft, pflichten_geaendert, pflichten_entfaellt, pflichten_ics, pflichten_erinnerungen_an, pflichten_erinnerungen_aus, pflichten_filter_alle, pflichten_haftung`, `rolle_gf … rolle_finanzen`.

- [ ] **Step 1: Write the failing test** (Flask-Testclient, Login per `session_transaction` wie `test_admin_konten.py`):
  - Schalter aus, normales Konto: `GET /meine-pflichten` → 404; Admin-Konto → 200.
  - Schalter an, Konto ohne Analyse → 200 und enthält `t("pflichten_ohne_pruefung","de")`.
  - Konto mit Analyse → enthält EUDR-Schritttitel und „laufend“ für eine geltende Pflicht.
  - `POST …/erledigt` mit fremder/inaktiver `schritt_id` → 404.
  - Zuständigkeit mit `<script>` wird escaped ausgegeben.
  - `?rolle=einkauf` blendet Schritte mit anderer Rolle aus.
  - `.ics` enthält genau ein `VEVENT` je datierten offenen Schritt, keinen für `laufend`.
  - Env `PFLICHTEN_PLAN=aus`: Route 404 auch für Admin; Ergebnis-Karte zeigt Schritte aus `i18n.FIRST_STEPS`.
  - Bestehende Tests `test_waescherei.py` und `test_katalog_erweiterung.py` bleiben grün.
- [ ] **Step 2:** Test → FAIL.
- [ ] **Step 3:** Routen, Template (Stil der vorhandenen Seiten, Aufklappen je Pflicht, Haftungshinweis oben), `views.py`-Umstellung, i18n.
- [ ] **Step 4:** Neuer Test und alle vorhandenen `test_*.py` grün.
- [ ] **Step 5: Commit** `git add app.py views.py i18n.py templates/meine_pflichten.html templates/base.html test_pflichten_ansicht.py && git commit -m "Pflichten-Plan: Ansicht, Kalenderexport, erste Schritte aus der Datenbank"`

### Task 5: Vorschläge, Freigabe, Handpflege

**Files:**
- Modify: `pflichten_db.py`, `app.py`
- Create: `templates/admin_pflichten.html`, `templates/admin_pflichten_vorschlag.html`
- Test: `test_pflichten_freigabe.py`

**Interfaces:**
- Produces:
  - `pflichten_db.neuer_vorschlag(reg_key: str, art: str, ausloeser: str, nachher: dict, *, schritt_id: int | None = None, ausloeser_ref: str = "", beleg: str = "", begruendung: str = "") -> int` — `vorher_json` wird aus dem aktuellen Schritt gefüllt. `nachher` = `{"rolle","frist_typ","frist_wert","link","quelle","sortierung","texte":{lang:{"titel","beschreibung","daten"}}}` (fehlende Felder = unverändert).
  - `pflichten_db.offene_vorschlaege() -> list[dict]`, `pflichten_db.vorschlag(vid) -> dict|None`
  - `pflichten_db.freigeben(vid: int, admin_email: str, aenderungen: dict | None, today: date) -> bool` — in einer Transaktion: nur wenn `status == 'offen'` (sonst `False`, nichts geändert); `aenderungen` überschreibt Felder von `nachher`; wendet an (neu/aendern/deaktivieren), `version += 1`, Versionseintrag, `geprueft_am = today`; `geaendert_am = today` und Hinweise (`pflicht_hinweise`, `art='inhalt'`) nur wenn `ausloeser != 'startbestand'` und `einstellung("pflichten_plan_aktiv") == "1"`, an alle Konten mit `nutzer_pflichten.reg_key` und `entfallen_am IS NULL`.
  - `pflichten_db.verwerfen(vid: int, admin_email: str, grund: str, today: date) -> bool` (nur aus `offen`)
  - `pflichten_db.katalog_export() -> dict` (alle Schritte mit Texten, für JSON-Download)
  - Routen (alle `_require_login` + `_is_admin()` zum Lesen; schreibende zusätzlich `_is_stamm_admin()`, sonst 403):
    - `GET /admin/pflichten` (Katalog je Regulierung, Schalter `pflichten_plan_aktiv`, Zahl offener Vorschläge, Link Export)
    - `POST /admin/pflichten/schalter` (Form `aktiv=1|0`)
    - `GET /admin/pflichten/schritt/<int:sid>` und `/admin/pflichten/neu/<reg_key>` (Formular, nur deutsche Felder) → `POST` erzeugt Vorschlag `ausloeser='hand'`, ruft `pflichten_vorschlag.uebersetzen` (Task 6; bis dahin Platzhalter, der die deutschen Texte für alle Sprachen kopiert) und leitet auf die Vorschlagsseite
    - `GET /admin/pflichten/vorschlaege`, `GET /admin/pflichten/vorschlag/<int:vid>` (Vorher/Nachher je Feld und Sprache nebeneinander, Beleg, Felder editierbar)
    - `POST /admin/pflichten/vorschlag/<int:vid>/freigeben`, `POST …/verwerfen` (Form `grund`)
    - `GET /admin/pflichten/export.json`

- [ ] **Step 1: Write the failing test:**
  - Vorschlag `aendern` mit neuer Rolle → nach `freigeben` hat der Schritt die Rolle, `version` +1, ein Versionseintrag, `geprueft_am == today`.
  - Zweites `freigeben` derselben ID → `False`, `version` unverändert, Hinweiszahl unverändert.
  - `verwerfen` → Schritt unverändert, Status `verworfen`, Grund gespeichert.
  - Schalter an + Konto mit EUDR in `nutzer_pflichten` → genau ein Hinweis nach Freigabe eines EUDR-Vorschlags; Konto mit `entfallen_am` → keiner.
  - `ausloeser='startbestand'` → kein Hinweis, `geaendert_am` unverändert.
  - Schalter aus → kein Hinweis.
  - `deaktivieren` → Schritt fehlt in `schritte_fuer`, erscheint im Plan nicht mehr.
  - Route-Rechte: ernannter Admin `POST …/freigeben` → 403; Stamm-Admin → Redirect, Status `freigegeben`; normales Konto `GET /admin/pflichten` → Redirect auf Dashboard (wie andere Admin-Seiten).
- [ ] **Step 2:** Test → FAIL.
- [ ] **Step 3:** Implementieren.
- [ ] **Step 4:** Test + `test_admin_rollen.py` grün.
- [ ] **Step 5: Commit** `git add pflichten_db.py app.py templates/admin_pflichten*.html test_pflichten_freigabe.py && git commit -m "Pflichten-Plan: Vorschlaege, Freigabe und Handpflege"`

### Task 6: KI-Vorschläge (Watchdog, Startbestand) und Übersetzung

**Files:**
- Create: `pflichten_vorschlag.py`
- Modify: `watchdog.py` (nach Erkennen einer Änderung), `app.py` (Platzhalter aus Task 5 durch echte Übersetzung ersetzen; Knopf „Startbestand ergänzen lassen“ auf `/admin/pflichten`, nur Stamm-Admin, startet Hintergrund-Thread)
- Test: `test_pflichten_vorschlag.py`

**Interfaces:**
- Consumes: `llm.LLMClient().ask(system, user, max_tokens, json_mode=True) -> str` (async), `llm._extract_json`, `pflichten_db.neuer_vorschlag`, `fetcher.version_text`, `lawparse.build_context`.
- Produces (jede Funktion nimmt optional `ask: Callable[[str, str], Awaitable[str]]` für Tests):
  - `async uebersetzen(texte_de: dict, ask=None) -> dict[str, dict]` — Eingabe `{"titel","beschreibung","daten"}`, Ausgabe für `en, es, fr, it, zh`; bei unbrauchbarer Antwort Ausnahme `VorschlagFehler`.
  - `async vorschlaege_aus_aenderung(reg_key: str, alter_text: str, neuer_text: str, ask=None) -> list[int]` — sendet Diff-Ausschnitt (wie `watchdog._diff_excerpt`) + aktuelle Schritte (deutsch, mit Frist-Regel); erwartet JSON `{"aenderungen":[{"art","schritt_id"|null,"nachher":{…},"beleg","begruendung"}]}`; leere Liste → kein Vorschlag; `schritt_id`, die nicht zu `reg_key` gehört, wird verworfen; Frist-Werte, die `frist_fuer` als `keine` einstuft, obwohl Typ ≠ `keine`, werden verworfen; je gültiger Änderung `uebersetzen` + `neuer_vorschlag(ausloeser='watchdog', ausloeser_ref=<run_id>)`.
  - `async startbestand_vorschlaege(reg_key: str, ask=None) -> list[int]` — für Schritte mit `geprueft_am IS NULL` je ein `aendern`-Vorschlag mit Rolle (aus `ROLLEN`), Frist-Regel, Daten, Beleg; `ausloeser='startbestand'`; Gesetzesauszug über `lawparse.build_context`.
  - `benachrichtige_admin(anzahl: dict[str, int], versand=mailer.send) -> None` — eine Mail an `ADMIN_EMAILS` („EUDR: 2 Vorschläge“) mit Link `PUBLIC_BASE_URL + /admin/pflichten/vorschlaege`, Eintrag `mail_log` mit `purpose='pflichten_vorschlag'`.
  - Watchdog: nach `changed.append(entry)` bei `use_llm` → `vorschlaege_aus_aenderung`; Fehler landen in `errors`, brechen den Lauf nicht ab; am Ende `benachrichtige_admin`, falls Vorschläge entstanden.
  - System-Prompt: Deutsch, „schlage nur Änderungen vor, die der neue Text belegt; zitiere die Stelle; erfinde nichts; Fristen nur als Regeltypen relativ/fest/jaehrlich/keine“. Keine Profil- oder Kontodaten im Prompt.

- [ ] **Step 1: Write the failing test** mit Fake-`ask`:
  - Gültige Antwort mit einer Änderung → ein Vorschlag mit `ausloeser 'watchdog'`, Texte in allen sechs Sprachen.
  - Antwort `{"aenderungen": []}` → keine Vorschläge.
  - Kaputtes JSON → `VorschlagFehler`, kein Vorschlag angelegt.
  - Fremde `schritt_id` → verworfen.
  - `frist_typ "relativ", frist_wert "bald"` → verworfen.
  - Der an `ask` übergebene Prompt enthält weder Firmenname noch E-Mail des Testkontos.
  - `startbestand_vorschlaege("EUDR")` → je ungeprüftem EUDR-Schritt ein Vorschlag mit `ausloeser 'startbestand'`.
  - `benachrichtige_admin` ruft `versand` einmal mit Admin-Adresse und Link auf.
  - `watchdog.run(use_llm=False)` verhält sich wie vorher (bestehende Watchdog-Tests, falls vorhanden, grün).
- [ ] **Step 2:** Test → FAIL.
- [ ] **Step 3:** Implementieren.
- [ ] **Step 4:** Test grün; `test_llm_fallback.py` grün.
- [ ] **Step 5: Commit** `git add pflichten_vorschlag.py watchdog.py app.py test_pflichten_vorschlag.py && git commit -m "Pflichten-Plan: KI-Vorschlaege aus Watchdog und Startbestand, Uebersetzung"`

### Task 7: Täglicher Lauf: Erinnerungen, Hinweise, Datumsänderungen, Lebenszeichen

**Files:**
- Create: `pflichten_erinnerung.py`
- Modify: `i18n.py` (Mailtexte 6 Sprachen), `db.py`/`pflichten_db.py` (Abfragen)
- Test: `test_pflichten_erinnerung.py`

**Interfaces:**
- Consumes: `plan_fuer`, `pflichten_db`, `mailer.send`, `db.log_mail`.
- Produces:
  - `lauf(today: date, versand=None) -> dict` mit Zählern `{"erinnerungen","uebersichten","hinweise","konten"}`. Tut nichts (Zähler 0), wenn `funktion_aktiv()` falsch oder Schalter aus.
  - Je berechtigtem Konto (approved, nicht locked, `erinnerungen = 1`): `plan_fuer(uid, lang, today)`; Datumsänderung (ersetzt laut Spec 6.7 den Auslöser „geänderter Anwendungsbeginn“ aus 6.4; Fristen ziehen ohnehin nach): für jede Pflicht `deadline_for(...)["gilt_ab"]` gegen `nutzer_pflichten.letzter_gilt_ab` — abweichend und vorher nicht NULL → Hinweis `art='datum'`; danach Wert speichern (erstes Mal nur speichern).
  - Erinnerungen: offene Schritte mit `art == "datum"`, `0 <= (datum - today).days <= 7` → Art `7`; sonst `<= 30` → Art `30`; nur wenn kein Eintrag `(uid, sid, art, datum)` in `pflicht_erinnerungen`. Alle fälligen eines Kontos in **einer** Mail.
  - Am Monatsersten (`today.day == 1`): Übersicht (offen in 90 Tagen, überfällig, Block „laufend“).
  - Ungesendete `pflicht_hinweise` des Kontos in derselben Mail bündeln, danach `gesendet_am` setzen.
  - Pro Konto höchstens eine Mail je Lauf; `mail_log` `purpose='pflichten_erinnerung'`; Fehler beim Versand eines Kontos brechen den Lauf nicht ab und markieren nichts als gesendet.
  - Am Monatsersten Lebenszeichen an `ADMIN_EMAILS` mit Zählern des Vormonats (aus `mail_log`).
  - `main(argv)`: `python pflichten_erinnerung.py [--heute YYYY-MM-DD] [--probe]` (`--probe` = nichts senden, nur ausgeben).
  - Mail enthält Link `PUBLIC_BASE_URL + /meine-pflichten` und Hinweis zum Abbestellen auf der Kontoseite.

- [ ] **Step 1: Write the failing test** mit Fake-`versand`:
  - Schritt `fest` in 30 Tagen → eine Mail Art 30; gleicher Tag erneut → keine Mail.
  - Lauf ausgefallen: Frist in 5 Tagen, kein Eintrag Art 7 → Mail; nächster Tag → keine weitere.
  - `laufend`- und `offen`-Schritte → nie Erinnerung; am 1. stehen `laufend`-Schritte im Block „laufend“.
  - Erledigter Schritt → keine Erinnerung.
  - Konto `locked=1`, `approved=0` oder `erinnerungen=0` → keine Mail.
  - Zwei fällige Schritte + ein Hinweis → genau eine Mail.
  - `letzter_gilt_ab` geändert (Profil von 120 auf 40 Beschäftigte bei EUDR → kleines Unternehmen) → ein Hinweis `datum`; erster Lauf ohne Vorwert → keiner.
  - Schalter aus → keine Mail, Zähler 0.
  - Versand wirft `MailError` → Erinnerung nicht als gesendet markiert.
  - Mail-Sprache `en` bei `signup_lang='en'`, `de` bei NULL.
- [ ] **Step 2:** Test → FAIL.
- [ ] **Step 3:** Implementieren.
- [ ] **Step 4:** Test grün.
- [ ] **Step 5: Commit** `git add pflichten_erinnerung.py pflichten_db.py i18n.py test_pflichten_erinnerung.py && git commit -m "Pflichten-Plan: taeglicher Lauf mit Erinnerungen und Hinweisen"`

### Task 8: Datenschutz, Doku, Sicherheitsprüfung, Ausrollen

**Files:**
- Modify: `templates/datenschutz.html` (Erinnerungsmails, gespeicherte Häkchen und Zuständigkeitstexte, Übermittlung von Gesetzestext an Gemini für Vorschläge ohne Mitgliederdaten; Stand-Datum), `CLAUDE.md` (Feature-Inventar, Cron, Schalter, Env), `README.md` (kurz)

- [ ] **Step 1:** Datenschutzerklärung und Doku ergänzen; Commit `git add templates/datenschutz.html CLAUDE.md README.md && git commit -m "Pflichten-Plan: Datenschutz und Doku"`.
- [ ] **Step 2:** Skill `web-sicherheit` gegen die neuen Routen ausführen (Rechte je Route, IDOR bei `schritt_id`, CSRF-Herkunftsprüfung bei allen POST, XSS in Zuständigkeit/Admin-Feldern, .ics-Injection über Zeilenumbrüche). Befunde dem Nutzer melden, nicht still reparieren.
- [ ] **Step 3:** Alle `test_*.py` laufen lassen → keine `FAIL`-Zeile.
- [ ] **Step 4:** Push, Image-Build abwarten, Deploy beider Container per `/root/esg_redeploy.py`. Im Legacy-Container `esg-regulierungs-check` Env `PFLICHTEN_PLAN=aus` setzen (vorher prüfen, wie `esg_redeploy.py` Env-Werte übernimmt; nicht raten).
- [ ] **Step 5:** Cron im Hauptcontainer ergänzen: `30 6 * * * docker exec esg-ki-textil-mode python pflichten_erinnerung.py >> /var/log/esg-pflichten.log 2>&1`. Probe: `docker exec esg-ki-textil-mode python pflichten_erinnerung.py --probe`.
- [ ] **Step 6:** Live prüfen: `/esg/meine-pflichten` als Admin 200, als normales Konto 404 (Schalter aus); `/esg/admin/pflichten` zeigt den Startbestand. Schalter bleibt aus, bis der Nutzer die Startvorschläge freigegeben hat.
- [ ] **Step 7:** `pwsh _uebersicht/log-fortschritt.ps1 -slug esg-regulierungs-check -typ feature -titel "Pflichten-Plan (Meine Pflichten)" -detail "…" -status live` und dasselbe für `wissen-berichtspflichten`.
