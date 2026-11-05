# 실습 카드 A4 앞·뒤 생성기 v.1.0.0 — HTML(인쇄용, QR은 SVG로 내장) → PDF는 playwright로
# 사용: python3 card1105.py <출력 html 경로>
import sys, io, qrcode, qrcode.image.svg

OUT = sys.argv[1]
VER = 'v.1.0.0'
DATE = '26.10.29'

def qr(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=0, box_size=10)
    b = io.BytesIO(); img.save(b)
    s = b.getvalue().decode()
    return s[s.index('<svg'):].replace('<svg ', '<svg class="qr" ', 1)

APPS = [('ChatGPT', '필수', 'chatgpt.com', 'https://chatgpt.com', '묻고 쓰기 · 사진 읽기 · 음성'),
        ('Gemini', '필수', 'gemini.google.com', 'https://gemini.google.com', '사진 편집 · 카메라 대화'),
        ('NotebookLM', '선택', 'notebooklm.google.com', 'https://notebooklm.google.com', '자료 요약 · 라디오'),
        ('클로바노트', '선택', 'clovanote.naver.com', 'https://clovanote.naver.com', '녹음 → 회의록')]

MISSIONS = [
    ('01', '종이를 찍으면 표가 됩니다', 'ChatGPT', ['카메라(+) 누르기', '<b>뒷면 표</b>를 찍기', '아래처럼 말하기'],
     ['이 표를 엑셀 표로 만들어 줘', '민원이 가장 많은 3가지를 요약해 줘']),
    ('02', '내 사진을 바꿔 봅니다', 'Gemini', ['+ → 사진 고르기', '셀카 또는 앨범 사진', '바꾸고 싶은 모습을 말로'],
     ['증명사진처럼 바꿔 줘', '캐리커처로 그려 줘', '흑백 사진을 컬러로 복원해 줘']),
    ('03', 'AI와 말로 대화합니다', 'Gemini Live', ['물결 아이콘(Live) 누르기', '편하게 말 걸기 — 사투리 OK', '카메라 켜고 물건 비추기'],
     ['오늘 진주 저녁 메뉴 추천해 줘', '이거 뭐야? 어디에 쓰는 거야?']),
    ('04', 'AI가 틀린 곳을 찾아라', '강의 화면', ['화면의 AI 답변 세 개 읽기', '틀린 곳 찾기', '손들고 말하기'],
     ['AI는 틀려도 자신 있게 말합니다', '→ 확인은 사람이']),
]

TABLE = [  # 미션 1용 가상 자료 (합계는 아래에서 계산)
    ('불법 주정차', 412, 389, 455), ('도로 파손·포트홀', 96, 188, 143), ('생활 소음', 131, 142, 118),
    ('쓰레기 무단투기', 205, 231, 197), ('가로등 고장', 58, 47, 71), ('공원·놀이터 시설', 39, 62, 44), ('기타', 87, 93, 101)]

BINGO = ['사진으로\n표 만들기', '내 사진\n바꾸기', 'AI와\n말로 대화', '카메라로\n보여 주며 묻기', '틀린 곳\n찾기', '폰으로\n투표하기', '옆 사람\n도와주기', '영어 한 문장\n연습하기', '흑백 사진\n컬러로']

PROMPTS = [('표로 정리해 줘', '긴 글·사진을 한눈에'), ('공문체로 다듬어 줘', '말투를 보고서처럼'), ('세 줄로 요약해 줘', '긴 자료를 짧게'),
           ('초등학생도 알게 설명해 줘', '어려운 용어 풀기'), ('틀린 곳이 있는지 확인해 줘', '내 글 점검'), ('출처를 같이 알려 줘', '확인할 근거 받기')]

def esc_nl(t): return t.replace('\n', '<br>')

apps = ''.join(f'''<div class="app{' must' if need == '필수' else ''}"><div class="apph"><b>{nm}</b><span class="need">{need}</span></div>
<div class="qrw">{qr(full)}</div><div class="url">{url}</div><div class="use">{use}</div></div>''' for nm, need, url, full, use in APPS)

ms = ''
for n, t, tool, steps, says in MISSIONS:
    ms += f'''<div class="ms"><div class="msh"><span class="mn">MISSION {n}</span><span class="tool">{tool}</span><span class="ck"></span></div>
<div class="mt">{t}</div><ol>{''.join(f'<li>{s}</li>' for s in steps)}</ol>
<div class="says">{''.join(f'<div class="say">“{s}”</div>' if not s.startswith('→') and not s.startswith('AI는') else f'<div class="say plain">{s}</div>' for s in says)}</div></div>'''

rows = ''
tot = [0, 0, 0]
for name, a, b, c in TABLE:
    rows += f'<tr><td class="l">{name}</td><td>{a:,}</td><td>{b:,}</td><td>{c:,}</td><td class="s">{a+b+c:,}</td></tr>'
    tot = [tot[0] + a, tot[1] + b, tot[2] + c]
rows += f'<tr class="t"><td class="l">합계</td><td>{tot[0]:,}</td><td>{tot[1]:,}</td><td>{tot[2]:,}</td><td class="s">{sum(tot):,}</td></tr>'

bingo = ''.join(f'<div class="bg{" free" if i == 4 else ""}"><span>{esc_nl(t)}</span></div>' for i, t in enumerate(BINGO))
prompts = ''.join(f'<div class="pr"><b>“{p}”</b><span>{d}</span></div>' for p, d in PROMPTS)

HTML = f'''<!doctype html>
<html lang="ko"><head>
<!--
## 변경 이력
| 버전 | 날짜 | 수정 내용 |
|---|---|---|
| v.1.0.0 | 26.10.29 | 최초 작성 — 앞면(앱 QR 4 · 미션 4 · 보안 3원칙 · 투표 안내) / 뒷면(미션 1용 가상 민원 통계표 · AI 빙고 · 자주 쓰는 말 6 · 내일 해 볼 것 하나 · 강사 연락처 QR). 흑백 인쇄에서도 읽히게 흰 바탕 + 검정 글씨, 주황은 보조 |
-->
<meta charset="utf-8"><title>실습 카드 — 공무원을 위한 AI도구 활용법</title>
<style>
@font-face{{font-family:P;src:local("Pretendard"),local("Pretendard Variable");}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0;word-break:keep-all}}
body{{font-family:Pretendard,P,sans-serif;color:#111;background:#ddd}}
.page{{width:210mm;height:297mm;background:#fff;margin:0 auto;padding:11mm 12mm 10mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:4mm}}
.page:last-child{{page-break-after:auto}}
@media screen{{.page{{margin:8mm auto;box-shadow:0 2px 12px rgba(0,0,0,.2)}}}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.6mm solid #111;padding-bottom:2.5mm}}
.top .k{{font-size:8.5pt;font-weight:800;letter-spacing:.18em;color:#e04a12}}
.top h1{{font-size:21pt;font-weight:900;letter-spacing:-.03em;line-height:1.15;margin-top:1mm;position:relative;padding-left:5mm}}
.top h1:before{{content:"";position:absolute;left:0;top:.4mm;width:3.4mm;height:3.4mm;border-left:.7mm solid #111;border-top:.7mm solid #111}}
.top .r{{text-align:right;font-size:8.5pt;color:#555;line-height:1.5}}.top .r b{{color:#111;font-size:10pt}}
.sec{{display:flex;align-items:baseline;gap:2.5mm;font-size:12.5pt;font-weight:900}}
.sec i{{font-style:normal;font-size:8.5pt;font-weight:800;color:#fff;background:#111;border-radius:1mm;padding:.5mm 1.8mm;letter-spacing:.1em}}
.sec span{{font-size:8.5pt;font-weight:600;color:#666}}
.apps{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}
.app{{border:.35mm solid #bbb;border-radius:3mm;padding:2.6mm;text-align:center}}
.app.must{{border:.6mm solid #111}}
.apph{{display:flex;justify-content:space-between;align-items:center}}.apph b{{font-size:11.5pt;font-weight:900}}
.need{{font-size:7.5pt;font-weight:800;border-radius:5mm;padding:.4mm 2mm;border:.3mm solid #999;color:#555}}
.must .need{{background:#ff5a1f;border-color:#ff5a1f;color:#111}}
.qrw{{margin:2mm auto 1.2mm;width:27mm;height:27mm}}.qr{{width:100%;height:100%}}
.url{{font-size:7.5pt;font-weight:700}}.use{{font-size:7.5pt;color:#666;margin-top:.6mm}}
.note{{font-size:8.5pt;color:#444;background:#f3f1ee;border-radius:2mm;padding:2mm 3mm}}.note b{{color:#111}}
.mss{{display:grid;grid-template-columns:1fr 1fr;gap:3mm}}
.ms{{border:.35mm solid #999;border-radius:3mm;padding:3.6mm 4mm}}
.msh{{display:flex;align-items:center;gap:2mm}}
.mn{{font-size:8pt;font-weight:900;letter-spacing:.16em;color:#e04a12}}
.tool{{font-size:7.5pt;font-weight:800;background:#111;color:#fff;border-radius:5mm;padding:.4mm 2.2mm}}
.ck{{margin-left:auto;width:5mm;height:5mm;border:.45mm solid #111;border-radius:1mm}}
.mt{{font-size:13.5pt;font-weight:900;margin-top:1.4mm;letter-spacing:-.02em}}
ol{{margin:1.8mm 0 0 4.8mm;font-size:10.2pt;line-height:1.6}}ol b{{font-weight:900}}
.says{{margin-top:1.8mm;display:flex;flex-direction:column;gap:1.2mm}}
.say{{font-size:9.6pt;font-weight:700;background:#f3f1ee;border-radius:2mm 2mm 2mm .5mm;padding:1.2mm 2.4mm;align-self:flex-start}}
.say.plain{{background:none;padding:0 0 0 .4mm;font-weight:800}}
.safe{{border:.6mm solid #111;border-radius:3mm;padding:3mm 4mm;display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:3mm;align-items:center}}
.safe .h{{font-size:12pt;font-weight:900;line-height:1.25}}.safe .h small{{display:block;font-size:8pt;font-weight:700;color:#e04a12;letter-spacing:.1em}}
.safe div.x{{border-left:.35mm solid #ccc;padding-left:3mm}}
.safe div.x b{{display:block;font-size:10.5pt;font-weight:900}}.safe div.x span{{font-size:9pt;color:#555;line-height:1.4}}
.safe .tip{{grid-column:1/-1;font-size:8.8pt;font-weight:700;border-top:.3mm dashed #bbb;padding-top:2mm}}
.vote{{display:flex;align-items:center;gap:3mm;font-size:9pt;color:#333}}.vote b{{color:#111}}
.vote .big{{font-size:20pt}}
table{{width:100%;border-collapse:collapse;font-size:11pt}}
caption{{text-align:left;font-size:11.5pt;font-weight:900;padding-bottom:1.6mm}}caption span{{font-size:8.5pt;font-weight:600;color:#666;margin-left:2mm}}
th,td{{border:.35mm solid #333;padding:1.9mm 2.4mm;text-align:right}}
th{{background:#eee;font-weight:800;text-align:center}}td.l{{text-align:left;font-weight:700}}td.s{{font-weight:800}}
tr.t td{{background:#f3f1ee;font-weight:900}}
.tbx{{border:.6mm solid #111;border-radius:3mm;padding:3.5mm 4mm}}
.tbx .cap{{font-size:8pt;color:#666;margin-top:1.6mm}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}}
.bingo{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6mm}}
.bg{{aspect-ratio:1.25;border:.4mm solid #333;border-radius:2mm;display:flex;align-items:center;justify-content:center;text-align:center;font-size:9pt;font-weight:800;line-height:1.3}}
.bg.free{{background:#ffe7dc;border-color:#e04a12}}
.bsub{{font-size:8.3pt;color:#555;margin-top:1.6mm}}
.prs{{display:grid;gap:1.6mm}}
.pr{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:.3mm solid #ddd;padding:1.3mm 0}}.pr b{{font-size:10pt;font-weight:800}}.pr span{{font-size:8pt;color:#666}}
.write{{border:.45mm solid #111;border-radius:3mm;padding:3mm 4mm}}
.write .h{{font-size:11.5pt;font-weight:900}}.write .h span{{font-size:8.3pt;font-weight:600;color:#666;margin-left:2mm}}
.line{{border-bottom:.3mm solid #999;height:9mm}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:4mm;border-top:.4mm solid #111;padding-top:2.6mm}}
.foot .qrw{{margin:0;width:17mm;height:17mm}}
.foot .who{{font-size:8.5pt;line-height:1.55;color:#444}}.foot .who b{{font-size:11pt;color:#111}}
.foot .msg{{margin-left:auto;text-align:right;font-size:14pt;font-weight:900;line-height:1.25}}.foot .msg span{{color:#e04a12}}
.pg{{position:absolute;right:12mm;bottom:4mm;font-size:7pt;color:#999}}
</style></head><body>

<section class="page">
  <div class="top"><div><div class="k">제23기 중견리더과정 · 실습 카드</div><h1>공무원을 위한 AI도구 활용법</h1></div>
  <div class="r"><b>2026. 11. 5.(목)</b><br>경상남도인재개발원 601호<br>강사 김경훈</div></div>

  <div class="sec"><i>준비</i>오늘 폰에 이 앱만 있으면 됩니다<span>QR을 폰 카메라로 비추면 바로 열립니다 · 구글 계정 하나면 Gemini·NotebookLM 로그인</span></div>
  <div class="apps">{apps}</div>
  <div class="vote"><span class="big">📱</span><div><b>투표·퀴즈는 강의 화면의 QR</b>을 찍으세요. 로그인 없이 바로 참여합니다. 막히면 <b>옆 사람과 함께</b> 해도 좋습니다.</div></div>

  <div class="sec"><i>실습</i>폰으로 해 봅시다<span>끝낸 미션은 오른쪽 네모에 ✔</span></div>
  <div class="mss">{ms}</div>

  <div class="sec"><i>보안</i>AI에 넣으면 안 되는 것 3가지</div>
  <div class="safe"><div class="h"><small>SAFE</small>넣기 전에<br>한 번 더</div>
    <div class="x"><b>① 개인정보</b><span>주민번호 · 연락처 · 주소<br>민원인 실명</span></div>
    <div class="x"><b>② 비공개 문서</b><span>내부 보고 · 감사 자료<br>원문 그대로</span></div>
    <div class="x"><b>③ 결재 전 자료</b><span>확정 안 된 계획 · 예산<br>아직 나가면 안 되는 숫자</span></div>
    <div class="tip">→ 꼭 필요하면 <b>가명 · 요약</b>으로 바꿔서 넣고, <b>기관 AI 사용 지침</b>을 먼저 확인합니다.  AI 답은 <b>출처 · 숫자 · 과정</b>을 사람이 확인합니다.</div></div>
  <div class="pg">앞면 · {VER}({DATE})</div>
</section>

<section class="page">
  <div class="top"><div><div class="k">MISSION 01 재료 · 이 면을 폰으로 찍으세요</div><h1>종이를 찍으면 표가 됩니다</h1></div>
  <div class="r"><b>ChatGPT 앱 → 카메라(+)</b><br>“이 표를 엑셀 표로 만들어 줘”<br>“민원이 가장 많은 3가지를 요약해 줘”</div></div>

  <div class="tbx"><table><caption>○○시 3분기 생활 민원 접수 현황<span>(단위: 건 · 실습용 가상 자료)</span></caption>
  <tr><th>민원 유형</th><th>7월</th><th>8월</th><th>9월</th><th>합계</th></tr>{rows}</table>
  <div class="cap">더 해 보기 — “8월에 도로 파손이 늘어난 이유를 추측해 줘”, “이 표로 보고서 첫 문단을 공문체로 써 줘”, “막대그래프로 그려 줘”</div></div>

  <div class="two">
    <div><div class="sec"><i>빙고</i>AI 빙고<span>해 본 칸에 ✔</span></div>
      <div class="bingo" style="margin-top:2mm">{bingo}</div>
      <div class="bsub">한 줄(가로·세로·대각선)을 채우면 손을 들어 주세요!</div></div>
    <div><div class="sec"><i>꿀팁</i>이렇게 말하면 잘 됩니다</div>
      <div class="prs" style="margin-top:2mm">{prompts}</div>
      <div class="note" style="margin-top:2.4mm"><b>좋은 질문 = 역할 + 할 일 + 형식</b><br>“너는 홍보 담당자야. 이 행사 안내를 <b>공문체로</b>, <b>세 문단</b>으로 써 줘.”</div></div>
  </div>

  <div class="write"><div class="h">내일 출근해서 해 볼 것 하나<span>강의 끝에 폰으로도 보내 주세요</span></div>
    <div class="line"></div><div class="line"></div></div>

  <div class="foot"><div class="qrw">{qr('https://ssca1612.pages.dev')}</div>
    <div class="who"><b>김경훈</b> · AI 챔피언(BLACK) · 경남소방본부<br>ssca1612.pages.dev · blog.naver.com/ai-sobang<br>ssca1612@korea.kr</div>
    <div class="msg">일단 써 보세요.<br><span>작은 것부터.</span></div></div>
  <div class="pg">뒷면 · {VER}({DATE})</div>
</section>
</body></html>'''
open(OUT, 'w').write(HTML)
print('ok', OUT, 'table total', sum(tot))
