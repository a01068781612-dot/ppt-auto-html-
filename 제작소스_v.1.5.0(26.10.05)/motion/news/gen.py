import json,os,shutil,sys
from PIL import Image
CAP='/tmp/yt/cap2/'
BASE='/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/hf/p1cover/'
T=json.load(open('topics.json'))
CSS=open('style.css').read()
for t in T:
    d=t['id']; os.makedirs(d,exist_ok=True)
    for f in ['gsap.min.js','PretendardVariable.woff2','hyperframes.json','meta.json','package.json']:
        if os.path.exists(BASE+f): shutil.copy(BASE+f,d)
    im=Image.open(CAP+t['cap']+'.png').convert('RGB')
    bx=t['box']; y0=max(0,min(bx[1]-200,im.size[1]-940))
    im.crop((0,y0,1280,y0+940)).save(f'{d}/cap.jpg',quality=90)
    s=880/1280; hx=bx[0]*s; hy=(bx[1]-y0)*s; hw=(bx[2]-bx[0])*s; hh=(bx[3]-bx[1])*s
    lines=''.join(f'<div class="ln l{i}"><i></i>{x}</div>' for i,x in enumerate(t['lines']))
    html=f'''<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/><script src="gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="6" data-width="1920" data-height="1080">
<div class="ghost gh clip" data-start="0" data-duration="6" data-track-index="0">News.</div>
<div class="lbl clip" data-start="0" data-duration="6" data-track-index="1">{t['tag']}</div>
<div class="ttl clip" data-start="0" data-duration="6" data-track-index="2">{t['title']}</div>
<div class="src clip" data-start="0" data-duration="6" data-track-index="3"><b>출처</b>{t['src']}</div>
<div class="lines clip" data-start="0" data-duration="6" data-track-index="4">{lines}</div>
<div class="next clip" data-start="0" data-duration="6" data-track-index="5"><span class="pl"></span><div><b>영상으로 살펴보겠습니다</b><em>{t['video']}</em></div></div>
<div class="win clip" data-start="0" data-duration="6" data-track-index="6">
  <div class="bar"><i></i><i></i><i></i><div class="url">🔒 {t['url']}</div></div>
  <div class="view"><div class="zoom" style="transform-origin:{hx+hw/2:.0f}px {hy+hh/2:.0f}px"><img class="shot" src="cap.jpg"/><div class="hl" style="left:{hx:.0f}px;top:{hy:.0f}px;width:{hw:.0f}px;height:{hh:.0f}px"></div></div></div>
  <div class="badge">실제 기사</div>
</div>
<div class="sq clip" data-start="0" data-duration="6" data-track-index="7"></div>
</div>
<script>
const tl=gsap.timeline({{paused:true}});
tl.from(".lbl",{{opacity:0,x:-30,duration:.5}},0)
.from(".win",{{opacity:0,x:160,duration:.9,ease:"power3.out"}},0.1)
.from(".sq",{{opacity:0,scale:.4,rotation:-45,duration:.6,ease:"back.out(1.8)"}},0.6)
.from(".ttl",{{opacity:0,y:50,duration:.8,ease:"power3.out"}},0.35)
.from(".gh",{{opacity:0,duration:1}},0.5)
.from(".src",{{opacity:0,y:20,duration:.5}},0.9)
.from(".shot, .hl",{{y:30,duration:5,ease:"none"}},0.2)
.from(".hl",{{scaleX:0,transformOrigin:"left",duration:.6,ease:"power2.out"}},1.5)
.from(".badge",{{scale:0,duration:.45,ease:"back.out(2)"}},1.8)
.from(".ln",{{opacity:0,x:-24,duration:.5,stagger:.25}},1.7)
.from(".next",{{opacity:0,y:20,duration:.6}},2.6)
.from(".url",{{clipPath:"inset(0 100% 0 0)",duration:.9,ease:"none"}},0.5)
.to(".zoom",{{scale:1.12,duration:2.2,ease:"power2.inOut"}},2.4)
.fromTo(".next .pl",{{scale:1}},{{scale:1.12,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},3.3);
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>'''
    open(f'{d}/index.html','w').write(html)
print('ok',len(T))
