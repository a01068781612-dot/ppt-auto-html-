// 원본 장면 HTML의 글자와 PPT 글상자 글자가 장마다 똑같은지 대조(빠진 글자 · 남는 글자 0이어야 함).
// 사용: NODE_PATH=/opt/node22/lib/node_modules node check_text.js <OUT.pptx 풀어 둔 것 말고 pptx 파일> "<장:폴더,...>" [건너뛸 장,...]
//   예) node check_text.js out/c.pptx "1-40:fit/g1,41-86:fit/h2,87-120:fit/h3" "3,62,70,119"
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const [PPTX, SPEC, SKIP] = process.argv.slice(2); const skip = new Set((SKIP || '').split(',').filter(Boolean).map(Number)); const jobs = [];
for (const part of SPEC.split(',')) { const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number); for (let n = a; n <= (b || a); n++) jobs.push([n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`)]); }
const count = s => { const m = new Map(); for (const c of s) if (!/\s/.test(c)) m.set(c, (m.get(c) || 0) + 1); return m; };
const diff = (a, b) => { let o = ''; for (const [c, k] of a) if ((b.get(c) || 0) < k) o += c.repeat(k - (b.get(c) || 0)); return o; };
(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } }); let bad = 0;
  for (const [n, f] of jobs) {
    if (skip.has(n)) continue;
    await pg.goto('file://' + f); await pg.waitForTimeout(80);
    const src = await pg.evaluate(() => { const R = document.getElementById('r') || document.body; let s = ''; const tw = document.createTreeWalker(R, NodeFilter.SHOW_TEXT);
      for (let t; (t = tw.nextNode());) { const e = t.parentElement; if (e.closest('svg,script,style')) continue; const z = getComputedStyle(e); if (z.visibility === 'hidden' || z.opacity === '0' || z.display === 'none') continue;
        const r = e.getBoundingClientRect(); if (r.right < 0 || r.left > 1920 || r.bottom < 0 || r.top > 1080) continue; s += t.nodeValue; } return s; });
    const x = execSync(`unzip -p "${PPTX}" ppt/slides/slide${n}.xml`).toString('utf8'); let txt = '';
    for (const sp of x.match(/<p:sp>[\s\S]*?<\/p:sp>/g) || []) { const off = sp.match(/<a:off x="(-?\d+)"/); if (off && +off[1] >= 12192000) continue;   // 화면 밖 제목 상자 제외
      for (const m of sp.matchAll(/<a:t>([^<]*)<\/a:t>/g)) txt += m[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&amp;/g, '&'); }
    const a = count(src), b = count(txt), miss = diff(a, b), extra = diff(b, a);
    if (miss || extra) { bad++; console.log(n, '빠짐:', miss.slice(0, 60), '| 남음:', extra.slice(0, 60)); }
  }
  await br.close(); console.log('글자 다른 장', bad);
})();
