"""Upper Sixth ICT: AI and computer networks (lessons 1-33)."""
from helpers import *
from f3_maths_part1 import table
from u6_cs_part1 import LESSONS as U6CS
from l6_ict_part1 import LESSONS as L6ICT
from u6_cs_part5 import OSI


def topo(kind):
    import math
    pts = [(210 + 120 * math.cos(math.radians(a)), 100 + 75 * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
    g = ''
    if kind == 'star':
        g += ''.join(f'<line x1="210" y1="100" x2="{x}" y2="{y}" class="v-line" style="stroke-width:2"/>' for x, y in pts)
        g += '<rect x="185" y="85" width="50" height="30" rx="6" class="v-box2"/><text x="210" y="105" text-anchor="middle" class="v-s">switch</text>'
    elif kind == 'ring':
        g += f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" class="v-line" style="fill:none;stroke-width:2"/>'
    elif kind == 'mesh':
        g += ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" class="v-line"/>' for i, a in enumerate(pts) for b in pts[i + 1:])
    elif kind == 'bus':
        pts = [(60 + i * 60, 60 if i % 2 else 140) for i in range(6)]
        g += '<line x1="30" y1="100" x2="390" y2="100" class="v-line" style="stroke-width:4"/>'
        g += ''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="100" class="v-line" style="stroke-width:2"/>' for x, y in pts)
    g += ''.join(f'<rect x="{x - 16}" y="{y - 11}" width="32" height="22" rx="4" class="v-box"/>' for x, y in pts)
    return svg(420, 200, g, kind + ' topology')


LESSONS = {
    1: U6CS[1],
    2: L6ICT[3],
    3: U6CS[2],
    4: U6CS[3],
    5: U6CS[4],

    7: L('A computer network is two or more devices linked to share resources and communicate.',
         [('Why network?', '<ul><li>Share files, printers and the internet connection</li><li>Communicate: email, chat, video</li><li>Centralised data and backups</li><li>Run shared applications</li></ul>'),
          ('Components', table(['Component', 'Role'], [['Nodes', 'computers, phones, printers'], ['NIC', 'connects a device to the network (has a MAC address)'], ['Transmission media', 'cables or wireless'], ['Connecting devices', 'switch, router, access point'], ['Protocols', 'rules for communication (TCP/IP)'], ['Network OS / services', 'manage users, files, security']])),
          ('Pros and cons', '<div class="two-col"><div><b>➕</b>sharing, communication, central management, cost saving</div><div><b>➖</b>set-up cost, security risks, viruses spread, dependence on the server</div></div>')],
         [match('Match the component.', [('NIC', 'Connects a device to the network'), ('Protocol', 'Rules for communication'), ('Switch', 'Connects devices in a LAN'), ('Node', 'Any device on the network')]),
          sort('Advantage or disadvantage of networking?', ['Advantage', 'Disadvantage'], [('One printer for 30 computers', 'Advantage'), ('Malware can spread to all PCs', 'Disadvantage'), ('Central backup of files', 'Advantage'), ('Server failure stops everyone', 'Disadvantage')]),
          tf('Every network card has a unique MAC address.', True)]),

    8: L('Running a network brings challenges: performance, security, scalability, cost and troubleshooting.',
         [('Performance measures', table(['Measure', 'Meaning'], [['Bandwidth', 'maximum data rate (Mbps)'], ['Throughput', 'actual data rate achieved'], ['Latency', 'delay (ms) for data to arrive'], ['Jitter', 'variation in latency (bad for calls)'], ['Packet loss', '% of packets that never arrive']])),
          ('Challenges', '<ul><li>Congestion when many users share bandwidth</li><li>Security threats and patching</li><li>Scalability as users grow</li><li>Single points of failure</li><li>Power cuts, cost of maintenance, skilled staff</li></ul>'),
          ('Transfer time', '<p class="wt-key">time = size (bits) ÷ rate (bits/s)</p><p>100 MB at 20 Mbps: 100 × 8 = 800 Mb → 800 ÷ 20 = <b>40 s</b></p>')],
         [fill('A 50 MB file on a 10 Mbps link.', 'Time = {0} s', [['40']], '50 × 8 = 400 Mb; 400 ÷ 10'),
          fill('A 2 GB backup over 100 Mbps (1 GB = 1000 MB).', 'Time = {0} s', [['160']], '2000 × 8 = 16 000 Mb ÷ 100'),
          match('Match the measure.', [('Video call breaks up because delay keeps changing', 'Jitter'), ('Maximum speed of the line', 'Bandwidth'), ('Delay before a reply arrives', 'Latency'), ('Speed actually achieved', 'Throughput')]),
          mcq('One switch connects every office. If it fails, all offices stop. This is a…', ['single point of failure', 'redundancy', 'VPN'], 'single point of failure')]),

    10: L('Networks are classified by the area they cover: PAN, LAN, CAN, MAN and WAN.',
          [('Types', table(['Type', 'Coverage', 'Example'], [['PAN', 'a few metres', 'phone ↔ Bluetooth earbuds'], ['LAN', 'a building', 'school computer lab'], ['WLAN', 'a building, wireless', 'Wi-Fi in a hotel'], ['CAN', 'a campus', 'University of Buea network'], ['MAN', 'a city', 'city-wide fibre network'], ['WAN', 'countries / world', 'the internet, a bank\'s national network']])),
           ('Other types', '<p><b>SAN</b> (storage area network) for data centres; <b>VPN</b> over the internet.</p>')],
          [order('From smallest to largest coverage.', ['PAN', 'LAN', 'CAN', 'MAN', 'WAN']),
           match('Match the example.', [('Smartwatch linked to a phone', 'PAN'), ('Computers in one office', 'LAN'), ('Bank branches across Cameroon', 'WAN'), ('All buildings of one university', 'CAN')]),
           tf('The internet is the largest WAN.', True)]),

    11: L('Choose a network by the organisation\'s size, distance, budget, security and growth.',
          [('Factors', '<div class="chips"><span>Number of users</span><span>Distance</span><span>Budget</span><span>Security needs</span><span>Speed</span><span>Scalability</span><span>Mobility</span><span>Available skills</span></div>'),
           ('Scenarios', table(['Organisation', 'Suggested network'], [['Small shop, 4 PCs', 'peer-to-peer LAN / small WLAN'], ['Secondary school', 'client–server LAN + Wi-Fi'], ['Hospital with 3 buildings', 'CAN with fibre backbone'], ['Bank with branches in 10 towns', 'WAN / VPN with leased lines']]))],
          [match('Best choice.', [('Café offering internet to customers', 'WLAN (Wi-Fi hotspot)'), ('Company with offices in Douala and Yaoundé', 'WAN / VPN'), ('One small office, 3 computers', 'Peer-to-peer LAN'), ('University with many buildings', 'CAN')]),
           mcq('Which factor matters most for a bank network?', ['Security', 'Colour of cables', 'Number of printers'], 'Security'),
           tf('Scalability means the network can grow easily.', True)]),

    13: L('Network architecture: peer-to-peer (all equal) or client–server (a central server provides services).',
          [('Comparison', table(['', 'Peer-to-peer', 'Client–server'], [['Control', 'each PC manages itself', 'central server'], ['Cost', 'cheap', 'server + NOS cost more'], ['Security', 'weak', 'strong, central accounts'], ['Backup', 'each PC', 'central'], ['Size', 'small (≤ 10)', 'any size'], ['Failure', 'one PC down doesn\'t stop others', 'server failure affects all']])),
           ('Servers', '<p>File, print, web, email, database, DHCP, DNS, authentication (domain controller).</p>')],
          [sort('Peer-to-peer or client–server feature?', ['Peer-to-peer', 'Client–server'], [('Central user accounts', 'Client–server'), ('Cheap and simple for 4 PCs', 'Peer-to-peer'), ('Central backups', 'Client–server'), ('No dedicated server', 'Peer-to-peer')]),
           mcq('A school wants all students to log in with central accounts. Use…', ['client–server', 'peer-to-peer', 'no network'], 'client–server'),
           match('Match the server.', [('Gives IP addresses automatically', 'DHCP server'), ('Translates names to IP addresses', 'DNS server'), ('Stores shared files', 'File server'), ('Hosts websites', 'Web server')])]),

    14: L('The physical topology is how devices are cabled together: bus, star, ring, mesh, tree or hybrid.',
          [('Star', topo('star') + '<p>All nodes connect to a central switch. Most common in LANs.</p>'),
           ('Bus and ring', topo('bus') + topo('ring') + '<p>Bus: one backbone cable with terminators. Ring: each node connects to two neighbours; data travels around.</p>'),
           ('Mesh', topo('mesh') + '<p>Full mesh links every pair: <b>n(n − 1)/2</b> links. 6 nodes → 15 links. Very reliable, expensive.</p>')],
          [fill('Full mesh with 5 nodes needs how many links?', '{0}', [['10']]),
           fill('Full mesh with 8 nodes?', '{0}', [['28']]),
           mcq('Which topology is shown?', ['Star', 'Bus', 'Ring'], 'Star', visual=topo('star')),
           match('Match the topology.', [('Central switch', 'Star'), ('Single backbone cable', 'Bus'), ('Each node linked to two neighbours in a loop', 'Ring'), ('Many redundant paths', 'Mesh')])]),

    15: L('Compare topologies on cost, reliability, performance and ease of expansion to choose the right one.',
          [('Comparison', table(['Topology', 'Advantages', 'Disadvantages'], [['Bus', 'cheap, little cable', 'backbone failure stops all; collisions'], ['Star', 'easy to add nodes, one cable fault affects one PC', 'switch is a single point of failure, more cable'], ['Ring', 'orderly, no collisions', 'one break can stop the ring'], ['Mesh', 'very reliable, redundant paths', 'expensive, complex'], ['Tree / hybrid', 'scalable, hierarchical', 'depends on backbone']]))],
          [match('Best topology.', [('Very high reliability between data centres', 'Mesh'), ('School lab, easy to add PCs', 'Star'), ('Cheapest temporary set-up with one cable', 'Bus'), ('Several star networks joined by a backbone', 'Tree / hybrid')]),
           mcq('In a star network, one cable breaks. What happens?', ['Only that one PC loses connection', 'The whole network stops', 'Nothing at all'], 'Only that one PC loses connection'),
           tf('A bus topology is easy to troubleshoot.', False)]),

    17: L('Network equipment connects, forwards, extends and protects network traffic.',
          [('Devices', table(['Device', 'Layer', 'Role'], [['NIC', '2', 'connects a device'], ['Hub', '1', 'repeats data to all ports (old)'], ['Switch', '2', 'sends frames only to the right port (MAC table)'], ['Router', '3', 'forwards packets between networks (IP)'], ['Modem', '1', 'modulates/demodulates signals (DSL, 4G)'], ['Access point', '2', 'connects wireless devices to the LAN'], ['Repeater', '1', 'boosts signals over distance'], ['Firewall', '3–7', 'filters traffic'], ['Gateway', '7', 'links different protocols']]))],
          [match('Match the device.', [('Connects the school LAN to the internet', 'Router'), ('Sends data only to the destination port', 'Switch'), ('Lets laptops join the LAN by Wi-Fi', 'Access point'), ('Boosts a weak signal', 'Repeater')]),
           mcq('Why is a switch better than a hub?', ['It sends frames only to the correct port', 'It is wireless', 'It routes between networks'], 'It sends frames only to the correct port'),
           mcq('A switch uses which address to forward?', ['MAC address', 'IP address', 'Email address'], 'MAC address')]),

    18: L('Setting up a LAN: plan, cable or configure Wi-Fi, assign IP addresses, test and share resources.',
          [('Steps', '<ol><li>Plan: users, topology, location of equipment</li><li>Install switch/router and run cables (UTP Cat 6, RJ-45)</li><li>Connect PCs and configure IP (DHCP or static)</li><li>Set up Wi-Fi with WPA2/WPA3 and a strong passphrase</li><li>Test with <code>ping</code> and <code>ipconfig</code></li><li>Share folders and printers; document the network</li></ol>'),
           ('Cables', '<p><b>Straight-through</b>: PC ↔ switch. <b>Crossover</b>: PC ↔ PC (older devices). Wiring standard T568B.</p>'),
           ('IP settings', table(['Setting', 'Example'], [['IP address', '192.168.1.20'], ['Subnet mask', '255.255.255.0'], ['Default gateway', '192.168.1.1 (router)'], ['DNS', '8.8.8.8']]))],
          [order('Order the set-up steps.', ['Plan the network', 'Install the switch and cables', 'Configure IP addresses', 'Secure the Wi-Fi', 'Test with ping', 'Share resources']),
           mcq('Which command checks if another computer can be reached?', ['ping', 'dir', 'format'], 'ping'),
           mcq('The default gateway is usually the address of the…', ['router', 'printer', 'DNS server only'], 'router'),
           mcq('Which Wi-Fi security is best?', ['WPA3', 'WEP', 'No password'], 'WPA3')]),

    19: L('Select equipment by the organisation\'s needs: number of users, speed, coverage, security, budget and growth.',
          [('Questions to ask', '<ul><li>How many ports/users now and in 3 years?</li><li>Wired, wireless or both? Area to cover?</li><li>Speed needed (100 Mbps, 1 Gbps)?</li><li>Managed or unmanaged switch? PoE for cameras/APs?</li><li>Security: firewall, VLANs</li><li>Power: UPS for cuts</li></ul>'),
           ('Example', '<p>School with 40 lab PCs + staff Wi-Fi: 48-port gigabit switch, router with firewall, 3 access points, Cat 6 cabling, UPS.</p>')],
          [fill('A lab has 30 PCs, a printer and a link to the router. Minimum switch ports needed =', '{0}', [['32']]),
           match('Match the need to the equipment.', [('Power IP cameras through the network cable', 'PoE switch'), ('Keep the network running during power cuts', 'UPS'), ('Block attacks from the internet', 'Firewall'), ('Cover a large hall with Wi-Fi', 'Several access points')]),
           tf('Buying a switch with spare ports allows for growth.', True)]),

    21: L('The internet is public, an intranet is private to an organisation, and an extranet opens part of it to partners.',
          [('Comparison', table(['', 'Users', 'Example'], [['Internet', 'everyone', 'public websites'], ['Intranet', 'employees only', 'staff portal, internal HR documents'], ['Extranet', 'employees + authorised outsiders', 'supplier ordering portal, parent portal']])),
           ('Benefits', '<p>Intranet: share documents, announcements, forms internally. Extranet: work with suppliers/customers securely (login, VPN).</p>')],
          [match('Intranet, extranet or internet?', [('Staff-only school portal', 'Intranet'), ('Parents log in to see their child\'s results', 'Extranet'), ('Public school website', 'Internet')]),
           mcq('Access to an extranet is controlled by…', ['logins and permissions', 'nothing', 'the colour of the site'], 'logins and permissions'),
           tf('An intranet uses the same technologies as the internet (web, TCP/IP).', True)]),

    22: L('A VPN creates an encrypted tunnel over the internet so remote users can connect securely and privately.',
          [('How it works', flow([('Laptop', 'VPN client'), ('Encrypted tunnel', 'over internet'), ('VPN server', 'company'), ('Private network', 'files, apps')])),
           ('Uses', '<ul><li>Staff working from home access company systems</li><li>Linking branch offices (site-to-site VPN)</li><li>Privacy on public Wi-Fi</li></ul>'),
           ('Limits', '<p>Slows the connection a little, needs trust in the VPN provider, does not stop malware or phishing.</p>')],
          [mcq('Main purpose of a VPN?', ['Secure, encrypted connection over a public network', 'Faster downloads', 'Free internet'], 'Secure, encrypted connection over a public network'),
           order('Order the path of VPN data.', ['Laptop VPN client', 'Encrypted tunnel over the internet', 'Company VPN server', 'Private network']),
           tf('A VPN protects you from clicking a phishing link.', False)]),

    23: L('Network security protects confidentiality, integrity and availability (CIA) against threats.',
          [('CIA triad', table(['Goal', 'Meaning', 'Example control'], [['Confidentiality', 'only authorised people read data', 'encryption, access control'], ['Integrity', 'data is not altered', 'hashing, checksums, permissions'], ['Availability', 'systems work when needed', 'backups, UPS, DoS protection']])),
           ('Threats', '<div class="chips"><span>Malware</span><span>Phishing</span><span>Man-in-the-middle</span><span>Denial of service</span><span>Password attacks</span><span>Insider threats</span><span>Unpatched software</span></div>'),
           ('Controls', '<p>Firewalls, IDS/IPS, antivirus, encryption (HTTPS, WPA3), 2FA, updates, user training, security policy.</p>')],
          [match('Which CIA goal?', [('Hacker changes exam marks', 'Integrity'), ('Website down after a flood of traffic', 'Availability'), ('Salaries read by an unauthorised clerk', 'Confidentiality')]),
           match('Match the threat.', [('Attacker intercepts traffic on public Wi-Fi', 'Man-in-the-middle'), ('Server flooded with requests', 'Denial of service'), ('Fake email asking for a password', 'Phishing')]),
           mcq('An IDS…', ['detects suspicious network activity', 'speeds up the network', 'assigns IP addresses'], 'detects suspicious network activity')]),

    24: L('Data protection and access control ensure only the right people access the right data.',
          [('AAA', table(['Step', 'Question'], [['Authentication', 'Who are you? (password, biometrics, 2FA)'], ['Authorisation', 'What may you do? (permissions)'], ['Accounting / auditing', 'What did you do? (logs)']])),
           ('Access control models', '<ul><li><b>Least privilege</b>: only what the job needs</li><li><b>RBAC</b>: permissions by role (teacher, bursar)</li><li><b>ACLs</b>: lists of who can read/write each resource</li></ul>'),
           ('Protecting data', '<p>Encryption at rest and in transit, backups, data minimisation, consent, compliance with data protection law.</p>')],
          [order('Order AAA.', ['Authentication', 'Authorisation', 'Accounting']),
           match('Match the concept.', [('Teachers can enter marks; students can only view', 'Role-based access control'), ('Give users only the access they need', 'Least privilege'), ('Log of who opened each file', 'Auditing')]),
           tf('Encrypting data in transit protects it while it travels over the network.', True)]),

    25: L('Validation checks data is sensible; verification checks it was entered or transmitted correctly.',
          [('Validation', table(['Check', 'Example'], [['Presence', 'required field'], ['Type', 'number only'], ['Range', '0 ≤ mark ≤ 20'], ['Length', 'PIN has 4 digits'], ['Format', 'email has @'], ['Lookup', 'region from a list'], ['Check digit', 'last digit of a barcode']])),
           ('Verification', '<p>Double entry, proofreading/visual check, and in transmission: parity bits, checksums, CRC, echo checks.</p>')],
          [match('Match the check.', [('Email must contain @', 'Format check'), ('Age between 15 and 25', 'Range check'), ('Type the email twice', 'Double entry verification'), ('Last digit of an ISBN computed from the others', 'Check digit')]),
           tf('A value can pass validation but still be wrong.', True, 'e.g. age 17 typed instead of 18.'),
           mcq('Which is verification?', ['Proofreading data against the source document', 'A range check', 'A type check'], 'Proofreading data against the source document')]),

    27: L('Transmission mode is the direction of data flow: simplex, half-duplex or full-duplex.',
          [('Directions', table(['Mode', 'Direction', 'Example'], [['Simplex', 'one way only', 'TV/radio broadcast, keyboard → PC'], ['Half-duplex', 'both ways, one at a time', 'walkie-talkie'], ['Full-duplex', 'both ways at once', 'phone call, modern Ethernet']])),
           ('Serial vs parallel', '<p><b>Serial</b>: one bit after another on one wire (USB, long distances). <b>Parallel</b>: several bits at once on many wires (short distances; skew problems).</p>')],
          [match('Match the mode.', [('FM radio', 'Simplex'), ('Walkie-talkie', 'Half-duplex'), ('Phone conversation', 'Full-duplex')]),
           mcq('Why is serial used for long distances?', ['No skew between wires, fewer wires', 'It is always faster', 'It is wireless'], 'No skew between wires, fewer wires'),
           tf('In half-duplex, both sides can send at the same time.', False)]),

    28: L('Broadband carries many channels at high speed; narrowband carries a small amount of data on a narrow frequency range.',
          [('Comparison', table(['', 'Narrowband', 'Broadband'], [['Capacity', 'low (kbps)', 'high (Mbps–Gbps)'], ['Channels', 'one', 'many at once'], ['Examples', 'dial-up, SMS, IoT LPWAN', 'fibre, 4G/5G, cable, satellite internet']])),
           ('Baseband', '<p>Baseband uses the whole medium for one digital signal (Ethernet LANs).</p>')],
          [sort('Broadband or narrowband?', ['Broadband', 'Narrowband'], [('Fibre to the home', 'Broadband'), ('Old dial-up modem', 'Narrowband'), ('4G mobile internet', 'Broadband'), ('Smart meter sending tiny readings', 'Narrowband')]),
           mcq('Streaming HD video needs…', ['broadband', 'narrowband', 'simplex only'], 'broadband'),
           tf('Ethernet LANs use baseband transmission.', True)]),

    29: L('Data can be transmitted as analog or digital, serially or in parallel, synchronously or asynchronously, to one or many receivers.',
          [('Types', table(['Type', 'Meaning'], [['Analog', 'continuous signal (old telephone)'], ['Digital', 'discrete 0/1 signals'], ['Asynchronous', 'start and stop bits around each character'], ['Synchronous', 'blocks of data timed by a shared clock'], ['Unicast', 'one to one'], ['Multicast', 'one to a group'], ['Broadcast', 'one to all']])),
           ('Overhead', '<p>Asynchronous 8-bit character + 1 start + 1 stop = 10 bits → 20% overhead.</p>')],
          [match('Match the transmission.', [('Video conference to 20 chosen users', 'Multicast'), ('DHCP discover sent to everyone', 'Broadcast'), ('Web page to one user', 'Unicast')]),
           fill('Asynchronous: 1 start bit + 8 data bits + 1 stop bit. Bits per character =', '{0}', [['10']]),
           fill('How many characters per second at 9600 bps with that format?', '{0}', [['960']]),
           mcq('Synchronous transmission uses…', ['a shared clock for blocks of data', 'start/stop bits for each character', 'no timing at all'], 'a shared clock for blocks of data')]),

    30: L('Transmission media are guided (cables) or unguided (wireless).',
          [('Guided', table(['Medium', 'Notes'], [['Twisted pair (UTP/STP)', 'cheap, LANs, up to 100 m (Cat 6)'], ['Coaxial', 'TV, older networks, better shielding'], ['Fibre optic', 'light, very fast, long distances, immune to interference, expensive']])),
           ('Unguided', table(['Medium', 'Use'], [['Radio / Wi-Fi', 'LAN wireless'], ['Bluetooth', 'PAN'], ['Microwave', 'point-to-point links, line of sight'], ['Satellite', 'remote areas, TV, GPS'], ['Infrared', 'remote controls, short range']])),
           ('Choosing', '<p>Distance, speed, cost, interference, security, installation.</p>')],
          [sort('Guided or unguided?', ['Guided', 'Unguided'], [('Fibre optic', 'Guided'), ('Wi-Fi', 'Unguided'), ('Coaxial', 'Guided'), ('Satellite', 'Unguided'), ('UTP', 'Guided'), ('Bluetooth', 'Unguided')]),
           mcq('Which medium is immune to electromagnetic interference?', ['Fibre optic', 'UTP', 'Coaxial'], 'Fibre optic'),
           mcq('Best way to connect a remote village school with no cables nearby?', ['Satellite or microwave link', 'UTP', 'Infrared'], 'Satellite or microwave link'),
           fill('Maximum recommended length of a UTP Ethernet cable (metres)?', '{0}', [['100']])]),

    31: L('The CPU controls peripherals using drivers, ports, buffers, handshaking and polling, interrupts or DMA.',
          [('Mechanisms', table(['Mechanism', 'How'], [['Polling', 'CPU repeatedly checks device status'], ['Interrupts', 'device signals the CPU when ready'], ['DMA', 'device transfers data directly to memory'], ['Buffering', 'temporary storage to match speeds'], ['Handshaking', 'signals agree on readiness (ready/acknowledge)'], ['Device driver', 'software that controls the device']])),
           ('Ports', '<div class="chips"><span>USB</span><span>HDMI</span><span>Ethernet (RJ-45)</span><span>Thunderbolt</span><span>Bluetooth</span></div>')],
          [match('Match the mechanism.', [('Printer tells CPU "out of paper"', 'Interrupt'), ('CPU keeps checking the keyboard', 'Polling'), ('Disk copies a block straight to RAM', 'DMA'), ('Printer stores pages before printing', 'Buffering')]),
           mcq('Which wastes the most CPU time?', ['Polling', 'Interrupts', 'DMA'], 'Polling'),
           tf('Handshaking lets sender and receiver confirm they are ready.', True)]),

    32: L('Protocols are rules for communication. Each common protocol has a role and a port number.',
          [('Common protocols', table(['Protocol', 'Role', 'Port'], [['HTTP / HTTPS', 'web pages (HTTPS encrypted)', '80 / 443'], ['FTP', 'file transfer', '21'], ['SMTP', 'send email', '25 / 587'], ['POP3 / IMAP', 'receive email', '110 / 143'], ['DNS', 'name → IP address', '53'], ['DHCP', 'automatic IP addresses', '67/68'], ['SSH', 'secure remote login', '22'], ['TCP / UDP', 'transport: reliable / fast', '—'], ['IP', 'addressing and routing', '—']])),
           ('TCP vs UDP', '<div class="two-col"><div><b>TCP</b>connection, acknowledgements, ordered, reliable — web, email</div><div><b>UDP</b>no connection, fast, may lose packets — video calls, games, DNS</div></div>')],
          [match('Match the protocol.', [('Sending an email', 'SMTP'), ('Secure web page', 'HTTPS'), ('Translating www.minesec.gov.cm to an IP', 'DNS'), ('Giving a laptop an IP automatically', 'DHCP')]),
           fill('Default port of HTTPS?', '{0}', [['443']]),
           mcq('Live video calls usually use…', ['UDP', 'TCP only', 'FTP'], 'UDP'),
           mcq('Which protocol keeps emails on the server and syncs across devices?', ['IMAP', 'POP3', 'FTP'], 'IMAP')]),

    33: L('Protocol suites like TCP/IP are organised in layers; the OSI model is the 7-layer reference model.',
          [('OSI model', OSI),
           ('OSI vs TCP/IP', table(['TCP/IP layer', 'OSI layers'], [['Application', '7, 6, 5'], ['Transport', '4'], ['Internet', '3'], ['Network access', '2, 1']])),
           ('Encapsulation', '<p>Going down, each layer adds a header: data → <b>segment</b> (transport) → <b>packet</b> (network) → <b>frame</b> (data link) → <b>bits</b> (physical).</p>')],
          [order('Order the OSI layers from 1 to 7.', ['Physical', 'Data link', 'Network', 'Transport', 'Session', 'Presentation', 'Application']),
           match('Match the PDU to the layer.', [('Segment', 'Transport'), ('Packet', 'Network'), ('Frame', 'Data link'), ('Bits', 'Physical')]),
           fill('How many layers does the TCP/IP model have?', '{0}', [['4']]),
           mcq('Encryption and data formats belong to which OSI layer?', ['Presentation', 'Session', 'Physical'], 'Presentation')]),
}
