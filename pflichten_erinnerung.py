# -*- coding: utf-8 -*-
"""Pflichten-Plan: taeglicher Lauf mit Erinnerungen, Hinweisen und Lebenszeichen.

Je Konto, das Post bekommen darf (freigeschaltet, nicht gesperrt,
Erinnerungen an), hoechstens **eine** Mail je Lauf. Sie buendelt:

* **Erinnerungen** an offene Schritte mit Datum: Frist in 0–7 Tagen (Art `7`)
  bzw. 8–30 Tagen (Art `30`). Fenster statt exakter Tag, damit ein
  ausgefallener Lauf nichts verschluckt; das Protokoll
  `pflicht_erinnerungen (Konto, Schritt, Art, Frist)` verhindert Doppelversand.
  Aendert sich die Frist, ist es eine neue Erinnerung. `laufend`, `offen`,
  `keine` und erledigte Schritte erinnern nie.
* **Hinweise** aus `pflicht_hinweise` (Art `inhalt` aus Freigaben, Art `datum`
  aus diesem Lauf). Der Mailtext entsteht hier aus reg_key + Art in der
  Sprache des Kontos; `text_de` ist nur intern. Hinweise zu Pflichten, die
  fuer das Konto entfallen sind, werden still als gesendet markiert.
* **Datumsaenderungen** (Spec 6.7): je Konto und Pflicht wird der zuletzt
  berechnete Anwendungsbeginn (`deadline_for(...)["gilt_ab"]`) in
  `nutzer_pflichten.letzter_gilt_ab` gespeichert; weicht er ab (und gab es
  einen Vorwert), entsteht ein Hinweis `datum`.
* **Monatsuebersicht** im ersten erfolgreichen Lauf des Monats (normal am
  1.; scheitert der Versand oder faellt der Lauf aus, holt der naechste Lauf
  sie nach): faellig in 90 Tagen, ueberfaellig, Block „laufend“. Marker je
  Konto: `pflicht_erinnerungen` mit schritt_id 0, art 'monat', frist 'YYYY-MM'.

Ebenso im ersten erfolgreichen Lauf des Monats ein Lebenszeichen an die
Haupt-Admins mit der Zahl der Erinnerungsmails der **letzten 30 Tage** (ab dem
Stichtag) aus `mail_log` (laenger haelt das Protokoll nichts vor). Marker:
Einstellung `lebenszeichen_monat`. Bleibt es aus, laeuft der Cron nicht.

Alles nur, wenn die Funktion an ist (`PFLICHTEN_PLAN` nicht `aus`) und der
Schalter `pflichten_plan_aktiv` = `1` steht.

Cron (Hauptcontainer):
    30 6 * * * docker exec esg-ki-textil-mode python pflichten_erinnerung.py >> /var/log/esg-pflichten.log 2>&1

Von Hand:
    python pflichten_erinnerung.py --probe                     # nichts senden, nur zeigen
    python pflichten_erinnerung.py --heute 2026-12-01 --probe  # Stichtag vorgeben

`--probe` verschickt nichts und markiert nichts (keine Versandvermerke, keine
Hinweise, kein `letzter_gilt_ab`, kein Lebenszeichen-Marker). Es gleicht aber
wie jeder Planaufruf `nutzer_pflichten` mit dem letzten Pruefergebnis ab
(`plan_fuer` -> `sync_pflichten`): neue Zeilen bzw. `entfallen_am` werden
geschrieben — dasselbe passiert beim naechsten Aufruf von „Meine Pflichten“.
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from typing import Callable, Optional

from dotenv import load_dotenv

# VOR den Projekt-Importen: db.py liest `ESG_DB_PATH` beim Import. Ohne
# override, damit Tests (und der Container mit eigener Umgebung) Vorrang haben.
load_dotenv(override=False)

import db  # noqa: E402
import mailer  # noqa: E402
import pflichten  # noqa: E402
import pflichten_db as pdb  # noqa: E402
from i18n import normalize_lang, t  # noqa: E402

PURPOSE = "pflichten_erinnerung"
PURPOSE_LEBENSZEICHEN = "pflichten_lebenszeichen"
PFAD_PLAN = f"{mailer.APP_PFAD}/meine-pflichten"
PFAD_KONTO = f"{mailer.APP_PFAD}/passwort-aendern"   # dort liegt der Erinnerungs-Schalter

Versand = Callable[[str, str, str], Optional[str]]


def _leer() -> dict:
    return {"erinnerungen": 0, "uebersichten": 0, "hinweise": 0, "konten": 0}


def _datum(d: date) -> str:
    return d.strftime("%d.%m.%Y")


def _jetzt() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def _aktiv() -> bool:
    return pdb.funktion_aktiv() and pdb.einstellung("pflichten_plan_aktiv", "0") == "1"


# ---------------------------------------------------------------------------
# Inhalt je Konto
# ---------------------------------------------------------------------------
def _datumsaenderungen(uid: int, plan: dict, today: date, probe: bool) -> list[dict]:
    """Vergleicht `gilt_ab` mit `letzter_gilt_ab`, speichert den neuen Wert.

    Rueckgabe: neue Hinweise (im Probelauf nur im Speicher, sonst angelegt).
    """
    if not plan["hat_profil"]:
        return []
    vorher = {r["reg_key"]: r["letzter_gilt_ab"] for r in pdb.nutzer_pflichten(uid)}
    neu: list[dict] = []
    for p in plan["pflichten"]:
        if p["entfaellt"]:
            continue
        alt, jetzt = vorher.get(p["reg_key"]), p["gilt_ab"] or ""
        if alt == jetzt:
            continue
        if alt is not None:
            text = f"{p['reg_key']}: Anwendungsbeginn {alt or 'offen'} -> {jetzt or 'offen'}"
            hid = None if probe else pdb.neuer_hinweis(uid, p["reg_key"], "datum", text, today)
            neu.append({"id": hid, "reg_key": p["reg_key"], "art": "datum"})
        if not probe:
            pdb.setze_letzter_gilt_ab(uid, p["reg_key"], jetzt)
    return neu


def _faellige(uid: int, plan: dict, today: date) -> list[dict]:
    out = []
    for p in plan["pflichten"]:
        if p["entfaellt"]:
            continue
        for s in p["schritte"]:
            if s["erledigt"] or s["frist"]["art"] != "datum":
                continue
            frist = s["frist"]["datum"]
            tage = (frist - today).days
            art = "7" if 0 <= tage <= 7 else "30" if 8 <= tage <= 30 else None
            if art and not pdb.erinnerung_vorhanden(uid, s["id"], art, frist.isoformat()):
                out.append({"pflicht": p, "schritt": s, "art": art, "tage": tage})
    out.sort(key=lambda e: (e["schritt"]["frist"]["datum"], e["pflicht"]["name"].casefold()))
    return out


def _uebersicht(uid: int, plan: dict, today: date) -> dict | None:
    # Erster erfolgreicher Lauf des Monats: nur der Marker zaehlt, nicht der Tag.
    if pdb.erinnerung_vorhanden(uid, *pdb.MONATS_MARKER, today.strftime("%Y-%m")):
        return None
    bald, ueber, laufend = [], [], []
    for p in plan["pflichten"]:
        if p["entfaellt"]:
            continue
        for s in p["schritte"]:
            if s["erledigt"]:
                continue
            if s["ueberfaellig"]:
                ueber.append((p, s))
            elif s["frist"]["art"] == "datum" and (s["frist"]["datum"] - today).days <= 90:
                bald.append((p, s))
            elif s["frist"]["art"] == "laufend":
                laufend.append((p, s))
    if not (bald or ueber or laufend):
        return None
    bald.sort(key=lambda e: e[1]["frist"]["datum"])
    ueber.sort(key=lambda e: e[1]["frist"]["datum"])
    return {"bald": bald, "ueberfaellig": ueber, "laufend": laufend}


def _aktive_keys(plan: dict) -> set[str]:
    return {p["reg_key"] for p in plan["pflichten"] if not p["entfaellt"]}


def _hinweis_zeilen(hinweise: list[dict], plan: dict, lang: str) -> list[str]:
    """Eine Zeile je (Regulierung, Art); gleiche Hinweise werden zusammengefasst.

    Nur Hinweise zu Pflichten, die fuer das Konto (noch) gelten.
    """
    pflichten_nach_key = {p["reg_key"]: p for p in plan["pflichten"] if not p["entfaellt"]}
    zeilen, gesehen = [], set()
    for h in hinweise:
        schluessel = (h["reg_key"], h["art"])
        p = pflichten_nach_key.get(h["reg_key"])
        if p is None or schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        name = p["name"]
        if h["art"] == "datum":
            gilt_ab = p.get("gilt_ab") or t("pflichten_mail_datum_offen", lang)
            zeilen.append(t("pflichten_mail_hinweis_datum", lang).format(name=name, datum=gilt_ab))
        else:
            zeilen.append(t("pflichten_mail_hinweis_inhalt", lang).format(name=name))
    return zeilen


def _schritt_zeile(p: dict, s: dict, lang: str, tage: int | None = None) -> str:
    teile = [f"- {p['name']}: {s['titel']}"]
    if s["frist"]["art"] == "datum":
        frist = t("pflichten_bis", lang).format(datum=_datum(s["frist"]["datum"]))
        if s["ueberfaellig"]:
            frist = f"{t('pflichten_ueberfaellig', lang)}, {frist}"
        elif tage is not None:
            frist = f"{frist}, {t('pflichten_mail_noch_tage', lang).format(tage=tage)}"
        teile.append(f" ({frist})")
    return "".join(teile)


def mailtext(lang: str, faellig: list[dict], hinweis_zeilen: list[str],
             uebersicht: dict | None) -> tuple[str, str]:
    """Betreff und Text der gesammelten Mail in `lang`."""
    teile = [t("pflichten_mail_anrede", lang), "", t("pflichten_mail_einleitung", lang)]
    if faellig:
        teile += ["", t("pflichten_mail_faellig", lang)]
        teile += [_schritt_zeile(e["pflicht"], e["schritt"], lang, e["tage"]) for e in faellig]
    if hinweis_zeilen:
        teile += ["", t("pflichten_mail_hinweise", lang)]
        teile += [f"- {z}" for z in hinweis_zeilen]
    if uebersicht:
        # Was oben unter "Fristen in den naechsten Tagen" steht, nicht noch einmal
        # im 90-Tage-Block; bleibt nichts, entfaellt die Uebersicht in dieser Mail.
        schon = {e["schritt"]["id"] for e in faellig}
        bloecke = {k: [(p, s) for p, s in uebersicht[k]
                       if k != "bald" or s["id"] not in schon]
                   for k in ("ueberfaellig", "bald", "laufend")}
        if any(bloecke.values()):
            teile += ["", t("pflichten_mail_uebersicht", lang)]
        for schluessel, kopf in (("ueberfaellig", "pflichten_mail_ueberfaellig"),
                                 ("bald", "pflichten_mail_90"),
                                 ("laufend", "pflichten_mail_laufend")):
            if bloecke[schluessel]:
                teile += ["", t(kopf, lang)]
                teile += [_schritt_zeile(p, s, lang) for p, s in bloecke[schluessel]]
    teile += ["", t("pflichten_mail_link", lang).format(
                  link=mailer.oeffentlicher_link(PFAD_PLAN)),
              "", t("pflichten_mail_abbestellen", lang).format(
                  link=mailer.oeffentlicher_link(PFAD_KONTO)),
              "", t("pflichten_mail_gruss", lang)]
    return t("pflichten_mail_betreff", lang), "\n".join(teile)


# ---------------------------------------------------------------------------
# Versand
# ---------------------------------------------------------------------------
def _protokoll(empfaenger: str, purpose: str, status: str, wer: str, **kw) -> None:
    """`db.log_mail`, das nie wirft: ein kaputtes Protokoll aendert nichts am Versand."""
    try:
        db.log_mail(empfaenger, purpose, status, **kw)
    except Exception as exc:                                  # noqa: BLE001
        print(f"[pflichten] {wer}: mail_log nicht geschrieben ({status}): {exc!r}", flush=True)


def _senden(empfaenger: str, betreff: str, text: str, versand: Versand | None,
            purpose: str, wer: str) -> bool:
    """Ein Versuch; Ergebnis im `mail_log`. Wirft nie.

    `wer` erscheint in der Cron-Ausgabe (z. B. „Konto 17“), nie die Adresse.
    Ist der Versand gelungen, gilt die Mail als gesendet, auch wenn danach das
    Protokollieren scheitert.
    """
    try:
        if versand is not None:
            mid = versand(empfaenger, betreff, text)
        else:
            mid = mailer.send(empfaenger, betreff, text)
    except Exception as exc:                                  # noqa: BLE001
        _protokoll(empfaenger, purpose, "failed", wer, error=str(exc)[:300])
        print(f"[pflichten] {wer}: Mail fehlgeschlagen: {exc}", flush=True)
        return False
    _protokoll(empfaenger, purpose, "sent", wer, message_id=mid)
    return True


def _konto(konto: dict, today: date, versand: Versand | None, probe: bool,
           zaehler: dict) -> None:
    uid = konto["id"]
    lang = normalize_lang(konto.get("signup_lang"))
    plan = pflichten.plan_fuer(uid, lang, today)        # gleicht nutzer_pflichten ab
    neue_datum = _datumsaenderungen(uid, plan, today, probe)
    alle_hinweise = pdb.offene_hinweise(uid) + (neue_datum if probe else [])
    aktiv = _aktive_keys(plan)
    hinweise = [h for h in alle_hinweise if h["reg_key"] in aktiv]
    # Hinweise zu entfallenen Pflichten: still erledigen, nie mailen.
    stumm = [h["id"] for h in alle_hinweise if h["reg_key"] not in aktiv and h.get("id")]
    if stumm and not probe:
        pdb.hinweise_gesendet(stumm, _jetzt())
    faellig = _faellige(uid, plan, today)
    uebersicht = _uebersicht(uid, plan, today)
    if not (faellig or hinweise or uebersicht):
        return

    betreff, text = mailtext(lang, faellig, _hinweis_zeilen(hinweise, plan, lang), uebersicht)
    if probe:
        print(f"--- an {konto['email']} ({lang}) ---\nBetreff: {betreff}\n{text}\n", flush=True)
    elif not _senden(konto["email"], betreff, text, versand, PURPOSE, f"Konto {uid}"):
        return          # nichts als gesendet markieren; naechster Lauf versucht es wieder
    else:
        zeit = _jetzt()
        eintraege = [(e["schritt"]["id"], e["art"], e["schritt"]["frist"]["datum"].isoformat())
                     for e in faellig]
        if uebersicht:
            eintraege.append((*pdb.MONATS_MARKER, today.strftime("%Y-%m")))
        pdb.merke_erinnerungen(uid, eintraege, zeit)
        pdb.hinweise_gesendet([h["id"] for h in hinweise if h.get("id")], zeit)

    zaehler["konten"] += 1
    zaehler["erinnerungen"] += len(faellig)
    zaehler["hinweise"] += len(hinweise)
    zaehler["uebersichten"] += 1 if uebersicht else 0


def _lebenszeichen(today: date, versand: Versand | None, probe: bool) -> None:
    """Erster erfolgreicher Lauf des Monats: Zahl der Erinnerungsmails der letzten
    30 Tage (ab dem Stichtag `today`, damit `--heute` wirkt) an die Haupt-Admins.
    Scheitert der Versand, bleibt der Marker leer und der naechste Lauf versucht es.
    """
    monat = today.strftime("%Y-%m")
    if pdb.einstellung("lebenszeichen_monat") == monat:
        return
    seit = (today - timedelta(days=db.MAIL_LOG_KEEP_DAYS)).isoformat()
    zahlen = pdb.mail_zaehlen(PURPOSE, seit)
    gesendet, fehl = zahlen.get("sent", 0), zahlen.get("failed", 0)
    fehltext = (f" {fehl} Versuche sind fehlgeschlagen (Details im Mailprotokoll der "
                "Admin-Seite)." if fehl else "")
    betreff = "ESG-Check: Pflichten-Erinnerungen laufen"
    text = ("Hallo,\n\n"
            "dies ist das monatliche Lebenszeichen des täglichen Erinnerungslaufs im "
            f"Pflichten-Plan: In den letzten {db.MAIL_LOG_KEEP_DAYS} Tagen gingen "
            f"{gesendet} Erinnerungsmails an Mitglieder.{fehltext}\n\n"
            "Bleibt diese Nachricht am Anfang eines Monats aus, läuft der Erinnerungslauf "
            "nicht mehr (Container, Cron-Eintrag oder Mailversand auf dem Server prüfen).\n")
    if probe:
        print(f"--- Lebenszeichen an {', '.join(sorted(pdb.STAMM_ADMINS))} ---\n{text}",
              flush=True)
        return
    ok = [_senden(a, betreff, text, versand, PURPOSE_LEBENSZEICHEN, "Lebenszeichen")
          for a in sorted(pdb.STAMM_ADMINS)]
    if any(ok):
        pdb.setze_einstellung("lebenszeichen_monat", monat)


def lauf(today: date, versand: Versand | None = None, probe: bool = False) -> dict:
    """Ein taeglicher Durchgang. `versand(empfaenger, betreff, text)` ersetzt im
    Test `mailer.send`; `probe` sendet nichts, markiert nichts und gibt die Mails aus.
    """
    db.init_db()
    zaehler = _leer()
    if not _aktiv():
        return zaehler
    # Erst das Lebenszeichen: es zaehlt die Erinnerungen vor diesem Lauf.
    # Ein Fehler darin darf die Mitgliedermails nicht verhindern.
    try:
        _lebenszeichen(today, versand, probe)
    except Exception as exc:                                  # noqa: BLE001
        print(f"[pflichten] Lebenszeichen uebersprungen: {exc!r}", flush=True)
    for konto in pdb.erinnerungs_konten():
        try:
            _konto(konto, today, versand, probe, zaehler)
        except Exception as exc:                              # noqa: BLE001
            # Ein kaputtes Konto darf den Lauf fuer alle anderen nicht stoppen.
            print(f"[pflichten] Konto {konto['id']} uebersprungen: {exc!r}", flush=True)
    return zaehler


def main(argv: list[str]) -> int:
    today = date.today()
    if "--heute" in argv:
        i = argv.index("--heute")
        try:
            today = date.fromisoformat(argv[i + 1])
        except (IndexError, ValueError):
            print("Aufruf: python pflichten_erinnerung.py [--heute YYYY-MM-DD] [--probe]")
            return 2
    probe = "--probe" in argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")   # zh-Mails auf einer cp1252-Konsole
    db.init_db()
    if probe:
        print(f"Datenbank: {db.DB_PATH} · Stichtag {_datum(today)} · Probelauf, nichts wird "
              f"gesendet", flush=True)
        if not _aktiv():
            print("Funktion oder Schalter pflichten_plan_aktiv ist aus: es wuerde nichts "
                  "verschickt.", flush=True)
    zaehler = lauf(today, probe=probe)
    if probe or any(zaehler.values()):
        print(f"[{_datum(today)}] {zaehler['konten']} Mail(s): {zaehler['erinnerungen']} "
              f"Erinnerung(en), {zaehler['hinweise']} Hinweis(e), "
              f"{zaehler['uebersichten']} Uebersicht(en)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
