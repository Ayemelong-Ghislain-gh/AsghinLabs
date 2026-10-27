/* =====================================================================
   ACADEMY — search + "request notes"
   Shared by the shop (academy-shop.js) and the free-sample gallery
   (academy.js). Load it after academy-data.js and before those two files.
   - AcademySearch.match(item, query): true if every word of the query is
     found in the item (subject, title, level, stage). Understands short
     forms: CSC, CS, L6, U6, F1, A Level, maths, bio, chem, phy …
   - AcademySearch.openRequest(text): opens the "Request notes" form, which
     sends the request to us on WhatsApp.
   - A search box is added to the top of the page (hero); it fills the shop
     search and jumps to the results. ?q=… in the URL does the same.
   ===================================================================== */
(function () {
  const FR = document.documentElement.lang === 'fr';
  const t = (en, fr) => (FR ? fr : en);
  const PHONE = typeof ACADEMY_WHATSAPP !== 'undefined' ? ACADEMY_WHATSAPP : '237682402876';
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  // Phrases and short forms → one canonical word.
  const RULES = [
    [/information and communication technolog(y|ies)|\btic\b/g, ' ict '],
    [/computer science|computer sci\b|computing|informatique|\bcsc\b|\bcomp\b|\bcomputer\b/g, ' cs '],
    [/pure maths? with mechanics|pure mathematics|further maths?|mathematiques|mathematics|\bmaths?\b|\bpmm\b|\bmath\b/g, ' maths '],
    [/biology|biologie|\bbio\b|\bsvt\b/g, ' bio '],
    [/chemistry|chimie|\bchem\b/g, ' chem '],
    [/physics|physique|\bphys?\b|\bpct\b/g, ' phy '],
    [/lower\s*(sixth|6th|six)|lowersixth|\blower\b|\bl6\b|\bls\b|\blsx\b/g, ' l6 '],
    [/upper\s*(sixth|6th|six)|uppersixth|\bupper\b|\bu6\b|\bus\b|\busx\b/g, ' u6 '],
    [/\bform\s*([1-5])\b|\bf\s?([1-5])\b/g, (m, a, b) => ` f${a || b} `],
    [/\bo[\s-]?levels?\b|ordinary level|\bol\b/g, ' olevel '],
    [/\ba[\s-]?levels?\b|advanced level|\bal\b/g, ' alevel '],
    [/\blesson notes?\b|\bnotes?\b|\bfiches?\b|\bcours\b|\bpdf\b/g, ' notes '],
    [/\bworkbooks?\b|\bcahiers?\b|\bpamphlets?\b/g, ' workbook '],
  ];
  const STOP = new Set(['the', 'for', 'and', 'of', 'in', 'a', 'an', 'to', 'de', 'la', 'le', 'les', 'des', 'du', 'et', 'en', 'pour', 'sixth', 'six', 'level', 'full', 'complete', 'i', 'need', 'want', 'please']);

  function plain(s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[—–·|()+&,.:;/\\'"!?]/g, ' ');
  }
  function canon(s) {
    let x = ' ' + plain(s) + ' ';
    RULES.forEach(([re, rep]) => { x = x.replace(re, rep); });
    return x;
  }
  const words = (s) => s.split(/\s+/).filter(Boolean);

  function haystack(item) {
    const text = [item.subject, item.title, item.level, item.stage, item.keywords].filter(Boolean).join(' ');
    let extra = '';
    if (/sixth|a level/i.test(text)) extra += ' alevel';
    if (/form [45]|o level/i.test(text)) extra += ' olevel';
    if (/notes/i.test(text) || (item.id || '').startsWith('notes-') || item.sample) extra += ' notes';
    if (/workbook/i.test(text)) extra += ' workbook';
    // A both-years or all-subjects pack also answers "Lower Sixth" and "Upper Sixth" searches.
    if (/lower \+ upper|lower & upper/i.test(text)) extra += ' l6 u6';
    if (item.id === 'notes-all') extra += ' cs maths bio chem phy l6 u6';
    return new Set(words(canon(text) + ' ' + plain(text) + extra));
  }

  function queryWords(q) {
    return words(canon(q)).filter(w => !STOP.has(w));
  }

  // Every query word must start some word of the item ("chem" finds "chemistry").
  function match(item, q) {
    const qs = queryWords(q);
    if (!qs.length) return true;
    const hay = [...haystack(item)];
    return qs.every(w => hay.some(h => h === w || (w.length >= 2 && h.startsWith(w))));
  }

  /* ---------------- Request notes (→ WhatsApp) ---------------- */
  let modal = null;
  function buildModal() {
    modal = document.createElement('div');
    modal.className = 'order-panel req-panel';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', t('Request notes', 'Demander des notes'));
    modal.innerHTML = `
      <div class="order-sheet">
        <div class="order-head">
          <h3>📩 ${t('Request notes', 'Demander des notes')}</h3>
          <button type="button" class="order-close" aria-label="${t('Close', 'Fermer')}">✕</button>
        </div>
        <p class="req-intro">${t("Tell us what you need. We'll reply on WhatsApp and tell you when it's ready, and the price.",
          'Dites-nous ce qu’il vous faut. Nous répondons sur WhatsApp avec le délai et le prix.')}</p>
        <form class="order-form" id="reqForm" novalidate>
          <label for="reqWhat">${t('Which notes or workbook?', 'Quelles notes ou quel cahier ?')}</label>
          <input id="reqWhat" type="text" required placeholder="${t('e.g. Economics Upper Sixth notes', 'ex. Notes de SVT Terminale D')}">
          <label for="reqClass">${t('Class / level', 'Classe / niveau')}</label>
          <select id="reqClass">
            ${(FR
              ? ['', '6e', '5e', '4e', '3e', 'Seconde', 'Première', 'Terminale', 'Autre']
              : ['', 'Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', 'Lower Sixth', 'Upper Sixth', 'Other'])
              .map(c => `<option value="${c}">${c || t('Choose…', 'Choisir…')}</option>`).join('')}
          </select>
          <label for="reqName">${t('Your name', 'Votre nom')}</label>
          <input id="reqName" type="text" autocomplete="name" required placeholder="${t('e.g. Ngwa Brenda', 'ex. Ngo Bassa Carine')}">
          <label for="reqRole">${t('You are…', 'Vous êtes…')}</label>
          <select id="reqRole">
            <option>${t('A student', 'Élève')}</option>
            <option>${t('A parent', 'Parent')}</option>
            <option>${t('A teacher', 'Enseignant')}</option>
          </select>
          <label for="reqNote">${t('Anything else (optional)', 'Autre précision (facultatif)')}</label>
          <textarea id="reqNote" rows="2" placeholder="${t('e.g. I need it before the mock exam', 'ex. J’en ai besoin avant le bac blanc')}"></textarea>
          <button type="submit" class="order-send">💬 ${t('Send request on WhatsApp', 'Envoyer la demande sur WhatsApp')}</button>
          <p class="order-feedback" aria-live="polite"></p>
        </form>
      </div>`;
    document.body.appendChild(modal);
    const close = () => { modal.classList.remove('open'); document.body.style.overflow = ''; };
    modal.querySelector('.order-close').addEventListener('click', close);
    modal.addEventListener('click', e => { if (e.target === modal) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
    modal.querySelector('#reqForm').addEventListener('submit', e => {
      e.preventDefault();
      const v = id => modal.querySelector(id).value.trim();
      const fb = modal.querySelector('.order-feedback');
      if (!v('#reqWhat') || !v('#reqName')) {
        fb.textContent = t('✏️ Please say which notes you need and your name.', '✏️ Indiquez les notes recherchées et votre nom.');
        fb.style.color = '#ffaa66';
        return;
      }
      let msg = t("Hello AsghinLabs Academy 👋, I couldn't find these notes on your website:\n\n",
        'Bonjour AsghinLabs Academy 👋, je n’ai pas trouvé ces notes sur votre site :\n\n');
      msg += `• ${v('#reqWhat')}\n`;
      if (v('#reqClass')) msg += t(`Class: ${v('#reqClass')}\n`, `Classe : ${v('#reqClass')}\n`);
      msg += t(`\nName: ${v('#reqName')} (${v('#reqRole')})\n`, `\nNom : ${v('#reqName')} (${v('#reqRole')})\n`);
      if (v('#reqNote')) msg += t(`Note: ${v('#reqNote')}\n`, `Remarque : ${v('#reqNote')}\n`);
      if (typeof gtag === 'function') gtag('event', 'request_notes', { item: v('#reqWhat') });
      window.open(`https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
      fb.textContent = t('✨ Opening WhatsApp — just press send.', '✨ WhatsApp s’ouvre : appuyez sur Envoyer.');
      fb.style.color = '#2ee68b';
    });
  }
  function openRequest(text) {
    if (!modal) buildModal();
    modal.querySelector('#reqWhat').value = text || '';
    modal.querySelector('.order-feedback').textContent = '';
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => modal.querySelector(text ? '#reqName' : '#reqWhat').focus(), 50);
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-request-notes]');
    if (b) { e.preventDefault(); openRequest(b.dataset.requestNotes || ''); }
  });

  // A "nothing found" block with the request button, for both searches.
  function noResults(q, what) {
    return `
      <div class="search-empty">
        <div class="search-empty-icon">🔎</div>
        <p><strong>${t(`No ${what} found for “${esc(q)}” yet.`, `Aucun résultat pour « ${esc(q)} » pour l’instant.`)}</strong></p>
        <p>${t('We are adding new notes every week. Tell us what you need and we will prepare it for you.',
          'Nous ajoutons de nouvelles notes chaque semaine. Dites-nous ce qu’il vous faut.')}</p>
        <button type="button" class="apply-btn" data-request-notes="${esc(q)}">📩 ${t('Request these notes', 'Demander ces notes')}</button>
      </div>`;
  }

  window.AcademySearch = { match, openRequest, noResults, t };

  /* ---------------- Hero search box ---------------- */
  // Fills the shop search (#wbSearch, created by academy-shop.js) and jumps to it.
  function goSearch(q) {
    const input = document.getElementById('wbSearch');
    const shop = document.getElementById('workbooks');
    if (!input || !shop) return;
    input.value = q;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    shop.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.academy-hero-text') || document.querySelector('.academy-hero');
    const hasShop = typeof ACADEMY_WORKBOOKS !== 'undefined' && ACADEMY_WORKBOOKS.length;
    if (hero && hasShop && document.getElementById('workbookGrid')) {
      const f = document.createElement('form');
      f.className = 'hero-search';
      f.setAttribute('role', 'search');
      f.innerHTML = `
        <label for="heroSearch" class="visually-hidden">${t('Search notes and workbooks', 'Rechercher des notes et cahiers')}</label>
        <input id="heroSearch" type="search" autocomplete="off" placeholder="${t('🔎 Search notes: e.g. CSC Upper Sixth', '🔎 Rechercher : ex. Maths Terminale')}">
        <button type="submit">${t('Search', 'Rechercher')}</button>`;
      const cta = hero.querySelector('.academy-cta');
      if (cta) cta.insertAdjacentElement('afterend', f); else hero.appendChild(f);
      f.addEventListener('submit', e => { e.preventDefault(); goSearch(f.querySelector('input').value.trim()); });
    }
    const q = new URLSearchParams(location.search).get('q');
    if (q) setTimeout(() => goSearch(q), 300);
  });
})();
