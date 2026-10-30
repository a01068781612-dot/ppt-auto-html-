# 강사 폰 화면 녹화 → 슬라이드용 영상 (1920x1080, 다크 디자인)
# 기다리는 구간은 빠르게, 왼쪽에 지금 단계 표시. 소리 없음(강사가 설명)
# 사용: python3 clip1105.py <녹화폴더> <출력폴더(hf2)> <lib폴더>
import os, sys, json, subprocess
SRC, OUT, LIB = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))

CLIPS = {
 'v_gemini': dict(
   file='Screen_Recording_20261030_205508_Google.mp4', tag='PART 2 · 강사 시연', title='Gemini로<br>사진 만들고 고치기',
   # (시작초, 끝초, 배속)
   segs=[(0, 16, 2), (16, 56, 2.5), (56, 72, 6), (72, 96, 1.2), (96, 128, 2.5), (128, 136, 6), (136, 162, 1.2), (162, 174, 2.5), (174, 190, 6), (190, 200.6, 1)],
   steps=[(0, 'Gemini 앱 열기', 'Play 스토어 → 「Google Gemini」'), (16, '말로 사진 만들기', '“세종대왕이 책을 읽는 사진”'),
          (96, '말로 고치기', '“책 대신 노트북으로 작업하는 상황으로”'), (162, '한 번 더', '“낚시하는 상황으로 교체”')]),
 'v_flow': dict(
   file='Screen_Recording_20261030_210531_Flow.mp4', tag='PART 2 · 강사 시연', title='Flow로<br>이미지 → 영상',
   segs=[(0, 80, 2.5), (80, 136, 3), (136, 170, 8), (170, 200, 1.5), (200, 270, 3), (270, 350, 10), (350, 372, 1), (372, 430, 3), (430, 455, 8), (455, 470, 1.5), (470, 485, 3), (485, 555, 10), (555, 569, 1)],
   steps=[(0, 'Flow 앱 설치', 'Play 스토어 → 「Google Flow」'), (80, '말로 이미지 6장', '“경복궁 건설 과정을 처음부터 끝까지 3x2로”'),
          (200, '사진을 영상으로', '“각 사진을 첫 프레임으로 영상화”'), (372, '우리 청사로', '“경남 서부청사를 짓는 과정, 미니어처 스타일”')]),
}

PX, PY, PH = 1310, 60, 960          # 폰 화면 위치·높이
PW = round(1080 * PH / 2340 / 2) * 2

def outtime(segs, t):
    o = 0
    for a, b, k in segs:
        if t <= a: break
        o += (min(t, b) - a) / k
    return o

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
    lst = []
    for i, (a, b, k) in enumerate(segs):
        sf = f'{d}/seg{i}.mp4'; lst.append(sf)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', os.path.join(SRC, c['file']), '-an',
                        '-vf', f'setpts=PTS/{k},scale={PW}:{PH},fps=30', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', sf], check=True)
    open(f'{d}/seg.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/seg.txt', '-c', 'copy', f'{d}/phone.mp4'], check=True)
    f = '[0:v][1:v]alphamerge[ph];'
    ts = [outtime(segs, t) for t, _, _ in c['steps']] + [9999]
    T = f'{outtime(segs, 1e9):.2f}'
    inputs = ['-i', f'{d}/phone.mp4', '-loop', '1', '-framerate', '30', '-t', T, '-i', f'{d}/mask.png']
    for i in range(len(c['steps'])): inputs += ['-loop', '1', '-framerate', '30', '-t', T, '-i', f'{d}/panel{i}.png']
    base = '[2:v]'
    for i in range(1, len(c['steps'])):
        f += f'{base}[{i+2}:v]overlay=enable=\'gte(t,{ts[i]:.2f})\'[b{i}];'; base = f'[b{i}]'
    f += f'{base}[ph]overlay={PX}:{PY}:shortest=1,format=yuv420p[o]'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', f, '-map', '[o]', '-an', '-c:v', 'libx264', '-crf', '24', '-preset', 'veryfast', '-r', '30', f'{d}/out.mp4'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '6', '-i', f'{d}/out.mp4', '-frames:v', '1', f'{d}/last.png'], check=True)
    for x in ['mask.png', 'phone.mp4', 'seg.txt'] + [os.path.basename(x) for x in lst] + [f'panel{i}.png' for i in range(len(c['steps']))]: os.remove(f'{d}/{x}')
    print(id, round(outtime(segs, 1e9), 1), 's')
