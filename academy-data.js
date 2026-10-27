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
// Free SAMPLES only (cover, contents and the first lessons). The complete
// notes are sold in the shop below: "order" is the id of the matching
// product in ACADEMY_WORKBOOKS, so the card shows a "Get the full notes" button.
const NOTES_SAMPLE = (slug, title, subject, level, pages, fullPages, order) => ({
  file: `files/academy/notes/samples/${slug}-notes-sample.pdf`,
  cover: `images/academy/notes/${slug}-notes.jpg`,
  title, subject, level, pages, fullPages, order, sample: true,
});
const ACADEMY_NOTES = [
  NOTES_SAMPLE("maths-lower-sixth", "Mathematics — Full Lesson Notes", "Mathematics", "Lower Sixth", 29, 275, "notes-maths-l6"),
  NOTES_SAMPLE("biology-lower-sixth", "Biology — Full Lesson Notes", "Biology", "Lower Sixth", 25, 217, "notes-bio-l6"),
  NOTES_SAMPLE("physics-lower-sixth", "Physics — Full Lesson Notes", "Physics", "Lower Sixth", 23, 96, "notes-phy-l6"),
  NOTES_SAMPLE("chemistry-lower-sixth", "Chemistry — Full Lesson Notes", "Chemistry", "Lower Sixth", 25, 154, "notes-chem-l6"),
  NOTES_SAMPLE("computer-science-lower-sixth", "Computer Science — Full Lesson Notes", "Computer Science", "Lower Sixth", 22, 201, "notes-cs-l6"),
  NOTES_SAMPLE("maths-upper-sixth", "Pure Maths with Mechanics — Full Lesson Notes", "Mathematics", "Upper Sixth", 29, 249, "notes-maths-u6"),
  NOTES_SAMPLE("biology-upper-sixth", "Biology — Full Lesson Notes", "Biology", "Upper Sixth", 24, 133, "notes-bio-u6"),
  NOTES_SAMPLE("physics-upper-sixth", "Physics — Full Lesson Notes", "Physics", "Upper Sixth", 24, 101, "notes-phy-u6"),
  NOTES_SAMPLE("chemistry-upper-sixth", "Chemistry — Full Lesson Notes", "Chemistry", "Upper Sixth", 24, 137, "notes-chem-u6"),
  NOTES_SAMPLE("computer-science-upper-sixth", "Computer Science — Full Lesson Notes", "Computer Science", "Upper Sixth", 20, 208, "notes-cs-u6"),
  NOTES_SAMPLE("ict-lower-sixth", "ICT — Full Lesson Notes", "ICT", "Lower Sixth", 20, 190, "notes-ict-l6"),
  NOTES_SAMPLE("ict-upper-sixth", "ICT — Full Lesson Notes", "ICT", "Upper Sixth", 24, 159, "notes-ict-u6"),
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
// A Level lesson notes (PDF, sent on WhatsApp). Single-level books (hideInAll)
// only show under the "A Level Notes (PDF)" filter, so "All" stays short.
// ICT is sold per level and per subject (not part of the 5-subject package).
// Prices: 3 000 FCFA per subject
// per level, 5 000 FCFA for both levels of one subject, 20 000 FCFA for all 5 subjects.
const NOTES_PRICE = { level: 3000, both: 5000, all: 20000 };
const NOTES_SUBJECTS = [
  // [code, subject, image slug, Upper Sixth title]
  ["maths", "Mathematics", "maths", "Pure Maths with Mechanics"],
  ["bio", "Biology", "biology", "Biology"],
  ["phy", "Physics", "physics", "Physics"],
  ["chem", "Chemistry", "chemistry", "Chemistry"],
  ["cs", "Computer Science", "computer-science", "Computer Science"],
  ["ict", "ICT", "ict", "ICT"],
];
const ACADEMY_LESSON_NOTES = [
  {
    id: "notes-all", subject: "A Level Notes (PDF)", level: "A Level",
    title: "Complete A Level Notes Package", stage: "Maths, Biology, Physics, Chemistry & Computer Science · Lower + Upper Sixth · PDF",
    price: NOTES_PRICE.all, cover: "images/academy/notes/a-level-notes-package.jpg", status: "available", pack: true, packLabel: "⭐ Best value · 5 subjects",
  },
  ...NOTES_SUBJECTS.flatMap(([code, subject, img, u6title]) => [
    { id: `notes-${code}-both`, subject: "A Level Notes (PDF)", level: "A Level", title: `${subject} — Lower + Upper Sixth`,
      stage: "Both years of the progression · PDF", price: NOTES_PRICE.both, cover: `images/academy/notes/${img}-upper-sixth-notes.jpg`,
      status: "available", pack: true, packLabel: "⭐ 2 years" },
    { id: `notes-${code}-l6`, subject: "A Level Notes (PDF)", level: "Lower Sixth", title: `${subject} — Lower Sixth`,
      stage: "Every lesson of the progression · PDF", price: NOTES_PRICE.level, hideInAll: true, cover: `images/academy/notes/${img}-lower-sixth-notes.jpg`, status: "available" },
    { id: `notes-${code}-u6`, subject: "A Level Notes (PDF)", level: "Upper Sixth", title: `${u6title} — Upper Sixth`,
      stage: "Every lesson of the progression · PDF", price: NOTES_PRICE.level, hideInAll: true, cover: `images/academy/notes/${img}-upper-sixth-notes.jpg`, status: "available" },
  ]),
];

const ACADEMY_WORKBOOKS = [
  ...ACADEMY_LESSON_NOTES,
  ...buildWorkbooks("Computer Science", "cs", ["form-1", "form-2", "form-3", "o-level-complete", "a-level-complete"]),
  ...buildWorkbooks("ICT", "ict", ["a-level-complete"]),
  // Mathematics has its own prices.
  ...buildWorkbooks("Mathematics", "maths", ["form-1", "form-2", "form-3", "o-level-complete", "a-level-complete"], {
    "form-1": 2500, "form-2": 2500, "form-3": 3000, "o-level-complete": 5000, "a-level-complete": 8000,
  }),
];

/* ---------------------------------------------------------------------
   OFFICIAL RESOURCES (English subsystem)
   Links to the Ministry of Secondary Education's own websites. We link to
   them instead of copying their files, so students always get the
   official, up-to-date papers and progression sheets.
   --------------------------------------------------------------------- */
const MINESEC_PAPERS = "https://minesec-distance.schoolfaqs.net/revision";
const ACADEMY_OFFICIAL = {
  papers: [
    // These open our own library page (/past-papers), which lists every paper by year and subject.
    { kind: "GCE · Form 5", title: "GCE O Level past papers", desc: "277 official papers, 2014–2025, all subjects.", url: "/past-papers#gce-ordinary-level", cta: "See the papers →" },
    { kind: "GCE · Upper Sixth", title: "GCE A Level past papers", desc: "395 official papers, 2013–2025, all subjects.", url: "/past-papers#gce-advanced-level", cta: "See the papers →" },
    { kind: "Technical · Intermediate", title: "TVEE Intermediate Level", desc: "Commercial, industrial and mock papers.", url: "/past-papers#tvee-il-commercial", cta: "See the papers →" },
    { kind: "Technical · Advanced", title: "TVEE Advanced Level", desc: "Commercial, industrial and mock papers.", url: "/past-papers#tvee-al-commercial", cta: "See the papers →" },
  ],
  progressions: [
    { kind: "MINESEC · 2026-27", title: "Official progression sheets", desc: "Choose “English Sub System”, then your class and subject, to see the lessons of the year term by term.", url: "https://minesec-ige.com/progression-sheets", cta: "Find my progression ↗" },
  ],
};
