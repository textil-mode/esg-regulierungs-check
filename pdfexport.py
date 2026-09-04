"""PDF-Export der Analyse-Ergebnisse im textil+mode-Corporate-Design.

Ersetzt den frueheren CSV-Export. Der Informationsumfang ist derselbe
(Status, Nr., Regulierung, Bezeichnung, Gilt ab, Begruendung, greifende
Stelle, Quelle) und zusaetzlich das, was die Ergebniskarten zeigen:
Kopfbereich mit Unternehmen, Erstellungsdatum, Zusammenfassung und
Gesetzesstand je Regulierung.

Warum reportlab
---------------
Die App laeuft in `python:3.12-slim`. reportlab bringt fuer CPython 3.12
fertige Wheels mit und braucht ausser Pillow keine Systembibliotheken --
anders als WeasyPrint, das Cairo und Pango voraussetzt. Gegenueber fpdf2
faellt die Wahl auf reportlab, weil dessen Platypus-Layout Seitenumbrueche
und umbrechende Tabellenzellen selbst erledigt und weil es CJK-Schriften
ohne mitgelieferte Font-Datei ansprechen kann (siehe unten).

Schrift und Zeichensatz
-----------------------
* Latein (de/en/es/fr/it): **Helvetica** -- die PDF-Kernschrift, die jeder
  Betrachter metrisch wie Arial setzt. Sie deckt Windows-1252 ab, also
  saemtliche Umlaute und Akzente dieser fuenf Sprachen. Zeichen ausserhalb
  davon koennte Helvetica nicht darstellen; `_clean()` ersetzt sie deshalb
  durch "?", statt schwarze Kaesten zu drucken.
* Chinesisch (zh): **STSong-Light** ueber reportlabs CID-Mechanismus
  (Adobe-GB1, Encoding UniGB-UCS2-H). Die Schrift wird **nicht eingebettet**
  -- eine eingebettete CJK-Schrift wuerde rund 15 MB in jedes PDF und eine
  Font-Datei von ~120 MB in das Container-Image tragen. Acrobat und die
  meisten Desktop-Betrachter loesen STSong-Light ueber ihr Asian-Font-Pack
  auf. Betrachter ohne dieses Pack (u. a. die PDF-Anzeige mancher Browser)
  zeigen die chinesischen Zeichen unter Umstaenden nicht. Ehrlich benannt
  statt still kaputt: wer chinesische PDFs garantiert braucht, muss eine
  CJK-TTF (z. B. Noto Sans SC) ins Image legen und hier registrieren.
"""
from __future__ import annotations

import io
import os
import re
from datetime import datetime
from functools import partial
from html import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (Flowable, Image, Paragraph,
                                SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from i18n import t
from views import APPLIES_ORDER, I18N, deadline_parts

# --- Farben (textil+mode-CD) ------------------------------------------------
NAVY = colors.HexColor("#0F3750")     # Ueberschriften
LINK = colors.HexColor("#0070C0")     # Hyperlinks
BOX = colors.HexColor("#F2F2F2")      # Kaesten / Tabellenkoepfe
RULE = colors.HexColor("#D9D9D9")     # Trennlinien
MUTED = colors.HexColor("#5A5A5A")    # Fussnoten
BLACK = colors.black
ACCENT_FROM = (0x32, 0xAF, 0xDC)      # Hellblau
ACCENT_TO = (0x78, 0xB9, 0x50)        # Gruen

# Statusfarben spiegeln views.BADGE_STYLES: Gruen/Orange aus dem Logo, die
# Schrift darauf in Dunkelblau (weiss waere zu kontrastarm).
STATUS_COLORS = {
    "ja": (colors.HexColor("#78B950"), NAVY),
    "moeglich": (colors.HexColor("#F59B23"), NAVY),
    "nein": (colors.HexColor("#6B6B6B"), colors.white),
    "error": (colors.HexColor("#A32020"), colors.white),
}

_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "static", "images", "textil-mode-logo.png")
_LOGO_RATIO = 1925 / 437  # Seitenverhaeltnis des Originals, nie verzerren
_LOGO_WIDTH = 46 * mm

_PAGE_W, _PAGE_H = A4
_MARGIN = 20 * mm
_CONTENT_W = _PAGE_W - 2 * _MARGIN
# Breite der Label-Spalte. 38 mm, weil das laengste Label
# ("Anwendungsbeginn") sonst mitten im Wort umbricht.
_LABEL_W = 38 * mm

_CJK_FONT = "STSong-Light"
_cjk_state: bool | None = None


# ---------------------------------------------------------------------------
# Schrift
# ---------------------------------------------------------------------------
def _fonts(language: str) -> tuple[str, str]:
    """(Regular, Bold) fuer diese Sprache.

    STSong-Light kennt keinen fetten Schnitt; dort tragen Ueberschriften die
    Hervorhebung ueber Groesse und Farbe.
    """
    global _cjk_state
    if language == "zh":
        if _cjk_state is None:
            try:
                pdfmetrics.registerFont(UnicodeCIDFont(_CJK_FONT))
                _cjk_state = True
            except Exception:
                _cjk_state = False
        if _cjk_state:
            return _CJK_FONT, _CJK_FONT
    return "Helvetica", "Helvetica-Bold"


def _clean(text: str, font: str) -> str:
    """Whitespace normalisieren und nicht darstellbare Zeichen entschaerfen."""
    s = re.sub(r"\s+", " ", str(text or "")).strip()
    if font.startswith("Helvetica"):
        # Helvetica ist WinAnsi: alles darueber hinaus wuerde als schwarzer
        # Kasten erscheinen. Lieber ein sichtbares "?" als ein kaputtes PDF.
        s = s.encode("cp1252", "replace").decode("cp1252")
    return s


# CJK-Bloecke inkl. Kana, Hangul-Jamo-freier Bereiche und Vollbreiten-Satzzeichen.
_CJK_RE = re.compile(r"[⺀-鿿豈-﫿＀-￯　-〿]+")


def _mk(text: str, font: str, bold: bool = False) -> str:
    """Escaptes Paragraph-Markup.

    In der chinesischen Fassung stehen weiterhin lateinische Passagen im Text:
    Regulierungsnamen, Rechtsakt-Nummern und die woertlichen Zitate aus dem
    deutschen bzw. englischen Gesetzestext. Adobe-GB1 (STSong-Light) traegt
    dafuer keine brauchbaren Umlaut-Glyphen -- aus "Müller & Söhne" wuerde
    "Mü ller & Shne". Deshalb schaltet jeder nicht-chinesische Lauf hier auf
    Helvetica zurueck; die chinesischen Laeufe bleiben auf der CID-Schrift.
    """
    s = _clean(text, font)
    if font != _CJK_FONT:
        return escape(s)
    latin = "Helvetica-Bold" if bold else "Helvetica"

    def _latin(part: str) -> str:
        part = part.encode("cp1252", "replace").decode("cp1252")
        return f'<font name="{latin}">{escape(part)}</font>' if part else ""

    out, pos = [], 0
    for m in _CJK_RE.finditer(s):
        out.append(_latin(s[pos:m.start()]))
        out.append(escape(m.group(0)))
        pos = m.end()
    out.append(_latin(s[pos:]))
    return "".join(out)


def _mk_b(text: str, font: str) -> str:
    """Wie `_mk`, aber fett — soweit die Schrift einen fetten Schnitt hat."""
    if font == _CJK_FONT:
        return _mk(text, font, bold=True)
    return f"<b>{_mk(text, font)}</b>"


# ---------------------------------------------------------------------------
# Schmuckelement: schmale Kante im Verlauf Hellblau -> Gruen
# ---------------------------------------------------------------------------
class AccentRule(Flowable):
    """Einziges Schmuckelement des CD: eine Kante, keine Flaeche."""

    def __init__(self, width: float, height: float = 2.4):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_w, avail_h):
        return (self.width, self.height)

    def draw(self):
        steps = 140
        seg = self.width / steps
        for i in range(steps):
            f = i / (steps - 1)
            r, g, b = (a + (z - a) * f for a, z in zip(ACCENT_FROM, ACCENT_TO))
            self.canv.setFillColorRGB(r / 255, g / 255, b / 255)
            # Ueberlappung von 0.4pt gegen Haarlinien zwischen den Segmenten
            self.canv.rect(i * seg, 0, seg + 0.4, self.height, stroke=0, fill=1)


# ---------------------------------------------------------------------------
# Seitenrahmen
# ---------------------------------------------------------------------------
def _page_furniture(canvas, doc, language: str, font: str) -> None:
    """Fusszeile auf jeder Seite: Hinweis links, Seitenzahl rechts."""
    canvas.saveState()
    y = 14 * mm
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(_MARGIN, y, _PAGE_W - _MARGIN, y)
    canvas.setFont(font, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(_MARGIN, y - 4.2 * mm,
                      _clean(t("disclaimer_short", language), font))
    canvas.drawRightString(_PAGE_W - _MARGIN, y - 4.2 * mm,
                           f"{_clean(t('pdf_page', language), font)} {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Bausteine
# ---------------------------------------------------------------------------
def _styles(language: str, font: str, bold: str) -> dict[str, ParagraphStyle]:
    # Chinesisch kennt keine Wortzwischenraeume: ohne wordWrap="CJK" bliebe
    # eine Zeile ungebrochen stehen und liefe aus der Zelle heraus. Fuer die
    # Quellen-URLs gilt dasselbe (lange Pfade ohne Leerzeichen).
    wrap = "CJK" if language == "zh" else None
    base = dict(fontName=font, fontSize=9.5, leading=13, textColor=BLACK,
                wordWrap=wrap)
    return {
        "title": ParagraphStyle("title", fontName=bold, fontSize=18,
                                leading=22, textColor=NAVY, wordWrap=wrap),
        "meta": ParagraphStyle("meta", **base),
        "meta_strong": ParagraphStyle("meta_strong", **{**base, "fontName": bold,
                                                        "fontSize": 12,
                                                        "leading": 16}),
        "h2": ParagraphStyle("h2", fontName=bold, fontSize=11.5, leading=15,
                             textColor=NAVY, wordWrap=wrap),
        "status": ParagraphStyle("status", fontName=bold, fontSize=8.5,
                                 leading=11, alignment=1, wordWrap=wrap),
        "card_title": ParagraphStyle("card_title", **{**base, "fontSize": 10.5,
                                                     "leading": 14}),
        "label": ParagraphStyle("label", **{**base, "fontName": bold,
                                            "fontSize": 9, "leading": 12,
                                            "textColor": NAVY}),
        "body": ParagraphStyle("body", **base),
        "quote": ParagraphStyle("quote", **{**base, "textColor":
                                            colors.HexColor("#333333")}),
        "url": ParagraphStyle("url", **{**base, "fontSize": 8.5, "leading": 11,
                                        "wordWrap": "CJK"}),
        "num": ParagraphStyle("num", fontName=bold, fontSize=20, leading=24,
                              alignment=1, wordWrap=wrap),
        "num_label": ParagraphStyle("num_label", fontName=font, fontSize=8.5,
                                    leading=11, alignment=1, textColor=BLACK,
                                    wordWrap=wrap),
    }


def _header_story(company: str, created: str, language: str, font: str,
                  bold: str, st: dict) -> list:
    """Logo oben links, Titel, Verlaufskante, Unternehmen und Datum."""
    story: list = []
    if os.path.exists(_LOGO_PATH):
        logo = Image(_LOGO_PATH, width=_LOGO_WIDTH,
                     height=_LOGO_WIDTH / _LOGO_RATIO)
        logo.hAlign = "LEFT"
        story.append(logo)
        story.append(Spacer(1, 7 * mm))
    story.append(Paragraph(_mk(t("app_title", language), font, bold=True),
                           st["title"]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(AccentRule(_CONTENT_W))
    story.append(Spacer(1, 6 * mm))
    if company:
        story.append(Paragraph(_mk(company, font, bold=True), st["meta_strong"]))
        story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph(
        f'{_mk(t("pdf_created", language), font)}: {_mk(created, font)}',
        st["meta"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(_mk(t("pdf_disclaimer", language), font),
                           st["meta"]))
    story.append(Spacer(1, 6 * mm))
    return story


def _summary_story(shown: list[dict], language: str, font: str, st: dict,
                   lang_dict: dict) -> list:
    counts = [(r.get("applies") or "").lower() for r in shown]
    cells = []
    for key, label_key in (("ja", "metric_yes"), ("moeglich", "metric_maybe"),
                           ("nein", "metric_no")):
        n = sum(1 for a in counts if a == key)
        colour = STATUS_COLORS[key][0]
        num = ParagraphStyle(f"num_{key}", parent=st["num"], textColor=colour)
        cells.append([Paragraph(_mk(str(n), font, bold=True), num),
                      Paragraph(_mk(lang_dict[label_key], font),
                                st["num_label"])])
    col = _CONTENT_W / 3
    box = Table([[Table([[num], [lbl]], colWidths=[col - 6])
                  for num, lbl in cells]], colWidths=[col, col, col])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BOX),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return [Paragraph(_mk(t("pdf_summary", language), font, bold=True), st["h2"]),
            Spacer(1, 2 * mm), box, Spacer(1, 8 * mm)]


def _row(label: str, flowable, st: dict, font: str) -> list:
    return [Paragraph(_mk(label, font, bold=True), st["label"]), flowable]


def _reg_story(r: dict, language: str, font: str, st: dict, lang_dict: dict,
               profile: dict | None) -> list:
    applies = (r.get("applies") or "").lower()
    bg, fg = STATUS_COLORS.get(applies, STATUS_COLORS["nein"])
    label = lang_dict["applies_label"].get(applies, applies.upper())

    status_style = ParagraphStyle("st_x", parent=st["status"], textColor=fg)
    status_cell = Paragraph(_mk(label, font, bold=True), status_style)

    name = _mk(r.get("name") or "", font)
    full = _mk(r.get("full_name") or "", font)
    url = (r.get("url") or "").strip()
    title = (_mk_b(f'{t("col_regulation", language)} {r.get("nr", "")}', font)
             + ": ")
    title += (f'<a href="{escape(url, quote=True)}" color="#0070C0">{name}</a>'
              if url else name)
    if full and full != name:
        title += f" &mdash; {full}"
    rows = [[status_cell, Paragraph(title, st["card_title"])]]
    styles = [
        # Kopfzeile
        ("BACKGROUND", (0, 0), (0, 0), bg),
        ("BACKGROUND", (1, 0), (1, 0), BOX),
        ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, 0), 5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        # Angaben
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 3),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
    ]

    parts = deadline_parts(r.get("key") or "", applies, profile, language)
    if parts:
        label, value, note = parts
        text = _mk(value, font)
        if note:
            text += f'<br/><font size="8" color="#5A5A5A">{_mk(note, font)}</font>'
        rows.append(_row(label, Paragraph(text, st["body"]), st, font))
    reason = r.get("reason") or lang_dict["reason_missing"]
    rows.append(_row(lang_dict["reason"],
                     Paragraph(_mk(reason, font), st["body"]), st, font))
    passage = _clean(r.get("passage") or "", font)
    if passage:
        rows.append(_row(lang_dict["passage"],
                         Paragraph(f'<i>{_mk(passage, font)}</i>', st["quote"]),
                         st, font))
    if url:
        rows.append(_row(t("pdf_source", language),
                         Paragraph(f'<a href="{escape(url, quote=True)}" '
                                   f'color="#0070C0">{_mk(url, font)}</a>',
                                   st["url"]), st, font))
    as_of = _iso_date(r.get("law_as_of") or "")
    if as_of:
        rows.append(_row(t("law_state_of", language),
                         Paragraph(_mk(as_of, font), st["url"]), st, font))

    # Kopf und Angaben in EINER Tabelle: so darf ein langer Block umbrechen,
    # statt eine halbleere Seite zu erzwingen. `repeatRows=1` wiederholt dann
    # die Statuszeile oben auf der Folgeseite, damit die Angaben zuordenbar
    # bleiben.
    block = Table(rows, colWidths=[_LABEL_W, _CONTENT_W - _LABEL_W], repeatRows=1)
    block.setStyle(TableStyle(styles))
    return [block, Spacer(1, 5 * mm)]


def _iso_date(value: str) -> str:
    """'2026-09-01T10:11:12' -> '01.09.2026'."""
    v = (value or "")[:10]
    parts = v.split("-")
    if len(parts) == 3 and all(parts):
        return f"{parts[2]}.{parts[1]}.{parts[0]}"
    return v


# ---------------------------------------------------------------------------
# Einstieg
# ---------------------------------------------------------------------------
def render_pdf(results: list[dict], language: str = "de",
               profile: dict | None = None,
               created_at: str | None = None) -> bytes:
    """Erzeugt das Ergebnis-PDF als Bytes.

    `results` ist das gespeicherte Analyse-Ergebnis, `profile` das
    Unternehmensprofil (liefert Name und die unternehmensindividuelle Frist).
    """
    font, bold = _fonts(language)
    st = _styles(language, font, bold)
    lang_dict = I18N.get(language, I18N["de"])

    shown = [r for r in results
             if (r.get("applies") or "").lower() in APPLIES_ORDER]
    shown.sort(key=lambda r: (APPLIES_ORDER.get((r.get("applies") or "").lower(), 9),
                              r.get("nr", 0)))

    company = (profile or {}).get("name") or ""
    created = _iso_date(created_at) if created_at else f"{datetime.now():%d.%m.%Y}"

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=_MARGIN, rightMargin=_MARGIN,
        topMargin=18 * mm, bottomMargin=24 * mm,
        title=_clean(f'{t("app_title", language)} {company}'.strip(), font),
        author="textil+mode", subject=_clean(t("app_subtitle", language), font),
    )

    story = _header_story(company, created, language, font, bold, st)
    story += _summary_story(shown, language, font, st, lang_dict)
    for r in shown:
        story += _reg_story(r, language, font, st, lang_dict, profile)

    draw = partial(_page_furniture, language=language, font=font)
    doc.build(story, onFirstPage=draw, onLaterPages=draw)
    return buf.getvalue()
