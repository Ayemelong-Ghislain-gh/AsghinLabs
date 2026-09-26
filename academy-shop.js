/* =====================================================================
   ACADEMY — workbook shop (order basket → WhatsApp)
   Workbooks, prices and the WhatsApp number live in academy-data.js.
   ===================================================================== */
(function () {
  const grid = document.getElementById('workbookGrid');
  if (!grid || typeof ACADEMY_WORKBOOKS === 'undefined') return;

  const PHONE = typeof ACADEMY_WHATSAPP !== 'undefined' ? ACADEMY_WHATSAPP : '237682402876';
  const BOOKS = ACADEMY_WORKBOOKS;
  const byId = Object.fromEntries(BOOKS.map(b => [b.id, b]));
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const money = (n) => n.toLocaleString('en-US').replace(/,/g, ' ') + ' FCFA';
  const priceLabel = (b) => b.price ? money(b.price) : 'Ask for price';

  // ---------- Basket (kept for this visitor between visits) ----------
  let cart = {};
  try { cart = JSON.parse(localStorage.getItem('asghin-cart') || '{}') || {}; } catch (e) { cart = {}; }
  Object.keys(cart).forEach(id => { if (!byId[id] || !(cart[id] > 0)) delete cart[id]; });
  const save = () => { try { localStorage.setItem('asghin-cart', JSON.stringify(cart)); } catch (e) {} };
  const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
  const total = () => Object.entries(cart).reduce((a, [id, q]) => a + (byId[id].price || 0) * q, 0);
  const hasUnpriced = () => Object.keys(cart).some(id => !byId[id].price);

  function setQty(id, q) {
    if (q <= 0) delete cart[id]; else cart[id] = Math.min(q, 200);
    save();
    refresh();
  }

  // ---------- Filters ----------
  const subjects = ['All', ...new Set(BOOKS.map(b => b.subject))];
  let activeSubject = 'All';
  const filterEl = document.getElementById('workbookFilters');
  if (filterEl) {
    filterEl.innerHTML = subjects.map(s =>
      `<button type="button" class="wb-filter${s === 'All' ? ' active' : ''}" data-subject="${esc(s)}" aria-pressed="${s === 'All'}">${esc(s === 'All' ? 'All subjects' : s)}</button>`
    ).join('');
    filterEl.addEventListener('click', e => {
      const btn = e.target.closest('.wb-filter');
      if (!btn) return;
      activeSubject = btn.dataset.subject;
      filterEl.querySelectorAll('.wb-filter').forEach(b => {
        const on = b === btn;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', on);
      });
      renderGrid();
    });
  }

  function cardActions(b) {
    const q = cart[b.id] || 0;
    if (!q) {
      return `<button type="button" class="wb-add" data-add="${b.id}">🛒 Add to order</button>
              <button type="button" class="wb-buy" data-buy="${b.id}">Order now →</button>`;
    }
    return `<div class="wb-stepper" role="group" aria-label="Quantity">
              <button type="button" data-dec="${b.id}" aria-label="One less">−</button>
              <span>${q} in order</span>
              <button type="button" data-inc="${b.id}" aria-label="One more">+</button>
            </div>
            <button type="button" class="wb-buy" data-open-cart>Checkout →</button>`;
  }

  function renderGrid() {
    const list = BOOKS.filter(b => activeSubject === 'All' || b.subject === activeSubject);
    grid.innerHTML = list.map(b => `
      <article class="wb-card${b.pack ? ' is-pack' : ''}" data-id="${b.id}">
        <div class="wb-cover">
          <img src="${esc(b.cover)}" alt="${esc(b.subject)} — ${esc(b.title)}" loading="lazy" width="600" height="800">
          ${b.status === 'preorder' ? '<span class="wb-badge">Pre-order</span>' : (b.pack ? '<span class="wb-badge pack">⭐ 2-year exam pack</span>' : '')}
        </div>
        <div class="wb-body">
          <span class="wb-subject">${esc(b.subject)}</span>
          <h4>${esc(b.title)}</h4>
          <p class="wb-stage">${esc(b.stage)}</p>
          <p class="wb-price">${esc(priceLabel(b))}</p>
          <div class="wb-actions">${cardActions(b)}</div>
        </div>
      </article>`).join('');
  }

  function refreshCards() {
    grid.querySelectorAll('.wb-card').forEach(card => {
      const b = byId[card.dataset.id];
      card.classList.toggle('in-cart', !!cart[b.id]);
      card.querySelector('.wb-actions').innerHTML = cardActions(b);
    });
  }

  // ---------- Sticky order bar ----------
  const bar = document.createElement('div');
  bar.className = 'order-bar';
  bar.innerHTML = `
    <div class="order-bar-info"><strong class="ob-count"></strong><span class="ob-total"></span></div>
    <button type="button" class="order-bar-btn" data-open-cart>Review order →</button>`;
  document.body.appendChild(bar);

  // ---------- Order panel ----------
  const panel = document.createElement('div');
  panel.className = 'order-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'true');
  panel.setAttribute('aria-label', 'Your workbook order');
  panel.innerHTML = `
    <div class="order-sheet">
      <div class="order-head">
        <h3>🛒 Your order</h3>
        <button type="button" class="order-close" aria-label="Close">✕</button>
      </div>
      <div class="order-items"></div>
      <div class="order-total"></div>
      <form class="order-form" id="orderForm" novalidate>
        <label for="orderName">Your name</label>
        <input id="orderName" type="text" autocomplete="name" required placeholder="e.g. Ngwa Brenda">
        <label for="orderPhone">Phone / WhatsApp number</label>
        <input id="orderPhone" type="tel" autocomplete="tel" required placeholder="e.g. 6XX XXX XXX">
        <label for="orderTown">Town &amp; school (optional)</label>
        <input id="orderTown" type="text" placeholder="e.g. Bamenda — GHS Down Town">
        <fieldset class="order-delivery">
          <legend>How do you want to receive it?</legend>
          <label><input type="radio" name="orderDelivery" value="Delivery" checked> Delivery</label>
          <label><input type="radio" name="orderDelivery" value="Pickup"> I'll pick it up</label>
        </fieldset>
        <label for="orderNote">Note (optional)</label>
        <textarea id="orderNote" rows="2" placeholder="Anything we should know"></textarea>
        <button type="submit" class="order-send">💬 Send order on WhatsApp</button>
        <p class="order-feedback" aria-live="polite"></p>
        <p class="order-small">No payment on this site. We confirm your order, the total and delivery with you on WhatsApp.</p>
      </form>
    </div>`;
  document.body.appendChild(panel);

  const itemsEl = panel.querySelector('.order-items');
  const totalEl = panel.querySelector('.order-total');
  const feedback = panel.querySelector('.order-feedback');
  let lastFocus = null;

  function renderPanel() {
    const ids = Object.keys(cart);
    if (!ids.length) {
      itemsEl.innerHTML = `<p class="order-empty">Your order is empty. Add a workbook to get started.</p>`;
      totalEl.textContent = '';
      return;
    }
    itemsEl.innerHTML = ids.map(id => {
      const b = byId[id];
      return `
        <div class="order-item">
          <img src="${esc(b.cover)}" alt="" width="48" height="64">
          <div class="order-item-info">
            <strong>${esc(b.subject)} — ${esc(b.title)}</strong>
            <span>${esc(priceLabel(b))}</span>
          </div>
          <div class="wb-stepper small">
            <button type="button" data-dec="${id}" aria-label="One less">−</button>
            <span>${cart[id]}</span>
            <button type="button" data-inc="${id}" aria-label="One more">+</button>
          </div>
        </div>`;
    }).join('');
    totalEl.innerHTML = `<span>Total</span><strong>${money(total())}${hasUnpriced() ? ' + items to confirm' : ''}</strong>`;
  }

  function openPanel() {
    lastFocus = document.activeElement;
    renderPanel();
    panel.classList.add('open');
    document.body.style.overflow = 'hidden';
    panel.querySelector('.order-close').focus();
  }
  function closePanel() {
    panel.classList.remove('open');
    document.body.style.overflow = '';
    feedback.textContent = '';
    if (lastFocus) lastFocus.focus();
  }

  function refresh() {
    const n = count();
    bar.classList.toggle('show', n > 0);
    document.body.classList.toggle('has-order-bar', n > 0);
    bar.querySelector('.ob-count').textContent = `${n} workbook${n === 1 ? '' : 's'}`;
    bar.querySelector('.ob-total').textContent = money(total()) + (hasUnpriced() ? ' +' : '');
    refreshCards();
    if (panel.classList.contains('open')) renderPanel();
  }

  document.addEventListener('click', e => {
    const t = e.target.closest('[data-add],[data-buy],[data-inc],[data-dec],[data-open-cart]');
    if (!t) return;
    if (t.dataset.add) { setQty(t.dataset.add, 1); track('add_to_order', t.dataset.add); }
    else if (t.dataset.buy) { if (!cart[t.dataset.buy]) setQty(t.dataset.buy, 1); track('add_to_order', t.dataset.buy); openPanel(); }
    else if (t.dataset.inc) setQty(t.dataset.inc, (cart[t.dataset.inc] || 0) + 1);
    else if (t.dataset.dec) setQty(t.dataset.dec, (cart[t.dataset.dec] || 0) - 1);
    else if ('openCart' in t.dataset) openPanel();
  });

  panel.querySelector('.order-close').addEventListener('click', closePanel);
  panel.addEventListener('click', e => { if (e.target === panel) closePanel(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('open')) closePanel(); });

  function track(name, id) {
    if (typeof gtag === 'function') gtag('event', name, { item: id });
  }

  panel.querySelector('#orderForm').addEventListener('submit', e => {
    e.preventDefault();
    const name = panel.querySelector('#orderName').value.trim();
    const phone = panel.querySelector('#orderPhone').value.trim();
    const town = panel.querySelector('#orderTown').value.trim();
    const note = panel.querySelector('#orderNote').value.trim();
    const delivery = (panel.querySelector('input[name="orderDelivery"]:checked') || {}).value || 'Delivery';

    if (!count()) { feedback.textContent = 'Add at least one workbook first.'; feedback.style.color = '#ffaa66'; return; }
    if (!name || !phone) { feedback.textContent = '✏️ Please add your name and phone number.'; feedback.style.color = '#ffaa66'; return; }

    let msg = `Hello AsghinLabs Academy 👋, I'd like to order these workbooks:\n\n`;
    Object.entries(cart).forEach(([id, q]) => {
      const b = byId[id];
      msg += `• ${q} × ${b.subject} — ${b.title}${b.price ? ` (${money(b.price * q)})` : ''}\n`;
    });
    msg += `\nTotal: ${money(total())}${hasUnpriced() ? ' + items to confirm' : ''}\n`;
    msg += `\nName: ${name}\nPhone: ${phone}\n`;
    if (town) msg += `Town/School: ${town}\n`;
    msg += `Receive by: ${delivery}\n`;
    if (note) msg += `Note: ${note}\n`;

    track('send_order', Object.keys(cart).join(','));
    window.open(`https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    feedback.textContent = '✨ Opening WhatsApp — just press send. Your basket is kept until you clear it.';
    feedback.style.color = '#2ee68b';
  });

  // "Order for a whole class or school" link can preselect a subject tab.
  document.querySelectorAll('[data-shop-subject]').forEach(a => a.addEventListener('click', () => {
    const btn = filterEl && filterEl.querySelector(`[data-subject="${a.dataset.shopSubject}"]`);
    if (btn) btn.click();
  }));

  renderGrid();
  refresh();
})();
