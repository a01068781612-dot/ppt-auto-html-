const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const D=process.argv[2],k=process.argv[3];const fps=30;
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+D+'/mo.html');await p.evaluate(()=>document.fonts.ready);
const dur=await p.evaluate(k=>SCENES[k].d,k);const dir=D+'/o_'+k;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
const n=Math.round(dur*fps);for(let i=0;i<n;i++){await p.evaluate(([k,t])=>draw(k,t),[k,i/fps]);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`,omitBackground:true});}
console.log('done',n);await b.close();})();
