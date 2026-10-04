/* =====================================================================
   ACADEMY CONTENT — EDIT THIS FILE TO ADD NOTES, PAST QUESTIONS AND
   WORKBOOKS. The Academy page rebuilds itself from these lists; no other
   code needs to change.
   ===================================================================== */

// WhatsApp number that receives workbook orders and applications
// (country code + number, no "+" or spaces).
const ACADEMY_WHATSAPP = "237682402876";

/* ---------------------------------------------------------------------
   NOTES & PAST QUESTIONS
   1. Put the PDF in files/academy/notes/ (or files/academy/past-questions/)
   2. Add one line below. "cover" is optional: a picture of page 1 makes
      the card look much better (images/academy/notes/…).
   Visitors can read every PDF right on the site, or download it.
   --------------------------------------------------------------------- */
const ACADEMY_NOTES = [
  {
    file: "files/academy/notes/computer-science-lower-sixth-complete-notes.pdf",
    cover: "images/academy/notes/cs-lower-sixth-notes.jpg",
    title: "Computer Science — Complete Lesson Notes",
    subject: "Computer Science",
    level: "Lower Sixth",
    pages: 380,
    size: "2.6 MB",
  },
];

const ACADEMY_PAST_QUESTIONS = [
  // { file: "files/academy/past-questions/example.pdf", title: "2025 Mock Exam", subject: "Computer Science", level: "O Level", pages: 12, size: "1 MB" },
];

/* ---------------------------------------------------------------------
   WORKBOOKS (shop)
   - price: in FCFA. Set it to 0 to show "Ask for price" instead.
   - status: "available" or "preorder" (shows a "Pre-order" badge).
   - To add or remove a workbook, add or delete its line.
   Covers live in images/academy/workbooks/.
   --------------------------------------------------------------------- */
const WORKBOOK_LEVELS = {
  "form-1": { level: "Form 1", title: "Form 1 Workbook", stage: "Lower Secondary", price: 2000 },
  "form-2": { level: "Form 2", title: "Form 2 Workbook", stage: "Lower Secondary", price: 2000 },
  "form-3": { level: "Form 3", title: "Form 3 Workbook", stage: "Lower Secondary", price: 2500 },
  "o-level-complete": {
    level: "O Level", title: "Complete O Level Workbook", stage: "Form 4 & Form 5 · GCE exam preparation",
    price: 5000, pack: true,
  },
  "a-level-complete": {
    level: "A Level", title: "Complete A Level Workbook", stage: "Lower & Upper Sixth · GCE exam preparation",
    price: 7000, pack: true,
  },
};

// prices (optional): override the default price for this subject,
// e.g. { "form-1": 2500 }.
function buildWorkbooks(subject, code, slugs, prices = {}) {
  return slugs.map(slug => ({
    id: `${code}-${slug}`,
    subject,
    ...WORKBOOK_LEVELS[slug],
    ...(prices[slug] ? { price: prices[slug] } : {}),
    cover: `images/academy/workbooks/${code}-${slug}.jpg`,
    status: "available",
  }));
}

// Computer Science runs Form 1 → A Level. At A Level it splits into
// Computer Science and ICT, so ICT only has an A Level workbook.
const ACADEMY_WORKBOOKS = [
  ...buildWorkbooks("Computer Science", "cs", ["form-1", "form-2", "form-3", "o-level-complete", "a-level-complete"]),
  ...buildWorkbooks("ICT", "ict", ["a-level-complete"]),
  // Mathematics has its own prices.
  ...buildWorkbooks("Mathematics", "maths", ["form-1", "form-2", "form-3", "o-level-complete", "a-level-complete"], {
    "form-1": 2500, "form-2": 2500, "form-3": 3000, "o-level-complete": 5000, "a-level-complete": 8000,
  }),
];
