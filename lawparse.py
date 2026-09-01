"""Strukturbasierte Auswahl des Gesetzestext-Kontexts fuer die LLM-Analyse.

Bisher wurde Gesetzestext + Guidelines konkateniert und vorn auf
FULLTEXT_MAX_CHARS abgeschnitten. EU-Rechtsakte beginnen aber mit bis zu
100 Erwaegungsgruenden — der Anwendungsbereich (Art. 1-3) lag dadurch oft
hinter dem Schnitt, die Guidelines fast immer.

Dieses Modul zerlegt den Rohtext in Artikel-/Paragraphen-Abschnitte und baut
den Kontext gezielt aus den relevanten Abschnitten zusammen:

  a) Art. 1-3 (Gegenstand, Anwendungsbereich, Begriffsbestimmungen)
  b) die in regulations.py gepflegten `key_article`-Verweise
  c) Abschnitte mit Schwellenwert-Signalwoertern
  d) gekuerzte Guidelines
  e) restliche Abschnitte in Dokumentreihenfolge, solange Budget bleibt

Jeder Abschnitt bekommt eine Kopfzeile (`=== Art. 2 - Anwendungsbereich ===`),
damit das LLM die Fundstelle sauber zitieren kann.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

_ARTICLE_WORDS = r"Artikel|Article|Articolo|Art[ií]culo|Art\."
_ANNEX_WORDS = r"ANHANG|Anhang|ANNEX|Annex|ANNEXE|Annexe|ANEXO|Anexo|ALLEGATO|Allegato|Anlage"

# Zeichen, die vor einer Ueberschrift stehen koennen (zitierte eingefuegte
# Artikel in Aenderungsrichtlinien: >>"Artikel 19a<<).
_LEAD_JUNK = "„“”«»‘’\"'()*-–— \t"

# Steht direkt hinter der Nummer eines dieser Woerter, ist die Zeile ein
# Querverweis im Fliesstext ("Artikel 19a Absatz 9 ..."), keine Ueberschrift.
_CROSSREF = re.compile(
    r"^(absatz|abs\.|buchstabe|unterabsatz|ziffer|nummer|satz|paragraph|paragraphe|"
    r"point|para|letter|subparagraph|apartado|comma|bis|und|and|oder|or|des|der|dieser|"
    r"of|the|dieses|genannt)\b",
    re.I,
)

_ART_HEAD = re.compile(rf"^(?:{_ARTICLE_WORDS})\s*(\d{{1,3}}[a-z]?)\b(.*)$", re.I)
_PAR_HEAD = re.compile(r"^§{1,2}\s*(\d{1,4}[a-z]?)\b(.*)$")
_ANN_HEAD = re.compile(rf"^(?:{_ANNEX_WORDS})\b[\s:.-]*([IVXLC]{{1,6}}|\d{{1,2}})?\s*$")


def _clean_title(rest: str) -> str | None:
    """Titel-Rest einer Ueberschriftszeile, oder None wenn es keine Ueberschrift ist."""
    t = rest.strip(" \t:.-–—·")
    if not t:
        return ""
    if len(t) > 100 or _CROSSREF.match(t):
        return None
    # Ueberschriften sind gross geschrieben; "Artikel 5 gilt entsprechend."
    # ist Fliesstext.
    if not t[0].isupper():
        return None
    return t


def parse_sections(raw: str) -> list[dict]:
    """Zerlegt einen Gesetzestext in Abschnitte.

    Liefert eine Liste von {label, kind, num, title, text}. `kind` ist
    "article" (Artikel / §) oder "annex". Alles vor der ersten Ueberschrift
    (Erwaegungsgruende, Praeambel) wird verworfen. Bei Texten ohne erkennbare
    Struktur ist die Liste leer — der Aufrufer reicht dann den Rohtext durch.
    """
    if not raw:
        return []
    lines = raw.replace(" ", " ").replace("\r\n", "\n").split("\n")

    heads: list[tuple[int, str, str, str, str]] = []  # (zeile, kind, marker, num, titel)
    for i, line in enumerate(lines):
        s = line.lstrip(_LEAD_JUNK).rstrip()
        if not s:
            continue
        m = _PAR_HEAD.match(s)
        if m:
            title = _clean_title(m.group(2))
            if title is not None:
                heads.append((i, "article", "§", m.group(1), title))
                continue
        m = _ART_HEAD.match(s)
        if m:
            title = _clean_title(m.group(2))
            if title is not None:
                heads.append((i, "article", "Art.", m.group(1), title))
                continue
        m = _ANN_HEAD.match(s)
        if m:
            heads.append((i, "annex", "Anhang", (m.group(1) or "").upper(), ""))

    if len(heads) < 3:
        return []

    sections: list[dict] = []
    for pos, (ln, kind, marker, num, title) in enumerate(heads):
        end = heads[pos + 1][0] if pos + 1 < len(heads) else len(lines)
        body = "\n".join(lines[ln + 1:end]).strip()
        if not title:
            # PDF-Artefakt: Ueberschrift und Titel stehen auf zwei Zeilen.
            first = body.split("\n", 1)[0].strip() if body else ""
            if first and len(first) < 90 and not first[0].isdigit() and not first.startswith("("):
                title = first
        label = f"{marker} {num}".strip()
        sections.append({
            "label": label,
            "kind": kind,
            "num": num.lower(),
            "title": title,
            "text": body,
        })
    # Inhaltsverzeichnis-Seiten (gesetze-im-internet.de) erzeugen viele
    # Ueberschriften ohne Text — dann lieber den Rohtext durchreichen.
    if sum(len(s["text"]) for s in sections) < 1000:
        return []
    return sections


# ---------------------------------------------------------------------------
# key_article-Referenzen ("Art. 19a, 29a", "§§ 289b-289h HGB-E", "Annex I")
# ---------------------------------------------------------------------------

_REF_RE = re.compile(
    r"(?:§§|§|Art\.|Artikel|Article)\s*"
    r"(\d{1,4}[a-z]?(?:\s*[-–—]\s*\d{0,4}[a-z]?)?(?:\s*,\s*\d{1,4}[a-z]?)*)",
    re.I,
)
_ANNEX_REF_RE = re.compile(rf"(?:{_ANNEX_WORDS})\s+([IVXLC]{{1,6}}|\d{{1,2}})\b")
_TOKEN_RE = re.compile(r"^(\d{1,4})([a-z]?)$")


def _expand_range(a: str, b: str) -> list[str]:
    ma, mb = _TOKEN_RE.match(a), _TOKEN_RE.match(b)
    if not ma or not mb:
        return [a, b]
    if ma.group(1) == mb.group(1) and ma.group(2) and mb.group(2):
        return [ma.group(1) + chr(c) for c in range(ord(ma.group(2)), ord(mb.group(2)) + 1)]
    lo, hi = int(ma.group(1)), int(mb.group(1))
    if 0 <= hi - lo <= 20:
        return [str(n) for n in range(lo, hi + 1)]
    return [a, b]


def article_refs(key_article: str) -> tuple[list[str], list[str]]:
    """Parst das `key_article`-Feld zu (Artikelnummern, Anhang-Kennungen)."""
    arts: list[str] = []
    for m in _REF_RE.finditer(key_article or ""):
        for part in m.group(1).split(","):
            part = part.strip()
            rng = re.split(r"[-–—]", part)
            if len(rng) == 2 and rng[0].strip() and rng[1].strip():
                arts.extend(_expand_range(rng[0].strip().lower(), rng[1].strip().lower()))
            elif part:
                arts.append(part.lower())
    annexes = [m.group(1).upper() for m in _ANNEX_REF_RE.finditer(key_article or "")]
    # Reihenfolge erhalten, Duplikate raus
    return list(dict.fromkeys(arts)), list(dict.fromkeys(annexes))


# ---------------------------------------------------------------------------
# Schwellenwert-Signalwoerter
# ---------------------------------------------------------------------------

_SIGNALS = (
    "anwendungsbereich", "geltungsbereich", "gegenstand", "begriffsbestimmungen",
    "scope", "subject matter", "definitions", "objet", "ambito", "ámbito", "oggetto",
    "beschäftigt", "beschaeftigt", "arbeitnehmer", "mitarbeiter", "belegschaft",
    "employees", "workers", "employés", "empleados", "dipendenti",
    "umsatz", "turnover", "revenue", "chiffre d'affaires", "volumen de negocios",
    "bilanzsumme", "balance sheet total", "balance sheet",
    "in verkehr bringen", "inverkehrbringen", "in verkehr gebracht",
    "placing on the market", "placed on the market", "made available on the market",
    "bereitstellung auf dem markt", "einführer", "importeur", "importer",
    "große unternehmen", "grosse unternehmen", "large undertakings",
    "kleine und mittlere", "small and medium", "kleinstunternehmen", "microenterprise",
    "schwellenwert", "threshold", "gilt für", "gilt fuer", "findet anwendung",
    "applies to", "shall apply to", "this regulation applies", "diese verordnung gilt",
    "diese richtlinie gilt", "dieses gesetz gilt",
    "marktteilnehmer", "wirtschaftsakteur", "operator", "economic operator",
)


def _signal_score(text: str) -> int:
    low = text.lower()
    return sum(1 for s in _SIGNALS if s in low)


# ---------------------------------------------------------------------------
# Kontext-Aufbau
# ---------------------------------------------------------------------------

_SCOPE_NUMS = ("1", "2", "3")


def _block(sec: dict, cap: int) -> str:
    head = f"=== {sec['label']}" + (f" - {sec['title']}" if sec["title"] else "") + " ==="
    body = sec["text"]
    if len(body) > cap:
        body = body[:cap].rstrip() + " […]"
    return f"{head}\n{body}" if body else head


def build_context(reg: dict, law_text: str, guidelines: list[dict] | None,
                  max_chars: int) -> str:
    """Baut den LLM-Kontext fuer eine Regulierung.

    reg         — Eintrag aus regulations.REGULATIONS
    law_text    — Rohtext des Gesetzes (aus dem fetcher-Cache)
    guidelines  — [{"name", "url", "text"}, …] (optional)
    max_chars   — Gesamtbudget (FULLTEXT_MAX_CHARS)
    """
    guidelines = guidelines or []
    header = f"=== GESETZESTEXT: {reg.get('full_name') or reg.get('name') or ''} ==="
    law_text = (law_text or "").strip()

    # Guidelines zuerst kuerzen, damit ihr echter Platzbedarf feststeht.
    g_total = min(3000 * len(guidelines), max(0, max_chars // 5))
    per_g = g_total // len(guidelines) if guidelines else 0
    g_blocks: list[str] = []
    for g in guidelines:
        text = (g.get("text") or "").strip()
        if not text or per_g <= 0:
            continue
        if len(text) > per_g:
            text = text[:per_g].rstrip() + " […]"
        g_blocks.append(f"=== GUIDELINE: {g.get('name', '')} ({g.get('url', '')}) ===\n{text}")
    g_len = sum(len(b) + 1 for b in g_blocks)

    law_budget = max(0, max_chars - len(header) - 1 - g_len)
    sections = parse_sections(law_text)

    if not sections:
        # Kein erkennbarer Aufbau (TOC-Seite, Landingpage, PDF-Artefakte):
        # Rohtext unveraendert durchreichen.
        law_part = law_text[:law_budget]
    else:
        ref_arts, ref_annexes = article_refs(reg.get("key_article") or "")

        prio: list[int] = []
        for i, s in enumerate(sections):
            if s["kind"] == "article" and s["num"] in _SCOPE_NUMS:
                prio.append(i)
        for i, s in enumerate(sections):
            if s["kind"] == "article" and s["num"] in ref_arts:
                prio.append(i)
            elif s["kind"] == "annex" and s["num"] in ref_annexes:
                prio.append(i)
        prio = list(dict.fromkeys(prio))

        # Budget so auf die Vorrang-Abschnitte verteilen, dass alle hineinpassen
        # (bei Aenderungsrichtlinien wie der CSRD sind das schnell 6 Abschnitte).
        cap_prio = max(2000, law_budget // max(3, len(prio)))
        cap_sig = max(800, law_budget // 8)
        cap_fill = max(600, law_budget // 12)

        scored = sorted(
            ((_signal_score(s["text"] + " " + s["title"]), -len(s["text"]), i)
             for i, s in enumerate(sections)),
            reverse=True,
        )
        signal = [i for score, _, i in scored if score >= 2]

        chosen: dict[int, int] = {}   # index -> cap
        for i in prio:
            chosen.setdefault(i, cap_prio)
        for i in signal:
            chosen.setdefault(i, cap_sig)
        for i in range(len(sections)):
            chosen.setdefault(i, cap_fill)

        used = 0
        keep: dict[int, str] = {}
        # prio/signal/fill in dieser Reihenfolge einpassen, Ausgabe spaeter in
        # Dokumentreihenfolge.
        order = list(dict.fromkeys(prio + signal + list(range(len(sections)))))
        for i in order:
            block = _block(sections[i], chosen[i])
            if used + len(block) + 1 > law_budget:
                continue
            keep[i] = block
            used += len(block) + 1
        law_part = "\n".join(keep[i] for i in sorted(keep))

    parts = [header]
    if law_part:
        parts.append(law_part)
    parts.extend(g_blocks)
    return "\n".join(parts)[:max_chars]
