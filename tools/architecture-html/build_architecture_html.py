"""Render architecture.md to a self-contained HTML page.

Usage: python build_architecture_html.py <architecture.md> <architecture.html>

The Markdown is the only source. The page carries the same headings, paragraphs, list items, table cells
and diagram text as the Markdown; check that with check_html_parity.py after every build.

Supported in the Markdown: # to #### headings, paragraphs, bullet and numbered lists (one nested level),
tables, `code`, **bold**, *italic*, [links](url), block quotes, and these fenced mermaid diagrams:
  sequenceDiagram  participant/alias, ->>, -->>, alt/else/end, Note over
  classDiagram     class blocks with <<stereotype>> and members, `A --> B : label`, `%% place Name col row`
  flowchart        marked `%% diagram: module`: an outer subgraph holding one subgraph per kind of type,
                   each with an optional `%% columns: N` line and one box per type
A section with two or more ### headings is drawn as tabs. Every layout rule is checked in code, and the
build stops with an assertion when a box overlaps, an arrow crosses a box, or a label touches an arrow.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'

if len(sys.argv) != 3:
    sys.exit(__doc__)
md_path, out_path = sys.argv[1:3]
css = open(os.path.join(HERE, 'theme.css'), encoding='utf-8').read()
fonts = FONTS

EXTRA_CSS = """
  .doc-meta{ margin-top: 16px; font-size: 14px; color: var(--ink-soft); }
  .doc-meta p{ margin: 3px 0; }
  .doc-meta strong{ color: var(--ink); font-family: "IBM Plex Mono", ui-monospace, monospace; font-weight: 600; }
  figure.diagram-fig{ margin: 14px 0 22px; }
  figure.diagram-fig figcaption{ color: var(--ink-soft); font-size: 13px; margin-top: 8px; }
  svg.diagram-svg{ width: 100%; height: auto; max-width: 1040px; display: block; font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 11px; }
  .dg-group{ fill: var(--schematic); stroke: var(--line); stroke-width: 1; }
  .dg-box{ fill: var(--panel); stroke: var(--line); stroke-width: 1; }
  .dg-root{ stroke: var(--accent); stroke-dasharray: 5 4; }
  .dg-h{ fill: var(--accent-ink); font-weight: 600; font-size: 12px; }
  .dg-t{ fill: var(--ink); }
  .dg-g{ fill: var(--ink-soft); font-size: 12px; letter-spacing: 0.02em; }
  .dg-l{ fill: var(--ink-soft); font-size: 11px; }
  .dg-edge{ stroke: var(--accent); stroke-width: 1.5; fill: none; }
  .dg-dash{ stroke-dasharray: 6 4; }
  .dg-head{ fill: var(--accent); }
  .dg-life{ stroke: var(--line); stroke-width: 1; stroke-dasharray: 4 4; }
  .dg-note{ fill: var(--accent-soft); stroke: var(--accent); stroke-width: 1; }
  .dg-frame{ fill: none; stroke: var(--accent); stroke-width: 1; }
  .dg-frame-line{ stroke: var(--accent); stroke-width: 1; stroke-dasharray: 5 4; }
  .dg-tag{ fill: var(--accent-ink); font-weight: 600; font-size: 11px; }
  pre.diagram{ background: var(--schematic); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; overflow-x: auto; font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 12.5px; line-height: 1.5; color: var(--ink); margin: 14px 0 22px; }
  pre.diagram code{ background: transparent; border: 0; padding: 0; font-size: inherit; }
  section h3{ margin: 22px 0 8px; }
  section h4{ margin: 20px 0 6px; font-size: 15px; }
  /* main entries: dark and medium weight. Tab entries: smaller, lighter, indented under a connector line */
  nav.toc > ol > li > a{ color: var(--ink); font-weight: 500; transition: color .12s; }
  nav.toc > ol > li.is-active > a{ color: var(--accent-ink); border-left-color: var(--accent); font-weight: 700; }
  nav.toc .toc-sub{ display: none; list-style: none; margin: 0 0 8px 46px; padding: 0; border-left: 1px solid var(--line); }
  nav.toc li.is-active > .toc-sub{ display: block; }
  nav.toc .toc-sub a{ display: block; padding: 4px 0 4px 12px; margin-left: -1px; font-size: 12px; font-weight: 400; color: var(--ink-soft); border-left: 2px solid transparent; }
  nav.toc .toc-sub a:hover{ color: var(--ink); border-left-color: var(--line); }
  nav.toc .toc-sub a[aria-current="true"]{ color: var(--accent-ink); border-left-color: var(--accent); font-weight: 600; }
  html.js section.is-off{ display: none; }
  @media print{ html.js section.is-off{ display: block; } }
  html.js .tabs > .panel > h3:first-child{ display: none; }   /* the tab already names the panel */
  html.js .tabs.sub > .panel > h4:first-child{ display: none; }
  section p, section ul, section ol{ max-width: 88ch; }
"""


CHAR_W = 6.7  # estimated advance of the 11px monospace face, used only to keep text inside boxes

DIAG_COUNT = [0]   # numbers the SVG marker ids so they stay unique in the page


def parse_class_diagram(code):
    """Returns (classes, places, relations). classes: name -> (stereotype or None, [members])."""
    classes, places, rels, cur = {}, {}, [], None
    for ln in code:
        t = ln.strip()
        if not t or t == 'classDiagram':
            continue
        mm = re.match(r'%% place (\w+) (\d+) (\d+)$', t)
        if mm:
            places[mm.group(1)] = (int(mm.group(2)), int(mm.group(3)))
            continue
        if t.startswith('%%'):
            continue
        mm = re.match(r'class (\w+) \{$', t)
        if mm:
            cur = mm.group(1)
            classes[cur] = [None, []]
            continue
        if t == '}':
            cur = None
            continue
        if cur is not None:
            mm = re.match(r'<<(\w+)>>$', t)
            if mm:
                classes[cur][0] = mm.group(1)
            else:
                classes[cur][1].append(t)
            continue
        mm = re.match(r'(\w+) --> (\w+) : (.+)$', t)
        assert mm, ('unsupported class diagram line', t)
        rels.append((mm.group(1), mm.group(2), mm.group(3)))
    return classes, places, rels


def svg_class(code):
    """Class diagram: a UML box per class (name, stereotype, members) on a grid, with arrows for relations.
    Layout is checked in code: no overlaps, arrows never cross a box, labels never sit on a box or an arrow."""
    classes, places, rels = parse_class_diagram(code)
    assert set(places) == set(classes), ('every class needs a place', set(classes) ^ set(places))
    GX, GY, M = 90, 56, 20
    size = {}
    for n, (st, mem) in classes.items():
        w = max([len(n) * 7.6, len('«%s»' % st) * CHAR_W if st else 0] + [len(x) * CHAR_W for x in mem]) + 28
        w = max(w, 130)
        hh = 28 + (18 if st else 0)
        h = hh + (10 + 18 * len(mem) + 4 if mem else 8)
        size[n] = (w, h, hh)
    ncol = max(c for c, _ in places.values()) + 1
    nrow = max(r for _, r in places.values()) + 1
    colw = [max([size[n][0] for n in classes if places[n][0] == c] or [0]) for c in range(ncol)]
    rowh = [max([size[n][1] for n in classes if places[n][1] == r] or [0]) for r in range(nrow)]
    GX = max(GX, (1040 - 2 * M - sum(colw)) / max(ncol - 1, 1))   # same canvas width for every class diagram
    colx = [M + sum(colw[:c]) + GX * c for c in range(ncol)]
    rowy = [M + sum(rowh[:r]) + GY * r for r in range(nrow)]
    W = int(M * 2 + sum(colw) + GX * (ncol - 1))
    H = int(M * 2 + sum(rowh) + GY * (nrow - 1))
    rect, out = {}, []
    for n, (st, mem) in classes.items():
        c, r = places[n]
        w, h, hh = size[n]
        x = colx[c] + (colw[c] - w) / 2
        y = rowy[r] + (rowh[r] - h) / 2
        rect[n] = (x, y, w, h)
        out.append(f'<rect class="dg-box" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8"/>')
        out.append(f'<text class="dg-h" x="{x + w / 2:.1f}" y="{y + 20:.1f}" text-anchor="middle">{html.escape(n)}</text>')
        if st:
            out.append(f'<text class="dg-t" x="{x + w / 2:.1f}" y="{y + 38:.1f}" text-anchor="middle">{html.escape(chr(171) + st + chr(187))}</text>')
        if mem:
            out.append(f'<line class="dg-edge" x1="{x:.1f}" y1="{y + hh:.1f}" x2="{x + w:.1f}" y2="{y + hh:.1f}"/>')
            for k, tx in enumerate(mem):
                out.append(f'<text class="dg-t" x="{x + 12:.1f}" y="{y + hh + 22 + 18 * k:.1f}">{html.escape(tx)}</text>')

    def clip(n, tx, ty):
        """Point where the line from the centre of box n towards (tx, ty) leaves the box."""
        x, y, w, h = rect[n]
        cx, cy = x + w / 2, y + h / 2
        dx, dy = tx - cx, ty - cy
        s = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
        return cx + dx * s, cy + dy * s

    def centre(n):
        x, y, w, h = rect[n]
        return x + w / 2, y + h / 2

    segs, labels = [], []
    for a, b, lab in rels:
        assert a in classes and b in classes, ('relation names an unknown class', a, b)
        p0 = clip(a, *centre(b))
        p1 = clip(b, *centre(a))
        segs.append((a, b, p0, p1))
    boxes = list(rect.items())

    def hit(p0, p1, box, pad=3):
        x, y, w, h = box
        for k in range(301):
            t = k / 300
            px, py = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
            if x - pad < px < x + w + pad and y - pad < py < y + h + pad:
                return True
        return False

    for i, (n, bx) in enumerate(boxes):
        for n2, b2 in boxes[i + 1:]:
            assert not (bx[0] < b2[0] + b2[2] and b2[0] < bx[0] + bx[2] and bx[1] < b2[1] + b2[3] and b2[1] < bx[1] + bx[3]), ('boxes overlap', n, n2)
    for a, b, p0, p1 in segs:
        for n, bx in boxes:
            if n in (a, b):
                continue
            assert not hit(p0, p1, bx), ('arrow crosses a box', a, b, n)
    placed = []
    for a, b, p0, p1 in segs:
        lab = [r[2] for r in rels if r[0] == a and r[1] == b][0]
        tw = len(lab) * 6.7
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        for dx, dy in ((-tw / 2, -8), (-tw / 2, 18), (8, -8), (-tw - 8, -8), (8, 18), (-tw - 8, 18)):
            lx, ly = mx + dx, my + dy
            bb = (lx, ly - 11, lx + tw, ly + 3)
            bad = any(bb[0] < x + w and x < bb[2] and bb[1] < y + h and y < bb[3] for _, (x, y, w, h) in boxes)
            bad = bad or any(hit(q0, q1, (bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]), pad=0) for _, _, q0, q1 in segs)
            bad = bad or any(bb[0] < o[2] and o[0] < bb[2] and bb[1] < o[3] and o[1] < bb[3] for o in placed)
            if not bad:
                break
        else:
            raise AssertionError(('no free place for the label', lab))
        placed.append(bb)
        out.append(f'<polyline class="dg-edge" points="{p0[0]:.1f},{p0[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}" marker-end="url(#dg-arrow)"/>')
        out.append(f'<text class="dg-l" x="{lx:.1f}" y="{ly:.1f}">{html.escape(lab)}</text>')
    names = ', '.join(classes)
    return _fig(W, H, ''.join(out), 'Class diagram: ' + names, 'Each class with its members. Arrows show which class refers to which.')


def svg_module(code):
    """One module as its own figure: an outer group (the module) holding one inner group per kind of type
    (<module>/<kind>/), each holding a box per type. Layout is checked in code."""
    outer, inner, cur = None, [], None
    for ln in code:
        t = ln.strip()
        mm = re.match(r'subgraph \w+\["([^"]+)"\]', t)
        if mm:
            if outer is None:
                outer = mm.group(1)
            else:
                cur = {'label': mm.group(1), 'cols': 1, 'items': []}
                inner.append(cur)
            continue
        mm = re.match(r'%% columns: (\d+)', t)
        if mm and cur is not None:
            cur['cols'] = int(mm.group(1))
            continue
        mm = re.match(r'\w+\["([^"]+)"\]$', t)
        if mm and cur is not None:
            parts = mm.group(1).split('<br/>')
            cur['items'].append((parts[0], parts[1:]))
    assert outer and inner and all(g['items'] for g in inner), 'module diagram needs an outer module and kinds with types'
    W, GAP, TOP = 1040, 16, 40
    OX, OY, IPAD = 30, 16, 16
    OW = W - 60
    IW = OW - 2 * IPAD
    out, boxes, groups = [], [], []
    y = OY + TOP
    for g in inner:
        cols = g['cols']
        colw = (IW - 2 * IPAD - (cols - 1) * GAP) / cols
        gy = y
        y += TOP - 8
        for r0 in range(0, len(g['items']), cols):
            row = g['items'][r0:r0 + cols]
            h = max(40, max(22 + 18 * len(ls) + 14 if ls else 40 for _, ls in row))
            for k, (title, ls) in enumerate(row):
                x = OX + IPAD + IPAD + k * (colw + GAP)
                for tx in [title] + ls:
                    assert len(tx) * CHAR_W <= colw - 16, (title, tx)
                boxes.append((x, y, colw, h))
                out.append(f'<rect class="dg-box" x="{x}" y="{y}" width="{colw}" height="{h}" rx="8"/>')
                if ls:
                    out.append(f'<text class="dg-h" x="{x + colw / 2}" y="{y + 22}" text-anchor="middle">{html.escape(title)}</text>')
                    for j, tx in enumerate(ls):
                        out.append(f'<text class="dg-t" x="{x + colw / 2}" y="{y + 22 + 18 * (j + 1)}" text-anchor="middle">{html.escape(tx)}</text>')
                else:
                    out.append(f'<text class="dg-h" x="{x + colw / 2}" y="{y + h / 2 + 4}" text-anchor="middle">{html.escape(title)}</text>')
            y += h + GAP
        gh = y - GAP + IPAD - gy
        groups.append((OX + IPAD, gy, IW, gh, g['label']))
        y = gy + gh + GAP
    OH = y - GAP + IPAD - OY
    H = OY + OH + 16
    for (gx, gy, gw, gh, _) in groups:
        assert gx >= OX and gy >= OY and gx + gw <= OX + OW and gy + gh <= OY + OH, 'kind outside its module'
    for i, a in enumerate(groups):
        for b in groups[i + 1:]:
            assert not (a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]), 'kinds overlap'
    for i, a in enumerate(boxes):
        assert any(a[0] >= g[0] and a[1] >= g[1] and a[0] + a[2] <= g[0] + g[2] and a[1] + a[3] <= g[1] + g[3] for g in groups), 'box outside its kind'
        for b in boxes[i + 1:]:
            assert not (a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]), 'boxes overlap'
    body = (f'<rect class="dg-group" x="{OX}" y="{OY}" width="{OW}" height="{OH}" rx="12"/>'
            f'<text class="dg-g" x="{OX + 16}" y="{OY + 22}">{html.escape(outer)}</text>')
    for (gx, gy, gw, gh, lb) in groups:
        body += (f'<rect class="dg-group" x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10"/>'
                 f'<text class="dg-g" x="{gx + 16}" y="{gy + 22}">{html.escape(lb)}</text>')
    names = '; '.join(g['label'] + ': ' + ', '.join(t for t, _ in g['items']) for g in inner)
    return _fig(W, H, body + ''.join(out), f'Module {outer}: {names}', f'The module {outer}, its kinds of type, and every type in each.')


def _defs():
    return ('<defs><marker id="dg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path class="dg-head" d="M0,0 L10,5 L0,10 z"/></marker></defs>')


def _fig(W, H, body, aria, caption):
    return (f'<figure class="diagram-fig"><svg class="diagram-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(aria)}">'
            f'{_defs()}{body}</svg><figcaption>{html.escape(caption)}</figcaption></figure>')


def svg_sequence(code):
    """A sequence diagram drawn from a small Mermaid subset. Every layout rule is checked in code."""
    parts, events = [], []
    for raw in code[1:]:
        t = raw.strip()
        if not t or t.startswith('%%'):
            continue
        m = re.match(r'participant (\w+) as (.+)$', t)
        if m:
            parts.append([m.group(1), m.group(2)])
            continue
        m = re.match(r'(\w+)(-->>|->>)(\w+): (.+)$', t)
        if m:
            events.append(('msg', m.group(1), m.group(3), m.group(4), m.group(2) == '-->>'))
            continue
        m = re.match(r'alt (.+)$', t)
        if m:
            events.append(('alt', m.group(1)))
            continue
        m = re.match(r'else (.+)$', t)
        if m:
            events.append(('else', m.group(1)))
            continue
        if t == 'end':
            events.append(('end',))
            continue
        m = re.match(r'Note over (\w+): (.+)$', t)
        if m:
            events.append(('note', m.group(1), m.group(2)))
            continue
        raise AssertionError(('unsupported sequence line', t))
    ids = [p[0] for p in parts]
    idx = {p: i for i, p in enumerate(ids)}
    n = len(parts)
    HW = [max(110, len(p[1]) * 7.3 + 28) for p in parts]
    need = [(HW[k] + HW[k + 1]) / 2 + 30 for k in range(n - 1)]
    for ev in events:
        if ev[0] == 'msg':
            i, j = sorted((idx[ev[1]], idx[ev[2]]))
            assert j == i + 1, ('non-adjacent message', ev)
            need[i] = max(need[i], len(ev[3]) * 6.7 + 44)
    # a note over the first or last participant must stay inside the alt frame, which starts 20 px from each edge
    NOTE_INSET = 34
    LM = RM = 40
    for ev in events:
        if ev[0] == 'note':
            half = (len(ev[2]) * 6.7 + 24) / 2
            k = idx[ev[1]]
            if k == 0:
                LM = max(LM, NOTE_INSET + half - HW[0] / 2)
            if k == n - 1:
                RM = max(RM, NOTE_INSET + half - HW[-1] / 2)
    cx = [LM + HW[0] / 2]
    for k in range(n - 1):
        cx.append(cx[-1] + need[k])
    W = round(cx[-1] + HW[-1] / 2 + RM)
    assert W <= 1040, ('sequence diagram too wide', W)
    X0, X1 = 20, W - 20

    front, back = [], []
    labels = []          # (text, x0, y0, x1, y1) for the overlap check
    borders = []         # y of every horizontal frame border
    note_boxes = []      # (x0, y0, x1, y1) of every note, so no label can sit on one
    y = 92
    depth, frame_top = 0, None
    for ev in events:
        kind = ev[0]
        if kind == 'msg':
            f, t = idx[ev[1]], idx[ev[2]]
            x1, x2 = cx[f], cx[t]
            span = abs(x2 - x1)
            tw = len(ev[3]) * 6.7
            assert tw + 30 <= span, ('message label wider than its span', ev[3], tw, span)
            cls = 'dg-edge dg-dash' if ev[4] else 'dg-edge'
            front.append(f'<line class="{cls}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-end="url(#dg-arrow)"/>')
            lx = (x1 + x2) / 2
            front.append(f'<text class="dg-l" x="{lx}" y="{y - 8}" text-anchor="middle">{html.escape(ev[3])}</text>')
            labels.append((ev[3], lx - tw / 2, y - 18, lx + tw / 2, y - 5))
            y += 40
        elif kind == 'note':
            k = idx[ev[1]]
            w = len(ev[2]) * 6.7 + 24
            neighbours = [abs(cx[k] - cx[j]) for j in (k - 1, k + 1) if 0 <= j < n]
            assert w / 2 + 8 <= min(neighbours), ('note wider than its column', ev[2], w, neighbours)
            assert cx[k] - w / 2 >= X0 + 8 and cx[k] + w / 2 <= X1 - 8, ('note sticks out of the frame', ev[2])
            front.append(f'<rect class="dg-note" x="{cx[k] - w / 2}" y="{y}" width="{w}" height="28" rx="6"/>')
            note_boxes.append((cx[k] - w / 2, y, cx[k] + w / 2, y + 28))
            front.append(f'<text class="dg-t" x="{cx[k]}" y="{y + 18}" text-anchor="middle">{html.escape(ev[2])}</text>')
            y += 54   # room for the next message label below the note
        elif kind == 'alt':
            assert depth == 0, 'nested alt is not supported'
            depth, frame_top = 1, y - 14
            borders.append(frame_top)
            tw = len(ev[1]) * 6.7
            assert X0 + 44 + tw <= X1, ('alt label too wide', ev[1])
            front.append(f'<text class="dg-tag" x="{X0 + 10}" y="{frame_top + 17}">alt</text>')
            front.append(f'<text class="dg-l" x="{X0 + 44}" y="{frame_top + 17}">{html.escape(ev[1])}</text>')
            y += 28
        elif kind == 'else':
            assert depth == 1
            ly = y - 10
            borders.append(ly)
            front.append(f'<line class="dg-frame-line" x1="{X0}" y1="{ly}" x2="{X1}" y2="{ly}"/>')
            tw = len(ev[1]) * 6.7
            assert X0 + 52 + tw <= X1, ('else label too wide', ev[1])
            front.append(f'<text class="dg-tag" x="{X0 + 10}" y="{ly + 17}">else</text>')
            front.append(f'<text class="dg-l" x="{X0 + 52}" y="{ly + 17}">{html.escape(ev[1])}</text>')
            y += 28
        elif kind == 'end':
            assert depth == 1
            back.append(f'<rect class="dg-frame" x="{X0}" y="{frame_top}" width="{X1 - X0}" height="{y - 6 - frame_top}" rx="6"/>')
            borders.append(y - 6)
            depth = 0
            y += 28   # room for the next message label below the frame border
    assert depth == 0, 'unclosed alt'
    for (txt, lx0, ly0, lx1, ly1) in labels:
        for (nx0, ny0, nx1, ny1) in note_boxes:
            assert not (lx0 < nx1 and nx0 < lx1 and ly0 < ny1 and ny0 < ly1), ('a message label touches a note', txt)
        for by in borders:
            assert not (ly0 - 1 < by < ly1 + 1), ('a message label touches a frame border', txt, by)
    H = round(y + 16)

    head = []
    for k, (pid, label) in enumerate(parts):
        w = HW[k]
        head.append(f'<line class="dg-life" x1="{cx[k]}" y1="52" x2="{cx[k]}" y2="{H - 10}"/>')
        head.append(f'<rect class="dg-box" x="{cx[k] - w / 2}" y="16" width="{w}" height="36" rx="8"/>')
        head.append(f'<text class="dg-h" x="{cx[k]}" y="39" text-anchor="middle">{html.escape(label)}</text>')
    for i in range(n - 1):
        assert cx[i] + HW[i] / 2 + 8 <= cx[i + 1] - HW[i + 1] / 2, ('participant headers overlap', parts[i][1], parts[i + 1][1])
    return _fig(W, H, ''.join(head + back + front),
                'Sequence diagram: ' + '; '.join(p[1] for p in parts),
                'Participants across the top, time running down. Solid arrows are calls, dashed arrows are replies.')


def pick_diagram(code):
    DIAG_COUNT[0] += 1
    first = code[0].strip() if code else ''
    if first == 'sequenceDiagram':
        svg = svg_sequence(code)
    elif first == 'classDiagram':
        svg = svg_class(code)
    elif any('%% diagram: module' in l for l in code):
        svg = svg_module(code)
    else:
        raise AssertionError(('unknown diagram', first))
    # every SVG carries its own marker id, so ids stay unique in the page
    return svg.replace('dg-arrow', 'dg-arrow-%d' % DIAG_COUNT[0])


USED_IDS = set()


def unique_id(s):
    """An HTML id from a heading, made unique when several sections repeat a heading such as 'Error flow'."""
    base = slug(s)
    n, cand = 2, base
    while cand in USED_IDS:
        cand = '%s-%d' % (base, n)
        n += 1
    USED_IDS.add(cand)
    return cand


def slug(s):
    s = re.sub(r'`', '', s.lower())
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


def inline(text):
    stash = []

    def keep(mo):
        stash.append('<code>' + html.escape(mo.group(1)) + '</code>')
        return '\x00%d\x00' % (len(stash) - 1)

    t = re.sub(r'`([^`]+)`', keep, text)
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda mo: '<a href="%s">%s</a>' % (mo.group(2), mo.group(1)), t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])', r'<em>\1</em>', t)
    return re.sub(r'\x00(\d+)\x00', lambda mo: stash[int(mo.group(1))], t)


lines = open(md_path, encoding='utf-8').read().replace('\r\n', '\n').split('\n')

sections = []          # (id, title, html_body)
cur = None
h1 = None
body = []


def flush_para(buf):
    if buf:
        if len(buf) > 1 and all(x.startswith('**') for x in buf):
            for x in buf:
                body.append('<p>' + inline(x.strip()) + '</p>')
        else:
            body.append('<p>' + inline(' '.join(x.strip() for x in buf)) + '</p>')
    buf.clear()


preamble = []   # paragraphs before the first ## heading: Audience, Status, Format, FR


section_tabs = {}   # section id -> [(panel id, tab title)]


SUBTAB_SECTIONS = {'data-flow'}   # sections whose #### parts become sub-tabs inside each tab


def plain_chunk(c):
    """A chunk as HTML when it is not being turned into a tab: headings stay headings."""
    if not isinstance(c, tuple):
        return c
    if c[0] == 'H3':
        return '<h3 id="%s">%s</h3>' % (unique_id(c[1]), inline(c[1]))
    return '<h4 id="%s">%s</h4>' % (unique_id(c[1]), inline(c[1]))


def render_parts(chunks, base, subtabs):
    """The chunks of one panel. Its #### parts become sub-tabs when asked and there are two or more."""
    marks = [k for k, c in enumerate(chunks) if isinstance(c, tuple) and c[0] == 'H4']
    if not subtabs or len(marks) < 2:
        return '\n'.join(plain_chunk(c) for c in chunks)
    lead = [plain_chunk(c) for c in chunks[:marks[0]]]
    tabs, panels = [], []
    for n, k in enumerate(marks):
        end = marks[n + 1] if n + 1 < len(marks) else len(chunks)
        title = chunks[k][1]
        pid = slug(base + '-' + title)
        tabs.append('<button type="button" role="tab" id="tab-%s" aria-controls="%s" aria-selected="%s" tabindex="%s">%s</button>'
                    % (pid, pid, 'true' if n == 0 else 'false', '0' if n == 0 else '-1', inline(title)))
        panels.append('<div class="panel" role="tabpanel" id="%s" aria-labelledby="tab-%s">\n<h4>%s</h4>\n%s\n</div>'
                      % (pid, pid, inline(title), '\n'.join(plain_chunk(c) for c in chunks[k + 1:end])))
    return '\n'.join(lead + ['<div class="tabs sub" data-tabs>', '<div class="tablist" role="tablist" aria-label="%s">' % html.escape(base) + ''.join(tabs) + '</div>'] + panels + ['</div>'])


def render_body(sid, chunks):
    """A section with two or more ### parts becomes tabs (one panel per part); otherwise the parts stay in order."""
    marks = [k for k, c in enumerate(chunks) if isinstance(c, tuple) and c[0] == 'H3']
    subtabs = sid in SUBTAB_SECTIONS
    if len(marks) < 2:
        return render_parts(chunks, sid, False)
    lead = [render_parts(chunks[:marks[0]], sid, False)] if marks[0] else []
    tabs, panels = [], []
    section_tabs[sid] = []
    for n, k in enumerate(marks):
        end = marks[n + 1] if n + 1 < len(marks) else len(chunks)
        title = chunks[k][1]
        pid = slug(sid + '-' + title)
        section_tabs[sid].append((pid, title))
        tabs.append('<button type="button" role="tab" id="tab-%s" aria-controls="%s" aria-selected="%s" tabindex="%s">%s</button>'
                    % (pid, pid, 'true' if n == 0 else 'false', '0' if n == 0 else '-1', inline(title)))
        panels.append('<div class="panel" role="tabpanel" id="%s" aria-labelledby="tab-%s">\n<h3>%s</h3>\n%s\n</div>'
                      % (pid, pid, inline(title), render_parts(chunks[k + 1:end], pid, subtabs)))
    return '\n'.join(lead + ['<div class="tabs" data-tabs>', '<div class="tablist" role="tablist" aria-label="%s">' % html.escape(sid) + ''.join(tabs) + '</div>'] + panels + ['</div>'])


def close_section():
    global cur, body
    if cur is not None:
        sections.append((cur[0], cur[1], render_body(cur[0], body)))
    else:
        preamble.extend(body)
    body = []


i = 0
para = []
while i < len(lines):
    ln = lines[i]
    if ln.startswith('```'):
        flush_para(para)
        info = ln[3:].strip()
        i += 1
        code = []
        while i < len(lines) and not lines[i].startswith('```'):
            code.append(lines[i])
            i += 1
        i += 1
        if info == 'mermaid':
            body.append(pick_diagram(code))
        else:
            body.append('<pre class="diagram"><code>' + html.escape('\n'.join(code)) + '</code></pre>')
        continue
    if ln.startswith('# '):
        flush_para(para)
        h1 = ln[2:].strip()
        i += 1
        continue
    if ln.startswith('## '):
        flush_para(para)
        close_section()
        t = ln[3:].strip()
        cur = (slug(t), t)
        i += 1
        continue
    if ln.startswith('#### '):
        flush_para(para)
        t = ln[5:].strip()
        body.append(('H4', t))
        i += 1
        continue
    if ln.startswith('### '):
        flush_para(para)
        body.append(('H3', ln[4:].strip()))
        i += 1
        continue
    if ln.startswith('|'):
        flush_para(para)
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            rows.append(lines[i])
            i += 1
        cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
        head, data = cells[0], [r for r in cells[2:]]
        th = ''.join('<th>%s</th>' % inline(c) for c in head)
        tr = '\n'.join('    <tr>' + ''.join('<td>%s</td>' % inline(c) for c in r) + '</tr>' for r in data)
        body.append('<div class="table-wrap">\n<table>\n  <thead><tr>%s</tr></thead>\n  <tbody>\n%s\n  </tbody>\n</table>\n</div>' % (th, tr))
        continue
    if re.match(r'^(- |\d+\. )', ln):
        flush_para(para)
        ordered = bool(re.match(r'^\d+\. ', ln))
        items = []
        while i < len(lines) and re.match(r'^(- |\d+\. |  - |  +\S)', lines[i]):
            L = lines[i]
            if re.match(r'^(- |\d+\. )', L):
                items.append([re.sub(r'^(- |\d+\. )', '', L), []])
            elif L.startswith('  - '):
                items[-1][1].append(L[4:])
            elif items[-1][1]:
                items[-1][1][-1] += ' ' + L.strip()
            else:
                items[-1][0] += ' ' + L.strip()
            i += 1
        tag = 'ol' if ordered else 'ul'
        def li(it):
            sub = ''
            if it[1]:
                sub = '<ul>' + ''.join('<li>%s</li>' % inline(x) for x in it[1]) + '</ul>'
            return '  <li>%s%s</li>' % (inline(it[0]), sub)
        nl = chr(10)
        body.append('<' + tag + '>' + nl + nl.join(li(x) for x in items) + nl + '</' + tag + '>')
        continue
    if ln.startswith('> '):
        flush_para(para)
        body.append('<p class="note">' + inline(ln[2:].strip()) + '</p>')
        i += 1
        continue
    if ln.strip() == '':
        flush_para(para)
        i += 1
        continue
    para.append(ln)
    i += 1
flush_para(para)
close_section()

TOC_FLAT = {'overview'}   # sections whose tabs are not repeated under their sidebar entry


def nav_item(sid, t):
    sub = ''
    if sid in section_tabs and sid not in TOC_FLAT:
        sub = '\n              <ol class="toc-sub">' + ''.join(
            '<li><a href="#%s" data-panel="%s">%s</a></li>' % (p, p, inline(tt)) for p, tt in section_tabs[sid]) + '</ol>\n            '
    return '            <li data-section="%s"><a href="#%s"><span class="tn"></span>%s</a>%s</li>' % (sid, sid, html.escape(t), sub)


nav = '\n'.join(nav_item(sid, t) for sid, t, _ in sections)
secs = '\n'.join('      <section id="%s">\n        <h2>%s</h2>\n%s\n      </section>' % (sid, html.escape(t), b) for sid, t, b in sections)

TAB_JS = '''<script>
(function () {
  document.documentElement.classList.add('js');
  function select(tab, focus) {
    var list = tab.parentNode;
    Array.prototype.forEach.call(list.querySelectorAll(':scope > [role="tab"]'), function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) { panel.hidden = !on; }
    });
    if (focus) { tab.focus(); }
  }
  function showHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id && document.getElementById(id);
    if (!el) { return; }
    var panel = el.closest('[role="tabpanel"]');
    var any = false;
    while (panel) {
      var tab = document.getElementById(panel.getAttribute('aria-labelledby'));
      if (tab) { select(tab, false); any = true; }
      panel = panel.parentElement && panel.parentElement.closest('[role="tabpanel"]');
    }
    if (any) { el.scrollIntoView(); }
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-tabs]'), function (root) {
    var list = root.querySelector(':scope > [role="tablist"]');
    var tabs = Array.prototype.slice.call(list.querySelectorAll(':scope > [role="tab"]'));
    select(tabs[0], false);
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t, true); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') { n = tabs[(i + 1) % tabs.length]; }
        else if (e.key === 'ArrowLeft') { n = tabs[(i - 1 + tabs.length) % tabs.length]; }
        else if (e.key === 'Home') { n = tabs[0]; }
        else if (e.key === 'End') { n = tabs[tabs.length - 1]; }
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('nav.toc a'), function (a) {
    a.addEventListener('click', function () { setTimeout(showHash, 0); });
  });
  window.addEventListener('hashchange', showHash);
  showHash();
})();
</script>'''

TOC_JS = '''<script>
(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('nav.toc > ol > li[data-section]'));
  if (!items.length) { return; }
  var sections = items.map(function (li) { return document.getElementById(li.getAttribute('data-section')); });
  // only the section selected in the sidebar is shown; without JavaScript every section shows
  function showSection(i) {
    items.forEach(function (li, k) { li.classList.toggle('is-active', k === i); });
    sections.forEach(function (s, k) { if (s) { s.classList.toggle('is-off', k !== i); } });
  }
  function syncTabs() {
    var selected = {};
    Array.prototype.forEach.call(document.querySelectorAll('[role="tab"][aria-selected="true"]'), function (t) {
      selected[t.getAttribute('aria-controls')] = true;
    });
    Array.prototype.forEach.call(document.querySelectorAll('nav.toc .toc-sub a'), function (a) {
      if (selected[a.getAttribute('data-panel')]) { a.setAttribute('aria-current', 'true'); } else { a.removeAttribute('aria-current'); }
    });
  }
  function fromHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id ? document.getElementById(id) : null;
    var section = el ? el.closest('section') : null;
    var i = section ? sections.indexOf(section) : -1;
    showSection(i < 0 ? 0 : i);
    syncTabs();
    if (el) { el.scrollIntoView(); }
  }
  window.addEventListener('hashchange', function () { setTimeout(fromHash, 0); });
  Array.prototype.forEach.call(document.querySelectorAll('[role="tab"]'), function (el) {
    el.addEventListener('click', function () { setTimeout(syncTabs, 0); });
  });
  fromHash();
})();
</script>'''

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(h1)}</title>
<style>{css}{EXTRA_CSS}</style>
{fonts}
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>{html.escape(h1)}</h1>
    <div class="doc-meta">{"".join(preamble)}</div>
  </header>

  <div class="shell">
    <nav class="toc">
          <p class="toc-label">On this page</p>
          <ol>
{nav}
          </ol>
        </nav>

    <main>
{secs}
    </main>
  </div>
</div>
{TAB_JS}
{TOC_JS}
</body>
</html>
"""
open(out_path, 'w', encoding='utf-8', newline='\n').write(page)
print('wrote', out_path, len(page), 'bytes;', len(sections), 'sections')
