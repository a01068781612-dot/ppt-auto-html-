# 정적 슬라이드 → HyperFrames 모션 (v.1.4.0)
# 각 장면은 build.js의 정적 슬라이드와 같은 배치(1920×1080 px)를 쓰고, 장면마다 다른 등장 효과를 준다.
import os, shutil, json
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
 dict(id='sum01', tag='AI 에이전트', title='챗봇은 대답하고, 에이전트는 실행합니다', hi=1, points=["챗봇은 '대답',\n에이전트는 '실행'", "목표만 주면 순서를 스스로 짜고 도구를 쓴다", "사람은 시키는 사람에서 맡기고 확인하는 사람으로"], key='질문하는 AI에서, 일을 맡기는 AI로', fx='rise', head='mask'),
 dict(id='sum02a', tag='AX', title='AI 도입과 AX는 다릅니다', hi=1, points=["AI 도입 =\n도구(계정)를 나눠 주는 것", "AX =\n일하는 방식을 바꾸는 것", "계정만 준다고 조직이 바뀌지 않는다"], key='바꿔야 하는 것은 도구가 아니라 일하는 방식', fx='zoom', head='chars'),
 dict(id='sum03', tag='프롬프트 그다음', title='잘 묻는 것보다, 맡기는 구조', hi=2, points=["잘 묻는 기술(프롬프트)만으로는 한계", "하루 업무 전체를 AI에게 맡기는 사람이 나왔다", "차이는 '질문'이 아니라 '맡기는 구조'"], key='AI를 잘 쓰는 사람 = 일을 잘 나눠 맡기는 사람', fx='wipe', head='blur'),
 dict(id='sum04', tag='하네스', title='프롬프트 → 컨텍스트 → 하네스', hi=2, points=["프롬프트\n잘 묻기", "컨텍스트\n자료 주기", "하네스\n일할 환경 짜기"], key='에이전트 = 모델(말) + 하네스(마구) — 우리말로 매뉴얼 + 권한 + 결재선 + 점검', fx='flow', head='mask'),
 dict(id='sum09', tag='① Hermes', title='Hermes — 쓸수록 똑똑해지는 AI', hi=0, points=["일한 방법을 '스킬'로 저장 — 쓸수록 똑똑해진다", "어제 일을 기억하고 이어서 시작", "매일 반복하는 정리·보고·자료 수집에"], key='천재를 사 오지 말고, 직원을 키운다', fx='flip', head='blur'),
 dict(id='sum06', tag='② Aside', title='Aside — 웹을 직접 움직이는 AI', hi=3, points=["로그인해 둔 사이트 안에서 AI가 직접 클릭·입력", "비밀번호는 Vault가 관리 — AI가 직접 보지 않음", "한 번 성공한 방법을 메모리로 기억하고 개선", "한국인 청년 3명이 만든 브라우저"], key='보는 AI에서, 직접 손을 움직이는 AI로', fx='rise', head='blur'),
 dict(id='sum05', tag='③ Jev', title='Jev — 빠르게 판단하는 AI', hi=1, points=["글을 쓰지 않고 보기 중에서 고르는 AI (+ 확신도)", "챗GPT보다 최대 200배 빠르고 400배 저렴", "메일·문의 분류, 우선순위 판단에"], key="사람의 '직감'처럼 빠르게 판단하는 AI", fx='flip', head='chars'),
 dict(id='sum07', tag='④ Muse', title='Muse — 생활을 대신하는 AI', hi=0, points=["앱을 닫아도 일하는 개인 비서", "여행·쇼핑·일정을 대화 한 번으로", "출시 12일 280만 다운로드, 앱스토어 1위"], key='하나씩 시키는 AI에서, 생활을 통째로 맡기는 AI로', fx='zoom', head='mask'),
 dict(id='sum08', tag='⑤ Dots', title='Dots — 24시간 일하는 직원', hi=2, points=["클라우드에 자기 컴퓨터 — 노트북을 덮어도 24시간", "먼저 말을 건다 — 밤새 온 연락 중 급한 것만 아침에", "Muse = 생활 비서\nDots = 업무 직원"], key='물어볼 때만 답하는 AI에서, 알아서 일하는 비서로', fx='wipe', head='chars'),
 dict(id='sum10', tag='그래서 우리는', title='도구보다, 일하는 방식', hi=1, points=["도구보다\n일하는 방식", "바꾸는 건\n리더부터", "직접 써 봐야\n보인다"], key='→ PART 3  다른 기관은 이미 움직이고 있습니다', fx='flow', head='chars'),
]

CARD_FX = {
 'rise': 'tl.from(".cd",{opacity:0,y:90,duration:.8,stagger:.18,ease:"power3.out"},.7).from(".cd .num",{opacity:0,y:30,duration:.5,stagger:.18},1.0).from(".cd .ln",{scaleX:0,duration:.6,stagger:.18,ease:"power2.out"},1.1).from(".cd .pt",{opacity:0,y:16,duration:.5,stagger:.18},1.25);',
 'zoom': 'tl.from(".cd",{opacity:0,scale:.6,duration:.75,stagger:.15,ease:"back.out(1.5)"},.7).from(".cd .num",{opacity:0,scale:1.8,duration:.5,stagger:.15,ease:"power2.out"},1.0).from(".cd .ln",{scaleX:0,duration:.5,stagger:.15},1.15).from(".cd .pt",{opacity:0,x:-20,duration:.5,stagger:.15},1.25);',
 'wipe': 'tl.from(".cd",{clipPath:"inset(0 0 100% 0 round 29px)",duration:.9,stagger:.2,ease:"power3.inOut"},.7).from(".cd .num",{opacity:0,yPercent:60,duration:.6,stagger:.2},1.1).from(".cd .ln",{scaleX:0,duration:.6,stagger:.2},1.2).from(".cd .pt",{opacity:0,duration:.6,stagger:.2},1.35);',
 'flip': 'tl.from(".cd",{opacity:0,rotationX:-75,transformPerspective:2400,transformOrigin:"center top",duration:.9,stagger:.2,ease:"power3.out"},.7).from(".cd .num",{opacity:0,duration:.4,stagger:.2},1.1).from(".cd .ln",{scaleX:0,duration:.6,stagger:.2},1.15).from(".cd .pt",{opacity:0,y:14,duration:.5,stagger:.2},1.3);',
 'flow': 'tl.from(".cd",{opacity:0,x:-60,duration:.7,stagger:.45,ease:"power3.out"},.7).from(".arw",{opacity:0,scaleX:0,transformOrigin:"left center",duration:.35,stagger:.45,ease:"power2.out"},1.2).from(".cd .num",{opacity:0,duration:.4,stagger:.45},.95).from(".cd .ln",{scaleX:0,duration:.5,stagger:.45},1.0).from(".cd .pt",{opacity:0,y:14,duration:.45,stagger:.45},1.1);',
}

def summary(o):
    dur = 7
    b = B(dur)
    title = o['title']
    if o['head'] == 'chars': th = chars(title)
    elif o['head'] == 'mask': th = f'<span class="mask"><span>{title}</span></span>'
    else: th = title
    header(b, 'PART 2 · 정리', o['tag'], 'Summary.', th)
    n = len(o['points']); gap = 30; cw = (1700 - gap * (n - 1)) / n
    for i, p in enumerate(o['points']):
        x = 110 + i * (cw + gap); hi = o['hi'] == i
        fs = 34 if n > 3 else 40
        inner = (f'<div class="num a blk" style="left:40px;top:34px;font-size:100px;line-height:1.1;color:{"#ff5a1f" if hi else "#f4f4f2"}">{i+1:02d}</div>'
                 f'<div class="ln hl" style="left:40px;top:180px;width:{cw-80:.0f}px"></div>'
                 f'<div class="pt a" style="left:40px;top:204px;width:{cw-80:.0f}px;font-size:{fs}px;font-weight:700;line-height:1.3;white-space:pre-line">{p}</div>')
        b.add('card cd' + (' hi' if hi else ''), f'left:{x:.0f}px;top:300px;width:{cw:.0f}px;height:470px', inner)
    if o['fx'] == 'flow':
        for i in range(n - 1):
            x = 110 + (i + 1) * (cw + gap) - gap
            b.add('a arw', f'left:{x-14:.0f}px;top:680px;width:58px;height:58px;border-radius:50%;background:#ff5a1f;color:#111;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center;z-index:5', '→')
    b.add('card kb', 'left:110px;top:810px;width:1700px;height:120px;border-radius:22px',
          '<div class="a" style="left:40px;top:0;height:120px;display:flex;align-items:center;font-size:22px;font-weight:700;letter-spacing:.35em;color:#ff5a1f">KEY</div>'
          f'<div class="a kt" style="left:180px;top:0;height:120px;width:1480px;display:flex;align-items:center;font-size:36px;font-weight:700;white-space:nowrap">{o["key"]}</div>')
    js = HEAD_JS[o['head']] + CARD_FX[o['fx']]
    t0 = 1.6 + (n - 1) * (0.45 if o['fx'] == 'flow' else 0.2)
    js += f'tl.from(".kb",{{opacity:0,y:40,duration:.6,ease:"power3.out"}},{t0:.2f}).from(".kt",{{clipPath:"inset(0 100% 0 0)",duration:1.2,ease:"none"}},{t0+.35:.2f})'
    js += f'.to(".cd.hi",{{boxShadow:"0 0 0 10px rgba(255,90,31,.18), 0 30px 70px rgba(255,90,31,.25)",y:-10,duration:.6,ease:"power2.out"}},{t0+1.4:.2f});'
    write(o['id'], dur, b, js)

for o in SUMS: summary(o)

# ───────────── 9월 한 달 ─────────────
def sep():
    b = B(7)
    header(b, 'PART 2 · 1막', '올여름부터 지금까지, 시간 순서로', 'Now.', '<span class="mask"><span>공통점은 \'대답\'에서 <span class="acc">\'실행\'</span>으로</span></span>', 1280, 540)
    ev = [["7월", "Hermes", "오픈소스 에이전트 확산", "쓸수록 노하우가 쌓이는 AI"], ["9. 14", "Aside", "AI 브라우저 윈도우판 출시", "로그인한 사이트에서 AI가 직접 조작"], ["9. 15", "Jev", "TypeSafe AI 공개", "글 대신 '선택'으로 답하는 판단 AI"], ["9월", "Muse", "Meta 개인 AI 비서", "앱을 닫아도 일하는 생활 비서"], ["9. 29", "Dots", "OpenAI DevDay 공개", "클라우드에서 24시간 일하는 직원"]]
    cw = (1700 - 4 * 24) / 5
    b.add('a tline', 'left:110px;top:420px;width:1700px;height:2px;background:#ff5a1f;transform-origin:left')
    for i, (d, n, a, c) in enumerate(ev):
        x = 110 + i * (cw + 24); on = i == 4
        b.add('a dt', f'left:{x:.0f}px;top:296px;font-size:64px;line-height:1.2' + (';color:#ff5a1f' if on else ''), f'<span class="blk">{d}</span>')
        b.add('a dot' + (' on' if on else ''), f'left:{x:.0f}px;top:408px;width:24px;height:24px;border-radius:50%;border:3px solid #ff5a1f;background:{"#ff5a1f" if on else "#0c0b0b"}')
        b.add('card ec', f'left:{x:.0f}px;top:470px;width:{cw:.0f}px;height:440px;border-radius:26px',
              f'<div class="a blk" style="left:30px;top:24px;font-size:44px">{n}</div>'
              f'<div class="a cap" style="left:30px;top:100px;width:{cw-60:.0f}px;font-size:24px;line-height:1.2">{a}</div>'
              f'<div class="hl" style="left:30px;top:190px;width:{cw-60:.0f}px"></div>'
              f'<div class="a" style="left:30px;top:212px;width:{cw-60:.0f}px;font-size:30px;font-weight:700;line-height:1.3">{c}</div>')
    js = HEAD_JS['mask'] + ('tl.from(".tline",{scaleX:0,duration:1.6,ease:"power2.inOut"},.6)'
        '.from(".dot",{scale:0,duration:.4,stagger:.28,ease:"back.out(3)"},.8)'
        '.from(".dt",{opacity:0,y:-30,duration:.5,stagger:.28},.85)'
        '.from(".ec",{opacity:0,y:70,duration:.7,stagger:.28,ease:"power3.out"},1.0)'
        '.to(".dot.on",{scale:1.6,duration:.4,yoyo:true,repeat:3,ease:"sine.inOut"},3.2);')
    write('sep', 7, b, js)
sep()

# ───────────── 한눈에 보기 ─────────────
def compare():
    b = B(7)
    header(b, 'PART 2 · 3막', '한눈에 보기 · 시간 순서', 'Compare.', chars('다섯 가지 신문물, 우리 일에 빗대면'))
    cols = [300, 380, 520, 500]; xs = [110]
    for c in cols[:-1]: xs.append(xs[-1] + c)
    rows = [("Hermes", "Nous Research", "쓸수록 노하우가 쌓임", "인수인계가 쌓이는 직원"), ("Aside", "한국인 창업 3인", "로그인한 웹을 직접 조작", "시스템 입력 대행"), ("Jev", "TypeSafe AI", "빠르게 고르고 판단", "문의·민원 분류 담당"), ("Muse", "Meta", "생활을 대신하는 비서", "개인 비서"), ("Dots", "OpenAI", "24시간 일하는 직원", "야간에도 일하는 직원")]
    hdr = ''.join(f'<div class="a" style="left:{x-110+30}px;top:0;height:90px;display:flex;align-items:center;font-size:26px;font-weight:700;letter-spacing:.12em;color:#ff5a1f">{t}</div>' for x, t in zip(xs, ["이름", "만든 곳", "한 줄로", "우리 일에 빗대면"]))
    b.add('a th', 'left:110px;top:270px;width:1700px;height:90px;background:#151312;border:1.5px solid #3a3533', hdr)
    for r, row in enumerate(rows):
        last = r == 4; y = 360 + r * 124
        cells = ''
        for c, (x, t) in enumerate(zip(xs, row)):
            st = ['font-size:38px;font-weight:900', 'font-size:30px;color:#a59f98', 'font-size:30px', 'font-size:30px;font-weight:700'][c]
            if last and c in (0, 3): st += ';color:#ff5a1f'
            cells += f'<div class="a" style="left:{x-110+30}px;top:0;height:124px;display:flex;align-items:center;{st}">{t}</div>'
        cells += ''.join(f'<div class="a" style="left:{x-110}px;top:0;width:1.5px;height:124px;background:#3a3533"></div>' for x in xs[1:])
        b.add('a tr' + (' last' if last else ''), f'left:110px;top:{y}px;width:1700px;height:124px;background:#1d1a19;border:1.5px solid #3a3533;border-top:none;overflow:hidden',
              ('<div class="a sweep" style="left:0;top:0;width:100%;height:100%;background:linear-gradient(90deg,rgba(255,90,31,.22),rgba(255,90,31,0));transform-origin:left"></div>' if last else '') + cells)
    js = HEAD_JS['chars'] + ('tl.from(".th",{opacity:0,y:-20,duration:.5},.7)'
        '.from(".tr",{opacity:0,x:-80,duration:.6,stagger:.2,ease:"power3.out"},.9)'
        '.from(".sweep",{scaleX:0,duration:1.0,ease:"power2.out"},2.4)'
        '.from(".tr.last",{scale:1,duration:.01},2.4).to(".tr.last",{scale:1.02,duration:.4,yoyo:true,repeat:1,ease:"sine.inOut"},2.6);')
    write('compare', 7, b, js)
compare()

# ───────────── PART 1 END ─────────────
def p1end():
    b = B(6)
    b.add('a e-lb dim', 'left:150px;top:108px;font-size:22px;letter-spacing:.3em', 'PART 1 · END')
    b.add('hl e-hl', 'left:150px;top:170px;width:1660px')
    b.add('a e-gh blk', 'right:80px;top:236px;font-size:330px;line-height:1.1;color:#24211f', 'End.')
    b.add('sq e-sq', 'left:82px;top:346px;width:60px;height:60px')
    b.add('a e-p acc', 'left:150px;top:298px;font-size:34px;font-weight:700;letter-spacing:.3em', 'PART 1')
    b.add('a e-t blk', 'left:150px;top:364px;font-size:140px;line-height:1.0',
          '<span class="mask"><span>국토부 실습</span></span><span class="mask"><span>돌아보기</span></span>')
    b.add('a e-s', 'left:150px;top:745px;font-size:36px;color:#cbc5ba', '말로 만든 업무 도구 — 다음 날 바로 쓰는 AI')
    b.add('card e-nx', 'left:150px;top:850px;width:1660px;height:110px;border-radius:22px',
          '<div class="a dim" style="left:44px;top:0;height:110px;display:flex;align-items:center;font-size:22px;font-weight:700;letter-spacing:.35em">NEXT</div>'
          '<div class="a" style="left:204px;top:0;height:110px;display:flex;align-items:center;font-size:36px;font-weight:700"><span class="acc">PART 2&nbsp;&nbsp;</span>2026 AI 트렌드 — 대답하는 AI에서 일하는 AI로</div>'
          '<div class="a acc e-ar" style="right:36px;top:0;height:110px;display:flex;align-items:center;font-size:48px;font-weight:700">→</div>')
    js = ('tl.from(".e-lb",{opacity:0,duration:.5},0).from(".e-hl",{scaleX:0,duration:1,ease:"power2.inOut"},0)'
          '.from(".e-gh",{opacity:0,x:200,duration:1.4,ease:"power3.out"},.2)'
          '.from(".e-sq",{opacity:0,scale:.3,rotation:-90,duration:.7,ease:"back.out(1.8)"},.5)'
          '.from(".e-p",{opacity:0,x:-30,duration:.5},.5)'
          '.from(".e-t .mask>span",{yPercent:105,duration:.8,stagger:.15,ease:"power3.out"},.6)'
          '.from(".e-s",{opacity:0,y:20,duration:.6},1.3)'
          '.from(".e-nx",{clipPath:"inset(0 100% 0 0 round 22px)",duration:.9,ease:"power3.inOut"},1.8)'
          '.to(".e-ar",{x:14,duration:.4,yoyo:true,repeat:5,ease:"sine.inOut"},2.7);')
    write('p1end', 6, b, js)
p1end()

# ───────────── 국무회의 영상 소개 ─────────────
def vintro():
    b = B(7)
    b.add('a v-dt', 'left:110px;top:148px;font-size:22px;letter-spacing:.2em', '<b class="acc">2026. 8. 11 </b><span class="dim">· 제35회 국무회의</span>')
    b.add('a v-gh ghost', 'left:110px;top:240px;font-size:92px;line-height:1.05;white-space:pre-line;letter-spacing:-.035em', '국무회의에서\n나온 AI 이야기')
    b.add('a v-t blk', 'left:110px;top:200px;font-size:92px;line-height:1.05',
          '<span class="mask"><span>국무회의에서</span></span><span class="mask"><span>나온 AI 이야기</span></span>')
    b.add('a v-s body', 'left:110px;top:470px;font-size:28px', '"공무원이 직접 만드는 AI" — 과기정통부 · 행안부 보고')
    flow = [["01", "과기부총리", "범부처 국민 AI 서비스 혁신추진단"], ["02", "대통령", "\"공무원이 직접 만들어 성과 낸 경우는?\""], ["03", "과기부총리", "\"행안부가 AI 챔피언을 키우고 있다\""], ["04", "행정안전부 장관", "\"최고급 개발 실력 · 블랙 등급 18명\""]]
    b.add('hl v-l0', 'left:110px;top:548px;width:760px')
    for i, (n, who, what) in enumerate(flow):
        y = 548 + i * 60
        b.add('a v-r', f'left:110px;top:{y}px;width:760px;height:60px;border-bottom:1px solid #3a3533',
              f'<div class="a acc" style="left:0;top:14px;font-size:20px;font-weight:700">{n}</div>'
              f'<div class="a" style="left:54px;top:10px;white-space:nowrap"><b style="font-size:25px">{who}&nbsp;&nbsp;</b><span class="cap" style="font-size:21px">{what}</span></div>')
    b.add('a v-pl', 'left:110px;top:892px;width:92px;height:92px;border-radius:50%;background:#ff5a1f',
          '<div class="a" style="left:36px;top:26px;border-left:30px solid #111;border-top:20px solid transparent;border-bottom:20px solid transparent"></div>')
    b.add('a v-nx', 'left:228px;top:900px', '<div style="font-size:28px;font-weight:700">다음 화면에서 전체화면으로 재생됩니다</div><div class="cap" style="font-size:22px;margin-top:8px">출처 JBN뉴스</div>')
    b.add('a v-fr', 'left:910px;top:150px;width:900px;height:780px;border:1.5px solid #55504c')
    b.add('sq v-sq', 'left:884px;top:124px;width:70px;height:70px')
    b.add('a v-im', 'left:932px;top:172px;width:856px;height:482px;overflow:hidden', '<img class="v-img" src="intro_poster.png" style="width:100%;height:100%;object-fit:cover"/>')
    b.add('a v-c1 cap', 'left:932px;top:680px;font-size:22px', '대통령 · 과기정통부 부총리 · 행정안전부 장관')
    b.add('a v-c2 body', 'left:932px;top:740px;width:856px;font-size:26px;line-height:1.35', "대통령 주재 국무회의에서 'AI를 직접 만드는 공무원'과 'AI 챔피언'이 어떻게 언급됐는지 보여 줍니다.")
    js = ('tl.from(".v-dt",{opacity:0,x:-30,duration:.5},0)'
          '.from(".v-t .mask>span",{yPercent:105,duration:.8,stagger:.15,ease:"power3.out"},.15)'
          '.from(".v-gh",{opacity:0,duration:1.2},.5)'
          '.from(".v-s",{opacity:0,y:20,duration:.5},.8)'
          '.from(".v-l0",{scaleX:0,duration:.6},.9)'
          '.from(".v-r",{opacity:0,x:-40,duration:.5,stagger:.22,ease:"power3.out"},1.0)'
          '.from(".v-fr",{clipPath:"inset(0 0 100% 0)",duration:1,ease:"power3.inOut"},.3)'
          '.from(".v-sq",{opacity:0,scale:.3,rotation:-90,duration:.7,ease:"back.out(1.8)"},.9)'
          '.from(".v-im",{opacity:0,y:40,duration:.8,ease:"power3.out"},.8)'
          '.fromTo(".v-img",{scale:1.15},{scale:1,duration:6,ease:"none"},.8)'
          '.from(".v-c1",{opacity:0,duration:.5},1.4).from(".v-c2",{opacity:0,y:16,duration:.6},1.6)'
          '.from(".v-pl",{scale:0,duration:.5,ease:"back.out(2)"},2.2).from(".v-nx",{opacity:0,x:-20,duration:.5},2.4)'
          '.to(".v-pl",{scale:1.12,duration:.45,yoyo:true,repeat:5,ease:"sine.inOut"},3.0);')
    write('vintro', 7, b, js, [PP + 'intro_poster.png'])
vintro()

# ───────────── 강사 소개 1 ─────────────
def prof1():
    b = B(7)
    b.add('a p-ph', 'left:0;top:0;width:600px;height:1080px;overflow:hidden', '<img class="p-img" src="photo_col.jpg" style="width:600px;height:1080px"/><img src="fade.png" style="position:absolute;left:0;top:0;width:600px;height:1080px"/>')
    b.add('a p-nm', 'left:70px;top:690px;font-size:110px;font-weight:900;letter-spacing:.12em', '김경훈')
    b.add('a p-en cap', 'left:70px;top:836px;font-size:20px;letter-spacing:.6em', 'KIM KYUNG HUN')
    b.add('a p-r1', 'left:70px;top:898px;font-size:30px;font-weight:700', '현직 공무원 <span class="acc">AI 강사</span>')
    b.add('a p-r2 cap', 'left:70px;top:946px;font-size:22px', '경남소방본부 소방교')
    R = 680; RW = 1920 - 100 - R
    b.add('a p-tg', f'left:{R}px;top:92px;font-size:22px;letter-spacing:.2em;white-space:nowrap', '<b class="acc">NO.01 PROFILE 2026 </b><span class="dim">· PUBLIC SECTOR AI</span>')
    b.add('a p-hd', f'left:{R}px;top:136px;width:{RW}px;font-size:44px;font-weight:700;line-height:1.2',
          '<span class="mask"><span>외부 강사가 아닌 현직 공무원이,</span></span><span class="mask"><span>공공의 보안 환경에 맞춘 <span class="acc">AI 활용·업무자동화</span>를 가르칩니다</span></span>')
    sy = 312; sw = RW / 4
    b.add('hl p-l1', f'left:{R}px;top:{sy}px;width:{RW}px'); b.add('hl p-l2', f'left:{R}px;top:{sy+182}px;width:{RW}px')
    stats = [["BLACK", "", "AI 챔피언 블랙 과정", "고급과정 선발 2026 · 영남 유일"], ["7", "건", "AI·데이터 분야 수상", "장관상 등 기관장상 4"], ["80", "명", "국토교통부 교육", "AI 활용·업무자동화 2일"], ["7", "곳", "출강 기관", "국가인재개발원 외"]]
    for i, (n, u, l1, l2) in enumerate(stats):
        x = R + i * sw; pad = 0 if i == 0 else 26
        num = f'<span class="cnt" data-to="{n}">{n}</span>' if n.isdigit() else n
        b.add('a p-st', f'left:{x:.0f}px;top:{sy}px;width:{sw:.0f}px;height:182px' + (';border-left:1px solid #3a3533' if i else ''),
              f'<div class="a" style="left:{pad}px;top:18px;white-space:nowrap"><span style="font-size:64px;font-weight:900">{num}</span><span class="acc" style="font-size:28px;font-weight:700">{(" " + u) if u else ""}</span></div>'
              f'<div class="a" style="left:{pad}px;top:104px;font-size:22px;font-weight:700;white-space:nowrap">{l1}</div>'
              f'<div class="a cap" style="left:{pad}px;top:138px;font-size:18px;white-space:nowrap">{l2}</div>')
    b.add('a p-aw', f'left:{R}px;top:532px;font-size:34px;white-space:nowrap', '<b class="acc" style="font-size:24px">01&nbsp;&nbsp;</b><b>수상 내역&nbsp;&nbsp;</b><span class="dim" style="font-size:18px;letter-spacing:.3em">AWARDS</span>')
    aw = [["1위", "AI 재난 원패스(Disaster One-Pass)", "대상 · 행정안전부 장관상", "2026"], ["1위", "119원패스 AI 플랫폼 구축에 관한 연구", "경상남도 도지사 표창", "2026"], ["1위", "농촌 소방 AI 지능형 훈련 시스템", "최우수 · 소방청장상", "2025"], ["1위", "500m 격자별 소방력 최적화 배치 분석", "최우수 · KISTI 원장상", "2024"], ["3위", "AI 기반 민원 답변 자동화", "장려 · 인사혁신처장상", "2025"], ["3위", "119 세이프 리스트", "우수상 · 소방 안전 빅데이터 활용", "2026"], ["3위", "기후재난 위험징후 분석·실시간 공유 서비스", "우수상 · 소방 안전 빅데이터 활용", "2025"]]
    b.add('hl p-al', f'left:{R}px;top:592px;width:{RW}px')
    for i, (rk, t, org, yr) in enumerate(aw):
        y = 592 + i * 58; g = rk == "1위"
        b.add('a p-row', f'left:{R}px;top:{y}px;width:{RW}px;height:58px;border-bottom:1px solid #3a3533',
              f'<div class="a rk" style="left:0;top:13px;width:64px;height:32px;border:2px solid {"#ff5a1f" if g else "#8a847e"};color:{"#ff5a1f" if g else "#f4f4f2"};font-size:17px;font-weight:700;display:flex;align-items:center;justify-content:center">{rk}</div>'
              f'<div class="a" style="left:86px;top:0;height:58px;display:flex;align-items:center;font-size:25px;font-weight:700;white-space:nowrap">{t}</div>'
              f'<div class="a cap" style="right:96px;top:0;height:58px;display:flex;align-items:center;font-size:21px;white-space:nowrap">{org}</div>'
              f'<div class="a body" style="right:0;top:0;height:58px;display:flex;align-items:center;font-size:21px;font-weight:700">{yr}</div>')
    js = ('tl.from(".p-ph",{clipPath:"inset(0 100% 0 0)",duration:1.1,ease:"power3.inOut"},0)'
          '.fromTo(".p-img",{scale:1.12},{scale:1,duration:6,ease:"none"},0)'
          '.from(".p-nm",{opacity:0,letterSpacing:"0.5em",duration:1.1,ease:"power3.out"},.6)'
          '.from(".p-en",{opacity:0,duration:.6},1.0).from(".p-r1",{opacity:0,y:20,duration:.5},1.1).from(".p-r2",{opacity:0,y:20,duration:.5},1.2)'
          '.from(".p-tg",{opacity:0,x:-30,duration:.5},.3)'
          '.from(".p-hd .mask>span",{yPercent:105,duration:.8,stagger:.15,ease:"power3.out"},.4)'
          '.from(".p-l1,.p-l2",{scaleX:0,duration:.8,ease:"power2.inOut"},.8)'
          '.from(".p-st",{opacity:0,y:30,duration:.6,stagger:.15,ease:"power3.out"},1.0)'
          '.from(".p-aw",{opacity:0,x:-30,duration:.5},1.7).from(".p-al",{scaleX:0,duration:.7},1.75)'
          '.from(".p-row",{opacity:0,x:60,duration:.5,stagger:.12,ease:"power3.out"},1.9)'
          '.from(".p-row .rk",{scale:0,duration:.4,stagger:.12,ease:"back.out(2.5)"},2.0);'
          'document.querySelectorAll(".cnt").forEach(e=>{const o={v:0},to=+e.dataset.to;tl.to(o,{v:to,duration:1.2,ease:"power2.out",onUpdate:()=>{e.textContent=Math.round(o.v)}},1.1);});')
    write('prof1', 7, b, js, [PP + 'photo_col.jpg', PP + 'fade.png'])
prof1()

# ───────────── 강사 소개 2 ─────────────
def prof2():
    b = B(7)
    L = 110; W = 1700
    b.add('ghost q-gh', 'left:1010px;top:44px;font-size:120px', 'Profile.')
    b.add('a q-tg acc', f'left:{L}px;top:92px;font-size:22px;font-weight:700;letter-spacing:.2em', 'NO.02 TEACHING · CERTIFICATES · PRESS')
    b.add('a q-t blk', f'left:{L}px;top:128px;font-size:64px', chars('직접 만들고, 직접 가르칩니다'))
    b.add('a q-w', 'right:110px;top:146px;text-align:right', '<div class="cap" style="font-size:24px">웹 프로필 · 수상작 자료</div><div style="font-size:30px;font-weight:700;margin-top:2px">ssca1612.pages.dev</div>')
    b.add('hl q-l', f'left:{L}px;top:236px;width:{W}px')
    c1, c1w = L, 900; c2 = L + 970; c2w = W - 970
    b.add('a q-h1', f'left:{c1}px;top:262px;font-size:34px;white-space:nowrap', '<b class="acc" style="font-size:24px">02&nbsp;&nbsp;</b><b>강의와 위원 활동&nbsp;&nbsp;</b><span class="dim" style="font-size:18px;letter-spacing:.3em">TEACHING</span>')
    tch = [["ONLINE", "국가인재개발원 AI 활용 e러닝 강사", "인사혁신처"], ["2026", "경상남도 AI 활용 대표 강사", "내부강사 15명 중, AI 분야 최초"], ["2026", "국토교통부 초청 AI 활용 및 업무자동화", "직원 약 80명, 2일"], ["2026", "소방기관 AI 활용·직장훈련 강의", "경남소방본부 · 경남·광주 소방학교 · 사천소방서"], ["2026", "충북도립대학교 AI 융합 강의실 구축 평가위원장", "최연소"]]
    b.add('hl q-tl', f'left:{c1}px;top:324px;width:{c1w}px')
    for i, (k, t, d) in enumerate(tch):
        y = 324 + i * 72
        b.add('a q-tr', f'left:{c1}px;top:{y}px;width:{c1w}px;height:72px;border-bottom:1px solid #3a3533',
              f'<div class="a acc" style="left:0;top:20px;font-size:22px;font-weight:700">{k}</div>'
              f'<div class="a" style="left:120px;top:8px;font-size:25px;font-weight:700;white-space:nowrap">{t}</div>'
              f'<div class="a cap" style="left:120px;top:42px;font-size:20px;white-space:nowrap">{d}</div>')
    b.add('a q-h2', f'left:{c2}px;top:262px;font-size:34px;white-space:nowrap', '<b class="acc" style="font-size:24px">03&nbsp;&nbsp;</b><b>자격&nbsp;&nbsp;</b><span class="dim" style="font-size:18px;letter-spacing:.3em">CERTIFICATES</span>')
    cert = [["DATA", "빅데이터분석기사 · 데이터분석준전문가(ADsP)"], ["COMPUTER", "컴퓨터활용능력 1급 · 워드프로세서 1급"], ["TEACHING", "교원자격증(수학) · 레크리에이션 강사 · 웃음치료사"], ["FIELD", "위험물 · 화학분석 · 드론 운용 · 1종 대형 · 지게차 · 한자 2급"]]
    b.add('hl q-cl', f'left:{c2}px;top:324px;width:{c2w}px')
    for i, (k, t) in enumerate(cert):
        y = 324 + i * 90
        b.add('a q-cr', f'left:{c2}px;top:{y}px;width:{c2w}px;height:90px;border-bottom:1px solid #3a3533',
              f'<div class="a dim" style="left:0;top:14px;font-size:16px;font-weight:700;letter-spacing:.4em">{k}</div>'
              f'<div class="a" style="left:0;top:42px;font-size:24px;font-weight:700;white-space:nowrap">{t}</div>')
    py = 724; pw = (W - 26 * 3) / 4.05; ph = 276
    press = [["press1.jpg", "김경훈 소방교, 소방청 AI 인력풀 개발팀 합류"], ["press3.jpg", "국토부 초청 AI 특강… 이틀간 80명 교육"], ["press5.jpg", "AI 기반 화재안전조사 대상 선별 시스템, 우수상"]]
    for i, (img, t) in enumerate(press):
        x = L + i * (pw + 26)
        b.add('a q-pc', f'left:{x:.0f}px;top:{py}px;width:{pw:.0f}px;height:{ph}px;background:#1d1a19;border:1.5px solid #3a3533;overflow:hidden',
              f'<div style="height:130px;overflow:hidden"><img class="q-pi" src="{img}" style="width:100%;height:130px;object-fit:cover"/></div>'
              f'<div class="acc" style="margin:18px 20px 0;font-size:15px;font-weight:700;letter-spacing:.25em">FPN DAILY</div>'
              f'<div style="margin:8px 20px 0;font-size:22px;font-weight:700;line-height:1.2">{t}</div>')
    wx = L + 3 * (pw + 26); ww = W - 3 * (pw + 26)
    b.add('a q-wl', f'left:{wx:.0f}px;top:{py}px;width:{ww:.0f}px;height:2px;background:#ff5a1f;transform-origin:left')
    why = [["보안 환경 그대로", "내부망·보안 규정 안에서"], ["공공 문서 양식 그대로", "보고서·PPT·민원"], ["검증된 업무자동화", "현업 검증 사례"], ["기관 맞춤 설계", "기관 업무·시스템 맞춤"]]
    for i, (a_, c) in enumerate(why):
        y = py + i * ph / 4
        b.add('a q-wy', f'left:{wx:.0f}px;top:{y:.0f}px;width:{ww:.0f}px;height:{ph/4:.0f}px;border-bottom:1px solid #3a3533',
              f'<div class="a" style="left:4px;top:0;height:100%;display:flex;align-items:center;font-size:22px;font-weight:700;white-space:nowrap">{a_}</div>'
              f'<div class="a cap" style="right:4px;top:0;height:100%;display:flex;align-items:center;font-size:17px;white-space:nowrap">{c}</div>')
    js = ('tl.from(".q-tg",{opacity:0,x:-30,duration:.5},0)'
          '.from(".q-t .ch",{opacity:0,y:40,duration:.45,stagger:.03,ease:"back.out(1.7)"},.1)'
          '.from(".q-gh",{opacity:0,x:80,duration:1.2},.3).from(".q-w",{opacity:0,x:30,duration:.6},.5)'
          '.from(".q-l",{scaleX:0,duration:.9,ease:"power2.inOut"},.5)'
          '.from(".q-h1,.q-h2",{opacity:0,y:20,duration:.5,stagger:.1},.8)'
          '.from(".q-tl,.q-cl",{scaleX:0,duration:.7},.9)'
          '.from(".q-tr",{opacity:0,x:-50,duration:.5,stagger:.12,ease:"power3.out"},1.0)'
          '.from(".q-cr",{opacity:0,x:50,duration:.5,stagger:.12,ease:"power3.out"},1.1)'
          '.from(".q-pc",{opacity:0,y:80,duration:.7,stagger:.18,ease:"power3.out"},1.8)'
          '.fromTo(".q-pi",{scale:1.25},{scale:1,duration:3,ease:"power2.out"},1.8)'
          '.from(".q-wl",{scaleX:0,duration:.6},2.3).from(".q-wy",{opacity:0,x:30,duration:.45,stagger:.12},2.4);')
    write('prof2', 7, b, js, [PROF + 'press1.jpg', PROF + 'press3.jpg', PROF + 'press5.jpg'])
prof2()

# ───────────── 마무리 ─────────────
def closing():
    b = B(7)
    b.add('a c-lb dim', 'left:150px;top:108px;font-size:22px;letter-spacing:.3em', 'CLOSING')
    b.add('hl c-hl', 'left:150px;top:170px;width:1620px')
    b.add('sq c-sq', 'left:82px;top:336px;width:60px;height:60px')
    b.add('a c-t blk', 'left:150px;top:350px;font-size:140px;line-height:1.05',
          '<span class="mask"><span>AI는 선택이 아닌</span></span><span class="mask"><span><span class="acc c-must" style="position:relative;display:inline-block">필수<i class="c-ul" style="position:absolute;left:0;right:0;bottom:6px;height:10px;background:#ff5a1f;transform-origin:left"></i></span>입니다</span></span>')
    b.add('a c-s', 'left:150px;top:760px;font-size:36px;color:#cbc5ba;line-height:1.3;white-space:pre-line', '도구보다 일하는 방식,\n그 변화는 리더에게서 시작됩니다')
    b.add('vl c-vl', 'left:1280px;top:300px;height:600px')
    recap = [["01", "써 보기", "말로 만든 업무 도구"], ["02", "알아보기", "대답하는 AI에서 일하는 AI로"], ["03", "바꾸기", "제도 · 기관장 · 현장의 변화"]]
    for i, (n, a_, c) in enumerate(recap):
        y = 300 + i * 200
        b.add('a c-rc', f'left:1340px;top:{y}px;width:470px;height:200px' + (';border-bottom:1px solid #3a3533' if i < 2 else ''),
              f'<div class="a acc" style="top:28px;font-size:28px;font-weight:700">{n}</div>'
              f'<div class="a blk" style="top:70px;font-size:46px">{a_}</div>'
              f'<div class="a cap" style="top:136px;font-size:24px">{c}</div>')
    js = ('tl.from(".c-lb",{opacity:0,duration:.5},0).from(".c-hl",{scaleX:0,duration:1,ease:"power2.inOut"},0)'
          '.from(".c-sq",{opacity:0,scale:.3,rotation:-90,duration:.7,ease:"back.out(1.8)"},.3)'
          '.from(".c-t .mask>span",{yPercent:105,duration:.9,stagger:.25,ease:"power3.out"},.4)'
          '.from(".c-ul",{scaleX:0,duration:.7,ease:"power3.out"},1.5)'
          '.fromTo(".c-must",{scale:1},{scale:1.08,transformOrigin:"left bottom",duration:.35,yoyo:true,repeat:1,ease:"sine.inOut"},1.6)'
          '.from(".c-s",{opacity:0,y:24,duration:.7},1.7)'
          '.from(".c-vl",{scaleY:0,duration:.9,ease:"power2.inOut"},1.0)'
          '.from(".c-rc",{opacity:0,x:60,duration:.6,stagger:.25,ease:"power3.out"},1.4);')
    write('closing', 7, b, js)
closing()

# ───────────── Q&A ─────────────
def qna():
    b = B(6)
    b.add('a z-q blk', 'left:110px;top:150px;font-size:230px;line-height:1.1', chars('Q&A'))
    b.add('a z-ty blk', 'left:110px;top:420px;font-size:110px;color:#2a2725', 'Thank you.')
    b.add('a z-s', 'left:110px;top:600px;font-size:36px;color:#cbc5ba', '궁금하신 점을 편하게 물어봐 주세요')
    b.add('hl z-l', 'left:110px;top:700px;width:760px')
    info = [["WEB", "ssca1612.pages.dev"], ["BLOG", "blog.naver.com/ai-sobang"], ["MAIL", "ssca1612@korea.kr"]]
    for i, (k, v) in enumerate(info):
        y = 700 + i * 76
        b.add('a z-r', f'left:110px;top:{y}px;width:760px;height:76px;border-bottom:1px solid #3a3533',
              f'<div class="a dim" style="left:0;top:24px;font-size:20px;font-weight:700;letter-spacing:.3em">{k}</div>'
              f'<div class="a" style="left:140px;top:16px;font-size:30px;font-weight:700">{v}</div>')
    b.add('a z-fr', 'left:960px;top:230px;width:850px;height:620px;border:1.5px solid #55504c')
    b.add('sq z-sq', 'left:936px;top:206px;width:70px;height:70px')
    b.add('a z-qr', 'left:990px;top:270px;width:790px;height:461px', '<img src="qr_card.png" style="width:100%;height:100%"/>')
    b.add('a z-c cap', 'left:990px;top:770px;width:790px;text-align:center;font-size:26px', 'QR을 찍으면 수상작·강의 자료로 바로 연결됩니다')
    js = ('tl.from(".z-q .ch",{opacity:0,y:-160,duration:.8,stagger:.15,ease:"bounce.out"},0)'
          '.from(".z-ty",{opacity:0,x:-120,duration:1.1,ease:"power3.out"},.6)'
          '.from(".z-s",{opacity:0,y:20,duration:.6},1.0)'
          '.from(".z-l",{scaleX:0,duration:.7},1.2).from(".z-r",{opacity:0,x:-40,duration:.5,stagger:.15},1.3)'
          '.from(".z-fr",{clipPath:"inset(100% 0 0 0)",duration:1,ease:"power3.inOut"},.3)'
          '.from(".z-sq",{opacity:0,scale:.3,rotation:-90,duration:.7,ease:"back.out(1.8)"},.9)'
          '.from(".z-qr",{opacity:0,rotationY:-90,transformPerspective:1600,duration:1,ease:"power3.out"},1.0)'
          '.from(".z-c",{opacity:0,duration:.6},1.8);')
    write('qna', 6, b, js, [PP + 'qr_card.png'])
qna()

json.dump(['vintro', 'prof1', 'prof2', 'p1end', 'sep'] + [o['id'] for o in SUMS] + ['compare', 'closing', 'qna'], open(os.path.join(HERE, 'list.json'), 'w'))
print('ok')
