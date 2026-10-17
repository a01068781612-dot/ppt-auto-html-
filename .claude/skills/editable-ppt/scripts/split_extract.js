// 분해판 1단계 — 장면 HTML의 모든 요소를 PowerPoint 개체로 나누기 위한 목록을 뽑는다.
// 사용: NODE_PATH=/opt/node22/lib/node_modules node split_extract.js <OUT> <장:폴더,...>
//   결과: OUT/b###.jpg(바탕만) · OUT/o###.json(그리는 순서대로 개체 목록) · OUT/r###_k.png(따로 찍은 장식 · SVG · 외곽선 글자)
// 개체 종류: shape(단색 · 테두리 · 둥근 모서리 · 그림자 → PowerPoint 도형) · img(사진, 보이는 부분만) · raster(그 밖의 장식, 투명 PNG) · text(글상자)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [OUT, SPEC] = process.argv.slice(2);
fs.mkdirSync(OUT, { recursive: true });
const jobs = [];
for (const part of SPEC.split(',')) {
  const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number);
  for (let n = a; n <= b; n++) jobs.push([n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`)]);
}

function walk() {
  const R = document.getElementById('r'); const ops = []; let k = 0;
  const alpha = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return 0; const p = m[1].split(',').map(s => parseFloat(s)); return p.length > 3 ? p[3] : 1; };
  const opac = el => { let o = 1; for (let e = el; e && e !== R; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity); return o; };
  const clipOf = el => { // 조상 중 overflow:hidden 이 만드는 잘림 영역 + 모서리 둥글기
    let c = { l: 0, t: 0, r: 1920, b: 1080 }, rad = 0;
    for (let e = el.parentElement; e && e !== R; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflow !== 'visible') {
        const q = e.getBoundingClientRect(), bw = parseFloat(cs.borderTopWidth) || 0;
        c = { l: Math.max(c.l, q.left + bw), t: Math.max(c.t, q.top + bw), r: Math.min(c.r, q.right - bw), b: Math.min(c.b, q.bottom - bw) };
        rad = Math.max(rad, (parseFloat(cs.borderTopLeftRadius) || 0) - bw);
      }
    }
    return [c, rad];
  };
  const visit = el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const q = el.getBoundingClientRect(), o = opac(el);
    const tag = el.tagName.toLowerCase();
    const cls = (typeof el.className === 'string' ? el.className : (el.getAttribute('class') || '')).trim();
    if (tag === 'svg') { el.dataset.k = ++k; ops.push({ t: 'raster', k, x: q.left, y: q.top, w: q.width, h: q.height, pad: 4, cls: 'svg', paths: el.querySelectorAll('path').length, rects: el.querySelectorAll('rect,circle,line,polyline').length }); return; }
    if (tag === 'img') {
      const nw = el.naturalWidth, nh = el.naturalHeight; if (!nw || q.width < 1) return;
      const fit = cs.objectFit; const [pp0, pp1] = cs.objectPosition.split(' ').map(v => parseFloat(v) / 100);
      let s = fit === 'cover' ? Math.max(q.width / nw, q.height / nh) : fit === 'contain' ? Math.min(q.width / nw, q.height / nh) : null;
      let dx, dy, dw, dh;
      if (s === null) { dx = q.left; dy = q.top; dw = q.width; dh = q.height; } else { dw = nw * s; dh = nh * s; dx = q.left + (q.width - dw) * (isNaN(pp0) ? .5 : pp0); dy = q.top + (q.height - dh) * (isNaN(pp1) ? .5 : pp1); }
      const [c, rad] = clipOf(el);
      const L = Math.max(dx, q.left, c.l), T = Math.max(dy, q.top, c.t), Rr = Math.min(dx + dw, q.right, c.r), B = Math.min(dy + dh, q.bottom, c.b);
      if (Rr - L < 1 || B - T < 1) return;
      const sx = nw / dw, sy = nh / dh;
      ops.push({ t: 'img', src: decodeURIComponent(new URL(el.currentSrc || el.src).pathname), x: L, y: T, w: Rr - L, h: B - T,
        sx: (L - dx) * sx, sy: (T - dy) * sy, sw: (Rr - L) * sx, sh: (B - T) * sy, rad, op: o, cls: (el.closest('.shot') || el).className, label: (el.closest('.shot') && el.closest('.shot').querySelector('.lbl') || {}).textContent || '' });
      return;
    }
    if (el !== R) {
      const bg = cs.backgroundColor, bgi = cs.backgroundImage;
      const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ w: parseFloat(cs[`border${s}Width`]) || 0, c: cs[`border${s}Color`], st: cs[`border${s}Style`] }))
        .map(b => (b.st === 'none' || alpha(b.c) === 0 ? { w: 0, c: b.c } : b));
      const anyB = sides.some(b => b.w > 0), hasBg = alpha(bg) > 0;
      const special = (bgi && bgi !== 'none') || el.classList.contains('ghost') || (cs.webkitTextStroke && parseFloat(cs.webkitTextStrokeWidth) > 0)
        || (anyB && (q.width - (parseFloat(cs.borderLeftWidth) || 0) - (parseFloat(cs.borderRightWidth) || 0) < 1 || q.height - (parseFloat(cs.borderTopWidth) || 0) - (parseFloat(cs.borderBottomWidth) || 0) < 1)) || cs.transform !== 'none' || cs.filter !== 'none' || cs.clipPath !== 'none' || (cs.boxShadow !== 'none' && cs.boxShadow.split('rgba').length > 2);
      if (special && q.width > 0) {
        el.dataset.k = ++k; const pad = cs.boxShadow !== 'none' ? 70 : 4;
        ops.push({ t: 'raster', k, x: q.left, y: q.top, w: q.width, h: q.height, pad, cls, text: (el.textContent || '').trim().slice(0, 30) });
      } else if ((hasBg || anyB || cs.boxShadow !== 'none') && q.width > 0 && q.height > 0) {
        const uni = sides.every(b => b.w === sides[0].w && b.c === sides[0].c);
        const sh = cs.boxShadow !== 'none' ? cs.boxShadow : null;
        if (hasBg || (uni && sides[0].w > 0) || sh)   // 칠도 테두리도 없는 빈 도형은 만들지 않음(한쪽 테두리만 있으면 선만)
          ops.push({ t: 'shape', x: q.left, y: q.top, w: q.width, h: q.height, fill: hasBg ? bg : null, rad: parseFloat(cs.borderTopLeftRadius) || 0,
          line: uni && sides[0].w > 0 ? { w: sides[0].w, c: sides[0].c } : null, shadow: sh, op: o, cls, tag });
        if (!uni) sides.forEach((b, i) => { if (!b.w) return;
          const r = i === 0 ? [q.left, q.top, q.width, b.w] : i === 1 ? [q.right - b.w, q.top, b.w, q.height] : i === 2 ? [q.left, q.bottom - b.w, q.width, b.w] : [q.left, q.top, b.w, q.height];
          ops.push({ t: 'shape', x: r[0], y: r[1], w: r[2], h: r[3], fill: b.c, rad: 0, line: null, shadow: null, op: o, cls, tag, side: ['위', '오른쪽', '아래', '왼쪽'][i] }); });
      }
    }
    for (const ch of el.children) visit(ch);
  };
  visit(R);
  return ops;
}

function grab() {   // 글상자 — edit_extract.js와 같은 방법(화면 줄바꿈 그대로)
  const R = document.getElementById('r');
  const skip = el => !!el.closest('svg, .ghost');
  const blockOf = node => { let e = node.parentElement; while (e && e !== R && getComputedStyle(e).display === 'inline') e = e.parentElement; return e; };
  const groups = new Map(); const tw = document.createTreeWalker(R, NodeFilter.SHOW_TEXT);
  for (let t; (t = tw.nextNode());) {
    if (!t.nodeValue.trim() || skip(t.parentElement)) continue;
    const cs = getComputedStyle(t.parentElement);
    if (cs.visibility === 'hidden' || cs.color === 'rgba(0, 0, 0, 0)') continue;
    const b = blockOf(t); if (!groups.has(b)) groups.set(b, []); groups.get(b).push(t);
  }
  const boxes = [];
  for (const [blk, texts] of groups) {
    const bcs = getComputedStyle(blk); const lines = []; let cur = null;
    let L = 1e9, T = 1e9, Rr = -1e9, B = -1e9, fsMax = 0;
    for (const t of texts) {
      const cs = getComputedStyle(t.parentElement);
      const st = { color: cs.color, fs: parseFloat(cs.fontSize), fw: +cs.fontWeight, ls: parseFloat(cs.letterSpacing) || 0, it: cs.fontStyle === 'italic' };
      fsMax = Math.max(fsMax, st.fs); const s = t.nodeValue, rg = document.createRange();
      for (let i = 0; i < s.length; i++) {
        rg.setStart(t, i); rg.setEnd(t, i + 1);
        const rc = [...rg.getClientRects()].filter(q => q.width > 0 || q.height > 0)[0]; if (!rc) continue;
        const ch = /\s/.test(s[i]) ? ' ' : s[i];
        if (!cur || rc.top > cur.bottom - (cur.bottom - cur.top) * 0.3) { cur = { runs: [], top: rc.top, bottom: rc.bottom }; lines.push(cur); }
        if (ch !== ' ' || cur.runs.length) {
          const last = cur.runs[cur.runs.length - 1];
          if (last && last.color === st.color && last.fs === st.fs && last.fw === st.fw && last.ls === st.ls && last.it === st.it) last.text += ch; else cur.runs.push({ ...st, text: ch });
        }
        cur.bottom = Math.max(cur.bottom, rc.bottom);
        if (ch !== ' ') { L = Math.min(L, rc.left); Rr = Math.max(Rr, rc.right); T = Math.min(T, rc.top); B = Math.max(B, rc.bottom); cur.left = Math.min(cur.left ?? 1e9, rc.left); }
      }
    }
    lines.forEach(l => { const r = l.runs[l.runs.length - 1]; if (r) r.text = r.text.replace(/\s+$/, ''); l.runs = l.runs.filter(r => r.text.length); });
    const ls = lines.filter(l => l.runs.length); if (!ls.length || L > Rr) continue;
    const pitch = ls.length > 1 ? (ls[ls.length - 1].top - ls[0].top) / (ls.length - 1) : (parseFloat(bcs.lineHeight) || fsMax * 1.25);
    const role = blk.closest('.ttl') ? '제목' : blk.closest('.tag') ? '머리표' : blk.closest('.key') ? 'KEY' : blk.closest('.pg') ? '쪽번호' : blk.closest('.lbl') ? '사진 설명' : blk.closest('td,th') ? '표' : blk.closest('.chip') ? '칩' : '';
    boxes.push({ t: 'text', x: L, y: T, w: Rr - L, h: B - T, pitch, align: bcs.textAlign, lines: ls.map(l => l.runs), lefts: ls.map(l => l.left), role, fsMax });   // lefts: 줄마다 왼쪽 끝(둘째 줄 들여쓰기)
  }
  return boxes;
}

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  const HIDE_TEXT = '#r *:not(svg):not(svg *):not(.ghost){color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}';
  for (const [n, f] of jobs) {
    const id = String(n).padStart(3, '0');
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready.then(() => 1)); await pg.waitForTimeout(150);
    const texts = await pg.evaluate(grab);
    const ops = await pg.evaluate(walk);
    await pg.addStyleTag({ content: HIDE_TEXT });
    const iso = await pg.addStyleTag({ content: '#r *{visibility:hidden!important}' });
    await pg.screenshot({ path: path.join(OUT, `b${id}.jpg`), type: 'jpeg', quality: 90 });   // 바탕(#r 배경)만
    await pg.evaluate(() => { document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent'; document.getElementById('r').style.background = 'none'; });
    for (const o of ops.filter(o => o.t === 'raster')) {
      const css = `#r [data-k="${o.k}"], #r svg[data-k="${o.k}"] *{visibility:visible!important}`;
      const h = await pg.addStyleTag({ content: css });
      const x = Math.max(0, o.x - o.pad), y = Math.max(0, o.y - o.pad), w = Math.min(1920, o.x + o.w + o.pad) - x, hh = Math.min(1080, o.y + o.h + o.pad) - y;
      Object.assign(o, { x, y, w, h: hh, file: `r${id}_${o.k}.png` });
      if (w >= 1 && hh >= 1) await pg.screenshot({ path: path.join(OUT, o.file), clip: { x, y, width: w, height: hh }, omitBackground: true });
      await h.evaluate(e => e.remove());
    }
    fs.writeFileSync(path.join(OUT, `o${id}.json`), JSON.stringify(ops.concat(texts)));
    process.stdout.write(`${n}:${ops.length}+${texts.length} `);
  }
  await br.close(); console.log('\ndone');
})();
