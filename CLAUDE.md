# ESG-Regulierungs-Check — Projekt-Memo für Claude Code

> **Dieses Dokument ist die Quelle der Wahrheit über den aktuellen Stand.**
> Beim Sitzungsstart hier zuerst hineinschauen, dann gezielt in den Code.

---

## Aktueller stabiler Stand

- **Produktions-URL (neu):** https://ki-textil-mode.de/esg/ (Root `/` redirected auf `/esg/login`)
- **Legacy-URL:** https://schuckert.cloud/regulierungs-check (weiterhin aktiv, selber Container)
- **Stabiler Commit:** `d18caba` (branch `main`)
- **Git-Tag:** `stable-2026-04-21`
- **Stand dieses Dokuments:** 2026-06-10 (LLM-Konfig erneut live verifiziert: beide Container unverändert auf Gemini 2.5 Flash Lite; Container laufen noch mit Image aus altem Namespace `ghcr.io/textilundmode/…`)

> Der Flask-Container ist derselbe fuer beide Domains. Die nginx-Konfig auf
> dem Hostinger-VPS setzt je nach Host-Header unterschiedliche
> `X-Script-Name`-Prefixes (`/regulierungs-check` bzw. `/esg`); die
> `PrefixMiddleware` in `app.py` sorgt dafuer, dass `url_for()`
> automatisch den korrekten Prefix liefert.

---

## Was funktioniert (Feature-Inventar)

| Feature | Ort | Status |
|---|---|---|
| Login / Registrierung (bcrypt, SQLite) | `app.py`, `db.py` | ✅ |
| **Bremse gegen Passwort-Durchprobieren** (5 Fehlversuche je Konto+IP in 15 min mit sich verdoppelnder Wartezeit, zusätzlich 30/Stunde je IP; persistent in `login_attempts`) — siehe eigenen Abschnitt unten | `db.py` `begin_login_attempt`, `app.py` `/login` | ✅ |
| **Passwort ändern** (eingeloggt, altes PW nötig) | `/passwort-aendern`, `templates/password_change.html` | ✅ |
| **Passwort vergessen → Admin-Reset-Link** (kein Mailversand; Ticket + einmaliger 24h-Token, nur als SHA-256-Hash gespeichert) | `/admin/passwort-resets`, `db.password_resets` | ✅ |
| Stammdaten-Formular (inkl. Standorte, Produktkategorien, **Rolle in der Wertschoepfungskette**, **Materialien**) | `templates/dashboard.html` | ✅ |
| Stammdaten-Frage "EU-Importeur / erstmaliges Inverkehrbringen" | `templates/dashboard.html`, `db.eu_importer` | ✅ |
| LLM-Analyse über 20 Regulierungen (Volltext + Guidelines) | `app.py` `_run_analysis_bg`, `llm.py` | ✅ |
| **Result-Cache, nutzeruebergreifend und wortstabil** (`analysis_cache`, PK `(reg_key, profile_hash, reg_hash)`): `profile_hash` deckt nur die `relevant_fields` der jeweiligen Reg ab (Firmenname o. Ä. verwirft nichts), `reg_hash` zusaetzlich Kriterien, Prompt-Stand und Gesetzesstand (`fetcher.current_text_hash`). Ist die Quelle gerade nicht abrufbar (`None`), gilt der zuletzt gespeicherte Eintrag weiter statt jedes Mal neu zu formulieren | `db.py`, `llm.py` `plan_analysis` | ✅ |
| **Datentrennung im globalen Cache** (siehe Invariante unten): der Prompt zeigt exakt die `relevant_fields` der Regulierung, der Firmenname steht nirgends darin, und der System-Prompt verbietet das Nennen eines Namens | `llm.py` `_format_profile`, `_SYSTEM_BASE` | ✅ |
| **Handlungsplan je Karte**: "Gilt ab" mit unternehmensindividueller Frist (Phase-in) und aufklappbare "Erste Schritte" (2-4 kuratierte Stichpunkte + Leitlinien-Link) | `deadlines.py`, `regulations.py` `FIRST_STEPS_BY_REG_KEY`, `views.py` | ✅ |
| **Schwellen-Naehe** ("Was waere wenn"): Hinweis, wenn das Profil ±20 % um eine Schwelle liegt (LkSG 1000, HinSchG 50, CSRD 1000/450 Mio., CSDDD 5000/1,5 Mrd.) | `thresholds.py`, `views.py` | ✅ |
| **Deterministische Begruendungen ohne LLM** fuer die gekoppelten Regs (CSRD, CSRD_DE, TaxonomieVO, HinSchG, WhistleblowerRL, CSR-RUG): handgeschriebene Bausteine in 6 Sprachen, 0 LLM-Calls, fuer immer byte-stabil | `regulations.py` `coupling_verdict`, `i18n.py` `coupling_texts`, `llm.py` `deterministic_result` | ✅ |
| Gesetzestext-Cache mit ETag / Last-Modified | `fetcher.py` `law_texts` | ✅ |
| **Strukturbasierte Kontext-Auswahl** (Art. 1-3 + `key_article` + Schwellenwert-Abschnitte statt Blind-Kappung; Kopfzeilen `=== Art. 2 - … ===`) | `lawparse.py` `build_context`, `app.py` Phase 1 | ✅ |
| **EUR-Lex-Fallback ueber publications.europa.eu** (EUR-Lex antwortet Server-Clients mit AWS-WAF-Challenge, HTTP 202 + leerer Body) | `fetcher.py` `_cellar_text` | ✅ |
| **Datumslose CELEX-URLs** (`CELEX:02024L1760` statt `…-20260318`); die juengste konsolidierte Fassung wird zur Laufzeit per SPARQL aufgeloest | `fetcher.py` `_latest_consolidated` | ✅ |
| **Schutz vor stillem Rueckfall auf die Ursprungsfassung**: laesst sich die Konsolidierung nicht ermitteln, wird der vorhandene Cache-Text BEHALTEN statt des Basisrechtsakts; ohne Cache wird der Basisakt zwar genommen, aber in `source_status` (≤ -1000) und `source_note` markiert und auf der Admin-Seite rot ausgewiesen. Zusaetzlich Inhaltspruefung der Konsolidierungs-Kopfzeile | `fetcher.py` `_is_consolidated_text`, `source_is_base_act_fallback` | ✅ |
| **Schutz vor Datenverlust im Cache**: ein vorhandener Text wird nie durch einen leeren oder auf unter 50 % geschrumpften Abruf ersetzt (greift nur bei unveraenderter `text_url`, damit ein bewusster Quellenwechsel weiter moeglich bleibt) | `fetcher.py` `_MIN_KEEP_RATIO` | ✅ |
| **Erstkonsolidierung ≠ Notbehelf**: ist die einzige konsolidierte Fassung auf den ABl.-Tag datiert (z. B. ESG-Rating-VO), gibt es keine spaeteren Aenderungen — der Ursprungstext ist der geltende Text, es wird nicht gewarnt | `fetcher.py` `_is_initial_consolidation` | ✅ |
| **Textversionierung** (`law_versions`: reg_key, language, sha256, text, url, fetched_at); `current_text_hash(reg_key, language)` als Schluessel fuer nachgelagerte Caches | `fetcher.py` | ✅ |
| **Anwendungsdaten + Status je Regulierung** (`applies_from`, abgeleiteter Status `in_kraft`/`gilt_ab`/`entwurf`/`rueckzug_angekuendigt`), Spalte "Gilt ab / Status" in der Regulierungsliste | `regulations.py` `application_for`, `templates/regulierungsliste.html` | ✅ |
| **Watchdog** (`python watchdog.py`): laedt alle 20 Texte mit `force=True`, vergleicht Hashes, schreibt `watchdog_runs`; bei Aenderung LLM-Zusammenfassung als **Vorschlag** (nie automatische `criteria`-Aenderung) | `watchdog.py` | ✅ |
| **Admin-Seite Regulierungs-Status** (Gesetzesstand, Fassungszahl, letzter Watchdog-Lauf, erkannte Aenderungen) | `/admin/regulierungs-status`, `templates/admin_regstatus.html` | ✅ |
| **"Gesetzesstand vom …"** auf jeder Ergebnis-Karte | `app.py` `law_dates`, `views.py` | ✅ |
| **PDF-Export im textil+mode-CD** (Logo, Verlaufskante, Statusfarben; gleicher Umfang wie das frühere CSV plus Kopfbereich und Zusammenfassung). Chinesisch nutzt die nicht eingebettete CID-Schrift STSong-Light — siehe Modul-Docstring | `/download-pdf`, `pdfexport.py` | ✅ |
| Fullscreen-Ansicht Ergebnisse | `/fullscreen` | ✅ |
| **Regulierungsliste** (3-spaltig: Reg / Guidelines / Quelle+Stand) | `/regulierungsliste`, `templates/regulierungsliste.html` | ✅ |
| **textil+mode-Logo oben links** (verlinkt textil-mode.de) | `templates/base.html`, `static/images/textil-mode-logo.png` | ✅ |
| **Dunkelgraue Seitenränder** (`#2b2b2b` außerhalb des 1140px-Containers) | `templates/base.html` | ✅ |
| **Footer-Hinweis** ("Claude Code + OpenAI Codex") unten rechts als `<details>` | `templates/base.html` | ✅ |
| LLM-Robustheit: 60s Request-Timeout, max_tokens 3000, JSON-Auto-Repair | `llm.py` | ✅ |
| **KI-Autofill Stammdaten** (Button "✨ KI-generiert ausfüllen": Wikipedia + Website → nur explizit belegte Felder) | `autofill.py`, `/api/autofill`, `templates/dashboard.html` | ✅ |
| **Deterministische Ergebnisse** (seed=42 + topK=1; `_PROMPT_VERSION` in `reg_hash` invalidiert Cache bei Prompt-Änderungen) | `llm.py` | ✅ |
| **Begründung immer in UI-Sprache** (auch bei englischem Gesetzestext), Zitat bleibt Original | `llm.py` `_SYSTEM_BASE` | ✅ |
| **Kennzahl-Hervorhebung** in "Greifende Stelle" (Zahl+Einheit leicht rot, Passage-Box mit Gold-Rand) | `views.py` `_highlight_kennzahlen`, `base.html` | ✅ |
| "Greifende Stelle" auf 280 Zeichen gekappt (+ " …"). Das statische `key_article` wird NICHT mehr vorangestellt — die Begruendungstexte tragen die Fundstelle seit Prompt v5 selbst, sonst stuenden zwei widerspruechliche Angaben da und die Kappung griffe nur auf den halben Text | `views.py` `_shorten_passage`, `_card_html` | ✅ |
| Fehler-Regulierung als rote ✕-Karte sichtbar | `views.py` `APPLIES_ORDER` + `BADGE_STYLES` | ✅ |
| i18n (DE / EN / ES / FR / IT / ZH) | `i18n.py` | ✅ |

---

### Auswahllisten und alte Firmenprofile (Stand 02.09.2026)

`PRODUCT_CATEGORIES` in `regulations.py` wurde vollstaendig ausgetauscht (jetzt
Verpackungen, Holz, Holzprodukte, Papier, Kautschuk/Gummi, Bekleidung,
Heimtextilien, technische Textilien, PSA, Schuhe, Lederwaren, textile
Medizinprodukte, Automotive-Textilien). Dazu kamen zwei weitere
Mehrfachauswahlen: `VALUE_CHAIN_ROLES` (Rolle in der Wertschoepfungskette) und
`MATERIALS`.

Bestandsprofile in der Produktivdatenbank tragen die alten Kategorien
("Kaffee / Kakao", "Keine physischen Produkte …"). **`db.get_company()` filtert
alle Werte heraus, die in der jeweiligen Liste nicht mehr stehen** (`db._known`),
und `db.upsert_company()` tut dasselbe beim Schreiben. Folge:

- Das Formular zeigt nur noch gueltige Haken; alte Werte erscheinen nirgends.
- Weder LLM-Prompt noch `profile_hash` sehen einen unbekannten Wert — die
  Cache-Invariante bleibt gewahrt.
- In der Spalte `product_categories_json` **bleiben** die alten Werte stehen,
  bis der Nutzer das Formular das naechste Mal speichert; dann werden sie
  ueberschrieben. Es gibt bewusst keine Datenmigration, die fremde Angaben
  stillschweigend umdeutet.

---

### ⚠️ Invariante: Prompt ≡ `relevant_fields` (Datentrennung)

Der `analysis_cache` ist **nutzeruebergreifend**. Damit sich zwei Unternehmen einen
Eintrag teilen duerfen, muss gelten:

> Der LLM-Prompt einer Regulierung enthaelt **genau** die Profilfelder, die auch in
> ihren `profile_hash` eingehen — also `relevant_fields` (+ `language`).

`llm._format_profile(profile, reg)` baut den Profilblock deshalb aus
`relevant_fields_for(reg)`. Zwei Nutzer mit demselben `profile_hash` erzeugen so
denselben Prompt; eine Begruendung kann nichts enthalten, worin sie sich
unterscheiden. Der **Firmenname** gehoert in keine `relevant_fields` und steht
darum nicht im Prompt; zusaetzlich verbietet `_SYSTEM_BASE` das Nennen eines Namens.

Wer hier etwas aendert, muss beides zusammen aendern:
- ein Feld in den Prompt aufnehmen → in die `relevant_fields` der Reg aufnehmen,
- ein Feld aus den `relevant_fields` entfernen → es verschwindet aus dem Prompt.

Sonst wandern Daten des Erstnutzers in die Karten aller weiteren Nutzer. Der Test
`test_cache_stability.py` (Szenario 7) prueft das mit zwei Nutzern nach.

Angenehmer Nebeneffekt: das Modell kann keine Zahl mehr aus einem fremden Feld
importieren. Vor der Umstellung las das LLM beim LkSG „Total employees: 1200" und
begruendete damit „1.200 Arbeitnehmer im Inland" — obwohl das Gesetz auf die
900 Inlandsbeschaeftigten abstellt.

---

## Architektur (Deployment-Kette)

```
Browser
  ├─> https://ki-textil-mode.de/esg/…          (neu, Haupt-Domain)
  └─> https://schuckert.cloud/regulierungs-check/…   (Legacy)
        └─> nginx (auf VPS) — strippt Prefix und setzt X-Script-Name
              └─> localhost:8082 (Docker host port)
                    └─> Container esg-regulierungs-check (interne Port 8080)
                          └─> Gunicorn (1 Worker, 8 Threads) → Flask `app:app`
```

**Reverse-Proxy-Prefix-Handling** (wichtig!): nginx setzt je nach Host-
Header den HTTP-Header `X-Script-Name: /esg` bzw. `X-Script-Name:
/regulierungs-check`. `app.py` hat eine `PrefixMiddleware`, die diesen
Header liest und `environ["SCRIPT_NAME"]` setzt — dadurch produziert
Flask's `url_for()` automatisch Pfade mit dem korrekten Prefix, egal ueber
welche Domain der Nutzer kommt.

---

## Hosting (Hostinger VPS)

- **Hoster:** Hostinger
- **VPS-Plan:** KVM 4 (Ubuntu 24.04, Docker)
- **VPS-ID:** 1400170 · `srv1400170.hstgr.cloud` · IP `187.77.88.67`
- **Docker Manager:** https://hpanel.hostinger.com/vps/1400170/docker-manager
- **Projektname dort:** `esg-regulierungs-check`
- **Container-Name:** `esg-regulierungs-check`
- **Port-Mapping:** `8082:8080` (host:container)
- **Volume:** `esg-data` → `/app/data` (SQLite-DB persistiert hier)
- **Compose-Datei im Hostinger-UI** enthält Secrets (API-Keys), NICHT ident mit der Repo-Kopie editieren.

---

## CI/CD

- **Repo:** `textil-mode/esg-regulierungs-check` (privat, Org textil-mode; umgezogen von `textilundmode`)
- **Workflow:** `.github/workflows/docker-build.yml`
  - Trigger: push auf `main` oder `master`
  - Baut Docker-Image aus `Dockerfile`
  - Pusht nach `ghcr.io/textil-mode/esg-regulierungs-check:latest` (seit Commit `ddb1ec4`)
  - ✅ ghcr-Umzug abgeschlossen (2026-06-10): beide Live-Container laufen mit dem `textil-mode`-Image.
  - **Deploy per SSH** (schneller als Hostinger-UI): `ssh root@187.77.88.67`, dann
    `docker pull ghcr.io/textil-mode/esg-regulierungs-check:latest && python3 /root/esg_redeploy.py esg-ki-textil-mode 8083 && python3 /root/esg_redeploy.py esg-regulierungs-check 8082`
    (Skript übernimmt Env/Volumes/Ports 1:1 aus dem laufenden Container). Rollback: gleiches Skript mit altem Image-Tag.
  - Dauer: typischerweise 1-2 Min (Build-Cache vorhanden)

### Deploy-Prozedur (nach Code-Änderung)

1. `git add <geänderte Dateien>` — **kein** `git add -A` (vermeidet versehentliches Einchecken von Secrets / Scratch-Dateien)
2. `git commit -m "…"`
3. `git push origin main`
4. Warten auf Build-Erfolg: https://github.com/textil-mode/esg-regulierungs-check/actions
5. Hostinger → Docker Manager → Projekt `esg-regulierungs-check` → **Verwalten** → **Bereitstellen**
6. Nach ~15 s testen: https://ki-textil-mode.de/esg/ (bzw. Legacy https://schuckert.cloud/regulierungs-check)

> ⚠️ **Einmalig nach dem Deploy der strukturbasierten Extraktion: den Gesetzestext-Cache leeren.**
> Bis dahin lagen die Texte auf `FULLTEXT_MAX_CHARS` (25.000 Zeichen) gekappt in `law_texts`.
> Ein normaler Lauf ersetzt sie nicht zuverlaessig: wo die Quelle mit `304 Not Modified`
> antwortet (z. B. `CSRD_DE`, Bundestags-PDF), gibt der Fetcher den alten, gekappten Text
> zurueck und konserviert ihn dauerhaft. Deshalb je Container einmal:
> ```bash
> docker exec <container> python3 -c "import sqlite3; c=sqlite3.connect('/app/data/esg.db'); c.execute('DELETE FROM law_texts'); c.commit()"
> ```
> (`<container>` = `esg-ki-textil-mode` und `esg-regulierungs-check`.) Der naechste
> "Jetzt pruefen"-Lauf laedt alle Texte in voller Laenge neu.

> ⚠️ **Dockerfile muss `COPY static/ static/` und `COPY templates/ templates/` enthalten.** Sonst fehlen Assets im Image. Beide sind drin (Stand Tag `stable-2026-04-20`).

---

## Rollback auf diesen stabilen Stand

Falls die App nach einer Änderung nicht mehr läuft:

```bash
# Option A: Lokal auf den stabilen Stand zurück und Force-Push (ZERSTÖRT neuere Commits!)
git fetch origin
git reset --hard stable-2026-04-21
git push origin main --force-with-lease

# Option B: Neuen Commit bauen, der den Stand des Tags wiederherstellt (non-destructive)
git revert <bad-commit-sha>  # oder gezielt
# oder:
git checkout -b rollback-2026-04-21 stable-2026-04-21
git push origin rollback-2026-04-21
# dann PR/Merge nach main

# Nach dem Push:
# → GitHub Actions baut neu (~2 min)
# → Hostinger → Verwalten → Bereitstellen
```

---

## LLM-Konfiguration

> Die eingecheckte `docker-compose.hostinger.yml` ist ein **Dummy/Vorlage** (Platzhalter statt Keys, seit 2026-06-10 strukturell am Live-Stand ausgerichtet). Die echten Werte stehen nur im Hostinger-Docker-Manager-UI; die folgende Tabelle wurde am 2026-05-07 per `docker exec env` gezogen und am **2026-06-10 erneut verifiziert** (beide Container identisch konfiguriert, unverändert).

**Live aktiv** in den Containern `esg-ki-textil-mode` und `esg-regulierungs-check` (Legacy-Spiegel, macht kaum Calls):

| Variable | Wert |
|---|---|
| `LLM_PROVIDER` | `google` |
| `OPENAI_MODEL` | `gemini-2.5-flash-lite` (wird im google-Pfad als Modellname genutzt) |
| `OPENAI_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` (im google-Code-Pfad **ignoriert**, dort ist Base-URL hardcoded auf `…/v1beta`) |
| `OPENAI_API_KEY` | Google-AI-Studio-Key (`AQ.…`, 53 Zeichen) — wird vom google-Pfad als Fallback gelesen, falls `GOOGLE_API_KEY` fehlt (`llm.py:315`) |
| `LLM_CONCURRENCY` | `8` |
| `LLM_RPM` | `150` |
| `FULLTEXT_MAX_CHARS` | `25000` |
| `ANTHROPIC_API_KEY` / `GOOGLE_API_KEY` | **nicht gesetzt** im Live-Container |

**Tarif:** Paid-Tier (Google Billing aktiv, `serviceTier: "standard"` in der API-Response). NICHT free.

**Verifizierte Kosten** (Stand 2026-09-04, am Live-Modell nachgemessen)

Gemessen mit `countTokens` (Eingabe, exakt) und echten `generateContent`-Aufrufen
(Ausgabe) gegen `gemini-2.5-flash-lite`, Live-Konfiguration `FULLTEXT_MAX_CHARS=25000`,
Referenzprofil 1.200 Beschaeftigte / 80 Mio. Umsatz / Textil.

| Metrik | Wert |
|---|---|
| Regulierungen gesamt | 20 |
| davon ohne LLM entschieden (Textbausteine) | **6** (CSRD, CSRD_DE, CSR-RUG, TaxonomieVO, WhistleblowerRL, HinSchG) |
| tatsaechliche LLM-Aufrufe je Durchlauf | **14** |
| Eingabe-Token gesamt | 91.672 (rund 7.000 je Aufruf bei vollem 25k-Kontext) |
| Ausgabe-Token gesamt | rund 2.100 (rund 149 je Aufruf) |
| Denk-Token | **0** — Flash-Lite denkt nicht mit, keine versteckten Kosten |
| Preise (09/2026) | 0,10 USD je 1 Mio. Eingabe, 0,40 USD je 1 Mio. Ausgabe |
| **Kosten je Durchlauf** | **rund 1,0 US-Cent** (0,0092 USD Eingabe + 0,0008 USD Ausgabe) |
| 100 Durchlaeufe | rund 1 USD |
| 1.000 Durchlaeufe | rund 10 USD |

Die Eingabe macht **92 % der Kosten** aus — der Hebel liegt also im Kontext, nicht in der
Antwortlaenge. `FULLTEXT_MAX_CHARS` wirkt daher fast linear auf den Preis.

Nicht enthalten:
- **Wiederholte Laeufe kosten nichts**, solange Profil und Gesetzesstand gleich bleiben
  (globaler Cache, siehe Abschnitt Begruendungen).
- **KI-Autofill** ist ein eigener, zusaetzlicher Aufruf je Nutzung.
- **Watchdog** ruft das LLM nur, wenn sich ein Gesetzestext tatsaechlich geaendert hat.
- Seltene Wiederholungen nach Fehlern (Retry) kommen oben drauf.

Der frueher hier dokumentierte Wert von 0,7 ¢ (Stand 05/2026) galt fuer 22 Regulierungen,
zu denen EUR-Lex damals wegen des Bot-Schutzes teils gar keinen Volltext lieferte — die
Aufrufe waren also kuerzer und die Ergebnisse schwaecher.

Provider-Switch: Im Hostinger-Compose-UI (NICHT in der Repo-Datei) `LLM_PROVIDER` und Modell ändern → Bereitstellen.

**Empfehlung:** in Google Cloud Billing einen Budget-Alert (z. B. 5 €/Monat) setzen, falls die Nutzung stark wächst.

---

## Daten-/Content-Quellen

### Regulierungen — statische Metadaten (`regulations.py`)

- `REGULATIONS` — 20 Einträge mit `key`, `name`, `full_name`, `url`, `text_url`, `scope`, `criteria`, `key_article`
- `GUIDELINES_BY_REG_KEY` — je Regulierung eine Liste kuratierter offizieller Leitlinien (EU-Kommission, BAFA, EFRAG, ESMA, IDW, BfJ, DRSC)
- `PUBLISHED_BY_REG_KEY` — Veröffentlichungsdatum je Reg (OJ-Datum bzw. BGBl.-Datum), Format `DD.MM.YYYY`

Wenn ein Datum / eine Guideline-URL aktualisiert werden muss → direkt in `regulations.py` editieren, kein DB-Migration nötig.

### Dynamische Daten (Cache, SQLite in `/app/data/esg.db`)

> **Testlaeufe:** `ESG_DB_PATH=/pfad/zur/kopie.db` biegt `db.py` **und** `fetcher.py`
> gemeinsam auf eine andere Datei um. Ohne diese Variable schreibt jeder Direktaufruf
> (z. B. `python watchdog.py`) in `data/esg.db`.

- `analysis_cache` — nutzeruebergreifend, PK `(reg_key, profile_hash, reg_hash)` + Spalte `text_hash`.
  Der alte, nutzergebundene Cache wird beim ersten Start durch `db._migrate_analysis_cache()`
  einmalig verworfen (die Eintraege tragen den Gesetzesstand nicht und lassen sich nicht
  uebersetzen); der naechste Lauf erzeugt sie neu.
- `users`, `companies`, `analyses`, `law_texts` (Volltext + ETag + Last-Modified +
  fetched_at + `source_status` + `source_note`; `source_status ≤ -1000` = nur Ursprungsrechtsakt
  geladen, spaetere Aenderungen fehlen)
- `law_versions` — Historie der Gesetzestexte, eine Zeile je inhaltlich abweichender Fassung
  (`reg_key`, `language`, `text_hash` = sha256, `text`, `url`, `fetched_at`). Wird vom Fetcher
  bei jeder Aenderung fortgeschrieben; `fetcher.current_text_hash(reg_key, language)` liefert den
  Hash des aktuellen Stands (oder `None`, wenn kein Text im Cache liegt).
- `watchdog_runs` — je Lauf: `started_at`, `finished_at`, `language`, `checked`,
  `changed_json` (`[{reg_key, name, previous_hash, text_hash, summary}]`), `errors_json`.
- Guidelines werden ebenfalls in `law_texts` gespeichert mit `reg_key` = `GUIDE:<sha256-prefix>` (siehe `fetcher.py` `_guideline_key`).

---

## Schlüsseldateien (was wo lebt)

| Datei | Zweck |
|---|---|
| `app.py` | Flask-Routen, Login, Analyse-Orchestrierung, PrefixMiddleware |
| `llm.py` | LLM-Provider-Abstraktion (openai / ollama / anthropic / google), Prompt, Rate-Limit |
| `fetcher.py` | HTTP-Download von Gesetzes-/Guideline-Texten, HTML/PDF-Extraktion, ETag-Cache, EUR-Lex-Fallback |
| `lawparse.py` | Zerlegt Gesetzestexte in Artikel-/§-/Anhang-Abschnitte und baut daraus den LLM-Kontext (Anwendungsbereich statt Praeambel) |
| `test_lawparse.py` | Tests dazu — laufen gegen eine Kopie der DB (`data/esg_lawparse_test.db`), nie gegen `data/esg.db` |
| `test_cache_stability.py` | Beweist die Wortstabilitaet der Begruendungen (6 Szenarien, eigene DB `data/esg_cache_test.db`). Ohne Argument mit Platzhalter statt LLM (kostenlos), mit `--live` echte Calls |
| `regulations.py` | 20 Regulierungen + Guidelines-Map + Veröffentlichungs- **und Anwendungsdaten** + Auswahllisten |
| `watchdog.py` | Wöchentlicher Aktualitäts-Wächter (Cron auf dem VPS), schreibt `watchdog_runs` |
| `i18n.py` | Übersetzungen (6 Sprachen) |
| `db.py` | SQLite-Schema, Migrationen, Cache-Zugriff |
| `deadlines.py` | Leitet je Regulierung und Profil den fuer DIESES Unternehmen geltenden Anwendungsbeginn ab (Phase-in-Stufen); rein deterministisch, kein LLM |
| `thresholds.py` | Erkennt Naehe zu Schwellenwerten (±20 %) fuer die "Was waere wenn"-Hinweise |
| `test_deadlines.py` | Tests zu beidem plus CSR-RUG-Regel; ohne DB, Netz und LLM |
| `test_login_throttle.py` | Tests zur Login-Bremse und zum Zeitgleichlauf beider Fehlerpfade (16 Blöcke, eigene DB `data/esg_login_test.db`, kein Netz, kein LLM) |
| `views.py` | Card-Renderer (Kennzahl-Hervorhebung, "Gilt ab", "Erste Schritte", Schwellen-Hinweise) |
| `pdfexport.py` | PDF-Export der Ergebnisse (reportlab, textil+mode-CD) |
| `autofill.py` | KI-Autofill der Stammdaten (Wikipedia/Wikidata/Website + LLM-Extraktion) |
| `templates/base.html` | Layout, CSS, Logo, Topbar, Footer |
| `templates/dashboard.html` | Hauptseite (Stammdaten + "Jetzt prüfen" + "Regulierungsliste"-Button) |
| `templates/regulierungsliste.html` | Tabelle aller 20 Regs + Guidelines + Stand |
| `templates/login.html`, `fullscreen.html`, `analysis.html` | Auth, Fullscreen, Progress-Page |
| `static/images/textil-mode-logo.png` | offizielles textil+mode-Logo (1925x437) |
| `Dockerfile` | Python 3.12-slim + Gunicorn; **muss `static/` und `templates/` kopieren** |
| `docker-compose.hostinger.yml` | Compose-Dummy/Vorlage (nur Platzhalter — echte Keys live im Hostinger-UI) |
| `.github/workflows/docker-build.yml` | Build-Push nach ghcr.io |

---

## Login-Bremse — Betrieb und Notausgang

Gegen Passwort-Durchprobieren greifen zwei Bremsen (Schwellen und Begründung
stehen als Kommentar in `db.py`, Abschnitt „Login-Bremse"):

| Bremse | Schwelle | Sperre |
|---|---|---|
| je **(Konto, Quell-IP)** | 5 Fehlversuche / 15 min | 60 s, verdoppelnd, Deckel 15 min |
| je **Quell-IP** (alle Konten) | 30 Fehlversuche / 60 min | 15 min ab dem letzten Versuch |

Wichtig für das Verständnis: Die Kontobremse hängt **am Paar (Konto, IP)**, nicht
am Konto allein. Sonst könnte jemand ein fremdes Konto — insbesondere das
Admin-Konto — durch Dauerbeschuss aussperren. So sperrt ein Angreifer nur seine
eigene Adresse; der Inhaber kommt von seiner Adresse weiter hinein.

Die Quell-IP kommt hinter nginx aus **`X-Real-IP`** (nginx setzt den Header
selbst). `X-Forwarded-For` dient nur als Rückfall, und dann zählt der **letzte**
Eintrag: die nginx-Konfig nutzt `$proxy_add_x_forwarded_for`, hängt die echte
Adresse also hinten an und lässt vom Client mitgeschickte Werte vorne stehen.
Beide Header werden nur ausgewertet, wenn die Gegenstelle im privaten Netz sitzt
— über den direkt offenen Port sind sie wirkungslos.

Gezählt wird persistent in der Tabelle `login_attempts`; ein Container-Neustart
hebt eine laufende Sperre also **nicht** auf. Einträge älter als 3 Stunden
räumt die App selbst weg.

**Notausgang, wenn niemand mehr hineinkommt:**

```bash
docker exec esg-ki-textil-mode python -m db unlock mschuckert@textil-mode.de
```

Das löscht alle Fehlversuch-Einträge dieses Kontos (über alle Adressen) und gibt
aus, wie viele es waren. Die IP-Bremse bleibt davon unberührt — wer auch die
lösen muss, leert `login_attempts` ganz:

```bash
docker exec esg-ki-textil-mode python3 -c "import sqlite3; c=sqlite3.connect('/app/data/esg.db'); c.execute('DELETE FROM login_attempts'); c.commit()"
```

**Restrisiko, bewusst getragen:** Wer über viele Adressen verfügt (Botnetz),
umgeht die Kontobremse, weil je Adresse nur vier Versuche anfallen. Gegen ihn
wirkt allein die IP-Bremse mit 30 Versuchen je Stunde und Adresse. Der Preis
einer kontoweiten Sperre wäre die Verfügbarkeit des Kontos — und die wiegt hier
schwerer.

---

## Watchdog auf dem VPS einrichten (einmalig, macht der Nutzer)

Woechentlich montags 03:15 Uhr, Log nach `/var/log/esg-watchdog.log`:

```bash
(crontab -l 2>/dev/null; echo '15 3 * * 1 docker exec esg-ki-textil-mode python watchdog.py >> /var/log/esg-watchdog.log 2>&1') | crontab -
```

Ergebnis danach unter https://ki-textil-mode.de/esg/admin/regulierungs-status (nur Admin-Konto).
Ein Lauf dauert ~45 s und kostet nur dann LLM-Tokens, wenn sich ein Text geaendert hat;
`python watchdog.py --no-llm` erfasst Aenderungen ohne Zusammenfassung.

---

## Verifikations-Checks (smoke-tests nach Deploy)

1. https://ki-textil-mode.de/esg/ (bzw. Legacy https://schuckert.cloud/regulierungs-check) → Login-Seite laedt, Logo oben links sichtbar, Footer "© 2026 · Alle Rechte vorbehalten".
2. Nach Login: Dashboard mit Button "Regulierungsliste" oben rechts neben "Jetzt pruefen". Rechts in der Rechts-Spalte die Checkbox "EU-Importeur / erstmaliges Inverkehrbringen in der EU".
3. https://ki-textil-mode.de/esg/regulierungsliste → Tabelle mit 20 Zeilen, Stand = Veroeffentlichungsdatum (DD.MM.YYYY), Guidelines klickbar.
4. Footer unten rechts: `<details>` "Hinweis" → auf Klick Popover mit Claude-Code-/Codex-Text.
5. "Jetzt pruefen" laeuft bis 20/20 durch, keine rote ✕-Fehlerkarte. "Greifende Stelle" max. ~280 Zeichen.

---

## Konventionen für Claude Code

- Scratch-Dateien (`_*.txt`, Debug-Screenshots) und `Bugreport/`, `.playwright-mcp/`, `.claude/` sind seit 2026-06-10 in `.gitignore`; trotzdem nie manuell stagen.
- **Nur explizit geänderte Dateien stagen**, kein `git add -A`.
- Syntax-Check vor Commit: `./.venv/Scripts/python.exe -m py_compile app.py db.py fetcher.py regulations.py llm.py i18n.py views.py`.
- Feature-Arbeit: neuer Commit, neuer Tag, wenn wieder "stabil".

---

## Offene Punkte / Ideen

- **Fehlgeschlagene Aktualisierungen während eines Analyse-Laufs sind nicht dauerhaft sichtbar.**
  `_run_analysis_bg` schreibt sie nur ins Container-Log (`[analysis] <key>: <error>`); auf
  `/admin/regulierungs-status` erscheinen sie erst, wenn der wöchentliche Watchdog denselben
  Fehler erneut sieht (`watchdog_runs.errors_json`). Für dauerhafte Sichtbarkeit bräuchte
  `law_texts` eine Spalte `last_error` samt Anzeige und i18n — bewusst nicht mitgemacht, weil es
  den Analyse-Pfad berührt.
- **`reg_hash` deckt nicht alles ab, was in den Prompt geht.** Enthalten sind `criteria`,
  `_PROMPT_VERSION`, Sprache und Gesetzesstand — nicht aber `key_article`, die
  Guideline-Texte und `FULLTEXT_MAX_CHARS`. Ändert sich nur eines davon, bleibt die alte
  Begründung stehen. Bewusst offen gelassen: Guidelines werden bei jedem Lauf frisch
  geladen, ihr Hash würde den Cache oft ohne inhaltlichen Grund verwerfen. Wer `key_article`
  oder `FULLTEXT_MAX_CHARS` ändert, zählt ersatzweise `_PROMPT_VERSION` hoch.
- **Die Zwei-Satz-Regel hält das Modell nicht immer ein** (Gemini 2.5 Flash Lite: in
  etwa 5 von 20 Fällen ein dritter Satz). Inhaltlich korrekt, nur stilistisch uneinheitlich;
  die deterministischen Bausteine sind davon nicht betroffen.
- **`analysis_cache` wächst unbegrenzt.** Je Gesetzesänderung bleibt eine alte Zeile je
  Profil-Hash liegen (die None-Fallback-Logik lebt davon). Bei ~500 Byte pro Zeile
  unkritisch; wenn es je stört, die ältesten Zeilen je `(reg_key, profile_hash)` kappen.
- Einige Guideline-URLs sind Landing-Pages (nicht direkt der Leitfaden-PDF). Feintuning später.
- Beim nächsten Deploy: Hostinger-Pull-Konfig auf `ghcr.io/textil-mode/…` umstellen (siehe CI/CD).
- Empfehlung: Budget-Alert in Google Cloud Billing setzen (z. B. 5 €/Monat).
- ⚠️ Sicherheit: Bis 2026-06-10 lagen ein OpenRouter- und ein Anthropic-Key im Klartext in der eingecheckten `docker-compose.hostinger.yml` (und damit in der Git-History). Beide Keys sollten rotiert/widerrufen werden.
