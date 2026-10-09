/* Regulierungs-Assistent: Chatfenster unten rechts (nur angemeldet).
 *
 * Aufbau nach dem go-textile-Widget, im textil+mode-Design. Eingebunden von
 * templates/base.html; die Konfiguration (Adressen, Sprache, Texte) steht dort
 * in <script id="assistent-config" type="application/json">.
 * Das Widget lebt in einem Shadow DOM: Seite und Widget beeinflussen ihre
 * Gestaltung gegenseitig nicht.
 * Von der Seite aus: window.esgAssistent.open() / .ask(frage, regKey).
 * Die Knoepfe "Nachfragen" auf den Ergebniskarten (.ask-btn) rufen ask() auf.
 */
(function () {
'use strict';
if (window.esgAssistent) return;
const cfgEl = document.getElementById('assistent-config');
if (!cfgEl) return;
let CFG;
try { CFG = JSON.parse(cfgEl.textContent); } catch (e) { return; }
const T = CFG.t || {};

const host = document.createElement('div');
host.id = 'esg-assistent';
host.style.cssText = 'position:fixed;z-index:2147483000;right:0;bottom:0;width:0;height:0';
const root = host.attachShadow({mode: 'open'});
root.innerHTML = '<style>' + `
  :host{all:initial;--navy:#0F3750;--blue:#32AFDC;--green:#78B950;--link:#0070C0;--box:#F2F2F2;
    --line:#DCDCDC;--muted:#5A5A5A}
  *{box-sizing:border-box}
  button,input{font-family:Arial,Helvetica,sans-serif}
  .wrap{font-family:Arial,Helvetica,sans-serif;color:#000;font-size:14.5px;line-height:1.45}
  #launch{position:fixed;right:22px;bottom:22px;min-height:50px;border-radius:25px;border:none;cursor:pointer;
    background:var(--navy);color:#fff;display:flex;align-items:center;gap:10px;padding:0 20px 0 16px;
    font:bold 15px Arial,Helvetica,sans-serif;box-shadow:0 6px 18px rgba(15,55,80,.28);transition:transform .2s}
  #launch:hover{transform:translateY(-2px)}
  #launch:focus-visible,.head button:focus-visible,.foot button:focus-visible,.sugg button:focus-visible{
    outline:2px solid var(--blue);outline-offset:2px}
  #launch svg{flex:none}
  #panel{position:fixed;right:22px;bottom:86px;width:420px;max-width:calc(100vw - 32px);height:74vh;max-height:680px;
    background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 40px rgba(0,0,0,.18);
    display:none;flex-direction:column;overflow:hidden}
  #panel.open{display:flex}
  .head{background:var(--navy);color:#fff;padding:12px 10px 12px 16px;display:flex;align-items:center;gap:10px}
  .head .ttl{min-width:0}
  .head b{font-size:15px;display:block}
  .head small{display:block;font-size:12px;color:#C9D6DE;margin-top:2px}
  .head button{background:none;border:none;color:#C9D6DE;cursor:pointer;font:13px Arial,Helvetica,sans-serif;
    min-width:44px;min-height:44px;padding:0 8px}
  .head .reset{margin-left:auto}
  .head .x{font-size:20px;line-height:1}
  .head button:hover{color:#fff}
  .accent{height:4px;flex:none;background:linear-gradient(90deg,var(--blue),var(--green))}
  .body{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px;background:#fff}
  .row{display:flex;flex-direction:column;align-items:flex-start;gap:6px;max-width:100%}
  .who{font-size:12px;font-weight:bold;color:var(--navy)}
  .msg{line-height:1.55;white-space:pre-wrap;word-wrap:break-word;overflow-wrap:anywhere;min-width:0}
  .msg.bot{max-width:100%}
  .msg.bot a{color:var(--link)}
  .msg.user{background:var(--box);border-left:3px solid var(--blue);align-self:flex-end;max-width:88%;
    border-radius:6px;padding:9px 12px}
  .sugg{display:grid;gap:6px;width:100%}
  .sugg button{font:13.5px Arial,Helvetica,sans-serif;color:var(--navy);text-align:left;background:#fff;
    border:1px solid var(--line);border-radius:6px;padding:10px 12px;min-height:44px;cursor:pointer}
  .sugg button:hover{border-color:var(--navy)}
  .sources{display:grid;grid-template-columns:1fr 1fr;gap:6px;width:100%}
  .sources a{font-size:12.5px;text-decoration:none;color:var(--link);background:var(--box);
    border-left:3px solid var(--blue);border-radius:4px;padding:7px 9px;line-height:1.3;min-width:0;overflow:hidden}
  .sources a:hover{text-decoration:underline}
  .dots{display:inline-flex;gap:4px;padding:6px 0}
  .dots i{width:7px;height:7px;border-radius:50%;background:var(--navy);animation:dot 1.1s infinite ease-in-out}
  .dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
  @keyframes dot{0%,60%,100%{transform:translateY(0);opacity:.35}30%{transform:translateY(-5px);opacity:1}}
  .foot{display:flex;gap:6px;align-items:center;margin:8px 12px 6px;border:1px solid #BFBFBF;border-radius:6px;
    padding:4px 4px 4px 12px}
  .foot:focus-within{border-color:var(--blue);box-shadow:0 0 0 2px rgba(50,175,220,.28)}
  .foot input{flex:1;min-width:0;border:none;padding:10px 0;font-size:16px;outline:none;background:none;color:#000}
  .foot button{background:var(--navy);border:none;border-radius:5px;width:44px;height:44px;cursor:pointer;
    display:flex;align-items:center;justify-content:center;flex:none}
  .foot button:disabled{opacity:.4;cursor:default}
  .foot #mic{background:#fff;border:1px solid #BFBFBF}
  .foot #mic svg{stroke:var(--navy)}
  .foot #mic.listening{background:#A32020;border-color:#A32020}
  .foot #mic.listening svg{stroke:#fff}
  .disc{font-size:11px;color:var(--muted);text-align:center;padding:0 12px 10px;background:#fff}
  .disc a{color:inherit}
  @media (max-width:480px){
    #panel{right:8px;left:8px;width:auto;max-width:none;bottom:76px;height:calc(100vh - 96px);max-height:none}
    #launch{right:12px;bottom:12px;padding:0 14px}
    #launch .lbl{display:none}
    .sources{grid-template-columns:1fr}
  }
  @media (prefers-reduced-motion: reduce){ #launch,.dots i{animation:none!important;transition:none!important} }
` + '</style><div class="wrap">' + `
  <button id="launch" type="button"></button>
  <div id="panel" role="dialog">
    <div class="head">
      <div class="ttl"><b></b><small></small></div>
      <button class="reset" type="button"></button>
      <button class="x" type="button">&#x2715;</button>
    </div>
    <div class="accent"></div>
    <div class="body" id="body" aria-live="polite"></div>
    <div class="foot">
      <input id="input" maxlength="800" autocomplete="off">
      <button id="mic" type="button" hidden>
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/></svg>
      </button>
      <button id="send" type="button">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>
    <div class="disc"></div>
  </div>` + '</div>';
document.body.appendChild(host);

const $ = id => root.getElementById(id);
const body = $('body'), input = $('input'), sendBtn = $('send'), panel = $('panel'), micBtn = $('mic'),
      launch = $('launch');

function esc(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

// Texte setzen (alles ueber textContent/esc, nichts ungeprueft als HTML)
launch.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#fff" ' +
  'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/>' +
  '<path d="M9 9h6M9 12h4"/></svg><span class="lbl">' + esc(T.title || '') + '</span>';
launch.setAttribute('aria-label', T.open || T.title || '');
launch.title = T.open || '';
panel.setAttribute('aria-label', T.title || '');
root.querySelector('.head b').textContent = T.title || '';
root.querySelector('.head small').textContent = T.subtitle || '';
const resetBtn = root.querySelector('.reset'), closeBtn = root.querySelector('.x');
resetBtn.textContent = T.new || 'Neu'; resetBtn.title = T.new_title || '';
closeBtn.setAttribute('aria-label', T.close || ''); closeBtn.title = T.close || '';
input.placeholder = T.placeholder || '';
input.setAttribute('aria-label', T.placeholder || '');
sendBtn.setAttribute('aria-label', T.send || ''); sendBtn.title = T.send || '';
micBtn.setAttribute('aria-label', T.mic || ''); micBtn.title = T.mic || '';
const disc = root.querySelector('.disc');
disc.textContent = (T.disclaimer || '') + ' · ';
if (CFG.privacy) {
  const a = document.createElement('a');
  a.href = CFG.privacy; a.textContent = T.privacy || 'Datenschutz';
  disc.appendChild(a);
}

let busy = false;

// Markdown der Modellantwort: **fett**, Aufzaehlungen, Links [Text](https://…) und nackte URLs.
// Erst escapen, dann gezielt Auszeichnung erlauben — Modelltext ist nie HTML.
// Links werden zuerst durch Platzhalter ersetzt und erst am Ende eingesetzt: sonst fand der
// Durchlauf fuer nackte URLs auch die Adresse im href eines schon gebauten Links und schachtelte
// ein zweites <a> hinein — daraus liess sich ein Ereignis-Attribut bauen (Abnahme 09.10.2026).
function format(txt) {
  const links = [];
  const link = (href, label) => {
    links.push('<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + label + '</a>');
    return '\u0000' + (links.length - 1) + '\u0000';
  };
  return esc(String(txt).replace(/\u0000/g, ''))
    .replace(/\[([^\]\n]+)\]\((https?:\/\/[^\s)&]+(?:&amp;[^\s)&]+)*)\)/g, (m, label, href) => link(href, label))
    .replace(/(^|[\s(])(https?:\/\/[^\s<)&\u0000]+(?:&amp;[^\s<)&\u0000]+)*)/g, (m, pre, href) => {
      const tail = (href.match(/[.,;:!?]+$/) || [''])[0];   // Satzzeichen gehoert nicht zur Adresse
      href = href.slice(0, href.length - tail.length);
      return pre + link(href, href) + tail;
    })
    .replace(/^#{1,4}[ \t]+(.+)$/gm, '<b>$1</b>')
    .replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>')
    .replace(/^[ \t]*[*-][ \t]+/gm, '• ')
    .replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,:;!?]|$)/gm, '$1<i>$2</i>')
    .replace(/\u0000(\d+)\u0000/g, (m, i) => links[+i]);
}
function scrollDown() { body.scrollTop = body.scrollHeight; }
function isOpen() { return panel.classList.contains('open'); }
function openPanel() {
  if (isOpen()) return;
  panel.classList.add('open'); launch.setAttribute('aria-expanded', 'true');
  scrollDown(); input.focus();
}
function closePanel() { panel.classList.remove('open'); launch.setAttribute('aria-expanded', 'false'); launch.focus(); }
function toggle() { isOpen() ? closePanel() : openPanel(); }

function addUser(txt) {
  const d = document.createElement('div'); d.className = 'msg user'; d.textContent = txt;
  body.appendChild(d); scrollDown();
}
function addBot(txt) {
  const row = document.createElement('div'); row.className = 'row';
  const who = document.createElement('div'); who.className = 'who'; who.textContent = T.who || 'Assistent';
  const m = document.createElement('div'); m.className = 'msg bot'; m.textContent = txt || '';
  row.appendChild(who); row.appendChild(m); body.appendChild(row); scrollDown();
  return {row, m};
}
function addSources(row, sources) {
  const box = document.createElement('div'); box.className = 'sources';
  for (const s of sources) {
    if (!/^https?:\/\//.test(s.url || '')) continue;
    const a = document.createElement('a');
    a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = s.title || s.url;
    box.appendChild(a);
  }
  if (box.children.length) { row.appendChild(box); scrollDown(); }
}

// Gespraechsverlauf: nur in diesem Browser-Tab (sessionStorage), der Server speichert nichts.
// Der Schluessel haengt an der Sitzung (neu bei jeder Anmeldung): Meldet sich im selben Tab
// jemand anderes an, sieht er das Gespraech der Vorperson nicht.
const PREFIX = 'esg-assistent-', HIST_KEY = PREFIX + (CFG.sid || 'x'), HIST_SEND = 6, HIST_KEEP = 30;
let history = [];
function loadHistory() {
  try {
    for (let i = sessionStorage.length - 1; i >= 0; i--) {
      const k = sessionStorage.key(i);
      if (k && k.indexOf(PREFIX) === 0 && k !== HIST_KEY) sessionStorage.removeItem(k);
    }
    history = JSON.parse(sessionStorage.getItem(HIST_KEY) || '[]');
  } catch (e) { history = []; }
  if (!Array.isArray(history)) history = [];
}
function saveHistory() { try { sessionStorage.setItem(HIST_KEY, JSON.stringify(history.slice(-HIST_KEEP))); } catch (e) {} }

function renderStart() {
  body.innerHTML = '';
  const g = addBot(T.greeting || '');
  if (!history.length) {
    const s = document.createElement('div'); s.className = 'sugg';
    [T.sugg1, T.sugg2, T.sugg3].filter(Boolean).forEach(v => {
      const b = document.createElement('button'); b.type = 'button'; b.textContent = v; b.onclick = () => ask(v);
      s.appendChild(b);
    });
    g.row.appendChild(s);
  }
  for (const m of history) {
    if (m.role === 'user') addUser(m.text);
    else addBot('').m.innerHTML = format(m.text);
  }
}
function reset() { if (busy) return; history = []; saveHistory(); renderStart(); input.focus(); }

loadHistory();
renderStart();

let pendingReg = null;   // Regulierung aus "Nachfragen", geht mit der naechsten Frage mit
function ask(q, regKey) {
  openPanel();
  if (busy) return;
  pendingReg = regKey || null;
  input.value = q;
  send();
}

async function send() {
  const q = input.value.trim(); if (!q || busy) return;
  if (listening) stopListening(true);
  busy = true; sendBtn.disabled = true; input.value = '';
  body.querySelectorAll('.sugg').forEach(s => s.remove());
  addUser(q);
  const bot = addBot('');
  bot.m.innerHTML = '<span class="dots" role="status" aria-label="' + esc(T.thinking || '') + '"><i></i><i></i><i></i></span>';
  const regKey = pendingReg; pendingReg = null;
  try {
    const res = await fetch(CFG.api, {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: q, history: history.slice(-HIST_SEND), reg_key: regKey})
    });
    if (!res.ok) {
      const d = await res.json().catch(() => ({}));
      bot.m.textContent = d.error || (res.status === 401 ? T.session : T.error) || '';
    } else {
      const reader = res.body.getReader(), dec = new TextDecoder();
      let buf = '', first = true, sources = [], suche = '', notice = '';
      for (;;) {
        const {value, done} = await reader.read(); if (done) break;
        buf += dec.decode(value, {stream: true});
        const lines = buf.split('\n'); buf = lines.pop();
        for (const line of lines) {
          if (!line.trim()) continue;
          const o = JSON.parse(line);
          if (o.type === 'meta') suche = o.suche || '';
          if (o.type === 'sources') sources = o.sources || [];
          if (o.type === 'notice') notice = o.text || '';
          if (o.type === 'token') {
            if (first) { bot.m.textContent = ''; first = false; }
            bot.m.textContent += o.text; scrollDown();
          }
        }
      }
      // Hinweise (ausgelastet, unterbrochen) erscheinen kursiv und gehen nicht in den Verlauf.
      const hinweis = notice ? '<i>' + esc(notice) + '</i>' : '';
      if (first) bot.m.innerHTML = hinweis || esc(T.no_answer || '');
      else {
        const answer = bot.m.textContent;
        bot.m.innerHTML = format(answer) + (hinweis ? '\n\n' + hinweis : '');
        history.push({role: 'user', text: q, suche: suche}, {role: 'model', text: answer}); saveHistory();
      }
      if (sources.length) addSources(bot.row, sources);
    }
  } catch (e) { bot.m.textContent = T.error || ''; }
  busy = false; sendBtn.disabled = false; input.focus();
}

// ---- Spracheingabe ----
// Chrome, Edge, Safari: Spracherkennung des Browsers (Chrome schickt das Gesprochene dafuer an
// Google). Firefox: Aufnahme, Umwandlung auf dem Server (Gemini). Abgeschickt wird nach
// STILLE_MS ohne neues Wort oder per erneutem Tippen auf das Mikrofon.
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const SR_LANG = {de: 'de-DE', en: 'en-GB', es: 'es-ES', fr: 'fr-FR', it: 'it-IT', zh: 'zh-CN'};
const PLACEHOLDER = input.placeholder, STILLE_MS = 3000, MAX_MS = 60000;
const MODUS = SR ? 'browser' : (navigator.mediaDevices && window.MediaRecorder && CFG.speech ? 'server' : null);
let rec = null, listening = false, fertig = false, bisher = '', aktuell = '', fehler = null, stille = null,
    startZeit = 0, aufn = null;
if (MODUS) micBtn.hidden = false;

function setMic(on, hinweis) {
  listening = on; micBtn.classList.toggle('listening', on);
  micBtn.setAttribute('aria-label', on ? (T.mic_done || '') : (T.mic || ''));
  input.placeholder = hinweis || (on ? (T.listening || '') : PLACEHOLDER);
}
function stopListening(verwerfen) {
  if (MODUS === 'server') { if (aufn) (verwerfen ? aufn.verwerfen() : aufn.stop()); return; }
  fertig = true; clearTimeout(stille);
  try { verwerfen ? rec.abort() : rec.stop(); } catch (e) {}
}
function mic() {
  if (busy) return;
  if (MODUS === 'server') return aufnahme();
  if (listening) { stopListening(false); return; }
  bisher = ''; aktuell = ''; fehler = null; fertig = false; startZeit = Date.now(); input.value = '';
  setMic(true); micStart();
}
function micStart() {
  rec = new SR(); rec.lang = SR_LANG[CFG.lang] || 'de-DE';
  rec.interimResults = true; rec.continuous = true; rec.maxAlternatives = 1;
  rec.onresult = e => {
    let fin = '', zw = '';
    for (let i = 0; i < e.results.length; i++) {
      const tx = e.results[i][0].transcript;
      if (e.results[i].isFinal) fin += tx + ' '; else zw += tx;
    }
    aktuell = fin;
    input.value = (bisher + ' ' + fin + zw).replace(/\s+/g, ' ').trim();
    clearTimeout(stille); stille = setTimeout(() => stopListening(false), STILLE_MS);
  };
  rec.onerror = e => {
    if (e.error === 'no-speech') { if (!input.value.trim()) { fehler = T.mic_nothing; fertig = true; } return; }
    if (e.error === 'aborted') return;
    fehler = (e.error === 'not-allowed' || e.error === 'service-not-allowed') ? T.mic_denied
           : e.error === 'audio-capture' ? T.mic_none : T.mic_unavailable;
    fertig = true;
  };
  rec.onend = () => {
    bisher = (bisher + ' ' + aktuell).trim(); aktuell = '';
    if (!fertig && Date.now() - startZeit < MAX_MS) { try { micStart(); return; } catch (e) {} }
    clearTimeout(stille);
    setMic(false, fehler);
    if (input.value.trim() && !busy) send();
  };
  try { rec.start(); } catch (e) { fertig = true; setMic(false); }
}

async function aufnahme() {
  if (listening) { aufn.stop(); return; }
  let stream;
  try { stream = await navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true, noiseSuppression: true}}); }
  catch (e) { setMic(false, e.name === 'NotFoundError' ? T.mic_none : T.mic_denied); return; }
  const typ = ['audio/ogg;codecs=opus', 'audio/webm;codecs=opus', 'audio/webm', 'audio/mp4']
    .find(x => MediaRecorder.isTypeSupported(x)) || '';
  const mr = new MediaRecorder(stream, typ ? {mimeType: typ, audioBitsPerSecond: 32000} : {audioBitsPerSecond: 32000});
  const teile = []; mr.ondataavailable = e => { if (e.data.size) teile.push(e.data); };
  const ctx = new (window.AudioContext || window.webkitAudioContext)(), an = ctx.createAnalyser();
  an.fftSize = 1024; ctx.createMediaStreamSource(stream).connect(an);
  const puffer = new Float32Array(an.fftSize), start = Date.now();
  let gesprochen = false, letzterLaut = start, gestoppt = false, verworfen = false;
  const takt = setInterval(() => {
    an.getFloatTimeDomainData(puffer); let s = 0; for (const v of puffer) s += v * v;
    if (Math.sqrt(s / puffer.length) > 0.015) { gesprochen = true; letzterLaut = Date.now(); }
    const jetzt = Date.now();
    if ((gesprochen && jetzt - letzterLaut > STILLE_MS) || (!gesprochen && jetzt - start > 8000) || jetzt - start > MAX_MS) stoppe();
  }, 100);
  function stoppe() { if (gestoppt) return; gestoppt = true; clearInterval(takt); try { mr.stop(); } catch (e) {} }
  mr.onstop = async () => {
    stream.getTracks().forEach(x => x.stop()); ctx.close();
    if (verworfen) return;
    if (!gesprochen) { setMic(false, T.mic_nothing); return; }
    const blob = new Blob(teile, {type: (mr.mimeType || typ || 'audio/webm').split(';')[0]});
    setMic(false, T.mic_recognizing); micBtn.disabled = true;
    try {
      const r = await fetch(CFG.speech, {method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': blob.type}, body: blob});
      const d = await r.json().catch(() => ({}));
      micBtn.disabled = false;
      if (!r.ok || !d.text) { setMic(false, d.error || T.mic_nothing); return; }
      setMic(false); input.value = d.text; send();
    } catch (e) { micBtn.disabled = false; setMic(false, T.mic_unavailable); }
  };
  aufn = {stop: stoppe, verwerfen() { verworfen = true; stoppe(); setMic(false); }};
  mr.start(250); setMic(true);
}

launch.setAttribute('aria-expanded', 'false');
launch.addEventListener('click', toggle);
resetBtn.addEventListener('click', reset);
closeBtn.addEventListener('click', closePanel);
micBtn.addEventListener('click', mic);
sendBtn.addEventListener('click', send);
input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
root.addEventListener('keydown', e => { if ((e.key === 'Escape' || e.key === 'Esc') && isOpen()) closePanel(); });

// "Nachfragen" auf den Ergebniskarten
document.addEventListener('click', e => {
  const b = e.target && e.target.closest ? e.target.closest('.ask-btn') : null;
  if (!b) return;
  e.preventDefault();
  const name = b.getAttribute('data-name') || '';
  ask((T.ask_card || '{name}').replace('{name}', name), b.getAttribute('data-reg') || null);
});

window.esgAssistent = {open: openPanel, ask: ask};
})();
