"""Pflichten-Plan: KI-Vorschlaege (Watchdog, Startbestand) und Uebersetzungen.

Die KI entwirft nur: Jede Aenderung landet als offener Vorschlag in
`pflicht_vorschlaege` und wird erst mit der Freigabe durch einen Haupt-Admin
sichtbar (Aufgabe 5). In keinen Prompt gehen Mitglieder-, Profil- oder
Kontodaten — nur Gesetzestext und Katalog.

Jede LLM-Funktion nimmt optional `ask(system, user) -> str` (async), damit die
Tests ohne Netz und ohne LLM laufen. Ohne `ask` wird `llm.LLMClient` benutzt.

Regel wie bei der Handpflege: In `nachher` stehen nur Felder und Textfelder,
die sich gegenueber dem aktuellen Schritt wirklich aendern. Sonst setzte die
Freigabe eines zweiten Vorschlags zum selben Schritt die uebrigen Felder auf
einen alten Stand zurueck.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import threading
from datetime import date
from typing import Awaitable, Callable
from urllib.parse import urlsplit

import db
import fetcher
import lawparse
import mailer
import pflichten
import pflichten_db as pdb
from regulations import REGULATIONS

log = logging.getLogger(__name__)

ZIELSPRACHEN = ("en", "es", "fr", "it", "zh")
Ask = Callable[[str, str], Awaitable[str]]

BELEG_MAX = 2000
BEGRUENDUNG_MAX = 2000


class VorschlagFehler(Exception):
    """Unbrauchbare KI-Antwort (kein JSON, falsche Form, fehlende Sprache)."""


def _standard_ask(max_tokens: int) -> Ask:
    async def ask(system: str, user: str) -> str:
        from llm import LLMClient
        return await LLMClient().ask(system, user, max_tokens=max_tokens, json_mode=True)
    return ask


def _json(antwort: str) -> dict:
    from llm import _extract_json
    try:
        data = _extract_json(antwort or "")
    except Exception as exc:  # noqa: BLE001 — auch abgeschnittene Antworten sind unbrauchbar
        raise VorschlagFehler(f"keine gueltige JSON-Antwort: {exc}") from exc
    if not isinstance(data, dict):
        raise VorschlagFehler("JSON-Antwort ist kein Objekt")
    return data


def _text(wert) -> str:
    return "" if wert is None else str(wert).strip()


def _reg(reg_key: str) -> dict:
    for reg in REGULATIONS:
        if reg["key"] == reg_key:
            return reg
    raise ValueError(f"unbekannte Regulierung: {reg_key!r}")


# ---------- Uebersetzung ----------

SYSTEM_UEBERSETZUNG = (
    "Du bist Fachuebersetzer fuer Texte zu Nachhaltigkeits- und Lieferkettenpflichten "
    "von Unternehmen. Uebersetze die deutschen Texte ins Englische (en), Spanische (es), "
    "Franzoesische (fr), Italienische (it) und vereinfachte Chinesische (zh). Behalte "
    "Artikelangaben, Zahlen, Daten, Abkuerzungen und Eigennamen von Rechtsakten bei; "
    "fuege nichts hinzu und lasse nichts weg. Antworte nur mit JSON der Form "
    '{"en": {...}, "es": {...}, "fr": {...}, "it": {...}, "zh": {...}} — '
    "in jeder Sprache genau dieselben Schluessel wie in der Eingabe."
)


async def uebersetzen(texte_de: dict, ask: Ask | None = None) -> dict[str, dict]:
    """Deutsche Textfelder -> `{lang: {...}}` fuer en, es, fr, it, zh.

    Uebersetzt genau die gegebenen Felder aus `titel`/`beschreibung`/`daten`
    und liefert je Sprache genau diese zurueck (fehlende Felder bleiben
    fehlend). Leere Texte bleiben leer, ohne LLM. Unbrauchbare Antwort ->
    `VorschlagFehler`.
    """
    felder = {f: _text(texte_de[f]) for f in pdb.TEXTFELDER if f in (texte_de or {})}
    zu_uebersetzen = {f: t for f, t in felder.items() if t}
    if not zu_uebersetzen:
        return {lang: dict(felder) for lang in ZIELSPRACHEN}
    ask = ask or _standard_ask(3000)
    user = ("Uebersetze diese Texte. Schluessel unveraendert lassen.\n"
            + json.dumps(zu_uebersetzen, ensure_ascii=False, indent=1))
    data = _json(await ask(SYSTEM_UEBERSETZUNG, user))
    out: dict[str, dict] = {}
    for lang in ZIELSPRACHEN:
        fassung = data.get(lang)
        if not isinstance(fassung, dict):
            raise VorschlagFehler(f"Uebersetzung {lang} fehlt")
        out[lang] = {}
        for f, de in felder.items():
            if not de:
                out[lang][f] = ""
                continue
            wert = fassung.get(f)
            if not isinstance(wert, str) or not wert.strip():
                raise VorschlagFehler(f"Uebersetzung {lang}/{f} fehlt")
            out[lang][f] = wert.strip()
    return out


# ---------- Pruefen und Anlegen ----------

def _pruefe_aenderung(reg_key: str, art: str, schritt_id, roh: dict, today: date,
                      *, leer_erlaubt: bool = False) -> dict | str:
    """KI-Aenderung -> `{art, schritt, felder, texte_de}` oder Grund fuer Verwerfen.

    Prueft mit `pflichten_db.pruefe_felder` (Frist-Typ und -Wert gemeinsam,
    fehlender Teil vom aktuellen Schritt) und behaelt nur, was sich aendert.
    """
    if art not in pdb.VORSCHLAG_ARTEN:
        return f"unbekannte Art {art!r}"
    schritt = None
    if art != "neu":
        try:
            sid = int(schritt_id)
        except (TypeError, ValueError):
            return f"{art} ohne gueltige schritt_id ({schritt_id!r})"
        schritt = pdb.schritt(sid)
        if not schritt or schritt["reg_key"] != reg_key:
            return f"Schritt {schritt_id} gehoert nicht zu {reg_key}"
    if art == "deaktivieren":
        return {"art": art, "schritt": schritt, "felder": {}, "texte_de": {}}

    roh = roh if isinstance(roh, dict) else {}
    felder = {k: _text(roh[k]) for k in pdb.SCHRITT_FELDER if roh.get(k) is not None}
    texte_de = {f: _text(roh[f]) for f in pdb.TEXTFELDER if roh.get(f) is not None}
    if "rolle" in felder:
        felder["rolle"] = felder["rolle"].lower()
    if felder.get("frist_typ") == "keine":
        felder["frist_wert"] = ""  # 'keine' hat nie einen Wert
    probe = dict(felder)
    if schritt is not None and ("frist_typ" in probe) != ("frist_wert" in probe):
        probe.setdefault("frist_typ", schritt.get("frist_typ"))
        probe.setdefault("frist_wert", schritt.get("frist_wert"))
    fehler = pdb.pruefe_felder(probe, today)
    if fehler:
        return "; ".join(fehler)

    if art == "neu":
        if not texte_de.get("titel"):
            return "neuer Schritt ohne Titel"
    else:
        alt_de = (schritt.get("texte") or {}).get("de", {})
        felder = {k: v for k, v in felder.items() if v != _text(schritt.get(k))}
        texte_de = {f: t for f, t in texte_de.items() if t != _text(alt_de.get(f))}
        if "titel" in texte_de and not texte_de["titel"]:
            return "Titel darf nicht leer werden"
        if not felder and not texte_de and not leer_erlaubt:
            return f"keine Aenderung an Schritt {schritt['id']}"
    return {"art": art, "schritt": schritt, "felder": felder, "texte_de": texte_de}


async def _anlegen(reg_key: str, geprueft: dict, ausloeser: str, *, ausloeser_ref: str,
                   beleg: str, begruendung: str, ask: Ask | None) -> int:
    texte: dict[str, dict] = {}
    if geprueft["texte_de"]:
        try:
            fremd = await uebersetzen(geprueft["texte_de"], ask)
        except Exception as exc:  # noqa: BLE001 — Vorschlag nicht verlieren; Admin prueft
            log.warning("Uebersetzung fuer %s fehlgeschlagen: %s", reg_key, exc)
            fremd = {lang: dict(geprueft["texte_de"]) for lang in ZIELSPRACHEN}
            begruendung = (begruendung + " [Übersetzung fehlgeschlagen: die fremden Sprachen "
                           "enthalten den deutschen Text, bitte vor der Freigabe korrigieren.]")
        texte = {"de": dict(geprueft["texte_de"]), **fremd}
    nachher = dict(geprueft["felder"])
    if texte:
        nachher["texte"] = texte
    schritt = geprueft["schritt"]
    return pdb.neuer_vorschlag(
        reg_key, geprueft["art"], ausloeser, nachher,
        schritt_id=schritt["id"] if schritt else None, ausloeser_ref=ausloeser_ref,
        beleg=beleg[:BELEG_MAX], begruendung=begruendung.strip()[:BEGRUENDUNG_MAX],
    )


def _katalog_text(schritte: list[dict]) -> str:
    """Aktuelle Schritte, deutsch, eine JSON-Zeile je Schritt."""
    zeilen = []
    for s in schritte:
        zeilen.append(json.dumps({
            "schritt_id": s["id"], "sortierung": s.get("sortierung"),
            "titel": s.get("titel", ""), "beschreibung": s.get("beschreibung", ""),
            "daten": s.get("daten", ""), "rolle": s.get("rolle", ""),
            "frist_typ": s.get("frist_typ", "keine"), "frist_wert": s.get("frist_wert", ""),
            "link": s.get("link") or "", "quelle": s.get("quelle") or "",
        }, ensure_ascii=False))
    return "\n".join(zeilen) or "(noch keine Schritte)"


_REGELN = (
    "Fristen nur als Regeltypen relativ/fest/jaehrlich/keine: relativ = Abstand zum "
    "Anwendungsbeginn der Regulierung, z. B. -6m, -30d, +0d; fest = Datum TT.MM.JJJJ, "
    "z. B. 31.12.2027; jaehrlich = Stichtag TT.MM., z. B. 31.05.; keine = leerer Wert. "
    "Rollen nur: " + ", ".join(pflichten.ROLLEN) + " (oder leer). "
    "Alle Texte auf Deutsch, knapp und fuer Unternehmen verstaendlich."
)


# ---------- Watchdog ----------

SYSTEM_AENDERUNG = (
    "Du pflegst den Pflichten-Katalog eines Branchenverbands: je Regulierung eine Liste "
    "konkreter Schritte mit Titel, Beschreibung, benoetigten Daten, zustaendiger Rolle und "
    "Frist. Du bekommst den Unterschied zwischen alter und neuer Fassung eines Gesetzes "
    "und die aktuellen Schritte. Schlage nur Aenderungen vor, die der neue Text belegt; "
    "zitiere die Stelle woertlich im Feld beleg; erfinde nichts. Reine Formatierungs- oder "
    "Layout-Unterschiede sind keine Aenderung. " + _REGELN + " "
    "In nachher stehen nur die Felder, die sich aendern (titel, beschreibung, daten, rolle, "
    "frist_typ, frist_wert, link, quelle). Antworte nur mit JSON: "
    '{"aenderungen": [{"art": "neu|aendern|deaktivieren", "schritt_id": <Zahl oder null>, '
    '"nachher": {...}, "beleg": "...", "begruendung": "..."}]}. '
    'Ist keine Aenderung noetig: {"aenderungen": []}.'
)


def _verwerfen(verworfen: list | None, reg_key: str, grund: str) -> None:
    log.warning("KI-Vorschlag %s verworfen: %s", reg_key, grund)
    if verworfen is not None:
        verworfen.append(grund)


async def vorschlaege_aus_aenderung(reg_key: str, alter_text: str, neuer_text: str,
                                    ask: Ask | None = None, *, ausloeser_ref: str = "",
                                    verworfen: list | None = None,
                                    today: date | None = None) -> list[int]:
    """Gesetzesaenderung -> offene Vorschlaege (`ausloeser='watchdog'`); Rueckgabe: IDs.

    Unbrauchbare Gesamtantwort -> `VorschlagFehler` (nichts angelegt). Einzelne
    ungueltige Aenderungen werden verworfen; der Grund landet in `verworfen`.
    """
    from watchdog import _diff_excerpt  # spaeter Import: watchdog importiert dieses Modul

    today = today or date.today()
    reg = _reg(reg_key)
    schritte = pdb.schritte_fuer(reg_key, "de", nur_aktiv=True)
    user = (
        f"Regulierung: {reg.get('full_name') or reg['name']} ({reg_key})\n\n"
        f"AKTUELLE SCHRITTE (eine JSON-Zeile je Schritt):\n{_katalog_text(schritte)}\n\n"
        f"{_diff_excerpt(alter_text, neuer_text)}\n\n"
        "Welche Schritte muessen wegen dieser Aenderung neu angelegt, geaendert oder "
        "gestrichen werden?"
    )
    data = _json(await (ask or _standard_ask(4000))(SYSTEM_AENDERUNG, user))
    liste = data.get("aenderungen")
    if not isinstance(liste, list):
        raise VorschlagFehler("Antwort ohne Liste 'aenderungen'")

    ids: list[int] = []
    for a in liste:
        if not isinstance(a, dict):
            _verwerfen(verworfen, reg_key, "Eintrag ist kein Objekt")
            continue
        beleg = _text(a.get("beleg"))
        if not beleg:
            _verwerfen(verworfen, reg_key, "ohne Beleg aus dem Gesetzestext")
            continue
        geprueft = _pruefe_aenderung(reg_key, _text(a.get("art")), a.get("schritt_id"),
                                     a.get("nachher"), today)
        if isinstance(geprueft, str):
            _verwerfen(verworfen, reg_key, geprueft)
            continue
        ids.append(await _anlegen(reg_key, geprueft, "watchdog", ausloeser_ref=ausloeser_ref,
                                  beleg=beleg, begruendung=_text(a.get("begruendung")),
                                  ask=ask))
    return ids


# ---------- Startbestand ----------

SYSTEM_STARTBESTAND = (
    "Du pruefst den Startbestand eines Pflichten-Katalogs gegen den Gesetzestext. Fuer jeden "
    "uebergebenen Schritt bestimmst du die zustaendige Rolle, die Frist-Regel und die "
    "benoetigten Daten. Schlage nur vor, was der Gesetzesauszug belegt; zitiere die Stelle "
    "woertlich im Feld beleg; erfinde nichts. Was der Text nicht belegt, uebernimmst du "
    "unveraendert aus dem aktuellen Schritt. " + _REGELN + " Antworte nur mit JSON: "
    '{"schritte": [{"schritt_id": <Zahl>, "rolle": "...", "frist_typ": "...", '
    '"frist_wert": "...", "daten": "...", "beleg": "...", "begruendung": "..."}]}.'
)

_STARTBESTAND_FELDER = ("rolle", "frist_typ", "frist_wert", "daten")


async def startbestand_vorschlaege(reg_key: str, ask: Ask | None = None, *,
                                   verworfen: list | None = None,
                                   today: date | None = None) -> list[int]:
    """Je ungepruefter Schritt (`geprueft_am IS NULL`) ein `aendern`-Vorschlag.

    `ausloeser='startbestand'`. Bestaetigt die KI den Schritt unveraendert, ist
    `nachher` leer — die Freigabe setzt dann nur `geprueft_am`. Schritte mit
    schon offenem Startbestand-Vorschlag werden uebersprungen (kein Doppel).
    """
    today = today or date.today()
    reg = _reg(reg_key)
    offen = {v["schritt_id"] for v in pdb.offene_vorschlaege()
             if v["ausloeser"] == "startbestand" and v["reg_key"] == reg_key}
    ungeprueft = {s["id"]: s for s in pdb.schritte_fuer(reg_key, "de", nur_aktiv=True)
                  if not s.get("geprueft_am") and s["id"] not in offen}
    if not ungeprueft:
        return []

    gesetz = (fetcher.fetch_law_text(reg, language="de") or {}).get("text") or ""
    if not gesetz.strip():
        raise VorschlagFehler(f"kein Gesetzestext fuer {reg_key}")
    kontext = lawparse.build_context(reg, gesetz, None,
                                     int(os.getenv("FULLTEXT_MAX_CHARS", "40000")))
    user = (
        f"Regulierung: {reg.get('full_name') or reg['name']} ({reg_key})\n\n"
        f"ZU PRUEFENDE SCHRITTE (eine JSON-Zeile je Schritt):\n"
        f"{_katalog_text(list(ungeprueft.values()))}\n\n{kontext}"
    )
    data = _json(await (ask or _standard_ask(4000))(SYSTEM_STARTBESTAND, user))
    liste = data.get("schritte")
    if not isinstance(liste, list):
        raise VorschlagFehler("Antwort ohne Liste 'schritte'")

    ids: list[int] = []
    erledigt: set[int] = set()
    for a in liste:
        if not isinstance(a, dict):
            _verwerfen(verworfen, reg_key, "Eintrag ist kein Objekt")
            continue
        try:
            sid = int(a.get("schritt_id"))
        except (TypeError, ValueError):
            sid = None
        if sid not in ungeprueft or sid in erledigt:
            _verwerfen(verworfen, reg_key, f"Schritt {a.get('schritt_id')!r} nicht zu pruefen")
            continue
        roh = {k: a[k] for k in _STARTBESTAND_FELDER if k in a}
        geprueft = _pruefe_aenderung(reg_key, "aendern", sid, roh, today, leer_erlaubt=True)
        if isinstance(geprueft, str):
            _verwerfen(verworfen, reg_key, geprueft)
            continue
        begruendung = _text(a.get("begruendung"))
        if not geprueft["felder"] and not geprueft["texte_de"]:
            begruendung = (begruendung + " (Schritt bestätigt, keine Änderung)").strip()
        erledigt.add(sid)
        ids.append(await _anlegen(reg_key, geprueft, "startbestand", ausloeser_ref="",
                                  beleg=_text(a.get("beleg")), begruendung=begruendung,
                                  ask=ask))
    return ids


# ---------- Admin-Mail ----------

def _link_vorschlaege() -> str:
    teile = urlsplit((os.getenv("PUBLIC_BASE_URL") or "").strip())
    basis = (f"{teile.scheme}://{teile.netloc}"
             if teile.scheme in ("http", "https") and teile.netloc else "")
    return basis + "/admin/pflichten/vorschlaege"


def benachrichtige_admin(anzahl: dict[str, int], versand=mailer.send, *,
                         fehler: list[str] | None = None,
                         empfaenger=None) -> None:
    """Eine Mail an die Haupt-Admins: je Regulierung die Zahl neuer Vorschlaege.

    Nichts zu melden (keine Vorschlaege, keine Fehler) -> keine Mail. Jeder
    Versuch steht in `mail_log` (`purpose='pflichten_vorschlag'`).
    """
    zeilen = [f"{k}: {n} {'Vorschlag' if n == 1 else 'Vorschläge'}"
              for k, n in sorted(anzahl.items()) if n > 0]
    fehler = [f for f in (fehler or []) if f]
    if not zeilen and not fehler:
        return
    gesamt = sum(n for n in anzahl.values() if n > 0)
    betreff = f"Pflichten-Plan: {gesamt} neue KI-Vorschläge zur Freigabe"
    text = ("Guten Tag,\n\ndie KI hat Vorschläge für den Pflichten-Katalog erstellt. "
            "Sichtbar werden sie erst nach Ihrer Freigabe.\n\n")
    if zeilen:
        text += "\n".join(zeilen) + "\n\n"
    if fehler:
        text += "Nicht bearbeitet:\n" + "\n".join(f"- {f}" for f in fehler[:30]) + "\n\n"
    text += f"Zur Prüfung: {_link_vorschlaege()}\n"
    for adresse in sorted(empfaenger or pdb.STAMM_ADMINS):
        try:
            message_id = versand(adresse, betreff, text)
        except Exception as exc:  # noqa: BLE001 — Mailfehler darf den Lauf nicht abbrechen
            log.warning("Admin-Mail Pflichten-Vorschlaege an %s fehlgeschlagen: %s", adresse, exc)
            db.log_mail(adresse, "pflichten_vorschlag", "failed", error=str(exc)[:300])
        else:
            db.log_mail(adresse, "pflichten_vorschlag", "sent", message_id=message_id)


# ---------- Startbestand im Hintergrund ----------

_startbestand_sperre = threading.Lock()


def startbestand_laeuft() -> bool:
    return _startbestand_sperre.locked()


def startbestand_alle(ask: Ask | None = None, versand=mailer.send) -> dict:
    """Alle Regulierungen mit ungeprueften Schritten, ein LLM-Aufruf je Regulierung.

    Fehler je Regulierung brechen den Lauf nicht ab; am Ende eine Admin-Mail.
    """
    keys = [r["key"] for r in REGULATIONS
            if any(not s.get("geprueft_am") for s in pdb.schritte_fuer(r["key"], "de"))]
    anzahl: dict[str, int] = {}
    fehler: list[str] = []
    verworfen: list[str] = []
    for key in keys:
        try:
            anzahl[key] = len(asyncio.run(startbestand_vorschlaege(key, ask,
                                                                   verworfen=verworfen)))
        except Exception as exc:  # noqa: BLE001
            log.warning("Startbestand %s fehlgeschlagen: %s", key, exc)
            fehler.append(f"{key}: {type(exc).__name__}: {exc}"[:300])
    log.info("Startbestand fertig: %s Vorschlaege, %s verworfen, %s Fehler",
             sum(anzahl.values()), len(verworfen), len(fehler))
    benachrichtige_admin(anzahl, versand=versand, fehler=fehler)
    return {"anzahl": anzahl, "fehler": fehler, "verworfen": verworfen}


def starte_startbestand(*, lauf: Callable[[], object] | None = None) -> bool:
    """Startet `startbestand_alle` in einem Hintergrund-Thread.

    False, wenn schon ein Lauf in diesem Prozess aktiv ist (kein Doppelstart).
    """
    if not _startbestand_sperre.acquire(blocking=False):
        return False

    def ziel() -> None:
        try:
            (lauf or startbestand_alle)()
        except Exception:  # noqa: BLE001
            log.exception("Startbestand-Lauf abgebrochen")
        finally:
            _startbestand_sperre.release()

    try:
        threading.Thread(target=ziel, name="pflichten-startbestand", daemon=True).start()
    except Exception:
        _startbestand_sperre.release()
        raise
    return True
