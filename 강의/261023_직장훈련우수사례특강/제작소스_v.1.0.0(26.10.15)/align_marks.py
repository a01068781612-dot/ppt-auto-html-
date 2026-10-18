# 모든 장: 꺾쇠를 제목 첫 글자 왼쪽 위 45도(간격 = 꺾쇠 크기 × 0.46), 꺾쇠 위 주황 머리표는 꺾쇠 위 39px(1장 기준)
import re, sys, json
from PIL import Image
import numpy as np
D, R = sys.argv[1], sys.argv[2]   # 풀어 둔 pptx 폴더, 렌더 그림 폴더(a-NNN.png)
E = 6350; GAP_TAG = 39; K = 0.46
def off(b): o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"\s*/>\s*<a:ext cx="(\d+)" cy="(\d+)"', b); return [int(v) / E for v in o.groups()] if o else None
def inkbox(a, x0, y0, x1, y1, th):
    x0, y0 = max(0, int(x0)), max(0, int(y0)); x1, y1 = min(1920, int(x1)), min(1080, int(y1))
    ys, xs = np.nonzero(a[y0:y1, x0:x1] > th)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()) if len(xs) else None
rep = []
for n in range(1, 121):
    p = f'{D}/ppt/slides/slide{n}.xml'; x = open(p, encoding='utf-8').read()
    marks = [b for b in re.findall(r'<p:pic>.*?</p:pic>', x, re.S) if 'name="모서리 마크"' in b]
    tsp = [b for b in re.findall(r'<p:sp>.*?</p:sp>', x, re.S) if 'name="슬라이드 제목"' in b]
    if not marks or not tsp: continue
    T = off(tsp[0]);
    if T[0] > 1920: continue
    img = Image.open(f'{R}/a-{n:03d}.png').convert('RGB'); a = np.asarray(img.convert('L')).astype(int).copy()
    mk = min(marks, key=lambda b: abs(off(b)[0] - T[0]) + abs(off(b)[1] - T[1])); M = off(mk)
    if abs(M[0] - T[0]) > 200 or abs(M[1] - T[1]) > 200:   # 꺾쇠가 제목 옆이 아니면(마을 지면 등) 꺾쇠 오른쪽 아래 가장 가까운 글상자 기준
        near = [(abs(off(b)[0] - M[0]) + abs(off(b)[1] - M[1]), off(b)) for b in re.findall(r'<p:sp>.*?</p:sp>', x, re.S) if '<a:t>' in b and off(b) and off(b)[0] > M[0] and off(b)[1] > M[1] - 10 and off(b)[0] - M[0] < 120 and off(b)[1] - M[1] < 120]
        if not near: rep.append((n, 'mark far')); continue
        T = min(near)[1]
    mi = inkbox(a, M[0], M[1], M[0] + M[2], M[1] + M[3], 90); padx, pady = mi[0] - M[0], mi[1] - M[1]; vis = mi[2] - mi[0] + 1
    a2 = a.copy(); a2[int(M[1]):int(M[1] + M[3]) + 1, int(M[0]):int(M[0] + M[2]) + 1] = 0
    ti = inkbox(a2, T[0], T[1], T[0] + T[2], T[1] + T[3], 170)
    if not ti: rep.append((n, 'no title ink')); continue
    d = round(vis * K); cx, cy = ti[0] - d, ti[1] - d
    new = re.sub(r'<a:off x="-?\d+" y="-?\d+"', f'<a:off x="{round((cx - padx) * E)}" y="{round((cy - pady) * E)}"', mk, count=1)
    x = x.replace(mk, new); msg = f'mark {M[0]:.0f},{M[1]:.0f}->{cx - padx:.0f},{cy - pady:.0f}'
    # 꺾쇠 위 주황 머리표: 제목 위, 왼쪽이 제목과 비슷, 주황 글자가 있는 글상자 중 제목에 가장 가까운 것
    cands = []
    for sp in re.findall(r'<p:sp>.*?</p:sp>', x, re.S):
        if '<a:t>' not in sp or 'FF5A1F' not in sp or 'name="슬라이드 제목"' in sp: continue
        B = off(sp)
        if B and B[1] + B[3] <= T[1] + 12 and T[1] - B[1] < 220 and abs(B[0] - T[0]) < 60: cands.append((T[1] - B[1], sp, B))
    if cands:
        _, sp, B = min(cands, key=lambda c: c[0])
        gi = inkbox(a2, B[0], B[1], B[0] + B[2], B[1] + B[3], 90)
        if gi:
            dy = (cy - GAP_TAG) - gi[3]
            if B[1] + dy < 20: dy = 20 - B[1]
            o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', sp)
            sp2 = sp.replace(o.group(0), f'<a:off x="{o.group(1)}" y="{int(o.group(2)) + round(dy * E)}"', 1); x = x.replace(sp, sp2)
            msg += f' | tag {dy:+.0f}px'
    open(p, 'w', encoding='utf-8').write(x); rep.append((n, msg))
json.dump(rep, open(R + '/align_rep.json', 'w'), ensure_ascii=False)
for r in rep: print(*r)
