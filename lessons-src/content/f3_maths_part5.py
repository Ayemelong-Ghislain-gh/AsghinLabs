"""Form 3 Mathematics: statistics and probability (lessons 65-74)."""
from helpers import *
from f3_maths_part1 import table


def bars(labels, values, top=10, touching=False, xlabels=None):
    """Simple bar chart / histogram (y axis from 0 to top)."""
    W, H, L, B = 420, 230, 40, 190
    n = len(values)
    slot = (W - L - 15) / n
    bw = slot if touching else slot * 0.6
    s = f'<line x1="{L}" y1="15" x2="{L}" y2="{B}" class="v-line"/><line x1="{L}" y1="{B}" x2="{W - 10}" y2="{B}" class="v-line"/>'
    step = 2 if top <= 10 else 5
    for v in range(0, top + 1, step):
        y = B - v / top * (B - 20)
        s += f'<text x="{L - 6}" y="{y + 4}" text-anchor="end" class="v-s">{v}</text><line x1="{L}" y1="{y}" x2="{W - 10}" y2="{y}" class="v-line" style="opacity:.25"/>'
    for i, (lab, v) in enumerate(zip(labels, values)):
        x = L + i * slot + (0 if touching else (slot - bw) / 2)
        y = B - v / top * (B - 20)
        s += f'<rect x="{x}" y="{y}" width="{bw}" height="{B - y}" class="{("v-box", "v-box2", "v-box3")[i % 3]}" rx="{0 if touching else 3}"/>'
        if not touching:
            s += f'<text x="{x + bw / 2}" y="{B + 18}" text-anchor="middle" class="v-s">{lab}</text>'
    if touching and xlabels:
        for i, t in enumerate(xlabels):
            s += f'<text x="{L + i * slot}" y="{B + 18}" text-anchor="middle" class="v-s">{t}</text>'
    return svg(W, H + 10, s, 'bar chart')


FRUIT = bars(['Mango', 'Banana', 'Orange', 'Pawpaw'], [8, 5, 4, 3], top=10)
HIST = bars(['0–5', '5–10', '10–15', '15–20'], [2, 6, 9, 3], top=10, touching=True, xlabels=['0', '5', '10', '15', '20'])

LESSONS = {
    65: L('A bar chart shows each category as a bar. The height of the bar is the frequency.',
          [('Reading a bar chart', '<p>Favourite fruit of 20 students:</p>' + FRUIT),
           ('Drawing a bar chart', '<ol><li>Draw the axes: categories across, frequency up</li><li>Choose a scale (e.g. 1 square = 1 student)</li><li>Draw bars of equal width with <b>gaps</b> between them</li><li>Give a title and label the axes</li></ol>'),
           ('Tip', '<p class="wt-key">Bars in a bar chart do not touch. In a histogram they do.</p>')],
          [fill('Use the bar chart.', 'Mango: {0} students, Orange: {1} students', [['8'], ['4']], visual=FRUIT),
           mcq('Which fruit is the most popular?', ['Mango', 'Banana', 'Pawpaw'], 'Mango'),
           fill('How many more students chose mango than pawpaw?', '{0}', [['5']]),
           fill('How many students chose banana or orange?', '{0}', [['9']]),
           tf('In a bar chart, the bars must touch each other.', False)]),

    66: L('A pie chart shows how a whole is shared. Each sector angle = (frequency ÷ total) × 360°.',
          [('Angles', '<p>Favourite fruit (total 20):</p>' + table(['Fruit', 'Frequency', 'Angle'], [['Mango', '8', '8/20 × 360 = 144°'], ['Banana', '5', '90°'], ['Orange', '4', '72°'], ['Pawpaw', '3', '54°'], ['Total', '20', '360°']])),
           ('Drawing it', '<ol><li>Calculate each angle</li><li>Check they add up to 360°</li><li>Draw a circle and a radius</li><li>Measure each angle with a protractor</li><li>Label each sector</li></ol>'),
           ('Reading it', '<p>A sector of 90° out of 40 students → 90/360 × 40 = <b>10 students</b>.</p>')],
          [fill('30 students: 10 walk to school. What angle?', '{0}°', [['120']], '10/30 × 360 = 120'),
           fill('60 people: 15 chose red. What angle?', '{0}°', [['90']]),
           fill('A pie chart for 36 students has a sector of 60°.', 'Number of students = {0}', [['6']], '60/360 × 36 = 6'),
           mcq('The angles of a pie chart always add up to…', ['360°', '180°', '100°'], '360°'),
           tf('A pie chart is good for showing parts of a whole.', True)]),

    67: L('Collect data in a tally table, then choose the best chart to show it.',
          [('Tally and frequency', '<p>Each stroke is one item; the 5th stroke crosses the first four: <b><s>||||</s></b> = 5.</p>' + table(['Shoe size', 'Tally', 'Frequency'], [['38', '<s>||||</s> ||', '7'], ['39', '<s>||||</s> <s>||||</s> |', '11'], ['40', '||||', '4']])),
           ('Which chart?', table(['Chart', 'Best for'], [['Bar chart', 'comparing categories'], ['Pie chart', 'parts of a whole'], ['Line graph', 'change over time'], ['Pictogram', 'simple data with pictures'], ['Histogram', 'grouped numerical data']])),
           ('A good chart', '<p class="wt-key">Title · labelled axes · a clear scale · a key if needed.</p>')],
          [match('Match the chart to its best use.', [('Line graph', 'Temperature during a week'), ('Pie chart', 'How a budget is shared'), ('Bar chart', 'Comparing sales of 4 drinks'), ('Histogram', 'Grouped marks of a class')]),
           fill('A tally shows <s>||||</s> <s>||||</s> |||. What is the frequency?', '{0}', [['13']]),
           mcq('In a pictogram 1 ⚽ = 4 students. How many students do 3 ⚽ and a half represent?', ['14', '12', '7'], '14'),
           tf('Every chart needs a title.', True)]),

    68: L('A histogram shows grouped data. The bars touch because the classes follow each other.',
          [('Example', '<p>Marks of 20 students:</p>' + table(['Marks', '0–5', '5–10', '10–15', '15–20'], [['Frequency', '2', '6', '9', '3']]) + HIST),
           ('Rules (equal class widths)', '<ul><li>Classes go on the horizontal axis as a continuous scale</li><li>Height = frequency</li><li>No gaps between bars</li></ul>'),
           ('Modal class', '<p>The class with the highest bar: <b>10–15</b>.</p>')],
          [fill('Use the histogram.', 'Frequency of 5–10 = {0}', [['6']], visual=HIST),
           mcq('What is the modal class?', ['10–15', '5–10', '15–20'], '10–15'),
           fill('How many students scored 10 or more?', '{0}', [['12']], '9 + 3 = 12'),
           mcq('Why do the bars of a histogram touch?', ['The data is continuous', 'To save space', 'It looks nicer'], 'The data is continuous'),
           fill('What is the total number of students?', '{0}', [['20']])]),

    69: L('The mode is the most frequent value. The median is the middle value once the data is in order.',
          [('Mode', '<p>3, 7, 7, 2, 9, 7, 4 → 7 appears 3 times → <b>mode = 7</b></p>'),
           ('Median (odd count)', '<p>Order first: 2, 3, 4, <b>7</b>, 7, 7, 9 → middle value = <b>7</b></p>'),
           ('Median (even count)', '<p>4, 8, 5, 10 → 4, 5, 8, 10 → middle two 5 and 8 → median = (5 + 8)/2 = <b>6.5</b></p><p class="wt-key">Position of the median: (n + 1)/2</p>')],
          [fill('Find the mode.', '5, 2, 8, 5, 3, 5, 2 → mode = {0}', [['5']]),
           fill('Find the median.', '9, 3, 6, 1, 7 → median = {0}', [['6']], 'In order: 1, 3, 6, 7, 9.'),
           fill('Find the median.', '12, 4, 10, 6 → median = {0}', [['8']], 'In order: 4, 6, 10, 12 → (6 + 10)/2 = 8.'),
           fill('15 values are in order. The median is the value in position…', '{0}', [['8']], '(15 + 1)/2 = 8'),
           mcq('What must you do before finding the median?', ['Put the values in order', 'Add them up', 'Find the mode'], 'Put the values in order')]),

    70: L('The mean is the sum of all values divided by how many there are.',
          [('Mean', '<p class="wt-key">Mean = sum of values ÷ number of values</p><p>12, 15, 9, 14, 10 → 60 ÷ 5 = <b>12</b></p>'),
           ('From a frequency table', '<p class="wt-key">Mean = Σfx ÷ Σf</p>' + table(['x', 'f', 'fx'], [['1', '4', '4'], ['2', '3', '6'], ['3', '3', '9'], ['Total', '10', '19']]) + '<p>Mean = 19 ÷ 10 = <b>1.9</b></p>'),
           ('Missing value', '<p>The mean of 4 numbers is 6 → their sum is 24. If three are 5, 7, 8, the fourth is 24 − 20 = <b>4</b>.</p>')],
          [fill('Find the mean.', '4, 8, 6, 10, 7 → mean = {0}', [['7']]),
           fill('Find the mean from the table: x = 0, 1, 2 with f = 5, 3, 2.', 'Mean = {0}', [['0.7']], 'Σfx = 0 + 3 + 4 = 7; Σf = 10.'),
           fill('The mean of 5 marks is 11. Four of them are 10, 12, 9, 13.', 'The fifth mark is {0}', [['11']], 'Sum = 55; 55 − 44 = 11.'),
           mcq('Which average is affected most by one very large value?', ['The mean', 'The mode', 'The median'], 'The mean'),
           tf('Σf means the total of the frequencies.', True)]),

    71: L('The sample space is the set of all possible outcomes. An event is a part of it.',
          [('Sample space S', table(['Experiment', 'Sample space'], [['Toss a coin', '{H, T}'], ['Roll a die', '{1, 2, 3, 4, 5, 6}'], ['Toss two coins', '{HH, HT, TH, TT}']])),
           ('Events', '<p>Rolling a die, event E = "an even number" = {2, 4, 6}.</p><p>An event is a <b>subset</b> of the sample space.</p>'),
           ('Tip', '<p class="wt-key">List outcomes in an orderly way so you don\'t miss any (a table helps for two dice).</p>')],
          [fill('How many outcomes when you roll one die?', 'n(S) = {0}', [['6']]),
           fill('How many outcomes when you toss two coins?', 'n(S) = {0}', [['4']]),
           fill('How many outcomes when you roll two dice?', 'n(S) = {0}', [['36']], '6 × 6 = 36'),
           mcq('Roll a die. Event "a number greater than 4" = ?', ['{5, 6}', '{4, 5, 6}', '{1, 2, 3, 4}'], '{5, 6}'),
           mcq('Toss two coins. Event "exactly one head" = ?', ['{HT, TH}', '{HH}', '{HH, HT, TH}'], '{HT, TH}')]),

    72: L('Outcomes are equiprobable when each one has the same chance of happening.',
          [('Equiprobable', '<p>A fair coin: H and T each have the same chance. A fair die: each number has the same chance.</p>'),
           ('Not equiprobable', '<ul><li>A biased (loaded) die</li><li>Rain tomorrow or no rain</li><li>Picking a colour from a bag with 7 red and 1 blue ball</li></ul>'),
           ('Why it matters', '<p class="wt-key">The formula P = favourable ÷ total only works when outcomes are equiprobable.</p>')],
          [sort('Equiprobable outcomes or not?', ['Equiprobable', 'Not equiprobable'], [('Heads or tails on a fair coin', 'Equiprobable'), ('Numbers on a fair die', 'Equiprobable'), ('Red or blue from 7 red and 1 blue', 'Not equiprobable'), ('Winning or losing a football match', 'Not equiprobable')]),
           tf('A loaded die gives equiprobable outcomes.', False),
           mcq('A bag has 3 red, 3 blue and 3 green balls. Picking each colour is…', ['equiprobable', 'not equiprobable', 'impossible'], 'equiprobable')]),

    73: L('P(E) = number of favourable outcomes ÷ total number of outcomes (when they are equiprobable).',
          [('Formula', '<p class="wt-key">P(E) = n(E) / n(S)</p><p>Die, even number: P = 3/6 = <b>1/2</b></p>'),
           ('Bags of balls', '<p>3 red and 5 blue balls → P(red) = <b>3/8</b>, P(blue) = 5/8</p>'),
           ('Not happening', '<p class="wt-key">P(not E) = 1 − P(E)</p><p>P(not red) = 1 − 3/8 = 5/8</p><p>Two coins: P(at least one head) = 3/4 (HH, HT, TH).</p>')],
          [fill('Roll a die.', 'P(a 5) = {0}', [['1/6']]),
           fill('Roll a die.', 'P(a number greater than 4) = {0}', [['1/3', '2/6']]),
           fill('A bag has 4 red and 6 green balls.', 'P(green) = {0}', [['3/5', '6/10', '0.6']]),
           fill('P(rain) = 0.3.', 'P(no rain) = {0}', [['0.7']]),
           fill('Toss two coins.', 'P(two heads) = {0}', [['1/4', '0.25']])]),

    74: L('All probabilities lie between 0 (impossible) and 1 (certain).',
          [('The scale', svg(420, 90, ''.join([
              '<line x1="20" y1="40" x2="400" y2="40" class="v-line" style="stroke-width:3"/>',
              ''.join(f'<line x1="{x}" y1="32" x2="{x}" y2="48" class="v-line"/><text x="{x}" y="22" text-anchor="middle" class="v-s">{t}</text><text x="{x}" y="70" text-anchor="middle" class="v-s">{w}</text>'
                      for x, t, w in [(20, '0', 'impossible'), (115, '', 'unlikely'), (210, '1/2', 'even'), (305, '', 'likely'), (400, '1', 'certain')]),
          ]), 'Probability scale')),
           ('Examples', '<ul><li>Rolling a 7 on a die: <b>0</b> (impossible)</li><li>Heads on a coin: <b>1/2</b> (even chance)</li><li>The sun rising tomorrow: <b>1</b> (certain)</li></ul>'),
           ('Remember', '<p class="wt-key">A probability can never be negative or bigger than 1.</p>')],
          [sort('Where is it on the scale?', ['Impossible', 'Even chance', 'Certain'], [('Rolling a 7 on a normal die', 'Impossible'), ('Getting tails on a fair coin', 'Even chance'), ('A month having fewer than 32 days', 'Certain'), ('Picking a red card from a normal deck', 'Even chance')]),
           tf('A probability can be 1.5.', False),
           mcq('Which probability means "very likely"?', ['0.95', '0.05', '0.5'], '0.95'),
           order('Put these from least likely to most likely.', ['P = 0', 'P = 0.2', 'P = 0.5', 'P = 0.9', 'P = 1'])]),
}
