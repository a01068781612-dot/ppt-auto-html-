# 중복 제거: md5 동일 + 지각 해시(phash·dhash 모두 거리 ≤ 4, 비율 비슷) → 한 무리로 묶고, 분류는 우선순위가 가장 높은 출처, 파일은 해상도가 가장 큰 것
import sys, hashlib, os, numpy as np, imagehash
from PIL import Image
C = sys.argv[1]
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(C, 'manifest.tsv'))]
PRI = ['05_', '10_2026_AI기반_현지적응훈련/2026', '06_', '01_', '02_', '03_', '07_', '09_', '11_', '12_', '04_농골길책자/책자_마을사진', '04_농골길책자/책자_발췌',
       '04_농골길책자/책자_전체페이지', '08_확산·수상/직장훈련', '08_확산·수상\t', '13_', '10_2026_AI기반_현지적응훈련/고도화', '08_확산·수상/AI', '_시각화', '99_']
def pri(lab):
    for i, p in enumerate(PRI):
        if (lab + '\t').startswith(p): return i
    return len(PRI)
md5, ph, dh, ar, px = [], [], [], [], []
for fn, lab, src, wh in rows:
    b = open(os.path.join(C, fn), 'rb').read(); md5.append(hashlib.md5(b).hexdigest())
    im = Image.open(os.path.join(C, fn)).convert('RGB'); w, h = im.size
    ph.append(np.array(imagehash.phash(im).hash).flatten()); dh.append(np.array(imagehash.dhash(im).hash).flatten())
    ar.append(w / h); px.append(w * h)
n = len(rows); par = list(range(n))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
PH, DH, AR = np.array(ph), np.array(dh), np.array(ar)
for i in range(n):
    d1 = (PH[i + 1:] != PH[i]).sum(1); d2 = (DH[i + 1:] != DH[i]).sum(1)
    ok = ((d1 <= 4) & (d2 <= 4) & (np.abs(AR[i + 1:] / AR[i] - 1) < .08))
    for j in np.nonzero(ok)[0] + i + 1: par[f(j)] = f(i)
    for j in range(i + 1, n):
        if md5[j] == md5[i]: par[f(j)] = f(i)
G = {}
for i in range(n): G.setdefault(f(i), []).append(i)
out = open(os.path.join(C, 'groups.tsv'), 'w')
for g in G.values():
    lab = min((rows[i][1] for i in g), key=pri); best = max(g, key=lambda i: px[i])
    out.write('\t'.join([rows[best][0], lab, rows[best][2], rows[best][3], str(len(g)), '|'.join(rows[i][0] for i in g)]) + '\n')
print('candidates', n, 'unique', len(G))
