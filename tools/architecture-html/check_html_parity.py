"""Check that an HTML doc carries exactly the content of its Markdown source.

Compares, in order: headings, paragraphs, list items, table cells; and diagram text (Mermaid labels
against SVG <text>). Chrome that is derived from the headings (the sidebar table of contents) is ignored.
"""
import html as H
import re
import sys
from html.parser import HTMLParser

md_path, html_path = sys.argv[1], sys.argv[2]


def norm(s):
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)     # links -> text
    s = s.replace('`', '').replace('**', '')
    s = re.sub(r'(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])', r'\1', s)
    s = H.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


# ------------------------------------------------------------------ markdown side
def parse_md(text):
    lines = text.replace('\r\n', '\n').split('\n')
    heads, paras, items, cells, diagram = [], [], [], [], []
    i, para = 0, []

    def flush():
        if para:
            if len(para) > 1 and all(x.startswith('**') for x in para):
                paras.extend(norm(x) for x in para)
            else:
                paras.append(norm(' '.join(para)))
        para.clear()

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            flush()
            info = ln[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            if info == 'mermaid' and code and code[0].strip() == 'sequenceDiagram':
                for c in code[1:]:
                    t = c.strip()
                    for pat in (r'participant \w+ as (.+)$', r'\w+(?:-->>|->>)\w+: (.+)$', r'alt (.+)$', r'else (.+)$', r'Note over \w+: (.+)$'):
                        m = re.match(pat, t)
                        if m:
                            diagram.append(norm(m.group(1)))
                            break
            elif info == 'mermaid' and code and code[0].strip() == 'classDiagram':
                for c in code[1:]:
                    t = c.strip()
                    if not t or t.startswith('%%') or t == '}' or t.startswith('class '):
                        m2 = re.match(r'class (\w+) \{$', t)
                        if m2:
                            diagram.append(m2.group(1))
                        continue
                    m2 = re.match(r'<<(\w+)>>$', t)
                    if m2:
                        diagram.append('\u00ab' + m2.group(1) + '\u00bb')
                        continue
                    m2 = re.match(r'\w+ --> \w+ : (.+)$', t)
                    diagram.append(norm(m2.group(1)) if m2 else norm(t))
            elif info == 'mermaid':
                for c in code:
                    m = re.match(r'\s*subgraph \w+\["([^"]+)"\]', c)
                    if m:
                        diagram.append(norm(m.group(1)))
                        continue
                    for m in re.finditer(r'\["([^"]+)"\]', c):
                        diagram.extend(norm(x) for x in m.group(1).split('<br/>'))
                    for m in re.finditer(r'\|([^|]+)\|', c):
                        diagram.append(norm(m.group(1)))
                    m = re.match(r'\s*(\w+)\["', c)
            continue
        m = re.match(r'^(#{1,4}) (.*)', ln)
        if m:
            flush()
            heads.append((len(m.group(1)), norm(m.group(2))))
            i += 1
            continue
        if ln.startswith('|'):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i])
                i += 1
            for k, r in enumerate(rows):
                if k == 1:
                    continue
                cells.extend(norm(c) for c in r.strip().strip('|').split('|'))
            continue
        if re.match(r'^(- |\d+\. |  - |  +\S)', ln) and (re.match(r'^(- |\d+\. )', ln) or items):
            flush()
            while i < len(lines) and re.match(r'^(- |\d+\. |  - |  +\S)', lines[i]):
                L = lines[i]
                if re.match(r'^(- |\d+\. )', L):
                    items.append(re.sub(r'^(- |\d+\. )', '', L))
                elif L.startswith('  - '):
                    items.append(L[4:])
                else:
                    items[-1] += ' ' + L.strip()
                i += 1
            continue
        if ln.startswith('> '):
            flush()
            paras.append(norm(ln[2:]))
            i += 1
            continue
        if ln.strip() == '':
            flush()
            i += 1
            continue
        para.append(ln)
        i += 1
    flush()
    return heads, paras, [norm(x) for x in items], cells, diagram


# ------------------------------------------------------------------ html side
class HP(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.buf = [], None
        self.heads, self.paras, self.items, self.cells, self.diagram = [], [], [], [], []
        self.skip = 0
        self.in_svg = False
        self.li_stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.stack.append((tag, a))
        if tag in ('style', 'script', 'title'):
            self.skip += 1
        if tag == 'nav' and 'toc' in (a.get('class') or ''):
            self.skip += 1
        if tag == 'svg':
            self.in_svg = True
        if tag in ('h1', 'h2', 'h3', 'h4', 'p', 'td', 'th', 'text'):
            self.buf = []
            self.tag_text = tag == 'text' and 'dg-tag' in (a.get('class') or '')   # the 'alt' and 'else' keywords
        if tag == 'li' and not self.skip:
            self.li_stack.append([])
        if tag == 'ul' and self.li_stack and not self.skip:
            # text before a nested list belongs to the parent item
            self.items.append(''.join(self.li_stack[-1]))
            self.li_stack[-1] = None

    def handle_endtag(self, tag):
        if tag in ('style', 'script', 'title'):
            self.skip -= 1
        if tag == 'nav' and self.stack and 'toc' in (self.stack[-1][1].get('class') or ''):
            self.skip -= 1
        if tag == 'svg':
            self.in_svg = False
        if tag in ('h1', 'h2', 'h3', 'h4') and self.buf is not None and not self.skip:
            self.heads.append((int(tag[1]), norm(''.join(self.buf))))
            self.buf = None
        elif tag == 'p' and self.buf is not None and not self.skip:
            t = norm(''.join(self.buf))
            if t:
                self.paras.append(t)
            self.buf = None
        elif tag in ('td', 'th') and self.buf is not None and not self.skip:
            self.cells.append(norm(''.join(self.buf)))
            self.buf = None
        elif tag == 'text' and self.buf is not None:
            if not getattr(self, 'tag_text', False):
                self.diagram.append(norm(''.join(self.buf)))
            self.buf = None
        if tag == 'li' and self.li_stack and not self.skip:
            cur = self.li_stack.pop()
            if cur is not None:
                self.items.append(norm(''.join(cur)))
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.skip:
            return
        if self.buf is not None:
            self.buf.append(data)
        if self.li_stack and self.li_stack[-1] is not None and self.buf is None:
            self.li_stack[-1].append(data)

    def handle_entityref(self, name):
        self.handle_data(H.unescape('&%s;' % name))

    def handle_charref(self, name):
        self.handle_data(H.unescape('&#%s;' % name))


def parse_html(text):
    p = HP()
    p.convert_charrefs = True
    p.feed(text)
    return p.heads, p.paras, [norm(x) for x in p.items], p.cells, p.diagram


mh, mp, mi, mc, md_dia = parse_md(open(md_path, encoding='utf-8').read())
hh, hp, hi, hc, h_dia = parse_html(open(html_path, encoding='utf-8').read())


def compare(name, a, b, ordered=True):
    aa = a if ordered else sorted(a)
    bb = b if ordered else sorted(b)
    if aa == bb:
        print(f'  PASS {name}: {len(a)} identical')
        return True
    print(f'  FAIL {name}: markdown {len(a)}, html {len(b)}')
    only_a = [x for x in a if x not in b]
    only_b = [x for x in b if x not in a]
    for x in only_a[:6]:
        print('       only in markdown:', x[:110])
    for x in only_b[:6]:
        print('       only in html    :', x[:110])
    return False


print('parity of', html_path.split('/')[-1], 'against', md_path.split('/')[-1])
ok = all([
    compare('headings', mh, hh),
    compare('paragraphs', mp, hp),
    compare('list items', mi, hi),
    compare('table cells', mc, hc),
    compare('diagram text (mermaid vs svg)', md_dia, h_dia, ordered=False),
])
sys.exit(0 if ok else 1)
