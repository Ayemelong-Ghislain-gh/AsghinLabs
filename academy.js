(function () {
  // Levels are shown in this order when present; anything with a level
  // not listed here (or no level at all) is grouped under "General" at
  // the end, so new material never breaks the layout — it just lands
  // in the right bucket, or a sensible fallback one.
  const LEVEL_ORDER = ['O Level', 'Lower Sixth', 'Upper Sixth'];

  function groupByLevel(items) {
    const groups = new Map();
    items.forEach(item => {
      const level = item.level || 'General';
      if (!groups.has(level)) groups.set(level, []);
      groups.get(level).push(item);
    });

    const orderedKeys = [
      ...LEVEL_ORDER.filter(l => groups.has(l)),
      ...[...groups.keys()].filter(l => !LEVEL_ORDER.includes(l)),
    ];
    return orderedKeys.map(level => ({ level, items: groups.get(level) }));
  }

  function fileCard(item) {
    return `
      <a href="${item.file}" target="_blank" rel="noopener" class="academy-file-card">
        <span class="academy-file-subject">${item.subject || ''}</span>
        <h4>${item.title}</h4>
        <span class="academy-file-link">Download →</span>
      </a>`;
  }

  function renderList(containerId, items, emptyIcon, emptyText, emptySub) {
    const el = document.getElementById(containerId);
    if (!el) return;

    if (!items || items.length === 0) {
      el.innerHTML = `
        <div class="academy-empty">
          <div class="academy-empty-icon">${emptyIcon}</div>
          <p>${emptyText}</p>
          <p class="academy-empty-sub">${emptySub}</p>
        </div>`;
      return;
    }

    const groups = groupByLevel(items);

    el.innerHTML = groups.map(group => `
      <div class="academy-level-group">
        <h3 class="academy-level-heading">${group.level}</h3>
        <div class="academy-file-grid">
          ${group.items.map(fileCard).join('')}
        </div>
      </div>
    `).join('');
  }

  renderList(
    'notesGallery',
    typeof ACADEMY_NOTES !== 'undefined' ? ACADEMY_NOTES : [],
    '🗂️', 'No notes uploaded yet — check back soon.',
    'Complete programs and lesson notes will be added here as they\'re ready.'
  );

  renderList(
    'pastQuestionsGallery',
    typeof ACADEMY_PAST_QUESTIONS !== 'undefined' ? ACADEMY_PAST_QUESTIONS : [],
    '🧾', 'No past questions uploaded yet — check back soon.',
    'Practice papers will be added here as they\'re ready.'
  );
})();
