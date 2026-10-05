"""Small helpers so lesson content stays short and readable."""


def mcq(q, options, answer, why='', hint=None, visual=None, wrong=None):
    assert answer in options, (q, answer)
    a = dict(type='mcq', q=q, options=options, answer=answer, why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    if wrong: a['wrong'] = wrong
    return a


def tf(q, answer, why='', hint=None, visual=None):
    a = dict(type='tf', q=q, answer=bool(answer), why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    return a


def sort(q, groups, items, why='', hint=None, visual=None):
    for t, g in items: assert g in groups, (q, t, g)
    a = dict(type='sort', q=q, groups=groups, items=[list(i) for i in items], why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    return a


def match(q, pairs, why='', hint=None, visual=None):
    rights = [p[1] for p in pairs]; assert len(set(rights)) == len(rights), q
    a = dict(type='match', q=q, pairs=[list(p) for p in pairs], why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    return a


def order(q, items, why='', hint=None, visual=None):
    a = dict(type='order', q=q, items=list(items), why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    return a


def label(q, svg, labels, why='', hint=None):
    assert len(set(labels)) == len(labels), q
    a = dict(type='label', q=q, svg=svg, labels=list(labels), why=why)
    if hint: a['hint'] = hint
    return a


def fill(q, q2, answers, why='', hint=None, visual=None):
    a = dict(type='fill', q=q, q2=q2, answers=[[x] if isinstance(x, str) else list(x) for x in answers], why=why)
    if hint: a['hint'] = hint
    if visual: a['visual'] = visual
    return a


def L(lead, cards, acts, desc=None):
    d = dict(lead=lead, cards=cards, acts=acts)
    if desc: d['desc'] = desc
    return d


# ---------- visuals (inline SVG, colours come from style-lesson.css) ----------
ARROW = '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="rgba(255,255,255,0.75)"/></marker></defs>'


def svg(w, h, inner, label='diagram'):
    return f'<svg class="viz" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{ARROW}{inner}</svg>'


def box(x, y, w, h, text, sub='', cls='v-box', r=10):
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>'
    cy = y + h / 2 + (0 if not sub else -6)
    t += f'<text x="{x + w / 2}" y="{cy + 5}" text-anchor="middle" class="v-t">{text}</text>'
    if sub:
        t += f'<text x="{x + w / 2}" y="{cy + 22}" text-anchor="middle" class="v-s">{sub}</text>'
    return t


def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="v-arrow"/>'


def marker(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="11" class="v-mk"/><text x="{x}" y="{y + 4}" text-anchor="middle" class="v-mkt">{n}</text>'


def flow(steps, w=420, cls_cycle=('v-box', 'v-box2', 'v-box3')):
    """Horizontal flow of boxes with arrows (wraps to 2 rows if more than 3)."""
    n = len(steps)
    bw, bh, gap = 112, 56, 28
    per = min(n, 3)
    rows = (n + per - 1) // per
    width = per * bw + (per - 1) * gap + 20
    out = ''
    for i, s in enumerate(steps):
        r, c = divmod(i, per)
        if r % 2: c = per - 1 - c          # snake layout
        x, y = 10 + c * (bw + gap), 10 + r * (bh + 34)
        t, sub = (s if isinstance(s, tuple) else (s, ''))
        out += box(x, y, bw, bh, t, sub, cls_cycle[i % 3])
        if i + 1 < n:
            r2, c2 = divmod(i + 1, per)
            if r2 % 2: c2 = per - 1 - c2
            x2, y2 = 10 + c2 * (bw + gap), 10 + r2 * (bh + 34)
            if r2 == r:
                out += arrow(x + bw if c2 > c else x, y + bh / 2, x2 if c2 > c else x2 + bw, y2 + bh / 2)
            else:
                out += arrow(x + bw / 2, y + bh, x2 + bw / 2, y2)
    return svg(width, rows * (bh + 34) - 14, out)
