import re, sys, ast
from hwpx.document import HwpxDocument
src = open('doc2.py').read()
S = ast.literal_eval(src[src.index('S=[')+2:src.index(']\nD.add_paragraph()')+1])
MM = 283.465
doc = HwpxDocument.new()
doc.set_page_setup(paper_size='A4', orientation='landscape', margins_mm={'left':15,'right':15,'top':12,'bottom':12}, header_margin_mm=0, footer_margin_mm=0)
F = '맑은 고딕'
st_title = doc.ensure_run_style(bold=True, size=16, color='#111827', font=F)
st_title_b = doc.ensure_run_style(bold=True, size=16, color='#2F80ED', font=F)
st_note = doc.ensure_run_style(size=10, color='#4B5563', font=F)
st_h = doc.ensure_run_style(bold=True, size=11, color='#111827', font=F)
st_body = doc.ensure_run_style(size=12.5, color='#111827', font=F)
st_bold = doc.ensure_run_style(bold=True, size=12.5, color='#2F80ED', font=F)
st_time = doc.ensure_run_style(size=11, color='#9CA3AF', font=F)
st_cap = doc.ensure_run_style(bold=True, size=10.5, color='#111827', font=F)
st_capt = doc.ensure_run_style(size=10.5, color='#6B7280', font=F)
st_small = doc.ensure_run_style(size=10, color='#111827', font=F)

def runs(par, text, base, bold):
    m = re.match(r'^(.*?)\s*(\(\d:\d\d\))\s*$', text)
    body, tm = (m.group(1), m.group(2)) if m else (text, None)
    for i, seg in enumerate(re.split(r'\*\*', body)):
        if seg: par.add_run(seg, char_pr_id_ref=bold if i % 2 else base)
    if tm: par.add_run('  ' + tm, char_pr_id_ref=st_time)

p = doc.add_paragraph('', include_run=False)
p.add_run('적극행정 우수사례 발표 대본', char_pr_id_ref=st_title_b); p.add_run('  —  재난 골든타임, 세 번 앞당기다', char_pr_id_ref=st_title)
p = doc.add_paragraph('', include_run=False)
p.add_run('발표자 박중휘 · 총 약 4분 37초(영상 2개 2분 11초 포함) · 남성 기준 천천히(초당 약 4음절) · ', char_pr_id_ref=st_note)
p.add_run('파란 굵은 글씨', char_pr_id_ref=doc.ensure_run_style(bold=True, size=10, color='#2F80ED', font=F)); p.add_run(' = 슬라이드에 없는 말 · 괄호 = 그 문장이 끝나는 목표 시각', char_pr_id_ref=st_note)
p = doc.add_paragraph('', include_run=False); p.add_run('변경 이력', char_pr_id_ref=st_h)
W = int(267 * MM)
vt = doc.add_table(3, 3, width=W)
vt.set_column_widths([int(30*MM), int(30*MM), W - int(60*MM)])
rows = [('버전','날짜','수정 내용'),
        ('v.1.2.0','26.10.15','한글(hwpx) 양식, PPT v.2.4.0(4장 태그 위치·모션) 화면 반영'),
        ('v.1.1.0','26.10.15','3장 "재해가 끝나도", 8개 기관, 영상2 1분 26초 반영(6장 이후 +6초)')]
for r, row in enumerate(rows):
    for c, txt in enumerate(row):
        cell = vt.cell(r, c); cell.set_text('')
        par = cell.paragraphs[0]; par.add_run(txt, char_pr_id_ref=st_h if r == 0 else st_small)
        if r == 0: vt.set_cell_shading(r, c, '#E8EEF7') if hasattr(vt, 'set_cell_shading') else None
doc.add_paragraph('')
LW, RW = int(124 * MM), W - int(124 * MM)
t = doc.add_table(len(S) + 1, 2, width=W)
t.set_column_widths([LW, RW])
for c, txt in enumerate(['발표 슬라이드', '발표 스크립트']):
    cell = t.cell(0, c); cell.set_text(''); cell.paragraphs[0].add_run(txt, char_pr_id_ref=st_h)
    try: t.set_cell_shading(0, c, '#E8EEF7')
    except Exception: pass
for i, (n, title, tm, lines) in enumerate(S, 1):
    left = t.cell(i, 0); left.set_text('')
    bid = doc.add_image(open(f'v24-{n}.png', 'rb').read(), 'png')
    pw = int(118 * MM); ph = int(pw * 9 / 16)
    left.paragraphs[0].add_picture(bid, width=pw, height=ph, treat_as_char=True)
    cp = left.add_paragraph(''); cp.add_run(title, char_pr_id_ref=st_cap); cp.add_run('   ' + tm, char_pr_id_ref=st_capt)
    right = t.cell(i, 1); right.set_text('')
    first = True
    for ln in lines:
        par = right.paragraphs[0] if first else right.add_paragraph('')
        first = False
        runs(par, ln, st_body, st_bold)
        right.add_paragraph('')
doc.save_to_path(sys.argv[1]); print('ok')
