"""Form 3 Mathematics: matrices, congruency and similarity, indices and logarithms (lessons 18-32)."""
from helpers import *
from f3_maths_part1 import table


def mat(rows):
    """A matrix written with brackets (CSS class .mat in style-lesson.css)."""
    n = len(rows[0])
    cells = ''.join(f'<span>{c}</span>' for r in rows for c in r)
    return f'<span class="mat" style="grid-template-columns:repeat({n},auto)">{cells}</span>'


A2 = mat([[1, 2], [3, 4]])
B2 = mat([[5, 6], [7, 8]])

THALES = svg(400, 220, ''.join([
    '<polygon points="200,15 30,200 370,200" class="v-box"/>',
    '<line x1="145" y1="75" x2="255" y2="75" class="v-arrow" style="marker-end:none"/>',
    '<text x="200" y="12" text-anchor="middle" class="v-t">A</text>',
    '<text x="18" y="214" class="v-t">B</text><text x="372" y="214" class="v-t">C</text>',
    '<text x="128" y="78" class="v-t">M</text><text x="262" y="78" class="v-t">N</text>',
    '<text x="200" y="68" text-anchor="middle" class="v-s">MN ∥ BC</text>',
]), 'Thales configuration')

SIM = svg(420, 150, ''.join([
    '<polygon points="20,130 110,130 20,70" class="v-box"/>',
    '<text x="65" y="146" text-anchor="middle" class="v-s">4</text><text x="8" y="104" class="v-s">3</text><text x="74" y="94" class="v-s">5</text>',
    '<polygon points="200,130 380,130 200,10" class="v-box2"/>',
    '<text x="290" y="146" text-anchor="middle" class="v-s">8</text><text x="186" y="74" class="v-s">6</text><text x="300" y="64" class="v-s">10</text>',
    '<text x="150" y="80" text-anchor="middle" class="v-t">×2</text>',
]), 'Two similar triangles')

LESSONS = {
    18: L('A matrix is a rectangular table of numbers. Its order is rows × columns.',
          [('Order', '<p>' + mat([[1, 2, 3], [4, 5, 6]]) + ' has 2 rows and 3 columns → order <b>2 × 3</b>.</p><p class="wt-key">Order = rows × columns (always rows first).</p>'),
           ('Elements', '<p>a<sub>ij</sub> is the element in row i, column j.</p><p>In the matrix above, a<sub>12</sub> = 2 and a<sub>21</sub> = 4.</p>'),
           ('Types', table(['Type', 'Example'], [['Row matrix', mat([[3, 1, 7]])], ['Column matrix', mat([[2], [5]])], ['Square matrix', mat([[1, 4], [2, 3]])], ['Zero (null) matrix', mat([[0, 0], [0, 0]])], ['Identity matrix I', mat([[1, 0], [0, 1]])], ['Diagonal matrix', mat([[3, 0], [0, 7]])]]))],
          [fill('What is the order of a matrix with 3 rows and 2 columns?', '{0} × {1}', [['3'], ['2']]),
           mcq('A matrix has order 1 × 4. It is a…', ['row matrix', 'column matrix', 'square matrix'], 'row matrix'),
           match('Match the matrix to its type.', [('[1 0 ; 0 1]', 'Identity matrix'), ('[0 0 ; 0 0]', 'Zero matrix'), ('[4 ; 9]', 'Column matrix'), ('[2 0 ; 0 5]', 'Diagonal matrix')], 'The ; separates rows.'),
           fill('In the matrix [ 7 2 9 ; 1 8 3 ], find:', 'a₁₃ = {0} and a₂₁ = {1}', [['9'], ['1']], 'Row first, then column.'),
           tf('A square matrix has the same number of rows and columns.', True)]),

    19: L('Add or subtract matrices of the same order element by element. A scalar multiplies every element.',
          [('Addition', '<p>' + mat([[2, 1], [3, 4]]) + ' + ' + mat([[1, 5], [0, 2]]) + ' = ' + mat([[3, 6], [3, 6]]) + '</p><p>Add elements in the same position.</p>'),
           ('Subtraction', '<p>' + mat([[2, 1], [3, 4]]) + ' − ' + mat([[1, 5], [0, 2]]) + ' = ' + mat([[1, -4], [3, 2]]) + '</p>'),
           ('Scalar multiplication', '<p>3 × ' + mat([[2, 1], [3, 4]]) + ' = ' + mat([[6, 3], [9, 12]]) + '</p><p class="wt-key">Matrices must have the same order to be added or subtracted.</p>')],
          [fill('A = [4 2 ; 1 3], B = [1 0 ; 5 2]. Find A + B.', '[ {0} {1} ; {2} {3} ]', [['5'], ['2'], ['6'], ['5']]),
           fill('Same A and B. Find A − B.', '[ {0} {1} ; {2} {3} ]', [['3'], ['2'], ['-4'], ['1']]),
           fill('Find 2A for A = [4 2 ; 1 3].', '[ {0} {1} ; {2} {3} ]', [['8'], ['4'], ['2'], ['6']]),
           mcq('Can you add a 2 × 3 matrix and a 3 × 2 matrix?', ['No: the orders are different', 'Yes, always', 'Only if they contain zeros'], 'No: the orders are different'),
           tf('A + B = B + A for matrices of the same order.', True)]),

    20: L('Multiply row by column: multiply matching elements and add.',
          [('When is it possible?', '<p>A (m × <b>n</b>) × B (<b>n</b> × p) → result is <b>m × p</b>.</p><p class="wt-key">Columns of A must equal rows of B.</p>'),
           ('Row × column', '<p>' + A2 + ' × ' + B2 + '</p><ul><li>Row 1 · column 1: 1×5 + 2×7 = 19</li><li>Row 1 · column 2: 1×6 + 2×8 = 22</li><li>Row 2 · column 1: 3×5 + 4×7 = 43</li><li>Row 2 · column 2: 3×6 + 4×8 = 50</li></ul><p>= ' + mat([[19, 22], [43, 50]]) + '</p>'),
           ('Order matters', '<p>B × A = ' + mat([[23, 34], [31, 46]]) + ' ≠ A × B</p><p class="wt-key">In general AB ≠ BA.</p>')],
          [mcq('A is 2 × 3 and B is 3 × 4. What is the order of AB?', ['2 × 4', '3 × 3', 'Not possible'], '2 × 4'),
           mcq('A is 2 × 3 and B is 2 × 3. Can you find AB?', ['No', 'Yes, it is 2 × 3', 'Yes, it is 3 × 3'], 'No', 'Columns of A (3) ≠ rows of B (2).'),
           fill('Find [2 1 ; 0 3] × [1 4 ; 2 1].', '[ {0} {1} ; {2} {3} ]', [['4'], ['9'], ['6'], ['3']], '2×1+1×2=4, 2×4+1×1=9, 0×1+3×2=6, 0×4+3×1=3'),
           fill('Find [1 2] × [3 ; 4] (row × column).', '{0}', [['11']], '1×3 + 2×4 = 11'),
           tf('For matrices, AB is always equal to BA.', False),
           mcq('What is A × I, where I is the identity matrix?', ['A', 'I', 'The zero matrix'], 'A', 'The identity matrix works like the number 1.')]),

    21: L('For a 2 × 2 matrix [a b ; c d]: transpose swaps rows and columns, det = ad − bc, adjoint = [d −b ; −c a].',
          [('Transpose Aᵀ', '<p>Rows become columns: ' + mat([[3, 2], [1, 4]]) + 'ᵀ = ' + mat([[3, 1], [2, 4]]) + '</p>'),
           ('Determinant', '<p>det ' + mat([['a', 'b'], ['c', 'd']]) + ' = <b>ad − bc</b></p><p>det ' + mat([[3, 2], [1, 4]]) + ' = 3×4 − 2×1 = <b>10</b></p>'),
           ('Adjoint', '<p>Swap a and d, change the signs of b and c:</p><p>adj ' + mat([[3, 2], [1, 4]]) + ' = ' + mat([[4, -2], [-1, 3]]) + '</p>')],
          [fill('Find the determinant of [5 3 ; 2 4].', 'det = {0}', [['14']], '5×4 − 3×2 = 20 − 6 = 14'),
           fill('Find the determinant of [2 −1 ; 3 4].', 'det = {0}', [['11']], '2×4 − (−1)(3) = 8 + 3 = 11'),
           fill('Find the adjoint of [5 3 ; 2 4].', '[ {0} {1} ; {2} {3} ]', [['4'], ['-3'], ['-2'], ['5']]),
           fill('Find the transpose of [1 7 ; 4 2].', '[ {0} {1} ; {2} {3} ]', [['1'], ['4'], ['7'], ['2']]),
           mcq('For [a b ; c d], the determinant is…', ['ad − bc', 'ab − cd', 'ac − bd'], 'ad − bc')]),

    22: L('A⁻¹ = (1/det A) × adj A. If det A = 0 the matrix has no inverse (it is singular).',
          [('The inverse', '<p>A × A⁻¹ = I</p><p class="wt-key">A⁻¹ = (1 / det A) × adj A</p>'),
           ('Example', '<p>A = ' + mat([[3, 5], [1, 2]]) + ': det = 6 − 5 = 1</p><p>adj A = ' + mat([[2, -5], [-1, 3]]) + ' so A⁻¹ = ' + mat([[2, -5], [-1, 3]]) + '</p>'),
           ('Singular matrix', '<p>det ' + mat([[2, 4], [1, 2]]) + ' = 4 − 4 = 0 → <b>no inverse</b>.</p>'),
           ('Solving equations', '<p>3x + 5y = 11 and x + 2y = 4 → ' + mat([[3, 5], [1, 2]]) + mat([['x'], ['y']]) + ' = ' + mat([[11], [4]]) + '</p><p>' + mat([['x'], ['y']]) + ' = A⁻¹' + mat([[11], [4]]) + ' = ' + mat([[2], [1]]) + ' → x = 2, y = 1</p>')],
          [fill('Find det of A = [4 3 ; 1 1].', 'det = {0}', [['1']]),
           fill('Then find A⁻¹ for A = [4 3 ; 1 1].', '[ {0} {1} ; {2} {3} ]', [['1'], ['-3'], ['-1'], ['4']], 'det = 1, so A⁻¹ = adj A.'),
           mcq('Which matrix has NO inverse?', ['[6 3 ; 4 2]', '[1 2 ; 3 4]', '[2 0 ; 0 2]'], '[6 3 ; 4 2]', 'det = 12 − 12 = 0.'),
           mcq('A = [4 7 ; 2 6] has det = 10. What is A⁻¹?', ['(1/10)[6 −7 ; −2 4]', '10[6 −7 ; −2 4]', '(1/10)[4 7 ; 2 6]'], '(1/10)[6 −7 ; −2 4]'),
           tf('A × A⁻¹ = I (the identity matrix).', True)]),

    23: L('Congruent figures have exactly the same shape and the same size.',
          [('Definition', '<p>Two figures are <b>congruent</b> if one fits exactly on top of the other (≅).</p><p>All corresponding sides and angles are equal.</p>'),
           ('Transformations', '<p><b>Translation</b>, <b>rotation</b> and <b>reflection</b> give congruent figures. An <b>enlargement</b> (scale factor ≠ 1) does not.</p>'),
           ('Corresponding parts', '<p>If ΔABC ≅ ΔPQR then AB = PQ, BC = QR, AC = PR and ∠A = ∠P, ∠B = ∠Q, ∠C = ∠R.</p><p class="wt-key">The order of the letters tells you which parts match.</p>')],
          [sort('Does it always give a congruent figure?', ['Congruent', 'Not congruent'], [('Translation', 'Congruent'), ('Rotation', 'Congruent'), ('Reflection', 'Congruent'), ('Enlargement by 2', 'Not congruent')]),
           mcq('ΔABC ≅ ΔXYZ. Which side is equal to BC?', ['YZ', 'XY', 'XZ'], 'YZ', 'B ↔ Y and C ↔ Z.'),
           mcq('ΔABC ≅ ΔXYZ and ∠B = 70°. Which angle is also 70°?', ['∠Y', '∠X', '∠Z'], '∠Y'),
           tf('Two squares with sides 4 cm and 5 cm are congruent.', False, 'Same shape but not the same size.')]),

    24: L('Two triangles are congruent if they satisfy one of four conditions: SSS, SAS, ASA or RHS.',
          [('The four conditions', table(['Case', 'Meaning'], [['SSS', '3 sides equal'], ['SAS', '2 sides and the angle between them'], ['ASA', '2 angles and the side between them'], ['RHS', 'Right angle, Hypotenuse and one Side']])),
           ('Not enough', '<ul><li><b>AAA</b>: same angles → similar, maybe different size</li><li><b>SSA</b>: the angle is not between the sides → not always congruent</li></ul>'),
           ('How to write a proof', '<ol><li>Name the triangles in matching order</li><li>Give 3 equal pairs with reasons</li><li>State the condition (e.g. SAS)</li></ol>')],
          [match('Match the condition to its meaning.', [('SSS', 'Three sides equal'), ('SAS', 'Two sides and the included angle'), ('ASA', 'Two angles and the included side'), ('RHS', 'Right angle, hypotenuse, one side')]),
           sort('Is it enough to prove congruence?', ['Enough', 'Not enough'], [('SSS', 'Enough'), ('AAA', 'Not enough'), ('SAS', 'Enough'), ('SSA', 'Not enough'), ('RHS', 'Enough')]),
           mcq('AB = DE, BC = EF and ∠B = ∠E. Which condition?', ['SAS', 'SSS', 'ASA'], 'SAS', '∠B is between AB and BC.'),
           mcq('Two right-angled triangles have equal hypotenuses and one other equal side. Which condition?', ['RHS', 'ASA', 'AAA'], 'RHS')]),

    25: L('Similar figures have the same shape: equal angles and sides in the same ratio k (scale factor).',
          [('Similar triangles', SIM + '<p>Every side is multiplied by <b>k = 2</b>. The angles stay the same.</p>'),
           ('Scale factor', '<p class="wt-key">k = new length ÷ old length</p><p>6 ÷ 3 = 8 ÷ 4 = 10 ÷ 5 = 2</p>'),
           ('Find a missing side', '<p>Triangle sides 4 and 6 are similar to sides 6 and x.</p><p>k = 6 ÷ 4 = 1.5 → x = 6 × 1.5 = <b>9</b></p>')],
          [fill('Find the scale factor from the small triangle to the big one.', 'k = {0}', [['2']], visual=SIM),
           fill('Two similar triangles: sides 5 cm and 8 cm ↔ 15 cm and x cm.', 'k = {0}, x = {1} cm', [['3'], ['24']]),
           tf('All squares are similar.', True, 'Their angles are all 90° and their sides keep the same ratio.'),
           tf('All rectangles are similar.', False, 'A 1 × 2 and a 1 × 5 rectangle have different shapes.'),
           mcq('Two triangles have the same three angles. They are…', ['similar', 'always congruent', 'neither'], 'similar')]),

    26: L('If lengths are multiplied by k, areas are multiplied by k² and volumes by k³.',
          [('The rule', table(['Lengths', 'Areas', 'Volumes'], [['× k', '× k²', '× k³'], ['× 2', '× 4', '× 8'], ['× 3', '× 9', '× 27']])),
           ('Area example', '<p>A shape of area 10 cm² is enlarged with k = 3.</p><p>New area = 10 × 3² = <b>90 cm²</b></p>'),
           ('Volume example', '<p>A box of volume 5 cm³ is enlarged with k = 2.</p><p>New volume = 5 × 2³ = <b>40 cm³</b></p><p class="wt-key">Lengths k, areas k², volumes k³.</p>')],
          [fill('Lengths are tripled. Areas are multiplied by…', '{0}', [['9']]),
           fill('Lengths are doubled. Volumes are multiplied by…', '{0}', [['8']]),
           fill('A photo of area 12 cm² is enlarged with scale factor 2.', 'New area = {0} cm²', [['48']]),
           fill('Two similar cubes: lengths in ratio 1 : 3. The small one has volume 4 cm³.', 'Big volume = {0} cm³', [['108']], '4 × 27 = 108'),
           mcq('Two similar shapes have areas 4 cm² and 25 cm². What is the length scale factor?', ['5/2', '25/4', '21'], '5/2', 'k² = 25/4, so k = 5/2.')]),

    27: L('Thales: a line parallel to one side of a triangle cuts the other two sides in the same ratio.',
          [('The property', THALES + '<p class="wt-key">If MN ∥ BC then AM/AB = AN/AC = MN/BC</p>'),
           ('Example', '<p>AM = 3, AB = 9, AN = 2, BC = 12.</p><p>Ratio = 3/9 = 1/3 → AC = 2 × 3 = <b>6</b>, MN = 12 ÷ 3 = <b>4</b></p>'),
           ('The converse', '<p>If AM/AB = AN/AC, then <b>MN ∥ BC</b>. We use it to prove that lines are parallel.</p>')],
          [fill('MN ∥ BC. AM = 4, AB = 12, BC = 15.', 'MN = {0}', [['5']], 'Ratio 4/12 = 1/3, so MN = 15/3 = 5.', visual=THALES),
           fill('MN ∥ BC. AM = 2, AB = 6, AN = 3.', 'AC = {0}', [['9']]),
           mcq('AM = 3, AB = 9, AN = 4, AC = 12. Is MN ∥ BC?', ['Yes, because 3/9 = 4/12', 'No', 'We cannot know'], 'Yes, because 3/9 = 4/12', 'This is the converse of Thales.'),
           tf('Thales\' property only works when MN is parallel to BC.', True)]),

    28: L('Similarity lets us find real sizes from models and maps, and compare areas and volumes.',
          [('Models and maps', '<p>A model car is made at scale 1 : 50. The model is 8 cm long → the real car is 8 × 50 = <b>400 cm = 4 m</b>.</p>'),
           ('Capacities', '<p>Two similar bottles: heights 10 cm and 20 cm (k = 2). The small one holds 0.5 L → the big one holds 0.5 × 2³ = <b>4 L</b>.</p>'),
           ('From areas to volumes', '<p>Areas in ratio 4 : 9 → lengths 2 : 3 (square root) → volumes 8 : 27 (cube).</p><p class="wt-key">Go back to the length ratio first.</p>')],
          [fill('A map has scale 1 : 100 000. 3 cm on the map is…', '{0} km in real life', [['3']], '3 × 100 000 = 300 000 cm = 3 km'),
           fill('Two similar jugs: heights 12 cm and 24 cm. The small one holds 1 litre.', 'The big one holds {0} litres', [['8']]),
           fill('Two similar solids have surface areas in ratio 9 : 25.', 'Lengths ratio 3 : {0}, volumes ratio 27 : {1}', [['5'], ['125']]),
           mcq('A model house is 1 : 20. The model\'s floor area is 300 cm². The real floor area is…', ['120 000 cm²', '6 000 cm²', '8 000 cm²'], '120 000 cm²', '300 × 20² = 300 × 400.')]),

    29: L('The laws of indices tell you what to do with powers when you multiply, divide or raise them.',
          [('The laws', table(['Law', 'Example'], [['aᵐ × aⁿ = aᵐ⁺ⁿ', '2³ × 2⁴ = 2⁷'], ['aᵐ ÷ aⁿ = aᵐ⁻ⁿ', '5⁶ ÷ 5² = 5⁴'], ['(aᵐ)ⁿ = aᵐⁿ', '(3²)³ = 3⁶'], ['a⁰ = 1', '7⁰ = 1'], ['a⁻ⁿ = 1/aⁿ', '2⁻³ = 1/8']])),
           ('Fractional indices', '<p>a<sup>1/n</sup> = ⁿ√a: 9<sup>1/2</sup> = 3, 8<sup>1/3</sup> = 2</p><p>a<sup>m/n</sup> = (ⁿ√a)ᵐ: 16<sup>3/4</sup> = (⁴√16)³ = 2³ = <b>8</b></p>'),
           ('Tip', '<p class="wt-key">Root first, then power: it keeps the numbers small.</p>')],
          [fill('Simplify, giving the answer as a power of 2.', '2³ × 2⁴ = 2^{0}', [['7']]),
           fill('Simplify.', 'x⁸ ÷ x³ = x^{0}', [['5']]),
           fill('Evaluate.', '5⁰ = {0}', [['1']]),
           fill('Evaluate.', '2⁻³ = 1/{0}', [['8']]),
           fill('Evaluate.', '27^(2/3) = {0}', [['9']], '∛27 = 3, then 3² = 9.'),
           mcq('Simplify (a²)³.', ['a⁶', 'a⁵', 'a⁸'], 'a⁶', 'Multiply the powers: 2 × 3 = 6.')]),

    30: L('To solve an exponential equation, write both sides as powers of the same base, then compare the powers.',
          [('Same base', '<p>2ˣ = 32 → 2ˣ = 2⁵ → <b>x = 5</b></p><p class="wt-key">If aᵐ = aⁿ then m = n.</p>'),
           ('More examples', '<p>3ˣ⁺¹ = 81 = 3⁴ → x + 1 = 4 → <b>x = 3</b></p><p>4ˣ = 8 → 2²ˣ = 2³ → 2x = 3 → <b>x = 3/2</b></p><p>9ˣ = 1/3 → 3²ˣ = 3⁻¹ → <b>x = −1/2</b></p>'),
           ('Useful powers', '<div class="chips"><span>2,4,8,16,32,64</span><span>3,9,27,81,243</span><span>5,25,125,625</span></div>')],
          [fill('Solve.', '3ˣ = 27 → x = {0}', [['3']]),
           fill('Solve.', '2ˣ = 64 → x = {0}', [['6']]),
           fill('Solve.', '5ˣ⁻¹ = 25 → x = {0}', [['3']]),
           fill('Solve.', '7ˣ = 1 → x = {0}', [['0']], '7⁰ = 1'),
           mcq('Solve 4ˣ = 32.', ['x = 5/2', 'x = 8', 'x = 5'], 'x = 5/2', '2²ˣ = 2⁵ → 2x = 5.'),
           mcq('Solve 2ˣ = 1/8.', ['x = −3', 'x = 3', 'x = 1/3'], 'x = −3')]),

    31: L('A logarithm answers: "what power?" log₂ 8 = 3 because 2³ = 8.',
          [('Definition', '<p class="wt-key">logₐ x = y ⟺ aʸ = x</p><p>log₁₀ 1000 = 3 because 10³ = 1000. "log" alone means base 10.</p>'),
           ('Laws', table(['Law', 'Example'], [['log(xy) = log x + log y', 'log 2 + log 5 = log 10 = 1'], ['log(x/y) = log x − log y', 'log 50 − log 5 = log 10 = 1'], ['log xⁿ = n log x', '2 log 3 = log 9'], ['logₐ a = 1', 'log₅ 5 = 1'], ['logₐ 1 = 0', 'log 1 = 0']])),
           ('Tip', '<p>Do not write log(x + y) = log x + log y: that is wrong!</p>')],
          [fill('Evaluate.', 'log₂ 16 = {0}', [['4']]),
           fill('Evaluate.', 'log₃ 81 = {0}', [['4']]),
           fill('Evaluate.', 'log 4 + log 25 = {0}', [['2']], 'log(4 × 25) = log 100 = 2'),
           fill('Evaluate.', 'log 80 − log 8 = {0}', [['1']]),
           mcq('Write 3 log 2 as a single log.', ['log 8', 'log 6', 'log 5'], 'log 8', '3 log 2 = log 2³'),
           tf('log(x + y) = log x + log y', False, 'The law is log(xy) = log x + log y.')]),

    32: L('Solve log equations by using the definition or by combining logs into one.',
          [('Use the definition', '<p>log₂ x = 5 → x = 2⁵ = <b>32</b></p><p>log₃(x − 1) = 2 → x − 1 = 9 → <b>x = 10</b></p>'),
           ('Combine first', '<p>log x + log 4 = log 20 → log 4x = log 20 → 4x = 20 → <b>x = 5</b></p><p>log(x + 2) + log 5 = 2 → 5(x + 2) = 100 → <b>x = 18</b></p>'),
           ('Unknown power', '<p>2ˣ = 5 → x = log 5 ÷ log 2 ≈ <b>2.32</b></p><p class="wt-key">Check: the number inside a log must be positive.</p>')],
          [fill('Solve.', 'log₂ x = 4 → x = {0}', [['16']]),
           fill('Solve.', 'log x = 3 → x = {0}', [['1000']]),
           fill('Solve.', 'log₅(x + 3) = 2 → x = {0}', [['22']]),
           fill('Solve.', 'log x + log 3 = log 12 → x = {0}', [['4']]),
           fill('Solve.', 'log x − log 2 = 1 → x = {0}', [['20']], 'log(x/2) = 1 → x/2 = 10.'),
           mcq('Solve 3ˣ = 10.', ['x = log 10 / log 3 ≈ 2.10', 'x = 10/3', 'x = 7'], 'x = log 10 / log 3 ≈ 2.10')]),
}
