"""
Make lessons-src/data/paper-files.json: one entry per past-paper file, used by build_papers.py.

  python lessons-src/tools/index_papers.py <index.csv> <images folder>

  <index.csv>      "MINESEC Past Papers/index.csv" (made by the download script)
  <images folder>  the folder convert_papers.py wrote to (one folder per paper with pages.json),
                   the same folder that is published at https://papers.asghinlabs.com

Each entry: exam, year, subject, subject_slug, slug (the paper's MINESEC address),
pages (height of each page image, width is always 1000) and dir (image folder).
Papers whose PDF is byte-for-byte the same as another share one image folder.
"""
import csv, hashlib, json, os, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'lessons-src' / 'data'
EXAM = {'GCE O Level': 'gce-ordinary-level', 'GCE A Level': 'gce-advanced-level', 'BEPC': 'bepc', 'BEPC blanc': 'bepc-blanc',
        'Probatoire - examens blancs': 'probatoire-examen-blanc', 'Baccalaureat - examens blancs': 'baccalaureat-blanc',
        'TVEE Advanced - Commercial': 'tvee-al-commercial', 'TVEE Intermediate - Commercial': 'tvee-il-commercial',
        'TVEE Advanced - Industrial': 'tvee-al-industrial', 'TVEE Intermediate - Industrial': 'tvee-il-industrial',
        'TVEE Intermediate - Mock': 'mock-o-level-technical', 'TVEE Advanced - Mock': 'mock-a-level-technical', 'CAPIEMP': 'capiemp'}


def main(index_csv, images):
    index_csv, images = Path(index_csv), Path(images)
    pdf_root = index_csv.parent
    lib = json.loads((DATA / 'minesec-papers.json').read_text(encoding='utf-8'))
    slug_of = {(r['exam'], int(r['year']), r['subject']): r['slug'] for r in lib}
    seen, out, missing = {}, [], []
    for r in csv.DictReader(open(index_csv, encoding='utf-8-sig')):
        exam, year = EXAM[r['Exam']], int(r['Year'])
        ss = slug_of[(exam, year, r['Subject'])]
        folder = f"{exam}/{year}/{ss}/{r['Paper']}"
        pj = images / folder / 'pages.json'
        if not pj.exists():
            missing.append(folder); continue
        pdf = pdf_root / r['File'].replace('\\', '/')
        digest = hashlib.sha1(pdf.read_bytes()).hexdigest() if pdf.exists() else folder
        canonical = seen.setdefault(digest, folder)            # identical PDF → reuse the first copy's images
        names = json.loads(pj.read_text())['pages']
        heights = [Image.open(images / canonical / n).height for n in names]
        out.append(dict(exam=exam, year=year, subject=r['Subject'], subject_slug=ss, slug=r['Paper'],
                        source=r['Source'], dir=canonical, pages=heights))
    out.sort(key=lambda e: (e['exam'], -e['year'], e['subject_slug'], e['slug']))
    (DATA / 'paper-files.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    used = {e['dir'] for e in out}
    print(f'{len(out)} papers · {len(used)} image folders · {sum(len(e["pages"]) for e in out)} pages shown'
          + (f' · {len(missing)} not converted yet' if missing else ''))
    return used


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
