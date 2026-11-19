/* =====================================================================
   ACADEMY — workbook shop (order basket → WhatsApp)
   Workbooks, prices and the WhatsApp number live in academy-data.js.
   ===================================================================== */
(function () {
  const grid = document.getElementById('workbookGrid');
  if (!grid || typeof ACADEMY_WORKBOOKS === 'undefined') return;
  // academie.html (francophone subsystem) has <html lang="fr">: same shop, French words.
  const FR = document.documentElement.lang === 'fr';
  const t = (en, fr) => (FR ? fr : en);

  const PHONE = typeof ACADEMY_WHATSAPP !== 'undefined' ? ACADEMY_WHATSAPP : '237682402876';
  const BOOKS = ACADEMY_WORKBOOKS;
  const byId = Object.fromEntries(BOOKS.map(b => [b.id, b]));
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const money = (n) => n.toLocaleString('en-US').replace(/,/g, ' ') + ' FCFA';
  const priceLabel = (b) => b.price ? money(b.price) : t('Ask for price', 'Prix sur demande');

  // Keep the hero "From … FCFA" in sync with the cheapest priced workbook
  const lowestEl = document.getElementById('lowestPrice');
  const priced = BOOKS.filter(b => b.price > 0).map(b => b.price);
  if (lowestEl && priced.length) lowestEl.textContent = money(Math.min(...priced));

  // ---------- Basket (kept for this visitor between visits) ----------
  let cart = {};
  const CART_KEY = FR ? 'asghin-cart-fr' : 'asghin-cart';   // one basket per subsystem
  try { cart = JSON.parse(localStorage.getItem(CART_KEY) || '{}') || {}; } catch (e) { cart = {}; }
  Object.keys(cart).forEach(id => { if (!byId[id] || !(cart[id] > 0)) delete cart[id]; });
  const save = () => { try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {} };
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
  if (!BOOKS.length) {
    // Nothing on sale yet for this subsystem: the page shows its own "coming soon" block.
    const f = document.getElementById('workbookFilters');
    if (f) f.hidden = true;
    grid.hidden = true;
    return;
  }
  let activeSubject = 'All';
  const filterEl = document.getElementById('workbookFilters');

  // ---------- Search (academy-search.js) ----------
  const S = window.AcademySearch;
  let query = '';
  let searchInfo = null;
  if (S && filterEl) {
    const box = document.createElement('div');
    box.className = 'wb-search';
    box.setAttribute('role', 'search');
    box.innerHTML = `
      <label for="wbSearch" class="visually-hidden">${t('Search notes and workbooks', 'Rechercher des notes et cahiers')}</label>
      <span class="wb-search-icon" aria-hidden="true">🔎</span>
      <input id="wbSearch" type="search" autocomplete="off" placeholder="${t('Search: e.g. CSC Upper Sixth, ICT, Form 2 maths, chemistry notes', 'Rechercher : ex. maths, cahier 3e')}">
      <button type="button" class="wb-search-clear" aria-label="${t('Clear search', 'Effacer')}" hidden>✕</button>`;
    filterEl.parentNode.insertBefore(box, filterEl);
    searchInfo = document.createElement('p');
    searchInfo.className = 'wb-search-info';
    searchInfo.setAttribute('aria-live', 'polite');
    filterEl.parentNode.insertBefore(searchInfo, grid);
    const reqLine = document.createElement('p');
    reqLine.className = 'wb-request-line';
    reqLine.innerHTML = t(`Can’t find the notes you need? <button type="button" class="link-btn" data-request-notes="">📩 Request notes</button> and we’ll prepare them.`,
      `Vous ne trouvez pas vos notes ? <button type="button" class="link-btn" data-request-notes="">📩 Demandez-les</button>, nous les préparons.`);
    grid.parentNode.insertBefore(reqLine, grid.nextSibling);
    const input = box.querySelector('input');
    const clear = box.querySelector('.wb-search-clear');
    let timer = null;
    input.addEventListener('input', () => {
      query = input.value.trim();
      clear.hidden = !query;
      renderGrid();
      clearTimeout(timer);
      if (query && typeof gtag === 'function') timer = setTimeout(() => gtag('event', 'search', { search_term: query }), 1200);
    });
    clear.addEventListener('click', () => { input.value = ''; input.dispatchEvent(new Event('input')); input.focus(); });
  }
  if (filterEl) {
    filterEl.innerHTML = subjects.map(s =>
      `<button type="button" class="wb-filter${s === 'All' ? ' active' : ''}" data-subject="${esc(s)}" aria-pressed="${s === 'All'}">${esc(s === 'All' ? t('All subjects', 'Toutes les matières') : s)}</button>`
    ).join('');
    filterEl.addEventListener('click', e => {
      const btn = e.target.closest('.wb-filter');
      if (!btn) return;
      activeSubject = btn.dataset.subject;
      const si = document.getElementById('wbSearch');
      if (si && si.value) { si.value = ''; query = ''; const c = document.querySelector('.wb-search-clear'); if (c) c.hidden = true; }
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
      return `<button type="button" class="wb-add" data-add="${b.id}">🛒 ${t('Add to order', 'Ajouter à la commande')}</button>
              <button type="button" class="wb-buy" data-buy="${b.id}">${t('Order now →', 'Commander →')}</button>`;
    }
    return `<div class="wb-stepper" role="group" aria-label="${t('Quantity', 'Quantité')}">
              <button type="button" data-dec="${b.id}" aria-label="${t('One less', 'Un de moins')}">−</button>
              <span>${q} ${t('in order', 'dans la commande')}</span>
              <button type="button" data-inc="${b.id}" aria-label="${t('One more', 'Un de plus')}">+</button>
            </div>
            <button type="button" class="wb-buy" data-open-cart>${t('Checkout →', 'Valider →')}</button>`;
  }

  function renderGrid() {
    // While searching, look through everything (all subjects, single-level notes too).
    const list = query
      ? BOOKS.filter(b => S.match(b, query))
      : BOOKS.filter(b => activeSubject === 'All' ? !b.hideInAll : b.subject === activeSubject);
    if (filterEl) filterEl.classList.toggle('is-dimmed', !!query);
    if (searchInfo) {
      searchInfo.innerHTML = query && list.length
        ? t(`${list.length} result${list.length === 1 ? '' : 's'} for “${esc(query)}” · <button type="button" class="link-btn" data-request-notes="">Not what you need? Request notes</button>`,
            `${list.length} résultat${list.length === 1 ? '' : 's'} pour « ${esc(query)} » · <button type="button" class="link-btn" data-request-notes="">Pas ce qu’il vous faut ? Demandez</button>`)
        : '';
    }
    if (query && !list.length) {
      grid.innerHTML = S.noResults(query, t('notes or workbooks', 'notes ou cahiers'));
      return;
    }
    grid.innerHTML = list.map(b => `
      <article class="wb-card${b.pack ? ' is-pack' : ''}" data-id="${b.id}">
        <div class="wb-cover">
          <img src="${esc(b.cover)}" alt="${esc(b.subject)} — ${esc(b.title)}" loading="lazy" width="600" height="800">
          ${b.status === 'preorder' ? `<span class="wb-badge">${t('Pre-order', 'Précommande')}</span>` : (b.pack ? `<span class="wb-badge pack">${b.packLabel || t('⭐ 2-year exam pack', '⭐ Pack examen')}</span>` : '')}
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
    <button type="button" class="order-bar-btn" data-open-cart>${t('Review order →', 'Voir la commande →')}</button>`;
  document.body.appendChild(bar);

  // ---------- Order panel ----------
  const panel = document.createElement('div');
  panel.className = 'order-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'true');
  panel.setAttribute('aria-label', t('Your workbook order', 'Votre commande de cahiers'));
  panel.innerHTML = `
    <div class="order-sheet">
      <div class="order-head">
        <h3>🛒 ${t('Your order', 'Votre commande')}</h3>
        <button type="button" class="order-close" aria-label="${t('Close', 'Fermer')}">✕</button>
      </div>
      <div class="order-items"></div>
      <div class="order-total"></div>
      <form class="order-form" id="orderForm" novalidate>
        <label for="orderName">${t('Your name', 'Votre nom')}</label>
        <input id="orderName" type="text" autocomplete="name" required placeholder="${t('e.g. Ngwa Brenda', 'ex. Ngo Bassa Carine')}">
        <label for="orderPhone">${t('Phone / WhatsApp number', 'Téléphone / WhatsApp')}</label>
        <input id="orderPhone" type="tel" autocomplete="tel" required placeholder="${t('e.g. 6XX XXX XXX', 'ex. 6XX XXX XXX')}">
        <label for="orderTown">${t('Town &amp; school (optional)', 'Ville et établissement (facultatif)')}</label>
        <input id="orderTown" type="text" placeholder="${t('e.g. Bamenda — GHS Down Town', 'ex. Douala — Lycée de Bonabéri')}">
        <fieldset class="order-delivery">
          <legend>${t('How do you want to receive it?', 'Comment voulez-vous le recevoir ?')}</legend>
          <label><input type="radio" name="orderDelivery" value="Delivery" checked> ${t('Delivery', 'Livraison')}</label>
          <label><input type="radio" name="orderDelivery" value="Pickup"> ${t("I'll pick it up", 'Je passe le récupérer')}</label>
        </fieldset>
        <label for="orderNote">${t('Note (optional)', 'Remarque (facultatif)')}</label>
        <textarea id="orderNote" rows="2" placeholder="${t('Anything we should know', 'Une précision pour nous ?')}"></textarea>
        <button type="button" class="order-send order-pay" data-pay-now>💳 ${t('Pay now · MTN MoMo or Orange Money', 'Payer maintenant · MTN MoMo ou Orange Money')}</button>
        <button type="submit" class="order-send order-send-wa">💬 ${t('Or order on WhatsApp, pay later', 'Ou commander sur WhatsApp, payer après')}</button>
        <p class="order-feedback" aria-live="polite"></p>
        <p class="order-small">${t('Secure payment through Fapshi. You pay on Fapshi’s page and come back here with your order confirmed. We then deliver or send your notes on WhatsApp.', 'Paiement sécurisé via Fapshi. Vous payez sur la page Fapshi puis revenez ici avec votre commande confirmée. Nous livrons ou envoyons vos notes sur WhatsApp.')}</p>
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
      itemsEl.innerHTML = `<p class="order-empty">${t('Your order is empty. Add a workbook or notes to get started.', 'Votre commande est vide. Ajoutez un cahier pour commencer.')}</p>`;
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
    totalEl.innerHTML = `<span>Total</span><strong>${money(total())}${hasUnpriced() ? t(' + items to confirm', ' + articles à confirmer') : ''}</strong>`;
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
    bar.querySelector('.ob-count').textContent = FR ? `${n} article${n === 1 ? '' : 's'}` : `${n} item${n === 1 ? '' : 's'}`;
    bar.querySelector('.ob-total').textContent = money(total()) + (hasUnpriced() ? ' +' : '');
    refreshCards();
    if (typeof refreshPayBtn === 'function') refreshPayBtn();
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

    if (!count()) { feedback.textContent = t('Add at least one item first.', "Ajoutez d'abord au moins un cahier."); feedback.style.color = '#ffaa66'; return; }
    if (!name || !phone) { feedback.textContent = t('✏️ Please add your name and phone number.', '✏️ Indiquez votre nom et votre numéro de téléphone.'); feedback.style.color = '#ffaa66'; return; }

    let msg = t(`Hello AsghinLabs Academy 👋, I'd like to order:\n\n`,
      `Bonjour AsghinLabs Academy 👋, je souhaite commander ces cahiers (sous-système francophone) :\n\n`);
    Object.entries(cart).forEach(([id, q]) => {
      const b = byId[id];
      msg += `• ${q} × ${b.subject} — ${b.title}${b.price ? ` (${money(b.price * q)})` : ''}\n`;
    });
    msg += `\nTotal: ${money(total())}${hasUnpriced() ? t(' + items to confirm', ' + articles à confirmer') : ''}\n`;
    msg += t(`\nName: ${name}\nPhone: ${phone}\n`, `\nNom : ${name}\nTéléphone : ${phone}\n`);
    if (town) msg += t(`Town/School: ${town}\n`, `Ville/Établissement : ${town}\n`);
    msg += t(`Receive by: ${delivery}\n`, `Réception : ${delivery === 'Pickup' ? 'Retrait' : 'Livraison'}\n`);
    if (note) msg += t(`Note: ${note}\n`, `Remarque : ${note}\n`);
    if (Object.keys(cart).some(id => id.startsWith('notes-'))) msg += t('(PDF notes: please send them on WhatsApp)\n', '(Notes PDF : à envoyer sur WhatsApp)\n');

    track('send_order', Object.keys(cart).join(','));
    window.open(`https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    feedback.textContent = t('✨ Opening WhatsApp — just press send. Your basket is kept until you clear it.', '✨ WhatsApp s’ouvre : appuyez simplement sur Envoyer. Votre panier est conservé.');
    feedback.style.color = '#2ee68b';
  });

  // ---------- Pay online with Fapshi (MTN MoMo / Orange Money) ----------
  const payBtn = panel.querySelector('[data-pay-now]');
  if (!document.getElementById('payBtnStyle')) {
    const st = document.createElement('style');
    st.id = 'payBtnStyle';
    st.textContent = '.order-send.order-pay{background:#ffcc00;color:#1a1300;margin-bottom:10px}.order-send.order-pay:disabled{opacity:.5;cursor:not-allowed}.order-send.order-send-wa{background:transparent;border:1px solid #25d366;color:#25d366}';
    document.head.appendChild(st);
  }
  function refreshPayBtn() {
    const off = !count() || hasUnpriced();
    payBtn.disabled = off;
    payBtn.title = hasUnpriced() ? t('Some items need a price confirmation: order on WhatsApp.', 'Certains articles n’ont pas de prix : commandez sur WhatsApp.') : '';
  }
  payBtn.addEventListener('click', async () => {
    const name = panel.querySelector('#orderName').value.trim();
    const phone = panel.querySelector('#orderPhone').value.trim();
    const say = (msg, ok) => { feedback.textContent = msg; feedback.style.color = ok ? '#2ee68b' : '#ffaa66'; };
    if (!count()) return say(t('Add at least one item first.', "Ajoutez d'abord au moins un article."));
    if (hasUnpriced()) return say(t('Some items have no price yet: please order on WhatsApp.', 'Certains articles n’ont pas encore de prix : commandez sur WhatsApp.'));
    const digits = phone.replace(/\D/g, '').replace(/^(00)?237(?=6\d{8}$)/, '');
    if (!name || !/^6\d{8}$/.test(digits)) return say(t('✏️ Add your name and a valid Cameroon number (e.g. 6XX XXX XXX).', '✏️ Indiquez votre nom et un numéro camerounais valide (ex. 6XX XXX XXX).'));
    payBtn.disabled = true;
    say(t('⏳ Preparing your secure payment…', '⏳ Préparation du paiement sécurisé…'), true);
    if (typeof gtag === 'function') gtag('event', 'begin_checkout', { currency: 'XAF', value: total(), items: Object.keys(cart).map(id => ({ item_id: id, quantity: cart[id] })) });
    try {
      const r = await fetch('/api/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: cart, name, phone: digits, lang: FR ? 'fr' : 'en',
          town: panel.querySelector('#orderTown').value.trim(),
          note: panel.querySelector('#orderNote').value.trim(),
          delivery: (panel.querySelector('input[name="orderDelivery"]:checked') || {}).value || 'Delivery',
        }),
      });
      const data = await r.json().catch(() => ({}));
      if (data.ok && data.link) { window.location.href = data.link; return; }
      const why = data.error === 'too_many' ? t('Too many attempts. Please wait a little or order on WhatsApp.', 'Trop de tentatives. Patientez un peu ou commandez sur WhatsApp.')
        : t('Online payment is not available right now. Please order on WhatsApp.', 'Le paiement en ligne est indisponible pour le moment. Commandez sur WhatsApp.');
      say(why);
    } catch (err) {
      say(t('Connection problem. Check your internet and try again, or order on WhatsApp.', 'Problème de connexion. Vérifiez internet et réessayez, ou commandez sur WhatsApp.'));
    }
    payBtn.disabled = false;
  });

  // "Order for a whole class or school" link can preselect a subject tab.
  document.querySelectorAll('[data-shop-subject]').forEach(a => a.addEventListener('click', () => {
    const btn = filterEl && filterEl.querySelector(`[data-subject="${a.dataset.shopSubject}"]`);
    if (btn) btn.click();
  }));

  renderGrid();
  refresh();
})();


/* ---------- Back from Fapshi: show the payment result ----------
   Fapshi sends the student back to /academy?order=<id>. We ask our own
   /api/pay (which checks with Fapshi) and never trust the address bar. */
(function () {
  const params = new URLSearchParams(location.search);
  const orderId = params.get('order');
  if (!orderId || !/^[A-Z0-9]{6,40}$/.test(orderId)) return;
  const FR = document.documentElement.lang === 'fr';
  const t = (en, fr) => (FR ? fr : en);
  const PHONE = typeof ACADEMY_WHATSAPP !== 'undefined' ? ACADEMY_WHATSAPP : '237682402876';
  const money = (n) => Number(n).toLocaleString('en-US').replace(/,/g, ' ') + ' FCFA';
  const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const box = document.createElement('div');
  box.className = 'pay-result';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.style.cssText = 'position:fixed;inset:0;z-index:2000;display:grid;place-items:center;padding:16px;background:rgba(3,6,18,.82)';
  box.innerHTML = `<div style="max-width:440px;width:100%;background:#0d1326;border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:24px;color:#e8ecf5;line-height:1.6">
    <div class="pay-body">⏳ ${t('Checking your payment…', 'Vérification de votre paiement…')}</div>
    <button type="button" class="pay-close" style="margin-top:16px;width:100%;padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:transparent;color:#fff;cursor:pointer">${t('Close', 'Fermer')}</button>
  </div>`;
  document.body.appendChild(box);
  const body = box.querySelector('.pay-body');
  const close = () => {
    box.remove();
    history.replaceState(null, '', location.pathname + location.hash);
  };
  box.querySelector('.pay-close').addEventListener('click', close);

  let tries = 0;
  async function check() {
    tries++;
    let data = {};
    try { data = await fetch('/api/pay?order=' + encodeURIComponent(orderId), { cache: 'no-store' }).then(r => r.json()); } catch (e) {}
    const o = data.order;
    if (!o) {
      body.innerHTML = `❓ ${t('We could not find this order. If you paid, send us your payment SMS on WhatsApp.', 'Commande introuvable. Si vous avez payé, envoyez-nous le SMS de paiement sur WhatsApp.')}`;
      return;
    }
    if (o.status === 'pending' && tries < 8) {
      body.innerHTML = `⏳ ${t('Waiting for the payment confirmation… (approve it on your phone if asked)', 'En attente de la confirmation… (validez sur votre téléphone si demandé)')}`;
      setTimeout(check, 4000);
      return;
    }
    const list = o.items.map(i => `• ${i.qty} × ${i.subject} — ${i.title}`).join('\n');
    if (o.status === 'paid') {
      try { localStorage.removeItem(FR ? 'asghin-cart-fr' : 'asghin-cart'); } catch (e) {}
      if (typeof gtag === 'function') gtag('event', 'purchase', { transaction_id: o.id, currency: 'XAF', value: o.total });
      const msg = t(`Hello AsghinLabs Academy 👋, I have paid online.\n\nOrder: ${o.id}\nAmount: ${money(o.total)}\n${list}\n\nName: ${o.name}\nReceive by: ${o.delivery}${o.town ? '\nTown/School: ' + o.town : ''}`,
        `Bonjour AsghinLabs Academy 👋, j'ai payé en ligne.\n\nCommande : ${o.id}\nMontant : ${money(o.total)}\n${list}\n\nNom : ${o.name}\nRéception : ${o.delivery === 'Pickup' ? 'Retrait' : 'Livraison'}${o.town ? '\nVille/Établissement : ' + o.town : ''}`);
      body.innerHTML = `<h3 style="margin:0 0 8px">✅ ${t('Payment received!', 'Paiement reçu !')}</h3>
        <p style="margin:0 0 8px">${t('Order', 'Commande')} <strong>${esc(o.id)}</strong> · ${esc(money(o.total))}</p>
        <p style="white-space:pre-line;color:#aab3c8;margin:0 0 14px">${esc(list)}</p>
        <p style="margin:0 0 14px">${t('Last step: send this confirmation on WhatsApp so we deliver or send your notes right away.', 'Dernière étape : envoyez cette confirmation sur WhatsApp pour recevoir vos notes ou votre livraison rapidement.')}</p>
        <a href="https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}" target="_blank" rel="noopener" style="display:block;text-align:center;padding:13px;border-radius:12px;background:#25d366;color:#04140a;font-weight:700;text-decoration:none">💬 ${t('Send confirmation on WhatsApp', 'Envoyer la confirmation sur WhatsApp')}</a>`;
    } else if (o.status === 'failed') {
      body.innerHTML = `<h3 style="margin:0 0 8px">❌ ${t('Payment not completed', 'Paiement non effectué')}</h3>
        <p style="margin:0">${t('No money was taken. Your basket is still saved: you can try again or order on WhatsApp.', 'Aucun montant prélevé. Votre panier est conservé : réessayez ou commandez sur WhatsApp.')}</p>`;
    } else {
      body.innerHTML = `<h3 style="margin:0 0 8px">⏳ ${t('Payment still pending', 'Paiement en attente')}</h3>
        <p style="margin:0">${t('If you approved the payment, it may take a minute. Reload this page later, or send us your order number', 'Si vous avez validé, cela peut prendre une minute. Rechargez la page plus tard ou envoyez-nous le numéro')} <strong>${esc(o.id)}</strong> ${t('on WhatsApp.', 'sur WhatsApp.')}</p>`;
    }
  }
  check();
})();
