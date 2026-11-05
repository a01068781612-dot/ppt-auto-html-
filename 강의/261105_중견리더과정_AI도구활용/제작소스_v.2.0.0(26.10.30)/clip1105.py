# 강사 폰 화면 녹화 → 슬라이드용 영상 (1920x1080, 다크 디자인)
# 기다리는 구간은 빠르게, 왼쪽에 지금 단계 표시, 누르는 곳은 멈추고 빨간 테두리. 소리 없음(강사가 설명)
# 사용: python3 clip1105.py <녹화폴더> <출력폴더(hf2)> <lib폴더>
import os, sys, json, subprocess
SRC, OUT, LIB = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))

CLIPS = {
 'v_gemini': dict(
   file='Screen_Recording_20261030_205508_Google.mp4', tag='PART 2 · 강사 시연', title='Gemini로<br>사진 만들고 고치기',
   # (시작초, 끝초, 배속)
   # 누르는 곳: (원본 초, x, y, w, h) — 그 직전 화면을 멈추고 빨간 굵은 테두리로 표시
   taps=[(0.5, 570, 960, 190, 230), (5.0, 440, 2000, 190, 150), (23.0, 545, 810, 495, 115), (26.6, 880, 465, 125, 125),
         (31.8, 50, 150, 130, 120), (35.0, 20, 605, 740, 115), (40.5, 80, 1960, 920, 150), (58.3, 840, 945, 125, 125),
         (76.8, 60, 650, 960, 540), (87.4, 790, 2000, 200, 120), (91.5, 50, 120, 130, 120), (92.6, 80, 1960, 920, 150),
         (117.3, 830, 940, 130, 130), (133.9, 70, 730, 945, 515), (142.0, 45, 120, 130, 130), (167.4, 830, 1090, 130, 130),
         (188.6, 60, 650, 950, 530), (198.2, 55, 115, 130, 130)],
   segs=[(0, 16, 2), (16, 56, 2.5), (56, 72, 6), (72, 96, 1.2), (96, 128, 2.5), (128, 136, 6), (136, 162, 1.2), (162, 174, 2.5), (174, 190, 6), (190, 200.6, 1)],
   steps=[(0, 'Gemini 앱 열기', 'Play 스토어 → 「Google Gemini」'), (16, '말로 사진 만들기', '“세종대왕이 책을 읽는 사진”'),
          (96, '말로 고치기', '“책 읽는 상황 말고 노트북하는 상황으로 교체”'), (162, '한 번 더', '“낚시하는 상황으로 교체”')]),
 'v_flow': dict(
   file='Screen_Recording_20261030_210531_Flow.mp4', tag='PART 2 · 강사 시연', title='Flow로<br>이미지 → 영상',
   # 계정 선택 화면(이메일 목록)은 가림: (시작초, 끝초, x, y, w, h) 원본 화면 기준
   hide=[(45.3, 50.0, 0, 0, 1080, 2340), (43.5, 56.0, 0, 1760, 1080, 220)],
   taps=[(4.2, 445, 2000, 190, 150), (21.7, 15, 470, 1050, 215), (26.6, 35, 805, 1010, 120), (39.9, 545, 560, 495, 135),
         (53.2, 60, 2005, 960, 125), (57.3, 60, 2000, 960, 120), (62.5, 760, 1095, 290, 125), (63.0, 40, 1830, 1000, 240),
         (120.0, 530, 1110, 345, 115), (124.5, 40, 1665, 180, 130), (133.6, 870, 1100, 135, 135), (171.2, 5, 845, 535, 425),
         (208.9, 545, 1990, 520, 145), (270.6, 870, 1092, 135, 135), (274.6, 420, 1375, 240, 90), (411.5, 5, 500, 535, 310),
         (443.7, 545, 1990, 520, 145), (470.4, 860, 1095, 135, 135)],
   segs=[(0, 80, 2.5), (80, 136, 3), (136, 170, 8), (170, 200, 1.5), (200, 270, 3), (270, 350, 10), (350, 372, 1), (372, 430, 3), (430, 455, 8), (455, 470, 1.5), (470, 485, 3), (485, 555, 10), (555, 569, 1)],
   steps=[(0, 'Flow 앱 설치', 'Play 스토어 → 「Google Flow」'), (80, '말로 이미지 만들기', '“경복궁 건설 과정을 처음부터 끝까지 이미지로 만들어 줘”'),
          (200, '사진을 영상으로', '“각 사진을 첫 프레임으로 경복궁 짓는 과정을 영상으로”'), (372, '우리 청사로', '“경남 서부청사를 짓는 과정을 미니어처 스타일로”')]),
}

PX, PY, PH = 1310, 60, 960          # 폰 화면 위치·높이
PW = round(1080 * PH / 2340 / 2) * 2

FREEZE = 1.4   # 누르는 곳을 보여 주는 멈춤(초)

def outtime(segs, t, taps=()):
    o = 0
    for a, b, k in segs:
        if t <= a: break
        o += (min(t, b) - a) / k
    return o + FREEZE * sum(1 for tt, *_ in taps if tt < t)

def panels(id, c, d):
    steps = ''.join(f'<div class="st" id="s{i}"><i>{i+1}</i><div><b>{t}</b><span>{s}</span></div></div>' for i, (_, t, s) in enumerate(c['steps']))
    html = f'''<html><head><style>@font-face{{font-family:P;src:url("file://{LIB}/PretendardVariable.woff2")}}
body{{margin:0;width:1920px;height:1080px;background:#0c0b0b url("file://{HERE}/bg.png");background-size:cover;font-family:P;color:#f4f4f2;position:relative;overflow:hidden}}
.tag{{position:absolute;left:110px;top:96px;font-size:28px;font-weight:800;letter-spacing:.12em;color:#ff5a1f}}
h1{{position:absolute;left:110px;top:150px;margin:0;font-size:96px;line-height:1.1;letter-spacing:-.04em;font-weight:900}}
.sts{{position:absolute;left:110px;top:410px;width:1080px}}
.st{{display:flex;gap:28px;align-items:center;padding:16px 30px;margin-bottom:12px;border-radius:24px;border:2px solid transparent;opacity:.4}}
.st i{{flex:none;width:72px;height:72px;border-radius:50%;border:2.5px solid #55504c;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:32px;font-weight:900}}
.st b{{display:block;font-size:42px;font-weight:800}} .st span{{display:block;font-size:28px;color:#a59f98;margin-top:6px}}
.st.on{{opacity:1;background:#1d1a19;border-color:#ff5a1f;box-shadow:0 20px 60px rgba(255,90,31,.18)}} .st.on i{{border-color:#ff5a1f;background:#ff5a1f;color:#111}}
.st.done{{opacity:.75}}
.ph{{position:absolute;left:{PX-14}px;top:{PY-14}px;width:{PW+28}px;height:{PH+28}px;border-radius:50px;background:#2a2523;box-shadow:0 30px 90px rgba(0,0,0,.6)}}
.cap{{position:absolute;left:110px;bottom:60px;font-size:22px;color:#8a847e}}</style></head><body>
<div class="tag">{c["tag"]}</div><h1>{c["title"]}</h1><div class="sts">{steps}</div><div class="ph"></div>
<div class="cap">강사 폰 화면 녹화 (26.10.30) · 기다리는 시간은 빠르게 넘김</div></body></html>'''
    open(f'{d}/panel.html', 'w').write(html)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});"
          f"await p.goto('file://{d}/panel.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);"
          f"for(let i=0;i<{len(c['steps'])};i++){{await p.evaluate(i=>document.querySelectorAll('.st').forEach((e,j)=>e.className='st'+(j==i?' on':j<i?' done':'')),i);"
          f"await p.screenshot({{path:'{d}/panel'+i+'.png'}});}}await b.close();}})();")
    subprocess.run(['node', '-e', js], check=True)
    os.remove(f'{d}/panel.html')

def mask(d):
    from PIL import Image, ImageDraw
    m = Image.new('L', (PW, PH), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, PW - 1, PH - 1], 38, fill=255); m.save(f'{d}/mask.png')

for id, c in CLIPS.items():
    if len(sys.argv) > 4 and id not in sys.argv[4:]: continue
    d = os.path.join(OUT, id); os.makedirs(d, exist_ok=True)
    panels(id, c, d); mask(d)
    segs = c['segs']; n = len(segs)
    # 구간별로 잘라 배속 → 이어 붙이기 (원본이 1080x2340이라 한 번에 하면 메모리 부족)
    lst = []; taps = sorted(c.get('taps', []))
    def piece(a, b, k):
        sf = f'{d}/seg{len(lst)}.mp4'; lst.append(sf)
        hide = ''.join(f"drawbox={x}:{y}:{w}:{h}:color=0x1d1a19@1:t=fill:enable='between(t,{h0-a:.2f},{h1-a:.2f})'," for h0, h1, x, y, w, h in c.get('hide', []) if h1 > a and h0 < b)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', os.path.join(SRC, c['file']), '-an',
                        '-vf', f'{hide}setpts=PTS/{k},scale={PW}:{PH},fps=30', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', sf], check=True)
    def freeze(t, x, y, w, h):
        from PIL import Image, ImageDraw, ImageFont
        st = f'{d}/_st.png'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', os.path.join(SRC, c['file']), '-frames:v', '1', st], check=True)
        im = Image.open(st).convert('RGB'); dr = ImageDraw.Draw(im)
        for h0, h1, hx, hy, hw, hh in c.get('hide', []):
            if h0 <= t <= h1: dr.rectangle([hx, hy, hx + hw, hy + hh], fill=(29, 26, 25))
        dim = Image.new('RGB', im.size, (0, 0, 0)); m = Image.new('L', im.size, 110); ImageDraw.Draw(m).rounded_rectangle([x, y, x + w, y + h], 18, fill=0)
        im = Image.composite(dim, im, m); dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([x - 6, y - 6, x + w + 6, y + h + 6], 22, outline=(255, 30, 30), width=16)
        fnt = ImageFont.truetype(os.environ.get('KFONT', '/root/.fonts/Pretendard-Bold.otf'), 62)
        lab = '여기 누르기'; tw = dr.textlength(lab, font=fnt); bw, bh = tw + 60, 100
        bx = min(max(x + w / 2 - bw / 2, 20), 1080 - bw - 20); by = y - bh - 30 if y - bh - 30 > 60 else y + h + 30
        dr.rounded_rectangle([bx, by, bx + bw, by + bh], 26, fill=(255, 30, 30)); dr.text((bx + 30, by + 14), lab, font=fnt, fill=(255, 255, 255))
        im.save(st)
        sf = f'{d}/seg{len(lst)}.mp4'; lst.append(sf)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', str(FREEZE), '-i', st, '-vf', f'scale={PW}:{PH}',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', sf], check=True)
        os.remove(st)
    for a, b, k in segs:
        cur = a
        for t, *box in taps:
            if a <= t < b:
                if t > cur: piece(cur, t, k)
                freeze(t, *box); cur = t
        if b > cur: piece(cur, b, k)
    open(f'{d}/seg.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/seg.txt', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', f'{d}/phone.mp4'], check=True)
    f = '[0:v][1:v]alphamerge[ph];'
    ts = [outtime(segs, t, taps) for t, _, _ in c['steps']] + [9999]
    T = f'{outtime(segs, 1e9, taps):.2f}'
    inputs = ['-i', f'{d}/phone.mp4', '-loop', '1', '-framerate', '30', '-t', T, '-i', f'{d}/mask.png']
    for i in range(len(c['steps'])): inputs += ['-loop', '1', '-framerate', '30', '-t', T, '-i', f'{d}/panel{i}.png']
    base = '[2:v]'
    for i in range(1, len(c['steps'])):
        f += f'{base}[{i+2}:v]overlay=enable=\'gte(t,{ts[i]:.2f})\'[b{i}];'; base = f'[b{i}]'
    f += f'{base}[ph]overlay={PX}:{PY}:shortest=1,format=yuv420p[o]'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', f, '-map', '[o]', '-an', '-c:v', 'libx264', '-crf', '24', '-preset', 'veryfast', '-r', '30', f'{d}/out.mp4'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '6', '-i', f'{d}/out.mp4', '-frames:v', '1', f'{d}/last.png'], check=True)
    for x in ['mask.png', 'phone.mp4', 'seg.txt'] + [os.path.basename(x) for x in lst] + [f'panel{i}.png' for i in range(len(c['steps']))]: os.remove(f'{d}/{x}')
    print(id, round(outtime(segs, 1e9, taps), 1), 's,', len(taps), 'taps')
