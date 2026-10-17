import subprocess
P='../op2/p119.mp4';S2='../op2/slide2.mp4'
segs=[('black',None,0,3),('v',P,5.5,4),('v',P,16.0,3),('v',P,25.0,4),('v',P,35.5,4),('img','sat.png',0,3),('img','s4_66.jpg',0,1.5),('v',P,53.5,4.5),('v',S2,39.0,4),('v',S2,51.0,3),('v',S2,55.5,3),('v',P,61.0,8)]
inputs=[];fil=[];k=0
for i,(t,src,ss,d) in enumerate(segs):
    if t=='black':
        fil.append(f'color=black:s=1920x1080:r=30:d={d}[s{i}]')
    elif t=='v':
        inputs+=['-ss',str(ss),'-t',str(d),'-i',src]
        fil.append(f'[{k}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,trim=duration={d},setpts=PTS-STARTPTS[s{i}]');k+=1
    else:
        inputs+=['-loop','1','-t',str(d),'-i',src]
        n=int(d*30)
        fil.append(f'[{k}:v]scale=3840:-2,crop=3840:2160,zoompan=z=\'1+0.0015*on\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s=1920x1080:fps=30,setsar=1,trim=duration={d}[s{i}]');k+=1
fil.append(''.join(f'[s{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=1:a=0[base]')
inputs+=['-framerate','30','-i','o_v1_full/%04d.png'];ov=k
fil.append(f'[base][{ov}:v]overlay=0:0:format=auto,format=yuv420p[v]')
# audio: siren 0-14 fading, drone, kicks
siren="aevalsrc='0.25*sin(2*PI*(750*t-240/(2*PI*0.45)*cos(2*PI*0.45*t)))*min(t/3,1)*if(lt(t,12),1,max(0,(14-t)/2))':s=48000:d=45"
drone="aevalsrc='0.12*sin(2*PI*55*t)+0.06*sin(2*PI*82.5*t)':s=48000:d=45"
kick="aevalsrc='0.9*sin(2*PI*55*t)*(exp(-8*max(0,t-10.2))*gte(t,10.2)+exp(-8*max(0,t-22.7))*gte(t,22.7)+exp(-8*max(0,t-34.2))*gte(t,34.2))':s=48000:d=45"
cmd=['ffmpeg','-v','error','-y']+inputs+['-f','lavfi','-i',siren,'-f','lavfi','-i',drone,'-f','lavfi','-i',kick]
a=ov+1
fil.append(f'[{a}:a][{a+1}:a][{a+2}:a]amix=inputs=3:normalize=0,afade=t=out:st=43.5:d=1.5,volume=0.8[a]')
cmd+=['-filter_complex',';'.join(fil),'-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','45','v1_draft.mp4']
subprocess.run(cmd,check=True);print('ok')
