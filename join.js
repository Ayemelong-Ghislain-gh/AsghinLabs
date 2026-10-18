// Join-the-team form: builds a WhatsApp message to the AsghinLabs business
// number (same approach as the Academy apply form), so applications land
// in one inbox without needing a backend.
(function () {
  const form = document.getElementById('joinForm');
  const feedback = document.getElementById('joinFeedback');
  const seatSelect = document.getElementById('joinSeat');
  const WHATSAPP_NUMBER = '237682402876';
  if (!form) return;

  // "Apply for this" on a role card pre-selects it and jumps to the form.
  document.querySelectorAll('.seat-pick').forEach(btn => {
    btn.addEventListener('click', () => {
      seatSelect.value = btn.getAttribute('data-seat');
      document.getElementById('apply').scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => document.getElementById('joinName').focus({ preventScroll: true }), 500);
    });
  });

  const val = id => document.getElementById(id).value.trim();

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = val('joinName'), city = val('joinCity'), phone = val('joinPhone');
    const seat = seatSelect.value, work = val('joinWork'), pitch = val('joinPitch');
    const hours = val('joinHours'), why = val('joinWhy');

    if (!name || !city || !phone || !seat || !pitch || !hours) {
      feedback.textContent = '✏️ Please fill in all fields marked * / Remplissez les champs marqués *';
      feedback.style.color = '#ffaa66';
      return;
    }

    let msg = `Hi AsghinLabs, I'd like to join the team.\n\n`;
    msg += `Role: ${seat}\nName: ${name}\nCity: ${city}\nWhatsApp: ${phone}\n`;
    if (work) msg += `My work: ${work}\n`;
    msg += `Hours/week: ${hours}\n\nMy pitch to a shop owner:\n${pitch}\n`;
    if (why) msg += `\nWhy AsghinLabs:\n${why}`;

    if (typeof gtag === 'function') gtag('event', 'join_application', { role: seat });
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    feedback.textContent = '✨ Opening WhatsApp with your application… just press send.';
    feedback.style.color = '#2ee68b';
  });
})();
