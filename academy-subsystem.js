/* =====================================================================
   SUBSYSTEM CHOOSER — English subsystem (GCE) / Sous-système francophone
   ---------------------------------------------------------------------
   Used on academy.html (English subsystem), academie.html (francophone),
   lessons.html and lecons.html.

   Each page says which subsystem it belongs to on its <body>:
     data-subsystem="en" | "fr"
     data-subsystem-other="/academie"      (the same page in the other subsystem)
     data-subsystem-ask                     (optional: show the chooser on the first visit)

   The visitor's choice is remembered in this browser, so the chooser only
   appears once. They can switch at any time with the switch in the menu.
   ===================================================================== */
(function () {
  const body = document.body;
  const here = body.dataset.subsystem;
  if (here !== 'en' && here !== 'fr') return;

  const KEY = 'asghin-subsystem';
  const other = here === 'en' ? 'fr' : 'en';
  const otherUrl = body.dataset.subsystemOther || (here === 'en' ? '/academie' : '/academy');
  const pageFor = { [here]: location.pathname + location.search, [other]: otherUrl };

  const read = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const save = (v) => { try { localStorage.setItem(KEY, v); } catch (e) {} };
  const track = (name, v) => { if (typeof gtag === 'function') gtag('event', name, { subsystem: v }); };

  const LABEL = {
    en: { short: 'Anglophone', long: 'English Subsystem' },
    fr: { short: 'Francophone', long: 'Sous-système francophone' },
  };

  /* ---------- 1. Switch in the menu ---------- */
  const links = document.getElementById('navLinks');
  if (links) {
    const li = document.createElement('li');
    li.className = 'subsystem-switch-item';
    li.innerHTML =
      `<div class="subsystem-switch" role="group" aria-label="${here === 'fr' ? 'Sous-système' : 'Subsystem'}">` +
      ['en', 'fr'].map(s => s === here
        ? `<span class="ss-opt on" aria-current="page">${LABEL[s].short}</span>`
        : `<a class="ss-opt" href="${pageFor[s]}" data-choose="${s}" hreflang="${s}" lang="${s}">${LABEL[s].short}</a>`).join('') +
      '</div>';
    const back = links.querySelector('.nav-back');
    links.insertBefore(li, back ? back.closest('li') : null);
  }

  // Any link marked data-choose="en|fr" remembers the choice before leaving.
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-choose]');
    if (!a) return;
    save(a.dataset.choose);
    track('choose_subsystem', a.dataset.choose);
  });

  /* ---------- 2. Gentle reminder when the visitor chose the other subsystem ---------- */
  const stored = read();
  if (stored === other) {
    const bar = document.createElement('div');
    bar.className = 'subsystem-bar';
    bar.setAttribute('role', 'note');
    bar.innerHTML = other === 'fr'
      ? `<span lang="fr">Vous suivez le sous-système francophone ?</span>
         <a href="${otherUrl}" data-choose="fr" lang="fr">Aller à l'Académie francophone →</a>
         <button type="button" class="subsystem-bar-close" aria-label="Stay on the English subsystem">✕</button>`
      : `<span lang="en">Are you in the English subsystem?</span>
         <a href="${otherUrl}" data-choose="en" lang="en">Go to the English-subsystem Academy →</a>
         <button type="button" class="subsystem-bar-close" aria-label="Rester sur le sous-système francophone">✕</button>`;
    bar.querySelector('.subsystem-bar-close').addEventListener('click', () => { save(here); bar.remove(); });
    const nav = document.querySelector('nav');
    (nav && nav.nextSibling ? nav.parentNode.insertBefore(bar, nav.nextSibling) : body.prepend(bar));
  }

  /* ---------- 3. The chooser (first visit only) ---------- */
  if (!('subsystemAsk' in body.dataset) || stored) return;

  const dlg = document.createElement('div');
  dlg.className = 'subsystem-chooser';
  dlg.setAttribute('role', 'dialog');
  dlg.setAttribute('aria-modal', 'true');
  dlg.setAttribute('aria-labelledby', 'ssTitle');
  dlg.innerHTML = `
    <div class="ss-sheet">
      <img src="/images/logo-blue.jpeg" alt="" class="ss-logo" width="56" height="56">
      <p class="ss-kicker">AsghinLabs Academy</p>
      <h2 id="ssTitle"><span lang="en">Which subsystem are you in?</span><span class="ss-sep" aria-hidden="true"></span><span lang="fr">Quel est votre sous-système&nbsp;?</span></h2>
      <p class="ss-sub"><span lang="en">Lessons, workbooks and past papers follow your own school programme.</span>
        <span lang="fr">Leçons, cahiers et sujets suivent votre propre programme.</span></p>

      <div class="ss-cards">
        <a class="ss-card" href="${pageFor.en}" data-pick="en" lang="en">
          <span class="ss-badge">GCE</span>
          <strong>English Subsystem</strong>
          <em>Sous-système anglophone</em>
          <span class="ss-levels">Form 1 → Upper Sixth</span>
          <span class="ss-exams">GCE O Level · A Level · TVEE</span>
          <span class="ss-go">Continue in English →</span>
        </a>
        <a class="ss-card fr" href="${pageFor.fr}" data-pick="fr" lang="fr">
          <span class="ss-badge">BEPC · BAC</span>
          <strong>Sous-système francophone</strong>
          <em>French Subsystem</em>
          <span class="ss-levels">6<sup>e</sup> → Terminale</span>
          <span class="ss-exams">BEPC · Probatoire · Baccalauréat · CAP</span>
          <span class="ss-go">Continuer en français →</span>
        </a>
      </div>

      <p class="ss-note"><span lang="en">You can switch at any time from the menu.</span> ·
        <span lang="fr">Vous pouvez changer à tout moment depuis le menu.</span></p>
    </div>`;
  body.appendChild(dlg);
  body.classList.add('ss-open');

  const cards = [...dlg.querySelectorAll('.ss-card')];
  const lastFocus = document.activeElement;
  // The card for the page the visitor opened gets the focus, so Enter keeps them here.
  (dlg.querySelector(`[data-pick="${here}"]`) || cards[0]).focus();

  function close() {
    dlg.remove();
    body.classList.remove('ss-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  cards.forEach(card => card.addEventListener('click', e => {
    const pick = card.dataset.pick;
    save(pick);
    track('choose_subsystem', pick);
    if (pick === here) { e.preventDefault(); close(); }
  }));

  // Esc keeps the visitor on this page (and remembers it).
  dlg.addEventListener('keydown', e => {
    if (e.key === 'Escape') { save(here); close(); }
    if (e.key === 'Tab') {               // keep the keyboard inside the chooser
      const i = cards.indexOf(document.activeElement);
      e.preventDefault();
      cards[(i + (e.shiftKey ? cards.length - 1 : 1)) % cards.length].focus();
    }
  });
})();
