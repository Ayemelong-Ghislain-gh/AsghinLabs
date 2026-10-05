(function () {
  const $ = (id) => document.getElementById(id);
  const r1 = (n) => Math.round(n * 10) / 10;
  const r3 = (n) => Math.round(n * 1000) / 1000;
  const rad = (d) => d * Math.PI / 180, deg = (r) => r * 180 / Math.PI;
  const FN = { sin: Math.sin, cos: Math.cos, tan: Math.tan };

  // Right angle at B (bottom right). θ at A (bottom left). opp = BC, adj = AB, hyp = AC.
  function triangle(lab) {
    const A = [30, 170], B = [250, 170], C = [250, 40];
    const t = (p, s, cls) => `<text x="${p[0]}" y="${p[1]}" class="tri-lbl ${cls || ''}" text-anchor="middle">${s}</text>`;
    return `<svg class="tri-svg" viewBox="0 0 290 200" role="img" aria-label="Right-angled triangle">
      <polygon points="${A} ${B} ${C}" class="tri"/>
      <polyline points="234,170 234,154 250,154" class="tri-right"/>
      ${lab.angle ? '' : '<!--'}<path d="M 62 170 A 32 32 0 0 0 ${30 + 32 * Math.cos(Math.atan2(130, 220))} ${170 - 32 * Math.sin(Math.atan2(130, 220))}" class="tri-arc"/>${lab.angle ? '' : '-->'}
      ${t([78, 160], lab.angle, 'ang')}
      ${t([140, 192], lab.adj || '', lab.adjCls)}
      ${t([270, 110], lab.opp || '', lab.oppCls)}
      ${t([122, 92], lab.hyp || '', lab.hypCls)}
    </svg>`;
  }

  runWalkthrough($('walk'), [
    {
      title: 'Name the three sides',
      html: `${triangle({ angle: 'θ', opp: 'opp', adj: 'adj', hyp: 'hyp' })}
             <ul><li><b>Hypotenuse</b>: the longest side, opposite the right angle</li><li><b>Opposite</b>: across from the angle θ</li><li><b>Adjacent</b>: next to θ (not the hypotenuse)</li></ul>`,
    },
    {
      title: 'SOH CAH TOA',
      html: `<ul><li><b>S</b>in = <b>O</b>pposite ÷ <b>H</b>ypotenuse</li><li><b>C</b>os = <b>A</b>djacent ÷ <b>H</b>ypotenuse</li><li><b>T</b>an = <b>O</b>pposite ÷ <b>A</b>djacent</li></ul>
             <p class="wt-key">Pick the ratio that uses the side you know and the side you want.</p>`,
    },
    {
      title: 'Finding a side',
      html: `<p>θ = 30°, hypotenuse = 10, find the opposite side x.</p>
             <p>Opposite and hypotenuse → <b>sin</b></p>
             <p>sin 30° = x ÷ 10 → x = 10 × sin 30° = 10 × 0.5 = <b>5</b></p>`,
    },
    {
      title: 'Pythagoras and finding an angle',
      html: `<p><b>Pythagoras:</b> hyp² = a² + b². For sides 3 and 4: hyp = √(9 + 16) = √25 = <b>5</b></p>
             <p><b>An angle:</b> tan θ = 3 ÷ 4 = 0.75 → θ = tan⁻¹(0.75) = <b>36.9°</b></p>
             <p class="wt-key">Use the sin⁻¹, cos⁻¹, tan⁻¹ buttons (SHIFT) on your calculator.</p>`,
    },
  ]);

  const SIDES = ['opposite', 'adjacent', 'hypotenuse'];
  const RATIO = { sin: ['opposite', 'hypotenuse'], cos: ['adjacent', 'hypotenuse'], tan: ['opposite', 'adjacent'] };
  const short = { opposite: 'opp', adjacent: 'adj', hypotenuse: 'hyp' };

  function sideQ() {
    const fn = pick(['sin', 'cos', 'tan']);
    const [top, bottom] = RATIO[fn];
    const ang = pick([25, 30, 35, 40, 50, 55, 60, 65]);
    const knownIsTop = Math.random() < 0.4;          // usually we know the bottom side
    const known = knownIsTop ? top : bottom, want = knownIsTop ? bottom : top;
    const L = rint(5, 20);
    const ratio = FN[fn](rad(ang));
    const x = knownIsTop ? L / ratio : L * ratio;
    const lab = { angle: ang + '°' };
    lab[short[known]] = String(L); lab[short[want]] = 'x'; lab[short[want] + 'Cls'] = 'unk';
    const formula = knownIsTop ? `x = ${L} ÷ ${fn} ${ang}°` : `x = ${L} × ${fn} ${ang}°`;
    const wrongF = knownIsTop ? [`x = ${L} × ${fn} ${ang}°`, `x = ${fn} ${ang}° ÷ ${L}`] : [`x = ${L} ÷ ${fn} ${ang}°`, `x = ${fn} ${ang}° ÷ ${L}`];
    return {
      q: `Find the side <b>x</b> (to 1 decimal place).${triangle(lab)}`,
      steps: [
        { html: `Name the sides from the angle ${ang}°: the side ${L} is the {0}, and x is the {1}`,
          fields: [{ answer: known, kind: 'choice', options: SIDES, label: 'side ' + L }, { answer: want, kind: 'choice', options: SIDES, label: 'side x' }],
          hint: 'The hypotenuse is the longest side, opposite the right angle. The opposite side is across from the angle. The adjacent side touches the angle.',
          why: `${L} is the <b>${known}</b> and x is the <b>${want}</b>.` },
        { html: `${known} and ${want} → use {0}`,
          fields: [{ answer: fn, kind: 'choice', options: ['sin', 'cos', 'tan'], label: 'ratio' }],
          hint: 'SOH: sin uses opposite & hypotenuse. CAH: cos uses adjacent & hypotenuse. TOA: tan uses opposite & adjacent.',
          why: `${RATIO[fn][0]} and ${RATIO[fn][1]} → <b>${fn}</b>.` },
        { html: `Rearrange: {0}`,
          fields: [{ answer: formula, kind: 'choice', options: shuffle([formula, ...wrongF]), label: 'equation' }],
          hint: `Start from ${fn} ${ang}° = ${top === want ? 'x' : L} ÷ ${top === want ? L : 'x'}, then get x alone.`,
          why: `${fn} ${ang}° = ${knownIsTop ? L + ' ÷ x' : 'x ÷ ' + L} → <b>${formula}</b>` },
        { html: `Calculate (${fn} ${ang}° = ${r3(ratio)}): x = {0}`,
          fields: [{ answer: r1(x), kind: 'num', size: 5, label: 'x', tol: 0.15 }],
          hint: `Use your calculator: ${formula.replace('x = ', '')}. Round to 1 decimal place.`,
          why: `x = <b>${r1(x)}</b>` },
      ],
    };
  }

  function pythQ() {
    const findHyp = Math.random() < 0.6;
    let a = rint(3, 12), b = rint(3, 12);
    const h = Math.sqrt(a * a + b * b);
    const lab = { angle: '' };
    if (findHyp) { lab.opp = String(a); lab.adj = String(b); lab.hyp = 'x'; lab.hypCls = 'unk'; }
    else { if (a < b) [a, b] = [b, a]; lab.opp = 'x'; lab.oppCls = 'unk'; lab.adj = String(b); lab.hyp = String(r1(h)); }
    const hyp = findHyp ? null : r1(h);
    const x = findHyp ? h : Math.sqrt(hyp * hyp - b * b);
    return {
      q: `Find the side <b>x</b> using Pythagoras (to 1 decimal place).${triangle(lab)}`,
      steps: findHyp ? [
        { html: 'x is opposite the right angle, so x is the {0}',
          fields: [{ answer: 'hypotenuse', kind: 'choice', options: SIDES }],
          hint: 'The side across from the small square (right angle).', why: 'x is the <b>hypotenuse</b>.' },
        { html: `x² = ${a}² + ${b}² = {0} + {1} = {2}`,
          fields: [{ answer: a * a, kind: 'int', size: 3 }, { answer: b * b, kind: 'int', size: 3 }, { answer: a * a + b * b, kind: 'int', size: 4 }],
          hint: 'Square each side (multiply it by itself), then add.', why: `x² = <b>${a * a + b * b}</b>` },
        { html: `x = √${a * a + b * b} = {0}`,
          fields: [{ answer: r1(h), kind: 'num', size: 5, tol: 0.15 }],
          hint: 'Use the √ button. Round to 1 decimal place.', why: `x = <b>${r1(h)}</b>` },
      ] : [
        { html: `The hypotenuse is ${hyp}, so x is a shorter side. x² = hyp² {0} ${b}²`,
          fields: [{ answer: '−', kind: 'choice', options: ['+', '−'] }],
          hint: 'For a shorter side you subtract: shorter² = hyp² − other².', why: `x² = ${hyp}² <b>−</b> ${b}²` },
        { html: `x² = {0} − {1} = {2}`,
          fields: [{ answer: r1(hyp * hyp), kind: 'num', size: 6, tol: 0.15 }, { answer: b * b, kind: 'int', size: 3 }, { answer: r1(hyp * hyp - b * b), kind: 'num', size: 6, tol: 0.25 }],
          hint: `Square ${hyp} and ${b}, then subtract.`, why: `x² = <b>${r1(hyp * hyp - b * b)}</b>` },
        { html: `x = √${r1(hyp * hyp - b * b)} = {0}`,
          fields: [{ answer: r1(x), kind: 'num', size: 5, tol: 0.15 }],
          hint: 'Use the √ button. Round to 1 decimal place.', why: `x = <b>${r1(x)}</b>` },
      ],
    };
  }

  function angleQ() {
    const fn = pick(['sin', 'cos', 'tan']);
    const [top, bottom] = RATIO[fn];
    let p, q;
    do { p = rint(3, 15); q = rint(4, 20); } while (fn !== 'tan' && p >= q);
    const lab = { angle: 'θ' };
    lab[short[top]] = String(p); lab[short[bottom]] = String(q);
    const val = p / q, th = deg(fn === 'sin' ? Math.asin(val) : fn === 'cos' ? Math.acos(val) : Math.atan(val));
    return {
      q: `Find the angle <b>θ</b> (to 1 decimal place).${triangle(lab)}`,
      steps: [
        { html: `From θ: ${p} is the {0} and ${q} is the {1}`,
          fields: [{ answer: top, kind: 'choice', options: SIDES }, { answer: bottom, kind: 'choice', options: SIDES }],
          hint: 'Hypotenuse = longest side, opposite the right angle. Opposite = across from θ. Adjacent = touching θ.',
          why: `${p} is the <b>${top}</b>, ${q} is the <b>${bottom}</b>.` },
        { html: 'So use {0}',
          fields: [{ answer: fn, kind: 'choice', options: ['sin', 'cos', 'tan'] }],
          hint: 'SOH CAH TOA: which ratio uses these two sides?', why: `<b>${fn}</b> θ = ${p} ÷ ${q}` },
        { html: `${fn} θ = ${p} ÷ ${q} = {0} (3 decimal places)`,
          fields: [{ answer: r3(val), kind: 'num', size: 6, tol: 0.002 }],
          hint: 'Divide on your calculator.', why: `${fn} θ = <b>${r3(val)}</b>` },
        { html: `θ = ${fn}⁻¹(${r3(val)}) = {0}°`,
          fields: [{ answer: r1(th), kind: 'num', size: 5, tol: 0.15 }],
          hint: `Press SHIFT then ${fn} on your calculator.`, why: `θ = <b>${r1(th)}°</b>` },
      ],
    };
  }

  const next = practice({ slug: 'right-triangles', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'),
    build: () => ({ side: sideQ, pyth: pythQ, angle: angleQ, mix: pick([sideQ, pythQ, angleQ]) })[$('pType').value]() });
  $('pNew').addEventListener('click', next);
  $('pType').addEventListener('change', next);
})();
