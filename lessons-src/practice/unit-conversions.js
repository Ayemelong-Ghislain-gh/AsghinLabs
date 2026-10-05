(function () {
  const $ = (id) => document.getElementById(id);
  const fmt = (n) => n.toLocaleString('en-US').replace(/,/g, ' ');

  runWalkthrough($('walk'), [
    {
      title: 'The storage ladder',
      html: `<div class="ladder"><span>bit</span><i>× 8</i><span>Byte</span><i>× 1024</i><span>KB</span><i>× 1024</i><span>MB</span><i>× 1024</i><span>GB</span><i>× 1024</i><span>TB</span></div>
             <p>8 bits = 1 byte. After that, each unit is 1024 of the one before.</p>
             <p class="wt-key">1 KB = 1024 B · 1 MB = 1024 KB · 1 GB = 1024 MB</p>`,
    },
    {
      title: 'Big unit → small unit: multiply',
      html: `<p>Going down the ladder (GB → MB → KB …) the number gets <b>bigger</b>, so <b>multiply</b>.</p>
             <p>3 MB = 3 × 1024 = <b>3072 KB</b></p>
             <p class="wt-key">One step = × 1024 (or × 8 for bytes → bits).</p>`,
    },
    {
      title: 'Small unit → big unit: divide',
      html: `<p>Going up the ladder (KB → MB → GB …) the number gets <b>smaller</b>, so <b>divide</b>.</p>
             <p>4096 KB = 4096 ÷ 1024 = <b>4 MB</b></p>
             <p class="wt-key">Two steps? Do it twice: GB → KB = × 1024 × 1024.</p>`,
    },
    {
      title: 'Time units',
      html: `<p>60 seconds = 1 minute · 60 minutes = 1 hour · 24 hours = 1 day</p>
             <p>2 h 15 min = 2 × 60 + 15 = <b>135 min</b></p>
             <p class="wt-key">Same rule: big → small multiply, small → big divide.</p>`,
    },
  ]);

  const UNITS = ['bits', 'bytes', 'KB', 'MB', 'GB', 'TB'];
  const factor = (i) => (i === 0 ? 8 : 1024);          // factor between UNITS[i] and UNITS[i+1]

  function storageQ() {
    const down = Math.random() < 0.5;
    let hi, lo;
    do { hi = rint(1, 5); lo = hi - rint(1, 2); } while (lo < 0 || (lo === 0 && hi - lo > 1));
    let n, val = [];
    if (down) {                                         // big → small: start small number
      n = rint(2, 9);
      val = [n];
      for (let i = hi - 1; i >= lo; i--) val.push(val[val.length - 1] * factor(i));
    } else {                                            // small → big: start from exact multiple
      const top = rint(2, 9);
      const chain = [top];
      for (let i = hi - 1; i >= lo; i--) chain.push(chain[chain.length - 1] * factor(i));
      val = chain.reverse();
    }
    const from = down ? UNITS[hi] : UNITS[lo], to = down ? UNITS[lo] : UNITS[hi];
    const stepsN = hi - lo;
    const steps = [
      {
        html: `${from} → ${to}: the starting unit is the {0} one, so we {1}.`,
        fields: [{ answer: down ? 'bigger' : 'smaller', kind: 'choice', options: ['bigger', 'smaller'], label: 'bigger or smaller' },
                 { answer: down ? 'multiply' : 'divide', kind: 'choice', options: ['multiply', 'divide'], label: 'multiply or divide' }],
        hint: 'Look at the ladder: bits, bytes, KB, MB, GB, TB. Is the starting unit higher up or lower down?',
        why: down ? `${from} is bigger than ${to}: going down the ladder, so <b>multiply</b>.` : `${from} is smaller than ${to}: going up the ladder, so <b>divide</b>.`,
      },
      {
        html: `How many steps on the ladder from ${from} to ${to}? {0}`,
        fields: [{ answer: stepsN, kind: 'int', size: 2, label: 'steps' }],
        hint: 'Count the jumps between the two units on the ladder.',
        why: `${stepsN} step${stepsN > 1 ? 's' : ''}: ${(down ? UNITS.slice(lo, hi + 1).reverse() : UNITS.slice(lo, hi + 1)).join(' → ')}.`,
      },
    ];
    for (let k = 0; k < stepsN; k++) {
      const i = down ? hi - 1 - k : lo + k;           // ladder index of this jump
      const f = factor(i), a = val[k], b = val[k + 1];
      const u1 = down ? UNITS[i + 1] : UNITS[i], u2 = down ? UNITS[i] : UNITS[i + 1];
      steps.push({
        html: `${fmt(a)} ${u1} ${down ? '×' : '÷'} ${f} = {0} ${u2}`,
        fields: [{ answer: b, kind: 'int', size: 8, label: u2 }],
        hint: down ? `Multiply ${fmt(a)} by ${f}.` : `Divide ${fmt(a)} by ${f}. It divides exactly.`,
        why: `${fmt(a)} ${u1} = <b>${fmt(b)} ${u2}</b>.`,
      });
    }
    return { q: `Convert <b>${fmt(val[0])} ${from}</b> to <b>${to}</b>.`, steps };
  }

  function timeQ() {
    const kind = pick(['h2m', 'm2h', 'd2h', 'm2s']);
    if (kind === 'h2m') {
      const h = rint(1, 9), m = rint(5, 55);
      return { q: `Convert <b>${h} h ${m} min</b> to minutes.`, steps: [
        { html: `First the hours: ${h} h × 60 = {0} min`, fields: [{ answer: h * 60, kind: 'int', size: 4 }], hint: '1 hour = 60 minutes.', why: `${h} × 60 = <b>${h * 60}</b> minutes.` },
        { html: `Add the extra minutes: ${h * 60} + ${m} = {0} min`, fields: [{ answer: h * 60 + m, kind: 'int', size: 4 }], hint: 'Add the two numbers.', why: `${h} h ${m} min = <b>${h * 60 + m} min</b>.` },
      ] };
    }
    if (kind === 'm2h') {
      const h = rint(1, 9), m = rint(1, 59), total = h * 60 + m;
      return { q: `Convert <b>${total} min</b> to hours and minutes.`, steps: [
        { html: `Divide by 60: ${total} ÷ 60 = {0} remainder {1}`, fields: [{ answer: h, kind: 'int', size: 3 }, { answer: m, kind: 'int', size: 3 }],
          hint: `How many whole 60s fit in ${total}? The remainder is what is left over.`, why: `60 × ${h} = ${h * 60}, and ${total} − ${h * 60} = ${m}.` },
        { html: `So ${total} min = {0} h {1} min`, fields: [{ answer: h, kind: 'int', size: 3 }, { answer: m, kind: 'int', size: 3 }],
          hint: 'The answer of the division is the hours, the remainder is the minutes.', why: `<b>${h} h ${m} min</b>.` },
      ] };
    }
    if (kind === 'd2h') {
      const d = rint(2, 7);
      return { q: `How many hours are in <b>${d} days</b>?`, steps: [
        { html: `1 day = {0} hours`, fields: [{ answer: 24, kind: 'int', size: 3 }], hint: 'A full day and night.', why: '1 day = <b>24 hours</b>.' },
        { html: `${d} × 24 = {0} hours`, fields: [{ answer: d * 24, kind: 'int', size: 4 }], hint: 'Big unit → small unit: multiply.', why: `${d} days = <b>${d * 24} hours</b>.` },
      ] };
    }
    const m = rint(2, 15);
    return { q: `How many seconds are in <b>${m} minutes</b>?`, steps: [
      { html: `1 minute = {0} seconds`, fields: [{ answer: 60, kind: 'int', size: 3 }], hint: 'Think of a clock.', why: '1 min = <b>60 s</b>.' },
      { html: `${m} × 60 = {0} seconds`, fields: [{ answer: m * 60, kind: 'int', size: 4 }], hint: 'Big unit → small unit: multiply.', why: `${m} min = <b>${m * 60} s</b>.` },
    ] };
  }

  const next = practice({
    slug: 'unit-conversions', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'),
    build: () => ($('pType').value === 'time' ? timeQ() : $('pType').value === 'mix' ? (Math.random() < 0.6 ? storageQ() : timeQ()) : storageQ()),
  });
  $('pNew').addEventListener('click', next);
  $('pType').addEventListener('change', next);
})();
