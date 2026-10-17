(function () {
  const form = document.getElementById('applyForm');
  const feedback = document.getElementById('applyFeedback');
  const programSelect = document.getElementById('applyProgram');
  const WHATSAPP_NUMBER = '237682402876';
  const FR = document.documentElement.lang === 'fr';   // academie.html
  const t = (en, fr) => (FR ? fr : en);

  if (!form) return;

  // Clicking "Apply Now →" on a program card pre-selects that program
  // in the form below, so the visitor doesn't have to pick it again.
  document.querySelectorAll('.apply-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const program = btn.getAttribute('data-program');
      if (program && programSelect) programSelect.value = program;
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('applyName').value.trim();
    const program = programSelect.value;
    const school = document.getElementById('applySchool').value.trim();
    const phone = document.getElementById('applyPhone').value.trim();
    const detailsEl = document.getElementById('applyDetails');
    const details = detailsEl ? detailsEl.value.trim() : '';

    if (!name || !program || !phone) {
      feedback.textContent = t('✏️ Please fill in your name, program, and phone number.', '✏️ Indiquez votre nom, le cours choisi et votre numéro de téléphone.');
      feedback.style.color = '#ffaa66';
      return;
    }

    let message;
    if (FR) {
      message = program === 'Pas encore sûr'
        ? `Bonjour AsghinLabs Academy, je souhaite suivre un cours (sous-système francophone) mais je ne sais pas encore lequel.\n\n`
        : `Bonjour AsghinLabs Academy, je souhaite m'inscrire à : ${program} (sous-système francophone)\n\n`;
      message += `Nom : ${name}\n`;
      if (details) message += `Matière/classe : ${details}\n`;
      if (school) message += `Établissement : ${school}\n`;
      message += `Téléphone : ${phone}`;
    } else {
      message = program === 'Not sure yet'
        ? `Hi AsghinLabs Academy, I'd like to join a class but I'm not sure which one yet.\n\n`
        : `Hi AsghinLabs Academy, I'd like to apply for: ${program}\n\n`;
      message += `Name: ${name}\n`;
      if (details) message += `Subject/level: ${details}\n`;
      if (school) message += `School: ${school}\n`;
      message += `Phone: ${phone}`;
    }

    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank', 'noopener');

    feedback.textContent = t('✨ Opening WhatsApp with your application...', '✨ WhatsApp s’ouvre avec votre demande…');
    feedback.style.color = '#2ee68b';
  });
})();
