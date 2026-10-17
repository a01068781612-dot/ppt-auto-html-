# 사각 장식을 제목 첫 글자에 걸치게 배치 (표지 방식: 사각형 위에 글자가 올라가 겹친 부분은 글자에 가려짐)
# 사용: python3 sqfix.py <index.html> <제목 클래스>
import re, sys

SQJS = r'''
(function(){
if(document.querySelector('.sqn')) tl.from('.sqn',{opacity:0,scale:.4,rotation:-45,duration:.6,ease:'back.out(1.8)'},0.5);
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
})();
'''

def fix(path, target, before=None):
    s = open(path).read()
    if 'data-sq=' in s:
        return
    m = re.search(r'<div class="[^"]*\bsq2?\b[^"]*"[^>]*></div>\n?', s)
    if m:
        sqtag = m.group(0).rstrip('\n'); s = s[:m.start()] + s[m.end():]
    else:
        sqtag = '<div class="sq sqn clip" data-start="0" data-duration="6" data-track-index="99"></div>'
    sqtag = sqtag.replace('<div ', f'<div data-sq=".{target}" ', 1)
    sqtag = re.sub(r' style="[^"]*"', '', sqtag)
    dur = re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', s)
    if dur: sqtag = re.sub(r'data-duration="[\d.]+"', f'data-duration="{dur.group(1)}"', sqtag)
    t = re.search(r'<div class="[^"]*\b' + re.escape(before or target) + r'\b[^"]*"', s)
    assert t, (path, target)
    s = s[:t.start()] + sqtag + '\n' + s[t.start():]
    if '.sq{' not in s and '.sq ' not in s:
        s = s.replace('</style>', '.sq{position:absolute;border:3px solid #f4f4f2}</style>', 1)
    s = s.replace('window.__timelines["main"]=tl;', 'window.__timelines["main"]=tl;' + SQJS, 1)
    s = s.replace('.sq2{left:80px;top:140px;width:70px;height:70px}', '')
    open(path, 'w').write(s)

if __name__ == '__main__':
    fix(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
