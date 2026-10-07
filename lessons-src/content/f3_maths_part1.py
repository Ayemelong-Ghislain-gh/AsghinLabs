"""Form 3 Mathematics: algebra, variation, trigonometry (lessons 1-16)."""
from helpers import *


def table(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="mini"><tr>{h}</tr>{b}</table>'


def tri(a='A', b='B', c='C', sides=('', '', ''), angle='θ', marks=False):
    """Right triangle: right angle at C (bottom right), angle at A (bottom left), B on top.
    sides = (opposite BC, adjacent AC, hypotenuse AB)."""
    s = ('<polygon points="40,170 300,170 300,30" class="v-box"/>'
         '<rect x="286" y="156" width="14" height="14" class="v-line"/>'
         f'<text x="28" y="186" class="v-t">{a}</text><text x="306" y="26" class="v-t">{b}</text><text x="306" y="188" class="v-t">{c}</text>'
         f'<text x="82" y="162" class="v-t">{angle}</text>'
         f'<text x="318" y="105" class="v-s">{sides[0]}</text><text x="170" y="192" text-anchor="middle" class="v-s">{sides[1]}</text>'
         f'<text x="150" y="88" text-anchor="end" class="v-s">{sides[2]}</text>')
    if marks:
        s += marker(312, 120, 1) + marker(170, 158, 2) + marker(160, 105, 3)
    return svg(400, 200, s, 'right-angled triangle')


TRI_LABEL = tri(marks=True)
TRI_345 = tri(sides=('3', '4', '5'))

LESSONS = {
    1: L('Simplify by collecting like terms: terms with exactly the same letters and powers.',
         [('Like terms', '<div class="two-col"><div><b>Like</b>3x and 5x · 2ab and −ab · x² and 4x²</div><div><b>Not like</b>3x and 3y · x and x² · 5 and 5x</div></div>'
           '<p class="wt-key">Add or subtract the numbers in front (coefficients). The letters stay the same.</p>'),
          ('Collect like terms', '<p>4a + 3b − 2a + 5b<br>= (4a − 2a) + (3b + 5b)<br>= <b>2a + 8b</b></p>'),
          ('Multiply and divide', '<p>Multiply numbers, then letters:</p><p>3x × 4y = <b>12xy</b><br>2x × 3x = <b>6x²</b><br>12x² ÷ 4x = <b>3x</b></p>')],
         [sort('Is it a like term with 3x?', ['Like 3x', 'Not like 3x'], [('−7x', 'Like 3x'), ('3y', 'Not like 3x'), ('x', 'Like 3x'), ('3x²', 'Not like 3x'), ('10x', 'Like 3x'), ('3', 'Not like 3x')]),
          fill('Simplify.', '5x + 2x − 3x = {0}', [['4x']]),
          fill('Simplify.', '4a + 3b − 2a + 5b = {0}', [['2a+8b', '8b+2a']], 'Collect a-terms: 4a − 2a = 2a. Collect b-terms: 3b + 5b = 8b.'),
          mcq('Simplify 2x × 3x.', ['6x²', '6x', '5x²'], '6x²', '2 × 3 = 6 and x × x = x².'),
          fill('Simplify.', '15ab ÷ 5a = {0}', [['3b']], '15 ÷ 5 = 3, and a cancels.'),
          fill('Simplify.', '7y − 3y + 2 − 5 = {0}', [['4y-3', '4y−3']], 'y-terms: 4y. Numbers: 2 − 5 = −3.')]),

    3: L('Factorising is the reverse of expanding: take out the highest common factor (HCF).',
         [('Common factor', '<p>6x + 9: the HCF of 6x and 9 is <b>3</b>.</p><p>6x + 9 = <b>3(2x + 3)</b></p><p class="wt-key">Check by expanding: 3 × 2x + 3 × 3 = 6x + 9 ✓</p>'),
          ('Letters too', '<p>x² + 5x = <b>x(x + 5)</b><br>4ab − 6a = <b>2a(2b − 3)</b></p><p>Take the biggest number <b>and</b> the letters common to all terms.</p>'),
          ('Grouping (4 terms)', '<p>ax + ay + bx + by<br>= a(x + y) + b(x + y)<br>= <b>(x + y)(a + b)</b></p><p>Group in pairs, factorise each pair, then take out the common bracket.</p>')],
         [fill('What is the HCF of 8x and 12?', '{0}', [['4']]),
          fill('Factorise.', '5x + 10 = 5({0})', [['x+2']]),
          mcq('Factorise 2x² + 6x completely.', ['2x(x + 3)', '2(x² + 3x)', 'x(2x + 6)'], '2x(x + 3)', 'The HCF is 2x. The other answers are not complete.'),
          fill('Factorise.', '4ab − 6a = 2a({0})', [['2b-3', '2b−3']]),
          mcq('Factorise xy + 3x + 2y + 6.', ['(x + 2)(y + 3)', '(x + 3)(y + 2)', '(x + 6)(y + 1)'], '(x + 2)(y + 3)', 'x(y + 3) + 2(y + 3) = (x + 2)(y + 3).'),
          tf('3(2x + 3) is the factorised form of 6x + 9.', True, 'Expanding it gives 6x + 9.')]),

    5: L('The difference of two squares: a² − b² = (a + b)(a − b).',
         [('The rule', '<p class="wt-key">a² − b² = (a + b)(a − b)</p><p>Check: (a + b)(a − b) = a² − ab + ab − b² = a² − b² ✓</p>'),
          ('Examples', '<p>x² − 9 = x² − 3² = <b>(x + 3)(x − 3)</b><br>4x² − 25 = (2x)² − 5² = <b>(2x + 5)(2x − 5)</b><br>2x² − 18 = 2(x² − 9) = <b>2(x + 3)(x − 3)</b></p>'),
          ('A quick trick', '<p>51² − 49² = (51 + 49)(51 − 49) = 100 × 2 = <b>200</b></p>'),
          ('Watch out', '<p>x² + 9 is a <b>sum</b>, not a difference: it does not factorise this way.</p>')],
         [fill('Factorise.', 'x² − 16 = (x + {0})(x − {1})', [['4'], ['4']]),
          mcq('Factorise 9x² − 1.', ['(3x + 1)(3x − 1)', '(9x + 1)(x − 1)', '(3x − 1)²'], '(3x + 1)(3x − 1)', '9x² = (3x)² and 1 = 1².'),
          mcq('Factorise 2x² − 18 completely.', ['2(x + 3)(x − 3)', '(2x + 9)(x − 2)', '2(x² − 9)'], '2(x + 3)(x − 3)', 'First take out 2, then use the difference of two squares.'),
          fill('Use the trick to calculate.', '101² − 99² = {0}', [['400']], '(101 + 99)(101 − 99) = 200 × 2 = 400'),
          tf('x² + 4 factorises as (x + 2)(x − 2).', False, '(x + 2)(x − 2) = x² − 4, not x² + 4.')]),

    7: L('Direct variation: when x grows, y grows in the same ratio. Inverse variation: when x grows, y shrinks.',
         [('Direct variation', '<p>y ∝ x means <b>y = kx</b> (k is the constant).</p><p>y = 12 when x = 3 → k = 12 ÷ 3 = 4 → y = 4x.<br>When x = 5: y = <b>20</b>.</p>'),
          ('Inverse variation', '<p>y ∝ 1/x means <b>y = k/x</b>.</p><p>y = 6 when x = 4 → k = 6 × 4 = 24 → y = 24/x.<br>When x = 8: y = <b>3</b>.</p>'),
          ('Method', '<ol><li>Write the equation (y = kx or y = k/x)</li><li>Use the given values to find k</li><li>Use k to find the new value</li></ol>'),
          ('Other powers', '<p>y ∝ x² → y = kx². If y = 18 when x = 3: k = 18 ÷ 9 = 2. When x = 5: y = 2 × 25 = <b>50</b>.</p>')],
         [sort('Direct or inverse variation?', ['Direct', 'Inverse'], [('Cost of pens and number of pens bought', 'Direct'), ('Speed and time for the same journey', 'Inverse'), ('Number of workers and days to finish a job', 'Inverse'), ('Distance and time at constant speed', 'Direct')]),
          fill('y varies directly as x. y = 15 when x = 3.', 'k = {0}, and when x = 7, y = {1}', [['5'], ['35']]),
          fill('y varies inversely as x. y = 10 when x = 2.', 'k = {0}, and when x = 5, y = {1}', [['20'], ['4']]),
          fill('y varies as x². y = 12 when x = 2.', 'k = {0}, and when x = 3, y = {1}', [['3'], ['27']], 'k = 12 ÷ 4 = 3; y = 3 × 9 = 27.'),
          mcq('6 workers build a wall in 10 days. How long for 12 workers (same speed)?', ['5 days', '20 days', '12 days'], '5 days', 'Twice as many workers → half the time (inverse variation: k = 60).')]),

    9: L('To solve an equation, do the same thing to both sides until x is alone.',
         [('Balance', '<p>An equation is like a balance: whatever you do to one side, do to the other.</p><p>3x + 5 = 20<br>3x = 15 &nbsp;(−5 both sides)<br>x = <b>5</b> &nbsp;(÷3 both sides)</p>'),
          ('Brackets', '<p>2(x − 3) = 10<br>2x − 6 = 10<br>2x = 16<br>x = <b>8</b></p>'),
          ('x on both sides', '<p>5x − 4 = 3x + 6<br>5x − 3x = 6 + 4<br>2x = 10 → x = <b>5</b></p>'),
          ('Fractions', '<p>(2x + 1)/3 = 5 → multiply both sides by 3: 2x + 1 = 15 → x = <b>7</b></p><p class="wt-key">Always check: put your answer back into the equation.</p>')],
         [fill('Solve.', '3x + 5 = 20 → x = {0}', [['5']]),
          fill('Solve.', '2(x − 3) = 10 → x = {0}', [['8']]),
          fill('Solve.', '5x − 4 = 3x + 6 → x = {0}', [['5']]),
          fill('Solve.', 'x/4 + 1 = 3 → x = {0}', [['8']], 'x/4 = 2, so x = 8.'),
          fill('Solve.', '(2x + 1)/3 = 5 → x = {0}', [['7']]),
          order('Put the steps for solving 4x − 7 = 13 in order.', ['4x − 7 = 13', '4x = 20', 'x = 5', 'Check: 4 × 5 − 7 = 13 ✓'])]),

    11: L('Substitution: make one letter the subject of one equation, then put it into the other.',
          [('Method', '<ol><li>Make x or y the subject of one equation</li><li>Substitute into the other equation</li><li>Solve for one letter</li><li>Put it back to find the other</li><li>Check in both equations</li></ol>'),
           ('Example', '<p>y = 2x + 1 and 3x + y = 11</p><p>3x + (2x + 1) = 11<br>5x + 1 = 11 → x = 2<br>y = 2(2) + 1 = 5</p><p class="wt-key">x = 2, y = 5</p>'),
           ('Another one', '<p>x + y = 7 and x − y = 1</p><p>From the second: x = y + 1<br>(y + 1) + y = 7 → 2y = 6 → y = 3, x = 4</p>')],
          [order('Put the steps in order.', ['Make one letter the subject', 'Substitute into the other equation', 'Solve for one letter', 'Find the other letter', 'Check in both equations']),
           fill('Solve: y = x − 2 and 2x + 3y = 14.', 'x = {0}, y = {1}', [['4'], ['2']], '2x + 3(x − 2) = 14 → 5x − 6 = 14 → x = 4, y = 2.'),
           fill('Solve: y = 3x and x + y = 12.', 'x = {0}, y = {1}', [['3'], ['9']]),
           fill('Solve: x + y = 10 and x − y = 4.', 'x = {0}, y = {1}', [['7'], ['3']]),
           mcq('From 2x + y = 9, which is y as the subject?', ['y = 9 − 2x', 'y = 2x − 9', 'y = 9 + 2x'], 'y = 9 − 2x')]),

    12: L('Turn a story into an equation: name the unknown, write the equation, solve, then answer in words.',
          [('Steps', '<ol><li><b>Let</b> x = the unknown</li><li>Write the <b>equation</b> from the story</li><li><b>Solve</b> it</li><li><b>Check</b> and answer in a sentence</li></ol>'),
           ('Example 1', '<p>"I think of a number, multiply by 3 and add 4. I get 19."</p><p>3x + 4 = 19 → x = <b>5</b></p>'),
           ('Example 2', '<p>A book costs 3 times a pen. Together they cost 2000 FCFA.</p><p>Pen = x, book = 3x → x + 3x = 2000 → x = 500</p><p class="wt-key">Pen: 500 FCFA, book: 1500 FCFA</p>'),
           ('Two unknowns', '<p>Two numbers add up to 30 and differ by 6: x + y = 30, x − y = 6 → x = 18, y = 12.</p>')],
          [mcq('"A number doubled, minus 7, gives 15." Which equation?', ['2x − 7 = 15', '2(x − 7) = 15', 'x − 14 = 15'], '2x − 7 = 15'),
           fill('Solve that problem.', 'The number is {0}', [['11']]),
           fill('A father is 3 times as old as his son. Together they are 48.', 'Son: {0} years, father: {1} years', [['12'], ['36']], 'x + 3x = 48 → x = 12.'),
           fill('A rectangle has perimeter 30 cm. Its length is 3 cm more than its width.', 'width = {0} cm, length = {1} cm', [['6'], ['9']], '2(w + w + 3) = 30 → 4w + 6 = 30 → w = 6.'),
           fill('2 pens and 1 book cost 1500 FCFA. 1 pen and 1 book cost 1000 FCFA.', 'pen = {0} FCFA, book = {1} FCFA', [['500'], ['500']], 'Subtract: 1 pen = 500. Then book = 1000 − 500 = 500.')]),

    13: L('If A × B = 0, then A = 0 or B = 0. So factorise, then set each bracket to zero.',
          [('The key idea', '<p class="wt-key">If (x − 2)(x − 3) = 0 then x − 2 = 0 or x − 3 = 0.</p><p>So x = 2 or x = 3.</p>'),
           ('Method', '<ol><li>Make one side 0</li><li>Factorise</li><li>Set each factor to 0</li><li>Solve</li></ol>'),
           ('Examples', '<p>x² − 5x + 6 = 0 → (x − 2)(x − 3) = 0 → <b>x = 2 or 3</b></p><p>x² + 4x = 0 → x(x + 4) = 0 → <b>x = 0 or −4</b></p><p>x² − 9 = 0 → (x + 3)(x − 3) = 0 → <b>x = ±3</b></p>'),
           ('Careful', '<p>x² = 5x: do <b>not</b> divide by x (you lose x = 0). Write x² − 5x = 0 → x(x − 5) = 0 → x = 0 or 5.</p>')],
          [mcq('Solve (x − 4)(x + 1) = 0.', ['x = 4 or x = −1', 'x = −4 or x = 1', 'x = 4 only'], 'x = 4 or x = −1'),
           fill('Solve x² − 7x + 12 = 0 (smaller root first).', 'x = {0} or x = {1}', [['3'], ['4']], '(x − 3)(x − 4) = 0'),
           fill('Solve x² + x − 12 = 0 (smaller root first).', 'x = {0} or x = {1}', [['-4'], ['3']], '(x + 4)(x − 3) = 0'),
           mcq('Solve x² = 5x.', ['x = 0 or x = 5', 'x = 5 only', 'x = 0 only'], 'x = 0 or x = 5', 'x² − 5x = 0 → x(x − 5) = 0.'),
           fill('Solve x² − 25 = 0 (smaller root first).', 'x = {0} or x = {1}', [['-5'], ['5']]),
           order('Put the steps in order to solve x² − 3x = 10.', ['x² − 3x − 10 = 0', '(x − 5)(x + 2) = 0', 'x − 5 = 0 or x + 2 = 0', 'x = 5 or x = −2'])]),

    '13b': L('When you can\'t factorise, use the formula x = (−b ± √(b² − 4ac)) / 2a.',
             [('The formula', '<p>For ax² + bx + c = 0:</p><p class="wt-key">x = (−b ± √(b² − 4ac)) / 2a</p>'),
              ('Example', '<p>2x² + 3x − 2 = 0: a = 2, b = 3, c = −2</p><p>b² − 4ac = 9 − 4(2)(−2) = 9 + 16 = 25</p><p>x = (−3 ± 5) / 4 → x = <b>0.5</b> or x = <b>−2</b></p>'),
              ('The discriminant Δ = b² − 4ac', table(['Δ', 'Roots'], [['Δ > 0', 'two different roots'], ['Δ = 0', 'one (repeated) root'], ['Δ < 0', 'no real roots']])),
              ('Tips', '<ul><li>Put the equation in the form ax² + bx + c = 0 first</li><li>Keep the signs of b and c</li><li>Use brackets on the calculator: (−b + √Δ) ÷ (2a)</li></ul>')],
             [fill('In 3x² − 2x − 7 = 0, find a, b and c.', 'a = {0}, b = {1}, c = {2}', [['3'], ['-2'], ['-7']]),
              fill('For x² − 6x + 5 = 0, find the discriminant.', 'Δ = {0}', [['16']], '(−6)² − 4(1)(5) = 36 − 20 = 16'),
              fill('Now solve x² − 6x + 5 = 0 (smaller root first).', 'x = {0} or x = {1}', [['1'], ['5']], 'x = (6 ± 4) / 2'),
              mcq('How many real roots has x² + 4x + 4 = 0?', ['One (repeated)', 'Two', 'None'], 'One (repeated)', 'Δ = 16 − 16 = 0'),
              mcq('How many real roots has x² + x + 1 = 0?', ['None', 'One', 'Two'], 'None', 'Δ = 1 − 4 = −3 < 0'),
              tf('The quadratic formula works even when the equation does not factorise.', True)]),

    15: L('In a right-angled triangle: sin = opposite/hypotenuse, cos = adjacent/hypotenuse, tan = opposite/adjacent.',
          [('Name the sides', TRI_LABEL + '<ol><li><b>Opposite</b>: across from the angle θ</li><li><b>Adjacent</b>: next to θ (not the hypotenuse)</li><li><b>Hypotenuse</b>: the longest side, across from the right angle</li></ol>'),
           ('SOH CAH TOA', '<p class="wt-key">Sin = O/H · Cos = A/H · Tan = O/A</p>'),
           ('Example', TRI_345 + '<p>sin θ = 3/5 = 0.6 · cos θ = 4/5 = 0.8 · tan θ = 3/4 = 0.75</p>'),
           ('Complementary angles', '<p>Two angles that add up to 90° are complementary. Then:</p><p class="wt-key">sin θ = cos(90° − θ)</p><p>Example: sin 30° = cos 60°, sin 40° = cos 50°.</p>')],
          [label('Name the sides compared with the angle θ.', TRI_LABEL, ['Opposite', 'Adjacent', 'Hypotenuse']),
           match('Match each ratio to its formula.', [('sin θ', 'opposite / hypotenuse'), ('cos θ', 'adjacent / hypotenuse'), ('tan θ', 'opposite / adjacent')]),
           fill('In the 3-4-5 triangle, write each ratio as a decimal.', 'sin θ = {0}, cos θ = {1}, tan θ = {2}', [['0.6', '3/5'], ['0.8', '4/5'], ['0.75', '3/4']], visual=TRI_345),
           mcq('sin 40° is equal to…', ['cos 50°', 'cos 40°', 'tan 50°'], 'cos 50°', '40° + 50° = 90°.'),
           fill('Complete.', 'cos 25° = sin {0}°', [['65']]),
           tf('The hypotenuse is always the longest side.', True)]),

    16: L('Learn the exact values for 30°, 45° and 60°, and use a calculator in DEG mode for other angles.',
          [('Exact values', table(['', '30°', '45°', '60°'], [['sin', '1/2', '√2/2', '√3/2'], ['cos', '√3/2', '√2/2', '1/2'], ['tan', '√3/3', '1', '√3']])),
           ('How to remember', '<p>sin goes up: <b>√1/2, √2/2, √3/2</b> (30°, 45°, 60°). cos goes the other way.</p><p class="wt-key">tan = sin ÷ cos</p>'),
           ('Using the calculator', '<ul><li>Check the screen shows <b>D</b> or DEG (degrees)</li><li>sin 35° → press <b>sin 35 =</b> → 0.5736</li><li>Find an angle: sin θ = 0.5 → <b>SHIFT sin 0.5 =</b> → 30°</li></ul>')],
          [match('Match each value.', [('sin 30°', '1/2'), ('cos 30°', '√3/2'), ('tan 45°', '1'), ('tan 60°', '√3'), ('sin 45°', '√2/2')]),
           fill('Complete.', 'cos 60° = {0}', [['1/2', '0.5']]),
           fill('Find the angle.', 'If tan θ = 1, then θ = {0}°', [['45']]),
           fill('Find the angle.', 'If sin θ = 0.5, then θ = {0}°', [['30']]),
           mcq('Your calculator gives sin 30° = −0.988. What is wrong?', ['It is in RAD mode, not DEG', 'The battery is low', 'sin 30° is negative'], 'It is in RAD mode, not DEG', 'Switch to degrees (D on the screen).'),
           tf('sin 60° = cos 30°.', True, '60° and 30° are complementary.')]),
}
