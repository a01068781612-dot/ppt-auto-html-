import sys, os
from PIL import Image, ImageDraw
C, OUT, pat = sys.argv[1], sys.argv[2], sys.argv[3]
lim = int(sys.argv[4]) if len(sys.argv) > 4 else 80
g = [l.split('\t') for l in open(os.path.join(C, 'groups.tsv')) if l.split('\t')[1].startswith(pat)][:lim]
T = 170; cols = 10; rows = (len(g) + cols - 1) // cols
sh = Image.new('RGB', (cols * T, rows * (T + 16)), 'white'); d = ImageDraw.Draw(sh)
for k, r in enumerate(g):
    im = Image.open(os.path.join(C, r[0])).convert('RGB'); im.thumbnail((T - 6, T - 6))
    x, y = k % cols * T, k // cols * (T + 16); sh.paste(im, (x + 3, y + 3)); d.text((x + 3, y + T), r[0][1:6] + ' ' + r[3], fill='black')
sh.save(OUT, quality=80); print(len(g))
