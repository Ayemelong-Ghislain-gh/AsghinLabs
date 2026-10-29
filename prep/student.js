/* Private exam-prep space — student side. Talks to /api/prep. */
(function () {
  'use strict';

  /* ---------- tiny helpers ---------- */
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } },
  };
  function md(src) {
    const html = window.marked ? marked.parse(String(src || ''), { breaks: true }) : esc(src).replace(/\n/g, '<br>');
    return window.DOMPurify ? DOMPurify.sanitize(html) : esc(src);
  }
  const pctClass = p => p == null ? '' : p >= 70 ? 'good' : p >= 45 ? 'mid' : 'bad';
  const avg = a => a && a.length ? Math.round(a.reduce((x, y) => x + y, 0) / a.length) : null;

  let device = store.get('prep-device');
  if (!device) { device = 'd' + Math.random().toString(36).slice(2) + Date.now().toString(36); store.set('prep-device', device); }

  const S = { code: '', me: null, track: null, questions: [], progress: { questions: {}, topics: {}, mocks: [] }, view: 'topics', list: [], chats: {}, images: {}, timer: null };

  async function api(action, data = {}) {
    const r = await fetch('/api/prep', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, code: S.code, device, ...data }),
    });
    let j = {};
    try { j = await r.json(); } catch (e) { /* network */ }
    if (!r.ok || !j.ok) {
      const err = new Error(j.error || 'Connexion impossible. Vérifiez votre internet et réessayez.');
      err.status = r.status;
      if (r.status === 401 || r.status === 403) { if (action !== 'login') logout(err.message); }
      throw err;
    }
    return j;
  }

  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn.dataset.label = btn.innerHTML; btn.disabled = true; btn.innerHTML = `<span class="spin"></span> ${label || 'Patientez…'}`; }
    else { btn.disabled = false; if (btn.dataset.label) btn.innerHTML = btn.dataset.label; }
  }

  // Photos are shrunk on the phone before sending (saves data and time).
  function shrink(file, max = 1400, quality = 0.75) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const k = Math.min(1, max / Math.max(img.width, img.height));
        const c = document.createElement('canvas');
        c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(img.src);
        resolve({ type: 'image/jpeg', data: c.toDataURL('image/jpeg', quality).split(',')[1] });
      };
      img.onerror = () => reject(new Error('Photo illisible.'));
      img.src = URL.createObjectURL(file);
    });
  }

  async function loadImages(root) {
    for (const el of root.querySelectorAll('img[data-img]')) {
      const id = el.dataset.img;
      try {
        if (!S.images[id]) { const j = await api('image', { id }); S.images[id] = `data:${j.mime};base64,${j.data}`; }
        el.src = S.images[id];
      } catch (e) { el.alt = 'Image indisponible'; }
    }
  }
  document.addEventListener('click', e => {
    const img = e.target.closest('.pages img');
    if (img && img.src) {
      const z = document.createElement('div');
      z.className = 'zoom'; z.innerHTML = `<img src="${img.src}" alt="">`;
      z.onclick = () => z.remove();
      document.body.appendChild(z);
    }
  });

  /* ---------- login ---------- */
  async function login(code, silent) {
    S.code = code.trim().toUpperCase();
    const btn = $('#loginBtn');
    busy(btn, true, 'Connexion…');
    $('#loginErr').textContent = '';
    try {
      const j = await api('login');
      S.me = j;
      store.set('prep-code', S.code);
      $('#login').classList.add('hide');
      $('#app').classList.remove('hide');
      $('#who').innerHTML = `<span>👋 ${esc(j.name.split(' ')[0])}</span><button class="btn sm ghost" id="out">Quitter</button>`;
      $('#out').onclick = () => logout();
      if (!j.tracks.length) { $('#view').innerHTML = '<div class="card">Aucun programme n’est encore ouvert pour votre code. Contactez AsghinLabs.</div>'; return; }
      $('#trackTabs').innerHTML = j.tracks.length > 1
        ? j.tracks.map(t => `<button class="tab" data-track="${esc(t.id)}">${esc(t.title)}</button>`).join('') : '';
      const last = store.get('prep-track');
      await setTrack(j.tracks.find(t => t.id === last) ? last : j.tracks[0].id);
    } catch (e) {
      if (!silent) $('#loginErr').textContent = e.message;
      else $('#loginErr').textContent = e.status === 403 ? e.message : '';
      if (e.status === 401 || e.status === 403) store.del('prep-code');
    } finally { busy(btn, false); }
  }
  function logout(msg) {
    store.del('prep-code');
    S.code = ''; S.me = null;
    clearInterval(S.timer);
    $('#app').classList.add('hide');
    $('#login').classList.remove('hide');
    $('#who').innerHTML = '';
    $('#loginErr').textContent = msg || '';
  }
  $('#loginForm').onsubmit = e => { e.preventDefault(); login($('#code').value); };

  /* ---------- track + views ---------- */
  const track = () => S.me.tracks.find(t => t.id === S.track);
  const topicTitle = id => { const t = (track().topics || []).find(x => x.id === id); return t ? t.title : 'Autres questions'; };
  const prog = id => S.progress.questions[id];
  const topicScores = tid => ((S.progress.topics[`${S.track}|${tid}`] || {}).scores || []);

  async function setTrack(tid) {
    S.track = tid;
    store.set('prep-track', tid);
    document.querySelectorAll('#trackTabs .tab').forEach(b => b.classList.toggle('on', b.dataset.track === tid));
    $('#view').innerHTML = '<div class="card muted"><span class="spin"></span> Chargement des sujets…</div>';
    const [q, p] = await Promise.all([api('questions', { track: tid }), api('progress')]);
    S.questions = q.questions;
    S.progress = p;
    show(S.view);
  }
  $('#trackTabs').onclick = e => { const b = e.target.closest('[data-track]'); if (b) setTrack(b.dataset.track); };
  $('#viewTabs').onclick = e => { const b = e.target.closest('[data-view]'); if (b) show(b.dataset.view); };

  function show(view) {
    if (S.timer && view !== 'mock-run') { clearInterval(S.timer); S.timer = null; }
    S.view = view;
    document.querySelectorAll('#viewTabs .tab').forEach(b => b.classList.toggle('on', b.dataset.view === view));
    const views = { topics: viewTopics, papers: viewPapers, train: viewTrain, mock: viewMock, progress: viewProgress };
    (views[view] || viewTopics)();
    window.scrollTo({ top: 0 });
  }

  function header() {
    const t = track();
    return `<div class="card"><div class="row"><div class="grow"><h2 style="margin:0">${esc(t.title)}</h2>
      <span class="muted small">Préparation ${esc(t.exam)} · accès jusqu’au ${esc(S.me.expires || '—')} · IA restante aujourd’hui : ${S.me.aiLeft}</span></div></div></div>`;
  }
  const empty = () => `<div class="card"><h3>Les sujets arrivent bientôt</h3><p class="muted">Votre enseignant ajoute en ce moment les anciens sujets et leurs corrections. En attendant, posez vos questions au tuteur IA ou faites un exercice d’entraînement par chapitre.</p></div>`;

  function qItem(q) {
    const p = prog(q.id);
    const status = p && p.n ? `<span class="pill ${pctClass(p.last)}">${p.last}%</span>` : p && p.revealed ? '<span class="pill">corrigé lu</span>' : '<span class="pill">à faire</span>';
    return `<button class="item" data-q="${esc(q.id)}"><div><div class="t">${esc(q.paper || 'Sujet')} — ${esc(q.number || '')}</div>
      <div class="s">${esc(topicTitle(q.topic))} · ${q.marks} pt${q.marks > 1 ? 's' : ''}</div></div><div class="end">${status}</div></button>`;
  }
  function bindQuestions(root, list) {
    root.querySelectorAll('[data-q]').forEach(b => b.onclick = () => { S.list = list.map(q => q.id); openQuestion(b.dataset.q); });
  }

  function viewTopics() {
    const t = track();
    const topics = [...(t.topics || []), { id: '', title: 'Autres questions' }];
    const groups = topics.map(tp => ({ tp, qs: S.questions.filter(q => (q.topic || '') === tp.id || (!tp.id && !(t.topics || []).some(x => x.id === q.topic))) }))
      .filter(g => g.qs.length || g.tp.id);
    let html = header();
    if (!S.questions.length && !(t.topics || []).length) html += empty();
    html += '<div class="list">' + groups.map((g, i) => {
      const a = avg(topicScores(g.tp.id));
      return `<button class="item" data-topic="${i}"><div class="grow"><div class="t">${esc(g.tp.title)}</div>
        <div class="s">${g.qs.length} question${g.qs.length > 1 ? 's' : ''} d’examen${a != null ? ` · votre moyenne ${a}%` : ''}</div>
        ${a != null ? `<div class="bar"><i style="width:${a}%;background:var(--${pctClass(a) || 'brand'})"></i></div>` : ''}</div>
        <div class="end">›</div></button>`;
    }).join('') + '</div>';
    $('#view').innerHTML = html;
    $('#view').querySelectorAll('[data-topic]').forEach(b => b.onclick = () => openTopic(groups[b.dataset.topic]));
  }

  function openTopic(g) {
    const v = $('#view');
    v.innerHTML = `<button class="btn sm ghost" id="back">← Chapitres</button>
      <div class="card" style="margin-top:12px"><h2>${esc(g.tp.title)}</h2>
      <div class="row">${g.tp.id ? '<button class="btn sm" id="prac">✨ Exercice d’entraînement IA</button>' : ''}<button class="btn sm" id="ask">💬 Poser une question au tuteur</button></div></div>
      ${g.qs.length ? `<div class="list">${g.qs.map(qItem).join('')}</div>` : '<div class="card muted">Pas encore d’ancien sujet sur ce chapitre. Essayez un exercice d’entraînement IA.</div>'}
      <div id="tutorBox"></div>`;
    $('#back').onclick = () => show('topics');
    if ($('#prac')) $('#prac').onclick = () => practice(g.tp.id);
    $('#ask').onclick = () => { tutor($('#tutorBox'), { topic: g.tp.id || null, key: 'topic:' + g.tp.id }); $('#tutorBox').scrollIntoView({ behavior: 'smooth' }); };
    bindQuestions(v, g.qs);
  }

  function papers() {
    const map = new Map();
    for (const q of S.questions) { const k = q.paper || 'Sujet'; if (!map.has(k)) map.set(k, []); map.get(k).push(q); }
    return [...map.entries()].map(([paper, qs]) => ({ paper, qs, marks: qs.reduce((s, q) => s + (Number(q.marks) || 0), 0) }));
  }

  function viewPapers() {
    const ps = papers();
    $('#view').innerHTML = header() + (ps.length ? ps.map((p, i) => `<div class="card"><div class="row"><h3 class="grow" style="margin:0">${esc(p.paper)}</h3><span class="pill">${p.qs.length} questions · ${p.marks} pts</span></div>
      <div class="list" style="margin-top:12px" data-paper="${i}">${p.qs.map(qItem).join('')}</div></div>`).join('') : empty());
    $('#view').querySelectorAll('[data-paper]').forEach(el => bindQuestions(el, ps[el.dataset.paper].qs));
  }

  /* ---------- one past question ---------- */
  function openQuestion(id) {
    const q = S.questions.find(x => x.id === id);
    if (!q) return;
    const i = S.list.indexOf(id);
    const p = prog(id);
    const draftKey = `prep-ans:${S.code}:${id}`;
    const v = $('#view');
    v.innerHTML = `<div class="row"><button class="btn sm ghost" id="back">← Retour</button><span class="grow"></span>
        ${i > 0 ? '<button class="btn sm" id="prev">‹ Précédente</button>' : ''}${i >= 0 && i < S.list.length - 1 ? '<button class="btn sm" id="next">Suivante ›</button>' : ''}</div>
      <div class="card" style="margin-top:12px">
        <div class="qhead"><span class="pill brand">${esc(q.paper || 'Sujet')}</span><span class="pill">${esc(q.number || '')}</span><span class="pill">${q.marks} pt${q.marks > 1 ? 's' : ''}</span><span class="pill">${esc(topicTitle(q.topic))}</span>
          ${p && p.n ? `<span class="pill ${pctClass(p.best)}">meilleur : ${p.best}%</span>` : ''}</div>
        ${q.text ? `<div class="md">${md(q.text)}</div>` : ''}
        ${q.images.length ? `<div class="pages">${q.images.map(im => `<img data-img="${esc(im)}" alt="Page du sujet">`).join('')}</div><p class="small muted">Touchez une image pour l’agrandir.</p>` : ''}
      </div>
      <div class="card">
        <h3>Votre réponse</h3>
        <p class="small muted">Répondez comme le jour de l’examen, puis faites-vous corriger. Vous pouvez aussi prendre en photo votre copie.</p>
        <textarea id="ans" placeholder="Écrivez votre réponse ici…">${esc(store.get(draftKey) || '')}</textarea>
        <div class="row" style="margin-top:10px">
          <label class="btn sm" style="cursor:pointer">📷 Photo de ma copie<input type="file" id="photo" accept="image/*" capture="environment" hidden></label>
          <span id="photoName" class="small muted"></span>
        </div>
        <div class="row" style="margin-top:14px">
          <button class="btn primary" id="mark">✅ Faire corriger par l’IA</button>
          <button class="btn" id="reveal">📖 Voir la correction</button>
          <button class="btn" id="ask">💬 Tuteur IA</button>
        </div>
        <div class="err" id="qErr"></div>
      </div>
      <div id="resultBox"></div><div id="corrBox"></div><div id="tutorBox"></div>`;

    $('#back').onclick = () => show(S.view);
    if ($('#prev')) $('#prev').onclick = () => openQuestion(S.list[i - 1]);
    if ($('#next')) $('#next').onclick = () => openQuestion(S.list[i + 1]);
    loadImages(v);

    const ans = $('#ans');
    ans.oninput = () => store.set(draftKey, ans.value);
    let photo = null;
    $('#photo').onchange = async e => {
      const f = e.target.files[0];
      if (!f) return;
      try { photo = await shrink(f); $('#photoName').textContent = '✓ Photo ajoutée'; } catch (err) { $('#photoName').textContent = err.message; }
    };

    $('#mark').onclick = async () => {
      $('#qErr').textContent = '';
      if (!ans.value.trim() && !photo) { $('#qErr').textContent = 'Écrivez votre réponse ou ajoutez une photo d’abord.'; return; }
      busy($('#mark'), true, 'Correction en cours…');
      try {
        const j = await api('mark', { track: S.track, id, answer: ans.value, photo });
        S.me.aiLeft = Math.max(0, S.me.aiLeft - 1);
        const prev = prog(id) || { n: 0, best: 0 };
        const pct = Math.round((j.result.score / j.result.max) * 100);
        S.progress.questions[id] = { ...prev, n: (prev.n || 0) + 1, last: pct, best: Math.max(prev.best || 0, pct), topic: q.topic };
        const tk = `${S.track}|${q.topic}`;
        S.progress.topics[tk] = { scores: [...((S.progress.topics[tk] || {}).scores || []), pct].slice(-10) };
        showResult($('#resultBox'), j.result);
      } catch (e) { $('#qErr').textContent = e.message; }
      finally { busy($('#mark'), false); }
    };

    $('#reveal').onclick = async () => {
      const tried = (prog(id) && prog(id).n) || ans.value.trim();
      if (!tried && !confirm('Essayez d’abord de répondre : c’est comme ça qu’on progresse. Voir quand même la correction ?')) return;
      busy($('#reveal'), true);
      try {
        const j = await api('reveal', { track: S.track, id });
        S.progress.questions[id] = { ...(prog(id) || { n: 0, best: 0 }), revealed: true };
        $('#corrBox').innerHTML = `<div class="card correction"><h3>📖 Correction de l’enseignant</h3><div class="md">${md(j.answer)}</div>
          ${j.scheme ? `<h3 style="margin-top:14px">Barème</h3><div class="md">${md(j.scheme)}</div>` : ''}</div>`;
        $('#corrBox').scrollIntoView({ behavior: 'smooth' });
      } catch (e) { $('#qErr').textContent = e.message; }
      finally { busy($('#reveal'), false); }
    };

    $('#ask').onclick = () => { tutor($('#tutorBox'), { id, key: 'q:' + id }); $('#tutorBox').scrollIntoView({ behavior: 'smooth' }); };
  }

  function showResult(box, r) {
    const pct = Math.round((r.score / r.max) * 100);
    box.innerHTML = `<div class="card result"><div class="row"><div class="score" style="color:var(--${pctClass(pct)})">${r.score} / ${r.max}</div><span class="pill ${pctClass(pct)}">${pct}%</span></div>
      <p><b>${esc(r.verdict)}</b></p>
      ${r.good && r.good.length ? `<div class="small muted">Ce qui vous a rapporté des points</div><ul>${r.good.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}
      ${r.missing && r.missing.length ? `<div class="small muted">Ce qui vous a fait perdre des points</div><ul>${r.missing.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}
      ${r.advice ? `<p class="notice">💡 ${esc(r.advice)}</p>` : ''}</div>`;
    box.scrollIntoView({ behavior: 'smooth' });
  }

  /* ---------- AI tutor chat ---------- */
  function tutor(box, ctx) {
    const msgs = S.chats[ctx.key] = S.chats[ctx.key] || [];
    box.innerHTML = `<div class="card"><h3>💬 Tuteur IA</h3><p class="small muted">Posez votre question : explication, méthode, ce que l’examinateur attend…</p>
      <div class="chat" id="chat"></div>
      <form class="chat-in" id="chatForm"><textarea id="chatIn" placeholder="Votre question…" required></textarea><button class="btn primary" id="chatBtn">Envoyer</button></form>
      <div class="err" id="chatErr"></div></div>`;
    const draw = () => {
      $('#chat').innerHTML = msgs.map(m => `<div class="msg ${m.role === 'user' ? 'me' : 'ai'} md">${m.role === 'user' ? esc(m.content) : md(m.content)}</div>`).join('');
      $('#chat').scrollTop = 1e9;
    };
    draw();
    $('#chatIn').onkeydown = e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('#chatForm').requestSubmit(); } };
    $('#chatForm').onsubmit = async e => {
      e.preventDefault();
      const content = $('#chatIn').value.trim();
      if (!content) return;
      msgs.push({ role: 'user', content });
      $('#chatIn').value = '';
      draw();
      busy($('#chatBtn'), true, '');
      $('#chatErr').textContent = '';
      try {
        const j = await api('tutor', { track: S.track, id: ctx.id || null, topic: ctx.topic || null, messages: msgs });
        S.me.aiLeft = Math.max(0, S.me.aiLeft - 1);
        msgs.push({ role: 'assistant', content: j.reply });
        draw();
      } catch (err) { msgs.pop(); draw(); $('#chatIn').value = content; $('#chatErr').textContent = err.message; }
      finally { busy($('#chatBtn'), false); }
    };
  }

  /* ---------- AI practice question ---------- */
  async function practice(topicId) {
    const v = $('#view');
    v.innerHTML = `<button class="btn sm ghost" id="back">← Retour</button><div class="card" style="margin-top:12px"><span class="spin"></span> L’IA prépare un exercice sur « ${esc(topicTitle(topicId))} »…</div>`;
    $('#back').onclick = () => show(S.view);
    let p;
    try { p = (await api('practice', { track: S.track, topic: topicId })).practice; S.me.aiLeft = Math.max(0, S.me.aiLeft - 1); }
    catch (e) { v.querySelector('.card').innerHTML = `<p class="err">${esc(e.message)}</p>`; return; }
    v.innerHTML = `<div class="row"><button class="btn sm ghost" id="back">← Retour</button><span class="grow"></span><button class="btn sm" id="again">↻ Autre exercice</button></div>
      <div class="card" style="margin-top:12px">
        <div class="qhead"><span class="pill mid">Exercice d’entraînement (IA)</span><span class="pill">${esc(topicTitle(topicId))}</span><span class="pill">${p.marks} pts</span></div>
        <p class="notice">Cet exercice a été écrit par l’IA dans le style de l’examen. Ce n’est pas un ancien sujet officiel.</p>
        <div class="md" style="margin-top:12px">${md(p.question)}</div></div>
      <div class="card"><h3>Votre réponse</h3><textarea id="ans" placeholder="Écrivez votre réponse ici…"></textarea>
        <div class="row" style="margin-top:14px"><button class="btn primary" id="mark">✅ Corriger</button><button class="btn" id="reveal">📖 Voir le corrigé</button></div>
        <div class="err" id="qErr"></div></div>
      <div id="resultBox"></div><div id="corrBox"></div>`;
    $('#back').onclick = () => show(S.view);
    $('#again').onclick = () => practice(topicId);
    $('#reveal').onclick = () => { $('#corrBox').innerHTML = `<div class="card correction"><h3>📖 Corrigé proposé</h3><div class="md">${md(p.answer)}</div></div>`; };
    $('#mark').onclick = async () => {
      const a = $('#ans').value;
      if (!a.trim()) { $('#qErr').textContent = 'Écrivez votre réponse d’abord.'; return; }
      busy($('#mark'), true, 'Correction…');
      try {
        const j = await api('mark', { track: S.track, practice: p, answer: a });
        S.me.aiLeft = Math.max(0, S.me.aiLeft - 1);
        const tk = `${S.track}|${topicId}`;
        S.progress.topics[tk] = { scores: [...((S.progress.topics[tk] || {}).scores || []), Math.round(j.result.score / j.result.max * 100)].slice(-10) };
        showResult($('#resultBox'), j.result);
      } catch (e) { $('#qErr').textContent = e.message; }
      finally { busy($('#mark'), false); }
    };
  }

  /* ---------- targeted training ---------- */
  function viewTrain() {
    const t = track();
    const topics = (t.topics || []).map(tp => {
      const qs = S.questions.filter(q => q.topic === tp.id);
      const todo = qs.filter(q => !(prog(q.id) && (prog(q.id).n || prog(q.id).revealed)));
      return { tp, qs, todo, a: avg(topicScores(tp.id)) };
    });
    // Weakest first, then chapters never practised.
    const order = [...topics].sort((x, y) => (x.a == null ? 101 : x.a) - (y.a == null ? 101 : y.a));
    const weak = order.filter(x => x.a != null && x.a < 60);
    let html = header() + `<div class="card"><h3>🎯 Vos points faibles</h3><p class="muted small">Calculé à partir de vos dernières corrections. Travaillez d’abord les chapitres en rouge.</p>
      ${weak.length ? '' : order.some(x => x.a != null) ? '<p class="ok-msg">Aucun chapitre faible pour le moment 👏 Continuez avec les chapitres pas encore travaillés.</p>' : '<p class="muted">Pas encore assez de corrections. Faites quelques questions et revenez ici.</p>'}</div>`;
    html += '<div class="list">' + order.map((x, i) => `<div class="item" style="cursor:default"><div class="grow"><div class="t">${esc(x.tp.title)}</div>
      <div class="s">${x.a != null ? `moyenne ${x.a}%` : 'pas encore travaillé'} · ${x.todo.length} ancien${x.todo.length > 1 ? 's' : ''} sujet${x.todo.length > 1 ? 's' : ''} pas encore fait${x.todo.length > 1 ? 's' : ''}</div>
      ${x.a != null ? `<div class="bar"><i style="width:${x.a}%;background:var(--${pctClass(x.a)})"></i></div>` : ''}</div>
      <div class="end"><button class="btn sm primary" data-go="${i}">S’entraîner</button></div></div>`).join('') + '</div>';
    if (!order.length) html += empty();
    $('#view').innerHTML = html;
    $('#view').querySelectorAll('[data-go]').forEach(b => b.onclick = () => {
      const x = order[b.dataset.go];
      // Real past questions first; when they are all done, a fresh AI exercise.
      if (x.todo.length) { S.list = x.qs.map(q => q.id); openQuestion(x.todo[0].id); }
      else practice(x.tp.id);
    });
  }

  /* ---------- mock exam ---------- */
  function viewMock() {
    const ps = papers();
    const t = track();
    $('#view').innerHTML = header() + `<div class="card"><h3>⏱️ Examen blanc</h3><p class="muted">Traitez une épreuve complète en temps limité (${t.duration} min), comme le jour J. À la fin, l’IA corrige toute la copie et vous donne votre note.</p></div>` +
      (ps.length ? '<div class="list">' + ps.map((p, i) => {
        const done = (S.progress.mocks || []).filter(m => m.track === S.track && m.paper === p.paper);
        const best = done.length ? Math.max(...done.map(m => Math.round(m.total / m.max * 100))) : null;
        return `<div class="item" style="cursor:default"><div class="grow"><div class="t">${esc(p.paper)}</div><div class="s">${p.qs.length} questions · ${p.marks} pts${best != null ? ` · meilleure note ${best}%` : ''}</div></div>
          <div class="end"><button class="btn sm primary" data-start="${i}">Commencer</button></div></div>`;
      }).join('') + '</div>' : empty());
    $('#view').querySelectorAll('[data-start]').forEach(b => b.onclick = () => {
      if (confirm(`L’examen dure ${t.duration} minutes. Le chronomètre démarre maintenant. Prêt ?`)) runMock(ps[b.dataset.start]);
    });
  }

  function runMock(p) {
    const t = track();
    S.view = 'mock-run';
    const key = `prep-mock:${S.code}:${S.track}:${p.paper}`;
    let saved = {};
    try { saved = JSON.parse(store.get(key) || '{}'); } catch (e) { saved = {}; }
    if (!saved.end || saved.end < Date.now()) saved = { end: Date.now() + t.duration * 60000, answers: {} };
    store.set(key, JSON.stringify(saved));
    const v = $('#view');
    v.innerHTML = `<div class="timer" id="timer"><span>⏱️</span><b id="clock">--:--</b><span class="grow small muted">${esc(p.paper)}</span><button class="btn sm primary" id="submit">Rendre ma copie</button></div>
      ${p.qs.map((q, n) => `<div class="card"><div class="qhead"><span class="pill brand">${esc(q.number || 'Question ' + (n + 1))}</span><span class="pill">${q.marks} pts</span></div>
        ${q.text ? `<div class="md">${md(q.text)}</div>` : ''}${q.images.length ? `<div class="pages">${q.images.map(im => `<img data-img="${esc(im)}" alt="">`).join('')}</div>` : ''}
        <textarea data-a="${esc(q.id)}" placeholder="Votre réponse…">${esc(saved.answers[q.id] || '')}</textarea></div>`).join('')}
      <div class="err" id="mErr"></div><div id="mockRes"></div>`;
    loadImages(v);
    v.querySelectorAll('[data-a]').forEach(el => el.oninput = () => { saved.answers[el.dataset.a] = el.value; store.set(key, JSON.stringify(saved)); });

    const tick = () => {
      const left = Math.max(0, saved.end - Date.now());
      const m = Math.floor(left / 60000), s = Math.floor(left / 1000) % 60;
      $('#clock').textContent = `${m}:${String(s).padStart(2, '0')}`;
      $('#timer').classList.toggle('low', left < 5 * 60000);
      if (!left) { clearInterval(S.timer); S.timer = null; submit(true); }
    };
    clearInterval(S.timer);
    S.timer = setInterval(tick, 1000);
    tick();

    let sent = false;
    async function submit(auto) {
      if (sent) return;
      if (!auto && !confirm('Rendre votre copie maintenant ?')) return;
      sent = true;
      clearInterval(S.timer); S.timer = null;
      v.querySelectorAll('[data-a]').forEach(el => { el.readOnly = true; });
      busy($('#submit'), true, 'Correction…');
      $('#mErr').textContent = auto ? 'Temps écoulé ! Votre copie est envoyée.' : '';
      try {
        const j = await api('mock', { track: S.track, paper: p.paper, answers: saved.answers });
        S.me.aiLeft = Math.max(0, S.me.aiLeft - 1);
        store.del(key);
        S.progress = await api('progress');
        const pct = Math.round(j.total / j.max * 100);
        const note20 = Math.round(j.total / j.max * 200) / 10;
        $('#mockRes').innerHTML = `<div class="card result"><h2>Résultat : ${j.total} / ${j.max} <span class="pill ${pctClass(pct)}">${note20} / 20</span></h2><p>${esc(j.summary)}</p></div>` +
          j.results.map(r => { const q = p.qs.find(x => x.id === r.id) || {}; const rp = Math.round(r.score / r.max * 100);
            return `<div class="card"><div class="row"><b class="grow">${esc(q.number || '')}</b><span class="pill ${pctClass(rp)}">${r.score} / ${r.max}</span></div><p>${esc(r.verdict)}</p>
              ${r.missing.length ? `<ul>${r.missing.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}<button class="btn sm" data-see="${esc(r.id)}">Revoir cette question</button></div>`; }).join('');
        $('#mockRes').querySelectorAll('[data-see]').forEach(b => b.onclick = () => { S.view = 'papers'; S.list = p.qs.map(q => q.id); openQuestion(b.dataset.see); });
        $('#timer').classList.add('hide');
        $('#mockRes').scrollIntoView({ behavior: 'smooth' });
      } catch (e) {
        sent = false;
        v.querySelectorAll('[data-a]').forEach(el => { el.readOnly = false; });
        $('#mErr').textContent = e.message + ' Vos réponses sont gardées : réessayez « Rendre ma copie ».';
      } finally { busy($('#submit'), false); }
    }
    $('#submit').onclick = () => submit(false);
  }

  /* ---------- progress ---------- */
  function viewProgress() {
    const t = track();
    const mine = S.questions.filter(q => prog(q.id) && prog(q.id).n);
    const scores = mine.map(q => prog(q.id).last);
    const mocks = (S.progress.mocks || []).filter(m => m.track === S.track);
    let html = header() + `<div class="stats">
      <div class="stat"><b>${mine.length}/${S.questions.length}</b><span>anciens sujets traités</span></div>
      <div class="stat"><b>${avg(scores) != null ? avg(scores) + '%' : '—'}</b><span>moyenne de vos corrections</span></div>
      <div class="stat"><b>${mocks.length}</b><span>examens blancs</span></div></div>`;
    html += `<div class="card"><h3>Par chapitre</h3>${(t.topics || []).map(tp => { const a = avg(topicScores(tp.id));
      return `<div style="margin:12px 0"><div class="row"><span class="grow">${esc(tp.title)}</span><span class="small ${a == null ? 'muted' : ''}">${a == null ? 'pas encore' : a + '%'}</span></div>
        <div class="bar"><i style="width:${a || 0}%;background:var(--${pctClass(a) || 'brand'})"></i></div></div>`; }).join('') || '<p class="muted">Aucun chapitre pour le moment.</p>'}</div>`;
    if (mocks.length) html += `<div class="card"><h3>Examens blancs</h3>${mocks.map(m => `<div class="row" style="margin:8px 0"><span class="grow">${esc(m.paper)} <span class="small muted">· ${new Date(m.at).toLocaleDateString('fr-FR')}</span></span>
      <span class="pill ${pctClass(Math.round(m.total / m.max * 100))}">${Math.round(m.total / m.max * 200) / 10} / 20</span></div>`).join('')}</div>`;
    $('#view').innerHTML = html;
  }

  /* ---------- start ---------- */
  const fromLink = (location.hash.match(/c=([A-Za-z0-9-]+)/) || [])[1];
  if (fromLink) history.replaceState(null, '', location.pathname);
  const saved = fromLink || store.get('prep-code');
  if (saved) { $('#code').value = saved; login(saved, true); }
})();
