# 직장훈련특강 PART 2(22~39장) 정지 미리보기 생성기 — 기획안 v.2.3.0 기준
# 사용: python3 part2_preview.py <자료폴더> <출력폴더>
#   자료폴더: PretendardVariable.woff2, bg.png, p220.png, p220_sat.png, limit.png, noentry1/2.png,
#             bulga1/2.png(220쪽 위성지도에서 자른 불가1·2 사진), docplan.png(고도화 계획 공문 PDF 1쪽 220dpi), g_hi.jpg(GPTs 영상 60초), w20/w70/w130.jpg(웹 영상 프레임)
# 디자인: PPT디자인시스템_v.1.3.0 (검정·흰색·주황, 사각 장식, 외곽선 영단어, 구분선 y=244)
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
table{border-collapse:collapse;width:100%}td,th{padding:16px 20px;border-bottom:1px solid #3a3533;text-align:left;font-size:28px;vertical-align:top}
th{color:#8a847e;font-size:22px;letter-spacing:.1em;font-weight:700}
.shot{position:absolute;border-radius:18px;overflow:hidden;border:1.5px solid #3a3533;background:#111}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.chip{display:inline-block;padding:12px 26px;margin:0 14px 14px 0;border:1.5px solid #55504c;border-radius:40px;font-size:28px;font-weight:700;color:#d6d2c9}
.play{position:absolute;width:120px;height:120px;border-radius:50%;background:#ff5a1f;display:flex;align-items:center;justify-content:center}
.play:after{content:"";border-left:38px solid #fff;border-top:24px solid transparent;border-bottom:24px solid transparent;margin-left:10px}
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

# 22 PART 인트로
slide(22, '''<div class="a" style="left:150px;top:150px;font-size:26px;letter-spacing:.3em" class="acc"><b style="color:#ff5a1f">PART 02</b></div>
<div class="a" style="right:90px;top:120px;font-size:560px;font-weight:900;color:rgba(255,255,255,.06);line-height:1">02</div>''' + sq(108, 232, 70) + '''
<div class="a" style="left:150px;top:250px;font-size:150px;font-weight:900;letter-spacing:-.045em;line-height:1.08">책자를 AI로,<br>그리고 <span class="acc">웹으로</span></div>
<div class="a body" style="left:150px;top:610px;font-size:36px">데이터는 이미 있었다. 출동 중에 꺼내 쓸 방법을 만들었다.</div>
<div class="a" style="left:150px;top:720px;width:1500px"><span class="chip">90초</span><span class="chip">220쪽</span><span class="chip">GPTs</span><span class="chip">한계</span><span class="chip">농골길 웹</span><span class="chip">최우수</span></div>''')

# 23 책자의 한계
slide(23, head('PART 2 · 문제', '1차 대응의 한계', 'Limit.', '책은 있었다, 출동 중엔 못 꺼냈다') + '''
<div class="shot" style="left:110px;top:300px;width:1060px;height:406px;background:#fff"><img src="limit.png" style="object-fit:contain"></div>
<div class="card hi" style="left:1220px;top:300px;width:590px;height:406px;padding:46px 50px">
<div class="cap" style="font-size:26px">267쪽 책자에서 마을 하나 찾기</div>
<div style="font-size:200px;font-weight:900;line-height:1.05;color:#ff5a1f;letter-spacing:-.05em">90<span style="font-size:80px">초</span></div>
<div class="body" style="font-size:28px;line-height:1.45">책자 65부 · 전 차량 배부<br>차량 단말기에도 저장했지만</div></div>
<div class="key"><b>KEY</b>데이터가 부족한 게 아니라, 전달 방식이 현장과 맞지 않았다</div>''')

# 24 해결 방식 선택
opts = [('책자 보완', '쪽수·색인 개선', '여전히 넘겨서 찾아야 함'), ('외주 개발', '전용 앱 발주', '예산·기간, 수정할 때마다 다시 발주'),
        ('교육 강화', '239개 마을 암기', '인사이동하면 처음부터'), ('GPTs 자체 구축', '마을명 입력 → 정보 출력', '담당자 1인 · 코딩 0줄 · 바로 수정')]
cards = ''.join(f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*432}px;top:300px;width:404px;height:520px;padding:42px 36px">'
                f'<div class="{"acc" if i==3 else "dim"}" style="font-size:24px;font-weight:800;letter-spacing:.15em">0{i+1}</div>'
                f'<div style="font-size:44px;font-weight:900;margin:18px 0 26px">{t}</div><div class="body" style="font-size:30px;line-height:1.4;margin-bottom:26px">{a}</div>'
                f'<div class="{"acc" if i==3 else "cap"}" style="font-size:28px;font-weight:700;line-height:1.4">{b}</div></div>' for i, (t, a, b) in enumerate(opts))
slide(24, head('PART 2 · 선택', '해결 방식 비교', 'Choice.', '사지 않고, 직접 만들었다') + cards +
      '<div class="key"><b>KEY</b>가장 빠르고 싸게 바꿀 수 있는 방법 — 있는 데이터에 AI를 붙인다</div>')

# 25 책자 220쪽 지면
slide(25, '''<div class="tag"><b>PART 2 · 함께 보기</b>  <span>책자 220쪽</span></div><div class="ghost">Page 220.</div>
<div class="shot" style="left:110px;top:80px;width:640px;height:906px;background:#fff"><img src="p220.png" style="object-fit:contain"></div>''' + sq(808, 222) + '''
<div class="a" style="left:850px;top:230px;font-size:92px;font-weight:900;letter-spacing:-.04em;line-height:1.12">무곡마을<br><span class="body" style="font-size:52px;font-weight:700">정곡면 법정로6길 92-1</span></div>
<div class="a body" style="left:850px;top:520px;width:960px;font-size:34px;line-height:1.7">
<div>· 위성지도 위에 <b class="acc">진입곤란 1·2</b>와 부서 위치, 최심부</div>
<div>· 차량별 진입 가부 — 펌프 · 물탱크 · 구급 · 굴절</div>
<div>· 최심부까지 필요 호스 매수, 대체 진입로, 인근 소화전</div></div>
<div class="a cap" style="left:850px;top:860px;font-size:24px">2025 농촌마을 골든타임 길라잡이 220쪽 (총 267쪽 · 65부)</div>''')

# 26 위성지도
slide(26, head('PART 2 · 함께 보기', '220쪽 위성지도', 'Map.', '한 장의 지도에 담긴 것') + '''
<div class="shot" style="left:110px;top:290px;width:1180px;height:666px"><img src="p220_sat.png"></div>
<div class="shot" style="left:1330px;top:290px;width:480px;height:300px"><img src="bulga1.png" style="object-fit:contain;background:#000"></div>
<div class="a cap" style="left:1330px;top:598px;font-size:22px">▲ 불가1 · 도로폭 약 1.4m, 진입 불가</div>
<div class="shot" style="left:1330px;top:640px;width:480px;height:280px"><img src="bulga2.png" style="object-fit:contain;background:#000"></div>
<div class="a cap" style="left:1330px;top:928px;font-size:22px">▲ 불가2 · 도로폭 약 2.2m, 굴곡으로 진입 어려움</div>''')

# 27 4층 구조
lay = [('01', '식별', '마을명 · 위치 · 도로명주소', '정곡면 법정로6길 92-1'), ('02', '실측', '도로폭 · 거리 · 소화전', '1.4m(113m) · 2.2m(181m)<br>부서위치~최심부 45m'),
       ('03', '판정', '차량별 진입 가부', '곤란1 펌프·물탱크·구급·굴절 X<br>곤란2 구급만 O'), ('04', '전술', '호스 · 진입 방식', '호스 4매 이상 · 대체 진입로 없음<br>소화전 정곡-A-36 587m')]
cards = ''.join(f'<div class="card{" hi" if i==2 else ""}" style="left:{110+i*432}px;top:300px;width:404px;height:500px;padding:40px 34px">'
                f'<div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.15em">{n}</div><div style="font-size:64px;font-weight:900;margin:10px 0 14px">{t}</div>'
                f'<div class="cap" style="font-size:26px;margin-bottom:34px">{d}</div><div class="body" style="font-size:30px;line-height:1.5;font-weight:700">{v}</div></div>' for i, (n, t, d, v) in enumerate(lay))
slide(27, head('PART 2 · 함께 보기', '한 쪽에 담긴 4층 구조', 'Layer.', '마을 하나 = 4줄의 데이터') + cards +
      '<div class="key"><b>KEY</b>이 4줄이 그대로 AI의 재료가 됐다</div>')

# 28 KEY 정리
slide(28, '''<div class="tag"><b>PART 2 · 정리</b>  <span>책자에서 AI로</span></div><div class="ghost">Summary.</div>''' + sq(108, 352, 70) + '''
<div class="a" style="left:150px;top:370px;font-size:96px;font-weight:900;letter-spacing:-.04em;line-height:1.25">책 한 쪽을 읽는 일을,<br><span class="acc">마을 이름 하나로</span></div>
<div class="a body" style="left:150px;top:680px;font-size:34px">식별 · 실측 · 판정 · 전술 — 239개 마을 데이터를 GPTs에 학습</div>''')

# 29 GPTs 영상
slide(29, '''<div class="shot" style="left:0;top:0;width:1920px;height:1080px;border:0;border-radius:0"><img src="g_hi.jpg" style="object-fit:contain;background:#000"></div>
<div class="a" style="left:0;top:0;width:1920px;height:1080px;background:rgba(0,0,0,.35)"></div><div class="play" style="left:900px;top:480px"></div>
<div class="a" style="left:110px;bottom:70px;font-size:30px;font-weight:700">🎬 AI 농골길 코치(GPTs) 실제 화면 · 전체화면 자동 재생 · 무음 <span class="cap">(2:48)</span></div>''')

# 30 출력 구조
flow = ['기본 정보', '진입 · 소방 접근', '대체 진입로', '인근 소화전', '비고 · 전술', '근거 자료 표기']
desc = ['마을명 · 위치 · 주소', '최심부 진입 가부 · 호스 매수<br>차량별 진입 가부', '마을 내부 우회로', '코드 · 거리 · 위치', '현장 판단 메모', '어느 자료에서 왔는지<br>(환각 방지)']
cards = ''.join(f'<div class="card{" hi" if i==1 else ""}" style="left:{110+i*287}px;top:330px;width:262px;height:400px;padding:34px 24px">'
                f'<div class="acc" style="font-size:22px;font-weight:800">0{i+1}</div><div style="font-size:36px;font-weight:900;margin:12px 0 22px;line-height:1.2">{t}</div>'
                f'<div class="body" style="font-size:24px;line-height:1.5">{d}</div></div>' for i, (t, d) in enumerate(zip(flow, desc)))
slide(30, head('PART 2 · AI 농골길 코치', 'GPTs 출력 구조', 'Output.', '마을명 하나 → 6블록 답변') + cards +
      '<div class="a cap" style="left:110px;top:770px;font-size:28px">1차: 마을 정보 + 기본 전술 → 필요하면 2차: 차량 배치 · 호스 전개 순서</div>')

# 31 장점과 한계
good = ['마을명 하나로 몇 초 만에 조회', '데이터 바로 수정 — 재인쇄 없음', '담당자 1인 · 코딩 0줄로 구축', '출동 중 단말기 조회 → 팀원에게 전달']
bad = ['출동 시스템은 <b>지번</b>, GPTs는 <b>마을</b> 단위 — 검색이 어렵다', '지도·사진 같은 <b>시각화 자료</b>를 보여 주기 어렵다',
       '<b>음성 입력·출력</b> 불가 — 글자로 묻고 글자로 받는 <b>T2T</b>만', '차량 도착·배치를 <b>텍스트로만</b> 확인 — 직관적이지 않다', '같은 질문에도 답이 흔들릴 때가 있다']
g = ''.join(f'<div style="font-size:30px;line-height:1.45;margin-bottom:22px">· {t}</div>' for t in good)
b = ''.join(f'<div style="font-size:29px;line-height:1.45;margin-bottom:18px">{i+1}. {t}</div>' for i, t in enumerate(bad))
slide(31, head('PART 2 · 써 보니', '장점과 한계', 'Review.', '써 보니 — 좋았던 점, 막힌 점') + f'''
<div class="card" style="left:110px;top:290px;width:640px;height:560px;padding:40px 42px"><div class="dim" style="font-size:24px;font-weight:800;letter-spacing:.2em;margin-bottom:26px">장점</div><div class="body">{g}</div></div>
<div class="card hi" style="left:780px;top:290px;width:1030px;height:560px;padding:40px 46px"><div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.2em;margin-bottom:26px">한계</div>{b}</div>
<div class="a cap" style="left:110px;top:880px;font-size:26px">현장 의견 — "복장 때문에 단말기 조작이 어려움" · "단말기가 한 대뿐" (2026. 8. 디브리핑)</div>''')

# 32 한계 → 웹
steps = [('지번으로 찍힌다', '지번 주소로 검색'), ('텍스트만 나온다', '지도를 띄운다'), ('진입불가를 글로 읽는다', '지도에서 진입불가 구간을 바로 확인'),
         ('전술은 사람이 짠다', '건축물대장 API → 건물 정보 → AI가 전술'), ('배치를 글로 상상한다', '차량별 진입 경로·배치 위치 예상')]
cards = ''.join(f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*345}px;top:{560-i*60}px;width:320px;height:{300+i*60}px;padding:30px 26px">'
                f'<div class="cap" style="font-size:24px;line-height:1.4;text-decoration:line-through;text-decoration-color:#8a847e">{a}</div>'
                f'<div class="acc" style="font-size:40px;margin:14px 0">↓</div><div style="font-size:32px;font-weight:900;line-height:1.35">{c}</div></div>' for i, (a, c) in enumerate(steps))
slide(32, head('PART 2 · 그래서', '한계를 웹에서 푼다', 'Next.', '그래서, 웹으로 만들고 있다') + cards)

# 33 웹 영상
slide(33, '''<div class="shot" style="left:0;top:0;width:1920px;height:1080px;border:0;border-radius:0"><img src="w70.jpg" style="object-fit:contain;background:#000"></div>
<div class="a" style="left:0;top:0;width:1920px;height:1080px;background:rgba(0,0,0,.35)"></div><div class="play" style="left:900px;top:480px"></div>
<div class="a" style="left:110px;bottom:70px;font-size:30px;font-weight:700">🎬 농골길 웹 · 휴대폰 화면 녹화 — 핵심 구간 약 2분 · 무음</div>''')

# 34 라이브 웹
slide(34, head('PART 2 · 라이브', '농골길 웹 직접 접속', 'Live.', '지금 만들고 있는 농골길 웹') + '''
<div class="shot" style="left:110px;top:290px;width:1150px;height:647px"><img src="w20.jpg"></div>
<div class="a" style="left:1300px;top:300px;width:510px">
<div class="acc" style="font-size:24px;font-weight:800;letter-spacing:.15em">LIVE</div>
<div style="font-size:40px;font-weight:900;margin:10px 0 30px">nonggolgil.pages.dev</div>
<div class="body" style="font-size:30px;line-height:1.75">① 지번으로 검색<br>② 지도 · 진입불가 구간<br>③ 건축물 정보 · AI 전술<br>④ 차량별 진입 경로 · 배치</div>
<div class="cap" style="font-size:24px;margin-top:34px">허가 사용자 로그인 · 계속 업그레이드 중</div></div>''')

# 35 직장훈련 최우수
slide(35, head('PART 2 · 훈련으로', '2025. 12.', 'Award.', '직장훈련 우수 운영사례, 최우수') + '''
<div class="card hi" style="left:110px;top:310px;width:1700px;height:300px;padding:50px 60px">
<div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.2em">소방청 · 직장훈련 우수 운영사례</div>
<div style="font-size:84px;font-weight:900;margin-top:16px">최우수 · 소방청장상</div></div>
<div class="a body" style="left:110px;top:670px;font-size:36px;line-height:1.8">· "AI를 통한 신속한 현장대응활동 기반 조성"<br>· "전국 최초 농촌마을 소방 GPTs 개발"</div>
<div class="a cap" style="left:110px;top:870px;font-size:24px">출처: 2025 농골길 결과보고(현장대응단-11301)</div>''')

# 36 2026 — 왼쪽 카드 3개 같은 높이, 오른쪽 공문 크게
st = [("'26. 2. 11.", '고도화 · 활용 증진 계획', '책자 개정 · 용수시설 정밀 좌표'), ("'26. 3. 5.", '전 대원 GPTs 활용 교육', '현장대응단-2515'), ("'26. 7.~", 'AI 기반 현지적응훈련', '현장대응단-7033 · 지휘팀 평가')]
cards = ''.join(f'<div class="card{" hi" if i==2 else ""}" style="left:110px;top:{276+i*243}px;width:560px;height:218px;padding:30px 32px">'
                f'<div class="acc" style="font-size:24px;font-weight:800">{d}</div><div style="font-size:36px;font-weight:900;margin:8px 0 6px">{t}</div>'
                f'<div class="cap" style="font-size:22px">{c}</div></div>' for i, (d, t, c) in enumerate(st))
slide(36, head('PART 2 · 훈련으로', '2026 B사업', 'Train.', '도구를 만들고, 훈련에 넣었다') + cards +
      '<div class="a acc" style="left:688px;top:600px;font-size:44px;font-weight:900">▶</div>'
      '<div class="shot" style="left:740px;top:276px;width:1070px;height:704px;background:#fff;border-radius:12px"><img src="docplan.png" style="object-fit:contain"></div>'
      '<div class="a cap" style="left:740px;top:990px;font-size:22px">▲ 의령소방서 「농촌마을 골든타임 길라잡이 고도화·활용 증진 계획」(2026)</div>')

# 37 평가표
rows = [('AI 정보 분석', '출동 중 『AI 농골길 코치』에 신속히 접속했는가'), ('지도 연동', '소화전·비상소화장치 위치 실시간 공유'),
        ('AI 기반 차량부서', '도로 협소 시 무리한 진입 지양, 분산 부서'), ('전술 검증', '<b class="acc">AI 예측 호스 매수 vs 실제 전개 매수</b> 대조'), ('디브리핑 · 환류', '실측 타임라인과 AI 가이드 대조 → 시스템 수정')]
t = ''.join(f'<tr><td style="width:300px;font-weight:800">{a}</td><td class="body">{b}</td><td class="dim" style="width:110px">20점</td></tr>' for a, b in rows)
slide(37, head('PART 2 · 운영관리자 관점', '농·골·길 고도화 숙지도 평가표', 'Check.', 'AI가 평가 항목이 된 훈련') + f'''
<div class="a" style="left:110px;top:290px;width:1140px"><table>{t}</table></div>
<div class="card hi" style="left:1300px;top:300px;width:510px;height:400px;padding:44px 40px">
<div class="cap" style="font-size:26px">2026. 9. 1회차 · 12개 팀</div>
<div style="font-size:150px;font-weight:900;color:#ff5a1f;letter-spacing:-.05em;line-height:1.1">80.3</div>
<div class="body" style="font-size:30px">평균 점수 · 숙련(80↑) 7개 팀</div></div>
<div class="key"><b>Q</b>여러분 훈련 평가표에 한 줄 넣는다면?</div>''')

# 38 9월 실측
data = [('1팀', '우곡', '39초', '4:30', '1:20', '5:40'), ('1팀', '익구', '43초', '5:10', '3:30', '8:40'), ('1팀', '석곡', '41초', '1:30', '3:20', '4:50'),
        ('2팀', '무하', '47초', '3:50', '2:32', '7:09'), ('2팀', '율리', '44초', '3:11', '2:15', '6:10'), ('2팀', '상촌', '45초', '3:58', '1:50', '6:33'),
        ('3팀', '무중', '37초', '7:01', '1:58', '9:36'), ('3팀', '율리', '35초', '8:55', '0:54', '10:24'), ('3팀', '신기', '40초', '6:58', '1:12', '8:50')]
t = '<tr><th>주관</th><th>마을</th><th>차고탈출</th><th>현장도착</th><th>최심부 호스전개</th><th>총 소요</th></tr>' + ''.join(
    '<tr>' + ''.join(f'<td style="font-size:26px;padding:10px 20px">{c}</td>' for c in r) + '</tr>' for r in data)
slide(38, head('PART 2 · 훈련으로', '2026. 9. 1회차 실측 · 동원 25명 · 차량 8~9대', 'Data.', '마을마다 재 본 시간') + f'''
<div class="a" style="left:110px;top:275px;width:1700px"><table>{t}</table></div>
<div class="a cap" style="left:110px;top:985px;font-size:22px">출처: 9월 1회차 지휘팀 주관 AI 기반 현지적응훈련 결과보고 3건 · 무중마을은 재훈련으로 소요시간 단축</div>''')

# 39 END
slide(39, '''<div class="tag"><b>PART 2 · END</b>  <span>책자를 AI로, 그리고 웹으로</span></div>
<div class="a" style="left:150px;top:200px;font-size:300px;font-weight:900;letter-spacing:-.05em;line-height:1">End<span class="acc">.</span></div>
<div class="a" style="left:150px;top:560px;font-size:56px;font-weight:900;line-height:1.35">만들고 → 훈련하고 →<br>한계를 보고 → <span class="acc">다시 만든다</span></div>
<div class="a" style="left:0;bottom:0;width:1920px;height:120px;background:#ff5a1f;display:flex;align-items:center;padding-left:150px;font-size:34px;font-weight:800">NEXT ▸ PART 3 · 경남으로, 우리 센터로</div>''')

HS = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
for no, html in SL:
    p = os.path.join(OUT, f's{no}.html')
    open(p, 'w', encoding='utf-8').write(html)
    subprocess.run([HS, '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1920,1080',
                    '--virtual-time-budget=3000', f'--screenshot={os.path.join(OUT, f"s{no}.png")}', 'file://' + p],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('rendered', len(SL))
