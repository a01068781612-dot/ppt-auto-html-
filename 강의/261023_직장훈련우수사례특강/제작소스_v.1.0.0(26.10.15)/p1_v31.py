# 직장훈련특강 PART 1(1~40장) 정지 미리보기 — 기획안 v.3.1.0 기준 (농골길 먼저, 제안서는 PART 2로)
# 사용: python3 p1_v3.py <자료폴더> <출력폴더>
# 자료: 결과보고 PDF 속 사진(rep*), 시각화자료 엑셀 속 훈련 사진(m*), 제안서 쪽(jth-*), 구조구급 PPT 장면(op*)
import os, sys, shutil, subprocess

A, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(A):
    if os.path.isfile(os.path.join(A, f)):
        shutil.copy(os.path.join(A, f), OUT)

CSS = '''@font-face{font-family:"Pretendard";src:url("PretendardVariable.woff2") format("woff2");font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box;word-break:keep-all}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0c0b0b}
#r{width:1920px;height:1080px;position:relative;font-family:"Pretendard",sans-serif;color:#f4f4f2;background:#0c0b0b url(bg.png) center/cover}
.a{position:absolute}.acc{color:#ff5a1f}.cap{color:#a59f98}.dim{color:#8a847e}.body{color:#d6d2c9}
.tag{position:absolute;left:110px;top:92px;font-size:22px;letter-spacing:.12em;white-space:nowrap}.tag b{color:#ff5a1f}.tag span{color:#8a847e}
.ttl{position:absolute;left:110px;top:130px;font-size:66px;font-weight:900;letter-spacing:-.03em;line-height:1.25;white-space:nowrap}
.ghost{position:absolute;right:110px;top:62px;font-size:110px;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.13);font-weight:900;letter-spacing:-.04em;line-height:1}
.hl{position:absolute;left:110px;top:244px;width:1700px;height:1px;background:#55504c}
.card{position:absolute;background:#1d1a19;border:1.5px solid #3a3533;border-radius:29px}
.card.hi{background:#2a2523;border:4px solid #ff5a1f;box-shadow:0 18px 50px rgba(255,90,31,.18)}
.key{position:absolute;left:110px;bottom:70px;width:1700px;padding:22px 34px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:34px;font-weight:700}
.key b{color:#ff5a1f;font-size:22px;letter-spacing:.2em;margin-right:22px}
.pg{position:absolute;right:110px;bottom:34px;font-size:20px;color:#8a847e;letter-spacing:.1em}
table{border-collapse:collapse;width:100%}td,th{padding:16px 22px;border-bottom:1px solid #3a3533;text-align:left;font-size:32px}
th{color:#8a847e;font-size:22px;letter-spacing:.1em;font-weight:700}
.shot{position:absolute;border-radius:16px;overflow:hidden;border:1.5px solid #3a3533;background:#111}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.paper{background:#fff}.paper img{object-fit:contain}
.lbl{position:absolute;left:0;bottom:0;right:0;padding:8px 14px;background:linear-gradient(transparent,rgba(0,0,0,.85));font-size:20px;color:#f4f4f2}
.chip{display:inline-block;padding:12px 26px;margin:0 14px 14px 0;border:1.5px solid #55504c;border-radius:40px;font-size:28px;font-weight:700;color:#d6d2c9}
.note{position:absolute;left:0;top:0;padding:10px 18px;background:rgba(255,90,31,.92);font-size:20px;font-weight:700;color:#fff}
.hlbox{position:absolute;border:5px solid #ff5a1f;border-radius:10px;box-shadow:0 0 0 9999px rgba(0,0,0,0)}
'''

def sq(x, y, s=40):
    w = max(3, round(s * .06))
    return (f'<svg class="a" style="left:{x}px;top:{y}px" width="{s+w}" height="{s+w}">'
            f'<path d="M{s+w/2},{w/2+s*.25} L{s+w/2},{w/2} L{w/2},{w/2} L{w/2},{s+w/2} L{w/2+s*.3},{s+w/2}" '
            f'fill="none" stroke="#f4f4f2" stroke-width="{w}"/></svg>')

def head(tag, sub, ghost, title):
    return (f'<div class="tag"><b>{tag}</b>  <span>{sub}</span></div><div class="ghost">{ghost}</div>'
            f'{sq(70, 122)}<div class="ttl">{title}</div><div class="hl"></div>')

def shot(src, x, y, w, h, label='', paper=False):
    return (f'<div class="shot{" paper" if paper else ""}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="{src}">'
            + (f'<div class="lbl">{label}</div>' if label else '') + '</div>')

def grid(items, x=110, y=280, w=1700, h=700, cols=3, gap=20):
    rows = (len(items) + cols - 1) // cols
    cw = (w - gap * (cols - 1)) // cols; ch = (h - gap * (rows - 1)) // rows
    return ''.join(shot(s, x + (i % cols) * (cw + gap), y + (i // cols) * (ch + gap), cw, ch, l) for i, (s, l) in enumerate(items))

def cards(items, top=320, h=420, hi=-1, fs=44):
    n = len(items); gap = 25; w = (1700 - gap * (n - 1)) // n
    out = ''
    for i, (a, b, c) in enumerate(items):
        out += (f'<div class="card{" hi" if i==hi else ""}" style="left:{110+i*(w+gap)}px;top:{top}px;width:{w}px;height:{h}px;padding:40px 36px">'
                f'<div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.1em">{a}</div>'
                f'<div style="font-size:{fs}px;font-weight:900;margin:16px 0 18px;line-height:1.25">{b}</div>'
                f'<div class="body" style="font-size:26px;line-height:1.5">{c}</div></div>')
    return out

def key(t): return f'<div class="key"><b>KEY</b>{t}</div>'

SL = []
def slide(no, body):
    SL.append((no, f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head>'
                   f'<body><div id="r">{body}<div class="pg">{no}</div></div></body></html>'))

def intro(no, num, l1, l2, sub, chips):
    slide(no, f'''<div class="a" style="left:150px;top:150px;font-size:26px;letter-spacing:.3em"><b style="color:#ff5a1f">PART {num}</b></div>
<div class="a" style="right:90px;top:120px;font-size:560px;font-weight:900;color:rgba(255,255,255,.06);line-height:1">{num}</div>{sq(108,232,70)}
<div class="a" style="left:150px;top:250px;font-size:150px;font-weight:900;letter-spacing:-.045em;line-height:1.08">{l1}<br><span class="acc">{l2}</span></div>
<div class="a body" style="left:150px;top:610px;font-size:36px">{sub}</div>
<div class="a" style="left:150px;top:720px;width:1600px">{"".join(f'<span class="chip">{c}</span>' for c in chips)}</div>''')

# ───────── 1-1 오프닝
slide(1, '''<div class="a acc" style="left:150px;top:150px;font-size:30px;font-weight:800;letter-spacing:.06em">제7기 직장훈련 운영관리자 과정</div>''' + sq(104, 228, 90) + '''
<div class="a" style="left:150px;top:250px;font-size:170px;font-weight:900;letter-spacing:-.045em;line-height:1.05">현장의 문제가<br><span class="acc">훈련</span>이 된다</div>
<div class="a body" style="left:150px;top:640px;font-size:36px">데이터로 설계하는 직장훈련 — 농촌마을 골든타임 길라잡이에서 AI 농골길 코치까지</div>
<div class="a" style="right:150px;bottom:150px;text-align:right"><div class="cap" style="font-size:28px">2026. 10. 23. · 광주소방학교</div>
<div style="font-size:34px;font-weight:800;margin-top:10px">AI 챔피언(BLACK) 김경훈</div></div>
<div class="a" style="left:150px;bottom:150px;font-size:28px;letter-spacing:.3em"><span class="acc">●</span> <span class="dim">○ ○</span></div>''')
for n, img, note in [(2, 'op2.png', '구조구급 PPT 2번 그대로'), (3, 'op3.png', '구조구급 PPT 3번 · 🎬 국무회의 영상 2:44'),
                     (4, 'op4.png', '강사 소개 1 — 실제 PPT는 워크숍판(10.12)'), (5, 'op5.png', '강사 소개 2 — 실제 PPT는 워크숍판(10.12)')]:
    slide(n, f'<img class="a" src="{img}" style="left:0;top:0;width:1920px;height:1080px;object-fit:cover"><div class="note">{note}</div>')
slide(6, head('CONTENTS', '오늘의 순서', 'Contents.', '오늘 이야기할 세 가지') + cards([
    ('01 · 농골길', '문제를 데이터로', '사고 · 239개 마을 전수조사 · 책자 마을 지면 · 2025 현지적응훈련 · 적극행정 최우수'),
    ('02 · AI 농골길 코치', '데이터를 훈련으로', '직장훈련 공모전 제안서 · GPTs · 한계와 웹 · 훈련 평가표 · 실측 · 환류'),
    ('03', '조직과 관할로', '언론 12건 · 18개 소방서 확산 · 간부의 훈련 설계 캔버스 · Q&A')], top=300, h=520, hi=1, fs=50))

# ───────── 1-2 사례 한눈에
slide(7, head('PART 1 · 사례', '무엇을 받았나', 'Award.', '같은 사업, 두 번의 최우수') + '''
<div class="card hi" style="left:110px;top:300px;width:830px;height:480px;padding:50px 54px">
<div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.15em">2025. 9. · 경상남도</div>
<div style="font-size:48px;font-weight:900;margin:22px 0 10px;line-height:1.3">상반기 적극행정<br>우수공무원</div><div style="font-size:96px;font-weight:900;color:#ff5a1f">최우수 <span style="font-size:56px">1위</span></div>
<div class="body" style="font-size:28px;margin-top:10px">농촌마을 골든타임 길라잡이 — 전수조사 · 책자 · 훈련</div></div>
<div class="card hi" style="left:980px;top:300px;width:830px;height:480px;padding:50px 54px">
<div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.15em">2025. 12. · 소방청</div>
<div style="font-size:48px;font-weight:900;margin:22px 0 10px;line-height:1.3">직장훈련<br>우수 운영사례</div><div style="font-size:96px;font-weight:900;color:#ff5a1f">최우수 <span style="font-size:56px">소방청장상</span></div>
<div class="body" style="font-size:28px;margin-top:10px">AI 농골길 코치 — 농촌 소방 AI 지능형 훈련 시스템</div></div>''' + key('하나의 문제를 끝까지 붙잡으면 — 행정 평가와 훈련 평가 둘 다에서 인정받는다'))
tl = [("'24.8.", '부림 신반리 화재 사망 1'), ("'25.2.", '239개 마을 전수조사'), ("'25.6.", '책자 267쪽 발간'), ("'25.9.", '적극행정 최우수'),
      ("'25.하", 'GPTs 자체 구축'), ("'25.12.", '직장훈련 최우수'), ("'26.3.", '전 대원 GPTs 교육'), ("'26.5.", '18개 소방서 시행계획'), ("'26.7.", 'AI 기반 훈련'), ("'26.10.", '농골길 웹')]
tlh = '<div class="a" style="left:110px;top:520px;width:1700px;height:3px;background:#ff5a1f"></div>' + ''.join(
    f'<div class="a" style="left:{120+i*188}px;top:508px;width:26px;height:26px;border-radius:50%;background:{"#ff5a1f" if i in (3,5) else "#55504c"}"></div>'
    f'<div class="a" style="left:{100+i*188}px;top:{430 if i%2==0 else 570}px;width:180px"><div class="acc" style="font-size:26px;font-weight:800">{d}</div>'
    f'<div style="font-size:26px;font-weight:800;line-height:1.3;margin-top:6px">{t}</div></div>' for i, (d, t) in enumerate(tl))
slide(8, head('PART 1 · 사례', '2024 ~ 2026', 'Timeline.', '2년, 한 줄로 보기') + tlh + key('사고 → 데이터 → 도구 → 훈련 → 확산, 한 번도 끊기지 않았다'))
nums = [('239', '개 마을', '전수조사'), ('59', '개소', '중점관리대상'), ('267', '쪽', '책자 · 65부'), ('166', '건', '2025 현지적응훈련'), ('73', '건', '2025 숙지도 평가'), ('80.3', '점', '2026.9. 12개 팀 평균')]
slide(9, head('PART 1 · 사례', '숫자로 본 사업', 'Number.', '숫자로 본 2년') + ''.join(
    f'<div class="card{" hi" if i==5 else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*330}px;width:550px;height:300px;padding:40px 44px">'
    f'<div style="font-size:110px;font-weight:900;line-height:1;color:{"#ff5a1f" if i==5 else "#f4f4f2"}">{a}<span style="font-size:40px">{b}</span></div>'
    f'<div class="body" style="font-size:30px;margin-top:24px">{c}</div></div>' for i, (a, b, c) in enumerate(nums)))
slide(10, head('PART 1 · 사례', '오늘 간부 여러분께', 'For you.', '오늘 가져가실 세 가지') + cards([
    ('01', '훈련 대상을<br>데이터로 고르는 법', '전수조사 항목 · 선정 기준(호스 8매 · 진입불가 5개소 · 센터장 판단)'),
    ('02', '훈련을<br>평가표로 재는 법', '5항목 × 20점 · 숙련 기준 · 실측 소요시간 · 디브리핑 → 데이터 수정'),
    ('03', '조직 밖까지<br>넓히는 법', '군청 협의 · 주민참여예산 · 도 시행계획 · 18개 소방서')], top=300, h=480, hi=1, fs=46))

# ───────── 1-3 제안서 한 쪽씩
def page_full(no, n, title, pts, img=None):
    img = img or f'jth-{n}.png'
    slide(no, f'<div class="tag"><b>PART 1 · 제출 제안서</b>  <span>{n} / 5쪽</span></div><div class="ghost">Paper {n}.</div>'
          + shot(img, 110, 70, 660, 934, paper=True) + sq(818, 222)
          + f'<div class="a" style="left:860px;top:230px;font-size:64px;font-weight:900;letter-spacing:-.03em;line-height:1.2;width:950px">{title}</div>'
          + '<div class="a body" style="left:860px;top:450px;width:950px;font-size:32px;line-height:1.75">' + ''.join(f'<div>· {p}</div>' for p in pts) + '</div>'
          + '<div class="a cap" style="left:860px;top:930px;font-size:22px">소방공무원 직장훈련 우수 운영사례 제안서 (2025. 11. 제출)</div>')
def page_zoom(no, n, img, title, sub, msg):
    slide(no, head('PART 1 · 제출 제안서', f'{n}쪽 확대', 'Zoom.', title)
          + shot(img, 110, 280, 1150, 640, paper=True)
          + f'<div class="card hi" style="left:1300px;top:280px;width:510px;height:640px;padding:44px 40px"><div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.15em">짚을 곳</div>'
          + f'<div style="font-size:38px;font-weight:900;margin:18px 0 22px;line-height:1.35">{sub}</div><div class="body" style="font-size:28px;line-height:1.6">{msg}</div></div>')
# (제출 제안서 11~20장은 PART 2로 이동)

# ───────── 1-4 사고와 통계
intro(11, '01', '농골길 —', '문제를 데이터로', '농촌마을 골든타임 길라잡이: 한 번의 사고, 239개 마을, 267쪽의 책', ['사망 1명', '239개 마을', '전수조사', '중점 59개소', '267쪽', '적극행정'])
slide(12, '''<div class="tag"><b>PART 1 · 질문</b>  <span>여러분께 먼저</span></div><div class="ghost">Question.</div>
<div class="a cap" style="left:150px;top:300px;font-size:40px">여러분 안전센터 관할에서</div>''' + sq(108, 362, 70) + '''
<div class="a" style="left:150px;top:380px;font-size:104px;font-weight:900;letter-spacing:-.04em;line-height:1.25">소방차가 가장 늦게 닿는<br><span class="acc">마을은 어디입니까?</span></div>
<div class="a" style="left:150px;top:760px"><span class="chip">좁은 진입로</span><span class="chip">원거리 마을</span><span class="chip">섬 · 산간</span><span class="chip">전통시장 · 공단</span></div>''')
ev = [("'24. 2. 8.", '낙서면 정곡리', '부상 1'), ("'24. 6. 13.", '정곡면 중교리', '부상 1'), ("'24. 7. 15.", '정곡면 예둔리', '부상 1'), ("'24. 8. 11.", '부림면 신반리', '사망 1')]
slide(13, head('PART 1 · 계기', '2024년 의령군 화재 인명피해', 'Start.', '2024년, 네 번의 인명피해')
      + '<div class="a" style="left:110px;top:464px;width:1700px;height:3px;background:#ff5a1f"></div>' + ''.join(
          f'<div class="a" style="left:{170+i*435}px;top:452px;width:26px;height:26px;border-radius:50%;background:{"#ff5a1f" if i==3 else "#55504c"}"></div>'
          f'<div class="a" style="left:{130+i*435}px;top:380px;font-size:28px;font-weight:800">{d}</div>'
          f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*435}px;top:520px;width:400px;height:260px;padding:36px 34px"><div style="font-size:38px;font-weight:900">{p}</div>'
          f'<div style="font-size:{72 if i==3 else 52}px;font-weight:900;margin-top:20px;color:{"#ff5a1f" if i==3 else "#d6d2c9"}">{h}</div></div>' for i, (d, p, h) in enumerate(ev))
      + key('"현장 활동의 어려움이 인명피해로 직결되는 양상" — 2025 결과보고'))
rows = [('2022', '55건', '32건', '3명', '0'), ('2023', '71건', '23건', '3명', '0'), ('2024', '73건', '25건', '4명', '1')]
t = '<tr><th>연도</th><th>화재</th><th>주거화재</th><th>인명피해</th><th>사망</th></tr>' + ''.join(
    f'<tr style="{"color:#ff5a1f;font-weight:900" if r[0]=="2024" else ""}">' + ''.join(f'<td style="font-size:44px">{c}</td>' for c in r) + '</tr>' for r in rows)
slide(14, head('PART 1 · 계기', '의령군 최근 3년 화재 · 인명피해', 'Data.', '숫자로 본 3년') + f'<div class="a" style="left:110px;top:300px;width:1700px"><table>{t}</table></div>'
      + '<div class="a cap" style="left:110px;top:760px;font-size:24px">출처: 2025 농촌마을 골든타임 길라잡이 결과보고(의령소방서 현장대응단-11301)</div>')
slide(15, head('PART 1 · 정리', '사고 이전의 출동', 'Summary.', '그때까지 우리는') + cards([
    ('01', '출동 중 차 안에서<br>구두로 확인', '책자도 지도도 없이 "그 마을 어디로 들어가더라?"'),
    ('02', '경험자가 있으면 빠르고<br>없으면 늦었다', '판단 속도가 사람에 따라 갈림'),
    ('03', '인사이동 한 번이면<br>처음부터 다시', '지역 숙지가 조직에 남지 않음')], h=400, hi=2, fs=40) + key('판단이 기억에 달려 있었다'))
t = '<tr><th>부서</th><th>관할 읍면</th><th>마을</th></tr>' + ''.join(f'<tr><td>{a}</td><td class="body" style="font-size:28px">{b}</td><td style="font-weight:900">{c}</td></tr>' for a, b, c in [
    ('의령센터', '의령읍 · 화정 · 칠곡 · 대의', '76'), ('구조대', '용덕 · 가례', '34'), ('정곡센터', '정곡 · 지정 · 유곡', '57'), ('부림센터', '낙서 · 부림 · 봉수 · 궁류', '72')])
slide(16, head('PART 1 · 계기', '관할 구조', 'Area.', '4개 부서, 13개 읍면, 239개 마을') + f'<div class="a" style="left:110px;top:300px;width:1000px"><table>{t}</table>'
      + '<div style="font-size:44px;font-weight:900;margin-top:24px">합계 <span class="acc">239</span>개 행정마을</div></div>'
      + shot('map239.png', 1160, 280, 650, 680))

# ───────── 1-5 전수조사
slide(17, head('PART 1 · 전수조사', "추진계획 · 현장대응단-1016('25.2.6.)", 'Plan.', '무엇을 조사할지부터 정했다') + shot('rep010.png', 110, 280, 520, 690, paper=True) + shot('rep011.png', 650, 280, 520, 690, paper=True)
      + '<div class="a" style="left:1220px;top:290px;width:590px"><div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.15em">필수 조사 항목</div>'
      + '<div class="body" style="font-size:31px;line-height:1.7;margin-top:18px">① 소방차 진입 도로 폭<br>② 진입 가능 지점 ~ 최원거리 가구 거리 · 필요 호스 매수<br>③ 인근 소화전 · 주요 대상물<br>④ 그 밖에 현장활동에 필요한 사항</div>'
      + '<div class="cap" style="font-size:24px;margin-top:30px">▲ 왼쪽: 추진계획 공문 · 오른쪽: 지리조사 서식</div></div>')
slide(18, head('PART 1 · 전수조사', '2025. 2.~5. 현장조사', 'Survey.', '239개 마을을 직접 걸었다') + grid([('rep012.png', '현장조사 — 진입로 실측'), ('rep013.png', '현장조사 — 골목 확인'), ('m10.jpeg', '진입로 · 골목 폭'), ('m4.jpeg', '최심부까지 거리'), ('m6.jpeg', '마을 내부 확인'), ('m8.jpeg', '진입 가능 지점')], cols=3))
slide(19, head('PART 1 · 전수조사', '진입불가 구간 기록', 'Record.', '못 들어가는 곳을 사진으로 남겼다') + grid([('bulga1.png', '불가1 · 도로폭 1.4m'), ('bulga2.png', '불가2 · 도로폭 2.2m'), ('m5.jpeg', '좁은 골목'), ('m9.jpeg', '마을 최심부 방향')], cols=2))
slide(20, head('PART 1 · 전수조사', "TF 구성 · 현장대응단-3655('25.4.30.)", 'TF.', 'TF 18명이 기준을 만들었다') + shot('rep014.png', 110, 280, 520, 690, paper=True) + shot('rep016.png', 660, 280, 1150, 430, 'TF 회의')
      + '<div class="a body" style="left:660px;top:740px;width:1150px;font-size:30px;line-height:1.7">· 지휘조사 6 + 각 센터·구조대 3 — <b class="acc">18명</b><br>· 1차 TF: 지도 내용 수정·통일, 기본 틀 / 2차 TF: 중점대상 선정 기준, 지도별 수정</div>')
slide(21, head('PART 1 · 전수조사', '중점관리대상 선정', 'Criteria.', '중점관리대상 59개소, 이렇게 골랐다') + cards([
    ('기준 01', '최심부 필요 호스<br><span class="acc">8매 이상</span>', '차를 세운 곳에서 마지막 집까지 호스로 몇 매?'),
    ('기준 02', '진입불가 지역<br><span class="acc">5개소 이상</span>', '마을 안에 차가 못 들어가는 지점이 몇 곳?'),
    ('기준 03', '센터장 판단', '애로사항 가능성이 높은 지역 — 숫자로 못 잡는 현장 감각')], h=420, hi=0, fs=44)
      + '<div class="a body" style="left:110px;top:770px;font-size:30px">1차 심사: 각 센터장 → 2차 심사: 현장대응단장 · 지휘조사팀 → <b class="acc">59개소</b></div>' + key('간부가 정하는 선정 기준이 곧 그해의 훈련 대상이다'))
slide(22, head('PART 1 · 전수조사', '조사 결과를 담는 틀', 'Layer.', '마을 하나 = 4줄의 데이터') + cards([
    ('01', '식별', '마을명 · 위치 · 도로명주소'), ('02', '실측', '도로폭 · 진입곤란 지점까지 거리 · 소화전 거리'),
    ('03', '판정', '차량별 진입 가부 — 펌프 · 물탱크 · 구급 · 굴절'), ('04', '전술', '최심부 필요 호스 · 대체 진입로 · 부서 위치')], h=440, hi=2, fs=60) + key('이 4줄이 책자의 한 쪽이 되고, 나중에 AI의 재료가 된다'))
slide(23, head('PART 1 · 책자', '2025. 6. 발간', 'Book.', '그렇게 만든 267쪽의 책') + shot('rep025.png', 110, 280, 480, 640, paper=True) + shot('rep026.png', 610, 280, 480, 640, paper=True)
      + '''<div class="a" style="left:1140px;top:290px;width:670px"><div style="display:flex;gap:40px"><div style="font-size:120px;font-weight:900;color:#ff5a1f;line-height:1">267<span style="font-size:48px">쪽</span></div>
<div style="font-size:120px;font-weight:900;line-height:1">65<span style="font-size:48px">부</span></div></div>
<div class="body" style="font-size:31px;line-height:1.8;margin-top:36px">· 마을별 항공사진 · 입체 약도<br>· 진입불가 구간 우회 전술지도<br>· 최원거리 방수선 전개요령<br>· 전 차량·지휘관 배부 + 단말기 저장<br>· 제작 515만 원 · 경남기록원 발간등록번호</div></div>''')


# ───────── 1-5b 책자 마을 (2026 개정판 실제 지면)
stat = [('225', '개 마을', '2026 책자 본편'), ('61', '곳', '펌프차 진입 가능 (27%)'), ('42', '곳', '펌프 · 물탱크 · 구급 모두 진입 불가'), ('57', '곳', '최심부 호스 8매 이상'), ('5.6', '매', '최심부 필요 호스 평균'), ('37', '매', '최대 — 낙서면 아근마을')]
slide(24, head('PART 1 · 책자', '2026 개정판 225개 마을 데이터', 'Data.', '책자 225개 마을을 숫자로 보면') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*330}px;width:550px;height:300px;padding:40px 44px">'
    f'<div style="font-size:110px;font-weight:900;line-height:1;color:{"#ff5a1f" if i==2 else "#f4f4f2"}">{a}<span style="font-size:40px">{b}</span></div>'
    f'<div class="body" style="font-size:30px;margin-top:24px">{c}</div></div>' for i, (a, b, c) in enumerate(stat))
    + '<div class="a cap" style="left:110px;top:985px;font-size:22px">출처: 2026 농촌마을 골든타임 길라잡이(의령소방서 현장대응단, 2026. 6.) 본편 225개 마을 집계</div>')
def ox(v):
    if v is None: return '<span style="color:#8a847e">-</span>'
    return f'<b style="color:{"#2fbf5b" if v=="O" else "#ff4d4f"}">{v}</b>'
def village(no, img, name, area, page, hose, gon, car, why, ghost='Village.'):
    rows = ''.join(f'<span style="display:inline-block;margin-right:26px">{k} {ox(v)}</span>' for k, v in zip(['펌프', '물탱크', '구급', '굴절'], car))
    slide(no, f'<div class="tag"><b>PART 1 · 책자 마을</b>  <span>2026 개정판 {page}쪽</span></div><div class="ghost">{ghost}</div>'
          + shot(img, 110, 70, 660, 934, paper=True) + sq(818, 182)
          + f'<div class="a" style="left:860px;top:190px;font-size:84px;font-weight:900;letter-spacing:-.04em">{name}</div>'
          + f'<div class="a body" style="left:860px;top:300px;font-size:34px">{area}</div>'
          + f'<div class="card" style="left:860px;top:380px;width:950px;height:400px;padding:34px 40px;font-size:30px;line-height:1.55">'
          + f'<div class="cap" style="font-size:22px;letter-spacing:.1em">진입곤란</div><div style="margin-bottom:16px">{gon}</div>'
          + f'<div class="cap" style="font-size:22px;letter-spacing:.1em">차량 진입 가부</div><div style="margin-bottom:16px;font-size:32px">{rows}</div>'
          + f'<div class="cap" style="font-size:22px;letter-spacing:.1em">최심부 필요 호스</div><div style="font-size:56px;font-weight:900;color:#ff5a1f">{hose}<span style="font-size:30px">매</span></div></div>'
          + f'<div class="a" style="left:860px;top:820px;width:950px;padding:20px 28px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:30px;font-weight:700">{why}</div>')
village(25, 'bk213-213.png', '무곡마을', '정곡면 법정로6길 92-1', 213, 4, '진입곤란 1: 회관에서 약 113m · 진입곤란 2: 약 181m', ['X', 'X', 'X', 'X'], '기준 사례 — 도로폭 1.4m · 2.2m, 소화전 587m')
slide(26, head('PART 1 · 책자 마을', '무곡마을 위성지도(2025판 220쪽)', 'Map.', '한 장의 지도에 담긴 것') + shot('p220_sat.png', 110, 290, 1180, 666)
      + shot('bulga1.png', 1330, 290, 480, 300, '불가1 · 도로폭 약 1.4m').replace('<img src="bulga1.png">', '<img src="bulga1.png" style="object-fit:contain;background:#000">')
      + shot('bulga2.png', 1330, 640, 480, 280, '불가2 · 도로폭 약 2.2m').replace('<img src="bulga2.png">', '<img src="bulga2.png" style="object-fit:contain;background:#000">'))
village(27, 'bk15-015.png', '가미마을', '용덕면 가미리 덕암로9길 20', 15, 16, '마을 입구에서 약 <b class="acc">3m</b> 지점까지만 차량 진입 가능', ['X', 'X', 'X', 'X'], '입구부터 막힌다 — 4개 차종 모두 진입 불가, 호스 16매')
village(28, 'bk51-051.png', '아근마을', '낙서면 내제로3길 13', 51, 37, '마을 내 진입 가능하나 이후 커브길 등 대형차량 진입곤란', ['O', 'X', 'O', None], '225개 마을 중 최다 — 최심부까지 호스 <b class="acc">37매</b>')
village(29, 'bk76-076.png', '평촌마을', '가례면 운암리', 76, 30, '마을 입구에서 약 90m 지점까지 차량진입 가능', ['X', 'X', 'O', 'X'], '호스 30매 — 화재피해약자 정보까지 함께 수록')
village(30, 'bk133-133.png', '감암마을', '부림면 미타로1길 19-4', 133, 6, '마을 입구에서 약 1km 지점까지 차량진입 가능', ['X', 'X', 'O', None], '제안서 사진 속 "출동 전술 시뮬레이션"을 한 마을')
village(31, 'bk268-268.png', '수월지장사', '의령읍 중동리 · 특수관리대상', 268, 29, '사찰 입구(의병박물관)에서 약 540m — 경형펌프 · 펌프차 진입 가능', ['O', 'X', 'O', 'X'], '마을만이 아니다 — 사찰 · 산림 인접 대상, 호스 29매', ghost='Special.')
village(32, 'bk270-270.png', '의령전통시장', '의령읍 서동리 · 특수관리대상', 270, 6, '북·남문 도로폭 5m, 서·동문 4.5m — 구간 밖 시장 내부는 장애물로 진입 제한', ['O', 'X', 'O', 'X'], '농촌만이 아니다 — 시장 · 다중이용 대상도 같은 틀로', ghost='Special.')
slide(39, head('PART 1 · 정리', '농골길이 만든 것', 'Summary.', '농골길 = 데이터 · 책 · 훈련 · 협업') + cards([
    ('데이터', '239개 마을', '전수조사 · 4층 구조'), ('책', '267쪽 → 304쪽', '2025 발간 · 2026 개정'), ('훈련', '166건 · 73건', '현지적응훈련 · 숙지도 평가'), ('협업', '1억 원', '군청 · 주민참여예산 · 적극행정 최우수')], h=420, hi=0, fs=48)
    + key('남은 문제 하나 — 이 책을 출동 중 차 안에서 어떻게 꺼내 쓰나?'))

# ───────── 1-6 2025 현지적응훈련
r34 = [('센터', '주 2개 대상', '중점 59개소 순환'), ('지휘조사팀', '월 2회 주관', '센터 합동 · 평가'), ('목표', '접수~도착 7분', '최심부 호스 전개까지'), ('훈련 후', '디브리핑', '결과 분석 · 개선점 도출')]
slide(33, head('PART 1 · 훈련', "현지적응훈련 계획 · 현장대응단-6577('25.7.29.)", 'Rhythm.', '책을 만들고, 훈련으로 돌렸다') + shot('rep028.png', 110, 280, 520, 690, paper=True) + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{660+(i%2)*585}px;top:{280+(i//2)*355}px;width:565px;height:335px;padding:40px 40px">'
    f'<div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.1em">{a}</div><div style="font-size:52px;font-weight:900;margin:16px 0">{b}</div>'
    f'<div class="body" style="font-size:28px">{c}</div></div>' for i, (a, b, c) in enumerate(r34)))
slide(34, head('PART 1 · 훈련', '2025. 8.~12. 현지적응훈련', 'Field.', '골목 끝 마지막 집까지 호스를 폈다') + grid([('m14.jpeg', '최심부 호스 전개'), ('m15.png', '좁은 골목 진입'), ('m16.jpeg', '소화전 점령'), ('rep030.png', '현지적응훈련'), ('rep031.png', '차량 부서 · 대원 배치'), ('m17.jpeg', '훈련 전 브리핑')], cols=3))
slide(35, head('PART 1 · 훈련', '훈련 후', 'Debrief.', '훈련 뒤에는 반드시 디브리핑과 평가') + shot('rep029.png', 110, 280, 520, 690, paper=True) + grid([('m29.jpeg', '디브리핑'), ('m30.jpeg', '팀별 토의'), ('m31.jpeg', '결과 공유'), ('m32.jpeg', '개선점 정리')], x=660, w=1150, cols=2)
      + '<div class="a cap" style="left:110px;top:980px;font-size:22px">▲ 숙지도 평가표(2025)</div>')
mon = [('8월', 22, 77.3), ('9월', 47, 79.6), ('10월', 30, 81.1), ('11월', 44, 84.0), ('12월', 23, 82.0)]
bars = ''.join(f'<div class="a" style="left:{180+i*170}px;top:{860-c*9}px;width:110px;height:{c*9}px;background:{"#ff5a1f" if c==47 else "#55504c"};border-radius:8px 8px 0 0"></div>'
               f'<div class="a" style="left:{180+i*170}px;top:{820-c*9}px;width:110px;text-align:center;font-size:32px;font-weight:900">{c}</div>'
               f'<div class="a cap" style="left:{180+i*170}px;top:880px;width:110px;text-align:center;font-size:26px">{m}</div>' for i, (m, c, s) in enumerate(mon))
line = ''.join(f'<div class="a" style="left:{1080+i*150}px;top:{860-(s-70)*30}px;width:22px;height:22px;border-radius:50%;background:#ff5a1f"></div>'
               f'<div class="a" style="left:{1050+i*150}px;top:{810-(s-70)*30}px;width:90px;text-align:center;font-size:28px;font-weight:900">{s}</div>'
               f'<div class="a cap" style="left:{1050+i*150}px;top:880px;width:90px;text-align:center;font-size:26px">{m}</div>' for i, (m, c, s) in enumerate(mon))
slide(36, head('PART 1 · 훈련', '2025 실적', 'Result.', '5개월, 훈련 166건 · 평가 73건') + bars + line
      + '<div class="a acc" style="left:180px;top:290px;font-size:28px;font-weight:800">월별 훈련 건수 — 합계 166건</div><div class="a acc" style="left:1050px;top:290px;font-size:28px;font-weight:800">숙지도 평가 월평균(100점)</div>'
      + '<div class="a cap" style="left:110px;top:950px;font-size:22px">출처: 2025 현지적응훈련 통합 집계 · 월별 결과보고(현장대응단-7932·8848·10111·11394·693) — 책자·훈련(A사업) 성과</div>')

# ───────── 1-7 적극행정
slide(37, head('PART 1 · 적극행정', '2025 상반기 경상남도 적극행정 우수공무원', 'Proactive.', '세 번의 심사, 최우수 1위') + shot('rep038.png', 110, 280, 760, 570, '2025 상반기 적극행정 우수사례 경진대회') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:910px;top:{280+i*200}px;width:900px;height:180px;padding:28px 36px"><div class="acc" style="font-size:24px;font-weight:800">{a}</div>'
    f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:8px"><div class="body" style="font-size:30px">{b}</div><div style="font-size:52px;font-weight:900;color:{"#ff5a1f" if i==2 else "#f4f4f2"}">{c}</div></div></div>'
    for i, (a, b, c) in enumerate([('1차', '적극행정위원회 서면심사', '10팀'), ('2차', '도민투표 · 직원 설문 · 주민 모니터링단', '5팀'), ("3차 · '25. 9. 23.", '발표 · 현장심사', '최우수 1위')]))
      + '<div class="a cap" style="left:110px;top:880px;font-size:24px;line-height:1.6">🔗 FPN "의령소방서, 적극행정 우수사례 경진대회서 최우수상 수상" · 경남도민일보 "경남도, 상반기 적극행정 우수사례 5건 시상" (원문 링크)</div>')
slide(38, head('PART 1 · 적극행정', '소방서 밖으로', 'Outside.', '군청과 주민까지 움직였다') + grid([('rep034.png', '의령군청 부군수 협의'), ('rep035.png', '소방 4 · 군 4 협의')], y=280, h=380, cols=2) + cards([
    ('협의', '부군수 협의', '중장비 지원 · 곡각지·처마 개선 과제'), ('예산', '주민참여예산 1억 원', '비상소화장치 약 15개소(2026 상반기)'), ('공유', '산청군 주민포럼 발표', '산불 재난 예방 우수 사례')], top=690, h=250, fs=40))
slide(40, '''<div class="tag"><b>PART 1 · END</b>  <span>문제를 데이터로</span></div>
<div class="a" style="left:150px;top:200px;font-size:300px;font-weight:900;letter-spacing:-.05em;line-height:1">End<span class="acc">.</span></div>
<div class="a" style="left:150px;top:560px;font-size:56px;font-weight:900;line-height:1.35">책은 있었다.<br>그런데 <span class="acc">출동 중엔 꺼내 쓸 수 없었다</span></div>
<div class="a" style="left:0;bottom:0;width:1920px;height:120px;background:#ff5a1f;display:flex;align-items:center;padding-left:150px;font-size:34px;font-weight:800">NEXT ▸ PART 2 · AI 농골길 코치 — 데이터를 훈련으로</div>''')

HS = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
for no, html in SL:
    p = os.path.join(OUT, f'v{no:03d}.html')
    open(p, 'w', encoding='utf-8').write(html)
    subprocess.run([HS, '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1920,1080',
                    '--virtual-time-budget=3000', f'--screenshot={os.path.join(OUT, f"v{no:03d}.png")}', 'file://' + p],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('rendered', len(SL))
