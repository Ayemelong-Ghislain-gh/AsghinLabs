"""
Prepare the folder that is published at https://papers.asghinlabs.com (GitHub repo
"asghinlabs-papers" → Cloudflare Pages).

  python lessons-src/tools/publish_papers.py <images folder> <publish folder>

Copies only the image folders listed in data/paper-files.json (duplicates are skipped),
adds t.webp (a small picture of the top of page 1, used on the subject pages) to each,
and writes _headers (lets asghinlabs.com/tutor read the pages, long browser cache),
index.html and robots.txt.
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'lessons-src' / 'data'

HEADERS = """/*
  Access-Control-Allow-Origin: *
  Cache-Control: public, max-age=2592000
"""
INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AsghinLabs Academy past papers</title><meta http-equiv="refresh" content="0; url=https://www.asghinlabs.com/past-papers">
<link rel="canonical" href="https://www.asghinlabs.com/past-papers"></head>
<body><p>The past papers are on <a href="https://www.asghinlabs.com/past-papers">www.asghinlabs.com/past-papers</a>.</p></body></html>
"""


def thumb(page1, out):
    im = Image.open(page1).convert('L')
    top = im.crop((0, 0, im.width, round(im.width * 0.4)))
    top.resize((400, 160), Image.LANCZOS).save(out, 'WEBP', quality=50, method=4)


def main(images, publish):
    images, publish = Path(images), Path(publish)
    papers = json.loads((DATA / 'paper-files.json').read_text(encoding='utf-8'))
    dirs = sorted({e['dir']: len(e['pages']) for e in papers}.items())
    publish.mkdir(parents=True, exist_ok=True)
    files = total = 0
    for d, n in dirs:
        src, dst = images / d, publish / d
        dst.mkdir(parents=True, exist_ok=True)
        for i in range(1, n + 1):
            f = f'p{i}.webp'
            if not (dst / f).exists() or (dst / f).stat().st_size != (src / f).stat().st_size:
                shutil.copy2(src / f, dst / f)
            total += (dst / f).stat().st_size; files += 1
        if not (dst / 't.webp').exists():
            thumb(src / 'p1.webp', dst / 't.webp')
        total += (dst / 't.webp').stat().st_size; files += 1
    (publish / '_headers').write_text(HEADERS)
    (publish / 'index.html').write_text(INDEX)
    (publish / 'robots.txt').write_text('User-agent: *\nAllow: /\n')
    print(f'{len(dirs)} papers · {files} files · {total // (1024 * 1024)} MB in {publish}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
