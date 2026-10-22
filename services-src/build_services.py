"""
Build the AsghinLabs service pages (English + French), the French home page
and the "how much does a website cost" guides.

    python services-src/build_services.py

Edit the texts in PAGES below, run the script, then commit and push.
It writes one .html file per page at the project root (served without
".html" thanks to cleanUrls) and adds the addresses to sitemap.xml.
This folder is not published (see .vercelignore).
"""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://www.asghinlabs.com'
WA = '237682402876'
PHONE = '+237 682 402 876'
EMAIL = 'asghinlabs@gmail.com'
TODAY = '2026-10-22'


def wa(text):
    return f'https://wa.me/{WA}?text={quote(text)}'


# --------------------------------------------------------------- building blocks
def section(title, sub, body, alt=False, sid=None):
    s = f' id="{sid}"' if sid else ''
    sub = f'\n  <div class="section-sub">{sub}</div>' if sub else ''
    return f'<section class="svc-section{" alt" if alt else ""}"{s}>\n  <h2>{title}</h2>{sub}\n  {body}\n</section>'


def cards(items):
    out = []
    for it in items:
        ico, title, text = it[:3]
        href = it[3] if len(it) > 3 else None
        more = it[4] if len(it) > 4 else ''
        inner = f'<div class="ico">{ico}</div><h3>{title}</h3><p>{text}</p>' + (f'<span class="more">{more}</span>' if more else '')
        out.append(f'<a class="svc-card" href="{href}">{inner}</a>' if href else f'<div class="svc-card">{inner}</div>')
    return '<div class="svc-grid">' + ''.join(out) + '</div>'


def gallery(imgs, cls=''):
    figs = ''.join(
        f'<figure><img src="{src}" alt="{escape(alt)}" loading="lazy" width="400" height="500"><figcaption>{escape(cap)}</figcaption></figure>'
        for src, alt, cap in imgs)
    return f'<div class="svc-gallery {cls}">{figs}</div>'


def plans(items, small=''):
    out = []
    for p in items:
        feat = ' featured' if p.get('featured') else ''
        lis = ''.join(f'<li>{x}</li>' for x in p['items'])
        out.append(f'<div class="svc-plan{feat}"><h3>{p["name"]}</h3><div class="amount">{p["amount"]}</div>'
                   f'<div class="note">{p["note"]}</div><ul>{lis}</ul>'
                   f'<a class="svc-btn wa" href="{p["wa"]}" target="_blank" rel="noopener">💬 {p["cta"]}</a></div>')
    sm = f'<p class="svc-small">{small}</p>' if small else ''
    return '<div class="svc-prices">' + ''.join(out) + '</div>' + sm


def steps(items):
    return '<div class="svc-steps">' + ''.join(f'<div><h3>{t}</h3><p>{p}</p></div>' for t, p in items) + '</div>'


def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


# --------------------------------------------------------------- shared texts
T = {
    'en': dict(
        nav=[('/', 'Home'), ('/website-design-douala', 'Websites'), ('/flyer-design-douala', 'Flyers'),
             ('/logo-design-douala', 'Logos'), ('/ai-automation-cameroon', 'AI'), ('/portfolio', 'Portfolio')],
        academy=('/academy', 'Academy'), lang_label='FR', lang_title='Version française',
        home=('/', 'Home'), menu='Menu',
        cta_title="Let's talk about your project",
        cta_text='Tell us what you need on WhatsApp. We reply within 24 hours with questions, a price and a delivery date — no obligation.',
        cta_wa='💬 Get a quote on WhatsApp', cta_mail='✉️ Send an email',
        related='Other services',
        footer_tag='Building practical digital solutions for businesses and organizations.',
        footer_line='Web • Software • AI • Design — Douala, Cameroon',
        rights='All rights reserved.',
    ),
    'fr': dict(
        nav=[('/fr', 'Accueil'), ('/creation-site-web-douala', 'Sites web'), ('/conception-flyers-douala', 'Flyers'),
             ('/creation-logo-douala', 'Logos'), ('/automatisation-ia-cameroun', 'IA'), ('/portfolio', 'Réalisations')],
        academy=('/academie', 'Academy'), lang_label='EN', lang_title='English version',
        home=('/fr', 'Accueil'), menu='Menu',
        cta_title='Parlons de votre projet',
        cta_text='Dites-nous ce dont vous avez besoin sur WhatsApp. Nous répondons sous 24 heures avec nos questions, un prix et un délai, sans engagement.',
        cta_wa='💬 Demander un devis sur WhatsApp', cta_mail='✉️ Envoyer un e-mail',
        related='Nos autres services',
        footer_tag='Des solutions numériques pratiques pour les entreprises et les organisations.',
        footer_line='Web • Logiciels • IA • Design — Douala, Cameroun',
        rights='Tous droits réservés.',
    ),
}

FOOTER_SERVICES = [
    ('/website-design-douala', 'Website design Douala'), ('/flyer-design-douala', 'Flyer &amp; pamphlet design'),
    ('/logo-design-douala', 'Logo design'), ('/ai-automation-cameroon', 'AI &amp; automation'),
    ('/website-cost-cameroon', 'Website cost in Cameroon'),
    ('/creation-site-web-douala', 'Création site web Douala'), ('/conception-flyers-douala', 'Flyers et dépliants'),
    ('/creation-logo-douala', 'Création de logo'), ('/automatisation-ia-cameroun', 'Automatisation IA'),
    ('/combien-coute-un-site-web-cameroun', 'Prix d’un site web au Cameroun'), ('/fr', 'AsghinLabs en français'),
]

FLYERS = [
    ('images/portfolio/flyers/YokoSuperMarket.jpeg', 'Supermarket promotion flyer', 'Yoko Supermarket — promo flyer'),
    ('images/portfolio/flyers/EasyGas.jpeg', 'Gas delivery flyer', 'Easy Gas — delivery flyer'),
    ('images/portfolio/flyers/HarrietsShopping.jpeg', 'Shop flyer', 'Harriet’s Shopping — shop flyer'),
    ('images/portfolio/flyers/SupremeLaundry.jpeg', 'Laundry service flyer', 'Supreme Laundry — service flyer'),
    ('images/portfolio/flyers/Tralopro.jpeg', 'Business flyer', 'Tralopro — business flyer'),
    ('images/portfolio/flyers/YourHealthYourWealth.jpeg', 'Health awareness flyer', 'Your Health Your Wealth — awareness flyer'),
    ('images/portfolio/flyers/YokoSuperMarket2.jpeg', 'Supermarket flyer, second design', 'Yoko Supermarket — weekly offers'),
]
BANNERS = [
    ('images/portfolio/banners/DoualaSupermarche.jpg', 'Supermarket banner', 'Douala Supermarché — banner'),
    ('images/portfolio/banners/EasyGas.jpg', 'Gas delivery banner', 'Easy Gas — banner'),
    ('images/portfolio/banners/HarrietsShopping.jpg', 'Shop banner', 'Harriet’s Shopping — banner'),
    ('images/portfolio/banners/novatechsolutions.jpg', 'Tech company banner', 'NovaTech Solutions — banner'),
]
LOGOS = [
    ('images/portfolio/logos/DebbiesCloset.jpeg', 'Debbie’s Closet logo', 'Debbie’s Closet'),
    ('images/portfolio/logos/FlassyImport.jpeg', 'Flassy Import logo', 'Flassy Import'),
    ('images/portfolio/logos/MMLuxe.jpeg', 'MM Luxe logo', 'MM Luxe'),
    ('images/portfolio/logos/WildaluxCosmetics.jpeg', 'Wildalux Cosmetics logo', 'Wildalux Cosmetics'),
    ('images/portfolio/logos/YoungDevAfrica.jpeg', 'Young Dev Africa logo', 'Young Dev Africa'),
]


def web_projects(lang):
    en = lang == 'en'
    return cards([
        ('🛒', 'Stacy Xholani — Provisions &amp; More',
         'Online shop for a Douala provisions store: catalogue with search, retail and wholesale prices, gas delivery, and a cart that sends the order straight to WhatsApp. English and French.' if en else
         'Boutique en ligne pour un magasin de provisions à Douala : catalogue avec recherche, prix détail et gros, livraison de gaz et un panier qui envoie la commande directement sur WhatsApp. Français et anglais.',
         'https://stacy-xholani-website.vercel.app/', 'View the site →' if en else 'Voir le site →'),
        ('👞', 'J-VIC CHAKA — Shoe maker',
         'Showcase site for a Douala shoe maker: collections, product pages and a WhatsApp button on every shoe to turn visitors into orders.' if en else
         'Site vitrine pour un cordonnier de Douala : collections, fiches produits et un bouton WhatsApp sur chaque chaussure pour transformer les visites en commandes.',
         'https://jvic-chaka.vercel.app/', 'View the site →' if en else 'Voir le site →'),
        ('🏠', 'StudentStay',
         'Student accommodation platform: students find rooms and hostels, owners reach tenants online.' if en else
         'Plateforme de logement étudiant : les étudiants trouvent des chambres, les propriétaires trouvent des locataires en ligne.',
         'https://studentstay-cm.vercel.app/', 'View the site →' if en else 'Voir le site →'),
        ('🚗', 'Ride Along',
         'Ride-sharing web app: drivers post trips, passengers book seats, chat with the driver and follow the car live on a map.' if en else
         'Application de covoiturage : les chauffeurs publient leurs trajets, les passagers réservent, discutent avec le chauffeur et suivent la voiture en direct.',
         'https://ridealong-two.vercel.app/', 'View the app →' if en else 'Voir l’application →'),
    ])


# --------------------------------------------------------------- pages
def page_web(lang):
    en = lang == 'en'
    q = wa("Hi AsghinLabs, I'd like a website for my business. Can we talk about the price?" if en else
           "Bonjour AsghinLabs, je voudrais un site web pour mon entreprise. Pouvons-nous parler du prix ?")
    return dict(
        slug='/website-design-douala' if en else '/creation-site-web-douala',
        alt='/creation-site-web-douala' if en else '/website-design-douala',
        title='Website Design in Douala, Cameroon — from 75 000 FCFA | AsghinLabs' if en else
              'Création de site web à Douala, Cameroun — dès 75 000 FCFA | AsghinLabs',
        desc='Professional websites for businesses in Douala and across Cameroon: showcase sites, online shops with WhatsApp orders and web apps. Mobile-first, from 75 000 FCFA.' if en else
             'Création de sites web professionnels à Douala et partout au Cameroun : sites vitrines, boutiques en ligne avec commande WhatsApp, applications web. Adaptés au mobile, dès 75 000 FCFA.',
        crumb='Website design' if en else 'Création de site web',
        tag='✦ Website design · Douala ✦' if en else '✦ Création de site web · Douala ✦',
        h1='Websites that bring you customers' if en else 'Un site web qui vous apporte des clients',
        lead=('We design and build fast, mobile-first websites for businesses, schools, churches and NGOs in Douala and across Cameroon — with a WhatsApp button so visitors become customers.' if en else
              'Nous concevons des sites web rapides et adaptés au mobile pour les entreprises, écoles, églises et associations de Douala et de tout le Cameroun, avec un bouton WhatsApp pour transformer vos visiteurs en clients.'),
        price=('Websites from', '75 000 FCFA') if en else ('Sites web dès', '75 000 FCFA'),
        wa=q,
        hero_list=(['Designed for phones first — where your customers are', 'WhatsApp and call buttons on every page',
                    'Set up so Google can find you (SEO basics, Google Business Profile tips)', 'English, French or both',
                    'You own your domain name and your site'] if en else
                   ['Pensé d’abord pour le téléphone, là où sont vos clients', 'Boutons WhatsApp et appel sur chaque page',
                    'Préparé pour être trouvé sur Google (bases du référencement)', 'En français, en anglais ou les deux',
                    'Le nom de domaine et le site vous appartiennent']),
        body=[
            section('What we build' if en else 'Ce que nous créons', '', cards([
                ('🏪', 'Showcase website' if en else 'Site vitrine',
                 'Present your business, services, prices and location. The fastest way to look serious online.' if en else
                 'Présentez votre activité, vos services, vos prix et votre adresse. Le moyen le plus rapide d’être pris au sérieux en ligne.'),
                ('🛒', 'Online shop with WhatsApp orders' if en else 'Boutique en ligne avec commande WhatsApp',
                 'Product catalogue and a cart that sends the full order to your WhatsApp. No complicated payment setup needed.' if en else
                 'Un catalogue de produits et un panier qui envoie la commande complète sur votre WhatsApp. Pas besoin de paiement en ligne compliqué.'),
                ('🏫', 'Schools, churches &amp; NGOs' if en else 'Écoles, églises et associations',
                 'News, events, admissions, galleries and contact forms, easy for your team to keep up to date.' if en else
                 'Actualités, événements, inscriptions, galeries et formulaires de contact, faciles à mettre à jour.'),
                ('⚙️', 'Web apps &amp; booking systems' if en else 'Applications web et réservations',
                 'Bookings, client accounts, dashboards and records — built around how you already work.' if en else
                 'Réservations, comptes clients, tableaux de bord et fichiers : construits autour de votre façon de travailler.'),
            ])),
            section('Recent websites' if en else 'Quelques réalisations', 'Real projects you can open and test.' if en else 'Des projets réels que vous pouvez ouvrir et tester.', web_projects(lang), alt=True),
            section('Prices' if en else 'Tarifs', 'Clear prices agreed before we start — no surprises.' if en else 'Un prix clair, fixé avant de commencer, sans surprise.', plans([
                dict(name='Starter website' if en else 'Site vitrine simple', amount='75 000 FCFA', featured=True,
                     note='starting price' if en else 'prix de départ',
                     items=(['1 to 3 pages', 'Mobile-first design', 'WhatsApp, call and map buttons', 'Contact form', 'Basic Google setup'] if en else
                            ['1 à 3 pages', 'Design adapté au mobile', 'Boutons WhatsApp, appel et plan', 'Formulaire de contact', 'Configuration Google de base']),
                     cta='Order this' if en else 'Je veux ce site', wa=q),
                dict(name='Business website' if en else 'Site d’entreprise', amount='On quote' if en else 'Sur devis',
                     note='depends on pages and features' if en else 'selon les pages et fonctions',
                     items=(['More pages (services, gallery, team, blog…)', 'English and French versions', 'Content writing help', 'Search-friendly structure'] if en else
                            ['Plus de pages (services, galerie, équipe, blog…)', 'Version française et anglaise', 'Aide à la rédaction des textes', 'Structure optimisée pour Google']),
                     cta='Ask for a quote' if en else 'Demander un devis', wa=q),
                dict(name='Online shop / web app' if en else 'Boutique / application web', amount='On quote' if en else 'Sur devis',
                     note='after a short chat about your needs' if en else 'après un court échange sur vos besoins',
                     items=(['Product catalogue and cart', 'Orders sent to WhatsApp', 'Bookings, accounts or dashboards', 'Training to manage it yourself'] if en else
                            ['Catalogue de produits et panier', 'Commandes envoyées sur WhatsApp', 'Réservations, comptes ou tableaux de bord', 'Formation pour gérer vous-même']),
                     cta='Ask for a quote' if en else 'Demander un devis', wa=q),
            ], small=('The domain name (your .com or .cm address) is renewed every year and is billed separately at cost. '
                      'Read our guide: <a href="/website-cost-cameroon">How much does a website cost in Cameroon?</a>' if en else
                      'Le nom de domaine (votre adresse en .com ou .cm) se renouvelle chaque année et est facturé à part, au prix coûtant. '
                      'Lire notre guide : <a href="/combien-coute-un-site-web-cameroun">Combien coûte un site web au Cameroun ?</a>'))),
            section('How it works' if en else 'Comment ça se passe', '', steps([
                ('Tell us about your business' if en else 'Parlez-nous de votre activité', 'A short chat on WhatsApp or by phone about your goals and your budget.' if en else 'Un court échange sur WhatsApp ou par téléphone sur vos objectifs et votre budget.'),
                ('Get a clear price' if en else 'Recevez un prix clair', 'We agree on the pages, the features, the price and the delivery date.' if en else 'Nous fixons ensemble les pages, les fonctions, le prix et le délai.'),
                ('We design and build' if en else 'Nous concevons le site', 'You see the site as it grows and ask for changes before launch.' if en else 'Vous voyez le site avancer et demandez des modifications avant la mise en ligne.'),
                ('Launch and support' if en else 'Mise en ligne et suivi', 'We put it online, connect your domain, show you how to use it and stay available.' if en else 'Nous le mettons en ligne, branchons votre domaine, vous montrons comment l’utiliser et restons disponibles.'),
            ]), alt=True),
        ],
        faq=([('How much does a website cost in Cameroon?', 'Our websites start at 75 000 FCFA for a simple 1–3 page site. Bigger sites, online shops and web apps are priced after a short chat, and the price is agreed before work starts. Our <a href="/website-cost-cameroon">website cost guide</a> explains what changes the price.'),
              ('How long does it take?', 'It depends on the size of the site and how quickly we receive your texts and photos. We agree on a delivery date with you before we start.'),
              ('Do you only work in Douala?', 'No. We are based in Douala and work with clients anywhere in Cameroon and abroad, over WhatsApp, phone and video calls.'),
              ('Can customers order on WhatsApp from my website?', 'Yes. We add WhatsApp buttons, and for shops a cart that writes the full order and sends it to your WhatsApp.'),
              ('Will my website appear on Google?', 'We build every site so Google can read it: clear titles, descriptions, fast pages and a sitemap. We also guide you to set up your free Google Business Profile, which helps you appear on Google Maps.')] if en else
             [('Combien coûte un site web au Cameroun ?', 'Nos sites commencent à 75 000 FCFA pour un site simple de 1 à 3 pages. Les sites plus grands, boutiques en ligne et applications sont chiffrés après un court échange, et le prix est fixé avant de commencer. Notre <a href="/combien-coute-un-site-web-cameroun">guide des prix</a> explique ce qui fait varier le coût.'),
              ('Combien de temps faut-il ?', 'Cela dépend de la taille du site et de la rapidité avec laquelle nous recevons vos textes et photos. Nous fixons le délai avec vous avant de commencer.'),
              ('Travaillez-vous seulement à Douala ?', 'Non. Nous sommes basés à Douala et travaillons avec des clients partout au Cameroun et à l’étranger, par WhatsApp, téléphone et visioconférence.'),
              ('Mes clients peuvent-ils commander sur WhatsApp depuis le site ?', 'Oui. Nous ajoutons des boutons WhatsApp et, pour les boutiques, un panier qui rédige la commande complète et l’envoie sur votre WhatsApp.'),
              ('Mon site apparaîtra-t-il sur Google ?', 'Chaque site est construit pour être lu par Google : titres clairs, descriptions, pages rapides et sitemap. Nous vous guidons aussi pour créer votre fiche Google Business Profile gratuite, qui aide à apparaître sur Google Maps.')]),
        service=dict(name='Website design and development' if en else 'Création de site web', type='Web design',
                     offer=('75000', 'Starter website (1–3 pages)' if en else 'Site vitrine simple (1 à 3 pages)')),
        related=['flyers', 'logos', 'ai'],
    )


def page_flyers(lang):
    en = lang == 'en'
    q = wa("Hi AsghinLabs, I need a flyer / pamphlet design. Here is what it's for:" if en else
           "Bonjour AsghinLabs, j'ai besoin d'un flyer / dépliant. Voici à quoi il servira :")
    qp = wa("Hi AsghinLabs, I need flyers designed AND printed. Quantity and size:" if en else
            "Bonjour AsghinLabs, je veux des flyers conçus ET imprimés. Quantité et format :")
    return dict(
        slug='/flyer-design-douala' if en else '/conception-flyers-douala',
        alt='/conception-flyers-douala' if en else '/flyer-design-douala',
        title='Flyer, Pamphlet &amp; Poster Design in Douala — from 5 000 FCFA | AsghinLabs' if en else
              'Conception de flyers, dépliants et affiches à Douala — dès 5 000 FCFA | AsghinLabs',
        desc='Eye-catching flyers, pamphlets, posters, banners and business cards for businesses and events in Douala and Cameroon. Design from 5 000 FCFA, printing on request.' if en else
             'Flyers, dépliants, affiches, kakémonos et cartes de visite qui attirent l’œil, pour entreprises et événements à Douala et au Cameroun. Conception dès 5 000 FCFA, impression sur demande.',
        crumb='Flyer &amp; pamphlet design' if en else 'Flyers et dépliants',
        tag='✦ Flyers · Pamphlets · Posters ✦' if en else '✦ Flyers · Dépliants · Affiches ✦',
        h1='Flyers and pamphlets people actually read' if en else 'Des flyers et dépliants qu’on a envie de lire',
        lead=('Promotions, openings, events, church programmes, school admissions: we design print and social media visuals that make your offer clear in two seconds. Printing on request.' if en else
              'Promotions, ouvertures, événements, programmes d’église, inscriptions scolaires : nous concevons des visuels pour l’impression et les réseaux sociaux qui rendent votre offre claire en deux secondes. Impression sur demande.'),
        price=('Flyer design from', '5 000 FCFA') if en else ('Conception de flyer dès', '5 000 FCFA'),
        wa=q,
        hero_list=(['Print-ready files (A5, A4, DL and custom sizes)', 'Matching version for WhatsApp status, Facebook and Instagram',
                    'Your logo, colours and contact details', 'Printing arranged on request', 'Made with Photoshop, Illustrator, Figma and Canva'] if en else
                   ['Fichiers prêts pour l’impression (A5, A4, DL et formats sur mesure)', 'Version adaptée au statut WhatsApp, à Facebook et Instagram',
                    'Votre logo, vos couleurs et vos contacts', 'Impression organisée sur demande', 'Réalisés avec Photoshop, Illustrator, Figma et Canva']),
        body=[
            section('What we design' if en else 'Ce que nous concevons', '', cards([
                ('📄', 'Flyers' if en else 'Flyers', 'Promotions, new products, openings and events — one clear message, easy to share.' if en else 'Promotions, nouveaux produits, ouvertures et événements : un message clair, facile à partager.'),
                ('📑', 'Pamphlets &amp; brochures' if en else 'Dépliants et brochures', 'Folded leaflets that present your services, prices or programme in detail.' if en else 'Des dépliants pliés qui présentent en détail vos services, vos prix ou votre programme.'),
                ('🪧', 'Posters &amp; banners' if en else 'Affiches et kakémonos', 'Posters, roll-up banners and shop signs that are readable from far away.' if en else 'Affiches, roll-up et enseignes lisibles de loin.'),
                ('💳', 'Business cards' if en else 'Cartes de visite', 'Clean, professional cards that match your logo and colours.' if en else 'Des cartes nettes et professionnelles assorties à votre logo et à vos couleurs.'),
                ('📱', 'Social media posts' if en else 'Visuels réseaux sociaux', 'WhatsApp status, Facebook and Instagram posts and ad creatives.' if en else 'Statuts WhatsApp, publications Facebook et Instagram, visuels publicitaires.'),
                ('⛪', 'Programmes &amp; menus' if en else 'Programmes et menus', 'Church and event programmes, restaurant menus, price lists.' if en else 'Programmes d’église et d’événements, menus de restaurant, listes de prix.'),
            ])),
            section('Flyers we have designed' if en else 'Quelques flyers réalisés', 'Real work for businesses in Douala and Cameroon.' if en else 'Des réalisations pour des entreprises de Douala et du Cameroun.',
                    gallery(FLYERS) + '<p class="svc-small"><a href="/portfolio" style="color:var(--brand-primary)">' + ('See the full portfolio →' if en else 'Voir tout le portfolio →') + '</a></p>', alt=True),
            section('Banners' if en else 'Bannières', '', gallery(BANNERS, 'wide')),
            section('Prices' if en else 'Tarifs', 'The design price is agreed before we start.' if en else 'Le prix de la conception est fixé avant de commencer.', plans([
                dict(name='Flyer design' if en else 'Conception de flyer', amount='5 000 FCFA', featured=True, note='starting price, one side' if en else 'prix de départ, recto',
                     items=(['Print-ready file (PDF / high quality)', 'Social media version', 'Your logo and contacts'] if en else
                            ['Fichier prêt à imprimer (PDF / haute qualité)', 'Version réseaux sociaux', 'Votre logo et vos contacts']),
                     cta='Order a flyer' if en else 'Commander un flyer', wa=q),
                dict(name='Pamphlets, posters &amp; banners' if en else 'Dépliants, affiches et kakémonos', amount='On quote' if en else 'Sur devis',
                     note='depends on size and number of pages' if en else 'selon le format et le nombre de pages',
                     items=(['Folded pamphlets and brochures', 'Posters and roll-up banners', 'Business cards and menus'] if en else
                            ['Dépliants et brochures', 'Affiches et roll-up', 'Cartes de visite et menus']),
                     cta='Ask for a quote' if en else 'Demander un devis', wa=q),
                dict(name='Design + printing' if en else 'Conception + impression', amount='On quote' if en else 'Sur devis',
                     note='printing on request' if en else 'impression sur demande',
                     items=(['Tell us the quantity, size and paper', 'We arrange the printing for you', 'Printing is quoted separately from the design'] if en else
                            ['Indiquez la quantité, le format et le papier', 'Nous organisons l’impression pour vous', 'L’impression est chiffrée à part de la conception']),
                     cta='Design + print' if en else 'Conception + impression', wa=qp),
            ])),
            section('How it works' if en else 'Comment ça se passe', '', steps([
                ('Send your details' if en else 'Envoyez vos informations', 'What it is for, your text, logo, photos and the size you need.' if en else 'À quoi il sert, vos textes, logo, photos et le format souhaité.'),
                ('Agree the price' if en else 'Validez le prix', 'We confirm the price and when you will get the first design.' if en else 'Nous confirmons le prix et la date du premier visuel.'),
                ('Review the design' if en else 'Relisez le visuel', 'You check it on your phone and ask for changes.' if en else 'Vous le vérifiez sur votre téléphone et demandez des modifications.'),
                ('Get your files — or prints' if en else 'Recevez vos fichiers ou vos impressions', 'Print-ready and social media files, or printed copies if you asked for printing.' if en else 'Fichiers prêts à imprimer et pour les réseaux, ou exemplaires imprimés si vous avez choisi l’impression.'),
            ]), alt=True),
        ],
        faq=([('How much does a flyer design cost?', 'Flyer design starts at 5 000 FCFA. Pamphlets, posters, banners and bigger jobs are priced after we see what you need, and the price is agreed before we start.'),
              ('Do you print the flyers too?', 'Yes, on request. Tell us the quantity, size and paper, and we arrange the printing. Printing is quoted separately from the design.'),
              ('What do I need to send?', 'The purpose of the flyer, the text (or the main points), your logo, any photos and your contact details. If you have no logo yet, we can design one.'),
              ('Can I use the same design on WhatsApp and Facebook?', 'Yes. We give you a version sized for WhatsApp status and social media as well as the print file.')] if en else
             [('Combien coûte la conception d’un flyer ?', 'La conception d’un flyer commence à 5 000 FCFA. Les dépliants, affiches, kakémonos et travaux plus importants sont chiffrés après avoir vu votre besoin, et le prix est fixé avant de commencer.'),
              ('Imprimez-vous aussi les flyers ?', 'Oui, sur demande. Indiquez la quantité, le format et le papier, et nous organisons l’impression. L’impression est chiffrée à part de la conception.'),
              ('Que dois-je envoyer ?', 'L’objectif du flyer, le texte (ou les points principaux), votre logo, vos photos et vos contacts. Si vous n’avez pas encore de logo, nous pouvons le créer.'),
              ('Puis-je utiliser le même visuel sur WhatsApp et Facebook ?', 'Oui. Nous vous remettons une version adaptée au statut WhatsApp et aux réseaux sociaux en plus du fichier d’impression.')]),
        service=dict(name='Flyer, pamphlet and poster design' if en else 'Conception de flyers, dépliants et affiches', type='Graphic design',
                     offer=('5000', 'Flyer design' if en else 'Conception de flyer')),
        related=['web', 'logos', 'ai'],
    )


def page_logos(lang):
    en = lang == 'en'
    q = wa("Hi AsghinLabs, I need a logo for my business. My business is:" if en else
           "Bonjour AsghinLabs, j'ai besoin d'un logo pour mon entreprise. Mon activité :")
    return dict(
        slug='/logo-design-douala' if en else '/creation-logo-douala',
        alt='/creation-logo-douala' if en else '/logo-design-douala',
        title='Logo Design &amp; Brand Identity in Douala, Cameroon | AsghinLabs' if en else
              'Création de logo et identité visuelle à Douala, Cameroun | AsghinLabs',
        desc='Logos and brand identities for businesses in Douala and Cameroon: logo, colours, fonts, business cards and social media kit. Get a quote on WhatsApp.' if en else
             'Création de logos et d’identités visuelles pour entreprises à Douala et au Cameroun : logo, couleurs, polices, cartes de visite et kit réseaux sociaux. Devis sur WhatsApp.',
        crumb='Logo design' if en else 'Création de logo',
        tag='✦ Logos · Brand identity ✦' if en else '✦ Logos · Identité visuelle ✦',
        h1='A logo that makes your business look established' if en else 'Un logo qui donne à votre entreprise une image sérieuse',
        lead=('From a simple logo to a full brand kit — colours, fonts, business cards and social media templates — so everything you print and post looks like the same business.' if en else
              'D’un simple logo à une identité complète (couleurs, polices, cartes de visite, modèles pour les réseaux sociaux), pour que tout ce que vous imprimez et publiez ait la même image.'),
        price=None, wa=q,
        hero_list=(['Several first ideas to choose from', 'Files for print, web and social media (PNG, PDF, SVG)',
                    'Colour palette and fonts you can reuse', 'Business card and social media versions'] if en else
                   ['Plusieurs premières pistes au choix', 'Fichiers pour l’impression, le web et les réseaux (PNG, PDF, SVG)',
                    'Palette de couleurs et polices réutilisables', 'Versions carte de visite et réseaux sociaux']),
        body=[
            section('Logos we have designed' if en else 'Quelques logos réalisés', '', gallery(LOGOS, 'logos') +
                    '<p class="svc-small"><a href="/portfolio?group=brand" style="color:var(--brand-primary)">' + ('See all brand work →' if en else 'Voir toutes nos identités visuelles →') + '</a></p>'),
            section('What you get' if en else 'Ce que vous recevez', '', cards([
                ('✏️', 'Logo' if en else 'Logo', 'Main logo, a simple icon version and black / white versions.' if en else 'Logo principal, version icône simplifiée et versions noir / blanc.'),
                ('🎨', 'Colours &amp; fonts' if en else 'Couleurs et polices', 'A small guide so your flyers, shop and website stay consistent.' if en else 'Un petit guide pour que vos flyers, votre boutique et votre site restent cohérents.'),
                ('💳', 'Business cards' if en else 'Cartes de visite', 'Ready to print, matching your new identity.' if en else 'Prêtes à imprimer, assorties à votre nouvelle identité.'),
                ('📱', 'Social media kit' if en else 'Kit réseaux sociaux', 'Profile picture, cover images and post templates.' if en else 'Photo de profil, images de couverture et modèles de publications.'),
            ]), alt=True),
            section('How it works' if en else 'Comment ça se passe', '', steps([
                ('Tell us about your business' if en else 'Présentez votre activité', 'Your name, what you sell, who your customers are and styles you like.' if en else 'Votre nom, ce que vous vendez, vos clients et les styles que vous aimez.'),
                ('Get a price' if en else 'Recevez un prix', 'We quote the logo or the full brand kit before starting.' if en else 'Nous chiffrons le logo ou l’identité complète avant de commencer.'),
                ('Choose and refine' if en else 'Choisissez et affinez', 'Pick your favourite idea and we refine it with you.' if en else 'Choisissez votre piste préférée, nous l’affinons avec vous.'),
                ('Receive all files' if en else 'Recevez tous les fichiers', 'Print, web and social media files, ready to use.' if en else 'Fichiers pour l’impression, le web et les réseaux, prêts à l’emploi.'),
            ])),
        ],
        faq=([('How much does a logo cost?', 'It depends on whether you need a logo only or a full brand kit. Message us on WhatsApp with a few details and we send a clear price before starting.'),
              ('Will I own my logo?', 'Yes. Once the work is paid, the logo and all its files are yours.'),
              ('Can you also design my flyers and website?', 'Yes — that is where a consistent brand pays off. See our <a href="/flyer-design-douala">flyer design</a> and <a href="/website-design-douala">website design</a> services.')] if en else
             [('Combien coûte un logo ?', 'Cela dépend si vous voulez seulement un logo ou une identité complète. Écrivez-nous sur WhatsApp avec quelques détails et nous envoyons un prix clair avant de commencer.'),
              ('Le logo m’appartiendra-t-il ?', 'Oui. Une fois le travail payé, le logo et tous ses fichiers sont à vous.'),
              ('Pouvez-vous aussi créer mes flyers et mon site ?', 'Oui, c’est là qu’une image cohérente fait la différence. Voir nos services de <a href="/conception-flyers-douala">conception de flyers</a> et de <a href="/creation-site-web-douala">création de site web</a>.')]),
        service=dict(name='Logo and brand identity design' if en else 'Création de logo et identité visuelle', type='Logo design', offer=None),
        related=['flyers', 'web', 'ai'],
    )


def page_ai(lang):
    en = lang == 'en'
    q = wa("Hi AsghinLabs, I'd like to automate part of my business. Here is what takes us time:" if en else
           "Bonjour AsghinLabs, je voudrais automatiser une partie de mon activité. Voici ce qui nous prend du temps :")
    return dict(
        slug='/ai-automation-cameroon' if en else '/automatisation-ia-cameroun',
        alt='/automatisation-ia-cameroun' if en else '/ai-automation-cameroon',
        title='AI &amp; Automation for Businesses in Cameroon | AsghinLabs' if en else
              'Automatisation et intelligence artificielle pour entreprises au Cameroun | AsghinLabs',
        desc='AI assistants, WhatsApp order automation, automated reports and custom tools that save your team hours every week. Built in Douala for businesses across Cameroon.' if en else
             'Assistants IA, automatisation des commandes WhatsApp, rapports automatiques et outils sur mesure qui font gagner des heures à votre équipe. Conçus à Douala pour les entreprises du Cameroun.',
        crumb='AI &amp; automation' if en else 'Automatisation IA',
        tag='✦ AI · Automation ✦' if en else '✦ IA · Automatisation ✦',
        h1='Let software do the repetitive work' if en else 'Laissez le logiciel faire le travail répétitif',
        lead=('Answering the same questions, copying orders, preparing reports by hand: we build AI assistants and automations that do it for you, so your team can focus on customers.' if en else
              'Répondre toujours aux mêmes questions, recopier les commandes, préparer les rapports à la main : nous créons des assistants IA et des automatisations qui le font pour vous, pour que votre équipe se concentre sur les clients.'),
        price=None, wa=q,
        hero_list=(['Starts from a real problem in your business', 'Works with the tools you already use (WhatsApp, Google Sheets, email)',
                    'Clear price agreed before we start', 'We show your team how to use it'] if en else
                   ['On part d’un vrai problème de votre activité', 'Fonctionne avec vos outils (WhatsApp, Google Sheets, e-mail)',
                    'Prix clair fixé avant de commencer', 'Nous formons votre équipe à l’utiliser']),
        body=[
            section('What we can automate' if en else 'Ce que nous pouvons automatiser', '', cards([
                ('💬', 'Customer questions' if en else 'Questions des clients', 'An assistant that answers common questions about prices, opening hours and delivery, day and night.' if en else 'Un assistant qui répond aux questions fréquentes sur les prix, les horaires et la livraison, jour et nuit.'),
                ('🛒', 'WhatsApp orders' if en else 'Commandes WhatsApp', 'Orders collected and organised automatically instead of copied by hand.' if en else 'Des commandes collectées et organisées automatiquement au lieu d’être recopiées à la main.'),
                ('📊', 'Reports &amp; data' if en else 'Rapports et données', 'Daily or weekly sales, stock or school results reports prepared for you.' if en else 'Rapports quotidiens ou hebdomadaires de ventes, de stock ou de résultats scolaires préparés pour vous.'),
                ('📄', 'Documents' if en else 'Documents', 'Invoices, receipts, certificates and letters generated from your data.' if en else 'Factures, reçus, attestations et courriers générés à partir de vos données.'),
            ])),
            section('Built in-house' if en else 'Déjà réalisé chez nous', '', cards([
                ('🎓', 'AI Tutor — AsghinLabs Academy' if en else 'Tuteur IA — AsghinLabs Academy',
                 'A free AI tutor used by Cameroon GCE students: questions, explanations of uploaded notes and live classes on a virtual board.' if en else
                 'Un tuteur IA gratuit utilisé par les élèves du GCE : questions, explications de cours envoyés en photo et classes en direct sur un tableau virtuel.',
                 '/tutor', 'Try it →' if en else 'L’essayer →'),
                ('🎮', '450+ interactive lessons' if en else 'Plus de 450 leçons interactives',
                 'Lessons with instant correction and a feedback dashboard, generated automatically from the school progression sheets.' if en else
                 'Des leçons avec correction immédiate et un tableau de bord des retours, générées automatiquement à partir des progressions officielles.',
                 '/lessons', 'Browse the lessons →' if en else 'Voir les leçons →'),
                ('🤖', 'StoreBot (in development)' if en else 'StoreBot (en développement)',
                 'An AI assistant that takes orders on WhatsApp for a shop and checks them before they reach the seller.' if en else
                 'Un assistant IA qui prend les commandes sur WhatsApp pour une boutique et les vérifie avant de les transmettre au vendeur.'),
            ]), alt=True),
            section('How it works' if en else 'Comment ça se passe', '', steps([
                ('Show us the problem' if en else 'Montrez-nous le problème', 'What takes your team the most time every week?' if en else 'Qu’est-ce qui prend le plus de temps à votre équipe chaque semaine ?'),
                ('Small first version' if en else 'Une première version simple', 'We agree on a small, useful first step and its price.' if en else 'Nous fixons une première étape simple et utile, et son prix.'),
                ('Test with your team' if en else 'Test avec votre équipe', 'You use it for real and we adjust it.' if en else 'Vous l’utilisez réellement et nous l’ajustons.'),
                ('Grow it' if en else 'On l’améliore', 'Add more automations once the first one pays off.' if en else 'On ajoute d’autres automatisations une fois la première rentable.'),
            ])),
        ],
        faq=([('Is AI expensive for a small business?', 'Not necessarily. We start with one small automation that saves time quickly, priced before we start, and grow from there only if it is worth it.'),
              ('Do I need new software or computers?', 'Usually not. We connect to what you already use: WhatsApp, Google Sheets, email or your website.')] if en else
             [('L’IA coûte-t-elle cher pour une petite entreprise ?', 'Pas forcément. Nous commençons par une petite automatisation qui fait vite gagner du temps, avec un prix fixé avant de commencer, puis on l’étend seulement si cela vaut la peine.'),
              ('Faut-il de nouveaux logiciels ou ordinateurs ?', 'En général non. Nous nous connectons à ce que vous utilisez déjà : WhatsApp, Google Sheets, e-mail ou votre site web.')]),
        service=dict(name='AI and business automation' if en else 'Automatisation et intelligence artificielle', type='Business automation', offer=None),
        related=['web', 'flyers', 'logos'],
    )


RELATED = {
    'en': {'web': ('🌐', 'Website design', 'Showcase sites, online shops and web apps from 75 000 FCFA.', '/website-design-douala'),
           'flyers': ('📄', 'Flyers &amp; pamphlets', 'Flyers, pamphlets, posters and banners. Design from 5 000 FCFA, printing on request.', '/flyer-design-douala'),
           'logos': ('✏️', 'Logo design', 'Logos and brand identity kits.', '/logo-design-douala'),
           'ai': ('🤖', 'AI &amp; automation', 'AI assistants and automations that save your team time.', '/ai-automation-cameroon')},
    'fr': {'web': ('🌐', 'Création de site web', 'Sites vitrines, boutiques en ligne et applications dès 75 000 FCFA.', '/creation-site-web-douala'),
           'flyers': ('📄', 'Flyers et dépliants', 'Flyers, dépliants, affiches et kakémonos. Conception dès 5 000 FCFA, impression sur demande.', '/conception-flyers-douala'),
           'logos': ('✏️', 'Création de logo', 'Logos et identités visuelles.', '/creation-logo-douala'),
           'ai': ('🤖', 'Automatisation IA', 'Assistants IA et automatisations qui font gagner du temps.', '/automatisation-ia-cameroun')},
}


def page_fr_home():
    q = wa("Bonjour AsghinLabs, je voudrais parler d'un projet.")
    return dict(
        slug='/fr', alt='/', kind='home',
        title='AsghinLabs — Création de sites web, logiciels et design à Douala, Cameroun' ,
        desc='Studio de développement web et logiciel à Douala : création de sites web dès 75 000 FCFA, boutiques en ligne, applications, automatisation IA, flyers et logos. Devis sur WhatsApp.',
        crumb=None,
        tag='✦ Web ✦ Logiciels ✦ IA ✦ Design ✦',
        h1='Des solutions numériques qui font avancer votre activité',
        lead='AsghinLabs est un studio de développement web et logiciel basé à Douala. Nous créons des sites web, des applications, des automatisations IA et les visuels (flyers, logos) qui aident les entreprises et les organisations du Cameroun à trouver des clients et à mieux travailler.',
        price=('Sites web dès', '75 000 FCFA'), wa=q,
        hero_list=['Vous travaillez directement avec le développeur', 'Basés à Douala, clients partout au Cameroun et à l’étranger',
                   'Réponse sous 24 heures', 'Français et anglais'],
        body=[
            section('Nos services', 'Cliquez sur un service pour voir les détails, les réalisations et les prix.', cards([
                ('🌐', 'Création de site web', 'Sites vitrines, boutiques en ligne avec commande WhatsApp, sites d’écoles et d’associations. Dès 75 000 FCFA.', '/creation-site-web-douala', 'Voir les détails →'),
                ('📄', 'Flyers, dépliants et affiches', 'Visuels pour l’impression et les réseaux sociaux. Conception dès 5 000 FCFA, impression sur demande.', '/conception-flyers-douala', 'Voir les détails →'),
                ('✏️', 'Logos et identité visuelle', 'Un logo et une image cohérente pour tout ce que vous imprimez et publiez.', '/creation-logo-douala', 'Voir les détails →'),
                ('🤖', 'Automatisation et IA', 'Assistants IA, commandes WhatsApp automatisées, rapports et documents générés automatiquement.', '/automatisation-ia-cameroun', 'Voir les détails →'),
                ('🧩', 'Logiciels sur mesure', 'Gestion de stock, réservations, suivi clients, résultats scolaires : un outil construit autour de votre façon de travailler.', wa("Bonjour AsghinLabs, je voudrais un logiciel sur mesure pour :"), 'En parler sur WhatsApp →'),
                ('🎓', 'Formations', 'Bases de l’informatique, création de sites web, IA au travail : en petits groupes, à Douala ou en ligne.', '/formations', 'Voir les formations →'),
            ]), sid='services'),
            section('Quelques réalisations', 'Des projets réels que vous pouvez ouvrir et tester.', web_projects('fr'), alt=True),
            section('Pourquoi AsghinLabs', '', cards([
                ('🎯', 'Des solutions pratiques', 'Nous partons de votre problème réel, pas d’une technologie à la mode.'),
                ('🤝', 'Contact direct', 'Vous parlez à la personne qui construit votre projet, sur WhatsApp ou au téléphone.'),
                ('💰', 'Prix clair', 'Le prix et le délai sont fixés avant de commencer.'),
                ('⚡', 'Technologies modernes', 'Des sites rapides, adaptés au mobile et préparés pour Google.'),
            ])),
            section('AsghinLabs Academy', 'Notre branche éducation pour les élèves et les enseignants.', cards([
                ('🎮', 'Leçons interactives', 'Plus de 450 leçons gratuites en informatique et mathématiques, de la 6e à la Terminale et de la Form 1 à l’Upper Sixth.', '/lecons', 'Voir les leçons →'),
                ('📝', 'Épreuves officielles', 'BEPC, Probatoire, Bac, GCE : les épreuves classées par année et par matière.', '/epreuves', 'Voir les épreuves →'),
                ('📚', 'Cahiers et fascicules', 'Cahiers d’exercices et notes de cours complètes pour l’A Level, avec extraits gratuits.', '/academy#workbooks', 'Voir la boutique →'),
            ]), alt=True),
        ],
        faq=[('Combien coûte un site web ?', 'Nos sites commencent à 75 000 FCFA pour un site simple de 1 à 3 pages. Les projets plus importants sont chiffrés après un court échange. Lire notre <a href="/combien-coute-un-site-web-cameroun">guide des prix d’un site web au Cameroun</a>.'),
             ('Travaillez-vous avec des clients hors de Douala ?', 'Oui. Nous travaillons à distance avec des clients partout au Cameroun et à l’étranger.'),
             ('Que se passe-t-il après la mise en ligne ?', 'Nous testons, mettons en ligne, vous montrons comment utiliser votre site ou votre outil, et proposons un suivi et des améliorations si vous le souhaitez.')],
        service=None, related=[],
    )


def page_guide(lang):
    en = lang == 'en'
    q = wa("Hi AsghinLabs, I read your guide on website prices. I'd like a quote for:" if en else
           "Bonjour AsghinLabs, j'ai lu votre guide sur le prix d'un site web. Je voudrais un devis pour :")
    if en:
        art = f'''
<p class="meta">Updated October 2026 · by Ayemelong Selobie Ghislain, founder of AsghinLabs</p>
<p>“How much is a website?” is the first question most business owners in Douala ask us. The honest answer is: it depends on what the site must do. This guide explains what changes the price, what you pay once and what you pay every year, and how to avoid paying for a site you cannot use.</p>

<h2>Our prices in short</h2>
<div class="svc-table-wrap"><table>
<tr><th>Type of website</th><th>AsghinLabs price</th></tr>
<tr><td>Simple showcase site (1–3 pages)</td><td>from 75 000 FCFA</td></tr>
<tr><td>Larger business site, bilingual site</td><td>on quote</td></tr>
<tr><td>Online shop with WhatsApp orders</td><td>on quote</td></tr>
<tr><td>Web app, booking or management system</td><td>on quote</td></tr>
</table></div>
<p>Every quote is agreed before work starts. Message us on <a href="{q}" target="_blank" rel="noopener">WhatsApp</a> with what you need.</p>

<h2>What changes the price of a website</h2>
<h3>1. The number of pages</h3>
<p>A one-page site with your services and contacts is quick to build. Ten pages with a gallery, team, blog and service pages takes more design and more writing.</p>
<h3>2. What the site must do</h3>
<p>Showing information is the cheapest. Taking orders, bookings, client accounts or payments means more development and more testing.</p>
<h3>3. Languages</h3>
<p>In Cameroon many businesses need English and French. A bilingual site is almost two sites of content.</p>
<h3>4. Who writes the content</h3>
<p>If you send clear texts and good photos, the work goes faster. If you need help writing or taking photos, budget for it.</p>
<h3>5. Custom design or template</h3>
<p>A design made for your brand costs more than a ready-made template, but it looks like you and loads faster.</p>

<h2>One-time costs and yearly costs</h2>
<ul>
<li><strong>Design and building</strong> — paid once.</li>
<li><strong>Domain name</strong> (yourbusiness.com or .cm) — renewed every year. Make sure it is registered in <strong>your</strong> name.</li>
<li><strong>Hosting</strong> — where the site lives. Simple, fast sites can be hosted at low cost; shops and apps with a database cost more.</li>
<li><strong>Maintenance</strong> — optional updates, new products, changes and support.</li>
</ul>

<h2>Five questions to ask before you pay anyone</h2>
<ol>
<li>Will the domain name be in my name, with my login?</li>
<li>Can I see websites you have built and open them on my phone?</li>
<li>Does the price include mobile design, a contact form and WhatsApp buttons?</li>
<li>What will I pay every year after the first year?</li>
<li>Who do I call if something breaks?</li>
</ol>

<h2>Is a Facebook page enough?</h2>
<p>A Facebook page is a good start, but you do not control it and it does not appear well on Google. A website gives you an address you own, shows up when people search for your service in Douala, and makes you look established. The best results come from using both, plus a free Google Business Profile.</p>

<h2>Want a clear price for your website?</h2>
<p>Tell us about your business and what the site should do. We reply within 24 hours with questions and a price. See examples on our <a href="/website-design-douala">website design page</a>.</p>
'''
    else:
        art = f'''
<p class="meta">Mis à jour en octobre 2026 · par Ayemelong Selobie Ghislain, fondateur d’AsghinLabs</p>
<p>« Combien coûte un site web ? » C’est la première question que nous posent la plupart des chefs d’entreprise à Douala. La réponse honnête : cela dépend de ce que le site doit faire. Ce guide explique ce qui fait varier le prix, ce que vous payez une seule fois et chaque année, et comment éviter de payer pour un site inutilisable.</p>

<h2>Nos prix en bref</h2>
<div class="svc-table-wrap"><table>
<tr><th>Type de site</th><th>Prix AsghinLabs</th></tr>
<tr><td>Site vitrine simple (1 à 3 pages)</td><td>dès 75 000 FCFA</td></tr>
<tr><td>Site d’entreprise plus complet, site bilingue</td><td>sur devis</td></tr>
<tr><td>Boutique en ligne avec commande WhatsApp</td><td>sur devis</td></tr>
<tr><td>Application web, réservations, gestion</td><td>sur devis</td></tr>
</table></div>
<p>Chaque devis est validé avant de commencer. Écrivez-nous sur <a href="{q}" target="_blank" rel="noopener">WhatsApp</a> en décrivant votre besoin.</p>

<h2>Ce qui fait varier le prix d’un site web</h2>
<h3>1. Le nombre de pages</h3>
<p>Un site d’une page avec vos services et vos contacts se réalise vite. Dix pages avec galerie, équipe, blog et pages de services demandent plus de design et de rédaction.</p>
<h3>2. Ce que le site doit faire</h3>
<p>Présenter des informations coûte le moins cher. Prendre des commandes, des réservations, gérer des comptes clients ou des paiements demande plus de développement et de tests.</p>
<h3>3. Les langues</h3>
<p>Au Cameroun, beaucoup d’entreprises ont besoin du français et de l’anglais. Un site bilingue représente presque deux fois plus de contenu.</p>
<h3>4. Qui rédige les textes</h3>
<p>Si vous envoyez des textes clairs et de bonnes photos, le travail avance plus vite. Si vous avez besoin d’aide pour écrire ou photographier, prévoyez-le dans le budget.</p>
<h3>5. Design sur mesure ou modèle</h3>
<p>Un design créé pour votre marque coûte plus qu’un modèle tout fait, mais il vous ressemble et se charge plus vite.</p>

<h2>Coûts uniques et coûts annuels</h2>
<ul>
<li><strong>Conception et réalisation</strong> : payées une seule fois.</li>
<li><strong>Nom de domaine</strong> (votreentreprise.com ou .cm) : à renouveler chaque année. Vérifiez qu’il est enregistré à <strong>votre</strong> nom.</li>
<li><strong>Hébergement</strong> : l’endroit où vit le site. Un site simple et rapide peut être hébergé à faible coût ; une boutique ou une application avec base de données coûte plus.</li>
<li><strong>Maintenance</strong> : mises à jour, nouveaux produits, modifications et assistance, en option.</li>
</ul>

<h2>Cinq questions à poser avant de payer qui que ce soit</h2>
<ol>
<li>Le nom de domaine sera-t-il à mon nom, avec mes accès ?</li>
<li>Puis-je voir des sites que vous avez réalisés et les ouvrir sur mon téléphone ?</li>
<li>Le prix comprend-il l’adaptation au mobile, un formulaire de contact et les boutons WhatsApp ?</li>
<li>Combien vais-je payer chaque année après la première année ?</li>
<li>Qui dois-je appeler en cas de problème ?</li>
</ol>

<h2>Une page Facebook suffit-elle ?</h2>
<p>Une page Facebook est un bon début, mais vous ne la contrôlez pas et elle ressort mal sur Google. Un site web vous donne une adresse qui vous appartient, apparaît quand on cherche votre service à Douala et vous donne une image sérieuse. Le mieux est d’utiliser les deux, avec une fiche Google Business Profile gratuite.</p>

<h2>Vous voulez un prix clair pour votre site ?</h2>
<p>Présentez-nous votre activité et ce que le site doit faire. Nous répondons sous 24 heures avec nos questions et un prix. Voir des exemples sur notre page <a href="/creation-site-web-douala">création de site web</a>.</p>
'''
    return dict(
        slug='/website-cost-cameroon' if en else '/combien-coute-un-site-web-cameroun',
        alt='/combien-coute-un-site-web-cameroun' if en else '/website-cost-cameroon', kind='article',
        title='How Much Does a Website Cost in Cameroon? (2026 Guide) | AsghinLabs' if en else
              'Combien coûte un site web au Cameroun ? (Guide 2026) | AsghinLabs',
        desc='What changes the price of a website in Cameroon, one-time and yearly costs, and five questions to ask before paying a web designer. Websites from 75 000 FCFA in Douala.' if en else
             'Ce qui fait varier le prix d’un site web au Cameroun, les coûts uniques et annuels, et cinq questions à poser avant de payer un développeur. Sites web dès 75 000 FCFA à Douala.',
        crumb='Website cost guide' if en else 'Prix d’un site web',
        tag='✦ Guide ✦',
        h1='How much does a website cost in Cameroon?' if en else 'Combien coûte un site web au Cameroun ?',
        lead=None, price=None, wa=q, hero_list=None, article=art,
        faq=None, service=None, related=['web', 'flyers', 'logos'],
    )


PAGES = [page_web('en'), page_web('fr'), page_flyers('en'), page_flyers('fr'), page_logos('en'), page_logos('fr'),
         page_ai('en'), page_ai('fr'), page_fr_home(), page_guide('en'), page_guide('fr')]


# --------------------------------------------------------------- render
def lang_of(p):
    return 'en' if p['slug'] in ('/website-design-douala', '/flyer-design-douala', '/logo-design-douala',
                                 '/ai-automation-cameroon', '/website-cost-cameroon') else 'fr'


def jsonld(p, lang):
    url = SITE + p['slug']
    org = {"@id": SITE + "/#organization", "@type": "ProfessionalService", "name": "AsghinLabs", "url": SITE + "/",
           "telephone": "+237682402876", "email": EMAIL,
           "address": {"@type": "PostalAddress", "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM"}}
    graph = []
    home = T[lang]['home']
    crumbs = [{"@type": "ListItem", "position": 1, "name": home[1], "item": SITE + (home[0] if home[0] != '/' else '/')}]
    if p.get('crumb'):
        crumbs.append({"@type": "ListItem", "position": 2, "name": strip_tags(p['crumb']).replace('&amp;', '&'), "item": url})
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if p.get('service'):
        s = p['service']
        node = {"@type": "Service", "name": s['name'], "serviceType": s['type'], "provider": org,
                "areaServed": [{"@type": "City", "name": "Douala"}, {"@type": "Country", "name": "Cameroon"}],
                "url": url, "inLanguage": lang, "description": strip_tags(p['desc']).replace('&amp;', '&')}
        if s.get('offer'):
            node["offers"] = {"@type": "Offer", "price": s['offer'][0], "priceCurrency": "XAF", "name": s['offer'][1],
                              "url": url, "priceSpecification": {"@type": "PriceSpecification", "minPrice": s['offer'][0], "priceCurrency": "XAF"}}
        graph.append(node)
    if p.get('kind') == 'home':
        org2 = dict(org); org2['@type'] = ['Organization', 'ProfessionalService']
        org2['description'] = strip_tags(p['desc'])
        org2['knowsLanguage'] = ['fr', 'en']
        graph.append(org2)
    if p.get('kind') == 'article':
        graph.append({"@type": "Article", "headline": p['h1'], "inLanguage": lang, "datePublished": TODAY, "dateModified": TODAY,
                      "author": {"@type": "Person", "name": "Ayemelong Selobie Ghislain", "url": SITE + "/founder"},
                      "publisher": {"@id": SITE + "/#organization", "name": "AsghinLabs"},
                      "image": SITE + "/images/og-cover.jpg", "mainEntityOfPage": url})
    if p.get('faq'):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p['faq']]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def render(p):
    lang = lang_of(p)
    t = T[lang]
    url = SITE + p['slug']
    alt_lang = 'fr' if lang == 'en' else 'en'
    en_url = url if lang == 'en' else SITE + p['alt']
    fr_url = url if lang == 'fr' else SITE + p['alt']
    if en_url == SITE + '/':
        en_url = SITE + '/'
    title_plain = p['title']
    cur = ' aria-current="page"'
    nav = ''.join(f'<li><a href="{h}"{cur if h == p["slug"] else ""}>{n}</a></li>' for h, n in t['nav'])
    nav += f'<li><a href="{t["academy"][0]}" class="nav-cta">{t["academy"][1]}</a></li>'
    nav += f'<li><a href="{p["alt"]}" class="nav-lang" hreflang="{alt_lang}" lang="{alt_lang}" title="{t["lang_title"]}">{t["lang_label"]}</a></li>'

    crumbs = ''
    if p.get('crumb'):
        crumbs = f'<p class="svc-crumbs"><a href="{t["home"][0]}">{t["home"][1]}</a> › {p["crumb"]}</p>'

    if p.get('kind') == 'article':
        hero = f'''<section class="svc-hero" style="grid-template-columns:1fr;padding-bottom:20px">
  <div>{crumbs}<span class="tag">{p["tag"]}</span><h1>{p["h1"]}</h1></div>
</section>
<div class="svc-section" style="padding-top:0"><article class="svc-article">{p["article"]}
<div class="svc-actions"><a class="svc-btn wa" href="{p["wa"]}" target="_blank" rel="noopener">{t["cta_wa"]}</a></div>
</article></div>'''
    else:
        price = ''
        if p.get('price'):
            price = f'<div class="svc-price"><span>{p["price"][0]}</span><strong>{p["price"][1]}</strong></div>'
        lis = ''.join(f'<li>{x}</li>' for x in p['hero_list'])
        card_title = 'Included' if lang == 'en' else 'Inclus'
        if p.get('kind') == 'home':
            card_title = 'Pourquoi nous choisir'
        second = ('See our work' if lang == 'en' else 'Voir nos réalisations')
        hero = f'''<section class="svc-hero">
  <div>
    {crumbs}<span class="tag">{p["tag"]}</span>
    <h1>{p["h1"]}</h1>
    <p class="lead">{p["lead"]}</p>
    {price}
    <div class="svc-actions">
      <a class="svc-btn wa" href="{p["wa"]}" target="_blank" rel="noopener">{t["cta_wa"]}</a>
      <a class="svc-btn ghost" href="/portfolio">{second}</a>
    </div>
  </div>
  <aside class="svc-hero-card"><h2>{card_title}</h2><ul class="svc-check">{lis}</ul></aside>
</section>'''

    body = '\n'.join(p.get('body', []))
    faq = ''
    if p.get('faq'):
        faq = section('Frequently asked questions' if lang == 'en' else 'Questions fréquentes', '', faq_html(p['faq']), sid='faq')
    related = ''
    if p.get('related'):
        related = section(t['related'], '', cards([RELATED[lang][k] + ('Learn more →' if lang == 'en' else 'En savoir plus →',) for k in p['related']]), alt=True)

    cta = f'''<div class="svc-cta">
  <h2>{t["cta_title"]}</h2>
  <p>{t["cta_text"]}</p>
  <div class="svc-actions">
    <a class="svc-btn wa" href="{p["wa"]}" target="_blank" rel="noopener">{t["cta_wa"]}</a>
    <a class="svc-btn ghost" href="mailto:{EMAIL}">{t["cta_mail"]}</a>
  </div>
  <p class="svc-contact-line">📞 <a href="tel:+237682402876">{PHONE}</a> · 📧 <a href="mailto:{EMAIL}">{EMAIL}</a> · 📍 Douala, {"Cameroon" if lang == "en" else "Cameroun"}</p>
</div>'''

    fsvc = ''.join(f'<a href="{h}">{n}</a>' for h, n in FOOTER_SERVICES)
    og_locale, og_alt = ('en_US', 'fr_FR') if lang == 'en' else ('fr_FR', 'en_US')
    xdefault = en_url
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_plain}</title>
  <meta name="description" content="{p["desc"]}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="fr" href="{fr_url}">
  <link rel="alternate" hreflang="x-default" href="{xdefault}">
  <link rel="icon" href="images/logo-blue.jpeg">
  <link rel="apple-touch-icon" href="images/logo-blue.jpeg">
  <meta property="og:site_name" content="AsghinLabs">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:locale:alternate" content="{og_alt}">
  <meta property="og:type" content="{"article" if p.get("kind") == "article" else "website"}">
  <meta property="og:title" content="{title_plain}">
  <meta property="og:description" content="{p["desc"]}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/og-cover.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title_plain}">
  <meta name="twitter:description" content="{p["desc"]}">
  <meta name="twitter:image" content="{SITE}/images/og-cover.jpg">
  <meta name="geo.region" content="CM-LT">
  <meta name="geo.placename" content="Douala">
  <link rel="stylesheet" href="style-main.css">
  <link rel="stylesheet" href="style-service.css">
  <script type="application/ld+json">
{jsonld(p, lang)}
  </script>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FK679H74R1"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-FK679H74R1');
  </script>
</head>
<body>
<!-- Generated by services-src/build_services.py: edit the script, not this file. -->
<nav>
  <a class="logo" href="{t["home"][0]}">
    <img src="images/logo-blue.jpeg" alt="AsghinLabs" id="navLogoImg" width="42" height="42">
    <span>ASGHINLABS</span>
  </a>
  <button class="hamburger" id="hamburgerBtn" aria-label="{t["menu"]}" aria-expanded="false" aria-controls="navLinks">
    <span></span><span></span><span></span>
  </button>
  <ul class="nav-links" id="navLinks">{nav}</ul>
</nav>

<main>
{hero}
{body}
{faq}
{related}
{cta}
</main>

<footer>
  <p style="font-weight:700; color:var(--text-light); margin-bottom:6px;">AsghinLabs</p>
  <p style="margin-bottom:6px;">{t["footer_tag"]}</p>
  <p style="margin-bottom:18px;">{t["footer_line"]}</p>
  <div class="svc-footer-services" role="navigation" aria-label="Services">{fsvc}</div>
  <div class="footer-links" role="navigation" aria-label="Footer">
    <a href="/">Home</a> · <a href="/fr">Accueil (FR)</a> · <a href="/portfolio">Portfolio</a> · <a href="/academy">Academy</a> · <a href="/founder">Founder</a> · <a href="/join">Join us</a>
  </div>
  <p style="margin-top:14px">© 2026 AsghinLabs. {t["rights"]}</p>
</footer>

<a class="whatsapp-float" href="{p["wa"]}" target="_blank" rel="noopener" aria-label="WhatsApp">💬</a>
<script src="script-main.js"></script>
</body>
</html>
'''


def update_sitemap(urls):
    p = ROOT / 'sitemap.xml'
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    nl = '\r\n' if '\r\n' in s else '\n'
    for u in urls:
        loc = SITE + u
        s = re.sub(r'\s*<url>\s*<loc>' + re.escape(loc) + r'</loc>.*?</url>', '', s, flags=re.S)
    add = ''.join(f'  <url>{nl}    <loc>{SITE + u}</loc>{nl}    <lastmod>{TODAY}</lastmod>{nl}    <changefreq>monthly</changefreq>{nl}    <priority>{"0.9" if u == "/fr" else "0.8"}</priority>{nl}  </url>{nl}' for u in urls)
    s = s.replace('</urlset>', add + '</urlset>')
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def main():
    urls = []
    for p in PAGES:
        name = 'fr' if p['slug'] == '/fr' else p['slug'].lstrip('/')
        (ROOT / f'{name}.html').write_text(render(p), encoding='utf-8')
        urls.append(p['slug'])
    update_sitemap(urls)
    print(f'Built {len(urls)} pages: ' + ', '.join(urls))


if __name__ == '__main__':
    main()
