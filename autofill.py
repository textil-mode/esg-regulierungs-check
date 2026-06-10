"""KI-gestütztes Vorbefüllen der Stammdaten anhand des Unternehmensnamens.

Ablauf:
  1. Wikipedia-Suche (de, Fallback en) → Artikel-Volltext
  2. Wikidata-Property P856 → offizielle Website → Homepage-Text (fetcher-Cache)
  3. LLM extrahiert NUR explizit belegte Angaben als JSON (sonst null)
  4. Server-seitige Validierung: Enums müssen exakt den Formular-Optionen
     entsprechen, Zahlen werden geparst — alles andere wird verworfen.

Es wird nichts geraten: kein Treffer → Feld bleibt leer und damit manuell.
"""
from __future__ import annotations

import asyncio
import json
import time

import httpx

from fetcher import USER_AGENT, fetch_url_text
from llm import LLMClient, _extract_json, _TruncatedJSON
from regulations import (
    BRANCHES,
    GROUP_ROLES,
    LEGAL_FORMS,
    LOCATIONS,
    PRODUCT_CATEGORIES,
)

_WIKI_TIMEOUT = 12.0
_MAX_SOURCE_CHARS = 18000


def _wiki_api(lang: str, params: dict) -> dict:
    url = f"https://{lang}.wikipedia.org/w/api.php"
    base = {"format": "json", "formatversion": 2}
    with httpx.Client(timeout=_WIKI_TIMEOUT, headers={"User-Agent": USER_AGENT}) as c:
        r = c.get(url, params={**base, **params})
        r.raise_for_status()
        return r.json()


def _wiki_lookup(name: str) -> tuple[str, str | None, str | None]:
    """Sucht den Wikipedia-Artikel. Rückgabe: (volltext, artikel_url, wikidata_id)."""
    for lang in ("de", "en"):
        try:
            search = _wiki_api(lang, {
                "action": "query", "list": "search", "srsearch": name, "srlimit": 1,
            })
            hits = search.get("query", {}).get("search") or []
            if not hits:
                continue
            title = hits[0]["title"]
            page = _wiki_api(lang, {
                "action": "query", "prop": "extracts|pageprops", "explaintext": 1,
                "titles": title, "ppprop": "wikibase_item",
            })
            pages = page.get("query", {}).get("pages") or []
            if not pages:
                continue
            p = pages[0]
            text = (p.get("extract") or "").strip()
            if not text:
                continue
            url = f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}"
            qid = (p.get("pageprops") or {}).get("wikibase_item")
            # Der Plaintext-Export laesst die Infobox weg — dort stehen aber
            # gerade Mitarbeiterzahl, Umsatz, Rechtsform. Deshalb zusaetzlich
            # die gerenderte Artikelseite holen (Infobox-Text inklusive).
            try:
                html_res = fetch_url_text(url, language=lang, timeout=10.0)
                html_text = (html_res.get("text") or "").strip()
                if html_text:
                    text = f"{html_text[:6000]}\n\n{text}"
            except Exception as e:  # noqa: BLE001
                print(f"[autofill] wiki-html fehlgeschlagen: {e}", flush=True)
            return text[:_MAX_SOURCE_CHARS], url, qid
        except Exception as e:  # noqa: BLE001
            print(f"[autofill] wiki {lang} fehlgeschlagen: {e}", flush=True)
    return "", None, None


def _official_website(qid: str) -> str | None:
    """Offizielle Website (P856) aus Wikidata."""
    try:
        with httpx.Client(timeout=_WIKI_TIMEOUT, headers={"User-Agent": USER_AGENT}) as c:
            r = c.get("https://www.wikidata.org/w/api.php", params={
                "action": "wbgetclaims", "entity": qid, "property": "P856",
                "format": "json",
            })
            r.raise_for_status()
            claims = r.json().get("claims", {}).get("P856") or []
            if claims:
                return claims[0]["mainsnak"]["datavalue"]["value"]
    except Exception as e:  # noqa: BLE001
        print(f"[autofill] wikidata P856 fehlgeschlagen: {e}", flush=True)
    return None


_EXTRACT_SYSTEM = """You are a careful data-extraction assistant for a German ESG compliance form.
You receive source texts (Wikipedia article, company website) about ONE company.

Extract ONLY values that are EXPLICITLY stated in the sources. If a value is not
explicitly stated, return null for that field. NEVER guess, NEVER estimate,
NEVER derive from world knowledge — only what the given texts literally support.

Your ENTIRE response MUST be a single valid JSON object, no markdown, no commentary:
{{
  "name": string|null,              // official company name
  "employees": integer|null,        // total employees worldwide
  "employees_de": integer|null,     // employees in Germany (only if explicitly stated)
  "revenue_eur": number|null,       // annual net revenue in EUR (convert "4,3 Mrd." -> 4300000000)
  "balance_sheet_eur": number|null, // balance sheet total in EUR
  "legal_form": one of {legal_forms} or null,
  "group_role": one of {group_roles} or null,
  "branch": one of {branches} or null,
  "b2c": true|false|null,           // sells to consumers
  "listed": true|false|null,        // capital-market oriented / stock-listed
  "eu_importer": true|false|null,   // imports products from third countries into the EU
  "product_categories": array of values from {product_categories} (only explicitly supported ones, else []),
  "hq_location": one of {locations} or null  // where the headquarters is located
}}

Rules for enum fields: pick EXACTLY one of the listed strings (verbatim, including
umlauts) or null. When in doubt between two enum values, return null instead.
- "legal_form": map e.g. "Aktiengesellschaft"/"SE" -> "AG / SE".
- "branch": pick the MOST SPECIFIC listed industry the sources clearly name
  (e.g. a fashion/apparel company -> "Textil / Bekleidung / Leder", NOT the
  generic "Verarbeitendes Gewerbe / Industrie").
- "group_role": only if the sources explicitly describe the group structure
  (e.g. "Muttergesellschaft des Konzerns", "Tochter von X"); otherwise null.
- "product_categories": only categories the company itself manufactures or
  sells as core business according to the sources.
Currency: if revenue is given in USD and no EUR figure exists, return null.
"""

_EXTRACT_USER = """Company name entered by the user: {name}

=== SOURCE 1: WIKIPEDIA ({wiki_url}) ===
{wiki_text}

=== SOURCE 2: COMPANY WEBSITE ({site_url}) ===
{site_text}

Extract the JSON now."""


def _validate(parsed: dict) -> dict:
    """Verwirft alles, was nicht exakt zu den Formular-Optionen passt."""
    out: dict = {}

    def _num(key: str, cast):
        v = parsed.get(key)
        if isinstance(v, (int, float)) and v > 0:
            out[key] = cast(v)

    if isinstance(parsed.get("name"), str) and parsed["name"].strip():
        out["name"] = parsed["name"].strip()[:200]
    _num("employees", int)
    _num("employees_de", int)
    _num("revenue_eur", float)
    _num("balance_sheet_eur", float)

    for key, allowed in (("legal_form", LEGAL_FORMS), ("group_role", GROUP_ROLES),
                         ("branch", BRANCHES), ("hq_location", LOCATIONS)):
        v = parsed.get(key)
        if isinstance(v, str) and v in allowed:
            out[key] = v

    for key in ("b2c", "listed", "eu_importer"):
        v = parsed.get(key)
        if isinstance(v, bool):
            out[key] = v

    cats = parsed.get("product_categories")
    if isinstance(cats, list):
        valid = [c for c in cats if isinstance(c, str) and c in PRODUCT_CATEGORIES]
        if valid:
            out["product_categories"] = valid

    return out


def research_company(name: str, language: str = "de") -> dict:
    """Recherchiert Stammdaten. Rückgabe: {fields: {...}, sources: [urls]}."""
    name = (name or "").strip()
    if not name:
        return {"fields": {}, "sources": [], "error": "kein Name"}

    wiki_text, wiki_url, qid = _wiki_lookup(name)
    site_url = _official_website(qid) if qid else None
    site_text = ""
    if site_url:
        try:
            res = fetch_url_text(site_url, language=language, timeout=10.0)
            site_text = (res.get("text") or "")[:_MAX_SOURCE_CHARS]
        except Exception as e:  # noqa: BLE001
            print(f"[autofill] website-fetch fehlgeschlagen: {e}", flush=True)

    if not wiki_text and not site_text:
        return {"fields": {}, "sources": [], "error": "keine Quellen gefunden"}

    system = _EXTRACT_SYSTEM.format(
        legal_forms=json.dumps(LEGAL_FORMS, ensure_ascii=False),
        group_roles=json.dumps(GROUP_ROLES, ensure_ascii=False),
        branches=json.dumps(BRANCHES, ensure_ascii=False),
        product_categories=json.dumps(PRODUCT_CATEGORIES, ensure_ascii=False),
        locations=json.dumps(LOCATIONS, ensure_ascii=False),
    )
    user = _EXTRACT_USER.format(
        name=name,
        wiki_url=wiki_url or "-",
        wiki_text=wiki_text or "(nicht gefunden)",
        site_url=site_url or "-",
        site_text=site_text or "(nicht gefunden)",
    )

    client = LLMClient()
    raw = None
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            raw = asyncio.run(client.ask(system, user, max_tokens=1500))
            break
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"[autofill] LLM-Versuch {attempt + 1} fehlgeschlagen: {e}", flush=True)
            time.sleep(2.0 * (attempt + 1))
    if raw is None:
        return {"fields": {}, "sources": [u for u in (wiki_url, site_url) if u],
                "error": f"LLM nicht erreichbar: {last_err}"}
    try:
        parsed = _extract_json(raw)
    except _TruncatedJSON as e:
        parsed = e.partial
    except ValueError as e:
        return {"fields": {}, "sources": [u for u in (wiki_url, site_url) if u],
                "error": f"LLM-Antwort unlesbar: {e}"}

    fields = _validate(parsed if isinstance(parsed, dict) else {})
    sources = [u for u in (wiki_url, site_url) if u]
    return {"fields": fields, "sources": sources, "error": None}
