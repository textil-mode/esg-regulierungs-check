"""HTML-Generierung für Regulierungskarten + CSV-Export.

Kein Streamlit mehr — reines HTML/CSS für Flask-Templates.
"""
from __future__ import annotations

import csv
import io
import re
from html import escape

from i18n import t

APPLIES_ORDER = {"error": 0, "ja": 1, "moeglich": 2, "nein": 3}

I18N = {
    "de": {
        "metric_yes": "Greift",
        "metric_maybe": "Möglich / zu prüfen",
        "metric_no": "Nicht einschlägig",
        "applies_label": {"ja": "GREIFT", "moeglich": "MÖGLICH", "nein": "NICHT EINSCHLÄGIG", "error": "FEHLER"},
        "reason": "Begründung",
        "reason_missing": "Keine Begründung verfügbar.",
        "passage": "Greifende Stelle",
    },
    "en": {
        "metric_yes": "Applies",
        "metric_maybe": "Possible / to verify",
        "metric_no": "Not applicable",
        "applies_label": {"ja": "APPLIES", "moeglich": "POSSIBLE", "nein": "NOT APPLICABLE", "error": "ERROR"},
        "reason": "Reason",
        "reason_missing": "No justification available.",
        "passage": "Triggering passage",
    },
    "es": {
        "metric_yes": "Aplica",
        "metric_maybe": "Posible / a verificar",
        "metric_no": "No aplicable",
        "applies_label": {"ja": "APLICA", "moeglich": "POSIBLE", "nein": "NO APLICABLE", "error": "ERROR"},
        "reason": "Justificación",
        "reason_missing": "Sin justificación disponible.",
        "passage": "Pasaje relevante",
    },
    "fr": {
        "metric_yes": "S'applique",
        "metric_maybe": "Possible / à vérifier",
        "metric_no": "Non applicable",
        "applies_label": {"ja": "S'APPLIQUE", "moeglich": "POSSIBLE", "nein": "NON APPLICABLE", "error": "ERREUR"},
        "reason": "Justification",
        "reason_missing": "Aucune justification disponible.",
        "passage": "Passage pertinent",
    },
    "it": {
        "metric_yes": "Si applica",
        "metric_maybe": "Possibile / da verificare",
        "metric_no": "Non applicabile",
        "applies_label": {"ja": "SI APPLICA", "moeglich": "POSSIBILE", "nein": "NON APPLICABILE", "error": "ERRORE"},
        "reason": "Motivazione",
        "reason_missing": "Nessuna motivazione disponibile.",
        "passage": "Passaggio rilevante",
    },
    "zh": {
        "metric_yes": "适用",
        "metric_maybe": "可能 / 需核实",
        "metric_no": "不适用",
        "applies_label": {"ja": "适用", "moeglich": "可能", "nein": "不适用", "error": "错误"},
        "reason": "理由",
        "reason_missing": "暂无理由说明。",
        "passage": "相关条款",
    },
}

# textil+mode-CD: Gruen/Orange stammen aus dem Logo und sind hier bewusst
# punktuell als Statusfarbe eingesetzt. Die Schrift steht darauf in Dunkelblau
# (weiss waere auf #78B950 bzw. #F59B23 zu kontrastarm).
BADGE_STYLES = {
    "ja": ("background:#78B950;color:#0F3750;", "✓"),
    "moeglich": ("background:#F59B23;color:#0F3750;", "?"),
    "nein": ("background:#6b6b6b;color:#ffffff;", "—"),
    "error": ("background:#A32020;color:#ffffff;", "✕"),
}


_PASSAGE_MAX_CHARS = 280

# Kennzahlen (Zahl + Einheit/Groessenwort) im Zitat leicht rot hervorheben.
# Bewusst NUR Zahlen mit Signalwort (€, %, Mio., Beschaeftigte, …), damit
# Artikel-/Paragraphen-Nummern (Art. 19a, § 267) NICHT markiert werden.
_KENNZAHL_RE = re.compile(
    r"(?:€|Euro|EUR)\s?\d[\d .,]*\d?"
    r"(?:\s*(?:Mio\.?|Mrd\.?|Millionen|Milliarden|millions?|billions?))?"
    r"|\d[\d .,]*\d?\s*"
    r"(?:Mio\.?|Mrd\.?|Millionen|Milliarden|millions?|billions?)?\s*"
    r"(?:€|Euro|EUR|%|Prozent|percent"
    r"|Besch[aä]ftigte\w*|Mitarbeiter\w*|Mitarbeitende\w*|Arbeitnehmer\w*"
    r"|employees?|workers?|Personen)"
    r"|\d[\d .,]*\d\s*(?:Mio\.?|Mrd\.?|Millionen|Milliarden|millions?|billions?)",
    re.IGNORECASE,
)


def _highlight_kennzahlen(escaped_text: str) -> str:
    """Markiert Kennzahlen (Schwellenwerte) in bereits HTML-escaptem Text."""
    return _KENNZAHL_RE.sub(
        lambda m: f'<span class="kennzahl">{m.group(0)}</span>', escaped_text
    )


def _shorten_passage(text: str) -> str:
    """Kurzform fuer das 'Greifende Stelle'-Feld.

    Manche Modelle liefern ganze Paragraphen-Listen statt einem kurzen Zitat.
    Wir nehmen den ersten Satz oder die ersten 280 Zeichen; der Rest wird
    mit … abgeschnitten.
    """
    t = (text or "").strip()
    if not t:
        return ""
    # Zeilenumbrueche und Aufzaehlungspunkte entfernen
    t = re.sub(r"\s*[\r\n]+\s*[-*•]?\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    if len(t) <= _PASSAGE_MAX_CHARS:
        return t
    cut = t[:_PASSAGE_MAX_CHARS]
    # Wenn moeglich nach Satzende kappen
    dot = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if dot > _PASSAGE_MAX_CHARS // 2:
        return cut[:dot + 1].rstrip() + " …"
    return cut.rstrip() + " …"


def _iso_to_display(value: str) -> str:
    """'2026-09-01T10:11:12' → '01.09.2026'; unbekanntes Format unveraendert."""
    v = (value or "")[:10]
    parts = v.split("-")
    if len(parts) == 3 and all(parts):
        return f"{parts[2]}.{parts[1]}.{parts[0]}"
    return v


def _card_html(r: dict, lang_dict: dict, language: str = "de") -> str:
    a = r["applies"]
    bg, icon = BADGE_STYLES.get(a, ("background:#6b6b6b;color:#ffffff;", "·"))
    label = lang_dict["applies_label"].get(a, a.upper())
    name = escape(r["name"])
    full = escape(r["full_name"])
    url = escape(r["url"])
    # `article` (statisches key_article) wird NICHT mehr vorangestellt: die
    # Begruendungstexte tragen die Fundstelle seit Prompt v5 selbst, und zwar
    # die tatsaechlich zitierte Stelle statt der pauschalen ("Art. 1, 3").
    # Doppelnennungen wie "Art. 2 (Anwendungsbereich): Art. 2(1): …" entfielen
    # damit, und die 280-Zeichen-Kappung greift wieder auf den ganzen Text.
    passage = _highlight_kennzahlen(escape(_shorten_passage(r.get("passage") or "")))
    reason_raw = (r.get("reason") or "").strip()
    reason = escape(reason_raw) if reason_raw else f'<em style="color:#5A5A5A;">{escape(lang_dict["reason_missing"])}</em>'
    nr = r.get("nr", "")
    as_of = _iso_to_display(r.get("law_as_of") or "")
    as_of_html = (
        f'\n  <div class="reg-asof">{escape(t("law_state_of", language))} {escape(as_of)}</div>'
        if as_of else ""
    )
    return f"""
<div class="reg-card">
  <div class="reg-card-header">
    <span class="badge" style="{bg}">{icon} {label}</span>
    <span class="reg-nr">Nr. {nr}</span>
    <a href="{url}" target="_blank" rel="noopener" class="reg-name">{name}</a>
    <span class="reg-full">— {full}</span>
  </div>
  <div class="reg-reason"><strong>{escape(lang_dict['reason'])}:</strong> {reason}</div>
  <div class="reg-passage"><strong>{escape(lang_dict['passage'])}:</strong> <em>{passage}</em></div>{as_of_html}
</div>"""


def _metrics_html(shown: list[dict], lang_dict: dict) -> str:
    yes = sum(1 for r in shown if r["applies"] == "ja")
    maybe = sum(1 for r in shown if r["applies"] == "moeglich")
    no = sum(1 for r in shown if r["applies"] == "nein")
    return f"""
<div class="metrics">
  <div class="metric metric-yes"><div class="metric-value">{yes}</div><div class="metric-label">{escape(lang_dict['metric_yes'])}</div></div>
  <div class="metric metric-maybe"><div class="metric-value">{maybe}</div><div class="metric-label">{escape(lang_dict['metric_maybe'])}</div></div>
  <div class="metric metric-no"><div class="metric-value">{no}</div><div class="metric-label">{escape(lang_dict['metric_no'])}</div></div>
</div>"""


def render_cards_html(results: list[dict], language: str = "de") -> str:
    """Generiert das komplette Ergebnis-HTML (Metriken + Karten)."""
    lang_dict = I18N.get(language, I18N["de"])
    shown = [r for r in results if (r.get("applies") or "").lower() in APPLIES_ORDER]
    shown.sort(key=lambda r: (APPLIES_ORDER.get((r.get("applies") or "").lower(), 9), r["nr"]))

    if not shown:
        return '<p class="no-results">—</p>'

    parts = [_metrics_html(shown, lang_dict)]
    parts.extend(_card_html(r, lang_dict, language) for r in shown)
    return "\n".join(parts)


def render_csv(results: list[dict], language: str = "de") -> bytes:
    """Generiert CSV als UTF-8-BOM-Bytes."""
    lang_dict = I18N.get(language, I18N["de"])
    shown = [r for r in results if (r.get("applies") or "").lower() in APPLIES_ORDER]
    shown.sort(key=lambda r: (APPLIES_ORDER.get((r.get("applies") or "").lower(), 9), r["nr"]))

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Status", "Nr.", "Regulierung", "Bezeichnung",
                     lang_dict["reason"], lang_dict["passage"], "URL"])
    for r in shown:
        writer.writerow([
            lang_dict["applies_label"].get(r["applies"], r["applies"].upper()),
            r["nr"],
            r["name"],
            r["full_name"],
            r.get("reason", ""),
            r.get("passage", ""),
            r["url"],
        ])
    return ("\ufeff" + buf.getvalue()).encode("utf-8")
