# v.1.0.0 결과 → v.1.1.0: 한 단계 폴더 "순번 이름(장수)", 작은 폴더는 묶고, 공문(PDF 쪽 이미지) · 언론보도는 따로. 묶은 폴더 안 파일 이름 앞에 세부 분류를 붙여 미리보기에서 순서대로 보이게
import sys, os, csv, re, shutil, subprocess, tempfile, hashlib
from PIL import Image
SRC, EX, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
rows = list(csv.reader(open(os.path.join(SRC, '00_사진출처목록.csv'), encoding='utf-8-sig')))[1:]
F = {1: '추진배경·계획·협의', 2: '농골길책자_마을사진', 3: '농골길책자_쪽이미지', 4: '2025_현지적응훈련', 5: '디브리핑_위성지도',
     6: '2026_AI기반_현지적응훈련', 7: 'AI농골길코치·웹·확산·수상', 8: '언론보도', 9: '공문·문서', 99: '분류보류'}
def route(p, src):
    d, doc = os.path.dirname(p), '_문서·도표' in p
    m = re.search(r'(20\d\d-\d\d(?:-1회차_\d팀)?)', d)
    if doc:
        if '.pdf::' in src: return None                     # PDF에서 뽑은 문서 이미지는 PDF 쪽 이미지로 대체
        tag = {'08_확산·수상/AI': 'AI코치제출문서', '08_확산·수상/직장': '직장훈련제안서', '06_': '디브리핑·숙지도평가', '10_': '2026고도화', '05_': '2025훈련결과보고',
               '02_': '추진계획', '03_': 'TF', '09_': 'GPTs', '11_': '웹'}
        return 9, '2_첨부_' + next((v for k, v in tag.items() if d.startswith(k)), '문서')
    if d.startswith(('01_', '02_', '03_', '07_')): return 1, {'01': '현장여건', '02': '계획·전수조사', '03': 'TF', '07': '군청협의'}[d[:2]]
    if '책자_마을사진' in d: return 2, '마을사진'
    if '책자_발췌' in d: return 3, '0_발췌'
    if '책자_전체페이지' in d: return 3, '쪽'
    if d.startswith('05_'): return 4, m.group(1)
    if d.startswith('06_'): return 5, m.group(1)
    if d.startswith('10_'): return 6, m.group(1) if m else '고도화현장조사'
    if d.startswith('09_'): return 7, '1_GPTs'
    if d.startswith('11_'): return 7, '2_웹'
    if d.startswith('13_'): return 7, '3_도식'
    if '직장훈련' in d: return 7, '5_직장훈련제안서'
    if d.startswith('08_'): return 7, '4_확산·수상'
    if d.startswith('12_'): return 8, '기사화면' if '기사화면' in d else '기사사진'
    return 99, '보류'
items = []   # (폴더, 접두어, 원본 경로, 크기, 출처)
for p, wh, n, src in rows:
    r = route(p, src)
    if r: items.append((r[0], r[1], os.path.join(SRC, p), wh, src))
# 공문 PDF 쪽 이미지(같은 PDF가 두 폴더에 있으면 한 번만)
seen, tmp = set(), tempfile.mkdtemp()
G = os.path.join(EX, '농골길 관련 공문-정리')
for r, ds, fs in sorted(os.walk(G)):
    for f in sorted(fs):
        if not f.endswith('.pdf') or '[붙임2]' in f: continue
        pth = os.path.join(r, f); h = hashlib.md5(open(pth, 'rb').read()).hexdigest()
        if h in seen: continue
        seen.add(h)
        stem = os.path.splitext(f)[0]
        for a, b in [('농촌마을 골든타임 길라잡이', '농골길'), ('농촌마을 골든타임 확보를 위한 ', ''), ('농촌마을 골든타임 확보 ', ''), ('농촌마을 골든타임 ', ''), ('「', ''), ('」', ''),
                     ('‘', ''), ('’', ''), ('“', ''), ('”', ''), (' ', '')]: stem = stem.replace(a, b)
        y = '2026' if ('04_2026' in r or '03_2026' in r) else '2025'
        if '25년' in stem or '2025년' in stem: y = '2025'
        o = os.path.join(tmp, h); subprocess.run(['pdftoppm', '-r', '110', '-jpeg', '-jpegopt', 'quality=88', pth, o], check=True)
        for pg in sorted(x for x in os.listdir(tmp) if x.startswith(h)):
            k = int(re.search(r'-(\d+)\.jpg$', pg).group(1))
            items.append((9, f'1_공문_{y}_{stem[:38]}_p{k:02d}', os.path.join(tmp, pg), '', 'PDF 쪽 이미지: ' + os.path.relpath(pth, EX)))
cnt = {}
for it in items: cnt[it[0]] = cnt.get(it[0], 0) + 1
idx, seq = [], {}
for fo, pre, path, wh, src in sorted(items, key=lambda x: (x[0], x[1], x[2])):
    dname = f'{fo:02d} {F[fo]}({cnt[fo]})'
    os.makedirs(os.path.join(OUT, dname), exist_ok=True)
    if pre.startswith('1_공문_'): name = pre + '.jpg'
    else:
        seq[(fo, pre)] = seq.get((fo, pre), 0) + 1; name = f'{pre}_{seq[(fo, pre)]:03d}{os.path.splitext(path)[1]}'
    if os.path.splitext(path)[1].lower() in ('.bmp', '.gif', '.tif', '.tiff', '.webp'):   # 미리보기 잘 되게 PNG로
        name = os.path.splitext(name)[0] + '.png'; Image.open(path).convert('RGB').save(os.path.join(OUT, dname, name))
    else: shutil.copy2(path, os.path.join(OUT, dname, name))
    idx.append((f'{dname}/{name}', src))
with open(os.path.join(OUT, '00_사진출처목록.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['파일', '원래 출처']); w.writerows(idx)
shutil.rmtree(tmp)
for k in sorted(cnt): print(f'{k:02d} {F[k]}({cnt[k]})')
print('total', len(idx))
