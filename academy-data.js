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
const WORKBOOK_PRICES = {
  // ⚠️ Placeholder prices — change these to your real prices.
  "Form 1": 2500, "Form 2": 2500, "Form 3": 2500,
  "Form 4": 3000, "Form 5": 3000,
  "Lower Sixth": 3500, "Upper Sixth": 3500,
};

const WORKBOOK_LEVELS = [
  { level: "Form 1", slug: "form-1", stage: "Lower Secondary" },
  { level: "Form 2", slug: "form-2", stage: "Lower Secondary" },
  { level: "Form 3", slug: "form-3", stage: "Lower Secondary" },
  { level: "Form 4", slug: "form-4", stage: "O Level Preparation" },
  { level: "Form 5", slug: "form-5", stage: "GCE O Level" },
  { level: "Lower Sixth", slug: "lower-sixth", stage: "A Level Preparation" },
  { level: "Upper Sixth", slug: "upper-sixth", stage: "GCE A Level" },
];

function buildWorkbooks(subject, code, slugs) {
  return WORKBOOK_LEVELS
    .filter(l => !slugs || slugs.includes(l.slug))
    .map(l => ({
      id: `${code}-${l.slug}`,
      subject,
      level: l.level,
      stage: l.stage,
      cover: `images/academy/workbooks/${code}-${l.slug}.jpg`,
      price: WORKBOOK_PRICES[l.level] || 0,
      status: "available",
    }));
}

const ACADEMY_WORKBOOKS = [
  ...buildWorkbooks("Computer Science", "cs"),
  ...buildWorkbooks("ICT", "ict", ["form-4", "form-5", "lower-sixth", "upper-sixth"]),
  ...buildWorkbooks("Mathematics", "maths"),
];
