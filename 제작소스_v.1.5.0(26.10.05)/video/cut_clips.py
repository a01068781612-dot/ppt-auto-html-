import subprocess,glob,json
F={i:glob.glob(f'out/{i:02d}.*')[0] for i in range(1,11)}
CL={'01':(1,[(12.4,164.4)]),'02a':(2,[(50.0,162.3)]),'02b':(2,[(272.6,377.8)]),'03':(3,[(0.0,112.0)]),'04':(4,[(93.4,330.5)]),
    '05':(5,[(0.0,218.7)]),'06':(6,[(0.0,51.2),(169.4,334.8),(477.8,514.6)]),'07':(7,[(0.0,264.2)]),'08':(8,[(0.0,54.0)]),'09':(9,[(44.0,216.4)]),'10':(10,[(353.6,432.2)])}
dur={}
for cid,(fi,segs) in CL.items():
    parts=[]
    for k,(a,b) in enumerate(segs):
        d=b-a; p=f'clips/_{cid}_{k}.mp4'
        if fi==8:
            vf=("[0:v]split[a][b];[a]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,boxblur=30:5,eq=brightness=-0.15[bg];"
                "[b]scale=-2:720[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p")
        else:
            vf="[0:v]scale=1280:720,format=yuv420p"
        vf+=f",fade=t=in:st=0:d=0.3,fade=t=out:st={d-0.5:.2f}:d=0.5[v]"
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-t',f'{d:.2f}','-i',F[fi],'-filter_complex',vf,'-map','[v]','-map','0:a:0',
            '-af',f'afade=t=in:st=0:d=0.3,afade=t=out:st={d-0.5:.2f}:d=0.5','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart',p],check=True)
        parts.append(p)
    out=f'clips/{cid}.mp4'
    if len(parts)==1: subprocess.run(['mv',parts[0],out])
    else:
        open('clips/list.txt','w').write(''.join(f"file '{p.split('/')[-1]}'\n" for p in parts))
        subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','clips/list.txt','-c','copy','-movflags','+faststart',out],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    dur[cid]=round(d,2)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','0.6','-i',out,'-frames:v','1',f'clips/{cid}.png'])
    print(cid,dur[cid],flush=True)
json.dump(dur,open('clips/dur.json','w'))
