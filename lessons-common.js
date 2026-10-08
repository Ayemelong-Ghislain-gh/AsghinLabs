/* =====================================================================
   Helpers shared by the interactive lessons (lesson-*.html).
   ===================================================================== */

// Random integer between a and b (both included)
function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }

// Random integer between a and b that is never 0
function rnz(a, b) { let n = 0; while (n === 0) n = rint(a, b); return n; }

function pick(list) { return list[Math.floor(Math.random() * list.length)]; }

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

// Number as text, rounded to 2 decimals, with a proper minus sign (−)
function num(n) { return String(+n.toFixed(2)).replace('-', '\u2212'); }

// [[coef, 'x²'], [coef, 'x'], [coef, '']] → "6x² + 8x − 3x − 12"
function joinTerms(terms) {
  return terms.map(([k, sym], i) => {
    const abs = Math.abs(k);
    const body = (abs === 1 && sym) ? sym : num(abs) + sym;
    if (i === 0) return (k < 0 ? '\u2212' : '') + body;
    return (k < 0 ? '\u2212 ' : '+ ') + body;
  }).join(' ');
}

// Coefficients of [x², x, number] → "x² − 5x + 6". Zero terms are left out.
function polyStr(coefs) {
  const syms = ['x\u00B2', 'x', ''];
  const terms = coefs.map((k, i) => [k, syms[i]]).filter(t => t[0] !== 0);
  return terms.length ? joinTerms(terms) : '0';
}

// Same event name as the sorting lesson, so Analytics groups them together
function viewLesson(slug) {
  if (typeof gtag === 'function') gtag('event', 'view_interactive_lesson', { lesson: slug });
  feedbackBox(slug);
}

// Tracks the main interactions: 'check_correct', 'check_wrong', 'new_question' ...
function trackLesson(slug, action) {
  if (typeof gtag === 'function') gtag('event', 'lesson_' + action, { lesson: slug });
}

/* =====================================================================
   Guided steps: the student fills in one step at a time, presses Check,
   and gets told what is right, what is wrong and why.

   runSteps(container, steps, { onFinish(usedHelp) })
   Each step: {
     html:   'Text with {0} {1} … where the answer boxes go',
     fields: [{ answer, kind: 'int' | 'bin' | 'bin4' | 'hex' | 'hexdigit', label }],
     hint:   'Shown when the answer is wrong (optional)',
     why:    'Full explanation, shown when the step is solved or revealed',
     info:   true  → no boxes, the step is just shown (e.g. "split into groups")
   }
   ===================================================================== */
function runSteps(container, steps, opts) {
  opts = opts || {};
  let usedHelp = false;
  container.innerHTML = '';

  const clean = (v) => String(v).trim().replace(/−/g, '-').replace(/\s+/g, '');

  function test(field, raw) {
    const v = clean(raw);
    const a = field.answer;
    switch (field.kind) {
      case 'int':
        return /^-?\d+$/.test(v) && Number(v) === Number(a) ? { ok: true } : { ok: false };
      case 'bin':
        if (!/^[01]+$/.test(v)) return { ok: false, note: 'Binary numbers only use the digits 0 and 1.' };
        return parseInt(v, 2) === parseInt(String(a), 2) ? { ok: true } : { ok: false };
      case 'bin4':
        if (!/^[01]+$/.test(v)) return { ok: false, note: 'Binary numbers only use the digits 0 and 1.' };
        if (parseInt(v, 2) === parseInt(a, 2) && v.length !== 4) return { ok: false, note: 'Right value, but write it with exactly 4 bits: <b>' + a + '</b>.' };
        return v === a ? { ok: true } : { ok: false };
      case 'hexdigit':
        if (/^\d+$/.test(v) && Number(v) > 9 && Number(v) === parseInt(a, 16)) return { ok: false, note: 'Right value, but in hex ' + v + ' is written as the single digit <b>' + a + '</b>.' };
        return v.toUpperCase() === String(a).toUpperCase() ? { ok: true } : { ok: false };
      case 'num': {
        const n = Number(v.replace(',', '.'));
        if (!/^-?\d*[.,]?\d+$/.test(v)) return { ok: false, note: 'Type a number, e.g. 7.3' };
        return Math.abs(n - Number(a)) <= (field.tol == null ? 0.05 : field.tol) ? { ok: true } : { ok: false };
      }
      case 'text':
        return v.toUpperCase().replace(/^=/, '') === clean(a).toUpperCase().replace(/^=/, '') ? { ok: true } : { ok: false };
      case 'choice':
        return v.toLowerCase() === clean(a).toLowerCase() ? { ok: true } : { ok: false };
      case 'hex':
        if (!/^[0-9a-fA-F]+$/.test(v)) return { ok: false, note: 'Hex digits are 0–9 and A–F only.' };
        return parseInt(v, 16) === parseInt(a, 16) ? { ok: true } : { ok: false };
    }
    return { ok: false };
  }

  function show(i) {
    if (i >= steps.length) { if (opts.onFinish) opts.onFinish(usedHelp); return; }
    const st = steps[i];
    const box = document.createElement('div');
    box.className = 'gstep current';
    let html = st.html.replace(/\{(\d+)\}/g, (m, k) => {
      const f = st.fields[Number(k)];
      if (f.options) return `<select class="gin gsel" data-k="${k}" aria-label="${f.label || 'Answer'}"><option value="">choose…</option>` +
        f.options.map(o => `<option>${o}</option>`).join('') + '</select>';
      return `<input class="gin" data-k="${k}" type="text" autocomplete="off" autocapitalize="characters" spellcheck="false" aria-label="${f.label || 'Answer'}" size="${f.size || 4}">`;
    });
    box.innerHTML =
      `<div class="gstep-num">Step ${i + 1}</div>` +
      `<div class="gstep-body"><div class="gstep-q">${html}</div>` +
      (st.info ? '' : `<div class="gstep-actions"><button type="button" class="lesson-btn primary g-check">Check</button><button type="button" class="lesson-btn g-show">Show me</button></div>`) +
      `<div class="gstep-msg" aria-live="polite"></div></div>`;
    container.appendChild(box);

    const msg = box.querySelector('.gstep-msg');
    const inputs = [...box.querySelectorAll('.gin')];

    const finish = (revealed) => {
      box.classList.remove('current');
      box.classList.add(revealed ? 'revealed' : 'done');
      inputs.forEach(inp => { inp.disabled = true; inp.classList.remove('bad'); inp.classList.add(revealed ? 'shown' : 'good'); });
      box.querySelectorAll('.gstep-actions').forEach(n => n.remove());
      msg.className = 'gstep-msg ' + (revealed ? '' : 'ok');
      msg.innerHTML = (revealed ? '👀 ' : '✅ ') + (st.why || 'Correct!');
      if (opts.onStep) opts.onStep(i, st, revealed);
      show(i + 1);
    };

    if (st.info) { finish(false); box.classList.add('info'); msg.innerHTML = st.why || ''; msg.className = 'gstep-msg'; return; }

    function check() {
      if (inputs.some(inp => clean(inp.value) === '')) {
        msg.className = 'gstep-msg bad'; msg.textContent = 'Fill in every box first.'; return;
      }
      const notes = [];
      let allOk = true;
      const custom = st.validate ? st.validate(inputs.map(inp => clean(inp.value))) : null;
      inputs.forEach((inp, n) => {
        const r = custom ? { ok: custom.ok[n] } : test(st.fields[Number(inp.dataset.k)], inp.value);
        inp.classList.toggle('good', r.ok); inp.classList.toggle('bad', !r.ok);
        if (!r.ok) { allOk = false; if (r.note) notes.push(r.note); }
      });
      if (custom && custom.notes) notes.push(...custom.notes);
      if (allOk) { finish(false); if (opts.onCheck) opts.onCheck(true); return; }
      if (opts.onCheck) opts.onCheck(false);
      const wrongCount = inputs.filter(inp => inp.classList.contains('bad')).length;
      msg.className = 'gstep-msg bad';
      msg.innerHTML = '❌ ' + (inputs.length > 1 ? (wrongCount === 1 ? 'One box (in red) is not right yet.' : wrongCount + ' boxes (in red) are not right yet.') : 'Not right yet.') +
        (notes.length ? '<br>' + [...new Set(notes)].join('<br>') : '') +
        (st.hint ? '<br><span class="g-hint">💡 ' + st.hint + '</span>' : '') +
        '<br><span class="g-hint">Fix what is in red and press Check again, or press <b>Show me</b>.</span>';
    }

    box.querySelector('.g-check').addEventListener('click', check);
    box.querySelector('.g-show').addEventListener('click', () => {
      usedHelp = true;
      inputs.forEach(inp => { inp.value = st.fields[Number(inp.dataset.k)].answer; });
      inputs.forEach(inp => { if (inp.tagName === 'SELECT') inp.value = st.fields[Number(inp.dataset.k)].answer; });
      finish(true);
    });
    inputs.forEach((inp, n) => inp.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter') return;
      if (n < inputs.length - 1 && clean(inputs[n + 1].value) === '') inputs[n + 1].focus(); else check();
    }));
    if (i > 0 || opts.focusFirst) inputs[0] && inputs[0].focus({ preventScroll: false });
  }

  show(0);
}


/* =====================================================================
   Walkthrough: a short explanation shown one card at a time.
   runWalkthrough(container, [{ title, html }, …])
   ===================================================================== */
function runWalkthrough(container, slides) {
  let i = 0;
  container.innerHTML =
    '<div class="wt-card"><div class="wt-top"><span class="wt-count"></span><h3 class="wt-title"></h3></div>' +
    '<div class="wt-body"></div>' +
    '<div class="wt-nav"><button type="button" class="lesson-btn wt-back">← Back</button>' +
    '<div class="wt-dots"></div>' +
    '<button type="button" class="lesson-btn primary wt-next">Next →</button></div></div>';
  const $q = (s) => container.querySelector(s);
  const dots = $q('.wt-dots');
  dots.innerHTML = slides.map((_, k) => `<button type="button" class="wt-dot" aria-label="Card ${k + 1}" data-k="${k}"></button>`).join('');
  function draw() {
    $q('.wt-count').textContent = `${i + 1} / ${slides.length}`;
    $q('.wt-title').innerHTML = slides[i].title;
    $q('.wt-body').innerHTML = slides[i].html;
    $q('.wt-back').disabled = i === 0;
    $q('.wt-next').textContent = i === slides.length - 1 ? 'Start again ↺' : 'Next →';
    dots.querySelectorAll('.wt-dot').forEach((d, k) => d.classList.toggle('on', k === i));
  }
  $q('.wt-back').addEventListener('click', () => { if (i > 0) { i--; draw(); } });
  $q('.wt-next').addEventListener('click', () => { i = (i + 1) % slides.length; draw(); });
  dots.addEventListener('click', (e) => { const d = e.target.closest('.wt-dot'); if (d) { i = Number(d.dataset.k); draw(); } });
  draw();
}

// Shared "finished" banner for guided practice
function practiceEnd(stepsEl, usedHelp, onNext) {
  const end = document.createElement('div');
  end.className = 'gstep-end';
  end.innerHTML = (usedHelp ? '👍 Finished. Try another one on your own.' : '🎉 Well done! You solved it without help.') +
    ' <button type="button" class="lesson-btn primary">Next question →</button>';
  end.querySelector('button').addEventListener('click', onNext);
  stepsEl.appendChild(end);
}


/* =====================================================================
   "How was this lesson?" box at the end of every lesson.
   Sends to /api/feedback; the teacher reads it on feedback-dashboard.html.
   ===================================================================== */
function feedbackBox(slug) {
  shareBar();
  if (document.getElementById('fbBox')) return;
  const wrap = document.querySelector('.lesson-wrap');
  if (!wrap) return;
  const box = document.createElement('div');
  box.className = 'lesson-panel fb-panel';
  box.id = 'fbBox';
  const levels = ['Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', 'Lower Sixth', 'Upper Sixth', 'Other'];
  box.innerHTML = `
    <h2>💬 How was this lesson?</h2>
    <p class="lesson-hint">Tell your teacher. Every message is read and helps make the lessons better.</p>
    <form class="fb-form" novalidate>
      <p class="fb-label">Did you understand it?</p>
      <div class="fb-choices" role="radiogroup" aria-label="Did you understand it?">
        <button type="button" class="fb-choice" data-v="yes" role="radio" aria-checked="false">😀 Yes</button>
        <button type="button" class="fb-choice" data-v="partly" role="radio" aria-checked="false">🙂 A little</button>
        <button type="button" class="fb-choice" data-v="no" role="radio" aria-checked="false">😕 Not yet</button>
      </div>
      <label class="fb-field">What was hard or confusing? <span>(optional)</span>
        <textarea name="hard" rows="2" maxlength="600" placeholder="e.g. I don't understand the minus signs"></textarea></label>
      <label class="fb-field">Do you have a question? <span>(optional)</span>
        <textarea name="question" rows="2" maxlength="600" placeholder="Ask anything about this lesson"></textarea></label>
      <div class="fb-row">
        <label class="fb-field">First name <span>(optional)</span><input name="name" maxlength="40" autocomplete="given-name"></label>
        <label class="fb-field">Class <span>(optional)</span><select name="level"><option value="">—</option>${levels.map(l => `<option>${l}</option>`).join('')}</select></label>
      </div>
      <input name="website" class="fb-trap" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button type="submit" class="lesson-btn primary fb-send">Send to my teacher</button>
      <div class="fb-msg" aria-live="polite"></div>
    </form>`;
  const next = wrap.querySelector('.lesson-next, .lesson-feedback');
  if (next) wrap.insertBefore(box, next); else wrap.appendChild(box);

  const form = box.querySelector('form'), msg = box.querySelector('.fb-msg'), send = box.querySelector('.fb-send');
  let understood = '';
  box.querySelectorAll('.fb-choice').forEach(b => b.addEventListener('click', () => {
    understood = b.dataset.v; msg.textContent = '';
    box.querySelectorAll('.fb-choice').forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-checked', on); });
  }));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const data = {
      lesson: slug, understood,
      hard: (f.get('hard') || '').trim(), question: (f.get('question') || '').trim(),
      name: (f.get('name') || '').trim(), level: f.get('level') || '', website: f.get('website') || '',
    };
    if (!data.understood && !data.hard && !data.question) {
      msg.className = 'fb-msg bad'; msg.textContent = 'Choose Yes, A little or Not yet, or write something first.'; return;
    }
    send.disabled = true; msg.className = 'fb-msg'; msg.textContent = 'Sending…';
    const wa = 'https://wa.me/237682402876?text=' + encodeURIComponent(
      `Lesson: ${document.title.split('—')[0].trim()}\nUnderstood: ${({ yes: 'Yes', partly: 'A little', no: 'Not yet' })[understood] || '-'}` +
      (data.hard ? `\nHard: ${data.hard}` : '') + (data.question ? `\nQuestion: ${data.question}` : ''));
    try {
      const r = await fetch('/api/feedback', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
      if (!r.ok) throw new Error(r.status);
      form.innerHTML = `<p class="fb-thanks">✅ Thank you${data.name ? ', ' + data.name.replace(/[<>&"]/g, '') : ''}! Your teacher will read this.</p>` +
        (data.question ? `<p class="lesson-hint">Need an answer quickly? <a class="inline-link" href="${wa}" target="_blank" rel="noopener">Ask on WhatsApp →</a></p>` : '') +
        (understood === 'no' || understood === 'partly' ? '<p class="lesson-hint">Tip: read the short cards again, then try one more question with <b>Show me</b> on the hard step.</p>' : '');
      if (typeof gtag === 'function') gtag('event', 'lesson_feedback', { lesson: slug, understood: understood || 'none' });
    } catch (err) {
      send.disabled = false;
      msg.className = 'fb-msg bad';
      msg.innerHTML = `Sorry, it didn't send. <a class="inline-link" href="${wa}" target="_blank" rel="noopener">Send it on WhatsApp instead →</a>`;
    }
  });
}


// Shuffle a copy of a list (for multiple-choice options)
function shuffle(list) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

// Standard practice runner: question text + steps + score + "next question"
function practice(cfg) {
  // cfg: { slug, questionEl, stepsEl, scoreEl, build: () => ({ q, steps, onStep? }) , afterRender? }
  let done = 0, clean = 0;
  function next() {
    const Q = cfg.build();
    cfg.questionEl.innerHTML = Q.q;
    if (Q.before && cfg.extraEl) cfg.extraEl.innerHTML = Q.before; else if (cfg.extraEl) cfg.extraEl.innerHTML = '';
    runSteps(cfg.stepsEl, Q.steps, {
      onCheck: (ok) => trackLesson(cfg.slug, ok ? 'check_correct' : 'check_wrong'),
      onStep: Q.onStep,
      onFinish: (usedHelp) => {
        done++; if (!usedHelp) clean++;
        if (cfg.scoreEl) cfg.scoreEl.textContent = `${done} finished · ${clean} without help`;
        practiceEnd(cfg.stepsEl, usedHelp, () => { next(); cfg.questionEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
        trackLesson(cfg.slug, 'question_finished');
      },
    });
    if (Q.after) Q.after();
  }
  next();
  return next;
}


/* =====================================================================
   Share a lesson: WhatsApp, copy link, or the phone's own share menu.
   shareLesson(url, title, button) is also used by the cards on lessons.html.
   ===================================================================== */
function lessonUrl() {
  const c = document.querySelector('link[rel="canonical"]');
  return c ? c.href : location.origin + location.pathname;
}

function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
  return new Promise((resolve, reject) => {
    const t = document.createElement('textarea');
    t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
    document.body.appendChild(t); t.select();
    try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); }
    t.remove();
  });
}

function shareButtons(url, title) {
  const text = `Try this free lesson: ${title} ${url}`;
  const wrap = document.createElement('div');
  wrap.className = 'share-bar';
  wrap.innerHTML =
    `<a class="share-btn wa" href="https://wa.me/?text=${encodeURIComponent(text)}" target="_blank" rel="noopener">💬 Share on WhatsApp</a>` +
    '<button type="button" class="share-btn copy">🔗 Copy link</button>' +
    (navigator.share ? '<button type="button" class="share-btn more">📤 More</button>' : '') +
    '<span class="share-msg" aria-live="polite"></span>';
  const msg = wrap.querySelector('.share-msg');
  wrap.querySelector('.copy').addEventListener('click', () => {
    copyText(url).then(() => { msg.textContent = '✅ Link copied. Paste it to your classmates.'; },
                       () => { msg.innerHTML = `Copy this link: <input class="share-url" value="${url}" readonly>`; const i = msg.querySelector('input'); i.focus(); i.select(); });
    if (typeof gtag === 'function') gtag('event', 'share_lesson', { method: 'copy', url });
  });
  wrap.querySelector('.wa').addEventListener('click', () => { if (typeof gtag === 'function') gtag('event', 'share_lesson', { method: 'whatsapp', url }); });
  const more = wrap.querySelector('.more');
  if (more) more.addEventListener('click', () => {
    navigator.share({ title, text: `Try this free lesson: ${title}`, url }).catch(() => {});
    if (typeof gtag === 'function') gtag('event', 'share_lesson', { method: 'native', url });
  });
  return wrap;
}

function shareBar() {
  const wrap = document.querySelector('.lesson-wrap');
  if (!wrap || wrap.querySelector('.share-bar')) return;
  const title = (document.querySelector('.lesson-wrap h1') || {}).textContent || document.title;
  const lead = wrap.querySelector('p.lead') || wrap.querySelector('h1');
  const top = shareButtons(lessonUrl(), title.trim());
  top.classList.add('share-top');
  lead.insertAdjacentElement('afterend', top);
  const next = wrap.querySelector('.lesson-next, .lesson-feedback');
  if (next) {
    const box = document.createElement('div');
    box.className = 'share-end';
    box.innerHTML = '<p class="lesson-hint">Found this useful? Send it to a classmate:</p>';
    box.appendChild(shareButtons(lessonUrl(), title.trim()));
    next.insertBefore(box, next.querySelector('.fb') || null);
  }
}


/* =====================================================================
   "Stuck? Ask the AI tutor" card + WhatsApp Channel button, added to
   every lesson page. The tutor opens with this lesson already asked.
   ===================================================================== */
const ACADEMY_CHANNEL = 'https://whatsapp.com/channel/0029VbE2bN42f3ELs70szW0B';

function lessonContext() {
  const parts = location.pathname.split('/').filter(Boolean);   // lessons/form-3/mathematics/slug
  const nice = s => (s || '').split('-').map(w => w === 'ict' ? 'ICT' : w[0].toUpperCase() + w.slice(1)).join(' ');
  const h1 = document.querySelector('.lesson-wrap h1');
  return {
    title: (h1 ? h1.textContent : document.title.split('|')[0]).trim(),
    level: parts[0] === 'lessons' ? nice(parts[1]) : '',
    subject: parts[0] === 'lessons' ? nice(parts[2]) : '',
  };
}

// The lesson's own content as plain text, so the tutor teaches it the same way.
function lessonText(c) {
  const plain = html => {
    const d = document.createElement('div');
    d.innerHTML = String(html || '')
      .replace(/<sup>(.*?)<\/sup>/gi, '^($1)').replace(/<sub>(.*?)<\/sub>/gi, '_($1)')   // 9<sup>1/2</sup> → 9^(1/2)
      .replace(/<\/(td|th)>/gi, ' | ')
      .replace(/<\/(tr|p|li|h\d)>|<br\s*\/?>/gi, '\n');
    return d.textContent.replace(/[ \t]+/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
  };
  let body = '';
  if (typeof LESSON !== 'undefined' && LESSON && Array.isArray(LESSON.cards)) {
    body = LESSON.cards.map(card => `${card.title}:\n${plain(card.html)}`).join('\n\n');
  } else {
    const learn = document.getElementById('learn');
    body = learn ? learn.innerText : '';
  }
  return `Lesson: ${c.title}${c.subject ? ` (${c.level} ${c.subject})` : ''}\n\n${body}`.slice(0, 3800);
}

function tutorHelp() {
  const wrap = document.querySelector('.lesson-wrap');
  if (!wrap || document.getElementById('tutorHelp')) return;
  const c = lessonContext();
  const about = `"${c.title}"${c.subject ? ` (${c.level} ${c.subject})` : ''}`;
  const q = `I'm studying the lesson ${about}. Please explain it to me simply, step by step, with an example.`;
  const params = obj => new URLSearchParams(Object.assign(c.level ? { level: c.level } : {}, obj)).toString();
  const box = document.createElement('div');
  box.className = 'lesson-panel tutor-help';
  box.id = 'tutorHelp';
  box.innerHTML = `
    <div class="th-text">
      <h3>🤔 Stuck on this lesson?</h3>
      <p>Ask the free AI tutor. It explains step by step, answers your questions, or teaches it as a live class on the board.</p>
    </div>
    <div class="th-actions">
      <a class="next-btn primary" href="/tutor?${params({ tab: 'ask', q })}">💬 Ask the AI tutor</a>
      <a class="next-btn" href="/tutor?${params({ tab: 'class', topic: `${c.title}${c.subject ? ` (${c.level} ${c.subject})` : ''}` })}">🖍️ Watch it as a live class</a>
    </div>`;
  const anchor = wrap.querySelector('.lesson-pn') || wrap.querySelector('.lesson-next');
  if (anchor) wrap.insertBefore(box, anchor); else wrap.appendChild(box);
  box.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    try { localStorage.setItem('tutor-lesson-ctx', JSON.stringify({ title: c.title, text: lessonText(c), at: Date.now() })); }
    catch (e) { /* storage blocked: the tutor still gets the lesson title */ }
    if (typeof gtag === 'function') gtag('event', 'lesson_to_tutor', { lesson: location.pathname, action: a.href.includes('tab=class') ? 'class' : 'ask' });
  }));
}

function channelButton() {
  const next = document.querySelector('.lesson-wrap .lesson-next');
  if (!next || next.querySelector('.channel-btn')) return;
  const p = document.createElement('p');
  p.className = 'channel-line';
  p.innerHTML = `<a class="channel-btn" href="${ACADEMY_CHANNEL}" target="_blank" rel="noopener">📢 Join our WhatsApp Channel</a><span>New lessons, GCE tips and exam reminders, free.</span>`;
  p.querySelector('a').addEventListener('click', () => { if (typeof gtag === 'function') gtag('event', 'join_channel', { from: 'lesson' }); });
  const fb = next.querySelector('.fb');
  next.insertBefore(p, fb || null);
}

if (document.querySelector('.lesson-wrap')) {
  if (location.pathname.startsWith('/lessons/')) tutorHelp();   // real lessons, not the lessons index
  channelButton();
}
