// 분해판 보조 — 외곽선 글자(.ghost · -webkit-text-stroke, 예: 오른쪽 위 "Data." · 120장 "Thank you.")를 글상자로 넣기 위해 줄 · 위치 · 크기 · 선 두께를 뽑는다.
// 사용: NODE_PATH=/opt/node22/lib/node_modules node ghost_extract.js <OUT.json> <장:폴더,...> [<장:파일,...>]
//   예) node ghost_extract.js gh.json "1-40:p2/g1,41-86:p2/h2,87-120:p2/h3" "2:wsh/v002.html,4:wsh/v004.html,5:wsh/v005.html"
//   결과: {장: [{ex, ey, x, y, w, h, pitch, align, sw, sc, lines:[[{text, fs, fw, ls, color, it}]]}]} — ex · ey는 split_extract의 raster 자리(맞춰 바꿀 때 씀)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [OUT, SPEC, ONE] = process.argv.slice(2);
const jobs = new Map();
for (const part of SPEC.split(',')) {
  const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number);
  for (let n = a; n <= b; n++) jobs.set(n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`));
}
for (const part of (ONE || '').split(',').filter(Boolean)) { const [n, f] = part.split(':'); jobs.set(+n, path.resolve(f)); }

function grab() {
  const R = document.getElementById('r'), res = [];
  for (const el of R.querySelectorAll('*')) {
    if (el.closest('svg')) continue;
    const cs = getComputedStyle(el), sw = parseFloat(cs.webkitTextStrokeWidth) || 0;
    if (!(el.classList.contains('ghost') || sw > 0) || !el.textContent.trim()) continue;
    if (el.parentElement.closest('.ghost')) continue;
    const q = el.getBoundingClientRect(), lines = []; let cur = null, L = 1e9, T = 1e9, Rr = -1e9, B = -1e9;
    const st = { fs: parseFloat(cs.fontSize), fw: +cs.fontWeight, ls: parseFloat(cs.letterSpacing) || 0, it: cs.fontStyle === 'italic', color: 'rgba(0, 0, 0, 0)' };
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), rg = document.createRange();
    for (let t; (t = tw.nextNode());) {
      const s = t.nodeValue;
      for (let i = 0; i < s.length; i++) {
        rg.setStart(t, i); rg.setEnd(t, i + 1);
        const rc = [...rg.getClientRects()].filter(r => r.width > 0 || r.height > 0)[0]; if (!rc) continue;
        const ch = /\s/.test(s[i]) ? ' ' : s[i];
        if (!cur || rc.top > cur.bottom - (cur.bottom - cur.top) * 0.3) { cur = { text: '', top: rc.top, bottom: rc.bottom }; lines.push(cur); }
        if (ch !== ' ' || cur.text) cur.text += ch;
        cur.bottom = Math.max(cur.bottom, rc.bottom);
        if (ch !== ' ') { L = Math.min(L, rc.left); Rr = Math.max(Rr, rc.right); T = Math.min(T, rc.top); B = Math.max(B, rc.bottom); }
      }
    }
    const ls = lines.map(l => ({ ...l, text: l.text.replace(/\s+$/, '') })).filter(l => l.text);
    if (!ls.length) continue;
    const pitch = ls.length > 1 ? (ls[ls.length - 1].top - ls[0].top) / (ls.length - 1) : (parseFloat(cs.lineHeight) || st.fs * 1.25);
    res.push({ ex: q.left, ey: q.top, x: L, y: T, w: Rr - L, h: B - T, pitch, align: cs.textAlign, sw: sw || 1.5, sc: sw ? cs.webkitTextStrokeColor : 'rgba(255, 255, 255, 0.13)', lines: ls.map(l => [{ ...st, text: l.text }]) });
  }
  return res;
}

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } }); const out = {}; let k = 0;
  for (const [n, f] of [...jobs].sort((a, b) => a[0] - b[0])) {
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready.then(() => 1)); await pg.waitForTimeout(150);
    const g = await pg.evaluate(grab); if (g.length) { out[n] = g; k += g.length; }
  }
  fs.writeFileSync(OUT, JSON.stringify(out)); await br.close(); console.log('ok slides', Object.keys(out).length, 'boxes', k);
})();
