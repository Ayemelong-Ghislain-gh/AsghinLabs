"""Form 3 Mathematics: vectors and sets (lessons 33-46)."""
from helpers import *
from f3_maths_part1 import table
from f3_maths_part2 import mat


def col(x, y):
    return mat([[x], [y]])


def grid_vec(x1, y1, x2, y2, name='', n=8, s=22):
    """Vector arrow drawn on a small square grid (grid units, y up)."""
    g = ''.join(f'<line x1="{10 + i * s}" y1="10" x2="{10 + i * s}" y2="{10 + n * s}" class="v-line"/>'
                f'<line x1="10" y1="{10 + i * s}" x2="{10 + n * s}" y2="{10 + i * s}" class="v-line"/>' for i in range(n + 1))
    X = lambda v: 10 + v * s
    Y = lambda v: 10 + (n - v) * s
    g += f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" class="v-arrow" style="stroke-width:3"/>'
    g += f'<circle cx="{X(x1)}" cy="{Y(y1)}" r="4" class="v-mk"/>'
    if name:
        g += f'<text x="{(X(x1) + X(x2)) / 2 - 14}" y="{(Y(y1) + Y(y2)) / 2 - 6}" class="v-t">{name}</text>'
    return svg(20 + n * s, 20 + n * s, g, 'vector on a grid')


VENN = svg(420, 230, ''.join([
    '<rect x="10" y="10" width="400" height="210" rx="10" class="v-line"/>',
    '<text x="26" y="34" class="v-t">U</text>',
    '<circle cx="165" cy="118" r="78" class="v-box" style="fill-opacity:.55"/>',
    '<circle cx="265" cy="118" r="78" class="v-box2" style="fill-opacity:.55"/>',
    '<text x="120" y="52" class="v-t">A</text><text x="300" y="52" class="v-t">B</text>',
    marker(130, 120, 1), marker(215, 120, 2), marker(300, 120, 3), marker(380, 200, 4),
]), 'Venn diagram with regions')


def venn_nums(a, ab, b, out, la='A', lb='B'):
    return svg(420, 230, ''.join([
        '<rect x="10" y="10" width="400" height="210" rx="10" class="v-line"/>',
        '<circle cx="165" cy="118" r="78" class="v-box" style="fill-opacity:.55"/>',
        '<circle cx="265" cy="118" r="78" class="v-box2" style="fill-opacity:.55"/>',
        f'<text x="110" y="52" class="v-t">{la}</text><text x="290" y="52" class="v-t">{lb}</text>',
        f'<text x="130" y="124" text-anchor="middle" class="v-t">{a}</text><text x="215" y="124" text-anchor="middle" class="v-t">{ab}</text>',
        f'<text x="300" y="124" text-anchor="middle" class="v-t">{b}</text><text x="380" y="206" text-anchor="middle" class="v-t">{out}</text>',
    ]), 'Venn diagram with numbers')


LESSONS = {
    33: L('A scalar has only a size. A vector has a size and a direction.',
          [('Scalar or vector?', '<div class="two-col"><div><b>Scalar</b>mass, time, speed, temperature, distance</div><div><b>Vector</b>displacement, velocity, force, acceleration</div></div>'),
           ('Representation', grid_vec(1, 1, 5, 4, 'a') + '<p>A vector is drawn as an arrow: the length is its size, the arrow shows its direction.</p>'),
           ('Notation', '<ul><li>With letters: <b>AB</b> with an arrow on top, or bold <b>a</b> (underlined a in your book)</li><li>As a column vector: a = ' + col(4, 3) + ' → 4 right, 3 up</li></ul><p class="wt-key">Top number: horizontal (x). Bottom number: vertical (y).</p>')],
          [sort('Scalar or vector?', ['Scalar', 'Vector'], [('Mass', 'Scalar'), ('Velocity', 'Vector'), ('Temperature', 'Scalar'), ('Force', 'Vector'), ('Speed', 'Scalar'), ('Displacement', 'Vector')]),
           fill('Write the column vector of the arrow (right, then up).', '( {0} , {1} )', [['4'], ['3']], visual=grid_vec(1, 1, 5, 4, 'a')),
           fill('Write the column vector of this arrow.', '( {0} , {1} )', [['3'], ['-2']], 'It goes 3 right and 2 down.', visual=grid_vec(2, 6, 5, 4, 'b')),
           mcq('The vector (−2, 5) means…', ['2 left and 5 up', '2 right and 5 down', '5 left and 2 up'], '2 left and 5 up'),
           tf('Speed is a vector.', False, 'Speed has no direction. Velocity is the vector.')]),

    34: L('A position vector starts at the origin O. A free vector can be drawn anywhere; a localized vector is fixed to a point.',
          [('Position vectors', '<p>The position vector of A(3, 2) is <b>OA</b> = ' + col(3, 2) + '. Same numbers as the coordinates.</p>'),
           ('Vector between two points', '<p class="wt-key">AB = OB − OA</p><p>A(1, 2), B(4, 6): AB = ' + col(4, 6) + ' − ' + col(1, 2) + ' = ' + col(3, 4) + '</p>'),
           ('Free and localized', '<div class="two-col"><div><b>Free vector</b>can be moved anywhere: only size and direction matter</div><div><b>Localized vector</b>tied to a starting point or line (e.g. a force applied at one point)</div></div>')],
          [fill('Write the position vector of P(−2, 5).', 'OP = ( {0} , {1} )', [['-2'], ['5']]),
           fill('A(2, 1) and B(7, 4). Find AB.', 'AB = ( {0} , {1} )', [['5'], ['3']]),
           fill('A(3, 5) and B(1, 2). Find AB.', 'AB = ( {0} , {1} )', [['-2'], ['-3']]),
           mcq('AB = OB − OA. Then BA = …', ['OA − OB', 'OA + OB', 'OB − OA'], 'OA − OB'),
           tf('A position vector always starts at the origin.', True)]),

    35: L('Add or subtract vectors component by component. Equal vectors have the same size and direction.',
          [('Equal vectors', '<p>Two vectors are <b>equal</b> if they have the same components, wherever they are drawn.</p><p>' + col(2, 3) + ' = ' + col('x', 3) + ' → x = 2</p>'),
           ('Addition', '<p>' + col(2, 3) + ' + ' + col(4, -1) + ' = ' + col(6, 2) + '</p><p class="wt-key">Triangle law: AB + BC = AC</p>'),
           ('Subtraction and negative', '<p>' + col(2, 3) + ' − ' + col(4, -1) + ' = ' + col(-2, 4) + '</p><p>BA = −AB: same size, opposite direction.</p>')],
          [fill('a = (3, 1), b = (2, 5). Find a + b.', '( {0} , {1} )', [['5'], ['6']]),
           fill('a = (3, 1), b = (2, 5). Find a − b.', '( {0} , {1} )', [['1'], ['-4']]),
           fill('AB = (4, −2). Find BA.', '( {0} , {1} )', [['-4'], ['2']]),
           mcq('AB + BC = ?', ['AC', 'CA', 'BA'], 'AC', 'Go from A to B, then B to C: you end up going from A to C.'),
           fill('(x, 5) = (7, y). Find x and y.', 'x = {0}, y = {1}', [['7'], ['5']])]),

    36: L('Multiplying by a scalar stretches a vector. The dot product of two vectors gives a number.',
          [('Scalar multiplication', '<p>3 × ' + col(2, -1) + ' = ' + col(6, -3) + '</p><p>If b = k a, then a and b are <b>parallel</b>.</p>'),
           ('Dot product', '<p class="wt-key">' + col('x₁', 'y₁') + ' · ' + col('x₂', 'y₂') + ' = x₁x₂ + y₁y₂</p><p>' + col(2, 3) + ' · ' + col(4, -1) + ' = 8 − 3 = <b>5</b></p>'),
           ('Perpendicular vectors', '<p>If a · b = 0, the vectors are <b>perpendicular</b>.</p><p>' + col(1, 2) + ' · ' + col(4, -2) + ' = 4 − 4 = 0 ✓</p>')],
          [fill('Find 4 × (3, −2).', '( {0} , {1} )', [['12'], ['-8']]),
           fill('Find (3, 1) · (2, 5).', '{0}', [['11']]),
           fill('Find (−2, 3) · (4, 1).', '{0}', [['-5']]),
           mcq('Which vector is perpendicular to (3, 2)?', ['(2, −3)', '(3, 2)', '(6, 4)'], '(2, −3)', '3 × 2 + 2 × (−3) = 0'),
           mcq('Which vector is parallel to (2, 5)?', ['(6, 15)', '(5, 2)', '(2, −5)'], '(6, 15)', '(6, 15) = 3 × (2, 5).')]),

    37: L('The magnitude of (x, y) is √(x² + y²). Its direction is the angle it makes, found with tan.',
          [('Magnitude', '<p class="wt-key">|a| = √(x² + y²)</p><p>|(3, 4)| = √(9 + 16) = √25 = <b>5</b></p><p>It is Pythagoras\' theorem!</p>'),
           ('Distance between points', '<p>A(1, 2), B(7, 10): AB = (6, 8) → |AB| = √(36 + 64) = <b>10</b></p>'),
           ('Direction and sense', '<p>Direction: the angle θ with the x-axis, tan θ = y/x. (1, 1) → θ = 45°.</p><p><b>Sense</b>: which way it points along that line. AB and BA have the same direction but opposite sense.</p>')],
          [fill('Find the magnitude.', '|(6, 8)| = {0}', [['10']]),
           fill('Find the magnitude.', '|(5, 12)| = {0}', [['13']]),
           fill('A(2, 3), B(5, 7). Find |AB|.', '{0}', [['5']], 'AB = (3, 4), |AB| = 5.'),
           fill('The vector (1, 1) makes an angle of … with the x-axis.', '{0}°', [['45']]),
           tf('AB and BA have the same magnitude.', True, 'Only the sense is opposite.')]),

    38: L('Numbers belong to sets: ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ. Each set contains the one before it.',
          [('The sets', table(['Set', 'Contains', 'Examples'], [['ℕ natural', '0, 1, 2, 3, …', '0, 7, 100'], ['ℤ integers', '… −2, −1, 0, 1, 2 …', '−5, 0, 3'], ['ℚ rationals', 'fractions a/b (b ≠ 0)', '3/4, −0.5, 2'], ['ℝ reals', 'all numbers on the number line', '√2, π, 1.5']])),
           ('Nested sets', svg(420, 170, ''.join([
               '<rect x="10" y="10" width="400" height="150" rx="16" class="v-box3"/><text x="30" y="36" class="v-t">ℝ</text>',
               '<rect x="40" y="40" width="300" height="110" rx="14" class="v-box2"/><text x="58" y="64" class="v-t">ℚ</text>',
               '<rect x="80" y="70" width="190" height="70" rx="12" class="v-box"/><text x="96" y="94" class="v-t">ℤ</text>',
               '<rect x="140" y="92" width="100" height="40" rx="10" class="v-box2"/><text x="190" y="117" text-anchor="middle" class="v-t">ℕ</text>',
               '<text x="375" y="100" text-anchor="middle" class="v-s">√2, π</text>',
           ]), 'Nested number sets') + '<p class="wt-key">ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ</p>'),
           ('Irrational numbers', '<p>Numbers in ℝ but not in ℚ: they cannot be written as a fraction. Examples: √2, √3, π.</p>')],
          [sort('What is the smallest set the number belongs to?', ['ℕ', 'ℤ', 'ℚ', 'ℝ'], [('5', 'ℕ'), ('−3', 'ℤ'), ('3/4', 'ℚ'), ('√2', 'ℝ'), ('0', 'ℕ'), ('−0.5', 'ℚ'), ('π', 'ℝ')]),
           tf('Every integer is a rational number.', True, 'For example 3 = 3/1.'),
           tf('√9 is irrational.', False, '√9 = 3, which is a natural number.'),
           mcq('Which is irrational?', ['√5', '0.25', '−7'], '√5'),
           order('Put the sets from smallest to biggest.', ['ℕ', 'ℤ', 'ℚ', 'ℝ'])]),

    39: L('A set is closed under an operation if the answer is always in the same set.',
          [('Closure', '<p>ℕ is closed under addition: natural + natural is always natural (2 + 3 = 5).</p><p>ℕ is <b>not</b> closed under subtraction: 2 − 5 = −3 ∉ ℕ.</p>'),
           ('Summary', table(['', '+', '−', '×', '÷'], [['ℕ', '✓', '✗', '✓', '✗'], ['ℤ', '✓', '✓', '✓', '✗'], ['ℚ', '✓', '✓', '✓', '✓ (not ÷ 0)'], ['ℝ', '✓', '✓', '✓', '✓ (not ÷ 0)']])),
           ('One counter-example is enough', '<p class="wt-key">To show a set is not closed, give one example that fails: 1 ÷ 2 = 0.5 ∉ ℤ.</p>')],
          [tf('ℕ is closed under multiplication.', True),
           tf('ℤ is closed under division.', False, '1 ÷ 2 = 0.5 is not an integer.'),
           mcq('Which example shows that ℕ is not closed under subtraction?', ['3 − 7 = −4', '7 − 3 = 4', '5 − 5 = 0'], '3 − 7 = −4'),
           mcq('In which set is subtraction always possible?', ['ℤ', 'ℕ', 'Neither'], 'ℤ'),
           tf('ℚ is closed under addition.', True)]),

    40: L('Sets have their own language: ∈, ∉, ⊂, ∅ and three ways to describe a set.',
          [('Symbols', table(['Symbol', 'Meaning'], [['∈', 'is an element of'], ['∉', 'is not an element of'], ['⊂', 'is a subset of'], ['∅ or { }', 'empty set'], ['n(A)', 'number of elements of A']])),
           ('Describing a set', '<ul><li><b>Listing</b>: A = {2, 4, 6, 8}</li><li><b>Words</b>: A = {even numbers between 1 and 9}</li><li><b>Set-builder</b>: A = {x : x is even, 1 &lt; x &lt; 9}</li></ul>'),
           ('Example', '<p>A = {2, 4, 6, 8}: 4 ∈ A, 5 ∉ A, {2, 4} ⊂ A, n(A) = 4</p>')],
          [match('Match the symbol to its meaning.', [('∈', 'is an element of'), ('∉', 'is not an element of'), ('⊂', 'is a subset of'), ('∅', 'the empty set')]),
           mcq('A = {1, 3, 5, 7}. Which is true?', ['3 ∈ A', '4 ∈ A', '7 ∉ A'], '3 ∈ A'),
           fill('List the set {x : x is a whole number, 2 < x < 7}.', '{ {0}, {1}, {2}, {3} }', [['3'], ['4'], ['5'], ['6']]),
           fill('B = {a, e, i, o, u}.', 'n(B) = {0}', [['5']]),
           tf('{2, 4} ⊂ {1, 2, 3, 4}', True)]),

    41: L('Sets can be finite, infinite, empty or singletons. Equal sets have the same elements; equivalent sets have the same number of elements.',
          [('Types', table(['Type', 'Example'], [['Finite', '{days of the week}'], ['Infinite', 'ℕ = {0, 1, 2, …}'], ['Empty (null) ∅', '{months with 40 days}'], ['Singleton', '{5}: one element']])),
           ('Equal vs equivalent', '<div class="two-col"><div><b>Equal</b> A = B<br>same elements: {1, 2, 3} = {3, 1, 2}</div><div><b>Equivalent</b> A ↔ B<br>same number: {a, b, c} ↔ {1, 2, 3}</div></div>'),
           ('Remember', '<p class="wt-key">Equal sets are always equivalent, but equivalent sets are not always equal.</p>')],
          [sort('Finite or infinite?', ['Finite', 'Infinite'], [('{students in your class}', 'Finite'), ('{even numbers}', 'Infinite'), ('{letters of the alphabet}', 'Finite'), ('{points on a line}', 'Infinite')]),
           match('Match each set to its type.', [('{0}', 'Singleton'), ('{ }', 'Empty set'), ('{1, 2, 3, …}', 'Infinite'), ('{red, green, blue}', 'Finite with 3 elements')]),
           mcq('{a, b, c} and {x, y, z} are…', ['equivalent', 'equal', 'neither'], 'equivalent'),
           tf('{1, 2, 3} and {3, 2, 1} are equal sets.', True, 'Order does not matter.'),
           tf('{0} is the empty set.', False, '{0} has one element: the number 0. It is a singleton.')]),

    42: L('The universal set U contains everything we are talking about. The complement A\' is everything in U that is not in A.',
          [('Universal set', '<p>U = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}</p>'),
           ('Complement', '<p>A = {even numbers in U} = {2, 4, 6, 8, 10}</p><p>A\' = {1, 3, 5, 7, 9}</p><p class="wt-key">n(A) + n(A\') = n(U)</p>'),
           ('Relative complement', '<p>A − B (or A \\ B): elements of A that are not in B.</p><p>A = {1, 2, 3, 4}, B = {3, 4, 5} → A − B = {1, 2}, B − A = {5}</p>')],
          [fill('U = {1, …, 8}, A = {1, 2, 3}. List A\'.', '{ {0}, {1}, {2}, {3}, {4} }', [['4'], ['5'], ['6'], ['7'], ['8']]),
           fill('n(U) = 30 and n(A) = 12.', 'n(A\') = {0}', [['18']]),
           mcq('A = {a, b, c, d}, B = {c, d, e}. A − B = ?', ['{a, b}', '{e}', '{c, d}'], '{a, b}'),
           mcq('Same sets. B − A = ?', ['{e}', '{a, b}', '{a, b, e}'], '{e}'),
           tf('(A\')\' = A', True, 'The complement of the complement is the set itself.')]),

    43: L('n(A) counts the elements. A set with n elements has 2ⁿ subsets, and they form its power set.',
          [('Cardinality', '<p>A = {red, green, blue} → <b>n(A) = 3</b></p>'),
           ('Subsets', '<p>B ⊂ A if every element of B is in A. ∅ and A itself are always subsets of A.</p>'),
           ('Power set', '<p>A = {a, b}: P(A) = { ∅, {a}, {b}, {a, b} } → 4 subsets</p><p class="wt-key">Number of subsets = 2ⁿ · proper subsets = 2ⁿ − 1</p>')],
          [fill('A = {1, 2, 3}. How many subsets?', '{0}', [['8']], '2³ = 8'),
           fill('A set has 4 elements. How many subsets?', '{0}', [['16']]),
           fill('A set has 5 elements. How many proper subsets?', '{0}', [['31']], '2⁵ − 1 = 31'),
           tf('The empty set is a subset of every set.', True),
           mcq('Which is NOT a subset of {1, 2, 3}?', ['{4}', '{1, 3}', '∅'], '{4}')]),

    44: L('A ∩ B (intersection) is what is in both. A ∪ B (union) is what is in at least one.',
          [('Intersection and union', '<p>A = {1, 2, 3, 4}, B = {3, 4, 5, 6}</p><p>A ∩ B = <b>{3, 4}</b><br>A ∪ B = <b>{1, 2, 3, 4, 5, 6}</b></p>'),
           ('Disjoint sets', '<p>A ∩ B = ∅: no element in common. {odd numbers} and {even numbers} are disjoint.</p>'),
           ('Counting formula', '<p class="wt-key">n(A ∪ B) = n(A) + n(B) − n(A ∩ B)</p><p>We subtract the overlap because it was counted twice.</p>')],
          [mcq('A = {a, b, c}, B = {b, c, d}. A ∩ B = ?', ['{b, c}', '{a, b, c, d}', '{a, d}'], '{b, c}'),
           mcq('Same sets. A ∪ B = ?', ['{a, b, c, d}', '{b, c}', '{a, b, b, c, c, d}'], '{a, b, c, d}', 'Each element is written only once.'),
           fill('n(A) = 10, n(B) = 8, n(A ∩ B) = 3.', 'n(A ∪ B) = {0}', [['15']]),
           fill('n(A ∪ B) = 20, n(A) = 12, n(B) = 11.', 'n(A ∩ B) = {0}', [['3']]),
           tf('{1, 3, 5} and {2, 4, 6} are disjoint.', True)]),

    45: L('A Venn diagram shows sets as circles inside a rectangle U. De Morgan\'s laws link ∪, ∩ and complements.',
          [('The regions', VENN + '<ol><li>A only: A ∩ B\'</li><li>Both: A ∩ B</li><li>B only: A\' ∩ B</li><li>Neither: (A ∪ B)\'</li></ol>'),
           ('De Morgan\'s laws', '<p class="wt-key">(A ∪ B)\' = A\' ∩ B\'</p><p class="wt-key">(A ∩ B)\' = A\' ∪ B\'</p><p>"Not in A or B" = "not in A and not in B".</p>')],
          [label('Name each region.', VENN, ['A only', 'A ∩ B', 'B only', '(A ∪ B)\'']),
           mcq('(A ∪ B)\' is equal to…', ['A\' ∩ B\'', 'A\' ∪ B\'', 'A ∩ B'], 'A\' ∩ B\''),
           mcq('(A ∩ B)\' is equal to…', ['A\' ∪ B\'', 'A\' ∩ B\'', 'A ∪ B'], 'A\' ∪ B\''),
           fill('Use the Venn diagram.', 'n(A) = {0}, n(A ∪ B) = {1}, n(A ∪ B)\' = {2}', [['9'], ['15'], ['5']], 'n(A) = 6 + 3; n(A ∪ B) = 6 + 3 + 6.', visual=venn_nums(6, 3, 6, 5))]),

    46: L('Venn diagrams solve counting problems: fill the middle first, then work outwards.',
          [('Method', '<ol><li>Draw U and two circles</li><li>Put the number in <b>both</b> first</li><li>Subtract to get "A only" and "B only"</li><li>Subtract from the total to get "neither"</li></ol>'),
           ('Example', '<p>30 students: 18 play football (F), 15 basketball (B), 7 play both.</p>' + venn_nums(11, 7, 8, 4, 'F', 'B') +
            '<p>F only = 18 − 7 = 11 · B only = 15 − 7 = 8 · neither = 30 − 26 = 4</p>'),
           ('Unknown overlap', '<p>40 people: 25 drink tea, 20 coffee, 10 neither.</p><p>Tea or coffee = 40 − 10 = 30 → both = 25 + 20 − 30 = <b>15</b></p><p class="wt-key">n(A ∩ B) = n(A) + n(B) − n(A ∪ B)</p>')],
          [fill('50 students: 30 study French, 25 Spanish, 10 both.', 'French only = {0}, Spanish only = {1}, neither = {2}', [['20'], ['15'], ['5']]),
           fill('35 people: 20 like rice, 18 like beans, 5 like neither.', 'Both = {0}', [['8']], 'Rice or beans = 30. Both = 20 + 18 − 30 = 8.'),
           order('Put the steps in order.', ['Draw U and two circles', 'Write the number in both', 'Find the "only" parts', 'Find the "neither" part']),
           mcq('In a class of 40, 22 like maths, 25 like science and every student likes at least one. How many like both?', ['7', '3', '47'], '7', '22 + 25 − 40 = 7.')]),
}
