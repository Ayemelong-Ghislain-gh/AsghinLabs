"""
AsghinLabs Academy — lesson builder
===================================
Run from the project root:      python lessons-src/build/build.py

It (re)creates everything students see:
  lessons/<class>/<subject>/<lesson>.html   every lesson page
  lessons.html                               the lessons page (class tabs, chapters, search)
  sitemap.xml                                lesson URLs for Google
  vercel.json                                redirects from old lesson addresses

Never edit files inside lessons/ by hand — edit the sources in lessons-src/ and run this again.
See lessons-src/README.md.
"""
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # project root
SRC = ROOT / 'lessons-src'
BUILD = SRC / 'build'
sys.path.insert(0, str(SRC / 'content'))
sys.path.insert(0, str(BUILD))

from practice_lessons import LESSONS as PRACTICE_META, LOGIC_EXPLORE  # noqa: E402

SITE = 'https://www.asghinlabs.com'
CLASSES = ['Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', 'Lower Sixth', 'Upper Sixth']
CLASS_DIR = {c: c.lower().replace(' ', '-') for c in CLASSES}
SUBJ_DIR = {'Computer Science': 'computer-science', 'Mathematics': 'mathematics', 'ICT': 'ict'}
SUBJ_FILE = {'Computer Science': 'cs', 'Mathematics': 'maths', 'ICT': 'ict'}
CLASS_FILE = {'Form 1': 'f1', 'Form 2': 'f2', 'Form 3': 'f3', 'Form 4': 'f4', 'Form 5': 'f5', 'Lower Sixth': 'l6', 'Upper Sixth': 'u6'}

CHAPTER_FIX = {
    'Understanding Computer evolution': 'Understanding computer evolution',
    'Working with GUI Operating system': 'Working with a GUI operating system',
    'Exploring ai concepts and emerging technologies': 'Exploring AI concepts and emerging technologies',
    'Selecting and manipulating abstract data types (adts) and data structures': 'Selecting and manipulating abstract data types (ADTs) and data structures',
    'Write, debug and run programs in c': 'Write, debug and run programs in C',
    'Introducing Ethics in computing': 'Introducing ethics in computing',
}

# ---------------------------------------------------------------------------
# Practice lessons (step-by-step pages). Each has ONE home address; other
# progression lessons that use it simply link to that address.
#   key: (home class, home subject, page name, source)
#   source = 'handmade:<file>' (lessons-src/handmade) or 'practice' (lessons-src/practice/<key>.js)
# ---------------------------------------------------------------------------
PRACTICE_PAGES = {
    'algorithms-order':       ('Form 1', 'Computer Science', 'introduction-to-algorithms', 'practice'),
    'binary-converter':       ('Form 2', 'Computer Science', 'number-systems-conversions', 'handmade:lesson-binary-converter.html'),
    'unit-conversions':       ('Form 2', 'Computer Science', 'units-of-time-and-storage', 'practice'),
    'expanding-brackets':     ('Form 3', 'Mathematics', 'expanding-brackets', 'handmade:lesson-expanding-brackets.html'),
    'factorising-quadratics': ('Form 3', 'Mathematics', 'factorising-quadratic-trinomials', 'handmade:lesson-factorising-quadratics.html'),
    'change-subject':         ('Form 3', 'Mathematics', 'change-the-subject-of-a-formula', 'practice'),
    'graph-plotter':          ('Form 3', 'Mathematics', 'graphs-lines-and-curves', 'handmade:lesson-graph-plotter.html'),
    'simultaneous-equations': ('Form 3', 'Mathematics', 'simultaneous-equations-elimination', 'practice'),
    'right-triangles':        ('Form 3', 'Mathematics', 'pythagoras-and-soh-cah-toa', 'practice'),
    'cell-referencing':       ('Lower Sixth', 'ICT', 'cell-referencing', 'practice'),
    'logic-gates':            ('Lower Sixth', 'ICT', 'logic-gates-and-truth-tables', 'practice'),
    'sorting-algorithms':     ('Lower Sixth', 'ICT', 'sorting-algorithms', 'handmade:lesson-sorting-algorithms.html'),
    'cpu-scheduling':         ('Upper Sixth', 'Computer Science', 'cpu-scheduling', 'practice'),
}

# Which progression lessons are covered by a practice page: (class, subject, lesson number) -> key
PRACTICE_FOR = {
    ('Form 1', 'Computer Science', 11): 'algorithms-order',
    ('Form 2', 'Computer Science', 14): 'binary-converter',
    ('Form 2', 'Computer Science', 18): 'unit-conversions',
    ('Form 2', 'Computer Science', 19): 'unit-conversions',
    ('Form 3', 'Mathematics', 2): 'expanding-brackets',
    ('Form 3', 'Mathematics', 4): 'factorising-quadratics',
    ('Form 3', 'Mathematics', 6): 'change-subject',
    ('Form 3', 'Mathematics', 8): 'graph-plotter',
    ('Form 3', 'Mathematics', 10): 'simultaneous-equations',
    ('Form 3', 'Mathematics', 14): 'right-triangles',
    ('Form 3', 'Mathematics', 17): 'right-triangles',
    ('Lower Sixth', 'ICT', 15): 'unit-conversions',
    ('Lower Sixth', 'ICT', 34): 'cell-referencing',
    ('Lower Sixth', 'ICT', 72): 'binary-converter',
    ('Lower Sixth', 'ICT', 74): 'logic-gates',
    ('Lower Sixth', 'ICT', 75): 'logic-gates',
    ('Lower Sixth', 'ICT', 89): 'sorting-algorithms',
    ('Upper Sixth', 'Computer Science', 11): 'sorting-algorithms',
    ('Upper Sixth', 'Computer Science', 45): 'cpu-scheduling',
    ('Upper Sixth', 'Computer Science', 46): 'cpu-scheduling',
    ('Upper Sixth', 'Computer Science', 47): 'cpu-scheduling',
}

slugify = lambda t: re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower().replace('&', 'and'))).strip('-')[:60].strip('-')


def practice_url(key):
    c, s, name, _ = PRACTICE_PAGES[key]
    return f'/lessons/{CLASS_DIR[c]}/{SUBJ_DIR[s]}/{name}'


def out_path(url):
    return ROOT / (url.lstrip('/') + '.html')


# ---------------------------------------------------------------- helpers
def absolutize(text):
    """Turn relative links (style.css, images/x.png, academy.html) into site-root links (/style.css …)."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r'^(https?:|/|#|mailto:|tel:|data:|javascript:|\{|\$)', val) or val == '':
            return m.group(0)
        return f'{attr}="/{val}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, text)


TEMPLATE = absolutize((SRC / 'handmade' / 'lesson-expanding-brackets.html').read_text(encoding='utf-8'))
HEAD = TEMPLATE[:TEMPLATE.index('<div class="lesson-wrap">')]
FOOT = TEMPLATE[TEMPLATE.index('<footer>'):TEMPLATE.index('<script src="/script-main.js"></script>')]
TEMPLATE_URL = SITE + '/lesson-expanding-brackets.html'


def make_head(title, desc, url, ld):
    h = HEAD
    h = h.replace(re.search(r'<title>(.*?)</title>', h).group(1), html.escape(title))
    for pat in [r'<meta name="description" content="(.*?)">', r'<meta property="og:description" content="(.*?)">']:
        h = h.replace(re.search(pat, h).group(1), html.escape(desc, quote=True))
    h = h.replace(re.search(r'<meta property="og:title" content="(.*?)">', h).group(1), html.escape(title, quote=True))
    h = h.replace(TEMPLATE_URL, SITE + url)
    return re.sub(r'<script type="application/ld\+json">.*?</script>',
                  '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n  </script>', h, flags=re.S)


def ld_for(title, desc, url, level, subject):
    return {"@context": "https://schema.org", "@type": "LearningResource", "name": title, "description": desc, "url": SITE + url,
            "learningResourceType": "Interactive lesson", "educationalLevel": level, "teaches": title, "about": subject,
            "isAccessibleForFree": True, "inLanguage": "en",
            "provider": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + "/academy.html"},
            "author": {"@type": "Person", "name": "Ayemelong Selobie Ghislain"}}


def wa_link(title):
    return 'https://wa.me/237682402876?text=' + ('Hi AsghinLabs Academy, I tried the lesson "' + title + '" and wanted to say...').replace(' ', '%20').replace('"', '%22').replace('&', '%26')


CLEAN = re.compile(r'(https://www\.asghinlabs\.com/(?:academy|lessons|founder|portfolio))\.html')


def write(url, text):
    text = CLEAN.sub(r'\1', text)   # the site uses clean URLs: /academy, not /academy.html
    p = out_path(url)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


# ---------------------------------------------------------------- practice pages
def build_handmade(key, fname):
    url = practice_url(key)
    t = absolutize((SRC / 'handmade' / fname).read_text(encoding='utf-8'))
    old = SITE + '/' + fname
    t = t.replace(old, SITE + url)
    write(url, t)


def build_practice(key):
    L = next(x for x in PRACTICE_META if x['slug'] == key)
    url = practice_url(key)
    title, desc = L['title'], L['desc']
    head = make_head(f'{title} — Interactive Lesson | AsghinLabs Academy', desc, url, ld_for(title, desc, url, L['level'], L['subject']))
    body = f'''<div class="lesson-wrap">
  <a class="lesson-crumb" href="/lessons#{CLASS_DIR[L['level']]}">← All {L['level']} lessons</a>
  <span class="lesson-badge">🧪 {L['subject']} · {L['level']} · Lesson {L['ref']}</span>
  <h1>{html.escape(title)}</h1>
  <p class="lead">{L['lead']}</p>
{L.get('explore', '')}
  <div class="lesson-panel" id="learn">
    <h2>📘 Learn it</h2>
    <p class="lesson-hint">Four short cards. Read them, then practise below.</p>
    <div id="walk"></div>
  </div>

  <div class="lesson-panel" id="practice">
    <h2>✍️ Practise step by step</h2>
    <p class="lesson-hint">One step at a time. Wrong answers turn red with a hint. Press <b>Show me</b> if you are stuck.</p>
    <div class="lesson-controls">
      {L.get('controls', '')}
      <button type="button" id="pNew" class="primary">🔀 New question</button>
      <span class="chal-score" id="pScore"></span>
    </div>
    <div class="q-big" id="pQuestion"></div>
    <div id="pExtra"></div>
    <div id="pSteps" class="gsteps"></div>
  </div>

  <div class="lesson-panel lesson-next">
    <h3>Keep practising</h3>
    <p>{L.get('next', 'Get more practice in the AsghinLabs Academy workbooks.')}</p>
    <div class="lesson-next-actions">
      <a class="next-btn primary" href="/academy.html#workbooks">🛒 See the workbooks</a>
      <a class="next-btn" href="/lessons#{CLASS_DIR[L['level']]}">More lessons →</a>
    </div>
    <div class="fb"><a href="{wa_link(title)}" target="_blank" rel="noopener">💬 Tell us what to improve on WhatsApp →</a></div>
  </div>
</div>

'''
    script = (SRC / 'practice' / f'{key}.js').read_text(encoding='utf-8')
    tail = f'''<script src="/script-main.js"></script>
<script src="/lessons-common.js"></script>
<script>
{script}
viewLesson("{key}");
</script>
</body>
</html>
'''
    write(url, head + body + FOOT + tail)


# ---------------------------------------------------------------- activity lessons
def load_content(cls, subj):
    path = SRC / 'content' / f'{CLASS_FILE[cls]}_{SUBJ_FILE[subj]}.py'
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location(f'content_{CLASS_FILE[cls]}_{SUBJ_FILE[subj]}', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.LESSONS


def catalogue():
    """Every non-integration lesson of every progression, in order, with its page (or 'soon')."""
    P = json.loads((SRC / 'data' / 'progressions.json').read_text(encoding='utf-8'))
    recs = []
    for p in P:
        cls, subj = p['class'], p['subject']
        content = load_content(cls, subj)
        used = set()
        for ch in p['chapters']:
            chap = CHAPTER_FIX.get(ch['chapter'], ch['chapter'])
            for l in ch['lessons']:
                if l['integration']:
                    continue
                n = l['n']; nint = int(re.match(r'\d+', str(n)).group())
                r = dict(cls=cls, subj=subj, chapter=chap, n=n, title=l['title'])
                key = PRACTICE_FOR.get((cls, subj, n))
                if key:
                    r.update(kind='practice', url=practice_url(key), key=key)
                elif n in content or (isinstance(n, int) and nint in content):
                    name = slugify(l['title'])
                    while name in used: name += '-2'
                    used.add(name)
                    r.update(kind='activities', url=f'/lessons/{CLASS_DIR[cls]}/{SUBJ_DIR[subj]}/{name}', data=content.get(n, content.get(nint)))
                else:
                    r.update(kind='soon', url=None)
                recs.append(r)
    return recs


def build_activity(r, prev, nxt):
    d, title, url = r['data'], r['title'], r['url']
    desc = d.get('desc') or f"{title}: a free interactive {r['subj']} lesson for {r['cls']} ({r['chapter']}). Short explanations, visuals and activities with instant correction."
    head = make_head(f"{title} — {r['cls']} {r['subj']} | AsghinLabs Academy", desc, url, ld_for(title, desc, url, r['cls'], r['subj']))
    link = lambda x, side: '' if not x else (
        f'<a class="{side}" href="{x["url"]}"><span>' + (f'← Previous: Lesson {x["n"]}' if side == 'prev' else f'Next: Lesson {x["n"]} →') + f'</span>{html.escape(x["title"])}</a>')
    anchor = CLASS_DIR[r['cls']]
    body = f'''<div class="lesson-wrap">
  <div class="lesson-path"><a href="/lessons#{anchor}">← {r['cls']}</a> › <span>{r['subj']}</span> › <span>{html.escape(r['chapter'])}</span></div>
  <span class="lesson-badge">🧩 {r['subj']} · {r['cls']} · Lesson {r['n']}</span>
  <h1>{html.escape(title)}</h1>
  <p class="lead">{d.get('lead', '')}</p>

  <div class="lesson-panel" id="learn">
    <h2>📘 Learn it</h2>
    <p class="lesson-hint">Short cards. Read them, then check your understanding below.</p>
    <div id="walk"></div>
  </div>

  <div class="lesson-panel" id="practice">
    <h2>✍️ Check your understanding</h2>
    <p class="lesson-hint">Answer each activity and press <b>Check</b>. Wrong answers turn red. Press <b>Show me</b> if you are stuck.</p>
    <div id="acts"></div>
  </div>

  <div class="lesson-pn">{link(prev, 'prev')}{link(nxt, 'next')}</div>

  <div class="lesson-panel lesson-next">
    <h3>Keep learning</h3>
    <p>Revise this chapter in the AsghinLabs Academy workbooks.</p>
    <div class="lesson-next-actions">
      <a class="next-btn primary" href="/academy.html#workbooks">🛒 See the workbooks</a>
      <a class="next-btn" href="/lessons#{anchor}">All {r['cls']} lessons →</a>
    </div>
    <div class="fb"><a href="{wa_link(title)}" target="_blank" rel="noopener">💬 Tell us what to improve on WhatsApp →</a></div>
  </div>
</div>

'''
    data = json.dumps({'cards': [{'title': t, 'html': h} for t, h in d['cards']], 'acts': d['acts']}, ensure_ascii=False)
    slug = url.rsplit('/', 1)[1]
    tail = f'''<script src="/script-main.js"></script>
<script src="/lessons-common.js"></script>
<script src="/lessons-activities.js"></script>
<script>
const LESSON = {data};
runWalkthrough(document.getElementById('walk'), LESSON.cards);
runActivities(document.getElementById('acts'), LESSON.acts, {{ slug: "{CLASS_FILE[r['cls']]}-{SUBJ_FILE[r['subj']]}-{slug}" }});
viewLesson("{CLASS_FILE[r['cls']]}-{SUBJ_FILE[r['subj']]}-{slug}");
</script>
</body>
</html>
'''
    write(url, head + body + FOOT + tail)


# ---------------------------------------------------------------- lessons.html (hub)
def build_hub(recs):
    p = ROOT / 'lessons.html'
    s = p.read_text(encoding='utf-8')
    keywords = {x['slug']: x.get('keywords', '') for x in PRACTICE_META}
    by = {}
    for r in recs:
        by.setdefault(r['cls'], {}).setdefault(r['subj'], {}).setdefault(r['chapter'], []).append(r)
    ICON = {'Computer Science': '💻', 'Mathematics': '📐', 'ICT': '🖥️'}
    ready = lambda c: sum(1 for subj in by.get(c, {}).values() for ch in subj.values() for x in ch if x['kind'] != 'soon')
    search = '''<div class="hub-search" role="search">
    <input type="search" id="lessonSearch" placeholder="🔎 Search a lesson: e.g. binary, SOH CAH TOA, ports" aria-label="Search lessons" autocomplete="off">
  </div>
  <p class="hub-empty" id="hubEmpty" hidden>No lesson found for that search yet. <a class="inline-link" href="https://wa.me/237682402876?text=Hi%20AsghinLabs%20Academy%2C%20I%27d%20like%20an%20interactive%20lesson%20on..." target="_blank" rel="noopener">Ask for this lesson on WhatsApp →</a></p>'''
    tabs = ('<div class="hub-filters class-tabs" id="hubClasses" role="tablist" aria-label="Choose your class">'
            '<button type="button" class="hub-filter active" data-class="all">All classes</button>' +
            ''.join(f'<button type="button" class="hub-filter" data-class="{CLASS_DIR[c]}">{c} <span class="tab-n">{ready(c) or "soon"}</span></button>' for c in CLASSES) + '</div>')
    secs = ''
    for c in CLASSES:
        secs += f'\n  <section class="hub-subject" data-class="{CLASS_DIR[c]}" id="{CLASS_DIR[c]}">\n    <h2>{c}</h2>\n'
        if c not in by:
            secs += (f'    <p class="hub-soon">Lessons for {c} are coming soon. <a class="inline-link" href="https://wa.me/237682402876?text=Hi%20AsghinLabs%20Academy%2C%20I%27m%20in%20'
                     f'{c.replace(" ", "%20")}%20and%20I%27d%20like%20an%20interactive%20lesson%20on..." target="_blank" rel="noopener">Tell us which topic you need →</a></p>\n')
        for subj in ['Mathematics', 'Computer Science', 'ICT']:
            if subj not in by.get(c, {}):
                continue
            secs += f'    <h3 class="hub-level">{ICON[subj]} {subj}</h3>\n    <div class="chapters">\n'
            for k, (chap, rows) in enumerate(by[c][subj].items()):
                n_ready = sum(1 for x in rows if x['kind'] != 'soon')
                secs += (f'      <details class="chapter" data-search="{html.escape((chap + " " + c + " " + subj).lower())}">\n'
                         f'        <summary><span class="ch-n">Chapter {k + 1}</span><span class="ch-t">{html.escape(chap)}</span><span class="ch-c">{n_ready}/{len(rows)}</span></summary>\n'
                         '        <ul class="ch-lessons">\n')
                for x in rows:
                    kw = html.escape(' '.join([x['title'], chap, c, subj, keywords.get(x.get('key') or '', '')]).lower())
                    if x['kind'] == 'soon':
                        secs += f'          <li class="lrow soon" data-search="{kw}"><span class="l-n">{x["n"]}</span><span class="l-t">{html.escape(x["title"])}</span><span class="l-k">soon</span></li>\n'
                    else:
                        badge = '🧮 Practice' if x['kind'] == 'practice' else '🧩 Activities'
                        secs += (f'          <li class="lrow" data-search="{kw}"><a href="{x["url"]}"><span class="l-n">{x["n"]}</span><span class="l-t">{html.escape(x["title"])}</span><span class="l-k {x["kind"]}">{badge}</span></a>'
                                 f'<button type="button" class="card-share row-share" data-url="{SITE + x["url"]}" data-title="{html.escape(x["title"])}" aria-label="Share {html.escape(x["title"])}">📤</button></li>\n')
                secs += '        </ul>\n      </details>\n'
            secs += '    </div>\n'
        secs += '  </section>'
    a = s.index('<div class="hub-search"') if '<div class="hub-search"' in s else s.index('<div class="hub-filters')
    b = s.index('<div class="lesson-panel lesson-next">')
    s = s[:a] + search + '\n  ' + tabs + '\n' + secs + '\n\n  ' + s[b:]
    s = re.sub(r'<p class="lead">.*?</p>', '<p class="lead">Choose your class, open a chapter and pick a lesson. Every lesson follows your school programme: short explanations, visuals and activities that correct you as you go.</p>', s, count=1, flags=re.S)
    a = s.index('<script>\n(function () {\n  const buttons')
    b = s.index('</script>', a) + len('</script>')
    s = s[:a] + (BUILD / 'hub.js').read_text(encoding='utf-8') + s[b:]
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE + x['url'], "name": x['title']} for i, x in enumerate([x for x in recs if x['kind'] == 'activities'] + [dict(url=practice_url(k), title=k) for k in PRACTICE_PAGES])]
    s = re.sub(r'"itemListElement":\s*\[.*?\]\s*(?=\})', '"itemListElement": ' + json.dumps(items, ensure_ascii=False) + '\n', s, flags=re.S)
    p.write_text(CLEAN.sub(r'\1', s), encoding='utf-8')


# ---------------------------------------------------------------- sitemap + redirects
def build_sitemap(urls):
    p = ROOT / 'sitemap.xml'
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'\s*<url>\s*<loc>https://www\.asghinlabs\.com/(lesson-|lessons/)[^<]*</loc>.*?</url>', '', s, flags=re.S)
    add = ''.join(f'  <url>\n    <loc>{SITE + u}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n' for u in urls)
    s = s.replace('</urlset>', add + '</urlset>')
    p.write_text(s, encoding='utf-8')


def build_redirects():
    """Old addresses (lesson-xyz.html at the site root) keep working."""
    p = ROOT / 'vercel.json'
    v = json.loads(p.read_text(encoding='utf-8'))
    v['cleanUrls'] = True
    keep = [r for r in v.get('redirects', []) if not r['source'].startswith('/lesson-') and r['source'] not in ('/academy', '/lessons')]
    for r in keep:
        if r['source'] == '/learn':
            r['destination'] = '/academy'
    legacy = []
    for key in PRACTICE_PAGES:
        for src in (f'/lesson-{key}', f'/lesson-{key}.html'):
            legacy.append({'source': src, 'destination': practice_url(key), 'permanent': True})
    v['redirects'] = keep + legacy
    p.write_text(json.dumps(v, indent=2) + '\n', encoding='utf-8')


def main():
    for key, (_, _, _, source) in PRACTICE_PAGES.items():
        if source.startswith('handmade:'):
            build_handmade(key, source.split(':', 1)[1])
        else:
            build_practice(key)
    recs = catalogue()
    for c in CLASSES:
        for subj in SUBJ_DIR:
            seq = [r for r in recs if r['cls'] == c and r['subj'] == subj and r['kind'] != 'soon']
            for k, r in enumerate(seq):
                if r['kind'] == 'activities':
                    build_activity(r, seq[k - 1] if k else None, seq[k + 1] if k + 1 < len(seq) else None)
    build_hub(recs)
    urls = sorted({r['url'] for r in recs if r['url']})
    build_sitemap(urls)
    build_redirects()
    act = sum(r['kind'] == 'activities' for r in recs)
    print(f'Built {act} activity lessons + {len(PRACTICE_PAGES)} practice lessons · '
          f'{sum(r["kind"] == "soon" for r in recs)} of {len(recs)} progression lessons still to write.')


if __name__ == '__main__':
    main()
