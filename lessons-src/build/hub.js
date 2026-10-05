<script>
(function () {
  const buttons = document.querySelectorAll('#hubClasses .hub-filter');
  const sections = document.querySelectorAll('.hub-subject');
  const hasLessons = (s) => !!s.querySelector('.lrow:not(.soon)');
  function show(c) {
    if (![...buttons].some(b => b.dataset.class === c)) c = 'all';
    buttons.forEach(b => { const on = b.dataset.class === c; b.classList.toggle('active', on); b.setAttribute('aria-selected', on); });
    sections.forEach(s => { s.hidden = c === 'all' ? !hasLessons(s) : s.dataset.class !== c; });
    try { localStorage.setItem('lessonClass', c); } catch (e) {}
  }
  buttons.forEach(btn => btn.addEventListener('click', () => {
    show(btn.dataset.class);
    history.replaceState(null, '', btn.dataset.class === 'all' ? location.pathname : '#' + btn.dataset.class);
  }));
  let start = location.hash.slice(1);
  if (!start) { try { start = localStorage.getItem('lessonClass') || 'all'; } catch (e) { start = 'all'; } }
  show(start);

  // Remember which chapters a student opened
  const chapters = document.querySelectorAll('details.chapter');
  let openSet = [];
  try { openSet = JSON.parse(localStorage.getItem('openChapters') || '[]'); } catch (e) {}
  chapters.forEach((d, i) => {
    const id = d.closest('.hub-subject').dataset.class + ':' + d.querySelector('.ch-t').textContent;
    if (openSet.includes(id)) d.open = true;
    d.addEventListener('toggle', () => {
      if (d.dataset.searching) return;
      openSet = openSet.filter(x => x !== id); if (d.open) openSet.push(id);
      try { localStorage.setItem('openChapters', JSON.stringify(openSet.slice(-30))); } catch (e) {}
    });
  });

  // Search through every class, chapter and lesson
  const box = document.getElementById('lessonSearch'), empty = document.getElementById('hubEmpty');
  const tabs = document.getElementById('hubClasses');
  const norm = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  const saved = new Map();
  box.addEventListener('input', () => {
    const words = norm(box.value).split(/\s+/).filter(Boolean);
    if (!words.length) {
      tabs.hidden = false; empty.hidden = true;
      document.querySelectorAll('.lrow, details.chapter, .hub-level, .chapters').forEach(el => { el.hidden = false; });
      chapters.forEach(d => { if (saved.has(d)) { d.dataset.searching = '1'; d.open = saved.get(d); delete d.dataset.searching; } });
      saved.clear();
      show(document.querySelector('#hubClasses .active').dataset.class); return;
    }
    tabs.hidden = true;
    let found = 0;
    sections.forEach(sec => {
      let inSec = 0;
      sec.querySelectorAll('.chapters').forEach(group => {
        let inGroup = 0;
        group.querySelectorAll('details.chapter').forEach(d => {
          const chapterHit = words.every(w => norm(d.dataset.search).includes(w));
          let n = 0;
          d.querySelectorAll('.lrow').forEach(row => {
            const ok = chapterHit || words.every(w => norm(row.dataset.search).includes(w));
            row.hidden = !ok; if (ok) n++;
          });
          d.hidden = !n;
          if (!saved.has(d)) saved.set(d, d.open);
          d.dataset.searching = '1'; d.open = n > 0; delete d.dataset.searching;
          inGroup += n;
        });
        group.hidden = !inGroup; group.previousElementSibling.hidden = !inGroup; inSec += inGroup;
      });
      sec.hidden = !inSec; found += inSec;
    });
    empty.hidden = found > 0;
  });

  // Share buttons on each lesson
  document.querySelectorAll('.row-share').forEach(btn => btn.addEventListener('click', () => {
    const row = btn.closest('.lrow');
    const open = row.querySelector('.share-bar');
    document.querySelectorAll('.lrow .share-bar').forEach(el => el.remove());
    if (open) return;
    if (typeof shareButtons === 'function') row.appendChild(shareButtons(btn.dataset.url, btn.dataset.title));
  }));
})();
</script>