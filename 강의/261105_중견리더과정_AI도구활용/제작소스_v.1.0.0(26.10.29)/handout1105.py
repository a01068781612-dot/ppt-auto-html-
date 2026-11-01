# 제출·배부용 강의안 PDF 생성기 v.1.0.0
# 슬라이드 마지막 장면(last.png) 중 교육생에게 줄 장만 골라 A4 세로, 한 쪽에 3장 + 메모 칸
# 빼는 장: 📌 자리표시(영상·사진) · 퀴즈·투표·정답 공개(현장 재미용) · 쉬는 시간
# 사용: python3 handout1105.py <모션 렌더 폴더 HF> <출력 html>  → playwright로 PDF
import sys, os, io, base64
from PIL import Image

HF, OUT = sys.argv[1], sys.argv[2]
VER, DATE = 'v.1.0.0', '26.10.29'

PICK = [
    ('오프닝', 'toc', '오늘 강의 순서'),
    ('PART 1 · AI 도구 지도', 'p1in', ''), ('PART 1 · AI 도구 지도', 'toolmap', '무엇을 하고 싶은가로 고릅니다'),
    ('PART 1 · AI 도구 지도', 'freepaid', '처음엔 무료로 충분합니다'), ('PART 1 · AI 도구 지도', 'apps', 'QR로 바로 열기'),
    ('PART 2 · 폰으로 해 봅시다', 'p2in', ''), ('PART 2 · 폰으로 해 봅시다', 'm1', '미션 1'), ('PART 2 · 폰으로 해 봅시다', 'm2', '미션 2'),
    ('PART 2 · 폰으로 해 봅시다', 'm3', '미션 3'), ('PART 2 · 폰으로 해 봅시다', 'm4', '미션 4 — 정답은 강의에서'),
    ('PART 3 · 노트북으로 만들기', 'p3in', ''), ('PART 3 · 노트북으로 만들기', 'showcase', ''), ('PART 3 · 노트북으로 만들기', 'share', '만든 것을 폰으로 보내는 법'),
    ('PART 3 · 노트북으로 만들기', 'sum_p3', ''),
    ('PART 4 · AI는 지금 어디까지', 'p4in', ''), ('PART 4 · AI는 지금 어디까지', 'sum01', 'AI 에이전트'), ('PART 4 · AI는 지금 어디까지', 'sum03', '프롬프트 그다음'),
    ('PART 4 · AI는 지금 어디까지', 'ladder', ''), ('PART 4 · AI는 지금 어디까지', 'compare', ''),
    ('PART 5 · 리더가 알아야 할 것', 'p5in', ''), ('PART 5 · 리더가 알아야 할 것', 'security', ''), ('PART 5 · 리더가 알아야 할 것', 'review', ''),
    ('마무리', 'act', ''), ('마무리', 'closing', ''), ('마무리', 'qna', ''),
]

def img(id, w=1280):
    im = Image.open(os.path.join(HF, id, 'last.png')).convert('RGB')
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

FLOW = [('오프닝', '설문·사진 퀴즈(폰 투표) · 강사 소개'), ('PART 1', 'AI 도구 지도 — 무료로 쓰는 도구 한눈에'), ('PART 2', '폰으로 해 봅시다 — 미션 네 가지'),
        ('PART 3', '노트북으로 만들기 — 말로 만드는 업무 도구'), ('PART 4', 'AI는 지금 어디까지 — 대답하는 AI에서 일하는 AI로'),
        ('PART 5', '리더가 알아야 할 것 — 보안·확인·결과물 보는 법'), ('마무리', '일단 써 보세요. 작은 것부터.')]

cards = []
for i, (part, id, cap) in enumerate(PICK):
    cards.append(f'''<div class="it"><div class="sl"><img src="{img(id)}"><span class="no">{i+1}</span></div>
<div class="memo"><div class="pt">{part}</div>{f'<div class="cp">{cap}</div>' if cap else ''}<div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div></div></div>''')
pages = [cards[k:k + 3] for k in range(0, len(cards), 3)]
total = len(pages) + 1

flow = ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in FLOW)
html = f'''<!doctype html><html lang="ko"><head>
<!--
## 변경 이력
| 버전 | 날짜 | 수정 내용 |
|---|---|---|
| v.1.0.0 | 26.10.29 | 최초 작성 — 제출·배부용 강의안: 표지(강의 개요·흐름) + 슬라이드 {len(PICK)}장(한 쪽 3장 + 메모 칸). 영상·사진 장, 퀴즈·투표·정답 공개 장, 쉬는 시간은 뺌 |
-->
<meta charset="utf-8"><title>강의안 — 공무원을 위한 AI도구 활용법</title><style>
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0;word-break:keep-all}}
body{{font-family:Pretendard,sans-serif;color:#111}}
.page{{width:210mm;height:297mm;padding:12mm 13mm 10mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column}}
.page:last-child{{page-break-after:auto}}
.hd{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:.5mm solid #111;padding-bottom:2mm;margin-bottom:4mm;font-size:8.5pt;color:#555}}.hd b{{color:#111;font-weight:800}}
.it{{display:grid;grid-template-columns:118mm 1fr;gap:5mm;margin-bottom:6mm}}
.sl{{position:relative}}.sl img{{width:118mm;height:66.4mm;display:block;border-radius:1.5mm;border:.3mm solid #999}}
.no{{position:absolute;left:-1.5mm;top:-1.5mm;background:#ff5a1f;color:#111;font-size:8pt;font-weight:900;border-radius:5mm;padding:.3mm 2mm}}
.memo{{display:flex;flex-direction:column}}.pt{{font-size:8pt;font-weight:800;color:#e04a12;letter-spacing:.06em}}.cp{{font-size:10pt;font-weight:800;margin-top:1mm}}
.ln{{border-bottom:.3mm solid #bbb;height:9.5mm}}
.ft{{position:absolute;left:13mm;right:13mm;bottom:6mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#888}}
.cv .k{{font-size:9pt;font-weight:800;letter-spacing:.2em;color:#e04a12;margin-top:6mm}}
.cv h1{{font-size:30pt;font-weight:900;letter-spacing:-.03em;line-height:1.2;margin-top:3mm;position:relative;padding-left:7mm}}
.cv h1:before{{content:"";position:absolute;left:0;top:1mm;width:5mm;height:5mm;border-left:1mm solid #111;border-top:1mm solid #111}}
.cv .sub{{font-size:13pt;color:#444;margin-top:3mm;padding-left:7mm}}
.cv .hero{{margin:6mm 0 5mm}}.cv .hero img{{width:100%;border-radius:2mm;display:block}}
.info{{width:100%;border-collapse:collapse;font-size:10.5pt}}.info th,.info td{{border-bottom:.3mm solid #ccc;padding:2mm 2mm;text-align:left;vertical-align:top}}
.info th{{width:26mm;font-weight:800;color:#555}}
h2{{font-size:12.5pt;font-weight:900;margin:5mm 0 1.5mm}}
.note{{margin-top:auto;margin-bottom:6mm;font-size:9pt;color:#444;background:#f3f1ee;border-radius:2mm;padding:3mm 4mm;line-height:1.6}}.note b{{color:#111}}
</style></head><body>
<section class="page cv">
  <div class="k">경상남도인재개발원 · 제23기 중견리더과정</div>
  <h1>공무원을 위한 AI도구 활용법 소개</h1>
  <div class="sub">폰 하나로 오늘부터 — 묻고, 만들고, 맡기는 AI</div>
  <div class="hero"><img src="{img('cover', 1600)}"></div>
  <table class="info"><tr><th>일시</th><td>2026. 11. 5.(목) 13:00 ~ 14:50</td></tr><tr><th>장소</th><td>경상남도청 서부청사 6층 601호</td></tr>
  <tr><th>강사</th><td>김경훈 · 경남소방본부 · AI 챔피언(BLACK)<br><span style="color:#666">ssca1612.pages.dev · blog.naver.com/ai-sobang · ssca1612@korea.kr</span></td></tr></table>
  <h2>강의 흐름</h2><table class="info">{flow}</table>
  <div class="note"><b>준비물</b> 스마트폰 (ChatGPT · Gemini 앱 설치, 구글 계정 로그인이면 충분합니다)<br>
  <b>실습 카드</b>를 함께 보시면서 따라 하세요. 강의 중 퀴즈·투표는 화면의 QR로 참여합니다.</div>
  <div class="ft"><span>공무원을 위한 AI도구 활용법 · 강의안 {VER}({DATE})</span><span>1 / {total}</span></div>
</section>
''' + ''.join(f'''<section class="page"><div class="hd"><span><b>공무원을 위한 AI도구 활용법</b> · 제23기 중견리더과정</span><span>2026. 11. 5 · 김경훈</span></div>
{''.join(p)}<div class="ft"><span>강의안 {VER}({DATE})</span><span>{n+2} / {total}</span></div></section>''' for n, p in enumerate(pages)) + '</body></html>'
open(OUT, 'w').write(html)
print('ok', OUT, len(PICK), 'slides', total, 'pages')
