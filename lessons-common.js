/* =====================================================================
   Helpers shared by the interactive lessons (lesson-*.html).
   ===================================================================== */

// Random integer between a and b (both included)
function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }

// Random integer between a and b that is never 0
function rnz(a, b) { let n = 0; while (n === 0) n = rint(a, b); return n; }

function pick(list) { return list[Math.floor(Math.random() * list.length)]; }

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

// Number as text, rounded to 2 decimals, with a proper minus sign (−)
function num(n) { return String(+n.toFixed(2)).replace('-', '\u2212'); }

// [[coef, 'x²'], [coef, 'x'], [coef, '']] → "6x² + 8x − 3x − 12"
function joinTerms(terms) {
  return terms.map(([k, sym], i) => {
    const abs = Math.abs(k);
    const body = (abs === 1 && sym) ? sym : num(abs) + sym;
    if (i === 0) return (k < 0 ? '\u2212' : '') + body;
    return (k < 0 ? '\u2212 ' : '+ ') + body;
  }).join(' ');
}

// Coefficients of [x², x, number] → "x² − 5x + 6". Zero terms are left out.
function polyStr(coefs) {
  const syms = ['x\u00B2', 'x', ''];
  const terms = coefs.map((k, i) => [k, syms[i]]).filter(t => t[0] !== 0);
  return terms.length ? joinTerms(terms) : '0';
}

// Same event name as the sorting lesson, so Analytics groups them together
function viewLesson(slug) {
  if (typeof gtag === 'function') gtag('event', 'view_interactive_lesson', { lesson: slug });
}

// Tracks the main interactions: 'check_correct', 'check_wrong', 'new_question' ...
function trackLesson(slug, action) {
  if (typeof gtag === 'function') gtag('event', 'lesson_' + action, { lesson: slug });
}
