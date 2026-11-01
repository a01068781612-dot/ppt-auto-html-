# 강사 폰 시연 녹화 → 슬라이드 영상 v.2 (큰 화면 + 줌인·줌아웃)
# 가운데 큰 창(1000x880)에 폰 화면 일부를 따라가며 보여 줌: 글자 칠 때·누를 때·결과 나올 때 확대
# 누르는 곳은 멈추고 빨간 테두리 + 「여기 누르기」. Flow는 결과 사진 → 결과 영상 → 녹화(설치는 10.30 녹화, 뒤는 11.01 녹화)
# 사용: python3 clip2_1105.py <출력폴더(hf2)> [v_gemini|v_flow ...]
# 환경: W1030=10.30 녹화 폴더, UPD=11.01 업뎃 자료 폴더
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]; ONLY = sys.argv[2:]
HERE = os.path.dirname(os.path.abspath(__file__))
W1030 = os.environ.get('W1030', '/home/user/ppt-auto-html-/data/west')
UPD = os.environ.get('UPD', '/home/user/ppt-auto-html-/data/upd')
FB, FX = '/root/.fonts/Pretendard-Bold.otf', '/root/.fonts/Pretendard-ExtraBold.otf'
font = lambda s, p=FB: ImageFont.truetype(p, s)
FPS = 30; HOLD, ZIN, ZHOLD = 2.2, 1.3, 0.9   # 누르기: 정지(설명) → 천천히 확대 → 잠깐 유지
WX, WY, WW, WH = 560, 170, 1000, 880        # 폰 화면 창
SW, SH = 1080, 2340                          # 녹화 원본
BG = Image.open(os.path.join(HERE, 'bg.png')).convert('RGB').resize((1920, 1080))
DARK = (20, 18, 17)

# ── 장면 정의 (시간은 원본 녹화 초)
# segs: (시작, 끝, 배속)  taps: (초, x, y, w, h)  zooms: (시작, 끝, 중심x, 중심y, 배율, 표시)
GEMINI = dict(
    title='Gemini로 사진 만들고 고치기',
    steps=[('Gemini 앱 열기', 'Play 스토어 → 「Google Gemini」'), ('글로 사진 만들기', '“세종대왕이 책을 읽는 사진”'),
           ('글로 고치기', '“책 읽는 상황 말고 노트북하는 상황으로 교체”'), ('한 번 더', '“낚시하는 상황으로 교체”')],
    parts=[dict(file=f'{W1030}/Screen_Recording_20261030_205508_Google.mp4', step_at=[(0, 0), (35, 1), (96, 2), (150, 3)],
        segs=[(0, 16, 2), (16, 41, 2.5), (41, 58, 1.4), (58, 72, 6), (72, 96, 1.2), (96, 100, 2.5), (100, 117, 1.4), (117, 128, 2.5),
              (128, 136, 6), (136, 150, 1.5), (150, 167, 1.4), (167, 174, 2.5), (174, 190, 6), (190, 200.6, 1)],
        taps=[(0.5, 570, 960, 190, 230), (5.0, 440, 2000, 190, 150), (23.0, 545, 810, 495, 115), (26.6, 880, 465, 125, 125),
              (31.8, 50, 150, 130, 120), (35.0, 20, 605, 740, 115), (40.5, 80, 1960, 920, 150), (58.3, 840, 945, 125, 125),
              (76.8, 60, 650, 960, 540), (87.4, 790, 2000, 200, 120), (91.5, 50, 120, 130, 120), (92.6, 80, 1960, 920, 150),
              (117.3, 830, 940, 130, 130), (133.9, 70, 730, 945, 515), (142.0, 45, 120, 130, 130), (167.4, 830, 1090, 130, 130),
              (188.6, 60, 650, 950, 530), (198.2, 55, 115, 130, 130)],
        zooms=[(41, 58.2, 540, 900, 1.0, '입력'), (100, 117.2, 540, 880, 1.0, '입력'), (150, 167.3, 540, 1040, 1.0, '입력'),
               (72, 76.5, 540, 920, 1.15, '결과'), (124, 133.8, 540, 920, 1.15, '결과'), (174, 188.5, 540, 1150, 1.15, '결과'),
               (77.4, 87.0, 540, 1170, 0.8, '결과'), (134.5, 141.6, 540, 1170, 0.8, '결과'), (189.2, 197.8, 540, 1170, 0.8, '결과')])])

FLOW = dict(
    title='Flow로 이미지 → 영상',
    steps=[('Flow 앱 설치', 'Play 스토어 → 「Google Flow」'), ('글로 이미지', '“조선시대 열심히 공부하는 학자들”'),
           ('글로 고치기', '“공부 후 휴식을 취하는 학자들, 저녁 배경으로”'), ('영상으로', '“신이 나서 흥이 나는 분위기”'), ('내려받기', '다운로드 → 720p')],
    parts=[
      dict(file=f'{W1030}/Screen_Recording_20261030_210531_Flow.mp4', step_at=[(0, 0)],
        hide=[(45.3, 50.0, 0, 0, 1080, 2340), (43.5, 56.0, 0, 1760, 1080, 220)],   # 계정 목록(이메일) 가림
        segs=[(0, 63.4, 2.5)],
        taps=[(4.2, 445, 2000, 190, 150), (21.7, 15, 470, 1050, 215), (26.6, 35, 805, 1010, 120), (39.9, 545, 560, 495, 135),
              (53.2, 60, 2005, 960, 125), (57.3, 60, 2000, 960, 120), (62.5, 760, 1095, 290, 125)], zooms=[]),
      dict(file=f'{UPD}/Screen_Recording_20261101_104717_Flow.mp4', step_at=[(0, 1), (100, 2), (205, 3), (318, 4)],
        segs=[(0, 19, 3), (19, 31.9, 1.4), (31.9, 64, 10), (64, 80, 1.5), (80, 85.3, 1.5),
              (103, 110, 3), (110, 126, 1.4), (126, 160, 10), (160, 168, 1.2), (209, 216, 1.5), (216, 228, 1.4), (228, 256, 3.5),
              (256, 292, 10), (292, 298, 1.5), (320, 333, 1), (333, 359, 2)],
        taps=[(1.5, 590, 1990, 240, 110), (14.0, 850, 1880, 130, 100), (19.2, 40, 1090, 700, 110), (31.7, 870, 1095, 130, 130),
              (85.1, 40, 2010, 470, 110), (125.4, 870, 1100, 130, 130), (209.9, 560, 2010, 480, 110), (255.0, 870, 995, 130, 130),
              (320.6, 10, 500, 530, 560), (337.4, 380, 850, 520, 90), (341.1, 190, 1180, 380, 80), (343.1, 370, 1380, 520, 90)],
        zooms=[(19.5, 31.9, 540, 1015, 1.0, '입력'), (110, 125.4, 540, 1040, 1.0, '입력'), (216, 228, 540, 1010, 1.0, '입력'),
               (64, 85, 540, 700, 1.0, '결과'), (160, 168, 540, 900, 1.15, '결과'), (292, 298, 540, 800, 1.0, '결과'),
               (321, 333, 540, 960, 1.1, '결과')])])


def panel(c, cur, tag):
    o = BG.copy(); d = ImageDraw.Draw(o); steps = c['steps']
    d.text((60, 40), 'PART 2 · 강사 시연', font=font(26), fill=(255, 90, 31)); d.text((60, 78), c['title'], font=font(44, FX), fill=(244, 244, 242))
    x0 = 700 if len(steps) > 4 else 760
    for i, (s, _) in enumerate(steps):
        on = i == cur; lab = f'{i+1}  {s}'; w = d.textlength(lab, font=font(28)) + 44
        d.rounded_rectangle([x0, 58, x0 + w, 118], 30, fill=(255, 90, 31) if on else (29, 26, 25), outline=None if on else (58, 53, 51), width=2)
        d.text((x0 + 22, 70), lab, font=font(28), fill=(17, 17, 17) if on else (138, 132, 126)); x0 += w + 14
    sh = Image.new('L', (1920, 1080), 0); ImageDraw.Draw(sh).rounded_rectangle([WX - 14, WY + 6, WX + WW + 14, WY + WH + 34], 50, fill=160)
    o = Image.composite(Image.new('RGB', o.size, (0, 0, 0)), o, sh.filter(ImageFilter.GaussianBlur(30))); d = ImageDraw.Draw(o)
    d.rounded_rectangle([WX - 14, WY - 14, WX + WW + 14, WY + WH + 14], 46, fill=(42, 37, 35))
    d.text((60, 250), f'{cur+1}', font=font(120, FX), fill=(255, 90, 31)); d.text((60, 400), steps[cur][0], font=font(46, FX), fill=(244, 244, 242))
    q = steps[cur][1]; lines, ln = [], ''
    for wd in q.split(' '):
        tt = (ln + ' ' + wd).strip()
        if ln and d.textlength(tt, font=font(32)) > 450: lines.append(ln); ln = wd
        else: ln = tt
    lines.append(ln)
    for i, l in enumerate(lines): d.text((60, 470 + i * 46), l, font=font(32), fill=(214, 210, 201))
    if tag:
        red = tag == '누르기'
        d.rounded_rectangle([1620, 250, 1880, 330], 40, fill=(255, 30, 30) if red else (255, 90, 31))
        d.text((1650, 266), tag, font=font(38, FX), fill=(255, 255, 255) if red else (17, 17, 17))
    d.text((60, 1030), '강사 폰 화면 녹화 · 대기 시간은 빠르게', font=font(20), fill=(138, 132, 126))
    return o

MASK = Image.new('L', (WW, WH), 0); ImageDraw.Draw(MASK).rounded_rectangle([0, 0, WW - 1, WH - 1], 34, fill=255)

def view(im, cx, cy, z):
    cw = SW / z; ch = cw * WH / WW
    if cw <= SW: l = min(max(cx - cw / 2, 0), SW - cw)
    else: l = (SW - cw) / 2
    if ch <= SH: t = min(max(cy - ch / 2, 0), SH - ch)
    else: t = (SH - ch) / 2
    return im.crop((int(l), int(t), int(l + cw), int(t + ch))).resize((WW, WH), Image.BICUBIC)

def tapimg(im, x, y, w, h):
    im = im.copy(); m = Image.new('L', im.size, 110); ImageDraw.Draw(m).rounded_rectangle([x, y, x + w, y + h], 18, fill=0)
    im = Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, m); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x - 8, y - 8, x + w + 8, y + h + 8], 24, outline=(255, 30, 30), width=14)
    fb = font(60); lab = '여기 누르기'; tw = d.textlength(lab, font=fb); bh = 96
    by = y - bh - 24 if y - bh - 24 > 0 else y + h + 24; bx = min(max(x + 20, 20), SW - tw - 60)
    d.rounded_rectangle([bx, by, bx + tw + 40, by + bh], 26, fill=(255, 30, 30)); d.text((bx + 20, by + 12), lab, font=fb, fill=(255, 255, 255))
    U = (min(x, bx) - 10, min(y, by) - 10, max(x + w, bx + tw + 40) + 10, max(y + h, by + bh) + 10)   # 테두리+글씨 전체
    return im, U

def frames_of(src, a, b, k):
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', src, '-an', '-vf', f'fps={FPS / k:.5f},scale={SW}:{SH}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = 0
    while True:
        buf = p.stdout.read(SW * SH * 3)
        if len(buf) < SW * SH * 3: break
        yield a + n * k / FPS, Image.frombuffer('RGB', (SW, SH), buf, 'raw', 'RGB', 0, 1); n += 1
    p.wait()

def grab(src, t):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       stdout=subprocess.PIPE, check=True)
    return Image.frombuffer('RGB', (SW, SH), r.stdout, 'raw', 'RGB', 0, 1)

class Cam:
    def __init__(s): s.x, s.y, s.z = SW / 2, SH * 0.55, 1.0
    def go(s, x, y, z, k=0.05):
        s.x += (x - s.x) * k; s.y += (y - s.y) * k; s.z += (z - s.z) * k

def hide(im, part, t):
    hs = [h for h in part.get('hide', []) if h[0] <= t <= h[1]]
    if not hs: return im
    im = im.copy(); d = ImageDraw.Draw(im)
    for _, _, x, y, w, h in hs: d.rectangle([x, y, x + w, y + h], fill=(29, 26, 25))
    return im

def render(id, c):
    d = os.path.join(OUT, id); os.makedirs(d, exist_ok=True)
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', f'{d}/out.mp4'], stdin=subprocess.PIPE)
    put = lambda im: enc.stdin.write(im.tobytes())
    PAN = {}
    def pan(cur, tag):
        if (cur, tag) not in PAN: PAN[(cur, tag)] = panel(c, cur, tag)
        return PAN[(cur, tag)]
    nfr = 0
    # ── Flow 앞부분: 결과 사진 → 결과 영상
    if c.get('photos'):
        def stage(img, label, sub):
            o = BG.copy(); dr = ImageDraw.Draw(o)
            dr.text((110, 60), 'PART 2 · 강사 시연', font=font(26), fill=(255, 90, 31)); dr.text((110, 98), label, font=font(52, FX), fill=(244, 244, 242))
            dr.text((110, 172), sub, font=font(28), fill=(165, 159, 152))
            fw, fh = 1440, 810; x0, y0 = 240, 240
            dr.rounded_rectangle([x0 - 10, y0 - 10, x0 + fw + 10, y0 + fh + 10], 30, fill=(42, 37, 35))
            m = Image.new('L', (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, fw - 1, fh - 1], 22, fill=255)
            o.paste(img.resize((fw, fh), Image.BICUBIC), (x0, y0), m); return o
        ph = [Image.open(f).convert('RGB') for f in c['photos']]
        for i, im in enumerate(ph):
            for j in range(int(1.8 * FPS)):
                z = 1 + 0.06 * j / (1.8 * FPS); w, h = im.size; cw, ch = w / z, h / z
                put(stage(im.crop((int((w - cw) / 2), int((h - ch) / 2), int((w + cw) / 2), int((h + ch) / 2))),
                          '① 오늘 만들 결과 — 사진', f'Flow로 말 한 줄 → 사진 {i+1} / {len(ph)}')); nfr += 1
        for _, im in frames_of(c['movie'], 0, 60, 1):
            put(stage(im if im.size == (1440, 810) else im, '② 그 사진으로 만든 영상', 'Flow 「애니메이션」 — “신이 나서 흥이 나는 분위기”')); nfr += 1
    # ── 녹화
    cam = Cam()
    for part in c['parts']:
        src = part['file']
        taps = sorted(part['taps']); zooms = part['zooms']
        def step(t): return [s for a, s in part['step_at'] if a <= t][-1]
        def target(t):
            for a, b, x, y, z, tag in zooms:
                if a <= t <= b: return x, y, z, tag
            nxt = [tp for tp in taps if tp[0] > t]
            if nxt:
                _, x, y, w, h = nxt[0]; return x + w / 2, y + h / 2, 1.0, ''
            return SW / 2, SH * 0.5, 1.0, ''
        for a, b, k in part['segs']:
            cuts = [tp for tp in taps if a <= tp[0] < b]; cur = a
            pieces = []
            for tp in cuts: pieces += [('run', cur, tp[0]), ('tap', tp)]; cur = tp[0]
            pieces.append(('run', cur, b))
            for pc in pieces:
                if pc[0] == 'run':
                    if pc[2] - pc[1] < 0.05: continue
                    for t, im in frames_of(src, pc[1], pc[2], k):
                        x, y, z, tag = target(t); cam.go(x, y, z)
                        o = pan(step(t), tag).copy(); o.paste(view(hide(im, part, t), cam.x, cam.y, cam.z), (WX, WY), MASK); put(o); nfr += 1
                else:
                    t, x, y, w, h = pc[1]; im, U = tapimg(hide(grab(src, t), part, t), x, y, w, h)
                    uw, uh = U[2] - U[0] + 160, U[3] - U[1] + 160          # 여유 포함 — 글씨가 잘리지 않게
                    zt = max(1.0, min(1.4, SW / uw, SW * WH / WW / uh))
                    ease = lambda u: u * u * (3 - 2 * u)
                    x0, y0, z0 = cam.x, cam.y, cam.z; bx, by = (U[0] + U[2]) / 2, (U[1] + U[3]) / 2
                    keys = [(HOLD, (bx, by, 1.0), 0.6), (ZIN, (bx, by, zt), ZIN), (ZHOLD, (bx, by, zt), 0)]
                    for dur, (tx, ty, tz), mv in keys:
                        sx, sy, sz = cam.x, cam.y, cam.z
                        for j in range(int(dur * FPS)):
                            u = ease(min(1, j / max(1, mv * FPS))) if mv else 1
                            cam.x, cam.y, cam.z = sx + (tx - sx) * u, sy + (ty - sy) * u, sz + (tz - sz) * u
                            o = pan(step(t), '누르기').copy(); o.paste(view(im, cam.x, cam.y, cam.z), (WX, WY), MASK); put(o); nfr += 1
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '3', '-i', f'{d}/out.mp4', '-frames:v', '1', f'{d}/last.png'], check=True)
    print(id, round(nfr / FPS, 1), 's')

for id, c in (('v_gemini', GEMINI), ('v_flow', FLOW)):
    if ONLY and id not in ONLY: continue
    render(id, c)
