"""
Past-paper pages, one for every official paper in data/paper-files.json:

  /papers/<exam>/<year>/<subject>            the subject's papers for that year
  /papers/<exam>/<year>/<subject>/<paper>    the paper itself (<paper> is its MINESEC address)

The paper is shown page by page as light pictures, loaded one by one from PAPERS_HOST
(papers.asghinlabs.com, a separate free site so this one stays small). The pages are the
originals, never edited, shown with the owners' permission. Each page has an
"Ask AI tutor" button that sends that page to /tutor.

Answers: a paper gets "See answers" only when data/solutions/ has a file for it (matched by
its "source_page" address). Every answer there is written and checked by AsghinLabs teachers.
"check": true marks an answer still being checked: students see "being checked", not the answer.
Papers without answers show a "Request the answers" button (WhatsApp).

Solution file format (data/solutions/<name>.json):
  {"exam", "exam_name", "year", "subject", "subject_slug", "paper", "paper_code", "kind",
   "owner", "source_page", "level", "questions": [{"n", "topic", "answer", "why", "check"?}]}
"""
import json
import re
from collections import OrderedDict
from pathlib import Path
from urllib.parse import quote

import build_academy_pages as A

ROOT = A.ROOT
DATA = A.DATA
SITE = A.SITE
PAPERS_HOST = 'https://papers.asghinlabs.com'      # where the page images live (Cloudflare Pages)
esc = A.esc
FR_EXAMS = {'bepc', 'bepc-blanc', 'probatoire-examen-blanc', 'baccalaureat-blanc'}
EXAM_NAME = {slug: name for lang in A.EXAMS for slug, name, _ in A.EXAMS[lang]}
LEVEL = {'gce-ordinary-level': 'Form 5', 'gce-advanced-level': 'Upper Sixth', 'tvee-il-commercial': 'Form 5',
         'tvee-il-industrial': 'Form 5', 'mock-o-level-technical': 'Form 5', 'tvee-al-commercial': 'Upper Sixth',
         'tvee-al-industrial': 'Upper Sixth', 'mock-a-level-technical': 'Upper Sixth'}
SLUG = re.compile(r'^(?:(sw|nw|we|su|ce|es|lt|fn|ad|no)-)?(.+?)(?:-(\d))?-(\d{4})(?:-(\d+))?$')

T = {
    'en': dict(
        back='← {exam} {subject} {year}', back_lib='← All {exam} papers',
        paper='Paper', version='version', pages_n='{n} pages', page='Page {i} of {n}',
        title='{exam} {subject} {year} {paper}: past paper', title_ans='{exam} {subject} {year} {paper}: past paper with answers',
        desc='The official {exam} {subject} {year} {paper}, free to read page by page on your phone. Ask the AI tutor about any page{ans}.',
        desc_ans=', then check every answer with its explanation',
        owner='Paper © the examining body named on it (GCE Board, MINESEC or its regional delegation). Shown unedited, with permission, to help students revise.',
        see='✅ See answers', request='📝 Request the answers', tutor_all='🤖 Ask AI tutor', tutor_page='🤖 Ask AI tutor about this page',
        ask_page='I am revising {exam} {subject} {year} ({paper}). Page {i} of the official paper is attached. Go through the questions on this page one by one: explain how to approach each one, then give the answer and why. If I name a question number, focus on that one.',
        req_msg='Hi AsghinLabs Academy, please add the answers for {exam} {subject} {year} ({paper}): {url}',
        no_ans_h='Answers coming soon', no_ans_p='Our teachers check every answer before it goes online. Tell us you need this paper and we will do it sooner. Meanwhile, the AI tutor can explain any page.',
        ans_h='Answers and explanations', by='Answers written and checked by AsghinLabs Academy teachers.',
        report='Think an answer is wrong? Tell us on WhatsApp →', report_msg='Hi AsghinLabs Academy, about the answers for {exam} {subject} {year} ({paper}), question ...',
        score='{ok} correct out of {done} tried', reset='↺ Start again', all_on='Show all answers', all_off='Hide all answers',
        see_one='See answer', hide='Hide answer', tutor='Ask AI tutor', answer='Answer', right='✅ Correct!', wrong='❌ Not this one. Try again or press See answer.',
        checking='⏳ This answer is being checked by our teachers. Ask the AI tutor meanwhile.',
        ask_q='I am revising {exam} {subject} {year} ({paper}), question {n} ({topic}). The answer is {ans}. My teacher explains: {why} Explain this to me more simply, step by step, then give me a similar practice question to try.',
        ask_q_check='I am revising {exam} {subject} {year} ({paper}), question {n} ({topic}). Explain how to work it out step by step.',
        sub_title='{exam} {subject} {year}: past papers', sub_h1='{exam} {subject} {year}<span>Past papers · free to read</span>',
        sub_desc='Official {exam} {subject} {year} papers, free to read page by page, with an AI tutor for every page.',
        sub_lead='Pick a paper. It opens right here, page by page.', with_ans='✅ with answers', open='Open →'),
    'fr': dict(
        back='← {exam} {subject} {year}', back_lib='← Toutes les épreuves {exam}',
        paper='Épreuve', version='version', pages_n='{n} pages', page='Page {i} sur {n}',
        title='{exam} {subject} {year} {paper} : épreuve', title_ans='{exam} {subject} {year} {paper} : épreuve et corrigé',
        desc="L'épreuve officielle {exam} {subject} {year} ({paper}), gratuite, page par page sur votre téléphone. Demandez au tuteur IA de vous expliquer n'importe quelle page{ans}.",
        desc_ans=', puis vérifiez chaque réponse avec son explication',
        owner="Épreuve © l'organisme qui l'a conçue (MINESEC, ses délégations régionales, l'Office du Bac…). Reproduite sans modification, avec autorisation, pour aider les élèves à réviser.",
        see='✅ Voir le corrigé', request='📝 Demander le corrigé', tutor_all='🤖 Demander au tuteur IA', tutor_page='🤖 Demander au tuteur IA (cette page)',
        ask_page="Je révise {exam} {subject} {year} ({paper}). La page {i} de l'épreuve officielle est jointe. Prends les questions de cette page une par une : explique comment aborder chacune, puis donne la réponse et pourquoi. Réponds en français. Si je donne un numéro de question, concentre-toi sur celle-là.",
        req_msg="Bonjour AsghinLabs Academy, pouvez-vous ajouter le corrigé de {exam} {subject} {year} ({paper}) : {url}",
        no_ans_h='Corrigé bientôt disponible', no_ans_p="Nos enseignants vérifient chaque réponse avant de la publier. Dites-nous que vous avez besoin de cette épreuve et nous la traiterons plus vite. En attendant, le tuteur IA peut vous expliquer n'importe quelle page.",
        ans_h='Corrigé et explications', by="Corrigé rédigé et vérifié par les enseignants d'AsghinLabs Academy.",
        report='Une réponse vous semble fausse ? Dites-le-nous sur WhatsApp →', report_msg="Bonjour AsghinLabs Academy, à propos du corrigé {exam} {subject} {year} ({paper}), question ...",
        score='{ok} juste(s) sur {done} essayée(s)', reset='↺ Recommencer', all_on='Afficher toutes les réponses', all_off='Masquer les réponses',
        see_one='Voir la réponse', hide='Masquer', tutor='Demander au tuteur IA', answer='Réponse', right='✅ Juste !', wrong='❌ Pas celle-ci. Réessayez ou appuyez sur Voir la réponse.',
        checking='⏳ Cette réponse est en cours de vérification par nos enseignants. Demandez au tuteur IA en attendant.',
        ask_q="Je révise {exam} {subject} {year} ({paper}), question {n} ({topic}). La réponse est {ans}. Mon enseignant explique : {why} Explique-moi cela plus simplement, en français, étape par étape, puis donne-moi une question d'entraînement semblable.",
        ask_q_check="Je révise {exam} {subject} {year} ({paper}), question {n} ({topic}). Explique-moi comment la résoudre étape par étape, en français.",
        sub_title='{exam} {subject} {year} : épreuves', sub_h1='{exam} {subject} {year}<span>Épreuves · lecture gratuite</span>',
        sub_desc='Épreuves officielles {exam} {subject} {year}, gratuites, page par page, avec un tuteur IA pour chaque page.',
        sub_lead="Choisissez une épreuve. Elle s'ouvre ici, page par page.", with_ans='✅ avec corrigé', open='Ouvrir →'),
}


def lang_of(exam):
    return 'fr' if exam in FR_EXAMS else 'en'


def label(slug, lang):
    """sw-biology-1-2025 → 'Paper 1 · SW', computer-science-1-2024-2 → 'Paper 1 · version 3'."""
    t = T[lang]
    m = SLUG.match(slug)
    if not m:
        return t['paper']
    region, _, n, _, copy = m.groups()
    parts = [f"{t['paper']} {n}" if n and n != '0' else t['paper']]
    if region:
        parts.append(region.upper())
    if copy:
        parts.append(f"{t['version']} {int(copy) + 1}")
    return ' · '.join(parts)


def sort_key(e):
    m = SLUG.match(e['slug'])
    region, _, n, _, copy = m.groups() if m else ('', '', '', '', '')
    return (int(n or 0), region or '', int(copy or 0))


def subject_url(e):
    return f"/papers/{e['exam']}/{e['year']}/{e['subject_slug']}"


def paper_url(e):
    return f"{subject_url(e)}/{e['slug']}"


def tutor_link(level, q, img=None):
    params = [('tab', 'ask'), ('level', level), ('img', img), ('q', q)]
    return '/tutor?' + '&'.join(f'{k}={quote(v, safe="")}' for k, v in params if v)


def load_solutions():
    """MINESEC paper address → solution data, for papers with AsghinLabs answers."""
    out = {}
    folder = DATA / 'solutions'
    for f in sorted(folder.glob('*.json')) if folder.exists() else []:
        d = json.loads(f.read_text(encoding='utf-8'))
        out[d['source_page'].rstrip('/').rsplit('/', 1)[1]] = d
    return out


def all_papers():
    p = DATA / 'paper-files.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else []


def write(url, text):
    out = ROOT / (url.lstrip('/') + '.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')


def head(L, title, desc, url, ld):
    return A.head(L, title, desc, url, url, ld).replace(
        '<link rel="stylesheet" href="/style-subsystem.css">',
        '<link rel="stylesheet" href="/style-subsystem.css">\n  <link rel="stylesheet" href="/style-papers.css">')


def answers_html(d, t, f, level):
    qs = d['questions']
    mcq = all(q['answer'] in 'ABCD' for q in qs)
    cards = ''
    for q in qs:
        checking = bool(q.get('check'))
        topic = q['topic'].rstrip('.')
        ask = (t['ask_q_check'] if checking else t['ask_q']).format(n=q['n'], topic=topic, ans=q['answer'], why=q['why'], **f)
        choices = '' if checking or not mcq else ''.join(f'<button type="button" class="pv-choice" data-c="{c}">{c}</button>' for c in 'ABCD')
        body = (f'<p>{t["checking"]}</p>' if checking
                else f'<strong>{t["answer"]}: {esc(q["answer"])}</strong><p>{esc(q["why"])}</p>')
        cards += f'''
    <article class="pv-q" id="q{q['n']}" data-answer="{'' if checking else esc(q['answer'])}">
      <div class="pv-q-head"><span class="pv-n">{q['n']}</span><span class="pv-topic">{esc(q['topic'])}</span></div>
      <div class="pv-q-actions">{choices}<button type="button" class="pv-see">{t['see_one']}</button><a class="pv-tutor" href="{tutor_link(level, ask)}">🤖 {t['tutor']}</a></div>
      <p class="pv-feedback" aria-live="polite"></p>
      <div class="pv-answer" hidden>{body}</div>
    </article>'''
    return mcq, f'''
  <section class="pv-questions" id="answers" aria-label="{t['ans_h']}">
    <h2 class="pv-h2">{t['ans_h']}</h2>
    <div class="pv-bar">
      <span class="pv-score" data-tpl="{esc(t['score'])}"></span>
      <button type="button" class="pv-all" data-on="{esc(t['all_on'])}" data-off="{esc(t['all_off'])}">{t['all_on']}</button>
      <button type="button" class="pv-reset">{t['reset']}</button>
    </div>
    <div class="pv-grid">{cards}
    </div>
  </section>
  <p class="official-note">{t['by']} <a href="{A.wa(t['report_msg'].format(**f))}" target="_blank" rel="noopener">{t['report']}</a></p>'''


def build_paper(e, sol):
    lang = lang_of(e['exam'])
    L, t = A.T[lang], T[lang]
    url = paper_url(e)
    exam = EXAM_NAME[e['exam']]
    name = label(e['slug'], lang)
    f = dict(exam=exam, subject=e['subject'], year=e['year'], paper=name)
    level = (sol or {}).get('level') or LEVEL.get(e['exam'], '')
    n = len(e['pages'])
    title = (t['title_ans'] if sol else t['title']).format(**f) + ' | AsghinLabs Academy'
    desc = t['desc'].format(ans=t['desc_ans'] if sol else '', **f)
    img = lambda i: f"{PAPERS_HOST}/{e['dir']}/p{i}.webp"

    ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": title.split(' | ')[0], "url": SITE + url,
          "inLanguage": lang, "learningResourceType": "Past exam paper", "educationalLevel": level, "about": e['subject'],
          "isAccessibleForFree": True, "provider": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + L['academy']}}
    if sol:
        ld["hasPart"] = [{"@type": "Question", "name": f"{q['n']}. {q['topic']}",
                          "acceptedAnswer": {"@type": "Answer", "text": f"{q['answer']}. {q['why']}"}}
                         for q in sol['questions'] if not q.get('check')]

    pages = ''.join(
        f'''
    <figure class="pv-page" id="page-{i}">
      <img src="{img(i)}" width="1000" height="{h}" loading="{'eager' if i == 1 else 'lazy'}" decoding="async" alt="{esc(t['page'].format(i=i, n=n))} · {esc(exam)} {esc(e['subject'])} {e['year']}">
      <figcaption><span>{t['page'].format(i=i, n=n)}</span><a class="pv-page-tutor" href="{tutor_link(level, t['ask_page'].format(i=i, **f), img(i))}" data-page="{i}">{t['tutor_page']}</a></figcaption>
    </figure>''' for i, h in enumerate(e['pages'], 1))

    req = A.wa(t['req_msg'].format(url=SITE + url, **f))
    if sol:
        mcq, after = answers_html(sol, t, f, level)
        main_btn = f'<a class="apply-btn" href="#answers">{t["see"]}</a>'
    else:
        mcq, after = False, f'''
  <section class="pv-noans" id="answers">
    <h2 class="pv-h2">{t['no_ans_h']}</h2>
    <p>{t['no_ans_p']}</p>
    <a class="apply-btn" href="{req}" target="_blank" rel="noopener" data-request-answers>{t['request']}</a>
  </section>'''
        main_btn = f'<a class="apply-btn" href="{req}" target="_blank" rel="noopener" data-request-answers>{t["request"]}</a>'

    page = head(L, title, desc, url, ld) + f'<body class="academy-page pv-body" data-mcq="{int(mcq)}">\n' + A.nav(L, L['papers_url']) + f'''
<main class="pv-wrap">
  <a class="pv-back" href="{subject_url(e)}">{t['back'].format(**f)}</a>
  <h1 class="pv-h1">{esc(exam)} {esc(e['subject'])} {e['year']}<span>{esc(name)}</span></h1>
  <p class="pv-meta">{t['pages_n'].format(n=n)} · {esc(e['slug'])}</p>
  <div class="pv-source">
    <div class="pv-actions">{main_btn}<a class="pv-tutor-all" href="{tutor_link(level, t['ask_page'].format(i=1, **f), img(1))}">{t['tutor_all']}</a></div>
    <p class="pv-owner">{t['owner']}</p>
  </div>
  <section class="pv-pages" aria-label="{esc(name)}">{pages}
  </section>{after}
</main>
''' + A.footer(L) + f'''
<script>window.PV_TEXT = {json.dumps(dict(see=t['see_one'], hide=t['hide'], right=t['right'], wrong=t['wrong']), ensure_ascii=False)};</script>
<script src="/script-main.js"></script>
<script src="/papers.js"></script>
</body>
</html>
'''
    write(url, page)
    return url


def build_subject(papers, sols):
    e0 = papers[0]
    lang = lang_of(e0['exam'])
    L, t = A.T[lang], T[lang]
    url = subject_url(e0)
    exam = EXAM_NAME[e0['exam']]
    f = dict(exam=exam, subject=e0['subject'], year=e0['year'])
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": t['sub_title'].format(**f), "url": SITE + url,
          "inLanguage": lang, "isAccessibleForFree": True}
    cards = ''.join(
        f'''
    <a class="pv-card" href="{paper_url(e)}"><img src="{PAPERS_HOST}/{e['dir']}/t.webp" width="400" height="160" loading="lazy" decoding="async" alt="">'''
        f'''<strong>{esc(label(e['slug'], lang))}</strong>'''
        f'''<span>{t['pages_n'].format(n=len(e['pages']))}{' · ' + t['with_ans'] if e['slug'] in sols else ''}</span><em>{t['open']}</em></a>'''
        for e in sorted(papers, key=sort_key))
    page = head(L, t['sub_title'].format(**f) + ' | AsghinLabs Academy', t['sub_desc'].format(**f), url, ld) + \
        '<body class="academy-page pv-body">\n' + A.nav(L, L['papers_url']) + f'''
<main class="pv-wrap">
  <a class="pv-back" href="{L['papers_url']}#{e0['exam']}">{t['back_lib'].format(exam=esc(exam))}</a>
  <h1 class="pv-h1">{t['sub_h1'].format(**{k: esc(str(v)) for k, v in f.items()})}</h1>
  <p class="pv-meta">{t['sub_lead']}</p>
  <div class="pv-cards">{cards}
  </div>
  <p class="official-note">{t['owner']}</p>
</main>
''' + A.footer(L) + '''
<script src="/script-main.js"></script>
</body>
</html>
'''
    write(url, page)
    return url


def build_old_answer_redirects(sols, papers):
    """The first answers page lived at /papers/<exam>/<year>/<subject>/paper-<n>. Keep that address working."""
    by_slug = {e['slug']: e for e in papers}
    vp = ROOT / 'vercel.json'
    v = json.loads(vp.read_text(encoding='utf-8'))
    for slug, d in sols.items():
        if slug not in by_slug:
            continue
        n = re.search(r'\d+', d['paper']).group()
        old = f"/papers/{d['exam']}/{d['year']}/{d['subject_slug']}/paper-{n}"
        new = paper_url(by_slug[slug])
        write(old, f'<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="robots" content="noindex">'
                   f'<link rel="canonical" href="{SITE + new}"><meta http-equiv="refresh" content="0; url={new}">'
                   f'<title>Moved</title></head><body><a href="{new}">{SITE + new}</a></body></html>\n')
        v['redirects'] = [r for r in v.get('redirects', []) if r['source'] != old] + [{'source': old, 'destination': new, 'permanent': True}]
    vp.write_text(json.dumps(v, indent=2) + '\n', encoding='utf-8')


def main():
    papers, sols = all_papers(), load_solutions()
    urls = [build_paper(e, sols.get(e['slug'])) for e in papers]
    groups = OrderedDict()
    for e in papers:
        groups.setdefault((e['exam'], e['year'], e['subject_slug']), []).append(e)
    urls += [build_subject(g, sols) for g in groups.values()]
    build_old_answer_redirects(sols, papers)
    print(f'Past papers: {len(papers)} paper pages ({sum(e["slug"] in sols for e in papers)} with answers) · {len(groups)} subject pages')
    return urls


if __name__ == '__main__':
    main()
