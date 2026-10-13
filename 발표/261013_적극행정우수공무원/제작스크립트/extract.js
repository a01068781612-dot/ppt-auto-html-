const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,D,HTML,OUT]=process.argv;const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+D+'/'+HTML);await p.waitForSelector('body[data-ready]');
const data=await p.evaluate(()=>{
 const ids=['s1','v1','s2','s3','v2','s4','s5','s6'];
 const col=c=>{const m=c&&c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const v=m[1].split(',').map(s=>parseFloat(s));const a=v.length>3?v[3]:1;if(a<=0.01)return null;
   const bl=v.slice(0,3).map(x=>Math.round(x*a+255*(1-a)));return bl.map(x=>x.toString(16).padStart(2,'0')).join('').toUpperCase();};
 const INL=new Set(['inline']);
 const out={};
 for(const id of ids){
  const S=document.getElementById(id);const sb=S.getBoundingClientRect();const items=[];
  const rel=r=>({x:r.left-sb.left,y:r.top-sb.top,w:r.width,h:r.height});
  const vis=e=>{const cs=getComputedStyle(e);return cs.display!=='none'&&cs.visibility!=='hidden'&&parseFloat(cs.opacity)>0.01};
  function runsOf(e,runs){for(const n of e.childNodes){
    if(n.nodeType===3){const t=n.nodeValue.replace(/\s+/g,' ');if(!t)continue;const cs=getComputedStyle(n.parentElement);
      let c=col(cs.color);const st=cs.webkitTextStrokeWidth&&parseFloat(cs.webkitTextStrokeWidth)>0?col(cs.webkitTextStrokeColor):null;let ghost=false;if(!c&&st){c=st;ghost=true}
      const rs=[];const r=document.createRange();r.selectNodeContents(n);for(const q of r.getClientRects())if(q.width>0)rs.push(q);
      runs.push({t,size:parseFloat(cs.fontSize),wt:parseInt(cs.fontWeight),c:c||'000000',ls:parseFloat(cs.letterSpacing)||0,lh:cs.lineHeight,rects:rs.map(rel),ghost});}
    else if(n.nodeType===1){if(n.tagName==='BR'){runs.push({br:true});continue}const cs=getComputedStyle(n);if(!vis(n))continue;
      if(INL.has(cs.display)&&!col(cs.backgroundColor)&&parseFloat(cs.borderTopWidth)===0)runsOf(n,runs);}}
   return runs;}
  function walk(e,isRoot){
   if(!vis(e))return;const cs=getComputedStyle(e);const r=rel(e.getBoundingClientRect());
   if(e.classList.contains('sq')){const s=r.w,T=Math.max(3,Math.round(0.06*s));
     items.push({k:'rect',x:r.x,y:r.y,w:s,h:T,fill:'111827'},{k:'rect',x:r.x,y:r.y,w:T,h:s,fill:'111827'},{k:'rect',x:r.x+s-T,y:r.y,w:T,h:s*.25,fill:'111827'},{k:'rect',x:r.x,y:r.y+s-T,w:s*.3,h:T,fill:'111827'});return;}
   if(e.tagName==='IMG'){items.push({k:'img',...r,src:e.getAttribute('src'),nw:e.naturalWidth,nh:e.naturalHeight,fit:cs.objectFit,pos:cs.objectPosition,rad:parseFloat(cs.borderTopLeftRadius)||0});return;}
   if(!isRoot){
    let fill=col(cs.backgroundColor);if(!fill&&cs.backgroundImage.includes('gradient')){const m=cs.backgroundImage.match(/rgba?\([^)]+\)/);if(m)fill=col(m[0]);}
    const bw=['Top','Right','Bottom','Left'].map(s=>cs['border'+s+'Style']!=='none'?parseFloat(cs['border'+s+'Width']):0);
    const bc=['Top','Right','Bottom','Left'].map(s=>col(cs['border'+s+'Color']));
    const all=bw.every(w=>w>0&&w===bw[0])&&bc.every(c=>c===bc[0]);
    const rad=parseFloat(cs.borderTopLeftRadius)||0;
    const cp=cs.clipPath;let shape=null;if(cp&&cp!=='none'){const l=cp.includes('6% 50%'),rr=cp.includes('100% 50%');shape=l&&rr?'chevron':rr?'homePlate':'notchL';}
    const sh=cs.boxShadow!=='none';
    if(fill||all){items.push({k:'shape',...r,fill,line:all?bc[0]:null,lw:all?bw[0]:0,dash:all&&cs.borderTopStyle==='dashed',rad,shape,shadow:sh,ellipse:rad>=Math.min(r.w,r.h)/2-0.5&&Math.abs(r.w-r.h)<1});}
    if(!all){const sd=[[0,r.x,r.y,r.w,bw[0]],[1,r.x+r.w-bw[1],r.y,bw[1],r.h],[2,r.x,r.y+r.h-bw[2],r.w,bw[2]],[3,r.x,r.y,bw[3],r.h]];
      for(const [i,x,y,w,h] of sd)if(bw[i]>0&&bc[i])items.push({k:'rect',x,y,w,h,fill:bc[i]});}
   }
   const boxed=!!col(cs.backgroundColor)||parseFloat(cs.borderTopWidth)>0;
   if(!INL.has(cs.display)||isRoot||boxed){const runs=runsOf(e,[]);const tr=runs.filter(x=>!x.br&&x.t.trim());
    if(tr.length){const rs=tr.flatMap(x=>x.rects);if(rs.length){
      const L=Math.min(...rs.map(q=>q.x)),T=Math.min(...rs.map(q=>q.y)),R=Math.max(...rs.map(q=>q.x+q.w)),B=Math.max(...rs.map(q=>q.y+q.h));
      const tops=[...new Set(rs.map(q=>Math.round(q.y/4)))].length;const brs=runs.filter(x=>x.br).length;
      let ta=cs.textAlign;if(ta==='start')ta='left';if(ta==='end')ta='right';
      if(cs.display.includes('flex')&&(cs.alignItems==='center'&&cs.flexDirection==='column'||cs.justifyContent==='center'&&cs.flexDirection!=='column'))ta=ta==='left'?'center':ta;
      // trim leading/trailing spaces
      items.push({k:'text',x:L,y:T,w:R-L,h:B-T,align:ta,lines:tops,brs,runs:runs.map(x=>x.br?{br:true}:{...x,rects:undefined}),lh:cs.lineHeight,fs:parseFloat(cs.fontSize)});}}}
   for(const c of e.children)walk(c,false);
  }
  const cs=getComputedStyle(S);
  walk(S,true);out[id]={bg:col(cs.backgroundColor)||'FFFFFF',items};
 }
 return out;});
fs.writeFileSync(OUT,JSON.stringify(data));for(const k in data)console.log(k,data[k].items.length);await b.close();})();
