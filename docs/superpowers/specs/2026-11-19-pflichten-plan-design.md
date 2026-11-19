# Pflichten-Plan („Meine Pflichten“): Design

Stand 19.11.2026. Baustein 1 des Pflichten-Navigators (Herleitung:
`H:\KI-Projekte\Berichtspflichten\TOOL-IDEE.md` und `BEDARFE.md`, Projekt
`wissen-berichtspflichten`). Wird als Erweiterung des ESG-Regulierungs-Checks gebaut, nicht als
eigene App.

## 1. Absicht

Der Check endet heute bei „Sie sind betroffen“ und zeigt je Karte 2–4 erste Schritte ohne
Datum. Mitglieder brauchen aber die nächste Stufe: **was zu tun ist, bis wann, mit welchen
Daten, von wem**. Gleichzeitig darf die Pflege der Schritte und Fristen den Verband nicht
dauerhaft binden. Deshalb rechnen sich die Fristen aus Regeln selbst, Gesetzesänderungen
erzeugen KI-Vorschläge, und ein Mensch gibt sie mit einem Klick frei.

Entscheidungen des Nutzers (Michael Schuckert, Admin):
- Form: **laufende Arbeitsliste** im Check (nicht ein Plan zum Ausdrucken).
- Pflege: **weitgehend automatisch, aber mit Freigabe durch einen Menschen**. Keine
  Vollautomatik (frühere KI-Fehler im Check: CSRD-Schwellen ODER statt UND, veraltete
  CSDDD-Schwellen; Haftung des Verbands).
- Freigabe: **vorerst allein der Haupt-Admin** (fest hinterlegtes Konto in `ADMIN_EMAILS`).

## 2. Ziele

1. Neuer Menüpunkt **„Meine Pflichten“** für angemeldete Konten. Er baut sich aus dem
   **letzten Prüfergebnis** auf: alle Regulierungen mit `applies` = `ja` oder `moeglich`.
2. Je Regulierung eine Liste von **Schritten**. Jeder Schritt zeigt: Titel, kurze Beschreibung,
   **Frist** (unternehmensindividuell berechnet), **Rolle** (Geschäftsführung, Einkauf,
   Personal, Logistik/Versand, Produktentwicklung, Nachhaltigkeit, Finanzen), **benötigte
   Daten**, Link auf offizielle Quelle oder Leitfaden, **„Geprüft am“** des Eintrags.
3. Das Mitglied kann je Schritt **abhaken** und eine **zuständige Person als freien Text**
   eintragen (z. B. „Frau Meier, Einkauf“).
4. **Erinnerungen per Mail** an den Kontoinhaber: 30 und 7 Tage vor einer Frist, dazu eine
   **Monatsübersicht** am Monatsersten (offene Schritte der nächsten 90 Tage, überfällige).
   Abbestellbar.
5. **Kalender-Export (.ics)** aller Fristen des Kontos.
6. **Fristen als Regeln**, nicht als feste Daten (siehe 6.2). Ändert sich ein
   Anwendungsbeginn, ziehen alle abhängigen Fristen und Erinnerungen automatisch nach.
7. **Änderungsvorschläge mit Freigabe**: Meldet der Watchdog einen geänderten Gesetzestext
   oder ändert sich ein Anwendungsbeginn, erstellt die KI einen Vorschlag (Vorher/Nachher,
   Textstelle als Beleg, Übersetzungen). Der Admin bekommt eine Mail, prüft auf einer
   Admin-Seite und klickt **Freigeben** oder **Verwerfen**. Erst danach sehen Mitglieder die
   Änderung; nur Betroffene bekommen einen Hinweis.
8. **Admin-Pflege von Hand**: Schritte anlegen, ändern, deaktivieren, sortieren, als geprüft
   markieren, ohne Deploy.
9. Alle Texte für Mitglieder in den **sechs Sprachen** des Checks.

## 3. Nicht-Ziele (diese Runde)

- **Neue Regulierungen im Check** (Textil-EPR Deutschland, VerpackG, Entgelttransparenz,
  CBAM). Sie sind für den Pflichten-Plan wichtig, aber ein eigener Schritt nach dem bekannten
  Muster der Katalogerweiterung (`test_katalog_erweiterung.py`). Der Plan zeigt sie
  automatisch, sobald es die Karten gibt. *(Eigene Festlegung, um den Umfang zu halten.)*
- **Kopplung an den Gesetzesradar** (eigenes Projekt `tool-gesetzesradar`). Das ist Baustein 2.
  Diese Runde nutzt nur die Auslöser, die im Check schon existieren.
- Konten für Kolleginnen und Kollegen, Aufgaben an Dritte verschicken, Rechte je Schritt.
- PDF-Export des Plans (später als Erweiterung von `pdfexport.py` möglich).
- Mehrere Freigabeberechtigte (später: alle Admins, einer reicht).

## 4. Anti-Ziele (wäre ein Fehlschlag, auch wenn es technisch läuft)

- Eine KI-Änderung wird **ohne Freigabe** für Mitglieder sichtbar oder löst Mails aus.
- Ein Mitglied verliert seine Häkchen oder Zuständigkeiten, weil es neu prüft oder ein Schritt
  geändert wurde.
- Erinnerungen kommen doppelt, zu einer nicht mehr gültigen Frist oder an abgemeldete Konten.
- Der Plan liest sich wie verbindliche Rechtsberatung (Haftungshinweis wie auf den Karten
  nötig; Freigabe der Texte durch die Rechtsabteilung bleibt offen, wie beim Assistenten).
- Personenbezogene Daten Dritter werden mehr als nötig gespeichert (Zuständigkeit ist freier
  Text, den das Mitglied selbst einträgt; kein Pflichtfeld).

## 5. Bauweisen (betrachtet)

| Bauweise | Vorteil | Nachteil |
|---|---|---|
| **A: Katalog im Code** (wie `FIRST_STEPS_BY_REG_KEY` + `i18n.FIRST_STEPS`) | einfach, versioniert in Git, testbar | jede Änderung braucht Commit und Deploy; „Freigeben mit einem Klick“ geht nicht |
| **B: Katalog in der Datenbank mit Freigabe-Seite** (gewählt) | Änderungen ohne Deploy, Vorschlag → Freigabe → sichtbar in einem Schritt, Prüfdatum je Eintrag | mehr Code (Admin-Oberfläche, Versionierung), Katalog nicht mehr in Git |
| C: Eigene App | unabhängig | zweites Profil und zweites Konto für Mitglieder, genau das Problem aus BEDARFE.md |

Gewählt: **B**, vom Nutzer an Claude übertragen („lets go“). Ausgleich für den Nachteil
„nicht in Git“: Jede Änderung wird als Version gespeichert (wer, wann, vorher/nachher), und
ein Admin-Export als JSON erlaubt eine Sicherung im Repo.

## 6. Entwurf

### 6.1 Startbestand des Katalogs

Beim ersten Start werden die vorhandenen ersten Schritte (`FIRST_STEPS_BY_REG_KEY`,
Texte aus `i18n.FIRST_STEPS`, 34 Regulierungen, 6 Sprachen) in die Datenbank übernommen.
Rolle, Frist und benötigte Daten sind dann leer; der Admin ergänzt sie. Damit es nicht bei
leeren Feldern bleibt, erzeugt ein einmaliger Lauf **KI-Vorschläge für Rolle, Frist-Regel und
Daten** je Schritt. Sie landen als normale Vorschläge in der Freigabe-Liste (gleicher Weg wie
in 6.4). Die Karten im Check zeigen ab dann die ersten Schritte aus der Datenbank, damit es
nur eine Quelle gibt.

### 6.2 Frist-Regeln

Jeder Schritt hat genau eine Frist-Regel:

| Typ | Beispiel | Berechnung |
|---|---|---|
| `relativ` | „6 Monate vor Anwendungsbeginn“, „am Anwendungsbeginn“ | Anker ist `deadlines.deadline_for(reg_key, profil)["gilt_ab"]` (berücksichtigt schon Staffelungen nach Größe) plus Versatz in Tagen oder Monaten |
| `fest` | „31.12.2027“ | festes Datum |
| `jaehrlich` | „jährlich bis 31.05.“ | nächstes Vorkommen ab heute |
| `keine` | Daueraufgabe | keine Frist, keine Erinnerung |

Sonderfälle:
- Anwendungsbeginn **offen** (`gilt_ab` leer, z. B. CSRD-Umsetzungsgesetz): Frist zeigt
  „offen, hängt vom Gesetz ab“, keine Erinnerung.
- **Pflicht gilt schon** (Anwendungsbeginn vorbei, Stand heute 29 von 34 Regulierungen):
  relative Fristen werden zu **„laufend“, ohne Datum** (Entscheidung des Nutzers, 19.11.2026).
  Keine 30/7-Tage-Erinnerung, kein .ics-Eintrag, nicht „überfällig“. Offene laufende Schritte
  erscheinen in der Monatsübersicht in einem eigenen Block „laufend“. Datierte Erinnerungen
  gibt es dort nur über `fest` und `jaehrlich`.
- Frist mit Datum **in der Vergangenheit** und Schritt nicht erledigt: „überfällig“.
- Die Frist wird bei jeder Anzeige und jedem Erinnerungslauf **neu berechnet**, nie
  gespeichert. Verschiebungen wirken dadurch sofort.

### 6.3 Ansicht „Meine Pflichten“

```
Meine Pflichten                              [Kalender (.ics)]  [Erinnerungen: an]
Grundlage: Prüfung vom 12.11.2026 · 5 Pflichten · 3 Schritte fällig in 90 Tagen

▾ EUDR – gilt für Sie ab 30.06.2027                         2 von 4 erledigt
  ☐ Betroffene Artikel und Zolltarifnummern ermitteln     bis 31.12.2026 · Einkauf
      Daten: Artikelliste mit KN-Code, Materialanteil Leder     [Zuständig: ______]
      Quelle: EU-Leitfaden ↗ · geprüft 19.11.2026
  ☐ Geodaten bei Lieferanten anfordern                   bis 31.03.2027 · Einkauf
  ☑ ...
▸ Textilkennzeichnung – gilt (Daueraufgabe)                 0 von 2 erledigt
▸ Entfällt nach neuer Prüfung (1)                            (eingeklappt)
```

- Sortierung der Pflichten nach nächster offener Frist, überfällige oben.
- Filter nach Rolle („nur Einkauf“), damit die Liste an eine Abteilung weitergegeben werden
  kann.
- Neue Prüfung: Häkchen und Zuständigkeiten bleiben (gebunden an die Schritt-ID).
  Pflichten, die nicht mehr greifen, wandern in „Entfällt“ (eingeklappt, mit Datum).
- Wurde ein Schritt nach dem Abhaken inhaltlich geändert (freigegebene Änderung), zeigt er
  „geändert am …, bitte prüfen“, bleibt aber abgehakt.
- Hinweis oben: Haftungshinweis wie im Check, KI-Kennzeichnung, „geprüft am“ je Schritt.
- Ohne Prüfergebnis: Verweis auf den Check.

### 6.4 Änderungsvorschläge und Freigabe

Auslöser:
1. **Watchdog** (`watchdog.py`, wöchentlich) meldet einen geänderten Text für eine
   Regulierung. Er erzeugt heute schon eine KI-Zusammenfassung. Neu: Für jede geänderte
   Regulierung, zu der es Schritte gibt, prüft die KI den neuen Text gegen die Schritte und
   schlägt Änderungen vor (oder meldet „keine Änderung an den Schritten nötig“ – dann kein
   Vorschlag, nur ein Vermerk).
2. **Geänderter Anwendungsbeginn** in `regulations.py` (`applies_from`, kommt per Deploy):
   Beim Start vergleicht die App den Wert mit dem zuletzt gespeicherten. Fristen ziehen
   ohnehin automatisch nach. Neu ist nur ein Hinweis an Betroffene; ein Vorschlag entsteht
   nur, wenn Schrittinhalte vom Datum abhängen (KI prüft).
3. **Startbestand** (6.1).

Ein Vorschlag enthält: Regulierung, Art (neu / ändern / deaktivieren), Vorher und Nachher je
Feld, die Textstelle aus dem Gesetz als Beleg (Ausschnitt + Link), die KI-Begründung, alle
sechs Sprachfassungen, den Auslöser.

Ablauf:
- Mail an den Haupt-Admin: „EUDR: Gesetzestext geändert, 2 Schritte betroffen“ mit Link auf
  `/admin/pflichten/vorschlaege`. Die Freigabe selbst passiert auf der Seite, nicht per Link in
  der Mail (ein Klick in der Mail wäre ohne Anmeldung angreifbar). *(Eigene Festlegung.)*
- Admin-Seite: Liste offener Vorschläge, je Vorschlag Vorher/Nachher nebeneinander, Beleg,
  Felder **vor der Freigabe editierbar**, Knöpfe **Freigeben** und **Verwerfen** (mit
  optionalem Grund).
- Freigeben: Schritt wird als neue Version gespeichert, „geprüft am“ = heute, sofort sichtbar.
  Betroffene Mitglieder (letztes Prüfergebnis enthält die Regulierung mit `ja`/`moeglich`,
  Erinnerungen nicht abbestellt) bekommen eine kurze Mail in ihrer Sprache: „Für EUDR hat sich
  etwas geändert: …“ mit Link auf „Meine Pflichten“. Mehrere Freigaben am selben Tag werden zu
  einer Mail je Mitglied gebündelt.
- Verwerfen: Vorschlag bleibt mit Grund im Verlauf, nichts ändert sich.
- Wer freigeben darf: vorerst nur Konten aus `ADMIN_EMAILS` (nicht die per Oberfläche
  ernannten Admins). Später erweiterbar.

### 6.5 Erinnerungen

- Täglicher Lauf per Cron (gleiches Muster wie `testzugang.py`/`linkwaechter.py`:
  `docker exec esg-ki-textil-mode python pflichten_erinnerung.py`, z. B. 06:30), nur im
  Hauptcontainer.
- Je Konto mit Erinnerungen an: Schritte mit Frist in genau 30 bzw. 7 Tagen (oder überholt,
  falls ein Lauf ausfiel: Fenster statt exakter Tag) und nicht erledigt → eine gesammelte Mail.
  Am Monatsersten zusätzlich die Übersicht.
- Doppelversand verhindert ein Protokoll (Konto, Schritt, Art, berechnete Frist). Ändert sich
  die Frist, ist es eine neue Erinnerung.
- Mail-Sprache = Sprache des Kontos. Abbestellen über einen Link auf die Kontoseite
  (Anmeldung nötig). *(Eigene Festlegung; ein Abmeldelink ohne Anmeldung wäre bequemer, braucht
  aber ein eigenes Token.)*
- Versand über `mailer.send`, Eintrag im `mail_log` mit eigenem `purpose`.
- Monatliches Lebenszeichen an den Admin wie beim Linkwächter (Anzahl versandter
  Erinnerungen), damit ein ausgefallener Cron auffällt.

### 6.6 Datenmodell (Vorschlag, Details beim Bau)

- `pflicht_schritte`: id, reg_key, sortierung, rolle, frist_typ, frist_wert, link, quelle,
  aktiv, version, geprueft_am, geaendert_am
- `pflicht_schritt_texte`: schritt_id, sprache, titel, beschreibung, daten
- `pflicht_schritt_versionen`: schritt_id, version, inhalt_json, geaendert_am, geaendert_von,
  vorschlag_id
- `pflicht_vorschlaege`: id, reg_key, schritt_id (leer bei neu), art, ausloeser,
  ausloeser_ref, vorher_json, nachher_json, beleg, begruendung, status, erstellt_am,
  entschieden_am, entschieden_von, grund
- `nutzer_schritte`: user_id, schritt_id, erledigt_am, zustaendig, gesehen_version
- `pflicht_erinnerungen`: user_id, schritt_id, art, frist, gesendet_am
- `users`: neue Spalte `erinnerungen` (an/aus, Standard an)
- Kontolöschung (`db.delete_user`) muss die neuen Nutzer-Tabellen mitlöschen (Kaskade).

### 6.7 Festlegungen nach der Builder-Prüfung (eigene Festlegungen, zur Kontrolle)

- **Einführung:** „Meine Pflichten“ ist nach dem Deploy zunächst **nur für Admins sichtbar**
  (Schalter `PFLICHTEN_PLAN_AKTIV` in der Datenbank, umlegbar auf der Admin-Seite). Solange er
  aus ist, gehen keine Erinnerungen und keine Änderungsmails an Mitglieder. Freigaben aus dem
  Startbestand (6.1) lösen nie Änderungsmails oder „geändert, bitte prüfen“ aus.
- **Fremdsprachen bei Handänderungen:** Auch eine Handänderung des Admins läuft als Vorschlag:
  Der Admin speichert den deutschen Text, die KI übersetzt, der Admin sieht alle sechs
  Fassungen und gibt dann frei. Keine KI-Übersetzung wird ohne diese Freigabe sichtbar.
- **Wer pflegt:** Handpflege und Freigabe nur für Konten aus `ADMIN_EMAILS`; ernannte Admins
  sehen die Seiten lesend.
- **Legacy-Container** (`esg-regulierungs-check`, schuckert.cloud): Funktion per Env-Variable
  abgeschaltet; die Karten lesen dort weiter die ersten Schritte aus dem Code. Im
  Hauptcontainer ist die Datenbank die einzige Quelle.
- **Datumsänderungen:** Erkannt wird auf Ebene des Mitglieds. Der tägliche Lauf speichert je
  Konto und Regulierung den zuletzt berechneten Anwendungsbeginn
  (`deadline_for(...)["gilt_ab"]`); weicht er ab, gibt es einen Hinweis. So fallen auch
  Änderungen an den Staffelkonstanten in `deadlines.py` auf, und nur die wirklich betroffene
  Größenklasse bekommt Post.
- **Jährliche Schritte:** Das Häkchen gilt für eine Periode (bis zum nächsten Stichtag). Danach
  ist der Schritt wieder offen; frühere Erledigungen bleiben im Verlauf sichtbar („2026
  erledigt am …“). Damit geht kein Häkchen verloren.
- Weitere kleine Festlegungen: Mail-Sprache = `signup_lang`, sonst Deutsch; Fristen mit dem
  aktuellen Profil; Fehlerkarten (`applies` = `error`) führen nicht zu „Entfällt“; keine
  Erinnerungen an gesperrte oder nicht freigeschaltete Konten; gebündelte Änderungsmails über
  den täglichen Lauf; neue Regulierungen aus dem Code werden beim Start nachgesät.

## 7. Randbedingungen

- Stack bleibt: Flask 3, SQLite, Gemini über `llm.py` (mit Ausweichmodellen), Mail über
  `mailer.py`, Cron im Host per `docker exec`, Deploy per `/root/esg_redeploy.py` für beide
  Container.
- Neue Tabellen per `CREATE TABLE IF NOT EXISTS` in `db.init_db`, Migrationen idempotent.
- Tests offline im Stil der vorhandenen `test_*.py`; Fristberechnung und Erinnerungslogik mit
  festem „heute“ (keine Zeitbomben, siehe Commit 7ab5d93).
- Vor dem Deploy: Pflichtprüfung mit dem Skill `web-sicherheit` (neue Admin-Seite, neue
  Formulare, Mailversand).
- **Datenschutzerklärung** nachziehen: Erinnerungsmails, gespeicherte Häkchen und
  Zuständigkeitstexte, Übermittlung von Gesetzestext an Gemini für Vorschläge (keine
  Mitgliederdaten).
- Beim KI-Vorschlag gehen **keine Mitgliederdaten** an das Modell, nur Gesetzestext und
  Katalog.

## 8. Dem Bau überlassen

- Genaue Gestaltung der Admin-Seite und der Ansicht (im vorhandenen Stil des Checks).
- Prompt für die Vorschläge, Format der KI-Antwort, Umgang mit unbrauchbaren Antworten.
- Ob die Ansicht eine eigene Seite oder ein Reiter neben dem Ergebnis ist.
- Reihenfolge der Umsetzung; Vorschlag: Datenmodell + Startbestand → Ansicht mit Häkchen →
  Frist-Regeln + .ics → Admin-Pflege von Hand → Erinnerungen → Vorschläge mit Freigabe.
