/* =====================================================================
   Activities for theory lessons (AsghinLabs Academy)
   runActivities(container, activities, { slug })

   Activity types (all phone friendly — tap, no dragging):
     mcq      { type, q, options: [..], answer: 'text of right option', why }
     tf       { type, q, answer: true|false, why }
     sort     { type, q, groups: ['A','B'], items: [['item','A'], ...], why }
     match    { type, q, pairs: [['left','right'], ...], why }
     order    { type, q, items: ['first', 'second', ...] (correct order), why }
     label    { type, q, svg: '<svg>… numbered markers …</svg>', labels: ['answer for 1', 'answer for 2', ...], why }
     fill     { type, q: 'instruction', q2: 'sentence with {0} and {1}', answers: [['ok', 'also ok'], ['…']], why }
   Any activity may have:  hint, visual (HTML shown above the question)
   ===================================================================== */
function runActivities(container, acts, opts) {
  opts = opts || {};
  const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  // Maths answers (digits, no real words): ignore spaces, accept − or -, × or *, and 2,5 = 2.5.
  // Text answers: ignore case, spaces and punctuation.
  const norm = (s) => {
    s = String(s).toLowerCase().replace(/[−–]/g, '-').replace(/×/g, '*').trim();
    if (/\d/.test(s) && !/[a-z]{3,}/.test(s)) return s.replace(/\s+/g, '').replace(/(\d),(\d)/g, '$1.$2').replace(/^\+/, '').replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
    return s.replace(/[\s.,'’-]+/g, ' ').trim();
  };
  let firstTry = 0, finished = 0;

  container.innerHTML = '<div class="act-progress"><div class="act-bar"><i></i></div><span></span></div><div class="act-list"></div>';
  const list = container.querySelector('.act-list');
  const bar = container.querySelector('.act-bar i'), barTxt = container.querySelector('.act-progress span');
  const progress = () => {
    bar.style.width = (finished / acts.length * 100) + '%';
    barTxt.textContent = `${finished} of ${acts.length} done`;
  };
  progress();

  const TITLES = { mcq: 'Choose the right answer', tf: 'True or false?', sort: 'Sort into groups', match: 'Match the pairs', order: 'Put in order', label: 'Label the picture', fill: 'Fill in the blanks' };

  function show(i) {
    if (i >= acts.length) return end();
    const A = acts[i];
    const box = document.createElement('div');
    box.className = 'act current act-' + A.type;
    box.innerHTML = `<div class="act-head"><span class="act-num">${i + 1}/${acts.length}</span><span class="act-type">${A.title || TITLES[A.type]}</span></div>` +
      (A.visual ? `<div class="act-visual">${A.visual}</div>` : '') +
      `<p class="act-q">${A.q}</p><div class="act-body"></div>` +
      `<div class="act-actions"><button type="button" class="lesson-btn primary a-check">Check</button><button type="button" class="lesson-btn a-show" hidden>Show me</button></div>` +
      '<div class="act-msg" aria-live="polite"></div>';
    list.appendChild(box);
    const body = box.querySelector('.act-body'), msg = box.querySelector('.act-msg');
    const api = BUILD[A.type](A, body);
    let tries = 0;

    function done(revealed) {
      if (!revealed && tries === 1) firstTry++;
      finished++; progress();
      box.classList.remove('current'); box.classList.add(revealed ? 'revealed' : 'done');
      api.lock();
      box.querySelector('.act-actions').remove();
      msg.className = 'act-msg ' + (revealed ? 'shown' : 'ok');
      msg.innerHTML = (revealed ? '👀 ' : (tries === 1 ? '✅ Correct! ' : '✅ Well done. ')) + (A.why || '');
      if (typeof trackLesson === 'function') trackLesson(opts.slug || 'lesson', revealed ? 'activity_revealed' : 'activity_correct');
      show(i + 1);
    }
    box.querySelector('.a-check').addEventListener('click', () => {
      const r = api.check();
      if (r === null) { msg.className = 'act-msg bad'; msg.textContent = 'Answer every part first.'; return; }
      tries++;
      if (r.ok) return done(false);
      msg.className = 'act-msg bad';
      msg.innerHTML = '❌ ' + (r.text || 'Not yet.') + (A.hint ? `<br><span class="g-hint">💡 ${A.hint}</span>` : '') +
        '<br><span class="g-hint">Change what is in red and press Check again' + (tries >= 1 ? ', or press <b>Show me</b>' : '') + '.</span>';
      box.querySelector('.a-show').hidden = false;
      if (typeof trackLesson === 'function') trackLesson(opts.slug || 'lesson', 'activity_wrong');
    });
    box.querySelector('.a-show').addEventListener('click', () => { api.reveal(); done(true); });
    if (i > 0) box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function end() {
    const e = document.createElement('div');
    e.className = 'gstep-end act-end';
    const pct = Math.round(firstTry / acts.length * 100);
    e.innerHTML = `<div>${pct >= 80 ? '🎉 Excellent!' : pct >= 50 ? '👍 Good work!' : '💪 Keep going!'} You got <b>${firstTry} of ${acts.length}</b> right on the first try.</div>` +
      '<button type="button" class="lesson-btn primary">↺ Try again</button>';
    e.querySelector('button').addEventListener('click', () => {
      runActivities(container, acts, opts);
      container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    list.appendChild(e);
    if (typeof trackLesson === 'function') trackLesson(opts.slug || 'lesson', 'activities_finished');
  }

  // ---------- each activity type: build(A, body) → { check(), reveal(), lock() } ----------
  const BUILD = {
    mcq(A, body) {
      const opts2 = A.keep ? A.options : shuffle(A.options);
      body.innerHTML = '<div class="a-options">' + opts2.map(o => `<button type="button" class="a-opt" role="radio" aria-checked="false">${o}</button>`).join('') + '</div>';
      let picked = null;
      body.querySelectorAll('.a-opt').forEach((b, k) => b.addEventListener('click', () => {
        if (b.disabled) return;
        picked = opts2[k];
        body.querySelectorAll('.a-opt').forEach(x => { x.classList.toggle('on', x === b); x.classList.remove('bad'); x.setAttribute('aria-checked', x === b); });
      }));
      return {
        check() {
          if (picked === null) return null;
          const ok = picked === A.answer;
          body.querySelectorAll('.a-opt').forEach((b, k) => { if (opts2[k] === picked) b.classList.toggle('bad', !ok); });
          return { ok, text: A.wrong && A.wrong[picked] ? A.wrong[picked] : 'That is not the right answer.' };
        },
        reveal() { picked = A.answer; body.querySelectorAll('.a-opt').forEach((b, k) => b.classList.toggle('on', opts2[k] === A.answer)); },
        lock() { body.querySelectorAll('.a-opt').forEach((b, k) => { b.disabled = true; b.classList.remove('bad'); if (opts2[k] === A.answer) b.classList.add('good'); }); },
      };
    },
    tf(A, body) {
      return BUILD.mcq({ ...A, options: ['True', 'False'], answer: A.answer ? 'True' : 'False', keep: true }, body);
    },
    sort(A, body) {
      const items = shuffle(A.items);
      body.innerHTML = '<div class="a-sort">' + items.map(([t]) => `<div class="a-row"><span class="a-item">${t}</span><span class="a-seg">` +
        A.groups.map(g => `<button type="button" class="a-segb" data-g="${esc(g)}">${g}</button>`).join('') + '</span></div>').join('') + '</div>';
      const chosen = items.map(() => null);
      body.querySelectorAll('.a-row').forEach((row, k) => row.querySelectorAll('.a-segb').forEach(b => b.addEventListener('click', () => {
        if (b.disabled) return;
        chosen[k] = b.dataset.g;
        row.querySelectorAll('.a-segb').forEach(x => x.classList.toggle('on', x === b));
        row.classList.remove('bad');
      })));
      const rows = () => [...body.querySelectorAll('.a-row')];
      return {
        check() {
          if (chosen.some(c => c === null)) return null;
          let wrong = 0;
          rows().forEach((row, k) => { const ok = chosen[k] === items[k][1]; row.classList.toggle('bad', !ok); if (!ok) wrong++; });
          return { ok: !wrong, text: wrong === 1 ? '1 item is in the wrong group (in red).' : `${wrong} items are in the wrong group (in red).` };
        },
        reveal() { rows().forEach((row, k) => { chosen[k] = items[k][1]; row.querySelectorAll('.a-segb').forEach(x => x.classList.toggle('on', x.dataset.g === items[k][1])); }); },
        lock() { rows().forEach(row => { row.classList.remove('bad'); row.classList.add('good'); row.querySelectorAll('.a-segb').forEach(b => { b.disabled = true; }); }); },
      };
    },
    match(A, body) {
      const rights = shuffle(A.pairs.map(p => p[1]));
      const lefts = shuffle(A.pairs);
      body.innerHTML = '<div class="a-match">' + lefts.map(([l]) => `<div class="a-row"><span class="a-item">${l}</span><select class="gin gsel a-sel"><option value="">choose…</option>` +
        rights.map(r => `<option value="${esc(r)}">${r}</option>`).join('') + '</select></div>').join('') + '</div>';
      const sels = () => [...body.querySelectorAll('.a-sel')];
      sels().forEach(s => s.addEventListener('change', () => s.closest('.a-row').classList.remove('bad')));
      return {
        check() {
          if (sels().some(s => !s.value)) return null;
          let wrong = 0;
          sels().forEach((s, k) => { const ok = s.value === lefts[k][1]; s.closest('.a-row').classList.toggle('bad', !ok); if (!ok) wrong++; });
          return { ok: !wrong, text: wrong === 1 ? '1 pair is not right (in red).' : `${wrong} pairs are not right (in red).` };
        },
        reveal() { sels().forEach((s, k) => { s.value = lefts[k][1]; }); },
        lock() { sels().forEach(s => { s.disabled = true; s.closest('.a-row').classList.remove('bad'); s.closest('.a-row').classList.add('good'); }); },
      };
    },
    order(A, body) {
      let cur = shuffle(A.items);
      if (cur.every((x, k) => x === A.items[k])) cur = cur.slice().reverse();
      function draw(locked) {
        body.innerHTML = '<ol class="a-order">' + cur.map((t, k) => `<li class="a-row"><span class="a-item">${t}</span>` +
          (locked ? '' : `<span class="a-moves"><button type="button" class="a-mv" data-k="${k}" data-d="-1" aria-label="Move up" ${k === 0 ? 'disabled' : ''}>▲</button><button type="button" class="a-mv" data-k="${k}" data-d="1" aria-label="Move down" ${k === cur.length - 1 ? 'disabled' : ''}>▼</button></span>`) + '</li>').join('') + '</ol>';
        body.querySelectorAll('.a-mv').forEach(b => b.addEventListener('click', () => {
          const k = Number(b.dataset.k), j = k + Number(b.dataset.d);
          [cur[k], cur[j]] = [cur[j], cur[k]]; draw(false);
        }));
      }
      draw(false);
      return {
        check() {
          let wrong = 0;
          body.querySelectorAll('.a-row').forEach((row, k) => { const ok = cur[k] === A.items[k]; row.classList.toggle('bad', !ok); if (!ok) wrong++; });
          return { ok: !wrong, text: `${wrong} item${wrong === 1 ? ' is' : 's are'} not in the right place (in red). Use ▲ ▼ to move them.` };
        },
        reveal() { cur = A.items.slice(); draw(false); },
        lock() { draw(true); body.querySelectorAll('.a-row').forEach(r => r.classList.add('good')); },
      };
    },
    label(A, body) {
      const choices = shuffle(A.labels);
      body.innerHTML = `<div class="a-label-pic">${A.svg}</div><div class="a-match">` + A.labels.map((_, k) => `<div class="a-row"><span class="a-item"><span class="a-marker">${k + 1}</span></span><select class="gin gsel a-sel"><option value="">choose…</option>` +
        choices.map(r => `<option value="${esc(r)}">${r}</option>`).join('') + '</select></div>').join('') + '</div>';
      const sels = () => [...body.querySelectorAll('.a-sel')];
      sels().forEach(s => s.addEventListener('change', () => s.closest('.a-row').classList.remove('bad')));
      return {
        check() {
          if (sels().some(s => !s.value)) return null;
          let wrong = 0;
          sels().forEach((s, k) => { const ok = s.value === A.labels[k]; s.closest('.a-row').classList.toggle('bad', !ok); if (!ok) wrong++; });
          return { ok: !wrong, text: wrong === 1 ? '1 label is not right (in red).' : `${wrong} labels are not right (in red).` };
        },
        reveal() { sels().forEach((s, k) => { s.value = A.labels[k]; }); },
        lock() { sels().forEach(s => { s.disabled = true; s.closest('.a-row').classList.remove('bad'); s.closest('.a-row').classList.add('good'); }); },
      };
    },
    fill(A, body) {
      body.innerHTML = '<p class="a-fill">' + A.q2.replace(/\{(\d+)\}/g, (m, k) => `<input class="gin a-in" data-k="${k}" autocomplete="off" spellcheck="false" size="${Math.max(6, ...A.answers[k].map(a => a.length))}">`) + '</p>';
      const ins = () => [...body.querySelectorAll('.a-in')];
      ins().forEach(inp => inp.addEventListener('input', () => inp.classList.remove('bad')));
      return {
        check() {
          if (ins().some(i => !i.value.trim())) return null;
          let wrong = 0;
          ins().forEach(i => { const ok = A.answers[i.dataset.k].some(a => norm(a) === norm(i.value)); i.classList.toggle('bad', !ok); i.classList.toggle('good', ok); if (!ok) wrong++; });
          return { ok: !wrong, text: wrong === 1 ? '1 word is not right (in red).' : `${wrong} words are not right (in red).` };
        },
        reveal() { ins().forEach(i => { i.value = A.answers[i.dataset.k][0]; }); },
        lock() { ins().forEach(i => { i.disabled = true; i.classList.remove('bad'); i.classList.add('good'); }); },
      };
    },
  };

  show(0);
}
