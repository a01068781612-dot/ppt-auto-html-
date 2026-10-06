# 제목 박스가 왼쪽 끝에 붙은 기사 캡처를 가운데로 옮김 (1.12배 확대 시 잘림 방지)
import json,re
from PIL import Image
CAP='/tmp/yt/cap2/'; s=880/1280
for t in json.load(open('topics.json')):
    if t['id'] not in ('n07','n08','n10'): continue
    d=t['id']; bx=t['box']; im=Image.open(CAP+t['cap']+'.png').convert('RGB')
    y0=max(0,min(bx[1]-200,im.size[1]-940))
    shift=round(640-(bx[0]+bx[2])/2)          # 원본 px 기준, 박스 가운데 → 화면 가운데
    can=Image.new('RGB',(1280,940),(255,255,255))
    can.paste(im.crop((0,y0,1280,y0+940)),(shift,0)); can.save(f'{d}/cap.jpg',quality=90)
    hx=(bx[0]+shift)*s; hy=(bx[1]-y0)*s; hw=(bx[2]-bx[0])*s; hh=(bx[3]-bx[1])*s
    h=open(f'{d}/index.html').read()
    h=re.sub(r'class="zoom" style="transform-origin:[^"]*"',f'class="zoom" style="transform-origin:{hx+hw/2:.0f}px {hy+hh/2:.0f}px"',h)
    h=re.sub(r'class="hl" style="left:[^;]*;',f'class="hl" style="left:{hx:.0f}px;',h)
    open(f'{d}/index.html','w').write(h)
    print(d,'shift',shift,'box after zoom',round(hx+hw/2-1.12*hw/2),round(hx+hw/2+1.12*hw/2))
