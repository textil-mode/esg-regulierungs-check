"""Pflichten-Plan: KI-Vorschlaege und Uebersetzungen.

Platzhalter aus Aufgabe 5: `uebersetzen` kopiert die deutschen Texte in alle
anderen Sprachen, damit die Handpflege schon einen vollstaendigen Vorschlag
erzeugt. Aufgabe 6 ersetzt den Rumpf durch die KI-Uebersetzung (Signatur
bleibt). Sichtbar wird ohnehin nichts ohne Freigabe; der Admin sieht alle
sechs Fassungen auf der Vorschlagsseite und kann sie dort korrigieren.
"""
from __future__ import annotations

ZIELSPRACHEN = ("en", "es", "fr", "it", "zh")


class VorschlagFehler(Exception):
    """Unbrauchbare KI-Antwort (Aufgabe 6)."""


async def uebersetzen(texte_de: dict, ask=None) -> dict[str, dict]:
    """`{"titel","beschreibung","daten"}` -> `{lang: {...}}` fuer en, es, fr, it, zh."""
    return {lang: {f: texte_de.get(f, "") for f in ("titel", "beschreibung", "daten")}
            for lang in ZIELSPRACHEN}
