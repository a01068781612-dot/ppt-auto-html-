const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const D=process.argv[2];const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:2});
await p.goto('file://'+D+'/p_A.html');await p.waitForSelector('body[data-ready]');
const boxes={};
for(const id of ['s1','v1','s2','s3','v2','s4','s5','s6']){
  const el=await p.$('#'+id);const sb=await el.boundingBox();
  boxes[id]=await p.$$eval('#'+id+' .need',(ns,sb)=>ns.map(n=>{const r=n.getBoundingClientRect();return{x:r.left-sb.x,y:r.top-sb.y,w:r.width,h:r.height,t:n.querySelector('div').innerText.replace(/\n/g,' '),s:n.querySelector('i').innerText}}),sb);
  await p.$$eval('#'+id+' .need',ns=>ns.forEach(n=>n.style.visibility='hidden'));
  await el.screenshot({path:D+'/ppt/'+id+'.png'});
}
fs.writeFileSync(D+'/ppt/boxes.json',JSON.stringify(boxes,null,1));await b.close();})();
