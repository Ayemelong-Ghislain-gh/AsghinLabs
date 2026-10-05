(function () {
  const $ = (id) => document.getElementById(id);

  runWalkthrough($('walk'), [
    {
      title: 'What "change the subject" means',
      html: `<p>The subject is the letter on its own, on one side.</p>
             <p>In <b>v = u + at</b>, the subject is v. Making <b>t</b> the subject means writing <b>t = …</b></p>
             <p class="wt-key">Goal: get the new letter alone.</p>`,
    },
    {
      title: 'Undo with the opposite',
      html: `<ul><li>+ is undone by −, and − by +</li><li>× is undone by ÷, and ÷ by ×</li><li>² is undone by √</li></ul>
             <p class="wt-key">Whatever you do, do it to <b>both sides</b>.</p>`,
    },
    {
      title: 'One example',
      html: `<p>Make t the subject of v = u + at</p>
             <p>1. Subtract u from both sides: v − u = at</p>
             <p>2. Divide both sides by a: <b>t = (v − u) ÷ a</b></p>
             <p class="wt-key">Undo + and − first, then × and ÷.</p>`,
    },
    {
      title: 'Check with numbers',
      html: `<p>Pick numbers: u = 5, a = 3, t = 5 → v = 5 + 15 = 20</p>
             <p>Now use your answer: t = (20 − 5) ÷ 3 = <b>5</b> ✓</p>
             <p class="wt-key">Same number back → your formula is right.</p>`,
    },
  ]);

  // Each formula: steps of [operation, result], plus distractors and a number check
  const BANK = [
    { f: 'v = u + at', target: 't', ans: 't = (v − u) / a',
      steps: [['subtract u from both sides', 'v − u = at', ['add u to both sides', 'divide both sides by a'], ['v + u = at', 'v = at − u']],
              ['divide both sides by a', 't = (v − u) / a', ['multiply both sides by a', 'subtract a from both sides'], ['t = (v − u)a', 't = v − u − a']]],
      check: { given: 'v = 20, u = 5, a = 3', value: 5 } },
    { f: 'y = mx + c', target: 'x', ans: 'x = (y − c) / m',
      steps: [['subtract c from both sides', 'y − c = mx', ['add c to both sides', 'divide both sides by m'], ['y + c = mx', 'y = mx − c']],
              ['divide both sides by m', 'x = (y − c) / m', ['multiply both sides by m', 'subtract m from both sides'], ['x = m(y − c)', 'x = y − c − m']]],
      check: { given: 'y = 17, m = 3, c = 2', value: 5 } },
    { f: 'P = 2l + 2w', target: 'l', ans: 'l = (P − 2w) / 2',
      steps: [['subtract 2w from both sides', 'P − 2w = 2l', ['add 2w to both sides', 'divide both sides by w'], ['P + 2w = 2l', 'P = 2l − 2w']],
              ['divide both sides by 2', 'l = (P − 2w) / 2', ['multiply both sides by 2', 'subtract 2 from both sides'], ['l = 2(P − 2w)', 'l = P − 2w − 2']]],
      check: { given: 'P = 30, w = 4', value: 11 } },
    { f: 'V = IR', target: 'R', ans: 'R = V / I',
      steps: [['divide both sides by I', 'R = V / I', ['multiply both sides by I', 'subtract I from both sides'], ['R = VI', 'R = V − I']]],
      check: { given: 'V = 12, I = 3', value: 4 } },
    { f: 'C = 2πr', target: 'r', ans: 'r = C / (2π)',
      steps: [['divide both sides by 2π', 'r = C / (2π)', ['multiply both sides by 2π', 'subtract 2π from both sides'], ['r = 2πC', 'r = C − 2π']]],
      check: { given: 'C = 31.4 (use π = 3.14)', value: 5 } },
    { f: 'A = bh / 2', target: 'h', ans: 'h = 2A / b',
      steps: [['multiply both sides by 2', '2A = bh', ['divide both sides by 2', 'add 2 to both sides'], ['A / 2 = bh', 'A + 2 = bh']],
              ['divide both sides by b', 'h = 2A / b', ['multiply both sides by b', 'subtract b from both sides'], ['h = 2Ab', 'h = 2A − b']]],
      check: { given: 'A = 24, b = 8', value: 6 } },
    { f: 's = d / t', target: 't', ans: 't = d / s',
      steps: [['multiply both sides by t', 'st = d', ['divide both sides by t', 'add t to both sides'], ['s / t = d', 's + t = d']],
              ['divide both sides by s', 't = d / s', ['multiply both sides by s', 'subtract s from both sides'], ['t = ds', 't = d − s']]],
      check: { given: 'd = 150, s = 50', value: 3 } },
    { f: 'A = πr²', target: 'r', ans: 'r = √(A / π)',
      steps: [['divide both sides by π', 'A / π = r²', ['multiply both sides by π', 'subtract π from both sides'], ['Aπ = r²', 'A − π = r²']],
              ['take the square root of both sides', 'r = √(A / π)', ['square both sides', 'divide both sides by 2'], ['r = (A / π)²', 'r = A / (2π)']]],
      check: { given: 'A = 50.24 (use π = 3.14)', value: 4 } },
    { f: 'F = 9C / 5 + 32', target: 'C', ans: 'C = 5(F − 32) / 9',
      steps: [['subtract 32 from both sides', 'F − 32 = 9C / 5', ['add 32 to both sides', 'multiply both sides by 5'], ['F + 32 = 9C / 5', 'F = 9C / 5 − 32']],
              ['multiply both sides by 5', '5(F − 32) = 9C', ['divide both sides by 5', 'add 5 to both sides'], ['(F − 32) / 5 = 9C', 'F − 32 + 5 = 9C']],
              ['divide both sides by 9', 'C = 5(F − 32) / 9', ['multiply both sides by 9', 'subtract 9 from both sides'], ['C = 45(F − 32)', 'C = 5(F − 32) − 9']]],
      check: { given: 'F = 212', value: 100 } },
  ];

  let deck = [];
  function build() {
    if (!deck.length) deck = shuffle(BANK.map((_, k) => k));   // every formula once before any repeats
    const B = BANK[deck.pop()];
    let current = B.f;
    const steps = B.steps.map(([op, res, wrongOps, wrongRes], k) => {
      const before = current; current = res;
      return {
        html: `${k === 0 ? 'Start' : 'Now'}: <span class="g-code">${before}</span><br>To get ${B.target} alone, {0}<br>This gives: {1}`,
        fields: [{ answer: op, kind: 'choice', options: shuffle([op, ...wrongOps]), label: 'operation' },
                 { answer: res, kind: 'choice', options: shuffle([res, ...wrongRes]), label: 'result' }],
        hint: 'Undo what is done to ' + B.target + ' with the opposite operation. Undo + and − first, then × and ÷, then squares.',
        why: `We ${op}: <b>${res}</b>`,
      };
    });
    steps.push({
      html: `Check with numbers. If ${B.check.given}, then ${B.target} = {0}`,
      fields: [{ answer: B.check.value, kind: 'num', size: 5, label: B.target, tol: 0.05 }],
      hint: `Put the numbers into your answer: ${B.ans}`,
      why: `${B.ans} gives ${B.target} = <b>${B.check.value}</b>. ✔ Your new formula works.`,
    });
    return { q: `Make <b>${B.target}</b> the subject of <span class="g-code">${B.f}</span>`, steps };
  }

  const next = practice({ slug: 'change-subject', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'), build });
  $('pNew').addEventListener('click', next);
})();
