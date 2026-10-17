# v.2.2.0 → v.2.3.0: 재해가 끝나도 · 8개 기관 · 영상 삽입(녹음본) · 노트 시간 재계산(영상2 1:26)
import sys, subprocess
from pptx import Presentation
from pptx.util import Emu

SRC, OUT, V1, V2, TMP = sys.argv[1:6]
p = Presentation(SRC)
S = lambda n: p.slides[n - 1]
def sh(slide, sid):
    for s in slide.shapes:
        if s.shape_id == sid: return s
    raise KeyError(sid)
def set_text(s, text):
    rs = s.text_frame.paragraphs[0].runs
    rs[0].text = text
    for r in rs[1:]: r.text = ''

set_text(sh(S(4), 89), '한 층 더 · 재난 8개 기관 연결')
t = sh(S(4), 89); t.width = Emu(t.width + 9525 * 2)
set_text(sh(S(6), 46), '한 번 신청으로 8개 기관')

# 영상 삽입: 화면 전체, 슬라이드가 열리면 자동 재생
W, H = p.slide_width, p.slide_height
for n, v in ((2, V1), (5, V2)):
    poster = f'{TMP}/poster{n}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '0.5', '-i', v, '-frames:v', '1', poster], check=True)
    mv = S(n).shapes.add_movie(v, 0, 0, W, H, poster_frame_image=poster, mime_type='video/mp4')
    from lxml import etree
    sl = S(n).element
    tm = sl.find('{http://schemas.openxmlformats.org/presentationml/2006/main}timing')
    if tm is not None: sl.remove(tm)
    sid = mv.shape_id; dur = 45000 if n == 2 else 86200
    xml = f'''<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst><p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="6" dur="{dur}" fill="hold"/><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq><p:video><p:cMediaNode vol="80000"><p:cTn id="7" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cMediaNode></p:video></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'''
    el = etree.fromstring(xml)
    ext = sl.find('{http://schemas.openxmlformats.org/presentationml/2006/main}extLst')
    if ext is not None: ext.addprevious(el)
    else: sl.append(el)

NOTES = {
1: "[0:00–0:14]\n안녕하십니까, 경상남도 소방본부 119종합상황실 박중휘입니다. (0:08)\n재난 골든타임, 세 번 앞당기다. (0:12)\n먼저 영상입니다. (0:14)",
2: "[0:14–0:59] 영상1 · 45초 (녹음 내레이션 포함) — 멘트 없음. 슬라이드가 열리면 자동 재생.",
3: "[0:59–1:27]\n골든타임은 세 번 늦어집니다. (1:03)\n첫째, 출동. 막힌 길에서 신호를 어긴 긴급차량이 2.3배 늘었습니다. (1:11)\n둘째, 현장대응. 농촌 마을 164곳은 불을 끄는 중형 소방차가 못 들어갑니다. (1:20)\n셋째, 복구. 재해가 끝나도 6기관 8회, 90일을 기다립니다. (1:27)",
4: "[1:27–2:05]\n그래서 새로 만들지 않고, 기존 시스템에 한 층 더 얹었습니다. (1:34)\n첫째, 상황실 출동 정보를 카카오내비에 연결해, 긴급차량 접근 알림을 띄웁니다. (1:44)\n둘째, 대원들이 만든 마을 길 책자에 AI를 얹어, 5초 만에 답합니다. (1:52)\n셋째, 정부24 원스톱 서비스에 '재난'을 더해, 한 번 신청으로 8개 기관을 잇습니다. (2:02)\n실제 작동 화면입니다. (2:05)",
5: "[2:05–3:31] 영상2 · 1분 26초 (녹음 내레이션 포함) — 멘트 없음. 슬라이드가 열리면 자동 재생.",
6: "[3:31–4:03]\n세 번의 골든타임, 이렇게 앞당깁니다. (3:36)\n첫째, 출동. 우선신호로 56% 줄어든 통행시간이, 내비 알림을 더하면 약 60%까지 줄어들 것으로 기대합니다. (3:50)\n둘째, 현장대응. 출동에서 방수까지 3분 단축입니다. (3:57)\n셋째, 복구. 14일이 7분이 되도록 설계했습니다. (4:03)\n\n[질의응답 근거] 1km 200초 → 우선신호 87초(56%). 길이 비었을 때 60초, 남은 27초의 절반(13.5초)을 앞차 미양보 지연으로 보고, 알림 받는 운전자 50%가 비키면 6.75초 단축 → 80초(약 60%). 5km 출동 시 약 34초. 30%면 58.5%, 80%(현대·기아·티맵 확대)면 62%.",
7: "[4:03–4:24]\n경남에서 먼저 증명했습니다. (4:06)\n내비 알림 497대, 농골길 18개 서 공유. (4:12)\n재난 원패스는 행정안전부장관상 대상을 받아, 정부24 개발에 착수했습니다. (4:21)\n이제 전국으로 갑니다. (4:24)",
8: "[4:24–4:37]\n길을 비켜 준 시민, 마을과 마주한 대원, 손 내민 정부. (4:30)\n골든타임은, 함께 지킬 때 앞당겨집니다. (4:35)\n감사합니다. (4:37)",
}
for n, txt in NOTES.items():
    S(n).notes_slide.notes_text_frame.text = txt
p.save(OUT); print('saved')
