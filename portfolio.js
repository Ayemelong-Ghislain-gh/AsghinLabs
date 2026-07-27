(function () {
  const tabsEl = document.getElementById('portfolioTabs');
  const galleryEl = document.getElementById('portfolioGallery');
  const headerTitleEl = document.getElementById('portfolioHeaderTitle');
  const headerSubEl = document.getElementById('portfolioHeaderSub');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');
  const lightboxPrev = document.getElementById('lightboxPrev');
  const lightboxNext = document.getElementById('lightboxNext');

  if (!tabsEl || !galleryEl) return;

  const params = new URLSearchParams(window.location.search);
  const requestedGroup = params.get('group');
  const requestedCat = params.get('cat');

  // Which categories belong to the requested group. Falls back to the
  // first group found if none/an invalid group is specified.
  const defaultGroup = PORTFOLIO_CATEGORIES[0]?.group;
  const currentGroup = (requestedGroup && PORTFOLIO_CATEGORIES.some(c => c.group === requestedGroup))
    ? requestedGroup
    : defaultGroup;

  const groupCategories = PORTFOLIO_CATEGORIES.filter(c => c.group === currentGroup);

  let currentCategory = (requestedCat && groupCategories.some(c => c.id === requestedCat))
    ? requestedCat
    : groupCategories[0]?.id;

  let currentItems = [];
  let currentIndex = 0;

  function renderHeader() {
    const info = (typeof PORTFOLIO_GROUP_INFO !== 'undefined') && PORTFOLIO_GROUP_INFO[currentGroup];
    if (info && headerTitleEl && headerSubEl) {
      headerTitleEl.textContent = info.title;
      headerSubEl.textContent = info.sub;
    }
  }

  function renderTabs() {
    tabsEl.innerHTML = '';
    groupCategories.forEach(cat => {
      const btn = document.createElement('button');
      btn.className = 'portfolio-tab' + (cat.id === currentCategory ? ' active' : '');
      btn.textContent = cat.label;
      btn.type = 'button';
      btn.addEventListener('click', () => {
        currentCategory = cat.id;
        renderTabs();
        renderGallery();
      });
      tabsEl.appendChild(btn);
    });
  }

  function renderGallery() {
    const items = PORTFOLIO_ITEMS[currentCategory] || [];
    currentItems = items;
    galleryEl.innerHTML = '';

    if (items.length === 0) {
      galleryEl.innerHTML = `
        <div class="portfolio-empty">
          <div class="portfolio-empty-icon">🖼️</div>
          <p>No samples uploaded in this category yet.</p>
          <p class="portfolio-empty-sub">Check back soon — new work is added regularly.</p>
        </div>`;
      return;
    }

    items.forEach((item, index) => {
      const card = document.createElement('div');
      card.className = 'portfolio-item';
      card.innerHTML = `
        <img src="${item.src}" alt="${item.title || 'Portfolio sample'}" loading="lazy">
        <div class="portfolio-item-overlay">
          <span>${item.title || ''}</span>
          <span class="portfolio-zoom">🔍</span>
        </div>`;
      card.addEventListener('click', () => openLightbox(index));
      galleryEl.appendChild(card);
    });
  }

  function openLightbox(index) {
    currentIndex = index;
    updateLightbox();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function updateLightbox() {
    const item = currentItems[currentIndex];
    if (!item) return;
    lightboxImg.src = item.src;
    lightboxImg.alt = item.title || 'Portfolio sample';
    lightboxCaption.textContent = item.title || '';
  }

  function showNext(delta) {
    if (currentItems.length === 0) return;
    currentIndex = (currentIndex + delta + currentItems.length) % currentItems.length;
    updateLightbox();
  }

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightboxPrev) lightboxPrev.addEventListener('click', () => showNext(-1));
  if (lightboxNext) lightboxNext.addEventListener('click', () => showNext(1));
  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }
  window.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') showNext(1);
    if (e.key === 'ArrowLeft') showNext(-1);
  });

  renderHeader();
  renderTabs();
  renderGallery();
})();
