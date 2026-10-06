import json,os,shutil
from PIL import Image
CAP='/tmp/yt/cap/'; BASE='/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/hf/p1cover/'
CSS=open('../news/style.css').read()+open('extra.css').read()
TILES='<div class="tiles">'+'<i></i>'*8+'</div>'
for t in json.load(open('arts.json')):
    d=t['id']; os.makedirs(d,exist_ok=True)
    for f in ['gsap.min.js','PretendardVariable.woff2','hyperframes.json','meta.json','package.json']:
        if os.path.exists(BASE+f): shutil.copy(BASE+f,d)
    if t.get('photo'):
        pim=Image.open(t['photo']).convert('RGB'); r=pim.size[0]/pim.size[1]; pw,phh=880,880/r
        if phh>540: phh=540; pw=540*r
        pim.save(f'{d}/photo.jpg',quality=95)
        import math
        cw=max(pw,700); lines=math.ceil(len(t['photo_cap'])*23*0.93/cw); bh=phh+18+lines*34.5
        ftop=170+(690-bh)/2
        fig=f'<div class="fig w2 clip" style="top:{ftop:.0f}px;left:{110+(880-max(pw,700))/2:.0f}px;width:{pw:.0f}px" data-start="0" data-duration="7" data-track-index="1"><div class="fimg" style="width:{pw:.0f}px;height:{phh:.0f}px"><img class="pimg" src="photo.jpg"/>{TILES if t["id"]=="p4" else ""}</div><div class="fcap" style="width:{max(pw,700):.0f}px">▲ {t["photo_cap"]}</div><div class="badge">기사 사진</div></div>'
    im=Image.open(CAP+t['cap']+'.png').convert('RGB'); bx=t['box']; y0=max(0,min(bx[1]-200,1280-860))
    im.crop((0,y0,1280,y0+860)).save(f'{d}/cap.jpg',quality=90)
    s=880/1280; hx=bx[0]*s; hy=(bx[1]-y0)*s; hw=(bx[2]-bx[0])*s; hh=(bx[3]-bx[1])*s
    WIN=f'''<div class="win w2 clip" data-start="0" data-duration="7" data-track-index="1"><div class="bar"><i></i><i></i><i></i><div class="url">🔒 {t['url']}</div></div>
<div class="view"><img class="shot" src="cap.jpg"/><div class="hl" style="left:{hx:.0f}px;top:{hy:.0f}px;width:{hw:.0f}px;height:{hh:.0f}px"></div></div><div class="badge">실제 기사</div></div>'''
    big=f'<div class="big"><b>{t["big"][0]}</b><span>{t["big"][1]}</span><em>{t["big"][2]}</em></div>' if t.get('big') else ''
    pts=''.join(f'<div class="ln"><i></i>{x}</div>' for x in t['points'])
    quote=f'<div class="qt"><b>“</b>{t["quote"]}</div>' if t.get('quote') else ''
    WIN_JS='.from(".shot, .hl",{y:30,duration:6,ease:"none"},0.2).from(".hl",{scaleX:0,transformOrigin:"left",duration:.6},1.3)'
    PH_JS='.fromTo(".pimg",{scale:1.1},{scale:1,duration:6.5,ease:"none"},0.1).from(".fcap",{opacity:0,y:16,duration:.6},1.3)'
    EXTRA={
     # 01 정부 제도: 창이 왼쪽에서 + '2만'이 튀어오름
     'p1': WIN_JS+'.from(".big b",{scale:.2,opacity:0,transformOrigin:"left bottom",duration:.6,ease:"back.out(3)"},1.6)',
     # 02 지자체 인사: 창이 3D로 떨어지고 '0.5'가 0.0부터 올라감
     'p2': '.from(".shot, .hl",{y:30,duration:6,ease:"none"},0.2).from(".hl",{scaleX:0,transformOrigin:"left",duration:.6},1.3)'
           '.fromTo(".big b",{innerText:0},{innerText:0.5,snap:{innerText:0.1},duration:1.0,ease:"power2.out"},1.6)',
     # 03 기관장: 사진이 가운데서 열리듯 드러남
     'p3': '.from(".fimg",{clipPath:"inset(50% 50% 50% 50% round 14px)",duration:1.2,ease:"power4.inOut"},0.2).fromTo(".pimg",{scale:1.15},{scale:1,duration:6,ease:"none"},0.2).from(".fcap",{opacity:0,y:16,duration:.6},1.4)',
     # 04 현장: 8명 사진이 칸칸이 무작위로 켜짐
     'p4': '.to(".tiles i",{opacity:0,scale:.5,duration:.45,stagger:{each:.09,from:"random"},ease:"power2.in"},0.4).from(".fcap",{opacity:0,y:16,duration:.6},1.6)',
     # 05 한 사람: 사진이 옆으로 밀려 들어오며 안쪽은 반대로 움직임(시차)
     'p5': '.from(".fimg",{x:-260,opacity:0,duration:1.0,ease:"power3.out"},0.2).fromTo(".pimg",{x:70,scale:1.08},{x:0,scale:1,duration:2.4,ease:"power2.out"},0.2).from(".fcap",{opacity:0,y:16,duration:.6},1.4)',
    }
    js_win='.from(".w2",{opacity:0,x:-160,duration:.9,ease:"power3.out"},0.1)' if t['id'] in ('p1',) else ''
    if t['id']=='p2': js_win='.from(".w2",{opacity:0,rotationX:-70,y:-120,transformPerspective:1800,transformOrigin:"center top",duration:1.0,ease:"power3.out"},0.1)'
    html=f'''<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/><script src="gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="7" data-width="1920" data-height="1080">
<div class="lbl2 clip" data-start="0" data-duration="7" data-track-index="0">{t['tag']}</div>
{fig if t.get('photo') else WIN}
<div class="sq sq2 clip" data-start="0" data-duration="7" data-track-index="2"></div>
<div class="rc clip" data-start="0" data-duration="7" data-track-index="3"><div class="t2">{t['title']}</div>{big}<div class="pts">{pts}</div>{quote}</div>
<div class="src2 clip" data-start="0" data-duration="7" data-track-index="4"><b>출처</b>{t['src']}</div>
</div>
<script>
const tl=gsap.timeline({{paused:true}});
tl.from(".lbl2",{{opacity:0,x:-30,duration:.5}},0){js_win}
.from(".sq2",{{opacity:0,scale:.4,rotation:-45,duration:.6,ease:"back.out(1.8)"}},0.6)
{EXTRA.get(t['id'], PH_JS if t.get('photo') else WIN_JS)}.from(".badge",{{scale:0,duration:.45,ease:"back.out(2)"}},1.5)
.from(".t2",{{opacity:0,y:40,duration:.7,ease:"power3.out"}},0.5).from(".big",{{opacity:0,y:30,duration:.6}},1.6)
.from(".ln",{{opacity:0,x:24,duration:.5,stagger:.3}},2.0).from(".qt",{{opacity:0,y:20,duration:.6}},3.0).from(".src2",{{opacity:0,duration:.6}},1.2);
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>'''
    open(f'{d}/index.html','w').write(html)
print('ok')
