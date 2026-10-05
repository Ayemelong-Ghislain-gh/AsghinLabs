(function () {
  const $ = (id) => document.getElementById(id);
  const S = (k) => (k < 0 ? '−' : '') + Math.abs(k);
  const P = (k) => (k < 0 ? '(' + S(k) + ')' : String(k));
  const lhs = (a, b) => polyStr([0, a, 0]) + ' ' + (b < 0 ? '− ' : '+ ') + (Math.abs(b) === 1 ? '' : Math.abs(b)) + 'y';
  const eq = (a, b, c) => `${lhs(a, b)} = ${S(c)}`;

  runWalkthrough($('walk'), [
    {
      title: 'Two equations, two unknowns',
      html: `<p>x + y = 10 and x − y = 4</p>
             <p>We need the <b>one</b> pair of numbers that makes <b>both</b> true.</p>
             <p class="wt-key">Here x = 7 and y = 3. Check: 7 + 3 = 10 ✓ and 7 − 3 = 4 ✓</p>`,
    },
    {
      title: 'Eliminate one letter',
      html: `<p>Make one letter disappear by adding or subtracting the equations.</p>
             <ul><li>Signs <b>different</b> (+y and −y) → <b>add</b></li><li>Signs the <b>same</b> (+y and +y) → <b>subtract</b></li></ul>
             <p class="wt-key">(x + y) + (x − y) = 10 + 4 → 2x = 14 → x = 7</p>`,
    },
    {
      title: 'Find the other letter',
      html: `<p>Put x = 7 into one of the equations:</p>
             <p>7 + y = 10 → y = 10 − 7 = <b>3</b></p>
             <p class="wt-key">Then check your pair in the other equation.</p>`,
    },
    {
      title: 'When the numbers don\'t match',
      html: `<p>2x + 3y = 13 and x + y = 5</p>
             <p>Multiply the second equation by 3: 3x + 3y = 15</p>
             <p>Now the y terms match. Subtract: (3x + 3y) − (2x + 3y) = 15 − 13 → <b>x = 2</b>, then y = 3.</p>
             <p class="wt-key">Multiply so that one letter has the same number in both equations.</p>`,
    },
  ]);

  function build() {
    const hard = $('pLevel').value === 'hard';
    let x, y, a1, b1, a2, b2;
    do {
      x = rnz(-5, 7); y = rnz(-5, 7);
      a1 = rnz(1, 4); a2 = rnz(1, 4);
      if (hard) { b1 = rnz(-4, 4); b2 = rnz(-4, 4); }
      else { b1 = rnz(1, 4); b2 = pick([b1, -b1]); }
    } while (a1 * b2 - a2 * b1 === 0 || (hard && Math.abs(b1) === Math.abs(b2)) || Math.abs(a1 * b2 - a2 * b1) > 16);
    const c1 = a1 * x + b1 * y, c2 = a2 * x + b2 * y;
    const steps = [];
    let A1 = a1, B1 = b1, C1 = c1, A2 = a2, B2 = b2, C2 = c2;

    if (hard) {
      const g = gcd(b1, b2), k1 = Math.abs(b2) / g, k2 = Math.abs(b1) / g;
      steps.push({
        html: `To make the y numbers match, multiply equation (1) by {0} and equation (2) by {1}`,
        fields: [{ answer: k1, kind: 'int', size: 2, label: 'multiply (1) by' }, { answer: k2, kind: 'int', size: 2, label: 'multiply (2) by' }],
        validate: (v) => { const p = Number(v[0]), q = Number(v[1]); const ok = p === k1 && q === k2;
          const near = p > 0 && q > 0 && p * Math.abs(b1) === q * Math.abs(b2);
          return { ok: [ok, ok], notes: ok ? [] : [near ? `That works too, but use the smallest numbers: ${k1} and ${k2}.` : `${P(p)} × ${S(Math.abs(b1))} and ${P(q)} × ${S(Math.abs(b2))} are not the same number.`] }; },
        hint: `The y numbers are ${S(Math.abs(b1))} and ${S(Math.abs(b2))}. Find the smallest number both go into, then see what each must be multiplied by.`,
        why: `${k1} × ${Math.abs(b1)} = ${k1 * Math.abs(b1)} and ${k2} × ${Math.abs(b2)} = ${k2 * Math.abs(b2)}. Now both y numbers are ${k1 * Math.abs(b1)}.`,
      });
      A1 = a1 * k1; B1 = b1 * k1; C1 = c1 * k1; A2 = a2 * k2; B2 = b2 * k2; C2 = c2 * k2;
      steps.push({
        html: `Write the new equations:<br>(1) × ${k1}: {0}x + {1}y = {2}<br>(2) × ${k2}: {3}x + {4}y = {5}`,
        fields: [A1, B1, C1, A2, B2, C2].map(n => ({ answer: n, kind: 'int', size: 3 })),
        hint: 'Multiply every term of the equation, including the number after =. Keep the signs.',
        why: `(1): <b>${eq(A1, B1, C1)}</b> &nbsp; (2): <b>${eq(A2, B2, C2)}</b>`,
      });
    }
    const add = B1 === -B2;
    steps.push({
      html: `The y terms are ${S(B1)}y and ${S(B2)}y. To eliminate y, we {0} the equations.`,
      fields: [{ answer: add ? 'add' : 'subtract', kind: 'choice', options: ['add', 'subtract'], label: 'add or subtract' }],
      hint: 'Different signs → add. Same signs → subtract.',
      why: add ? `${S(B1)}y + ${P(B2)}y = 0, so we <b>add</b>.` : `${S(B1)}y − ${P(B2)}y = 0, so we <b>subtract</b>.`,
    });
    const AX = add ? A1 + A2 : A1 - A2, CX = add ? C1 + C2 : C1 - C2;
    steps.push({
      html: `${add ? 'Add' : 'Subtract'}: {0}x = {1}`,
      fields: [{ answer: AX, kind: 'int', size: 3 }, { answer: CX, kind: 'int', size: 4 }],
      hint: add ? `x numbers: ${S(A1)} + ${P(A2)}. Right side: ${S(C1)} + ${P(C2)}.` : `x numbers: ${S(A1)} − ${P(A2)}. Right side: ${S(C1)} − ${P(C2)}.`,
      why: `The y terms cancel and we get <b>${polyStr([0, AX, 0])} = ${S(CX)}</b>.`,
    });
    steps.push({
      html: `Divide: x = ${S(CX)} ÷ ${P(AX)} = {0}`,
      fields: [{ answer: x, kind: 'int', size: 3 }],
      hint: 'Divide the right side by the number in front of x. Watch the signs.',
      why: `<b>x = ${S(x)}</b>`,
    });
    steps.push({
      html: `Put x = ${S(x)} into equation (1) ${eq(a1, b1, c1)}:<br>${S(a1 * x)} ${b1 < 0 ? '−' : '+'} ${Math.abs(b1) === 1 ? '' : Math.abs(b1)}y = ${S(c1)} → {0}y = {1} → y = {2}`,
      fields: [{ answer: b1, kind: 'int', size: 3 }, { answer: c1 - a1 * x, kind: 'int', size: 4 }, { answer: y, kind: 'int', size: 3 }],
      hint: `Move ${S(a1 * x)} to the other side (change its sign), then divide by the number in front of y.`,
      why: `${S(b1)}y = ${S(c1)} − ${P(a1 * x)} = ${S(c1 - a1 * x)}, so <b>y = ${S(y)}</b>.`,
    });
    steps.push({
      html: `Check in equation (2): ${S(a2)} × ${P(x)} + ${P(b2)} × ${P(y)} = {0}`,
      fields: [{ answer: c2, kind: 'int', size: 4 }],
      hint: 'Multiply, then add.',
      why: `It gives ${S(c2)}, the right side of equation (2). ✔ The answer is <b>x = ${S(x)}, y = ${S(y)}</b>.`,
    });
    return { q: `Solve: <span class="eq-pair"><span>(1) ${eq(a1, b1, c1)}</span><span>(2) ${eq(a2, b2, c2)}</span></span>`, steps };
  }

  const next = practice({ slug: 'simultaneous-equations', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'), build });
  $('pNew').addEventListener('click', next);
  $('pLevel').addEventListener('change', next);
})();
