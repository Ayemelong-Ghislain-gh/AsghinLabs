(function () {
  const $ = (id) => document.getElementById(id);
  const r2 = (n) => Math.round(n * 100) / 100;

  runWalkthrough($('walk'), [
    {
      title: 'What scheduling means',
      html: `<p>Many processes want the CPU, but it runs <b>one at a time</b>. The scheduler decides the order.</p>
             <p>Each process has an <b>arrival time</b> (when it comes) and a <b>burst time</b> (how long it needs).</p>
             <p class="wt-key">We draw the order as a Gantt chart: a row of blocks along a time line.</p>`,
    },
    {
      title: 'FCFS and SJF',
      html: `<ul><li><b>FCFS</b> (First Come First Served): run them in the order they <b>arrive</b>.</li>
             <li><b>SJF</b> (Shortest Job First): when the CPU is free, pick the <b>shortest burst</b> among those that have arrived.</li></ul>
             <p class="wt-key">Both are non-preemptive: once a process starts, it finishes.</p>`,
    },
    {
      title: 'Round Robin',
      html: `<p>Each process runs for at most one <b>time quantum</b> (e.g. 2 units), then goes to the back of the queue if it is not finished.</p>
             <p>P1(5), P2(3), q = 2 → P1 P2 P1 P2 P1</p>
             <p class="wt-key">New arrivals join the queue before the process that was just stopped.</p>`,
    },
    {
      title: 'The three formulas',
      html: `<ul><li><b>Completion</b> = time the process finishes (read it from the Gantt chart)</li>
             <li><b>Turnaround</b> = Completion − Arrival</li><li><b>Waiting</b> = Turnaround − Burst</li></ul>
             <p class="wt-key">Average waiting = add all waiting times ÷ number of processes.</p>`,
    },
  ]);

  function simulate(algo, P, q) {
    const slots = [];
    if (algo === 'FCFS' || algo === 'SJF') {
      let t = 0; const left = P.slice();
      while (left.length) {
        const ready = left.filter(p => p.at <= t);
        const pickP = algo === 'FCFS' ? ready.sort((a, b) => a.at - b.at || a.id - b.id)[0] : ready.sort((a, b) => a.bt - b.bt || a.at - b.at || a.id - b.id)[0];
        slots.push({ p: pickP.name, start: t, end: t + pickP.bt }); t += pickP.bt;
        left.splice(left.indexOf(pickP), 1);
      }
      return slots;
    }
    // Round Robin
    const rem = Object.fromEntries(P.map(p => [p.name, p.bt]));
    const order = P.slice().sort((a, b) => a.at - b.at || a.id - b.id);
    let t = 0, i = 0; const queue = [];
    while (i < order.length && order[i].at <= t) queue.push(order[i++]);
    while (queue.length) {
      const p = queue.shift(); const run = Math.min(q, rem[p.name]);
      slots.push({ p: p.name, start: t, end: t + run }); t += run; rem[p.name] -= run;
      while (i < order.length && order[i].at <= t) queue.push(order[i++]);
      if (rem[p.name] > 0) queue.push(p);
    }
    return slots;
  }

  function gantt(slots, endField) {
    const bars = slots.map(s => `<div class="g-blk g-${s.p}" style="flex:${s.end - s.start}">${s.p}</div>`).join('');
    const times = slots.map((s, i) => `<div class="g-t" style="flex:${s.end - s.start}">${endField ? `{${i}}` : s.end}</div>`).join('');
    return `<div class="gantt" style="--n:${slots.length}"><div class="g-bars">${bars}</div><div class="g-times"><span class="g-t0">0</span>${times}</div></div>`;
  }

  function build() {
    const algo = $('pAlgo').value;
    const n = algo === 'RR' ? 3 : 4, q = 2;
    let P;
    do {
      P = []; let at = 0, sum = 0;
      for (let k = 0; k < n; k++) {
        const bt = rint(2, algo === 'RR' ? 5 : 8);
        P.push({ id: k, name: 'P' + (k + 1), at, bt });
        sum += bt; at = Math.min(at + rint(1, 3), sum - 1);   // next one arrives before the CPU is free (no idle time)
      }
    } while (algo === 'SJF' && simulate('SJF', P).map(s => s.p).join() === simulate('FCFS', P).map(s => s.p).join() && Math.random() < 0.8);
    const slots = simulate(algo, P, q);
    const comp = Object.fromEntries(P.map(p => [p.name, Math.max(...slots.filter(s => s.p === p.name).map(s => s.end))]));
    const tat = P.map(p => comp[p.name] - p.at), wt = P.map((p, k) => tat[k] - p.bt);
    const avg = r2(wt.reduce((a, b) => a + b, 0) / n);
    const names = P.map(p => p.name);
    const table = (extra) => '<div class="vt-wrap"><table class="vt pt"><tr><th>Process</th><th>Arrival</th><th>Burst</th>' + extra.map(e => `<th>${e.h}</th>`).join('') + '</tr>' +
      P.map((p, k) => `<tr><td>${p.name}</td><td>${p.at}</td><td>${p.bt}</td>` + extra.map(e => `<td>${e.cell(k)}</td>`).join('') + '</tr>').join('') + '</table></div>';
    const algoName = { FCFS: 'First Come First Served', SJF: 'Shortest Job First (non-preemptive)', RR: `Round Robin (quantum = ${q})` }[algo];

    const steps = [
      {
        html: (algo === 'RR' ? `Order of the Gantt chart blocks (each block runs at most ${q} units):<br>` : 'Order in which the processes run:<br>') +
          slots.map((s, i) => `{${i}}`).join(' → '),
        fields: slots.map(s => ({ answer: s.p, kind: 'choice', options: names, size: 3 })),
        hint: algo === 'FCFS' ? 'Sort by arrival time.' : algo === 'SJF' ? 'At time 0 only the processes that have arrived can run. Each time the CPU is free, choose the shortest burst among those waiting.'
          : 'Take the first process in the queue, run it for up to 2 units, then put it at the back if it still needs time. Add new arrivals to the queue before it.',
        why: 'Order: <b>' + slots.map(s => s.p).join(' → ') + '</b>',
      },
      {
        html: 'Now the times. Write the time at the <b>end</b> of each block:' + gantt(slots, true),
        fields: slots.map(s => ({ answer: s.end, kind: 'int', size: 2 })),
        hint: 'Start at 0. Each block ends at: its start + how long it runs.',
        why: 'Gantt chart:' + gantt(slots, false),
      },
      {
        html: 'Completion time of each process (when it finishes for the last time):' + table([{ h: 'Completion', cell: (k) => `{${k}}` }]),
        fields: P.map(p => ({ answer: comp[p.name], kind: 'int', size: 2 })),
        hint: algo === 'RR' ? 'Look for the LAST block of each process in the Gantt chart.' : 'Read the end of each process\'s block.',
        why: names.map(nm => `${nm} = ${comp[nm]}`).join(' · '),
      },
      {
        html: 'Turnaround = Completion − Arrival:' + table([{ h: 'Completion', cell: (k) => comp[names[k]] }, { h: 'Turnaround', cell: (k) => `{${k}}` }]),
        fields: tat.map(v => ({ answer: v, kind: 'int', size: 2 })),
        hint: 'Subtract the arrival time from the completion time for each row.',
        why: P.map((p, k) => `${p.name}: ${comp[p.name]} − ${p.at} = ${tat[k]}`).join(' · '),
      },
      {
        html: 'Waiting = Turnaround − Burst:' + table([{ h: 'Turnaround', cell: (k) => tat[k] }, { h: 'Waiting', cell: (k) => `{${k}}` }]),
        fields: wt.map(v => ({ answer: v, kind: 'int', size: 2 })),
        hint: 'Subtract the burst time from the turnaround time for each row.',
        why: P.map((p, k) => `${p.name}: ${tat[k]} − ${p.bt} = ${wt[k]}`).join(' · '),
      },
      {
        html: `Average waiting time = (${wt.join(' + ')}) ÷ ${n} = {0}`,
        fields: [{ answer: avg, kind: 'num', size: 5, tol: 0.011 }],
        hint: 'Add the waiting times, then divide by the number of processes. Give 2 decimal places if needed.',
        why: `${wt.reduce((a, b) => a + b, 0)} ÷ ${n} = <b>${avg}</b> time units.`,
      },
    ];
    return { q: `<b>${algoName}</b>${table([])}`, steps };
  }

  const next = practice({ slug: 'cpu-scheduling', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'), build });
  $('pNew').addEventListener('click', next);
  $('pAlgo').addEventListener('change', next);
})();
