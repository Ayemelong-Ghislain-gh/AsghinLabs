"""Lower Sixth ICT: data representation, Boolean algebra, data structures, design, algorithms (lessons 71-91)."""
import html
from helpers import *
from f3_maths_part1 import table


def code(src):
    return '<pre class="code">' + html.escape(src.strip('\n')) + '</pre>'


STRUCT_CHART = svg(440, 150, ''.join([
    box(150, 8, 140, 40, 'Payroll', '', 'v-box2'),
    arrow(220, 48, 70, 90), arrow(220, 48, 220, 90), arrow(220, 48, 370, 90),
    box(10, 90, 120, 44, 'Read hours', '', 'v-box'), box(160, 90, 120, 44, 'Calculate pay', '', 'v-box3'), box(310, 90, 120, 44, 'Print payslip', '', 'v-box'),
]), 'Structure chart')

LESSONS = {
    71: L('Computers represent all data — numbers, text, images, sound — as binary digits (bits).',
          [('Units and bases', table(['Base', 'Digits', 'Example'], [['Binary (2)', '0, 1', '1011₂'], ['Octal (8)', '0–7', '13₈'], ['Decimal (10)', '0–9', '11₁₀'], ['Hexadecimal (16)', '0–9, A–F', 'B₁₆']]) + '<p>All four examples above are the same number: eleven.</p>'),
           ('Characters', '<p><b>ASCII</b>: 7 bits, 128 characters (A = 65). <b>Unicode</b>: all languages and emojis (UTF-8, UTF-16).</p>'),
           ('Images and sound', '<p><b>Image</b>: pixels; size = width × height × colour depth (bits). 100 × 100 at 8 bits = 80 000 bits = 10 000 bytes.</p><p><b>Sound</b>: sampled; size = sample rate × bits per sample × seconds (× channels).</p>')],
          [fill('How many values can n = 8 bits represent?', '{0}', [['256']]),
           fill('Hex digit F in decimal.', '{0}', [['15']]),
           fill('Image 200 × 100 pixels, 8-bit colour.', 'Size = {0} bytes', [['20000']], '200 × 100 × 8 bits = 160 000 bits = 20 000 bytes'),
           mcq('Which code covers characters from all languages?', ['Unicode', 'ASCII', 'BCD'], 'Unicode'),
           fill('How many colours with a 4-bit colour depth?', '{0}', [['16']])]),

    73: L('Negative binary numbers use sign-and-magnitude or, more usefully, two\'s complement, which turns subtraction into addition.',
          [('Sign and magnitude', '<p>Leftmost bit = sign (0 +, 1 −). +5 = 00000101, −5 = 10000101. Problem: two zeros (+0, −0).</p>'),
           ('Two\'s complement', '<p class="wt-key">Invert all bits, then add 1.</p><p>+5 = 00000101 → invert 11111010 → +1 → <b>11111011 = −5</b></p><p>8-bit range: <b>−128 to +127</b>. The leftmost bit is worth −128.</p>'),
           ('Subtraction', '<p>7 − 5 = 7 + (−5):</p>' + code('  00000111   (+7)\n+ 11111011   (-5)\n= 1 00000010 -> ignore the carry -> 00000010 = 2'))],
          [fill('Two\'s complement of 6 (8 bits) is −6 =', '{0}', [['11111010']], '6 = 00000110 → 11111001 → +1'),
           fill('What denary value is 11111111 in 8-bit two\'s complement?', '{0}', [['-1']]),
           fill('What denary value is 10000000 in 8-bit two\'s complement?', '{0}', [['-128']]),
           mcq('Range of 8-bit two\'s complement?', ['−128 to 127', '−127 to 127', '0 to 255'], '−128 to 127'),
           fill('Binary addition: 0110 + 0011 =', '{0}', [['1001']]),
           tf('Sign-and-magnitude has two representations of zero.', True)]),

    76: L('Write a Boolean expression from a truth table by OR-ing together the rows where the output is 1 (sum of products).',
          [('Sum of products', table(['A', 'B', 'X'], [['0', '0', '0'], ['0', '1', '1'], ['1', '0', '1'], ['1', '1', '0']]) +
            '<p>Rows with X = 1: A\'B and AB\' → <b>X = A\'B + AB\'</b> (this is XOR, A ⊕ B).</p>'),
           ('De Morgan\'s laws', '<p class="wt-key">(A + B)\' = A\'·B\' &nbsp;&nbsp; (A·B)\' = A\' + B\'</p><p>"Break the bar, change the sign." NAND = NOT(AND), NOR = NOT(OR).</p>')],
          [mcq('Truth table: X = 1 only when A = 1 and B = 1. X = ?', ['A·B', 'A + B', 'A\' + B\''], 'A·B'),
           mcq('Truth table: X = 1 for (0,0) only. X = ?', ['A\'·B\'', 'A + B', 'A·B'], 'A\'·B\'', 'This is NOR.'),
           mcq('(A·B)\' = ?', ['A\' + B\'', 'A\'·B\'', 'A + B'], 'A\' + B\''),
           mcq('(A + B)\' = ?', ['A\'·B\'', 'A\' + B\'', 'A·B'], 'A\'·B\''),
           tf('NAND is the same as NOT AND.', True)]),

    77: L('Simplify Boolean expressions with the laws of Boolean algebra, so circuits need fewer gates.',
          [('Laws', table(['Law', 'AND form', 'OR form'], [['Identity', 'A·1 = A', 'A + 0 = A'], ['Null', 'A·0 = 0', 'A + 1 = 1'], ['Idempotent', 'A·A = A', 'A + A = A'], ['Complement', 'A·A\' = 0', 'A + A\' = 1'], ['Absorption', 'A(A + B) = A', 'A + AB = A'], ['Distributive', 'A(B + C) = AB + AC', 'A + BC = (A + B)(A + C)']])),
           ('Example', '<p>AB + AB\' = A(B + B\') = A·1 = <b>A</b></p><p>A + A\'B = <b>A + B</b></p><p>Karnaugh maps give a visual way to simplify up to 4 variables.</p>')],
          [mcq('Simplify A + 1.', ['1', 'A', '0'], '1'),
           mcq('Simplify A·A\'.', ['0', '1', 'A'], '0'),
           mcq('Simplify AB + AB\'.', ['A', 'B', 'AB'], 'A'),
           mcq('Simplify A + AB.', ['A', 'B', 'A + B'], 'A', 'Absorption law.'),
           mcq('Simplify A(A + B).', ['A', 'AB', 'B'], 'A')]),

    78: L('Data types say what kind of value a variable holds; data structures organise many values.',
          [('Data types', table(['Type', 'Example'], [['Integer', '42'], ['Real / float', '3.14'], ['Character', "'A'"], ['String', '"Hello"'], ['Boolean', 'True / False'], ['Date', '12/10/2026']])),
           ('Data structures', table(['Structure', 'Idea'], [['Array', 'fixed-size, same type, indexed'], ['Record', 'fields of different types (a student)'], ['List', 'ordered, can grow'], ['Stack', 'LIFO: last in, first out'], ['Queue', 'FIFO: first in, first out'], ['Tree', 'hierarchy (folders)'], ['File', 'stored records']]))],
          [match('Best data type.', [('Number of students', 'Integer'), ('Average mark 13.75', 'Real'), ('Has paid fees?', 'Boolean'), ('Student name', 'String')]),
           match('Match the structure.', [('Undo button history', 'Stack'), ('Printer jobs waiting', 'Queue'), ('Folder hierarchy', 'Tree'), ('Marks of 40 students', 'Array')]),
           mcq('LIFO describes a…', ['stack', 'queue', 'record'], 'stack')]),

    79: L('Operations on data structures: traverse, insert, delete, search; push/pop for stacks; enqueue/dequeue for queues.',
          [('Arrays', '<p>marks = [12, 15, 9, 18] → marks[0] = 12 (index starts at 0 in Python). Traverse with a loop; insert/delete may shift elements.</p>'),
           ('Stack', '<p>push(3), push(5), pop() → returns 5, push(7) → stack (bottom→top): 3, 7</p>'),
           ('Queue', '<p>enqueue(A), enqueue(B), dequeue() → returns A, enqueue(C) → queue (front→back): B, C</p>')],
          [fill('Stack: push(4), push(8), push(1), pop(), push(6).', 'Top element = {0}', [['6']]),
           fill('Queue: enqueue(4), enqueue(8), enqueue(1), dequeue().', 'Front element = {0}', [['8']]),
           fill('marks = [12, 15, 9, 18].', 'marks[2] = {0}', [['9']]),
           mcq('Removing from an empty stack causes…', ['stack underflow', 'stack overflow', 'a queue'], 'stack underflow')]),

    80: L('Software can be designed top-down, bottom-up, modularly or with objects.',
          [('Approaches', table(['Approach', 'Idea'], [['Top-down (stepwise refinement)', 'start with the whole problem, break into smaller parts'], ['Bottom-up', 'build small components first, then combine'], ['Modular', 'independent modules with clear interfaces'], ['Object-oriented', 'objects with data (attributes) and methods']])),
           ('Benefits of modules', '<p>Easier to understand, test and maintain; teamwork; reuse.</p>')],
          [match('Match the approach.', [('Start with "Run school", then split into smaller tasks', 'Top-down'), ('Build and test small routines, then combine', 'Bottom-up'), ('Classes like Student with methods', 'Object-oriented')]),
           tf('Modular design makes testing easier.', True),
           mcq('Stepwise refinement is another name for…', ['top-down design', 'bottom-up design', 'testing'], 'top-down design')]),

    81: L('Apply design techniques: decompose with a structure chart, aim for high cohesion and low coupling.',
          [('Structure chart', STRUCT_CHART + '<p>The main module calls sub-modules from left to right.</p>'),
           ('Quality', '<div class="two-col"><div><b>High cohesion</b>each module does one clear job</div><div><b>Low coupling</b>modules depend on each other as little as possible</div></div>')],
          [mcq('A good module has…', ['high cohesion, low coupling', 'low cohesion, high coupling', 'many unrelated tasks'], 'high cohesion, low coupling'),
           order('Order the modules for the payroll program.', ['Read hours', 'Calculate pay', 'Print payslip']),
           tf('In a structure chart, the top box is the main module.', True)]),

    82: L('Represent designs with structure charts, flowcharts, pseudocode, decision tables and UML diagrams.',
          [('Tools', table(['Tool', 'Shows'], [['Structure chart', 'module hierarchy'], ['Flowchart', 'flow of control'], ['Pseudocode', 'algorithm in structured English'], ['Decision table', 'conditions → actions'], ['UML class diagram', 'classes, attributes, methods'], ['UML use case', 'actors and what they do']])),
           ('Decision table', table(['Conditions', 'R1', 'R2', 'R3', 'R4'], [['Member?', 'Y', 'Y', 'N', 'N'], ['Order > 50 000?', 'Y', 'N', 'Y', 'N'], ['10% discount', '✓', '', '', ''], ['5% discount', '', '✓', '✓', '']]))],
          [match('Match the design tool.', [('Shows who uses the system and for what', 'Use case diagram'), ('Shows all combinations of conditions', 'Decision table'), ('Shows classes and methods', 'Class diagram'), ('Shows module hierarchy', 'Structure chart')]),
           mcq('From the decision table: a non-member orders 60 000 FCFA. Discount?', ['5%', '10%', 'None'], '5%'),
           fill('With 3 yes/no conditions, how many rules (columns)?', '{0}', [['8']])]),

    83: L('An algorithm is a finite sequence of clear steps that solves a problem.',
          [('Properties', '<ul><li><b>Finite</b>: it ends</li><li><b>Definite</b>: each step is clear</li><li><b>Input</b> and <b>output</b></li><li><b>Effective</b>: steps are doable</li></ul>'),
           ('Example', code('ALGORITHM Average\nREAD a, b, c\nsum <- a + b + c\navg <- sum / 3\nWRITE avg\nEND')),
           ('Ways to represent', '<p>Natural language, flowchart, pseudocode, program code.</p>')],
          [match('Match the property.', [('It stops after a number of steps', 'Finiteness'), ('Each step has one meaning', 'Definiteness'), ('Produces a result', 'Output'), ('Steps can actually be carried out', 'Effectiveness')]),
           fill('Run the algorithm with a = 10, b = 12, c = 14.', 'avg = {0}', [['12']]),
           tf('An algorithm that loops forever is still a valid algorithm.', False)]),

    84: L('Algorithms use variables, assignment, input/output, and arithmetic, relational and logical operators.',
          [('Instructions', table(['Instruction', 'Example'], [['Assignment', 'x ← 5'], ['Input', 'READ x'], ['Output', 'WRITE x'], ['Arithmetic', '+ − * / DIV MOD'], ['Relational', '= ≠ &lt; &gt; ≤ ≥'], ['Logical', 'AND OR NOT']])),
           ('DIV and MOD', '<p>17 DIV 5 = 3 (whole part) · 17 MOD 5 = 2 (remainder). x MOD 2 = 0 → x is even.</p>'),
           ('Trace', code('x <- 4\ny <- x * 3\nx <- y - x\nWRITE x, y')+ '<p>→ prints 8, 12</p>')],
          [fill('Evaluate.', '23 DIV 4 = {0}, 23 MOD 4 = {1}', [['5'], ['3']]),
           fill('a ← 7; b ← a + 3; a ← b * 2. Final a = ?', '{0}', [['20']]),
           mcq('(5 > 3) AND (2 > 4) is…', ['False', 'True'], 'False'),
           mcq('Which tests if n is odd?', ['n MOD 2 = 1', 'n DIV 2 = 1', 'n = 2'], 'n MOD 2 = 1')]),

    85: L('Flowcharts show an algorithm with standard symbols connected by arrows.',
          [('Symbols', table(['Symbol', 'Use'], [['Oval / terminator', 'Start, End'], ['Parallelogram', 'Input / Output'], ['Rectangle', 'Process'], ['Diamond', 'Decision (Yes/No)'], ['Arrow', 'Flow of control'], ['Rectangle with double sides', 'Predefined process / subroutine']])),
           ('Tips', '<p>One start, at least one end; decisions have two exits; flow top to bottom; loops go back with an arrow.</p>')],
          [match('Match the symbol.', [('Diamond', 'Decision'), ('Parallelogram', 'Input/Output'), ('Rectangle', 'Process'), ('Oval', 'Start/End')]),
           tf('A decision symbol has two exits.', True),
           mcq('A loop in a flowchart is drawn with…', ['an arrow going back to an earlier step', 'a second Start', 'a dotted box'], 'an arrow going back to an earlier step')]),

    86: L('Pseudocode writes algorithms in structured English with standard keywords.',
          [('Keywords', code('START / END\nREAD x          WRITE x\nx <- value\nIF cond THEN ... ELSE ... ENDIF\nCASE x OF ... ENDCASE\nFOR i <- 1 TO n DO ... ENDFOR\nWHILE cond DO ... ENDWHILE\nREPEAT ... UNTIL cond')),
           ('Example', code('START\nREAD n\ntotal <- 0\nFOR i <- 1 TO n DO\n    total <- total + i\nENDFOR\nWRITE total\nEND') + '<p>n = 4 → total = 1 + 2 + 3 + 4 = 10</p>')],
          [fill('Run the example with n = 5.', 'total = {0}', [['15']]),
           order('Put the pseudocode in order (find the larger of two numbers).', ['START', 'READ a, b', 'IF a > b THEN WRITE a', 'ELSE WRITE b', 'ENDIF', 'END']),
           mcq('Which loop always runs at least once?', ['REPEAT … UNTIL', 'WHILE … DO', 'FOR'], 'REPEAT … UNTIL')]),

    87: L('Sequence runs steps in order; selection (IF, CASE) chooses between paths.',
          [('IF … ELSE IF', code('READ mark\nIF mark >= 16 THEN grade <- "A"\nELSE IF mark >= 12 THEN grade <- "B"\nELSE IF mark >= 10 THEN grade <- "C"\nELSE grade <- "F"\nENDIF')),
           ('CASE', code('CASE day OF\n  1: WRITE "Monday"\n  2: WRITE "Tuesday"\n  OTHERWISE: WRITE "Other"\nENDCASE'))],
          [mcq('mark = 13. Grade?', ['B', 'A', 'C'], 'B'),
           mcq('mark = 16. Grade?', ['A', 'B', 'F'], 'A'),
           mcq('mark = 9. Grade?', ['F', 'C', 'B'], 'F'),
           mcq('Which is best for choosing among many fixed values (days 1–7)?', ['CASE', 'FOR', 'WHILE'], 'CASE')]),

    88: L('Loops repeat instructions: FOR (count-controlled), WHILE and REPEAT (condition-controlled).',
          [('Three loops', table(['Loop', 'Test', 'Use'], [['FOR i ← 1 TO n', 'fixed count', 'known number of repeats'], ['WHILE cond DO', 'before the body (may run 0 times)', 'unknown count'], ['REPEAT … UNTIL cond', 'after the body (runs ≥ 1 time)', 'input validation']])),
           ('Example', code('count <- 0\nx <- 1\nWHILE x < 50 DO\n    x <- x * 2\n    count <- count + 1\nENDWHILE\nWRITE x, count') + '<p>x: 1 → 2 → 4 → 8 → 16 → 32 → 64 · prints 64, 6</p>')],
          [fill('FOR i ← 1 TO 10 DO … ENDFOR runs how many times?', '{0}', [['10']]),
           fill('FOR i ← 3 TO 7: s ← s + i, with s starting at 0. Final s?', '{0}', [['25']]),
           fill('x ← 100; WHILE x > 1 DO x ← x DIV 2. Final x?', '{0}', [['1']], '100 → 50 → 25 → 12 → 6 → 3 → 1'),
           mcq('A loop that asks for a password until it is correct is best written with…', ['REPEAT … UNTIL', 'FOR', 'CASE'], 'REPEAT … UNTIL')]),

    90: L('Show an algorithm is correct with dry runs (trace tables), test data and pre/post-conditions.',
          [('Trace table', '<p>Algorithm: s ← 0; FOR i ← 1 TO 3: s ← s + i*i</p>' + table(['i', 's'], [['—', '0'], ['1', '1'], ['2', '5'], ['3', '14']])),
           ('Other methods', '<ul><li><b>Test data</b>: normal, boundary, erroneous</li><li><b>Precondition</b>: what must be true before (n ≥ 0)</li><li><b>Postcondition</b>: what is true after (s = sum of squares)</li><li><b>Loop invariant</b>: stays true each time round the loop</li></ul>')],
          [fill('Trace: s ← 1; FOR i ← 1 TO 4: s ← s * i. Final s?', '{0}', [['24']]),
           fill('Trace: a ← 2; b ← 5; t ← a; a ← b; b ← t.', 'a = {0}, b = {1}', [['5'], ['2']], 'This swaps a and b.'),
           mcq('A dry run is…', ['tracing the algorithm by hand with test values', 'running it on a computer', 'deleting bugs'], 'tracing the algorithm by hand with test values'),
           tf('A precondition is what must be true before the algorithm starts.', True)]),

    91: L('Algorithm efficiency is measured by how time and memory grow with input size n, written with Big-O.',
          [('Common orders', table(['Big-O', 'Name', 'Example'], [['O(1)', 'constant', 'access marks[5]'], ['O(log n)', 'logarithmic', 'binary search'], ['O(n)', 'linear', 'linear search'], ['O(n log n)', '', 'merge sort'], ['O(n²)', 'quadratic', 'bubble sort']])),
           ('Search comparison', '<p>1024 sorted items: linear search worst case 1024 comparisons; binary search at most <b>10</b> (2¹⁰ = 1024).</p>')],
          [order('From most to least efficient for large n.', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
           fill('Binary search on 1 000 000 sorted items needs at most about how many comparisons?', '{0}', [['20']], '2²⁰ ≈ 1 048 576'),
           fill('An O(n²) algorithm takes 1 s for n = 1000. For n = 2000 it takes about…', '{0} s', [['4']]),
           mcq('Bubble sort\'s worst case is…', ['O(n²)', 'O(n)', 'O(log n)'], 'O(n²)')]),
}
