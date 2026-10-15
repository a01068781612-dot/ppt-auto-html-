import re,sys
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
D=Document()
sec=D.sections[0];sec.orientation=WD_ORIENT.LANDSCAPE;sec.page_width,sec.page_height=Cm(29.7),Cm(21)
for m in ('left_margin','right_margin','top_margin','bottom_margin'):setattr(sec,m,Cm(1.5))
st=D.styles['Normal'];st.font.name='Pretendard';st.element.rPr.rFonts.set(qn('w:eastAsia'),'Pretendard');st.font.size=Pt(11)
def shade(c,col):
    tcPr=c._tc.get_or_add_tcPr();s=OxmlElement('w:shd');s.set(qn('w:val'),'clear');s.set(qn('w:fill'),col);tcPr.append(s)
def runs(par,text,size=12.5,color=None):
    for i,seg in enumerate(re.split(r'\*\*',text)):
        if not seg:continue
        r=par.add_run(seg);r.font.size=Pt(size);r.bold=(i%2==1)
        if i%2==1:r.font.color.rgb=RGBColor(0x2F,0x80,0xED)
        elif color:r.font.color.rgb=color
h=D.add_paragraph();runs(h,'**적극행정 우수사례 발표 대본** — 재난 골든타임, 세 번 앞당기다',16)
D.add_paragraph('발표자 박중휘 · 총 4분 30초(영상 2개 2분 5초 포함) · 남성 기준 천천히(초당 약 4음절) · 파란 굵은 글씨 = 슬라이드에 없는 말 · 괄호 = 그 문장이 끝나는 목표 시각')
D.add_paragraph().add_run('변경 이력').bold=True
t=D.add_table(rows=2,cols=3);t.style='Table Grid'
for c,x in zip(t.rows[0].cells,['버전','날짜','수정 내용']):c.text=x;shade(c,'E8EEF7')
for c,x in zip(t.rows[1].cells,['v.1.0.0','26.10.15','최초 작성: 4:30 확정 대본, PPT v.2.2.0 기준']):c.text=x
S=[
(1,'1장 · 표지','0:00–0:14',['**안녕하십니까,** 경상남도 소방본부 119종합상황실 박중휘**입니다.** (0:08)','재난 골든타임, 세 번 앞당기다. (0:12)','**먼저 영상입니다.** (0:14)']),
(2,'2장 · 영상1','0:14–0:59',['[영상 재생 45초 · 멘트 없음] (0:59)']),
(3,'3장 · 추진 배경','0:59–1:27',['골든타임은 세 번 늦어집니다. (1:03)','첫째, 출동. 막힌 길에서 **신호를 어긴 긴급차량이** 2.3배 **늘었습니다.** (1:11)','둘째, 현장대응. **농촌 마을** 164곳은 **불을 끄는** 중형 소방차가 못 들어갑니다. (1:20)','셋째, 복구. **불이 꺼져도** 6기관 8회, 90일을 기다립니다. (1:27)']),
(4,'4장 · 추진 내용','1:27–2:05',['**그래서** 새로 만들지 않고, 기존 시스템에 한 층 더 **얹었습니다.** (1:34)','첫째, 상황실 **출동 정보를 카카오내비에 연결해,** 긴급차량 접근 알림을 **띄웁니다.** (1:44)','둘째, 대원**들이 만든** 마을 **길** 책자에 AI를 **얹어,** 5초 **만에 답합니다.** (1:52)',"셋째, 정부24 원스톱 서비스에 '재난'을 **더해,** 한 번 신청으로 6개 기관을 **잇습니다.** (2:02)",'**실제 작동 화면입니다.** (2:05)']),
(5,'5장 · 영상2','2:05–3:24',['[영상 재생 1분 20초 · 멘트 없음] (3:24)']),
(6,'6장 · 기대효과','3:24–3:56',['세 번의 골든타임, 이렇게 앞당깁니다. (3:29)','첫째, 출동. 우선신호로 56% **줄어든** 통행시간이, 내비 알림을 **더하면 약** 60%**까지 줄어들 것으로** 기대**합니다.** (3:43)','둘째, 현장대응. 출동에서 방수까지 3분 단축**입니다.** (3:50)','셋째, 복구. 14일이 7분이 **되도록** 설계**했습니다.** (3:56)']),
(7,'7장 · 확산','3:56–4:17',['경남에서 **먼저** 증명**했습니다.** (3:59)','내비 알림 497대, 농골길 18개 서 공유. (4:05)','재난 원패스는 행정안전부장관상 대상을 **받아,** 정부24 개발 착수**했습니다.** (4:14)','**이제** 전국으로 **갑니다.** (4:17)']),
(8,'8장 · 마무리','4:17–4:30',['길을 비켜 준 시민, 마을과 마주한 대원, 손 내민 정부. (4:23)','골든타임은, 함께 지킬 때 앞당겨집니다. (4:28)','**감사합니다.** (4:30)']),
]
D.add_paragraph()
T=D.add_table(rows=1,cols=2);T.style='Table Grid';T.autofit=False
for c,x in zip(T.rows[0].cells,['발표 슬라이드','발표 스크립트']):
    c.text='';r=c.paragraphs[0].add_run(x);r.bold=True;shade(c,'E8EEF7')
W=[Cm(12.2),Cm(14.3)]
for n,title,tm,lines in S:
    row=T.add_row().cells
    row[0].paragraphs[0].add_run().add_picture(f'hi-{n}.png',width=Cm(11.8))
    cap=row[0].add_paragraph();runs(cap,f'**{title}**  {tm}',10.5)
    row[1].paragraphs[0].text=''
    first=True
    for ln in lines:
        par=row[1].paragraphs[0] if first else row[1].add_paragraph();first=False
        par.paragraph_format.space_after=Pt(8)
        runs(par,ln)
for row in T.rows:
    for c,w in zip(row.cells,W):c.width=w
D.save(sys.argv[1]);print('ok')
