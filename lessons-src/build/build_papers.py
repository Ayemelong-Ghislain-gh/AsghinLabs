"""
Past-paper pages with solutions: /papers/<exam>/<year>/<subject>/paper-<n>

One page per file in data/solutions/*.json. Each question gets:
  · A B C D buttons, so the student tries first (multiple choice papers)
  · "See answer"   → the AsghinLabs answer and explanation
  · "Ask AI tutor" → /tutor with the question already asked

The paper itself:
  · pages_permitted: false → a button opens the official paper on the MINESEC platform
  · pages_permitted: true  → the original pages are shown on the page, as compressed
                             images loaded one by one from PAPERS_HOST
                             (only for papers whose owner has given written permission)

Solution file format (data/solutions/<exam>-<year>-<subject>-paper-<n>.json):
  {"exam", "exam_name", "year", "subject", "subject_slug", "paper", "paper_code", "kind",
   "owner", "source_page", "pages_permitted", "pages": ["p1.webp", ...] (optional), "level",
   "questions": [{"n", "topic", "answer", "why", "check"?}]}
"check": true marks an answer for a teacher to confirm; it is not shown to students.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

import build_academy_pages as A

ROOT = A.ROOT
DATA = A.DATA / 'solutions'
SITE = A.SITE
PAPERS_HOST = 'https://papers.asghinlabs.com'      # where the page images live (Cloudflare Pages)
esc = A.esc

T = {
    'en': dict(back='← All {exam} papers', title='{exam} {subject} {year} {paper}: answers and explanations',
               h1='{exam} {subject} {year}<span>{paper} · answers &amp; explanations</span>',
               desc='Answers and step-by-step explanations for {exam} {subject} {year} {paper}, by AsghinLabs Academy. Try each question, check your answer, or ask the AI tutor.',
               open='📄 Open the official paper ↗', owner='Paper © {owner}, opened on the MINESEC platform.',
               owner_pages='Paper © {owner}, reproduced with permission.',
               how='Open the paper, try each question, then check your answer here.',
               score='{ok} correct out of {done} tried', reset='↺ Start again', all_on='Show all answers', all_off='Hide all answers',
               see='See answer', hide='Hide answer', tutor='Ask AI tutor', answer='Answer', right='✅ Correct!', wrong='❌ Not this one. Try again or press See answer.',
               ask='I am revising {exam} {subject} {year} {paper}, question {n} ({topic}). The answer is {ans}. My teacher explains: {why} Explain this to me more simply, step by step, then give me a similar practice question to try.',
               pages='The paper', page='Page {i} of {n}', questions='Questions', by='Answers written by AsghinLabs Academy teachers.',
               report='Think an answer is wrong? Tell us on WhatsApp →', report_msg='Hi AsghinLabs Academy, about the answers for {exam} {subject} {year} {paper}, question ...'),
    'fr': dict(back='← Toutes les épreuves {exam}', title='{exam} {subject} {year} {paper} : corrigé et explications',
               h1='{exam} {subject} {year}<span>{paper} · corrigé et explications</span>',
               desc='Corrigé et explications pas à pas : {exam} {subject} {year} {paper}, par AsghinLabs Academy. Essayez chaque question, vérifiez votre réponse ou demandez au tuteur IA.',
               open="📄 Ouvrir l'épreuve officielle ↗", owner='Épreuve © {owner}, ouverte sur la plateforme du MINESEC.',
               owner_pages='Épreuve © {owner}, reproduite avec autorisation.',
               how="Ouvrez l'épreuve, essayez chaque question, puis vérifiez votre réponse ici.",
               score='{ok} juste(s) sur {done} essayée(s)', reset='↺ Recommencer', all_on='Afficher toutes les réponses', all_off='Masquer les réponses',
               see='Voir la réponse', hide='Masquer', tutor='Demander au tuteur IA', answer='Réponse', right='✅ Juste !', wrong='❌ Pas celle-ci. Réessayez ou appuyez sur Voir la réponse.',
               ask="Je révise {exam} {subject} {year} {paper}, question {n} ({topic}). La réponse est {ans}. Mon enseignant explique : {why} Explique-moi cela plus simplement, en français, étape par étape, puis donne-moi une question d'entraînement semblable.",
               pages="L'épreuve", page='Page {i} sur {n}', questions='Questions', by='Corrigé rédigé par les enseignants d’AsghinLabs Academy.',
               report='Une réponse vous semble fausse ? Dites-le-nous sur WhatsApp →', report_msg="Bonjour AsghinLabs Academy, à propos du corrigé {exam} {subject} {year} {paper}, question ..."),
}
FR_EXAMS = {'bepc', 'bepc-blanc', 'probatoire-examen-blanc', 'baccalaureat-blanc'}


def paper_url(d):
    n = re.search(r'\d+', d['paper']).group()
    return f"/papers/{d['exam']}/{d['year']}/{d['subject_slug']}/paper-{n}"


def all_solutions():
    return [json.loads(p.read_text(encoding='utf-8')) for p in sorted(DATA.glob('*.json'))] if DATA.exists() else []


def build_page(d):
    lang = 'fr' if d['exam'] in FR_EXAMS else 'en'
    L, t = A.T[lang], T[lang]
    url = paper_url(d)
    f = dict(exam=d['exam_name'], subject=d['subject'], year=d['year'], paper=d['paper'])
    title = t['title'].format(**f) + ' | AsghinLabs Academy'
    desc = t['desc'].format(**f)
    qs = d['questions']
    mcq = all(q['answer'] in 'ABCD' for q in qs)
    ld = {"@context": "https://schema.org", "@type": "Quiz", "name": t['title'].format(**f), "url": SITE + url, "inLanguage": lang,
          "educationalLevel": d.get('level', ''), "about": d['subject'], "isAccessibleForFree": True,
          "provider": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + L['academy']},
          "hasPart": [{"@type": "Question", "name": f"{q['n']}. {q['topic']}", "acceptedAnswer": {"@type": "Answer", "text": f"{q['answer']}. {q['why']}"}} for q in qs]}

    pages_html = ''
    if d.get('pages_permitted') and d.get('pages'):
        base = f"{PAPERS_HOST}/{d['exam']}/{d['year']}/{d['subject_slug']}/{url.rsplit('/', 1)[1]}/"
        pages_html = (f'<section class="pv-pages" aria-label="{t["pages"]}">' +
                      ''.join(f'<figure class="pv-page"><img src="{base}{p}" loading="{"eager" if i == 0 else "lazy"}" decoding="async" width="1000" height="1414" alt="{esc(t["page"].format(i=i + 1, n=len(d["pages"])))}"><figcaption>{t["page"].format(i=i + 1, n=len(d["pages"]))}</figcaption></figure>'
                              for i, p in enumerate(d['pages'])) + '</section>')
        source = f'<p class="pv-owner">{t["owner_pages"].format(owner=esc(d["owner"]))}</p>'
    else:
        source = (f'<a class="apply-btn" href="{esc(d["source_page"])}" target="_blank" rel="noopener" data-open-paper>{t["open"]}</a>'
                  f'<p class="pv-owner">{t["owner"].format(owner=esc(d["owner"]))} {t["how"]}</p>')

    cards = ''
    for q in qs:
        ask = t['ask'].format(n=q['n'], topic=q['topic'].rstrip('.'), ans=q['answer'], why=q['why'], **f)
        tutor = '/tutor?' + '&'.join(f'{k}={quote(v)}' for k, v in [('tab', 'ask'), ('level', d.get('level', '')), ('q', ask)] if v)
        choices = ''.join(f'<button type="button" class="pv-choice" data-c="{c}">{c}</button>' for c in 'ABCD') if mcq else ''
        cards += f'''
    <article class="pv-q" id="q{q['n']}" data-answer="{esc(q['answer'])}">
      <div class="pv-q-head"><span class="pv-n">{q['n']}</span><span class="pv-topic">{esc(q['topic'])}</span></div>
      <div class="pv-q-actions">{choices}<button type="button" class="pv-see">{t['see']}</button><a class="pv-tutor" href="{tutor}">🤖 {t['tutor']}</a></div>
      <p class="pv-feedback" aria-live="polite"></p>
      <div class="pv-answer" hidden><strong>{t['answer']}: {esc(q['answer'])}</strong><p>{esc(q['why'])}</p></div>
    </article>'''

    back_url = f"{L['papers_url']}#{d['exam']}"
    head = A.head(L, title, desc, url, url, ld).replace('<link rel="stylesheet" href="/style-subsystem.css">',
                                                       '<link rel="stylesheet" href="/style-subsystem.css">\n  <link rel="stylesheet" href="/style-papers.css">')
    page = head + f'<body class="academy-page pv-body" data-mcq="{int(mcq)}">\n' + A.nav(L, L['papers_url']) + f'''
<main class="pv-wrap">
  <a class="pv-back" href="{back_url}">{t['back'].format(exam=esc(d['exam_name']))}</a>
  <h1 class="pv-h1">{t['h1'].format(**{k: esc(v) for k, v in f.items()})}</h1>
  <p class="pv-meta">{esc(d.get('paper_code', ''))} · {esc(d.get('kind', ''))}</p>
  <div class="pv-source">{source}</div>
  {pages_html}
  <section class="pv-questions" aria-label="{t['questions']}">
    <div class="pv-bar">
      <span class="pv-score" data-tpl="{esc(t['score'])}"></span>
      <button type="button" class="pv-all" data-on="{esc(t['all_on'])}" data-off="{esc(t['all_off'])}">{t['all_on']}</button>
      <button type="button" class="pv-reset">{t['reset']}</button>
    </div>
    <div class="pv-grid">{cards}
    </div>
  </section>
  <p class="official-note">{t['by']} <a href="{A.wa(t['report_msg'].format(**f))}" target="_blank" rel="noopener">{t['report']}</a></p>
</main>
''' + A.footer(L) + f'''
<script>window.PV_TEXT = {json.dumps(dict(see=t['see'], hide=t['hide'], right=t['right'], wrong=t['wrong']), ensure_ascii=False)};</script>
<script src="/script-main.js"></script>
<script src="/papers.js"></script>
</body>
</html>
'''
    out = ROOT / (url.lstrip('/') + '.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8')
    return url


def main():
    urls = [build_page(d) for d in all_solutions()]
    print(f'Papers with solutions: {len(urls)}')
    return urls


if __name__ == '__main__':
    main()
