import subprocess,os
V='../vid/';S2='../op2/slide2.mp4'
ENC=['-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','-an']
def run(a):subprocess.run(['ffmpeg','-v','error','-y']+a,check=True)
NAV=V+'nav.mp4';WEB=V+'web.mp4'
def phone(name,ss,d,co=True,small=False,bw=None):
    pw,ph,px,py,mk=(352,760,300,60,'mask_s.png') if small else (416,900,260,90,'mask.png')
    cy=440 if small else 560
    f=f"[0:v]fps=30,split=3[a][b][c];[a]scale=1920:-2,crop=1920:1080,boxblur=30:3,eq=brightness=-0.32[bg];[b]scale={pw}:{ph},setsar=1[fg0];[fg0][1:v]alphamerge[fg];[bg][fg]overlay={px}:{py}[o1]"
    last='o1'
    if co:
        f+=f";[c]crop=1012:187:34:1995,scale=900:166,setsar=1[co0];[co0][2:v]alphamerge[co];[o1][co]overlay=880:{cy-83}[o2]";last='o2'
    else:f+=";[c]nullsink"
    if bw:f+=f";[{last}]hue=s='min(1,max(0,(t-{bw[0]})/{bw[1]}))'[o3]";last='o3'
    run(['-ss',str(ss),'-t',str(d),'-i',NAV,'-loop','1','-i',mk,'-loop','1','-i','co_nav.png','-filter_complex',f,'-map',f'[{last}]','-t',str(d)]+ENC+[name])
def web(name,ss,d,mode='full',callout=None):
    if mode=='map':f="[0:v]fps=30,crop=1310:737:0:170,scale=1920:1080,setsar=1[o]"
    else:f="[0:v]fps=30,crop=1476:830:444:170,scale=1920:1080,setsar=1[o]"
    inputs=['-ss',str(ss),'-t',str(d),'-i',WEB];last='o'
    if callout:
        (x,y,w,h),mk,(ox,oy)=callout;W=int(w*1.6);H=int(h*1.6)
        f=f.replace('[o]','[ob]')+f";[ob]eq=brightness=-0.18[o];[0:v]crop={w}:{h}:{x}:{y},scale={W}:{H},setsar=1[c0];[c0][1:v]alphamerge[c];[o][c]overlay={ox}:{oy}[o2]";last='o2'
        inputs+=['-loop','1','-i',mk]
        f=f.replace("[0:v]fps=30,","[0:v]fps=30,split=2[s1][s2];[s1]",1).replace("[0:v]crop=","[s2]crop=")
    run(inputs+['-filter_complex',f,'-map',f'[{last}]','-t',str(d)]+ENC+[name])
CARD=((1320,190,580,265),'co_card.png',(110,300))
BRIEF=((1320,470,580,380),'co_brief.png',(110,230))
phone('D.mp4',0,1.5,co=False)
phone('E.mp4',4.0,4.5)
phone('F.mp4',23,2.5)
phone('G.mp4',34.5,2)
web('W1.mp4',7.0,4.5)
web('W2.mp4',12.5,4.0,callout=CARD)
web('W3.mp4',22,4.5,'map')
web('W4.mp4',76,4.0,callout=BRIEF)
web('W5.mp4',151,2.5)
run(['-ss','138','-t','5','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','5']+ENC+['K.mp4'])
run(['-ss','150','-t','4','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','4']+ENC+['L.mp4'])
run(['-ss','162','-t','4','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','4']+ENC+['M.mp4'])
phone('O.mp4',34.5,6,small=True,bw=(0,2))
web('Q.mp4',12.5,3.5,callout=CARD)
order=['A','B','C','D','E','F','G','W1','W2','W3','W4','W5','K','L','M','N','O','P','Q','R','S','T']
# A,B,C,N,P,R,S,T exist from before; adjust P length 3.5 handled below
open('list2.txt','w').write(''.join(f"file '{c}.mp4'\n" for c in order))
run(['-f','concat','-safe','0','-i','list2.txt','-c','copy','base2.mp4'])
print('ok')
