import subprocess
src1=open('segs.py').read().split("black('A.mp4'")[0]
src3=open('segs3.py').read()
src3=src3.split("import sys")[0]  # defs + CO 정의까지
exec(src1); exec(src3)
# 음성 길이에 맞춘 새 길이
still('C.mp4','share_ON.png',4.0,1.0,0.32,.5,.5,.80,.70)
phone('D.mp4',0,0.5,co=False)
run(['-ss','9.9','-t','1.5','-i',WEB,'-vf',"fps=30,crop=1476:830:444:170,scale=1920:1080,setsar=1",'-t','1.5']+ENC+['W1b.mp4'])
web('W2.mp4',12.5,7.0,callout=CARD)
web('W3.mp4',22,4.0,'map')
web('W4a.mp4',34.5,2.0,'map')
web('W4b.mp4',39.5,2.7,'map')
web('W5.mp4',151,4.0)
run(['-ss','138','-t','3.5','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','3.5']+ENC+['K.mp4'])
run(['-ss','150','-t','3','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','3']+ENC+['L.mp4'])
run(['-ss','162','-t','2','-i',S2,'-vf','fps=30,scale=1920:1080,setsar=1','-t','2']+ENC+['M.mp4'])
run(['-loop','1','-i','../drv/20260624_164009.jpg','-vf',"scale=4000:3000,crop=4000:2250:0:500,zoompan=z='1+0.35*on/132':x='(iw-iw/zoom)*0.95':y='(ih-ih/zoom)*0.55':d=132:s=1920x1080:fps=30,setsar=1",'-frames:v','132']+ENC+['AW.mp4'])
order=['A','B','C','D','E','F','G','W1a','W1b','W2','W3','W4a','W4b','W5','K','L','M','AW','N','O','P','Q','R','S','T']
open('list4.txt','w').write(''.join(f"file '{c}.mp4'\n" for c in order))
run(['-f','concat','-safe','0','-i','list4.txt','-c','copy','base4.mp4'])
print('ok')
