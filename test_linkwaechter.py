"""Tests zur woechentlichen Linkpruefung (linkwaechter.py, 12.10.2026).

Ausfuehren:  ./.venv/Scripts/python.exe test_linkwaechter.py

Kein Netz, kein LLM, kein Mailversand: Abruf, KI-Suche und Versand sind
Attrappen. Eigene DB `data/esg_linkwaechter_test.db`.

Bloecke:
  A  gesetze-im-internet.de: neues Kuerzel aus der Teilliste (Fall MPBetreibV)
  B  KI-Suche: Kandidaten werden gegengeprueft, Unpassendes faellt raus
  C  Lauf: speichern, Mail nur bei Defekt, einmal Entwarnung, nie doppelt
  D  Mailtext und Admin-Seite
  E  Einstufung: gesperrt / voruebergehend / echter Fehler (keine Fehlalarme)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_linkwaechter_test.db"
os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["ASSISTENT_WARMUP"] = "0"
os.environ["PUBLIC_BASE_URL"] = "https://test.example"
os.environ["LINKCHECK_KI"] = "1"
os.environ["LINKCHECK_RETRY_SEC"] = "0"      # Wiederholung ohne Wartezeit
if TEST_DB.exists():
    TEST_DB.unlink()

import db  # noqa: E402
import linkwaechter as lw  # noqa: E402
from check_links import Result  # noqa: E402

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


# --- Attrappen --------------------------------------------------------------
class Antwort:
    def __init__(self, url: str, text: str = "", status: int = 200):
        self.url, self.text, self.status_code = url, text, status
        self.content = text.encode("iso-8859-1", errors="replace")


class Client:
    """Antwortet aus einem Woerterbuch {url: text}; alles andere 404."""
    def __init__(self, seiten: dict[str, str], weiter: dict[str, str] | None = None):
        self.seiten, self.weiter, self.abrufe = seiten, weiter or {}, []

    def get(self, url, headers=None, follow_redirects=True):
        self.abrufe.append(url)
        ziel = self.weiter.get(url, url)
        return Antwort(ziel, self.seiten.get(ziel, ""), 200 if ziel in self.seiten else 404)


def pruefer_aus(ok: set[str], kaputt: dict[str, str] | None = None):
    kaputt = kaputt or {}

    def pruefer(url, where, label, client):
        if url in ok:
            return Result(url, where, label, "OK", 200, url, "text/html", 5000)
        return Result(url, where, label, "BROKEN", 404, url, "text/html", 100,
                      kaputt.get(url, "HTTP 404"))
    return pruefer


TEILLISTE = ('<p><a href="./mpav/index.html">MPAV</a></p>'
             '<p><a href="./mpbetreibv_2025/index.html">MPBetreibV</a></p>'
             '<p><a href="./mpbetreibvx/index.html">andere Vorschrift</a></p>'
             '<p><a href="./mpdg/index.html">MPDG</a></p>')


# ---------------------------------------------------------------------------
def block_a() -> None:
    print("\n--- A  gesetze-im-internet.de ---")
    k = lw._gii_kandidaten_kuerzel
    check("A mpbetreibv -> mpbetreibv_2025", k("mpbetreibv", TEILLISTE) == ["mpbetreibv_2025"])
    check("A aehnliches Kuerzel (mpbetreibvx) ist kein Nachfolger",
          "mpbetreibvx" not in k("mpbetreibv", TEILLISTE))
    liste_2031 = TEILLISTE + '<a href="./mpbetreibv_2031/index.html">'
    check("A juengste Neufassung zuerst",
          k("mpbetreibv", liste_2031) == ["mpbetreibv_2031", "mpbetreibv_2025"])
    check("A nie zurueck auf eine aeltere Fassung",
          k("mpbetreibv_2031", liste_2031 + '<a href="./mpbetreibv/index.html">') == [])

    gii = lw.GII
    index = '<a href="BJNR0260B0025.html">Volltext</a> <a href="BJNR0260B0025.html#x">x</a>'
    client = Client({f"{gii}Teilliste_M.html": TEILLISTE, f"{gii}mpbetreibv_2025/index.html": index})
    ziel = f"{gii}mpbetreibv_2025/BJNR0260B0025.html"
    v = lw.gii_ersatz(f"{gii}mpbetreibv/BJNR176200998.html", client, pruefer_aus({ziel}))
    check("A Volltext unter dem neuen Kuerzel vorgeschlagen", [s["url"] for s in v] == [ziel], str(v))
    # Einzelnorm: zuerst dieselbe Datei unter dem neuen Kuerzel
    einzel = f"{gii}mpbetreibv_2025/__8.html"
    v = lw.gii_ersatz(f"{gii}mpbetreibv/__8.html", client, pruefer_aus({einzel, ziel}))
    check("A Einzelnorm bleibt Einzelnorm", v and v[0]["url"] == einzel, str(v))
    check("A fremde Domain: kein Vorschlag", lw.gii_ersatz("https://example.org/x", client) == [])


# ---------------------------------------------------------------------------
def block_b() -> None:
    print("\n--- B  KI-Suche ---")
    alt = "https://www.bfarm.de/alt/_node.html"
    gut = "https://www.bfarm.de/DE/Medizinprodukte/Vorkommnis-melden/_node.html"
    falsch = "https://www.bfarm.de/DE/Presse/_node.html"
    tot = "https://www.bfarm.de/gibts-nicht.html"
    umweg = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/abc"
    label = "BfArM – Vorkommnis melden: Hersteller und Bevollmächtigte"
    client = Client({gut: "Vorkommnis melden – Hinweise für Hersteller und Bevollmächtigte (BfArM)",
                     falsch: "Pressemitteilungen des BfArM"},
                    weiter={umweg: gut})

    def suche(l, u):
        return f"{tot}\n{falsch}\n{alt}", [umweg]

    v = lw.ki_ersatz(alt, label, client, pruefer_aus({gut, falsch}), suche)
    urls = [s["url"] for s in v]
    check("B toter Kandidat und die alte Adresse fallen raus", tot not in urls and alt not in urls)
    check("B Weiterleitung der Google-Suche aufgeloest, passender Inhalt zuerst",
          urls and urls[0] == gut and "passt" in v[0]["note"], str(v))
    check("B unpassender Inhalt nur mit Pruefhinweis",
          all("prüfen" in s["note"] for s in v if s["url"] == falsch))
    os.environ["LINKCHECK_KI"] = "0"
    try:
        check("B LINKCHECK_KI=0 schaltet die KI-Suche ab", lw._gemini_suche(label, alt) == ("", []))
    finally:
        os.environ["LINKCHECK_KI"] = "1"


# ---------------------------------------------------------------------------
def block_c() -> None:
    print("\n--- C  Lauf, Speicherung, Mail ---")
    gesendet: list[tuple[str, str, str]] = []

    def versand(an, betreff, text):
        gesendet.append((an, betreff, text))

    a, b = "https://example.org/a", "https://example.org/b"
    neu = "https://example.org/b-neu"
    items = [(a, "GUIDELINES[MPDG]", "Leitlinie A"), (b, "REGULATIONS[MPDG].url", "MPDG")]

    def suche(l, u):
        return (neu, []) if u == b else ("", [])

    # 1: alles gut, kein Vorlauf -> keine Mail
    r = lw.lauf(items, pruefer_aus({a, b}), suche, versand)
    check("C alles erreichbar: keine Mail", not gesendet and not r["broken"])
    check("C Lauf gespeichert", db.latest_link_check()["checked"] == 2)

    # 2: b defekt -> Mail mit Vorschlag
    r = lw.lauf(items, pruefer_aus({a, neu}), suche, versand)
    check("C defekt: genau eine Mail an den Admin", len(gesendet) == 1
          and gesendet[0][0] == "mschuckert@textil-mode.de", str([g[:2] for g in gesendet]))
    check("C Vorschlag gefunden und gespeichert",
          db.latest_link_check()["broken"][0]["suggestions"][0]["url"] == neu)
    check("C Mail nennt Fundort, alte Adresse und Vorschlag",
          all(x in gesendet[0][2] for x in ("MPDG – Link in Liste und Karte", b, neu)))

    # 3: noch defekt -> wieder eine Mail (woechentliche Erinnerung)
    lw.lauf(items, pruefer_aus({a}), suche, versand)
    check("C weiterhin defekt: erneute Mail", len(gesendet) == 2)
    check("C ohne Vorschlag: Hinweis auf Handsuche", "keine Ersatzadresse gefunden" in gesendet[1][2])

    # 4: repariert -> eine Entwarnung, danach Ruhe
    lw.lauf(items, pruefer_aus({a, b}), suche, versand)
    check("C Entwarnung nach Reparatur", len(gesendet) == 3 and "wieder erreichbar" in gesendet[2][1])
    lw.lauf(items, pruefer_aus({a, b}), suche, versand)
    check("C danach keine weitere Mail", len(gesendet) == 3)

    # --probe speichert nicht
    vorher = db.latest_link_check()["id"]
    lw.lauf(items, pruefer_aus({a}), suche, versand, speichern=False)
    check("C Probe speichert nichts und mailt nicht",
          db.latest_link_check()["id"] == vorher and len(gesendet) == 3)

    # Weiterleitungen: nur wesentliche
    def r_(url, final):
        return Result(url, "", "", "OK", 200, final, None, 5000)
    check("C http->https und / am Ende zaehlen nicht",
          not lw._wesentlich_weitergeleitet(r_("http://x.de/a/", "https://www.x.de/a")))
    check("C neuer Pfad zaehlt", lw._wesentlich_weitergeleitet(r_("https://x.de/a", "https://x.de/b")))


# ---------------------------------------------------------------------------
def block_d() -> None:
    print("\n--- D  Admin-Seite ---")
    import app as flaskapp
    uid = db.create_user("admin2@example.org", "ein-gutes-Passwort-2026")
    db.set_admin(uid, True)
    db.save_link_check("2026-10-12T03:45:00", 120,
                       [{"where": "GUIDELINES[MPDG]", "label": "X", "url": "https://example.org/tot",
                         "note": "HTTP 404", "http_status": 404,
                         "suggestions": [{"url": "https://example.org/neu", "source": "KI-Suche",
                                          "note": "erreichbar, Inhalt passt zum Titel"}]}],
                       [], [{"where": "GUIDELINES[MDR]", "label": "Y", "url": "https://a.example/1",
                             "final_url": "https://a.example/2"}])
    c = flaskapp.app.test_client()
    with c.session_transaction() as sess:
        sess["user_id"] = uid
        sess["ui_language"] = "de"
    html = c.get("/admin/regulierungs-status").get_data(as_text=True)
    check("D Abschnitt Linkpruefung sichtbar", "Letzte Linkprüfung" in html and "120 Links geprüft" in html)
    check("D defekter Link mit Vorschlag", "https://example.org/tot" in html and "https://example.org/neu" in html)
    check("D Weiterleitung aufklappbar", "https://a.example/2" in html)
    check("D Link in der Mail zeigt auf die Admin-Seite",
          lw._admin_link() == "https://test.example/esg/admin/regulierungs-status")


def block_e() -> None:
    print("\n--- E  Einstufung ---")
    gesendet: list = []

    def versand(an, betreff, text):
        gesendet.append(betreff)

    echa, bmg, tot = ("https://echa.example/scip", "https://bmg.example/mp",
                      "https://amt.example/weg")
    items = [(echa, "GUIDELINES[SCIP]", "ECHA"), (bmg, "GUIDELINES[MPBetreibV]", "BMG"),
             (tot, "GUIDELINES[MPDG]", "Amt")]
    aufrufe: dict[str, int] = {}

    def pruefer_mit(bmg_status: list):
        """ECHA 403 immer, `tot` 404 immer, BMG nacheinander die angegebenen Status."""
        aufrufe.clear()

        def pruefer(url, where, label, client):
            n = aufrufe.get(url, 0)
            aufrufe[url] = n + 1
            if url == echa:
                return Result(url, where, label, "BROKEN", 403, url, None, 100, "HTTP 403")
            if url == tot:
                return Result(url, where, label, "BROKEN", 404, url, None, 100, "HTTP 404")
            st = bmg_status[min(n, len(bmg_status) - 1)]
            if st == 200:
                return Result(url, where, label, "OK", 200, url, None, 5000)
            return Result(url, where, label, "BROKEN", st, url, None, 0,
                          "Verbindungsfehler" if st is None else f"HTTP {st}")
        return pruefer

    def keine_suche(label, url):
        return "", []

    # Woche 1: BMG 504, beim zweiten Versuch wieder da
    r = lw.lauf(items, pruefer_mit([504, 200]), keine_suche, versand)
    check("E 403 (Bot-Schutz) ist unklar, nicht defekt",
          echa not in [b["url"] for b in r["broken"]]
          and any(u["url"] == echa and u["kind"] == lw.GESPERRT for u in r["unknown"]))
    check("E kurze Stoerung: zweiter Versuch, dann gar nicht gemeldet",
          aufrufe.get(bmg) == 2 and bmg not in [x["url"] for x in r["broken"] + r["unknown"]])
    check("E echter 404 bleibt defekt -> Mail", [b["url"] for b in r["broken"]] == [tot]
          and len(gesendet) == 1)

    # Woche 2: BMG dauerhaft 504 -> erst unklar
    r = lw.lauf(items, pruefer_mit([504]), keine_suche, versand)
    check("E Stoerung in der ersten Woche: unklar, nicht defekt",
          any(u["url"] == bmg and u["kind"] == lw.VORUEBERGEHEND for u in r["unknown"])
          and bmg not in [b["url"] for b in r["broken"]])
    # Woche 3: immer noch nicht erreichbar -> defekt
    r = lw.lauf(items, pruefer_mit([None]), keine_suche, versand)
    eintrag = next((b for b in r["broken"] if b["url"] == bmg), None)
    check("E zwei Wochen in Folge nicht erreichbar: defekt",
          eintrag is not None and "seit mindestens einer Woche" in eintrag["note"], str(r["broken"]))


if __name__ == "__main__":
    for block in (block_a, block_b, block_c, block_d, block_e):
        block()
    print()
    if _failures:
        print(f"{len(_failures)} FEHLER:")
        for f in _failures:
            print("  -", f)
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
