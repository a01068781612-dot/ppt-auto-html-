# 발표 대본(왼쪽 슬라이드 · 오른쪽 대사) HTML 생성 v2 — 15분 시간 배분 · 슬라이드는 다 읽지 않고 핵심만 — 사용: python3 make_script_v1.py <슬라이드 jpg 폴더> <출력.html>
#   대사 표기: 한 줄 = 한 문장. {중괄호} = 슬라이드에 없는 표현(파란색), (괄호) = 행동 · 쉼(회색)
import sys, os, re, base64, html
IMG, OUT = sys.argv[1:3]
VER, DATE = 'v.1.1.0', '26.10.21'
# 장별 시간(초) — 영상 4개 8:08 + 말 6:38 = 14:46
SEC = {1: 15, 2: 10, 3: 8, 4: 20, 5: 20, 6: 20, 7: 5, 8: 87, 9: 20, 10: 25, 11: 25, 12: 25, 13: 8, 14: 25, 15: 25, 16: 25, 17: 20, 18: 8, 19: 234,
       20: 8, 21: 22, 22: 22, 23: 22, 24: 15, 25: 20, 26: 142, 27: 10}
VID = {8: '영상1', 11: 'GPTs 시연', 19: '영상2', 26: '영상3'}
S = [
 (1, '오프닝 · 질문', '질문 하나를 던지고 멈춘다 — 오늘 발표 전체가 이 질문의 답',
  ['이 골목, 소방차가 들어갈 수 있습니까?',
   '(3초 쉬기)',
   '{저희 팀 지방호족은 이 질문에서 시작했습니다.}']),
 (2, '목차', '세 단계로 답한다 — 길게 읽지 않고 넘어간다',
  ['{오늘은} 왜 만들었나, 무엇을 만들었나, 무엇이 좋아지나 — {세 가지로 말씀드리겠습니다.}']),
 (3, 'PART 1 표지', '문제의 시작은 좁은 골목 — 숫자는 뒤에서 하나씩, 여기선 한 줄만',
  ['{시작은} 좁은 골목{이었습니다.}']),
]
def line(t):
    t = html.escape(t)
    t = re.sub(r'\{(.+?)\}', r'<span class="off">\1</span>', t)
    t = re.sub(r'^\((.+)\)$', r'<span class="cue">(\1)</span>', t)
    return f'<div class="ln">{t}</div>'
rows = ''
cum = {}; t = 0
for k in sorted(SEC): t += SEC[k]; cum[k] = t
mmss = lambda x: f'{x // 60}:{x % 60:02d}'
for n, tag, msg, lines in S:
    b64 = base64.b64encode(open(os.path.join(IMG, f'p{n:03d}.jpg'), 'rb').read()).decode()
    rows += (f'<tr><td class="sl"><div class="no">{n}</div><img src="data:image/jpeg;base64,{b64}"><div class="tg">{tag}</div></td>'
             f'<td class="sc"><div class="tm">⏱ {SEC[n]}초 · 누적 {mmss(cum[n])}</div><div class="msg"><b>전할 메시지</b>{html.escape(msg)}</div>{"".join(line(x) for x in lines)}</td></tr>')
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

.tm{{display:inline-block;background:#222;color:#fff;font-size:14px;font-weight:700;padding:3px 10px;border-radius:12px;margin-bottom:8px}}
.tt td{{border:1px solid #ddd;padding:3px 6px;font-size:12px;text-align:center}} .tt td.v{{background:#fff3ec;color:#c2410c;font-weight:700}}
.off{{color:#1f6fe5;font-weight:600}} .cue{{color:#999;font-style:italic}}
table.h td{{border:1px solid #ccc;padding:4px 8px;font-size:12px}}
</style></head><body>
<h1>지방호족 발표 대본 — PART 1 앞부분(1~3장)</h1>
<div class="sub">{VER} ({DATE}) · 기준: PPT v.3.1.0(27장)</div>
<div class="lg"><span>검정 = 슬라이드에 있는 말</span><span class="off">파랑 = 슬라이드에 없는 말(덧붙이는 말)</span><span class="cue">(회색) = 행동 · 쉼</span></div>
<div style="margin-top:10px;font-size:14px"><b>15분 시간 배분</b> — 영상 4개 8:08(전체의 절반) + 말 6:38 = <b>14:46</b> · 말하는 장은 평균 17초(2~3문장)</div>
<table class="tt"><tr>{''.join(f'<td class="{"v" if k in VID else ""}">{k}</td>' for k in sorted(SEC))}</tr><tr>{''.join(f'<td class="{"v" if k in VID else ""}">{VID.get(k, "")}{" " if k in VID else ""}{SEC[k]}초</td>' for k in sorted(SEC))}</tr></table>
<table>{rows}</table>
<h3 style="margin-top:22px">변경 이력</h3>
<table class="h"><tr><td>버전</td><td>날짜</td><td>수정 내용</td></tr><tr><td>{VER}</td><td>{DATE}</td><td>15분에 맞춤 — 장별 시간 · 누적 시간 표시, 슬라이드를 다 읽지 않고 핵심 한두 문장만</td></tr><tr><td>v.1.0.0</td><td>{DATE}</td><td>새 구성(27장) 기준 첫 작성 — 1~3장. 장마다 "전할 메시지" + 한 문장씩 + 슬라이드에 없는 말 파랑 표시</td></tr></table>
</body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print(OUT)
