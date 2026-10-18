# 직장훈련특강 PART 2(41~80장) — 기획안 v.3.3.0 기준 · v.3.3: 여백 줄이고 글자 키움 · v.3.2: 의미 단위 줄바꿈
# 사용: python3 p2_v31.py <자료폴더> <출력폴더>   (도우미 함수는 p1_v31.py에서 가져옴)
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'p1_v33.py'), encoding='utf-8').read()
def part(a, b): return src[src.index(a):src.index(b)]
exec(part('import os, sys', '# ───────── 1-1 오프닝'))
exec(part('def page_full', '# ───────── 1-4').replace('PART 1 · 제출 제안서', 'PART 2 · 직장훈련 제안서').replace('PART 1 · 정리', 'PART 2 · 정리'))
exec(part('def ox(v)', "village(25,").replace('PART 1 · 책자 마을', 'PART 2 · 훈련 마을'))

def full(no, img, cap):
    slide(no, f'<div class="shot" style="left:0;top:0;width:1920px;height:1080px;border:0;border-radius:0"><img src="{img}" style="object-fit:contain;background:#000"></div>'
              '<div class="a" style="left:0;top:0;width:1920px;height:1080px;background:rgba(0,0,0,.35)"></div>'
              '<div class="a" style="left:900px;top:480px;width:120px;height:120px;border-radius:50%;background:#ff5a1f"></div>'
              '<div class="a" style="left:948px;top:516px;border-left:38px solid #fff;border-top:24px solid transparent;border-bottom:24px solid transparent"></div>'
              f'<div class="a" style="left:110px;bottom:70px;font-size:30px;font-weight:700">{cap}</div>')

# ───────── 2-1 책자의 한계와 선택
intro(41, '02', 'AI 농골길 코치 —', '데이터를 훈련으로', '소방청 직장훈련 우수 운영사례 최우수 · 소방청장상', ['90초', '직장훈련 제안서', 'GPTs', '한계', '농골길 웹', '평가표', '80.3점'])
slide(42, head('PART 2 · 문제', '1차 대응의 한계', 'Limit.', '책은 있었다, 출동 중엔 못 꺼냈다') + shot('limit.png', 110, 290, 1060, 600, paper=True)
      + '''<div class="card hi" style="left:1220px;top:290px;width:590px;height:600px;padding:0 50px;display:flex;flex-direction:column;justify-content:center"><div class="cap" style="font-size:32px">267쪽 책자에서<br>마을 하나 찾기</div>
<div style="font-size:240px;font-weight:900;line-height:1.05;color:#ff5a1f;letter-spacing:-.05em">90<span style="font-size:90px">초</span></div>
<div class="body" style="font-size:33px;line-height:1.5">책을 편다 → 쪽을 찾는다<br>→ 도면을 읽는다<br>→ 진입 가부를 읽는다<br>→ 구두로 전달</div></div>''' + key('데이터가 부족한 게 아니라, 전달 방식이 현장과 맞지 않았다'))
slide(43, head('PART 2 · 문제', '출동 중 차 안', 'Inside.', '달리는 차 안에서 책을 넘긴다는 것') + grid([('m19.jpeg', '책자를 펼쳐 보는 대원'), ('m20.jpeg', '단말기 확인'), ('m22.jpeg', '출동 중 정보 확인')], y=290, h=640, cols=3))
slide(44, head('PART 2 · 선택', '해결 방식 비교', 'Choice.', '사지 않고, 직접 만들었다') + cards([
    ('01', '책자<br>보완', '쪽수 · 색인 개선<br><span class="cap">여전히 넘겨서<br>찾아야 함</span>'), ('02', '외주<br>개발', '전용 앱 발주<br><span class="cap">예산 · 기간<br>수정할 때마다<br>다시 발주</span>'),
    ('03', '교육<br>강화', '239개 마을 암기<br><span class="cap">인사이동하면<br>처음부터</span>'), ('04', 'GPTs<br>자체 구축', '마을명 입력<br>→ 정보 출력<br><b class="acc">담당자 1인<br>코딩 0줄 · 바로 수정</b>')], hi=3, fs=54, bs=32)
      + key('가장 빠르고 싸게 바꿀 수 있는 방법 — 있는 데이터에 AI를 붙인다'))

# ───────── 2-2 직장훈련 공모전 제안서 한 쪽씩
page_full(45, 1, '1쪽 — 기본정보 · 추진배경 · 운영개요', ['참가구분 팀 · 공모주제 <b class="acc">기획 개선 분야</b>', '훈련 소개 3줄 요약', '추진배경 = 문제점 3줄(사고 · 인식 · 방법)', '운영개요 = 기간 · 장소 · 인원 · 형태'])
page_zoom(46, 1, 'jt1_bg.png', '추진배경 — 문제에서 출발', '사고 → 책자 → 90초 → GPTs', 'PART 1의 농골길이<br>바로 이 세 줄<br><b class="acc">기존 방법의 한계를 숫자 하나로</b><br>해결 방법을 한 줄로')
page_zoom(47, 1, 'jt1_op.png', '운영개요 — 훈련 형태', '복합형 훈련', 'AI 교육 + 출동 시뮬레이션<br>+ 현장 적용<br>자체 기획 · 운영(GPTs 제작)<br><span class="cap">※ 인원·기간은 제출 당시 기준<br>이후 공문 기준(전 직원 130명)으로 확대</span>')
page_full(48, 2, '2쪽 — 세부내용', ['AI 기반 해결전략과 목표(문제 · AI · 결과 표)', '농골길 코치 작동 프로세스 5단계', '<b class="acc">구축 타임라인 5단계</b>'])
page_zoom(49, 2, 'jt2_tl.png', '구축 타임라인 = 훈련 설계 순서', '사전준비 → AI 개발<br>→ 사용 교육 → 시뮬레이션<br>→ 현장 적용', '새 훈련을 도입할 때 그대로 쓰는 순서<br><b class="acc">도구를 만들고, 가르치고,<br>연습하고, 현장에 넣는다</b>')
page_full(50, 3, '3쪽 — 훈련 프로세스 · 보완 · 성과', ['훈련 프로세스 4단계<br>이론 교육 → 가상 시뮬레이션 → 실전 출동 → 현장 적용', '<b class="acc">보완점 개선 3가지</b>', '차별화 포인트 · 도입 전/후 비교'])
page_zoom(51, 3, 'jt3_fix.png', '보완점 개선 = 환류', '답변 부정확 · 정보 과다<br>통신 두절', '오류 데이터 수정 → 재학습<br>핵심 7개 항목으로<br>차량 내 책자 병행<br><b class="acc">훈련에서 나온 문제를 도구에 되돌린다</b>')
page_full(52, 4, '4쪽 — 발전 방안 · 확산', ['단계별 로드맵(음성 · 이미지 → GPS 연동 → 경남 확대)', '기대효과(지역 · 광역 · 전국)', '확산 방안: 매뉴얼 · 설명회 · 1:1 컨설팅', '타 기관 확산(경찰 · 보건 · 산림 · 지자체)'])
page_full(53, 5, '5쪽 — 관련 사진 · 참가자', ['AI 농골길 코치 실행 화면', '중점 마을 AI 정보 기반 호스 전개 훈련', '출동 중 AI 활용 · GPTs 사용방법 교육', '부림면 감암마을 출동 전술 시뮬레이션'], img='jth-5m.png')
slide(54, head('PART 2 · 정리', '제안서에서 배울 것', 'Summary.', '제안서 구조 = 훈련 설계 구조') + ''.join(
    f'<div class="card{" hi" if i==4 else ""}" style="left:{110+i*246}px;top:290px;width:226px;height:600px;display:flex;flex-direction:column;justify-content:center;align-items:center">'
    f'<div class="acc" style="font-size:34px;font-weight:800">0{i+1}</div><div style="font-size:60px;font-weight:900;margin-top:26px">{t}</div></div>'
    for i, t in enumerate(['문제', '데이터', '도구', '훈련', '평가', '환류', '확산'])) + key('보고서를 쓰는 순서가 아니라, 훈련을 만드는 순서다'))

# ───────── 2-3 GPTs
slide(55, head('PART 2 · AI 농골길 코치', '구축 흐름', 'Build.', '책 한 권을 AI에 넣기까지') + cards([
    ('01', '데이터 정제', '239개 마을<br>4층 구조<br>용수시설 좌표'), ('02', '프롬프트 설계', '출력 6블록<br>근거 자료 표기<br>7개 핵심 항목'),
    ('03', 'GPTs 구축', '마을명 입력 →<br>진입 가부 · 호스<br>소화전 · 전술'), ('04', '검증 · 재학습', '현장 훈련에서<br>틀린 답<br>→ 데이터 수정')], hi=2, fs=54, bs=32)
      + key('담당자 1명, 코딩 0줄 — 소방관이 직접 만든 훈련 도구'))
full(56, 'g_hi.jpg', '🎬 AI 농골길 코치(GPTs) 실제 화면 · 전체화면 자동 재생 · 무음 (2:48)')
flow = [('기본<br>정보', '마을명<br>위치 · 주소'), ('진입 · 소방<br>접근', '최심부 진입 가부<br>호스 매수<br>차량별 진입'), ('대체<br>진입로', '마을 내부<br>우회로'), ('인근<br>소화전', '코드 · 거리<br>위치'), ('비고 · 전술', '현장 판단<br>메모'), ('근거<br>자료', '어느 자료에서<br>왔는지<br>(환각 방지)')]
slide(57, head('PART 2 · AI 농골길 코치', 'GPTs 출력 구조', 'Output.', '마을명 하나 → 6블록 답변') + ''.join(
    f'<div class="card{" hi" if i==1 else ""}" style="left:{110+i*287}px;top:290px;width:262px;height:560px;padding:0 26px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:30px;font-weight:800">0{i+1}</div>'
    f'<div style="font-size:44px;font-weight:900;margin:16px 0 26px;line-height:1.2">{t}</div><div class="body" style="font-size:30px;line-height:1.5">{d}</div></div>' for i, (t, d) in enumerate(flow))
      + '<div class="a" style="left:110px;top:880px;width:1700px;padding:22px 34px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:36px;font-weight:700">1차: 마을 정보 + 기본 전술 → 필요하면 2차: 차량 배치 · 호스 전개 순서</div>')
slide(58, head('PART 2 · 교육', "전 대원 GPTs 활용 교육 · 현장대응단-2515('26.3.5.)", 'Teach.', '도구를 만들었으면, 가르쳐야 한다') + grid([('m29.jpeg', '사용법 교육'), ('m30.jpeg', '팀별 실습'), ('m31.jpeg', '사무실 교육'), ('m32.jpeg', '결과 해석')], cols=2))
slide(59, head('PART 2 · 현장', '출동 중 AI 조회', 'Use.', '차 안에서, 단말기로, 몇 초 만에') + grid([('m21.jpeg', '출동 중 단말기 조회'), ('m36.jpeg', '팀장 → 대원 정보 전달'), ('m22.jpeg', '이동 중 확인')], y=290, h=640, cols=3))
slide(60, head('PART 2 · 현장', '현장 도착 후', 'Field.', '현장에서 태블릿 지도로 확인한다') + grid([('m33.png', '태블릿 지도 확인'), ('m34.png', '팀원과 함께 확인'), ('m35.jpeg', '최심부 호스 전개')], y=290, h=640, cols=3))

# ───────── 2-4 한계 → 웹
good = ['마을명 하나로<br>몇 초 만에 조회', '데이터 바로 수정<br>재인쇄 없음', '담당자 1인 · 코딩 0줄로 구축', '출동 중 단말기 조회<br>→ 팀원에게 전달']
bad = ['출동 시스템은 <b>지번</b>, GPTs는 <b>마을</b> 단위<br>검색이 어렵다', '지도 · 사진 같은 <b>시각화 자료</b>를<br>보여 주기 어렵다', '<b>음성 입력 · 출력</b> 불가<br>글자로 묻고 글자로 받는 <b>T2T</b>만',
       '차량 도착 · 배치를 <b>텍스트로만</b> 확인<br>직관적이지 않다', '같은 질문에도 답이 흔들릴 때가 있다']
slide(61, head('PART 2 · 써 보니', '장점과 한계', 'Review.', '써 보니 — 좋았던 점, 막힌 점')
      + '<div class="card" style="left:110px;top:290px;width:640px;height:700px;padding:0 44px;display:flex;flex-direction:column;justify-content:center"><div class="dim" style="font-size:30px;font-weight:800;letter-spacing:.2em;margin-bottom:30px">장점</div>'
      + ''.join(f'<div class="body" style="font-size:36px;line-height:1.4;margin-bottom:30px;padding-left:24px;text-indent:-24px">· {t}</div>' for t in good) + '</div>'
      + '<div class="card hi" style="left:780px;top:290px;width:1030px;height:700px;padding:0 48px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:30px;font-weight:800;letter-spacing:.2em;margin-bottom:30px">한계</div>'
      + ''.join(f'<div style="font-size:35px;line-height:1.4;margin-bottom:26px;padding-left:36px;text-indent:-36px">{i+1}. {t}</div>' for i, t in enumerate(bad)) + '</div>')
q = [('좋았던 점', '"출동 중 단말기를 이용한<br>AI 검색 및 정보 전달"', '팀장 다수'), ('좋았던 점', '"팀장의 정보 전달을 통한<br>개인 임무 확인"', '대원 다수'),
     ('막힌 점', '"출동 중 복장 착용으로<br>단말기 조작이 어려움"', '2026. 8. 디브리핑'), ('막힌 점', '"단말기가 한 대뿐이라<br>확인 · 전달이 어려움"', '2026. 8. 디브리핑'),
     ('막힌 점', '"현장 상황과<br>AI 정보의 괴리"', '2026. 8. 디브리핑'), ('요구', '"AI로 음성 소방작전<br>전파 필요"', '개선 요구')]
slide(62, head('PART 2 · 써 보니', '현장 의견 원문', 'Voice.', '대원들이 직접 적어 낸 말') + ''.join(
    f'<div class="card{" hi" if a=="요구" else ""}" style="left:{110+(i%3)*575}px;top:{290+(i//3)*360}px;width:550px;height:340px;padding:0 42px;display:flex;flex-direction:column;justify-content:center">'
    f'<div class="{"acc" if a!="좋았던 점" else "dim"}" style="font-size:28px;font-weight:800;letter-spacing:.15em">{a}</div><div style="font-size:38px;font-weight:800;line-height:1.4;margin:18px 0">{b}</div><div class="cap" style="font-size:26px">{c}</div></div>' for i, (a, b, c) in enumerate(q)))
steps = [('지번으로 찍힌다', '지번 주소로<br>검색'), ('텍스트만 나온다', '지도를<br>띄운다'), ('진입불가를<br>글로 읽는다', '지도에서<br>진입불가 구간<br>바로 확인'),
         ('전술은<br>사람이 짠다', '건축물대장 API<br>→ 건물 정보<br>→ AI가 전술'), ('배치를<br>글로 상상한다', '차량별<br>진입 경로 ·<br>배치 위치 예상')]
slide(63, head('PART 2 · 그래서', '한계를 웹에서 푼다', 'Next.', '그래서, 웹으로 만들고 있다') + ''.join(
    f'<div class="card{" hi" if i==3 else ""}" style="left:{110+i*345}px;top:{610-i*80}px;width:320px;height:{380+i*80}px;padding:0 30px;display:flex;flex-direction:column;justify-content:center">'
    f'<div class="cap" style="font-size:30px;line-height:1.4;text-decoration:line-through">{a}</div><div class="acc" style="font-size:52px;margin:16px 0">↓</div>'
    f'<div style="font-size:40px;font-weight:900;line-height:1.35">{c}</div></div>' for i, (a, c) in enumerate(steps)))
full(64, 'w70.jpg', '🎬 농골길 웹 · 휴대폰 화면 녹화 — 핵심 구간 약 2분 · 무음')
slide(65, head('PART 2 · 라이브', '농골길 웹 직접 접속', 'Live.', '지금 만들고 있는 농골길 웹') + shot('w20.jpg', 110, 290, 1150, 647)
      + '''<div class="a" style="left:1300px;top:290px;width:520px;height:647px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:30px;font-weight:800;letter-spacing:.15em">LIVE</div>
<div style="font-size:46px;font-weight:900;margin:12px 0 34px">nonggolgil<br>.pages.dev</div>
<div class="body" style="font-size:38px;line-height:1.7">① 지번으로 검색<br>② 지도 · 진입불가 구간<br>③ 건축물 정보 · AI 전술<br>④ 차량별 진입 경로 · 배치</div>
<div class="cap" style="font-size:28px;margin-top:34px">허가 사용자 로그인<br>계속 업그레이드 중</div></div>''')
slide(66, head('PART 2 · 라이브', '웹 화면 해설', 'Guide.', '화면 한 장에 무엇이 있나') + shot('w130.jpg', 110, 290, 1150, 647) + ''.join(
    f'<div class="card" style="left:1300px;top:{290+i*167}px;width:510px;height:147px;padding:0 32px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:28px;font-weight:800">{a}</div><div style="font-size:31px;font-weight:800;margin-top:8px;line-height:1.3">{b}</div></div>'
    for i, (a, b) in enumerate([('지도', '진입곤란 · 대체구간<br>차량별 경로 범례'), ('차량 탭', '펌프 · 물탱크 · 구급 · 마을방문'), ('AI 브리핑', '건축물 정보 기반 전술 문장'), ('검색', '지번 · 도로명 · 마을명')])))

# ───────── 2-5 훈련 설계와 평가
slide(67, head('PART 2 · 훈련으로', '2025. 12.', 'Award.', '직장훈련 우수 운영사례, 최우수') + '''
<div class="card hi" style="left:110px;top:290px;width:1700px;height:340px;padding:0 60px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:32px;font-weight:800;letter-spacing:.2em">소방청 · 직장훈련 우수 운영사례</div>
<div style="font-size:110px;font-weight:900;margin-top:16px">최우수 · 소방청장상</div></div>
<div class="a body" style="left:110px;top:675px;font-size:42px;line-height:1.7">· "AI를 통한 신속한 현장대응활동 기반 조성"<br>· "전국 최초 농촌마을 소방 GPTs 개발<br>&nbsp;&nbsp;&nbsp;출동 중 화재 전술 제시, 실시간 조회 · 업데이트"</div>
<div class="a cap" style="left:110px;top:1030px;font-size:24px">출처: 2025 농골길 결과보고(현장대응단-11301) · 🔗 쿠키뉴스 원문 링크</div>''')
st = [("'26. 2. 11.", '고도화 · 활용 증진 계획', '책자 개정 · 용수시설 정밀 좌표'), ("'26. 3. 5.", '전 대원 GPTs 활용 교육', '현장대응단-2515'), ("'26. 7.~", 'AI 기반 현지적응훈련', '현장대응단-7033 · 지휘팀 평가')]
slide(68, head('PART 2 · 훈련으로', '2026 B사업', 'Train.', '도구를 만들고, 훈련에 넣었다') + ''.join(
    f'<div class="card{" hi" if i==2 else ""}" style="left:110px;top:{276+i*243}px;width:560px;height:218px;padding:0 34px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:30px;font-weight:800">{d}</div>'
    f'<div style="font-size:40px;font-weight:900;margin:8px 0 8px">{t}</div><div class="cap" style="font-size:27px">{c}</div></div>' for i, (d, t, c) in enumerate(st))
      + '<div class="a acc" style="left:688px;top:600px;font-size:44px;font-weight:900">▶</div>' + shot('docplan.png', 740, 276, 1070, 704, paper=True))
slide(69, head('PART 2 · 훈련 설계', "AI 기반 현지적응훈련 · 현장대응단-7033('26.7.22.)", 'Design.', '훈련을 이렇게 설계했다') + cards([
    ('주관', '지휘팀<br>주관', '지휘 1·2·3팀이<br>회차별 주관 · 평가'), ('규모', '동원<br>25명', '차량 8~9대<br>지휘 2 · 구조대 4<br>의령 7 · 부림 6<br>정곡 6'),
    ('대상', '마을 3곳<br>/ 회', '중점관리대상 순환<br>재훈련 포함'), ('흐름', '출동<br>→ AI 조회<br>→ 전개', '차고탈출<br>현장도착<br>최심부 호스전개 실측')], h=700, hi=3, fs=54, bs=32))
slide(70, head('PART 2 · 훈련', '2026 AI 기반 현지적응훈련', 'Field.', '골목 끝까지, AI 정보를 들고') + shot('train2608.jpg', 110, 280, 1700, 700, '2026. 8. 현지적응훈련 사진 모음'))
slide(71, head('PART 2 · 훈련', '2026 AI 기반 현지적응훈련', 'Tactic.', '태블릿을 보며 전술을 맞춘다') + grid([('m33.png', '태블릿으로 진입로 확인'), ('m34.png', '팀장·대원 함께 확인'), ('m14.jpeg', '최심부 호스 전개'), ('m16.jpeg', '소화전 점령'), ('m15.png', '좁은 골목 진입'), ('m17.jpeg', '훈련 전 브리핑')], cols=3))
items = [('AI 정보 분석', '출동 중 『AI 농골길 코치』에 신속히 접속했는가<br>진입로 폭 · 화재피해약자 정보를 도착 전 숙지했는가'), ('지도 연동', '지령탭 · 모바일 지도 링크 활성화<br>소화전 · 비상소화장치 위치 실시간 공유'),
         ('AI 기반<br>차량부서', '도로 협소 시 무리한 진입 지양<br>입구 공터 분산 부서'), ('전술 검증', '<b class="acc">AI가 예측한 호스 매수와<br>실제 전개 매수를 대조</b>했는가'), ('디브리핑 · 환류', '실측 타임라인과 AI 가이드를 대조해<br><b class="acc">수정사항을 시스템에 즉시 환류</b>했는가')]
t = ''.join(f'<tr><td style="width:330px;font-weight:800;font-size:36px;padding:19px 20px">{a}</td><td class="body" style="font-size:30px;line-height:1.35;padding:19px 20px">{b}</td><td class="acc" style="width:90px;font-size:38px;font-weight:900;padding:19px 20px">20</td></tr>' for a, b in items)
slide(72, head('PART 2 · 평가표 설계', '농·골·길 고도화 숙지도 평가표(2026. 9.)', 'Check.', 'AI가 평가 항목이 된 훈련') + f'<div class="a" style="left:110px;top:262px;width:1700px"><table>{t}</table></div>'
      + '<div class="a" style="left:110px;top:935px;width:1700px;padding:18px 32px;border-left:6px solid #ff5a1f;background:rgba(255,90,31,.08);font-size:32px;font-weight:700">숙련 기준 — <b class="acc">80점↑ 숙련</b> · 70~79 보통 · 50~69 미흡 · 50 미만 숙지 필요 <span class="cap" style="font-size:26px;font-weight:400">&nbsp; 평가자: 지휘조사팀장</span></div>')
slide(73, head('PART 2 · 평가표 설계', '간부가 볼 곳', 'Point.', '좋은 평가 항목의 조건') + cards([
    ('원칙 01', '행동으로<br>관찰 가능한<br>문장', '"숙지했는가"보다<br>"접속했는가"<br>"대조했는가"'), ('원칙 02', 'AI 사용<br>자체를<br>평가 대상으로', '도구를 만들었으면<br>쓰는지까지 잰다'),
    ('원칙 03', '예측과<br>실제를<br>대조한다', 'AI 예측 호스 매수<br>vs<br>실제 전개 매수'), ('원칙 04', '환류까지<br>점수에<br>넣는다', '디브리핑<br>→ 시스템 수정<br>= 20점')], hi=2, fs=48, bs=32)
      + key('평가표를 바꾸면 훈련이 바뀐다 — 간부가 가진 가장 강한 도구'))
teams = [('지휘2팀', '9. 3.', 77.3), ('지휘1팀', '9. 8.~11.', 80.0), ('지휘3팀', '9. 10.', 83.8)]
slide(74, head('PART 2 · 평가 결과', '2026. 9. 1회차 · 12개 팀', 'Score.', '12개 팀 평균 80.3점') + ''.join(
    f'<div class="a" style="left:{200+i*330}px;top:{900-(v-60)*22}px;width:200px;height:{(v-60)*22}px;background:{"#ff5a1f" if v>=80 else "#55504c"};border-radius:10px 10px 0 0"></div>'
    f'<div class="a" style="left:{200+i*330}px;top:{840-(v-60)*22}px;width:200px;text-align:center;font-size:52px;font-weight:900">{v}</div>'
    f'<div class="a cap" style="left:{150+i*330}px;top:915px;width:300px;text-align:center;font-size:32px">{a}<br>{d}</div>' for i, (a, d, v) in enumerate(teams))
      + '<div class="a" style="left:110px;top:{}px;width:1000px;height:2px;background:#f4f4f2;opacity:.5"></div>'.format(900-(80-60)*22)
      + '''<div class="card hi" style="left:1250px;top:290px;width:560px;height:700px;padding:0 48px;display:flex;flex-direction:column;justify-content:center"><div class="cap" style="font-size:34px">전체 12개 팀 평균</div>
<div style="font-size:190px;font-weight:900;color:#ff5a1f;letter-spacing:-.05em;line-height:1.1">80.3</div><div class="body" style="font-size:36px;line-height:1.6">숙련(80↑) 7개 팀<br>AI 정보 분석 평균 15.8 / 20</div></div>''')
data = [('1팀', '우곡', '39초', '4:30', '1:20', '5:40'), ('1팀', '익구', '43초', '5:10', '3:30', '8:40'), ('1팀', '석곡', '41초', '1:30', '3:20', '4:50'),
        ('2팀', '무하', '47초', '3:50', '2:32', '7:09'), ('2팀', '율리', '44초', '3:11', '2:15', '6:10'), ('2팀', '상촌', '45초', '3:58', '1:50', '6:33'),
        ('3팀', '무중', '37초', '7:01', '1:58', '9:36'), ('3팀', '율리', '35초', '8:55', '0:54', '10:24'), ('3팀', '신기', '40초', '6:58', '1:12', '8:50')]
t = '<tr><th>주관</th><th>마을</th><th>차고탈출</th><th>현장도착</th><th>최심부 호스전개</th><th>총 소요</th></tr>' + ''.join(
    f'<tr style="{"color:#ff5a1f" if r[1] in ("익구","무중") else ""}">' + ''.join(f'<td style="font-size:33px;padding:12px 20px">{c}</td>' for c in r) + '</tr>' for r in data)
slide(75, head('PART 2 · 실측', '2026. 9. 1회차 · 동원 25명 · 차량 8~9대', 'Data.', '마을마다 재 본 시간') + f'<div class="a" style="left:110px;top:258px;width:1700px"><table>{t}</table></div>'
      + '<div class="a cap" style="left:110px;top:985px;font-size:22px">출처: 9월 1회차 지휘팀 주관 AI 기반 현지적응훈련 결과보고 3건 · 3팀 차고탈출 평균 37초(8월 대비 8초 향상)</div>')
village(76, 'bk148-148.png', '익구마을', '부림면 익구로 126 · 2026. 9. 1팀 훈련', 148, 7, '마을 입구에서 약 140m 지점까지 차량진입 가능', ['X', 'X', 'O', None], '실측: 차고탈출 43초 · 도착 5:10 · <b class="acc">최심부 호스전개 3:30</b> · 총 8:40', ghost='Drill.')
village(77, 'bk30-030.png', '무중마을', '의령읍 무전로3길 12 · 2026. 9. 3팀 훈련', 30, 8, '마을 주도로 외 샛길은 차량 진입곤란', ['X', 'X', 'O', 'X'], '총 9:36 → <b class="acc">재훈련으로 소요시간 단축</b>(지형 숙지 효과, 결과보고 기재)', ghost='Drill.')
slide(78, head('PART 2 · 환류', '디브리핑 → 데이터 수정', 'Loop.', '훈련에서 나온 문제를 도구에 되돌린다') + grid([('m29.jpeg', '디브리핑'), ('m31.jpeg', '결과 공유')], x=110, y=280, w=820, h=640, cols=1)
      + ''.join(f'<div class="card{" hi" if i==2 else ""}" style="left:970px;top:{280+i*220}px;width:840px;height:200px;padding:0 40px;display:flex;flex-direction:column;justify-content:center"><div class="acc" style="font-size:30px;font-weight:800">{a}</div><div style="font-size:38px;font-weight:800;margin-top:10px;line-height:1.35">{b}</div></div>'
                for i, (a, b) in enumerate([('발견', '도로 굴곡 · 원거리로 현장도착 지연'), ('발견', '마을 입구 주정차 · 사제 구조물로<br>대형차 진입 한계'), ('환류', '데이터 수정 → AI 재학습<br>→ 같은 마을 재훈련(무중마을)')])))
cyc = ['대상 선정', '도구', '훈련', '평가표', '실측', '디브리핑', '데이터 수정']
slide(79, head('PART 2 · 정리', '간부의 훈련 사이클', 'Cycle.', '한 바퀴가 아니라, 계속 도는 바퀴') + ''.join(
    f'<div class="a" style="left:{960+560*__import__("math").cos(-1.5708+i*6.2832/7)-150:.0f}px;top:{650+300*__import__("math").sin(-1.5708+i*6.2832/7)-62:.0f}px;width:300px;height:124px;border-radius:62px;'
    f'background:{"#2a2523" if i!=6 else "#ff5a1f"};border:3px solid {"#ff5a1f" if i in (3,6) else "#55504c"};display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:900">{t}</div>' for i, t in enumerate(cyc))
      + '<div class="a" style="left:660px;top:560px;width:600px;text-align:center;font-size:56px;font-weight:900;line-height:1.3"><span style="color:#ff5a1f">데이터</span>가<br>훈련을 고친다</div>')
slide(80, '''<div class="tag"><b>PART 2 · END</b>  <span>AI 농골길 코치</span></div>
<div class="a" style="left:150px;top:200px;font-size:300px;font-weight:900;letter-spacing:-.05em;line-height:1">End<span class="acc">.</span></div>
<div class="a" style="left:150px;top:560px;font-size:56px;font-weight:900;line-height:1.35">만들고 → 훈련하고 →<br>재고 → <span class="acc">고친다</span></div>
<div class="a" style="left:0;bottom:0;width:1920px;height:120px;background:#ff5a1f;display:flex;align-items:center;padding-left:150px;font-size:34px;font-weight:800">NEXT ▸ PART 3 · 조직과 관할로</div>''')

exec(src[src.index("HS = '/opt"):])
