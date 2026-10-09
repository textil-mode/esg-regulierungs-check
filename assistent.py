"""Regulierungs-Assistent: Chat zu den Regulierungen des Katalogs (nur angemeldet).

Funktionsweise nach dem Vorbild des go-textile-Chatbots
(Zwischenspeicher/go-textile-chatbot/server.py):

- Das Widget (`static/assistent.js`) sitzt unten rechts auf jeder Seite, solange
  jemand angemeldet ist. Der Gespraechsverlauf liegt nur im Browser-Tab
  (sessionStorage) und geht mit jeder Frage gekuerzt mit; der Server speichert
  keine Gespraeche.
- Die Antwort kommt als Stream (NDJSON, eine Zeile je Ereignis):
  {"type": "meta", "suche": …}, {"type": "token", "text": …}, {"type": "sources", …}.

Was Gemini je Frage bekommt:

1. systemInstruction — Rolle, Regeln und der KATALOG aller Regulierungen
   (Kriterien, Anwendungsdaten, erste Schritte, Leitlinien). Sie ist fuer alle
   Nutzer und Fragen eines Tages byte-gleich, damit Gemini sie intern
   zwischenspeichern kann (implizites Caching, guenstigere Eingabe-Token).
2. die Frage, davor das UNTERNEHMENSPROFIL (ohne Firmennamen), das letzte
   PRUEFERGEBNIS und AUSZUEGE AUS DEN GESETZESTEXTEN.

Die Auszuege: Volltexte liegen ohnehin in `law_texts` (die Analyse und der
woechentliche Watchdog halten sie aktuell). Sie werden mit `lawparse` in
Artikel/Paragraphen zerlegt und mit BM25 durchsucht. Nennt die Frage eine
Regulierung (oder kommt sie ueber "Nachfragen" von einer Ergebniskarte), bekommt
das Modell zusaetzlich deren Anwendungsbereich und Kernartikel ueber
`lawparse.build_context` — dieselbe Auswahl, mit der auch die Pruefung arbeitet.

Datentrennung: Der Firmenname steht nirgends im Prompt (wie in llm.py). Anders
als die Begruendungen der Pruefung wird hier nichts zwischengespeichert, die
Antworten koennen also das ganze Profil nutzen, ohne dass es in fremde Konten
wandert.
"""
from __future__ import annotations

import asyncio
import base64
import json
import math
import os
import re
import threading
import time
from collections import Counter
from datetime import date
from typing import Iterable, Iterator

import httpx

import fetcher
import lawparse
from deadlines import deadline_for
from i18n import t, t_first_step
from llm import _LANG_NAMES, _PROFILE_LABELS, _render_field
from regulations import (REGULATIONS, application_for, first_steps_for,
                         guidelines_for)

# ---------------------------------------------------------------------------
# Stellschrauben
# ---------------------------------------------------------------------------
# Gesamtbudget der Gesetzesauszuege je Frage (Zeichen). 45.000 Zeichen sind
# rund 12.500 Token — mit Katalog, Profil und Verlauf ~25.000 Token je Frage,
# bei gemini-3.1-flash-lite rund 0,6 Cent.
CONTEXT_CHARS = int(os.getenv("ASSISTENT_CONTEXT_CHARS", "45000"))
TOP_CHUNKS = int(os.getenv("ASSISTENT_TOP_CHUNKS", "8"))   # BM25-Treffer ueber alle Texte
MAX_REGS = 3              # so viele genannte Regulierungen bekommen ihren Kernkontext
CHUNK_CHARS = 2200        # Abschnitte darueber werden fuer die Suche geteilt
MAX_QUESTION = 800
MAX_HISTORY = 6           # Nachrichten (Frage und Antwort einzeln)
HISTORY_CHARS = 1500      # je Nachricht
_ANSCHLUSS_WORTE = 8      # so kurze Fragen gelten als Anschlussfrage

APPLIES_TEXT = {"ja": "relevant", "moeglich": "pruefen", "nein": "nicht relevant",
                "error": "Fehler bei der Pruefung"}


def _log(msg: str) -> None:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "[assistent]", msg, flush=True)


# ---------------------------------------------------------------------------
# Regulierungen in der Frage erkennen
# ---------------------------------------------------------------------------
# Kuerzel und Kurzname kommen aus regulations.py; dazu Begriffe, unter denen
# die Vorschriften im Alltag laufen. Gesucht wird am Wortanfang, damit
# "Verpackungsverordnung" die PPWR findet, "erreichen" aber nicht REACH.
_ALIASES: dict[str, tuple[str, ...]] = {
    "CSDDD": ("lieferkettenrichtlinie", "cs3d", "sorgfaltspflichtenrichtlinie"),
    "LkSG": ("lieferkettengesetz", "lieferkettensorgfalt"),
    "EUDR": ("entwaldung", "deforestation"),
    "FLR": ("zwangsarbeit", "forced labour", "forced labor"),
    "CSRD": ("nachhaltigkeitsbericht", "esrs"),
    "CSRD_DE": ("csrd-umsetzungsgesetz", "umsetzungsgesetz"),
    "NFRD": ("nichtfinanzielle",),
    "CSR-RUG": ("csr-richtlinie-umsetzungsgesetz", "289b"),
    "TaxonomieVO": ("taxonomie",),
    "HinSchG": ("hinweisgeber", "whistleblow", "meldestelle"),
    "RightToRepair": ("reparatur", "right to repair"),
    "Oekodesign": ("ökodesign", "oekodesign", "ecodesign", "espr", "produktpass"),
    "Vernichtungsverbot": ("vernichtung", "unverkauft"),
    "PPWR": ("verpackung", "packaging"),
    "MinRohSorgG": ("konfliktmineral", "mineralische rohstoffe", "3tg"),
    "EmpCo": ("greenwashing", "umweltaussage", "umweltwerbung"),
    "REACH_XVII": ("reach", "anhang xvii", "azofarb", "dimethylformamid", "pfas"),
    "REACH_ART33": ("svhc", "kandidatenliste", "art. 33", "artikel 33"),
    "SCIP": ("scip",),
    "POP": ("pop-verordnung", "persistente organische", "pfoa"),
    "BPR": ("biozid", "behandelte ware"),
    "TKVO": ("textilkennzeichnung", "faserbezeichnung", "faserzusammensetzung"),
    "GPSR": ("produktsicherheit",),
    "PSA": ("schutzausrüstung", "schutzausruestung", "psa"),
    "MDR": ("medizinprodukt",),
    "Schuhkennzeichnung": ("schuhkennzeichnung", "schuhe"),
    "EnEfG": ("energieeffizienz", "energieaudit", "energiemanagement"),
    "AbwV38": ("abwasser", "abwv", "anhang 38"),
    "EPR_FR": ("refashion", "rep tlc", "agec"),
    "EPR_NL": ("upv textiel", "upv"),
}

REGS_BY_KEY = {r["key"]: r for r in REGULATIONS}


def _short_name(reg: dict) -> str:
    return reg["name"].split(" – ")[0].strip()


def _patterns() -> list[tuple[str, re.Pattern]]:
    out = []
    for reg in REGULATIONS:
        words = {reg["key"].lower(), _short_name(reg).lower()} | set(_ALIASES.get(reg["key"], ()))
        alt = "|".join(sorted((re.escape(w) for w in words if w), key=len, reverse=True))
        out.append((reg["key"], re.compile(rf"(?<![\w-])(?:{alt})", re.I)))
    return out


_REG_PATTERNS = _patterns()


def detect_regs(text: str) -> list[str]:
    """Regulierungen, die in `text` genannt sind — in der Reihenfolge ihrer Nennung."""
    hits = []
    for key, pat in _REG_PATTERNS:
        m = pat.search(text or "")
        if m:
            hits.append((m.start(), key))
    return [k for _, k in sorted(hits)]


# ---------------------------------------------------------------------------
# Suche in den Gesetzestexten (BM25)
# ---------------------------------------------------------------------------
_WORD = re.compile(r"\w+", re.UNICODE)
_STOP = frozenset("""
der die das den dem des ein eine einer eines einem einen und oder aber auch nicht kein keine
ist sind wird werden wurde wurden hat haben sein bei mit von vom zu zum zur im in an am auf aus
für fuer über ueber unter nach vor wie was wer wann wo welche welcher welches wenn dass ob als so
es er sie wir ihr ich du man sich uns unser unsere unseren mein meine muss müssen muessen kann
können koennen darf soll sollen gilt gelten diese dieser dieses dies the and or of to in for on
is are be by with from that this what which when how do does
""".split())
_SUFFIXES = ("ungen", "ung", "heiten", "heit", "keiten", "keit", "en", "er", "es", "e", "n", "s")


def _stem(word: str) -> str:
    for suf in _SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 4:
            return word[: -len(suf)]
    return word


def tokens(text: str) -> list[str]:
    return [_stem(w) for w in _WORD.findall((text or "").lower())
            if len(w) > 2 and w not in _STOP and not w.isdigit()]


class _Index:
    """Unveraenderlicher Suchindex ueber alle Gesetzesabschnitte einer Sprache."""

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.postings: dict[str, list[tuple[int, int]]] = {}
        self.lengths: list[int] = []
        for i, ch in enumerate(chunks):
            terms = Counter(tokens(ch["title"] + " " + ch["text"]))
            self.lengths.append(sum(terms.values()) or 1)
            for term, tf in terms.items():
                self.postings.setdefault(term, []).append((i, tf))
        self.avg = (sum(self.lengths) / len(self.lengths)) if self.lengths else 1.0

    def search(self, query: str, limit: int, only: set[str] | None = None) -> list[dict]:
        n = len(self.chunks)
        if not n:
            return []
        scores: dict[int, float] = {}
        for term in set(tokens(query)):
            plist = self.postings.get(term)
            if not plist:
                continue
            idf = math.log(1 + (n - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, tf in plist:
                if only is not None and self.chunks[i]["reg_key"] not in only:
                    continue
                norm = tf * 2.4 / (tf + 1.4 * (0.25 + 0.75 * self.lengths[i] / self.avg))
                scores[i] = scores.get(i, 0.0) + idf * norm
        best = sorted(scores, key=scores.get, reverse=True)[:limit]
        return [self.chunks[i] for i in best]


def _split(text: str, limit: int) -> list[str]:
    """Langen Text an Absatzgrenzen in Stuecke von hoechstens `limit` Zeichen teilen."""
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for para in text.split("\n"):
        while len(para) > limit:          # ein einzelner Riesenabsatz (PDF-Extrakt)
            if cur:
                parts.append(cur)
                cur = ""
            parts.append(para[:limit])
            para = para[limit:]
        if cur and len(cur) + len(para) + 1 > limit:
            parts.append(cur)
            cur = para
        else:
            cur = f"{cur}\n{para}" if cur else para
    if cur.strip():
        parts.append(cur)
    return [p for p in parts if p.strip()]


def _law_text(reg_key: str, lang: str) -> dict | None:
    """Gespeicherter Volltext in der UI-Sprache, sonst Deutsch, sonst Englisch."""
    for language in dict.fromkeys((lang, "de", "en")):
        row = fetcher.get_cached_text(reg_key, language)
        if row and (row.get("text") or "").strip():
            return row
    return None


def _chunks_for(reg: dict, text: str) -> list[dict]:
    sections = lawparse.parse_sections(text)
    if not sections:   # kein erkennbarer Aufbau: Rohtext in Stuecken
        sections = [{"label": "", "title": "", "text": text}]
    out = []
    for sec in sections:
        pieces = _split(sec["text"], CHUNK_CHARS)
        for n, piece in enumerate(pieces, 1):
            label = sec["label"] + (f" (Teil {n})" if len(pieces) > 1 and sec["label"] else "")
            out.append({"reg_key": reg["key"], "label": label.strip(),
                        "title": sec.get("title") or "", "text": piece.strip()})
    return out


_index_lock = threading.Lock()
_indexes: dict[str, tuple[tuple, _Index]] = {}   # lang -> (Stand, Index)
_index_checked: dict[str, float] = {}
INDEX_RECHECK_S = 600


def _stand(lang: str) -> tuple:
    """Fingerabdruck der gespeicherten Texte: aendert er sich, wird neu indiziert."""
    out = []
    for reg in REGULATIONS:
        row = _law_text(reg["key"], lang)
        out.append((reg["key"], (row or {}).get("fetched_at"), len((row or {}).get("text") or "")))
    return tuple(out)


def get_index(lang: str) -> _Index:
    now = time.time()
    with _index_lock:
        cached = _indexes.get(lang)
        if cached and now - _index_checked.get(lang, 0) < INDEX_RECHECK_S:
            return cached[1]
        stand = _stand(lang)
        _index_checked[lang] = now
        if cached and cached[0] == stand:
            return cached[1]
        start = time.time()
        chunks: list[dict] = []
        for reg in REGULATIONS:
            row = _law_text(reg["key"], lang)
            if row:
                chunks.extend(_chunks_for(reg, row["text"]))
        index = _Index(chunks)
        _indexes[lang] = (stand, index)
        _log(f"Suchindex {lang}: {len(chunks)} Abschnitte in {time.time() - start:.1f} s")
        return index


# ---------------------------------------------------------------------------
# Katalog (systemInstruction)
# ---------------------------------------------------------------------------
SYSTEM_RULES = """Du bist der Regulierungs-Assistent im ESG-Regulierungs-Check von textil+mode, \
dem Gesamtverband der deutschen Textil- und Modeindustrie. Du beantwortest Fragen von \
Unternehmen der Branche zu den Nachhaltigkeits-, Lieferketten-, Produkt- und \
Chemikalienvorschriften, die dieser Check abdeckt.

Dir liegen vor:
1. der KATALOG aller Regulierungen des Checks (unten): Anwendungskriterien, Anwendungsdaten, \
erste Schritte, amtliche Leitlinien und Quellen,
2. mit jeder Frage das UNTERNEHMENSPROFIL der fragenden Person und das ERGEBNIS IHRER LETZTEN PRUEFUNG,
3. mit jeder Frage AUSZUEGE AUS DEN GESETZESTEXTEN, passend zur Frage ausgewaehlt.

Regeln:
- Stuetze jede Aussage auf diese Quellen. Nenne die Fundstelle (z. B. "Art. 2 Abs. 1 CSDDD", \
"§ 1 LkSG"), wenn du dich auf einen Auszug stuetzt.
- Steht etwas nicht in den Quellen, sag das offen und verweise auf die amtliche Quelle aus dem \
Katalog oder auf die Beratung durch textil+mode. Erfinde keine Artikel, Fristen, Schwellenwerte, \
Grenzwerte oder Zahlen.
- Betrifft die Frage das eigene Unternehmen ("muessen wir", "gilt das fuer uns"), beziehe das \
Unternehmensprofil und das Pruefergebnis ein. Kommst du zu einer anderen Einschaetzung als das \
Pruefergebnis, sag das ausdruecklich und empfiehl, die Angaben zu pruefen und die Pruefung neu zu \
starten. Fehlt eine Angabe, die es fuer die Antwort braucht, frag danach oder nenne die Bedingung.
- Vorschriften ausserhalb des Katalogs gehoeren nicht zum Pruefumfang: Sag das, und bewerte sie \
nicht im Einzelnen.
- Du gibst allgemeine Informationen, keine Rechtsberatung. Geht es um eine verbindliche \
Bewertung im Einzelfall, weise in einem Satz auf die Beratung durch textil+mode hin — nicht bei \
jeder Antwort.
- Bleib beim Thema (Regulierung, Nachhaltigkeit und Compliance in der Textil- und Modebranche). \
Andere Anliegen lehnst du freundlich in einem Satz ab.
- Nenne keinen Firmennamen.
- Antworte in der Sprache, die unter der Frage angegeben ist. Sachlich, knapp und konkret: kurze \
Absaetze, Aufzaehlungen mit "- ", Wichtiges **fett**. Keine Begruessung, keine Floskeln. Verlinke \
nur Adressen aus dem Katalog.

=== KATALOG ===
"""

_catalog_cache: tuple[str, str] | None = None   # (Datum, Text)


def catalog_text(today: date | None = None) -> str:
    """Der Katalog als Text — taeglich neu, weil sich der Status (gilt ab/in Kraft) mit dem Datum aendert."""
    global _catalog_cache
    day = (today or date.today()).isoformat()
    if _catalog_cache and _catalog_cache[0] == day:
        return _catalog_cache[1]
    blocks = []
    for reg in REGULATIONS:
        app = application_for(reg["key"], today)
        lines = [f"## {reg['name']} [Kuerzel {reg['key']}]",
                 f"Rechtsakt: {reg['full_name']}",
                 f"Raeumlicher Geltungsbereich: {reg.get('scope', '-')}",
                 f"Quelle: {reg['url']}"]
        status = app.get("status") or ""
        applies_from = app.get("applies_from") or ""
        if status or applies_from:
            lines.append(f"Status: {status}" + (f", anwendbar ab {applies_from}" if applies_from else ""))
        lines.append(f"Anwendungskriterien: {reg['criteria']}")
        if reg.get("key_article"):
            lines.append(f"Kernvorschrift: {reg['key_article']}")
        steps = [t_first_step(k, "de") for k in first_steps_for(reg["key"])]
        steps = [s for s in steps if s]
        if steps:
            lines.append("Erste Schritte: " + " | ".join(steps))
        guides = guidelines_for(reg["key"])
        if guides:
            lines.append("Leitlinien: " + "; ".join(f"{g['name']} ({g['url']})" for g in guides))
        blocks.append("\n".join(lines))
    text = SYSTEM_RULES + "\n\n".join(blocks)
    _catalog_cache = (day, text)
    return text


# ---------------------------------------------------------------------------
# Profil, Pruefergebnis, Auszuege
# ---------------------------------------------------------------------------
def profile_block(profile: dict | None) -> str:
    if not profile:
        return "UNTERNEHMENSPROFIL: (noch nicht ausgefuellt)"
    lines = ["UNTERNEHMENSPROFIL (Angaben der fragenden Person):"]
    for field, label in _PROFILE_LABELS.items():   # bewusst ohne `name`
        lines.append(f"{label}: {_render_field(field, profile.get(field))}")
    return "\n".join(lines)


def result_block(analysis: dict | None, profile: dict | None) -> str:
    if not analysis or not analysis.get("result"):
        return "ERGEBNIS DER LETZTEN PRUEFUNG: (noch keine Pruefung durchgefuehrt)"
    when = (analysis.get("created_at") or "")[:10]
    lines = [f"ERGEBNIS DER LETZTEN PRUEFUNG (vom {when}; relevant / pruefen / nicht relevant):"]
    order = {"ja": 0, "moeglich": 1, "nein": 2}
    rows = sorted(analysis["result"],
                  key=lambda r: (order.get((r.get("applies") or "").lower(), 3), r.get("nr", 0)))
    for r in rows:
        a = (r.get("applies") or "").lower()
        line = f"- {r.get('name', r.get('key'))}: {APPLIES_TEXT.get(a, a)}"
        if a in ("ja", "moeglich") and profile:
            info = deadline_for(r.get("key", ""), profile) or {}
            if info.get("gilt_ab"):
                line += f" (gilt fuer dieses Unternehmen ab {info['gilt_ab']})"
        reason = re.sub(r"\s+", " ", (r.get("reason") or "")).strip()
        if reason:
            line += f" — {reason[:450]}"
        lines.append(line)
    return "\n".join(lines)


def _chunk_block(ch: dict) -> str:
    reg = REGS_BY_KEY.get(ch["reg_key"], {})
    head = _short_name(reg) if reg else ch["reg_key"]
    if ch["label"]:
        head += f" · {ch['label']}" + (f" - {ch['title']}" if ch["title"] else "")
    return f"=== {head} ===\n{ch['text']}"


def excerpts(search_q: str, reg_keys: list[str], lang: str,
             budget: int = CONTEXT_CHARS) -> tuple[str, list[str]]:
    """Gesetzesauszuege zur Frage und die Regulierungen, aus denen sie stammen."""
    index = get_index(lang)
    parts: list[str] = []
    used: list[str] = []
    seen: set[tuple[str, str]] = set()
    size = 0

    def add(block: str, reg_key: str) -> bool:
        nonlocal size
        if size + len(block) + 2 > budget:
            return False
        parts.append(block)
        size += len(block) + 2
        if reg_key not in used:
            used.append(reg_key)
        return True

    regs = [k for k in reg_keys if k in REGS_BY_KEY][:MAX_REGS]
    if regs:
        # Genannte Regulierungen: Anwendungsbereich + Kernartikel (wie die Pruefung),
        # dazu die zur Frage passendsten Abschnitte genau dieser Texte.
        per_reg = max(6000, int(budget * 0.6) // len(regs))
        for key in regs:
            row = _law_text(key, lang)
            if not row:
                continue
            core = lawparse.build_context(REGS_BY_KEY[key], row["text"], None, per_reg)
            if add(core, key):
                seen.update((key, lbl) for lbl in re.findall(r"^=== (.+?)(?: - .*)? ===$", core, re.M))
        for ch in index.search(search_q, 4 * len(regs), only=set(regs)):
            if (ch["reg_key"], ch["label"]) not in seen:
                if add(_chunk_block(ch), ch["reg_key"]):
                    seen.add((ch["reg_key"], ch["label"]))
    # Dazu die besten Treffer ueber alle Texte: findet auch, was die Frage nicht
    # beim Namen nennt ("Wer muss Azofarbstoffe pruefen?").
    added = 0
    for ch in index.search(search_q, TOP_CHUNKS * 2):
        if added >= TOP_CHUNKS:
            break
        if (ch["reg_key"], ch["label"]) in seen:
            continue
        if add(_chunk_block(ch), ch["reg_key"]):
            seen.add((ch["reg_key"], ch["label"]))
            added += 1
    return "\n\n".join(parts), used


# ---------------------------------------------------------------------------
# Gespraechsverlauf
# ---------------------------------------------------------------------------
def clean_history(raw) -> list[dict]:
    """Verlauf aus dem Browser pruefen: nur user/model, begrenzt, gleiche Rollen zusammengefasst."""
    out: list[dict] = []
    if isinstance(raw, list):
        for m in raw[-5 * MAX_HISTORY:]:
            if (isinstance(m, dict) and m.get("role") in ("user", "model")
                    and isinstance(m.get("text"), str) and m["text"].strip()):
                text = m["text"].strip()[:HISTORY_CHARS]
                if out and out[-1]["role"] == m["role"]:
                    out[-1]["text"] += "\n" + text
                else:
                    out.append({"role": m["role"], "text": text})
                if m["role"] == "user" and isinstance(m.get("suche"), str) and m["suche"].strip():
                    out[-1]["suche"] = m["suche"].strip()[:600]
    out = out[-MAX_HISTORY:]
    while out and out[0]["role"] != "user":
        out.pop(0)
    return out


def search_query(question: str, history: list[dict]) -> str:
    """Suchtext fuer die Gesetzesauszuege.

    Kurze Anschlussfragen ("Und ab wann?") tragen ihr Thema nicht selbst; dann
    wird die vorige Frage mitgesucht. Kein eigener Modellaufruf dafuer (go-textile
    formuliert um): Gemini versteht den Verlauf ohnehin, hier geht es nur darum,
    die richtigen Abschnitte vorzulegen.
    """
    last = next((m for m in reversed(history) if m["role"] == "user"), None)
    if last and len(question.split()) <= _ANSCHLUSS_WORTE and not detect_regs(question):
        return f"{question} {last.get('suche') or last['text']}"[:900]
    return question


# ---------------------------------------------------------------------------
# Sprachmodell
# ---------------------------------------------------------------------------
class ModelUnavailable(Exception):
    """Kein Modell lieferte ein erstes Wort (Last, Kontingent, Stoerung)."""


_GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"


def _google_models() -> list[str]:
    main = os.getenv("GOOGLE_MODEL") or os.getenv("OPENAI_MODEL", "gemini-2.5-flash")
    fb = os.getenv("GOOGLE_FALLBACK_MODELS", "gemini-3.5-flash-lite,gemini-3.6-flash")
    return [main] + [m.strip() for m in fb.split(",") if m.strip() and m.strip() not in ("-", main)]


def _google_key() -> str:
    return os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY") or ""


def _contents(prompt: str, history: list[dict]) -> list[dict]:
    contents = [{"role": m["role"], "parts": [{"text": m["text"]}]} for m in history]
    if contents and contents[-1]["role"] == "user":   # Verlauf endet mit unbeantworteter Frage
        contents[-1]["parts"].append({"text": prompt})
    else:
        contents.append({"role": "user", "parts": [{"text": prompt}]})
    return contents


def stream_google(system: str, contents: list[dict], usage: dict | None = None) -> Iterator[str]:
    """Antwort von Gemini streamen; vor dem ersten Wort reihum auf Ausweichmodelle wechseln."""
    key = _google_key()
    if not key:
        raise ModelUnavailable("kein API-Schluessel")
    last = ""
    for idx, model in enumerate(_google_models()):
        body = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": contents,
            # 4096: Denkende Modelle zaehlen ihre Denk-Token hier mit; eine
            # gekappte Antwort meldet `answer` als "unterbrochen" (finishReason).
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4096},
        }
        if idx > 0:
            body["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}
        url = f"{_GOOGLE_BASE}/models/{model}:streamGenerateContent?alt=sse"
        sent = False
        for _versuch in range(2):
            try:
                with httpx.stream("POST", url, json=body, headers={"x-goog-api-key": key},
                                  timeout=httpx.Timeout(60.0, connect=10.0)) as r:
                    if r.status_code == 400 and "thinkingConfig" in body["generationConfig"]:
                        del body["generationConfig"]["thinkingConfig"]
                        continue
                    if r.status_code != 200:
                        last = f"{model}: HTTP {r.status_code}"
                        break
                    for line in r.iter_lines():
                        if not line.startswith("data:"):
                            continue
                        try:
                            obj = json.loads(line[5:])
                        except ValueError:
                            if sent:
                                raise
                            raise httpx.DecodingError("unlesbare Antwortzeile")  # -> naechstes Modell
                        if usage is not None and obj.get("usageMetadata"):
                            um = obj["usageMetadata"]
                            usage.update(total=um.get("totalTokenCount", 0),
                                         cached=um.get("cachedContentTokenCount", 0), model=model)
                        for cand in obj.get("candidates", []):
                            if usage is not None and cand.get("finishReason"):
                                usage["finish"] = cand["finishReason"]
                            for part in cand.get("content", {}).get("parts", []):
                                if part.get("text") and not part.get("thought"):
                                    sent = True
                                    yield part["text"]
                    return
            except httpx.HTTPError as e:
                if sent:   # mitten in der Antwort: kein zweites Modell hinterherschicken
                    raise
                # Nie die Adresse samt Schluessel ins Log (der steht im Kopf, aber sicher ist sicher).
                last = re.sub(r"key=[^&\s'\"]+", "key=***", f"{model}: {e}")
                break
        _log(f"Modell nicht verfuegbar ({last}), naechstes")
    raise ModelUnavailable(last or "kein Modell erreichbar")


def stream_other(system: str, contents: list[dict]) -> Iterator[str]:
    """Andere Provider (lokale Entwicklung): ohne Stream ueber den vorhandenen LLM-Client."""
    from llm import LLMClient
    verlauf = "\n\n".join(
        f"{'Nutzer' if c['role'] == 'user' else 'Assistent'}: "
        + "\n".join(p["text"] for p in c["parts"]) for c in contents)
    try:
        text = asyncio.run(LLMClient().ask(system, verlauf, max_tokens=2048, json_mode=False))
    except Exception as e:  # noqa: BLE001
        raise ModelUnavailable(str(e)) from e
    yield text


def stream_model(system: str, contents: list[dict], usage: dict | None = None) -> Iterator[str]:
    if os.getenv("LLM_PROVIDER", "ollama").lower().strip() == "google":
        return stream_google(system, contents, usage)
    return stream_other(system, contents)


# ---------------------------------------------------------------------------
# Antwort
# ---------------------------------------------------------------------------
def _line(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False) + "\n"


def sources_for(answer_text: str, used: list[str], asked: list[str]) -> list[dict]:
    """Quellenkarten: die Regulierungen, deren Auszuege vorlagen und die die Antwort nennt.

    Nennt die Antwort keine, gelten die Regulierungen, nach denen gefragt war.
    """
    named = [k for k in detect_regs(answer_text) if k in used]
    keys = named or [k for k in asked if k in used]
    out = []
    for key in keys[:4]:
        reg = REGS_BY_KEY[key]
        out.append({"title": reg["name"], "url": reg["url"]})
    return out


def answer(question: str, history: list[dict], reg_key: str | None, lang: str,
           profile: dict | None, analysis: dict | None) -> Iterator[str]:
    """NDJSON-Zeilen der Antwort. Laeuft ausserhalb des Request-Kontexts (Stream)."""
    started = time.time()
    search_q = search_query(question, history)
    asked = ([reg_key] if reg_key in REGS_BY_KEY else []) + detect_regs(search_q)
    asked = list(dict.fromkeys(asked))
    yield _line({"type": "meta", "suche": search_q})

    try:
        context, used = excerpts(search_q, asked, lang)
    except Exception as e:  # noqa: BLE001 — ohne Auszuege antworten ist besser als gar nicht
        _log(f"Auszuege fehlgeschlagen: {e}")
        context, used = "", []

    teile = [profile_block(profile), result_block(analysis, profile),
             "AUSZUEGE AUS DEN GESETZESTEXTEN:\n" + (context or "(keine passenden Auszuege gefunden)"),
             "---", f"Frage: {question}"]
    if search_q != question:
        teile.append(f"(Im Gespraechszusammenhang gemeint: {search_q})")
    teile.append(f"Antwortsprache: {_LANG_NAMES.get(lang, 'German')}")
    prompt = "\n\n".join(teile)

    usage: dict = {}
    chunks: list[str] = []
    try:
        for piece in stream_model(catalog_text(), _contents(prompt, history), usage):
            chunks.append(piece)
            yield _line({"type": "token", "text": piece})
    except Exception as e:  # noqa: BLE001 — ModelUnavailable oder Abbruch mitten in der Antwort
        fehler = re.sub(r"key=[^&\s'\"]+", "key=***", str(e))
        _log(f"keine vollstaendige Antwort: {type(e).__name__}: {fehler[:200]}")
        # Hinweise kommen als eigener Typ: das Widget zeigt sie, nimmt sie aber
        # nicht in den Verlauf auf (sonst ginge "ausgelastet" als Antwort mit).
        if not chunks:
            yield _line({"type": "sources", "sources": []})
            yield _line({"type": "notice", "text": t("assistent_busy", lang)})
            return
        yield _line({"type": "notice", "text": t("assistent_cut", lang)})
    else:
        if usage.get("finish") == "MAX_TOKENS":   # Modell hat mitten im Satz aufgehoert
            yield _line({"type": "notice", "text": t("assistent_cut", lang)})
    text = "".join(chunks)
    yield _line({"type": "sources", "sources": sources_for(text, used, asked)})
    _log(f"Antwort in {time.time() - started:.1f} s, Auszuege {len(context)} Zeichen aus "
         f"{','.join(used) or '-'}, Tokens {usage.get('total', '?')} "
         f"(zwischengespeichert {usage.get('cached', 0)}) {usage.get('model', '')}")


# ---------------------------------------------------------------------------
# Spracheingabe fuer Browser ohne eigene Erkennung (Firefox)
# ---------------------------------------------------------------------------
MAX_AUDIO = 1024 * 1024  # das Widget nimmt mit 32 kbit/s auf: 60 s sind ~240 KB
AUDIO_TYPES = frozenset({"audio/ogg", "audio/webm", "audio/wav", "audio/x-wav",
                         "audio/mp4", "audio/mpeg", "audio/aac", "audio/flac"})


def transcribe(audio: bytes, mime: str, lang: str) -> str:
    """Gesprochene Frage -> Text (Gemini). Wirft ModelUnavailable bei Stoerung."""
    key = _google_key()
    if not key or os.getenv("LLM_PROVIDER", "").lower().strip() != "google":
        raise ModelUnavailable("Spracherkennung nicht eingerichtet")
    prompt = (f"This is a spoken question to an assistant about ESG and product regulations "
              f"for the textile and fashion industry. Transcribe it verbatim in "
              f"{_LANG_NAMES.get(lang, 'German')} with normal capitalisation and punctuation. "
              f"Output ONLY the text, no quotes, no explanation. If nothing intelligible is "
              f"audible, output nothing.")
    last = ""
    for model in _google_models():
        try:
            r = httpx.post(f"{_GOOGLE_BASE}/models/{model}:generateContent",
                           headers={"x-goog-api-key": key}, timeout=httpx.Timeout(25.0, connect=5.0),
                           json={"contents": [{"role": "user", "parts": [
                               {"inline_data": {"mime_type": "audio/wav" if mime == "audio/x-wav" else mime,
                                                "data": base64.b64encode(audio).decode()}},
                               {"text": prompt}]}],
                               "generationConfig": {"temperature": 0, "maxOutputTokens": 300}})
        except httpx.HTTPError as e:
            last = str(e)
            continue
        if r.status_code != 200:
            last = f"HTTP {r.status_code}"
            continue
        data = r.json()
        text = "".join(p.get("text", "") for c in data.get("candidates", [])
                       for p in c.get("content", {}).get("parts", []) if not p.get("thought"))
        return text.strip().strip('"„“').strip()[:MAX_QUESTION]
    raise ModelUnavailable(last or "keine Spracherkennung erreichbar")


def warm_up(langs: Iterable[str] = ("de",)) -> None:
    """Suchindex im Hintergrund vorbauen, damit die erste Frage nicht wartet."""
    def run():
        for lang in langs:
            try:
                get_index(lang)
            except Exception as e:  # noqa: BLE001
                _log(f"Vorbau {lang} fehlgeschlagen: {e}")
    threading.Thread(target=run, daemon=True, name="assistent-index").start()
