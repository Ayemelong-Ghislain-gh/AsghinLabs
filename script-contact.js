(function () {
  // ===================================================================
  // This form submits to Formspree, which forwards submissions straight
  // to asghinlabs@gmail.com. Formspree is a free service made for exactly
  // this: sending static-site form submissions to a real inbox with no
  // backend server required.
  //
  // ONE-TIME SETUP (takes ~2 minutes):
  // 1. Go to https://formspree.io and sign up using asghinlabs@gmail.com
  // 2. Create a new form -> it gives you an endpoint like:
  //    https://formspree.io/f/abcdwxyz
  // 3. Replace YOUR_FORM_ID below with that ID (the part after /f/)
  // Until you do this, the form will show a friendly error instead of
  // silently pretending to send.
  // ===================================================================
  const FORMSPREE_ID = "xeebpyka";

  const form = document.getElementById('contactForm');
  const sendBtn = document.getElementById('sendContactBtn');
  const feedback = document.getElementById('formFeedback');
  if (!form || !sendBtn) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('contactName')?.value.trim();
    const email = document.getElementById('contactEmail')?.value.trim();
    const service = document.getElementById('serviceSelect')?.value;
    const msg = document.getElementById('contactMsg')?.value.trim();

    if (!name || !email || !msg) {
      feedback.textContent = "✏️ Please fill all fields before sending.";
      feedback.style.color = "#ffaa66";
      return;
    }

    if (FORMSPREE_ID === "YOUR_FORM_ID") {
      feedback.innerHTML = '⚠️ Form isn\'t connected yet — set FORMSPREE_ID in script-contact.js (see comment at the top of the file). Meanwhile, reach us on WhatsApp below.';
      feedback.style.color = "#ffaa66";
      return;
    }

    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";
    feedback.textContent = "";

    try {
      const response = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: new FormData(form)
      });

      if (response.ok) {
        feedback.textContent = `✨ Thanks ${name}! We'll respond within 24h.`;
        feedback.style.color = "#2ee68b";
        form.reset();
      } else {
        feedback.textContent = "⚠️ Something went wrong sending your message. Please try WhatsApp instead.";
        feedback.style.color = "#ff6b6b";
      }
    } catch (err) {
      feedback.textContent = "⚠️ Network error — please try WhatsApp instead.";
      feedback.style.color = "#ff6b6b";
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = "Send message →";
      setTimeout(() => { feedback.textContent = ""; }, 6000);
    }
  });
})();
