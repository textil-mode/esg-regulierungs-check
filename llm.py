"""Volltext-basierte Regulierungsanalyse mit Provider-Switch.

Unterstützt Ollama (lokal/kostenfrei), Anthropic Claude und OpenAI.
Für jede Regulierung:
  1. Volltext aus DB-Cache holen (fetcher.py kümmert sich ums Laden/Aktualisieren)
  2. Profil + Kriterien + Volltext-Auszug an LLM
  3. LLM gibt JSON mit applies/reason/passage zurück
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import queue
import re
import threading
import time
from typing import Callable

import db
from fetcher import current_text_hash
from i18n import coupling_texts, normalize_lang
from regulations import coupling_premise, coupling_verdict, relevant_fields_for


class _TruncatedJSON(ValueError):
    """Antwort war unvollstaendig; `partial` haelt das auto-reparierte Fragment.

    Subklasse von ValueError, MUSS daher vor dem generischen ValueError-Handler
    abgefangen werden, damit eine Trunkierung einen Retry ausloest statt still
    ein halbes Ergebnis zu liefern.
    """

    def __init__(self, partial: dict) -> None:
        super().__init__("JSON unvollstaendig (auto-repariert)")
        self.partial = partial


# Eine einzige englische Basis-System-Prompt + sprachspezifische Anweisung
# am Ende. So skaliert es sauber auf beliebig viele Sprachen.
_SYSTEM_BASE = """You are a precise ESG compliance analyst.
You receive a company profile, the applicability criteria of a regulation
and an extract of the law consisting of the sections most relevant to scope
(subject matter, scope, definitions, key articles), each preceded by its heading.

CRITICAL FORMATTING:
- Your ENTIRE response MUST be a single valid JSON object.
- NO preamble, NO explanation, NO markdown, NO reasoning before or after the JSON.
- Start your response DIRECTLY with {{ and end with }}.

Schema:
{{
  "applies": "ja" | "nein" | "moeglich",
  "reason": "...",
  "passage": "..."
}}

Decision rules:
- "ja" only if all thresholds/criteria are clearly met.
- "moeglich" if information is missing, special rules may apply, or thresholds are close.
- "nein" if clearly outside the scope.
- Use ONLY the thresholds, figures and conditions given in the "Applicability criteria" block and the full text. NEVER import thresholds from other regulations or from prior knowledge; if a number is given, use exactly that number.
- The company profile lists ONLY the characteristics that matter for THIS regulation. Never invent, assume or mention a characteristic that is not listed there (no sector, no headcount, no products unless they appear in the profile).
- IDENTITY RULE: you are never told the company's name and MUST NOT invent or guess one. Always refer to it as "the company" (in {lang_name}), never by a name, brand or location.
- If a "BINDING PRE-DETERMINED FACT" block is present, treat that fact as established truth. Base your decision on it together with this regulation's own criteria and never state anything that contradicts it.

"reason" — MANDATORY in every case, written in {lang_name}, max. 60 words, and ALWAYS in EXACTLY two sentences — no more, no fewer — with this structure:
  1. The single decisive criterion for THIS regulation. This sentence MUST name BOTH the threshold or condition from the criteria AND the company's own matching value (e.g. "1,200 employees against a threshold of more than 1,000", "sector: textiles", "group role: subsidiary of a non-EU parent"). A sentence without the company's actual figure or value is wrong.
  2. The conclusion that follows (applies / does not apply / to be verified). If "applies" is "moeglich", this sentence MUST state WHY it is open: name the profile information that is missing, or the special rule, transitional provision or exemption that could apply.
  No extra sentences, no lists, no commentary. Never leave it empty.
  LANGUAGE RULE: "reason" MUST be written entirely in {lang_name} — even if the law text, the criteria or the guidelines are in English or any other language. Translate legal terms into {lang_name}; never copy English sentences into "reason".

"passage" — MUST start with the article, paragraph or section reference, followed by ": " and then a short verbatim quote from the LAW TEXT EXTRACT (preferred, keep the original language of the law text) or a paraphrase in {lang_name}; max. 40 words in total. Example shape: "Art. 2(1): ..." / "§ 1 (3): ...". Take the reference from the "=== Art. 2 - ... ===" headings of the extract — the heading above the quoted sentence is its source. Never quote from the "Applicability criteria" block, only from the law text. Apart from the reference and the quote it MUST contain nothing — no notes, no meta commentary, no reasoning.

Keep the "applies" values exactly as ja/nein/moeglich."""

_LANG_NAMES = {
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
    "zh": "Simplified Chinese (Mandarin)",
}


def _system_prompt(language: str) -> str:
    name = _LANG_NAMES.get(language, "German")
    return _SYSTEM_BASE.format(lang_name=name)


# Beschriftung je Profilfeld. Der Prompt zeigt AUSSCHLIESSLICH die
# `relevant_fields` der jeweiligen Regulierung — siehe `_format_profile`.
_PROFILE_LABELS: dict[str, str] = {
    "legal_form": "Legal form",
    "group_role": "Group structure",
    "employees": "Total employees",
    "employees_de": "Employees in Germany",
    "revenue_eur": "Net revenue (EUR/year)",
    "balance_sheet_eur": "Balance sheet total (EUR)",
    "branch": "Industry",
    "b2c": "B2C business",
    "listed": "Capital-market oriented",
    "env_claims": "Environmental claims/labels in marketing",
    "eu_importer": ("EU importer (places products from third countries on the EU market / "
                    "first placing on the market)"),
    "product_categories": "Product categories",
    "sites": "Sites",
}

_USER_TEMPLATE = """{profile}

REGULATION: {reg_name} ({reg_full})
Source: {reg_url}
Relevant article/section: {article}

Applicability criteria (summary):
{criteria}
{premise}
LAW TEXT EXTRACT (selected sections; a line "=== Art. 2 - ... ===" marks the
source section of everything that follows it, "[…]" marks a shortened section):
---
{fulltext}
---

Evaluate strictly and respond as JSON per the schema."""


def _render_field(field: str, value) -> str:
    if field == "sites":
        sites = value or []
        if not sites:
            return "- none -"
        return "\n" + "\n".join(
            f"- {s.get('count', 0)}x {s.get('type', '-')} in {s.get('location', '-')}"
            for s in sites
        )
    if field == "product_categories":
        return ", ".join(value or []) or "none"
    if field in _BOOL_FIELDS:
        return "yes" if value else "no"
    if field in _INT_FIELDS:
        return str(int(value or 0))
    if field in _FLOAT_FIELDS:
        return f"{float(value or 0):,.0f}".replace(",", ".")
    return str(value or "-")


def _format_profile(profile: dict, reg: dict) -> str:
    """Profilblock fuer den Prompt — nur die `relevant_fields` dieser Regulierung.

    Das ist keine Sparmassnahme, sondern die Bedingung dafuer, dass der Cache
    global sein darf: der Prompt enthaelt exakt die Felder, die auch in
    `profile_hash` eingehen. Damit kann eine Begruendung nichts nennen, was
    nicht im Schluessel steckt — zwei Unternehmen, die sich denselben
    Cache-Eintrag teilen, haben in allem, was das LLM gesehen hat, denselben
    Wert. Insbesondere steht der FIRMENNAME nirgends im Prompt (er gehoert in
    keine `relevant_fields`), sodass keine Begruendung ihn tragen kann.
    """
    lines = ["COMPANY PROFILE:"]
    for field in relevant_fields_for(reg):
        label = _PROFILE_LABELS.get(field)
        if not label:      # z. B. `language` — kein Profilmerkmal fuer den Prompt
            continue
        lines.append(f"{label}: {_render_field(field, profile.get(field))}")
    if len(lines) == 1:
        lines.append("(no company characteristic is relevant for this regulation)")
    return "\n".join(lines)


_BOOL_FIELDS = frozenset({"b2c", "listed", "env_claims", "eu_importer"})
_INT_FIELDS = frozenset({"employees", "employees_de"})
_FLOAT_FIELDS = frozenset({"revenue_eur", "balance_sheet_eur"})


def _stable_value(field: str, value):
    """Normalisiert einen Profilwert, damit belanglose Typunterschiede
    (0 vs. None, True vs. 1, Reihenfolge einer Liste) keinen Cache-Miss ausloesen."""
    if field == "sites":
        return sorted(
            ({"type": s.get("type"), "location": s.get("location"), "count": s.get("count")}
             for s in (value or [])),
            key=lambda d: (d["type"] or "", d["location"] or ""),
        )
    if field == "product_categories":
        return sorted(value or [])
    if field in _BOOL_FIELDS:
        return bool(value)
    if field in _INT_FIELDS:
        return int(value or 0)
    if field in _FLOAT_FIELDS:
        return float(value or 0)
    return value


def profile_hash(profile: dict, reg: dict) -> str:
    """Profil-Schluessel fuer GENAU diese Regulierung.

    Es gehen nur die Felder ein, die deren Bewertung tragen
    (`regulations.relevant_fields_for`). Eine Aenderung an einem Feld, das fuer
    die Regulierung ohne Bedeutung ist — etwa der Firmenname —, laesst den
    Schluessel unveraendert; die Begruendung bleibt damit wortgleich stehen.
    """
    stable = {f: _stable_value(f, profile.get(f)) for f in relevant_fields_for(reg)}
    return hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


# Bei Prompt-Aenderungen hochzaehlen: invalidiert den analysis_cache, damit alle
# Nutzer einmalig frische Ergebnisse mit dem neuen Prompt bekommen.
_PROMPT_VERSION = "v5-2026-09-01"


def reg_hash(reg: dict, language: str, law_text_hash: str | None) -> str:
    """Reg-Schluessel aus Kriterien, Prompt-Stand, Sprache und Gesetzesstand.

    `law_text_hash` ist `fetcher.current_text_hash(reg_key, language)`: aendert
    sich der Gesetzestext, aendert sich der Schluessel — die alte Begruendung
    verfaellt und wird einmalig neu formuliert. Liegt kein Text vor (Quelle
    nicht abrufbar, `None`), traegt der Schluessel den Platzhalter '-'; das
    allein verwirft aber nichts, siehe `_cache_hit`.
    """
    raw = f"{reg['criteria']}|{_PROMPT_VERSION}|{language}|{law_text_hash or '-'}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text[3:]
        if text.lower().startswith("json"):
            text = text[4:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    return text


def _extract_json(text: str) -> dict:
    """Robuste JSON-Extraktion.

    Versucht der Reihe nach: direktes parse, klammer-balanciertes Substring,
    trailing-comma-cleanup, und als letzte Rettung ein Auto-Repair fuer
    abgeschnittene Ausgaben (unterminierter String / fehlende }).
    """
    text = _strip_fences(text or "").strip()
    if not text:
        raise ValueError("leere Antwort")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Finde erstes { und das passende schließende } (mit String-Awareness)
    start = text.find("{")
    if start < 0:
        raise ValueError(f"kein JSON-Objekt gefunden: {text[:120]!r}")
    depth = 0
    in_string = False
    escape = False
    end = -1
    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if end >= 0:
        snippet = text[start:end]
        # trailing commas vor } oder ] entfernen
        snippet = re.sub(r",(\s*[]}])", r"\1", snippet)
        return json.loads(snippet)

    # Auto-Repair: Ausgabe wurde mid-string abgeschnitten (z.B. max_tokens-Limit).
    # Wir schliessen den offenen String und die offenen Objekte, damit wenigstens
    # die schon geschriebenen Felder parsen.
    snippet = text[start:]
    if in_string:
        snippet += '"'
    # noch offene { schliessen
    remaining = depth if not in_string else (depth if depth > 0 else 1)
    if remaining > 0:
        snippet += "}" * remaining
    # trailing commas entfernen
    snippet = re.sub(r",(\s*[]}])", r"\1", snippet)
    try:
        partial = json.loads(snippet)
    except json.JSONDecodeError as e:
        raise ValueError(f"kein vollständiges JSON-Objekt (auto-repair fehlgeschlagen): "
                         f"{text[start:start+200]!r} / {e}")
    # Erfolgreich repariert, aber die Antwort war abgeschnitten: als Trunkierung
    # signalisieren, damit _analyze_one einen sauberen Retry versuchen kann.
    raise _TruncatedJSON(partial)


def _normalize_applies(val: str) -> str:
    """Normalisiert applies-Wert sprachunabhängig auf ja|nein|moeglich.

    Akzeptiert DE, EN, ES, FR, IT, ZH.
    """
    a = (val or "").lower().strip()
    a = a.replace("ö", "oe").replace("ä", "ae").replace("ü", "ue").replace("ß", "ss")
    # Alle Sprachvarianten auf DE-Basis mappen
    yes_set = {
        "yes", "true", "applies",                    # EN
        "sí", "si", "aplica", "se aplica",           # ES
        "oui", "s'applique", "applicable",           # FR
        "sì", "si applica",                          # IT
        "是", "适用",                                 # ZH
    }
    no_set = {
        "no", "false", "does not apply", "not applicable",  # EN
        "nein",                                             # DE (passthrough)
        "no aplica", "no se aplica",                        # ES
        "non", "ne s'applique pas", "pas applicable",       # FR
        "non si applica", "non applicabile",                # IT
        "否", "不适用",                                     # ZH
    }
    maybe_set = {
        "possible", "maybe", "may apply", "could apply", "possibly",  # EN
        "moeglich",                                                    # DE
        "posible", "puede aplicar", "quizás", "quizas",                # ES
        "possible (fr)", "peut s'appliquer", "peut-être", "peut-etre", # FR
        "possibile", "potrebbe applicarsi", "può applicarsi",          # IT
        "可能", "可能适用",                                             # ZH
    }
    # ZH/entity-Zeichen nicht durch lower/replace verändert → direkter Vergleich
    raw = (val or "").strip()
    if raw in ("是", "适用"):
        return "ja"
    if raw in ("否", "不适用"):
        return "nein"
    if raw in ("可能", "可能适用"):
        return "moeglich"
    if a in yes_set:
        return "ja"
    if a in no_set:
        return "nein"
    if a in maybe_set:
        return "moeglich"
    return a if a in ("ja", "nein", "moeglich") else "moeglich"


def _enrich(reg: dict, parsed: dict) -> dict:
    return {
        "nr": reg["nr"],
        "key": reg["key"],
        "name": reg["name"],
        "full_name": reg["full_name"],
        "url": reg["url"],
        "scope": reg["scope"],
        "article": reg.get("key_article", ""),
        "applies": _normalize_applies(parsed.get("applies")),
        "reason": parsed.get("reason", ""),
        "passage": parsed.get("passage", "-"),
    }


# ---------- Deterministische Faelle + Cache-Planung ----------
def deterministic_result(reg: dict, profile: dict, language: str) -> dict | None:
    """Ergebnis ohne LLM, wo die Rechtslage die Antwort bereits festlegt.

    Betrifft die per Kopplung entschiedenen Regulierungen (CSRD, CSRD_DE, ESRS,
    Taxonomie-VO, HinSchG, Whistleblower-RL). Struktur identisch zu `_enrich`.
    None heisst: dieser Fall gehoert weiterhin dem LLM.
    """
    verdict = coupling_verdict(reg.get("key", ""), profile)
    if not verdict:
        return None
    texts = coupling_texts(reg["key"], verdict, language)
    if not texts:
        return None
    reason, passage = texts
    return {**_enrich(reg, {}), "applies": verdict["applies"],
            "reason": reason, "passage": passage}


def _cache_hit(rows: list[dict], reg: dict, language: str,
               law_text_hash: str | None, current_reg_hash: str) -> dict | None:
    """Passender Cache-Eintrag aus den Zeilen einer Regulierung (neueste zuerst).

    Normalfall: der Schluessel stimmt exakt. Liegt aktuell KEIN Gesetzestext vor
    (`law_text_hash is None`, z. B. Quelle voruebergehend nicht erreichbar), waere
    ein Miss die falsche Antwort: er wuerde bei jedem Lauf eine neue Begruendung
    erzeugen — und zwar ohne Gesetzestext, also schlechter als die vorhandene.
    Deshalb gilt dann der zuletzt gespeicherte Eintrag weiter, sofern Kriterien
    und Prompt-Stand unveraendert sind (nachgerechnet aus seinem `text_hash`).
    """
    for row in rows:
        if row.get("reg_hash") == current_reg_hash:
            return row["result"]
    if law_text_hash is not None:
        return None
    for row in rows:
        if row.get("reg_hash") == reg_hash(reg, language, row.get("text_hash")):
            return row["result"]
    return None


def plan_analysis(profile: dict, regs: list[dict], language: str
                  ) -> tuple[list[dict], list[dict], dict[str, tuple[str, str, str | None]]]:
    """Teilt die Regulierungen in "steht schon fest" und "muss ans LLM".

    Rueckgabe:
      ready — fertige Ergebnisse (Textbaustein oder Cache-Treffer)
      todo  — Regulierungen, die das LLM bewerten muss
      keys  — reg_key -> (profile_hash, reg_hash, text_hash) zum Zurueckschreiben
    """
    language = normalize_lang(language)
    pending: list[tuple[dict, str, str, str | None]] = []
    ready: list[dict] = []
    for reg in regs:
        fixed = deterministic_result(reg, profile, language)
        if fixed:
            ready.append(fixed)
            continue
        ph = profile_hash(profile, reg)
        th = current_text_hash(reg["key"], language)
        pending.append((reg, ph, reg_hash(reg, language, th), th))

    cached = db.get_cache([(reg["key"], ph) for reg, ph, _rh, _th in pending])
    todo: list[dict] = []
    keys: dict[str, tuple[str, str, str | None]] = {}
    for reg, ph, rh, th in pending:
        hit = _cache_hit(cached.get((reg["key"], ph), []), reg, language, th, rh)
        if hit is not None:
            ready.append(hit)
        else:
            todo.append(reg)
            keys[reg["key"]] = (ph, rh, th)
    return ready, todo, keys


# ---------- Provider-Abstraktion ----------
class LLMClient:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower().strip()
        if self.provider == "ollama":
            from openai import AsyncOpenAI
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
            self.client = AsyncOpenAI(base_url=f"{host}/v1", api_key="ollama")
            self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
            self.extra = {"extra_body": {"options": {"num_ctx": int(os.getenv("OLLAMA_CTX", "16384"))}}}
        elif self.provider == "openai":
            from openai import AsyncOpenAI
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY fehlt.")
            base_url = os.getenv("OPENAI_BASE_URL") or None
            # Explizites Timeout (Sek.) — sonst haengt der Default (10 Minuten)
            # die Analyse, wenn ein einzelner Call am Provider haengenbleibt.
            llm_timeout = float(os.getenv("LLM_REQUEST_TIMEOUT", "60"))
            self.client = AsyncOpenAI(api_key=key, base_url=base_url, timeout=llm_timeout)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.extra = {}
        elif self.provider == "google":
            import httpx as _httpx
            self.model = os.getenv("GOOGLE_MODEL") or os.getenv("OPENAI_MODEL", "gemini-2.5-flash")
            self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise RuntimeError("GOOGLE_API_KEY fehlt.")
            self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        elif self.provider == "anthropic":
            from anthropic import AsyncAnthropic
            key = os.getenv("ANTHROPIC_API_KEY")
            if not key:
                raise RuntimeError("ANTHROPIC_API_KEY fehlt.")
            self.client = AsyncAnthropic(api_key=key)
            self.model = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5")
            self.extra = {}
        else:
            raise RuntimeError(f"Unbekannter LLM_PROVIDER: {self.provider}")

    async def ask(self, system: str, user: str, max_tokens: int = 1500, json_mode: bool = True) -> str:
        if self.provider in ("ollama", "openai"):
            kwargs: dict = {
                "model": self.model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "max_tokens": max_tokens,
                "temperature": 0.0,
                # Fester Seed: gleiche Eingabe -> gleiche Formulierung (sofern Provider unterstuetzt)
                "seed": 42,
                **self.extra,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            try:
                resp = await self.client.chat.completions.create(**kwargs)
            except Exception as e:  # noqa: BLE001
                err = str(e)
                if json_mode and ("response_format" in err or "json_object" in err):
                    kwargs.pop("response_format", None)
                    resp = await self.client.chat.completions.create(**kwargs)
                elif "seed" in err.lower():
                    kwargs.pop("seed", None)
                    resp = await self.client.chat.completions.create(**kwargs)
                else:
                    raise
            return resp.choices[0].message.content or ""
        elif self.provider == "google":
            import httpx as _httpx
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            body = {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "generationConfig": {
                    "temperature": 0.0,
                    # Greedy-Sampling + fester Seed: minimiert Formulierungs-Varianz
                    # zwischen identischen Laeufen (Gemini ist sonst auch bei temp=0
                    # nicht deterministisch).
                    "topK": 1,
                    "seed": 42,
                    "maxOutputTokens": max_tokens,
                    "responseMimeType": "application/json" if json_mode else "text/plain",
                },
            }
            async with _httpx.AsyncClient(timeout=90) as client:
                resp = await client.post(url, json=body)
                resp.raise_for_status()
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:  # anthropic
            resp = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return resp.content[0].text


def _parse_retry_after(err_str: str) -> float:
    m = re.search(r"retry[-_ ]?after[\"':\s]*([0-9.]+)", err_str, re.I)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return 0.0


async def _analyze_one(client: LLMClient, reg: dict, fulltext: str,
                       language: str, profile: dict | None = None) -> dict:
    system = _system_prompt(language)
    profile_block = _format_profile(profile or {}, reg)
    fulltext_placeholder = "(full text unavailable)"
    premise = coupling_premise(reg.get("key", ""), profile or {})
    premise_block = f"\nBINDING PRE-DETERMINED FACT:\n{premise}\n" if premise else ""
    user_msg = _USER_TEMPLATE.format(
        profile=profile_block,
        reg_name=reg["name"],
        reg_full=reg["full_name"],
        reg_url=reg["url"],
        article=reg.get("key_article", ""),
        criteria=reg["criteria"],
        premise=premise_block,
        fulltext=fulltext[:int(os.getenv("FULLTEXT_MAX_CHARS", "40000"))] if fulltext else fulltext_placeholder,
    )
    last_error: str | None = None
    key = reg.get("key", "?")
    print(f"[llm] start {key}", flush=True)
    for attempt in range(6):  # mehr Versuche (war 4)
        try:
            # max_tokens großzügig, weil manche Modelle das 80-Wort-Limit
            # ueberschreiten und die JSON sonst mid-string abgeschnitten wird.
            text = await client.ask(system, user_msg, max_tokens=3000)
            parsed = _extract_json(text)
            print(f"[llm] ok    {key}", flush=True)
            return _enrich(reg, parsed)
        except _TruncatedJSON as e:
            # Antwort abgeschnitten: erneut versuchen; erst beim letzten Versuch
            # das auto-reparierte Fragment akzeptieren (besser als ein Fehler).
            last_error = "JSON unvollstaendig (Antwort abgeschnitten)"
            print(f"[llm] retry {key} attempt={attempt} truncated", flush=True)
            if attempt < 5:
                await asyncio.sleep(0.6)
                continue
            print(f"[llm] partial {key}: nutze auto-repariertes Fragment", flush=True)
            return _enrich(reg, e.partial)
        except (json.JSONDecodeError, ValueError) as e:
            last_error = f"JSON-Parse: {e}"
            print(f"[llm] retry {key} attempt={attempt} json-parse: {e}", flush=True)
            await asyncio.sleep(0.6)
        except Exception as e:  # noqa: BLE001
            last_error = str(e)
            err_low = last_error.lower()
            is_rate_limit = ("429" in last_error or "rate_limit" in err_low
                             or "resource_exhausted" in err_low or "quota" in err_low)
            print(f"[llm] retry {key} attempt={attempt} ratelimit={is_rate_limit}: {last_error[:160]}",
                  flush=True)
            if is_rate_limit:
                # Google sendet "retry in Xs" - parsen, sonst 60s default
                import re as _re
                m = _re.search(r"retry in ([\d.]+)s", last_error, _re.I)
                wait = float(m.group(1)) if m else (_parse_retry_after(last_error) or 60.0)
                await asyncio.sleep(min(wait + 2, 90))
            else:
                await asyncio.sleep(1.5 * (attempt + 1))
    print(f"[llm] fail  {key}: {last_error}", flush=True)
    return {**_enrich(reg, {}), "applies": "error", "reason": last_error or "unbekannter Fehler", "passage": "-"}


class RateLimiter:
    """Async sliding-window rate limiter. Begrenzt auf rpm Anfragen pro 60s."""

    def __init__(self, rpm: int) -> None:
        self.rpm = max(1, rpm)
        self.timestamps: list[float] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self.lock:
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < 60.0]
            if len(self.timestamps) >= self.rpm:
                wait = 60.0 - (now - self.timestamps[0]) + 0.2
                if wait > 0:
                    await asyncio.sleep(wait)
                    now = time.time()
                    self.timestamps = [t for t in self.timestamps if now - t < 60.0]
            self.timestamps.append(now)


async def _run(profile: dict, jobs: list[tuple[dict, str]], result_cb: Callable[[dict], None]) -> None:
    client = LLMClient()
    language = (profile.get("language") or "de").lower()
    if language not in ("de", "en", "es", "fr", "it", "zh"):
        language = "de"

    concurrency = int(os.getenv("LLM_CONCURRENCY", "4"))
    rpm = int(os.getenv("LLM_RPM", "18"))   # 18 statt 20 = Sicherheitspuffer
    sem = asyncio.Semaphore(max(1, concurrency))
    limiter = RateLimiter(rpm)

    async def bound(reg: dict, fulltext: str) -> None:
        async with sem:
            await limiter.acquire()
            res = await _analyze_one(client, reg, fulltext, language, profile)
            result_cb(res)

    await asyncio.gather(*(bound(reg, ft) for reg, ft in jobs))


def analyze_streaming(
    profile: dict,
    jobs: list[tuple[dict, str]],
    cached_hits: list[dict] | None = None,
) -> "queue.Queue[dict | None]":
    """Startet Analyse im Hintergrund-Thread.

    jobs  = Liste (Regulierung, Volltext) für Misses (echt zu analysieren)
    cached_hits = bereits gültige Cache-Einträge (werden sofort gepusht)
    """
    q: queue.Queue[dict | None] = queue.Queue()
    for hit in (cached_hits or []):
        q.put({**hit, "_from_cache": True})

    def worker() -> None:
        try:
            if jobs:
                asyncio.run(_run(profile, jobs, lambda r: q.put(r)))
        except Exception as e:  # noqa: BLE001
            for reg, _ in jobs:
                q.put({**_enrich(reg, {}), "applies": "error", "reason": f"Setup-Fehler: {e}", "passage": "-"})
        finally:
            q.put(None)

    threading.Thread(target=worker, daemon=True).start()
    return q
