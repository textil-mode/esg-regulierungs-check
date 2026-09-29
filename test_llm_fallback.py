"""Tests zum Ausweichen bei Lastspitzen des Modells (Stand 28.09.2026).

Ausfuehren:  ./.venv/Scripts/python.exe test_llm_fallback.py

Kein Netz, kein LLM, kein API-Key: der Google-Aufruf wird durch eine Attrappe
von `httpx.AsyncClient` ersetzt, `_analyze_one` bekommt einen Schein-Client.
Die Produktiv-DB `data/esg.db` wird nur gelesen (Gesetzestexte fuer Block C).

Anlass: Google meldete ueber Minuten `503 high demand` fuer gemini-3.1-flash-lite.
NFRD scheiterte nach sechs Versuchen, die Fortschrittsanzeige stand dabei auf
"EmpCo 15/16", und die rote Fehlerkarte zeigte die Anfrage-Adresse samt
API-Schluessel.

Bloecke:
  A  _analyze_one: Modellwechsel reihum, Markierung, Schluessel nie im Fehlertext
  B  LLMClient.ask (google): Schluessel im Kopf, Denkmodus nur beim Ausweichmodell
  C  app._run_analysis_bg: Ausweich-Ergebnis nicht im Cache, "waiting" nennt Offenes
"""
from __future__ import annotations

import asyncio
import os
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).parent
TEST_DB = BASE / "data" / "esg_fallback_test.db"
SOURCE_DB = BASE / "data" / "esg.db"

os.environ["ESG_DB_PATH"] = str(TEST_DB)
os.environ["LLM_PROVIDER"] = "google"
# Ausdruecklich setzen statt entfernen: app.py laedt die lokale .env, und die
# fuellt fehlende Variablen auf (mit echtem Schluessel und anderem Modell).
os.environ["OPENAI_API_KEY"] = "AQtest-geheim-123"
os.environ["GOOGLE_API_KEY"] = "AQtest-geheim-123"
os.environ["OPENAI_MODEL"] = "haupt-modell"
os.environ["GOOGLE_MODEL"] = "haupt-modell"
os.environ["GOOGLE_FALLBACK_MODELS"] = "ausweich-a,ausweich-b"

if TEST_DB.exists():
    TEST_DB.unlink()

import httpx  # noqa: E402

import db  # noqa: E402
import fetcher  # noqa: E402
import llm  # noqa: E402
import app as esg_app  # noqa: E402
from regulations import REGULATIONS  # noqa: E402

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


# Wartezeiten der Wiederholungen nicht absitzen, aber mitschreiben.
_sleeps: list[float] = []
_real_sleep = asyncio.sleep


async def _fast_sleep(sec: float, *a, **kw):
    _sleeps.append(sec)
    await _real_sleep(0)

asyncio.sleep = _fast_sleep

REG = next(r for r in REGULATIONS if llm.deterministic_result(r, {}, "de") is None)
OK_JSON = '{"applies": "nein", "reason": "Trifft nicht zu.", "passage": "-"}'
ERR_503 = ("Server error '503 Service Unavailable' for url "
           "'https://generativelanguage.googleapis.com/v1beta/models/x:generateContent?key=AQleak999'")


class FakeClient:
    """Antwortet je Modell nach Drehbuch: Liste von 'ok' / Fehlertext."""

    def __init__(self, script: dict[str, list[str]], models: list[str | None]):
        self.script = {m: list(v) for m, v in script.items()}
        self._models = models
        self.calls: list[str | None] = []

    def models(self):
        return self._models

    async def ask(self, system, user, max_tokens=1500, json_mode=True, model=None):
        self.calls.append(model)
        step = self.script.get(model, ["ok"]).pop(0) if self.script.get(model) else "ok"
        if step == "ok":
            return OK_JSON
        raise RuntimeError(step)


def run_one(client) -> dict:
    return asyncio.run(llm._analyze_one(client, REG, "Volltext", "de", {}))


# ---------------------------------------------------------------------------
def block_a() -> None:
    print("\n--- A  _analyze_one ---")
    m = ["haupt-modell", "ausweich-a", "ausweich-b"]

    c = FakeClient({"haupt-modell": [ERR_503, ERR_503]}, m)
    r = run_one(c)
    check("A1 zwei 503 beim Hauptmodell -> Ausweichmodell a liefert",
          r.get("applies") == "nein" and r.get("_fallback_model") == "ausweich-a",
          f"calls={c.calls} fallback={r.get('_fallback_model')}")
    check("A1 erster Fehlschlag bleibt beim Hauptmodell",
          c.calls == ["haupt-modell", "haupt-modell", "ausweich-a"], str(c.calls))

    c = FakeClient({"haupt-modell": [ERR_503]}, m)
    r = run_one(c)
    check("A2 ein 503, dann Hauptmodell ok -> keine Markierung",
          r.get("applies") == "nein" and "_fallback_model" not in r, str(c.calls))

    _sleeps.clear()
    c = FakeClient({"haupt-modell": [ERR_503, ERR_503, "ok"],
                    "ausweich-a": [ERR_503], "ausweich-b": [ERR_503]}, m)
    r = run_one(c)
    check("A3 Runde ueber alle Modelle, zurueck beim Hauptmodell -> ok ohne Markierung",
          r.get("applies") == "nein" and "_fallback_model" not in r
          and c.calls == ["haupt-modell", "haupt-modell", "ausweich-a", "ausweich-b", "haupt-modell"],
          str(c.calls))
    check("A3 zwischen Modellen kurz, vor der neuen Runde lang gewartet",
          _sleeps[1:3] == [1.0, 1.0] and _sleeps[3] >= 15, str(_sleeps))

    _sleeps.clear()
    c = FakeClient({x: [ERR_503] * 9 for x in m}, m)
    r = run_one(c)
    check("A4 alles ueberlastet -> Fehlerkarte", r.get("applies") == "error", str(c.calls))
    check("A4 neun Versuche, jedes Modell mehrfach", len(c.calls) == 9
          and c.calls.count("haupt-modell") == 4 and c.calls.count("ausweich-b") == 2
          and c.calls[:4] == ["haupt-modell", "haupt-modell", "ausweich-a", "ausweich-b"], str(c.calls))
    check("A4 Wartezeit gesamt mind. so lang wie vor dem Umbau (~3 min), keine Pause nach dem Ende",
          sum(_sleeps) >= 150 and len(_sleeps) == 8, f"{sum(_sleeps):.0f}s, {_sleeps}")
    check("A4 Fehlertext ohne Schluessel", "AQleak999" not in (r.get("reason") or ""),
          (r.get("reason") or "")[:120])

    err_400 = "Client error '400 Bad Request' for url '.../models/ausweich-a:generateContent'"
    c = FakeClient({"haupt-modell": [ERR_503, ERR_503], "ausweich-a": [err_400]}, m)
    r = run_one(c)
    check("A6 Ausweichmodell mit 400 -> sofort das naechste Modell (live gesehen 28.09.)",
          r.get("_fallback_model") == "ausweich-b"
          and c.calls == ["haupt-modell", "haupt-modell", "ausweich-a", "ausweich-b"], str(c.calls))

    c = FakeClient({None: [ERR_503]}, [None])
    r = run_one(c)
    check("A5 Provider ohne Ausweichmodelle -> wie bisher, ohne model-Argument",
          r.get("applies") == "nein" and c.calls == [None, None] and "_fallback_model" not in r,
          str(c.calls))


# ---------------------------------------------------------------------------
class _Resp:
    def __init__(self, status: int, text: str):
        self.status_code = status
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(f"{self.status_code}", request=None, response=None)

    def json(self):
        return {"candidates": [{"content": {"parts": [{"text": OK_JSON}]}}]}


class FakeAsyncClient:
    log: list[dict] = []
    reject_thinking = False
    reject_text = '{"error": {"message": "Thinking is not supported"}}'

    def __init__(self, *a, **kw):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def post(self, url, json=None, headers=None):
        import copy
        FakeAsyncClient.log.append({"url": url, "headers": dict(headers or {}),
                                    "body": copy.deepcopy(json)})
        gc = (json or {}).get("generationConfig", {})
        if FakeAsyncClient.reject_thinking and "thinkingConfig" in gc:
            return _Resp(400, FakeAsyncClient.reject_text)
        return _Resp(200, "")


def block_b() -> None:
    print("\n--- B  LLMClient.ask (google) ---")
    real = httpx.AsyncClient
    httpx.AsyncClient = FakeAsyncClient
    try:
        cl = llm.LLMClient()
        check("B1 Modellliste: Haupt + Ausweich aus der Umgebung",
              cl.models() == ["haupt-modell", "ausweich-a", "ausweich-b"], str(cl.models()))

        FakeAsyncClient.log.clear()
        asyncio.run(cl.ask("s", "u"))
        req = FakeAsyncClient.log[-1]
        check("B2 Schluessel nicht in der Adresse", "AQtest" not in req["url"] and "key=" not in req["url"],
              req["url"])
        check("B2 Schluessel im Kopf x-goog-api-key",
              req["headers"].get("x-goog-api-key") == "AQtest-geheim-123")
        check("B2 Hauptmodell ohne thinkingConfig (Anfrage unveraendert)",
              "thinkingConfig" not in req["body"]["generationConfig"]
              and "/models/haupt-modell:" in req["url"])

        FakeAsyncClient.log.clear()
        asyncio.run(cl.ask("s", "u", model="ausweich-a"))
        req = FakeAsyncClient.log[-1]
        check("B3 Ausweichmodell mit thinkingBudget 0",
              req["body"]["generationConfig"].get("thinkingConfig") == {"thinkingBudget": 0}
              and "/models/ausweich-a:" in req["url"])

        FakeAsyncClient.log.clear()
        FakeAsyncClient.reject_thinking = True
        out = asyncio.run(cl.ask("s", "u", model="ausweich-b"))
        FakeAsyncClient.reject_thinking = False
        check("B4 400 wegen Denkmodus -> zweiter Versuch ohne thinkingConfig",
              len(FakeAsyncClient.log) == 2 and out == OK_JSON
              and "thinkingConfig" not in FakeAsyncClient.log[1]["body"]["generationConfig"],
              f"{len(FakeAsyncClient.log)} Anfragen")

        # gemini-3.5-flash-lite nennt den Grund nicht (live 28.09.2026)
        FakeAsyncClient.log.clear()
        FakeAsyncClient.reject_thinking = True
        FakeAsyncClient.reject_text = '{"error": {"message": "Request contains an invalid argument."}}'
        out = asyncio.run(cl.ask("s", "u", model="ausweich-b"))
        FakeAsyncClient.reject_thinking = False
        check("B4b 400 ohne Nennung des Grundes -> ebenfalls ohne thinkingConfig wiederholt",
              len(FakeAsyncClient.log) == 2 and out == OK_JSON, f"{len(FakeAsyncClient.log)} Anfragen")

        os.environ["GOOGLE_FALLBACK_MODELS"] = "-"
        check("B5 '-' schaltet das Ausweichen ab", llm.LLMClient().models() == ["haupt-modell"])
        os.environ["GOOGLE_FALLBACK_MODELS"] = "haupt-modell, ausweich-a"
        check("B6 Hauptmodell taucht nicht doppelt auf",
              llm.LLMClient().models() == ["haupt-modell", "ausweich-a"])
        del os.environ["GOOGLE_FALLBACK_MODELS"]
        check("B7 Voreinstellung ohne Umgebungsvariable",
              llm.LLMClient().models() == ["haupt-modell", "gemini-3.5-flash-lite", "gemini-3.6-flash"])
        os.environ["GOOGLE_FALLBACK_MODELS"] = "ausweich-a,ausweich-b"
    finally:
        httpx.AsyncClient = real


# ---------------------------------------------------------------------------
def _setup_db() -> int:
    db.init_db()
    fetcher.init_fetcher()
    if not SOURCE_DB.exists():
        sys.exit(f"{SOURCE_DB} fehlt — Block C braucht die gecachten Gesetzestexte.")
    c = sqlite3.connect(TEST_DB, isolation_level=None, uri=True)
    try:
        c.execute("ATTACH DATABASE ? AS src", (SOURCE_DB.as_uri() + "?mode=ro",))
        here = {r[1] for r in c.execute("PRAGMA table_info(law_texts)")}
        there = [r[1] for r in c.execute("PRAGMA src.table_info(law_texts)")]
        cols = ", ".join(col for col in there if col in here)
        c.execute(f"INSERT INTO law_texts ({cols}) SELECT {cols} FROM src.law_texts")
        c.execute("DETACH DATABASE src")
    finally:
        c.close()
    return db.create_user("fallbacktest@example.invalid", "nur-fuer-den-test")


def block_c() -> None:
    print("\n--- C  app._run_analysis_bg ---")
    esg_app.fetch_law_text = lambda reg, language="de", **kw: {
        "text": (fetcher.get_cached_text(reg["key"], language) or {}).get("text") or "",
        "fetched_at": "2026-09-28", "error": ""}
    esg_app.fetch_url_text = lambda url, **kw: {"text": "", "error": ""}
    uid = _setup_db()
    llm_regs = [r for r in REGULATIONS if llm.deterministic_result(r, {}, "de") is None]
    fb_key = llm_regs[0]["key"]
    seen_waiting: dict[str, list[str]] = {}

    real = llm._analyze_one

    async def fake(client, reg, fulltext, language, profile=None):
        seen_waiting[reg["key"]] = list(esg_app._analysis_status[uid].get("waiting") or [])
        res = {**llm._enrich(reg, {}), "applies": "nein", "reason": f"Text {reg['key']}.", "passage": "-"}
        if reg["key"] == fb_key:
            res["_fallback_model"] = "ausweich-a"
        return res

    llm._analyze_one = fake
    try:
        profile = {"name": "Test GmbH", "employees": 300, "employees_de": 300,
                   "revenue_eur": 50_000_000.0, "balance_sheet_eur": 20_000_000.0,
                   "branch": "Herstellung von Schuhen", "language": "de"}
        esg_app._analysis_status[uid] = {"phase": "starting", "done": 0,
                                         "total": len(REGULATIONS), "name": ""}
        esg_app._run_analysis_bg(uid, profile, "de")
    finally:
        llm._analyze_one = real

    st = esg_app._analysis_status[uid]
    check("C1 Lauf fertig", st.get("phase") == "done", str(st)[:160])
    check("C2 'waiting' am Ende leer", st.get("waiting") == [], str(st.get("waiting")))
    name = next(r["name"] for r in REGULATIONS if r["key"] == fb_key)
    check("C3 'waiting' nennt die noch offene Regulierung, solange sie laeuft",
          name in seen_waiting.get(fb_key, []), str(seen_waiting.get(fb_key)))

    c = sqlite3.connect(TEST_DB)
    try:
        cached = {r[0] for r in c.execute("SELECT reg_key FROM analysis_cache")}
    finally:
        c.close()
    others = {r["key"] for r in llm_regs} - {fb_key}
    check("C4 Ausweich-Ergebnis NICHT im Cache", fb_key not in cached, f"{fb_key} in {sorted(cached)}")
    check("C5 Hauptmodell-Ergebnisse im Cache", others <= cached, f"fehlend: {sorted(others - cached)}")

    stored = {r["key"]: r for r in db.latest_analysis(uid)["result"]}
    check("C6 Ausweich-Ergebnis wird angezeigt und gespeichert",
          stored.get(fb_key, {}).get("applies") == "nein")
    check("C7 Markierung nicht in den gespeicherten Ergebnissen",
          all("_fallback_model" not in r for r in stored.values()))


def main() -> int:
    block_a()
    block_b()
    block_c()   # Test-DB bleibt liegen (unter Windows noch geoeffnet); der naechste Lauf loescht sie
    print()
    if _failures:
        print(f"{len(_failures)} Pruefung(en) fehlgeschlagen: {', '.join(_failures)}")
        return 1
    print("=" * 62)
    print("Alle Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
