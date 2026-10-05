# asghinlabs.com

Website of **AsghinLabs** (web, software, AI & automation studio, Douala) and
**AsghinLabs Academy** (workbooks, free notes, interactive lessons). Static site hosted on Vercel.

## Structure

| Path | What it is |
|---|---|
| `index.html`, `style-main.css`, `script-main.js`, `script-contact.js` | AsghinLabs home page (shared menu/footer script) |
| `academy.html`, `academy*.js`, `style-academy.css` | Academy page: workbook shop (WhatsApp orders), notes, classes |
| `founder.html`, `portfolio.html` (+ js/css) | Founder profile and design portfolio |
| `lessons.html` | Interactive lessons page — **generated**, see below |
| `lessons/<class>/<subject>/*.html` | Every lesson page — **generated**, do not edit by hand |
| `lessons-common.js`, `lessons-activities.js`, `style-lesson.css` | Shared lesson engine and styles |
| `lessons-src/` | Lesson **sources** + build script (not published) → read `lessons-src/README.md` |
| `api/feedback.js` | Serverless function storing lesson feedback (Upstash Redis via Vercel Storage) |
| `feedback-dashboard.html` | Private page to read lesson feedback (password = `FEEDBACK_ADMIN_KEY`) |
| `files/`, `images/`, `vendor/` | PDFs, pictures, pdf.js |
| `vercel.json` | Clean URLs, redirects, caching |

## Common tasks

* **Edit or add lessons:** see `lessons-src/README.md`, then `python lessons-src/build/build.py`.
* **Change workbook prices:** `academy-data.js`.
* **Deploy:** commit and push to `main` — Vercel deploys automatically.

## Environment variables (Vercel → Settings)

| Name | Purpose |
|---|---|
| `KV_REST_API_URL`, `KV_REST_API_TOKEN` | Added automatically when Upstash Redis is connected (feedback storage) |
| `FEEDBACK_ADMIN_KEY` | Password of the feedback dashboard |
