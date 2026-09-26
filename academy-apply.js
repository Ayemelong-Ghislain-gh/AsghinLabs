(function () {
  const form = document.getElementById('applyForm');
  const feedback = document.getElementById('applyFeedback');
  const programSelect = document.getElementById('applyProgram');
  const WHATSAPP_NUMBER = '237682402876';

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

    if (!name || !program || !phone) {
      feedback.textContent = '✏️ Please fill in your name, program, and phone number.';
      feedback.style.color = '#ffaa66';
      return;
    }

    let message = `Hi AsghinLabs Academy, I'd like to apply for: ${program}\n\n`;
    message += `Name: ${name}\n`;
    if (school) message += `School: ${school}\n`;
    message += `Phone: ${phone}`;

    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank', 'noopener');

    feedback.textContent = '✨ Opening WhatsApp with your application...';
    feedback.style.color = '#2ee68b';
  });
})();
