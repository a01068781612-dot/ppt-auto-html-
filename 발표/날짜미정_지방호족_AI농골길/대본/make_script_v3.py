# 발표 대본(왼쪽 슬라이드 · 오른쪽 대사) HTML 생성 v2 — 15분 시간 배분 · 슬라이드는 다 읽지 않고 핵심만 — 사용: python3 make_script_v1.py <슬라이드 jpg 폴더> <출력.html>
#   대사 표기: 한 줄 = 한 문장. {중괄호} = 슬라이드에 없는 표현(파란색), (괄호) = 행동 · 쉼(회색)
import sys, os, re, base64, html
IMG, OUT = sys.argv[1:3]
VER, DATE = 'v.2.0.0', '26.10.21'
# 장별 시간(초) — 영상 4개 8:08 + 말 6:38 = 14:46
SEC = {1: 15, 2: 10, 3: 8, 4: 20, 5: 20, 6: 20, 7: 5, 8: 87, 9: 20, 10: 25, 11: 25, 12: 25, 13: 8, 14: 25, 15: 25, 16: 25, 17: 20, 18: 8, 19: 234,
       20: 8, 21: 22, 22: 22, 23: 22, 24: 15, 25: 20, 26: 142, 27: 10}
VID = {8: '영상1', 11: 'GPTs 시연', 19: '영상2', 26: '영상3'}
S = [
 (1, '오프닝 · 질문', '질문 하나를 던지고 멈춘다 — 오늘 발표 전체가 이 질문의 답',
  ['이 골목, 소방차가 들어갈 수 있습니까?', '(3초 쉬기)', '{저희 팀 지방호족은 이 질문에서 시작했습니다.}']),
 (2, '목차', '세 단계로 답한다 — 길게 읽지 않고 넘어간다',
  ['{오늘은} 왜 만들었나, 무엇을 만들었나, 무엇이 좋아지나 — {세 가지로 말씀드리겠습니다.}']),
 (3, 'PART 1 표지', '문제의 시작은 좁은 골목 — 숫자는 뒤에서 하나씩, 여기선 한 줄만',
  ['{시작은} 좁은 골목{이었습니다.}']),
 (4, '사고', '실제로 사람이 죽었다 — 그리고 화재는 늘고 있었다',
  ['2024년 8월 11일, 부림면 신반리 주택화재.', '{소방차가} 마을 끝까지 못 들어갔고, 사망 1명.', '{의령의 화재는} 55건, 71건, 73건 — {해마다 늘고 있었습니다.}']),
 (5, '내비 vs 펌프차', '문제는 길 찾기가 아니라, 좁은 길을 더 들어갈 수 있느냐',
  ['내비는 "이 길로 더 들어가세요"{라고 합니다.}', '{하지만} 승용차 기준{입니다.}', '펌프차는 차폭 2.5m, 골목에서 멈춥니다.', '더 들어갈 수 있는지는 가본 사람 기억 속에만 {있었습니다.}']),
 (6, '140명 · 1년', '그 답을 만들려고 140명이 1년을 걸었다',
  ['그래서 140명이 239개 마을을 직접 가서 쟀습니다.', '골목마다 실측{하고,} 책을 만들고, 다시 확인{하는 데} 1년{이 걸렸습니다.}']),
 (7, '영상1 소개', '영상으로 넘긴다 — 한 문장',
  ['그 1년을 1분 27초로 {보시겠습니다.}']),
 (8, '🎬 영상1', '그 1년의 현장 — 영상이 말한다',
  ['(영상 재생 1:27 · 말 없음)']),
 (9, '책자 성과', '책은 효과가 있었다 — 3분 단축, 도지사상',
  ['답이 책이 됐고, 출동이 빨라졌습니다.', '현장 대응시간 7~8분에서 4~5분, 약 3분 단축.', '경상남도 적극행정 최우수, 도지사상{을 받았습니다.}']),
 (10, '책 → GPTs', '출동 중에는 책이 느렸다 — 그래서 AI로 90초를 25초로',
  ['{그런데} 출동 중 차 안에서 책을 봅니다.', '{흔들리는 차에서} 267쪽을 넘겨 마을을 찾는 데 90초.', '그래서 AI로 {만들었습니다.}', '마을 이름을 넣으면 25초.', '{이것으로} 소방청장상{을 받았습니다.}']),
 (11, '🎬 GPTs 시연', 'AI 농골길 코치가 실제로 답하는 모습',
  ['(영상 재생 0:25 · 내레이션 있음)']),
 (12, 'PAIN 두 가지', '상을 받고도 두 가지가 남았다 — 만드는 데 1년, 받은 답은 글뿐',
  ['그런데, 두 가지가 남았습니다.', '{하나,} 답을 만드는 데 1년 — 경남 18개 소방서가 또 해야 합니다.', '{둘,} 받은 답은 글뿐 — 어디까지 들어갈 수 있는지 지도로 안 보입니다.', '답을 빨리 만들고, 지도로 보여 줘야 했습니다.']),
 (13, 'PART 2 표지', '해법의 한 줄 — 지도에게 묻다',
  ['{그래서} 지도에게 물었습니다.']),
 (14, '내비 · GPTs · 우리', '내비는 소방차 폭을 모르고, GPTs는 "어디서" 막히는지 모른다 — 우리는 지도 위에 그 자리',
  ['내비는 길은 나오지만, 소방차 폭은 모릅니다.', 'GPTs는 표는 있지만, 그 자리는 모릅니다.', '{저희는} 지도 위에 그 자리{를 보여 줍니다.}']),
 (15, '원리', '사람이 가지 않고 지도로 폭을 재고, 코너까지 계산한다',
  ['사람 대신 지도로 폭을 잽니다.', '도로 대장 폭{에 더해,} 위성사진 AI가 포장 폭을 직접 잽니다.', '{그리고} 코너까지 — 중형펌프차가 90° 코너를 돌려면 3.62m{가} 필요{합니다.}', '사람이 가지 않아도, 마을 이름만으로 판정{합니다.}']),
 (16, '70% → 84%', '5주 동안 고쳐 70%를 84%로 — 같은 주소라도 차 폭마다 다른 답',
  ['처음엔 70%, {5주 동안} 고쳐서 84%{가 됐습니다.}', '같은 주소{라도} 차 폭마다 다른 답{이 나옵니다.}', '{차가 클수록 더 많이 올랐습니다.}', '정답지는 한 번도 보지 않고 {올린 숫자입니다.}']),
 (17, '정답지 대조', '사람이 1년 걸려 그린 선과 AI 선이 겹친다',
  ['사람이 1년 걸려 그린 선{과} AI가 그린 선{을 겹쳐 봤습니다.}', '정곡면 16개 마을, 16곳 일치.']),
 (18, '영상2 소개', '실제로 돌아가는 모습으로 넘긴다',
  ['지번을 넣으면 소방차 길이 그려집니다.', '{직접 보시겠습니다.}']),
 (19, '🎬 영상2', '주소 하나로 길 · 세울 곳 · 호스 본수까지 — 영상이 말한다',
  ['(영상 재생 3:54 · 말 없음)']),
 (20, 'PART 3 표지', '이제 숫자로 — 시간 · 예산 · 골든타임',
  ['{이제} 숫자로 {보겠습니다.}', '시간, 예산, 골든타임.']),
 (21, '기대효과 1 · 시간', '140명 1년이 4명 5주로 — 의령 한 곳에서 65,832시간',
  ['지금은 140명이 1년, 66,000시간.', '우리는 4명이 5주, 168시간.', '{의령 한 곳에서} 65,832시간{을 아낍니다.}', '경남 18개 소방서{면} 약 118만 시간{입니다.}']),
 (22, '기대효과 2 · 예산', '6억 6천만 원이 366만 원으로 — 경남이면 약 119억',
  ['지금은 인건비 6억 6,000만에 책 515만.', '우리는 168시간 × 2만{원에} 구독료 30만.', '{의령에서} 6억 6,149만 원, 경남{으로 넓히면} 약 119억 원{입니다.}']),
 (23, '기대효과 3 · 골든타임', '책자 3분, GPTs 65초 — 이번 프로젝트는 +80초가 목표',
  ['책자{로} 3분, GPTs{로} 65초{를 줄였습니다.}', '이번 프로젝트{의} 목표는 +80초{입니다.}', '판단 10초 이내, 호스 전개 1분 이내.']),
 (24, '다시 그 골목', '첫 질문으로 돌아온다 — 이제는 답할 수 있다',
  ['{처음 질문, 다시 드리겠습니다.}', '이 골목, 소방차가 들어갈 수 있습니까?', '(2초 쉬기)', '이제는 답할 수 있습니다.']),
 (25, 'P.S.', '기술을 배우러 와서, 사람을 얻었다',
  ['{마지막으로,} 기술을 배우러 와서, 사람을 얻었습니다.', '인사, 경찰, 소방, 해경 — 네 시선이 한 길에 {모였습니다.}', '이름만 알던 사이에서 동료가 됐습니다.']),
 (26, '🎬 영상3 엔딩', '26-1기, 최고였습니다 — 영상으로 마무리',
  ['(영상 재생 2:22 · 말 없음)']),
 (27, 'Q&A', '질문을 받는다',
  ['{감사합니다.}', '{질문 받겠습니다.}']),
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
td{{border-top:2px solid #222;vertical-align:top;padding:14px 10px}} tr{{page-break-inside:avoid}} td.sl{{width:42%}} td.sl img{{width:100%;border-radius:6px;display:block}}
.no{{font-size:28px;font-weight:900;color:#ff5a1f;margin-bottom:4px}} .tg{{font-size:13px;color:#666;margin-top:6px}}
.msg{{background:#fff3ec;border-left:5px solid #ff5a1f;padding:10px 14px;margin-bottom:12px;font-size:15px;line-height:1.5}}
.msg b{{display:block;color:#ff5a1f;font-size:13px;margin-bottom:2px}}
.ln{{font-size:19px;line-height:1.55;padding:3px 0;border-bottom:1px dashed #e4e4e4}}

.tm{{display:inline-block;background:#222;color:#fff;font-size:14px;font-weight:700;padding:3px 10px;border-radius:12px;margin-bottom:8px}}
.tt td{{border:1px solid #ddd;padding:3px 6px;font-size:12px;text-align:center}} .tt td.v{{background:#fff3ec;color:#c2410c;font-weight:700}}
.off{{color:#1f6fe5;font-weight:600}} .cue{{color:#999;font-style:italic}}
table.h td{{border:1px solid #ccc;padding:4px 8px;font-size:12px}}
</style></head><body>
<h1>지방호족 발표 대본 — 전체(1~27장)</h1>
<div class="sub">{VER} ({DATE}) · 기준: PPT v.3.1.0(27장)</div>
<div class="lg"><span>검정 = 슬라이드에 있는 말</span><span class="off">파랑 = 슬라이드에 없는 말(덧붙이는 말)</span><span class="cue">(회색) = 행동 · 쉼</span></div>
<div style="margin-top:10px;font-size:14px"><b>15분 시간 배분</b> — 영상 4개 8:08(전체의 절반) + 말 6:38 = <b>14:46</b> · 말하는 장은 평균 17초(2~3문장)</div>
<table class="tt"><tr>{''.join(f'<td class="{"v" if k in VID else ""}">{k}</td>' for k in sorted(SEC))}</tr><tr>{''.join(f'<td class="{"v" if k in VID else ""}">{VID.get(k, "")}{" " if k in VID else ""}{SEC[k]}초</td>' for k in sorted(SEC))}</tr></table>
<table>{rows}</table>
<h3 style="margin-top:22px">변경 이력</h3>
<table class="h"><tr><td>버전</td><td>날짜</td><td>수정 내용</td></tr><tr><td>{VER}</td><td>{DATE}</td><td>전체 27장 작성 — 15분 배분 그대로, 영상 4개는 재생 표시만</td></tr><tr><td>v.1.1.0</td><td>{DATE}</td><td>15분에 맞춤 — 장별 시간 · 누적 시간 표시, 슬라이드를 다 읽지 않고 핵심 한두 문장만</td></tr><tr><td>v.1.0.0</td><td>{DATE}</td><td>새 구성(27장) 기준 첫 작성 — 1~3장. 장마다 "전할 메시지" + 한 문장씩 + 슬라이드에 없는 말 파랑 표시</td></tr></table>
</body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print(OUT)
