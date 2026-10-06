import json,os,shutil,sys
from PIL import Image
CAP='/tmp/yt/cap2/'
BASE='/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/hf/p1cover/'
T=json.load(open('topics.json'))
COMMON = ('tl.from(".lbl",{opacity:0,x:-30,duration:.5},0)'
  '.from(".sq",{opacity:0,scale:.4,rotation:-45,duration:.6,ease:"back.out(1.8)"},0.6)'
  '.from(".gh",{opacity:0,duration:1},0.5).from(".src",{opacity:0,y:20,duration:.5},0.9)'
  '.from(".badge",{scale:0,duration:.45,ease:"back.out(2)"},1.8)'
  '.from(".ln",{opacity:0,x:-24,duration:.5,stagger:.25},1.7).from(".next",{opacity:0,y:20,duration:.6},2.6)'
  '.from(".url",{clipPath:"inset(0 100% 0 0)",duration:.9,ease:"none"},0.5)'
  '.fromTo(".next .pl",{scale:1},{scale:1.12,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"},3.3);')
VARIANTS = {
 # 창이 오른쪽에서 밀려 들어오고 제목 쪽으로 확대
 'slide': ('tl.from(".win",{opacity:0,x:160,duration:.9,ease:"power3.out"},0.1).from(".ttl",{opacity:0,y:50,duration:.8,ease:"power3.out"},0.35)'
           '.from(".shot, .hl",{y:30,duration:5,ease:"none"},0.2).from(".hl",{scaleX:0,transformOrigin:"left",duration:.6,ease:"power2.out"},1.5)'
           '.to(".zoom",{scale:1.12,duration:2.2,ease:"power2.inOut"},2.4);'),
 # 창이 가운데서 양옆으로 열림 + 제목이 왼쪽부터 드러남
 'split': ('tl.from(".win",{clipPath:"inset(0 50% 0 50% round 18px)",duration:1.0,ease:"power4.inOut"},0.1).from(".ttl",{clipPath:"inset(0 100% 0 0)",duration:.9,ease:"power3.inOut"},0.3)'
           '.from(".hl",{scaleY:0,transformOrigin:"center",duration:.5,ease:"back.out(2)"},1.4).to(".zoom",{scale:1.1,duration:2.4,ease:"power2.inOut"},2.4);'),
 # 기사를 아래에서 위로 스크롤해 올라오다 제목에서 멈춤
 'scroll': ('tl.from(".win",{opacity:0,y:40,duration:.6},0.1).fromTo(".shot, .hl",{y:-420},{y:0,duration:2.0,ease:"power3.out"},0.2)'
            '.from(".ttl",{opacity:0,x:-60,duration:.8,ease:"power3.out"},0.35).from(".hl",{scaleX:0,transformOrigin:"left",duration:.6,ease:"power2.out"},1.6)'
            '.to(".zoom",{scale:1.12,duration:2.0,ease:"power2.inOut"},2.6);'),
 # 창이 위에서 3D로 떨어지며 펴짐
 'drop3d': ('tl.from(".win",{opacity:0,rotationX:-70,y:-140,transformPerspective:1800,transformOrigin:"center top",duration:1.1,ease:"power3.out"},0.1)'
            '.from(".ttl",{opacity:0,rotationX:-60,transformPerspective:1200,transformOrigin:"left top",duration:.9,ease:"power3.out"},0.35)'
            '.from(".hl",{scaleX:0,transformOrigin:"left",duration:.6,ease:"power2.out"},1.5).to(".zoom",{scale:1.12,duration:2.2,ease:"power2.inOut"},2.4);'),
 # 제목 박스가 '쾅' 찍히며 창이 흔들림 (흔들었다·50배 같은 임팩트)
 'stamp': ('tl.from(".win",{opacity:0,scale:.92,duration:.6,ease:"power2.out"},0.1).from(".ttl",{opacity:0,scale:1.5,transformOrigin:"left center",duration:.5,ease:"power4.in"},0.4)'
           '.to(".ttl",{x:"+=8",duration:.05,repeat:5,yoyo:true},0.9).from(".hl",{opacity:0,scale:1.9,duration:.35,ease:"power4.in"},1.4)'
           '.to(".win",{x:"+=12",duration:.05,repeat:7,yoyo:true},1.75).to(".zoom",{scale:1.12,duration:2.0,ease:"power2.inOut"},2.6);'),
 # 제목에 크게 붙어 있다가 멀어지며 기사 전체가 보임 (2조 원 같은 큰 숫자)
 'zoomout': ('tl.from(".win",{opacity:0,duration:.4},0.1).fromTo(".zoom",{scale:2.3},{scale:1,duration:2.0,ease:"power3.inOut"},0.2)'
             '.from(".ttl",{opacity:0,filter:"blur(12px)",scale:1.25,transformOrigin:"left center",duration:1.0,ease:"power2.out"},0.35)'
             '.from(".hl",{opacity:0,duration:.4},0.25);'),
}
ASSIGN = {'n01':'slide','n02a':'split','n03':'scroll','n04':'drop3d','n09':'zoomout','n06':'split','n05':'stamp','n07':'slide','n08':'scroll','n10':'drop3d'}

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
    JS=(VARIANTS[ASSIGN[t['id']]]+COMMON)
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
{JS}
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>'''
    open(f'{d}/index.html','w').write(html)
print('ok',len(T))
