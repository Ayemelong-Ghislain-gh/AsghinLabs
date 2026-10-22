"""
Sous-système francophone: leçons interactives (/lecons/…) and the hub lecons.html.

Called by build.py after the English build. It reuses the English helpers
(template, head, writing) so both subsystems look the same, but every word
on the page is French and the lessons follow the francophone progressions.

Data
  lessons-src/data/progressions-fr.json   same shape as progressions.json:
      [{"class": "3e", "subject": "Informatique",
        "chapters": [{"chapter": "…", "lessons": [{"n": 1, "title": "…", "integration": false}]}]}]
  lessons-src/content/<code>_<subj>.py    LESSONS = {n: {...}} exactly like the English content files
      code: fr6 fr5 fr4 fr3 fr2nd fr1re frtle · subj: info maths svt     e.g. content/fr3_info.py
  A progression may carry "series": "D" (e.g. Première D SVTEEHB); it is shown next to the class.

Until a class has its progression, the hub shows that class with "bientôt".
"""
import html
import json
import re
import unicodedata

import build as B

SITE = B.SITE
CLASSES = ['6e', '5e', '4e', '3e', 'Seconde', 'Première', 'Terminale']
LABEL = {'6e': '6<sup>e</sup>', '5e': '5<sup>e</sup>', '4e': '4<sup>e</sup>', '3e': '3<sup>e</sup>',
         'Seconde': 'Seconde', 'Première': 'Première', 'Terminale': 'Terminale'}
EXAM = {'3e': 'BEPC', 'Première': 'Probatoire', 'Terminale': 'Baccalauréat'}
CLASS_DIR = {'6e': '6e', '5e': '5e', '4e': '4e', '3e': '3e', 'Seconde': 'seconde', 'Première': 'premiere', 'Terminale': 'terminale'}
CLASS_FILE = {'6e': 'fr6', '5e': 'fr5', '4e': 'fr4', '3e': 'fr3', 'Seconde': 'fr2nd', 'Première': 'fr1re', 'Terminale': 'frtle'}
SUBJECTS = ['Mathématiques', 'Informatique', 'SVTEEHB']
SUBJ_DIR = {'Informatique': 'informatique', 'Mathématiques': 'mathematiques', 'SVTEEHB': 'svteehb'}
SUBJ_FILE = {'Informatique': 'info', 'Mathématiques': 'maths', 'SVTEEHB': 'svt'}
ICON = {'Informatique': '💻', 'Mathématiques': '📐', 'SVTEEHB': '🧬'}


def series_of(r):
    """' D' for a Première D progression, '' otherwise."""
    return (' ' + r['series']) if r.get('series') else ''
WA = 'https://wa.me/237682402876?text='


def slugify(t):
    """« Les fonctions numériques » → les-fonctions-numeriques"""
    t = unicodedata.normalize('NFD', t.replace('&', ' et ').replace('œ', 'oe').replace('’', '-').replace("'", '-'))
    return B.slugify(''.join(ch for ch in t if not unicodedata.combining(ch)))


def wa(text):
    return WA + re.sub(r"[ \"&'()%]", lambda m: '%{:02X}'.format(ord(m.group())), text)


NAV = '''<ul class="nav-links" id="navLinks">
    <li><a href="/epreuves">Épreuves</a></li>
    <li><a href="/lecons">Leçons interactives</a></li>
    <li><a href="/academie#cahiers">Cahiers</a></li>
    <li><a href="/academie#cours">Cours</a></li>
    <li><a href="/academie#contact">Contact</a></li>
    <li><a href="/" class="nav-back">← AsghinLabs</a></li>
  </ul>'''

FOOT = f'''<footer>
  <div class="footer-links" role="navigation" aria-label="Pied de page">
    <a href="/">Accueil</a> · <a href="/academie">Académie (francophone)</a> · <a href="/lecons">Leçons interactives</a> · <a href="/academie#epreuves">Épreuves</a> · <a href="/academie#cours">Cours</a> · <a href="/academy" data-choose="en">English subsystem</a>
  </div>
  <p>© 2026 AsghinLabs Academy. Douala, Cameroun.</p>
</footer>

<a class="whatsapp-float" href="{wa("Bonjour AsghinLabs Academy, j'aimerais en savoir plus (sous-système francophone).")}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">💬</a>

'''


def frenchify_head(h):
    """English lesson <head> + nav → French."""
    h = h.replace('<html lang="en">', '<html lang="fr">', 1)
    h = re.sub(r'<ul class="nav-links" id="navLinks">.*?</ul>', NAV, h, count=1, flags=re.S)
    h = h.replace('<a class="logo" href="/academy.html">', '<a class="logo" href="/academie">', 1)
    h = h.replace('alt="AsghinLabs Academy Logo"', 'alt="Logo AsghinLabs Academy"')
    h = h.replace('aria-label="Menu"', 'aria-label="Menu"')
    if 'og:locale' not in h:
        h = h.replace('<meta property="og:type"', '<meta property="og:locale" content="fr_FR">\n  <meta property="og:type"', 1)
    return h


def ld_for(title, desc, url, level, subject):
    d = B.ld_for(title, desc, url, level, subject)
    d.update(inLanguage='fr', learningResourceType='Leçon interactive')
    d['provider']['url'] = SITE + '/academie'
    return d


# ---------------------------------------------------------------- catalogue
def load_content(cls, subj):
    path = B.SRC / 'content' / f'{CLASS_FILE[cls]}_{SUBJ_FILE[subj]}.py'
    if not path.exists():
        return {}
    spec = B.importlib.util.spec_from_file_location(f'content_{CLASS_FILE[cls]}_{SUBJ_FILE[subj]}', path)
    m = B.importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.LESSONS


def catalogue():
    path = B.SRC / 'data' / 'progressions-fr.json'
    P = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    recs = []
    for p in P:
        cls, subj = p['class'], p['subject']
        content = load_content(cls, subj)
        used = set()
        for ch in p['chapters']:
            for l in ch['lessons']:
                if l.get('integration'):
                    continue
                n = l['n']
                nint = int(re.match(r'\d+', str(n)).group())
                r = dict(cls=cls, subj=subj, chapter=ch['chapter'], n=n, title=l['title'], series=p.get('series', ''))
                if n in content or nint in content:
                    name = slugify(l['title'])
                    while name in used:
                        name += '-2'
                    used.add(name)
                    r.update(kind='activities', url=f'/lecons/{CLASS_DIR[cls]}/{SUBJ_DIR[subj]}/{name}', data=content.get(n, content.get(nint)))
                else:
                    r.update(kind='soon', url=None)
                recs.append(r)
    return recs


# ---------------------------------------------------------------- one lesson
def build_activity(r, prev, nxt):
    d, title, url = r['data'], r['title'], r['url']
    cls, subj = r['cls'], r['subj']
    ser = series_of(r)
    desc = d.get('desc') or f"{title} : leçon interactive gratuite de {subj} en {cls}{ser} ({r['chapter']}), sous-système francophone. Explications courtes, schémas et activités corrigées immédiatement."
    head = frenchify_head(B.make_head(f"{title} — {subj} {cls}{ser} | AsghinLabs Academy", desc, url, ld_for(title, desc, url, cls + ser, subj)))
    link = lambda x, side: '' if not x else (
        f'<a class="{side}" href="{x["url"]}"><span>' + (f'← Précédente : leçon {x["n"]}' if side == 'prev' else f'Suivante : leçon {x["n"]} →') + f'</span>{html.escape(x["title"])}</a>')
    anchor = CLASS_DIR[cls]
    body = f'''<div class="lesson-wrap">
  <div class="lesson-path"><a href="/lecons#{anchor}">← {LABEL[cls]}</a> › <span>{subj}</span> › <span>{html.escape(r['chapter'])}</span></div>
  <span class="lesson-badge">🧩 {subj} · {LABEL[cls]}{ser} · {'Séance' if subj == 'SVTEEHB' else 'Leçon'} {r['n']}</span>
  <h1>{html.escape(title)}</h1>
  <p class="lead">{d.get('lead', '')}</p>

  <div class="lesson-panel" id="learn">
    <h2>📘 Comprendre</h2>
    <p class="lesson-hint">De courtes fiches. Lisez-les, puis vérifiez ce que vous avez compris plus bas.</p>
    <div id="walk"></div>
  </div>

  <div class="lesson-panel" id="practice">
    <h2>✍️ Vérifier ce que j'ai compris</h2>
    <p class="lesson-hint">Répondez à chaque activité puis appuyez sur <b>Vérifier</b>. Les erreurs passent en rouge. Appuyez sur <b>Montrer</b> si vous êtes bloqué.</p>
    <div id="acts"></div>
  </div>

  <div class="lesson-pn">{link(prev, 'prev')}{link(nxt, 'next')}</div>

  <div class="lesson-panel lesson-next">
    <h3>Continuer</h3>
    <p>Entraînez-vous sur les épreuves officielles{(' du ' + EXAM[cls]) if cls in EXAM else ''}, ou demandez un cours particulier.</p>
    <div class="lesson-next-actions">
      <a class="next-btn primary" href="/academie#epreuves">📝 Voir les épreuves</a>
      <a class="next-btn" href="/lecons#{anchor}">Toutes les leçons de {LABEL[cls]} →</a>
    </div>
    <div class="fb"><a href="{wa(f'Bonjour AsghinLabs Academy, j’ai essayé la leçon « {title} » et je voulais dire...')}" target="_blank" rel="noopener">💬 Dites-nous quoi améliorer sur WhatsApp →</a></div>
  </div>
</div>

'''
    data = json.dumps({'cards': [{'title': t, 'html': h} for t, h in d['cards']], 'acts': d['acts']}, ensure_ascii=False)
    slug = f"{CLASS_FILE[cls]}-{SUBJ_FILE[subj]}-{url.rsplit('/', 1)[1]}"
    tail = f'''<script src="/script-main.js"></script>
<script src="/lessons-common.js"></script>
<script src="/lessons-activities.js"></script>
<script>
const LESSON = {data};
runWalkthrough(document.getElementById('walk'), LESSON.cards);
runActivities(document.getElementById('acts'), LESSON.acts, {{ slug: "{slug}" }});
viewLesson("{slug}");
</script>
</body>
</html>
'''
    B.write(url, head + body + FOOT + tail)


# ---------------------------------------------------------------- lecons.html (hub)
def build_hub(recs):
    by = {}
    for r in recs:
        by.setdefault(r['cls'], {}).setdefault(r['subj'], {}).setdefault(r['chapter'], []).append(r)
    ready = lambda c: sum(1 for s in by.get(c, {}).values() for ch in s.values() for x in ch if x['kind'] != 'soon')
    total = sum(ready(c) for c in CLASSES)

    tabs = ('<div class="hub-filters class-tabs" id="hubClasses" role="tablist" aria-label="Choisissez votre classe">'
            '<button type="button" class="hub-filter active" data-class="all">Toutes les classes</button>' +
            ''.join(f'<button type="button" class="hub-filter" data-class="{CLASS_DIR[c]}">{LABEL[c]} <span class="tab-n">{ready(c) or "bientôt"}</span></button>' for c in CLASSES) + '</div>')
    secs = ''
    for c in CLASSES:
        exam = f' <span class="hub-exam">{EXAM[c]}</span>' if c in EXAM else ''
        secs += f'\n  <section class="hub-subject" data-class="{CLASS_DIR[c]}" id="{CLASS_DIR[c]}">\n    <h2>{LABEL[c]}{exam}</h2>\n'
        if c not in by:
            ask = wa(f"Bonjour AsghinLabs Academy, je suis en {c} (sous-système francophone) et j'aimerais une leçon interactive sur...")
            secs += ('    <p class="hub-soon">' + ' · '.join(f'{ICON[s]} {s}' for s in SUBJECTS) +
                     f' : les leçons de {LABEL[c]} sont en préparation, d\'après la progression officielle. '
                     f'<a class="inline-link" href="{ask}" target="_blank" rel="noopener">Dites-nous le chapitre dont vous avez besoin →</a></p>\n')
        for subj in SUBJECTS:
            if subj not in by.get(c, {}):
                continue
            ser = next((series_of(x) for ch in by[c][subj].values() for x in ch), '')
            secs += f'    <h3 class="hub-level">{ICON[subj]} {subj}{(" — " + LABEL[c] + ser) if ser else ""}</h3>\n    <div class="chapters">\n'
            for k, (chap, rows) in enumerate(by[c][subj].items()):
                n_ready = sum(1 for x in rows if x['kind'] != 'soon')
                secs += (f'      <details class="chapter" data-search="{html.escape((chap + " " + c + " " + subj).lower())}">\n'
                         f'        <summary><span class="ch-n">Chapitre {k + 1}</span><span class="ch-t">{html.escape(chap)}</span><span class="ch-c">{n_ready}/{len(rows)}</span></summary>\n'
                         '        <ul class="ch-lessons">\n')
                for x in rows:
                    kw = html.escape(' '.join([x['title'], chap, c, subj]).lower())
                    if x['kind'] == 'soon':
                        secs += f'          <li class="lrow soon" data-search="{kw}"><span class="l-n">{x["n"]}</span><span class="l-t">{html.escape(x["title"])}</span><span class="l-k">bientôt</span></li>\n'
                    else:
                        secs += (f'          <li class="lrow" data-search="{kw}"><a href="{x["url"]}"><span class="l-n">{x["n"]}</span><span class="l-t">{html.escape(x["title"])}</span><span class="l-k activities">🧩 Activités</span></a>'
                                 f'<button type="button" class="card-share row-share" data-url="{SITE + x["url"]}" data-title="{html.escape(x["title"])}" aria-label="Partager {html.escape(x["title"])}">📤</button></li>\n')
                secs += '        </ul>\n      </details>\n'
            secs += '    </div>\n'
        secs += '  </section>'

    desc = ("Leçons interactives gratuites pour le sous-système francophone, de la 6e à la Terminale : "
            "Informatique, Mathématiques et SVT, d'après les progressions officielles du MINESEC. Préparation au BEPC, au Probatoire et au Bac.")
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE + x['url'], "name": x['title']}
             for i, x in enumerate(x for x in recs if x['kind'] == 'activities')]
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Leçons interactives : Informatique, Mathématiques et SVT",
          "description": desc, "url": SITE + "/lecons", "inLanguage": "fr",
          "isPartOf": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + "/academie"},
          "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    lead = ('Choisissez votre classe, ouvrez un chapitre et lancez une leçon. Chaque leçon suit la progression officielle du sous-système francophone : '
            'explications courtes, schémas et activités qui vous corrigent au fur et à mesure.')
    if not total:
        lead += ' Les premières leçons arrivent bientôt, en commençant par les classes d\'examen.'
    page = f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>Leçons interactives : Informatique, Mathématiques et SVT, 6e à Terminale | AsghinLabs Academy</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{SITE}/lecons">
  <link rel="alternate" hreflang="fr" href="{SITE}/lecons">
  <link rel="alternate" hreflang="en" href="{SITE}/lessons">
  <link rel="apple-touch-icon" href="/images/logo-blue.jpeg">
  <link rel="icon" href="/images/logo-blue.jpeg" type="image/jpeg">
  <meta property="og:site_name" content="AsghinLabs">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Leçons interactives : Informatique, Mathématiques et SVT | AsghinLabs Academy">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{SITE}/lecons">
  <meta property="og:image" content="{SITE}/images/og-cover.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style-main.css">
  <link rel="stylesheet" href="/style-lesson.css">
  <link rel="stylesheet" href="/style-subsystem.css">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FK679H74R1"></script>
  <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-FK679H74R1');
  </script>
</head>
<body data-subsystem="fr" data-subsystem-other="/lessons" data-subsystem-ask>

<nav>
  <a class="logo" href="/academie">
    <img src="/images/logo-blue.jpeg" alt="Logo AsghinLabs Academy" id="navLogoImg" width="42" height="42">
    <span>ASGHINLABS <span class="logo-sub">Academy</span></span>
  </a>
  <button class="hamburger" id="hamburgerBtn" aria-label="Menu" aria-expanded="false" aria-controls="navLinks">
    <span></span>
    <span></span>
    <span></span>
  </button>
  {NAV}
</nav>

<div class="lesson-wrap">
  <span class="lesson-badge" style="margin-left:0;">🎮 Gratuit · Sans inscription · Sous-système francophone</span>
  <h1>Leçons interactives</h1>
  <p class="lead">{lead}</p>

  <div class="hub-search" role="search">
    <input type="search" id="lessonSearch" placeholder="🔎 Chercher une leçon : ex. mitose, ADN, binaire, Thalès" aria-label="Chercher une leçon" autocomplete="off">
  </div>
  <p class="hub-empty" id="hubEmpty" hidden>Aucune leçon trouvée pour cette recherche. <a class="inline-link" href="{wa("Bonjour AsghinLabs Academy, j'aimerais une leçon interactive sur...")}" target="_blank" rel="noopener">Demander cette leçon sur WhatsApp →</a></p>
  {tabs}
{secs}

  <div class="lesson-panel lesson-next">
    <h3>Besoin d'une leçon précise ?</h3>
    <p>Dites-nous la matière, la classe et le chapitre qui vous posent le plus de difficultés : il passera en priorité.</p>
    <div class="lesson-next-actions">
      <a class="next-btn primary" href="{wa("Bonjour AsghinLabs Academy, je suis au sous-système francophone et j'aimerais une leçon interactive sur...")}" target="_blank" rel="noopener">💬 Demander une leçon</a>
      <a class="next-btn" href="/academie#epreuves">📝 Épreuves officielles</a>
    </div>
  </div>
</div>

{FOOT}<script src="/script-main.js"></script>
<script src="/lessons-common.js"></script>
{(B.BUILD / 'hub.js').read_text(encoding='utf-8')}
<script src="/academy-subsystem.js"></script>
</body>
</html>
'''
    (B.ROOT / 'lecons.html').write_text(page, encoding='utf-8')


def main():
    """Build every French page; returns the lesson URLs for the sitemap."""
    recs = catalogue()
    for c in CLASSES:
        for subj in SUBJECTS:
            seq = [r for r in recs if r['cls'] == c and r['subj'] == subj and r['kind'] != 'soon']
            for k, r in enumerate(seq):
                build_activity(r, seq[k - 1] if k else None, seq[k + 1] if k + 1 < len(seq) else None)
    build_hub(recs)
    n = sum(r['kind'] == 'activities' for r in recs)
    print(f'Francophone: {n} leçons · {sum(r["kind"] == "soon" for r in recs)} of {len(recs)} still to write '
          f'· {len({r["cls"] for r in recs})} of {len(CLASSES)} classes have a progression.')
    return sorted({r['url'] for r in recs if r['url']})
