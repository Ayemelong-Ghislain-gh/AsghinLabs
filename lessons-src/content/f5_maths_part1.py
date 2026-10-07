"""Form 5 Mathematics: coordinate geometry (lessons 1-10)."""
from helpers import *
from f3_maths_part1 import table


def plot(curves, xr=(-3, 5), yr=(-5, 6), points=(), hlines=(), labels=(), shade=None, s=28):
    """Coordinate grid with curves. curves: list of (function, class); points: (x, y, text)."""
    x0, x1 = xr; y0, y1 = yr
    W, H = (x1 - x0) * s + 30, (y1 - y0) * s + 30
    X = lambda x: 15 + (x - x0) * s
    Y = lambda y: 15 + (y1 - y) * s
    g = ''
    for x in range(x0, x1 + 1):
        g += f'<line x1="{X(x)}" y1="{Y(y0)}" x2="{X(x)}" y2="{Y(y1)}" class="v-line" style="opacity:.25"/>'
    for y in range(y0, y1 + 1):
        g += f'<line x1="{X(x0)}" y1="{Y(y)}" x2="{X(x1)}" y2="{Y(y)}" class="v-line" style="opacity:.25"/>'
    g += f'<line x1="{X(x0)}" y1="{Y(0)}" x2="{X(x1)}" y2="{Y(0)}" class="v-line" style="stroke-width:2"/>'
    g += f'<line x1="{X(0)}" y1="{Y(y0)}" x2="{X(0)}" y2="{Y(y1)}" class="v-line" style="stroke-width:2"/>'
    for x in range(x0, x1 + 1):
        if x: g += f'<text x="{X(x)}" y="{Y(0) + 14}" text-anchor="middle" class="v-s" style="font-size:10px">{x}</text>'
    for y in range(y0, y1 + 1):
        if y: g += f'<text x="{X(0) - 5}" y="{Y(y) + 4}" text-anchor="end" class="v-s" style="font-size:10px">{y}</text>'
    if shade:
        a, b = shade
        g += f'<rect x="{X(a)}" y="{Y(0) - 4}" width="{X(b) - X(a)}" height="8" rx="4" class="v-box3"/>'
    for y, cls in hlines:
        g += f'<line x1="{X(x0)}" y1="{Y(y)}" x2="{X(x1)}" y2="{Y(y)}" class="v-arrow" style="marker-end:none;stroke-dasharray:6 4"/>'
    colours = ['#00d4ff', '#ffb648', '#2ee68b']
    for i, f in enumerate(curves):
        pts, n = [], 200
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n
            y = f(x)
            if y0 - 1 <= y <= y1 + 1: pts.append(f'{X(x):.1f},{Y(y):.1f}')
        g += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colours[i % 3]}" stroke-width="3"/>'
    for x, y, t in points:
        g += f'<circle cx="{X(x)}" cy="{Y(y)}" r="5" class="v-mk"/><text x="{X(x) + 8}" y="{Y(y) - 8}" class="v-t" style="font-size:12px">{t}</text>'
    for x, y, t in labels:
        g += f'<text x="{X(x)}" y="{Y(y)}" class="v-t" style="font-size:12px">{t}</text>'
    return svg(W, H, g, 'graph')


PARA = plot([lambda x: x * x - 2 * x - 3], xr=(-3, 5), yr=(-5, 6), points=[(1, -4, 'vertex (1, −4)'), (-1, 0, ''), (3, 0, '')])
PARA_INEQ = plot([lambda x: x * x - 2 * x - 3], xr=(-3, 5), yr=(-5, 6), shade=(-1, 3))
PARA_LINE = plot([lambda x: x * x - 2 * x - 3], xr=(-3, 5), yr=(-5, 6), hlines=[(5, '')], points=[(-2, 5, ''), (4, 5, '')])
TWO_LINES = plot([lambda x: x + 1, lambda x: -x + 5], xr=(-1, 6), yr=(-1, 6), points=[(2, 3, '(2, 3)')])
LINE = plot([lambda x: 2 * x - 1], xr=(-2, 4), yr=(-4, 6), points=[(0, -1, '(0, −1)'), (2, 3, '(2, 3)')])

LESSONS = {
    1: L('A point P divides AB in the ratio m : n. Inside the segment it is internal division, outside it is external.',
         [('Internal division', '<p>AP : PB = m : n, with A(x₁, y₁) and B(x₂, y₂):</p><p class="wt-key">P = ( (n x₁ + m x₂)/(m + n) , (n y₁ + m y₂)/(m + n) )</p>'),
          ('Example', '<p>A(1, 2), B(7, 8), ratio 1 : 2</p><p>x = (2×1 + 1×7)/3 = 3, y = (2×2 + 1×8)/3 = 4 → <b>P(3, 4)</b></p><p>Check: P is one third of the way from A to B.</p>'),
          ('External division', '<p>P is outside AB:</p><p class="wt-key">P = ( (m x₂ − n x₁)/(m − n) , (m y₂ − n y₁)/(m − n) )</p><p>A(1, 2), B(4, 5), ratio 2 : 1 → P = (8 − 1, 10 − 2) = <b>(7, 8)</b></p>')],
         [fill('A(0, 0), B(6, 9). P divides AB internally in the ratio 1 : 2.', 'P( {0} , {1} )', [['2'], ['3']]),
          fill('A(2, 1), B(10, 5). P divides AB internally in the ratio 3 : 1.', 'P( {0} , {1} )', [['8'], ['4']], 'x = (1×2 + 3×10)/4 = 8, y = (1×1 + 3×5)/4 = 4'),
          fill('A(1, 1), B(3, 4). P divides AB externally in the ratio 2 : 1.', 'P( {0} , {1} )', [['5'], ['7']], 'x = (2×3 − 1×1)/1 = 5, y = (2×4 − 1×1)/1 = 7'),
          mcq('The midpoint divides AB internally in the ratio…', ['1 : 1', '1 : 2', '2 : 1'], '1 : 1'),
          tf('In external division, P lies outside the segment AB.', True)]),

    2: L('Distance AB = √((x₂ − x₁)² + (y₂ − y₁)²). Midpoint = average of the coordinates.',
         [('Distance', '<p class="wt-key">AB = √((x₂ − x₁)² + (y₂ − y₁)²)</p><p>A(1, 2), B(4, 6): AB = √(3² + 4²) = √25 = <b>5</b></p><p>It is Pythagoras on the grid.</p>'),
          ('Midpoint', '<p class="wt-key">M = ( (x₁ + x₂)/2 , (y₁ + y₂)/2 )</p><p>(2, 3) and (8, 7) → M = <b>(5, 5)</b></p>'),
          ('Uses', '<ul><li>Is a triangle isosceles? Compare side lengths.</li><li>Centre of a circle = midpoint of a diameter.</li></ul>')],
         [fill('Find AB for A(2, 1) and B(8, 9).', 'AB = {0}', [['10']]),
          fill('Find AB for A(−1, 3) and B(4, −9).', 'AB = {0}', [['13']], '√(5² + 12²) = 13'),
          fill('Midpoint of (−2, 4) and (6, 10).', 'M( {0} , {1} )', [['2'], ['7']]),
          fill('M(3, 5) is the midpoint of AB. A(1, 2).', 'B( {0} , {1} )', [['5'], ['8']], 'B = (2×3 − 1, 2×5 − 2)'),
          mcq('A(0, 0), B(3, 4), C(6, 0). The triangle is…', ['isosceles (AB = BC = 5)', 'equilateral', 'right-angled at B'], 'isosceles (AB = BC = 5)')]),

    3: L('The gradient m = (y₂ − y₁)/(x₂ − x₁) measures steepness. Points are collinear if the gradients are equal.',
         [('Gradient', '<p class="wt-key">m = rise / run = (y₂ − y₁)/(x₂ − x₁)</p><p>(1, 2) and (3, 8): m = 6/2 = <b>3</b></p>'),
          ('Signs', table(['m', 'Line'], [['positive', 'goes up ↗'], ['negative', 'goes down ↘'], ['0', 'horizontal'], ['undefined', 'vertical']])),
          ('Collinear points', '<p>A(1, 1), B(2, 3), C(4, 7): m(AB) = 2, m(BC) = 4/2 = 2 → equal → <b>A, B, C are collinear</b> (on one line).</p>')],
         [fill('Gradient through (2, 5) and (6, 13).', 'm = {0}', [['2']]),
          fill('Gradient through (−1, 4) and (3, −4).', 'm = {0}', [['-2']]),
          mcq('A line has gradient 0. It is…', ['horizontal', 'vertical', 'at 45°'], 'horizontal'),
          mcq('Are A(0, 1), B(1, 3), C(3, 7) collinear?', ['Yes: m(AB) = m(BC) = 2', 'No', 'Only A and B'], 'Yes: m(AB) = m(BC) = 2'),
          fill('Points (1, 2), (3, 6) and (5, k) are collinear.', 'k = {0}', [['10']], 'The gradient is 2, so from x = 3 to 5, y increases by 4.')]),

    4: L('Equation of a line: y − y₁ = m(x − x₁). With two points, find m first.',
         [('Gradient and a point', '<p class="wt-key">y − y₁ = m(x − x₁)</p><p>m = 2 through (1, 3): y − 3 = 2(x − 1) → <b>y = 2x + 1</b></p>'),
          ('Two points', '<p>(1, 2) and (3, 8): m = 3 → y − 2 = 3(x − 1) → <b>y = 3x − 1</b></p><p>Check with (3, 8): 3×3 − 1 = 8 ✓</p>'),
          ('Forms', '<p>y = mx + c (gradient m, y-intercept c) or ax + by + c = 0.</p>')],
          [mcq('Line with gradient 4 through (0, −3)?', ['y = 4x − 3', 'y = −3x + 4', 'y = 4x + 3'], 'y = 4x − 3'),
           mcq('Line with gradient −2 through (1, 5)?', ['y = −2x + 7', 'y = −2x + 5', 'y = 2x + 3'], 'y = −2x + 7', 'y − 5 = −2(x − 1)'),
           fill('Line through (2, 3) and (4, 11) is y = mx + c.', 'm = {0}, c = {1}', [['4'], ['-5']]),
           fill('What are the gradient and y-intercept of y = 5x − 2?', 'm = {0}, c = {1}', [['5'], ['-2']]),
           tf('The point (2, 7) is on y = 3x + 1.', True, '3 × 2 + 1 = 7')]),

    5: L('Parallel lines have equal gradients. Perpendicular lines have gradients that multiply to −1.',
         [('Rules', '<p class="wt-key">Parallel: m₁ = m₂ · Perpendicular: m₁ × m₂ = −1</p><p>Perpendicular gradient: flip and change sign. m = 2 → −1/2.</p>'),
          ('Example', '<p>Line perpendicular to y = 2x + 1 through (2, 3):</p><p>m = −1/2 → y − 3 = −½(x − 2) → <b>y = −½x + 4</b></p>')],
         [mcq('Which line is parallel to y = 3x − 2?', ['y = 3x + 5', 'y = −3x + 2', 'y = x/3'], 'y = 3x + 5'),
          fill('A line has gradient 4. A perpendicular line has gradient…', '{0}', [['-1/4', '-0.25']]),
          fill('A line has gradient −2/3. A perpendicular line has gradient…', '{0}', [['3/2', '1.5']]),
          mcq('Line through (0, 1) parallel to y = −x + 7?', ['y = −x + 1', 'y = x + 1', 'y = −x + 7'], 'y = −x + 1'),
          tf('y = 2x + 1 and y = −½x + 3 are perpendicular.', True, '2 × (−½) = −1')]),

    6: L('y = mx + c is a straight line. Make a table of values, plot the points and join them.',
         [('Table of values', '<p>y = 2x − 1</p>' + table(['x', '−1', '0', '1', '2', '3'], [['y', '−3', '−1', '1', '3', '5']])),
          ('The graph', LINE + '<p>Gradient 2 (up 2 for every 1 across), y-intercept −1.</p>'),
          ('Intercepts', '<p>y-intercept: put x = 0 → y = −1. x-intercept: put y = 0 → 2x − 1 = 0 → x = ½.</p><p class="wt-key">Three points are enough: if they line up, your table is right.</p>')],
         [fill('y = 3x + 2. Complete the table.', 'x = 0 → y = {0}; x = 2 → y = {1}; x = −1 → y = {2}', [['2'], ['8'], ['-1']]),
          fill('Find the x-intercept of y = 2x − 6.', 'x = {0}', [['3']]),
          mcq('Which point is on the line in the graph?', ['(1, 1)', '(1, 2)', '(0, 1)'], '(1, 1)', visual=LINE),
          mcq('y = −x + 4 goes…', ['down from left to right', 'up from left to right', 'horizontally'], 'down from left to right')]),

    7: L('The solution of two simultaneous equations is the point where their lines cross.',
         [('Method', '<ol><li>Draw both lines on the same axes</li><li>Read the intersection point</li><li>x and y of that point are the solution</li></ol>'),
          ('Example', '<p>y = x + 1 and y = −x + 5</p>' + TWO_LINES + '<p class="wt-key">They cross at (2, 3) → x = 2, y = 3</p>'),
          ('Special cases', '<ul><li>Parallel lines → no solution</li><li>Same line → infinitely many solutions</li></ul>')],
         [fill('Read the solution from the graph.', 'x = {0}, y = {1}', [['2'], ['3']], visual=TWO_LINES),
          mcq('y = 2x + 1 and y = 2x − 3 have…', ['no solution (parallel lines)', 'one solution', 'two solutions'], 'no solution (parallel lines)'),
          fill('Check algebraically: y = x + 2 and y = 8 − x cross at…', '( {0} , {1} )', [['3'], ['5']]),
          tf('A graphical solution may only be approximate.', True, 'Reading a graph is less exact than algebra.')]),

    8: L('y = ax² + bx + c is a parabola: a U-shaped (or ∩-shaped) curve.',
         [('Table of values', '<p>y = x² − 2x − 3</p>' + table(['x', '−2', '−1', '0', '1', '2', '3', '4'], [['y', '5', '0', '−3', '−4', '−3', '0', '5']])),
          ('The curve', PARA + '<p>Join the points with a <b>smooth curve</b>, not straight lines.</p>'),
          ('Tips', '<ul><li>Use brackets for negatives: (−2)² = 4</li><li>The table is symmetric around the vertex</li></ul>')],
         [fill('y = x² − 2x − 3. Find y when x = −2.', 'y = {0}', [['5']], '4 + 4 − 3 = 5'),
          fill('y = x² + 1. Complete.', 'x = −3 → y = {0}; x = 0 → y = {1}', [['10'], ['1']]),
          mcq('Should the points of a parabola be joined with a ruler?', ['No, with a smooth curve', 'Yes', 'Only the middle ones'], 'No, with a smooth curve'),
          fill('y = 2x² − 3x. Find y when x = 2.', 'y = {0}', [['2']])]),

    9: L('Study a parabola: its direction, axis of symmetry, vertex, roots and y-intercept.',
         [('Direction', '<div class="two-col"><div><b>a &gt; 0</b>opens up ∪, has a minimum</div><div><b>a &lt; 0</b>opens down ∩, has a maximum</div></div>'),
          ('Key features', PARA + table(['Feature', 'y = x² − 2x − 3'], [['Axis of symmetry', 'x = −b/2a = 1'], ['Vertex (turning point)', '(1, −4), minimum'], ['Roots (x-intercepts)', 'x = −1 and x = 3'], ['y-intercept', '−3 (= c)']]))],
         [fill('Axis of symmetry of y = x² − 6x + 5.', 'x = {0}', [['3']], '−b/2a = 6/2'),
          fill('Vertex of y = x² − 6x + 5.', '( {0} , {1} )', [['3'], ['-4']], '9 − 18 + 5 = −4'),
          mcq('y = −2x² + 4x + 1 has…', ['a maximum', 'a minimum', 'no turning point'], 'a maximum'),
          fill('y-intercept of y = 3x² − x + 7.', '{0}', [['7']]),
          fill('Roots of y = x² − 2x − 3 (read the graph, smaller first).', 'x = {0} and x = {1}', [['-1'], ['3']], visual=PARA)]),

    10: L('Use the graph: roots solve f(x) = 0, the part below the axis solves f(x) < 0, and a horizontal line solves f(x) = k.',
          [('f(x) = 0', '<p>Read where the curve crosses the x-axis: x² − 2x − 3 = 0 → <b>x = −1 or 3</b>.</p>'),
           ('f(x) &lt; 0', PARA_INEQ + '<p>The curve is below the axis between the roots → <b>−1 &lt; x &lt; 3</b>.</p><p>f(x) &gt; 0 → x &lt; −1 or x &gt; 3.</p>'),
           ('f(x) = k', PARA_LINE + '<p>x² − 2x − 3 = 5: draw y = 5 and read where it meets the curve → <b>x = −2 or 4</b>.</p>')],
          [mcq('Solve x² − 2x − 3 &gt; 0.', ['x &lt; −1 or x &gt; 3', '−1 &lt; x &lt; 3', 'x &gt; 3 only'], 'x &lt; −1 or x &gt; 3', visual=PARA),
           mcq('Solve x² − 2x − 3 ≤ 0.', ['−1 ≤ x ≤ 3', 'x ≤ −1 or x ≥ 3', 'x ≤ 3'], '−1 ≤ x ≤ 3'),
           fill('Use the graph to solve x² − 2x − 3 = −3 (smaller first).', 'x = {0} or x = {1}', [['0'], ['2']], 'Draw y = −3: it meets the curve at x = 0 and x = 2.'),
           mcq('To solve x² − 2x − 3 = 5 from the graph, which line do you draw?', ['y = 5', 'x = 5', 'y = −5'], 'y = 5'),
           tf('If a parabola never meets the x-axis, f(x) = 0 has no real roots.', True)]),
}
