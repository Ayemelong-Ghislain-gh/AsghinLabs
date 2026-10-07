"""Form 2 Computer Science: hardware, AI, problem solving, system software, encoding (lessons 1-16)."""
from helpers import *


def table(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="mini"><tr>{h}</tr>{b}</table>'


SYSTEM = svg(440, 150, ''.join([
    box(5, 45, 100, 56, 'Input', 'keyboard, mouse', 'v-box'), arrow(105, 73, 125, 73),
    box(125, 30, 150, 86, 'Processing', 'CPU', 'v-box2'), arrow(275, 73, 295, 73),
    box(295, 45, 140, 56, 'Output', 'screen, printer', 'v-box'),
    arrow(200, 116, 200, 128),
    box(125, 128, 150, 20, '', '', 'v-box3', 6),
    '<text x="200" y="143" text-anchor="middle" class="v-s">Storage: RAM, disk, flash</text>',
]), 'Input, processing, output and storage')

CPU = svg(420, 150, ''.join([
    '<rect x="10" y="10" width="400" height="130" rx="14" class="v-line"/>',
    '<text x="210" y="32" text-anchor="middle" class="v-t">CPU</text>',
    box(25, 50, 110, 70, 'CU', 'gives orders', 'v-box'),
    box(155, 50, 110, 70, 'ALU', 'calculates', 'v-box2'),
    box(285, 50, 110, 70, 'Registers', 'tiny fast memory', 'v-box3'),
    marker(25, 50, 1), marker(155, 50, 2), marker(285, 50, 3),
]), 'Parts of the CPU')

AI_TREE = svg(440, 170, ''.join([
    box(150, 8, 140, 44, 'AI', '', 'v-box2'),
    arrow(220, 52, 60, 92), arrow(220, 52, 165, 92), arrow(220, 52, 275, 92), arrow(220, 52, 385, 92),
    box(5, 92, 105, 60, 'Machine', 'learning', 'v-box'),
    box(115, 92, 100, 60, 'Computer', 'vision', 'v-box3'),
    box(220, 92, 105, 60, 'Language', '(NLP)', 'v-box'),
    box(330, 92, 105, 60, 'Robotics', '', 'v-box3'),
]), 'Branches of AI')

STEPS = flow([('1. Define', 'the problem'), ('2. Analyse', 'inputs, outputs'), ('3. Design', 'algorithm'),
              ('4. Code', 'the program'), ('5. Test', 'fix errors'), ('6. Document', 'explain it')])


def _oval(x, y, w, h, t):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" class="v-box2"/><text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>'


def _para(x, y, w, h, t):
    return f'<polygon points="{x + 14},{y} {x + w},{y} {x + w - 14},{y + h} {x},{y + h}" class="v-box"/><text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>'


def _rect(x, y, w, h, t):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="v-box3"/><text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>'


def _diam(cx, cy, w, h, t):
    return f'<polygon points="{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}" class="v-box"/><text x="{cx}" y="{cy + 5}" text-anchor="middle" class="v-t">{t}</text>'


SYMBOLS = svg(440, 110, ''.join([
    _oval(10, 30, 90, 40, 'Start'), _para(115, 30, 100, 40, 'Read N'), _rect(230, 30, 90, 40, 'S ← N×2'), _diam(385, 50, 100, 60, 'N > 0?'),
    marker(10, 30, 1), marker(125, 30, 2), marker(230, 30, 3), marker(338, 26, 4),
]), 'Flowchart symbols')

FLOWCHART = svg(300, 380, ''.join([
    _oval(90, 5, 120, 36, 'Start'), arrow(150, 41, 150, 58),
    _para(75, 58, 150, 38, 'Read mark'), arrow(150, 96, 150, 120),
    _diam(150, 152, 150, 64, 'mark ≥ 10?'),
    arrow(225, 152, 255, 152), arrow(255, 152, 255, 210),
    '<text x="240" y="145" class="v-s">Yes</text><text x="38" y="145" class="v-s">No</text>',
    arrow(75, 152, 45, 152), arrow(45, 152, 45, 210),
    _para(185, 210, 110, 38, 'Write "Pass"'), _para(5, 210, 110, 38, 'Write "Fail"'),
    arrow(240, 248, 240, 290), arrow(60, 248, 60, 290), '<line x1="60" y1="290" x2="240" y2="290" class="v-arrow"/>',
    arrow(150, 290, 150, 330), _oval(90, 330, 120, 36, 'End'),
]), 'Flowchart: pass or fail')

OS_LAYERS = svg(380, 190, ''.join([
    box(40, 8, 300, 40, 'User', '', 'v-box2'),
    box(40, 52, 300, 40, 'Application software', '', 'v-box'),
    box(40, 96, 300, 40, 'Operating system', '', 'v-box3'),
    box(40, 140, 300, 40, 'Hardware', '', 'v-box'),
]), 'Layers: user, applications, operating system, hardware')

LESSONS = {
    1: L('Input devices put data into the computer. Output devices give results out of it.',
         [('The computer system', SYSTEM + '<p class="wt-key">Input → Processing → Output, with storage to keep data.</p>'),
          ('Types of input devices',
           '<ul><li><b>Keying</b>: keyboard, keypad</li><li><b>Pointing</b>: mouse, touchpad, touchscreen, joystick</li><li><b>Scanning</b>: scanner, barcode reader, QR code reader</li><li><b>Audio / video</b>: microphone, webcam, digital camera</li><li><b>Sensors</b>: temperature, light, fingerprint reader</li></ul>'),
          ('Types of output devices',
           '<div class="two-col"><div><b>Soft copy</b>you see or hear it: monitor, projector, speakers, headphones</div><div><b>Hard copy</b>you can hold it: printer, plotter</div></div>'),
          ('Printers and screens',
           '<ul><li><b>Impact printer</b> hits the paper: dot-matrix (noisy, used for receipts)</li><li><b>Non-impact printer</b>: inkjet (sprays ink), laser (uses toner, fast)</li><li>Screens: old <b>CRT</b> (big, heavy) → <b>LCD / LED</b> (flat, light)</li></ul>'),
          ('Both input and output',
           '<p>Some devices do both: <b>touchscreen</b> (you touch = input, it shows = output), <b>headset</b> with microphone, <b>multifunction printer</b> (scan + print).</p>')],
         [sort('Input or output?', ['Input', 'Output'], [('Scanner', 'Input'), ('Projector', 'Output'), ('Microphone', 'Input'), ('Speakers', 'Output'), ('Barcode reader', 'Input'), ('Plotter', 'Output')]),
          match('Match each input device to its type.', [('Keyboard', 'Keying'), ('Joystick', 'Pointing'), ('QR code reader', 'Scanning'), ('Webcam', 'Audio / video'), ('Fingerprint reader', 'Sensor')]),
          sort('Soft copy or hard copy?', ['Soft copy', 'Hard copy'], [('Picture on a monitor', 'Soft copy'), ('Printed report card', 'Hard copy'), ('Music from speakers', 'Soft copy'), ('A plan printed by a plotter', 'Hard copy')]),
          mcq('A shop prints small receipts with a noisy printer that hits the paper. Which printer is it?', ['Dot-matrix printer', 'Laser printer', 'Inkjet printer'], 'Dot-matrix printer', 'Dot-matrix is an impact printer: pins hit an ink ribbon.'),
          mcq('Which device is both input and output?', ['Touchscreen', 'Mouse', 'Printer'], 'Touchscreen', 'You touch it (input) and it displays (output).'),
          tf('A laser printer is an impact printer.', False, 'Laser printers use toner and do not hit the paper: they are non-impact.')]),

    2: L('The CPU processes data. Storage devices keep data and programs.',
         [('The CPU: the brain', CPU +
           '<ul><li><b>Control Unit (CU)</b>: fetches instructions and gives orders</li><li><b>ALU</b> (Arithmetic and Logic Unit): does calculations (+, −) and comparisons (&gt;, =)</li><li><b>Registers</b>: very small, very fast memory inside the CPU</li></ul>'),
          ('Other processing devices',
           '<ul><li><b>GPU</b> (graphics card): processes images, video and games</li><li><b>Motherboard</b>: the main board that connects everything</li></ul><p>CPU speed is measured in <b>GHz</b> (gigahertz).</p>'),
          ('Primary storage (main memory)',
           '<div class="two-col"><div><b>RAM</b>holds what you are using now. <b>Volatile</b>: lost when power goes off.</div><div><b>ROM</b>holds start-up instructions. <b>Non-volatile</b>: kept without power.</div></div>'),
          ('Secondary storage',
           table(['Type', 'Examples'], [['Magnetic', 'Hard disk (HDD)'], ['Optical', 'CD, DVD, Blu-ray'], ['Solid state', 'SSD, flash drive, memory card'], ['Online', 'Cloud storage']]) +
           '<p class="wt-key">Secondary storage keeps your files even when the computer is off.</p>')],
         [label('Name the parts of the CPU.', CPU.replace('CU</text>', '?</text>').replace('ALU</text>', '?</text>').replace('Registers</text>', '?</text>'), ['Control Unit', 'ALU', 'Registers'], 'The CU gives orders, the ALU calculates, registers are tiny fast memory.'),
          match('Match the part to its job.', [('Control Unit', 'Fetches instructions and gives orders'), ('ALU', 'Does calculations and comparisons'), ('Registers', 'Tiny fast memory inside the CPU'), ('GPU', 'Processes images and video')]),
          sort('Volatile or non-volatile?', ['Volatile', 'Non-volatile'], [('RAM', 'Volatile'), ('ROM', 'Non-volatile'), ('Hard disk', 'Non-volatile'), ('Flash drive', 'Non-volatile')], 'Only RAM loses its content when the power goes off.'),
          sort('Which storage technology?', ['Magnetic', 'Optical', 'Solid state'], [('Hard disk drive', 'Magnetic'), ('DVD', 'Optical'), ('SSD', 'Solid state'), ('Memory card', 'Solid state'), ('CD-ROM', 'Optical')]),
          mcq('The power goes off while you type a document you have not saved. Why is it lost?', ['It was only in RAM, which is volatile', 'The hard disk is volatile', 'The CPU deleted it'], 'It was only in RAM, which is volatile', 'Save often: saving copies your work to secondary storage.'),
          tf('CPU speed is measured in gigahertz (GHz).', True)]),

    4: L('AI is a family of technologies that let computers learn, see, understand language and act.',
         [('What is AI?',
           '<p><b>Artificial Intelligence</b> is the ability of a computer to do tasks that normally need human intelligence: learning, recognising, understanding and deciding.</p>'),
          ('Branches of AI', AI_TREE +
           '<ul><li><b>Machine learning</b>: learns from data</li><li><b>Computer vision</b>: understands images (face unlock)</li><li><b>Natural language processing</b>: understands text and speech (chatbots, translation)</li><li><b>Robotics</b>: machines that move and act</li></ul>'),
          ('Narrow AI vs general AI',
           '<div class="two-col"><div><b>Narrow AI</b>does one task well: a chess program, a translator. All AI today is narrow.</div><div><b>General AI</b>would think like a human about anything. It does not exist yet.</div></div>'),
          ('How machine learning works',
           flow([('Data', 'many examples'), ('Train', 'find patterns'), ('Model', 'predicts')]) +
           '<p class="wt-key">Good, varied data → a better model.</p>')],
         [match('Match the AI branch to an example.', [('Computer vision', 'Face unlock on a phone'), ('Natural language processing', 'A chatbot answering in French'), ('Robotics', 'A robot arm in a factory'), ('Machine learning', 'Learning to spot spam emails from examples')]),
          mcq('All the AI we use today is…', ['narrow AI', 'general AI', 'human AI'], 'narrow AI', 'Each AI system is good at one kind of task.'),
          order('Put the machine learning steps in order.', ['Collect data', 'Train: find patterns', 'Use the model to predict'], 'First data, then training, then prediction.'),
          tf('A machine learning model trained on bad data can give bad answers.', True, '"Garbage in, garbage out."'),
          sort('Which branch of AI?', ['Computer vision', 'Language (NLP)'], [('Reading a car number plate', 'Computer vision'), ('Google Translate', 'Language (NLP)'), ('Voice assistant understanding you', 'Language (NLP)'), ('Detecting plant disease from a photo', 'Computer vision')])]),

    5: L('AI brings big benefits, but it also creates risks we must manage responsibly.',
         [('Where AI is used',
           '<ul><li><b>Health</b>: reading scans, predicting disease</li><li><b>Agriculture</b>: spotting plant disease, weather prediction</li><li><b>Finance</b>: detecting fraud in mobile money</li><li><b>Education</b>: tutoring, translation</li><li><b>Security</b>: face recognition, CCTV analysis</li></ul>'),
          ('Risks of AI',
           '<ul><li><b>Bias</b>: unfair results if the data is unfair</li><li><b>Deepfakes</b>: fake photos, voices or videos that look real</li><li><b>Privacy</b>: AI can collect a lot of personal data</li><li><b>Jobs</b>: some tasks are automated</li><li><b>Misinformation</b>: AI can state false things confidently</li></ul>'),
          ('Using AI responsibly',
           '<ul><li>Check AI answers with trusted sources</li><li>Say when you used AI</li><li>Do not share people\'s images or data without permission</li><li>A human must decide in important cases</li></ul>'
           '<p class="wt-key">AI is a tool: the human stays responsible.</p>')],
         [match('Match the area to how AI helps.', [('Finance', 'Detecting mobile money fraud'), ('Agriculture', 'Spotting plant disease'), ('Health', 'Reading medical scans'), ('Security', 'Recognising faces on CCTV')]),
          match('Match each risk to its meaning.', [('Bias', 'Unfair results from unfair data'), ('Deepfake', 'A fake video that looks real'), ('Privacy', 'Personal data collected or exposed'), ('Misinformation', 'False information stated confidently')]),
          mcq('A video shows a minister saying something shocking, but his lips look strange. What could it be?', ['A deepfake', 'A printer error', 'A virus scan'], 'A deepfake', 'Check the news on trusted sources before sharing.'),
          sort('Responsible or irresponsible?', ['Responsible', 'Irresponsible'], [('Checking an AI answer in your textbook', 'Responsible'), ('Making a fake voice message of your teacher', 'Irresponsible'), ('Saying "I used AI to help with this"', 'Responsible'), ('Uploading classmates\' photos to an AI app without asking', 'Irresponsible')]),
          tf('If an AI makes a decision, nobody is responsible.', False, 'Humans who build and use AI remain responsible.')]),

    6: L('A good prompt gives the AI a role, a task, context and a format. Then you improve it step by step.',
         [('Parts of a strong prompt',
           table(['Part', 'Example'], [['Role', 'You are a patient maths teacher.'], ['Task', 'Explain fractions'], ['Context', 'to a Form 2 student who finds it hard'], ['Format', 'in 5 short steps with one example']])),
          ('Give an example',
           '<p>Show the AI what you want: <i>"Make 3 quiz questions like this one: What does CPU stand for?"</i></p>'),
          ('Improve the answer (iterate)',
           '<ul><li>"Make it shorter."</li><li>"Use a simpler example."</li><li>"Put it in a table."</li></ul><p class="wt-key">Prompting is a conversation: refine until it is right.</p>'),
          ('Safe and honest',
           '<ul><li>No passwords or private data in prompts</li><li>Check facts: AI can invent things</li><li>Use AI to learn, not to cheat</li></ul>')],
         [match('Match each part of the prompt to its role.', [('Role', 'You are a history teacher'), ('Task', 'Summarise the history of Cameroon'), ('Context', 'for Form 2 students revising for a test'), ('Format', 'in 6 bullet points')]),
          mcq('Which prompt is the strongest?', ['"Explain the CPU."', '"You are a computer teacher. Explain the parts of the CPU to a Form 2 student in a table with 3 rows."', '"CPU?"'], '"You are a computer teacher. Explain the parts of the CPU to a Form 2 student in a table with 3 rows."', 'It has a role, a task, context and a format.'),
          order('Put the steps of good prompting in order.', ['Write a clear prompt', 'Read the answer', 'Ask for changes to improve it', 'Check facts with a trusted source'], 'Write, read, refine, verify.'),
          sort('Safe to put in a prompt?', ['Safe', 'Not safe'], [('A question about photosynthesis', 'Safe'), ('Your mobile money PIN', 'Not safe'), ('Your friend\'s home address', 'Not safe'), ('"Give me 5 revision questions on fractions"', 'Safe')]),
          tf('If the AI answer is too hard, you can ask it to explain more simply.', True)]),

    8: L('Programmers solve problems in clear steps: understand, plan, build, test.',
         [('The problem-solving steps', STEPS),
          ('Steps explained',
           '<ol><li><b>Define</b>: what exactly is the problem?</li><li><b>Analyse</b>: what are the inputs, the outputs and the processing?</li><li><b>Design</b>: write the algorithm (the steps)</li><li><b>Code</b>: write the program</li><li><b>Test</b>: try it and fix errors (bugs)</li><li><b>Document</b>: explain how to use it</li></ol>'),
          ('Analyse with an IPO table',
           '<p>Problem: find the average of 3 marks.</p>' + table(['Input', 'Processing', 'Output'], [['mark1, mark2, mark3', 'sum ÷ 3', 'average']]) +
           '<p class="wt-key">Always find the inputs and outputs first.</p>')],
         [order('Put the problem-solving steps in order.', ['Define the problem', 'Analyse inputs and outputs', 'Design the algorithm', 'Code the program', 'Test and fix errors', 'Document'], 'Understand before you build, test before you share.'),
          sort('Problem: calculate the area of a rectangle. Sort each item.', ['Input', 'Processing', 'Output'], [('Length', 'Input'), ('Width', 'Input'), ('Multiply length × width', 'Processing'), ('Area', 'Output')]),
          sort('Problem: convert a price in FCFA to euros. Sort each item.', ['Input', 'Processing', 'Output'], [('Price in FCFA', 'Input'), ('Divide by 656', 'Processing'), ('Price in euros', 'Output')]),
          mcq('An error in a program is called…', ['a bug', 'a byte', 'a pixel'], 'a bug', 'Finding and fixing bugs is called debugging.'),
          mcq('In which step do you check that the program gives correct results?', ['Testing', 'Defining', 'Documenting'], 'Testing')]),

    9: L('We describe an algorithm in pseudocode or with a flowchart before we code it.',
         [('Flowchart symbols', SYMBOLS +
           '<ol><li><b>Oval</b>: Start / End</li><li><b>Parallelogram</b>: Input / Output (Read, Write)</li><li><b>Rectangle</b>: Process (calculation)</li><li><b>Diamond</b>: Decision (Yes / No question)</li></ol>'),
          ('Pseudocode',
           '<p>Pseudocode is the algorithm in simple, structured English:</p><p><code>Start<br>Read mark<br>If mark ≥ 10 Then Write "Pass"<br>Else Write "Fail"<br>End If<br>End</code></p>'),
          ('The same as a flowchart', FLOWCHART),
          ('Three structures',
           '<ul><li><b>Sequence</b>: steps one after another</li><li><b>Selection</b>: a choice (If … Then … Else)</li><li><b>Iteration</b>: repeat (loop)</li></ul>')],
         [label('Name each flowchart symbol.', SYMBOLS, ['Start / End', 'Input / Output', 'Process', 'Decision']),
          match('Which symbol do you use?', [('Read age', 'Parallelogram'), ('total ← a + b', 'Rectangle'), ('Is age ≥ 18?', 'Diamond'), ('Start', 'Oval')]),
          mcq('In the flowchart, a student scores 12. What is written?', ['Pass', 'Fail', 'Nothing'], 'Pass', '12 ≥ 10 is true, so we follow the "Yes" arrow.', visual=FLOWCHART),
          mcq('In the same flowchart, a student scores 9. What is written?', ['Fail', 'Pass', '9'], 'Fail', '9 ≥ 10 is false, so we follow "No".'),
          sort('Which structure is it?', ['Sequence', 'Selection', 'Iteration'], [('Read a, then read b, then write a + b', 'Sequence'), ('If it rains, take an umbrella', 'Selection'), ('Repeat 10 times: do a push-up', 'Iteration'), ('If mark ≥ 10 write Pass else write Fail', 'Selection')]),
          order('Put this pseudocode in the right order to calculate the area of a rectangle.', ['Start', 'Read length, width', 'area ← length × width', 'Write area', 'End'])]),

    11: L('The operating system (OS) is the main program that manages the computer and lets you use it.',
          [('Where the OS sits', OS_LAYERS + '<p class="wt-key">The OS is the link between you, your apps and the hardware.</p>'),
           ('What the OS does',
            '<ul><li>Manages the <b>processor</b> (which program runs)</li><li>Manages <b>memory</b> (RAM)</li><li>Manages <b>files and folders</b></li><li>Manages <b>devices</b> (printer, keyboard)</li><li>Gives a <b>user interface</b></li><li>Provides <b>security</b> (passwords, accounts)</li></ul>'),
           ('Types of interface',
            '<div class="two-col"><div><b>CLI</b> (Command Line)you type commands: <code>dir</code>, <code>cd</code></div><div><b>GUI</b> (Graphical)you click windows, icons, menus</div></div>'),
           ('Examples',
            table(['Computers', 'Phones'], [['Windows', 'Android'], ['Linux', 'iOS'], ['macOS', '']]) +
            '<p><b>Multitasking</b> OS: runs many programs at once. <b>Multi-user</b> OS: many people with their own accounts.</p>')],
          [order('From top to bottom, put the layers in order.', ['User', 'Application software', 'Operating system', 'Hardware'], 'The OS sits between applications and hardware.'),
           match('Match the OS function to an example.', [('File management', 'Creating and deleting folders'), ('Memory management', 'Giving RAM to each open program'), ('Device management', 'Sending a document to the printer'), ('Security', 'Asking for a password at login')]),
           sort('Computer OS or phone OS?', ['Computer', 'Phone'], [('Windows', 'Computer'), ('Android', 'Phone'), ('macOS', 'Computer'), ('iOS', 'Phone'), ('Linux', 'Computer')]),
           mcq('You type "dir" to list files. Which interface are you using?', ['Command line interface (CLI)', 'Graphical user interface (GUI)', 'Touch interface'], 'Command line interface (CLI)'),
           tf('A multitasking OS can run several programs at the same time.', True),
           mcq('Which is NOT an operating system?', ['Microsoft Word', 'Linux', 'Android'], 'Microsoft Word', 'Word is application software.')]),

    12: L('Utility programs keep the computer healthy. Device drivers let the OS talk to hardware.',
          [('Utility software',
            table(['Utility', 'What it does'], [['Antivirus', 'finds and removes malware'], ['Disk cleanup', 'deletes useless files'], ['Defragmenter', 'reorganises a hard disk to make it faster'], ['Backup', 'copies files to keep them safe'], ['Compression', 'makes files smaller (zip)'], ['File manager', 'organises files and folders']])),
           ('Device drivers',
            flow([('OS', 'Windows'), ('Driver', 'translator'), ('Device', 'printer')]) +
            '<p>A <b>driver</b> is a small program that tells the OS how to use one device. A new printer often needs its driver installed.</p>'),
           ('Signs of a driver problem',
            '<ul><li>Device not recognised</li><li>No sound, or a blurry screen</li><li>Yellow warning sign in Device Manager</li></ul><p class="wt-key">Fix: install or update the right driver.</p>')],
          [match('Match the utility to its job.', [('Antivirus', 'Finds and removes malware'), ('Disk cleanup', 'Deletes useless temporary files'), ('Compression', 'Makes files smaller'), ('Backup', 'Keeps a copy of your files'), ('Defragmenter', 'Reorganises a hard disk')]),
           mcq('A device driver is…', ['a program that lets the OS use a device', 'a person who drives a computer', 'a cable'], 'a program that lets the OS use a device'),
           mcq('You plug in a new printer, but Windows does not recognise it. What should you install?', ['Its driver', 'A game', 'A new mouse'], 'Its driver'),
           sort('Utility software or application software?', ['Utility', 'Application'], [('Antivirus', 'Utility'), ('Microsoft Word', 'Application'), ('Disk cleanup', 'Utility'), ('A web browser', 'Application'), ('WinZip', 'Utility')]),
           tf('Compressing a file makes it smaller, so it is faster to send.', True)]),

    15: L('Computers store every number as bits. With n bits we can write 2ⁿ different numbers.',
          [('Bits and bytes',
            '<ul><li>A <b>bit</b> is 0 or 1</li><li>A <b>byte</b> = 8 bits</li><li>A <b>nibble</b> = 4 bits</li></ul>'),
           ('How many values?',
            table(['Bits', 'Values (2ⁿ)', 'Range'], [['1', '2', '0 – 1'], ['2', '4', '0 – 3'], ['4', '16', '0 – 15'], ['8', '256', '0 – 255']]) +
            '<p class="wt-key">n bits → 2ⁿ values, from 0 to 2ⁿ − 1.</p>'),
           ('Writing a number on 8 bits',
            '<p>13 in binary is 1101. On 8 bits we add zeros on the left:</p><p><b>13 = 0000 1101</b></p>' +
            table(['128', '64', '32', '16', '8', '4', '2', '1'], [['0', '0', '0', '0', '1', '1', '0', '1']]) + '<p>8 + 4 + 1 = 13</p>'),
           ('Overflow',
            '<p>The biggest number on 8 bits is <b>255 = 1111 1111</b>. A result bigger than 255 does not fit: this is an <b>overflow</b> error.</p>'),
           ('Negative numbers (sign bit)',
            '<p>One way: use the leftmost bit as a <b>sign</b>: 0 = positive, 1 = negative.</p><p>+5 = <b>0</b>000 0101 &nbsp; −5 = <b>1</b>000 0101</p>')],
          [fill('Complete.', '1 byte = {0} bits.', [['8']]),
           fill('How many different values can you write with 4 bits?', '{0}', [['16']], '2⁴ = 16'),
           fill('What is the biggest number you can write with 8 bits?', '{0}', [['255']], '2⁸ − 1 = 255'),
           mcq('Write 5 on 8 bits.', ['00000101', '101', '10100000'], '00000101', '5 = 101, then add zeros on the left to make 8 bits.'),
           fill('Which number is 0000 1010?', '{0}', [['10']], '8 + 2 = 10'),
           mcq('An 8-bit calculation gives 300. What happens?', ['Overflow: it does not fit', 'It is stored normally', 'It becomes negative 300'], 'Overflow: it does not fit', '300 > 255.'),
           mcq('With a sign bit, what is 1000 0011?', ['−3', '+3', '131'], '−3', 'Leftmost bit 1 = negative; 000 0011 = 3.')]),

    16: L('Every letter, digit and symbol has a number code. The computer stores that code in binary.',
          [('The idea',
            '<p>The computer only stores numbers. So each character gets a <b>code</b>: <b>A = 65</b>. The code is stored in binary: 65 = 0100 0001.</p>'),
           ('ASCII',
            '<p><b>ASCII</b> uses 7 bits → 128 characters (English letters, digits, symbols).</p>' +
            table(['Char', 'Code', 'Char', 'Code'], [['space', '32', 'A', '65'], ['0', '48', 'B', '66'], ['1', '49', 'a', '97'], ['9', '57', 'b', '98']]) +
            '<p class="wt-key">Letters follow each other: if A = 65 then C = 67. Lower case = upper case + 32.</p>'),
           ('Encode a word',
            '<p><b>CAB</b> → C = 67, A = 65, B = 66 → <b>67 65 66</b></p><p>Decode <b>72 73</b> → H I → "HI"</p>'),
           ('Unicode',
            '<p>ASCII cannot write é, ñ, Chinese or emojis. <b>Unicode</b> (UTF-8) has codes for more than 140 000 characters from every language. 😀</p>')],
          [fill('Use A = 65. What is the code of D?', 'D = {0}', [['68']], 'A=65, B=66, C=67, D=68.'),
           fill('Use a = 97. What is the code of c?', 'c = {0}', [['99']]),
           fill('Encode the word "BAD" (A = 65).', '{0} {1} {2}', [['66'], ['65'], ['68']]),
           mcq('Decode 72 69 89 (A = 65).', ['HEY', 'HAY', 'GEY'], 'HEY', '72 = H, 69 = E, 89 = Y.'),
           mcq('The code of "M" is 77. What is the code of "m"?', ['109', '78', '45'], '109', 'Lower case = upper case + 32: 77 + 32 = 109.'),
           mcq('How many characters can 7-bit ASCII code?', ['128', '256', '7'], '128', '2⁷ = 128'),
           tf('Unicode can encode emojis and letters from many languages.', True)]),
}
