// 보통(400) 글자를 SemiBold(600)로 — 줄바꿈 · 위치가 바뀌면 안 됨.
// 사용: NODE_PATH=/opt/node22/lib/node_modules node semibold.js <장면 폴더(fit 결과)>   → 같은 폴더의 v###.html을 고쳐 씀 + semibold.json(장마다 바꾼 글 · 자간 줄인 글 · 그대로 둔 글)
// 방법: 글이 직접 들어 있는 요소 중 굵기 400인 것을 600으로. 화면의 모든 글 덩어리마다 줄 수 · 줄마다 첫 글자 위치 · 덩어리 위치 · 높이를 바꾸기 전과 비교해
//       달라지면 자간을 0.005em씩 최대 0.06em 줄여 맞추고, 그래도 안 맞으면 그 덩어리만 400 그대로.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [DIR] = process.argv.slice(2);
const files = [];
for (const sub of fs.readdirSync(DIR)) { const d = path.join(DIR, sub); if (fs.statSync(d).isDirectory()) for (const f of fs.readdirSync(d)) if (/^v\d{3}\.html$/.test(f)) files.push(path.join(d, f)); }

function run() {
  const R = document.getElementById('r');
  const isBlock = e => getComputedStyle(e).display !== 'inline';
  const blockOf = e => { while (e !== R && !isBlock(e)) e = e.parentElement; return e; };
  const snap = b => {   // 줄마다 (top, 첫 글자 left), 덩어리 위치 · 크기
    const tw = document.createTreeWalker(b, NodeFilter.SHOW_TEXT), rg = document.createRange(), lines = [];
    for (let t; (t = tw.nextNode());) for (let i = 0; i < t.nodeValue.length; i++) { if (/\s/.test(t.nodeValue[i])) continue; rg.setStart(t, i); rg.setEnd(t, i + 1);
      const r = [...rg.getClientRects()].find(x => x.width > 0); if (!r) continue; const l = lines.find(l => Math.abs(l.t - r.top) < r.height * 0.5);
      if (l) l.l = Math.min(l.l, r.left); else lines.push({ t: r.top, l: r.left }); }
    const q = b.getBoundingClientRect(); return { lines, q: [q.left, q.top, q.width, q.height] };
  };
  const same = (a, b) => a.lines.length === b.lines.length && a.lines.every((l, i) => Math.abs(l.t - b.lines[i].t) < 1.5 && Math.abs(l.l - b.lines[i].l) < 1.5) && [0, 1, 3].every(i => Math.abs(a.q[i] - b.q[i]) < 1.5);   // 줄 수 · 줄마다 시작 위치 · 상자 왼쪽 · 위 · 높이(폭은 글이 굵어진 만큼 늘어도 됨)
  // 지금 굵기를 모두 그대로 고정 — <b>는 '한 단계 더 굵게'라서 부모가 600이 되면 900(Black)으로 바뀌어 버림
  for (const e of R.querySelectorAll('*')) { if (e.closest('svg')) continue; const w = +getComputedStyle(e).fontWeight; if (w !== 400) e.style.fontWeight = String(w); }
  // 들여쓰기용 공백(nbsp 2개 이상)은 굵기 400 그대로 — 굵게 하면 공백 폭이 늘어 둘째 줄 시작이 밀림
  { const tw = document.createTreeWalker(R, NodeFilter.SHOW_TEXT), ts = []; for (let t; (t = tw.nextNode());) if (/\u00a0{2,}/.test(t.nodeValue) && !t.parentElement.closest('svg')) ts.push(t);
    for (const t of ts) { const parts = t.nodeValue.split(/(\u00a0{2,})/); const frag = document.createDocumentFragment();
      for (const p of parts) { if (!p) continue; if (/^\u00a0{2,}$/.test(p)) { const sp = document.createElement('span'); sp.className = 'nb'; sp.style.fontWeight = '400'; sp.textContent = p; frag.appendChild(sp); } else frag.appendChild(document.createTextNode(p)); }
      t.parentNode.replaceChild(frag, t); } }
  const els = [...R.querySelectorAll('*')].filter(e => !e.closest('svg, .ghost') && [...e.childNodes].some(x => x.nodeType === 3 && x.nodeValue.trim()) && +getComputedStyle(e).fontWeight === 400 && !e.classList.contains('nb'));
  const groups = new Map(); els.forEach(e => { const b = blockOf(e); if (!groups.has(b)) groups.set(b, []); groups.get(b).push(e); });
  const all = [...new Set([...R.querySelectorAll('*')].filter(e => !e.closest('svg') && [...e.childNodes].some(x => x.nodeType === 3 && x.nodeValue.trim())).map(blockOf))];
  const before = new Map(all.map(b => [b, snap(b)]));
  const rep = { done: 0, tight: 0, kept: [] };
  for (const [b, es] of groups) {
    const keep = es.map(e => e.getAttribute('style'));
    const ls0 = es.map(e => parseFloat(getComputedStyle(e).letterSpacing) || 0), fs0 = es.map(e => parseFloat(getComputedStyle(e).fontSize));
    let ok = false, used = 0; const ib = getComputedStyle(b).display === 'inline-block', mr0 = parseFloat(getComputedStyle(b).marginRight) || 0, w0 = b.getBoundingClientRect().width, bst = b.getAttribute('style');
    for (let k = 0; k <= 12 && !ok; k++) {
      es.forEach((e, i) => { e.style.fontWeight = '600'; if (k) e.style.letterSpacing = (ls0[i] - fs0[i] * 0.005 * k).toFixed(2) + 'px'; });
      if (ib) { b.style.marginRight = mr0 + 'px'; const dw = b.getBoundingClientRect().width - w0; b.style.marginRight = (mr0 - dw).toFixed(2) + 'px'; }   // 나란한 칸(inline-block): 늘어난 폭만큼 오른쪽 간격을 줄여 다음 칸 위치 그대로
      ok = all.every(x => same(before.get(x), snap(x))); used = k;   // 이 덩어리뿐 아니라 화면의 모든 글 위치가 그대로여야 함
    }
    if (ok) { rep.done++; if (used) rep.tight++; }
    else { es.forEach((e, i) => { if (keep[i] === null) e.removeAttribute('style'); else e.setAttribute('style', keep[i]); }); if (ib && !es.includes(b)) { if (bst === null) b.removeAttribute('style'); else b.setAttribute('style', bst); } rep.kept.push(b.textContent.trim().slice(0, 20)); }
  }
  return rep;
}

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } }); const out = {};
  for (const f of files.sort()) {
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready.then(() => 1)); await pg.waitForTimeout(80);
    const r = await pg.evaluate(run); out[path.basename(f)] = r;
    fs.writeFileSync(f, '<!doctype html>\n' + await pg.evaluate(() => document.documentElement.outerHTML));
  }
  fs.writeFileSync(path.join(DIR, 'semibold.json'), JSON.stringify(out, null, 1)); await br.close();
  const v = Object.values(out); console.log('blocks done', v.reduce((a, r) => a + r.done, 0), 'tightened', v.reduce((a, r) => a + r.tight, 0), 'kept 400', v.reduce((a, r) => a + r.kept.length, 0));
})();
