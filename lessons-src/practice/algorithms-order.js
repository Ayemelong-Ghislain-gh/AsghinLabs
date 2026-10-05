(function () {
  const $ = (id) => document.getElementById(id);

  runWalkthrough($('walk'), [
    {
      title: 'What is an algorithm?',
      html: `<p>An algorithm is a list of <b>steps</b> to solve a problem or do a task.</p>
             <p>A recipe is an algorithm. So are the instructions to switch on a computer.</p>
             <p class="wt-key">Computers follow algorithms exactly, step by step.</p>`,
    },
    {
      title: 'The order matters',
      html: `<p>Making tea:</p>
             <ol><li>Boil water</li><li>Put the tea bag in a cup</li><li>Pour the water into the cup</li><li>Add sugar and stir</li></ol>
             <p class="wt-key">If you pour the water before boiling it, the tea is cold!</p>`,
    },
    {
      title: 'A good algorithm',
      html: `<ul><li>Has a clear <b>start</b> and a clear <b>end</b></li><li>Each step is <b>simple</b> and clear</li><li>Steps are in the <b>right order</b></li><li>Has <b>no missing</b> steps</li></ul>`,
    },
    {
      title: 'How to order the steps',
      html: `<p>Ask: <b>"What must happen first?"</b> Then: <b>"What can I do only after that?"</b></p>
             <p>You can't save a document before you type it, and you can't type before you open the program.</p>
             <p class="wt-key">Each step needs the one before it to be done.</p>`,
    },
  ]);

  const TASKS = [
    { name: 'switch on a computer and open a document', steps: ['Press the power button', 'Wait for the desktop to appear', 'Double-click the folder', 'Double-click the document to open it'] },
    { name: 'save a new document in a word processor', steps: ['Open the word processor', 'Type your text', 'Click File, then Save', 'Type a file name', 'Click the Save button'] },
    { name: 'send an email', steps: ['Open your email and log in', 'Click Compose', 'Type the address of the person', 'Write the subject and the message', 'Click Send'] },
    { name: 'search for information on the internet', steps: ['Open a web browser', 'Go to a search engine', 'Type your keywords', 'Press Enter', 'Open a result and read it'] },
    { name: 'wash your hands', steps: ['Open the tap', 'Wet your hands', 'Rub your hands with soap', 'Rinse off the soap', 'Close the tap and dry your hands'] },
    { name: 'make tea', steps: ['Boil water', 'Put the tea bag in a cup', 'Pour the hot water into the cup', 'Add sugar and stir'] },
    { name: 'shut down a computer safely', steps: ['Save your work', 'Close all programs', 'Click Start', 'Click Shut down'] },
    { name: 'print a document', steps: ['Open the document', 'Check the printer is on', 'Click File, then Print', 'Choose the number of copies', 'Click Print'] },
  ];

  let deck = [];
  function build() {
    if (!deck.length) deck = shuffle(TASKS.map((_, k) => k));
    const T = TASKS[deck.pop()];
    const n = T.steps.length;
    const options = shuffle(T.steps);
    // a "buggy" version with two neighbouring steps swapped
    const s = rint(0, n - 2);
    const bug = T.steps.slice(); [bug[s], bug[s + 1]] = [bug[s + 1], bug[s]];
    return {
      q: `Write an algorithm to <b>${T.name}</b>.`,
      steps: [
        {
          html: 'Put the steps in the right order:<div class="order-list">' + T.steps.map((_, i) => `<div><span class="ol-n">${i + 1}</span>{${i}}</div>`).join('') + '</div>',
          fields: T.steps.map((st, i) => ({ answer: st, kind: 'choice', options, label: 'Step ' + (i + 1) })),
          validate: (v) => {
            const ok = v.map((x, i) => x === T.steps[i].replace(/\s+/g, ''));
            const notes = [];
            const used = v.filter(Boolean);
            if (new Set(used).size < used.length) notes.push('You used the same step twice. Each step is used once.');
            return { ok, notes };
          },
          hint: 'Ask "what must happen first?" Each step needs the step before it to be done already.',
          why: 'Correct order:<ol class="why-list">' + T.steps.map(x => `<li>${x}</li>`).join('') + '</ol>',
        },
        {
          html: `A classmate wrote this. Two steps are in the wrong order. Which ones?<ol class="why-list bug-list">${bug.map(x => `<li>${x}</li>`).join('')}</ol>Step {0} and step {1} must swap.`,
          fields: [{ answer: s + 1, kind: 'int', size: 2, label: 'first step number' }, { answer: s + 2, kind: 'int', size: 2, label: 'second step number' }],
          validate: (v) => { const a = Number(v[0]), b = Number(v[1]); const ok = (a === s + 1 && b === s + 2) || (a === s + 2 && b === s + 1); return { ok: [ok, ok] }; },
          hint: 'Read the steps one by one. Where does a step need something that has not happened yet?',
          why: `Steps <b>${s + 1}</b> and <b>${s + 2}</b>: "${T.steps[s]}" must come before "${T.steps[s + 1]}".`,
        },
        {
          html: `How many steps does this algorithm have? {0}. Its first step is {1}`,
          fields: [{ answer: n, kind: 'int', size: 2, label: 'number of steps' }, { answer: T.steps[0], kind: 'choice', options: shuffle(T.steps), label: 'first step' }],
          hint: 'Count the steps in the correct order above. A good algorithm has a clear start.',
          why: `${n} steps, starting with "<b>${T.steps[0]}</b>" and ending with "<b>${T.steps[n - 1]}</b>".`,
        },
      ],
    };
  }

  const next = practice({ slug: 'algorithms-order', questionEl: $('pQuestion'), stepsEl: $('pSteps'), scoreEl: $('pScore'), build });
  $('pNew').addEventListener('click', next);
})();
