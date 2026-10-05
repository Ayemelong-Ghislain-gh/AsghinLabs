(function () {
  const $ = (id) => document.getElementById(id);
  const OPS = {
    AND: (a, b) => a & b, OR: (a, b) => a | b, NAND: (a, b) => 1 - (a & b), NOR: (a, b) => 1 - (a | b), XOR: (a, b) => a ^ b, NOT: (a) => 1 - a,
  };
  const RULE = {
    AND: 'Output is 1 only when <b>both</b> inputs are 1.', OR: 'Output is 1 when <b>at least one</b> input is 1.',
    NOT: 'Output is the <b>opposite</b> of the input.', NAND: 'NOT AND: the <b>opposite</b> of AND.',
    NOR: 'NOT OR: the <b>opposite</b> of OR.', XOR: 'Output is 1 when the inputs are <b>different</b>.',
  };

  // Simple gate symbols (inputs on the left, output on the right)
  function symbol(g) {
    const bubble = (x) => `<circle cx="${x}" cy="40" r="6" class="g-sym"/>`;
    const inLines = g === 'NOT' ? '<line x1="0" y1="40" x2="40" y2="40" class="g-wire"/>' :
      '<line x1="0" y1="25" x2="45" y2="25" class="g-wire"/><line x1="0" y1="55" x2="45" y2="55" class="g-wire"/>';
    let body = '', outX = 110;
    if (g === 'AND' || g === 'NAND') body = '<path d="M40 10 H75 A30 30 0 0 1 75 70 H40 Z" class="g-sym"/>';
    if (g === 'OR' || g === 'NOR' || g === 'XOR') body = '<path d="M38 10 Q58 40 38 70 Q85 70 108 40 Q85 10 38 10 Z" class="g-sym"/>' + (g === 'XOR' ? '<path d="M28 10 Q48 40 28 70" class="g-sym" fill="none"/>' : '');
    if (g === 'NOT') { body = '<path d="M40 12 L95 40 L40 68 Z" class="g-sym"/>'; outX = 95; }
    const neg = g === 'NAND' || g === 'NOR' || g === 'NOT';
    if (g === 'AND' || g === 'NAND') outX = 105;
    const end = neg ? outX + 12 : outX;
    return `<svg class="gate-svg" viewBox="0 0 160 80" aria-label="${g} gate">${inLines}${body}${neg ? bubble(outX + 6) : ''}<line x1="${end}" y1="40" x2="160" y2="40" class="g-wire"/></svg>`;
  }

  runWalkthrough($('walk'), [
    {
      title: '1 and 0',
      html: `<p>In a circuit, every wire is either <b>1</b> (ON, true) or <b>0</b> (OFF, false).</p>
             <p>A logic gate takes inputs (A, B) and gives one output (Q).</p>
             <p class="wt-key">A truth table lists the output for every possible input.</p>`,
    },
    {
      title: 'AND, OR, NOT',
      html: `<ul><li><b>AND</b>: 1 only if A <b>and</b> B are 1</li><li><b>OR</b>: 1 if A <b>or</b> B (or both) is 1</li><li><b>NOT</b>: flips the input (1 → 0, 0 → 1)</li></ul>
             <p class="wt-key">Try them in the explorer above.</p>`,
    },
    {
      title: 'NAND, NOR, XOR',
      html: `<ul><li><b>NAND</b> = NOT AND: the AND answer, flipped</li><li><b>NOR</b> = NOT OR: the OR answer, flipped</li><li><b>XOR</b>: 1 when A and B are <b>different</b></li></ul>
             <p class="wt-key">The small circle on a symbol means "NOT".</p>`,
    },
    {
      title: 'Circuits: one column at a time',
      html: `<p>Q = (A AND B) OR C</p>
             <p>1. Make a column for <b>A AND B</b></p><p>2. Then OR that column with C to get Q</p>
             <p class="wt-key">With 3 inputs there are 8 rows: 000, 001, 010 … 111.</p>`,
    },
  ]);

  // ---------- Explorer ----------
  let gate = 'AND', A = 0, B = 0;
  function drawExplorer() {
    const one = gate === 'NOT';
    const q = one ? OPS.NOT(A) : OPS[gate](A, B);
    $('gSymbol').innerHTML = symbol(gate);
    $('gRule').innerHTML = RULE[gate];
    $('swA').textContent = 'A = ' + A; $('swA').classList.toggle('on', !!A);
    $('swB').textContent = 'B = ' + B; $('swB').classList.toggle('on', !!B); $('swB').hidden = one;
    $('lamp').textContent = 'Q = ' + q; $('lamp').classList.toggle('on', !!q);
    const rows = one ? [[0], [1]] : [[0, 0], [0, 1], [1, 0], [1, 1]];
    $('gTable').innerHTML = `<tr><th>A</th>${one ? '' : '<th>B</th>'}<th>Q</th></tr>` + rows.map(r => {
      const out = one ? OPS.NOT(r[0]) : OPS[gate](r[0], r[1]);
      const cur = r[0] === A && (one || r[1] === B);
      return `<tr class="${cur ? 'cur' : ''}"><td>${r[0]}</td>${one ? '' : `<td>${r[1]}</td>`}<td><b>${out}</b></td></tr>`;
    }).join('');
  }
  $('gateSel').addEventListener('change', (e) => { gate = e.target.value; drawExplorer(); trackLesson('logic-gates', 'interact'); });
  $('swA').addEventListener('click', () => { A = 1 - A; drawExplorer(); });
  $('swB').addEventListener('click', () => { B = 1 - B; drawExplorer(); });
  drawExplorer();

  // ---------- Practice ----------
  const vtable = (head, rows, inputCol) => '<div class="vt-wrap"><table class="vt tt"><tr>' + head.map(h => `<th>${h}</th>`).join('') + '</tr>' +
    rows.map((r, i) => '<tr>' + r.map(v => `<td>${v}</td>`).join('') + (inputCol ? `<td>{${i}}</td>` : '') + '</tr>').join('') + '</table></div>';

  function gateQ() {
    const g = pick(['AND', 'OR', 'NAND', 'NOR', 'XOR', 'NOT']);
    const one = g === 'NOT';
    const rows = one ? [[0], [1]] : [[0, 0], [0, 1], [1, 0], [1, 1]];
    const out = rows.map(r => (one ? OPS.NOT(r[0]) : OPS[g](r[0], r[1])));
    return {
      q: `Complete the truth table for a <b>${g}</b> gate.${symbol(g)}`,
      steps: [
        { html: 'Q for each row:' + vtable(one ? ['A', 'Q'] : ['A', 'B', 'Q'], rows, true),
          fields: out.map(o => ({ answer: o, kind: 'int', size: 1, label: 'Q' })),
          hint: RULE[g].replace(/<\/?b>/g, ''),
          why: `${RULE[g]} So Q = ${out.join(', ')} going down.` },
      ],
    };
  }

  function circuitQ() {
    const op1 = pick(['AND', 'OR', 'NAND', 'NOR', 'XOR']), op2 = pick(['AND', 'OR']);
    const notC = Math.random() < 0.6;
    const rows = []; for (let n = 0; n < 8; n++) rows.push([(n >> 2) & 1, (n >> 1) & 1, n & 1]);
    const X = rows.map(([a, b]) => OPS[op1](a, b));
    const Y = rows.map(([, , c]) => (notC ? 1 - c : c));
    const Q = rows.map((r, i) => OPS[op2](X[i], Y[i]));
    const xName = `A ${op1} B`, yName = notC ? 'NOT C' : 'C';
    const steps = [
      { html: `Step by step. First the column <b>${xName}</b> (look only at A and B):` + vtable(['A', 'B', 'C', xName], rows, true),
        fields: X.map(v => ({ answer: v, kind: 'int', size: 1 })),
        hint: RULE[op1].replace(/<\/?b>/g, '') + ' Ignore C for now.',
        why: `${xName} = ${X.join(', ')}` },
    ];
    if (notC) steps.push({
      html: 'Now the column <b>NOT C</b> (flip C):' + vtable(['A', 'B', 'C', xName, 'NOT C'], rows.map((r, i) => [...r, X[i]]), true),
      fields: Y.map(v => ({ answer: v, kind: 'int', size: 1 })),
      hint: 'NOT turns 1 into 0 and 0 into 1.', why: `NOT C = ${Y.join(', ')}` });
    steps.push({
      html: `Finally Q = (${xName}) <b>${op2}</b> ${yName}:` + vtable(['A', 'B', 'C', xName, yName, 'Q'], rows.map((r, i) => [...r, X[i], Y[i]]), true),
      fields: Q.map(v => ({ answer: v, kind: 'int', size: 1 })),
      hint: `${RULE[op2].replace(/<\/?b>/g, '')} Use the two columns just before Q.`,
      why: `Q = ${Q.join(', ')}` });
    return { q: `Complete the truth table for <span class="g-code">Q = (A ${op1} B) ${op2} ${yName}</span>`, steps };
  }

  const next = practice({ slug: 'logic-gates', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'),
    build: () => ($('pType').value === 'gate' ? gateQ() : circuitQ()) });
  $('pNew').addEventListener('click', next);
  $('pType').addEventListener('change', next);
})();
