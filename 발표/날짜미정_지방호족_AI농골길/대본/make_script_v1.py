# 발표 대본(왼쪽 슬라이드 · 오른쪽 대사) HTML 생성 — 사용: python3 make_script_v1.py <슬라이드 jpg 폴더> <출력.html>
#   대사 표기: 한 줄 = 한 문장. {중괄호} = 슬라이드에 없는 표현(파란색), (괄호) = 행동 · 쉼(회색)
import sys, os, re, base64, html
IMG, OUT = sys.argv[1:3]
VER, DATE = 'v.1.0.0', '26.10.21'
S = [
 (1, '오프닝 · 질문', '청중에게 질문 하나를 던진다 — "이 골목, 소방차가 들어갈 수 있습니까?" 오늘 발표는 이 질문에 답하는 이야기',
  ['{안녕하십니까,} 팀 지방호족입니다.',
   '인사혁신처, 경찰, 소방, 해양경찰 — {네 기관이 한 팀입니다.}',
   '{사진 한 장 보시겠습니다.}',
   '이 골목, 소방차가 들어갈 수 있습니까?',
   '(3초 쉬기)',
   '{솔직히, 저희도 몰랐습니다.}']),
 (2, '목차', '발표는 세 단계 — 왜 만들었나 · 무엇을 만들었나 · 무엇이 좋아지나. 모두 "질문 하나"에 대한 답',
  ['오늘은 질문 하나에 답합니다.',
   '{첫째,} 왜 만들었나 — 골목이 좁아 소방차가 못 들어갔습니다.',
   '{둘째,} 무엇을 만들었나 — 주소만 넣으면 지도에 길이 그려집니다.',
   '{셋째,} 무엇이 좋아지나 — 시간, 예산, 골든타임을 숫자로 {보여 드리겠습니다.}']),
 (3, 'PART 1 표지', '문제의 시작은 "좁은 골목". 이 파트에서 나올 숫자 네 개(사망 1명 · 239개 마을 · 140명 1년 · 90초 → 25초)를 미리 깔아 둔다',
  ['{먼저,} 왜 만들었나입니다.',
   '골목이 좁아, 소방차가 마을 끝까지 못 들어갔습니다.',
   '{그 골목에서} 사망 1명.',
   '{그래서} 239개 마을을, 140명이 1년 동안 {직접 쟀습니다.}',
   '{그리고 출동 중 판단을} 90초에서 25초로 {줄였습니다.}',
   '{이 숫자들이 어떻게 나왔는지, 하나씩 말씀드리겠습니다.}']),
]
def line(t):
    t = html.escape(t)
    t = re.sub(r'\{(.+?)\}', r'<span class="off">\1</span>', t)
    t = re.sub(r'^\((.+)\)$', r'<span class="cue">(\1)</span>', t)
    return f'<div class="ln">{t}</div>'
rows = ''
for n, tag, msg, lines in S:
    b64 = base64.b64encode(open(os.path.join(IMG, f'p{n:03d}.jpg'), 'rb').read()).decode()
    rows += (f'<tr><td class="sl"><div class="no">{n}</div><img src="data:image/jpeg;base64,{b64}"><div class="tg">{tag}</div></td>'
             f'<td class="sc"><div class="msg"><b>전할 메시지</b>{html.escape(msg)}</div>{"".join(line(x) for x in lines)}</td></tr>')
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>지방호족 발표 대본</title><style>
@font-face{{font-family:P;src:url("PretendardVariable.woff2")}}
body{{font-family:P,"Pretendard","Malgun Gothic",sans-serif;margin:28px;color:#1b1b1b;background:#fff}}
h1{{font-size:24px;margin:0 0 4px}} .sub{{color:#666;font-size:13px;margin-bottom:12px}}
.lg span{{margin-right:16px;font-size:13px}} table{{width:100%;border-collapse:collapse;margin-top:10px}}
td{{border-top:2px solid #222;vertical-align:top;padding:14px 10px}} td.sl{{width:42%}} td.sl img{{width:100%;border-radius:6px;display:block}}
.no{{font-size:28px;font-weight:900;color:#ff5a1f;margin-bottom:4px}} .tg{{font-size:13px;color:#666;margin-top:6px}}
.msg{{background:#fff3ec;border-left:5px solid #ff5a1f;padding:10px 14px;margin-bottom:12px;font-size:15px;line-height:1.5}}
.msg b{{display:block;color:#ff5a1f;font-size:13px;margin-bottom:2px}}
.ln{{font-size:19px;line-height:1.55;padding:3px 0;border-bottom:1px dashed #e4e4e4}}
.off{{color:#1f6fe5;font-weight:600}} .cue{{color:#999;font-style:italic}}
table.h td{{border:1px solid #ccc;padding:4px 8px;font-size:12px}}
</style></head><body>
<h1>지방호족 발표 대본 — PART 1 앞부분(1~3장)</h1>
<div class="sub">{VER} ({DATE}) · 기준: PPT v.3.1.0(27장)</div>
<div class="lg"><span>검정 = 슬라이드에 있는 말</span><span class="off">파랑 = 슬라이드에 없는 말(덧붙이는 말)</span><span class="cue">(회색) = 행동 · 쉼</span></div>
<table>{rows}</table>
<h3 style="margin-top:22px">변경 이력</h3>
<table class="h"><tr><td>버전</td><td>날짜</td><td>수정 내용</td></tr><tr><td>{VER}</td><td>{DATE}</td><td>새 구성(27장) 기준 첫 작성 — 1~3장. 장마다 "전할 메시지" + 한 문장씩 + 슬라이드에 없는 말 파랑 표시</td></tr></table>
</body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print(OUT)
