# groups.tsv → 최종 폴더: 빈 페이지·검게 뒤집힌 마스크 제외, 흰 바탕이 넓은 이미지(문서 · 도표)는 각 폴더의 _문서·도표 하위 폴더로
import sys, os, shutil, numpy as np, csv
from PIL import Image
C, O = sys.argv[1], sys.argv[2]
NOSPLIT = ('04_', '09_', '11_', '12_', '13_', '99_')
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(C, 'groups.tsv'))]
rows.sort(key=lambda r: (r[1], r[0]))
seq, idx, drop = {}, [], 0
for fn, lab, src, wh, n, mem in rows:
    a = np.asarray(Image.open(os.path.join(C, fn)).convert('L').resize((200, 200)), dtype=float)
    if a.std() < 10 or (a.mean() < 45 and '.pdf' in src): drop += 1; continue
    white = (a > 235).mean()
    sub = lab
    if white > .40 and not lab.startswith(NOSPLIT): sub = lab + '/_문서·도표'
    if lab.startswith('99_') and '분류보류' not in lab: pass
    seq[sub] = seq.get(sub, 0) + 1
    base = lab.split('/')[-1].split('_', 1)[-1] if '/' in lab else lab.split('_', 1)[1]
    big = fn.endswith('.png') and os.path.getsize(os.path.join(C, fn)) > 400_000   # 큰 PNG는 JPEG(품질 90)로 — 용량만 줄이고 화질 유지
    name = f'{base}_{seq[sub]:03d}{".jpg" if big else os.path.splitext(fn)[1]}'
    os.makedirs(os.path.join(O, sub), exist_ok=True)
    if big: Image.open(os.path.join(C, fn)).convert('RGB').save(os.path.join(O, sub, name), quality=90)
    else: shutil.copy2(os.path.join(C, fn), os.path.join(O, sub, name))
    idx.append((sub + '/' + name, wh, n, src.replace('5.농골길/', '')))
with open(os.path.join(O, '00_사진출처목록.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['파일', '크기', '중복으로 합친 수', '원래 출처(문서 :: 문서 안 이미지)']); w.writerows(idx)
print('kept', len(idx), 'dropped', drop)
