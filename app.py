"""ESG-Regulierungs-Check — Flask-Anwendung.

Start: python app.py   (Dev-Server, Port 5000)
Prod:  gunicorn -w 2 -b 0.0.0.0:8080 app:app
"""
from __future__ import annotations

import json
import os
import queue
import secrets
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# VOR den Projekt-Importen: db.py liest `ESG_DB_PATH` beim Import.
load_dotenv(override=True)

from flask import (  # noqa: E402
    Flask,
    Response,
    flash,
    has_request_context,
    redirect,
    render_template,
    request,
    session,
    stream_with_context,
    url_for,
)
from flask.sessions import SecureCookieSessionInterface

import db
from i18n import (
    BRANCH_LABELS,
    GROUP_ROLE_LABELS,
    LANGUAGES,
    LEGAL_FORM_LABELS,
    LOCATION_LABELS,
    PRODUCT_CAT_LABELS,
    SITE_TYPE_LABELS,
    normalize_lang,
    t,
    t_applies_note,
    t_opt,
    t_status,
)
from lawparse import build_context
from llm import analyze_streaming, plan_analysis
from fetcher import (  # noqa: E402
    fetch_law_text,
    fetch_url_text,
    get_cached_text,
    list_versions,
    source_is_base_act_fallback,
)
from regulations import (
    BRANCHES,
    GROUP_ROLES,
    LEGAL_FORMS,
    LOCATIONS,
    PRODUCT_CATEGORIES,
    REGULATIONS,
    SITE_TYPES,
    application_for,
    guidelines_for,
    published_for,
    published_is_draft,
)
from views import render_cards_html, render_csv


def _secret_key() -> str:
    """Session-Secret aus der Umgebung, sonst persistent im Datenverzeichnis.

    Ein fester Default im Code waere ratbar (Sessions faelschbar), ein bei jedem
    Start neu gewuerfeltes Secret wuerde alle Sessions entwerten. Deshalb einmalig
    erzeugen und in data/flask_secret ablegen — das Verzeichnis ist ein Docker-Volume
    und steht in .gitignore/.dockerignore.
    """
    env_secret = (os.getenv("FLASK_SECRET") or "").strip()
    if env_secret:
        return env_secret
    path = Path(__file__).parent / "data" / "flask_secret"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        try:
            with open(path, "x", encoding="utf-8") as fh:
                fh.write(secrets.token_urlsafe(48))
            path.chmod(0o600)
        except (FileExistsError, OSError):
            pass
    return path.read_text(encoding="utf-8").strip()


class ProxyAwareSessionInterface(SecureCookieSessionInterface):
    """Setzt das Secure-Flag genau dann, wenn der Request ueber https kam.

    Hinter nginx wertet die PrefixMiddleware X-Forwarded-Proto aus (-> https),
    lokal ueber http bleibt das Cookie damit nutzbar.
    """

    def get_cookie_secure(self, app: Flask) -> bool:
        return bool(has_request_context() and request.is_secure)


app = Flask(__name__)
app.secret_key = _secret_key()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.session_interface = ProxyAwareSessionInterface()


# Reverse-Proxy Subpath: nginx sendet X-Script-Name Header,
# damit url_for() automatisch /regulierungs-check prefixed.
class PrefixMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
        # Damit url_for(_external=True) hinter dem Proxy https-Links baut
        # (gebraucht fuer den Passwort-Reset-Link).
        proto = environ.get("HTTP_X_FORWARDED_PROTO", "")
        if proto:
            environ["wsgi.url_scheme"] = proto.split(",")[0].strip()
        return self.wsgi_app(environ, start_response)


app.wsgi_app = PrefixMiddleware(app.wsgi_app)

db.init_db()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _lang() -> str:
    return normalize_lang(session.get("ui_language"))


def _uid() -> int | None:
    return session.get("user_id")


def _require_login():
    if not _uid():
        return redirect(url_for("login"))
    return None


def _provider_info() -> tuple[str, str]:
    provider = (os.getenv("LLM_PROVIDER") or "ollama").lower()
    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "-")
    elif provider == "anthropic":
        model = os.getenv("CLAUDE_MODEL", "-")
    else:
        model = os.getenv("OPENAI_MODEL", "-")
    return provider, model


# Jinja2 globals
@app.context_processor
def _inject_globals():
    lang = _lang()
    return dict(
        t=t,
        t_opt=t_opt,
        lang=lang,
        LANGUAGES=LANGUAGES,
        BRANCH_LABELS=BRANCH_LABELS,
        SITE_TYPE_LABELS=SITE_TYPE_LABELS,
        LOCATION_LABELS=LOCATION_LABELS,
        LEGAL_FORM_LABELS=LEGAL_FORM_LABELS,
        GROUP_ROLE_LABELS=GROUP_ROLE_LABELS,
        PRODUCT_CAT_LABELS=PRODUCT_CAT_LABELS,
    )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if _uid():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    lang = _lang()
    if request.method == "POST":
        action = request.form.get("action")
        email = (request.form.get("email") or "").strip()
        pw = request.form.get("password", "")

        if action == "login":
            uid = db.verify_user(email, pw)
            if uid:
                session["user_id"] = uid
                session["user_email"] = email
                return redirect(url_for("dashboard"))
            flash(t("err_login_failed", lang), "error")

        elif action == "forgot":
            # Bewusst immer dieselbe Meldung — sonst liesse sich abfragen,
            # welche Adressen registriert sind.
            db.create_reset_request(email)
            flash(t("ok_reset_requested", lang), "success")

        elif action == "signup":
            pw2 = request.form.get("password2", "")
            import re
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                flash(t("err_email_invalid", lang), "error")
            elif len(pw) < 8:
                flash(t("err_pw_short", lang), "error")
            elif pw != pw2:
                flash(t("err_pw_mismatch", lang), "error")
            elif db.email_exists(email):
                flash(t("err_email_exists", lang), "error")
            else:
                uid = db.create_user(email, pw)
                session["user_id"] = uid
                session["user_email"] = email
                flash(t("ok_account_created", lang), "success")
                return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Passwort: aendern, zuruecksetzen, Admin-Reset
# ---------------------------------------------------------------------------
ADMIN_EMAILS = {"mschuckert@textil-mode.de"}


def _is_admin() -> bool:
    return (session.get("user_email") or "").lower().strip() in ADMIN_EMAILS


@app.route("/passwort-aendern", methods=["GET", "POST"])
def change_password():
    redir = _require_login()
    if redir:
        return redir

    lang = _lang()
    if request.method == "POST":
        current = request.form.get("current_password", "")
        pw = request.form.get("password", "")
        pw2 = request.form.get("password2", "")

        if not db.check_password(_uid(), current):
            flash(t("err_pw_current_wrong", lang), "error")
        elif len(pw) < 8:
            flash(t("err_pw_short", lang), "error")
        elif pw != pw2:
            flash(t("err_pw_mismatch", lang), "error")
        else:
            db.set_password(_uid(), pw)
            flash(t("ok_pw_changed", lang), "success")
            return redirect(url_for("dashboard"))

    return render_template("password_change.html")


@app.route("/passwort-zuruecksetzen/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    lang = _lang()
    user = db.user_for_reset_token(token)
    if not user:
        return render_template("password_reset.html", invalid=True), 400

    if request.method == "POST":
        pw = request.form.get("password", "")
        pw2 = request.form.get("password2", "")
        if len(pw) < 8:
            flash(t("err_pw_short", lang), "error")
        elif pw != pw2:
            flash(t("err_pw_mismatch", lang), "error")
        else:
            # set_password entwertet den Token gleich mit.
            db.set_password(user["id"], pw)
            flash(t("ok_pw_changed", lang), "success")
            return redirect(url_for("login"))

    return render_template("password_reset.html", invalid=False, email=user["email"])


@app.route("/admin/passwort-resets", methods=["GET", "POST"])
def admin_resets():
    redir = _require_login()
    if redir:
        return redir
    if not _is_admin():
        return redirect(url_for("dashboard"))

    lang = _lang()
    issued = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        user = db.get_user_by_email(email)
        if not user:
            flash(t("err_user_unknown", lang), "error")
        else:
            token, expires = db.issue_reset_token(user["id"])
            issued = {
                "email": user["email"],
                "url": url_for("reset_password", token=token, _external=True),
                "expires": expires,
            }

    return render_template(
        "admin_resets.html", requests=db.list_open_resets(), issued=issued
    )


@app.route("/admin/regulierungs-status")
def admin_reg_status():
    """Gesetzesstand, Watchdog-Lauf und erkannte Textaenderungen je Regulierung."""
    redir = _require_login()
    if redir:
        return redir
    if not _is_admin():
        return redirect(url_for("dashboard"))

    lang = _lang()
    changes = db.watchdog_changes_by_reg()
    rows = []
    for reg in REGULATIONS:
        key = reg["key"]
        cached = get_cached_text(key, lang) or {}
        app_info = application_for(key)
        rows.append({
            "nr": reg["nr"],
            "key": key,
            "name": reg["name"],
            "url": reg.get("text_url") or reg["url"],
            "applies_from": app_info["applies_from"],
            "status_label": t_status(app_info["status"], lang),
            "status": app_info["status"],
            "law_as_of": (cached.get("fetched_at") or "")[:10],
            "has_text": bool((cached.get("text") or "").strip()),
            "source_note": cached.get("source_note") or "",
            # Notbehelf-Text: nur der Ursprungsrechtsakt, spaetere Aenderungen
            # fehlen. Muss sichtbar sein, sonst wirkt ein veralteter Stand wie
            # ein aktueller.
            "base_act": source_is_base_act_fallback(cached.get("source_status")),
            "versions": len(list_versions(key, lang, limit=50)),
            "change": changes.get(key),
        })
    return render_template(
        "admin_regstatus.html", rows=rows, last_run=db.latest_watchdog_run(), lang=lang
    )


@app.route("/set-language", methods=["POST"])
def set_language():
    lang = request.form.get("language", "de")
    session["ui_language"] = normalize_lang(lang)
    return redirect(request.referrer or url_for("index"))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    redir = _require_login()
    if redir:
        return redir

    uid = _uid()
    lang = _lang()
    company = db.get_company(uid)
    last = db.latest_analysis(uid)
    provider, model = _provider_info()

    cards_html = ""
    if last:
        cards_html = render_cards_html(last["result"], lang)

    return render_template(
        "dashboard.html",
        company=company or {},
        last=last,
        cards_html=cards_html,
        provider=provider,
        model=model,
        BRANCHES=BRANCHES,
        SITE_TYPES=SITE_TYPES,
        LOCATIONS=LOCATIONS,
        LEGAL_FORMS=LEGAL_FORMS,
        GROUP_ROLES=GROUP_ROLES,
        PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
        reg_count=len(REGULATIONS),
    )


@app.route("/save-company", methods=["POST"])
def save_company():
    redir = _require_login()
    if redir:
        return redir

    uid = _uid()
    lang = _lang()
    f = request.form

    sites = []
    i = 0
    while f"site_type_{i}" in f:
        count = int(f.get(f"site_count_{i}", 0) or 0)
        if count > 0:
            sites.append({
                "type": f.get(f"site_type_{i}", SITE_TYPES[0]),
                "location": f.get(f"site_location_{i}", LOCATIONS[0]),
                "count": count,
            })
        i += 1

    data = {
        "name": (f.get("name") or "").strip() or None,
        "employees": int(f.get("employees") or 0),
        "employees_de": int(f.get("employees_de") or 0),
        "revenue_eur": float(f.get("revenue_eur") or 0),
        "balance_sheet_eur": float(f.get("balance_sheet_eur") or 0),
        "legal_form": f.get("legal_form", LEGAL_FORMS[0]),
        "group_role": f.get("group_role", GROUP_ROLES[0]),
        "branch": f.get("branch", BRANCHES[0]),
        "b2c": "b2c" in f,
        "listed": "listed" in f,
        "env_claims": "env_claims" in f,
        "eu_importer": "eu_importer" in f,
        "product_categories": f.getlist("product_categories"),
        "sites": sites,
        "language": lang,
    }
    db.upsert_company(uid, data)
    flash(t("ok_saved", lang), "success")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------------------
# KI-Autofill der Stammdaten
# ---------------------------------------------------------------------------
@app.route("/api/autofill", methods=["POST"])
def autofill_api():
    uid = _uid()
    if not uid:
        return Response(json.dumps({"error": "not authenticated"}), status=401,
                        mimetype="application/json")
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return Response(json.dumps({"error": "name missing"}), status=400,
                        mimetype="application/json")
    from autofill import research_company
    try:
        result = research_company(name, language=_lang())
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        result = {"fields": {}, "sources": [], "error": str(e)}
    return Response(json.dumps(result, ensure_ascii=False), mimetype="application/json")


# ---------------------------------------------------------------------------
# Analyse (Background-Thread + Polling)
# ---------------------------------------------------------------------------
# Globaler Status-Speicher pro User (einfach, reicht für Single-VPS)
_analysis_status: dict[int, dict] = {}


def _run_analysis_bg(uid: int, profile: dict, lang: str) -> None:
    """Läuft im Background-Thread. Schreibt Fortschritt in _analysis_status."""
    status = _analysis_status[uid]
    try:
        total = len(REGULATIONS)
        status.update({"phase": "texts", "done": 0, "total": total, "name": ""})

        # Phase 1: Volltexte + Guidelines (immer Aktualität prüfen via ETag/Last-Modified)
        texts: dict[str, str] = {}
        law_dates: dict[str, str] = {}
        max_chars = int(os.getenv("FULLTEXT_MAX_CHARS", "40000"))
        for i, reg in enumerate(REGULATIONS, 1):
            status.update({"done": i, "name": reg["name"]})
            res = fetch_law_text(reg, language=lang)
            law_text = res.get("text") or ""
            law_dates[reg["key"]] = (res.get("fetched_at") or "")[:10]
            # Ein gescheiterter Aktualisierungsversuch bricht die Analyse nicht ab
            # (der Cache-Text trägt sie weiter), darf aber nicht spurlos bleiben.
            # Dauerhaft sichtbar wird so etwas erst über den Watchdog-Lauf auf
            # /admin/regulierungs-status — siehe offener Punkt in CLAUDE.md.
            if res.get("error"):
                print(f"[analysis] {reg['key']}: {res['error']}", flush=True)

            # Guidelines dazuladen. Kurzer Timeout (8s), damit eine langsame
            # Guideline-URL nicht die ganze Analyse blockiert. Fehler werden
            # still uebergangen.
            guides: list[dict] = []
            for g in guidelines_for(reg["key"]):
                try:
                    g_res = fetch_url_text(g["url"], language=lang, timeout=8.0)
                    g_text = (g_res.get("text") or "").strip()
                    if g_text:
                        guides.append({"name": g["name"], "url": g["url"], "text": g_text})
                except Exception as e:  # noqa: BLE001
                    print(f"[guideline-fetch] skipped {g['url']}: {e}", flush=True)

            # Strukturbasierte Auswahl statt Blind-Kappung: sonst landet bei
            # EU-Rechtsakten nur die Praeambel im Kontext.
            texts[reg["key"]] = build_context(reg, law_text, guides, max_chars)

        # Phase 2: LLM-Analyse — erst NACH Phase 1 planen, damit der
        # Gesetzesstand im Cache-Schluessel der eben geladene ist.
        ready, todo, cache_keys = plan_analysis(profile, REGULATIONS, lang)
        jobs = [(reg, texts.get(reg["key"], "")) for reg in todo]

        status.update({"phase": "analysis", "done": len(ready), "total": total,
                        "cached": len(ready), "new": len(jobs), "name": ""})

        q = analyze_streaming(profile, jobs, ready)
        results: list[dict] = []
        done = 0
        while True:
            item = q.get()
            if item is None:
                break
            is_cached = item.pop("_from_cache", False)
            if not is_cached and item.get("applies") != "error":
                key = cache_keys.get(item.get("key", ""))
                if key:
                    ph, rh, th = key
                    db.put_cache(ph, item["key"], rh, th, item)
            # Erst NACH dem Cache-Schreiben setzen: der Gesetzesstand gehoert zum
            # aktuellen Lauf, nicht zum zwischengespeicherten LLM-Urteil — sonst
            # zeigte ein Cache-Treffer spaeter ein veraltetes Datum.
            item["law_as_of"] = law_dates.get(item.get("key", ""), "")
            results.append(item)
            done += 1
            status.update({"done": done, "name": item.get("name", "-")})

        # Speichern
        if any((r.get("applies") or "").lower() != "error" for r in results):
            db.save_analysis(uid, results)

        status.update({"phase": "done", "done": total, "total": total})

    except Exception as e:
        import traceback
        traceback.print_exc()
        status.update({"phase": "error", "error": str(e)})


@app.route("/run-analysis")
def run_analysis_page():
    redir = _require_login()
    if redir:
        return redir

    uid = _uid()
    lang = _lang()
    company = db.get_company(uid)
    if not company or not company.get("employees"):
        return redirect(url_for("dashboard"))

    # Analyse im Background-Thread starten
    profile = {**company, "language": lang}
    _analysis_status[uid] = {"phase": "starting", "done": 0, "total": len(REGULATIONS), "name": ""}
    t_thread = threading.Thread(target=_run_analysis_bg, args=(uid, profile, lang), daemon=True)
    t_thread.start()

    return render_template("analysis.html")


@app.route("/api/analysis-status")
def analysis_status_api():
    uid = _uid()
    if not uid:
        return json.dumps({"phase": "error", "error": "not authenticated"}), 401
    status = _analysis_status.get(uid, {"phase": "idle"})
    return Response(json.dumps(status, ensure_ascii=False), mimetype="application/json")


# ---------------------------------------------------------------------------
# Vollbild + CSV
# ---------------------------------------------------------------------------
@app.route("/fullscreen")
def fullscreen():
    # Kein uid-Parameter: die Ansicht zeigt ausschliesslich die eigene Analyse.
    redir = _require_login()
    if redir:
        return redir
    last = db.latest_analysis(_uid())
    if not last:
        return render_template("fullscreen.html", cards_html="", last=None)
    lang = normalize_lang(request.args.get("lang") or _lang())
    cards_html = render_cards_html(last["result"], lang)
    return render_template("fullscreen.html", cards_html=cards_html, last=last, lang=lang)


@app.route("/regulierungsliste")
def regulations_list():
    """Tabellarische Uebersicht aller Regulierungen + Guidelines + Veroeffentlichungsdatum."""
    redir = _require_login()
    if redir:
        return redir
    lang = _lang()
    rows = []
    for reg in REGULATIONS:
        guides = [{"name": g["name"], "url": g["url"]}
                  for g in guidelines_for(reg["key"])]
        app_info = application_for(reg["key"])
        rows.append({
            "nr": reg["nr"],
            "key": reg["key"],
            "name": reg["name"],
            "full_name": reg.get("full_name") or reg["name"],
            "scope": reg.get("scope") or "",
            "url": reg["url"],
            "key_article": reg.get("key_article") or "",
            "stand": published_for(reg["key"]),
            # Uebersetztes "Entwurf" statt eines deutschen Freitexts im Datum.
            "stand_draft": (t_status("entwurf", lang)
                            if published_is_draft(reg["key"]) else ""),
            "guidelines": guides,
            "applies_from": app_info["applies_from"],
            "status": app_info["status"],
            "status_label": t_status(app_info["status"], lang),
            "applies_note": t_applies_note(app_info["note"], lang),
        })
    return render_template("regulierungsliste.html", rows=rows, lang=lang)


@app.route("/download-csv")
def download_csv():
    uid = _uid()
    if not uid:
        return redirect(url_for("login"))
    last = db.latest_analysis(uid)
    if not last:
        return "No results", 404
    lang = _lang()
    csv_bytes = render_csv(last["result"], lang)
    fname = f"esg_analyse_{datetime.now():%Y%m%d_%H%M}.csv"
    return Response(
        csv_bytes,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={fname}"},
    )


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
