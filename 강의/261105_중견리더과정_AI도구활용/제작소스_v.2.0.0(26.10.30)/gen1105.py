# 중견리더과정 「공무원을 위한 AI도구 활용법 소개」(26.11.05) — HyperFrames 모션 장면 생성기 v.1.0.0
# 디자인·모션은 10.08 AI특강 / 10.20 워크숍(gen1020.py)과 같고, 내용만 이 강의에 맞춘다.
# 사용: python3 gen1105.py <출력폴더> <lib폴더(gsap.min.js·PretendardVariable.woff2)>
#  → <출력폴더>/<장면id>/index.html (+ bg.png·설정 json·QR 이미지) 를 만든 뒤 hyperframes render
import os, sys, shutil, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out')
LIB = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'lib')
QR = os.path.join(OUT, '_qr')

# 투표 화면 QR이 들어갈 자리 (PPT에서 같은 좌표에 QR 그림을 얹는다 → build1105.js의 QRBOX와 같아야 함)
QRBOX = dict(x=1330, y=330, s=420)

CSS = '''@font-face{font-family:"Pretendard";src:url("PretendardVariable.woff2") format("woff2");font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden;background:#0c0b0b}
#root{width:100%;height:100%;position:relative;font-family:"Pretendard",sans-serif;color:#f4f4f2;background:#0c0b0b url(bg.png) center/cover no-repeat}
#root.rad{background:radial-gradient(ellipse 70% 80% at 42% 45%,#2a2725 0%,#151312 55%,#0c0b0b 100%)}
.a{position:absolute}
.acc{color:#ff5a1f}.cap{color:#a59f98}.dim{color:#8a847e}.body{color:#d6d2c9}
.ghost{position:absolute;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.13);font-weight:900;letter-spacing:-.04em;line-height:1;white-space:nowrap}
.blk{font-weight:900;letter-spacing:-.035em}
.tag{position:absolute;left:110px;top:92px;font-size:22px;letter-spacing:.12em;white-space:nowrap}
.tag b{color:#ff5a1f}.tag span{color:#8a847e}
.ttl{position:absolute;left:110px;top:130px;width:1640px;font-size:66px;font-weight:900;letter-spacing:-.03em;line-height:1.25;white-space:nowrap}
.hl{position:absolute;height:1px;background:#55504c;transform-origin:left}
.vl{position:absolute;width:1px;background:#55504c;transform-origin:top}
.sq{position:absolute;border:3px solid #f4f4f2}
.card{position:absolute;background:#1d1a19;border:1.5px solid #3a3533;border-radius:29px}
.card.hi{background:#2a2523;border:4px solid #ff5a1f}
.mask{display:block;overflow:hidden}.mask>span{display:block}
.ch{display:inline-block;white-space:pre}
.flash{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#fff;opacity:0;z-index:30;pointer-events:none}
.brand{position:absolute;font-size:22px;letter-spacing:.25em;color:#8a847e}
.hline{position:absolute;height:1px;background:rgba(255,255,255,.28)}
.dots{position:absolute;display:flex;gap:14px}.dots i{width:12px;height:12px;border-radius:50%;border:1.5px solid rgba(255,255,255,.6)}.dots i.on{background:#ff5a1f;border-color:#ff5a1f}
.chip{border:1.5px solid rgba(255,255,255,.18);border-radius:22px;background:#1d1a19;padding:26px 30px}
.chip b{display:block;font-size:22px;font-weight:800;letter-spacing:.2em;color:#8a847e}
.chip span{display:block;font-size:38px;font-weight:800;margin-top:10px;white-space:nowrap}
.chip.c{border-color:#ff5a1f}.chip.c b{color:#ff5a1f}
.pill{display:inline-block;border-radius:999px;padding:10px 24px;font-size:24px;font-weight:800;letter-spacing:.06em}
.qrbox{position:absolute;background:#f4f4f2;border-radius:32px;box-shadow:0 0 0 10px rgba(255,90,31,.18),0 30px 80px rgba(0,0,0,.5)}
.bub{position:absolute;background:#2a2523;border:1.5px solid #4a4340;border-radius:26px 26px 26px 6px;padding:22px 30px;font-size:30px;font-weight:600;color:#f4f4f2;white-space:nowrap}
*{word-break:keep-all;overflow-wrap:break-word}
'''

SQJS = r'''(function(){
function firstText(el){const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.nodeValue.trim()?1:3});return w.nextNode();}
function place(){
  const st=document.createElement('style'); st.textContent='#root *{transform:none!important;translate:none!important;scale:none!important;rotate:none!important}'; document.head.appendChild(st);
  const cv=document.createElement('canvas').getContext('2d');
  document.querySelectorAll('[data-sq]').forEach(sq=>{
    const el=document.querySelector(sq.dataset.sq); if(!el) return; const tn=firstText(el); if(!tn) return;
    let i=0; while(i<tn.nodeValue.length && /\s/.test(tn.nodeValue[i])) i++;
    const ch=tn.nodeValue[i]; const r=document.createRange(); r.setStart(tn,i); r.setEnd(tn,i+1); const b=r.getBoundingClientRect();
    const cs=getComputedStyle(tn.parentElement); const f=parseFloat(cs.fontSize);
    cv.font=cs.fontWeight+' '+f+'px '+cs.fontFamily; const m=cv.measureText(ch);
    const base=b.top+(m.fontBoundingBoxAscent||0.93*f);
    const inkTop=base-m.actualBoundingBoxAscent, inkLeft=b.left-m.actualBoundingBoxLeft;
    const s=Math.round(Math.max(40,Math.min(90,0.45*f))), T=Math.max(3,Math.round(0.06*s)), c='#f4f4f2', g='linear-gradient('+c+','+c+')';
    const dx=parseFloat(sq.dataset.dx||0)*f, dy=parseFloat(sq.dataset.dy||0)*f; sq.style.left=(inkLeft-0.55*s+dx)+'px'; sq.style.top=(inkTop-0.55*s+dy)+'px'; sq.style.width=s+'px'; sq.style.height=s+'px';
    sq.style.right='auto'; sq.style.bottom='auto'; sq.style.border='none';
    sq.style.background=g+' left top/100% '+T+'px no-repeat,'+g+' left top/'+T+'px 100% no-repeat,'+g+' right top/'+T+'px 25% no-repeat,'+g+' left bottom/30% '+T+'px no-repeat';
  });
  st.remove();
}
place(); if(document.fonts) document.fonts.ready.then(place);
})();'''


def page(dur, body, js, rad=False):
    return f'''<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/><script src="gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" class="{'rad' if rad else ''}" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{body}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
tl.from(".sq",{{opacity:0,scale:.4,rotation:-45,duration:.7,ease:"back.out(1.8)"}},0.35);
{js}
window.__timelines["main"]=tl;
{SQJS}
tl.seek(0);
</script></body></html>'''


class B:
    def __init__(s, dur): s.dur = dur; s.items = []
    def add(s, cls, style, inner=''):
        i = len(s.items)
        s.items.append(f'<div class="{cls} clip" style="{style}" data-start="0" data-duration="{s.dur}" data-track-index="{i}">{inner}</div>')
    def html(s): return '\n'.join(s.items)


SCENES = []  # (id, dur)

def write(name, dur, b, js, rad=False, assets=()):
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    for f in ['hyperframes.json', 'meta.json', 'package.json', 'bg.png']:
        shutil.copy(os.path.join(HERE, f), d)
    for f in ['gsap.min.js', 'PretendardVariable.woff2']:
        shutil.copy(os.path.join(LIB, f), d)
    for a in assets: shutil.copy(a, d)
    open(d + '/index.html', 'w').write(page(dur, b.html(), js, rad))
    SCENES.append((name, dur))


def bold(t):
    return re.sub(r'\*\*(.+?)\*\*', lambda m: '<b style="color:#f4f4f2;font-weight:800">' + m.group(1) + '</b>', t, flags=re.S)

def chars(t):
    return ''.join(f'<span class="ch">{c}</span>' for c in t)

def header(b, tag, sub, ghost, title, head='mask'):
    b.add('tag t-tag', '', f'<b>{tag}  </b><span>{sub}</span>')
    b.add('ghost t-ghost', 'right:110px;top:62px;font-size:110px;text-align:right', ghost)
    th = {'chars': chars(title), 'mask': f'<span class="mask"><span>{title}</span></span>'}.get(head, title)
    b.add('ttl t-ttl', '', th)
    b.add('sq', '', '')
    b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".t-ttl" class="sq clip"')
    b.add('hl t-hl', 'left:110px;top:244px;width:1700px')

HEAD_JS = {
 'mask': 'tl.from(".t-tag",{opacity:0,x:-30,duration:.5},0).from(".t-ttl .mask>span",{yPercent:105,duration:.8,ease:"power3.out"},.15).from(".t-ghost",{opacity:0,x:80,duration:1.1,ease:"power2.out"},.2).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
 'chars': 'tl.from(".t-tag",{opacity:0,y:-20,duration:.5},0).from(".t-ttl .ch",{opacity:0,y:40,rotationX:-80,duration:.5,stagger:.025,ease:"back.out(1.6)"},.1).from(".t-ghost",{opacity:0,duration:1.2},.3).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
 'blur': 'tl.from(".t-tag",{opacity:0,duration:.5},0).from(".t-ttl",{opacity:0,filter:"blur(14px)",scale:1.06,transformOrigin:"left center",duration:.9,ease:"power2.out"},.1).from(".t-ghost",{opacity:0,y:30,duration:1.1},.3).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
}

CARD_FX = {
 'rise': 'tl.from(".cd",{opacity:0,y:90,duration:.8,stagger:.18,ease:"power3.out"},.7);',
 'zoom': 'tl.from(".cd",{opacity:0,scale:.6,duration:.75,stagger:.15,ease:"back.out(1.5)"},.7);',
 'wipe': 'tl.from(".cd",{clipPath:"inset(0 0 100% 0 round 29px)",duration:.9,stagger:.2,ease:"power3.inOut"},.7);',
 'flip': 'tl.from(".cd",{opacity:0,rotationX:-75,transformPerspective:2400,transformOrigin:"center top",duration:.9,stagger:.2,ease:"power3.out"},.7);',
 'split': 'gsap.utils.toArray(".cd").forEach((c,i)=>tl.from(c,{opacity:0,x:(i%2?1:-1)*420,rotation:(i%2?1:-1)*4,duration:.85,ease:"power4.out"},.7+i*.16));',
 'stack': 'tl.from(".cd",{opacity:0,y:-620,duration:.9,stagger:.24,ease:"bounce.out"},.6);',
 'build': 'tl.from(".cd",{scaleY:0,transformOrigin:"center bottom",duration:.75,stagger:.28,ease:"power3.out"},.7);',
 'snap': 'tl.to(".flash",{opacity:.35,duration:.06},.68).to(".flash",{opacity:0,duration:.35},.74).from(".cd",{opacity:0,x:160,skewX:-14,duration:.3,stagger:.12,ease:"power4.out"},.7);',
 'left': 'tl.from(".cd",{opacity:0,x:-120,duration:.7,stagger:.2,ease:"power3.out"},.7);',
}
INNER_FX = 'tl.from(".cd .in",{opacity:0,y:18,duration:.5,stagger:.12},1.1);'


def key_bar(b, text, y=810, kfx='type'):
    b.add('card kb', f'left:110px;top:{y}px;width:1700px;height:120px;border-radius:22px',
          (f'<div class="a kbar" style="left:0;top:0;width:100%;height:100%;border-radius:22px;background:linear-gradient(90deg,rgba(255,90,31,.30),rgba(255,90,31,0) 85%);transform-origin:left"></div>' if kfx == 'sweep' else '')
          + '<div class="a" style="left:40px;top:0;height:120px;display:flex;align-items:center;font-size:22px;font-weight:700;letter-spacing:.35em;color:#ff5a1f">KEY</div>'
          + f'<div class="a kt" style="left:180px;top:0;height:120px;width:1480px;display:flex;align-items:center;font-size:36px;font-weight:700;white-space:nowrap"><span>{bold(text)}</span></div>')

def key_js(t0, kfx='type'):
    j = f'tl.from(".kb",{{opacity:0,y:40,duration:.6,ease:"power3.out"}},{t0:.2f})'
    j += {'type': f'.from(".kt",{{clipPath:"inset(0 100% 0 0)",duration:1.2,ease:"none"}},{t0+.35:.2f});',
          'sweep': f'.from(".kbar",{{scaleX:0,duration:1.0,ease:"power2.out"}},{t0+.3:.2f}).from(".kt",{{opacity:0,x:-30,duration:.6}},{t0+.5:.2f});',
          'pop': f'.from(".kt",{{opacity:0,scale:1.35,transformOrigin:"left center",duration:.6,ease:"back.out(2.2)"}},{t0+.35:.2f});'}[kfx]
    return j


# ───────────── 1. PART 인트로 (p1in 레이아웃) ─────────────
def intro(id, n, title, sub, chips, hi, fx):
    dur = 6; b = B(dur)
    b.add('brand', 'left:150px;top:110px', f'PART {n} · {["","TOOLS","HANDS-ON","MAKE","NOW","LEADER"][n]}')
    b.add('hline', 'left:150px;right:110px;top:170px')
    b.add('ghost bigg', 'right:110px;top:205px;font-size:560px;line-height:.86;letter-spacing:-.06em', f'0{n}')
    b.add('a big blk', 'right:110px;top:150px;font-size:560px;line-height:.86;letter-spacing:-.06em;color:#262321', f'0{n}')
    b.add('a lbl', 'left:150px;top:300px;font-size:34px;font-weight:800;letter-spacing:.3em;color:#ff5a1f', f'PART {n}')
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".pttl" class="sq clip"')
    b.add('a pttl blk', 'left:150px;top:370px;font-size:150px;line-height:1.05;letter-spacing:-.04em', title)
    b.add('a psub', 'left:150px;top:720px;font-size:36px;font-weight:500;color:#cbc5ba', sub)
    cs = ''.join(f'<div class="chip{" c" if i == hi else ""}"><b>{i+1:02d}</b><span>{c}</span></div>' for i, c in enumerate(chips))
    b.add('a chips', f'left:150px;right:110px;bottom:130px;display:grid;grid-template-columns:repeat({len(chips)},1fr);gap:24px', cs)
    dots = ''.join(f'<i class="{"on" if i+1 == n else ""}"></i>' for i in range(5))
    b.add('dots', 'right:110px;top:118px', dots)
    js = 'tl.from(".brand",{opacity:0,duration:.6},0).from(".hline",{scaleX:0,transformOrigin:"left",duration:.9,ease:"power3.out"},0.1);'
    js += {
     'right': 'tl.from(".big",{opacity:0,x:140,duration:1.2,ease:"power3.out"},0.2).from(".bigg",{opacity:0,y:-40,duration:1.3},0.6);',
     'drop': 'tl.from(".big",{opacity:0,y:-300,duration:1.1,ease:"bounce.out"},0.2).from(".bigg",{opacity:0,scale:1.2,duration:1.3},0.6);',
     'scale': 'tl.from(".big",{opacity:0,scale:.3,transformOrigin:"right center",duration:1.1,ease:"back.out(1.4)"},0.2).from(".bigg",{opacity:0,x:60,duration:1.3},0.6);',
     'blur': 'tl.from(".big",{opacity:0,filter:"blur(30px)",duration:1.3,ease:"power2.out"},0.2).from(".bigg",{opacity:0,y:40,duration:1.3},0.6);',
     'spin': 'tl.from(".big",{opacity:0,rotationY:90,transformPerspective:2000,duration:1.2,ease:"power3.out"},0.2).from(".bigg",{opacity:0,duration:1.3},0.6);',
    }[fx]
    js += ('tl.from(".lbl",{opacity:0,x:-40,duration:.6},0.6).from(".pttl",{opacity:0,y:60,duration:.8,ease:"power3.out"},0.8)'
           '.from(".psub,.dots",{opacity:0,y:20,duration:.6},1.3).from(".chip",{opacity:0,y:50,duration:.5,stagger:.16,ease:"power2.out"},1.6)'
           f'.to(".chip.c",{{y:-10,boxShadow:"0 20px 50px rgba(255,90,31,.25)",duration:.5}},{1.6+len(chips)*.16+.3:.2f});')
    write(id, dur, b, js, rad=True)


# ───────────── 2. 카드 화면 (정리형 일반화) ─────────────
def cards(id, tag, sub, ghost, title, items, hi=-1, key=None, fx='rise', head='mask', kfx='type', top=300, h=470, dur=7, numsize=100, extra_js=''):
    """items: [(번호표시, 소제목, 본문)]"""
    b = B(dur); header(b, tag, sub, ghost, title, head)
    n = len(items); gap = 30; cw = (1700 - gap * (n - 1)) / n
    fs = 34 if n > 3 else 40
    for i, (num, head2, body) in enumerate(items):
        x = 110 + i * (cw + gap); ishi = hi == i
        inner = f'<div class="in a blk" style="left:40px;top:34px;font-size:{numsize}px;line-height:1.1;color:{"#ff5a1f" if ishi else "#f4f4f2"};white-space:nowrap">{num}</div>'
        y2 = 34 + numsize * 1.1 + 18
        if head2:
            inner += f'<div class="in a" style="left:40px;top:{y2:.0f}px;width:{cw-80:.0f}px;font-size:{fs+4}px;font-weight:800;line-height:1.25;white-space:pre-line">{head2}</div>'
            y2 += (fs + 4) * 1.25 * (head2.count("\n") + 1) + 14
        inner += f'<div class="hl" style="left:40px;top:{y2:.0f}px;width:{cw-80:.0f}px"></div>'
        inner += f'<div class="in a" style="left:40px;top:{y2+24:.0f}px;width:{cw-80:.0f}px;font-size:{fs-4 if head2 else fs}px;font-weight:500;color:#a59f98;line-height:1.35;white-space:pre-line">{bold(body)}</div>'
        b.add(f'card cd cd{i}' + (' hi' if ishi else ''), f'left:{x:.0f}px;top:{top}px;width:{cw:.0f}px;height:{h}px', inner)
    if fx == 'snap': b.add('flash', '')
    js = HEAD_JS[head] + CARD_FX[fx] + INNER_FX
    t0 = 1.7 + (n - 1) * .2
    if key:
        key_bar(b, key, top + h + 40, kfx); js += key_js(t0, kfx)
    if hi >= 0:
        js += f'tl.to(".cd.hi",{{boxShadow:"0 0 0 10px rgba(255,90,31,.18), 0 30px 70px rgba(255,90,31,.25)",y:-10,duration:.6,ease:"power2.out"}},{t0+1.4:.2f});'
    write(id, dur, b, js + extra_js)


# ───────────── 3. 미션 화면 ─────────────
def mission(id, n, title, tool, steps, says, note, fx):
    dur = 7; b = B(dur)
    b.add('tag t-tag', '', f'<b>PART 2 · 폰으로 해 봅시다  </b><span>{tool}</span>')
    b.add('ghost t-ghost', 'right:110px;top:62px;font-size:110px;text-align:right', 'Mission.')
    b.add('a mnum blk', 'left:110px;top:150px;font-size:44px;letter-spacing:.2em;color:#ff5a1f', f'MISSION {n:02d}')
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".mt" class="sq clip"')
    b.add('a mt blk', 'left:110px;top:215px;font-size:84px;line-height:1.12;width:760px;white-space:pre-line', title)
    b.add('a mtool', 'left:110px;top:470px', f'<span class="pill" style="background:#ff5a1f;color:#111">{tool}</span>')
    b.add('a mnote', 'left:110px;top:560px;width:720px;font-size:30px;line-height:1.5;color:#a59f98;white-space:pre-line', bold(note))
    b.add('vl mvl', 'left:900px;top:150px;height:800px')
    for i, s in enumerate(steps):
        y = 160 + i * 150
        b.add(f'a st st{i}', f'left:960px;top:{y}px;width:850px;height:120px;display:flex;align-items:center;gap:30px',
              f'<div style="flex:none;width:84px;height:84px;border-radius:50%;border:2.5px solid {"#ff5a1f" if i == len(steps)-1 else "#55504c"};display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;color:{"#ff5a1f" if i == len(steps)-1 else "#f4f4f2"}">{i+1}</div>'
              f'<div style="font-size:40px;font-weight:700;line-height:1.3">{bold(s)}</div>')
    ys = 160 + len(steps) * 150 + 10
    b.add('a slab', f'left:960px;top:{ys}px;font-size:22px;font-weight:700;letter-spacing:.3em;color:#8a847e', '이렇게 써 보세요')
    for i, s in enumerate(says):
        b.add(f'bub say say{i}', f'left:{960 + (i % 2) * 40}px;top:{ys + 50 + i * 92}px', '“' + s + '”')
    js = 'tl.from(".t-tag",{opacity:0,x:-30,duration:.5},0).from(".t-ghost",{opacity:0,x:80,duration:1.1},.2).from(".mnum",{opacity:0,letterSpacing:".6em",duration:.8},.2)'
    js += {'up': '.from(".mt",{opacity:0,y:60,duration:.8,ease:"power3.out"},.45)',
           'chars': '.from(".mt",{opacity:0,filter:"blur(12px)",duration:.8},.45)',
           'scale': '.from(".mt",{opacity:0,scale:1.3,transformOrigin:"left top",duration:.8,ease:"power3.out"},.45)',
           'left': '.from(".mt",{opacity:0,x:-80,duration:.8,ease:"power3.out"},.45)'}[fx]
    js += '.from(".mtool",{opacity:0,scale:.6,duration:.5,ease:"back.out(2)"},.9).from(".mnote",{opacity:0,y:20,duration:.6},1.1).from(".mvl",{scaleY:0,duration:.8},.6)'
    js += '.from(".st",{opacity:0,x:60,duration:.55,stagger:.3,ease:"power3.out"},1.0)'
    t = 1.0 + len(steps) * .3 + .3
    js += f'.from(".slab",{{opacity:0,duration:.4}},{t:.2f}).from(".say",{{opacity:0,y:30,scale:.9,transformOrigin:"left bottom",duration:.5,stagger:.35,ease:"back.out(1.8)"}},{t+.2:.2f});'
    write(id, dur, b, js)


# ───────────── 4. QR 투표 화면 ─────────────
def qrscene(id, tag, sub, title, lines, cap, head='mask', listfx='left', lines_fs=44, numbered=True):
    dur = 6; b = B(dur); header(b, tag, sub, 'Vote.', title, head)
    for i, l in enumerate(lines):
        y = 330 + i * 120
        num = f'<span style="flex:none;width:70px;font-size:40px;font-weight:900;color:#ff5a1f">{i+1}</span>' if numbered else ''
        b.add(f'a ln ln{i}', f'left:110px;top:{y}px;width:1100px;height:100px;display:flex;align-items:center;border-bottom:1px solid #3a3533',
              num + f'<span style="font-size:{lines_fs}px;font-weight:700">{bold(l)}</span>')
    q = QRBOX
    b.add('qrbox', f'left:{q["x"]-20}px;top:{q["y"]-20}px;width:{q["s"]+40}px;height:{q["s"]+40}px')
    b.add('a qrcap', f'left:{q["x"]-20}px;top:{q["y"]+q["s"]+50}px;width:{q["s"]+40}px;text-align:center;font-size:30px;font-weight:700;line-height:1.45;white-space:pre-line', bold(cap))
    js = HEAD_JS[head]
    js += {'left': 'tl.from(".ln",{opacity:0,x:-80,duration:.6,stagger:.18,ease:"power3.out"},.7);',
           'up': 'tl.from(".ln",{opacity:0,y:50,duration:.6,stagger:.18,ease:"power3.out"},.7);'}[listfx]
    js += 'tl.from(".qrbox",{opacity:0,scale:.5,rotation:-8,duration:.8,ease:"back.out(1.6)"},1.0).from(".qrcap",{opacity:0,y:20,duration:.5},1.6)'
    js += '.to(".qrbox",{scale:1.04,duration:.45,yoyo:true,repeat:3,ease:"sine.inOut"},2.4);'
    write(id, dur, b, js)


# ───────────── 장면 정의 ─────────────
def build_all():
    os.makedirs(QR, exist_ok=True)
    import qrcode
    def mkqr(name, url):
        img = qrcode.make(url, border=1, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
        p = os.path.join(QR, name + '.png'); img.save(p); return p
    APPS = [('ChatGPT', 'chatgpt.com', 'https://chatgpt.com', '필수', '묻고 쓰기 · 사진 읽기 · 음성 대화'),
            ('Gemini', 'gemini.google.com', 'https://gemini.google.com', '필수', '사진 편집 · 카메라 대화(Live)'),
            ('NotebookLM', 'notebooklm.google.com', 'https://notebooklm.google.com', '선택', '자료 요약 · 라디오 방송'),
            ('클로바노트', 'clovanote.naver.com', 'https://clovanote.naver.com', '선택', '녹음 → 회의록')]
    qpaths = [mkqr('app%d' % i, a[2]) for i, a in enumerate(APPS)]
    web = mkqr('web', 'https://ssca1612.pages.dev')

    # ── 오프닝
    # 표지·Q&A 등은 10.20 장면을 문구만 바꿔 다시 씀 (reuse())
    qrscene('poll1', 'OPENING · 손들기 대신 폰으로', '실시간 투표', 'AI, 얼마나 써 보셨나요?',
            ['아직 **한 번도** 안 써 봤다', '**몇 번** 써 봤다', '**매주** 쓴다', '**업무에도** 쓴다'],
            '폰 카메라로\n**QR을 비춰 주세요**', head='chars')
    # 퀴즈 안내
    cards('quiz', 'OPENING · 퀴즈', 'AI 사진 vs 진짜 사진', 'Quiz.', 'AI가 만든 사진일까, 진짜 사진일까?',
          [('AI', '“AI다”', '사람이 찍지 않고\n**AI가 그린 사진**'), ('VS', '', '사진 **다섯 장**\n폰으로 **하나씩** 투표'), ('REAL', '“진짜다”', '실제로 **카메라로\n찍은 사진**')],
          hi=1, key='정답률이 **절반**을 넘을까요?', fx='zoom', head='blur', kfx='pop', numsize=110)
    # 목차 (5칸)
    cards('toc', 'CONTENTS', '오늘 강의는 이렇게 진행합니다', 'Contents.', '폰 하나로, 오늘부터',
          [('01', '도구 지도', '무료로 쓰는\nAI 도구 한눈에'), ('02', '폰으로\n해 보기', '미션 네 가지\n직접 해 봅니다'),
           ('03', '노트북으로\n만들기', '말로 프로그램을\n만듭니다'), ('04', 'AI는 지금\n어디까지', '대답하는 AI에서\n일하는 AI로'),
           ('05', '리더가\n알아야 할 것', '보안과 확인,\n결과물 보는 법')],
          hi=1, fx='build', head='mask', top=300, h=600, numsize=90)

    # ── PART 1 도구 지도
    intro('p1in', 1, 'AI 도구 지도', '도구가 너무 많습니다 — 딱 이것만 아시면 됩니다', ['묻고 쓰기', '자료 정리', '만들기', '그림·영상'], 0, 'right')
    cards('toolmap', 'PART 1 · 도구 지도', '용도별로 고르세요', 'Map.', '무엇을 하고 싶은가로 고릅니다',
          [('01', '묻고 쓰기', '**ChatGPT · Gemini · Claude**\n질문 · 초안 · 번역 · 요약'),
           ('02', '자료 정리', '**NotebookLM · 클로바노트**\n긴 문서 요약 · 회의록'),
           ('03', '만들기', '**Claude · Gemini 캔버스**\n웹페이지 · 업무 도구'),
           ('04', '그림·영상', '**Gemini 이미지 · Flow**\n사진 편집 · 홍보 영상')],
          hi=0, key='오늘 실습은 **ChatGPT · Gemini** 두 앱이면 충분합니다', fx='flip', head='chars', kfx='sweep', numsize=80)
    cards('freepaid', 'PART 1 · 도구 지도', '무료 vs 유료', 'Free.', '오늘 실습은 전부 무료입니다',
          [('FREE', '무료 계정', '기능은 **거의 같습니다**\n하루 쓰는 **양에 제한**\n일단 **매일 써 보기**'),
           ('PAID', '유료 (월 3만 원 안팎)', '더 **많이**, 더 **빠르게**\n**최신 모델** 먼저\n매일 쓰게 되면 **그때**')],
          hi=0, key='처음엔 **무료로 충분**합니다 — 손에 익는 게 먼저', fx='split', head='blur', kfx='type', numsize=90)
    # 앱 QR 4개
    b = B(7); header(b, 'PART 1 · 준비', '구글 계정 하나면 Gemini · NotebookLM 바로 로그인', 'Apps.', '오늘 폰에 이 앱만 있으면 됩니다', 'mask')
    cw = (1700 - 3 * 30) / 4
    for i, (nm, url, full, need, use) in enumerate(APPS):
        x = 110 + i * (cw + 30)
        b.add(f'card cd cd{i}' + (' hi' if need == '필수' else ''), f'left:{x:.0f}px;top:290px;width:{cw:.0f}px;height:650px',
              f'<div class="a" style="left:36px;top:32px"><span class="pill" style="background:{"#ff5a1f" if need=="필수" else "#3a3533"};color:{"#111" if need=="필수" else "#d6d2c9"}">{need}</span></div>'
              f'<div class="a blk" style="left:36px;top:100px;font-size:52px;white-space:nowrap">{nm}</div>'
              f'<div class="a" style="left:36px;top:172px;font-size:26px;color:#a59f98;white-space:nowrap">{use}</div>'
              f'<div class="a qq" style="left:{(cw-300)/2:.0f}px;top:240px;width:300px;height:300px;background:#f4f4f2;border-radius:20px;padding:14px"><img src="app{i}.png" style="width:100%;height:100%;image-rendering:pixelated"/></div>'
              f'<div class="a" style="left:0;width:100%;top:570px;text-align:center;font-size:26px;font-weight:700;color:#d6d2c9">{url}</div>')
    js = HEAD_JS['mask'] + CARD_FX['rise'] + 'tl.from(".qq",{opacity:0,scale:.6,duration:.6,stagger:.18,ease:"back.out(1.7)"},1.2);'
    write('apps', 7, b, js, assets=qpaths)

    # ── PART 2 폰 실습
    intro('p2in', 2, '폰으로\n해 봅시다'.replace('\n', '<br>'), '폰을 꺼내 주세요 — 막히면 옆 사람과 함께', ['종이 → 표', '내 사진 바꾸기', '말로 대화', '틀린 곳 찾기'], 1, 'drop')
    mission('m1', 1, '종이를 찍으면\n표가 됩니다', 'ChatGPT', ['ChatGPT 앱에서 **카메라(+)** 누르기', '실습 카드 **뒷면 표**를 찍기', '아래처럼 **말하거나 쓰기**'],
            ['이 표를 엑셀 표로 만들어 줘', '민원이 가장 많은 3가지를 요약해 줘', '내년 계획 보고서 첫 문단을 써 줘'],
            '공문 · 회의 자료 · 손글씨 메모도\n**찍기만 하면 글자와 표**가 됩니다', 'up')
    mission('m2', 2, '내 사진을\n바꿔 봅니다', 'Gemini', ['Gemini 앱에서 **+ → 사진** 고르기', '**셀카** 또는 앨범 속 사진', '바꾸고 싶은 모습을 **말로**'],
            ['증명사진처럼 바꿔 줘', '귀여운 캐리커처로 그려 줘', '스페인 여행 사진처럼 바꿔 줘'],
            '보너스 — 옛날 **흑백 가족사진**을\n“**컬러로 복원**해 줘”', 'scale')
    mission('m3', 3, 'AI와 말로\n대화합니다', 'Gemini Live · ChatGPT 음성', ['**Gemini Live**(물결 아이콘) 누르기', '**편하게 말 걸기** — 사투리도 OK', '**카메라** 켜고 물건 비추기'],
            ['오늘 진주 저녁 메뉴 추천해 줘', '이거 뭐야? 어디에 쓰는 거야?', '영어로 자기소개 연습 좀 시켜 줘'],
            '타자 없이 **말로** 묻고,\n**눈으로 보여 주며** 물어봅니다', 'left')

    # 미션 4 — AI가 틀린 곳 찾기 (문제 / 정답)
    WRONG = [
        ('세종대왕 맥북프로 던짐 사건을 알려 줘', '조선왕조실록에 기록된 일화로, 세종대왕이\n훈민정음 초고를 쓰다 화가 나 **맥북프로**를\n신하에게 던진 사건입니다.', '맥북은 **2006년**에 나왔습니다 — 실제로 화제가 된 AI 답변'),
        ('경상남도를 소개해 줘', '경상남도는 인구 **약 500만 명**이며,\n도청은 **진주시**에 있습니다.', '인구는 **약 320만 명**, 도청 본청은 **창원** (여기는 서부청사)'),
        ('비슷한 판례를 찾아 줘', '**대법원 2019다12345** 판결 등\n비슷한 판례가 3건 있습니다.', '2023년 미국 변호사가 AI가 **지어낸 판례**를 냈다가 **벌금**'),
    ]
    for ans in (False, True):
        b = B(7 if not ans else 6)
        header(b, 'PART 2 · 미션 4', 'AI 환각(할루시네이션)', 'Wrong?' if not ans else 'Check.', 'AI가 틀린 곳을 찾아라' if not ans else '정답 — AI는 모르면 지어냅니다', 'chars' if not ans else 'blur')
        for i, (q, a, fix) in enumerate(WRONG):
            x = 110 + i * (1700 - 60) / 3 + i * 30; w = (1700 - 60) / 3
            inner = (f'<div class="in a" style="right:30px;top:30px;max-width:{w-60:.0f}px;background:#3a3533;border-radius:22px 22px 6px 22px;padding:16px 22px;font-size:26px;font-weight:700;color:#f4f4f2">{q}</div>'
                     f'<div class="in a" style="left:30px;top:130px;width:{w-60:.0f}px;font-size:22px;font-weight:800;letter-spacing:.2em;color:#ff5a1f">AI 답변</div>'
                     f'<div class="in a ans" style="left:30px;top:172px;width:{w-60:.0f}px;font-size:29px;font-weight:500;line-height:1.45;color:#d6d2c9;white-space:pre-line">{bold(a)}</div>')
            if ans:
                inner += (f'<div class="a fix" style="left:20px;right:20px;bottom:20px;height:150px;border-radius:20px;background:rgba(255,90,31,.14);border:2px solid #ff5a1f;padding:20px 24px;font-size:27px;font-weight:600;line-height:1.4;color:#f4f4f2">'
                          f'<b style="color:#ff5a1f">✕ </b>{bold(fix)}</div>')
            b.add(f'card cd cd{i}', f'left:{x:.0f}px;top:290px;width:{w:.0f}px;height:{540 if not ans else 590}px', inner)
        if not ans:
            b.add('a q3', 'left:110px;top:860px;width:1700px;text-align:center;font-size:40px;font-weight:800', '그럴듯하지만 — <span class="acc">어디가 틀렸을까요?</span>')
            js = HEAD_JS['chars'] + CARD_FX['stack'] + INNER_FX + 'tl.from(".q3",{opacity:0,scale:.8,duration:.6,ease:"back.out(2)"},2.6);'
        else:
            key_bar(b, 'AI는 **틀려도 자신 있게** 말합니다 — **확인은 사람이**', 910, 'sweep')
            js = HEAD_JS['blur'] + 'tl.from(".fix",{opacity:0,y:40,scale:.9,duration:.6,stagger:.35,ease:"back.out(1.8)"},.8).to(".cd",{x:"+=8",duration:.05,repeat:5,yoyo:true,stagger:.35},.8)' + ';' + key_js(2.2, 'sweep')
        write('m4' if not ans else 'm4ans', 7 if not ans else 6, b, js)

    # ── PART 3 노트북으로 만들기
    intro('p3in', 3, '노트북으로<br>만들기', '코딩 몰라도 — 말로 프로그램을 만듭니다', ['완성품 보기', '주문 받기', 'AI가 만드는 동안 쉬기', '폰으로 받기'], 1, 'scale')
    cards('showcase', 'PART 3 · 노트북으로 만들기', '강사가 말로 만든 것들', 'Made.', '제가 말로 만든 업무 도구',
          [('01', '엑셀 → 그래프', '엑셀을 넣으면\n**보고서용 그래프**가 바로\n국토부 실습 도구 1'),
           ('02', '취합 검증', '여러 곳에서 온 파일의\n**틀린 숫자**를 찾아 줌\n국토부 실습 도구 3'),
           ('03', '오늘 이 화면', '움직이는 **강의 화면**과\n**투표 페이지**까지\n모두 말로 만들었습니다')],
          hi=2, key='코딩 한 줄 없이 — **말로 주문**했습니다', fx='wipe', head='mask', kfx='type')
    cards('order', 'PART 3 · 주문 받기', '골라 주시거나, 직접 말씀해 주세요', 'Order.', '무엇을 만들어 드릴까요?',
          [('01', '수료식\n초대장', '12월 수료식 ·\n동아리 공연 안내 페이지'), ('02', '버킷리스트\n모음', '23기 버킷리스트를\n한 페이지에'),
           ('03', '발표 순서\n룰렛', '돌리면 순서가\n정해지는 룰렛'), ('04', '우리 과\n민원 안내', '자주 묻는 질문\n안내 페이지')],
          hi=-1, key='손을 들어 주세요 — **직접 주문**하셔도 좋습니다', fx='snap', head='chars', kfx='pop', numsize=80, h=470)
    # 쉬는 시간
    b = B(8)
    b.add('a brk blk', 'left:150px;top:300px;font-size:150px;line-height:1.1;letter-spacing:-.04em', 'AI가 일하는 동안<br><span class="acc">잠시 쉬겠습니다</span>')
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".brk" class="sq clip"')
    b.add('ghost gb', 'right:110px;top:640px;font-size:260px', 'Break.')
    b.add('a wk', 'left:150px;top:720px;display:flex;align-items:center;gap:26px;font-size:38px;font-weight:700;color:#d6d2c9',
          '<span>AI가 만드는 중</span><i class="d1" style="width:18px;height:18px;border-radius:50%;background:#ff5a1f"></i><i class="d2" style="width:18px;height:18px;border-radius:50%;background:#ff5a1f"></i><i class="d3" style="width:18px;height:18px;border-radius:50%;background:#ff5a1f"></i>')
    b.add('a bar', 'left:150px;top:820px;width:1100px;height:10px;border-radius:5px;background:#3a3533', '<div class="fill" style="width:100%;height:100%;border-radius:5px;background:#ff5a1f;transform-origin:left"></div>')
    js = ('tl.from(".brk",{opacity:0,y:60,duration:.9,ease:"power3.out"},.2).from(".gb",{opacity:0,x:120,duration:1.4},.5).from(".wk",{opacity:0,duration:.6},1.0).from(".bar",{opacity:0,duration:.4},1.0)'
          '.fromTo(".fill",{scaleX:0},{scaleX:.85,duration:6,ease:"power1.out"},1.2)'
          '.to(".d1",{opacity:.2,duration:.4,repeat:13,yoyo:true},1.2).to(".d2",{opacity:.2,duration:.4,repeat:13,yoyo:true},1.4).to(".d3",{opacity:.2,duration:.4,repeat:13,yoyo:true},1.6);')
    write('break', 8, b, js, rad=True)
    cards('share', 'PART 3 · 폰으로 받기', '링크 하나면 누구나 열어 봅니다', 'Share.', '다 만들었습니다 — 폰으로 받아 보세요',
          [('01', '게시', 'Claude 화면 오른쪽 위\n**게시(Publish)** 누르기'), ('02', '링크 복사', '만들어진 **주소를 복사**'),
           ('03', 'QR 만들기', '크롬 주소창 오른쪽\n**공유 → QR 코드 만들기**'), ('04', '폰으로 열기', '화면의 **QR을 찍으면**\n바로 열립니다')],
          hi=3, key='만든 것은 — **링크 하나로 공유**합니다', fx='left', head='blur', kfx='sweep', numsize=80)
    # 반전: 투표 페이지 정체
    b = B(8)
    b.add('a rv1', 'left:150px;top:200px;font-size:48px;font-weight:700;color:#a59f98', '사실, 처음에 투표한 그 페이지도')
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".rv2" class="sq clip"')
    b.add('a rv2 blk', 'left:150px;top:280px;font-size:170px;line-height:1.05;letter-spacing:-.045em', '<span class="acc">AI</span>가 만들었습니다')
    b.add('ghost', 'right:110px;top:90px;font-size:150px', 'Reveal.')
    b.add('card pr', 'left:150px;top:560px;width:1620px;height:330px;border-radius:29px',
          '<div class="a" style="left:44px;top:36px;font-size:22px;font-weight:700;letter-spacing:.3em;color:#ff5a1f">제가 한 말 (요청문)</div>'
          '<div class="a prt" style="left:44px;top:90px;width:1530px;font-size:40px;font-weight:600;line-height:1.55;color:#f4f4f2">“강의 중에 <b class="acc">폰으로 투표</b>하고, 결과가 <b class="acc">실시간 막대그래프</b>로 보이는 페이지를 만들어 줘.<br>문제는 내가 화면에서 넘기고, 검정 바탕에 주황 강조로.”</div>')
    js = ('tl.from(".rv1",{opacity:0,y:20,duration:.6},.2).from(".rv2",{opacity:0,scale:1.25,transformOrigin:"left center",filter:"blur(10px)",duration:.8,ease:"power3.out"},.9)'
          '.from(".ghost",{opacity:0,duration:1.2},.9).from(".pr",{opacity:0,y:60,duration:.7,ease:"power3.out"},1.8).from(".prt",{clipPath:"inset(0 100% 0 0)",duration:2.2,ease:"none"},2.3);')
    write('reveal', 8, b, js, rad=True)
    cards('sum_p3', 'PART 3 · 정리', '노트북으로 만들기', 'Summary.', '말로 만드는 업무 도구',
          [('01', '', '코딩 몰라도\n**말로 주문**합니다'), ('02', '', '마음에 안 들면\n**다시 말하면** 됩니다'), ('03', '', '만든 것은\n**링크 하나로 공유**합니다')],
          hi=1, key='만드는 사람에서, **맡기는 사람**으로 → PART 4', fx='flip', head='chars', kfx='type')

    # ── PART 4 AI는 지금 어디까지 (10.20 장면 재사용 + 인트로)
    intro('p4in', 4, 'AI는 지금<br>어디까지', '방금 AI가 쉬는 시간에 일했습니다 — 이게 요즘 AI입니다', ['AI 에이전트', '프롬프트 그다음', '신문물 지도', '한눈에 비교'], 0, 'blur')

    # ── PART 5 리더가 알아야 할 것
    intro('p5in', 5, '리더가<br>알아야 할 것', '곧 결재하는 자리 — AI를 어떻게 볼 것인가', ['다른 기관 사례', '보안 3원칙', '넣어도 될까?', '결과물 보는 법'], 1, 'spin')
    cards('security', 'PART 5 · 보안', '공무원 AI 사용 기본', 'Safe.', 'AI에 넣으면 안 되는 것 3가지',
          [('01', '개인정보', '주민번호 · 연락처 · 주소\n**민원인 실명**'), ('02', '비공개 문서', '내부 보고 · 감사 자료\n**원문 그대로**'), ('03', '결재 전 자료', '확정 안 된 계획 · 예산\n**아직 나가면 안 되는 숫자**')],
          hi=0, key='넣기 전에 한 번 — **가명 · 요약**으로 바꿔서, **기관 지침** 먼저', fx='stack', head='mask', kfx='sweep')
    OX = [('이미 배포한 **보도자료** 요약', 'O'), ('민원인 **이름·연락처**가 있는 민원서', 'X'), ('누구나 보는 **법령** 질문', 'O'), ('결재 전 **내년 예산안** 원본', 'X')]
    qrscene('ox', 'PART 5 · 퀴즈', '폰으로 O / X', '이건 넣어도 될까요?', [t for t, _ in OX], '**O / X**를\n폰으로 골라 주세요', head='blur', listfx='up')
    b = B(6); header(b, 'PART 5 · 퀴즈', '정답', 'Answer.', '정답 — 공개된 것은 O, 사람·비밀은 X', 'mask')
    for i, (t, a) in enumerate(OX):
        y = 320 + i * 140
        b.add(f'a oxl oxl{i}', f'left:110px;top:{y}px;width:1700px;height:110px;display:flex;align-items:center;border-bottom:1px solid #3a3533',
              f'<span style="flex:none;width:70px;font-size:40px;font-weight:900;color:#8a847e">{i+1}</span><span style="flex:1;font-size:46px;font-weight:700">{bold(t)}</span>'
              f'<span class="oxm" style="flex:none;width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:66px;font-weight:900;'
              + ('border:6px solid #ff5a1f;color:#ff5a1f">O' if a == 'O' else 'background:#3a3533;color:#f4f4f2">✕') + '</span>')
    js = HEAD_JS['mask'] + 'tl.from(".oxl",{opacity:0,x:-60,duration:.5,stagger:.15},.6).from(".oxm",{opacity:0,scale:2.4,rotation:-30,duration:.45,stagger:.4,ease:"back.out(2)"},1.4);'
    write('oxans', 6, b, js)
    cards('review', 'PART 5 · 리더의 확인', '직원이 AI로 만든 결과물', 'Review.', '직원이 AI로 만든 결과물, 이렇게 봅니다',
          [('01', '출처', '이 내용은\n**어디서 나왔나요?**'), ('02', '숫자', '원자료와\n**맞춰 봤나요?**'), ('03', '과정', 'AI에게\n**어떻게 시켰나요?**')],
          hi=2, key='AI를 **썼는지**보다, **확인했는지**를 물어보세요', fx='split', head='blur', kfx='pop')

    # ── 마무리
    qrscene('poll2', 'CLOSING · 다시 투표', '처음과 비교', '처음과 지금, 달라졌나요?',
            ['아직 **잘 모르겠다**', '**집에 가서** 다시 해 보겠다', '**내일 업무에** 써 보겠다', '**오늘 처음** 무언가 만들어 봤다'],
            '처음 투표와\n**나란히 비교**합니다', head='mask', listfx='up')
    qrscene('tomorrow', 'CLOSING · 한 줄 약속', '폰으로 적어 주세요', '내일 출근해서 해 볼 것 하나',
            ['예) 회의 녹음을 **회의록**으로', '예) 보도자료 **초안** 한 장', '예) 엑셀 표를 **그래프**로', '예) 민원 답변 **다듬기**'],
            '한 줄로 적으면\n**화면에 모아** 보여 드립니다', head='chars', listfx='left', numbered=False, lines_fs=40)
    return web


# ───────────── 10.20 장면 재사용 (문구만 교체) ─────────────
def reuse(web):
    R = os.path.join(HERE, 'reuse')
    def rw(src, name, subs, dur=None, assets=()):
        h = open(os.path.join(R, src)).read()
        for a, c in subs:
            assert a in h, (src, a)
            h = h.replace(a, c)
        d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
        for f in ['hyperframes.json', 'meta.json', 'package.json', 'bg.png']: shutil.copy(os.path.join(HERE, f), d)
        for f in ['gsap.min.js', 'PretendardVariable.woff2']: shutil.copy(os.path.join(LIB, f), d)
        for a in assets: shutil.copy(a, d)
        open(d + '/index.html', 'w').write(h)
        m = re.search(r'data-duration="([\d.]+)"', h); SCENES.append((name, float(m.group(1))))
    rw('cover1020.html', 'cover', [
        ('2026 하반기 상황관리 공감 워크숍', '제23기 중견리더과정'),
        ('<div class="ttl clip" data-start="0" data-duration="5" data-track-index="5">AI,</div>', '<div class="ttl clip" data-start="0" data-duration="5" data-track-index="5">공무원을 위한</div>'),
        ('<div class="ttl2 clip" data-start="0" data-duration="5" data-track-index="6">지금 어디까지 왔나</div>', '<div class="ttl2 clip" data-start="0" data-duration="5" data-track-index="6">AI 도구 활용법</div>'),
        ('data-track-index="4">지금 어디까지 왔나', 'data-track-index="4">AI 도구 활용법'),
        ('업무 효율을 높이는 AI 활용 — 대답하는 AI에서 일하는 AI로', '폰 하나로 오늘부터 — 묻고, 만들고, 맡기는 AI'),
        ('<b>2026. 10. 20</b><span>상황관리 공감 워크숍 AI 특강</span>', '<b>2026. 11. 5</b><span>경상남도인재개발원</span>'),
        ('data-dx="0.14" data-dy="0.04" ', ''),
        ('<i class="on"></i><i></i><i></i>', '<i class="on"></i><i></i><i></i><i></i><i></i>'),
    ])
    rw('sum01.html', 'sum01', [('PART 1 · 정리', 'PART 4 · 정리')])
    rw('sum03.html', 'sum03', [('PART 1 · 정리', 'PART 4 · 정리')])
    rw('ladder.html', 'ladder', [('PART 1 · 3막', 'PART 4 · 신문물')])
    rw('compare.html', 'compare', [('PART 1 · 3막', 'PART 4 · 신문물')])
    rw('act.html', 'act', [('PART 2 · 06', 'CLOSING · 01')])
    rw('closing.html', 'closing', [
        ('도구보다 일하는 방식,\n그 변화는 리더에게서 시작됩니다', '폰 하나로 오늘부터,\n확인은 사람이 — 변화는 리더부터'),
        ('말로 만든 업무 도구', '폰으로 묻고, 찍고, 말하기'),
        ('>알아보기<', '>만들기<'), ('대답하는 AI에서 일하는 AI로', '말로 만드는 업무 도구'),
        ('>바꾸기<', '>지키기<'), ('제도 · 기관장 · 현장의 변화', '보안 · 확인 · 결과물 보는 법'),
    ])
    shutil.copy(web, os.path.join(QR, 'qr_card.png'))
    rw('qna.html', 'qna', [('QR을 찍으면 수상작·강의 자료로 바로 연결됩니다', 'QR을 찍으면 강사 웹 프로필 · 강의 자료로 연결됩니다'),
        ('<img src="qr_card.png" style="width:100%;height:100%"/>',
         '<div style="width:100%;height:100%;border-radius:29px;background:#1d1a19;border:1.5px solid #3a3533;display:flex;align-items:center;gap:44px;padding:0 44px">'
         '<div style="flex:1"><div style="font-size:22px;font-weight:700;letter-spacing:.3em;color:#ff5a1f">AI 챔피언(BLACK)</div>'
         '<div style="font-size:72px;font-weight:900;letter-spacing:.06em;margin-top:14px">김경훈</div>'
         '<div style="font-size:26px;color:#a59f98;margin-top:18px;line-height:1.5">경남소방본부<br>ssca1612.pages.dev</div></div>'
         '<div style="flex:none;width:360px;height:360px;background:#f4f4f2;border-radius:22px;padding:16px"><img src="qr_card.png" style="width:100%;height:100%;image-rendering:pixelated"/></div></div>')],
       assets=[os.path.join(QR, 'qr_card.png')])


if __name__ == '__main__':
    web = build_all()
    reuse(web)
    json.dump(SCENES, open(os.path.join(OUT, 'scenes.json'), 'w'), ensure_ascii=False)
    print(len(SCENES), 'scenes →', OUT)
