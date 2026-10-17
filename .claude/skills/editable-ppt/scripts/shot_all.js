const { chromium } = require('playwright'); const path=require('path');
const [OUT, SPEC]=process.argv.slice(2); const jobs=[];
for (const part of SPEC.split(',')) { const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number); for (let n = a; n <= b; n++) jobs.push([n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`)]); }
(async()=>{const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'}); const pg=await br.newPage({viewport:{width:1920,height:1080}});
for(const [n,f] of jobs){ await pg.goto('file://'+f); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(80); await pg.screenshot({path:path.join(OUT,`s${String(n).padStart(3,'0')}.jpg`),type:'jpeg',quality:90}); }
await br.close(); console.log('shots',jobs.length);})();
