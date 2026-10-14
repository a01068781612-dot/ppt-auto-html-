const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');
(async()=>{const D=process.argv[2];const keys=process.argv.slice(3);const fps=30;
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+D+'/mo.html');await p.evaluate(()=>document.fonts.ready);
for(const k of keys){const dur=await p.evaluate(k=>SCENES[k].d,k);const dir=D+'/f_'+k;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 const n=Math.round(dur*fps);for(let i=0;i<n;i++){await p.evaluate(([k,t])=>draw(k,t),[k,i/fps]);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
 execSync(`ffmpeg -v error -y -framerate ${fps} -i ${dir}/%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 ${D}/${k}.mp4`);console.log('done',k,n);}
await b.close();})();
