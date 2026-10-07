"""Form 3 Mathematics: relations and functions, mensuration (lessons 47-64)."""
from helpers import *
from f3_maths_part1 import table


def arrows(left, right, pairs, la='A', lb='B'):
    """Arrow diagram: two ovals with elements and arrows for each pair (index pairs)."""
    h = 40 + 36 * max(len(left), len(right))
    s = (f'<ellipse cx="90" cy="{h / 2}" rx="60" ry="{h / 2 - 8}" class="v-box"/>'
         f'<ellipse cx="330" cy="{h / 2}" rx="60" ry="{h / 2 - 8}" class="v-box2"/>'
         f'<text x="90" y="14" text-anchor="middle" class="v-s">{la}</text><text x="330" y="14" text-anchor="middle" class="v-s">{lb}</text>')
    ly = lambda i, n: h / 2 + (i - (n - 1) / 2) * 36
    for i, t in enumerate(left):
        s += f'<text x="90" y="{ly(i, len(left)) + 5}" text-anchor="middle" class="v-t">{t}</text>'
    for i, t in enumerate(right):
        s += f'<text x="330" y="{ly(i, len(right)) + 5}" text-anchor="middle" class="v-t">{t}</text>'
    for a, b in pairs:
        s += arrow(108, ly(a, len(left)), 312, ly(b, len(right)))
    return svg(420, h, s, 'arrow diagram')


def flowd(steps):
    return flow(steps)


CYL_NET = svg(420, 200, ''.join([
    '<circle cx="60" cy="50" r="35" class="v-box2"/><circle cx="60" cy="150" r="35" class="v-box2"/>',
    '<rect x="120" y="60" width="280" height="80" class="v-box"/>',
    '<text x="260" y="104" text-anchor="middle" class="v-t">2πr × h</text>',
    '<text x="260" y="54" text-anchor="middle" class="v-s">length = circumference 2πr</text>',
    '<text x="410" y="104" class="v-s">h</text>',
]), 'Net of a cylinder')

CONE = svg(300, 220, ''.join([
    '<polygon points="150,15 60,180 240,180" class="v-box"/>',
    '<ellipse cx="150" cy="180" rx="90" ry="22" class="v-box2" style="fill-opacity:.6"/>',
    '<line x1="150" y1="15" x2="150" y2="180" class="v-line" style="stroke-dasharray:5 4"/>',
    '<line x1="150" y1="180" x2="240" y2="180" class="v-line"/>',
    '<text x="158" y="110" class="v-s">h</text><text x="195" y="198" text-anchor="middle" class="v-s">r</text><text x="205" y="90" class="v-s">l</text>',
]), 'Cone with height, radius and slant height')

LESSONS = {
    47: L('A relation links elements of one set to elements of another (or the same) set, by a rule.',
          [('Relation between two sets', '<p>A = {2, 3}, B = {4, 6, 9}. Rule: "is a factor of".</p>' +
            arrows(['2', '3'], ['4', '6', '9'], [(0, 0), (0, 1), (1, 1), (1, 2)]) +
            '<p>R = {(2, 4), (2, 6), (3, 6), (3, 9)}</p>'),
           ('Ordered pairs', '<p>Each link is an ordered pair (a, b): a from the first set, b from the second. (2, 4) ≠ (4, 2).</p>'),
           ('Relation in a set', '<p>In A = {1, 2, 3, 4}, "is less than": (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)</p>')],
          [mcq('A = {1, 2}, B = {2, 3, 4}. Which pairs make "is half of"?', ['(1, 2) and (2, 4)', '(2, 1) and (4, 2)', '(1, 3) and (2, 4)'], '(1, 2) and (2, 4)'),
           fill('In A = {1, 2, 3}, how many pairs satisfy "is less than"?', '{0}', [['3']], '(1, 2), (1, 3), (2, 3)'),
           tf('(3, 5) and (5, 3) are the same ordered pair.', False, 'The order matters.'),
           sort('Rule "is a multiple of" from {6, 8} to {2, 3}. Is the pair in the relation?', ['Yes', 'No'], [('(6, 2)', 'Yes'), ('(6, 3)', 'Yes'), ('(8, 2)', 'Yes'), ('(8, 3)', 'No')])]),

    48: L('The Cartesian product A × B is the set of ALL ordered pairs (a, b) with a in A and b in B.',
          [('Definition', '<p>A = {1, 2}, B = {a, b, c}</p><p>A × B = {(1, a), (1, b), (1, c), (2, a), (2, b), (2, c)}</p><p class="wt-key">n(A × B) = n(A) × n(B) = 2 × 3 = 6</p>'),
           ('Arrow diagram', arrows(['1', '2'], ['a', 'b', 'c'], [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]) + '<p>Every element of A is joined to every element of B.</p>'),
           ('A × B ≠ B × A', '<p>B × A starts with elements of B: (a, 1), (a, 2), … Different pairs!</p>')],
          [fill('n(A) = 3 and n(B) = 4.', 'n(A × B) = {0}', [['12']]),
           mcq('A = {x, y}, B = {1, 2}. Which pair is in A × B?', ['(y, 1)', '(1, y)', '(x, y)'], '(y, 1)'),
           fill('A = {0, 1}. How many elements has A × A?', '{0}', [['4']]),
           tf('A × B = B × A', False),
           mcq('A relation from A to B is…', ['a subset of A × B', 'always equal to A × B', 'a single number'], 'a subset of A × B')]),

    49: L('Relations can be one-to-one, one-to-many, many-to-one or many-to-many.',
          [('The four types', table(['Type', 'Example'], [['One-to-one', 'country → its capital'], ['One-to-many', 'mother → her children'], ['Many-to-one', 'students → their class'], ['Many-to-many', 'students → subjects they study']])),
           ('Many-to-one', arrows(['Awa', 'Paul', 'Eric'], ['Form 3A', 'Form 3B'], [(0, 0), (1, 0), (2, 1)], 'students', 'class')),
           ('How to decide', '<p>Ask: can one element on the left have <b>many</b> arrows? Can one element on the right <b>receive</b> many arrows?</p>')],
          [match('Match the relation to its type.', [('Country → capital city', 'One-to-one'), ('Father → his children', 'One-to-many'), ('Pupils → their school', 'Many-to-one'), ('Teachers → classes they teach', 'Many-to-many')]),
           mcq('{(1, a), (2, a), (3, b)} is…', ['many-to-one', 'one-to-many', 'one-to-one'], 'many-to-one'),
           mcq('{(1, a), (1, b), (2, c)} is…', ['one-to-many', 'many-to-one', 'one-to-one'], 'one-to-many'),
           tf('"x ↦ x²" from {1, 2, 3} to {1, 4, 9} is one-to-one.', True, '1 → 1, 2 → 4, 3 → 9: each arrow has its own start and end.')]),

    50: L('A relation R in a set can be reflexive, symmetric and/or transitive.',
          [('Reflexive', '<p>Every a is related to itself: <b>a R a</b>. Example: "=" (5 = 5).</p>'),
           ('Symmetric', '<p>If a R b then <b>b R a</b>. Example: "is a sibling of".</p>'),
           ('Transitive', '<p>If a R b and b R c then <b>a R c</b>. Example: "&lt;" (2 &lt; 3 and 3 &lt; 7 → 2 &lt; 7).</p>'),
           ('Summary', table(['Relation', 'R', 'S', 'T'], [['=', '✓', '✓', '✓'], ['&lt;', '✗', '✗', '✓'], ['is perpendicular to', '✗', '✓', '✗'], ['is a factor of (in ℕ*)', '✓', '✗', '✓']]))],
          [match('Match each property to its rule.', [('Reflexive', 'a R a'), ('Symmetric', 'a R b ⇒ b R a'), ('Transitive', 'a R b and b R c ⇒ a R c')]),
           tf('"Is less than" is reflexive.', False, '3 < 3 is false.'),
           tf('"Is perpendicular to" (lines) is symmetric.', True),
           tf('"Is perpendicular to" (lines) is transitive.', False, 'If a ⊥ b and b ⊥ c then a ∥ c, not a ⊥ c.'),
           mcq('Which property does "is a factor of" NOT have?', ['Symmetric', 'Reflexive', 'Transitive'], 'Symmetric', '2 is a factor of 4, but 4 is not a factor of 2.')]),

    51: L('An equivalence relation is reflexive, symmetric AND transitive.',
          [('Definition', '<p class="wt-key">Equivalence relation = Reflexive + Symmetric + Transitive</p>'),
           ('Examples', '<ul><li>"=" on numbers</li><li>"has the same birthday as"</li><li>"is in the same class as"</li><li>"is congruent to"</li><li>"is parallel to" (a line counts as parallel to itself)</li></ul>'),
           ('Not equivalence relations', '<ul><li>"&lt;": not reflexive, not symmetric</li><li>"is a friend of": not always transitive</li><li>"is a factor of": not symmetric</li></ul>')],
          [sort('Equivalence relation or not?', ['Equivalence', 'Not equivalence'], [('Is equal to', 'Equivalence'), ('Is less than', 'Not equivalence'), ('Has the same age as', 'Equivalence'), ('Is a factor of', 'Not equivalence'), ('Is in the same class as', 'Equivalence')]),
           mcq('Which three properties make an equivalence relation?', ['Reflexive, symmetric, transitive', 'Reflexive and symmetric only', 'Symmetric and transitive only'], 'Reflexive, symmetric, transitive'),
           mcq('Why is "is a friend of" not an equivalence relation?', ['It is not always transitive', 'It is not symmetric', 'It has no pairs'], 'It is not always transitive', 'Your friend\'s friend is not always your friend.')]),

    52: L('For a mapping f: A → B, A is the domain, B the codomain, and the range is the set of images actually used.',
          [('Words', table(['Word', 'Meaning'], [['Domain', 'the starting set A (inputs)'], ['Codomain', 'the target set B'], ['Image of a', 'f(a), the element a goes to'], ['Range', 'the set of all images (⊆ codomain)']])),
           ('Example', '<p>f: {1, 2, 3} → {1, 2, …, 10}, f(x) = 2x + 1</p>' + arrows(['1', '2', '3'], ['3', '5', '7'], [(0, 0), (1, 1), (2, 2)], 'domain', 'images') +
            '<p>Range = {3, 5, 7}. The codomain is bigger.</p>')],
          [fill('f(x) = x + 4 on the domain {0, 1, 2}.', 'Range = { {0}, {1}, {2} }', [['4'], ['5'], ['6']]),
           fill('f(x) = 3x − 1. What is the image of 2?', 'f(2) = {0}', [['5']]),
           mcq('The range is always…', ['a subset of the codomain', 'bigger than the codomain', 'equal to the domain'], 'a subset of the codomain'),
           match('Match the word.', [('Domain', 'The set of inputs'), ('Codomain', 'The set the outputs belong to'), ('Range', 'The outputs actually reached')])]),

    53: L('A mapping sends each element of the domain to exactly one image. It can be injective, surjective or bijective.',
          [('Is it a mapping?', '<p>Every element of the domain must have <b>one and only one</b> image.</p>'),
           ('Types', table(['Type', 'Meaning'], [['Injective (one-to-one)', 'different inputs → different images'], ['Surjective (onto)', 'every element of the codomain is used (range = codomain)'], ['Bijective', 'both injective and surjective']])),
           ('Example', arrows(['1', '2', '3'], ['a', 'b', 'c'], [(0, 1), (1, 2), (2, 0)]) + '<p>Each element of B is hit exactly once → <b>bijective</b>.</p>')],
          [mcq('{(1, a), (2, a), (3, b)} from {1, 2, 3} to {a, b}. It is…', ['surjective but not injective', 'injective but not surjective', 'bijective'], 'surjective but not injective'),
           mcq('{(1, a), (2, b)} from {1, 2} to {a, b, c}. It is…', ['injective but not surjective', 'surjective', 'bijective'], 'injective but not surjective', 'c is never used.'),
           tf('If 2 is sent to both 4 and 5, the relation is a mapping.', False, 'Each input must have only one image.'),
           mcq('A bijection is…', ['injective and surjective', 'only injective', 'only surjective'], 'injective and surjective')]),

    54: L('A flow diagram shows the steps of a function. Run it backwards to find the input.',
          [('Forward', '<p>f(x) = 2x + 3:</p>' + flow(['x', '× 2', '+ 3', '2x + 3']) + '<p>Input 4 → 8 → <b>11</b></p>'),
           ('Backward', '<p>Reverse each step and the order: − 3, then ÷ 2.</p><p>Output 15 → 12 → <b>6</b></p><p class="wt-key">Undo the last step first.</p>'),
           ('Order matters', '<p>"× 2 then + 3" gives 2x + 3. "+ 3 then × 2" gives 2(x + 3) = 2x + 6.</p>')],
          [fill('Flow: × 3, then − 5. Input 4.', 'Output = {0}', [['7']]),
           fill('Flow: + 2, then × 5. Input 3.', 'Output = {0}', [['25']]),
           fill('Flow: × 2, then + 3. The output is 21.', 'Input = {0}', [['9']], '21 − 3 = 18, 18 ÷ 2 = 9.'),
           order('Build the flow diagram for 3x − 5.', ['x', '× 3', '− 5', '3x − 5']),
           mcq('Which expression does "+ 1, then × 4" give?', ['4(x + 1)', '4x + 1', 'x + 4'], '4(x + 1)')]),

    55: L('f(x) is the rule of a function. Replace x by a number to find its value.',
          [('Notation', '<p>f(x) = 2x + 1 means "f takes x to 2x + 1". Also written f: x ↦ 2x + 1.</p>'),
           ('Evaluate', '<p>f(x) = x² − 3</p><p>f(3) = 9 − 3 = <b>6</b><br>f(−2) = 4 − 3 = <b>1</b></p><p class="wt-key">Use brackets for negative numbers: (−2)² = 4.</p>'),
           ('Solve f(x) = k', '<p>f(x) = 2x + 1 = 9 → 2x = 8 → <b>x = 4</b></p>')],
          [fill('f(x) = 5x − 2.', 'f(3) = {0}', [['13']]),
           fill('f(x) = x² + 1.', 'f(−3) = {0}', [['10']]),
           fill('g(x) = 3x + 4. Solve g(x) = 19.', 'x = {0}', [['5']]),
           fill('h(x) = 2x² − x.', 'h(2) = {0}', [['6']]),
           mcq('f: x ↦ x − 7 means…', ['f(x) = x − 7', 'f(x) = 7x', 'f(x) = 7 − x'], 'f(x) = x − 7')]),

    56: L('The inverse function f⁻¹ undoes f. To find it: write y = f(x), make x the subject, then swap.',
          [('Method', '<ol><li>y = 2x + 3</li><li>Make x the subject: x = (y − 3)/2</li><li>Write it with x: <b>f⁻¹(x) = (x − 3)/2</b></li></ol>'),
           ('Check', '<p>f(4) = 11 and f⁻¹(11) = (11 − 3)/2 = 4 ✓</p><p class="wt-key">f⁻¹ takes you back to where you started.</p>'),
           ('When does it exist?', '<p>Only when f is a <b>bijection</b> (one-to-one and onto).</p>')],
          [mcq('f(x) = x + 5. f⁻¹(x) = ?', ['x − 5', 'x + 5', '5 − x'], 'x − 5'),
           mcq('f(x) = 3x. f⁻¹(x) = ?', ['x/3', '3/x', '−3x'], 'x/3'),
           mcq('f(x) = 2x − 1. f⁻¹(x) = ?', ['(x + 1)/2', '(x − 1)/2', '2x + 1'], '(x + 1)/2'),
           mcq('f(x) = (x + 1)/4. f⁻¹(x) = ?', ['4x − 1', '4x + 1', '(x − 1)/4'], '4x − 1'),
           fill('f(x) = 4x + 2. Find f⁻¹(14).', '{0}', [['3']], '(14 − 2)/4 = 3')]),

    57: L('A composite function applies one function and then another: fg(x) = f(g(x)). Do g first!',
          [('Meaning', '<p class="wt-key">fg(x) = f(g(x)): first g, then f.</p>'),
           ('Example', '<p>f(x) = 2x, g(x) = x + 3</p><p>fg(x) = f(x + 3) = <b>2x + 6</b><br>gf(x) = g(2x) = <b>2x + 3</b></p><p>fg ≠ gf: the order matters.</p>'),
           ('With numbers', '<p>fg(1): g(1) = 4, then f(4) = <b>8</b><br>gf(1): f(1) = 2, then g(2) = <b>5</b></p>')],
          [fill('f(x) = x², g(x) = x − 1.', 'fg(3) = {0}, gf(3) = {1}', [['4'], ['8']], 'fg(3) = f(2) = 4; gf(3) = g(9) = 8.'),
           mcq('f(x) = 3x, g(x) = x + 2. fg(x) = ?', ['3x + 6', '3x + 2', '3x²'], '3x + 6'),
           mcq('Same f and g. gf(x) = ?', ['3x + 2', '3x + 6', 'x + 5'], '3x + 2'),
           fill('f(x) = 2x + 1, g(x) = x².', 'fg(2) = {0}', [['9']], 'g(2) = 4, f(4) = 9'),
           tf('fg(x) and gf(x) are always equal.', False)]),

    58: L('A sphere of radius r has surface area 4πr² and volume (4/3)πr³.',
          [('Formulas', '<p class="wt-key">Surface area = 4πr² · Volume = (4/3)πr³</p>'),
           ('Example', '<p>r = 3 cm</p><p>A = 4π × 9 = <b>36π cm²</b> ≈ 113.1 cm²<br>V = (4/3)π × 27 = <b>36π cm³</b> ≈ 113.1 cm³</p>'),
           ('Hemisphere (half sphere)', '<p>Curved area = 2πr² · Total area = 3πr² (with the flat circle) · Volume = (2/3)πr³</p>')],
          [fill('A sphere has radius 5 cm. Give the answer in terms of π.', 'Surface area = {0} cm²', [['100π', '100pi']]),
           fill('A sphere has radius 3 cm. Give the answer in terms of π.', 'Volume = {0} cm³', [['36π', '36pi']]),
           fill('A sphere has radius 6 cm. Give the answer in terms of π.', 'Volume = {0} cm³', [['288π', '288pi']], '(4/3) × 216 = 288'),
           mcq('A hemisphere has radius 2 cm. Its total surface area is…', ['12π cm²', '8π cm²', '16π cm²'], '12π cm²', '3πr² = 3π × 4.'),
           tf('If the radius doubles, the volume of a sphere is multiplied by 8.', True, '2³ = 8')]),

    59: L('A cylinder\'s net is two circles and a rectangle. Volume = πr²h.',
          [('The net', CYL_NET + '<p>The rectangle wraps around: its length is the circumference 2πr.</p>'),
           ('Formulas', table(['', 'Formula'], [['Curved area', '2πrh'], ['Total area', '2πr² + 2πrh'], ['Volume', 'πr²h']])),
           ('Example', '<p>r = 3 cm, h = 5 cm</p><p>Curved = 30π · Total = 18π + 30π = <b>48π cm²</b> · Volume = 9π × 5 = <b>45π cm³</b></p>')],
          [fill('r = 2 cm, h = 10 cm. In terms of π:', 'Volume = {0} cm³', [['40π', '40pi']]),
           fill('r = 2 cm, h = 10 cm. In terms of π:', 'Curved area = {0} cm²', [['40π', '40pi']]),
           fill('r = 5 cm, h = 4 cm. In terms of π:', 'Total area = {0} cm²', [['90π', '90pi']], '2π(25) + 2π(5)(4) = 50π + 40π'),
           mcq('The rectangle in the net of a cylinder has length…', ['2πr', 'πr²', 'h'], '2πr'),
           mcq('A tank: r = 1 m, h = 2 m. Volume (π ≈ 3.14)?', ['6.28 m³', '3.14 m³', '12.56 m³'], '6.28 m³')]),

    60: L('A cone has volume (1/3)πr²h and curved area πrl, where l is the slant height.',
          [('Parts', CONE + '<p>r = radius, h = vertical height, l = slant height. Pythagoras: <b>l² = r² + h²</b>.</p>'),
           ('Formulas', table(['', 'Formula'], [['Curved area', 'πrl'], ['Total area', 'πr² + πrl'], ['Volume', '(1/3)πr²h']])),
           ('Example', '<p>r = 3, h = 4 → l = 5</p><p>Curved = 15π · Total = 9π + 15π = <b>24π</b> · Volume = (1/3)π × 9 × 4 = <b>12π</b></p><p>The net is a circle and a sector.</p>')],
          [fill('r = 6, h = 8. Find the slant height.', 'l = {0}', [['10']]),
           fill('r = 6, h = 8. In terms of π:', 'Curved area = {0}', [['60π', '60pi']]),
           fill('r = 6, h = 8. In terms of π:', 'Volume = {0}', [['96π', '96pi']], '(1/3) × 36 × 8 = 96'),
           mcq('A cone and a cylinder have the same r and h. The cone\'s volume is…', ['1/3 of the cylinder\'s', 'the same', 'half'], '1/3 of the cylinder\'s'),
           tf('The net of a cone is a circle and a sector.', True)]),

    61: L('A pyramid\'s volume is one third of base area × height. Its surface is the base plus the triangles.',
          [('Volume', '<p class="wt-key">V = (1/3) × base area × height</p>'),
           ('Example', '<p>Square base 6 cm, height 4 cm</p><p>V = (1/3) × 36 × 4 = <b>48 cm³</b></p>'),
           ('Surface area', '<p>Height of each triangle face (slant): √(4² + 3²) = 5 cm</p><p>4 triangles: 4 × ½ × 6 × 5 = 60 → Total = 36 + 60 = <b>96 cm²</b></p><p>The net of a square pyramid is a square with 4 triangles.</p>')],
          [fill('A pyramid has base area 30 cm² and height 10 cm.', 'V = {0} cm³', [['100']]),
           fill('Square base 9 cm, height 12 cm.', 'V = {0} cm³', [['324']], '(1/3) × 81 × 12'),
           fill('Square base 8 cm. Each triangular face has slant height 5 cm.', 'Total surface area = {0} cm²', [['144']], '64 + 4 × ½ × 8 × 5 = 64 + 80'),
           mcq('The net of a square-based pyramid has…', ['1 square and 4 triangles', '2 squares and 4 rectangles', '5 triangles'], '1 square and 4 triangles')]),

    62: L('A prism has the same cross-section all along. Volume = cross-section area × length.',
          [('Volume', '<p class="wt-key">V = area of cross-section × length</p><p>A cuboid and a cylinder are prisms too.</p>'),
           ('Triangular prism', '<p>Right triangle 3, 4, 5 cm; length 10 cm.</p><p>Cross-section = ½ × 3 × 4 = 6 cm² → V = 6 × 10 = <b>60 cm³</b></p>'),
           ('Surface area', '<p>2 triangles + 3 rectangles: 2 × 6 + (3 + 4 + 5) × 10 = 12 + 120 = <b>132 cm²</b></p><p>Tip: the rectangles together = perimeter of the cross-section × length.</p>')],
          [fill('A prism has cross-section 15 cm² and length 8 cm.', 'V = {0} cm³', [['120']]),
           fill('A cuboid is 5 × 4 × 3 cm.', 'V = {0} cm³', [['60']]),
           fill('A cuboid is 5 × 4 × 3 cm.', 'Surface area = {0} cm²', [['94']], '2(20 + 15 + 12) = 94'),
           fill('Triangular prism: right triangle with legs 6 and 8 (hypotenuse 10), length 5.', 'V = {0}, surface area = {1}', [['120'], ['168']], 'Cross-section 24 → V = 120. Area = 2 × 24 + 24 × 5 = 48 + 120.'),
           tf('A cylinder is a kind of prism with a circular cross-section.', True)]),

    63: L('A frustum is a cone with its top cut off. Volume = big cone − small cone.',
          [('Method', '<ol><li>Find the volume of the full cone</li><li>Find the volume of the small cone removed</li><li>Subtract</li></ol>'),
           ('Example', '<p>Full cone: r = 6, h = 8 → V = (1/3)π × 36 × 8 = 96π</p><p>Small cone: r = 3, h = 4 → V = (1/3)π × 9 × 4 = 12π</p><p>Frustum = 96π − 12π = <b>84π</b></p>'),
           ('Formula', '<p class="wt-key">V = (1/3)πh(R² + Rr + r²)</p><p>h = 4, R = 6, r = 3: (1/3)π × 4 × (36 + 18 + 9) = 84π ✓</p><p>Use similar triangles to find a missing height: r/R = h_small/h_big.</p>')],
          [fill('Big cone volume 200π, small cone removed 25π.', 'Frustum = {0}π', [['175']]),
           fill('A cone r = 10, h = 12 is cut halfway up. The small cone has r = {0} and h = {1}.', 'r = {0}, h = {1}', [['5'], ['6']]),
           fill('Then find the frustum volume (in terms of π).', 'V = {0}π', [['350']], 'Big: (1/3)×100×12 = 400π. Small: (1/3)×25×6 = 50π. 400π − 50π = 350π.'),
           mcq('A bucket is shaped like…', ['a frustum of a cone', 'a sphere', 'a pyramid'], 'a frustum of a cone')]),

    64: L('A frustum of a pyramid: the pyramid with the top cut off parallel to the base.',
          [('Volume by subtraction', '<p>Big pyramid: square base 6, h = 8 → V = (1/3) × 36 × 8 = 96</p><p>Small pyramid: base 3, h = 4 → V = 12</p><p>Frustum = <b>84</b></p>'),
           ('Formula', '<p class="wt-key">V = (h/3)(A₁ + A₂ + √(A₁A₂))</p><p>A₁ = 36, A₂ = 9, h = 4: (4/3)(36 + 9 + 18) = <b>84</b> ✓</p>'),
           ('Remember', '<p>A₁ and A₂ are the areas of the two parallel faces, h is the height between them.</p>')],
          [fill('Big pyramid volume 270 cm³, small pyramid cut off 10 cm³.', 'Frustum = {0} cm³', [['260']]),
           fill('A₁ = 16, A₂ = 4, h = 6. Use the formula.', 'V = {0}', [['56']], '(6/3)(16 + 4 + 8) = 2 × 28 = 56'),
           mcq('In the formula, A₁ and A₂ are…', ['the areas of the two parallel faces', 'two side faces', 'the heights'], 'the areas of the two parallel faces'),
           tf('The two parallel faces of a pyramid frustum are similar shapes.', True)]),
}
