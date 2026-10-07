"""Form 5 Mathematics: logic, loci and geometrical construction (lessons 46-56)."""
from helpers import *
from f3_maths_part1 import table

TT = table(['p', 'q', '~p', 'p ∧ q', 'p ∨ q', 'p ⇒ q', 'p ⇔ q'], [
    ['T', 'T', 'F', 'T', 'T', 'T', 'T'],
    ['T', 'F', 'F', 'F', 'T', 'F', 'F'],
    ['F', 'T', 'T', 'F', 'T', 'T', 'F'],
    ['F', 'F', 'T', 'F', 'F', 'T', 'T']])


def compass(inner, label):
    return svg(420, 220, inner, label)


def _arc(cx, cy, r, a1, a2):
    import math
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f}" class="v-line" style="fill:none;stroke-width:2"/>'


PERP_BISECTOR = svg(420, 250, ''.join([
    '<line x1="110" y1="130" x2="310" y2="130" class="v-line" style="stroke-width:3"/>',
    '<circle cx="110" cy="130" r="4" class="v-mk"/><circle cx="310" cy="130" r="4" class="v-mk"/>',
    '<text x="92" y="150" class="v-t">A</text><text x="316" y="150" class="v-t">B</text>',
    _arc(110, 130, 130, -55, -25), _arc(110, 130, 130, 25, 55),
    _arc(310, 130, 130, 205, 235), _arc(310, 130, 130, 125, 155),
    '<line x1="210" y1="20" x2="210" y2="240" class="v-arrow" style="marker-end:none;stroke-width:2"/>',
    '<text x="220" y="125" class="v-s">M (midpoint)</text>',
]), 'Perpendicular bisector construction')

INCIRCLE = compass(''.join([
    '<polygon points="60,200 360,200 160,30" class="v-box" style="fill-opacity:.35"/>',
    '<circle cx="177" cy="133" r="67" class="v-line" style="fill:none;stroke-width:2"/>',
    '<circle cx="177" cy="133" r="4" class="v-mk"/><text x="185" y="129" class="v-s">I</text>',
    '<line x1="60" y1="200" x2="177" y2="133" class="v-line" style="stroke-dasharray:5 4"/>',
    '<line x1="360" y1="200" x2="177" y2="133" class="v-line" style="stroke-dasharray:5 4"/>',
    '<line x1="160" y1="30" x2="177" y2="133" class="v-line" style="stroke-dasharray:5 4"/>',
    '<text x="183" y="180" class="v-s">r</text><line x1="177" y1="133" x2="177" y2="200" class="v-line"/>',
]), 'Inscribed circle of a triangle')

CIRCUM = svg(420, 280, ''.join([
    '<polygon points="100,170 320,170 170,60" class="v-box" style="fill-opacity:.35"/>',
    '<circle cx="210" cy="163" r="110" class="v-line" style="fill:none;stroke-width:2"/>',
    '<circle cx="210" cy="163" r="4" class="v-mk"/><text x="218" y="159" class="v-s">O</text>',
]), 'Circumscribed circle')

LESSONS = {
    46: L('A proposition is a statement that is either true or false. We combine propositions with "not", "and", "or".',
          [('Proposition', '<p>"Yaoundé is the capital of Cameroon" → true. "7 is even" → false.</p><p>Not propositions: questions ("Are you ready?"), orders ("Sit down!").</p>'),
           ('Connectives', table(['Symbol', 'Name', 'Read', 'True when'], [['~p', 'negation', 'not p', 'p is false'], ['p ∧ q', 'conjunction', 'p and q', 'both are true'], ['p ∨ q', 'disjunction', 'p or q', 'at least one is true']])),
           ('Example', '<p>p: "It rains", q: "I stay home"</p><p>p ∧ q: "It rains and I stay home" · ~p: "It does not rain"</p>')],
          [sort('Is it a proposition?', ['Proposition', 'Not a proposition'], [('5 + 3 = 8', 'Proposition'), ('Close the door!', 'Not a proposition'), ('Paris is in Africa', 'Proposition'), ('What time is it?', 'Not a proposition')]),
           mcq('p: "x is even". ~p is…', ['x is not even', 'x is odd and even', 'x is even'], 'x is not even'),
           mcq('p is true and q is false. p ∧ q is…', ['false', 'true'], 'false'),
           mcq('p is true and q is false. p ∨ q is…', ['true', 'false'], 'true'),
           tf('"2 is a prime number" is a true proposition.', True)]),

    47: L('p ⇒ q ("if p then q") is false only when p is true and q is false. p ⇔ q is true when p and q have the same truth value.',
          [('Implication p ⇒ q', table(['p', 'q', 'p ⇒ q'], [['T', 'T', 'T'], ['T', 'F', 'F'], ['F', 'T', 'T'], ['F', 'F', 'T']]) + '<p class="wt-key">A promise is only broken when p happens and q does not.</p>'),
           ('Bi-implication p ⇔ q', '<p>"p if and only if q": true when both are true or both are false.</p>'),
           ('Example', '<p>"If it rains, the ground is wet." Rain and dry ground → false. No rain → the statement is true whatever the ground.</p>')],
          [mcq('p: T, q: F. p ⇒ q is…', ['F', 'T'], 'F'),
           mcq('p: F, q: F. p ⇒ q is…', ['T', 'F'], 'T'),
           mcq('p: F, q: T. p ⇔ q is…', ['F', 'T'], 'F'),
           mcq('"If 2 + 2 = 5, then the moon is cheese." Truth value?', ['True (false premise)', 'False'], 'True (false premise)', 'An implication with a false "if" part is true.'),
           tf('p ⇔ q is true when p and q are both false.', True)]),

    48: L('A truth table lists every combination of truth values. With n propositions there are 2ⁿ rows.',
          [('The main table', TT),
           ('Building a table', '<ol><li>Write all combinations of p, q (2² = 4 rows)</li><li>Add a column for each part</li><li>Work from the inside out</li></ol><p class="wt-key">3 propositions → 8 rows</p>')],
          [fill('How many rows for p, q, r?', '{0}', [['8']]),
           fill('Complete ~(p ∧ q) for the rows TT, TF, FT, FF.', '{0}, {1}, {2}, {3}', [['F'], ['T'], ['T'], ['T']]),
           fill('Complete ~p ∨ q for the rows TT, TF, FT, FF.', '{0}, {1}, {2}, {3}', [['T'], ['F'], ['T'], ['T']], 'It is the same as p ⇒ q!'),
           mcq('A statement that is true in every row is called…', ['a tautology', 'a contradiction', 'a negation'], 'a tautology'),
           mcq('p ∧ ~p is always…', ['false (a contradiction)', 'true', 'the same as p'], 'false (a contradiction)')]),

    49: L('From p ⇒ q we get the converse, the inverse and the contrapositive. Only the contrapositive always has the same truth value.',
          [('Four statements', table(['Name', 'Form', 'Example'], [['Conditional', 'p ⇒ q', 'If it is a square, it is a rectangle'], ['Converse', 'q ⇒ p', 'If it is a rectangle, it is a square'], ['Inverse', '~p ⇒ ~q', 'If it is not a square, it is not a rectangle'], ['Contrapositive', '~q ⇒ ~p', 'If it is not a rectangle, it is not a square']])),
           ('Key fact', '<p class="wt-key">p ⇒ q ≡ ~q ⇒ ~p (contrapositive)</p><p>In the example, the conditional and contrapositive are true; the converse and inverse are false.</p>')],
          [match('Match each form to its name.', [('q ⇒ p', 'Converse'), ('~p ⇒ ~q', 'Inverse'), ('~q ⇒ ~p', 'Contrapositive')]),
           mcq('Contrapositive of "If x = 2 then x² = 4"?', ['If x² ≠ 4 then x ≠ 2', 'If x² = 4 then x = 2', 'If x ≠ 2 then x² ≠ 4'], 'If x² ≠ 4 then x ≠ 2'),
           tf('The converse of a true statement is always true.', False, '"If x = 2 then x² = 4" is true, but its converse fails for x = −2.'),
           tf('A statement and its contrapositive always have the same truth value.', True)]),

    50: L('Two statements are logically equivalent (≡) if their truth tables are identical. De Morgan\'s laws are the most useful.',
          [('De Morgan\'s laws', '<p class="wt-key">~(p ∧ q) ≡ ~p ∨ ~q</p><p class="wt-key">~(p ∨ q) ≡ ~p ∧ ~q</p><p>"Not (rich and famous)" = "not rich or not famous".</p>'),
           ('Other laws', table(['Law', 'Equivalence'], [['Double negation', '~(~p) ≡ p'], ['Implication', 'p ⇒ q ≡ ~p ∨ q'], ['Contrapositive', 'p ⇒ q ≡ ~q ⇒ ~p'], ['Commutative', 'p ∧ q ≡ q ∧ p']])),
           ('Same idea as sets', '<p>(A ∪ B)\' = A\' ∩ B\' — the same pattern with sets.</p>')],
          [mcq('~(p ∨ q) ≡ ?', ['~p ∧ ~q', '~p ∨ ~q', 'p ∧ q'], '~p ∧ ~q'),
           mcq('~(p ∧ q) ≡ ?', ['~p ∨ ~q', '~p ∧ ~q', 'p ∨ q'], '~p ∨ ~q'),
           mcq('Negate "Awa is tall and Paul is short."', ['Awa is not tall or Paul is not short.', 'Awa is not tall and Paul is not short.', 'Awa is short and Paul is tall.'], 'Awa is not tall or Paul is not short.'),
           mcq('p ⇒ q ≡ ?', ['~p ∨ q', 'p ∨ ~q', '~p ∧ q'], '~p ∨ q'),
           tf('~(~p) ≡ p', True)]),

    51: L('A locus is the set of all points that satisfy a condition.',
          [('The four basic loci', table(['Condition', 'Locus'], [['Fixed distance r from a point O', 'circle, centre O, radius r'], ['Equidistant from two points A and B', 'perpendicular bisector of AB'], ['Equidistant from two intersecting lines', 'the bisectors of the angles'], ['Fixed distance d from a straight line', 'two parallel lines at distance d']])),
           ('Regions', '<p>"Less than 3 cm from O" → inside the circle. "Nearer A than B" → the side of the perpendicular bisector containing A.</p><p class="wt-key">Solid line if the boundary is included, dashed if not.</p>')],
          [match('Match the condition to its locus.', [('5 cm from a point P', 'A circle of radius 5 cm'), ('Same distance from A and B', 'Perpendicular bisector of AB'), ('Same distance from two crossing roads', 'Angle bisectors'), ('2 m from a straight wall', 'Two parallel lines')]),
           mcq('A goat is tied to a post with a 4 m rope. The region it can reach is…', ['inside a circle of radius 4 m', 'a square', 'a straight line'], 'inside a circle of radius 4 m'),
           mcq('A water point must be equally far from two villages. Where?', ['On the perpendicular bisector between them', 'In one village', 'On the line joining them only'], 'On the perpendicular bisector between them'),
           tf('The locus of points 3 cm from a point is a circle.', True)]),

    52: L('With a ruler and compasses you can bisect a segment, bisect an angle and drop a perpendicular.',
          [('Perpendicular bisector of AB', PERP_BISECTOR + '<ol><li>Open the compasses to more than half of AB</li><li>Draw arcs from A, above and below</li><li>Same radius, draw arcs from B</li><li>Join the two crossing points</li></ol>'),
           ('Bisect an angle', '<ol><li>From the vertex, draw an arc cutting both arms</li><li>From each cut, draw arcs that cross inside the angle</li><li>Join the vertex to the crossing point</li></ol>'),
           ('Perpendicular from a point P to a line', '<ol><li>From P, draw an arc cutting the line twice</li><li>From each cut, draw arcs crossing on the other side</li><li>Join P to the crossing point</li></ol><p class="wt-key">Never rub out construction arcs: they show your method.</p>')],
          [order('Put the steps for the perpendicular bisector of AB in order.', ['Open compasses to more than half of AB', 'Draw arcs above and below from A', 'Draw arcs with the same radius from B', 'Join the two crossing points']),
           order('Put the steps for bisecting an angle in order.', ['Draw an arc from the vertex cutting both arms', 'Draw arcs from the two cuts', 'Join the vertex to where the arcs cross']),
           mcq('Why must the compass radius be more than half of AB?', ['So the arcs cross', 'So the line is longer', 'It doesn\'t matter'], 'So the arcs cross'),
           tf('You should rub out your construction arcs at the end.', False)]),

    53: L('Construct 60° with an equilateral triangle, then bisect to get 30°, 15°… Construct 90° with a perpendicular, then bisect for 45°.',
          [('60°', '<ol><li>Draw a line and mark a point A</li><li>Arc from A cutting the line at B</li><li>Same radius, arc from B cutting the first arc at C</li><li>Join AC: ∠CAB = 60°</li></ol>'),
           ('Other angles', table(['Angle', 'How'], [['30°', 'bisect 60°'], ['90°', 'perpendicular at a point'], ['45°', 'bisect 90°'], ['120°', '60° + 60° (two arcs along)'], ['75°', '60° + 15° (or bisect 60° and 90°)'], ['135°', '90° + 45°']]))],
          [match('How do you construct it?', [('30°', 'Bisect 60°'), ('45°', 'Bisect 90°'), ('120°', 'Two 60° steps'), ('15°', 'Bisect 30°')]),
           order('Put the steps to construct 60° in order.', ['Draw a line and mark A', 'Draw an arc from A cutting the line at B', 'With the same radius draw an arc from B', 'Join A to the crossing point']),
           mcq('Which angle can be made by bisecting the angle between 60° and 90°?', ['75°', '70°', '80°'], '75°'),
           tf('The construction of 60° uses an equilateral triangle.', True)]),

    54: L('Construct triangles from SSS, SAS or ASA data, and quadrilaterals by splitting them into triangles.',
          [('SSS (three sides)', '<ol><li>Draw the longest side AB</li><li>Arc from A with radius AC</li><li>Arc from B with radius BC</li><li>Join to the crossing point C</li></ol>'),
           ('SAS and ASA', '<p>SAS: draw a side, construct the angle, measure the second side.<br>ASA: draw the side, construct both angles at its ends; where the arms meet is the third vertex.</p>'),
           ('Quadrilaterals', '<p>Draw a diagonal first, then build the two triangles on it.</p><p class="wt-key">Always make a rough sketch with the measurements first.</p>')],
          [order('Construct a triangle with sides 7, 5 and 4 cm (SSS).', ['Draw AB = 7 cm', 'Arc of radius 5 cm from A', 'Arc of radius 4 cm from B', 'Join A and B to the crossing point']),
           mcq('Sides 3 cm, 4 cm and 9 cm: can you construct the triangle?', ['No: 3 + 4 < 9', 'Yes', 'Only with a protractor'], 'No: 3 + 4 < 9', 'Two sides together must be longer than the third.'),
           match('Which data is it?', [('AB = 6 cm, ∠A = 60°, AC = 5 cm', 'SAS'), ('AB = 6 cm, ∠A = 45°, ∠B = 60°', 'ASA'), ('AB = 6, BC = 5, CA = 4', 'SSS')]),
           tf('A rough sketch helps you plan a construction.', True)]),

    55: L('The circumscribed circle passes through the 3 vertices. Its centre is where the perpendicular bisectors of the sides meet.',
          [('Method', CIRCUM + '<ol><li>Construct the perpendicular bisector of two sides</li><li>They meet at O, the circumcentre</li><li>Radius = OA; draw the circle through A, B, C</li></ol>'),
           ('Facts', '<ul><li>O is equidistant from A, B and C</li><li>Acute triangle: O inside · right triangle: O on the hypotenuse · obtuse: O outside</li></ul>')],
          [order('Put the steps in order.', ['Construct the perpendicular bisector of AB', 'Construct the perpendicular bisector of BC', 'Mark O where they meet', 'Draw the circle with centre O through A']),
           mcq('The circumcentre is equidistant from…', ['the three vertices', 'the three sides', 'the midpoints only'], 'the three vertices'),
           mcq('For a right-angled triangle, the circumcentre is…', ['the midpoint of the hypotenuse', 'inside the triangle', 'outside the triangle'], 'the midpoint of the hypotenuse'),
           mcq('Three villages want one mobile mast at the same distance from each. Where?', ['At the circumcentre of the triangle', 'In the biggest village', 'At the incentre'], 'At the circumcentre of the triangle')]),

    56: L('The inscribed circle touches all 3 sides. Its centre is where the angle bisectors meet. Concentric circles share the same centre.',
          [('Method', INCIRCLE + '<ol><li>Bisect two angles of the triangle</li><li>They meet at I, the incentre</li><li>Draw a perpendicular from I to one side: that length is r</li><li>Draw the circle, centre I, radius r</li></ol>'),
           ('Concentric circles', '<p>Circles with the <b>same centre</b> and different radii, like the rings of a target. The region between them is an annulus: area = π(R² − r²).</p>')],
          [order('Put the steps in order.', ['Bisect angle A', 'Bisect angle B', 'Mark I where the bisectors meet', 'Drop a perpendicular from I to a side', 'Draw the circle, centre I']),
           mcq('The incentre is equidistant from…', ['the three sides', 'the three vertices', 'the circumcentre'], 'the three sides'),
           match('Which centre?', [('Meeting point of angle bisectors', 'Incentre'), ('Meeting point of perpendicular bisectors', 'Circumcentre')]),
           fill('Concentric circles with radii 5 and 3. In terms of π.', 'Area between them = {0}', [['16π', '16pi']]),
           tf('Concentric circles have the same centre.', True)]),
}
