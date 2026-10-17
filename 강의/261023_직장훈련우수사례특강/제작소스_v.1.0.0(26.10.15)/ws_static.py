# 2 · 4 · 5장(워크숍판 7초 모션)을 분해할 수 있게 정적 장면 HTML로 다시 만든다 — 모션이 끝난 마지막 모습 그대로.
# 장면 원본: 제작소스_v.1.5.0(26.10.05)/motion/static/gen.py 의 vintro(2장) · 강의/261020_상황관리공감워크숍_AI특강/제작소스_v.1.0.0(26.10.12)/prof1020.py 의 prof1 · prof2(4 · 5장)
# 사진은 원래 파일이 없어 영상 마지막 장면에서 잘라 씀(강사 사진 위 글자는 지우고 넣음 — 글자는 글상자로 따로 들어감).
# 사용: python3 ws_static.py <저장소 루트> <영상 마지막 장면 폴더(ws2_last.png · ws4_last.png · ws5_last.png)> <bg.png> <출력 폴더>
#   결과: 출력 폴더/v002.html · v004.html · v005.html (split_extract.js에 그대로 넣음)
import sys, os, re, shutil
import numpy as np, cv2
from PIL import Image
ROOT, FR, BG, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
GEN = open(os.path.join(ROOT, '제작소스_v.1.5.0(26.10.05)/motion/static/gen.py'), encoding='utf-8').read()
PROF = open(os.path.join(ROOT, '강의/261020_상황관리공감워크숍_AI특강/제작소스_v.1.0.0(26.10.12)/prof1020.py'), encoding='utf-8').read()
cut = lambda src, a, b: src[src.index(a):src.index(b)]
CSS = re.search(r"CSS = '''(.*?)'''", PROF, re.S).group(1).replace('#root', '#r')
ns = {'PP': '', 'PROF': ''}   # 원래 자료 폴더 이름(쓰지 않음)
exec(cut(PROF, 'class B:', 'def write('), ns)   # B(장면 조각 모음) · chars(글자 나누기)
pages = {}
ns['write'] = lambda name, dur, b, js, assets=(): pages.__setitem__(name, b.html())
exec(cut(GEN, 'def vintro():', 'vintro()\n'), ns); ns['vintro']()
exec(cut(PROF, 'def prof1():', '# ───────────── 강사 소개 2'), ns); ns['prof1']()
exec(cut(PROF, 'def prof2():', '\n\nprof1()'), ns); ns['prof2']()

fr = {k: Image.open(os.path.join(FR, f'{k}_last.png')).convert('RGB') for k in ('ws2', 'ws4', 'ws5')}
fr['ws2'].crop((932, 172, 932 + 856, 172 + 482)).save(os.path.join(OUT, '국무회의_화면.jpg'), quality=92)
# 강사 사진: 왼쪽 600px에서 이름 · 영문 · 직함 글자를 지움(OpenCV inpaint)
ph = np.array(fr['ws4'].crop((0, 0, 600, 1080)))[:, :, ::-1].copy()
g = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(ph, cv2.COLOR_BGR2HSV)
mask = np.zeros(g.shape, np.uint8)
for (x0, y0, x1, y1) in [(60, 680, 600, 832), (60, 830, 600, 870), (60, 890, 600, 990)]:   # 글자 줄 자리(HTML 위치 기준)
    sub = (g[y0:y1, x0:x1] > 120) | ((hsv[y0:y1, x0:x1, 1] > 120) & (hsv[y0:y1, x0:x1, 2] > 120))   # 흰 · 회색 · 주황 글자
    mask[y0:y1, x0:x1] = sub.astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
ph = cv2.inpaint(ph, mask, 9, cv2.INPAINT_TELEA)
Image.fromarray(ph[:, :, ::-1]).save(os.path.join(OUT, '강사사진.jpg'), quality=92)
pw = (1700 - 26 * 3) / 4.05
for i, f in enumerate(['기사사진1', '기사사진2', '기사사진3']):
    x = 110 + i * (pw + 26) + 1.5
    fr['ws5'].crop((round(x), 726, round(x + pw - 3), 726 + 130)).save(os.path.join(OUT, f + '.jpg'), quality=92)
shutil.copy(BG, os.path.join(OUT, 'bg.png'))
FONT = os.path.join(os.path.dirname(BG), 'PretendardVariable.woff2')
if os.path.exists(FONT): shutil.copy(FONT, OUT)
def sq(x, y, s=40):   # 제목 옆 모서리 마크(p1_v33.py와 같은 모양)
    w = max(3, round(s * .06))
    return (f'<svg class="a" style="left:{x}px;top:{y}px" width="{s+w}" height="{s+w}">'
            f'<path d="M{s+w/2},{w/2+s*.25} L{s+w/2},{w/2} L{w/2},{w/2} L{w/2},{s+w/2} L{w/2+s*.3},{s+w/2}" '
            f'fill="none" stroke="#f4f4f2" stroke-width="{w}"/></svg>')
# 워크숍판(26.10.20) 마지막 장면과 맞춤: 2장은 사진 틀 모서리 네모 대신 제목 옆 마크, 5장도 제목 옆 마크(영상 장면에서 위치 측정)
pages['vintro'] = re.sub(r'<div class="sq v-sq clip"[^>]*></div>', '', pages['vintro']) + sq(86, 185)
pages['prof2'] += sq(87, 113)
# 모션용 쪼개기 풀기: 글자마다 나눈 <span class="ch"> · 줄마다 가린 .mask → 한 글상자로(줄바꿈은 <br>)
def unsplit(h):
    h = re.sub(r'<span class="ch">(.*?)</span>', r'\1', h)
    h = re.sub(r'(?:<span class="mask"><span>(.*?)</span></span>)+', lambda m: '<br>'.join(re.findall(r'<span class="mask"><span>(.*?)</span></span>', m.group(0))), h)
    return h
for no, name in [(2, 'vintro'), (4, 'prof1'), (5, 'prof2')]:
    body = unsplit(pages[name]).replace('intro_poster.png', '국무회의_화면.jpg').replace('photo_col.jpg', '강사사진.jpg')
    body = re.sub(r'<img src="fade.png"[^>]*/>', '', body)   # 어둡게 하는 효과는 사진에 이미 들어 있음
    for i, f in enumerate(['press1', 'press3', 'press5']): body = body.replace(f'{f}.jpg', f'기사사진{i + 1}.jpg')
    html = f'<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><style>{CSS}</style></head><body><div id="r">{body}</div></body></html>'
    open(os.path.join(OUT, f'v{no:03d}.html'), 'w', encoding='utf-8').write(html)
print('ok', sorted(pages))
