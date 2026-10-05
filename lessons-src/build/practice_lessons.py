"""Settings of the step-by-step practice lessons: titles, descriptions, controls, search keywords.
Where each page lives and which progression lessons it covers is set in build.py (PRACTICE_PAGES / PRACTICE_FOR)."""

LOGIC_EXPLORE = '''
  <div class="lesson-panel" id="explore">
    <h2>🔌 Explore: tap the inputs</h2>
    <div class="lesson-controls">
      <select id="gateSel" aria-label="Gate">
        <option>AND</option><option>OR</option><option>NOT</option><option>NAND</option><option>NOR</option><option>XOR</option>
      </select>
    </div>
    <div class="gate-explore">
      <div class="gate-io">
        <button type="button" class="sw" id="swA">A = 0</button>
        <button type="button" class="sw" id="swB">B = 0</button>
      </div>
      <div id="gSymbol"></div>
      <div class="lamp" id="lamp">Q = 0</div>
    </div>
    <p class="lesson-hint" id="gRule"></p>
    <div class="vt-wrap"><table class="vt tt" id="gTable"></table></div>
  </div>
'''

LESSONS = [
    # ---------- already built ----------
    dict(slug='binary-converter', keywords='binary decimal hexadecimal hex number systems base 2 base 16 bits conversion convert', built_in=True, title='Binary, Decimal & Hex Conversions',
         card='Convert step by step and get corrected at every step.',
         places=[('Form 2', 'Computer Science', '14'), ('Lower Sixth', 'ICT', '72')]),
    dict(slug='sorting-algorithms', keywords='sort sorting bubble selection insertion algorithm array', built_in=True, title='Sorting Algorithms',
         card='Step through Bubble, Selection and Insertion Sort one comparison at a time.',
         places=[('Lower Sixth', 'ICT', '89'), ('Upper Sixth', 'Computer Science', '11')]),
    dict(slug='expanding-brackets', keywords='expand expansion brackets algebra grid method multiply', built_in=True, title='Expanding Brackets',
         card='Fill the grid, collect like terms and check your answer.',
         places=[('Form 3', 'Mathematics', '2')]),
    dict(slug='factorising-quadratics', keywords='factorise factorize factorisation quadratic trinomial algebra brackets', built_in=True, title='Factorising Quadratics',
         card='Find the two numbers, write the brackets and check.',
         places=[('Form 3', 'Mathematics', '4')]),
    dict(slug='graph-plotter', keywords='graph graphs straight line gradient intercept curve parabola table of values plot', built_in=True, title='Graphs: Lines & Curves',
         card='Make a table of values, plot it and read the graph.',
         places=[('Form 3', 'Mathematics', '8')]),

    # ---------- Batch 1 ----------
    dict(slug='algorithms-order', keywords='algorithm algorithms steps order sequence instructions problem solving form 1', title='Algorithms: Put the Steps in Order', level='Form 1', subject='Computer Science', ref='11',
         teaches='Introduction to algorithms: ordering steps to solve a problem',
         desc='Learn what an algorithm is by putting everyday and computer tasks in the right order, then spot the mistake in a classmate\'s algorithm. Free interactive Form 1 Computer Science lesson.',
         lead='An algorithm is a list of steps in the right order. Put the steps in order and find the mistakes.',
         next='Get more practice in the Form 1 Computer Science workbook.',
         card='Put everyday and computer tasks in the right order, then find the mistake.',
         places=[('Form 1', 'Computer Science', '11')]),
    dict(slug='unit-conversions', keywords='units storage bits bytes kb mb gb tb kilobyte megabyte gigabyte time hours minutes seconds convert conversion', title='Storage and Time Unit Conversions', level='Form 2', subject='Computer Science', ref='18–19',
         teaches='Converting between units of storage and time',
         desc='Convert bits, bytes, KB, MB, GB and TB, and hours, minutes and seconds, step by step with instant correction. Free interactive lesson for Form 2 Computer Science.',
         lead='Bits, bytes, KB, MB, GB … and hours, minutes, seconds. Learn when to multiply and when to divide.',
         controls='<select id="pType" aria-label="Type"><option value="storage">Storage units</option><option value="time">Time units</option><option value="mix">Mixed</option></select>',
         next='Practise more conversions in the Computer Science workbooks.',
         card='Know when to multiply and when to divide: bytes, KB, MB, GB and time.',
         places=[('Form 2', 'Computer Science', '18–19'), ('Lower Sixth', 'ICT', '15')]),
    dict(slug='change-subject', keywords='change the subject transposition formula formulae rearrange make subject', title='Change the Subject of a Formula', level='Form 3', subject='Mathematics', ref='6',
         teaches='Transposition of formulae',
         desc='Learn to change the subject of a formula one step at a time: choose the right operation, see the result and check with numbers. Free interactive Form 3 Maths lesson.',
         lead='Get a letter on its own by undoing each operation. One step at a time.',
         next='Get more transposition practice in the Mathematics workbooks.',
         card='Undo each operation to get the letter you want on its own.',
         places=[('Form 3', 'Mathematics', '6')]),
    dict(slug='simultaneous-equations', keywords='simultaneous equations elimination solve x y linear', title='Simultaneous Equations', level='Form 3', subject='Mathematics', ref='10–11',
         teaches='Solving simultaneous linear equations by elimination',
         desc='Solve simultaneous linear equations by elimination, step by step: match, add or subtract, find x and y and check. Free interactive Form 3 Maths lesson.',
         lead='Find the x and y that make two equations true at the same time, using elimination.',
         controls='<select id="pLevel" aria-label="Level"><option value="easy">Easier: add or subtract</option><option value="hard">Harder: multiply first</option></select>',
         next='Get more simultaneous equations practice in the Mathematics workbooks.',
         card='Eliminate one letter, find the other, then check.',
         places=[('Form 3', 'Mathematics', '10–11')]),
    dict(slug='right-triangles', keywords='trigonometry trig sin cos tan soh cah toa pythagoras hypotenuse right angle triangle angle', title='Pythagoras and SOH CAH TOA', level='Form 3', subject='Mathematics', ref='14–17',
         teaches='Pythagoras theorem and trigonometric ratios in right-angled triangles',
         desc='Name the sides, choose sin, cos or tan, and find missing sides and angles in right-angled triangles, with step-by-step correction. Free interactive Form 3 Maths lesson.',
         lead='Name the sides, pick the right ratio, and find any missing side or angle.',
         controls='<select id="pType" aria-label="Type"><option value="side">Find a side (SOH CAH TOA)</option><option value="angle">Find an angle</option><option value="pyth">Pythagoras</option><option value="mix">Mixed</option></select>',
         next='Have a calculator ready. Get more trigonometry practice in the Mathematics workbooks.',
         card='Name the sides, choose sin, cos or tan, then calculate.',
         places=[('Form 3', 'Mathematics', '14–17')]),
    dict(slug='cell-referencing', keywords='spreadsheet excel cell reference referencing relative absolute mixed dollar formula copy', title='Spreadsheet Cell Referencing', level='Lower Sixth', subject='ICT', ref='33–34',
         teaches='Relative, absolute and mixed cell references in spreadsheets',
         desc='Predict what a spreadsheet formula becomes when it is copied: relative, absolute ($A$1) and mixed references, with a real sheet to check. Free interactive ICT lesson.',
         lead='What happens to a formula when you copy it? Learn relative, absolute and mixed references.',
         controls='<select id="pLevel" aria-label="Level"><option value="easy">Copy down</option><option value="hard">Harder: mixed and across</option></select>',
         next='Practise spreadsheets in the ICT workbook.',
         card='Predict how a formula changes when copied. A1 vs $A$1.',
         places=[('Lower Sixth', 'ICT', '33–34'), ('Form 2', 'Computer Science', '37')]),
    dict(slug='logic-gates', keywords='logic gates and or not nand nor xor truth table circuit boolean', title='Logic Gates and Truth Tables', level='Lower Sixth', subject='ICT', ref='74–77',
         teaches='Logic gates, logic circuits and truth tables',
         desc='Tap the inputs of AND, OR, NOT, NAND, NOR and XOR gates, then fill in truth tables for gates and circuits, one column at a time. Free interactive lesson.',
         lead='Tap the inputs to see each gate work, then fill in truth tables yourself.',
         explore=LOGIC_EXPLORE,
         controls='<select id="pType" aria-label="Type"><option value="gate">One gate</option><option value="circuit">A circuit (3 inputs)</option></select>',
         next='Practise more logic circuits in the ICT and Computer Science workbooks.',
         card='Tap the inputs, then fill truth tables for gates and circuits.',
         places=[('Lower Sixth', 'ICT', '74–77'), ('Upper Sixth', 'Computer Science', '15')]),
    dict(slug='cpu-scheduling', keywords='cpu process scheduling fcfs sjf round robin gantt chart waiting turnaround operating system', title='CPU Scheduling: FCFS, SJF and Round Robin', level='Upper Sixth', subject='Computer Science', ref='45–47',
         teaches='Process scheduling algorithms, Gantt charts, turnaround and waiting times',
         desc='Build the Gantt chart for FCFS, SJF and Round Robin scheduling, then calculate completion, turnaround and average waiting times step by step. Free interactive lesson.',
         lead='Draw the Gantt chart, then calculate completion, turnaround and waiting times.',
         controls='<select id="pAlgo" aria-label="Algorithm"><option value="FCFS">FCFS</option><option value="SJF">SJF (non-preemptive)</option><option value="RR">Round Robin</option></select>',
         next='Practise more scheduling questions in the Computer Science workbook.',
         card='Gantt charts, turnaround and waiting times for FCFS, SJF and Round Robin.',
         places=[('Upper Sixth', 'Computer Science', '45–47')]),
]

CLASSES = ['Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', 'Lower Sixth', 'Upper Sixth']
