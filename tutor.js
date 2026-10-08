/* =====================================================================
   AI TUTOR (tutor.html) — chat, live class on a board, language practice.
   Talks to /api/tutor. Voice uses the browser's free built-in speech
   (SpeechRecognition to listen, SpeechSynthesis to speak).
   ===================================================================== */
(function () {
  'use strict';

  const $ = id => document.getElementById(id);
  const store = {
    get(key, fallback) { try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch (e) { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ } },
  };
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const LANG_CODES = { en: 'en-GB', fr: 'fr-FR', es: 'es-ES' };
  const LANG_NAMES = { en: 'English', fr: 'French', es: 'Spanish' };

  /* ---------------- Rendering: markdown + maths ---------------- */

  // Maths is pulled out before markdown runs (markdown would mangle the
  // backslashes), the HTML is sanitised, then KaTeX output is put back.
  function render(md) {
    const maths = [];
    const keep = (tex, display) => { maths.push({ tex, display }); return `@@M${maths.length - 1}@@`; };
    let src = String(md || '')
      .replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => keep(t, true))
      .replace(/\\\[([\s\S]+?)\\\]/g, (_, t) => keep(t, true))
      .replace(/\\\(([\s\S]+?)\\\)/g, (_, t) => keep(t, false))
      .replace(/(^|[^\\$])\$([^$\n]+?)\$/g, (_, pre, t) => pre + keep(t, false));
    let html = window.marked ? marked.parse(src, { breaks: true }) : src.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
    if (window.DOMPurify) html = DOMPurify.sanitize(html);
    return html.replace(/@@M(\d+)@@/g, (_, i) => {
      const m = maths[i];
      try { return katex.renderToString(m.tex, { displayMode: m.display, throwOnError: false }); }
      catch (e) { return m.tex; }
    });
  }

  // Board lines sometimes come back as bare LaTeX without $ signs.
  function boardText(line) {
    const s = String(line || '').trim();
    if (!s.includes('$') && /\\[a-zA-Z]+|\^|_\{/.test(s)) return `$${s}$`;
    return s;
  }

  /* ---------------- Speaking (text-to-speech) ---------------- */

  const synth = window.speechSynthesis;
  let speakToken = 0;

  // Voice settings, chosen by the student in the 🔊 Voice panel.
  //   engine "device": the phone/computer's own voices (free, unlimited)
  //   engine "ai":     Google's natural voices (limited per day, uses more data)
  const AI_VOICES = [
    { id: 'Kore', who: 'Woman', desc: 'clear and calm' },
    { id: 'Aoede', who: 'Woman', desc: 'relaxed and friendly' },
    { id: 'Leda', who: 'Woman', desc: 'young and bright' },
    { id: 'Charon', who: 'Man', desc: 'calm teacher' },
    { id: 'Puck', who: 'Man', desc: 'lively and upbeat' },
    { id: 'Orus', who: 'Man', desc: 'firm and clear' },
  ];
  const voiceSettings = Object.assign(
    { engine: 'ai', aiVoice: 'Kore', device: {}, rate: 1, pitch: 1 },
    store.get('tutor-voice-settings', {}),
  );
  const saveVoiceSettings = () => store.set('tutor-voice-settings', voiceSettings);

  // Natural-sounding device voices first: Edge "Online (Natural)", Google,
  // Apple "Enhanced/Premium" voices sound far more human than the defaults.
  function voiceScore(v) {
    let score = 0;
    if (/natural|neural|online|enhanced|premium|wavenet/i.test(v.name)) score += 4;
    if (/google/i.test(v.name)) score += 2;
    if (!v.localService) score += 1;
    if (/compact|espeak/i.test(v.name)) score -= 3;
    return score;
  }
  function deviceVoices(base) {
    if (!synth) return [];
    return synth.getVoices()
      .filter(v => v.lang && v.lang.slice(0, 2).toLowerCase() === base)
      .sort((a, b) => voiceScore(b) - voiceScore(a) || a.name.localeCompare(b.name));
  }
  function pickVoice(lang) {
    const base = lang.slice(0, 2).toLowerCase();
    const list = deviceVoices(base);
    const chosen = voiceSettings.device[base];
    return (chosen && list.find(v => v.voiceURI === chosen)) || list[0] || null;
  }
  if (synth && synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = () => { synth.getVoices(); if (window.refreshVoicePanel) window.refreshVoicePanel(); };
  }

  // Turns maths and markdown into words a student can follow by ear.
  function speechText(text) {
    const words = math => math
      .replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, ' $1 over $2 ')
      .replace(/\\sqrt\{([^{}]*)\}/g, ' square root of $1 ')
      .replace(/\\(overline|bar)\{([^{}]*)\}/g, ' NOT, $2, ')
      .replace(/\^\{?2\}?/g, ' squared ').replace(/\^\{?3\}?/g, ' cubed ')
      .replace(/\^\{([^{}]*)\}|\^(\w)/g, ' to the power $1$2 ')
      .replace(/\\times|\\cdot/g, ' times ').replace(/\\div/g, ' divided by ')
      .replace(/\\pm/g, ' plus or minus ').replace(/\\(le|leq)\b/g, ' less than or equal to ')
      .replace(/\\(ge|geq)\b/g, ' greater than or equal to ').replace(/\\neq/g, ' not equal to ')
      .replace(/\\approx/g, ' approximately ').replace(/\\pi/g, ' pi ').replace(/\\theta/g, ' theta ')
      .replace(/\\(text|mathbf|mathrm|textbf)\{([^{}]*)\}/g, '$2')
      .replace(/\\[a-zA-Z]+/g, ' ').replace(/[{}]/g, '')
      .replace(/(\w)\s*-\s*(\w)/g, '$1 minus $2').replace(/=/g, ' equals ').replace(/\+/g, ' plus ');
    return String(text || '')
      .replace(/```[\s\S]*?```/g, ' (see the code on screen) ')
      .replace(/\$\$([\s\S]*?)\$\$/g, (_, m) => ` ${words(m)}. `)
      .replace(/\$([^$\n]+?)\$/g, (_, m) => ` ${words(m)} `)
      .replace(/^\s*[-*+]\s+/gm, '')
      .replace(/^\s*\|?[\s:|-]+\|[\s:|-]*$/gm, '')
      .replace(/\|/g, ', ')
      .replace(/[*_`#>]/g, '')
      .replace(/\s{2,}/g, ' ')
      .replace(/\n+/g, '. ')
      .trim();
  }

  // ---- Device voice: long text is split into sentences because some
  // browsers cut off long utterances.
  async function speakDevice(clean, token, lang, rate) {
    if (!synth) return;
    const voice = pickVoice(lang);
    const chunks = clean.match(/[^.!?。]+[.!?。]*\s*/g) || [clean];
    for (const chunk of chunks) {
      if (token !== speakToken) return;
      if (!chunk.trim()) continue;
      await new Promise(resolve => {
        const u = new SpeechSynthesisUtterance(chunk.trim());
        u.lang = voice ? voice.lang : lang;
        if (voice) u.voice = voice;
        u.rate = rate;
        u.pitch = voiceSettings.pitch;
        u.onend = u.onerror = resolve;
        // Safety net: never hang the class if the browser never fires onend.
        setTimeout(resolve, 2500 + chunk.length * 110 / rate);
        synth.speak(u);
      });
    }
  }

  // ---- Natural AI voice: audio comes from /api/tutor (task "speak").
  // Clips are cached, so "Listen again" and prefetched class steps cost nothing extra.
  const AI_MAX_CHARS = 700;
  const aiClips = new Map();
  let aiVoiceOff = false;          // set when today's limit is reached

  // One reusable player, unlocked by the student's first tap: phones
  // (iPhones especially) block audio that wasn't started by a tap.
  const player = new Audio();
  const SILENT_WAV = 'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAA=';
  document.addEventListener('click', () => { player.src = SILENT_WAV; player.play().catch(() => {}); }, { once: true, capture: true });

  function aiClip(clean) {
    const key = voiceSettings.aiVoice + '|' + clean;
    if (!aiClips.has(key)) {
      const p = fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: 'speak', text: clean, voice: voiceSettings.aiVoice }),
      })
        .then(r => r.json().then(d => ({ status: r.status, d })))
        .then(({ status, d }) => {
          if (!d.ok) {
            if (status === 429) { aiVoiceOff = true; toast(d.error); }
            throw new Error(d.error || 'voice failed');
          }
          const bytes = Uint8Array.from(atob(d.audio), c => c.charCodeAt(0));
          return URL.createObjectURL(new Blob([bytes], { type: d.mime || 'audio/wav' }));
        });
      p.catch(() => aiClips.delete(key));
      aiClips.set(key, p);
      if (aiClips.size > 60) aiClips.delete(aiClips.keys().next().value);
    }
    return aiClips.get(key);
  }

  // Splits long text into clips of whole sentences, each under the server limit.
  function aiChunks(clean) {
    const sentences = clean.match(/[^.!?。]+[.!?。]*\s*/g) || [clean];
    const out = [];
    let cur = '';
    for (const s of sentences) {
      if ((cur + s).length > 400 && cur) { out.push(cur.trim()); cur = ''; }
      cur += s;
    }
    if (cur.trim()) out.push(cur.trim().slice(0, AI_MAX_CHARS));
    return out;
  }

  async function speakAI(clean, token, rate) {
    const chunks = aiChunks(clean);
    if (chunks.length > 4) return false;      // very long answers: the device voice saves data
    for (let i = 0; i < chunks.length; i++) {
      if (token !== speakToken) return true;
      let url;
      try { url = await aiClip(chunks[i]); } catch (e) { return i > 0; }
      if (chunks[i + 1]) aiClip(chunks[i + 1]).catch(() => {});   // fetch the next clip while this one plays
      if (token !== speakToken) return true;
      await new Promise(resolve => {
        const done = () => { player.onended = player.onerror = player.onpause = null; resolve(); };
        player.onended = player.onerror = player.onpause = null;
        player.src = url;
        player.playbackRate = rate;
        player.onended = player.onerror = player.onpause = done;
        player.play().catch(done);
      });
    }
    return true;
  }

  function prefetchSpeech(text) {
    if (voiceSettings.engine !== 'ai' || aiVoiceOff) return;
    const first = aiChunks(speechText(text))[0];
    if (first) aiClip(first).catch(() => {});
  }

  // Speaks text and resolves when finished (or stopped).
  async function speak(text, opts = {}) {
    const token = ++speakToken;
    player.pause();
    if (synth) synth.cancel();
    const lang = opts.lang || 'en-GB';
    const clean = opts.raw ? String(text).trim() : speechText(text);
    if (!clean) return;
    const rate = (opts.rate || 1) * voiceSettings.rate;
    if (voiceSettings.engine === 'ai' && !aiVoiceOff) {
      const done = await speakAI(clean, token, rate);
      if (done || token !== speakToken) return;
    }
    await speakDevice(clean, token, lang, rate);
  }
  function stopSpeaking() {
    speakToken++;
    player.pause();
    if (synth) synth.cancel();
  }

  function toast(message) {
    let t = document.getElementById('tutorToast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'tutorToast';
      t.className = 'toast';
      t.setAttribute('role', 'status');
      document.body.appendChild(t);
    }
    t.textContent = message;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.classList.remove('show'), 5000);
  }

  /* ---------------- Listening (speech-to-text) ---------------- */

  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let activeRec = null;

  function stopListening() { if (activeRec) { try { activeRec.stop(); } catch (e) { /* already stopped */ } } }

  // btn: mic button; input: field to fill; getLang(): language code;
  // onDone(text): called with the final words (for auto-send).
  function setupMic(btn, input, getLang, onDone) {
    if (!Recognition) { btn.hidden = true; btn.style.display = 'none'; return; }
    btn.addEventListener('click', () => {
      if (activeRec) { stopListening(); return; }
      stopSpeaking();
      const rec = new Recognition();
      rec.lang = getLang();
      rec.interimResults = true;
      rec.continuous = false;
      const before = input.value ? input.value.trim() + ' ' : '';
      let heard = '';
      rec.onresult = e => {
        heard = Array.from(e.results).map(r => r[0].transcript).join('');
        input.value = before + heard;
        input.dispatchEvent(new Event('input'));
      };
      rec.onerror = e => {
        if (e.error === 'not-allowed' || e.error === 'service-not-allowed') alert('Please allow the microphone to speak to the tutor.');
      };
      rec.onend = () => {
        activeRec = null;
        btn.classList.remove('listening');
        if (heard.trim() && onDone) onDone(input.value.trim());
      };
      activeRec = rec;
      btn.classList.add('listening');
      try { rec.start(); } catch (e) { activeRec = null; btn.classList.remove('listening'); }
    });
  }

  /* ---------------- Uploading notes ---------------- */

  const MAX_BYTES = 3 * 1024 * 1024;

  // Photos are resized (phone photos are often 5–10 MB); PDFs must be under 3 MB.
  async function readNotes(file) {
    if (!file) return null;
    if (file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      try {
        const img = await new Promise((resolve, reject) => {
          const i = new Image(); i.onload = () => resolve(i); i.onerror = reject; i.src = url;
        });
        const scale = Math.min(1, 1800 / Math.max(img.width, img.height));
        const canvas = document.createElement('canvas');
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
        const data = canvas.toDataURL('image/jpeg', 0.85);
        return { name: file.name, type: 'image/jpeg', data: data.split(',')[1] };
      } finally {
        URL.revokeObjectURL(url);
      }
    }
    if (file.type !== 'application/pdf') throw new Error('Please upload a PDF or a photo (JPG, PNG).');
    if (file.size > MAX_BYTES) throw new Error('That PDF is too big (max 3 MB). Try uploading a photo of the pages instead.');
    const data = await new Promise((resolve, reject) => {
      const r = new FileReader(); r.onload = () => resolve(r.result); r.onerror = reject; r.readAsDataURL(file);
    });
    return { name: file.name, type: file.type, data: String(data).split(',')[1] };
  }

  function showFileChip(chip, notes, onRemove) {
    chip.innerHTML = '';
    if (!notes) { chip.hidden = true; return; }
    const label = document.createElement('span');
    label.textContent = `📎 ${notes.name}`;
    const x = document.createElement('button');
    x.type = 'button'; x.textContent = '✕'; x.title = 'Remove'; x.setAttribute('aria-label', 'Remove file');
    x.onclick = onRemove;
    chip.append(label, x);
    chip.hidden = false;
  }

  /* ---------------- API ---------------- */

  const levelSelect = $('levelSelect');
  levelSelect.value = store.get('tutor-level', '');
  levelSelect.addEventListener('change', () => store.set('tutor-level', levelSelect.value));

  // Lesson the student came from (saved by the lesson page's "Stuck?" buttons).
  // Its content is sent along so answers follow the same method and notation.
  let lessonCtx = null;
  try {
    const saved = JSON.parse(localStorage.getItem('tutor-lesson-ctx') || 'null');
    if (saved && Date.now() - saved.at < 2 * 3600 * 1000) lessonCtx = saved;
  } catch (e) { /* storage blocked */ }

  function withLesson(body) {
    if (!lessonCtx || !['chat', 'lesson', 'ask'].includes(body.task)) return body;
    // A live class on another topic doesn't need this lesson.
    if (body.task === 'lesson' && body.topic && !body.topic.toLowerCase().includes(lessonCtx.title.toLowerCase())) return body;
    return { ...body, lessonText: lessonCtx.text };
  }

  async function post(body) {
    try {
      return await fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(withLesson({ level: levelSelect.value, ...body })),
      });
    } catch (e) {
      throw new Error("Can't reach the tutor. Check your internet connection and try again.");
    }
  }

  async function api(body) {
    const res = await post(body);
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      if (res.status === 413) throw new Error('That file is too big. Please upload a file under 3 MB.');
      throw new Error(data.error || 'Something went wrong. Please try again.');
    }
    if (window.gtag) gtag('event', 'tutor_' + body.task, { cached: !!data.cached });
    return data;
  }

  // Chat answers arrive word by word: onText(fullTextSoFar) is called as they come.
  async function apiStream(body, onText) {
    const res = await post({ ...body, stream: true });
    const type = res.headers.get('content-type') || '';
    if (!type.includes('ndjson')) {                       // errors (limit, bad file…) come back as normal JSON
      const data = await res.json().catch(() => ({}));
      if (res.status === 413) throw new Error('That file is too big. Please upload a file under 3 MB.');
      throw new Error(data.error || 'Something went wrong. Please try again.');
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = '', full = '', end = null;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.trim()) continue;
        let msg;
        try { msg = JSON.parse(line); } catch (e) { continue; }
        if (msg.t) { full += msg.t; onText(full); }
        if (msg.error) throw Object.assign(new Error(msg.error), { partial: full });
        if (msg.done) end = msg;
      }
    }
    if (!full.trim()) throw new Error('Something went wrong. Please try again.');
    if (window.gtag) gtag('event', 'tutor_chat', { cached: !!(end && end.cached) });
    return { reply: full.trim(), id: end && end.id, truncated: !end || end.truncated, cached: !!(end && end.cached) };
  }

  // 👍 / 👎 under an answer. getInfo() → { kind, question, answer, id }
  function rateButtons(getInfo) {
    const box = document.createElement('span');
    box.className = 'rate';
    const send = rating => {
      const info = getInfo();
      fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: 'rate', rating, level: levelSelect.value, lessonTitle: lessonCtx ? lessonCtx.title : '', ...info }),
      }).catch(() => {});
      if (window.gtag) gtag('event', 'tutor_rating', { rating, kind: info.kind });
      box.textContent = rating === 'up' ? '👍 Thanks!' : '👎 Thanks, we will improve it.';
    };
    const up = toolButton('👍', () => send('up'));
    const down = toolButton('👎', () => send('down'));
    up.title = 'Helpful'; up.setAttribute('aria-label', 'This answer was helpful');
    down.title = 'Not helpful'; down.setAttribute('aria-label', 'This answer was not helpful');
    box.append(up, down);
    return box;
  }

  /* ---------------- Shared chat helpers ---------------- */

  function autoGrow(el) {
    el.addEventListener('input', () => { el.style.height = 'auto'; el.style.height = Math.min(el.scrollHeight, 160) + 'px'; });
  }
  function enterToSend(el, form) {
    el.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
    });
  }
  function scrollDown(el) { el.scrollTop = el.scrollHeight; }

  function addBubble(log, role, html, opts = {}) {
    const row = document.createElement('div');
    row.className = `msg ${role === 'user' ? 'user' : 'bot'}`;
    const av = document.createElement('div');
    av.className = 'avatar';
    av.textContent = role === 'user' ? '🧑🏾' : '🎓';
    const bubble = document.createElement('div');
    bubble.className = 'bubble' + (role === 'user' ? '' : ' rich');
    if (opts.attach) {
      const a = document.createElement('span'); a.className = 'attach'; a.textContent = `📎 ${opts.attach}`;
      bubble.appendChild(a);
    }
    if (role === 'user') bubble.appendChild(document.createTextNode(html));
    else bubble.insertAdjacentHTML('beforeend', html);
    row.append(av, bubble);
    log.appendChild(row);
    scrollDown(log);
    return bubble;
  }
  function addTyping(log) {
    const row = document.createElement('div');
    row.className = 'msg bot';
    row.innerHTML = '<div class="avatar">🎓</div><div class="bubble typing" aria-label="Tutor is typing"><span></span><span></span><span></span></div>';
    log.appendChild(row);
    scrollDown(log);
    return row;
  }
  function addError(log, message) {
    const div = document.createElement('div');
    div.className = 'error-msg';
    div.textContent = '⚠️ ' + message;
    log.appendChild(div);
    scrollDown(log);
  }
  function toolButton(label, onClick) {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.onclick = onClick;
    return b;
  }

  /* =========================================================
     TABS
     ========================================================= */
  const tabs = ['ask', 'class', 'lang'];
  function openTab(name) {
    stopSpeaking(); stopListening();
    if (name !== 'class') classPause();
    tabs.forEach(t => {
      $('tab-' + t).setAttribute('aria-selected', String(t === name));
      $('panel-' + t).hidden = t !== name;
    });
    store.set('tutor-tab', name);
  }
  tabs.forEach(t => $('tab-' + t).addEventListener('click', () => openTab(t)));

  /* =========================================================
     1. ASK A TUTOR
     ========================================================= */
  const askLog = $('askLog'), askForm = $('askForm'), askInput = $('askInput'), askSend = $('askSend');
  let askMessages = store.get('tutor-chat', []);
  let askNotes = null;
  let askMode = 'explain';
  let askBusy = false;

  function setMode(mode) {
    askMode = mode;
    document.querySelectorAll('.mode').forEach(b => {
      const on = b.dataset.mode === mode;
      b.classList.toggle('on', on);
      b.setAttribute('aria-checked', String(on));
    });
  }
  document.querySelectorAll('.mode').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

  function addBotTools(bubble, text, question, id) {
    const tools = document.createElement('div');
    tools.className = 'bubble-tools';
    tools.append(
      toolButton('🔊 Listen', () => speak(text)),
      toolButton('⏹ Stop', stopSpeaking),
      toolButton('📋 Copy', () => navigator.clipboard && navigator.clipboard.writeText(text)),
    );
    if (question) tools.append(rateButtons(() => ({ kind: 'chat', question, answer: text, id })));
    bubble.appendChild(tools);
  }

  function botBubble(text, question, id) {
    const bubble = addBubble(askLog, 'bot', render(text));
    addBotTools(bubble, text, question, id);
  }

  function renderAskHistory() {
    if (!askMessages.length) return;
    $('askEmpty').hidden = true;
    askMessages.forEach((m, i) => m.role === 'user'
      ? addBubble(askLog, 'user', m.content, { attach: m.attach })
      : botBubble(m.content, askMessages[i - 1] && askMessages[i - 1].content, m.id));
  }

  async function askSendMessage(text) {
    if (askBusy) return;
    text = (text || '').trim();
    if (!text && askNotes) text = 'Please explain these notes in detail, step by step.';
    if (!text) return;
    $('askEmpty').hidden = true;
    stopSpeaking();
    const isNewFile = askNotes && !askNotes.sent;
    const msg = { role: 'user', content: text };
    if (isNewFile) { msg.attach = askNotes.name; askNotes.sent = true; }
    askMessages.push(msg);
    addBubble(askLog, 'user', text, { attach: msg.attach });
    askInput.value = ''; askInput.style.height = 'auto';
    askBusy = true; askSend.disabled = true;
    const typing = addTyping(askLog);
    let bubble = null, pending = null;
    // Re-draw at most once per frame while the answer streams in.
    const show = full => {
      pending = full;
      if (!bubble) { typing.remove(); bubble = addBubble(askLog, 'bot', ''); }
      requestAnimationFrame(() => {
        if (pending === null) return;
        const nearBottom = askLog.scrollHeight - askLog.scrollTop - askLog.clientHeight < 80;
        bubble.innerHTML = render(pending);
        pending = null;
        if (nearBottom) scrollDown(askLog);
      });
    };
    try {
      const { reply, id, truncated } = await apiStream({
        task: 'chat',
        mode: askMode,
        messages: askMessages.map(m => ({ role: m.role, content: m.content })),
        file: askNotes,
      }, show);
      const final = truncated ? `${reply}\n\n_(Answer cut short. Type "continue" to get the rest.)_` : reply;
      pending = null;
      if (!bubble) { typing.remove(); bubble = addBubble(askLog, 'bot', ''); }
      bubble.innerHTML = render(final);
      addBotTools(bubble, final, text, id);
      askMessages.push({ role: 'assistant', content: final, id });
      if ($('askSpeak').checked) speak(final);
    } catch (e) {
      pending = null;
      typing.remove();
      if (bubble) bubble.closest('.msg').remove();
      askMessages.pop();
      addError(askLog, e.message);
      askInput.value = text;
    } finally {
      askBusy = false; askSend.disabled = false;
      store.set('tutor-chat', askMessages.slice(-30));
    }
  }

  askForm.addEventListener('submit', e => { e.preventDefault(); askSendMessage(askInput.value); });
  autoGrow(askInput); enterToSend(askInput, askForm);
  setupMic($('askMic'), askInput, () => /[àâçéèêëîïôûùüÿœ]/i.test(askInput.value) ? 'fr-FR' : 'en-GB');

  $('askFile').addEventListener('change', async e => {
    const file = e.target.files[0];
    e.target.value = '';
    if (!file) return;
    try {
      askNotes = await readNotes(file);
      showFileChip($('askFileChip'), askNotes, () => { askNotes = null; showFileChip($('askFileChip'), null); });
      askInput.placeholder = 'Ask about your notes, or just press Send to have them explained…';
      askInput.focus();
    } catch (err) {
      alert(err.message);
    }
  });

  $('askClear').addEventListener('click', () => {
    stopSpeaking();
    askMessages = []; askNotes = null;
    store.set('tutor-chat', []);
    showFileChip($('askFileChip'), null);
    forgetLesson();
    askLog.querySelectorAll('.msg, .error-msg').forEach(n => n.remove());
    $('askEmpty').hidden = false;
    askInput.placeholder = 'Ask a question…';
  });

  document.querySelectorAll('#askEmpty .chip').forEach(chip => chip.addEventListener('click', () => {
    if (chip.dataset.mode) setMode(chip.dataset.mode);
    askSendMessage(chip.dataset.q);
  }));

  renderAskHistory();

  /* =========================================================
     2. LIVE CLASS
     ========================================================= */
  const board = $('board'), caption = $('caption');
  let lesson = null;          // { title, intro, steps: [{board, say, check}], summary }
  let classNotes = null;
  let idx = -1;               // -1 intro, 0..n-1 steps, n = summary
  let runToken = 0;           // bumping it stops the running class
  let playing = false;
  let notesByStep = {};       // board notes added by questions: { stepIndex: [{who, lines, right}] }
  let answered = {};          // check questions already answered
  let waitTurn = null;        // resolves when the student answers a "your turn" question

  const classVoice = $('classVoice'), classAuto = $('classAuto');
  classVoice.checked = store.get('tutor-voice', true);
  classVoice.addEventListener('change', () => { store.set('tutor-voice', classVoice.checked); if (!classVoice.checked) stopSpeaking(); });

  function setPlaying(on) {
    playing = on;
    const btn = $('ctlPlay');
    btn.textContent = on ? '⏸' : '▶';
    btn.title = on ? 'Pause' : 'Play';
    btn.setAttribute('aria-label', btn.title);
  }

  function setCaption(text, who = 'Teacher') {
    caption.innerHTML = '';
    if (!text) return;
    const w = document.createElement('span'); w.className = 'who'; w.textContent = who + ':';
    caption.append(w, document.createTextNode(text));
  }

  async function teacherSays(text) {
    setCaption(text);
    if (classVoice.checked) await speak(text);
    else await sleep(Math.min(9000, 1800 + text.length * 45));
  }

  function drawBoard(writeIndex) {
    board.innerHTML = '';
    if (!lesson) return;
    const last = Math.min(idx, lesson.steps.length - 1);
    for (let i = 0; i <= last; i++) {
      const step = lesson.steps[i];
      const line = document.createElement('div');
      line.className = 'board-line' + (i === idx ? ' current' : ' done') + (i === writeIndex ? ' write' : '');
      line.innerHTML = `<span class="num">${i + 1}.</span><div class="content rich">${render(boardText(step.board))}</div>`;
      board.appendChild(line);
      (notesByStep[i] || []).forEach(note => board.appendChild(noteEl(note)));
    }
    if (idx >= lesson.steps.length && lesson.summary) {
      board.appendChild(noteEl({ who: '✅ Summary', lines: [lesson.summary], right: true }));
    }
    const cur = board.querySelector('.board-line.current') || board.lastElementChild;
    if (cur) cur.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    $('classProgress').style.width = `${Math.max(0, Math.min(1, (idx + 1) / (lesson.steps.length + 1))) * 100}%`;
    $('ctlPrev').disabled = idx <= 0;
    $('ctlNext').disabled = idx >= lesson.steps.length;
  }

  function noteEl(note) {
    const div = document.createElement('div');
    div.className = 'board-note' + (note.right ? ' right' : '');
    const who = document.createElement('span'); who.className = 'who'; who.textContent = note.who;
    div.appendChild(who);
    const body = document.createElement('div');
    body.className = 'rich';
    body.innerHTML = note.lines.map(l => render(boardText(l))).join('');
    div.appendChild(body);
    return div;
  }

  function addNote(note) {
    const at = Math.max(0, Math.min(idx, lesson.steps.length - 1));
    (notesByStep[at] = notesByStep[at] || []).push(note);
    drawBoard();
  }

  // Plays the class from step `from`. Every pause/skip bumps runToken,
  // which stops this loop at its next check.
  async function playFrom(from) {
    if (!lesson) return;
    const token = ++runToken;
    stopSpeaking();
    setPlaying(true);
    $('turnBox').hidden = true;
    for (let k = from; k <= lesson.steps.length; k++) {
      if (token !== runToken) return;
      idx = k;
      if (k === -1) {
        drawBoard();
        prefetchSpeech(lesson.steps[0].say);
        await teacherSays(lesson.intro);
        continue;
      }
      if (k === lesson.steps.length) {
        drawBoard();
        await teacherSays(lesson.summary || 'That is the end of our class. Well done!');
        if (token === runToken) {
          setPlaying(false);
          setCaption('Class finished 🎉 Raise your hand ✋ to ask a question, or start a new class.', 'Teacher');
          const ask = document.createElement('span');
          ask.className = 'class-rate';
          ask.append(' Was this class helpful? ', rateButtons(() => ({
            kind: 'class', question: lesson.title, id: lesson.id,
            answer: lesson.steps.map((st, i) => `${i + 1}. ${st.board}`).join('\n'),
          })));
          caption.appendChild(ask);
        }
        return;
      }
      const step = lesson.steps[k];
      drawBoard(k);
      prefetchSpeech(lesson.steps[k + 1] ? lesson.steps[k + 1].say : lesson.summary);
      await teacherSays(step.say);
      if (token !== runToken) return;
      if (step.check && step.check.question && !answered[k]) {
        await askTurn(step.check, token);
        if (token !== runToken) return;
      }
      if (!classAuto.checked) { setPlaying(false); return; }
      await sleep(500);
    }
  }

  function classPause() {
    runToken++;
    stopSpeaking();
    setPlaying(false);
    if (waitTurn) { waitTurn(); waitTurn = null; }
  }

  function resumeClass() {
    if (!lesson) return;
    $('handBox').hidden = true;
    $('ctlHand').classList.remove('raised');
    const next = idx >= lesson.steps.length ? lesson.steps.length : idx + 1;
    playFrom(Math.min(next, lesson.steps.length));
  }

  $('ctlPlay').addEventListener('click', () => {
    if (playing) { classPause(); return; }
    $('handBox').hidden = true;
    $('ctlHand').classList.remove('raised');
    if (idx >= lesson.steps.length) { notesByStep = {}; answered = {}; playFrom(-1); }
    else playFrom(Math.max(idx, -1));
  });
  $('ctlNext').addEventListener('click', () => { if (lesson) { $('handBox').hidden = true; playFrom(Math.min(idx + 1, lesson.steps.length)); } });
  $('ctlPrev').addEventListener('click', () => { if (lesson) { $('handBox').hidden = true; playFrom(Math.max(idx - 1, 0)); } });

  // "Your turn" — the class waits until the student answers or skips.
  function askTurn(check, token) {
    setPlaying(false);
    $('turnQuestion').textContent = check.question;
    $('turnBox').hidden = false;
    $('turnInput').value = '';
    setTimeout(() => $('turnInput').focus({ preventScroll: true }), 100);
    if (classVoice.checked) speak('Your turn. ' + check.question, { raw: true });
    return new Promise(resolve => {
      waitTurn = () => { waitTurn = null; resolve(); };
      $('turnBox').dataset.step = String(idx);
      $('turnBox').dataset.token = String(token);
    });
  }

  // Marks obviously-right answers instantly, without using the AI quota.
  // Returns true when the answer clearly matches, null when unsure.
  const NUMBER_WORDS = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, zéro: 0, un: 1, deux: 2, trois: 3, quatre: 4, cinq: 5 };
  function normalise(s) {
    return String(s).toLowerCase()
      .replace(/\$|\\[a-z]+|[{}]/g, ' ')
      .replace(/[−–]/g, '-')
      .replace(/\b(negative|minus|moins)\s*/g, '-')
      .replace(/\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|zéro|un|deux|trois|quatre|cinq)\b/g, w => NUMBER_WORDS[w])
      .replace(/-\s+(?=\d)/g, '-');
  }
  function quickCheck(student, expected) {
    const nums = s => (normalise(s).match(/-?\d+(?:[.,]\d+)?/g) || []).map(n => Number(n.replace(',', '.'))).sort((a, b) => a - b);
    const want = nums(expected), got = nums(student);
    if (want.length) return want.length === got.length && want.every((n, i) => n === got[i]) ? true : null;
    const words = s => normalise(s).replace(/[^a-zà-ÿ0-9 ]/g, ' ').split(/\s+/).filter(w => w.length > 2 && !['the', 'and', 'les', 'des'].includes(w));
    const w = words(expected), g = words(student);
    return w.length && w.every(x => g.includes(x)) ? true : null;
  }

  // Shows a reassuring message if the AI takes a while; returns a cancel function.
  function slowNotice() {
    const t = setTimeout(() => setCaption('Still thinking… the AI is busy right now, please hang on a few seconds.', 'Teacher'), 9000);
    return () => clearTimeout(t);
  }

  $('turnForm').addEventListener('submit', async e => {
    e.preventDefault();
    const answer = $('turnInput').value.trim();
    if (!answer) return;
    const step = lesson.steps[idx];
    if (quickCheck(answer, step.check.answer)) {
      answered[idx] = true;
      $('turnBox').hidden = true;
      addNote({ who: `🙋 You answered: “${answer}”`, lines: [`✔ ${step.check.answer}`], right: true });
      setPlaying(true);
      const praise = ['Correct, well done!', 'Excellent, that is right!', 'Very good, you got it!'][Math.floor(Math.random() * 3)];
      await teacherSays(praise);
      if (waitTurn) waitTurn();
      return;
    }
    const btn = e.submitter || $('turnForm').querySelector('.send');
    btn.disabled = true;
    setCaption('Checking your answer…', 'Teacher');
    const stopNotice = slowNotice();
    try {
      const { data } = await api({
        task: 'ask', lesson, step: idx, question: answer,
        checkQuestion: step.check.question, checkAnswer: step.check.answer, file: classNotes,
      });
      stopNotice();
      answered[idx] = true;
      $('turnBox').hidden = true;
      addNote({ who: `🙋 You answered: “${answer}”`, lines: data.board && data.board.length ? data.board : [], right: data.correct === true });
      setPlaying(true);
      await teacherSays(data.say);
      if (waitTurn) waitTurn();
    } catch (err) {
      stopNotice();
      setCaption(err.message, '⚠️');
    } finally {
      btn.disabled = false;
    }
  });

  $('turnSkip').addEventListener('click', async () => {
    const step = lesson.steps[idx];
    answered[idx] = true;
    $('turnBox').hidden = true;
    addNote({ who: '💡 Answer', lines: [step.check.answer], right: true });
    setPlaying(true);
    await teacherSays('The answer is: ' + speechText(step.check.answer));
    if (waitTurn) waitTurn();
  });

  // ✋ Raise hand — pause, take the question, answer on the board, then continue.
  $('ctlHand').addEventListener('click', () => {
    if (!lesson) return;
    classPause();
    $('turnBox').hidden = true;
    $('ctlHand').classList.add('raised');
    $('handBox').hidden = false;
    setCaption('Yes? What is your question?', 'Teacher');
    if (classVoice.checked) speak('Yes? What is your question?', { raw: true });
    setTimeout(() => $('handInput').focus({ preventScroll: true }), 100);
  });
  $('handCancel').addEventListener('click', resumeClass);

  $('handForm').addEventListener('submit', async e => {
    e.preventDefault();
    const question = $('handInput').value.trim();
    if (!question) return;
    const btn = $('handForm').querySelector('.send');
    btn.disabled = true;
    setCaption('Good question, let me explain…', 'Teacher');
    const stopNotice = slowNotice();
    try {
      const { data } = await api({ task: 'ask', lesson, step: Math.max(0, Math.min(idx, lesson.steps.length - 1)), question, file: classNotes });
      stopNotice();
      $('handInput').value = '';
      $('handBox').hidden = true;
      $('ctlHand').classList.remove('raised');
      addNote({ who: `✋ You asked: “${question}”`, lines: data.board || [] });
      const token = ++runToken;
      setPlaying(true);
      await teacherSays(data.say);
      if (token !== runToken) return;
      setPlaying(false);
      setCaption('Any other question? Raise your hand ✋ again, or press ▶ to continue the class.', 'Teacher');
    } catch (err) {
      stopNotice();
      setCaption(err.message, '⚠️');
    } finally {
      btn.disabled = false;
    }
  });

  async function startClass(topic) {
    topic = (topic || '').trim();
    if (!topic && !classNotes) { $('classTopic').focus(); return; }
    $('classForm').querySelector('.send').classList.remove('pulse');
    stopSpeaking();
    // Unlocks speech on mobile browsers, which only allow it after a tap.
    if (synth) synth.speak(new SpeechSynthesisUtterance(''));
    $('classSetup').hidden = true;
    $('classroom').hidden = false;
    lesson = null; notesByStep = {}; answered = {}; idx = -1;
    $('classTitle').textContent = topic || (classNotes && classNotes.name) || 'Your class';
    board.innerHTML = '<div class="board-empty">✍️ Preparing your class…</div>';
    setCaption('One moment, I am preparing the lesson on the board…');
    $('turnBox').hidden = true; $('handBox').hidden = true;
    const stopNotice = slowNotice();
    try {
      const { data, id } = await api({ task: 'lesson', topic, file: classNotes });
      if (data) data.id = id;
      stopNotice();
      if (!data || !Array.isArray(data.steps) || !data.steps.length) throw new Error('The tutor could not prepare that class. Try a more specific topic.');
      lesson = data;
      $('classTitle').textContent = data.title || topic;
      playFrom(-1);
    } catch (err) {
      stopNotice();
      board.innerHTML = '';
      const div = document.createElement('div'); div.className = 'board-empty'; div.textContent = '⚠️ ' + err.message;
      board.appendChild(div);
      setCaption('');
      const retry = document.createElement('button');
      retry.className = 'send'; retry.style.marginTop = '14px'; retry.textContent = 'Try again';
      retry.onclick = () => startClass(topic);
      div.appendChild(document.createElement('br'));
      div.appendChild(retry);
    }
  }

  $('classForm').addEventListener('submit', e => { e.preventDefault(); startClass($('classTopic').value); });
  document.querySelectorAll('#classSetup .chip').forEach(chip => chip.addEventListener('click', () => {
    $('classTopic').value = chip.dataset.topic;
    startClass(chip.dataset.topic);
  }));
  $('classFile').addEventListener('change', async e => {
    const file = e.target.files[0];
    e.target.value = '';
    if (!file) return;
    try {
      classNotes = await readNotes(file);
      showFileChip($('classFileChip'), classNotes, () => { classNotes = null; showFileChip($('classFileChip'), null); });
      $('classTopic').placeholder = 'Optional: which part of the notes? Or just press Start class';
    } catch (err) {
      alert(err.message);
    }
  });
  $('classNew').addEventListener('click', () => {
    classPause();
    lesson = null;
    $('classroom').hidden = true;
    $('classSetup').hidden = false;
    $('classTopic').value = '';
  });

  const classLang = () => (/[àâçéèêëîïôûùüÿœ]/i.test(lesson ? lesson.title : '') ? 'fr-FR' : 'en-GB');
  setupMic($('handMic'), $('handInput'), classLang, () => $('handForm').requestSubmit());
  setupMic($('turnMic'), $('turnInput'), classLang, () => $('turnForm').requestSubmit());

  /* =========================================================
     3. LANGUAGES
     ========================================================= */
  const langLog = $('langLog'), langForm = $('langForm'), langInput = $('langInput');
  const langTarget = $('langTarget'), langHelper = $('langHelper'), langLevel = $('langLevel');
  let langMessages = [];
  let langScenario = 'free conversation about everyday life';
  let langBusy = false;

  const saved = store.get('tutor-lang', null);
  if (saved) { langTarget.value = saved.target; langHelper.value = saved.helper; langLevel.value = saved.level; }

  // You can't learn English with explanations in English as a beginner, etc.
  function fixHelper() {
    if (langTarget.value === langHelper.value) langHelper.value = langTarget.value === 'en' ? 'fr' : 'en';
  }
  langTarget.addEventListener('change', fixHelper);
  langHelper.addEventListener('change', () => {
    if (langTarget.value === langHelper.value) langTarget.value = langHelper.value === 'en' ? 'fr' : 'en';
  });
  fixHelper();

  document.querySelectorAll('#langScenarios .chip').forEach(chip => chip.addEventListener('click', () => {
    document.querySelectorAll('#langScenarios .chip').forEach(c => c.classList.remove('on'));
    chip.classList.add('on');
    langScenario = chip.dataset.scenario;
  }));

  const langSpeakOpts = () => ({ lang: LANG_CODES[langTarget.value], raw: true, rate: langLevel.value === 'beginner' ? 0.85 : 1 });

  function langBotBubble(data) {
    const bubble = addBubble(langLog, 'bot', '');
    const reply = document.createElement('div');
    reply.textContent = data.reply;
    const tr = document.createElement('span');
    tr.className = 'tr'; tr.textContent = data.translation || '';
    tr.hidden = !$('langShowTr').checked;
    bubble.append(reply, tr);
    if (data.words && data.words.length) {
      const words = document.createElement('div');
      words.className = 'words';
      data.words.forEach(w => {
        const s = document.createElement('span');
        const b = document.createElement('b'); b.textContent = w.word;
        s.append(b, document.createTextNode(' — ' + w.meaning));
        words.appendChild(s);
      });
      bubble.appendChild(words);
    }
    if (data.tip) {
      const tip = document.createElement('span'); tip.className = 'tip'; tip.textContent = '💡 ' + data.tip;
      bubble.appendChild(tip);
    }
    const tools = document.createElement('div');
    tools.className = 'bubble-tools';
    tools.append(
      toolButton('🔊 Listen again', () => speak(data.reply, langSpeakOpts())),
      toolButton('🐢 Slowly', () => speak(data.reply, { ...langSpeakOpts(), rate: 0.7 })),
      toolButton('🔤 Translate', () => { tr.hidden = !tr.hidden; }),
      rateButtons(() => ({
        kind: 'language',
        question: (langMessages.filter(m => m.role === 'user').pop() || {}).content || '(start)',
        answer: `${data.reply}\nCorrections: ${(data.corrections || []).map(c => `${c.wrong} → ${c.right}`).join('; ') || 'none'}`,
      })),
    );
    bubble.appendChild(tools);
    scrollDown(langLog);
  }

  function corrections(list) {
    const box = document.createElement('div');
    if (!list || !list.length) {
      box.className = 'fixes ok';
      box.textContent = '✅ No mistakes — well done!';
    } else {
      box.className = 'fixes';
      const head = document.createElement('strong');
      head.textContent = `✏️ ${list.length} correction${list.length > 1 ? 's' : ''}`;
      const ul = document.createElement('ul');
      list.forEach(c => {
        const li = document.createElement('li');
        const w = document.createElement('span'); w.className = 'wrong'; w.textContent = c.wrong;
        const r = document.createElement('span'); r.className = 'right'; r.textContent = c.right;
        const why = document.createElement('span'); why.className = 'why'; why.textContent = c.why;
        li.append(w, document.createTextNode(' → '), r, why);
        ul.appendChild(li);
      });
      box.append(head, ul);
    }
    langLog.appendChild(box);
    scrollDown(langLog);
  }

  async function langTurn(text) {
    if (langBusy) return;
    langBusy = true;
    langForm.querySelector('.send').disabled = true;
    if (text) {
      langMessages.push({ role: 'user', content: text });
      addBubble(langLog, 'user', text);
      langInput.value = ''; langInput.style.height = 'auto';
    }
    const typing = addTyping(langLog);
    try {
      const { data } = await api({
        task: 'language',
        target: langTarget.value, helper: langHelper.value, languageLevel: langLevel.value,
        scenario: langScenario, messages: langMessages,
      });
      typing.remove();
      if (text) corrections(data.corrections);
      langMessages.push({ role: 'assistant', content: data.reply });
      langBotBubble(data);
      if ($('langSpeak').checked) speak(data.reply, langSpeakOpts());
    } catch (e) {
      typing.remove();
      if (text) { langMessages.pop(); langInput.value = text; }
      addError(langLog, e.message);
    } finally {
      langBusy = false;
      langForm.querySelector('.send').disabled = false;
    }
  }

  $('langStart').addEventListener('click', () => {
    store.set('tutor-lang', { target: langTarget.value, helper: langHelper.value, level: langLevel.value });
    if (synth) synth.speak(new SpeechSynthesisUtterance(''));
    langMessages = [];
    langLog.innerHTML = '';
    const scenarioLabel = document.querySelector('#langScenarios .chip.on');
    $('langTitle').textContent = `${LANG_NAMES[langTarget.value]} · ${langLevel.options[langLevel.selectedIndex].text} · ${scenarioLabel ? scenarioLabel.textContent : ''}`;
    $('langSetup').hidden = true;
    $('langRoom').hidden = false;
    langInput.placeholder = `Speak or type in ${LANG_NAMES[langTarget.value]}…`;
    langTurn('');
  });
  $('langNew').addEventListener('click', () => {
    stopSpeaking(); stopListening();
    $('langRoom').hidden = true;
    $('langSetup').hidden = false;
  });
  $('langShowTr').addEventListener('change', () => {
    langLog.querySelectorAll('.tr').forEach(t => { t.hidden = !$('langShowTr').checked; });
  });
  langForm.addEventListener('submit', e => {
    e.preventDefault();
    const text = langInput.value.trim();
    if (text) langTurn(text);
  });
  autoGrow(langInput); enterToSend(langInput, langForm);
  setupMic($('langMic'), langInput, () => LANG_CODES[langTarget.value], () => langForm.requestSubmit());

  /* =========================================================
     VOICE SETTINGS PANEL
     ========================================================= */
  const voiceDialog = $('voiceDialog');
  const SAMPLES = {
    en: "Hello! I'm your AsghinLabs tutor. Let's learn together, step by step.",
    fr: "Bonjour ! Je suis ton tuteur AsghinLabs. Apprenons ensemble, étape par étape.",
    es: '¡Hola! Soy tu tutor de AsghinLabs. Aprendamos juntos, paso a paso.',
  };
  const LANG_FULL = { en: 'en-GB', fr: 'fr-FR', es: 'es-ES' };

  function showEngine() {
    const ai = voiceSettings.engine === 'ai';
    $('vdAi').hidden = !ai;
    $('vdDevice').hidden = ai;
    $('pitchRow').hidden = ai;      // AI voices have their own natural pitch
    voiceDialog.querySelectorAll('input[name="engine"]').forEach(r => { r.checked = r.value === voiceSettings.engine; });
  }

  function buildAiGrid() {
    const grid = $('aiVoiceGrid');
    grid.innerHTML = '';
    AI_VOICES.forEach(v => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'voice-card' + (v.id === voiceSettings.aiVoice ? ' on' : '');
      card.setAttribute('aria-pressed', String(v.id === voiceSettings.aiVoice));
      card.innerHTML = `<span class="vc-icon">${v.who === 'Woman' ? '👩🏾' : '👨🏾'}</span><span class="vc-text"><b></b><small></small></span><span class="vc-play">▶</span>`;
      card.querySelector('b').textContent = v.id;
      card.querySelector('small').textContent = `${v.who} · ${v.desc}`;
      card.onclick = () => {
        voiceSettings.aiVoice = v.id;
        saveVoiceSettings();
        buildAiGrid();
        speak(SAMPLES.en, { raw: true });
      };
      grid.appendChild(card);
    });
  }

  window.refreshVoicePanel = function () {
    ['en', 'fr', 'es'].forEach(base => {
      const sel = $('devVoice-' + base);
      const list = deviceVoices(base);
      sel.innerHTML = '';
      if (!list.length) {
        sel.add(new Option('No voice installed for this language', ''));
        sel.disabled = true;
        return;
      }
      sel.disabled = false;
      sel.add(new Option('Automatic (best available)', ''));
      list.forEach(v => sel.add(new Option(`${voiceScore(v) >= 4 ? '⭐ ' : ''}${v.name} (${v.lang})`, v.voiceURI)));
      sel.value = voiceSettings.device[base] && list.some(v => v.voiceURI === voiceSettings.device[base]) ? voiceSettings.device[base] : '';
    });
  };

  function showSliders() {
    $('voiceRate').value = voiceSettings.rate;
    $('voicePitch').value = voiceSettings.pitch;
    $('rateOut').textContent = voiceSettings.rate === 1 ? 'Normal' : `${voiceSettings.rate.toFixed(2)}×`;
    $('pitchOut').textContent = voiceSettings.pitch === 1 ? 'Normal' : (voiceSettings.pitch < 1 ? 'Deeper' : 'Higher');
  }

  function openVoicePanel() {
    stopSpeaking();
    showEngine();
    buildAiGrid();
    window.refreshVoicePanel();
    showSliders();
    if (voiceDialog.showModal) voiceDialog.showModal(); else voiceDialog.setAttribute('open', '');
  }
  document.querySelectorAll('[data-open-voice]').forEach(b => b.addEventListener('click', openVoicePanel));
  voiceDialog.addEventListener('close', stopSpeaking);
  voiceDialog.addEventListener('click', e => { if (e.target === voiceDialog) voiceDialog.close(); });   // tap outside to close

  voiceDialog.querySelectorAll('input[name="engine"]').forEach(r => r.addEventListener('change', () => {
    voiceSettings.engine = r.value;
    if (r.value === 'ai') aiVoiceOff = false;   // let the student try again
    saveVoiceSettings();
    showEngine();
    speak(SAMPLES.en, { raw: true });
  }));

  ['en', 'fr', 'es'].forEach(base => {
    $('devVoice-' + base).addEventListener('change', e => {
      voiceSettings.device[base] = e.target.value;
      saveVoiceSettings();
      speak(SAMPLES[base], { raw: true, lang: LANG_FULL[base] });
    });
  });
  voiceDialog.querySelectorAll('[data-preview]').forEach(b => b.addEventListener('click', () => {
    const base = b.dataset.preview;
    const keep = voiceSettings.engine;
    voiceSettings.engine = 'device';            // the ▶ next to each language previews the device voice
    speak(SAMPLES[base], { raw: true, lang: LANG_FULL[base] }).finally(() => { voiceSettings.engine = keep; });
  }));

  $('voiceRate').addEventListener('input', e => { voiceSettings.rate = Number(e.target.value); showSliders(); });
  $('voicePitch').addEventListener('input', e => { voiceSettings.pitch = Number(e.target.value); showSliders(); });
  ['voiceRate', 'voicePitch'].forEach(id => $(id).addEventListener('change', () => {
    saveVoiceSettings();
    speak(SAMPLES.en, { raw: true });
  }));
  $('voiceTest').addEventListener('click', () => speak(SAMPLES.en, { raw: true }));

  /* ---------------- Lesson the student came from ---------------- */
  function showLessonChips() {
    ['askLessonChip', 'classLessonChip'].forEach(id => {
      const chip = $(id);
      if (!chip) return;
      chip.innerHTML = '';
      chip.hidden = !lessonCtx;
      if (!lessonCtx) return;
      const label = document.createElement('span');
      label.textContent = `📘 Using your lesson: ${lessonCtx.title}`;
      const x = document.createElement('button');
      x.type = 'button'; x.textContent = '✕'; x.title = 'Stop using this lesson'; x.setAttribute('aria-label', 'Stop using this lesson');
      x.onclick = forgetLesson;
      chip.append(label, x);
    });
  }
  function forgetLesson() {
    lessonCtx = null;
    try { localStorage.removeItem('tutor-lesson-ctx'); } catch (e) { /* storage blocked */ }
    showLessonChips();
  }

  /* ---------------- Start ---------------- */
  // Links from lesson pages: /tutor?tab=ask&q=…  or  /tutor?tab=class&topic=…  (+ &level=Form 3)
  const params = new URLSearchParams(location.search);
  const startTab = params.get('tab') || store.get('tutor-tab', 'ask');
  openTab(tabs.includes(startTab) ? startTab : 'ask');

  const fromLesson = { q: params.get('q'), topic: params.get('topic'), level: params.get('level') };
  // The saved lesson only applies when the student just came from it.
  const lessonTitle = lessonCtx && lessonCtx.title.toLowerCase();
  if (!lessonCtx || !((fromLesson.q || '') + (fromLesson.topic || '')).toLowerCase().includes(lessonTitle)) lessonCtx = null;
  showLessonChips();
  if (fromLesson.q || fromLesson.topic || fromLesson.level) {
    // Remove the parameters so a refresh doesn't ask the same question again.
    history.replaceState(null, '', location.pathname + (params.get('tab') ? `?tab=${params.get('tab')}` : ''));
    if (fromLesson.level && !levelSelect.value && [...levelSelect.options].some(o => o.value === fromLesson.level)) {
      levelSelect.value = fromLesson.level;
      store.set('tutor-level', levelSelect.value);
    }
    if (fromLesson.q && startTab === 'ask') {
      setMode('explain');
      askSendMessage(fromLesson.q.slice(0, 1000));
    }
    if (fromLesson.topic && startTab === 'class') {
      // Sound needs a tap on this page, so the student presses "Start class" themselves.
      $('classTopic').value = fromLesson.topic.slice(0, 300);
      const start = $('classForm').querySelector('.send');
      start.classList.add('pulse');
      start.focus({ preventScroll: true });
      $('classSetup').scrollIntoView({ block: 'center' });
    }
  }
})();
