"""
Extra Academy pages, built in English and French from one source:

  /past-papers  + /epreuves     every official MINESEC paper, exam → year → subject,
                                from data/minesec-papers.json (each subject opens on
                                the ministry's own platform, which hosts the papers)
  /skills       + /formations   skills courses for anyone: Computer Basics,
                                Web Development, AI & Automation

Run through build.py (python lessons-src/build/build.py) or on its own.

Refreshing the papers list: data/minesec-papers.json holds one row per subject and
year: {"exam", "year", "subject", "papers", "slug"}. Add or change rows, then rebuild.
"""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'lessons-src' / 'data'
SITE = 'https://www.asghinlabs.com'
MINESEC = 'https://minesec-distance.schoolfaqs.net/revision'
WA = 'https://wa.me/237682402876?text='
esc = lambda s: html.escape(str(s), quote=True)


def wa(text):
    return WA + re.sub(r"[ \"&'()%#?]", lambda m: '%{:02X}'.format(ord(m.group())), text)


# ---------------------------------------------------------------- languages
EXAMS = {
    'en': [
        ('gce-ordinary-level', 'GCE O Level', 'General · Form 5'),
        ('gce-advanced-level', 'GCE A Level', 'General · Upper Sixth'),
        ('tvee-il-commercial', 'TVEE Intermediate · Commercial', 'Technical · Intermediate'),
        ('tvee-il-industrial', 'TVEE Intermediate · Industrial', 'Technical · Intermediate'),
        ('tvee-al-commercial', 'TVEE Advanced · Commercial', 'Technical · Advanced'),
        ('tvee-al-industrial', 'TVEE Advanced · Industrial', 'Technical · Advanced'),
        ('mock-o-level-technical', 'TVEE Intermediate · Mock', 'Technical · Mock exam'),
        ('mock-a-level-technical', 'TVEE Advanced · Mock', 'Technical · Mock exam'),
        ('capiemp', 'CAPIEMP', 'Teacher training'),
    ],
    'fr': [
        ('bepc', 'BEPC', '3e · examen officiel'),
        ('bepc-blanc', 'BEPC blanc', '3e · examen blanc'),
        ('probatoire-examen-blanc', 'Probatoire · examens blancs', 'Première'),
        ('baccalaureat-blanc', 'Baccalauréat · examens blancs', 'Terminale'),
        ('capiemp', 'CAPIEMP', 'Formation des enseignants'),
    ],
}

T = {
    'en': dict(
        lang='en', locale='en_GB', other='fr', academy='/academy', lessons='/lessons',
        papers_url='/past-papers', skills_url='/skills',
        nav=[('/academy#workbooks', 'Workbooks'), ('/past-papers', 'Past Papers'), ('/lessons', 'Interactive Lessons'),
             ('/skills', 'Skills Courses'), ('/tutor', 'AI Tutor'), ('/academy#enroll', 'Contact')],
        footer_links=[('/', 'Home'), ('/academy', 'Academy'), ('/past-papers', 'Past Papers'), ('/lessons', 'Interactive Lessons'),
                      ('/skills', 'Skills Courses'), ('/epreuves', 'Épreuves (francophone)')],
        footer_by='Part of <a href="/">AsghinLabs</a> · Web • Software • AI • Automation • Training',
        footer_place='📍 Douala, Cameroon', rights='© 2026 AsghinLabs. All rights reserved.',
        wa_hi="Hi AsghinLabs Academy, I'd like to learn more.", chat='Chat on WhatsApp', menu='Menu', logo_alt='AsghinLabs Academy logo',
        # papers
        pp_title='GCE & TVEE Past Papers: every official paper, by year | AsghinLabs Academy',
        pp_h1='GCE &amp; TVEE past papers',
        pp_tag='📝 Free · Official papers · English subsystem',
        pp_lead='Every official paper published by the Ministry of Secondary Education, sorted by exam, year and subject. Pick yours and it opens on the ministry\'s platform.',
        pp_desc='{n} official GCE O Level, A Level and TVEE past papers ({y0}–{y1}), sorted by exam, year and subject. Free, from the MINESEC platform.',
        pp_stats=('papers', 'subjects', 'exams', 'years'),
        pp_search='🔎 Search a subject: e.g. Computer Science, Physics, Accounting',
        pp_quick=['Mathematics', 'Computer Science', 'ICT', 'Physics', 'Chemistry', 'Biology', 'English', 'French', 'Economics'],
        pp_all='All exams', pp_answers='Answers', pp_paper=('paper', 'papers'), pp_open='Open ↗', pp_subjects=('subject', 'subjects'),
        pp_empty='No paper found for that search. <a class="inline-link" href="{wa}" target="_blank" rel="noopener">Ask us on WhatsApp →</a>',
        pp_note='Each paper belongs to the body that set it (the GCE Board, MINESEC or its regional delegations, as printed on the paper). They are hosted on the MINESEC distance-learning platform, which may ask you to sign in for some papers. AsghinLabs sorts them so you find yours faster, and adds its own answers where you see ✅.',
        pp_help_h='Stuck on a question?', pp_help_p='Ask the free AI tutor to explain it step by step, or get help from a teacher before the exam.',
        pp_help=[('/tutor', '💬 Ask the AI tutor'), ('/academy#classes', '🎓 GCE revision classes')],
        pp_other='Francophone subsystem? <a href="/epreuves" data-choose="fr" lang="fr">Épreuves du BEPC, Probatoire et Bac →</a>',
        pp_ld_name='GCE and TVEE past papers',
        # skills
        sk_title='Skills Courses: Computer Basics, Web Development, AI & Automation | AsghinLabs Academy',
        sk_desc='Practical courses for anyone in Douala or online: computer basics, building websites, and using AI and automation at work. Small groups, real projects, taught in English or French.',
        sk_tag='🛠️ For anyone · Not only school students',
        sk_h1='Skills that get you <span class="accent">work</span>, clients and confidence',
        sk_lead='Short, practical courses for students, parents, job seekers and business owners. You learn on real tasks and leave with something you made yourself. In person in Douala or online, in English or French.',
        sk_cta=('See the courses', 'Ask on WhatsApp'),
        sk_points=['Small groups or one-to-one', 'Taught by a developer who builds for real clients', 'English or French'],
        sk_courses_h='Choose a course', sk_courses_sub='Start where you are. Each course has a clear end result.',
        sk_for='Who it is for', sk_learn="What you'll be able to do", sk_end='You finish with',
        sk_level='Level', colon=': ', sk_join='Ask for the next start date →',
        sk_lang='<a href="/formations" lang="fr" hreflang="fr">Version française →</a>',
        sk_how_h='How it works',
        sk_how=[('💬', 'Message us', 'Tell us which course and your level. We reply on WhatsApp.'),
                ('🧭', 'Short placement chat', 'We check what you already know so you start at the right point.'),
                ('🚀', 'Start learning', 'Join the next group or book one-to-one sessions, in Douala or online.')],
        sk_price='Price and dates depend on the format (group, one-to-one, online). Ask on WhatsApp and you get them straight away.',
        sk_proof_h='Learn from someone who builds for real',
        sk_proof_p='AsghinLabs builds websites, software and AI automations for clients. The courses teach the same tools and habits, so what you learn is what is used at work.',
        sk_proof=[('/portfolio', 'See our work →'), ('/founder', 'Meet the teacher →')],
        sk_school='Preparing GCE exams instead? <a href="/academy" data-choose="en">English-subsystem Academy →</a> · <a href="/academie" data-choose="fr" lang="fr">Académie francophone →</a>',
        sk_faq_h='Questions',
        sk_faq=[('Do I need my own computer?', 'It helps a lot, especially for Web Development and AI &amp; Automation. For Computer Basics in Douala, tell us and we will find a solution together.'),
                ('Is there a minimum age?', 'Secondary-school students are welcome from about Form 3 for Web Development. Computer Basics and AI &amp; Automation are open to adults of any age.'),
                ('Do I get a certificate?', 'You get an AsghinLabs Academy certificate of completion, and for Web Development a live website you can show anyone.'),
                ('Can I pay in instalments?', 'Ask us on WhatsApp. We agree on the payment arrangement together before you start; nothing is paid on this site.')],
        courses=[
            dict(id='computer-basics', icon='🖥️', name='Computer Basics', tag='Beginner', c='0, 212, 255',
                 pitch='Use a computer with confidence, for school, work or your business.',
                 who='Complete beginners, parents, workers who were never shown properly, older learners.',
                 learn=['Use the keyboard, mouse and files without fear', 'Write and format documents in Word', 'Simple tables and sums in Excel',
                        'Search the internet and use e-mail safely', 'Avoid scams, viruses and lost files'],
                 end='Your own CV typed and saved, and an e-mail account you know how to use.'),
            dict(id='web-development', icon='🌐', name='Web Development', tag='Beginner → Intermediate', c='46, 230, 139',
                 pitch='Build and publish your own website, from the first line of code.',
                 who='Students from Form 3, job seekers, freelancers and small businesses that want a site.',
                 learn=['Structure pages with HTML and style them with CSS', 'Make them work on phones (responsive design)', 'Add interaction with JavaScript',
                        'Use the tools developers use: VS Code, Git and GitHub', 'Put your site online for free with a real address'],
                 end='A live website of your own, online, that you can show to clients or employers.'),
            dict(id='ai-automation', icon='🤖', name='AI & Automation', tag='Beginner · computer basics needed', c='255, 196, 0',
                 pitch='Make AI tools do real work for you, and automate the boring tasks.',
                 who='Business owners, teachers, students and office workers who want to save time.',
                 learn=['Write prompts that give useful answers, in English or French', 'Use AI for documents, lessons, marketing and research, and check its mistakes',
                        'Automate tasks with Google Sheets, Forms and WhatsApp Business', 'Read and adapt small Python scripts that do the work for you'],
                 end='At least one automation running on a real task from your own work or business.'),
        ],
    ),
    'fr': dict(
        lang='fr', locale='fr_FR', other='en', academy='/academie', lessons='/lecons',
        papers_url='/epreuves', skills_url='/formations',
        nav=[('/academie#cahiers', 'Cahiers'), ('/epreuves', 'Épreuves'), ('/lecons', 'Leçons interactives'),
             ('/formations', 'Formations'), ('/tutor', 'Tuteur IA'), ('/academie#contact', 'Contact')],
        footer_links=[('/', 'Accueil'), ('/academie', 'Académie'), ('/epreuves', 'Épreuves'), ('/lecons', 'Leçons interactives'),
                      ('/formations', 'Formations'), ('/past-papers', 'Past papers (anglophone)')],
        footer_by='Une marque d\'<a href="/">AsghinLabs</a> : Web • Logiciels • IA • Automatisation • Formation',
        footer_place='📍 Douala, Cameroun', rights='© 2026 AsghinLabs. Tous droits réservés.',
        wa_hi="Bonjour AsghinLabs Academy, j'aimerais en savoir plus.", chat='Écrire sur WhatsApp', menu='Menu', logo_alt='Logo AsghinLabs Academy',
        pp_title='Épreuves du BEPC, Probatoire et Bac : toutes les épreuves officielles | AsghinLabs Academy',
        pp_h1='Épreuves officielles',
        pp_tag='📝 Gratuit · Épreuves officielles · Sous-système francophone',
        pp_lead='Toutes les épreuves publiées par le Ministère des Enseignements Secondaires, classées par examen, par année et par matière. Choisissez la vôtre : elle s\'ouvre sur la plateforme du ministère.',
        pp_desc='{n} épreuves officielles du BEPC, du BEPC blanc, du Probatoire et du Bac blanc ({y0}–{y1}), classées par examen, année et matière. Gratuit, depuis la plateforme du MINESEC.',
        pp_stats=('épreuves', 'matières', 'examens', 'années'),
        pp_search='🔎 Chercher une matière : ex. Informatique, Mathématiques, Anglais',
        pp_quick=['Informatique', 'Mathématiques', 'Programmation', 'Physique', 'SVT', 'Anglais', 'Histoire', 'Géographie', 'Travaux pratiques'],
        pp_all='Tous les examens', pp_answers='Corrigé', pp_paper=('épreuve', 'épreuves'), pp_open='Ouvrir ↗', pp_subjects=('matière', 'matières'),
        pp_empty='Aucune épreuve trouvée pour cette recherche. <a class="inline-link" href="{wa}" target="_blank" rel="noopener">Demandez-nous sur WhatsApp →</a>',
        pp_note='Chaque épreuve appartient à l\'organisme qui l\'a conçue (MINESEC, ses délégations régionales, l\'Office du Bac…, comme indiqué sur l\'épreuve). Elles sont hébergées sur la plateforme d\'enseignement à distance du MINESEC, qui peut demander une connexion pour certaines épreuves. AsghinLabs les classe pour que vous trouviez la vôtre plus vite, et ajoute ses corrigés là où vous voyez ✅.',
        pp_help_h='Bloqué sur une question ?', pp_help_p='Demandez au tuteur IA gratuit de l\'expliquer étape par étape, ou faites-vous accompagner par un enseignant avant l\'examen.',
        pp_help=[('/tutor', '💬 Demander au tuteur IA'), ('/academie#cours', '🎓 Préparation aux examens')],
        pp_other='Sous-système anglophone ? <a href="/past-papers" data-choose="en" lang="en">GCE &amp; TVEE past papers →</a>',
        pp_ld_name='Épreuves officielles du BEPC, du Probatoire et du Baccalauréat',
        sk_title='Formations : bases de l\'informatique, développement web, IA et automatisation | AsghinLabs Academy',
        sk_desc='Des formations pratiques pour tous, à Douala ou en ligne : bases de l\'informatique, création de sites web, IA et automatisation au travail. Petits groupes, vrais projets, en français ou en anglais.',
        sk_tag='🛠️ Pour tous · Pas seulement pour les élèves',
        sk_h1='Des compétences pour trouver du <span class="accent">travail</span>, des clients et de l\'assurance',
        sk_lead='Des formations courtes et pratiques pour élèves, parents, chercheurs d\'emploi et entrepreneurs. Vous apprenez sur de vraies tâches et repartez avec quelque chose que vous avez fait vous-même. À Douala ou en ligne, en français ou en anglais.',
        sk_cta=('Voir les formations', 'Demander sur WhatsApp'),
        sk_points=['Petits groupes ou cours individuels', 'Un formateur qui développe pour de vrais clients', 'En français ou en anglais'],
        sk_courses_h='Choisissez une formation', sk_courses_sub='Commencez là où vous en êtes. Chaque formation a un résultat concret.',
        sk_for='Pour qui', sk_learn='Ce que vous saurez faire', sk_end='Vous repartez avec',
        sk_level='Niveau', colon=' : ', sk_join='Demander la prochaine date →',
        sk_lang='<a href="/skills" lang="en" hreflang="en">English version →</a>',
        sk_how_h='Comment ça marche',
        sk_how=[('💬', 'Écrivez-nous', 'Dites-nous la formation et votre niveau. Nous répondons sur WhatsApp.'),
                ('🧭', 'Petit échange de niveau', 'Nous voyons ce que vous savez déjà, pour commencer au bon endroit.'),
                ('🚀', 'Commencez', 'Rejoignez le prochain groupe ou réservez des séances individuelles, à Douala ou en ligne.')],
        sk_price='Le tarif et les dates dépendent de la formule (groupe, individuel, en ligne). Demandez sur WhatsApp et vous les recevez tout de suite.',
        sk_proof_h='Apprenez avec quelqu\'un qui réalise de vrais projets',
        sk_proof_p='AsghinLabs crée des sites web, des logiciels et des automatisations IA pour des clients. Les formations utilisent les mêmes outils et les mêmes méthodes : ce que vous apprenez sert vraiment au travail.',
        sk_proof=[('/portfolio', 'Voir nos réalisations →'), ('/founder', 'Rencontrer le formateur →')],
        sk_school='Vous préparez le BEPC ou le Bac ? <a href="/academie" data-choose="fr">Académie francophone →</a> · <a href="/academy" data-choose="en" lang="en">English-subsystem Academy →</a>',
        sk_faq_h='Questions',
        sk_faq=[('Faut-il avoir son propre ordinateur ?', 'C\'est vivement conseillé, surtout pour le développement web et l\'IA. Pour les bases de l\'informatique à Douala, dites-le-nous et nous trouverons une solution ensemble.'),
                ('Y a-t-il un âge minimum ?', 'Les élèves sont les bienvenus à partir de la 4<sup>e</sup> environ pour le développement web. Les bases de l\'informatique et l\'IA sont ouvertes aux adultes de tout âge.'),
                ('Reçoit-on une attestation ?', 'Vous recevez une attestation de fin de formation AsghinLabs Academy et, pour le développement web, un site en ligne que vous pouvez montrer à tous.'),
                ('Peut-on payer en plusieurs fois ?', 'Demandez-nous sur WhatsApp. Nous convenons ensemble du mode de paiement avant de commencer ; rien ne se paie sur ce site.')],
        courses=[
            dict(id='computer-basics', icon='🖥️', name='Bases de l\'informatique', tag='Débutant', c='0, 212, 255',
                 pitch='Utiliser un ordinateur avec assurance, pour l\'école, le travail ou votre activité.',
                 who='Grands débutants, parents, travailleurs à qui on n\'a jamais vraiment montré, apprenants plus âgés.',
                 learn=['Utiliser le clavier, la souris et les fichiers sans crainte', 'Rédiger et mettre en forme un document Word', 'Faire des tableaux et des calculs simples dans Excel',
                        'Chercher sur Internet et utiliser l\'e-mail en sécurité', 'Éviter les arnaques, les virus et la perte de fichiers'],
                 end='Votre CV saisi et enregistré, et une adresse e-mail que vous savez utiliser.'),
            dict(id='web-development', icon='🌐', name='Développement web', tag='Débutant → intermédiaire', c='46, 230, 139',
                 pitch='Créer et mettre en ligne votre propre site web, dès la première ligne de code.',
                 who='Élèves à partir de la 4e, chercheurs d\'emploi, indépendants et petites entreprises qui veulent un site.',
                 learn=['Structurer des pages en HTML et les mettre en forme en CSS', 'Les adapter aux téléphones (responsive design)', 'Ajouter de l\'interaction avec JavaScript',
                        'Utiliser les outils des développeurs : VS Code, Git et GitHub', 'Mettre votre site en ligne gratuitement, avec une vraie adresse'],
                 end='Votre propre site web, en ligne, à montrer à des clients ou à des employeurs.'),
            dict(id='ai-automation', icon='🤖', name='IA et automatisation', tag='Débutant · bases de l\'informatique requises', c='255, 196, 0',
                 pitch='Faire travailler les outils d\'IA pour vous, et automatiser les tâches répétitives.',
                 who='Entrepreneurs, enseignants, élèves et employés de bureau qui veulent gagner du temps.',
                 learn=['Écrire des consignes (prompts) qui donnent des réponses utiles, en français ou en anglais', 'Utiliser l\'IA pour les documents, les cours, le marketing et la recherche, et repérer ses erreurs',
                        'Automatiser des tâches avec Google Sheets, Forms et WhatsApp Business', 'Lire et adapter de petits scripts Python qui font le travail pour vous'],
                 end='Au moins une automatisation qui fonctionne sur une vraie tâche de votre travail ou de votre activité.'),
        ],
    ),
}


# ---------------------------------------------------------------- shared page parts
def head(L, title, desc, url, other_url, ld):
    return f'''<!DOCTYPE html>
<html lang="{L['lang']}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{SITE}{url}">
  <link rel="alternate" hreflang="{L['lang']}" href="{SITE}{url}">
  <link rel="alternate" hreflang="{L['other']}" href="{SITE}{other_url}">
  <link rel="apple-touch-icon" href="/images/logo-blue.jpeg">
  <link rel="icon" href="/images/logo-blue.jpeg" type="image/jpeg">
  <meta property="og:site_name" content="AsghinLabs">
  <meta property="og:locale" content="{L['locale']}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{SITE}{url}">
  <meta property="og:image" content="{SITE}/images/og-cover.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style-main.css">
  <link rel="stylesheet" href="/style-academy.css">
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
'''


def nav(L, here):
    cur = ' aria-current="page"'
    items = ''.join('\n    <li><a href="%s"%s>%s</a></li>' % (u, cur if u == here else '', t) for u, t in L['nav'])
    return f'''
<nav>
  <a class="logo" href="{L['academy']}">
    <img src="/images/logo-blue.jpeg" alt="{L['logo_alt']}" id="navLogoImg" width="42" height="42">
    <span>ASGHINLABS <span class="logo-sub">Academy</span></span>
  </a>
  <button class="hamburger" id="hamburgerBtn" aria-label="{L['menu']}" aria-expanded="false" aria-controls="navLinks">
    <span></span>
    <span></span>
    <span></span>
  </button>
  <ul class="nav-links" id="navLinks">{items}
    <li><a href="/" class="nav-back">← AsghinLabs</a></li>
  </ul>
</nav>
'''


def footer(L):
    links = ' · '.join(f'<a href="{u}">{t}</a>' for u, t in L['footer_links'])
    return f'''
<footer>
  <p style="font-weight:700; color:var(--text-light); margin-bottom:6px;">AsghinLabs Academy</p>
  <p style="margin-bottom:6px;">{L['footer_by']}</p>
  <p style="margin-bottom:18px;">{L['footer_place']} · 📞 <a href="tel:+237682402876">+237 682 402 876</a> · 📧 <a href="mailto:asghinlabs@gmail.com">asghinlabs@gmail.com</a></p>
  <div class="footer-links" role="navigation" aria-label="Footer">{links}</div>
  {L['rights']}
</footer>

<a class="whatsapp-float" href="{wa(L['wa_hi'])}" target="_blank" rel="noopener" aria-label="{L['chat']}">💬</a>
'''


def load_solutions():
    """(exam, year, subject-address) → [(paper name, page url)] for subjects with AsghinLabs answers."""
    out = {}
    for f in sorted((DATA / 'solutions').glob('*.json')) if (DATA / 'solutions').exists() else []:
        d = json.loads(f.read_text(encoding='utf-8'))
        n = re.search(r'\d+', d['paper']).group()
        out.setdefault((d['exam'], int(d['year']), d['subject_slug']), []).append(
            (d['paper'], f"/papers/{d['exam']}/{d['year']}/{d['subject_slug']}/paper-{n}"))
    return out


SOLUTIONS = {}


def write(url, text):
    (ROOT / (url.lstrip('/') + '.html')).write_text(text, encoding='utf-8')


# ---------------------------------------------------------------- past papers
def build_papers(lang, rows):
    L = T[lang]
    url, other_url = L['papers_url'], T[L['other']]['papers_url']
    exams = [e for e in EXAMS[lang] if any(r['exam'] == e[0] for r in rows)]
    mine = [r for r in rows if r['exam'] in {e[0] for e in exams}]
    n_papers = sum(r['papers'] for r in mine)
    years = sorted({r['year'] for r in mine})
    subjects = {r['subject'].lower() for r in mine}
    plural = lambda n, w: f'{n} {w[0] if n == 1 else w[1]}'

    desc = L['pp_desc'].format(n=n_papers, y0=years[0], y1=years[-1])
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": L['pp_ld_name'], "description": desc,
          "url": SITE + url, "inLanguage": lang, "isAccessibleForFree": True,
          "isPartOf": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + L['academy']}}

    chips = (f'<button type="button" class="pp-chip on" data-exam="all">{L["pp_all"]} <span>{n_papers}</span></button>' +
             ''.join(f'<button type="button" class="pp-chip" data-exam="{slug}">{esc(name)} <span>{sum(r["papers"] for r in mine if r["exam"] == slug)}</span></button>'
                     for slug, name, _ in exams))
    quick = ''.join(f'<button type="button" class="pp-quick" data-q="{esc(q)}">{esc(q)}</button>' for q in L['pp_quick'])

    secs = ''
    for slug, name, kind in exams:
        er = [r for r in mine if r['exam'] == slug]
        by_year = OrderedDict()
        for r in sorted(er, key=lambda r: (-r['year'], r['subject'].lower())):
            by_year.setdefault(r['year'], []).append(r)
        biggest = max(by_year, key=lambda y: (len(by_year[y]), y))      # open the most complete recent year
        secs += (f'\n  <section class="pp-exam" id="{slug}" data-exam="{slug}">\n'
                 f'    <div class="pp-exam-head"><span class="oc-kind">{esc(kind)}</span><h2>{esc(name)}</h2>'
                 f'<p>{plural(sum(r["papers"] for r in er), L["pp_paper"])} · {plural(len({r["subject"] for r in er}), L["pp_subjects"])} · {min(by_year)}–{max(by_year)}</p></div>\n')
        for y, rs in by_year.items():
            secs += (f'    <details class="pp-year"{" open" if y == biggest else ""}>\n'
                     f'      <summary><span class="pp-y">{y}</span><span class="pp-yc">{plural(sum(r["papers"] for r in rs), L["pp_paper"])} · {plural(len(rs), L["pp_subjects"])}</span></summary>\n'
                     '      <div class="pp-grid">\n')
            for r in rs:
                search = esc((r["subject"] + " " + name + " " + str(y)).lower())
                inner = f'<strong>{esc(r["subject"])}</strong><span>{plural(r["papers"], L["pp_paper"])}</span><em>{L["pp_open"]}</em>'
                sols = SOLUTIONS.get((slug, y, r['slug']), [])
                if not sols:
                    secs += f'        <a class="pp-sub" href="{MINESEC}/{slug}/{y}/{esc(r["slug"])}" target="_blank" rel="noopener" data-search="{search}">{inner}</a>\n'
                else:   # this subject has AsghinLabs answers: card with two links
                    ans = ''.join(f'<a class="pp-ans" href="{u}">✅ {L["pp_answers"]} · {esc(p)}</a>' for p, u in sols)
                    secs += (f'        <div class="pp-sub has-sol" data-search="{search} {L["pp_answers"].lower()}">'
                             f'<a class="pp-main" href="{MINESEC}/{slug}/{y}/{esc(r["slug"])}" target="_blank" rel="noopener">{inner}</a>{ans}</div>\n')
            secs += '      </div>\n    </details>\n'
        secs += '  </section>\n'

    stats = ''.join(f'<div><strong>{v}</strong><span>{k}</span></div>'
                    for v, k in zip([n_papers, len(subjects), len(exams), len(years)], L['pp_stats']))
    empty = L['pp_empty'].format(wa=wa(L['wa_hi']))
    help_links = ''.join(f'<a href="{u}" class="{"primary" if i == 0 else ""}">{t}</a>' for i, (u, t) in enumerate(L['pp_help']))
    page = (head(L, L['pp_title'], desc, url, other_url, ld) +
            f'<body class="academy-page pp-page" data-subsystem="{lang}" data-subsystem-other="{other_url}" data-subsystem-ask>\n' +
            nav(L, url) + f'''
<section class="pp-hero">
  <span class="academy-tag">{L['pp_tag']}</span>
  <h1>{L['pp_h1']}</h1>
  <p class="bio">{L['pp_lead']}</p>
  <div class="pp-stats">{stats}</div>
</section>

<section class="pp-tools" aria-label="Filter">
  <input type="search" id="ppSearch" class="pp-search" placeholder="{esc(L['pp_search'])}" aria-label="{esc(L['pp_search'])}" autocomplete="off">
  <div class="pp-quicks">{quick}</div>
  <div class="pp-chips" role="toolbar">{chips}</div>
  <p class="hub-empty pp-empty" id="ppEmpty" hidden>{empty}</p>
</section>
<div class="pp-list">{secs}</div>

<section class="compact pp-after">
  <p class="official-note">{L['pp_note']}</p>
  <div class="pp-help">
    <h3>{L['pp_help_h']}</h3>
    <p>{L['pp_help_p']}</p>
    <div class="academy-cta">{help_links}</div>
  </div>
  <p class="center-note">{L['pp_other']}</p>
</section>
''' + footer(L) + '''
<script src="/script-main.js"></script>
<script src="/academy-subsystem.js"></script>
<script src="/academy-papers.js"></script>
</body>
</html>
''')
    write(url, page)
    return n_papers


# ---------------------------------------------------------------- skills
def build_skills(lang):
    L = T[lang]
    url, other_url = L['skills_url'], T[L['other']]['skills_url']
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": L['sk_title'].split('|')[0].strip(), "url": SITE + url, "inLanguage": lang,
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
              "@type": "Course", "name": c['name'], "description": c['pitch'], "url": f"{SITE}{url}#{c['id']}", "inLanguage": ["en", "fr"],
              "provider": {"@type": "Organization", "name": "AsghinLabs Academy", "url": SITE + L['academy']}}}
              for i, c in enumerate(L['courses'])]}
    hi = "Hi AsghinLabs Academy, I'm interested in the {} course. When does the next one start, and what is the price?" if lang == 'en' else \
         "Bonjour AsghinLabs Academy, la formation « {} » m'intéresse. Quand commence la prochaine session, et quel est le tarif ?"
    cards = ''
    for c in L['courses']:
        learn = ''.join(f'<li>{x}</li>' for x in c['learn'])
        cards += f'''
    <article class="sk-card" id="{c['id']}" style="--c: {c['c']}">
      <div class="sk-top"><span class="sk-icon" aria-hidden="true">{c['icon']}</span><span class="sk-level">{L['sk_level']}{L['colon']}{esc(c['tag'])}</span></div>
      <h3>{esc(c['name'])}</h3>
      <p class="sk-pitch">{esc(c['pitch'])}</p>
      <h4>{L['sk_learn']}</h4>
      <ul class="track-list">{learn}</ul>
      <h4>{L['sk_for']}</h4>
      <p class="sk-who">{esc(c['who'])}</p>
      <div class="sk-end"><span>🏁 {L['sk_end']}</span>{esc(c['end'])}</div>
      <a class="apply-btn" href="{wa(hi.format(c['name']))}" target="_blank" rel="noopener" data-course="{c['id']}">{L['sk_join']}</a>
    </article>'''
    how = ''.join(f'<div class="sk-step"><span class="sk-step-n">{i + 1}</span><span class="sk-step-i" aria-hidden="true">{ic}</span><h3>{h}</h3><p>{p}</p></div>'
                  for i, (ic, h, p) in enumerate(L['sk_how']))
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in L['sk_faq'])
    points = ''.join(f'<li><span>✓</span> {p}</li>' for p in L['sk_points'])
    proof = ' · '.join(f'<a href="{u}">{t}</a>' for u, t in L['sk_proof'])
    page = (head(L, L['sk_title'], L['sk_desc'], url, other_url, ld) +
            f'<body class="academy-page sk-page" data-subsystem-lang="{lang}">\n' + nav(L, url) + f'''
<section class="academy-hero sk-hero">
  <div class="academy-hero-text">
    <span class="academy-tag">{L['sk_tag']}</span>
    <h1>{L['sk_h1']}</h1>
    <p class="bio">{L['sk_lead']}</p>
    <div class="academy-cta">
      <a href="#courses" class="primary">{L['sk_cta'][0]}</a>
      <a href="{wa(L['wa_hi'])}" target="_blank" rel="noopener">💬 {L['sk_cta'][1]}</a>
    </div>
    <ul class="trust-points">{points}</ul>
    <p class="sk-lang">🌍 {L['sk_lang']}</p>
  </div>
  <div class="sk-hero-art" aria-hidden="true">
    <div class="sk-code"><span class="k">&lt;h1&gt;</span>{'Mon premier site' if lang == 'fr' else 'My first website'}<span class="k">&lt;/h1&gt;</span><br><span class="c">// {'publié en ligne' if lang == 'fr' else 'published online'} ✓</span></div>
    <div class="sk-bubble">🤖 {'Résume ce rapport en 5 points' if lang == 'fr' else 'Summarise this report in 5 points'}</div>
    <div class="sk-sheet"><span>A</span><span>B</span><span>C</span><span>=SUM(B2:B9)</span></div>
  </div>
</section>

<section id="courses">
  <h2 style="text-align:center;">{L['sk_courses_h']}</h2>
  <div class="section-sub" style="text-align:center;">{L['sk_courses_sub']}</div>
  <div class="sk-grid">{cards}
  </div>
  <p class="center-note">{L['sk_price']}</p>
</section>

<section class="compact">
  <h2 style="text-align:center;">{L['sk_how_h']}</h2>
  <div class="sk-steps">{how}</div>
</section>

<section class="compact">
  <div class="pp-help sk-proof">
    <h3>{L['sk_proof_h']}</h3>
    <p>{L['sk_proof_p']}</p>
    <p class="sk-proof-links">{proof}</p>
  </div>
</section>

<section class="compact">
  <h2 style="text-align:center;">{L['sk_faq_h']}</h2>
  <div class="faq">{faq}</div>
  <p class="center-note">{L['sk_school']}</p>
</section>
''' + footer(L) + '''
<script src="/script-main.js"></script>
<script>
  document.querySelectorAll('[data-course]').forEach(a => a.addEventListener('click', () => {
    if (typeof gtag === 'function') gtag('event', 'skills_interest', { course: a.dataset.course, lang: document.documentElement.lang });
  }));
</script>
</body>
</html>
''')
    write(url, page)


def main():
    global SOLUTIONS
    SOLUTIONS = load_solutions()
    rows = json.loads((DATA / 'minesec-papers.json').read_text(encoding='utf-8'))
    n_en, n_fr = build_papers('en', rows), build_papers('fr', rows)
    build_skills('en')
    build_skills('fr')
    print(f'Past papers: {n_en} (English subsystem) + {n_fr} (francophone) · skills pages in English and French.')
    return ['/past-papers', '/epreuves', '/skills', '/formations']


if __name__ == '__main__':
    main()
