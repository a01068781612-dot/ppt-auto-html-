// 글자 수정판 1단계 — 장면 HTML에서 글자만 뽑고(위치 · 크기 · 색 · 굵기 · 줄바꿈), 글자를 지운 배경을 찍는다.
// 사용: NODE_PATH=/opt/node22/lib/node_modules node edit_extract.js <OUT> <장:폴더,...>
//   예) node edit_extract.js out "1-40:p2/g1,41-86:p2/h2,87-120:p2/h3"
//   결과: OUT/b###.jpg(글자 없는 배경) · OUT/t###.json(글상자 목록)
// 원칙: 화면 줄바꿈 그대로(브라우저가 나눈 줄마다 줄바꿈), 외곽선 글자(.ghost) · SVG 안 글자는 배경에 남김.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [OUT, SPEC] = process.argv.slice(2);
fs.mkdirSync(OUT, { recursive: true });
const jobs = [];
for (const part of SPEC.split(',')) {
  const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number);
  for (let n = a; n <= b; n++) jobs.push([n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`)]);
}

function grab() {
  const R = document.getElementById('r');
  const skip = el => !!el.closest('svg, .ghost');
  const blockOf = node => { let e = node.parentElement; while (e && e !== R && getComputedStyle(e).display === 'inline') e = e.parentElement; return e; };
  const groups = new Map();
  const tw = document.createTreeWalker(R, NodeFilter.SHOW_TEXT);
  for (let t; (t = tw.nextNode());) {
    if (!t.nodeValue.trim() || skip(t.parentElement)) continue;
    const cs = getComputedStyle(t.parentElement);
    if (cs.visibility === 'hidden' || cs.opacity === '0' || cs.color === 'rgba(0, 0, 0, 0)') continue;
    const b = blockOf(t); if (!groups.has(b)) groups.set(b, []); groups.get(b).push(t);
  }
  const boxes = [];
  for (const [blk, texts] of groups) {
    const bcs = getComputedStyle(blk);
    const lines = []; let cur = null, lastTop = null;
    let L = 1e9, T = 1e9, Rr = -1e9, B = -1e9, fsMax = 0;
    for (const t of texts) {
      const cs = getComputedStyle(t.parentElement);
      const st = { color: cs.color, fs: parseFloat(cs.fontSize), fw: +cs.fontWeight, ls: parseFloat(cs.letterSpacing) || 0, it: cs.fontStyle === 'italic' };
      fsMax = Math.max(fsMax, st.fs);
      const s = t.nodeValue, rg = document.createRange();
      for (let i = 0; i < s.length; i++) {
        rg.setStart(t, i); rg.setEnd(t, i + 1);
        const rc = [...rg.getClientRects()].filter(q => q.width > 0 || q.height > 0)[0];
        if (!rc) continue;
        const ch = s[i] === '\n' || s[i] === '\t' ? ' ' : s[i];
        if (!cur || rc.top > cur.bottom - (cur.bottom - cur.top) * 0.3) { cur = { runs: [], top: rc.top, bottom: rc.bottom }; lines.push(cur); lastTop = rc.top; }   // 큰 숫자 + 작은 단위처럼 크기가 달라도 세로로 겹치면 같은 줄
        if (ch !== ' ' || cur.runs.length) {
          const last = cur.runs[cur.runs.length - 1];
          if (last && last.color === st.color && last.fs === st.fs && last.fw === st.fw && last.ls === st.ls && last.it === st.it) last.text += ch;
          else cur.runs.push({ ...st, text: ch });
        }
        cur.bottom = Math.max(cur.bottom, rc.bottom);
        if (ch !== ' ') { L = Math.min(L, rc.left); Rr = Math.max(Rr, rc.right); T = Math.min(T, rc.top); B = Math.max(B, rc.bottom); }
      }
    }
    lines.forEach(l => { const r = l.runs[l.runs.length - 1]; if (r) r.text = r.text.replace(/\s+$/, ''); l.runs = l.runs.filter(r => r.text.length); });
    const ls = lines.filter(l => l.runs.length);
    if (!ls.length || L > Rr) continue;
    const pitch = ls.length > 1 ? (ls[ls.length - 1].top - ls[0].top) / (ls.length - 1) : (parseFloat(bcs.lineHeight) || fsMax * 1.25);
    const br = blk.getBoundingClientRect();
    boxes.push({ x: L, y: T, w: Rr - L, h: B - T, pitch, align: bcs.textAlign, bl: br.left, bw: br.width, lines: ls.map(l => l.runs) });
  }
  return boxes;
}

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [n, f] of jobs) {
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready.then(() => 1)); await pg.waitForTimeout(150);
    const boxes = await pg.evaluate(grab);
    await pg.addStyleTag({ content: '#r *:not(svg):not(svg *):not(.ghost){color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;caret-color:transparent!important}' });
    await pg.waitForTimeout(50);
    const id = String(n).padStart(3, '0');
    await pg.screenshot({ path: path.join(OUT, `b${id}.jpg`), type: 'jpeg', quality: 90 });
    fs.writeFileSync(path.join(OUT, `t${id}.json`), JSON.stringify(boxes));
    process.stdout.write(`${n}:${boxes.length} `);
  }
  await br.close(); console.log('\ndone');
})();
