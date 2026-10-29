/* Private exam-prep space — teacher side. Talks to /api/prep (admin actions). */
(function () {
  'use strict';
  const STUDENT_PAGE = 'https://www.asghinlabs.com/prep/9y3znsgt';

  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const md = src => { const h = window.marked ? marked.parse(String(src || ''), { breaks: true }) : esc(src); return window.DOMPurify ? DOMPurify.sanitize(h) : esc(src); };
  const avg = a => a && a.length ? Math.round(a.reduce((x, y) => x + y, 0) / a.length) : null;
  const pctClass = p => p == null ? '' : p >= 70 ? 'good' : p >= 45 ? 'mid' : 'bad';
  const ss = { get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* */ } } };

  const A = { key: '', tracks: [], codes: [], counts: {}, tab: 'students', qTrack: null, questions: [], images: {} };

  async function api(action, data = {}) {
    const r = await fetch('/api/prep', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action, key: A.key, ...data }) });
    let j = {};
    try { j = await r.json(); } catch (e) { /* */ }
    if (!r.ok || !j.ok) throw new Error(j.error || 'Network error. Try again.');
    return j;
  }
  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn.dataset.label = btn.innerHTML; btn.disabled = true; btn.innerHTML = `<span class="spin"></span> ${label || 'Wait…'}`; }
    else { btn.disabled = false; if (btn.dataset.label) btn.innerHTML = btn.dataset.label; }
  }
  function shrink(file, max = 1600, quality = 0.72) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const k = Math.min(1, max / Math.max(img.width, img.height));
        const c = document.createElement('canvas');
        c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
        const ctx = c.getContext('2d');
        ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height);
        ctx.drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(img.src);
        resolve({ type: 'image/jpeg', data: c.toDataURL('image/jpeg', quality).split(',')[1] });
      };
      img.onerror = () => reject(new Error('Could not read that image.'));
      img.src = URL.createObjectURL(file);
    });
  }
  async function imgSrc(id) {
    if (!A.images[id]) { const j = await api('a-image', { id }); A.images[id] = `data:${j.mime};base64,${j.data}`; }
    return A.images[id];
  }
  const trackName = id => (A.tracks.find(t => t.id === id) || {}).title || id;

  /* ---------- login ---------- */
  async function open(key) {
    A.key = key;
    try {
      await refresh();
      ss.set('prep-admin', key);
      $('#login').classList.add('hide'); $('#app').classList.remove('hide');
      tab(A.tab);
    } catch (e) { $('#loginErr').textContent = e.message; }
  }
  async function refresh() { const j = await api('a-overview'); A.tracks = j.tracks; A.codes = j.codes; A.counts = j.counts; A.today = j.today; }
  $('#loginForm').onsubmit = e => { e.preventDefault(); open($('#key').value); };
  $('#tabs').onclick = e => { const b = e.target.closest('[data-tab]'); if (b) tab(b.dataset.tab); };
  function tab(t) {
    A.tab = t;
    document.querySelectorAll('#tabs .tab').forEach(b => b.classList.toggle('on', b.dataset.tab === t));
    ({ students: viewStudents, questions: viewQuestions, tracks: viewTracks })[t]();
  }

  /* ---------- students & codes ---------- */
  function codeForm(s) {
    s = s || {};
    const nextYear = new Date().getFullYear() + (new Date().getMonth() >= 7 ? 1 : 0);
    return `<div class="card" id="codeCard"><h3>${s.code ? `Edit ${esc(s.code)}` : '➕ New student (after payment)'}</h3>
      <div class="grid2">
        <div><label class="f">Student name</label><input type="text" id="cName" value="${esc(s.name || '')}" placeholder="e.g. Ngono Marie"></div>
        <div><label class="f">WhatsApp number (optional)</label><input type="tel" id="cPhone" value="${esc(s.phone || '')}" placeholder="6XX XXX XXX"></div>
      </div>
      <label class="f">Programmes paid for</label>
      <div class="checks">${A.tracks.map(t => `<label><input type="checkbox" value="${esc(t.id)}" ${(s.tracks || []).includes(t.id) ? 'checked' : ''}> ${esc(t.title)} (${esc(t.exam)})</label>`).join('')}</div>
      <div class="grid2">
        <div><label class="f">Access until</label><input type="date" id="cExp" value="${esc(s.expires || `${nextYear}-07-31`)}"></div>
        <div><label class="f">Max devices</label><input type="number" id="cDev" min="1" max="5" value="${s.maxDevices || 2}"></div>
        <div><label class="f">AI requests per day</label><input type="number" id="cAi" min="5" max="500" value="${s.dailyAi || 80}"></div>
        <div><label class="f">Code prefix (new codes)</label><input type="text" id="cPre" value="${esc((s.code || 'ACA').split('-')[0])}" ${s.code ? 'disabled' : ''}></div>
      </div>
      <label class="f">Note (amount paid, class, school…)</label><input type="text" id="cNote" value="${esc(s.note || '')}">
      <div class="row" style="margin-top:14px"><button class="btn primary" id="cSave">${s.code ? 'Save changes' : 'Create code'}</button>${s.code ? '<button class="btn ghost" id="cCancel">Cancel</button>' : ''}</div>
      <div class="err" id="cErr"></div><div id="cOut"></div></div>`;
  }

  function welcome(s) {
    const t = s.tracks.map(trackName).join(' + ');
    return `Bonjour ${s.name} 👋\nBienvenue dans la préparation AsghinLabs Academy : ${t}.\n\n👉 Votre espace (touchez le lien) : ${STUDENT_PAGE}#c=${s.code}\n🔑 Votre code personnel : ${s.code}\n\nAccès valable jusqu’au ${s.expires || '—'}. Ce code est personnel : il ne marche que sur ${s.maxDevices} appareil${s.maxDevices > 1 ? 's' : ''}. Ne le partagez pas.\n\nSur la page : anciens sujets par chapitre, correction par l’IA, tuteur IA et examens blancs chronométrés. Bonne préparation ! 💪`;
  }
  function waLink(phone, msg) {
    let d = String(phone || '').replace(/\D/g, '');
    if (d.length === 9) d = '237' + d;
    return `https://wa.me/${d}?text=${encodeURIComponent(msg)}`;
  }
  function showWelcome(box, s) {
    const msg = welcome(s);
    box.innerHTML = `<div class="card correction" style="margin-top:14px"><h3>✅ Code ${esc(s.code)}</h3><p class="small muted">Send this message to the student:</p>
      <div class="msgbox" id="wMsg">${esc(msg)}</div>
      <div class="row" style="margin-top:10px"><button class="btn sm" id="wCopy">📋 Copy message</button>${s.phone ? `<a class="btn sm primary" target="_blank" rel="noopener" href="${esc(waLink(s.phone, msg))}">Open in WhatsApp</a>` : ''}</div></div>`;
    $('#wCopy').onclick = async () => { try { await navigator.clipboard.writeText(msg); $('#wCopy').textContent = '✓ Copied'; } catch (e) { $('#wCopy').textContent = 'Select and copy the text'; } };
  }

  function bindCodeForm(s) {
    $('#cSave').onclick = async () => {
      $('#cErr').textContent = '';
      const student = {
        code: s && s.code, prefix: $('#cPre').value, name: $('#cName').value, phone: $('#cPhone').value,
        tracks: [...document.querySelectorAll('#codeCard .checks input:checked')].map(x => x.value),
        expires: $('#cExp').value, maxDevices: $('#cDev').value, dailyAi: $('#cAi').value, note: $('#cNote').value,
        active: s ? s.active !== false : true,
      };
      busy($('#cSave'), true);
      try {
        const j = await api('a-save-code', { student });
        await refresh();
        viewStudents();
        showWelcome($('#cOut'), j.student);
        $('#cOut').scrollIntoView({ behavior: 'smooth' });
      } catch (e) { $('#cErr').textContent = e.message; busy($('#cSave'), false); }
    };
    if ($('#cCancel')) $('#cCancel').onclick = () => viewStudents();
  }

  function viewStudents(edit) {
    const now = A.today;
    const rows = A.codes.map(s => {
      const expired = s.expires && now > s.expires;
      const state = s.active === false ? '<span class="pill bad">off</span>' : expired ? '<span class="pill mid">expired</span>' : '<span class="pill good">active</span>';
      return `<tr><td><b>${esc(s.name)}</b><div class="small muted">${esc(s.phone || '')}${s.note ? ' · ' + esc(s.note) : ''}</div></td>
        <td><code>${esc(s.code)}</code><div>${state}</div></td>
        <td class="small">${s.tracks.map(t => esc(trackName(t))).join('<br>')}</td>
        <td class="small">until ${esc(s.expires || '—')}<br>${(s.devices || []).length}/${s.maxDevices} devices<br>${s.lastSeen ? 'seen ' + new Date(s.lastSeen).toLocaleDateString() : 'never opened'}</td>
        <td><div class="row" style="gap:6px">
          <button class="btn sm" data-act="see" data-c="${esc(s.code)}">Progress</button>
          <button class="btn sm" data-act="msg" data-c="${esc(s.code)}">Message</button>
          <button class="btn sm" data-act="edit" data-c="${esc(s.code)}">Edit</button>
          <button class="btn sm" data-act="reset" data-c="${esc(s.code)}" title="Use when the student changed phone">Reset devices</button>
          <button class="btn sm" data-act="toggle" data-c="${esc(s.code)}">${s.active === false ? 'Turn on' : 'Turn off'}</button>
          <button class="btn sm danger" data-act="del" data-c="${esc(s.code)}">Delete</button></div></td></tr>`;
    }).join('');
    $('#view').innerHTML = codeForm(edit) + `<div class="card"><h3>Students (${A.codes.length})</h3>
      ${A.codes.length ? `<div class="scroll"><table class="t"><tr><th>Student</th><th>Code</th><th>Programmes</th><th>Access</th><th></th></tr>${rows}</table></div>` : '<p class="muted">No students yet. Create the first code above after payment.</p>'}</div><div id="studentBox"></div>`;
    bindCodeForm(edit);
    $('#view').querySelectorAll('[data-act]').forEach(b => b.onclick = async () => {
      const s = A.codes.find(x => x.code === b.dataset.c);
      const act = b.dataset.act;
      try {
        if (act === 'edit') { viewStudents(s); window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
        if (act === 'msg') { showWelcome($('#studentBox'), s); $('#studentBox').scrollIntoView({ behavior: 'smooth' }); return; }
        if (act === 'see') { studentProgress(s.code); return; }
        if (act === 'reset') { if (!confirm(`Reset devices for ${s.name}? Their code will work on the next ${s.maxDevices} devices that open it.`)) return; await api('a-reset-devices', { code: s.code }); }
        if (act === 'toggle') await api('a-save-code', { student: { ...s, active: s.active === false } });
        if (act === 'del') { if (!confirm(`Delete ${s.name}'s code and all their results? This cannot be undone.`)) return; await api('a-delete-code', { code: s.code }); }
        await refresh(); viewStudents();
      } catch (e) { alert(e.message); }
    });
  }

  async function studentProgress(code) {
    const box = $('#studentBox');
    box.innerHTML = '<div class="card"><span class="spin"></span> Loading…</div>';
    box.scrollIntoView({ behavior: 'smooth' });
    try {
      const j = await api('a-student', { code });
      const qs = Object.values(j.questions || {});
      const tried = qs.filter(q => q.n);
      const topicRows = Object.entries(j.topics || {}).map(([k, v]) => {
        const [tid, top] = k.split('|');
        const tr = A.tracks.find(t => t.id === tid) || { topics: [] };
        const title = ((tr.topics || []).find(x => x.id === top) || {}).title || 'Other';
        return { title: `${title} <span class="small muted">(${esc(trackName(tid))})</span>`, a: avg(v.scores), n: (v.scores || []).length };
      }).sort((x, y) => x.a - y.a);
      box.innerHTML = `<div class="card"><h3>📈 ${esc(j.student.name)} — ${esc(code)}</h3>
        <div class="stats"><div class="stat"><b>${tried.length}</b><span>past questions marked</span></div>
          <div class="stat"><b>${avg(tried.map(q => q.last)) ?? '—'}${tried.length ? '%' : ''}</b><span>average score</span></div>
          <div class="stat"><b>${(j.mocks || []).length}</b><span>mock exams</span></div>
          <div class="stat"><b>${j.aiUsedToday}</b><span>AI requests today</span></div></div>
        <h3>Chapters (weakest first)</h3>
        ${topicRows.length ? topicRows.map(r => `<div style="margin:10px 0"><div class="row"><span class="grow">${r.title}</span><span class="small">${r.a}% · ${r.n} tries</span></div><div class="bar"><i style="width:${r.a}%;background:var(--${pctClass(r.a)})"></i></div></div>`).join('') : '<p class="muted">No marked answers yet.</p>'}
        ${(j.mocks || []).length ? `<h3 style="margin-top:16px">Mock exams</h3>${j.mocks.map(m => `<div class="row"><span class="grow">${esc(m.paper)} · ${new Date(m.at).toLocaleDateString()}</span><b>${Math.round(m.total / m.max * 200) / 10}/20</b></div>`).join('')}` : ''}
        <h3 style="margin-top:16px">Recent activity</h3>
        ${(j.hist || []).slice(0, 25).map(h => `<div class="small" style="margin:4px 0">${new Date(h.at).toLocaleString()} · ${esc(h.kind)} · ${h.score}/${h.max}</div>`).join('') || '<p class="muted small">Nothing yet.</p>'}
        <p class="small muted">Devices: ${(j.student.devices || []).map(d => 'first used ' + new Date(d.first).toLocaleDateString()).join(', ') || 'none yet'}</p></div>`;
    } catch (e) { box.innerHTML = `<div class="card err">${esc(e.message)}</div>`; }
  }

  /* ---------- past questions ---------- */
  async function viewQuestions() {
    A.qTrack = A.qTrack && A.tracks.find(t => t.id === A.qTrack) ? A.qTrack : A.tracks[0].id;
    $('#view').innerHTML = `<div class="card"><label class="f" style="margin-top:0">Programme</label><select id="qTrack">${A.tracks.map(t => `<option value="${esc(t.id)}" ${t.id === A.qTrack ? 'selected' : ''}>${esc(t.title)} (${A.counts[t.id] || 0} questions)</option>`).join('')}</select></div>
      <div id="qForm"></div><div id="qList"><div class="card"><span class="spin"></span></div></div>`;
    $('#qTrack').onchange = e => { A.qTrack = e.target.value; viewQuestions(); };
    questionForm();
    await loadQuestions();
  }

  async function loadQuestions() {
    try { A.questions = (await api('a-questions', { track: A.qTrack })).questions; }
    catch (e) { $('#qList').innerHTML = `<div class="card err">${esc(e.message)}</div>`; return; }
    const tr = A.tracks.find(t => t.id === A.qTrack);
    const topic = id => ((tr.topics || []).find(x => x.id === id) || {}).title || '<span class="muted">no chapter</span>';
    $('#qList').innerHTML = `<div class="card"><h3>Saved questions (${A.questions.length})</h3>${A.questions.length ? `<div class="scroll"><table class="t"><tr><th>Paper</th><th>Question</th><th>Chapter</th><th>Marks</th><th></th></tr>
      ${A.questions.map(q => `<tr><td>${esc(q.paper)}</td><td>${esc(q.number)}<div class="small muted">${esc((q.text || '').slice(0, 80))}${q.images.length ? ` · ${q.images.length} image(s)` : ''}</div></td><td class="small">${topic(q.topic)}</td><td>${q.marks}</td>
        <td><div class="row" style="gap:6px"><button class="btn sm" data-edit="${esc(q.id)}">Edit</button><button class="btn sm danger" data-del="${esc(q.id)}">Delete</button></div></td></tr>`).join('')}</table></div>` : '<p class="muted">No questions yet for this programme. Add the first one above.</p>'}</div>`;
    $('#qList').querySelectorAll('[data-edit]').forEach(b => b.onclick = () => { questionForm(A.questions.find(q => q.id === b.dataset.edit)); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    $('#qList').querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
      if (!confirm('Delete this question (and its images)?')) return;
      try { await api('a-delete-question', { track: A.qTrack, id: b.dataset.del }); A.counts[A.qTrack]--; loadQuestions(); } catch (e) { alert(e.message); }
    });
  }

  function questionForm(q, keep) {
    const tr = A.tracks.find(t => t.id === A.qTrack);
    q = q || keep || {};
    let images = q.id ? [...(q.images || [])] : [...((keep && keep.images) || [])];
    const box = $('#qForm');
    box.innerHTML = `<div class="card" id="qCard"><h3>${q.id ? '✏️ Edit question' : '➕ Add a past question'}</h3>
      ${(tr.topics || []).length ? '' : '<p class="notice">This programme has no chapters yet. Add them in “Programmes & chapters” so students can revise by chapter.</p>'}
      <div class="grid2">
        <div><label class="f">Paper (students see this)</label><input type="text" id="qPaper" value="${esc(q.paper || '')}" placeholder="e.g. ${esc(tr.exam)} 2023 — Informatique"></div>
        <div><label class="f">Year</label><input type="number" id="qYear" value="${esc(q.year || '')}" placeholder="2023"></div>
        <div><label class="f">Question number</label><input type="text" id="qNum" value="${esc(q.id ? q.number : '')}" placeholder="e.g. Exercice 1 — Q2"></div>
        <div><label class="f">Marks</label><input type="number" id="qMarks" step="0.5" min="0.5" value="${esc(q.id ? q.marks : '')}" placeholder="4"></div>
      </div>
      <label class="f">Chapter</label><select id="qTopic"><option value="">— no chapter —</option>${(tr.topics || []).map(t => `<option value="${esc(t.id)}" ${q.topic === t.id ? 'selected' : ''}>${esc(t.title)}</option>`).join('')}</select>
      <label class="f">Question text — type it exactly as on the paper (helps the AI mark well). Optional if you add page images.</label>
      <textarea id="qText" placeholder="Copy the question here, unedited…">${esc(q.id ? q.text : '')}</textarea>
      <label class="f">Page images (scan/photo of the paper, unedited)</label>
      <label class="btn sm" style="cursor:pointer">📎 Add images<input type="file" id="qImgs" accept="image/*" multiple hidden></label>
      <span id="imgState" class="small muted"></span>
      <div class="thumbs" id="thumbs"></div>
      <div class="row" style="margin-top:16px"><label class="f grow" style="margin:0">Correction (corrigé) — the AI marks students against this</label><button class="btn sm" id="qDraft">✨ AI draft (you must check it)</button></div>
      <textarea id="qAns" style="min-height:180px" placeholder="The complete, correct expected answer…">${esc(q.id ? q.answer : '')}</textarea>
      <label class="f">Marking scheme / barème (optional — where the marks go)</label>
      <textarea id="qScheme" style="min-height:90px" placeholder="e.g. Définition : 1 pt ; exemple : 1 pt…">${esc(q.id ? q.scheme || '' : '')}</textarea>
      <label class="row" style="margin-top:12px;gap:8px"><input type="checkbox" id="qOk" ${q.id ? 'checked' : ''}> I have checked this correction — it is correct</label>
      <div class="row" style="margin-top:14px"><button class="btn primary" id="qSave">Save</button>${q.id ? '' : '<button class="btn" id="qSaveNext">Save & add next question of this paper</button>'}${q.id || keep ? '<button class="btn ghost" id="qNew">New blank</button>' : ''}</div>
      <div class="err" id="qErr"></div><div class="ok-msg" id="qOkMsg"></div></div>`;

    async function drawThumbs() {
      $('#thumbs').innerHTML = images.map((id, i) => `<div><img data-i="${i}" alt=""><button data-rm="${i}" title="Remove">×</button></div>`).join('');
      $('#thumbs').querySelectorAll('[data-rm]').forEach(b => b.onclick = () => { images.splice(Number(b.dataset.rm), 1); drawThumbs(); });
      for (const el of $('#thumbs').querySelectorAll('img[data-i]')) { try { el.src = await imgSrc(images[el.dataset.i]); } catch (e) { el.alt = '?'; } }
    }
    drawThumbs();

    $('#qImgs').onchange = async e => {
      const files = [...e.target.files];
      for (const [n, f] of files.entries()) {
        $('#imgState').textContent = `Uploading ${n + 1}/${files.length}…`;
        try {
          const img = await shrink(f);
          const j = await api('a-upload-image', img);
          A.images[j.id] = `data:${img.type};base64,${img.data}`;
          images.push(j.id);
        } catch (err) { $('#qErr').textContent = err.message; }
      }
      $('#imgState').textContent = '';
      e.target.value = '';
      drawThumbs();
    };

    $('#qDraft').onclick = async () => {
      if (!$('#qText').value.trim() && !images.length) { $('#qErr').textContent = 'Type the question or add page images first.'; return; }
      if ($('#qAns').value.trim() && !confirm('Replace the correction you typed with an AI draft?')) return;
      busy($('#qDraft'), true, 'Drafting…');
      try {
        const j = await api('a-draft-answer', { track: A.qTrack, paper: $('#qPaper').value, number: $('#qNum').value, marks: $('#qMarks').value, text: $('#qText').value, images });
        $('#qAns').value = j.draft;
        $('#qOk').checked = false;
        $('#qOkMsg').textContent = '⚠️ AI draft added. Read and correct it carefully before ticking the box.';
      } catch (e) { $('#qErr').textContent = e.message; }
      finally { busy($('#qDraft'), false); }
    };

    async function save(next) {
      $('#qErr').textContent = ''; $('#qOkMsg').textContent = '';
      const question = { id: q.id, track: A.qTrack, paper: $('#qPaper').value, year: $('#qYear').value, number: $('#qNum').value, marks: $('#qMarks').value,
        topic: $('#qTopic').value, text: $('#qText').value, images, answer: $('#qAns').value, scheme: $('#qScheme').value, verified: $('#qOk').checked };
      if (!question.paper.trim()) { $('#qErr').textContent = 'Give the paper a name (e.g. BAC 2023 — Informatique).'; return; }
      const btn = next ? $('#qSaveNext') : $('#qSave');
      busy(btn, true, 'Saving…');
      try {
        await api('a-save-question', { question });
        if (!q.id) A.counts[A.qTrack] = (A.counts[A.qTrack] || 0) + 1;
        // "Save & next" keeps the paper, year and chapter (and page images, often shared by several questions).
        questionForm(null, next ? { paper: question.paper, year: question.year, topic: question.topic, images } : null);
        $('#qOkMsg').textContent = '✓ Saved. Students can see it now.';
        loadQuestions();
      } catch (e) { $('#qErr').textContent = e.message; busy(btn, false); }
    }
    $('#qSave').onclick = () => save(false);
    if ($('#qSaveNext')) $('#qSaveNext').onclick = () => save(true);
    if ($('#qNew')) $('#qNew').onclick = () => questionForm();
  }

  /* ---------- programmes & chapters ---------- */
  function viewTracks() {
    const draft = JSON.parse(JSON.stringify(A.tracks));
    const rid = () => Math.random().toString(36).slice(2, 8);
    function draw() {
      $('#view').innerHTML = `<div class="card"><p class="muted">Each programme is what a student can pay for. Chapters follow your progression sheet: students revise past questions chapter by chapter, and the AI finds their weak chapters.</p></div>` +
        draft.map((t, i) => `<div class="card" data-t="${i}">
          <div class="grid2">
            <div><label class="f">Programme name</label><input type="text" data-f="title" value="${esc(t.title)}"></div>
            <div><label class="f">Exam</label><input type="text" data-f="exam" value="${esc(t.exam)}" placeholder="Probatoire, BAC, BEPC, GCE O Level…"></div>
            <div><label class="f">Mock exam duration (minutes)</label><input type="number" data-f="duration" value="${t.duration}"></div>
            <div><label class="f">Language of the AI</label><select data-f="lang"><option value="fr" ${t.lang !== 'en' ? 'selected' : ''}>French</option><option value="en" ${t.lang === 'en' ? 'selected' : ''}>English</option></select></div>
          </div>
          <label class="f">Chapters (${t.topics.length})</label>
          ${t.topics.map((tp, j) => `<div class="topic-row"><input type="text" data-tp="${j}" value="${esc(tp.title)}"><button class="btn sm danger" data-rmtp="${j}">×</button></div>`).join('')}
          <div class="row"><button class="btn sm" data-addtp>+ Chapter</button><button class="btn sm" data-bulk>Paste many chapters</button>${draft.length > 1 && !(A.counts[t.id]) ? '<button class="btn sm danger" data-rmt>Remove programme</button>' : ''}</div>
          <p class="small muted">ID: ${esc(t.id)} · ${A.counts[t.id] || 0} questions</p></div>`).join('') +
        `<div class="row"><button class="btn" id="addT">+ Add a programme (e.g. GCE O Level CS, BEPC…)</button><button class="btn primary" id="saveT">Save programmes</button></div><div class="err" id="tErr"></div><div class="ok-msg" id="tOk"></div>`;

      $('#view').querySelectorAll('[data-t]').forEach(card => {
        const t = draft[card.dataset.t];
        card.querySelectorAll('[data-f]').forEach(el => el.oninput = () => { t[el.dataset.f] = el.value; });
        card.querySelectorAll('[data-tp]').forEach(el => el.oninput = () => { t.topics[el.dataset.tp].title = el.value; });
        card.querySelectorAll('[data-rmtp]').forEach(b => b.onclick = () => {
          if (confirm('Remove this chapter? Its questions will show under “Other questions”.')) { t.topics.splice(Number(b.dataset.rmtp), 1); draw(); }
        });
        card.querySelector('[data-addtp]').onclick = () => { t.topics.push({ id: rid(), title: '' }); draw(); };
        card.querySelector('[data-bulk]').onclick = () => {
          const txt = prompt('Paste chapter titles, one per line:');
          if (txt) { txt.split(/\r?\n/).map(s => s.replace(/^\s*[\d.)-]+\s*/, '').trim()).filter(Boolean).forEach(title => t.topics.push({ id: rid(), title })); draw(); }
        };
        const rm = card.querySelector('[data-rmt]');
        if (rm) rm.onclick = () => { if (confirm('Remove this programme?')) { draft.splice(Number(card.dataset.t), 1); draw(); } };
      });
      $('#addT').onclick = () => { draft.push({ id: 'p-' + rid(), title: 'New programme', exam: '', lang: 'fr', duration: 120, topics: [] }); draw(); };
      $('#saveT').onclick = async () => {
        busy($('#saveT'), true, 'Saving…');
        try {
          const j = await api('a-save-tracks', { tracks: draft.map(t => ({ ...t, topics: t.topics.filter(x => x.title.trim()) })) });
          A.tracks = j.tracks;
          viewTracks();
          $('#tOk').textContent = '✓ Saved.';
        } catch (e) { $('#tErr').textContent = e.message; busy($('#saveT'), false); }
      };
    }
    draw();
  }

  const saved = ss.get('prep-admin');
  if (saved) open(saved);
})();
