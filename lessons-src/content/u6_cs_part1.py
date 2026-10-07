"""Upper Sixth Computer Science: AI, ADTs, searching, fractional numbers, Boolean algebra (lessons 1-16)."""
from helpers import *
from f3_maths_part1 import table
from l6_ict_part5 import code


def bst():
    nodes = {50: (210, 25), 30: (110, 85), 70: (310, 85), 20: (60, 145), 40: (160, 145), 60: (260, 145), 80: (360, 145)}
    edges = [(50, 30), (50, 70), (30, 20), (30, 40), (70, 60), (70, 80)]
    g = ''.join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" class="v-line" style="stroke-width:2"/>' for a, b in edges)
    g += ''.join(f'<circle cx="{x}" cy="{y}" r="20" class="v-box2"/><text x="{x}" y="{y + 5}" text-anchor="middle" class="v-t">{v}</text>' for v, (x, y) in nodes.items())
    return svg(420, 175, g, 'Binary search tree')


BST = bst()

KMAP = table(['AB \\ C', 'C = 0', 'C = 1'], [['00', '0', '1'], ['01', '0', '1'], ['11', '0', '1'], ['10', '0', '1']])

LESSONS = {
    1: L('AI is the science of making machines that perceive, reason, learn and act. It must be developed and used ethically.',
         [('Definitions', '<p>AI performs tasks that normally need human intelligence. <b>Turing test</b>: if an evaluator cannot tell machine from human, the machine "passes".</p>' + table(['Kind', 'Meaning'], [['Narrow AI', 'one domain — all current systems'], ['General AI', 'human-level across domains — not achieved'], ['Superintelligence', 'beyond humans — hypothetical']])),
          ('Ethics', table(['Issue', 'Example'], [['Bias', 'hiring model rejects women because past data did'], ['Privacy', 'facial recognition in public spaces'], ['Accountability', 'who is liable when a self-driving car crashes?'], ['Transparency', '"black box" neural networks'], ['Misinformation', 'deepfakes, AI-generated fake news'], ['Employment', 'automation of routine jobs']])),
          ('Responsible AI', '<p class="wt-key">Fair data, explainability, privacy by design, human oversight, clear accountability, honest disclosure of AI use.</p>')],
         [mcq('All AI systems deployed today are…', ['narrow AI', 'general AI', 'superintelligent'], 'narrow AI'),
          match('Match the ethical issue.', [('Model trained only on urban data fails in villages', 'Bias'), ('Nobody can explain a loan rejection', 'Transparency'), ('App stores voice recordings without consent', 'Privacy'), ('Unclear who is liable for an AI error', 'Accountability')]),
          tf('Passing the Turing test proves a machine is conscious.', False, 'It only shows its answers are indistinguishable from a human\'s.'),
          mcq('"Human in the loop" means…', ['a person reviews important AI decisions', 'humans are replaced', 'AI trains humans'], 'a person reviews important AI decisions')]),

    2: L('AI techniques include search, knowledge representation, expert systems, fuzzy logic, neural networks and genetic algorithms.',
         [('Search', '<p><b>Uninformed</b>: breadth-first, depth-first. <b>Informed</b>: uses a heuristic, e.g. A* (f = g + h). Game playing: minimax.</p>'),
          ('Knowledge representation', '<ul><li><b>Rules</b>: IF fever AND rash THEN measles?</li><li><b>Semantic networks</b>: nodes and labelled links ("is-a")</li><li><b>Frames</b>: objects with slots</li><li><b>Logic</b>: predicate calculus, Prolog</li></ul>'),
          ('Other techniques', table(['Technique', 'Idea'], [['Expert system', 'knowledge base + inference engine (forward/backward chaining)'], ['Fuzzy logic', 'truth values between 0 and 1'], ['Neural network', 'weighted neurons in layers, trained by backpropagation'], ['Genetic algorithm', 'evolve solutions by selection, crossover, mutation']]))],
         [match('Match the technique.', [('A* route finding', 'Informed search'), ('IF–THEN medical rules', 'Expert system'), ('"Temperature is 0.7 hot"', 'Fuzzy logic'), ('Selection, crossover, mutation', 'Genetic algorithm')]),
          mcq('Starting from facts and applying rules until a goal is reached is…', ['forward chaining', 'backward chaining', 'backpropagation'], 'forward chaining'),
          mcq('In A*, h(n) is…', ['the estimated cost from n to the goal', 'the cost so far', 'the number of nodes'], 'the estimated cost from n to the goal'),
          tf('A semantic network represents knowledge as nodes linked by labelled relationships.', True)]),

    3: L('Machine learning builds models from data. Evaluate them with a confusion matrix and suitable metrics.',
         [('Types and algorithms', table(['Type', 'Algorithms', 'Task'], [['Supervised', 'linear regression, decision tree, k-NN, SVM', 'prediction from labelled data'], ['Unsupervised', 'k-means, hierarchical clustering', 'find groups'], ['Reinforcement', 'Q-learning', 'learn actions from rewards']])),
          ('Confusion matrix', table(['', 'Predicted +', 'Predicted −'], [['Actual +', 'TP = 40', 'FN = 10'], ['Actual −', 'FP = 5', 'TN = 45']]) +
           '<p>Accuracy = (TP + TN)/total = 85/100 = <b>85%</b> · Precision = TP/(TP + FP) = 40/45 ≈ <b>0.89</b> · Recall = TP/(TP + FN) = 40/50 = <b>0.8</b></p>'),
          ('Over/underfitting', '<p><b>Overfitting</b>: great on training, poor on new data (too complex). <b>Underfitting</b>: poor on both (too simple).</p>')],
         [fill('TP = 30, TN = 50, FP = 10, FN = 10.', 'Accuracy = {0}%', [['80']]),
          fill('Same values.', 'Precision = {0}', [['0.75', '3/4']]),
          fill('Same values.', 'Recall = {0}', [['0.75', '3/4']]),
          sort('Supervised or unsupervised algorithm?', ['Supervised', 'Unsupervised'], [('k-means', 'Unsupervised'), ('Decision tree', 'Supervised'), ('Linear regression', 'Supervised'), ('Hierarchical clustering', 'Unsupervised')]),
          mcq('Training accuracy 99%, test accuracy 62%. This is…', ['overfitting', 'underfitting', 'ideal'], 'overfitting')]),

    4: L('An AI project follows a pipeline: problem, data, model, evaluation, deployment and monitoring.',
         [('Pipeline', flow(['Problem', 'Data', 'Prepare', 'Train', 'Evaluate', 'Deploy', 'Monitor'])),
          ('Data split', '<p>Typical: 70% training, 15% validation (tune), 15% test (final check). Never test on training data.</p>'),
          ('Practical issues', '<ul><li>Data cleaning: missing values, duplicates, outliers</li><li>Feature selection and scaling</li><li>Hyperparameters (learning rate, tree depth)</li><li>Model drift after deployment → retrain</li><li>Tools: Python, scikit-learn, TensorFlow, Jupyter</li></ul>')],
         [order('Order the pipeline.', ['Define the problem', 'Collect data', 'Clean and prepare data', 'Train the model', 'Evaluate', 'Deploy', 'Monitor and retrain']),
          fill('10 000 examples split 70/15/15.', 'Training = {0}, test = {1}', [['7000'], ['1500']]),
          mcq('The validation set is used to…', ['tune hyperparameters', 'replace the test set', 'store the model'], 'tune hyperparameters'),
          mcq('Model accuracy falls months after deployment because real data changed. This is…', ['model drift', 'overfitting at training', 'a syntax error'], 'model drift')]),

    6: L('An abstract data type (ADT) is defined by its operations, not by how it is implemented.',
         [('Common ADTs', table(['ADT', 'Key operations', 'Order'], [['Stack', 'push, pop, peek, isEmpty', 'LIFO'], ['Queue', 'enqueue, dequeue, isEmpty', 'FIFO'], ['List', 'insert, delete, search, traverse', 'positional'], ['Dictionary / map', 'put(key, value), get(key)', 'by key'], ['Tree', 'insert, search, traverse', 'hierarchical'], ['Graph', 'addVertex, addEdge, neighbours', 'network']])),
          ('Implementations', '<ul><li><b>Static</b> (array): fixed size, fast index, may overflow</li><li><b>Dynamic</b> (linked list with pointers): grows, extra memory for pointers</li><li><b>Circular queue</b>: rear wraps round: rear = (rear + 1) MOD size</li></ul>')],
         [match('Match the ADT to its order.', [('Stack', 'Last in, first out'), ('Queue', 'First in, first out'), ('Dictionary', 'Access by key'), ('Tree', 'Hierarchy')]),
          fill('Circular queue size 5, rear = 4. After one enqueue, rear =', '{0}', [['0']], '(4 + 1) MOD 5 = 0'),
          mcq('Advantage of a linked list over an array?', ['It can grow and shrink dynamically', 'Faster access by index', 'Uses less memory per item'], 'It can grow and shrink dynamically'),
          fill('Stack: push A, push B, push C, pop, pop, push D. Top =', '{0}', [['D']])]),

    7: L('A binary tree has nodes with at most two children. In a binary search tree, left < node < right.',
         [('BST', BST + '<p>Inserted in order: 50, 30, 70, 20, 40, 60, 80. Root 50; leaves 20, 40, 60, 80; height 2 (edges).</p>'),
          ('Traversals', table(['Traversal', 'Order', 'Result'], [['Pre-order', 'Node, Left, Right', '50 30 20 40 70 60 80'], ['In-order', 'Left, Node, Right', '20 30 40 50 60 70 80 (sorted!)'], ['Post-order', 'Left, Right, Node', '20 40 30 60 80 70 50']])),
          ('Array representation', '<p>Node at index i (from 0): left child at 2i + 1, right child at 2i + 2, parent at (i − 1) DIV 2.</p>')],
         [mcq('In-order traversal of a BST gives…', ['the values in ascending order', 'the root first', 'a random order'], 'the values in ascending order'),
          fill('Pre-order of the tree shown: 50, {0}, {1}, …', '50, {0}, {1}', [['30'], ['20']], visual=BST),
          fill('Inserting 65 into the tree: it becomes the right child of…', '{0}', [['60']], '65 > 50 → right; 65 < 70 → left; 65 > 60 → right of 60.'),
          fill('Array tree: node at index 3. Its left child is at index…', '{0}', [['7']]),
          mcq('Which node of the tree is a leaf?', ['40', '30', '50'], '40')]),

    8: L('ADTs solve real problems: stacks for undo and expressions, queues for scheduling, trees for search, graphs for networks.',
          [('Applications', table(['ADT', 'Uses'], [['Stack', 'undo, back button, function calls, bracket matching, postfix evaluation'], ['Queue', 'print spooling, CPU scheduling, keyboard buffer, BFS'], ['Tree', 'file systems, BST search, expression trees, decision trees'], ['Graph', 'road maps, social networks, routing (Dijkstra)'], ['Hash table', 'fast lookup: dictionaries, symbol tables']])),
           ('Postfix with a stack', '<p>3 4 + 2 * : push 3, push 4, + → 7, push 2, * → <b>14</b>. Infix: (3 + 4) × 2.</p>')],
          [fill('Evaluate the postfix expression 5 1 2 + 4 * + 3 −', '{0}', [['14']], '1+2=3; 3×4=12; 5+12=17; 17−3=14'),
           fill('Evaluate 6 2 / 3 *', '{0}', [['9']]),
           match('Best ADT for the job.', [('Browser back button', 'Stack'), ('Printer jobs', 'Queue'), ('Shortest road between towns', 'Graph'), ('Folder hierarchy', 'Tree')]),
           mcq('Checking that brackets ( [ ] ) are balanced uses a…', ['stack', 'queue', 'graph'], 'stack')]),

    10: L('Linear search checks items one by one; binary search halves a sorted list each step; hashing jumps straight to the item.',
          [('Linear search', '<p>Works on any list. Worst case n comparisons → O(n).</p>'),
           ('Binary search', code('low <- 0; high <- n - 1\nWHILE low <= high\n    mid <- (low + high) DIV 2\n    IF A[mid] = target THEN RETURN mid\n    ELSE IF A[mid] < target THEN low <- mid + 1\n    ELSE high <- mid - 1\nENDWHILE\nRETURN -1') +
            '<p>[3, 8, 12, 19, 25, 31, 40], find 25: mid = 3 (19) → low = 4; mid = 5 (31) → high = 4; mid = 4 (25) found in <b>3 comparisons</b>. O(log n).</p>'),
           ('Hashing', '<p>Address = key MOD table size. Collisions handled by linear probing or chaining. Average O(1).</p>')],
          [fill('Binary search [2, 5, 9, 14, 20, 27, 33, 41] for 27 (indices 0–7). First mid index =', '{0}', [['3']], '(0 + 7) DIV 2 = 3'),
           fill('How many comparisons at most for binary search on 1024 items?', '{0}', [['10', '11']]),
           fill('Hash table size 11. Key 46 goes to address', '{0}', [['2']], '46 MOD 11 = 2'),
           mcq('Binary search requires the list to be…', ['sorted', 'short', 'stored in a stack'], 'sorted'),
           mcq('Two keys hash to the same address. This is a…', ['collision', 'overflow', 'deadlock'], 'collision')]),

    12: L('Fixed-point binary places the binary point at a fixed position: bits after it are worth ½, ¼, ⅛…',
          [('Place values', table(['4', '2', '1', '.', '½', '¼', '⅛'], [['1', '0', '1', '.', '1', '1', '0']]) + '<p>101.110 = 4 + 1 + 0.5 + 0.25 = <b>5.75</b></p>'),
           ('Decimal → binary', '<p>6.625: 6 = 110; fraction: 0.625 × 2 = 1.25 → 1, 0.25 × 2 = 0.5 → 0, 0.5 × 2 = 1 → 1 → <b>110.101</b></p>'),
           ('Limits', '<p>0.1 in decimal has no exact binary form (0.000110011…): rounding errors. Fixed point: simple and fast, but limited range and precision.</p>')],
          [fill('Convert 11.01 (binary) to decimal.', '{0}', [['3.25']]),
           fill('Convert 10.111 (binary) to decimal.', '{0}', [['2.875']]),
           fill('Convert 5.5 to binary.', '{0}', [['101.1']]),
           fill('Convert 0.375 to binary.', '0.{0}', [['011']], '0.375 × 2 = 0.75 → 0; × 2 = 1.5 → 1; 0.5 × 2 = 1 → 1'),
           tf('0.1 (decimal) can be stored exactly in binary.', False)]),

    13: L('Floating point stores a mantissa and an exponent: value = mantissa × 2^exponent. More mantissa bits = precision, more exponent bits = range.',
          [('Two\'s complement floating point', '<p>8-bit mantissa (point after the sign bit), 4-bit exponent.</p><p>Mantissa 0.1010000 = 0.625, exponent 0010 = 2 → 0.625 × 2² = <b>2.5</b></p>'),
           ('Normalisation', '<p>Maximises precision: a positive mantissa starts <b>0.1</b>, a negative one starts <b>1.0</b>. Shift the mantissa and adjust the exponent.</p>'),
           ('IEEE 754 single precision', table(['Sign', 'Exponent', 'Mantissa'], [['1 bit', '8 bits (bias 127)', '23 bits (hidden 1.)']])),
           ('Errors', '<p>Rounding errors, <b>overflow</b> (number too big), <b>underflow</b> (too close to 0).</p>')],
          [fill('Mantissa 0.1100000, exponent 0011.', 'Value = {0}', [['6']], '0.75 × 2³'),
           fill('Mantissa 0.1000000, exponent 1111 (−1).', 'Value = {0}', [['0.25', '1/4']], '0.5 × 2⁻¹'),
           mcq('Which mantissa is normalised (positive)?', ['0.1011000', '0.0101100', '1.1010000'], '0.1011000'),
           mcq('More exponent bits (same total) gives…', ['greater range, less precision', 'more precision, less range', 'no change'], 'greater range, less precision'),
           fill('IEEE 754 single precision uses an exponent bias of', '{0}', [['127']])]),

    15: L('Boolean algebra manipulates logic expressions using laws, duality and De Morgan\'s theorems.',
          [('Laws', table(['Law', 'Statement'], [['Commutative', 'A + B = B + A'], ['Associative', '(A + B) + C = A + (B + C)'], ['Distributive', 'A(B + C) = AB + AC; A + BC = (A + B)(A + C)'], ['Absorption', 'A + AB = A; A(A + B) = A'], ['Complement', 'A + A\' = 1; A·A\' = 0'], ['De Morgan', '(A + B)\' = A\'B\'; (AB)\' = A\' + B\''], ['Redundancy', 'A + A\'B = A + B']])),
           ('Duality', '<p>Swap + and ·, and 0 and 1: the dual of a law is also a law (A + 0 = A ↔ A·1 = A).</p>'),
           ('Example', '<p>A\'B + AB + AB\' = B(A\' + A) + AB\' = B + AB\' = <b>A + B</b></p>')],
          [mcq('Simplify A\'B + AB.', ['B', 'A', 'AB'], 'B'),
           mcq('Simplify A + A\'B.', ['A + B', 'A', 'AB'], 'A + B'),
           mcq('(A\' + B\')\' = ?', ['AB', 'A + B', 'A\'B\''], 'AB'),
           mcq('Dual of A + 1 = 1 is…', ['A·0 = 0', 'A·1 = A', 'A + 0 = A'], 'A·0 = 0'),
           mcq('Simplify (A + B)(A + B\').', ['A', 'B', 'AB'], 'A', 'A + BB\' = A + 0 = A')]),

    16: L('Write functions in standard forms (SOP, POS) and minimise them with Karnaugh maps.',
          [('Standard forms', '<p><b>SOP</b> (sum of minterms): f = Σm(1, 3) for rows with output 1. <b>POS</b> (product of maxterms): f = ΠM(…) for rows with output 0.</p>'),
           ('Karnaugh map', '<p>f(A, B, C) = Σm(1, 3, 5, 7):</p>' + KMAP + '<p>All 1s are in the C = 1 column → group of 4 → <b>f = C</b></p><p class="wt-key">Group 1s in rectangles of 1, 2, 4, 8 (as large as possible); rows use Gray code order 00, 01, 11, 10; edges wrap round.</p>'),
           ('Don\'t-care', '<p>X cells can be treated as 1 or 0 to make bigger groups.</p>')],
          [mcq('f(A, B, C) = Σm(0, 2, 4, 6) simplifies to…', ['C\'', 'C', 'A'], 'C\''),
           mcq('f(A, B, C) = Σm(6, 7) simplifies to…', ['AB', 'C', 'A + B'], 'AB'),
           mcq('Why are K-map rows ordered 00, 01, 11, 10?', ['Adjacent cells differ by one bit (Gray code)', 'Alphabetical order', 'To save space'], 'Adjacent cells differ by one bit (Gray code)'),
           fill('A group of 4 cells in a 3-variable K-map removes how many variables?', '{0}', [['2']]),
           mcq('Allowed group sizes are…', ['1, 2, 4, 8', '1, 3, 5', 'any size'], '1, 2, 4, 8')]),
}
