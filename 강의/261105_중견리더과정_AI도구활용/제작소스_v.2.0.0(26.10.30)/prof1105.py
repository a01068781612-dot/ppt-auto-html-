# 강사 소개 1·2 (10.20 워크숍 장면) — 웹 프로필 ssca1612.pages.dev 기준으로 갱신해 다시 렌더
# 사용: python3 prof1105.py <출력폴더(hf2)> <lib폴더> <사진폴더(_R8A4947---_완료.jpg)> <10.20 PPT 압축 푼 폴더>
import os, re, sys, shutil, subprocess
OUT, LIB, PHOTO, W1020 = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
M1020 = os.environ.get('M1020') or os.path.join(HERE, '../../261020_상황관리공감워크숍_AI특강/제작소스_v.1.0.0(26.10.12)/motion_html')
from PIL import Image, ImageDraw

def base(id, src):
    d = os.path.join(OUT, id); os.makedirs(d, exist_ok=True)
    for f in ['hyperframes.json', 'meta.json', 'package.json', 'bg.png']: shutil.copy(os.path.join(HERE, f), d)
    for f in ['gsap.min.js', 'PretendardVariable.woff2']: shutil.copy(os.path.join(LIB, f), d)
    return d, open(os.path.join(M1020, 'st', src, 'index.html')).read()

# ── 강사 소개 1: 수상 7건 → 8건 (2026 농촌 재난 골든타임 확보 2위 추가)
d, h = base('p_prof1', 'prof1')
h = h.replace('data-to="7"', 'data-to="8"')
rows = re.findall(r'<div class="a p-row clip".*?</div></div>\n', h, flags=re.S)
assert len(rows) == 7, len(rows)
new = (rows[4].replace('3위', '2위').replace('AI 기반 소방 민원 답변 자동화', '농촌 재난 골든타임 확보(마을 정보 AI 전환)')
       .replace('장려 · 인사혁신처장상', '우수상 · 경상남도지사상').replace('>2025<', '>2026<'))
rows2 = rows[:4] + [new] + rows[4:]
top0 = int(re.search(r'top:(\d+)px', rows[0]).group(1)); RH = 50
out = []
for i, r in enumerate(rows2):
    r = re.sub(r'(left:680px;top:)\d+px', lambda m: f'{m.group(1)}{top0 + i * RH}px', r, count=1)
    r = r.replace('height:58px', f'height:{RH}px').replace('top:13px;width:64px;height:32px', 'top:9px;width:64px;height:32px')
    r = re.sub(r'data-track-index="\d+"', f'data-track-index="{90 + i}"', r, count=1)
    out.append(r)
a = h.index(rows[0]); b = h.index(rows[-1]) + len(rows[-1])
h = h[:a] + ''.join(out) + h[b:]
open(d + '/index.html', 'w').write(h)
# 사진: 원본(흑백 정복)에서 600x1080 세로로 자름
im = Image.open(PHOTO).convert('RGB'); W, H = im.size; cw = int(H * 600 / 1080); x0 = int(W * 0.527 - cw * 0.53)
im.crop((x0, 0, x0 + cw, H)).resize((600, 1080), Image.LANCZOS).save(d + '/photo_col.jpg', quality=90)
# 아래·오른쪽 어둡게(이름 글자 읽히게)
f = Image.new('RGBA', (600, 1080), (0, 0, 0, 0)); px = f.load()
for y in range(1080):
    for x in range(600):
        a1 = max(0, (y - 560) / 520) ** 1.2 * 235; a2 = max(0, (x - 470) / 130) * 255
        px[x, y] = (12, 11, 11, int(min(255, max(a1, a2))))
f.save(d + '/fade.png')

# ── 강사 소개 2: 웹 프로필과 같은 내용 — 기사 사진은 10.20 장 마지막 화면에서 잘라 씀
d, h = base('p_prof2', 'prof2')
open(d + '/index.html', 'w').write(h)
fr = os.path.join(d, '_f.png')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-sseof', '-0.1', '-i', os.path.join(W1020, 'ppt/media/media-5-1.mp4'), '-frames:v', '1', fr], check=True)
im = Image.open(fr).convert('RGB')
for n, x in (('press1', 115), ('press3', 541), ('press5', 967)):
    im.crop((x, 726, x + 390, 856)).save(f'{d}/{n}.jpg', quality=92)
os.remove(fr)
print('ok')
