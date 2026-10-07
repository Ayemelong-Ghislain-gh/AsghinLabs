"""Lower Sixth ICT: digital citizenship, cybersecurity, systems and information systems (lessons 35-47)."""
from helpers import *
from f3_maths_part1 import table


def dfd_shape(kind, x, y, w, h, t):
    if kind == 'entity':
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="v-box"/><text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>'
    if kind == 'process':
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="v-box2"/><text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>'
    return (f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" class="v-line" style="stroke-width:2"/>'
            f'<line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" class="v-line" style="stroke-width:2"/>'
            f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" class="v-line" style="stroke-width:2"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="v-t">{t}</text>')


DFD = svg(440, 200, ''.join([
    dfd_shape('entity', 10, 70, 100, 50, 'Student'),
    dfd_shape('process', 170, 65, 110, 60, 'Register'),
    dfd_shape('store', 320, 145, 115, 40, 'D1 Students'),
    dfd_shape('entity', 330, 20, 100, 50, 'Bursar'),
    arrow(110, 95, 170, 95), arrow(280, 85, 330, 50), arrow(260, 125, 330, 160),
    '<text x="140" y="88" text-anchor="middle" class="v-s">details</text>',
    '<text x="318" y="78" class="v-s">fees due</text>',
    marker(10, 70, 1), marker(170, 65, 2), marker(320, 145, 3),
]), 'Data flow diagram')

SYSTEM = flow([('Input', ''), ('Process', ''), ('Output', '')])

LESSONS = {
    35: L('Computers bring huge benefits but can also be misused.',
          [('Positive uses', '<ul><li>Education: e-learning, research</li><li>Health: records, telemedicine</li><li>Business: e-commerce, mobile money</li><li>Communication: email, video calls</li><li>Government: e-services, ID systems</li></ul>'),
           ('Negative uses / effects', '<ul><li>Cybercrime, fraud, scams</li><li>Cyberbullying, hate speech, fake news</li><li>Addiction, isolation, health problems</li><li>Job losses through automation</li><li>E-waste pollution</li></ul>')],
          [sort('Positive or negative use?', ['Positive', 'Negative'], [('Telemedicine for remote villages', 'Positive'), ('Phishing scam messages', 'Negative'), ('Mobile money payments', 'Positive'), ('Spreading fake news', 'Negative'), ('E-learning platforms', 'Positive'), ('Cyberbullying', 'Negative')]),
           mcq('Which is an environmental impact of computers?', ['E-waste', 'Online banking', 'Video calls'], 'E-waste'),
           tf('Automation can replace some jobs while creating new ones.', True)]),

    36: L('Computer ethics are moral rules for using ICT. Laws make some behaviour illegal; Cameroon has specific cyber laws.',
          [('Ethics', '<ul><li>Respect privacy</li><li>Don\'t use others\' work without permission</li><li>Don\'t access systems without authorisation</li><li>Be honest and respectful online</li></ul>'),
           ('Cameroon law', '<p>Law No. 2010/012 of 21 December 2010 on <b>cybersecurity and cybercriminality</b> punishes illegal access, data interception, online fraud, child abuse content and spreading false news online. Law No. 2010/013 regulates electronic communications.</p><p>Bodies: <b>ANTIC</b> (security of ICT), <b>ART</b> (telecom regulator).</p>'),
           ('Ethics vs law', '<p class="wt-key">Something can be legal but unethical; laws are enforced, ethics are personal and professional standards.</p>')],
          [sort('Ethical or unethical?', ['Ethical', 'Unethical'], [('Citing the source of a picture', 'Ethical'), ('Reading a friend\'s messages without permission', 'Unethical'), ('Using licensed software', 'Ethical'), ('Sharing someone\'s private photo', 'Unethical')]),
           mcq('Which Cameroonian law deals with cybercrime?', ['Law No. 2010/012 on cybersecurity and cybercriminality', 'The Highway Code', 'The Labour Code'], 'Law No. 2010/012 on cybersecurity and cybercriminality'),
           mcq('Which agency handles the security of ICT in Cameroon?', ['ANTIC', 'ENEO', 'CAMTEL only'], 'ANTIC'),
           tf('Everything that is legal is also ethical.', False)]),

    37: L('Data protection keeps personal data safe; copyright protects creators; the digital divide is unequal access to ICT.',
          [('Data protection principles', '<ul><li>Collect only what is needed, for a clear purpose</li><li>Keep it accurate and secure</li><li>Don\'t keep it longer than needed</li><li>Get consent; respect people\'s rights</li></ul>'),
           ('Copyright', '<p>Protects software, music, text, images. Infringement: piracy, copying without permission. Alternatives: licences, <b>Creative Commons</b>, public domain, fair use for teaching with citation.</p>'),
           ('Digital divide', '<p>Gap between those with and without access to ICT: urban/rural, rich/poor, men/women, young/old. Causes: cost, electricity, connectivity, skills.</p>')],
          [sort('Respects or breaks data protection?', ['Respects', 'Breaks'], [('Asking consent before collecting phone numbers', 'Respects'), ('Selling a customer list without permission', 'Breaks'), ('Encrypting patient records', 'Respects'), ('Keeping old CVs forever "just in case"', 'Breaks')]),
           mcq('Copying and selling a film without permission is…', ['copyright infringement (piracy)', 'fair use', 'data protection'], 'copyright infringement (piracy)'),
           mcq('Which is a cause of the digital divide in rural areas?', ['Poor connectivity and electricity', 'Too many computers', 'Fast internet'], 'Poor connectivity and electricity'),
           tf('Creative Commons licences let creators share work under chosen conditions.', True)]),

    38: L('Protect systems from illegal access with physical security, authentication, access rights, firewalls and encryption.',
          [('Measures', table(['Measure', 'How it protects'], [['Physical security', 'locks, guards, CCTV, biometric doors'], ['Authentication', 'passwords, PIN, biometrics, two-factor (2FA)'], ['Access rights', 'users only see/edit what they need'], ['Firewall', 'filters network traffic'], ['Encryption', 'makes stolen data unreadable'], ['Audit logs', 'record who did what']])),
           ('Strong passwords', '<p>Long (12+), mix of characters, unique per site, use a password manager, never share.</p>')],
          [match('Match the threat to the measure.', [('Someone steals a laptop', 'Encrypt the disk'), ('Hackers probe open ports', 'Firewall'), ('A password is stolen', 'Two-factor authentication'), ('A clerk views salaries', 'Access rights')]),
           mcq('Which is the strongest password?', ['Rain-Mango-Tiger-82!', 'password123', 'Awa2008'], 'Rain-Mango-Tiger-82!'),
           tf('Encryption makes stolen data unreadable without the key.', True)]),

    39: L('Plan for disasters with backups and recovery, and work safely with ICT equipment.',
          [('Backup and recovery', '<ul><li><b>Full</b>, <b>incremental</b>, <b>differential</b> backups</li><li>3-2-1 rule: 3 copies, 2 media, 1 off-site</li><li>UPS for power cuts, RAID for disk failure</li><li>Disaster recovery plan: what to do, who does it, how fast</li></ul>'),
           ('Safe working practices', '<ul><li>No food or drinks near equipment</li><li>No overloaded sockets, no trailing cables</li><li>Fire extinguisher (CO₂) for electrical fires</li><li>Ventilation, good lighting, breaks</li></ul>')],
          [match('Match the risk to the measure.', [('Power cut', 'UPS'), ('Disk failure', 'RAID / backups'), ('Fire in the server room', 'CO₂ extinguisher'), ('Tripping over cables', 'Cable management')]),
           mcq('Which backup copies only files changed since the last backup of any type?', ['Incremental', 'Full', 'Differential'], 'Incremental'),
           tf('Water is the right extinguisher for an electrical fire.', False)]),

    40: L('Computer crimes include hacking, fraud, identity theft and cyberbullying. They are fought with technology, law and awareness.',
          [('Crimes', table(['Crime', 'Meaning'], [['Hacking', 'unauthorised access to systems'], ['Phishing', 'fake messages to steal details'], ['Identity theft', 'using someone\'s personal details'], ['Online fraud / scams', 'fake sales, "feyman" scams, SIM swap'], ['Cyberbullying', 'harassing people online'], ['Piracy', 'illegal copying of software/media'], ['Denial of service', 'flooding a site so it crashes']])),
           ('Combat measures', '<ul><li>Laws and cyber police; reporting to ANTIC</li><li>Firewalls, antivirus, updates, 2FA</li><li>Awareness: don\'t click unknown links, verify senders</li></ul>')],
          [match('Match the crime.', [('Fake bank SMS asking for your PIN', 'Phishing'), ('Flooding a website with traffic', 'Denial of service'), ('Using a stolen ID to open an account', 'Identity theft'), ('Copying and selling software', 'Piracy')]),
           mcq('You get a message: "You won 1 000 000 FCFA, send 10 000 to claim." What is it?', ['A scam', 'A real prize', 'A software update'], 'A scam'),
           tf('Two-factor authentication helps against stolen passwords.', True)]),

    41: L('Malware is malicious software. Each type spreads and harms in its own way.',
          [('Types', table(['Malware', 'Characteristic'], [['Virus', 'attaches to files; spreads when they are run'], ['Worm', 'spreads by itself over networks'], ['Trojan', 'pretends to be useful software'], ['Ransomware', 'encrypts files and demands payment'], ['Spyware / keylogger', 'secretly records activity / keystrokes'], ['Adware', 'unwanted adverts'], ['Rootkit', 'hides deep in the system']])),
           ('Signs of infection', '<p>Slow computer, pop-ups, unknown programs, files changed or encrypted, browser redirects.</p>')],
          [match('Match the malware.', [('Encrypts your files and asks for money', 'Ransomware'), ('Spreads alone across a network', 'Worm'), ('Looks like a free game but is harmful', 'Trojan'), ('Records every key you press', 'Keylogger')]),
           mcq('Which needs a host file to spread?', ['Virus', 'Worm', 'Adware'], 'Virus'),
           sort('Sign of malware or normal?', ['Possible malware', 'Normal'], [('Files suddenly encrypted', 'Possible malware'), ('Browser opens strange sites', 'Possible malware'), ('Windows update installs', 'Normal'), ('Many unexpected pop-ups', 'Possible malware')])]),

    42: L('Prevent, detect and remove malware with good habits and security software.',
          [('Prevention', '<ul><li>Install and update antivirus</li><li>Update the OS and apps (patches)</li><li>Don\'t open unknown attachments or links</li><li>Download only from trusted sources</li><li>Scan USB drives; use a firewall; back up</li></ul>'),
           ('Detection', '<p>Antivirus uses <b>signatures</b> (known patterns) and <b>heuristics</b> (suspicious behaviour). Infected files are <b>quarantined</b> or deleted.</p>'),
           ('Recovery', '<p>Disconnect from the network, scan in Safe Mode, restore from a clean backup.</p>')],
          [order('Order the response to an infection.', ['Disconnect from the network', 'Run a full scan', 'Quarantine or delete threats', 'Restore files from a clean backup']),
           mcq('Antivirus finding new, unknown malware by behaviour uses…', ['heuristics', 'signatures only', 'defragmentation'], 'heuristics'),
           mcq('What does "quarantine" do?', ['Isolates a suspicious file so it cannot run', 'Deletes all files', 'Speeds up the PC'], 'Isolates a suspicious file so it cannot run'),
           tf('Updating software closes security holes.', True)]),

    43: L('A system is a set of parts working together towards a goal, with input, process, output and feedback.',
          [('Parts of a system', SYSTEM + '<p>Plus <b>feedback</b> (output used to adjust input), a <b>boundary</b> and an <b>environment</b>.</p>'),
           ('Types', table(['Type', 'Meaning', 'Example'], [['Open', 'interacts with its environment', 'a business'], ['Closed', 'no interaction with environment', 'a sealed experiment'], ['Natural', 'not man-made', 'the digestive system'], ['Man-made', 'designed by people', 'payroll system'], ['Manual / automated', 'by hand / by computer', 'paper register / e-register'], ['Deterministic / probabilistic', 'predictable / uncertain output', 'calculator / weather']]))],
          [match('Match the system type.', [('A calculator', 'Deterministic'), ('Weather forecasting', 'Probabilistic'), ('A school', 'Open system'), ('The human body', 'Natural system')]),
           mcq('Thermostat turning heating off when warm enough is an example of…', ['feedback', 'boundary', 'input only'], 'feedback'),
           tf('An open system interacts with its environment.', True)]),

    44: L('A data flow diagram (DFD) shows how data moves between entities, processes and data stores.',
          [('Symbols', DFD + '<ol><li><b>External entity</b> (rectangle): source/destination of data</li><li><b>Process</b> (rounded box): transforms data</li><li><b>Data store</b> (open box): where data is kept</li></ol><p>Arrows are <b>data flows</b>, labelled with the data.</p>'),
           ('Rules', '<ul><li>Every process has at least one input and one output</li><li>Data can\'t flow directly between two entities or two stores</li><li>Level 0 (context diagram) → level 1 → level 2 for more detail</li></ul>')],
          [label('Name the DFD symbols.', DFD, ['External entity', 'Process', 'Data store']),
           mcq('Data cannot flow directly between…', ['two data stores', 'a process and a store', 'an entity and a process'], 'two data stores'),
           mcq('The top-level DFD showing the whole system as one process is the…', ['context diagram (level 0)', 'level 2 diagram', 'flowchart'], 'context diagram (level 0)'),
           tf('Every process must have both an input and an output.', True)]),

    45: L('An information system collects, processes, stores and distributes information to support decisions.',
          [('Components', '<div class="chips"><span>Hardware</span><span>Software</span><span>Data</span><span>People</span><span>Procedures</span><span>Networks</span></div>'),
           ('Data → information → knowledge', '<p><b>Data</b>: raw facts (12, 15). <b>Information</b>: processed, meaningful ("Average mark 13.5"). <b>Knowledge</b>: understanding used to decide.</p>'),
           ('Good information is…', '<p>accurate, relevant, complete, timely, concise, from a reliable source.</p>')],
          [sort('Data or information?', ['Data', 'Information'], [('45, 50, 38', 'Data'), ('"Sales rose 10% this month"', 'Information'), ('Raw sensor readings', 'Data'), ('"Class average is 12/20"', 'Information')]),
           mcq('Which is NOT a component of an information system?', ['Weather', 'People', 'Procedures'], 'Weather'),
           match('Match the quality of information.', [('Arrives in time to decide', 'Timely'), ('Free of errors', 'Accurate'), ('Related to the decision', 'Relevant'), ('Nothing important missing', 'Complete')])]),

    46: L('Organisations use different information systems at each level of management.',
          [('Types', table(['System', 'Users', 'Example'], [['TPS (transaction processing)', 'operational staff', 'sales, payroll, mobile money transactions'], ['MIS (management information)', 'middle managers', 'monthly sales reports'], ['DSS (decision support)', 'senior managers', 'what-if analysis for a new branch'], ['EIS / ESS (executive)', 'top executives', 'dashboards of key figures'], ['Expert system', 'specialists', 'medical diagnosis'], ['ERP', 'whole organisation', 'integrated finance, HR, stock']])),
           ('Pyramid', '<p>TPS at the bottom (many daily transactions) → MIS → DSS → EIS at the top (strategic decisions).</p>')],
          [match('Match the system.', [('Recording each sale at the till', 'TPS'), ('Monthly performance report for a manager', 'MIS'), ('Modelling "what if we raise prices?"', 'DSS'), ('Dashboard for the director', 'EIS')]),
           order('From operational to strategic.', ['TPS', 'MIS', 'DSS', 'EIS']),
           tf('An ERP integrates data from different departments in one system.', True)]),

    47: L('Data processing turns data into information. Commercial data processing handles large volumes of business transactions.',
          [('Data processing cycle', flow(['Collect', 'Prepare / validate', 'Input', 'Process', 'Output', 'Store'])),
           ('Processing modes', table(['Mode', 'Meaning', 'Example'], [['Batch', 'grouped, processed later', 'payroll, utility bills'], ['Online / real-time', 'processed immediately', 'ATM, flight booking'], ['Interactive', 'user dialogues with system', 'web forms'], ['Distributed', 'over several sites', 'bank branches']])),
           ('Validation vs verification', '<p><b>Validation</b>: is the data sensible? (range check, type check, presence check, check digit). <b>Verification</b>: was it copied correctly? (double entry, proofreading).</p>')],
          [sort('Batch or real-time?', ['Batch', 'Real-time'], [('Monthly electricity bills', 'Batch'), ('Airline seat booking', 'Real-time'), ('End-of-month payroll', 'Batch'), ('ATM withdrawal', 'Real-time')]),
           match('Match the check.', [('Age must be between 10 and 25', 'Range check'), ('Name field cannot be empty', 'Presence check'), ('Typing the password twice', 'Verification (double entry)'), ('Must be a number', 'Type check')]),
           order('Order the data processing cycle.', ['Collect', 'Prepare / validate', 'Input', 'Process', 'Output', 'Store'])]),
}
