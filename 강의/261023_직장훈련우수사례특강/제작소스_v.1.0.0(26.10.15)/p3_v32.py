# 직장훈련특강 PART 3(81~110장) 정지 미리보기 — 기획안 v.3.2.0 기준 (조직과 관할로)
# 사용: python3 p3_v31.py <자료폴더> <출력폴더>   (도우미 함수는 p1_v31.py에서 가져옴)
# 기사 대표 사진: og*.jpg(원문 og:image), 워크숍판 마무리: ws_promo_last.jpg · ws_card.jpg, 도 공문: g_*-1.png, 홍보 영상 프레임: promo_*.jpg
import os, qrcode
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'p1_v31.py'), encoding='utf-8').read()
def part(a, b): return src[src.index(a):src.index(b)]
exec(part('import os, sys', '# ───────── 1-1 오프닝'))

ARTS = [  # (번호, 대표 사진, 언론사, 날짜, 제목, 핵심, 주소) — 사진 없는 기사 · 같은 사진 기사 제외(12건 → 7건)
    (82, 'og1.jpg', 'FPN 소방방재신문', '2025. 9.', '의령소방서, 적극행정 우수사례 경진대회서 최우수상 수상', '2025 상반기 경상남도 적극행정 우수사례 경진대회 최우수', 'http://www.fpn119.co.kr/sub_read.html?uid=240575'),
    (83, 'og2.jpg', '경남도민일보', '2025. 9.', '경남도, 상반기 적극행정 우수사례 5건 시상', '도 단위 경진대회 — 발표 · 현장심사, 최종 5팀 중 최우수', 'https://www.idomin.com/news/articleView.html?idxno=946953'),
    (84, 'og5.jpg', '헤럴드경제', '2026. 3. 23.', '경남·안양·하동·서울 중구, 적극행정 \'최우수\' 기관에 선정', '행안부 2025 지방정부 적극행정 종합평가(243곳) — 경남 최우수', 'https://www.heraldk.com/article/2026032322064737999'),
    (85, 'og6.jpg', '다음(통신사 전재)', '2026. 3. 24.', '경남도, 적극행정 종합평가 전국 \'최우수\'', '"농촌마을 골든타임 길라잡이"가 경남 대표 사례', 'https://v.daum.net/v/20260324163020234'),
    (86, 'og8.jpg', 'FPN 소방방재신문', '2026. 4. 13.', '의령소방서 \'농촌마을 골든타임 길라잡이\', 경남도 적극행정 종합평가 \'최우수\' 견인', '소방서 한 곳의 사업이 도 전체 평가를 끌어올림', 'https://www.fpn119.co.kr/249649'),
    (87, 'og11.jpg', '전국매일신문', '2026. 7. 20.', '의령소방서, 2026년 \'농촌마을 골든타임 길라잡이\' 개정판 발간', '훈련 결과 반영 · 화재피해약자 현황 추가', 'https://www.jeonmae.co.kr/news/articleView.html?idxno=1276072'),
    (88, 'og12.jpg', '노컷뉴스(경남CBS)', '2026. 8. 3.', '\'시골길 소방차 골든타임 단축\'…경남도, 적극행정 \'전국 1위\'', '종합평가 전국 1위 · 대통령 표창 — "농촌 마을 골든타임 길라잡이 사업이 대표적인 적극행정 사례"', 'https://nocutnews.co.kr/news/6557511'),
]
SHORT = {82: '경진대회 최우수', 83: '도 우수사례 시상', 84: '종합평가 최우수', 85: '경남 대표 사례', 86: '최우수 견인', 87: '2026 개정판', 88: '전국 1위 · 대통령 표창'}

def qr(url, name):
    p = os.path.join(OUT, name); qrcode.make(url, border=1).save(p); return name

# 81 모아보기 — 날짜순 한 줄
row = '<div class="a" style="left:110px;top:700px;width:1700px;height:4px;background:linear-gradient(90deg,#ff5a1f,rgba(255,90,31,.2))"></div>' + ''.join(
    f'<div class="a" style="left:{110+i*246}px;top:300px;width:226px">'
    f'<div class="shot" style="position:relative;left:0;top:0;width:226px;height:380px"><img src="{c}"></div>'
    f'<div style="width:18px;height:18px;border-radius:50%;background:#ff5a1f;margin:11px 0 0 104px"></div>'
    f'<div class="acc" style="font-size:24px;font-weight:800;margin-top:26px">{d}</div><div style="font-size:21px;color:#8a847e;margin:4px 0 10px">{m}</div>'
    f'<div style="font-size:27px;font-weight:900;line-height:1.3">{SHORT[n]}</div></div>' for i, (n, c, m, d, t, k, u) in enumerate(ARTS))
slide(81, head('PART 3 · 언론', '기사 7건 — 누르면 원문', 'Press.', '언론이 본 농골길') + row
      + key('도 경진대회 → 행안부 종합평가 → 전국 1위 — 1년 동안 기사가 이어졌다'))
# 82~88 기사 — 대표 사진 크게
for n, c, m, d, t, k, u in ARTS:
    slide(n, head('PART 3 · 언론', f'{m} · {d}', 'Press.', '언론이 본 농골길')
          + f'<div class="shot" style="left:110px;top:280px;width:900px;height:620px"><img src="{c}" style="object-fit:contain;background:#0f0e0e"></div>'
          + '<div class="a cap" style="left:110px;top:915px;font-size:22px">기사 대표 사진 · 사진 · 제목을 누르면 원문이 열립니다</div>'
          + f'<div class="a" style="left:1060px;top:290px;width:750px"><div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.1em">{m}</div>'
          + f'<div class="cap" style="font-size:24px;margin:6px 0 24px">{d}</div><div style="font-size:44px;font-weight:900;line-height:1.3">{t}</div>'
          + f'<div class="body" style="font-size:30px;line-height:1.5;margin-top:30px;padding-left:20px;border-left:5px solid #ff5a1f">{k}</div></div>'
          + f'<img class="a" src="{qr(u, f"qr{n}.png")}" style="left:1060px;top:800px;width:150px;height:150px;background:#fff;padding:6px;border-radius:8px">'
          + f'<div class="a" style="left:1230px;top:820px;width:580px;font-size:22px;color:#8a847e;word-break:break-all">🔗 원문<br><span style="color:#d6d2c9">{u}</span></div>')

# 89 확산 타임라인
tl = [('25. 9.', '도 경진대회', '최우수'), ('25. 12.', '소방청 직장훈련', '최우수 · 도 우수시책 공유'), ('26. 3.', '행안부 종합평가', '경남 최우수'), ('26. 4.', '도 설명회', '40명 참석'),
      ('26. 5.', '18개 소방서', '시행계획'), ('26. 6.', '책자 개정판', '304쪽'), ('26. 8.', '종합평가', '전국 1위 · 대통령 표창')]
slide(89, head('PART 3 · 확산', '1년의 흐름', 'Spread.', '한 소방서의 책이 경남의 표준이 되기까지')
      + '<div class="a" style="left:110px;top:600px;width:1700px;height:4px;background:linear-gradient(90deg,rgba(255,90,31,.25),#ff5a1f)"></div>' + ''.join(
    f'<div class="a" style="left:{110+i*246}px;top:{360 if i%2==0 else 650}px;width:236px">'
    f'<div class="acc" style="font-size:34px;font-weight:900">{d}</div><div style="font-size:30px;font-weight:900;margin:8px 0 6px">{a}</div><div class="body" style="font-size:23px;line-height:1.4">{b}</div></div>'
    f'<div class="a" style="left:{110+i*246}px;top:589px;width:26px;height:26px;border-radius:50%;background:{"#ff5a1f" if i==6 else "#2a2624"};border:4px solid #ff5a1f"></div>' for i, (d, a, b) in enumerate(tl))
      + key('근거는 모두 공문 · 기사 — 도가 먼저 가져가 퍼뜨렸다'))

# 90~94 도 단위 확산
def gong(no, img, sub, title, pts):
    slide(no, head('PART 3 · 확산', sub, 'Spread.', title) + shot(img, 110, 270, 620, 760, paper=True)
          + '<div class="a body" style="left:790px;top:300px;width:1020px;font-size:32px;line-height:1.75">' + ''.join(f'<div>· {p}</div>' for p in pts) + '</div>')
gong(90, 'g_share-1.png', "대응구조구급과-28418('25.12.19.)", '도가 18개 소방서에 공유했다', ['시책명: 농촌마을 골든타임 길라잡이', '주요내용: 책자 제작(진입불가 우회도로 · 호스전개 요령) · 현장대응 훈련 · 군청 협의', '<b class="acc">주요성과: 적극행정 우수사례 · 직장훈련 우수 운영사례</b>', '붙임: 2025 농골길 결과보고'])
gong(91, 'g_brief-1.png', "재난대응과-4810('26.4.14.)", '도 설명회 — 40명이 들으러 왔다', ["일시: '26. 4. 30.(목) 14:00~16:00", '장소: 119특수대응단 3층 회의실', '<b class="acc">대상: 40명(본부 4 · 소방서 36)</b> — 소방서별 업무담당 · 담당자', "근거: '26 지방정부 적극행정 종합평가 경남 \"최우수\" 기관 선정(농·골·길 기여)"])
gong(92, 'g_plan-1.png', "재난대응과-5976('26.5.14.)", '18개 소방서 시행계획 — 경남 표준으로', ['"의령소방서 우수사례를 참고하여 각 소방서별 지역 특성에 맞게 추진"', "기간: '26년 연중 · 대상: 관내 농촌지역 및 소방차 진입장애지역", '<b class="acc">소방서별 자체 계획 수립 → 본부 제출(6. 5.까지)</b>', '관련 자료: 설명회 참석 직원 전원 통합메일 전송'])
steps = [('5~6월', '계획 수립 · 제출', '전 소방서 → 본부'), ('6월', '컨설팅', '필요 시 요청'), ('6~7월', '중간점검', '관서별 추진실적'), ('11~12월', '정보공유 · 설명회', '애로사항 · 지역별 향상 방안')]
slide(93, head('PART 3 · 확산', '시행계획 추진 절차', 'Process.', '한 소방서 → 18개 소방서, 이렇게 관리한다') + ''.join(
    f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*430}px;top:{600-i*90}px;width:405px;height:{300+i*90}px;padding:34px 32px"><div class="acc" style="font-size:28px;font-weight:800">{d}</div>'
    f'<div style="font-size:42px;font-weight:900;margin:14px 0">{t}</div><div class="cap" style="font-size:24px">{c}</div></div>' for i, (d, t, c) in enumerate(steps)))
slide(94, head('PART 3 · 확산', '2026. 6. 개정판', 'Revision.', '책은 해마다 다시 쓴다') + shot('bk26_1-001.png', 110, 280, 480, 680, paper=True) + shot('bk26_3-003.png', 610, 280, 480, 680, paper=True)
      + '<div class="a body" style="left:1140px;top:300px;width:670px;font-size:31px;line-height:1.8"><div style="font-size:110px;font-weight:900;color:#ff5a1f;line-height:1">304<span style="font-size:44px">쪽</span></div>'
      + '<div style="margin-top:30px">· 2025 현지적응훈련 결과 반영<br>· 안전센터 · 구조대가 마을 재방문<br>· <b class="acc">마을별 화재피해약자 현황</b> 추가<br>· 중점 · 일반 · 특수 대상 분류<br>· 225개 마을 + 특수관리대상 20곳</div></div>')

# 95 섹션 인트로
slide(95, '<div class="tag"><b>PART 3 · 간부의 도구</b>  <span>우리 관할로</span></div><div class="ghost">Yours.</div>' + sq(108, 362, 70)
      + '<div class="a" style="left:150px;top:380px;font-size:120px;font-weight:900;letter-spacing:-.045em;line-height:1.2">이제,<br><span class="acc">우리 관할</span> 차례입니다</div>'
      + '<div class="a body" style="left:150px;top:720px;font-size:36px">캔버스 · 선정 기준 · 조사 서식 · 평가표 · 운영 리듬 · 인수인계</div>')
# 96·98·100·102·104~106 간부의 설계 도구
can = [('문제', '사고 · 통계 · 출동 지연 지점'), ('데이터', '무엇을 조사할지 — 도로폭 · 거리 · 호스 · 소화전'), ('대상 선정 기준', '숫자 기준 2개 + 센터장 판단 1개'),
       ('도구', '책자 · 지도 · AI — 출동 중 꺼내 쓸 수 있나'), ('평가표', '행동 문장 · 20점 × 5 · 숙련 구간'), ('환류', '디브리핑 → 데이터 수정 → 재훈련')]
slide(96, head('PART 3 · 간부의 도구', '훈련 설계 캔버스', 'Canvas.', '우리 관할 훈련, 6칸으로 설계한다') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*330}px;width:550px;height:300px;padding:36px 40px"><div class="acc" style="font-size:24px;font-weight:800">0{i+1}</div>'
    f'<div style="font-size:48px;font-weight:900;margin:12px 0 16px">{t}</div><div class="body" style="font-size:27px;line-height:1.5">{d}</div></div>' for i, (t, d) in enumerate(can)))
t = ('<tr><th>구분</th><th>의령(농촌)</th><th>광주 · 전남이라면?</th></tr>' + ''.join(f'<tr><td style="font-weight:800">{a}</td><td class="body">{b}</td><td style="color:#ff5a1f;font-weight:800">{c}</td></tr>' for a, b, c in [
    ('숫자 기준 1', '최심부 호스 8매 이상', '섬 — 선착장~최심부 거리 · 도선 시간'), ('숫자 기준 2', '진입불가 5개소 이상', '산간 — 임도 폭 · 회차 가능 지점'),
    ('특수 대상', '사찰 · 전통시장', '공단 · 고층 · 전통시장 · 요양시설'), ('판단', '센터장 판단', '센터장 판단(그대로)')]))
slide(98, head('PART 3 · 간부의 도구', '대상 선정 기준 만들기', 'Criteria.', '기준은 관할마다 다르게 만든다') + f'<div class="a" style="left:110px;top:290px;width:1700px"><table>{t}</table></div>' + key('기준을 숫자로 적어 두면, 사람이 바뀌어도 훈련 대상은 남는다'))
tmpl = [('항목 이름', '예) AI 정보 분석'), ('관찰 문장', '예) 출동 중 차량 안에서 AI에 접속했는가'), ('배점', '20점 — 5항목이면 100점'), ('숙련 구간', '80↑ 숙련 · 70~79 보통 · 50~69 미흡'), ('대조 항목', '예측(AI·책자) vs 실제(전개 매수 · 시간)')]
slide(100, head('PART 3 · 간부의 도구', '평가표 한 줄 만들기', 'Template.', '평가표 한 줄은 이렇게 쓴다') + ''.join(
    f'<div class="card{" hi" if i==4 else ""}" style="left:110px;top:{280+i*135}px;width:1700px;height:115px;padding:0 40px;display:flex;align-items:center;gap:40px">'
    f'<div class="acc" style="font-size:30px;font-weight:900;width:260px">{a}</div><div style="font-size:32px;font-weight:700">{b}</div></div>' for i, (a, b) in enumerate(tmpl)))
t = '<tr><th>주기</th><th>누가</th><th>무엇을</th></tr>' + ''.join(f'<tr><td style="font-weight:800">{a}</td><td class="body">{b}</td><td>{c}</td></tr>' for a, b, c in [
    ('주 2회', '안전센터', '중점 대상 순환 현지적응훈련'), ('월 2회', '지휘조사팀', '주관 합동훈련 · 숙지도 평가'), ('회차마다', '훈련 참여 전원', '디브리핑 → 데이터 수정'), ('연 1회', '현장대응단', '책자 · 데이터 개정, 대상 재선정')])
slide(102, head('PART 3 · 간부의 도구', '운영 리듬', 'Rhythm.', '훈련은 리듬으로 굴러간다') + f'<div class="a" style="left:110px;top:290px;width:1700px"><table>{t}</table></div>' + key('리듬이 정해지면 담당자가 바뀌어도 훈련이 멈추지 않는다'))
slide(104, '''<div class="tag"><b>PART 3 · 토의</b>  <span>5분</span></div><div class="ghost">Talk.</div>''' + sq(108, 312, 70) + '''
<div class="a" style="left:150px;top:330px;font-size:96px;font-weight:900;letter-spacing:-.04em;line-height:1.25">옆 사람과 5분,<br><span class="acc">우리 관할 중점 대상 1곳</span></div>
<div class="a body" style="left:150px;top:640px;font-size:38px;line-height:1.6">① 어디인가 &nbsp; ② 왜 늦어지나(숫자로) &nbsp; ③ 선정 기준 한 줄</div>''')
slide(105, '''<div class="tag"><b>PART 3 · 발표</b>  <span>2~3명</span></div><div class="ghost">Share.</div>''' + sq(108, 362, 70) + '''
<div class="a" style="left:150px;top:380px;font-size:110px;font-weight:900;letter-spacing:-.04em;line-height:1.25">광주 한 분,<br><span class="acc">전남 한 분</span></div>
<div class="a body" style="left:150px;top:690px;font-size:36px">강사 피드백 — 의령 사례의 어떤 칸을 가져가면 될지</div>''')
slide(106, head('PART 3 · 정리', '데이터가 움직인 것', 'Impact.', '데이터 한 장이 조직을 움직였다') + ''.join(
    f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*430}px;top:320px;width:405px;height:440px;padding:40px 34px"><div class="acc" style="font-size:24px;font-weight:800">{a}</div>'
    f'<div style="font-size:44px;font-weight:900;margin:16px 0;line-height:1.25">{b}</div><div class="body" style="font-size:26px;line-height:1.5">{c}</div></div>'
    for i, (a, b, c) in enumerate([('군청', '부군수 협의', '곡각지 · 처마 개선 과제'), ('주민', '주민참여예산 1억', '비상소화장치 약 15개소'), ('도', '우수시책 공유 · 설명회', '40명 참석'), ('18개 소방서', '시행계획', '경남 표준 모델')])))
# 97 캔버스 의령판
yr = [('문제', '농촌 화재 출동 지연 — 사망 1명'), ('데이터', '239개 마을 전수조사 — 진입불가 · 호스 매수 · 소화전'), ('대상 선정 기준', '호스 8매↑ · 진입불가 5개소↑ · 센터장 판단'),
      ('도구', '책자(304쪽) · 지도 · AI 농골길 코치'), ('평가표', '숙지도 평가 — 5항목 × 20점'), ('환류', '디브리핑 → 책자 개정판 · 마을 재방문')]
slide(97, head('PART 3 · 간부의 도구', '캔버스 의령판', 'Canvas.', '농골길을 6칸에 넣으면') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*330}px;width:550px;height:300px;padding:36px 40px"><div class="acc" style="font-size:24px;font-weight:800">0{i+1} · {t}</div>'
    f'<div style="font-size:34px;font-weight:800;margin-top:22px;line-height:1.4">{d}</div></div>' for i, (t, d) in enumerate(yr)))
# 99 현장조사 서식 실물
slide(99, head('PART 3 · 간부의 도구', '2025 추진계획 붙임 — 현장조사 서식', 'Survey.', '데이터는 이렇게 모은다') + shot('rep011.png', 110, 270, 760, 740, paper=True)
      + shot('rep012.png', 910, 270, 440, 350) + shot('rep013.png', 1370, 270, 440, 350)
      + '<div class="a body" style="left:910px;top:670px;width:900px;font-size:30px;line-height:1.75">· 조사 항목: 도로 폭 · 진입불가 지점 · 회차 공간 · 소화전 · 최심부 호스 매수<br>· 현장 사진 — 진입로 입구 · 불가 지점 · 차량 부서 위치<br>· <b class="acc">서식을 먼저 정하면 누가 조사해도 같은 데이터</b></div>')
# 101 평가표 실물
slide(101, head('PART 3 · 간부의 도구', '숙지도 평가표 원본', 'Sheet.', '실제 평가표는 이렇게 생겼다') + shot('rep029.png', 110, 270, 900, 740, paper=True)
      + '<div class="a body" style="left:1070px;top:300px;width:740px;font-size:31px;line-height:1.8">· 항목마다 <b>관찰 가능한 행동</b>으로<br>· 점수 → 숙련 구간으로 묶어 보고<br>· 예측(책자 · AI)과 실제(전개 매수 · 시간)를 같이 기록<br>· <b class="acc">평가표가 다음 훈련 대상을 고른다</b></div>')
# 103 인수인계 3종
slide(103, head('PART 3 · 간부의 도구', '인수인계', 'Handover.', '담당자가 바뀌어도 훈련은 남는다') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{110+i*575}px;top:320px;width:550px;height:460px;padding:44px 40px"><div class="acc" style="font-size:26px;font-weight:800">0{i+1}</div>'
    f'<div style="font-size:50px;font-weight:900;margin:16px 0 22px">{a}</div><div class="body" style="font-size:29px;line-height:1.55">{b}</div></div>'
    for i, (a, b) in enumerate([('대상 목록', '마을 · 기준 충족 여부 · 우선순위 — 엑셀 한 장'), ('평가표', '항목 · 배점 · 숙련 구간 — 회차별 점수 누적'), ('디브리핑 기록', '예측과 실제의 차이 · 고친 데이터 · 다음 훈련 과제')]))
      + key('세 가지만 넘겨주면, 다음 담당자는 0에서 시작하지 않는다'))

# 107~110 마무리 — 워크숍판(00_AI특강_슬라이드 122~125장)과 같은 구성
slide(107, '<div class="tag"><b>PART 3 · 우리 관서가 할 일</b></div><div class="ghost">Start.</div>' + sq(118, 262, 50)
      + '<div class="a" style="left:130px;top:268px;font-size:48px;font-weight:800">그래서, 우리 관서는?</div>'
      + '<div class="a" style="left:150px;top:350px;font-size:150px;font-weight:900;letter-spacing:-.05em;line-height:1.12">마을 하나부터.<br><span class="acc">기준 한 줄부터.</span></div>' + ''.join(
    f'<div class="card" style="left:{150+i*560}px;top:790px;width:530px;height:140px;padding:26px 32px"><div class="acc" style="font-size:22px;font-weight:800">0{i+1}</div><div style="font-size:36px;font-weight:800;margin-top:8px">{t}</div></div>'
    for i, t in enumerate(['관할 마을 한 곳 조사', '선정 기준 한 줄', '훈련 후 데이터 고치기'])))
slide(108, '<div class="a" style="left:150px;top:110px;font-size:22px;letter-spacing:.3em;color:#8a847e">CLOSING</div><div class="a" style="left:150px;top:160px;width:1620px;height:1px;background:rgba(255,255,255,.15)"></div>'
      + sq(118, 322, 60) + '<div class="a" style="left:140px;top:330px;font-size:92px;font-weight:900;letter-spacing:-.045em;line-height:1.25">데이터는 이미 있었습니다.<br><span class="acc">꺼내 쓸 방법</span>을<br>만든 것뿐입니다</div>'
      + '<div class="a body" style="left:150px;top:790px;font-size:34px;line-height:1.6">훈련은 현장의 문제에서 시작되고,<br>그 변화는 관리자에게서 시작됩니다</div>'
      + '<div class="a" style="left:1360px;top:300px;width:440px;border-left:1px solid rgba(255,255,255,.15);padding-left:40px">' + ''.join(
    f'<div style="padding:22px 0;border-bottom:1px solid rgba(255,255,255,.12)"><div class="acc" style="font-size:24px;font-weight:800">0{i+1}</div><div style="font-size:38px;font-weight:900;margin:6px 0">{a}</div><div class="body" style="font-size:23px">{b}</div></div>'
    for i, (a, b) in enumerate([('농골길', '문제를 데이터로'), ('AI 농골길 코치', '데이터를 훈련으로'), ('확산', '조직과 관할로')])) + '</div>')
slide(109, '<div class="shot" style="left:0;top:0;width:1920px;height:1080px;border:0;border-radius:0"><img src="ws_promo_last.jpg" style="object-fit:contain;background:#000"></div>'
      '<div class="note">🎬 강사 홍보 영상(1:22, 워크숍판과 같은 파일) — 전체화면 자동 재생 → 마지막 장면(명함 · QR)에서 멈춤</div>')
slide(110, sq(108, 222, 80) + '<div class="a" style="left:130px;top:230px;font-size:240px;font-weight:900;letter-spacing:-.05em;line-height:1">Q&amp;A</div>'
      + '<div class="a" style="left:150px;top:460px;font-size:110px;font-weight:900;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.22)">Thank you.</div>'
      + '<div class="a body" style="left:150px;top:620px;font-size:34px;line-height:1.6">궁금하신 점을 편하게 물어봐 주세요<br><b style="color:#fff">현장의 고민, 언제든 함께 나누겠습니다</b></div>'
      + '<div class="a" style="left:150px;top:790px;width:780px">' + ''.join(
    f'<div style="display:flex;gap:60px;padding:12px 0;border-top:1px solid rgba(255,255,255,.12);font-size:28px"><span style="width:90px;letter-spacing:.3em;color:#8a847e;font-size:20px;line-height:40px">{a}</span><b>{b}</b></div>'
    for a, b in [('WEB', 'ssca1612.pages.dev'), ('BLOG', 'blog.naver.com/ai-sobang'), ('MAIL', 'ssca1612@korea.kr')]) + '</div>'
      + '<div class="a" style="left:1000px;top:300px;width:800px;height:540px;border:1px solid rgba(255,255,255,.15);padding:30px;text-align:center">'
      + '<img src="ws_card.jpg" style="width:740px;border-radius:14px"><div class="body" style="font-size:24px;margin-top:20px">QR을 찍으면 수상작 · 강의 자료로 바로 연결됩니다</div></div>')

exec(src[src.index("HS = '/opt"):])
