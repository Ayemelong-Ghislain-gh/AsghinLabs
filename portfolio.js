(function () {
  const tabsEl = document.getElementById('portfolioTabs');
  const categoryToggle = document.getElementById('categoryToggle');
  const categoryToggleLabel = document.getElementById('categoryToggleLabel');
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

  // Items currently shown in the lightbox (mirrors whatever category is active)
  let currentItems = [];
  let lightboxIndex = 0;

  // ---- Carousel state ----
  let carouselItems = [];
  let carouselIndex = 0;
  let carouselDegrees = 0;
  let carouselAngleStep = 0;
  let carouselBoxEl = null;
  let carouselCaptionEl = null;

  function debounce(fn, wait) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), wait);
    };
  }

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
        tabsEl.classList.remove('open');
      });
      tabsEl.appendChild(btn);
    });
    const activeCat = groupCategories.find(c => c.id === currentCategory);
    if (categoryToggleLabel && activeCat) categoryToggleLabel.textContent = activeCat.label;
  }

  // Mobile "hamburger" dropdown for switching categories
  if (categoryToggle) {
    categoryToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      tabsEl.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (tabsEl.classList.contains('open') && !tabsEl.contains(e.target) && e.target !== categoryToggle) {
        tabsEl.classList.remove('open');
      }
    });
  }

  function renderGallery() {
    const items = PORTFOLIO_ITEMS[currentCategory] || [];
    currentItems = items;
    galleryEl.innerHTML = '';
    carouselBoxEl = null;
    carouselCaptionEl = null;

    if (items.length === 0) {
      galleryEl.innerHTML = `
        <div class="portfolio-empty">
          <div class="portfolio-empty-icon">🖼️</div>
          <p>No samples uploaded in this category yet.</p>
          <p class="portfolio-empty-sub">Check back soon — new work is added regularly.</p>
        </div>`;
      return;
    }

    if (items.length === 1) {
      buildSingle(items);
      return;
    }

    buildCarousel(items);
  }

  // A single sample doesn't need a spinning ring — just show it large.
  function buildSingle(items) {
    const wrap = document.createElement('div');
    wrap.className = 'carousel-wrap carousel-single';
    wrap.innerHTML = `
      <div class="carousel-stage">
        <div class="carousel-item">
          <img src="${items[0].src}" alt="${items[0].title || 'Portfolio sample'}" loading="lazy">
          <div class="carousel-zoom-hint">🔍</div>
        </div>
      </div>
      <div class="carousel-caption">${items[0].title || ''}</div>
    `;
    galleryEl.appendChild(wrap);
    wrap.querySelector('.carousel-item').addEventListener('click', () => openLightbox(0));
  }

  // 2+ samples: a 3D ring sized to fit exactly that many items, evenly spaced.
  function buildCarousel(items) {
    carouselItems = items;
    carouselIndex = 0;
    carouselDegrees = 0;

    const n = items.length;
    carouselAngleStep = 360 / n;

    const wrap = document.createElement('div');
    wrap.className = 'carousel-wrap';
    wrap.innerHTML = `
      <div class="carousel-stage" tabindex="0" aria-label="Sample carousel, use arrow keys or swipe to browse">
        <div class="carousel-box"></div>
      </div>
      <div class="carousel-caption"></div>
      <div class="carousel-nav">
        <button type="button" class="carousel-btn prev" aria-label="Previous sample">‹</button>
        <button type="button" class="carousel-btn next" aria-label="Next sample">›</button>
      </div>
    `;
    galleryEl.appendChild(wrap);

    carouselBoxEl = wrap.querySelector('.carousel-box');
    carouselCaptionEl = wrap.querySelector('.carousel-caption');
    const stage = wrap.querySelector('.carousel-stage');

    items.forEach((item, i) => {
      const face = document.createElement('div');
      face.className = 'carousel-item';
      face.innerHTML = `
        <img src="${item.src}" alt="${item.title || 'Portfolio sample'}" loading="lazy" draggable="false">
        <div class="carousel-zoom-hint">🔍</div>`;
      face.addEventListener('click', () => {
        if (!wrap.dataset.dragging) openLightbox(i);
      });
      carouselBoxEl.appendChild(face);
    });

    positionItems();
    updateCaption();

    wrap.querySelector('.carousel-btn.prev').addEventListener('click', () => rotateCarousel(-1));
    wrap.querySelector('.carousel-btn.next').addEventListener('click', () => rotateCarousel(1));

    // ---- Touch swipe ----
    let touchStartX = 0, touchStartY = 0, touchDeltaX = 0, isTouching = false;

    stage.addEventListener('touchstart', (e) => {
      isTouching = true;
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      touchDeltaX = 0;
      carouselBoxEl.style.transition = 'none';
    }, { passive: true });

    stage.addEventListener('touchmove', (e) => {
      if (!isTouching) return;
      const dx = e.touches[0].clientX - touchStartX;
      const dy = e.touches[0].clientY - touchStartY;
      if (Math.abs(dx) > Math.abs(dy)) {
        touchDeltaX = dx;
        wrap.dataset.dragging = 'true';
        carouselBoxEl.style.transform = `rotateY(${carouselDegrees + dx / 3}deg)`;
      }
    }, { passive: true });

    stage.addEventListener('touchend', () => {
      isTouching = false;
      carouselBoxEl.style.transition = '';
      if (Math.abs(touchDeltaX) > 40) {
        rotateCarousel(touchDeltaX < 0 ? 1 : -1);
      } else {
        applyTransform();
      }
      setTimeout(() => { delete wrap.dataset.dragging; }, 50);
    });

    // ---- Keyboard nav (skips if the lightbox is open, which has its own handler) ----
    stage.addEventListener('keydown', (e) => {
      if (lightbox.classList.contains('open')) return;
      if (e.key === 'ArrowRight') rotateCarousel(1);
      if (e.key === 'ArrowLeft') rotateCarousel(-1);
    });

    window.addEventListener('resize', debounce(() => {
      if (carouselBoxEl) positionItems();
    }, 150));
  }

  function positionItems() {
    if (!carouselBoxEl) return;
    const boxWidth = carouselBoxEl.offsetWidth || 240;
    const n = carouselItems.length;
    // Regular-polygon radius so faces sit edge-to-edge without overlapping.
    // Clamped to a minimum of a 3-sided polygon so 2-item rings don't blow up.
    const radius = (boxWidth / 2) / Math.tan(Math.PI / Math.max(n, 3));
    Array.from(carouselBoxEl.children).forEach((face, i) => {
      face.style.transform = `rotateY(${i * carouselAngleStep}deg) translateZ(${radius}px)`;
    });
    applyTransform();
  }

  function applyTransform() {
    if (carouselBoxEl) carouselBoxEl.style.transform = `rotateY(${carouselDegrees}deg)`;
  }

  function rotateCarousel(direction) {
    carouselDegrees -= direction * carouselAngleStep;
    carouselIndex = ((carouselIndex + direction) % carouselItems.length + carouselItems.length) % carouselItems.length;
    applyTransform();
    updateCaption();
  }

  function updateCaption() {
    if (!carouselCaptionEl) return;
    const item = carouselItems[carouselIndex];
    carouselCaptionEl.innerHTML = `
      ${item?.title || ''}
      <span class="carousel-counter">${carouselIndex + 1} / ${carouselItems.length}</span>
    `;
  }

  // ---- Lightbox (shared by the single-item view and the carousel) ----
  function openLightbox(index) {
    lightboxIndex = index;
    updateLightbox();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function updateLightbox() {
    const item = currentItems[lightboxIndex];
    if (!item) return;
    lightboxImg.src = item.src;
    lightboxImg.alt = item.title || 'Portfolio sample';
    lightboxCaption.textContent = item.title || '';
  }

  function showNextLightbox(delta) {
    if (currentItems.length === 0) return;
    lightboxIndex = (lightboxIndex + delta + currentItems.length) % currentItems.length;
    updateLightbox();
  }

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightboxPrev) lightboxPrev.addEventListener('click', () => showNextLightbox(-1));
  if (lightboxNext) lightboxNext.addEventListener('click', () => showNextLightbox(1));
  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }
  window.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') showNextLightbox(1);
    if (e.key === 'ArrowLeft') showNextLightbox(-1);
  });

  renderHeader();
  renderTabs();
  renderGallery();
})();
