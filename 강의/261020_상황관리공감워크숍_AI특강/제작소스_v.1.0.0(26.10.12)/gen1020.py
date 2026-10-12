# 정적 슬라이드 → HyperFrames 모션 (v.1.4.0)
# 각 장면은 build.js의 정적 슬라이드와 같은 배치(1920×1080 px)를 쓰고, 장면마다 다른 등장 효과를 준다.
import os, shutil, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(os.path.dirname(HERE))
BASE = SP + '/hf/p1cover/'
PP = SP + '/pptop/'
PROF = SP + '/deck_op2/assets/profile/'

CSS = '''@font-face{font-family:"Pretendard";src:url("PretendardVariable.woff2") format("woff2");font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden;background:#0c0b0b}
#root{width:100%;height:100%;position:relative;font-family:"Pretendard",sans-serif;color:#f4f4f2;background:#0c0b0b url(bg.png) center/cover no-repeat}
.a{position:absolute}
.acc{color:#ff5a1f}.cap{color:#a59f98}.dim{color:#8a847e}.body{color:#d6d2c9}
.ghost{position:absolute;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.13);font-weight:900;letter-spacing:-.04em;line-height:1;white-space:nowrap}
.blk{font-weight:900;letter-spacing:-.035em}
.tag{position:absolute;left:110px;top:92px;font-size:22px;letter-spacing:.12em;white-space:nowrap}
.tag b{color:#ff5a1f}.tag span{color:#8a847e}
.ttl{position:absolute;left:110px;top:130px;width:1640px;font-size:66px;font-weight:900;letter-spacing:-.03em;line-height:1.25;white-space:nowrap}
.hl{position:absolute;height:1px;background:#55504c;transform-origin:left}
.hl2{position:absolute;height:1px;background:#3a3533;transform-origin:left}
.vl{position:absolute;width:1px;background:#55504c;transform-origin:top}
.sq{position:absolute;border:3px solid #f4f4f2}
.card{position:absolute;background:#1d1a19;border:1.5px solid #3a3533;border-radius:29px}
.card.hi{background:#2a2523;border:4px solid #ff5a1f}
.mask{display:block;overflow:hidden}.mask>span{display:block}
.ch{display:inline-block;white-space:pre}
*{word-break:keep-all;overflow-wrap:break-word}
.cur{position:absolute;width:46px;height:46px;z-index:20}
.rip{position:absolute;width:90px;height:90px;border-radius:50%;border:4px solid #ff5a1f;z-index:19}
.flash{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#fff;opacity:0;z-index:30;pointer-events:none}
'''

def page(dur, body, js):
    return f'''<!doctype html><html lang="ko"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/><script src="gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{body}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{js}
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>'''

class B:
    """top-level clip elements"""
    def __init__(s, dur): s.dur = dur; s.items = []
    def add(s, cls, style, inner=''):
        i = len(s.items)
        s.items.append(f'<div class="{cls} clip" style="{style}" data-start="0" data-duration="{s.dur}" data-track-index="{i}">{inner}</div>')
    def html(s): return '\n'.join(s.items)

def chars(t):
    return ''.join(f'<span class="ch">{c}</span>' for c in t)

def write(name, dur, b, js, assets=()):
    d = os.path.join(HERE, name); os.makedirs(d, exist_ok=True)
    for f in ['gsap.min.js', 'PretendardVariable.woff2', 'hyperframes.json', 'meta.json', 'package.json']:
        if os.path.exists(BASE + f): shutil.copy(BASE + f, d)
    shutil.copy(PP + 'bg.png', d)
    for a in assets: shutil.copy(a, d)
    open(d + '/index.html', 'w').write(page(dur, b.html(), js))

def header(b, tag, sub, ghost, title_html, ghost_x=1180, ghost_w=640):
    b.add('tag t-tag', '', f'<b>{tag}  </b><span>{sub}</span>')
    b.add('ghost t-ghost', f'right:{1920-ghost_x-ghost_w}px;top:62px;font-size:110px;text-align:right', ghost)
    b.add('ttl t-ttl', '', title_html)
    b.add('hl t-hl', 'left:110px;top:244px;width:1700px')

HEAD_JS = {
 'mask': 'tl.from(".t-tag",{opacity:0,x:-30,duration:.5},0).from(".t-ttl .mask>span",{yPercent:105,duration:.8,ease:"power3.out"},.15).from(".t-ghost",{opacity:0,x:80,duration:1.1,ease:"power2.out"},.2).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
 'chars': 'tl.from(".t-tag",{opacity:0,y:-20,duration:.5},0).from(".t-ttl .ch",{opacity:0,y:40,rotationX:-80,duration:.5,stagger:.025,ease:"back.out(1.6)"},.1).from(".t-ghost",{opacity:0,duration:1.2},.3).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
 'blur': 'tl.from(".t-tag",{opacity:0,duration:.5},0).from(".t-ttl",{opacity:0,filter:"blur(14px)",scale:1.06,transformOrigin:"left center",duration:.9,ease:"power2.out"},.1).from(".t-ghost",{opacity:0,y:30,duration:1.1},.3).from(".t-hl",{scaleX:0,duration:.9,ease:"power2.inOut"},.4);',
}

# ───────────── 정리(Summary) ─────────────
SUMS = [
 dict(id='sum01', tag='AI 에이전트', title='프로그램에 두뇌가 생겼습니다', hi=1, points=["예전 프로그램은\n**시키는 대로만** 했습니다", "이제 AI가 **스스로\n생각하고 판단**합니다", "일을 나눠 맡은 AI가\n**에이전트**입니다"], key='시키는 프로그램에서, 생각하는 AI로', fx='flip', kfx='type', count=False, head='mask'),
 dict(id='sum02a', tag='AX', title='AI 도입과 AX는 다릅니다', hi=1, points=["AI 도입은\n**도구를 들이는 것**입니다", "AX는 **일의 흐름을\n다시 짜는 것**입니다", "**사람 중심 →\n에이전트 중심**으로 바뀝니다"], key='바꿀 것은 도구가 아니라 일하는 방식', fx='split', kfx='sweep', count=False, head='chars'),
 dict(id='sum03', tag='프롬프트 그다음', title='잘 쓰는 것에서, 맡기는 것으로', hi=1, points=["도구를 잘 써도\n**일은 그대로**였습니다", "**쉬지 않는 에이전트**가\n일을 바꿉니다", "출근하면 **할 일과\n회의 자료가 준비**됩니다"], key='잘 묻는 사람보다, 잘 맡기는 사람', fx='stack', kfx='pop', count=False, head='blur'),
 dict(id='sum04', tag='하네스', title='프롬프트 → 컨텍스트 → 하네스', hi=2, points=["프롬프트\n**자세히 말하기**", "컨텍스트\n**일의 이력 알려 주기**", "하네스\n**규칙과 실수 잡는 장치**"], key='AI가 틀 안에서 스스로 고치며 일하게', fx='flow', kfx='underline', count=False, head='mask'),
 dict(id='sum09', tag='① Hermes', title='Hermes — 쓸수록 나에게 맞춰지는 AI', hi=1, points=["서버에서\n**24시간** 일합니다", "해결한 방법을\n**스킬로 저장**합니다", "쓸수록\n**나에게 맞춰집니다**"], key='한 번 세팅하면, 결과만 받아 봅니다', fx='build', kfx='type', count=False, head='blur'),
 dict(id='sum06', tag='② Aside', title='Aside — 웹을 직접 움직이는 AI', hi=0, points=["AI가 **직접\n클릭·입력**합니다", "비밀번호는\n**AI가 보지 않습니다**", "작업 기록을\n**기억하고 개선**합니다", "**한국인 청년 3명**이\n만든 브라우저입니다"], key='보는 AI에서, 손을 움직이는 AI로', fx='cursor', kfx='sweep', count=False, head='blur'),
 dict(id='sum05', tag='③ Jev', title='Jev — 빠르게 고르는 AI', hi=1, points=["보기 중 하나를\n**0.1초**에 고릅니다", "챗GPT보다 **200배 빠르고\n400배 저렴**합니다", "깊은 판단은\n**아직 기존 AI**가 낫습니다"], key='빠르게 고르는 반복 업무에 맞습니다', fx='snap', kfx='pop', count=True, head='chars'),
 dict(id='sum07', tag='④ Muse', title='Muse — 생활을 대신하는 AI', hi=1, points=["출시 열흘 만에\n**앱스토어 1위**", "여행 부탁에\n**예약까지 직접** 끝냅니다", "비행기가 늦으면\n**일정도 다시 짭니다**"], key='말하는 AI에서, 일하는 AI로', fx='zoom', kfx='underline', count=False, head='mask'),
 dict(id='sum08', tag='⑤ Dots', title='Dots — 24시간 일하는 비서', hi=1, points=["노트북을 덮어도\n**계속 일합니다**", "급한 연락만\n**아침에 먼저** 알립니다", "AI가 **먼저 말을 거는**\n시대입니다"], key='물으면 답하는 AI에서, 알아서 하는 비서로', fx='wipe', kfx='type', count=False, head='chars'),
 dict(id='sum10', tag='그래서 우리는', title='도구보다, 일하는 방식', hi=1, points=["한 사람보다\n**조직의 방식**이 먼저", "변화는\n**리더부터** 시작합니다", "**직접 써 봐야**\n결과가 납니다"], key='→ PART 2  다른 기관은 이미 움직이고 있습니다', fx='spotlight', kfx='sweep', count=False, head='chars'),
]

CARD_FX = {
 'rise': 'tl.from(".cd",{opacity:0,y:90,duration:.8,stagger:.18,ease:"power3.out"},.7).from(".cd .num",{opacity:0,y:30,duration:.5,stagger:.18},1.0).from(".cd .ln",{scaleX:0,duration:.6,stagger:.18,ease:"power2.out"},1.1).from(".cd .pt",{opacity:0,y:16,duration:.5,stagger:.18},1.25);',
 'zoom': 'tl.from(".cd",{opacity:0,scale:.6,duration:.75,stagger:.15,ease:"back.out(1.5)"},.7).from(".cd .num",{opacity:0,scale:1.8,duration:.5,stagger:.15,ease:"power2.out"},1.0).from(".cd .ln",{scaleX:0,duration:.5,stagger:.15},1.15).from(".cd .pt",{opacity:0,x:-20,duration:.5,stagger:.15},1.25);',
 'wipe': 'tl.from(".cd",{clipPath:"inset(0 0 100% 0 round 29px)",duration:.9,stagger:.2,ease:"power3.inOut"},.7).from(".cd .num",{opacity:0,yPercent:60,duration:.6,stagger:.2},1.1).from(".cd .ln",{scaleX:0,duration:.6,stagger:.2},1.2).from(".cd .pt",{opacity:0,duration:.6,stagger:.2},1.35);',
 'flip': 'tl.from(".cd",{opacity:0,rotationX:-75,transformPerspective:2400,transformOrigin:"center top",duration:.9,stagger:.2,ease:"power3.out"},.7).from(".cd .num",{opacity:0,duration:.4,stagger:.2},1.1).from(".cd .ln",{scaleX:0,duration:.6,stagger:.2},1.15).from(".cd .pt",{opacity:0,y:14,duration:.5,stagger:.2},1.3);',
 'flow': 'tl.from(".cd",{opacity:0,x:-60,duration:.7,stagger:.45,ease:"power3.out"},.7).from(".arw",{opacity:0,scaleX:0,transformOrigin:"left center",duration:.35,stagger:.45,ease:"power2.out"},1.2).from(".cd .num",{opacity:0,duration:.4,stagger:.45},.95).from(".cd .ln",{scaleX:0,duration:.5,stagger:.45},1.0).from(".cd .pt",{opacity:0,y:14,duration:.45,stagger:.45},1.1);',
 'split': 'gsap.utils.toArray(".cd").forEach((c,i)=>tl.from(c,{opacity:0,x:(i%2?1:-1)*420,rotation:(i%2?1:-1)*4,duration:.85,ease:"power4.out"},.7+i*.16));tl.from(".cd .num",{opacity:0,scale:.4,duration:.5,stagger:.16,ease:"back.out(2.4)"},1.1).from(".cd .ln",{scaleX:0,duration:.5,stagger:.16},1.2).from(".cd .pt",{opacity:0,y:14,duration:.5,stagger:.16},1.3);',
 'stack': 'tl.from(".cd",{opacity:0,y:-620,duration:.9,stagger:.24,ease:"bounce.out"},.6).from(".cd .num",{opacity:0,duration:.4,stagger:.24},1.2).from(".cd .ln",{scaleX:0,duration:.5,stagger:.24},1.3).from(".cd .pt",{opacity:0,duration:.5,stagger:.24},1.4);',
 'build': 'tl.from(".cd",{scaleY:0,transformOrigin:"center bottom",duration:.75,stagger:.28,ease:"power3.out"},.7).from(".cd .num",{opacity:0,y:40,duration:.5,stagger:.28},1.1).from(".cd .ln",{scaleX:0,duration:.5,stagger:.28},1.2).from(".cd .pt",{opacity:0,y:14,duration:.5,stagger:.28},1.3);',
 'snap': 'tl.to(".flash",{opacity:.35,duration:.06},.68).to(".flash",{opacity:0,duration:.35},.74).from(".cd",{opacity:0,x:160,skewX:-14,duration:.3,stagger:.12,ease:"power4.out"},.7).from(".cd .num",{opacity:0,x:40,duration:.25,stagger:.12},.85).from(".cd .ln",{scaleX:0,duration:.3,stagger:.12},.9).from(".cd .pt",{opacity:0,duration:.3,stagger:.12},.95).to(".cd",{x:"+=6",duration:.05,repeat:5,yoyo:true},1.3);',
 'spotlight': 'tl.from(".cd",{opacity:0,y:40,duration:.6,stagger:.15},.7).to(".cd:not(.hi)",{opacity:.28,duration:.5},1.5).fromTo(".cd.hi",{scale:1},{scale:1.07,duration:.6,ease:"back.out(2)"},1.5).to(".cd:not(.hi)",{opacity:1,duration:.6},3.4).to(".cd.hi",{scale:1,duration:.5},3.4);',
 'cursor': '',
}

def cntwrap(p):
    return re.sub(r'(?<![\d.])(\d{2,})(?![\d.])', lambda m: f'<span class="cnt" data-to="{m.group(1)}">{m.group(1)}</span>', p)

def bold(t):
    return re.sub(r'\*\*(.+?)\*\*', lambda m: '<b style="color:#f4f4f2;font-weight:800">'+m.group(1)+'</b>', t, flags=re.S)

def summary(o):
    dur = 7
    b = B(dur)
    title = o['title']
    if o['head'] == 'chars': th = chars(title)
    elif o['head'] == 'mask': th = f'<span class="mask"><span>{title}</span></span>'
    else: th = title
    header(b, 'PART 1 · 정리', o['tag'], 'Summary.', th)
    n = len(o['points']); gap = 30; cw = (1700 - gap * (n - 1)) / n
    for i, p in enumerate(o['points']):
        x = 110 + i * (cw + gap); hi = o['hi'] == i
        fs = 34 if n > 3 else 40
        inner = (f'<div class="num a blk" style="left:40px;top:34px;font-size:100px;line-height:1.1;color:{"#ff5a1f" if hi else "#f4f4f2"}">{i+1:02d}</div>'
                 f'<div class="ln hl" style="left:40px;top:180px;width:{cw-80:.0f}px"></div>'
                 f'<div class="pt a" style="left:40px;top:204px;width:{cw-80:.0f}px;font-size:{fs}px;font-weight:500;color:#a59f98;line-height:1.3;white-space:pre-line">{bold(cntwrap(p) if o.get("count") else p)}</div>')
        b.add(f'card cd cd{i}' + (' hi' if hi else ''), f'left:{x:.0f}px;top:300px;width:{cw:.0f}px;height:470px', inner)
    if o['fx'] == 'flow':
        for i in range(n - 1):
            x = 110 + (i + 1) * (cw + gap) - gap
            b.add('a arw', f'left:{x-14:.0f}px;top:680px;width:58px;height:58px;border-radius:50%;background:#ff5a1f;color:#111;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center;z-index:5', '→')
    b.add('card kb', 'left:110px;top:810px;width:1700px;height:120px;border-radius:22px',
          (f'<div class="a kbar" style="left:0;top:0;width:100%;height:100%;border-radius:22px;background:linear-gradient(90deg,rgba(255,90,31,.30),rgba(255,90,31,0) 85%);transform-origin:left"></div>' if o.get('kfx')=='sweep' else '')
          + '<div class="a" style="left:40px;top:0;height:120px;display:flex;align-items:center;font-size:22px;font-weight:700;letter-spacing:.35em;color:#ff5a1f">KEY</div>'
          + f'<div class="a kt" style="left:180px;top:0;height:120px;width:1480px;display:flex;align-items:center;font-size:36px;font-weight:700;white-space:nowrap"><span class="kw" style="position:relative;display:inline-block">{o["key"]}' + ('<i class="kul" style="position:absolute;left:0;right:0;bottom:-8px;height:5px;background:#ff5a1f;transform-origin:left"></i>' if o.get('kfx')=='underline' else '') + '</span></div>')
    if o['fx'] == 'snap': b.add('flash', '')
    js = HEAD_JS[o['head']] + CARD_FX[o['fx']]
    if o['fx'] == 'cursor':
        b.add('cur', 'left:1780px;top:980px', '<svg viewBox="0 0 24 24" width="46" height="46"><path d="M3 2l7 19 2.6-7.4L20 11z" fill="#f4f4f2" stroke="#111" stroke-width="1.2"/></svg>')
        b.add('rip', 'left:0;top:0;opacity:0')
        js += 'tl.set(".cd",{opacity:0,scale:.86},0);'
        t = .8
        for i in range(n):
            cx = 110 + i * (cw + gap) + cw / 2; cy = 470
            js += f'tl.to(".cur",{{left:{cx:.0f},top:{cy},duration:.45,ease:"power2.inOut"}},{t:.2f}).fromTo(".rip",{{left:{cx-45:.0f},top:{cy-45},opacity:1,scale:.2}},{{opacity:0,scale:1.6,duration:.45}},{t+.45:.2f}).to(".cd:nth-of-type({i+1})",{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{t+.45:.2f});'
            t += .62
        js = js.replace('.cd:nth-of-type', '.cdx')
        for i in range(n): js = js.replace(f'.cdx({i+1})', f'.cd{i}', 1)
        js += f'tl.to(".cur",{{opacity:0,duration:.3}},{t:.2f});'
        t0 = t + .1
    else:
        t0 = 1.6 + (n - 1) * (0.45 if o['fx'] == 'flow' else (0.28 if o['fx'] in ('build', 'stack') else 0.2))
    if o.get('count'):
        js += 'document.querySelectorAll(".cnt").forEach(e=>{tl.fromTo(e,{innerText:0},{innerText:+e.dataset.to,snap:{innerText:1},duration:1.1,ease:"power2.out"},1.2);});'
    k = o.get('kfx', 'type')
    js += f'tl.from(".kb",{{opacity:0,y:40,duration:.6,ease:"power3.out"}},{t0:.2f})'
    js += {'type': f'.from(".kt",{{clipPath:"inset(0 100% 0 0)",duration:1.2,ease:"none"}},{t0+.35:.2f})',
           'sweep': f'.from(".kbar",{{scaleX:0,duration:1.0,ease:"power2.out"}},{t0+.3:.2f}).from(".kt",{{opacity:0,x:-30,duration:.6}},{t0+.5:.2f})',
           'pop': f'.from(".kt",{{opacity:0,scale:1.35,transformOrigin:"left center",duration:.6,ease:"back.out(2.2)"}},{t0+.35:.2f})',
           'underline': f'.from(".kt",{{opacity:0,y:16,duration:.5}},{t0+.3:.2f}).from(".kul",{{scaleX:0,duration:.8,ease:"power3.out"}},{t0+.8:.2f})'}[k]
    js += f'.to(".cd.hi",{{boxShadow:"0 0 0 10px rgba(255,90,31,.18), 0 30px 70px rgba(255,90,31,.25)",y:-10,duration:.6,ease:"power2.out"}},{t0+1.4:.2f});'
    write(o['id'], dur, b, js)

for o in SUMS: summary(o)

