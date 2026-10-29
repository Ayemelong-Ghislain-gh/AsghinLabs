# asghinlabs.com

Website of **AsghinLabs** (web, software, AI & automation studio, Douala) and
**AsghinLabs Academy** (workbooks, free notes, interactive lessons). Static site hosted on Vercel.

## Structure

| Path | What it is |
|---|---|
| `index.html`, `style-main.css`, `script-main.js`, `script-contact.js` | AsghinLabs home page (shared menu/footer script) |
| `academy.html`, `academy*.js`, `style-academy.css` | Academy page: workbook shop (WhatsApp orders), notes, classes |
| `founder.html`, `portfolio.html` (+ js/css) | Founder profile and design portfolio |
| `website-design-douala.html`, `flyer-design-douala.html`, `logo-design-douala.html`, `ai-automation-cameroon.html`, `website-cost-cameroon.html` + French twins (`creation-site-web-douala`, `conception-flyers-douala`, `creation-logo-douala`, `automatisation-ia-cameroun`, `combien-coute-un-site-web-cameroun`) and `fr.html` (French home) | Service pages — **generated**: edit `services-src/build_services.py`, then `python services-src/build_services.py` |
| `style-service.css` | Styles of the service pages |
| `files/academy/notes/samples/`, `images/academy/notes/` | Free samples of the A Level notes + covers (the full notes are sold, never uploaded) |
| `lessons.html` | Interactive lessons page — **generated**, see below |
| `lessons/<class>/<subject>/*.html` | Every lesson page — **generated**, do not edit by hand |
| `lessons-common.js`, `lessons-activities.js`, `style-lesson.css` | Shared lesson engine and styles |
| `lessons-src/` | Lesson **sources** + build script (not published) → read `lessons-src/README.md` |
| `api/feedback.js` | Serverless function storing lesson feedback (Upstash Redis via Vercel Storage) |
| `feedback-dashboard.html` | Private page to read lesson feedback (password = `FEEDBACK_ADMIN_KEY`) |
| `prep/` + `api/prep.js` | **Private paid exam-prep space — hidden, never link it** (see below) |
| `files/`, `images/`, `vendor/` | PDFs, pictures, pdf.js |
| `vercel.json` | Clean URLs, redirects, caching |

## Common tasks

* **Edit or add lessons:** see `lessons-src/README.md`, then `python lessons-src/build/build.py`.
* **Change workbook or notes prices:** `academy-data.js` (`NOTES_PRICE` for the A Level notes).
* **Edit the service pages (texts, prices):** `services-src/build_services.py`, then `python services-src/build_services.py`.
* **Deploy:** commit and push to `main` — Vercel deploys automatically.

## Environment variables (Vercel → Settings)

| Name | Purpose |
|---|---|
| `KV_REST_API_URL`, `KV_REST_API_TOKEN` | Added automatically when Upstash Redis is connected (feedback storage) |
| `FEEDBACK_ADMIN_KEY` | Password of the feedback dashboard |

## Private exam-prep space (paid, hidden)

For students who pay for exam preparation (Probatoire / BAC ACA Informatique first; GCE, BEPC, other BAC series later).

| Path | What it is |
|---|---|
| `/prep/9y3znsgt` | **Student page** (French). The link is only sent on WhatsApp after payment. Students enter their personal code. |
| `/prep/admin-hbxl16m5` | **Teacher page**: create codes, add past questions + verified corrections, chapters, see each student's progress. Password = `FEEDBACK_ADMIN_KEY`. |
| `prep/student.js`, `prep/admin.js`, `prep/prep.css` | Code of those two pages |
| `api/prep.js` | Serverless function: codes, questions, AI marking / tutor / practice / mock exams (Upstash Redis + Gemini) |

Rules:
* **Never** link these pages from the site, the sitemap or robots.txt. They send `noindex` (meta tag + header in `vercel.json`).
* Past questions and corrections live in the database (added from the teacher page), **not** in the repo, so nobody can read them without a code.
* A code works on 2 devices by default (the teacher can reset it when a student changes phone) and stops on its expiry date.
* Students only see questions whose correction the teacher ticked as checked. The AI marks against that correction.
* AI exercises are labelled “Exercice d'entraînement (IA)” — never presented as official past papers.
* Optional env var: `PREP_DAILY_AI` (AI requests per student per day, default 80; can also be set per student).
