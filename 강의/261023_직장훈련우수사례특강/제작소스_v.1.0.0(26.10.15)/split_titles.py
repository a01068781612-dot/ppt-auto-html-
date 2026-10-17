# 분해판 4단계 — 슬라이드마다 이름(cSld name)을 "번호. 제목"으로 넣고, '슬라이드 제목' 글상자를 PowerPoint 제목 자리(title)로 지정한다.
# → 개요 보기 · 슬라이드 목록 · 하이퍼링크 대상 · 화면 읽기 프로그램에서 제목이 보임. 글자 모양은 그대로(글상자에 직접 지정된 서식 유지).
# 사용: python3 split_titles.py <IN.pptx> <IN_titles.json> <OUT.pptx>
import sys, zipfile, re, json, html
src, tj, dst = sys.argv[1:4]
T = {int(k): v for k, v in json.load(open(tj, encoding='utf-8')).items()}
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED); done = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    m = re.match(r'ppt/slides/slide(\d+)\.xml$', it.filename)
    if m:
        n = int(m.group(1)); x = d.decode('utf-8'); t = T.get(n, f'{n}장')
        nm = html.escape(f'{n}. {t}'[:120], quote=True)
        x = re.sub(r'<p:cSld(?: name="[^"]*")?>', f'<p:cSld name="{nm}">', x, count=1)
        x, k = re.subn(r'(<p:cNvPr id="\d+" name="슬라이드 제목(?:\(화면 밖\))?"[^>]*?/?>(?:.*?</p:cNvPr>)?<p:cNvSpPr[^>]*?(?:/>|>.*?</p:cNvSpPr>))<p:nvPr(?:/>|></p:nvPr>)', r'\1<p:nvPr><p:ph type="title"/></p:nvPr>', x, count=1, flags=re.S)
        x = re.sub(r'(</a:ln>)<a:solidFill><a:srgbClr val="FFFFFF"><a:alpha val="0"/></a:srgbClr></a:solidFill>', r'\1<a:noFill/>', x)   # 외곽선 글자: 글자 안 비움
        done += k; d = x.encode('utf-8')
    if it.filename.startswith('ppt/theme/theme') and it.filename.endswith('.xml'):   # 기본 글꼴(새로 넣는 글상자)도 Pretendard로
        x = d.decode('utf-8')
        x = x.replace('<a:latin typeface="Calibri Light"', '<a:latin typeface="Pretendard ExtraBold"').replace('<a:latin typeface="Calibri"', '<a:latin typeface="Pretendard"')
        x = x.replace('<a:ea typeface=""', '<a:ea typeface="Pretendard"').replace('script="Hang" typeface="맑은 고딕"', 'script="Hang" typeface="Pretendard"')
        d = x.encode('utf-8')
    zout.writestr(it, d, compress_type=zipfile.ZIP_STORED if it.filename.endswith(('.mp4', '.jpg', '.jpeg', '.png')) else zipfile.ZIP_DEFLATED)
zout.close(); print('ok titles', done)
