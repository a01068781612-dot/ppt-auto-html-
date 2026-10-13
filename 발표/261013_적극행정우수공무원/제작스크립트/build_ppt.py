import json,sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu,Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
D=sys.argv[1];OUT=sys.argv[2]
boxes=json.load(open(D+'/ppt/boxes.json'))
prs=Presentation();prs.slide_width=Emu(12192000);prs.slide_height=Emu(6858000)
px=lambda v:Emu(int(v*12192000/1920))
notes={
'v1':'[영상1 · 45초] 현 문제 실태\n삽입 → 비디오 → 이 디바이스 → 영상1 파일을 넣고 화면 전체 크기로 맞춘 뒤, 재생 → 시작: 자동 실행 / 전체 화면 재생.',
'v2':'[영상2 · 1분 20초] 실제 작동 + 감동 엔딩\n① 내비 실제 구동 → ② 농골길 실제 구동 → ③ 원패스 설계 시연 → 엔딩 "그 1분이, 누군가에게는 평생입니다"\n삽입 → 비디오 → 화면 전체 크기, 자동 실행.',
's3':'빨간 점선 칸 4개 = 필요 자료 자리. 사진을 넣을 때: 칸을 클릭 → 삭제 → 같은 자리에 삽입 → 그림 (또는 칸 위에 사진을 올리고 크기 맞춤).',
}
for i,id in enumerate(['s1','v1','s2','s3','v2','s4','s5','s6']):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    jp=f'{D}/ppt/{id}.jpg';Image.open(f'{D}/ppt/{id}.png').convert('RGB').save(jp,quality=90)
    s.shapes.add_picture(jp,0,0,prs.slide_width,prs.slide_height).name='배경(고정)'
    for n,b in enumerate(boxes[id]):
        r=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,px(b['x']),px(b['y']),px(b['w']),px(b['h']))
        r.name=f'필요자료{n+1}';r.adjustments[0]=0.08
        r.fill.solid();r.fill.fore_color.rgb=RGBColor(0xEA,0xF2,0xFF)
        r.line.color.rgb=RGBColor(0x2F,0x80,0xED);r.line.width=Pt(2);r.line.dash_style=MSO_LINE_DASH_STYLE.DASH
        tf=r.text_frame;tf.word_wrap=True;tf.vertical_anchor=MSO_ANCHOR.MIDDLE
        for k,(t,sz,c,bold) in enumerate([('필요 자료',9,'2F80ED',True),(b['t'],12,'111827',True),(b['s'],9,'6B7280',False)]):
            para=tf.paragraphs[0] if k==0 else tf.add_paragraph();para.alignment=PP_ALIGN.CENTER
            run=para.add_run();run.text=t;f=run.font;f.size=Pt(sz);f.bold=bold;f.color.rgb=RGBColor.from_string(c);f.name='맑은 고딕'
    if id in notes: s.notes_slide.notes_text_frame.text=notes[id]
prs.save(OUT);print('ok')
