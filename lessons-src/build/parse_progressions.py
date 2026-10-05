"""
Turn MINESEC harmonised progression PDFs into lessons-src/data/progressions.json

Usage (from the project root):
    pip install pdfplumber
    python lessons-src/build/parse_progressions.py "Form 2|Mathematics|path/to/progression.pdf" ["Class|Subject|file.pdf" ...]

New sheets are ADDED to progressions.json (an existing class + subject is replaced).
After running it, check the chapter and lesson titles in the JSON file, then run build.py.
"""
import json
import re
import sys
from pathlib import Path

import pdfplumber

DATA = Path(__file__).resolve().parents[1] / 'data' / 'progressions.json'


def parse(path):
    rows = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            # the big diagonal "OFFICIAL HARMONIZED PROGRESSION" watermark letters are > 15pt: drop them
            pg = pg.filter(lambda o: o.get('object_type') != 'char' or o.get('size', 0) < 15)
            for t in pg.extract_tables():
                for r in t:
                    if r and r[0] and re.match(r'^\d+$', r[0].strip()) and len(r) >= 4:
                        rows.append(r)
    chapters, cur = [], None
    for r in rows:
        chap = re.sub(r'\s+', ' ', (r[2] or '').replace('\n', ' ')).strip(' "')
        title = re.sub(r'\s+', ' ', (r[3] or '').replace('\n', ' ')).strip()
        if chap:
            chap = re.sub(r'^(\d+)\s*\.?\s*', '', chap).rstrip('.').strip()
            if chapters and chapters[-1]['chapter'].replace(" (cont')", '') == chap.replace(" (cont')", ''):
                cur = chapters[-1]
            else:
                cur = {'chapter': chap.replace(" (cont')", ''), 'lessons': []}
                chapters.append(cur)
        m = re.match(r'Lesson\s*(\d+)\s*[:.]?\s*(.*)', title, re.I)
        n, t = (int(m.group(1)), m.group(2).strip()) if m else (int(r[0]), title)
        t = t.rstrip('.').strip()
        t = t[:1].upper() + t[1:]
        cur['lessons'].append({'n': n, 'title': t, 'integration': bool(re.search(r'integration activit|contact with students', t, re.I))})
    return chapters


def main():
    data = json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else []
    for arg in sys.argv[1:]:
        cls, subj, path = arg.split('|')
        data = [p for p in data if not (p['class'] == cls and p['subject'] == subj)]
        data.append({'class': cls, 'subject': subj, 'chapters': parse(path)})
        print(f'{cls} {subj}: {sum(len(c["lessons"]) for c in data[-1]["chapters"])} lessons')
    DATA.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
