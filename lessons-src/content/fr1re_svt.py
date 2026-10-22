"""Première D — SVTEEHB, chapitre 1 : Identité biologique des organismes (séances 1 à 6).
Séance 7 (apprentissage de l'intégration) is folded into the last activities of séance 6."""
from helpers import *

# ---------------------------------------------------------------- visuals
# Animal cell (light microscope) with numbered markers for the label activity
CELL_ANIMAL = svg(420, 230, ''.join([
    '<path d="M70,120 C65,60 140,25 205,40 C275,55 320,100 300,155 C282,205 200,220 140,205 C95,193 73,163 70,120 Z" class="v-box2"/>',
    '<circle cx="190" cy="125" r="38" class="v-box"/>',
    '<circle cx="200" cy="116" r="10" fill="#7fe3ff"/>',
    marker(110, 95, 1), marker(190, 160, 2), marker(200, 116, 3), marker(300, 155, 4),
]), 'Cellule animale vue au microscope optique')

CELL_PLANT = svg(420, 230, ''.join([
    '<rect x="90" y="20" width="230" height="190" rx="8" fill="none" stroke="#7ff0b8" stroke-width="7"/>',
    '<rect x="98" y="28" width="214" height="174" rx="5" fill="rgba(46,230,139,0.06)" stroke="#7ff0b8" stroke-width="1.5"/>',
    '<rect x="150" y="65" width="140" height="110" rx="42" fill="rgba(127,227,255,0.12)" stroke="#7fe3ff" stroke-width="2"/>',
    '<circle cx="125" cy="58" r="18" class="v-box2"/>',
    '<ellipse cx="120" cy="180" rx="11" ry="6" fill="#2ee68b"/><ellipse cx="295" cy="45" rx="11" ry="6" fill="#2ee68b"/><ellipse cx="230" cy="190" rx="11" ry="6" fill="#2ee68b"/>',
    marker(90, 120, 1), marker(220, 120, 2), marker(125, 58, 3), marker(120, 180, 4),
]), 'Cellule végétale vue au microscope optique')

ORGANITES = svg(440, 250, ''.join([
    '<ellipse cx="220" cy="125" rx="200" ry="112" class="v-box2"/>',
    '<circle cx="200" cy="120" r="42" class="v-box"/>', '<circle cx="210" cy="112" r="11" fill="#7fe3ff"/>',
    '<ellipse cx="335" cy="80" rx="38" ry="17" fill="rgba(255,120,100,0.15)" stroke="#ff8a7a" stroke-width="2"/>',
    '<path d="M305,80 l9,-11 l8,22 l8,-22 l8,22 l8,-22 l8,22 l8,-11" fill="none" stroke="#ff8a7a" stroke-width="1.6"/>',
    '<path d="M300,170 q30,-18 60,0 M297,182 q34,-18 68,0 M294,194 q38,-18 76,0" fill="none" stroke="#ffcf85" stroke-width="3"/>',
    '<path d="M80,95 q18,-11 36,0 q18,11 36,0 M76,110 q18,-11 36,0 q18,11 36,0" fill="none" stroke="#c9a8ff" stroke-width="2.2"/>',
    '<circle cx="88" cy="88" r="2.4" fill="#fff"/><circle cx="104" cy="89" r="2.4" fill="#fff"/><circle cx="122" cy="96" r="2.4" fill="#fff"/><circle cx="138" cy="100" r="2.4" fill="#fff"/>',
    '<circle cx="130" cy="185" r="12" fill="rgba(46,230,139,0.15)" stroke="#7ff0b8" stroke-width="2"/>',
    marker(200, 170, 1), marker(335, 50, 2), marker(375, 175, 3), marker(80, 130, 4), marker(130, 212, 5),
]), 'Ultrastructure d’une cellule animale')

CHROMO = svg(420, 220, ''.join([
    '<path d="M180,15 q-12,40 8,85 q-20,45 -8,105 q12,8 22,0 q-6,-55 14,-105 q-18,-45 -14,-85 q-10,-8 -22,0 Z" class="v-box"/>',
    '<path d="M240,15 q12,40 -8,85 q20,45 8,105 q-12,8 -22,0 q6,-55 -14,-105 q18,-45 14,-85 q10,-8 22,0 Z" class="v-box"/>',
    '<circle cx="210" cy="100" r="9" fill="#7fe3ff"/>',
    marker(150, 60, 1), marker(270, 100, 2), marker(250, 18, 3), marker(150, 175, 4),
]), 'Chromosome en métaphase')

DNA = svg(420, 250, ''.join([
    '<path d="M110,15 C190,55 190,85 110,125 C30,165 30,195 110,235" fill="none" stroke="#7fe3ff" stroke-width="5"/>',
    '<path d="M310,15 C230,55 230,85 310,125 C390,165 390,195 310,235" fill="none" stroke="#ffcf85" stroke-width="5"/>',
    '<line x1="140" y1="35" x2="280" y2="35" class="v-line"/><text x="175" y="31" class="v-t">A</text><text x="245" y="31" class="v-t">T</text>',
    '<line x1="165" y1="65" x2="255" y2="65" class="v-line"/><text x="180" y="61" class="v-t">G</text><text x="232" y="61" class="v-t">C</text>',
    '<line x1="135" y1="105" x2="285" y2="105" class="v-line"/><text x="170" y="101" class="v-t">T</text><text x="245" y="101" class="v-t">A</text>',
    '<line x1="70" y1="150" x2="350" y2="150" class="v-line"/><text x="170" y="146" class="v-t">C</text><text x="245" y="146" class="v-t">G</text>',
    '<line x1="62" y1="185" x2="358" y2="185" class="v-line"/><text x="170" y="181" class="v-t">A</text><text x="245" y="181" class="v-t">T</text>',
    '<text x="210" y="248" text-anchor="middle" class="v-s">Deux brins complémentaires enroulés en double hélice</text>',
]), 'Double hélice d’ADN')

NUCLEOTIDE = svg(420, 110, ''.join([
    box(10, 25, 110, 56, 'Phosphate', 'P', 'v-box2'), arrow(120, 53, 150, 53),
    box(150, 25, 120, 56, 'Désoxyribose', 'sucre', 'v-box'), arrow(270, 53, 300, 53),
    box(300, 25, 110, 56, 'Base azotée', 'A, T, G ou C', 'v-box3'),
]), 'Un nucléotide')

def _cell(cx, inner):
    return f'<circle cx="{cx}" cy="70" r="52" class="v-box2"/>' + inner

MITOSE = svg(440, 165, ''.join([
    _cell(55, '<circle cx="55" cy="70" r="28" fill="none" stroke="#ffcf85" stroke-dasharray="4 3"/><path d="M42,55 l7,22 M48,53 l7,22 M62,57 l-4,22 M68,59 l-4,22" stroke="#7fe3ff" stroke-width="4" stroke-linecap="round"/>'),
    _cell(165, '<path d="M115,70 L165,40 L215,70 L165,100 Z" fill="none" stroke="rgba(255,255,255,0.35)"/><path d="M161,38 l8,18 M161,62 l8,18 M161,86 l8,18" stroke="#7fe3ff" stroke-width="4" stroke-linecap="round"/>'),
    _cell(275, '<path d="M240,52 l-9,-7 M240,88 l-9,7 M240,70 l-11,0 M310,52 l9,-7 M310,88 l9,7 M310,70 l11,0" stroke="#7fe3ff" stroke-width="4" stroke-linecap="round"/>'),
    _cell(385, '<circle cx="363" cy="70" r="16" class="v-box"/><circle cx="407" cy="70" r="16" class="v-box"/><line x1="385" y1="20" x2="385" y2="120" stroke="#ffcf85" stroke-dasharray="4 3"/>'),
    marker(55, 140, 1), marker(165, 140, 2), marker(275, 140, 3), marker(385, 140, 4),
]), 'Quatre cellules en division, dans le désordre')

CYCLE_ADN = svg(440, 200, ''.join([
    '<line x1="40" y1="165" x2="430" y2="165" class="v-line"/><line x1="40" y1="165" x2="40" y2="15" class="v-line"/>',
    '<polyline points="40,125 140,125 200,60 320,60 350,60 350,125 430,125" fill="none" stroke="#7fe3ff" stroke-width="4"/>',
    '<text x="32" y="129" text-anchor="end" class="v-s">Q</text><text x="32" y="64" text-anchor="end" class="v-s">2Q</text>',
    '<text x="90" y="185" text-anchor="middle" class="v-t">G1</text><text x="170" y="185" text-anchor="middle" class="v-t">S</text>',
    '<text x="260" y="185" text-anchor="middle" class="v-t">G2</text><text x="340" y="185" text-anchor="middle" class="v-t">M</text><text x="395" y="185" text-anchor="middle" class="v-t">G1</text>',
    '<text x="236" y="45" text-anchor="middle" class="v-s">ADN par cellule</text>',
]), 'Quantité d’ADN au cours du cycle cellulaire')

SERIE = '<p class="wt-key" style="margin-top:4px">Première D · SVTEEHB · Progression MINESEC 2026–2027</p>'

LESSONS = {
    # ------------------------------------------------------------ séance 1
    1: L('Tous les êtres vivants sont faits de cellules. Au microscope optique, on reconnaît une cellule animale et une cellule végétale grâce à quelques structures simples.',
         [('La cellule, unité du vivant',
           '<p>La <b>cellule</b> est l’unité de <b>structure</b> (de construction) et de <b>fonctionnement</b> de tous les êtres vivants (théorie cellulaire : Schleiden et Schwann, 1838–1839 ; Virchow, 1855 : « toute cellule provient d’une cellule »).</p>'
           '<p>Une cellule mesure environ 10 à 100 µm (1 µm = 0,001 mm) : il faut un <b>microscope optique</b> pour la voir.</p>' + SERIE),
          ('Le grossissement du microscope',
           '<p class="wt-key">Grossissement = grossissement de l’objectif × grossissement de l’oculaire</p>'
           '<p>Exemple : objectif ×40 et oculaire ×10 → grossissement <b>×400</b>.</p>'
           '<p>Taille réelle = taille sur le dessin ÷ grossissement. Une cellule de 6 cm sur une photo à ×3 000 mesure 60 000 µm ÷ 3 000 = <b>20 µm</b>.</p>'),
          ('La cellule animale',
           CELL_ANIMAL + '<p>1 = cytoplasme · 2 = noyau · 3 = nucléole · 4 = membrane plasmique</p>'
           '<p>Forme variable, pas de paroi, pas de chloroplaste, petites vacuoles.</p>'),
          ('La cellule végétale',
           CELL_PLANT + '<p>1 = paroi pectocellulosique · 2 = vacuole · 3 = noyau · 4 = chloroplaste</p>'
           '<p>Forme fixe, grâce à la <b>paroi</b> de cellulose et de pectine ; une grande <b>vacuole</b> ; des <b>chloroplastes</b> dans les parties vertes.</p>'),
          ('TP1 : préparer et observer',
           '<ul><li><b>Végétal :</b> épiderme d’oignon dans une goutte d’eau iodée (ou de rouge neutre), sous lamelle ; feuille d’élodée sans colorant pour voir les chloroplastes.</li>'
           '<li><b>Animal :</b> cellules de la joue raclées avec une spatule propre, dans une goutte de bleu de méthylène.</li>'
           '<li>Observer d’abord au faible grossissement, puis au fort.</li></ul>'
           '<p><b>Dessin d’observation :</b> au crayon, titre souligné, légendes alignées à droite avec des traits à la règle, grossissement indiqué.</p>'),
          ('À retenir',
           '<p class="wt-key">Toute cellule a une membrane plasmique, un cytoplasme et un noyau. La cellule végétale a en plus une paroi, une grande vacuole et des chloroplastes.</p>')],
         [label('Légendez la cellule animale.', CELL_ANIMAL, ['Cytoplasme', 'Noyau', 'Nucléole', 'Membrane plasmique'],
                'Le noyau, avec son nucléole, est entouré du cytoplasme ; la membrane plasmique limite la cellule.'),
          label('Légendez la cellule végétale.', CELL_PLANT, ['Paroi pectocellulosique', 'Vacuole', 'Noyau', 'Chloroplaste'],
                'La paroi épaisse entoure la cellule ; la grande vacuole repousse le noyau sur le côté.'),
          sort('Classez chaque structure.', ['Animale seulement', 'Végétale seulement', 'Les deux'],
               [('Paroi pectocellulosique', 'Végétale seulement'), ('Chloroplaste', 'Végétale seulement'), ('Noyau', 'Les deux'),
                ('Membrane plasmique', 'Les deux'), ('Centrosome', 'Animale seulement'), ('Grande vacuole centrale', 'Végétale seulement'), ('Cytoplasme', 'Les deux')],
               'La paroi, les chloroplastes et la grande vacuole sont propres aux cellules végétales ; le centrosome est typique des cellules animales.'),
          fill('Calculez.', 'Objectif ×40 et oculaire ×10 : grossissement ×{0}.', [['400']], '40 × 10 = 400.'),
          fill('Calculez la taille réelle.', 'Une cellule mesure 6 cm sur une photo prise à ×3 000. Sa taille réelle est {0} µm.', [['20']],
               '6 cm = 60 000 µm ; 60 000 ÷ 3 000 = 20 µm.', hint='Convertissez d’abord 6 cm en µm (1 cm = 10 000 µm).'),
          mcq('Pour observer des cellules de la joue, on utilise :', ['Du bleu de méthylène', 'De l’eau de javel', 'Du sel', 'De l’alcool pur'],
              'Du bleu de méthylène', 'Le bleu de méthylène colore le noyau et rend les cellules visibles.'),
          tf('Dans un dessin d’observation, les légendes se placent à droite, avec des traits tirés à la règle.', True)]),

    # ------------------------------------------------------------ séance 2
    2: L('Le microscope électronique montre l’ultrastructure de la cellule : chaque organite a une structure adaptée à son rôle.',
         [('Le microscope électronique',
           '<p>Il utilise un faisceau d’<b>électrons</b>. Son pouvoir de résolution est environ <b>1 000 fois meilleur</b> que celui du microscope optique : on voit les <b>organites</b>, petites structures du cytoplasme, souvent entourées d’une membrane.</p>'),
          ('Ultrastructure d’une cellule animale',
           ORGANITES + '<p>1 = noyau · 2 = mitochondrie · 3 = appareil de Golgi · 4 = réticulum endoplasmique granuleux + ribosomes · 5 = lysosome</p>'),
          ('Noyau et membrane',
           '<ul><li><b>Membrane plasmique :</b> double couche de lipides avec des protéines (mosaïque fluide) ; contrôle les échanges.</li>'
           '<li><b>Noyau :</b> enveloppe double percée de <b>pores</b>, chromatine (ADN), nucléole ; c’est le centre de commande.</li>'
           '<li><b>Nucléole :</b> fabrique les ribosomes.</li></ul>'),
          ('Les usines à protéines',
           '<ul><li><b>Ribosomes :</b> grains libres ou fixés au REG ; synthèse des protéines.</li>'
           '<li><b>Réticulum endoplasmique granuleux (REG) :</b> transport des protéines ; <b>lisse (REL)</b> : synthèse des lipides.</li>'
           '<li><b>Appareil de Golgi :</b> saccules empilés ; modifie, trie et exporte les protéines (sécrétion).</li></ul>'),
          ('Énergie, digestion, division',
           '<ul><li><b>Mitochondrie :</b> double membrane, la membrane interne forme des <b>crêtes</b> ; <b>respiration cellulaire</b> (production d’ATP).</li>'
           '<li><b>Chloroplaste</b> (végétal) : double membrane, <b>thylakoïdes</b> empilés en grana, stroma ; <b>photosynthèse</b>.</li>'
           '<li><b>Lysosome :</b> enzymes digestives ; digestion intracellulaire.</li>'
           '<li><b>Vacuole :</b> réserve d’eau et de substances.</li>'
           '<li><b>Centrosome</b> (animal) : deux centrioles ; organise le fuseau de division.</li></ul>'),
          ('À retenir',
           '<p class="wt-key">Structure adaptée à la fonction : les crêtes augmentent la surface de la respiration dans la mitochondrie ; les thylakoïdes portent la chlorophylle dans le chloroplaste.</p>')],
         [label('Légendez cette cellule vue au microscope électronique.', ORGANITES,
                ['Noyau', 'Mitochondrie', 'Appareil de Golgi', 'REG et ribosomes', 'Lysosome'],
                'La mitochondrie se reconnaît à ses crêtes ; l’appareil de Golgi à ses saccules empilés en arc.'),
          match('Reliez chaque organite à son rôle.',
                [('Mitochondrie', 'Respiration cellulaire'), ('Chloroplaste', 'Photosynthèse'), ('Ribosome', 'Synthèse des protéines'),
                 ('Appareil de Golgi', 'Tri et sécrétion des protéines'), ('Lysosome', 'Digestion intracellulaire'), ('Nucléole', 'Fabrication des ribosomes')]),
          mcq('Un organite a une double membrane et des empilements de sacs aplatis riches en pigment vert. C’est :',
              ['Un chloroplaste', 'Une mitochondrie', 'Un lysosome', 'Un appareil de Golgi'], 'Un chloroplaste',
              'Les thylakoïdes empilés (grana) contiennent la chlorophylle.'),
          mcq('Les crêtes de la mitochondrie servent à :', ['Augmenter la surface où se fait la respiration', 'Stocker l’ADN', 'Digérer les déchets', 'Fabriquer la paroi'],
              'Augmenter la surface où se fait la respiration'),
          tf('Les pores de l’enveloppe nucléaire permettent des échanges entre le noyau et le cytoplasme.', True),
          tf('Le centrosome organise le fuseau de division chez les cellules animales.', True),
          tf('On voit facilement les ribosomes au microscope optique.', False, 'Ils sont trop petits : il faut le microscope électronique.')]),

    # ------------------------------------------------------------ séance 3
    3: L('Le chromosome est formé d’ADN et de protéines. Le nombre et la forme des chromosomes, le caryotype, sont propres à chaque espèce.',
         [('Chromatine et chromosome',
           '<p>Dans un noyau au repos, l’ADN forme la <b>chromatine</b>, de longs filaments fins. Au début de la division, la chromatine se <b>condense</b> : les <b>chromosomes</b> deviennent visibles au microscope optique.</p>'),
          ('Structure d’un chromosome en métaphase',
           CHROMO + '<p>1 = chromatide · 2 = centromère · 3 = télomère · 4 = bras</p>'
           '<p>Deux <b>chromatides sœurs</b> identiques sont unies au <b>centromère</b>. Selon la position du centromère : métacentrique, submétacentrique, acrocentrique.</p>'),
          ('Composition chimique',
           '<p>Chromosome = <b>ADN + protéines</b>, surtout des <b>histones</b>.</p>'
           '<p>L’ADN s’enroule autour de groupes de huit histones : ce sont les <b>nucléosomes</b> (« collier de perles »), qui se replient encore pour former le chromosome.</p>'
           '<p class="wt-key">1 chromatide = 1 molécule d’ADN. Un chromosome à deux chromatides contient deux molécules d’ADN identiques.</p>'),
          ('Le caryotype',
           '<p>Le <b>caryotype</b> est l’ensemble des chromosomes d’une cellule, photographiés en métaphase et classés par paires.</p>'
           '<ul><li>Homme : <b>2n = 46</b> = 22 paires d’autosomes + 1 paire de chromosomes sexuels (XX ou XY).</li>'
           '<li>Cellule <b>diploïde (2n)</b> : chromosomes par paires (cellules du corps).</li>'
           '<li>Cellule <b>haploïde (n)</b> : un seul chromosome de chaque paire (gamètes, n = 23 chez l’Homme).</li></ul>'),
          ('À retenir',
           '<p class="wt-key">Chromosome = ADN + histones. Le caryotype est constant pour une espèce : c’est un élément de son identité biologique.</p>')],
         [label('Légendez le chromosome.', CHROMO, ['Chromatide', 'Centromère', 'Télomère', 'Bras'],
                'Les deux chromatides sont reliées par le centromère ; les télomères sont les extrémités.'),
          mcq('Un chromosome est formé de :', ['ADN et protéines (histones)', 'Lipides et sucres', 'ARN seulement', 'Cellulose et pectine'], 'ADN et protéines (histones)'),
          fill('Complétez.', 'Chez l’Homme, une cellule du corps a {0} chromosomes, soit {1} paires d’autosomes et 1 paire de chromosomes sexuels.', [['46'], ['22']]),
          match('Reliez chaque terme à sa définition.',
                [('Diploïde', 'Chromosomes groupés par paires (2n)'), ('Haploïde', 'Un seul chromosome de chaque paire (n)'),
                 ('Caryotype', 'Chromosomes classés par paires'), ('Nucléosome', 'ADN enroulé autour d’histones')]),
          mcq('Un caryotype humain montre 47 chromosomes avec trois chromosomes n° 21. Il s’agit de :',
              ['Une trisomie 21', 'Un caryotype normal', 'Une cellule haploïde', 'Une cellule en G1'], 'Une trisomie 21',
              'Le caryotype normal est 2n = 46 : un chromosome 21 en trop donne une trisomie 21.'),
          tf('Un chromosome à deux chromatides contient deux molécules d’ADN identiques.', True)]),

    # ------------------------------------------------------------ séance 4
    4: L('Des expériences historiques ont montré que l’ADN porte l’information génétique. Sa structure en double hélice permet de le copier fidèlement.',
         [('Les preuves expérimentales',
           '<ul><li><b>Griffith (1928)</b> : des pneumocoques S tués + des R vivants tuent la souris → un « principe transformant » passe des S aux R.</li>'
           '<li><b>Avery, MacLeod et McCarty (1944)</b> : la transformation n’a plus lieu seulement quand on détruit l’<b>ADN</b> → le principe transformant est l’ADN.</li>'
           '<li><b>Hershey et Chase (1952)</b> : seul l’ADN des bactériophages entre dans la bactérie et dirige la fabrication de nouveaux virus.</li></ul>'),
          ('Le nucléotide',
           NUCLEOTIDE + '<p>L’ADN est une longue chaîne de <b>nucléotides</b>. Quatre bases : <b>A</b> adénine, <b>T</b> thymine, <b>G</b> guanine, <b>C</b> cytosine.</p>'),
          ('La double hélice (Watson et Crick, 1953)',
           DNA + '<ul><li>Deux brins enroulés, montants phosphate–désoxyribose.</li>'
           '<li><b>Complémentarité :</b> A–T (2 liaisons hydrogène), G–C (3 liaisons hydrogène).</li>'
           '<li>Diamètre 2 nm ; un tour = 10 paires de bases = 3,4 nm.</li></ul>'),
          ('Règle de Chargaff et calculs',
           '<p class="wt-key">A = T et G = C, donc A + G = T + C = 50 %</p>'
           '<p>Si A = 30 %, alors T = 30 %, et G = C = (100 − 60) ÷ 2 = 20 %.</p>'
           '<p>3 400 paires de bases → 340 tours → 340 × 3,4 nm = 1 156 nm.</p>'),
          ('Le gène et l’information génétique',
           '<p>L’information génétique est écrite dans l’<b>ordre des bases</b>. Un <b>gène</b> est une portion d’ADN qui commande un caractère. Chaque brin permettant de reconstruire l’autre, l’ADN peut être copié sans erreur.</p>'
           '<p><b>TP3 :</b> construire une maquette d’ADN (pailles, perles de quatre couleurs) en respectant A–T et G–C, puis la torsader.</p>'),
          ('À retenir',
           '<p class="wt-key">L’ADN est le support de l’information génétique : une double hélice de nucléotides, bases complémentaires A–T et G–C.</p>')],
         [order('Remettez les découvertes dans l’ordre chronologique.',
                ['Griffith : le principe transformant', 'Avery, MacLeod et McCarty : c’est l’ADN', 'Hershey et Chase : seul l’ADN entre dans la bactérie', 'Watson et Crick : la double hélice'],
                '1928 → 1944 → 1952 → 1953.'),
          fill('Écrivez le brin complémentaire.', '5′-ATGCCGTA-3′ → 3′-{0}-5′', [['TACGGCAT']],
               'A en face de T, G en face de C.', hint='Remplacez chaque A par T, T par A, G par C et C par G.'),
          fill('Un ADN contient 30 % d’adénine. Complétez.', 'T = {0} %, G = {1} %, C = {2} %.', [['30'], ['20'], ['20']],
               'A = T = 30 % ; G + C = 40 %, donc G = C = 20 %.'),
          fill('Calculez.', 'Une molécule d’ADN de 3 400 paires de bases fait {0} tours d’hélice.', [['340']], '3 400 ÷ 10 = 340.'),
          mcq('Combien de liaisons hydrogène unissent G et C ?', ['3', '2', '1', '4'], '3', 'A–T : 2 liaisons ; G–C : 3 liaisons.'),
          sort('Ces éléments font-ils partie d’un nucléotide d’ADN ?', ['Oui', 'Non'],
               [('Phosphate', 'Oui'), ('Désoxyribose', 'Oui'), ('Thymine', 'Oui'), ('Uracile', 'Non'), ('Ribose', 'Non'), ('Guanine', 'Oui')],
               'L’uracile et le ribose appartiennent à l’ARN, pas à l’ADN.'),
          tf('L’information génétique est portée par l’ordre des bases le long de l’ADN.', True)]),

    # ------------------------------------------------------------ séance 5
    5: L('La mitose partage une cellule en deux cellules filles qui ont exactement les mêmes chromosomes que la cellule mère.',
         [('Définition',
           '<p>La <b>mitose</b> donne <b>deux cellules filles génétiquement identiques</b> à la cellule mère. Elle comprend la division du noyau (<b>caryocinèse</b>, en quatre phases) puis celle du cytoplasme (<b>cytodiérèse</b>). On l’observe bien dans les pointes de racines d’oignon.</p>'),
          ('Prophase',
           '<p>La chromatine se condense : les chromosomes à deux chromatides apparaissent. Le nucléole et l’enveloppe nucléaire disparaissent. Le <b>fuseau de division</b> se forme.</p>'),
          ('Métaphase',
           '<p>Les chromosomes, très condensés, s’alignent par leur centromère au milieu de la cellule : la <b>plaque équatoriale</b>. C’est le meilleur moment pour compter les chromosomes.</p>'),
          ('Anaphase',
           '<p>Les centromères se divisent ; les deux chromatides de chaque chromosome se séparent et migrent vers les pôles opposés (<b>ascension polaire</b>).</p>'),
          ('Télophase et cytodiérèse',
           '<p>Les chromosomes se décondensent ; une enveloppe nucléaire se reforme autour de chaque lot : deux noyaux. Puis le cytoplasme se partage :</p>'
           '<div class="two-col"><div><b>Cellule animale</b>par étranglement de la membrane ; fuseau formé à partir des centrosomes</div><div><b>Cellule végétale</b>par une plaque cellulaire (nouvelle paroi) au milieu ; pas de centrosome</div></div>'),
          ('À retenir',
           MITOSE + '<p class="wt-key">Prophase → métaphase → anaphase → télophase, puis cytodiérèse : deux cellules filles identiques.</p>'
           '<p><b>TP4 :</b> sur des photos de pointes de racines, repérer une cellule de chaque phase et justifier.</p>')],
         [label('Ces quatre cellules sont en division. Nommez la phase de chacune.', MITOSE, ['Prophase', 'Métaphase', 'Anaphase', 'Télophase'],
                '1 : chromosomes condensés dans le noyau ; 2 : plaque équatoriale ; 3 : chromatides vers les pôles ; 4 : deux noyaux.'),
          order('Remettez les étapes dans l’ordre.',
                ['Les chromosomes deviennent visibles, l’enveloppe nucléaire disparaît', 'Les chromosomes s’alignent sur la plaque équatoriale',
                 'Les chromatides se séparent et vont aux pôles', 'Deux noyaux se reforment', 'Le cytoplasme se partage'],
                'Prophase, métaphase, anaphase, télophase, puis cytodiérèse.'),
          match('Reliez chaque événement à sa phase.',
                [('Formation du fuseau', 'Prophase'), ('Plaque équatoriale', 'Métaphase'), ('Ascension polaire', 'Anaphase'), ('Reformation des noyaux', 'Télophase')]),
          mcq('Chez une cellule végétale, le cytoplasme se partage par :', ['Une plaque cellulaire', 'Un étranglement', 'La disparition de la paroi', 'Les centrosomes'],
              'Une plaque cellulaire', 'La paroi rigide empêche l’étranglement : une nouvelle paroi se forme au milieu.'),
          tf('Les deux cellules filles d’une mitose ont le même nombre de chromosomes que la cellule mère.', True),
          tf('C’est à l’anaphase que l’on compte le plus facilement les chromosomes.', False, 'C’est à la métaphase, quand ils sont alignés et très condensés.')]),

    # ------------------------------------------------------------ séance 6 (+ intégration)
    6: L('Le cycle cellulaire alterne la préparation (interphase) et la division (mitose). La réplication puis la mitose conservent l’identité génétique de chaque cellule.',
         [('Les phases du cycle cellulaire',
           '<ul><li><b>G1</b> : croissance ; chromosomes à <b>une</b> chromatide.</li>'
           '<li><b>S</b> : <b>réplication de l’ADN</b> ; chaque chromosome passe à <b>deux</b> chromatides.</li>'
           '<li><b>G2</b> : préparation à la division.</li>'
           '<li><b>M</b> : mitose.</li></ul><p>G1 + S + G2 = <b>interphase</b>, la phase la plus longue.</p>'),
          ('La quantité d’ADN',
           CYCLE_ADN + '<p class="wt-key">En phase S, l’ADN double (Q → 2Q) ; à l’anaphase il est partagé : chaque cellule fille retrouve Q.</p>'),
          ('Une réplication semi-conservative',
           '<p>Les deux brins de l’ADN se séparent ; chacun sert de <b>modèle</b> pour fabriquer un brin complémentaire (A–T, G–C). Chaque nouvelle molécule garde <b>un brin ancien et un brin nouveau</b> (Meselson et Stahl, 1958).</p>'
           '<p>Les deux chromatides d’un chromosome portent donc exactement la même information.</p>'),
          ('Les rôles de la mitose',
           '<ul><li><b>Croissance</b> de l’organisme à partir de la cellule-œuf.</li>'
           '<li><b>Renouvellement</b> des cellules usées (peau, sang, intestin).</li>'
           '<li><b>Réparation</b> des tissus (cicatrisation).</li>'
           '<li><b>Multiplication végétative</b> : boutures de manioc, rejets de bananier ; les nouvelles plantes sont des <b>clones</b>.</li>'
           '<li><b>Conservation de l’identité génétique</b> : toutes les cellules gardent le même caryotype.</li></ul>'),
          ('Intégration : la bouture de manioc',
           '<p>M. Fotso, à Bafang, veut une plantation qui garde les qualités de sa meilleure variété de manioc. Pourquoi planter des <b>boutures</b> plutôt que des graines ?</p>'
           '<p>La bouture grandit uniquement par <b>mitoses</b> : chaque cellule reçoit la même information génétique, répliquée fidèlement. Les plants sont des clones de la plante mère. Les graines viennent de la reproduction sexuée, qui mélange l’information de deux parents : certaines qualités peuvent se perdre.</p>'),
          ('À retenir',
           '<p class="wt-key">Cycle = G1 → S → G2 → M. Réplication semi-conservative + mitose = transmission fidèle de l’information génétique.</p>')],
         [order('Remettez les phases du cycle cellulaire dans l’ordre, à partir de la naissance de la cellule.', ['G1', 'S', 'G2', 'Mitose (M)'],
                'L’ADN est répliqué en S, entre G1 et G2.'),
          fill('Une cellule humaine en G1 contient 6,6 pg d’ADN. Complétez.', 'En G2 : {0} pg. Chaque cellule fille après la mitose : {1} pg.', [['13,2', '13.2'], ['6,6', '6.6']],
               'L’ADN double en phase S puis il est partagé entre les deux cellules filles.'),
          mcq('Pendant quelle phase la quantité d’ADN double-t-elle ?', ['S', 'G1', 'G2', 'Métaphase'], 'S'),
          mcq('Après une réplication semi-conservative, chaque molécule d’ADN est formée :',
              ['D’un brin ancien et d’un brin nouveau', 'De deux brins nouveaux', 'De deux brins anciens', 'D’un seul brin'],
              'D’un brin ancien et d’un brin nouveau'),
          sort('Ces situations font-elles appel à la mitose ?', ['Mitose', 'Pas la mitose'],
               [('Cicatrisation d’une plaie', 'Mitose'), ('Croissance d’un enfant', 'Mitose'), ('Bouture de manioc', 'Mitose'),
                ('Formation des gamètes', 'Pas la mitose'), ('Renouvellement des cellules de la peau', 'Mitose')],
               'Les gamètes (cellules haploïdes) se forment par un autre type de division, la méiose.'),
          fill('Calculez l’indice mitotique.', 'Sur 500 cellules d’une pointe de racine, 40 sont en mitose : indice mitotique = {0} %.', [['8']], '40 ÷ 500 × 100 = 8 %.'),
          mcq('M. Fotso veut garder exactement les qualités de son meilleur manioc. Il doit planter :',
              ['Des boutures de la meilleure plante', 'Des graines', 'N’importe quel plant du marché', 'Des graines de deux variétés mélangées'],
              'Des boutures de la meilleure plante',
              'Les boutures se développent par mitoses : les nouveaux plants ont la même information génétique que la plante mère.')]),
}
