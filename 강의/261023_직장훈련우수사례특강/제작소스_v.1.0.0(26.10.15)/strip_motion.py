# v.2.0.0 완성본 → 모션 없는 분해판: 모션 영상 · 큰 영상 · 장 전환 · 재생 타이밍 빼고, 큰 영상은 첫 화면 그림만 남김
import re, os, sys, glob, html
D = sys.argv[1]; N152 = sys.argv[2]   # 풀어 둔 v.2.0.0 폴더, v.1.5.2 pptx(글자 사이 간격 고친 글상자를 가져옴)
import zipfile
z152 = zipfile.ZipFile(N152)
rep = {'motion': 0, 'video': 0, 'gapfix': 0}
nontext = lambda s: ''.join(c for c in s if not c.isspace())
def sps(x): return re.findall(r'<p:sp>.*?</p:sp>', x, re.S)
def txt(sp): return html.unescape(''.join(re.findall(r'<a:t>([^<]*)</a:t>', sp)))
for f in sorted(glob.glob(D + '/ppt/slides/slide*.xml')):
    n = int(re.search(r'slide(\d+)\.xml', f).group(1)); x = open(f, encoding='utf-8').read()
    rf = D + f'/ppt/slides/_rels/slide{n}.xml.rels'; r = open(rf, encoding='utf-8').read()
    # 1) 모션 영상 그림 통째로 지움
    x, k = re.subn(r'<p:pic><p:nvPicPr><p:cNvPr id="\d+" name="모션 영상 \d+"/>.*?</p:pic>', '', x, flags=re.S); rep['motion'] += k
    # 2) 큰 영상: 영상 연결만 떼고 첫 화면 그림으로
    if '<a:videoFile' in x:
        x = re.sub(r'<a:videoFile r:link="[^"]*"/>', '', x)
        x = re.sub(r'<p:extLst><p:ext uri="\{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230\}">.*?</p:ext></p:extLst>', '', x, flags=re.S); rep['video'] += 1
    # 3) 재생 타이밍 · 장 전환 지움
    x = re.sub(r'<p:timing>.*?</p:timing>', '', x, flags=re.S)
    x = re.sub(r'<p:transition[^>]*/>|<p:transition[^>]*>.*?</p:transition>', '', x, flags=re.S)
    x = re.sub(r'<mc:AlternateContent[^>]*>\s*<mc:Choice[^>]*>\s*</mc:Choice>\s*<mc:Fallback>\s*</mc:Fallback>\s*</mc:AlternateContent>', '', x, flags=re.S)
    # 4) 글자 사이 간격(v.1.5.2): 같은 위치 · 같은 글자의 글상자 내용을 v.1.5.2 것으로
    try: y = z152.read(f'ppt/slides/slide{n}.xml').decode('utf-8')
    except KeyError: y = ''
    new = {}
    for sp in sps(y):
        o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', sp)
        if o and '<a:t>' in sp: new[(o.groups(), nontext(txt(sp)))] = sp
    def swap(m):
        sp = m.group(0); o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', sp)
        if not o or '<a:t>' not in sp: return sp
        b = new.get((o.groups(), nontext(txt(sp))))
        if not b: return sp
        tb = re.search(r'<p:txBody>.*?</p:txBody>', b, re.S).group(0); ta = re.search(r'<p:txBody>.*?</p:txBody>', sp, re.S).group(0)
        if tb != ta and txt(b) != txt(sp): rep['gapfix'] += 1; return sp.replace(ta, tb)
        return sp
    x = re.sub(r'<p:sp>.*?</p:sp>', swap, x, flags=re.S)
    open(f, 'w', encoding='utf-8').write(x)
    # 안 쓰는 관계(영상 · 모션 첫 화면) 지움
    ids = set(re.findall(r'r:(?:embed|link|id)="([^"]+)"', x))
    def keep(m):
        rid, tgt, typ = m.group(1), m.group(3), m.group(2)
        if rid in ids or typ.endswith(('slideLayout', 'notesSlide')): return m.group(0)
        return ''
    r = re.sub(r'<Relationship Id="([^"]+)" Type="([^"]+)" Target="([^"]+)"[^>]*/>', keep, r)
    open(rf, 'w', encoding='utf-8').write(r)
# 아무도 안 쓰는 미디어 파일 지움
used = set()
for rf in glob.glob(D + '/ppt/**/_rels/*.rels', recursive=True):
    for t in re.findall(r'Target="\.\./media/([^"]+)"', open(rf, encoding='utf-8').read()): used.add(t)
gone = [m for m in os.listdir(D + '/ppt/media') if m not in used]
for m in gone: os.remove(D + '/ppt/media/' + m)
print(rep, 'removed media', len(gone), 'left mp4', [m for m in os.listdir(D + '/ppt/media') if m.endswith('.mp4')])
