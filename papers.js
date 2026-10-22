/* =====================================================================
   Past-paper pages (/papers/...): tutor buttons, then try A-D, See answer, score.
   Progress is remembered on this phone/computer for each paper.
   ===================================================================== */
(function () {
  const T = window.PV_TEXT || {};
  const track = (name, extra) => { if (typeof gtag === 'function') gtag('event', name, Object.assign({ paper: location.pathname }, extra || {})); };
  document.querySelectorAll('.pv-page-tutor').forEach(a => a.addEventListener('click', () => track('paper_page_tutor', { page: a.dataset.page })));
  document.querySelectorAll('.pv-tutor-all').forEach(a => a.addEventListener('click', () => track('paper_ask_tutor_all')));
  document.querySelectorAll('[data-request-answers]').forEach(a => a.addEventListener('click', () => track('paper_request_answers')));

  const cards = [...document.querySelectorAll('.pv-q')];
  if (!cards.length) return;
  const KEY = 'pv:' + location.pathname;
  const score = document.querySelector('.pv-score');
  const allBtn = document.querySelector('.pv-all');
  let state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };

  function show(card, on) {
    card.querySelector('.pv-answer').hidden = !on;
    card.classList.toggle('open', on);
    card.querySelector('.pv-see').textContent = on ? T.hide : T.see;
  }
  function mark(card, choice) {
    const n = card.id.slice(1), right = card.dataset.answer;
    card.querySelectorAll('.pv-choice').forEach(b => {
      b.classList.toggle('picked', b.dataset.c === choice);
      b.classList.toggle('good', b.dataset.c === choice && choice === right);
      b.classList.toggle('bad', b.dataset.c === choice && choice !== right);
    });
    const fb = card.querySelector('.pv-feedback');
    fb.textContent = choice ? (choice === right ? T.right : T.wrong) : '';
    fb.className = 'pv-feedback ' + (choice ? (choice === right ? 'ok' : 'no') : '');
    if (choice === right) show(card, true);
    state[n] = choice;
  }
  function updateScore() {
    const tried = Object.entries(state).filter(([, c]) => c);
    const ok = tried.filter(([n, c]) => { const el = document.getElementById('q' + n); return el && el.dataset.answer === c; }).length;
    if (score) score.textContent = tried.length ? score.dataset.tpl.replace('{ok}', ok).replace('{done}', tried.length) : '';
  }

  cards.forEach(card => {
    const n = card.id.slice(1);
    if (state[n]) mark(card, state[n]);
    card.querySelectorAll('.pv-choice').forEach(b => b.addEventListener('click', () => {
      mark(card, b.dataset.c); save(); updateScore();
      track('paper_try', { question: n, correct: b.dataset.c === card.dataset.answer });
    }));
    card.querySelector('.pv-see').addEventListener('click', () => {
      const on = card.querySelector('.pv-answer').hidden; show(card, on);
      if (on) track('paper_see_answer', { question: n });
    });
    card.querySelector('.pv-tutor').addEventListener('click', () => track('paper_ask_tutor', { question: n }));
  });
  updateScore();

  let allOn = false;
  if (allBtn) allBtn.addEventListener('click', () => {
    allOn = !allOn; cards.forEach(c => show(c, allOn));
    allBtn.textContent = allOn ? allBtn.dataset.off : allBtn.dataset.on;
  });
  const reset = document.querySelector('.pv-reset');
  if (reset) reset.addEventListener('click', () => {
    state = {}; save(); cards.forEach(c => { mark(c, ''); show(c, false); }); updateScore();
    allOn = false; if (allBtn) allBtn.textContent = allBtn.dataset.on;
  });
  document.querySelectorAll('[data-open-paper]').forEach(a => a.addEventListener('click', () => track('paper_open_official')));
  if (location.hash && /^#q\d+$/.test(location.hash)) { const c = document.querySelector(location.hash); if (c) show(c, true); }
})();
