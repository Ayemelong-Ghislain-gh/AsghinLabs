# AsghinLabs Academy — interactive lessons

Everything in this folder is the **source** of the lessons. The pages students see are
**generated** into `/lessons/` and `/lessons.html` by one script. This folder is **not
published** on the website (see `/.vercelignore`).

> ⚠️ Never edit the files inside `/lessons/` by hand — your change will be lost the next time
> the build runs. Edit the source here, then rebuild.

---

## Quick start

```bash
# from the project root (needs Python 3.8+, nothing else)
python lessons-src/build/build.py
```

It prints something like:

```
Built 41 activity lessons + 13 practice lessons · 290 of 352 progression lessons still to write.
```

Then check the result (open `lessons.html` with a local server) and commit + push as usual.

---

## Folder map

```
lessons-src/
├── README.md                ← this file
├── data/
│   └── progressions.json    ← chapters + lessons of each MINESEC progression sheet
├── content/                 ← lesson text, one file per class & subject
│   ├── helpers.py           ← mcq(), sort(), match()… + small SVG drawing helpers
│   ├── f1_cs.py             ← Form 1 Computer Science (imports the 3 part files)
│   └── f1_cs_part1.py …     ← the actual lessons, by chapter
├── practice/                ← step-by-step practice lessons (JavaScript), one file each
├── handmade/                ← the first 5 lessons, written directly as HTML
└── build/
    ├── build.py             ← THE build script
    ├── practice_lessons.py  ← titles, descriptions and options of the practice lessons
    ├── hub.js               ← script of the lessons page (tabs, search, share)
    └── parse_progressions.py← reads a new progression PDF into progressions.json
```

What the build writes (do not edit):

```
lessons/<class>/<subject>/<lesson>.html   e.g. lessons/form-1/computer-science/decomposition.html
lessons.html                               the lessons page (class tabs → chapters → lessons)
sitemap.xml                                lesson addresses for Google
vercel.json                                clean URLs + redirects from old lesson addresses
```

Thanks to `"cleanUrls": true`, `lessons/form-1/computer-science/decomposition.html` is
served at **asghinlabs.com/lessons/form-1/computer-science/decomposition**.

---

## Two kinds of lessons

| Kind | Used for | Where it lives |
|---|---|---|
| 🧩 **Activities** | theory lessons: short cards + quiz, sort, match, order, label, fill-in | `content/<class>_<subject>.py` |
| 🧮 **Practice** | method lessons: step-by-step questions with correction (conversions, equations…) | `practice/<name>.js` (+ `build/practice_lessons.py`) or `handmade/` |

Both use the shared browser code in the project root:
`lessons-common.js` (step engine, cards, feedback box, share buttons) and
`lessons-activities.js` (activity types). Styles are in `style-lesson.css`.

---

## Edit an existing activity lesson

1. Find the lesson in `content/` (search for its number, e.g. `38:` for Lesson 38).
2. Change the text.
3. Run `python lessons-src/build/build.py`.

A lesson looks like this:

```python
38: L('Ports are the sockets where we plug cables and devices.',      # one-line intro
      [('Common ports', '<p>USB, HDMI, VGA…</p>'),                       # cards: (title, html)
       ('What plugs in where', '<ul><li>USB: flash drive…</li></ul>')],
      [match('Match the port to the device.', [('USB', 'Flash drive'), ('HDMI', 'Monitor')]),
       mcq('Which port carries picture and sound?', ['HDMI', 'VGA', 'Ethernet'], 'HDMI',
           'VGA carries picture only.'),                                # last text = explanation
       tf('A flash drive uses a USB port.', True)]),
```

### Activity types (from `content/helpers.py`)

| Helper | Student does | Example |
|---|---|---|
| `mcq(q, options, answer, why)` | picks one answer | `mcq('2+2?', ['3','4'], '4')` |
| `tf(q, True/False, why)` | true or false | `tf('RAM is permanent.', False)` |
| `sort(q, groups, [(item, group)…])` | taps a group for each item | input vs output devices |
| `match(q, [(left, right)…])` | chooses the right partner | word ↔ meaning |
| `order(q, [items in correct order])` | moves items with ▲▼ | boot process |
| `label(q, svg, [labels for markers 1, 2, 3…])` | names numbered parts of a picture | parts of a window |
| `fill(q, 'sentence with {0} and {1}', [['answer', 'other ok answer'], …])` | types missing words | |

Every helper also accepts `hint=` (shown when wrong) and `visual=` (picture above the question).
Pictures are small inline SVGs; see `box()`, `arrow()`, `marker()`, `flow()` in `helpers.py`.

---

## Add lessons for a new class or subject

1. **Add the progression** (once per sheet):

   ```bash
   pip install pdfplumber
   python lessons-src/build/parse_progressions.py "Form 2|Mathematics|C:/path/progression_form-2_mathematics.pdf"
   ```

   Check the chapter and lesson titles it wrote in `data/progressions.json` and fix typos.

2. **Create the content file** named `<class>_<subject>.py`:
   `f1, f2, f3, f4, f5, l6, u6` + `cs, maths, ict` → e.g. `content/f2_maths.py`

   ```python
   from helpers import *
   LESSONS = {
       1: L('intro', [cards], [activities]),
       2: …
   }
   ```

   Lessons you haven't written yet simply show as "soon" on the lessons page.

3. Run the build. New lessons appear in the right class, chapter and order automatically,
   with Previous / Next links inside the subject.

---

## Add a practice (step-by-step) lesson

1. Write `practice/<name>.js` (copy an existing one — they use `runWalkthrough()` for the
   cards and `practice({ build })` + `runSteps()` from `lessons-common.js` for the steps).
2. Add its titles and options to `build/practice_lessons.py`.
3. In `build/build.py`, add it to `PRACTICE_PAGES` (its home class, subject and page name) and
   to `PRACTICE_FOR` (which progression lesson numbers it covers).
4. Run the build.

---

## Feedback and sharing

Every lesson automatically gets the "How was this lesson?" box (answers go to
`/api/feedback` → read them at `/feedback-dashboard`) and Share buttons (WhatsApp, copy link).
Nothing to add per lesson.

## Testing tips

* Run a local server from the project root: `python -m http.server 8000`, then open
  `http://localhost:8000/lessons.html`. (Clean URLs only work on Vercel — locally, add `.html`.)
* Try each new lesson on a phone-sized window: every activity should fit without sideways scrolling.
