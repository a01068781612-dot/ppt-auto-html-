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
    stats = [["BLACK", "", "AI 챔피언 최고등급", "행정안전부 인증 · 영남 유일"], ["7", "건", "AI·데이터 분야 수상", "1위 4건 · 장관상(대상) 포함"], ["27", "곳", "출강·자문·협업 기관", "중앙부처 · 공공기관 · 대학"], ["ONLINE", "", "국가인재개발원 e러닝", "공무원 대상 AI 활용 과정"]]
    for i, (n, u, l1, l2) in enumerate(stats):
        x = R + i * sw; pad = 0 if i == 0 else 26
        num = f'<span class="cnt" data-to="{n}">{n}</span>' if n.isdigit() else n
        b.add('a p-st', f'left:{x:.0f}px;top:{sy}px;width:{sw:.0f}px;height:182px' + (';border-left:1px solid #3a3533' if i else ''),
              f'<div class="a" style="left:{pad}px;top:18px;white-space:nowrap"><span style="font-size:{64 if len(n) < 6 else 54}px;font-weight:900">{num}</span><span class="acc" style="font-size:28px;font-weight:700">{(" " + u) if u else ""}</span></div>'
              f'<div class="a" style="left:{pad}px;top:104px;font-size:22px;font-weight:700;white-space:nowrap">{l1}</div>'
              f'<div class="a cap" style="left:{pad}px;top:138px;font-size:18px;white-space:nowrap">{l2}</div>')
    b.add('a p-aw', f'left:{R}px;top:532px;font-size:34px;white-space:nowrap', '<b class="acc" style="font-size:24px">01&nbsp;&nbsp;</b><b>수상 내역&nbsp;&nbsp;</b><span class="dim" style="font-size:18px;letter-spacing:.3em">AWARDS</span>')
    aw = [["1위", "AI 재난 원패스(Disaster One-Pass)", "대상 · 행정안전부 장관상", "2026"], ["1위", "119원패스 AI 플랫폼 구축에 관한 연구", "경상남도 도지사 표창", "2026"], ["1위", "농촌 소방 AI 지능형 훈련 시스템", "최우수 · 소방청장상", "2025"], ["1위", "500m 격자별 소방력 최적화 배치 분석", "최우수 · KISTI 원장상", "2024"], ["3위", "AI 기반 소방 민원 답변 자동화", "장려 · 인사혁신처장상", "2025"], ["3위", "119 세이프 리스트", "우수상 · 소방 안전 빅데이터 활용", "2026"], ["3위", "기후재난 위험징후 분석·실시간 공유 서비스", "우수상 · 소방 안전 빅데이터 활용", "2025"]]
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
          'document.querySelectorAll(".cnt").forEach(e=>{tl.fromTo(e,{innerText:0},{innerText:+e.dataset.to,snap:{innerText:1},duration:1.2,ease:"power2.out"},1.1);});')
    write('prof1', 7, b, js, [PP + 'photo_col.jpg', PP + 'fade.png'])

# ───────────── 강사 소개 2 ─────────────
def prof2():
    b = B(7)
    L = 110; W = 1700
    b.add('ghost q-gh', 'left:1010px;top:44px;font-size:120px', 'Profile.')
    b.add('a q-tg acc', f'left:{L}px;top:92px;font-size:22px;font-weight:700;letter-spacing:.2em', 'NO.02 TEACHING · CERTIFICATES · PRESS')
    b.add('a q-t blk', f'left:{L}px;top:128px;font-size:64px', chars('직접 만들고, 직접 가르칩니다'))
    b.add('a q-w', 'right:110px;top:146px;text-align:right', '<div class="cap" style="font-size:24px">웹 프로필 · 수상작 자료</div><div style="font-size:30px;font-weight:700;margin-top:2px">ssca1612.pages.dev</div><div class="cap" style="font-size:20px;margin-top:4px">YouTube · Instagram @inside_ax</div>')
    b.add('hl q-l', f'left:{L}px;top:236px;width:{W}px')
    c1, c1w = L, 900; c2 = L + 970; c2w = W - 970
    b.add('a q-h1', f'left:{c1}px;top:262px;font-size:34px;white-space:nowrap', '<b class="acc" style="font-size:24px">02&nbsp;&nbsp;</b><b>강의와 위원 활동&nbsp;&nbsp;</b><span class="dim" style="font-size:18px;letter-spacing:.3em">TEACHING</span>')
    tch = [["ONLINE", "국가인재개발원 AI 활용 e러닝 강사", "인사혁신처 국가인재개발원"], ["2026", "경상남도 AI 활용 대표 강사", "내부강사 15명 중, AI 분야 최초"], ["27곳", "출강 · 자문 · 협업 기관", "국토교통부 · 법무부 · 경찰청 · 국세청 · LH · NIA · 충북도립대 외"], ["2026", "소방청 AI 인력풀 개발팀 합류", "바이브 코딩 · AI API 연동 · 업무자동화 직접 구현"], ["2026", "충북도립대학교 AI 융합 강의실 구축 평가위원장", "최연소 평가위원장"]]
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


prof1()
prof2()
print("ok")
