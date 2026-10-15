import subprocess,os
V='../vid/';S2='../op2/slide2.mp4'
ENC=['-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','-an']
def run(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
def black(name,d):run(['-f','lavfi','-i',f'color=black:s=1920x1080:r=30:d={d}']+ENC+[name])
def phone(name,src,ss,d,callout=None,co_from=0,bw=None,cy=560):
    # callout=(x,y,w,h) crop in source
    f=f"[0:v]fps=30,split=3[a][b][c];[a]scale=1920:-2,crop=1920:1080,boxblur=30:3,eq=brightness=-0.32[bg];[b]scale=416:900,setsar=1[fg0];[fg0][1:v]alphamerge[fg];[bg][fg]overlay=260:90[o1]"
    last='o1'
    if callout:
        x,y,w,h=callout;W=900;H=int(h*W/w)
        f+=f";[c]crop={w}:{h}:{x}:{y},scale={W}:{H},setsar=1[co];[o1][co]overlay=880:{cy-H//2}:enable='gte(t,{co_from})'[o2]";last='o2'
    else:
        f+=";[c]nullsink"
    if bw: f+=f";[{last}]hue=s='min(1,max(0,(t-{bw[0]})/{bw[1]}))'[o3]";last='o3'
    run(['-ss',str(ss),'-t',str(d),'-i',src,'-loop','1','-i','mask.png','-filter_complex',f,'-map',f'[{last}]','-t',str(d)]+ENC+[name])
def crop(name,src,ss,d,box=None,bw=None,zoom=0):
    f="[0:v]fps=30"
    if box:x,y,w,h=box;f+=f",crop={w}:{h}:{x}:{y}"
    f+=",scale=1920:1080,setsar=1"
    if zoom:f+=f",scale=iw*1.08:-2,zoompan=z='1+{zoom}*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30"
    if bw=='gray':f+=",hue=s=0"
    elif bw:f+=f",hue=s='min(1,max(0,(t-{bw[0]})/{bw[1]}))'"
    run(['-ss',str(ss),'-t',str(d),'-i',src,'-vf',f.replace('[0:v]',''),'-t',str(d)]+ENC+[name])
def still(name,img,d,z0,z1,cx0,cy0,cx1,cy1,bw=None):
    # zoom from z0 to z1 (crop width fraction) and center move
    n=int(d*30)
    from PIL import Image
    im=Image.open(img).convert('RGB');W,H=im.size
    os.makedirs('tmp_'+name,exist_ok=True)
    for i in range(n):
        p=i/(n-1);e=p*p*(3-2*p)
        z=z0+(z1-z0)*e;cx=cx0+(cx1-cx0)*e;cy=cy0+(cy1-cy0)*e
        cw=W*z;ch=cw*9/16
        if ch>H:ch=H;cw=ch*16/9
        x=min(max(cx*W-cw/2,0),W-cw);y=min(max(cy*H-ch/2,0),H-ch)
        fr=im.crop((int(x),int(y),int(x+cw),int(y+ch))).resize((1920,1080),Image.LANCZOS)
        if bw:
            s=min(1,max(0,(i/30-bw[0])/bw[1]))
            g=fr.convert('L').convert('RGB');fr=Image.blend(g,fr,s)
        fr.save(f'tmp_{name}/{i:04d}.jpg',quality=92)
    run(['-framerate','30','-i',f'tmp_{name}/%04d.jpg']+ENC+[name])
NAV=V+'nav.mp4';PH=V+'phone.mp4'
NAVCO=(30,1990,1020,195);PHCO=(0,1250,1080,400)
black('A.mp4',3)
still('B.mp4','share_OFF.png',1.5,1.0,1.0,.5,.5,.5,.5)
still('C.mp4','share_ON.png',2.5,1.0,0.32,.5,.5,.80,.70)
phone('D.mp4',NAV,0,2)
phone('E.mp4',NAV,4.0,5,NAVCO,0.5)
phone('F.mp4',NAV,23,3,NAVCO)
phone('G.mp4',NAV,34.5,2,NAVCO)
phone('H.mp4',PH,3.5,6.5,PHCO,4.8,cy=640)
crop('I.mp4',V+'web.mp4',12,6,(0,190,1100,619))
crop('J.mp4',V+'gpts.mp4',32,4.5,(390,180,1180,664))
crop('K.mp4',S2,138,6)
crop('L.mp4',S2,150,5)
crop('M.mp4',S2,162,5)
black('N.mp4',1)
phone('O.mp4',NAV,34.5,5,NAVCO,0,(0,2))
still('P.mp4','../drv/INDEX_2025-08.jpg',3,1.0,1.0,.5,.15,.5,.45,(0,1.5))
phone('Q.mp4',PH,8.3,3,PHCO,cy=640)
crop('R.mp4',S2,39,2,None,'gray')
crop('S.mp4',S2,288,5,None,(0,1.2))
black('T.mp4',9)
open('list.txt','w').write(''.join(f"file '{c}.mp4'\n" for c in 'ABCDEFGHIJKLMNOPQRST'))
run(['-f','concat','-safe','0','-i','list.txt','-c','copy','base.mp4'])
print('ok')
