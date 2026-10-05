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
      show(i + 1);
    };

    if (st.info) { finish(false); box.classList.add('info'); msg.innerHTML = st.why || ''; msg.className = 'gstep-msg'; return; }

    function check() {
      if (inputs.some(inp => clean(inp.value) === '')) {
        msg.className = 'gstep-msg bad'; msg.textContent = 'Fill in every box first.'; return;
      }
      const notes = [];
      let allOk = true;
      inputs.forEach(inp => {
        const r = test(st.fields[Number(inp.dataset.k)], inp.value);
        inp.classList.toggle('good', r.ok); inp.classList.toggle('bad', !r.ok);
        if (!r.ok) { allOk = false; if (r.note) notes.push(r.note); }
      });
      if (allOk) { finish(false); if (opts.onCheck) opts.onCheck(true); return; }
      if (opts.onCheck) opts.onCheck(false);
      const wrongCount = inputs.filter(inp => inp.classList.contains('bad')).length;
      msg.className = 'gstep-msg bad';
      msg.innerHTML = '❌ ' + (inputs.length > 1 ? (wrongCount === 1 ? 'One box (in red) is not right yet.' : wrongCount + ' boxes (in red) are not right yet.') : 'Not right yet.') +
        (notes.length ? '<br>' + [...new Set(notes)].join('<br>') : '') +
        (st.hint ? '<br><span class="g-hint">💡 ' + st.hint + '</span>' : '') +
        '<br><span class="g-hint">Fix the red box and press Check again, or press <b>Show me</b>.</span>';
    }

    box.querySelector('.g-check').addEventListener('click', check);
    box.querySelector('.g-show').addEventListener('click', () => {
      usedHelp = true;
      inputs.forEach(inp => { inp.value = st.fields[Number(inp.dataset.k)].answer; });
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
