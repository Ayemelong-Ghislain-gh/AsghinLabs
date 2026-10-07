"""Form 5 Mathematics: statistics and probability (lessons 11-26)."""
from helpers import *
from f3_maths_part1 import table
from f3_maths_part5 import bars


def tree():
    """Two-stage tree: bag with 3 red and 2 blue, drawn without replacement."""
    t = lambda x, y, s, c='v-t': f'<text x="{x}" y="{y}" class="{c}">{s}</text>'
    g = ''.join([
        arrow(20, 110, 130, 50), arrow(20, 110, 130, 170),
        t(60, 68, '3/5', 'v-s'), t(60, 160, '2/5', 'v-s'), t(136, 55, 'R'), t(136, 175, 'B'),
        arrow(155, 50, 265, 20), arrow(155, 50, 265, 80), arrow(155, 170, 265, 140), arrow(155, 170, 265, 200),
        t(200, 26, '2/4', 'v-s'), t(200, 80, '2/4', 'v-s'), t(200, 146, '3/4', 'v-s'), t(200, 200, '1/4', 'v-s'),
        t(272, 25, 'R  → RR = 6/20'), t(272, 85, 'B  → RB = 6/20'), t(272, 145, 'R  → BR = 6/20'), t(272, 205, 'B  → BB = 2/20'),
    ])
    return svg(440, 220, g, 'probability tree')


TREE = tree()
GROUPED = table(['Class', '0–10', '10–20', '20–30', '30–40'], [['f', '5', '8', '12', '5'], ['midpoint x', '5', '15', '25', '35'], ['fx', '25', '120', '300', '175']])

OGIVE = svg(420, 240, ''.join([
    '<line x1="40" y1="20" x2="40" y2="200" class="v-line"/><line x1="40" y1="200" x2="400" y2="200" class="v-line"/>',
    '<polyline points="40,200 120,170 200,122 280,50 360,20" fill="none" stroke="#00d4ff" stroke-width="3"/>',
    '<line x1="40" y1="110" x2="214" y2="110" class="v-line" style="stroke-dasharray:5 4"/><line x1="214" y1="110" x2="214" y2="200" class="v-line" style="stroke-dasharray:5 4"/>',
    '<text x="34" y="114" text-anchor="end" class="v-s">n/2</text><text x="214" y="216" text-anchor="middle" class="v-s">median</text>',
    '<text x="220" y="236" text-anchor="middle" class="v-s">upper class boundary →</text><text x="12" y="16" class="v-s">cf</text>',
]), 'Cumulative frequency curve')

LESSONS = {
    11: L('Data can be qualitative or quantitative, and it is collected with questionnaires, interviews, observation or experiments.',
          [('Types of data', table(['Type', 'Meaning', 'Example'], [['Qualitative', 'words / categories', 'favourite colour'], ['Quantitative discrete', 'counted, whole numbers', 'number of siblings'], ['Quantitative continuous', 'measured, any value', 'height, mass, time']])),
           ('Primary and secondary', '<div class="two-col"><div><b>Primary</b>you collect it yourself</div><div><b>Secondary</b>collected by someone else (census, internet)</div></div>'),
           ('Collection methods', '<ul><li>Questionnaire</li><li>Interview</li><li>Observation</li><li>Experiment</li></ul><p><b>Population</b>: everyone concerned. <b>Sample</b>: the part you actually ask.</p>')],
          [sort('What type of data?', ['Qualitative', 'Discrete', 'Continuous'], [('Blood group', 'Qualitative'), ('Number of goals scored', 'Discrete'), ('Height of a student', 'Continuous'), ('Favourite subject', 'Qualitative'), ('Time to run 100 m', 'Continuous'), ('Number of pupils in a class', 'Discrete')]),
           sort('Primary or secondary data?', ['Primary', 'Secondary'], [('Your survey of classmates', 'Primary'), ('Census figures from the ministry', 'Secondary'), ('Temperatures you measure each day', 'Primary'), ('Statistics from a newspaper', 'Secondary')]),
           mcq('Asking 50 students out of a school of 1200 is using…', ['a sample', 'the whole population', 'secondary data'], 'a sample'),
           tf('Mass is continuous data.', True)]),

    12: L('A frequency table counts how often each value (or each class of values) appears.',
          [('Ungrouped', '<p>Marks: 3, 5, 4, 3, 5, 5, 2, 4, 5, 3</p>' + table(['Mark', '2', '3', '4', '5'], [['Frequency', '1', '3', '2', '4']])),
           ('Grouped', '<p>For many different values, use classes: 0–9, 10–19, 20–29…</p>' + table(['Class', 'Boundaries', 'Width', 'Midpoint'], [['10–19', '9.5 – 19.5', '10', '14.5']])),
           ('Words', '<ul><li><b>Class width</b>: upper boundary − lower boundary</li><li><b>Midpoint</b>: (lower + upper)/2</li><li>Total of frequencies = number of data</li></ul>')],
          [fill('Count: 2, 4, 4, 1, 4, 2, 4. Frequency of 4?', '{0}', [['4']]),
           fill('Class 20–29 (whole numbers).', 'Midpoint = {0}, width = {1}', [['24.5'], ['10']]),
           fill('Class boundaries of 30–39.', '{0} to {1}', [['29.5'], ['39.5']]),
           mcq('A table has frequencies 4, 7, 6, 3. How many data values?', ['20', '7', '4'], '20')]),

    13: L('A pictogram uses symbols with a key. A bar chart uses bars of equal width with gaps.',
          [('Pictogram', '<p>Key: 📘 = 10 books</p><p>Monday 📘📘📘 = 30 books · Tuesday 📘📘½ = 25 books</p><p class="wt-key">Always give a key.</p>'),
           ('Bar chart', bars(['Mon', 'Tue', 'Wed', 'Thu'], [6, 4, 8, 2], top=10) + '<p>Bars have equal width and gaps between them; height = frequency.</p>')],
          [fill('Key: ⚽ = 4 goals. A team has ⚽⚽⚽ and a half.', '{0} goals', [['14']]),
           fill('Key: 🧍 = 5 students. How many symbols for 35 students?', '{0}', [['7']]),
           fill('Read the bar chart.', 'Wednesday = {0}, total = {1}', [['8'], ['20']], visual=bars(['Mon', 'Tue', 'Wed', 'Thu'], [6, 4, 8, 2], top=10)),
           tf('In a bar chart, all bars must have the same width.', True)]),

    14: L('A line graph shows change over time. A pie chart shows parts of a whole, with angles adding to 360°.',
          [('Line graph', svg(420, 200, ''.join([
              '<line x1="40" y1="20" x2="40" y2="170" class="v-line"/><line x1="40" y1="170" x2="400" y2="170" class="v-line"/>',
              '<polyline points="70,130 140,110 210,60 280,80 350,40" fill="none" stroke="#00d4ff" stroke-width="3"/>',
              ''.join(f'<circle cx="{x}" cy="{y}" r="4" class="v-mk"/><text x="{x}" y="188" text-anchor="middle" class="v-s">{m}</text>' for x, y, m in [(70, 130, 'Jan'), (140, 110, 'Feb'), (210, 60, 'Mar'), (280, 80, 'Apr'), (350, 40, 'May')]),
           ]), 'line graph') + '<p>Join the points with straight lines; time goes across.</p>'),
           ('Pie chart', '<p class="wt-key">Angle = (frequency ÷ total) × 360°</p><p>48 students, 12 walk → 12/48 × 360 = <b>90°</b></p>')],
          [fill('72 students, 18 come by bus.', 'Angle = {0}°', [['90']]),
           fill('A sector of 120° in a pie chart of 60 people.', '{0} people', [['20']]),
           match('Which chart is best?', [('Monthly rainfall over a year', 'Line graph'), ('How a family budget is shared', 'Pie chart'), ('Comparing 5 football teams\' goals', 'Bar chart')]),
           tf('The angles of a pie chart add up to 360°.', True)]),

    15: L('A histogram shows grouped data with touching bars. A frequency polygon joins the midpoints of the bar tops.',
          [('Histogram', bars(['', '', '', ''], [5, 8, 12, 5], top=12, touching=True, xlabels=['0', '10', '20', '30', '40']) + '<p>Equal class widths → height = frequency. No gaps.</p>'),
           ('Frequency polygon', '<p>Plot (midpoint, frequency) for each class: (5, 5), (15, 8), (25, 12), (35, 5), and join with straight lines.</p><p class="wt-key">Useful to compare two distributions on one graph.</p>')],
          [mcq('In a frequency polygon, the points are plotted at…', ['the class midpoints', 'the lower boundaries', 'the upper boundaries'], 'the class midpoints'),
           fill('Class 40–50 has frequency 7.', 'Point to plot: ( {0} , {1} )', [['45'], ['7']]),
           tf('The bars of a histogram touch.', True),
           mcq('The modal class is the class with…', ['the highest frequency', 'the biggest midpoint', 'the lowest frequency'], 'the highest frequency')]),

    16: L('Mode = most common, median = middle value in order, mean = total ÷ number of values.',
          [('Example', '<p>4, 7, 2, 7, 9, 3, 10</p><ul><li>Mode = <b>7</b></li><li>Order: 2, 3, 4, 7, 7, 9, 10 → median = <b>7</b></li><li>Mean = 42 ÷ 7 = <b>6</b></li></ul>'),
           ('Even number of values', '<p>3, 8, 5, 6 → 3, 5, 6, 8 → median = (5 + 6)/2 = <b>5.5</b></p>'),
           ('Which average?', '<p>Mean uses all values but is pulled by extreme values. Median resists extremes. Mode works for categories.</p>')],
          [fill('Data: 5, 9, 1, 5, 8, 2, 5.', 'mode = {0}, median = {1}, mean = {2}', [['5'], ['5'], ['5']]),
           fill('Data: 10, 4, 8, 6.', 'median = {0}, mean = {1}', [['7'], ['7']]),
           mcq('Salaries: 50k, 55k, 60k, 2 000k. Which average best describes a typical salary?', ['Median', 'Mean', 'They are all fine'], 'Median', 'The 2 000k value pulls the mean up.'),
           fill('The mean of 5 numbers is 8. Their sum is…', '{0}', [['40']])]),

    17: L('From a frequency table: mode = value with highest f, mean = Σfx ÷ Σf, median from cumulative frequencies.',
          [('Example', table(['x', '1', '2', '3', '4'], [['f', '3', '5', '8', '4'], ['fx', '3', '10', '24', '16'], ['cf', '3', '8', '16', '20']])),
           ('Results', '<ul><li>Mode = <b>3</b> (f = 8)</li><li>Mean = 53 ÷ 20 = <b>2.65</b></li><li>Median: n = 20, between 10th and 11th values → both are 3 → <b>3</b></li></ul>')],
          [fill('x: 0, 1, 2, 3 with f: 2, 5, 2, 1.', 'Σf = {0}, Σfx = {1}, mean = {2}', [['10'], ['12'], ['1.2']]),
           fill('Same table. Mode = ?', '{0}', [['1']]),
           fill('Same table. Median = ?', '{0}', [['1']], 'cf: 2, 7, 9, 10 → 5th and 6th values are both 1.'),
           mcq('Σf means…', ['the total frequency', 'the sum of the x values', 'the biggest frequency'], 'the total frequency')]),

    18: L('For grouped data, use class midpoints to estimate the mean. Find the modal class and the median class.',
          [('Table', GROUPED),
           ('Estimates', '<ul><li>Mean ≈ Σfx ÷ Σf = 620 ÷ 30 ≈ <b>20.7</b></li><li>Modal class: <b>20–30</b></li><li>Median position 30/2 = 15th; cf: 5, 13, 25 → median class <b>20–30</b></li></ul><p class="wt-key">It is an estimate: we don\'t know the exact values in each class.</p>')],
          [fill('Midpoint of the class 40–60.', '{0}', [['50']]),
           fill('Classes 0–10, 10–20 with f = 4, 6.', 'Σfx = {0}, estimated mean = {1}', [['110'], ['11']], '4×5 + 6×15 = 110; 110 ÷ 10 = 11'),
           mcq('Why is the grouped mean only an estimate?', ['We use midpoints, not the real values', 'The calculator is not precise', 'The frequencies are wrong'], 'We use midpoints, not the real values'),
           fill('cf: 5, 13, 25, 30 for classes 0–10, 10–20, 20–30, 30–40.', 'Median class: {0}', [['20–30', '20-30']])]),

    19: L('A cumulative frequency curve (ogive) is plotted at upper class boundaries. Read the median at n/2 and the quartiles at n/4 and 3n/4.',
          [('Cumulative frequency table', table(['Upper boundary', '10', '20', '30', '40'], [['cf', '5', '13', '25', '30']])),
           ('The ogive', OGIVE + '<p>Plot (upper boundary, cf) and join with a smooth S-shaped curve, starting at cf = 0.</p>'),
           ('Reading it', '<ul><li>Median: go across from n/2</li><li>Lower quartile Q₁: n/4</li><li>Upper quartile Q₃: 3n/4</li><li>Interquartile range = Q₃ − Q₁</li></ul>')],
          [fill('Frequencies 3, 7, 10, 5. Cumulative frequencies?', '{0}, {1}, {2}, {3}', [['3'], ['10'], ['20'], ['25']]),
           fill('n = 80. Read the median at cf = ?', '{0}', [['40']]),
           fill('n = 80. At which cumulative frequencies do you read the quartiles?', 'Q₁ at {0}, Q₃ at {1}', [['20'], ['60']]),
           mcq('Points of an ogive are plotted at…', ['upper class boundaries', 'midpoints', 'lower boundaries'], 'upper class boundaries'),
           fill('Q₁ = 24 and Q₃ = 41.', 'IQR = {0}', [['17']])]),

    20: L('Dispersion measures how spread out data is: range, interquartile range, variance and standard deviation.',
          [('Range and IQR', '<p>Range = largest − smallest. IQR = Q₃ − Q₁ (the middle half, not affected by extremes).</p>'),
           ('Standard deviation', '<p class="wt-key">σ = √( Σ(x − x̄)² ÷ n )</p><p>2, 4, 4, 4, 5, 5, 7, 9: mean = 5</p><p>Squared deviations: 9, 1, 1, 1, 0, 0, 4, 16 → sum 32 → variance = 32 ÷ 8 = 4 → <b>σ = 2</b></p>'),
           ('Meaning', '<p>Small σ: values close to the mean. Large σ: values spread out.</p>')],
          [fill('Data: 3, 9, 4, 12, 7.', 'Range = {0}', [['9']]),
           fill('Data: 1, 3, 5 (mean 3).', 'Variance = {0}', [['8/3', '2.67']], '(4 + 0 + 4)/3 = 8/3'),
           fill('Variance = 9.', 'σ = {0}', [['3']]),
           mcq('Class A: σ = 2. Class B: σ = 8. Same mean. Which class has marks closer together?', ['Class A', 'Class B', 'Same spread'], 'Class A'),
           mcq('Which measure is NOT affected by one extreme value?', ['Interquartile range', 'Range', 'Standard deviation'], 'Interquartile range')]),

    21: L('An experiment has outcomes. The set of all outcomes is the sample space S; an event is a subset of S.',
          [('Vocabulary', table(['Word', 'Meaning'], [['Experiment / trial', 'an action with uncertain result (rolling a die)'], ['Outcome', 'one possible result (a 4)'], ['Sample space S', 'all possible outcomes'], ['Event', 'a set of outcomes (an even number)']])),
           ('Two dice', '<p>Use a 6 × 6 table: n(S) = 36. Event "sum = 7": (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 outcomes.</p>')],
          [fill('Two coins and one die are thrown together.', 'n(S) = {0}', [['24']], '2 × 2 × 6'),
           fill('Two dice: how many outcomes give a sum of 7?', '{0}', [['6']]),
           fill('Two dice: how many outcomes give a double?', '{0}', [['6']]),
           mcq('A family has 2 children. S = ?', ['{BB, BG, GB, GG}', '{B, G}', '{BB, GG}'], '{BB, BG, GB, GG}')]),

    22: L('P(E) = n(E) ÷ n(S) when outcomes are equally likely. 0 ≤ P(E) ≤ 1.',
          [('Formula', '<p class="wt-key">P(E) = n(E) / n(S)</p><p>Two dice, sum 7: P = 6/36 = <b>1/6</b></p>'),
           ('Scale', '<p>0 = impossible · ½ = even chance · 1 = certain</p>'),
           ('Experimental probability', '<p>Relative frequency = number of times it happened ÷ number of trials. With many trials it gets close to the theoretical probability.</p>')],
          [fill('Two dice.', 'P(sum = 12) = {0}', [['1/36']]),
           fill('Two dice.', 'P(double) = {0}', [['1/6', '6/36']]),
           fill('A drawing pin lands point up 30 times out of 50.', 'Relative frequency = {0}', [['3/5', '0.6']]),
           mcq('Which cannot be a probability?', ['1.2', '0', '0.99'], '1.2')]),

    23: L('The complement A\' is "A does not happen": P(A\') = 1 − P(A). For "A or B": P(A ∪ B) = P(A) + P(B) − P(A ∩ B).',
          [('Complement', '<p class="wt-key">P(A\') = 1 − P(A)</p><p>P(rain) = 0.3 → P(no rain) = 0.7</p>'),
           ('Compound events', '<p>Die: A = even {2, 4, 6}, B = more than 3 {4, 5, 6}, A ∩ B = {4, 6}</p><p>P(A ∪ B) = 3/6 + 3/6 − 2/6 = <b>4/6 = 2/3</b></p><p>Check: A ∪ B = {2, 4, 5, 6} → 4/6 ✓</p>')],
          [fill('P(win) = 0.45.', 'P(not win) = {0}', [['0.55']]),
           fill('P(A) = 0.5, P(B) = 0.4, P(A ∩ B) = 0.2.', 'P(A ∪ B) = {0}', [['0.7']]),
           fill('Die. A = {1, 2, 3}, B = odd. P(A ∪ B) = ?', '{0}', [['2/3', '4/6']], 'A ∪ B = {1, 2, 3, 5}'),
           tf('P(A) + P(A\') = 1', True)]),

    24: L('Mutually exclusive events cannot happen together. Independent events do not affect each other.',
          [('Mutually exclusive', '<p>A ∩ B = ∅ → <b>P(A ∪ B) = P(A) + P(B)</b></p><p>Die: P(1 or 6) = 1/6 + 1/6 = 1/3</p>'),
           ('Independent', '<p>One does not change the other → <b>P(A ∩ B) = P(A) × P(B)</b></p><p>Coin and die: P(H and 6) = ½ × 1/6 = <b>1/12</b></p>'),
           ('Don\'t confuse', '<p class="wt-key">"or" with mutually exclusive → add · "and" with independent → multiply</p>')],
          [sort('Mutually exclusive or not?', ['Mutually exclusive', 'Not'], [('Rolling a 2 and rolling a 5 (one roll)', 'Mutually exclusive'), ('Rolling an even number and a number > 3', 'Not'), ('Head and tail on one coin toss', 'Mutually exclusive'), ('Drawing a king and a heart (one card)', 'Not')]),
           fill('Two coins.', 'P(two heads) = {0}', [['1/4', '0.25']]),
           fill('P(A) = 0.3 and P(B) = 0.5, independent.', 'P(A and B) = {0}', [['0.15']]),
           fill('P(A) = 0.2, P(B) = 0.5, mutually exclusive.', 'P(A or B) = {0}', [['0.7']])]),

    25: L('P(A | B) is the probability of A given that B has happened: P(A | B) = P(A ∩ B) ÷ P(B).',
          [('Formula', '<p class="wt-key">P(A | B) = P(A ∩ B) / P(B)</p><p>The sample space shrinks to B.</p>'),
           ('Die example', '<p>Given the number is even, what is P(6)? Even = {2, 4, 6} → P = <b>1/3</b>.</p>'),
           ('Table example', table(['', 'Glasses', 'No glasses', 'Total'], [['Girls', '5', '7', '12'], ['Boys', '3', '15', '18'], ['Total', '8', '22', '30']]) + '<p>P(glasses | girl) = 5/12 · P(girl | glasses) = 5/8</p>')],
          [fill('Die. Given the number is odd.', 'P(it is 3) = {0}', [['1/3']]),
           fill('Use the table.', 'P(glasses | boy) = {0}', [['3/18', '1/6']]),
           fill('P(A ∩ B) = 0.12, P(B) = 0.4.', 'P(A | B) = {0}', [['0.3']]),
           tf('P(A | B) is always equal to P(B | A).', False, 'P(glasses | girl) = 5/12 but P(girl | glasses) = 5/8.')]),

    26: L('A tree diagram shows events in stages. Multiply along branches; add the results of the branches you want.',
          [('The tree', '<p>Bag: 3 red, 2 blue. Draw 2 balls <b>without</b> replacement.</p>' + TREE),
           ('Rules', '<p class="wt-key">Along a branch: multiply · between branches: add</p><p>P(one of each) = RB + BR = 6/20 + 6/20 = <b>3/5</b></p>'),
           ('With replacement', '<p>The probabilities stay the same: P(RR) = 3/5 × 3/5 = <b>9/25</b>.</p><p>Without replacement the second probabilities change: P(RR) = 3/5 × 2/4 = <b>3/10</b>.</p>')],
          [fill('Use the tree (without replacement).', 'P(BB) = {0}', [['1/10', '2/20']], visual=TREE),
           fill('Same bag, WITH replacement.', 'P(BB) = {0}', [['4/25']]),
           fill('A coin is tossed 3 times.', 'P(3 heads) = {0}', [['1/8']]),
           mcq('The probabilities at the end of all branches add up to…', ['1', '0', '2'], '1'),
           fill('P(pass maths) = 0.8, P(pass English) = 0.7, independent.', 'P(pass both) = {0}', [['0.56']])]),
}
