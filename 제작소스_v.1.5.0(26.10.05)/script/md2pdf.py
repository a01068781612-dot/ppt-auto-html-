# 대본 md → A4 가로 PDF (표 · 굵은 글씨 주황 · 영상 장 회색 · 쪽 번호)
# 사용: python3 md2pdf.py <대본.md> <out.pdf>   (playwright-core + Chromium 필요, 글꼴 Pretendard 설치)
import re, html, sys, subprocess, os, tempfile
src = open(sys.argv[1], encoding='utf-8').read(); outpdf = os.path.abspath(sys.argv[2])
def inline(t):
    t = html.escape(t, quote=False).replace('&lt;br&gt;', '<br>')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); return re.sub(r'`(.+?)`', r'<code>\1</code>', t)
lines = src.split('\n'); out = []; i = 0; sec = None; hist = None
while i < len(lines):
    l = lines[i]
    if l.startswith('|'):
        tb = []
        while i < len(lines) and lines[i].startswith('|'): tb.append(lines[i]); i += 1
        rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in tb]
        hdr = rows[0]; cls = 'script' if hdr[0] == '장' and len(hdr) == 5 else ('tl' if hdr[0] == '구간' else 'meta')
        h = '<table class="%s"><thead><tr>%s</tr></thead><tbody>' % (cls, ''.join(f'<th>{inline(c)}</th>' for c in hdr))
        for r in rows[2:]:
            h += '<tr%s>%s</tr>' % (' class="vid"' if cls == 'script' and '🎬' in r[2] else '', ''.join(f'<td>{inline(c)}</td>' for c in r))
        h += '</tbody></table>'
        if sec == '변경 이력': hist = h
        else: out.append(h)
        continue
    if l.startswith('# '): out.append(f'<h1>{inline(l[2:])}</h1>')
    elif l.startswith('## '):
        sec = l[3:].strip()
        if sec != '변경 이력': out.append(f'<h2>{inline(sec)}</h2>')
    elif l.startswith('- '): out.append(f'<p class="li">• {inline(l[2:])}</p>')
    elif l.strip() and l.strip() != '---': out.append(f'<p>{inline(l)}</p>')
    i += 1
body = '\n'.join(out) + (f'<h3>변경 이력</h3>{hist}' if hist else '')
css = '''@page{size:A4 landscape}body{font-family:"Pretendard",sans-serif;color:#1a1817;font-size:10.5pt;line-height:1.5}
h1{font-size:20pt;margin:0 0 6px;border-left:8px solid #ff5a1f;padding-left:10px}h2{font-size:14pt;margin:14px 0 6px;border-bottom:2px solid #ff5a1f;padding-bottom:3px;break-after:avoid}
h3{font-size:10pt;margin:16px 0 4px;color:#777}p{margin:3px 0}p.li{margin:2px 0 2px 6px;color:#333}
table{width:100%;border-collapse:collapse;margin:4px 0 8px}th{background:#1d1a19;color:#fff;padding:5px 6px;text-align:left;font-size:9.5pt}
td{border-bottom:1px solid #ddd;padding:6px;vertical-align:top}tr{break-inside:avoid}
table.script td:nth-child(1){width:3.5%;text-align:center;font-weight:800;font-size:12pt;color:#ff5a1f}
table.script td:nth-child(2){width:7.5%;white-space:nowrap;font-size:9.5pt;color:#444}table.script td:nth-child(2) b{font-size:11pt;color:#111}
table.script td:nth-child(3){width:12%;font-weight:700}table.script td:nth-child(4){width:16%;color:#555;font-size:9.5pt}
table.script td:nth-child(5){width:61%;font-size:11pt;line-height:1.6}table.script td:nth-child(5) b{color:#c43e0c}
tr.vid td{background:#f4f2ef;color:#888}table.meta{width:auto}table.meta td{padding:3px 8px;font-size:9.5pt}
code{font-family:inherit;background:#f1efec;padding:0 3px;border-radius:3px}'''
d = tempfile.mkdtemp(); hp = os.path.join(d, 'script.html')
open(hp, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
js = f'''const {{chromium}}=require('playwright-core');(async()=>{{const b=await chromium.launch({{executablePath:process.env.CHROME||'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'}});
const p=await b.newPage();await p.goto('file://{hp}');await p.waitForTimeout(500);
await p.pdf({{path:{outpdf!r},format:'A4',landscape:true,printBackground:true,displayHeaderFooter:true,headerTemplate:'<div></div>',
footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#999"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
margin:{{top:'12mm',bottom:'14mm',left:'12mm',right:'12mm'}}}});await b.close();}})();'''
jp = os.path.join(d, 'pdf.js'); open(jp, 'w').write(js)
subprocess.run(['node', jp], check=True); print('PDF:', outpdf)
