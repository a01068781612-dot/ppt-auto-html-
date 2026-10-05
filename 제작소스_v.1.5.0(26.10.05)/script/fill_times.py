# 대본 md 표의 ⏱ 열에 장마다 시작 시각을 채우고, 파트별 처음·중간·끝 표시를 단다
# 사용: python3 fill_times.py <대본.md> <durations.json> <out.md>
#  durations.json 예: {"seconds": {"1": 40, "2": 30, "3": 184, ...}, "parts": [["오프닝",1,6], ["PART 1",7,8], ...]}
#  - 말하는 장: 20~45초(제목·인트로 20~40, 정리 30~35, 사진·기사 35~45)
#  - 영상 장: 실제 길이(ffprobe) + 앞뒤 멘트 0~20초,  시연: 분 단위로 따로
#  표는 "| 장 | ⏱ | 화면 | 📌 짚을 곳 | 🎤 대사 |" 형식이어야 함
import re, json, sys
md, dj, out = sys.argv[1:4]
J = json.load(open(dj)); dur = {int(k): float(v) for k, v in J['seconds'].items()}
start, t = {}, 0
for n in sorted(dur): start[n] = t; t += dur[n]
mm = lambda s: f"{int(round(s))//60}:{int(round(s))%60:02d}"
mark = {}
for name, a, b in J['parts']:
    mark[a] = '▶ 처음'; mark[b] = '■ 끝'
    if b - a >= 2:
        mid = (start[a] + start[b] + dur[b]) / 2
        m = min(range(a + 1, b), key=lambda n: abs(start[n] - mid)); mark[m] = '◆ 중간'
s = open(md, encoding='utf-8').read()
s = re.sub(r'^\| (\d+) \|[^|]*\|', lambda m: f"| {m.group(1)} | **{mm(start[int(m.group(1))])}**" + (f"<br>{mark[int(m.group(1))]}" if int(m.group(1)) in mark else '') + ' |', s, flags=re.M)
open(out, 'w', encoding='utf-8').write(s)
print('전체', mm(t))
for name, a, b in J['parts']: print(name, mm(start[a]), '→', mm(start[b] + dur[b]))
