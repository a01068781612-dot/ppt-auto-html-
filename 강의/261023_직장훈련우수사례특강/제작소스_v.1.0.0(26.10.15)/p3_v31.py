# 직장훈련특강 PART 3(81~110장) 정지 미리보기 — 기획안 v.3.1.0 기준 (조직과 관할로)
# 사용: python3 p3_v31.py <자료폴더> <출력폴더>   (도우미 함수는 p1_v31.py에서 가져옴)
# 기사 캡처: artc*.jpg(헤드리스 크롬으로 원문 화면 캡처), 도 공문: g_*-1.png, 홍보 영상 프레임: promo_*.jpg
import os, qrcode
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'p1_v31.py'), encoding='utf-8').read()
def part(a, b): return src[src.index(a):src.index(b)]
exec(part('import os, sys', '# ───────── 1-1 오프닝'))

ARTS = [  # (번호, 캡처, 언론사, 날짜, 제목, 핵심, 주소)
    (82, 'artc1.jpg', 'FPN 소방방재신문', '2025. 9.', '의령소방서, 적극행정 우수사례 경진대회서 최우수상 수상', '2025 상반기 경상남도 적극행정 우수사례 경진대회 최우수', 'http://www.fpn119.co.kr/sub_read.html?uid=240575'),
    (83, 'artc2.jpg', '경남도민일보', '2025. 9.', '경남도, 상반기 적극행정 우수사례 5건 시상', '도 단위 경진대회 — 최종 5팀 중 최우수', 'https://www.idomin.com/news/articleView.html?idxno=946953'),
    (84, 'artc3.jpg', '내외일보', '2025. 9.', '경남도, 2025 상반기 적극행정 우수사례 경진대회 개최', '발표 · 현장심사로 최종 순위 결정', 'https://www.naewoeilbo.com/news/articleView.html?idxno=2196151'),
    (85, None, '쿠키뉴스', '2025. 12. 31.', '의령소방서, 소방청 직장훈련 우수 운영사례(AI 농골길 코치)', '전국 최초 농촌 소방 훈련에 AI 접목 — 239개 마을 전수조사 데이터로 GPTs 설계', 'https://www.kukinews.com/article/view/kuk202512310207'),
    (86, 'artc5.jpg', '헤럴드경제', '2026. 3. 23.', '경남·안양·하동·서울 중구, 적극행정 \'최우수\' 기관에 선정', '행안부 2025 지방정부 적극행정 종합평가(243곳) — 경남 최우수, 농골길 소개', 'https://www.heraldk.com/article/2026032322064737999'),
    (87, 'artc6.jpg', '다음(통신사 전재)', '2026. 3. 24.', '경남도, 적극행정 종합평가 전국 \'최우수\'', '"농촌마을 골든타임 길라잡이"가 경남 대표 사례', 'https://v.daum.net/v/20260324163020234'),
    (88, 'artc7.jpg', '시사경찰일보', '2026. 3.', '경남도, 적극행정 종합평가 전국 \'최우수\'', '종합평가 5개 항목 · 18개 지표', 'https://www.police112.net/49387'),
    (89, 'artc8.jpg', 'FPN 소방방재신문', '2026. 4.', '의령소방서 \'농촌마을 골든타임 길라잡이\', 경남도 적극행정 종합평가 \'최우수\' 견인', '소방서 한 곳의 사업이 도 전체 평가를 끌어올림', 'https://www.fpn119.co.kr/249649'),
    (90, 'artc9.jpg', '네이트 뉴스', '2026. 4. 13.', '의령소방서 \'적극행정\' 성과…경남 최우수 기관 선정 견인', '포털 메인 노출', 'https://m.news.nate.com/view/20260413n32064'),
    (91, 'artc10.jpg', '의령신문', '2026. 4.', '\'농촌마을 골든타임 길라잡이\' 경남도 적극행정 종합평가 \'최우수\' 견인', '지역 언론 — 주민이 읽는 신문', 'http://m.urnews.co.kr/view.php?idx=103684'),
    (92, 'artc11.jpg', '전국매일신문', '2026.', '의령소방서, 2026년 \'농촌마을 골든타임 길라잡이\' 개정판 발간', '훈련 결과 반영 · 화재피해약자 현황 추가', 'https://www.jeonmae.co.kr/news/articleView.html?idxno=1276072'),
    (93, None, '노컷뉴스(경남CBS)', '2026. 8. 3.', '\'시골길 소방차 골든타임 단축\'…경남도, 적극행정 \'전국 1위\'', '"농촌 마을 골든타임 길라잡이 사업이 대표적인 적극행정 사례로 꼽혔다"', 'https://nocutnews.co.kr/news/6557511'),
]

def qr(url, name):
    p = os.path.join(OUT, name); qrcode.make(url, border=1).save(p); return name

# 81 모아보기
th = ''.join(
    f'<div class="shot" style="left:{110+(i%6)*285}px;top:{290+(i//6)*345}px;width:265px;height:325px">'
    + (f'<img src="{c}" style="object-position:top">' if c else f'<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#1d1a19;font-size:26px;font-weight:800;text-align:center;padding:20px">{m}</div>')
    + f'<div class="lbl" style="font-size:18px"><b class="acc">{n}</b> {m}</div></div>' for i, (n, c, m, d, t, k, u) in enumerate(ARTS))
slide(81, head('PART 3 · 언론', '기사 12건 — 누르면 원문', 'Press.', '언론이 본 농골길') + th
      + '<div class="a cap" style="left:110px;top:990px;font-size:22px">각 장의 기사 화면 · 제목을 누르면 원문이 열립니다(PPT 하이퍼링크)</div>')
# 82~93 기사
for n, c, m, d, t, k, u in ARTS:
    left = (shot(c, 110, 280, 900, 675) if c else
            '<div class="card" style="left:110px;top:280px;width:900px;height:675px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:20px">'
            f'<div style="font-size:44px;font-weight:900">{m}</div><div class="cap" style="font-size:26px">원문 화면은 강의 전날 다시 캡처</div></div>')
    slide(n, head('PART 3 · 언론', f'{m} · {d}', 'Press.', '언론이 본 농골길') + left
          + f'<div class="a" style="left:1060px;top:290px;width:750px"><div class="acc" style="font-size:26px;font-weight:800;letter-spacing:.1em">{m}</div>'
          + f'<div class="cap" style="font-size:24px;margin:6px 0 24px">{d}</div><div style="font-size:44px;font-weight:900;line-height:1.3">{t}</div>'
          + f'<div class="body" style="font-size:30px;line-height:1.5;margin-top:30px;padding-left:20px;border-left:5px solid #ff5a1f">{k}</div></div>'
          + f'<img class="a" src="{qr(u, f"qr{n}.png")}" style="left:1060px;top:800px;width:150px;height:150px;background:#fff;padding:6px;border-radius:8px">'
          + f'<div class="a" style="left:1230px;top:820px;width:580px;font-size:22px;color:#8a847e;word-break:break-all">🔗 원문<br><span style="color:#d6d2c9">{u}</span></div>')

# 94~98 도 단위 확산
def gong(no, img, sub, title, pts):
    slide(no, head('PART 3 · 확산', sub, 'Spread.', title) + shot(img, 110, 270, 620, 760, paper=True)
          + '<div class="a body" style="left:790px;top:300px;width:1020px;font-size:32px;line-height:1.75">' + ''.join(f'<div>· {p}</div>' for p in pts) + '</div>')
gong(94, 'g_share-1.png', "대응구조구급과-28418('25.12.19.)", '도가 18개 소방서에 공유했다', ['시책명: 농촌마을 골든타임 길라잡이', '주요내용: 책자 제작(진입불가 우회도로 · 호스전개 요령) · 현장대응 훈련 · 군청 협의', '<b class="acc">주요성과: 적극행정 우수사례 · 직장훈련 우수 운영사례</b>', '붙임: 2025 농골길 결과보고'])
gong(95, 'g_brief-1.png', "재난대응과-4810('26.4.14.)", '도 설명회 — 40명이 들으러 왔다', ["일시: '26. 4. 30.(목) 14:00~16:00", '장소: 119특수대응단 3층 회의실', '<b class="acc">대상: 40명(본부 4 · 소방서 36)</b> — 소방서별 업무담당 · 담당자', "근거: '26 지방정부 적극행정 종합평가 경남 \"최우수\" 기관 선정(농·골·길 기여)"])
gong(96, 'g_plan-1.png', "재난대응과-5976('26.5.14.)", '18개 소방서 시행계획 — 경남 표준으로', ['"의령소방서 우수사례를 참고하여 각 소방서별 지역 특성에 맞게 추진"', "기간: '26년 연중 · 대상: 관내 농촌지역 및 소방차 진입장애지역", '<b class="acc">소방서별 자체 계획 수립 → 본부 제출(6. 5.까지)</b>', '관련 자료: 설명회 참석 직원 전원 통합메일 전송'])
steps = [('5~6월', '계획 수립 · 제출', '전 소방서 → 본부'), ('6월', '컨설팅', '필요 시 요청'), ('6~7월', '중간점검', '관서별 추진실적'), ('11~12월', '정보공유 · 설명회', '애로사항 · 지역별 향상 방안')]
slide(97, head('PART 3 · 확산', '시행계획 추진 절차', 'Process.', '한 소방서 → 18개 소방서, 이렇게 관리한다') + ''.join(
    f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*430}px;top:{600-i*90}px;width:405px;height:{300+i*90}px;padding:34px 32px"><div class="acc" style="font-size:28px;font-weight:800">{d}</div>'
    f'<div style="font-size:42px;font-weight:900;margin:14px 0">{t}</div><div class="cap" style="font-size:24px">{c}</div></div>' for i, (d, t, c) in enumerate(steps)))
slide(98, head('PART 3 · 확산', '2026. 6. 개정판', 'Revision.', '책은 해마다 다시 쓴다') + shot('bk26_1-001.png', 110, 280, 480, 680, paper=True) + shot('bk26_3-003.png', 610, 280, 480, 680, paper=True)
      + '<div class="a body" style="left:1140px;top:300px;width:670px;font-size:31px;line-height:1.8"><div style="font-size:110px;font-weight:900;color:#ff5a1f;line-height:1">304<span style="font-size:44px">쪽</span></div>'
      + '<div style="margin-top:30px">· 2025 현지적응훈련 결과 반영<br>· 안전센터 · 구조대가 마을 재방문<br>· <b class="acc">마을별 화재피해약자 현황</b> 추가<br>· 중점 · 일반 · 특수 대상 분류<br>· 225개 마을 + 특수관리대상 20곳</div></div>')

# 99~106 간부의 설계 도구
can = [('문제', '사고 · 통계 · 출동 지연 지점'), ('데이터', '무엇을 조사할지 — 도로폭 · 거리 · 호스 · 소화전'), ('대상 선정 기준', '숫자 기준 2개 + 센터장 판단 1개'),
       ('도구', '책자 · 지도 · AI — 출동 중 꺼내 쓸 수 있나'), ('평가표', '행동 문장 · 20점 × 5 · 숙련 구간'), ('환류', '디브리핑 → 데이터 수정 → 재훈련')]
slide(99, head('PART 3 · 간부의 도구', '훈련 설계 캔버스', 'Canvas.', '우리 관할 훈련, 6칸으로 설계한다') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*330}px;width:550px;height:300px;padding:36px 40px"><div class="acc" style="font-size:24px;font-weight:800">0{i+1}</div>'
    f'<div style="font-size:48px;font-weight:900;margin:12px 0 16px">{t}</div><div class="body" style="font-size:27px;line-height:1.5">{d}</div></div>' for i, (t, d) in enumerate(can)))
t = ('<tr><th>구분</th><th>의령(농촌)</th><th>광주 · 전남이라면?</th></tr>' + ''.join(f'<tr><td style="font-weight:800">{a}</td><td class="body">{b}</td><td style="color:#ff5a1f;font-weight:800">{c}</td></tr>' for a, b, c in [
    ('숫자 기준 1', '최심부 호스 8매 이상', '섬 — 선착장~최심부 거리 · 도선 시간'), ('숫자 기준 2', '진입불가 5개소 이상', '산간 — 임도 폭 · 회차 가능 지점'),
    ('특수 대상', '사찰 · 전통시장', '공단 · 고층 · 전통시장 · 요양시설'), ('판단', '센터장 판단', '센터장 판단(그대로)')]))
slide(100, head('PART 3 · 간부의 도구', '대상 선정 기준 만들기', 'Criteria.', '기준은 관할마다 다르게 만든다') + f'<div class="a" style="left:110px;top:290px;width:1700px"><table>{t}</table></div>' + key('기준을 숫자로 적어 두면, 사람이 바뀌어도 훈련 대상은 남는다'))
tmpl = [('항목 이름', '예) AI 정보 분석'), ('관찰 문장', '예) 출동 중 차량 안에서 AI에 접속했는가'), ('배점', '20점 — 5항목이면 100점'), ('숙련 구간', '80↑ 숙련 · 70~79 보통 · 50~69 미흡'), ('대조 항목', '예측(AI·책자) vs 실제(전개 매수 · 시간)')]
slide(101, head('PART 3 · 간부의 도구', '평가표 한 줄 만들기', 'Template.', '평가표 한 줄은 이렇게 쓴다') + ''.join(
    f'<div class="card{" hi" if i==4 else ""}" style="left:110px;top:{280+i*135}px;width:1700px;height:115px;padding:0 40px;display:flex;align-items:center;gap:40px">'
    f'<div class="acc" style="font-size:30px;font-weight:900;width:260px">{a}</div><div style="font-size:32px;font-weight:700">{b}</div></div>' for i, (a, b) in enumerate(tmpl)))
t = '<tr><th>주기</th><th>누가</th><th>무엇을</th></tr>' + ''.join(f'<tr><td style="font-weight:800">{a}</td><td class="body">{b}</td><td>{c}</td></tr>' for a, b, c in [
    ('주 2회', '안전센터', '중점 대상 순환 현지적응훈련'), ('월 2회', '지휘조사팀', '주관 합동훈련 · 숙지도 평가'), ('회차마다', '훈련 참여 전원', '디브리핑 → 데이터 수정'), ('연 1회', '현장대응단', '책자 · 데이터 개정, 대상 재선정')])
slide(102, head('PART 3 · 간부의 도구', '운영 리듬', 'Rhythm.', '훈련은 리듬으로 굴러간다') + f'<div class="a" style="left:110px;top:290px;width:1700px"><table>{t}</table></div>' + key('리듬이 정해지면 담당자가 바뀌어도 훈련이 멈추지 않는다'))
slide(103, '''<div class="tag"><b>PART 3 · 토의</b>  <span>5분</span></div><div class="ghost">Talk.</div>''' + sq(108, 312, 70) + '''
<div class="a" style="left:150px;top:330px;font-size:96px;font-weight:900;letter-spacing:-.04em;line-height:1.25">옆 사람과 5분,<br><span class="acc">우리 관할 중점 대상 1곳</span></div>
<div class="a body" style="left:150px;top:640px;font-size:38px;line-height:1.6">① 어디인가 &nbsp; ② 왜 늦어지나(숫자로) &nbsp; ③ 선정 기준 한 줄</div>''')
slide(104, '''<div class="tag"><b>PART 3 · 발표</b>  <span>2~3명</span></div><div class="ghost">Share.</div>''' + sq(108, 362, 70) + '''
<div class="a" style="left:150px;top:380px;font-size:110px;font-weight:900;letter-spacing:-.04em;line-height:1.25">광주 한 분,<br><span class="acc">전남 한 분</span></div>
<div class="a body" style="left:150px;top:690px;font-size:36px">강사 피드백 — 의령 사례의 어떤 칸을 가져가면 될지</div>''')
slide(105, head('PART 3 · 정리', '데이터가 움직인 것', 'Impact.', '데이터 한 장이 조직을 움직였다') + ''.join(
    f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*430}px;top:320px;width:405px;height:440px;padding:40px 34px"><div class="acc" style="font-size:24px;font-weight:800">{a}</div>'
    f'<div style="font-size:44px;font-weight:900;margin:16px 0;line-height:1.25">{b}</div><div class="body" style="font-size:26px;line-height:1.5">{c}</div></div>'
    for i, (a, b, c) in enumerate([('군청', '부군수 협의', '곡각지 · 처마 개선 과제'), ('주민', '주민참여예산 1억', '비상소화장치 약 15개소'), ('도', '우수시책 공유 · 설명회', '40명 참석'), ('18개 소방서', '시행계획', '경남 표준 모델')])))
slide(106, sq(108, 252, 90) + '''<div class="a" style="left:150px;top:270px;font-size:110px;font-weight:900;letter-spacing:-.045em;line-height:1.2">데이터는 이미 있었다.<br>꺼내 쓸 방법을<br><span class="acc" style="border-bottom:8px solid #ff5a1f">만든 것</span>뿐이다.</div>
<div class="a" style="right:110px;top:300px;width:520px">''' + ''.join(f'<div style="border-left:4px solid #ff5a1f;padding:16px 24px;margin-bottom:26px"><div class="acc" style="font-size:24px;font-weight:800">{a}</div><div style="font-size:32px;font-weight:800;margin-top:6px">{b}</div></div>'
    for a, b in [('PART 1 · 농골길', '문제를 데이터로'), ('PART 2 · AI 농골길 코치', '데이터를 훈련으로'), ('PART 3 · 확산', '조직과 관할로')]) + '</div>')

# 107~110 안내 · Q&A
slide(107, head('PART 3 · 안내', '강사 홈페이지 · 유튜브', 'Contact.', '직장훈련 또는 AI 교육, 연락 주세요') + shot('artc13.jpg', 110, 280, 1000, 700)
      + f'<img class="a" src="{qr("https://ssca1612.pages.dev/", "qr_home.png")}" style="left:1170px;top:290px;width:240px;height:240px;background:#fff;padding:8px;border-radius:10px">'
      + '<div class="a" style="left:1170px;top:560px;width:640px;font-size:32px;line-height:1.7"><b>ssca1612.pages.dev</b><br><span class="body">YouTube · Instagram <b class="acc">@inside_ax</b></span><br><span class="body">ssca1612@korea.kr</span></div>'
      + '<div class="a" style="left:1170px;top:800px;width:640px;padding:22px 28px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:30px;font-weight:800">관서에서 직장훈련 또는 AI 교육이 필요하면<br>언제든 연락 주세요 · 명함 드립니다</div>')
slide(108, '<div class="shot" style="left:0;top:0;width:1920px;height:1080px;border:0;border-radius:0"><img src="promo_last.jpg" style="object-fit:contain;background:#000"></div>'
      '<div class="note">🎬 강사 홍보 영상(1:22) → 마지막 장면(명함 · QR)에서 멈춤</div>')
links = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:14px"><img src="{qr(u, f"ql{n}.png")}" style="width:92px;height:92px;background:#fff;padding:4px;border-radius:6px">'
                f'<div><div class="acc" style="font-size:20px;font-weight:800">{m}</div><div style="font-size:21px;font-weight:700;line-height:1.3">{t[:34]}{"…" if len(t)>34 else ""}</div></div></div>' for n, c, m, d, t, k, u in ARTS)
cols = links.split('</div></div></div>')
half = len(ARTS) // 2
L = '</div></div></div>'.join(cols[:half]) + '</div></div></div>'; R = '</div></div></div>'.join(cols[half:])
slide(109, head('PART 3 · 자료', '오늘 나온 기사 12건', 'Links.', '기사 원문, 휴대폰으로 바로')
      + f'<div class="a" style="left:110px;top:270px;width:830px">{L}</div><div class="a" style="left:980px;top:270px;width:830px">{R}</div>')
slide(110, '''<div class="a" style="left:150px;top:200px;font-size:260px;font-weight:900;letter-spacing:-.05em;line-height:1">Q&amp;A<span class="acc">.</span></div>
<div class="a" style="left:150px;top:480px;font-size:110px;font-weight:900;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.25)">Thank you</div>
<div class="a body" style="left:150px;top:700px;font-size:32px;line-height:1.8">김경훈 · AI 챔피언(BLACK)<br>ssca1612@korea.kr · 010-8470-0037<br>ssca1612.pages.dev · @inside_ax</div>'''
      + f'<img class="a" src="{qr("https://ssca1612.pages.dev/", "qr_home2.png")}" style="right:150px;top:340px;width:360px;height:360px;background:#fff;padding:12px;border-radius:14px">')

exec(src[src.index("HS = '/opt"):])
