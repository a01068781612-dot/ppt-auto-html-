# 모션 화면(HyperFrames index.html)에 실제로 들어간 글자를 장별로 뽑는다 → 대본은 이 글자를 바탕으로 쓴다
# 사용: python3 extract_text.py <dir1> <dir2> ...   (각 dir 안의 index.html)
import re, html, sys
for d in sys.argv[1:]:
    s = open(d.rstrip('/') + '/index.html', encoding='utf-8').read()
    b = s[s.index('<body>'):s.index('<script>', s.index('<body>'))]
    b = re.sub(r'<br\s*/?>', ' / ', b)
    b = re.sub(r'</(div|h3|p|i|b|em|span)>', ' ', b)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', b))
    print('##', d, ':', re.sub(r'\s+', ' ', t).strip(), '\n')
