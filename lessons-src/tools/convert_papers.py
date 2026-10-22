"""
Turn past-paper PDFs into light page images for the web (one WebP per page).

  python convert_papers.py <pdf> <out_dir>          one paper
  python convert_papers.py --batch <list.tsv> <root> many papers (pdf path <TAB> output dir)

Every page is kept and only resized and compressed, never edited or cropped.
For each page the smaller of two encodings is kept:
  · clean printed pages → 4 grey levels, lossless (sharp text, tiny files)
  · scans and photos    → normal lossy WebP (keeps the grey detail)
Writes pages.json in each output dir: {"pages": [...], "width": 1000, "bytes": total}.
Needs: poppler (pdftoppm) and Pillow.
"""
import io, json, os, subprocess, sys, tempfile, glob
from PIL import Image

WIDTH = 1000


def encode(im):
    grey = im.convert('L')
    if grey.width != WIDTH:
        grey = grey.resize((WIDTH, round(grey.height * WIDTH / grey.width)), Image.LANCZOS)
    hist = grey.histogram()
    mid = sum(hist[60:200]) / max(1, sum(hist))          # share of mid-grey pixels: high for scans and photos
    out = []
    if mid < 0.10:
        b = io.BytesIO(); grey.quantize(4).convert('L').save(b, 'WEBP', lossless=True, quality=100, method=4); out.append(b.getvalue())
    b = io.BytesIO(); grey.save(b, 'WEBP', quality=45, method=6); out.append(b.getvalue())
    if mid < 0.10 and len(out[0]) <= len(out[1]) * 1.25:
        return out[0]                                     # sharper text, prefer it unless much bigger
    return min(out, key=len)


def convert(pdf, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-r', '150', '-png', pdf, os.path.join(tmp, 'p')], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        files = sorted(glob.glob(os.path.join(tmp, 'p-*.png')), key=lambda f: int(f.rsplit('-', 1)[1][:-4]))
        pages, total = [], 0
        for i, f in enumerate(files, 1):
            data = encode(Image.open(f))
            name = f'p{i}.webp'
            open(os.path.join(out_dir, name), 'wb').write(data)
            pages.append(name); total += len(data)
    json.dump({'pages': pages, 'width': WIDTH, 'bytes': total}, open(os.path.join(out_dir, 'pages.json'), 'w'))
    return pages, total


if __name__ == '__main__':
    if sys.argv[1] == '--batch':
        root = sys.argv[3]
        for line in open(sys.argv[2], encoding='utf-8'):
            pdf, out = line.rstrip('\n').split('\t')
            p, t = convert(pdf, os.path.join(root, out))
            print(f'{len(p):2} pages {t // 1024:5} KB  {out}', flush=True)
    else:
        p, t = convert(sys.argv[1], sys.argv[2])
        print(len(p), 'pages', t // 1024, 'KB')
