# 농골길 사진 후보 수집: 원본 이미지 + 문서(xlsx·pptx·hwpx·hwp·pdf·zip·alz) 안에 든 이미지 → cand/ + manifest.tsv(파일, 분류, 출처)
import os, sys, io, zipfile, zlib, subprocess, tempfile, shutil, re
import olefile
from PIL import Image
EX, LOCAL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
IMG = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp')
man = open(os.path.join(OUT, 'manifest.tsv'), 'w')
cnt = [0]

def label(src):
    s = src
    if s.startswith('local/'): return '/'.join(s.split('/')[1:-1])
    M = re.search(r'(\d{1,2})월', s)
    mon = f'{int(M.group(1)):02d}' if M else ''
    if '/_tools/photos/20' in s:
        y, m = re.search(r'photos/(\d{4})-(\d{2})', s).groups()
        return (f'05_2025_현지적응훈련/2025-{m}' if y == '2025' else f'10_2026_AI기반_현지적응훈련/2026-{m}')
    if '직장훈련PDF' in s or '직장훈련HWP' in s or '직장훈련 공모전' in s: return '08_확산·수상/직장훈련공모전_제안서'
    if 'AI농골길코치_본문' in s or 'AI농골길코치_분야1' in s: return '08_확산·수상/AI농골길코치_공모전_제출문서'
    if '/_tools/sample_images/' in s: return '13_도식·인포그래픽'
    if '/_tools/book/' in s: return '04_농골길책자/책자_발췌'
    if '시각화' in s: return '_시각화자료'
    if '02_2025_현지적응훈련' in s or ('2025' in s and '현지적응훈련' in s and '결과' in s):
        if '디브리핑' in s: return f'06_디브리핑·숙지도평가/2025-{mon}_디브리핑'
        if '숙지도' in s: return f'06_디브리핑·숙지도평가/2025-{mon}_숙지도평가'
        return f'05_2025_현지적응훈련/2025-{mon}'
    if '04_2026_AI기반' in s:
        tm = re.search(r'\((\d)팀\)', s); sub = f'2026-{mon}' + (f'-1회차_{tm.group(1)}팀' if '1회차' in s and tm else '')
        if '디브리핑' in s: return f'06_디브리핑·숙지도평가/2026-{mon}_디브리핑'
        if '숙지도' in s: return f'06_디브리핑·숙지도평가/{sub}_숙지도평가'
        return f'10_2026_AI기반_현지적응훈련/{sub}'
    if '유관기관 협의' in s: return '07_유관기관협의·주민참여예산'
    if 'TF팀' in s: return '03_TF·선정기준'
    if '길라잡이 추진 계획' in s or '행정마을' in s or '지리조사' in s: return '02_계획·전수조사'
    if '(20P)' in s: return '04_농골길책자/책자_전체페이지'
    if '[붙임2]2025년' in s: return '04_농골길책자/책자_마을사진'
    if '설명회' in s or '우수시책' in s or '적극행정' in s: return '08_확산·수상'
    if '고도화' in s or '산림인접' in s or '주요업무계획' in s or '화재 고위험' in s: return '10_2026_AI기반_현지적응훈련/고도화_계획·현장조사'
    if '239마을' in s: return '02_계획·전수조사'
    if 'Gpts' in s or 'GPTs' in s: return '09_AI농골길코치_GPTs'
    return '99_분류보류'

def emit(data, src, ext):
    try:
        im = Image.open(io.BytesIO(data)); w, h = im.size
    except Exception:
        return
    if min(w, h) < 150: return
    cnt[0] += 1
    fn = f'c{cnt[0]:05d}{ext.lower() if ext.lower() != ".jpeg" else ".jpg"}'
    open(os.path.join(OUT, fn), 'wb').write(data)
    man.write(f'{fn}\t{label(src)}\t{src}\t{w}x{h}\n')

def from_zip(data, src, depth=0):
    try: z = zipfile.ZipFile(io.BytesIO(data))
    except Exception: return
    for i in z.infolist():
        n = i.filename
        if not (i.flag_bits & 0x800):
            try: n = n.encode('cp437').decode('cp949')
            except Exception: pass
        handle(z.read(i), f'{src}::{n}', depth + 1)

def from_hwp(data, src):
    try: o = olefile.OleFileIO(io.BytesIO(data))
    except Exception: return
    for e in o.listdir():
        if e[0] != 'BinData': continue
        b = o.openstream(e).read()
        for cand in (b,):
            try: cand = zlib.decompress(b, -15)
            except Exception: pass
            emit(cand, f'{src}::{"/".join(e)}', os.path.splitext(e[-1])[1] or '.png')

def from_pdf(data, src):
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'a.pdf'); open(p, 'wb').write(data)
    subprocess.run(['pdfimages', '-png', '-p', p, os.path.join(d, 'i')], capture_output=True)
    for f in sorted(os.listdir(d)):
        if f.startswith('i'): emit(open(os.path.join(d, f), 'rb').read(), f'{src}::{f}', '.png')
    shutil.rmtree(d)

def from_alz(data, src):
    d = tempfile.mkdtemp(); p = os.path.join(d, 'a.alz'); open(p, 'wb').write(data)
    o = os.path.join(d, 'o'); os.makedirs(o)
    subprocess.run(['unalz', '-utf8', '-d', o, p], capture_output=True)
    for r, _, fs in os.walk(o):
        for f in fs: handle(open(os.path.join(r, f), 'rb').read(), f'{src}::{os.path.relpath(os.path.join(r, f), o)}', 1)
    shutil.rmtree(d)

def handle(data, src, depth=0):
    e = os.path.splitext(src.split('::')[-1])[1].lower()
    if e in IMG: emit(data, src, e)
    elif e in ('.zip', '.xlsx', '.pptx', '.hwpx', '.docx') and depth < 4: from_zip(data, src, depth)
    elif e == '.hwp': from_hwp(data, src)
    elif e == '.pdf': from_pdf(data, src)
    elif e == '.alz': from_alz(data, src)

SKIP = ('INDEX_20', '원본백업', '레퍼런스도식', '/_tools/tpl', '우정사업본부', '119원패스', '인사혁신처')
for base in (EX, LOCAL):
    for r, ds, fs in os.walk(base):
        ds.sort()
        for f in sorted(fs):
            p = os.path.join(r, f)
            if any(k in p for k in SKIP): continue
            handle(open(p, 'rb').read(), os.path.relpath(p, os.path.dirname(base)))
man.close(); print('images', cnt[0])
