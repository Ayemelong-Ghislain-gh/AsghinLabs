/* =====================================================================
   ACADEMY — notes & past questions (with on-site PDF reader)
   Content comes from academy-data.js.
   ===================================================================== */
(function () {
  const LEVEL_ORDER = ['Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', 'O Level',
    'Lower Sixth', 'Upper Sixth', 'A Level'];

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  function groupByLevel(items) {
    const groups = new Map();
    items.forEach(item => {
      const level = item.level || 'General';
      if (!groups.has(level)) groups.set(level, []);
      groups.get(level).push(item);
    });
    const keys = [
      ...LEVEL_ORDER.filter(l => groups.has(l)),
      ...[...groups.keys()].filter(l => !LEVEL_ORDER.includes(l)),
    ];
    return keys.map(level => ({ level, items: groups.get(level) }));
  }

  function fileName(path) {
    return path.split('/').pop();
  }

  function fileCard(item, index, listKey) {
    const meta = [item.pages ? `${item.pages} pages` : '', item.size || '', 'PDF']
      .filter(Boolean).join(' · ');
    const cover = item.cover
      ? `<img src="${esc(item.cover)}" alt="Cover of ${esc(item.title)}" loading="lazy" width="600" height="776">`
      : `<div class="note-cover-fallback"><span>📄</span><strong>${esc(item.subject || 'Notes')}</strong><em>${esc(item.level || '')}</em></div>`;
    return `
      <article class="note-card">
        <button type="button" class="note-cover" data-read="${listKey}:${index}" aria-label="Read ${esc(item.title)} online">
          ${cover}
          <span class="note-cover-hint">📖 Read online</span>
        </button>
        <div class="note-body">
          <span class="academy-file-subject">${esc(item.subject || '')}${item.level ? ' · ' + esc(item.level) : ''}</span>
          <h4>${esc(item.title)}</h4>
          <p class="note-meta">${esc(meta)} · Free</p>
          <div class="note-actions">
            <button type="button" class="note-btn primary" data-read="${listKey}:${index}">📖 Read online</button>
            <a class="note-btn" href="${esc(item.file)}" download="${esc(fileName(item.file))}">⬇ Download</a>
          </div>
        </div>
      </article>`;
  }

  const LISTS = {
    notes: typeof ACADEMY_NOTES !== 'undefined' ? ACADEMY_NOTES : [],
    past: typeof ACADEMY_PAST_QUESTIONS !== 'undefined' ? ACADEMY_PAST_QUESTIONS : [],
  };

  function renderList(containerId, listKey, emptyIcon, emptyText, emptySub) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const items = LISTS[listKey];

    if (!items.length) {
      el.innerHTML = `
        <div class="academy-empty">
          <div class="academy-empty-icon">${emptyIcon}</div>
          <p>${emptyText}</p>
          <p class="academy-empty-sub">${emptySub}</p>
        </div>`;
      return;
    }

    // Keep each item's original index so the Read button finds it.
    const indexed = items.map((item, i) => ({ ...item, _i: i }));
    el.innerHTML = groupByLevel(indexed).map(group => `
      <div class="academy-level-group">
        <h3 class="academy-level-heading">${esc(group.level)}</h3>
        <div class="note-grid">
          ${group.items.map(item => fileCard(item, item._i, listKey)).join('')}
        </div>
      </div>`).join('');
  }

  renderList('notesGallery', 'notes', '🗂️', 'No notes uploaded yet — check back soon.',
    'Complete programs and lesson notes will be added here as they\'re ready.');
  renderList('pastQuestionsGallery', 'past', '🧾', 'Past questions are coming soon.',
    'Message us on WhatsApp if you need a specific paper now.');

  /* ================= PDF READER =================
     Uses PDF.js so PDFs open inside the page on every device — including
     Android phones, which otherwise just download the file. Pages render
     only when you scroll to them, so big files open fast. */
  // PDF.js (Mozilla, Apache-2.0) is hosted with the site in vendor/pdfjs/,
  // so the reader doesn't depend on any outside CDN.
  const PDFJS_URL = new URL('vendor/pdfjs/pdf.min.js', document.baseURI).href;
  const PDFJS_WORKER = new URL('vendor/pdfjs/pdf.worker.min.js', document.baseURI).href;
  let pdfjsPromise = null;

  function loadPdfJs() {
    if (!pdfjsPromise) {
      pdfjsPromise = import(PDFJS_URL).then(lib => {
        lib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER;
        return lib;
      }).catch(err => { pdfjsPromise = null; throw err; });
    }
    return pdfjsPromise;
  }

  const reader = document.createElement('div');
  reader.className = 'pdf-reader';
  reader.setAttribute('role', 'dialog');
  reader.setAttribute('aria-modal', 'true');
  reader.setAttribute('aria-label', 'Document reader');
  reader.innerHTML = `
    <div class="pdf-reader-bar">
      <button type="button" class="pdf-reader-close" aria-label="Close reader">✕</button>
      <div class="pdf-reader-title"></div>
      <div class="pdf-reader-page" aria-live="polite"></div>
      <div class="pdf-reader-actions">
        <button type="button" class="pdf-zoom" data-zoom="-1" aria-label="Zoom out">−</button>
        <button type="button" class="pdf-zoom" data-zoom="1" aria-label="Zoom in">+</button>
        <a class="pdf-reader-download" href="#" download>⬇ <span>Download</span></a>
      </div>
    </div>
    <div class="pdf-reader-body" tabindex="0">
      <div class="pdf-reader-pages"></div>
      <div class="pdf-reader-status"></div>
    </div>`;
  document.body.appendChild(reader);

  const titleEl = reader.querySelector('.pdf-reader-title');
  const pageEl = reader.querySelector('.pdf-reader-page');
  const bodyEl = reader.querySelector('.pdf-reader-body');
  const pagesEl = reader.querySelector('.pdf-reader-pages');
  const statusEl = reader.querySelector('.pdf-reader-status');
  const dlEl = reader.querySelector('.pdf-reader-download');

  let currentDoc = null;
  let currentTask = null;
  let zoom = 1;
  let observer = null;
  let pageObserver = null;
  let lastFocus = null;

  function closeReader() {
    reader.classList.remove('open');
    document.body.style.overflow = '';
    if (observer) observer.disconnect();
    if (pageObserver) pageObserver.disconnect();
    if (currentTask) { try { currentTask.destroy(); } catch (e) {} }
    currentDoc = null; currentTask = null;
    pagesEl.innerHTML = '';
    if (location.hash.startsWith('#read=')) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    if (lastFocus) lastFocus.focus();
  }

  async function renderPage(holder) {
    if (!currentDoc || holder.dataset.state === 'done' || holder.dataset.state === 'busy') return;
    holder.dataset.state = 'busy';
    const docAtStart = currentDoc;
    try {
      const page = await currentDoc.getPage(Number(holder.dataset.page));
      if (docAtStart !== currentDoc) return;
      const cssWidth = holder.clientWidth;
      const base = page.getViewport({ scale: 1 });
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const viewport = page.getViewport({ scale: (cssWidth / base.width) * dpr });
      const canvas = document.createElement('canvas');
      canvas.width = Math.floor(viewport.width);
      canvas.height = Math.floor(viewport.height);
      await page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
      if (docAtStart !== currentDoc) return;
      holder.innerHTML = '';
      holder.appendChild(canvas);
      holder.dataset.state = 'done';
    } catch (e) {
      holder.dataset.state = '';
    }
  }

  function layoutPages(ratio) {
    const n = currentDoc.numPages;
    const width = Math.min(bodyEl.clientWidth - 24, 900) * zoom;
    pagesEl.style.width = width + 'px';
    const frag = document.createDocumentFragment();
    for (let i = 1; i <= n; i++) {
      const holder = document.createElement('div');
      holder.className = 'pdf-page';
      holder.dataset.page = i;
      holder.style.aspectRatio = ratio;
      holder.innerHTML = `<span class="pdf-page-num">${i}</span>`;
      frag.appendChild(holder);
    }
    pagesEl.innerHTML = '';
    pagesEl.appendChild(frag);

    if (observer) observer.disconnect();
    observer = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) renderPage(e.target); });
    }, { root: bodyEl, rootMargin: '800px 0px' });

    if (pageObserver) pageObserver.disconnect();
    pageObserver = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) pageEl.textContent = `Page ${e.target.dataset.page} / ${n}`;
      });
    }, { root: bodyEl, rootMargin: '-50% 0px -50% 0px' });

    pagesEl.querySelectorAll('.pdf-page').forEach(h => { observer.observe(h); pageObserver.observe(h); });
    pageEl.textContent = `Page 1 / ${n}`;
  }

  let pageRatio = '612 / 792';

  async function openReader(item, key) {
    lastFocus = document.activeElement;
    zoom = 1;
    titleEl.textContent = item.title;
    dlEl.href = item.file;
    dlEl.setAttribute('download', fileName(item.file));
    pageEl.textContent = '';
    pagesEl.innerHTML = '';
    statusEl.innerHTML = '<div class="pdf-spinner"></div>Opening document…';
    statusEl.style.display = 'block';
    reader.classList.add('open');
    document.body.style.overflow = 'hidden';
    reader.querySelector('.pdf-reader-close').focus();
    if (key) history.replaceState(null, '', '#read=' + key);
    if (typeof gtag === 'function') gtag('event', 'read_notes', { item: item.title });

    try {
      const pdfjsLib = await loadPdfJs();
      currentTask = pdfjsLib.getDocument({ url: item.file, disableAutoFetch: true, rangeChunkSize: 262144 });
      currentDoc = await currentTask.promise;
      const first = await currentDoc.getPage(1);
      const vp = first.getViewport({ scale: 1 });
      pageRatio = `${vp.width} / ${vp.height}`;
      statusEl.style.display = 'none';
      layoutPages(pageRatio);
      bodyEl.scrollTop = 0;
    } catch (e) {
      statusEl.innerHTML = `The reader couldn't open this file on your device.<br>
        <a class="note-btn primary" href="${esc(item.file)}" target="_blank" rel="noopener">Open the PDF</a>
        <a class="note-btn" href="${esc(item.file)}" download>⬇ Download</a>`;
    }
  }

  reader.querySelector('.pdf-reader-close').addEventListener('click', closeReader);
  reader.querySelectorAll('.pdf-zoom').forEach(btn => btn.addEventListener('click', () => {
    if (!currentDoc) return;
    const next = Math.min(2.5, Math.max(0.6, zoom + Number(btn.dataset.zoom) * 0.25));
    if (next === zoom) return;
    const scrollRatio = bodyEl.scrollTop / Math.max(1, bodyEl.scrollHeight);
    zoom = next;
    layoutPages(pageRatio);
    bodyEl.scrollTop = scrollRatio * bodyEl.scrollHeight;
  }));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && reader.classList.contains('open')) closeReader();
  });
  dlEl.addEventListener('click', () => {
    if (typeof gtag === 'function') gtag('event', 'download_notes', { item: titleEl.textContent });
  });

  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-read]');
    if (!btn) return;
    const [key, idx] = btn.dataset.read.split(':');
    const item = (LISTS[key] || [])[Number(idx)];
    if (item) openReader(item, btn.dataset.read);
  });

  // Shareable link: academy.html#read=notes:0 opens that document directly.
  const m = location.hash.match(/^#read=(notes|past):(\d+)$/);
  if (m && LISTS[m[1]][Number(m[2])]) openReader(LISTS[m[1]][Number(m[2])], `${m[1]}:${m[2]}`);
})();
