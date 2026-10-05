"""Form 1 Computer Science — chapters 10 to 14."""
from helpers import *

WINDOW = svg(440, 250, ''.join([
    '<rect x="10" y="10" width="420" height="230" rx="10" class="v-line"/>',
    '<rect x="10" y="10" width="420" height="30" rx="10" class="v-box"/>',
    '<text x="24" y="31" class="v-t">My Document - Word</text>',
    '<rect x="362" y="17" width="16" height="16" class="v-line"/><rect x="384" y="17" width="16" height="16" class="v-line"/><rect x="406" y="17" width="16" height="16" rx="3" fill="#ff6b6b"/>',
    '<rect x="10" y="40" width="420" height="24" class="v-box2"/>',
    '<text x="24" y="57" class="v-s">File   Home   Insert   Layout   View</text>',
    '<rect x="20" y="74" width="390" height="140" rx="4" fill="rgba(255,255,255,0.05)"/>',
    '<rect x="414" y="74" width="10" height="140" rx="4" class="v-box3"/>',
    '<rect x="10" y="218" width="420" height="22" class="v-box"/>',
    marker(140, 25, 1), marker(370, 48, 2), marker(250, 52, 3), marker(200, 140, 4), marker(419, 120, 5), marker(80, 229, 6),
]), 'Parts of a window')

DESKTOP_GUI = svg(440, 200, ''.join([
    '<rect x="10" y="10" width="420" height="180" rx="10" fill="rgba(0,212,255,0.08)" class="v-line"/>',
    '<rect x="30" y="30" width="34" height="30" rx="4" class="v-box2"/><text x="47" y="74" text-anchor="middle" class="v-s">Folder</text>',
    '<rect x="30" y="90" width="34" height="30" rx="4" class="v-box3"/><text x="47" y="134" text-anchor="middle" class="v-s">Bin</text>',
    '<rect x="10" y="164" width="420" height="26" class="v-box"/>',
    '<rect x="16" y="168" width="40" height="18" rx="4" class="v-box2"/>',
    '<text x="400" y="182" text-anchor="end" class="v-s">10:45</text>',
    marker(76, 45, 1), marker(76, 105, 2), marker(36, 160, 3), marker(210, 177, 4), marker(380, 160, 5),
]), 'Parts of the desktop')

TREE = svg(420, 170, ''.join([
    box(150, 10, 120, 36, 'Documents', '', 'v-box2'),
    box(30, 80, 110, 36, 'School', '', 'v-box2'), box(280, 80, 110, 36, 'Photos', '', 'v-box2'),
    box(10, 130, 100, 30, 'maths.docx', '', 'v-box3'), box(120, 130, 100, 30, 'cs.docx', '', 'v-box3'), box(290, 130, 100, 30, 'party.jpg', '', 'v-box3'),
    arrow(190, 46, 95, 80), arrow(230, 46, 335, 80), arrow(70, 116, 60, 130), arrow(100, 116, 160, 130), arrow(335, 116, 340, 130),
]), 'Folder tree')

INTERNET = svg(420, 150, ''.join([
    box(10, 50, 90, 46, 'Your phone', '', 'v-box'), arrow(100, 73, 160, 73),
    box(160, 50, 100, 46, 'ISP', 'MTN, Orange…', 'v-box2'), arrow(260, 73, 320, 73),
    box(320, 50, 90, 46, 'Internet', 'servers', 'v-box3'),
    '<text x="210" y="130" text-anchor="middle" class="v-s">Your device → Internet Service Provider → the internet</text>',
]), 'How you connect to the internet')

LESSONS = {
    40: L('System software runs the computer itself. Without it, nothing else can work.',
          [('What is system software?', '<p>Programs that <b>control the computer</b> and help other programs run.</p>'),
           ('Types',
            '<ul><li><b>Operating system</b>: Windows, Linux, macOS, Android, iOS</li><li><b>Utility programs</b>: antivirus, disk cleanup, file compression</li><li><b>Device drivers</b>: let the computer use a printer, mouse…</li></ul>'),
           ('The operating system\'s jobs', '<div class="chips"><span>Starts the computer</span><span>Manages files</span><span>Runs programs</span><span>Controls devices</span><span>Gives a user interface</span></div>')],
          [sort('Operating system or utility?', ['Operating system', 'Utility program'], [('Windows 11', 'Operating system'), ('Antivirus', 'Utility program'), ('Android', 'Operating system'), ('Disk cleanup', 'Utility program'), ('Linux', 'Operating system')]),
           mcq('Which program lets the computer use a new printer?', ['Device driver', 'Word processor', 'Web browser'], 'Device driver'),
           tf('A computer can run Microsoft Word without an operating system.', False, 'Every application needs the operating system.')]),

    41: L('Application software is the programs we use to do our tasks: write, calculate, draw, browse…',
          [('Examples',
            '<ul><li><b>Word processor</b>: write letters — MS Word, LibreOffice Writer</li><li><b>Spreadsheet</b>: calculate — MS Excel</li><li><b>Presentation</b>: slides — PowerPoint</li><li><b>Graphics</b>: draw and edit pictures — Paint, Photoshop</li><li><b>Web browser</b>: visit websites — Chrome, Firefox</li></ul>'),
           ('System vs application', '<div class="two-col"><div><b>System software</b>runs the computer</div><div><b>Application software</b>does the user\'s tasks</div></div>')],
          [match('Match the task to the application.', [('Write a letter', 'Word processor'), ('Calculate class averages', 'Spreadsheet'), ('Make slides for a talk', 'Presentation software'), ('Edit a photo', 'Graphics software'), ('Visit a website', 'Web browser')]),
           sort('System or application software?', ['System software', 'Application software'], [('Microsoft Excel', 'Application software'), ('Windows', 'System software'), ('Google Chrome', 'Application software'), ('Device driver', 'System software'), ('PowerPoint', 'Application software')]),
           mcq('Which is application software?', ['Microsoft Word', 'BIOS', 'Windows'], 'Microsoft Word')]),

    43: L('A GUI (Graphical User Interface) lets you use the computer with pictures, windows and a mouse.',
          [('The desktop', DESKTOP_GUI + '<p>1 Icon · 2 Recycle Bin · 3 Start button · 4 Taskbar · 5 Clock / notification area</p>'),
           ('A window', WINDOW + '<p>1 Title bar · 2 Minimise/Maximise/Close · 3 Menu bar · 4 Work area · 5 Scroll bar · 6 Status bar</p>'),
           ('WIMP', '<p>A GUI uses <b>W</b>indows, <b>I</b>cons, <b>M</b>enus and a <b>P</b>ointer.</p>')],
          [label('Label the desktop.', DESKTOP_GUI, ['Icon', 'Recycle Bin', 'Start button', 'Taskbar', 'Clock']),
           label('Label the window.', WINDOW, ['Title bar', 'Close / minimise buttons', 'Menu bar', 'Work area', 'Scroll bar', 'Status bar']),
           fill('What does WIMP stand for?', '{0}, {1}, {2}, {3}', [['Windows', 'Window'], ['Icons', 'Icon'], ['Menus', 'Menu'], ['Pointer', 'Pointers']]),
           mcq('Which button makes a window disappear to the taskbar without closing it?', ['Minimise', 'Close', 'Maximise'], 'Minimise')]),

    44: L('Files hold your work. Folders keep files organised, like drawers in a cupboard.',
          [('Files and folders', TREE + '<p>A folder can hold files and other folders.</p>'),
           ('Operations', '<ul><li><b>Create</b> a new folder (right-click → New → Folder)</li><li><b>Rename</b> (right-click → Rename, or F2)</li><li><b>Copy</b> (Ctrl+C) and <b>Paste</b> (Ctrl+V)</li><li><b>Cut</b> (Ctrl+X) to move</li><li><b>Delete</b> (goes to the Recycle Bin)</li></ul>'),
           ('Copy vs move', '<p class="wt-key">Copy makes a second copy. Move (cut + paste) changes where the file is.</p>')],
          [match('Match the shortcut to the action.', [('Ctrl + C', 'Copy'), ('Ctrl + V', 'Paste'), ('Ctrl + X', 'Cut'), ('F2', 'Rename'), ('Delete', 'Send to Recycle Bin')]),
           order('Put the steps to copy a file into a folder in order.', ['Select the file', 'Press Ctrl + C', 'Open the destination folder', 'Press Ctrl + V']),
           mcq('Where does a deleted file go first?', ['Recycle Bin', 'Printer', 'Taskbar'], 'Recycle Bin', 'You can restore it from the Recycle Bin.'),
           tf('A folder can contain other folders.', True),
           mcq('In the tree, which folder contains "cs.docx"?', ['School', 'Photos', 'Desktop'], 'School', visual=TREE)]),

    46: L('A word processor is used to type, edit, format and print documents.',
          [('What can you do?', '<div class="chips"><span>Type text</span><span>Edit (correct)</span><span>Format (make it nice)</span><span>Insert pictures and tables</span><span>Save and print</span></div>'),
           ('Formatting', '<ul><li><b>Bold</b> (Ctrl+B), <i>Italic</i> (Ctrl+I), <u>Underline</u> (Ctrl+U)</li><li>Font, size, colour</li><li>Alignment: left, centre, right, justify</li></ul>'),
           ('Examples', '<p>MS Word, LibreOffice Writer, Google Docs, WPS Writer</p>')],
          [match('Match the shortcut to the format.', [('Ctrl + B', 'Bold'), ('Ctrl + I', 'Italic'), ('Ctrl + U', 'Underline'), ('Ctrl + S', 'Save')]),
           sort('Editing or formatting?', ['Editing', 'Formatting'], [('Correcting a spelling mistake', 'Editing'), ('Making a title bold', 'Formatting'), ('Deleting a sentence', 'Editing'), ('Changing the font size', 'Formatting')]),
           mcq('Which is a word processor?', ['Microsoft Word', 'Microsoft Excel', 'Paint'], 'Microsoft Word')]),

    47: L('A spreadsheet is a grid of cells used to store numbers and calculate automatically.',
          [('The grid', '<p><b>Columns</b> have letters (A, B, C), <b>rows</b> have numbers (1, 2, 3). Where they meet is a <b>cell</b>, e.g. <b>B3</b>.</p>'),
           ('Formulas', '<p>A formula starts with <b>=</b></p><ul><li><span class="g-code">=A1+B1</span> adds two cells</li><li><span class="g-code">=SUM(A1:A5)</span> adds a range</li><li><span class="g-code">=AVERAGE(B1:B10)</span> finds the mean</li></ul>'),
           ('Examples', '<p>MS Excel, LibreOffice Calc, Google Sheets</p>')],
          [fill('Name the cell.', 'The cell in column C and row 4 is called {0}.', [['C4']]),
           match('Match the formula to what it does.', [('=SUM(A1:A5)', 'Adds A1 to A5'), ('=AVERAGE(A1:A5)', 'Finds the mean of A1 to A5'), ('=A1*B1', 'Multiplies A1 by B1'), ('=MAX(A1:A5)', 'Finds the biggest value')]),
           mcq('Every formula starts with…', ['=', '+', '#'], '='),
           tf('Columns are named with numbers.', False, 'Columns use letters; rows use numbers.')]),

    48: L('Graphics software is used to draw, paint and edit pictures.',
          [('Examples', '<p>Paint, GIMP, Photoshop, Canva, Inkscape</p>'),
           ('Common tools', '<ul><li><b>Pencil / brush</b>: draw freely</li><li><b>Shapes</b>: lines, rectangles, circles</li><li><b>Fill (bucket)</b>: colour an area</li><li><b>Eraser</b>: rub out</li><li><b>Text</b>: add words</li><li><b>Select & crop</b>: cut part of a picture</li></ul>')],
          [match('Match the tool to its job.', [('Fill bucket', 'Colours a closed area'), ('Eraser', 'Rubs out'), ('Crop', 'Keeps only part of a picture'), ('Text tool', 'Adds words to a picture')]),
           mcq('Which program is graphics software?', ['Paint', 'Excel', 'Chrome'], 'Paint'),
           tf('Canva can be used to design a poster.', True)]),

    50: L('The internet is a worldwide network of computers that share information.',
          [('What is the internet?', '<p>Millions of computers connected together across the world.</p>' + INTERNET),
           ('What we use it for', '<div class="chips"><span>Websites (WWW)</span><span>Email</span><span>Social media</span><span>Video calls</span><span>Online learning</span><span>Mobile money</span></div>'),
           ('What you need', '<ul><li>A device (phone, computer)</li><li>An Internet Service Provider (ISP): MTN, Orange, Camtel, Nexttel…</li><li>Data bundle or Wi-Fi</li><li>A browser or app</li></ul>')],
          [order('How does your phone reach a website?', ['Your phone', 'Internet Service Provider', 'The internet', 'The website\'s server'], visual=INTERNET),
           mcq('Which is an Internet Service Provider in Cameroon?', ['MTN', 'Microsoft Word', 'Google Chrome'], 'MTN'),
           sort('Needs the internet or not?', ['Needs internet', 'Works offline'], [('Sending an email', 'Needs internet'), ('Typing in Word', 'Works offline'), ('Watching YouTube', 'Needs internet'), ('Using a calculator app', 'Works offline')]),
           tf('The internet and the World Wide Web are exactly the same thing.', False, 'The WWW (websites) is one service that runs on the internet.')]),

    51: L('A web browser opens websites. A search engine helps you find them.',
          [('Browser vs search engine', '<div class="two-col"><div><b>Browser</b>program that shows websites: Chrome, Firefox, Edge, Safari</div><div><b>Search engine</b>website that finds pages: Google, Bing, DuckDuckGo</div></div>'),
           ('Parts of a web address', '<p><span class="g-code">https://www.asghinlabs.com/lessons.html</span></p><ul><li><b>https</b>: secure protocol</li><li><b>asghinlabs.com</b>: domain name</li><li><b>lessons.html</b>: the page</li></ul>'),
           ('Search tips', '<ul><li>Use key words: "causes of malaria" not "what are all the things that cause…"</li><li>Use quotes for exact words: "Ada Lovelace"</li><li>Check who wrote the page</li></ul>')],
          [sort('Browser or search engine?', ['Browser', 'Search engine'], [('Google Chrome', 'Browser'), ('Google Search', 'Search engine'), ('Mozilla Firefox', 'Browser'), ('Bing', 'Search engine'), ('Microsoft Edge', 'Browser')]),
           mcq('In https://www.mtn.cm, what is "mtn.cm"?', ['The domain name', 'The browser', 'The search engine'], 'The domain name'),
           mcq('Which search is best for finding the inventor of the telephone?', ['inventor telephone', 'I want to know who it was that made the first ever telephone please', 'phone'], 'inventor telephone', 'Short key words give better results.'),
           tf('A padlock and "https" mean the connection is secure.', True)]),

    53: L('Computer rooms have dangers. Knowing them keeps you safe.',
          [('Electric shock', '<ul><li>Never touch bare wires or open a computer that is plugged in</li><li>Keep liquids away</li><li>Don\'t overload sockets</li></ul>'),
           ('Fire', '<ul><li>Caused by overloaded sockets, damaged cables, overheating</li><li>Use a <b>CO₂</b> extinguisher, never water, on electrical fires</li><li>Know the exit</li></ul>'),
           ('Flood', '<ul><li>Keep computers off the floor</li><li>Switch off power if water enters the room</li></ul>')],
          [match('Match the danger to a way to prevent it.', [('Electric shock', 'Don\'t touch bare wires'), ('Fire', 'Don\'t overload sockets'), ('Flood', 'Keep computers off the floor')]),
           order('A small electrical fire starts. Put the actions in order.', ['Raise the alarm and tell the teacher', 'Switch off the power if it is safe', 'Use a CO₂ extinguisher (trained adults)', 'Leave by the nearest exit']),
           tf('Water is safe to use on a computer fire.', False, 'Water conducts electricity.'),
           mcq('Plugging many devices into one socket can cause…', ['a fire', 'faster internet', 'better sound'], 'a fire')]),

    54: L('Using computers for a long time in a bad position can hurt your body. Good habits prevent it.',
          [('Common problems', '<ul><li><b>Eye strain</b>: tired, dry eyes</li><li><b>Back and neck pain</b>: bad posture</li><li><b>Wrist pain</b> (RSI): repeating the same movement</li><li><b>Headaches</b></li></ul>'),
           ('Prevention', '<ul><li>Sit up straight, feet flat</li><li>Screen at eye level, an arm\'s length away</li><li><b>20-20-20 rule</b>: every 20 minutes, look 20 feet (6 m) away for 20 seconds</li><li>Take breaks, stretch</li></ul>')],
          [match('Match the problem to its prevention.', [('Eye strain', 'Follow the 20-20-20 rule'), ('Back pain', 'Sit up straight with back support'), ('Wrist pain', 'Keep wrists straight and take breaks'), ('Neck pain', 'Screen at eye level')]),
           sort('Good habit or bad habit?', ['Good habit', 'Bad habit'], [('Taking a break every hour', 'Good habit'), ('Using a phone in the dark for hours', 'Bad habit'), ('Sitting with a straight back', 'Good habit'), ('Screen very close to the face', 'Bad habit')]),
           fill('Complete the rule.', 'Every {0} minutes, look 20 feet away for {1} seconds.', [['20'], ['20']])]),
}
