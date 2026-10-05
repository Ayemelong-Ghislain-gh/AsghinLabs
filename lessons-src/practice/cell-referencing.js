(function () {
  const $ = (id) => document.getElementById(id);
  const COLS = 'ABCDEF';
  const fmt = (n) => n.toLocaleString('en-US').replace(/,/g, ' ');

  runWalkthrough($('walk'), [
    {
      title: 'Copying a formula changes it',
      html: `<p>D2 has <span class="g-code">=B2*C2</span>. Copy it down to D3:</p>
             <p>it becomes <span class="g-code">=B3*C3</span></p>
             <p class="wt-key">Moved 1 row down → every row number goes up by 1.</p>`,
    },
    {
      title: 'Relative reference: B2',
      html: `<p>No $ sign. It <b>changes</b> when copied.</p>
             <ul><li>Copy down → the row number changes (B2 → B3)</li><li>Copy across → the letter changes (B2 → C2)</li></ul>`,
    },
    {
      title: 'Absolute reference: $F$1',
      html: `<p>$ in front of the letter <b>and</b> the number. It <b>never changes</b>.</p>
             <p>D2: <span class="g-code">=B2*$F$1</span> → copied to D5: <span class="g-code">=B5*$F$1</span></p>
             <p class="wt-key">Use $ for a cell everyone must use, like a rate or a fee.</p>`,
    },
    {
      title: 'Mixed reference: $B2 or B$2',
      html: `<p>Only one part is locked:</p>
             <ul><li><b>$B2</b>: column locked, row changes</li><li><b>B$2</b>: row locked, column changes</li></ul>
             <p class="wt-key">The $ locks whatever comes right after it.</p>`,
    },
  ]);

  const refRe = /(\$?)([A-F])(\$?)(\d+)/g;
  const kindOf = (r) => { const m = /(\$?)[A-F](\$?)\d+/.exec(r); return m[1] && m[2] ? 'absolute' : m[1] || m[2] ? 'mixed' : 'relative'; };
  const shift = (f, dr, dc) => f.replace(refRe, (all, c$, c, r$, r) => c$ + (c$ ? c : COLS[COLS.indexOf(c) + dc]) + r$ + (r$ ? r : Number(r) + dr));

  function sheet(data, formulaCell, formula, target) {
    const val = (c, r) => data[c + r];
    let h = '<div class="sheet-wrap"><table class="sheet"><tr><th></th>' + [...COLS].map(c => `<th>${c}</th>`).join('') + '</tr>';
    for (let r = 1; r <= 7; r++) {
      h += `<tr><th>${r}</th>`;
      for (const c of COLS) {
        const id = c + r;
        let v = val(c, r); v = v == null ? '' : typeof v === 'number' ? fmt(v) : v;
        if (id === formulaCell) v = `<span class="f-cell">${formula}</span>`;
        if (id === target) v = '<span class="t-cell">?</span>';
        h += `<td class="${id === formulaCell ? 'src' : id === target ? 'dst' : ''}">${v}</td>`;
      }
      h += '</tr>';
    }
    return h + '</table></div>';
  }

  function evaluate(f, data) {
    let e = f.replace(/^=/, '').replace(/SUM\(\$?([A-F])\$?(\d+):\$?([A-F])\$?(\d+)\)/g, (m, c1, r1, c2, r2) => {
      let s = 0;
      for (let c = COLS.indexOf(c1); c <= COLS.indexOf(c2); c++) for (let r = +r1; r <= +r2; r++) s += Number(data[COLS[c] + r]) || 0;
      return '(' + s + ')';
    }).replace(refRe, (all, a, c, b, r) => '(' + (Number(data[c + r]) || 0) + ')');
    if (!/^[0-9+\-*/(). ]+$/.test(e)) return NaN;
    return Function('return ' + e)();
  }

  function build() {
    const hard = $('pLevel').value === 'hard';
    const items = ['Pens', 'Books', 'Bags', 'Rulers', 'Chalk'];
    const data = { A1: 'Item', B1: 'Price', C1: 'Qty', D1: 'Total', E1: 'Fee', F1: pick([100, 200, 250, 500]) };
    items.forEach((it, i) => { data['A' + (i + 2)] = it; data['B' + (i + 2)] = rint(1, 18) * 50; data['C' + (i + 2)] = rint(1, 9); });
    data.A7 = 'Total';

    let src, formula, target, dr, dc;
    const across = hard && Math.random() < 0.35;
    if (across) {
      src = 'B7'; formula = pick(['=SUM(B2:B6)', '=SUM(B2:B6)+$F$1', '=B$2+B6']); target = 'C7'; dr = 0; dc = 1;
    } else {
      src = 'D2';
      formula = hard ? pick(['=B2*C2+$F$1', '=$B2*C2', '=B2*C$2', '=(B2+$F$1)*C2']) : pick(['=B2*C2', '=B2*$F$1', '=B2+C2', '=B2*C2+$F$1']);
      const r = rint(3, 6); target = 'D' + r; dr = r - 2; dc = 0;
    }
    const refs = formula.match(/\$?[A-F]\$?\d+/g);
    const uniq = [...new Set(refs)];
    const newF = shift(formula, dr, dc);
    const value = evaluate(newF, data);
    const steps = [
      {
        html: 'What type is each reference?<br>' + uniq.map((r, i) => `<span class="g-code">${r}</span> is {${i}}`).join('<br>'),
        fields: uniq.map(r => ({ answer: kindOf(r), kind: 'choice', options: ['relative', 'absolute', 'mixed'], label: r })),
        hint: 'No $ → relative. $ before the letter AND the number → absolute. Only one $ → mixed.',
        why: uniq.map(r => `${r}: <b>${kindOf(r)}</b>`).join(' · '),
      },
      {
        html: `From ${src} to ${target}, the formula moves {0} row(s) down and {1} column(s) across.`,
        fields: [{ answer: dr, kind: 'int', size: 2 }, { answer: dc, kind: 'int', size: 2 }],
        hint: `Compare the row numbers (${src.slice(1)} → ${target.slice(1)}) and the letters (${src[0]} → ${target[0]}).`,
        why: `<b>${dr}</b> row(s) down and <b>${dc}</b> column(s) across.`,
      },
      {
        html: `So ${target} contains: {0}`,
        fields: [{ answer: newF, kind: 'text', size: 14, label: 'formula' }],
        hint: `Add ${dr} to every row number and move every letter ${dc} place(s) across — except the parts locked with $.`,
        why: `${formula} → <b>${newF}</b>`,
      },
      {
        html: `Use the sheet: the value shown in ${target} is {0}`,
        fields: [{ answer: value, kind: 'int', size: 7, label: 'value' }],
        hint: `Replace each cell in ${newF} with its number from the sheet, then calculate.`,
        why: (/SUM/.test(newF) ? `${newF.replace(/^=/, '')} adds the cells in the range` : newF.replace(/^=/, '').replace(refRe, (m, a, c, b, r) => fmt(data[c + r]))) + ` = <b>${fmt(value)}</b>`,
      },
    ];
    return { q: `${src} contains <span class="g-code">${formula}</span>. It is copied to <b>${target}</b>.${sheet(data, src, formula, target)}`, steps };
  }

  const next = practice({ slug: 'cell-referencing', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'), build });
  $('pNew').addEventListener('click', next);
  $('pLevel').addEventListener('change', next);
})();
