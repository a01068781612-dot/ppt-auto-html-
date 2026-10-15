import subprocess
V='../vid/';S2='../op2/slide2.mp4'
ENC=['-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','-an']
def run(a):subprocess.run(['ffmpeg','-v','error','-y']+a,check=True)
NAV=V+'nav.mp4';WEB=V+'web.mp4'
# 내비 알림: 검은 박스 안쪽만 잘라(둥근 모서리·흰 배경 제외) 회색 바탕을 완전 검정으로
CO="crop=940:156:70:2012,format=rgb24,curves=all='0/0 0.26/0 1/1',format=yuv420p,setsar=1"
def phone(name,ss,d,co=True,small=False,bw=None):
    pw,ph,px,py,mk=(352,760,300,60,'mask_s.png') if small else (416,900,260,90,'mask.png')
    cy=440 if small else 560
    f=f"[0:v]fps=30,split=3[a][b][c];[a]scale=1920:-2,crop=1920:1080,boxblur=30:3,eq=brightness=-0.32[bg];[b]scale={pw}:{ph},setsar=1[fg0];[fg0][1:v]alphamerge[fg];[bg][fg]overlay={px}:{py}[o1]"
    last='o1'
    if co:f+=f";[c]{CO}[co];[o1]drawbox=x=868:y={cy-90}:w=964:h=180:color=black:t=fill[o1b];[o1b][co]overlay=880:{cy-78}[o2]";last='o2'
    else:f+=";[c]nullsink"
    if bw:f+=f";[{last}]hue=s='min(1,max(0,(t-{bw[0]})/{bw[1]}))'[o3]";last='o3'
    run(['-ss',str(ss),'-t',str(d),'-i',NAV,'-loop','1','-i',mk,'-filter_complex',f,'-map',f'[{last}]','-t',str(d)]+ENC+[name])
def web(name,ss,d,mode='full',callout=None,k=1.6):
    if mode=='map':f="[0:v]fps=30,crop=1310:737:0:170,scale=1920:1080,setsar=1[o]"
    else:f="[0:v]fps=30,crop=1476:830:444:170,scale=1920:1080,setsar=1[o]"
    inputs=['-ss',str(ss),'-t',str(d),'-i',WEB];last='o'
    if callout:
        (x,y,w,h),mk,(ox,oy)=callout;W=int(w*k);H=int(h*k)
        f=f.replace('[o]','[ob]')+f";[ob]eq=brightness=-0.18[o];[0:v]crop={w}:{h}:{x}:{y},scale={W}:{H},setsar=1[c0];[c0][1:v]alphamerge[c];[o][c]overlay={ox}:{oy}[o2]";last='o2'
        inputs+=['-loop','1','-i',mk]
        f=f.replace("[0:v]fps=30,","[0:v]fps=30,split=2[s1][s2];[s1]",1).replace("[0:v]crop=","[s2]crop=")
    run(inputs+['-filter_complex',f,'-map',f'[{last}]','-t',str(d)]+ENC+[name])
CARD=((1320,190,580,265),'co_card.png',(110,300))
BLD=((1330,320,550,640),'co_bld.png',(100,60))
import sys
if 'all' in sys.argv:
    phone('E.mp4',4.0,4.5);phone('F.mp4',23,2.5);phone('G.mp4',34.5,2);phone('O.mp4',34.5,6,small=True,bw=(0,2))
# 주소 입력 줌인 → 검색 버튼 쪽으로 팬 → 클릭
Z="if(lt(in,78),2.53,if(lt(in,102),2.53-1.06*(1-cos(PI*(in-78)/24))/2,1.47))"
run(['-ss','5.8','-t','4.1','-i',WEB,'-vf',f"fps=30,zoompan=z='{Z}':x=12:y=168:d=1:s=1920x1080:fps=30,setsar=1",'-t','4.1']+ENC+['W1a.mp4'])
web('W1b.mp4',9.9,2.0)
web('W2.mp4',12.5,3.5,callout=CARD)
web('W3.mp4',22,3.5,'map')
web('W4a.mp4',34.5,2.0,'map')
web('W4b.mp4',39.5,2.5,'map')
web('W5.mp4',151,1.9)
run(['-ss','138','-t','4','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','4']+ENC+['K.mp4'])
run(['-ss','150','-t','3.5','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','3.5']+ENC+['L.mp4'])
run(['-ss','162','-t','2.5','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','2.5']+ENC+['M.mp4'])
# 행정안전부장관상 실제 사진: 전체 → 상장 쪽으로 천천히 줌
run(['-loop','1','-i','../drv/20260624_164009.jpg','-vf',"scale=4000:3000,crop=4000:2250:0:500,zoompan=z='1+0.35*on/90':x='(iw-iw/zoom)*0.95':y='(ih-ih/zoom)*0.55':d=90:s=1920x1080:fps=30,setsar=1",'-frames:v','90']+ENC+['AW.mp4'])
web('Q.mp4',140,3.5,callout=BLD,k=1.5)
order=['A','B','C','D','E','F','G','W1a','W1b','W2','W3','W4a','W4b','W5','K','L','M','AW','N','O','P','Q','R','S','T']
open('list3.txt','w').write(''.join(f"file '{c}.mp4'\n" for c in order))
run(['-f','concat','-safe','0','-i','list3.txt','-c','copy','base3.mp4'])
print('ok')
