# 직장훈련특강 PART 1(1~21장) 정지 미리보기 생성기 — 기획안 v.2.4.0 기준
# 사용: python3 part1_preview.py <자료폴더> <출력폴더>
#   자료폴더: PretendardVariable.woff2, bg.png, op2~op5.png(구조구급 PPT 2~5번 장면), map239.png,
#             book_cover.jpg, book_pre.jpg, train2508.jpg, jth-1~4.png(직장훈련 제출본 PDF 쪽)
# 2~5장은 구조구급 PPT(00_AI특강_슬라이드_v.1.8.0) 장면 그대로. 4·5장은 실제 PPT에서 워크숍판(26.10.12)으로 교체
import os, sys, shutil, subprocess

A, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(A):
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
.key{position:absolute;left:110px;bottom:70px;width:1700px;padding:22px 34px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:36px;font-weight:700}
.key b{color:#ff5a1f;font-size:22px;letter-spacing:.2em;margin-right:22px}
.pg{position:absolute;right:110px;bottom:34px;font-size:20px;color:#8a847e;letter-spacing:.1em}
table{border-collapse:collapse;width:100%}td,th{padding:18px 22px;border-bottom:1px solid #3a3533;text-align:left;font-size:32px}
th{color:#8a847e;font-size:22px;letter-spacing:.1em;font-weight:700}
.shot{position:absolute;border-radius:18px;overflow:hidden;border:1.5px solid #3a3533;background:#111}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.chip{display:inline-block;padding:12px 26px;margin:0 14px 14px 0;border:1.5px solid #55504c;border-radius:40px;font-size:28px;font-weight:700;color:#d6d2c9}
.note{position:absolute;left:0;top:0;padding:10px 18px;background:rgba(255,90,31,.92);font-size:20px;font-weight:700;color:#fff}
'''

def sq(x, y, s=40):
    w = max(3, round(s * .06))
    return (f'<svg class="a" style="left:{x}px;top:{y}px" width="{s+w}" height="{s+w}">'
            f'<path d="M{s+w/2},{w/2+s*.25} L{s+w/2},{w/2} L{w/2},{w/2} L{w/2},{s+w/2} L{w/2+s*.3},{s+w/2}" '
            f'fill="none" stroke="#f4f4f2" stroke-width="{w}"/></svg>')

def head(tag, sub, ghost, title):
    return (f'<div class="tag"><b>{tag}</b>  <span>{sub}</span></div><div class="ghost">{ghost}</div>'
            f'{sq(70, 122)}<div class="ttl">{title}</div><div class="hl"></div>')

SL = []
def slide(no, body):
    SL.append((no, f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head>'
                   f'<body><div id="r">{body}<div class="pg">{no}</div></div></body></html>'))

def reuse(no, img, note):
    slide(no, f'<img class="a" src="{img}" style="left:0;top:0;width:1920px;height:1080px;object-fit:cover"><div class="note">{note}</div>')

# 1 표지
slide(1, '''<div class="a acc" style="left:150px;top:150px;font-size:30px;font-weight:800;letter-spacing:.06em">제7기 직장훈련 운영관리자 과정</div>''' + sq(104, 228, 90) + '''
<div class="a" style="left:150px;top:250px;font-size:170px;font-weight:900;letter-spacing:-.045em;line-height:1.05">현장의 문제가<br><span class="acc">훈련</span>이 된다</div>
<div class="a body" style="left:150px;top:640px;font-size:36px">농골길에서 AI 농골길 코치까지 — 적극행정 최우수 · 직장훈련 최우수 사례</div>
<div class="a" style="right:150px;bottom:150px;text-align:right"><div class="cap" style="font-size:28px">2026. 10. 23. · 광주소방학교</div>
<div style="font-size:34px;font-weight:800;margin-top:10px">AI 챔피언(BLACK) 김경훈</div></div>
<div class="a" style="left:150px;bottom:150px;font-size:28px;letter-spacing:.3em"><span class="acc">●</span> <span class="dim">○ ○</span></div>''')

reuse(2, 'op2.png', '구조구급 PPT 2번 그대로')
reuse(3, 'op3.png', '구조구급 PPT 3번 그대로 · 🎬 국무회의 영상 2:44 자동 재생')
reuse(4, 'op4.png', '강사 소개 1 — 실제 PPT는 워크숍판(10.12)으로 교체 (지표 7건·27곳·ONLINE)')
reuse(5, 'op5.png', '강사 소개 2 — 실제 PPT는 워크숍판(10.12)으로 교체')

# 6 목차
toc = [('01', '왜 시작했나', '사고 · 전수조사 · 책자 · 적극행정 최우수'), ('02', '책자를 AI로, 그리고 웹으로', '220쪽 · GPTs · 한계 · 농골길 웹 · 훈련'), ('03', '경남으로, 우리 센터로', '확산 · 실습 · 서류 쓰는 법 · Q&A')]
cards = ''.join(f'<div class="card{" hi" if i==1 else ""}" style="left:{110+i*575}px;top:{330 if i!=1 else 300}px;width:550px;height:{460 if i!=1 else 520}px;padding:46px 44px">'
                f'<div class="{"acc" if i==1 else "dim"}" style="font-size:90px;font-weight:900;line-height:1">{n}</div>'
                f'<div style="font-size:46px;font-weight:900;margin:30px 0 22px;line-height:1.25">{t}</div><div class="body" style="font-size:28px;line-height:1.5">{d}</div>'
                + ('<div class="acc" style="position:absolute;bottom:40px;font-size:22px;font-weight:800;letter-spacing:.2em">MAIN</div>' if i == 1 else '') + '</div>' for i, (n, t, d) in enumerate(toc))
slide(6, head('CONTENTS', '오늘의 순서', 'Contents.', '오늘 이야기할 세 가지') + cards)

# 8 두 번의 수상
slide(8, head('PART 1 · 소개', '무엇을 냈고, 무엇을 받았나', 'Award.', '같은 사업, 두 번의 최우수') + '''
<div class="card hi" style="left:110px;top:310px;width:830px;height:470px;padding:50px 54px">
<div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.15em">2025. 9. · 경상남도</div>
<div style="font-size:48px;font-weight:900;margin:22px 0 10px;line-height:1.3">상반기 적극행정<br>우수공무원</div><div style="font-size:96px;font-weight:900;color:#ff5a1f">최우수 <span style="font-size:56px">1위</span></div>
<div class="body" style="font-size:28px;margin-top:10px">농촌마을 골든타임 길라잡이(책자·훈련)</div></div>
<div class="card hi" style="left:980px;top:310px;width:830px;height:470px;padding:50px 54px">
<div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.15em">2025. 12. · 소방청</div>
<div style="font-size:48px;font-weight:900;margin:22px 0 10px;line-height:1.3">직장훈련<br>우수 운영사례</div><div style="font-size:96px;font-weight:900;color:#ff5a1f">최우수 <span style="font-size:56px">소방청장상</span></div>
<div class="body" style="font-size:28px;margin-top:10px">AI 농골길 코치 — 농촌 소방 AI 지능형 훈련 시스템</div></div>
<div class="key"><b>KEY</b>하나의 문제를 끝까지 붙잡으면, 상은 따라온다</div>''')

# 9 제출 서류 해부
pages = ''.join(f'<div class="shot" style="left:{110+i*300}px;top:{300+(i%2)*30}px;width:280px;height:396px;background:#fff;transform:rotate({[-3,2,-2,3][i]}deg)"><img src="jth-{i+1}.png" style="object-fit:contain"></div>' for i in range(4))
flow = ['추진배경', '운영개요', '세부내용', '성과', '향후 발전', '확산', '사진']
fl = ''.join(f'<div style="display:flex;align-items:center;margin-bottom:14px"><span class="acc" style="font-size:24px;font-weight:800;width:60px">0{i+1}</span><span style="font-size:{34 if i!=2 else 38}px;font-weight:{800 if i!=2 else 900}">{t}</span></div>' for i, t in enumerate(flow))
slide(9, head('PART 1 · 소개', '직장훈련 공모전 제안서 해부', 'Paper.', '실제로 낸 제안서, 이렇게 생겼습니다') + pages +
      f'<div class="a" style="left:1360px;top:290px">{fl}</div>'
      '<div class="a cap" style="left:1360px;top:850px;font-size:24px;line-height:1.5">세부내용 = 해결전략 · 작동 프로세스<br>구축 타임라인 · 보완점 · 차별화</div>'
      '<div class="key"><b>KEY</b>이 순서가 곧 오늘 강의의 순서입니다</div>')

# 11 PART 인트로
slide(11, '''<div class="a" style="left:150px;top:150px;font-size:26px;letter-spacing:.3em"><b style="color:#ff5a1f">PART 01</b></div>
<div class="a" style="right:90px;top:120px;font-size:560px;font-weight:900;color:rgba(255,255,255,.06);line-height:1">01</div>''' + sq(108, 232, 70) + '''
<div class="a" style="left:150px;top:250px;font-size:150px;font-weight:900;letter-spacing:-.045em;line-height:1.08">왜<br><span class="acc">시작했나</span></div>
<div class="a body" style="left:150px;top:610px;font-size:36px">한 번의 사고, 239개 마을, 267쪽의 책</div>
<div class="a" style="left:150px;top:720px;width:1500px"><span class="chip">사망 1명</span><span class="chip">239개 마을</span><span class="chip">전수조사</span><span class="chip">267쪽</span><span class="chip">적극행정</span></div>''')

# 12 질문
slide(12, '''<div class="tag"><b>PART 1 · 질문</b>  <span>여러분께 먼저</span></div><div class="ghost">Question.</div>
<div class="a cap" style="left:150px;top:300px;font-size:40px">여러분 안전센터 관할에서</div>''' + sq(108, 362, 70) + '''
<div class="a" style="left:150px;top:380px;font-size:104px;font-weight:900;letter-spacing:-.04em;line-height:1.25">소방차가 가장 늦게 닿는<br><span class="acc">마을은 어디입니까?</span></div>
<div class="a" style="left:150px;top:760px"><span class="chip">좁은 진입로</span><span class="chip">원거리 마을</span><span class="chip">섬 · 산간</span></div>''')

# 13 사고 타임라인
ev = [("'24. 2. 8.", '낙서면 정곡리', '부상 1'), ("'24. 6. 13.", '정곡면 중교리', '부상 1'), ("'24. 7. 15.", '정곡면 예둔리', '부상 1'), ("'24. 8. 11.", '부림면 신반리', '사망 1')]
dots = ''.join(f'<div class="a" style="left:{170+i*420}px;top:452px;width:26px;height:26px;border-radius:50%;background:{"#ff5a1f" if i==3 else "#55504c"}"></div>'
               f'<div class="a" style="left:{130+i*420}px;top:380px;font-size:28px;font-weight:800" class="{"acc" if i==3 else ""}">{d}</div>'
               f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*420}px;top:520px;width:390px;height:260px;padding:36px 34px">'
               f'<div style="font-size:38px;font-weight:900">{p}</div><div style="font-size:{72 if i==3 else 52}px;font-weight:900;margin-top:20px;color:{"#ff5a1f" if i==3 else "#d6d2c9"}">{h}</div></div>' for i, (d, p, h) in enumerate(ev))
slide(13, head('PART 1 · 계기', '2024년 의령군 화재 인명피해', 'Start.', '2024년, 네 번의 인명피해') +
      '<div class="a" style="left:110px;top:464px;width:1700px;height:3px;background:#ff5a1f"></div>' + dots +
      '<div class="key"><b>KEY</b>"현장 활동의 어려움이 인명피해로 직결되는 양상" — 2025 결과보고</div>')

# 14 3년 화재
rows = [('2022', '55건', '32건', '3명', '0'), ('2023', '71건', '23건', '3명', '0'), ('2024', '73건', '25건', '4명', '1')]
t = '<tr><th>연도</th><th>화재</th><th>주거화재</th><th>인명피해</th><th>사망</th></tr>' + ''.join(
    f'<tr style="{"color:#ff5a1f;font-weight:900" if r[0]=="2024" else ""}">' + ''.join(f'<td style="font-size:44px">{c}</td>' for c in r) + '</tr>' for r in rows)
slide(14, head('PART 1 · 계기', '의령군 최근 3년 화재 · 인명피해', 'Data.', '숫자로 본 3년') +
      f'<div class="a" style="left:110px;top:300px;width:1700px"><table>{t}</table></div>'
      '<div class="a cap" style="left:110px;top:760px;font-size:24px">출처: 2025 농촌마을 골든타임 길라잡이 결과보고(의령소방서 현장대응단-11301)</div>')

# 15 정리
c3 = [('출동 중 차 안에서', '구두로 확인'), ('경험자가 있으면 빠르고', '없으면 늦었다'), ('인사이동 한 번이면', '처음부터 다시')]
cards = ''.join(f'<div class="card{" hi" if i==2 else ""}" style="left:{110+i*575}px;top:320px;width:550px;height:380px;padding:46px 44px">'
                f'<div class="acc" style="font-size:24px;font-weight:800">0{i+1}</div><div class="body" style="font-size:36px;margin:24px 0 10px">{a}</div>'
                f'<div style="font-size:52px;font-weight:900">{b}</div></div>' for i, (a, b) in enumerate(c3))
slide(15, head('PART 1 · 정리', '사고 이전의 출동', 'Summary.', '그때까지 우리는') + cards +
      '<div class="key"><b>KEY</b>판단이 기억에 달려 있었다</div>')

# 16 A사업 계단
st = [("'25. 2. 6.", '추진계획', '현장대응단-1016'), ("'25. 2.~5.", '239개 마을 전수조사', '13개 읍면 · 4개 부서'), ("'25. 4.~5.", 'TF 18명', '중점관리대상 59개소 선정'), ("'25. 6.", '지도부책 발간', '267쪽 · 65부')]
cards = ''.join(f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*300}px;top:{620-i*80}px;width:282px;height:{300+i*80}px;padding:30px 26px">'
                f'<div class="acc" style="font-size:24px;font-weight:800">{d}</div><div style="font-size:34px;font-weight:900;margin:12px 0;line-height:1.3">{t}</div>'
                f'<div class="cap" style="font-size:22px;line-height:1.4">{c}</div></div>' for i, (d, t, c) in enumerate(st))
slide(16, head('PART 1 · 1차 대응', '농촌마을 골든타임 길라잡이(A사업)', 'Survey.', '239개 마을을 직접 걸었다') + cards +
      '<div class="shot" style="left:1340px;top:280px;width:470px;height:640px;background:#000"><img src="map239.png" style="object-fit:contain"></div>'
      '<div class="a cap" style="left:1340px;top:930px;font-size:22px">▲ 의령군 239개 행정마을</div>')

# 17 책자
slide(17, head('PART 1 · 1차 대응', '2025. 6. 발간', 'Book.', '그렇게 만든 267쪽의 책') + '''
<div class="shot" style="left:110px;top:290px;width:470px;height:665px;background:#fff"><img src="book_cover.jpg" style="object-fit:contain"></div>
<div class="shot" style="left:610px;top:290px;width:470px;height:665px;background:#fff"><img src="book_pre.jpg" style="object-fit:contain"></div>
<div class="a" style="left:1140px;top:300px;width:670px">
<div style="display:flex;gap:40px"><div><div style="font-size:120px;font-weight:900;color:#ff5a1f;line-height:1">267<span style="font-size:48px">쪽</span></div></div>
<div><div style="font-size:120px;font-weight:900;line-height:1">65<span style="font-size:48px">부</span></div></div></div>
<div class="body" style="font-size:32px;line-height:1.8;margin-top:40px">· 전 차량 · 지휘관 배부<br>· 차량 단말기에도 저장<br>· 제작비 515만 원<br>· 경남기록원 발간등록번호</div></div>''')

# 18 적극행정 선정 과정
st = [('1차', '적극행정위원회 서면심사', '10팀'), ('2차', '도민투표 · 직원 설문 · 주민 모니터링단', '5팀'), ("3차 · '25. 9. 23.", '발표 · 현장심사', '최우수 1위')]
cards = ''.join(f'<div class="card{" hi" if i==2 else ""}" style="left:{110+i*575}px;top:{560-i*90}px;width:550px;height:{300+i*90}px;padding:40px 40px">'
                f'<div class="acc" style="font-size:26px;font-weight:800">{d}</div><div class="body" style="font-size:34px;margin:16px 0;line-height:1.35">{t}</div>'
                f'<div style="font-size:{86 if i==2 else 70}px;font-weight:900;color:{"#ff5a1f" if i==2 else "#f4f4f2"}">{c}</div></div>' for i, (d, t, c) in enumerate(st))
slide(18, head('PART 1 · 적극행정', '2025 상반기 경상남도 적극행정 우수공무원', 'Proactive.', '세 번의 심사, 최우수') + cards)

# 19 그 밖의 성과
c3 = [('의령군청 협의', '부군수 협의 · 소방 4 · 군 4', '중장비 지원 · 곡각지·처마 개선 과제'), ('주민참여예산', '1억 원 확보', '비상소화장치 약 15개소 (2026 상반기)'), ('산청군 주민포럼', '우수 사례 발표', '산불 재난 예방 포럼')]
cards = ''.join(f'<div class="card{" hi" if i==1 else ""}" style="left:{110+i*575}px;top:320px;width:550px;height:420px;padding:46px 44px">'
                f'<div class="acc" style="font-size:24px;font-weight:800">0{i+1}</div><div class="cap" style="font-size:30px;margin:20px 0 10px">{a}</div>'
                f'<div style="font-size:52px;font-weight:900;line-height:1.2">{b}</div><div class="body" style="font-size:26px;margin-top:22px;line-height:1.45">{c}</div></div>' for i, (a, b, c) in enumerate(c3))
slide(19, head('PART 1 · 정리', '책자 밖으로 넓힌 것', 'Summary.', '소방서 밖까지 움직였다') + cards +
      '<div class="key"><b>KEY</b>훈련은 소방서 안에서 끝나지 않는다 — 군청 · 주민과 함께</div>')

# 20 END
slide(20, '''<div class="tag"><b>PART 1 · END</b>  <span>왜 시작했나</span></div>
<div class="a" style="left:150px;top:200px;font-size:300px;font-weight:900;letter-spacing:-.05em;line-height:1">End<span class="acc">.</span></div>
<div class="a" style="left:150px;top:560px;font-size:56px;font-weight:900;line-height:1.35">데이터는 모았다.<br>그런데 <span class="acc">출동 중엔 꺼내 쓸 수 없었다</span></div>
<div class="a" style="left:0;bottom:0;width:1920px;height:120px;background:#ff5a1f;display:flex;align-items:center;padding-left:150px;font-size:34px;font-weight:800">NEXT ▸ PART 2 · 책자를 AI로, 그리고 웹으로</div>''')

# 21 쉬는 시간
slide(21, '''<div class="a" style="left:0;top:330px;width:1920px;text-align:center;font-size:200px;font-weight:900;letter-spacing:-.04em">쉬는 시간<span class="acc">.</span></div>
<div class="a body" style="left:0;top:600px;width:1920px;text-align:center;font-size:40px">다음은 PART 2 — 책자를 AI로, 그리고 웹으로</div>''')

HS = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
for no, html in SL:
    p = os.path.join(OUT, f'p{no:02d}.html')
    open(p, 'w', encoding='utf-8').write(html)
    subprocess.run([HS, '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1920,1080',
                    '--virtual-time-budget=3000', f'--screenshot={os.path.join(OUT, f"p{no:02d}.png")}', 'file://' + p],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('rendered', len(SL))
