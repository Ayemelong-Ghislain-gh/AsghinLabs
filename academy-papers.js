/* =====================================================================
   Past-papers library (/past-papers, /epreuves): filter by exam, search a
   subject, quick subject buttons. Works without this script too: every
   paper is a plain link in the page.
   ===================================================================== */
(function () {
  const box = document.getElementById('ppSearch');
  if (!box) return;
  const chips = [...document.querySelectorAll('.pp-chip')];
  const quicks = [...document.querySelectorAll('.pp-quick')];
  const exams = [...document.querySelectorAll('.pp-exam')];
  const empty = document.getElementById('ppEmpty');
  const norm = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  const opened = new Map();            // details → was it open before searching?
  let exam = 'all';

  function apply() {
    const words = norm(box.value).split(/\s+/).filter(Boolean);
    let found = 0;
    exams.forEach(sec => {
      const examOk = exam === 'all' || sec.dataset.exam === exam;
      let inSec = 0;
      sec.querySelectorAll('details.pp-year').forEach(d => {
        let n = 0;
        d.querySelectorAll('.pp-sub').forEach(a => {
          const ok = examOk && words.every(w => norm(a.dataset.search).includes(w));
          a.hidden = !ok; if (ok) n++;
        });
        d.hidden = !n;
        if (words.length) {
          if (!opened.has(d)) opened.set(d, d.open);
          d.open = n > 0;
        } else if (opened.has(d)) {
          d.open = opened.get(d);
        }
        inSec += n;
      });
      if (!words.length) opened.clear();
      sec.hidden = !inSec; found += inSec;
    });
    empty.hidden = found > 0;
    quicks.forEach(q => q.classList.toggle('on', norm(q.dataset.q) === norm(box.value.trim())));
  }

  chips.forEach(c => c.addEventListener('click', () => {
    exam = c.dataset.exam;
    chips.forEach(x => { const on = x === c; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
    history.replaceState(null, '', exam === 'all' ? location.pathname : '#' + exam);
    apply();
  }));
  quicks.forEach(q => q.addEventListener('click', () => {
    box.value = q.classList.contains('on') ? '' : q.dataset.q;
    apply(); box.focus();
  }));
  let timer;
  box.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(apply, 120); });

  // Arriving on /past-papers#gce-advanced-level shows only that exam.
  const start = location.hash.slice(1);
  const chip = chips.find(c => c.dataset.exam === start);
  if (chip) chip.click();

  document.querySelectorAll('.pp-sub').forEach(a => a.addEventListener('click', () => {
    if (typeof gtag === 'function') gtag('event', 'open_past_paper', { paper: a.dataset.search, exam: a.closest('.pp-exam').dataset.exam });
  }));
})();
