// 카드 글자 맞춤 — 카드(.card) 안 글자가 오른쪽 여백을 많이 남기지 않게, 필요 없는 줄바꿈(<br>)은 없애고 글자를 카드에 맞게 키운다.
// 사용: NODE_PATH=/opt/node22/lib/node_modules node fit_cards.js <OUT 폴더> <장:폴더,...> [<장:파일,...>]
//   결과: OUT/<폴더 이름>/v###.html(맞춘 장면) + 같은 폴더의 그림 · 글꼴은 링크로 연결 · OUT/fit.json(장마다 카드별 배율 · 없앤 줄바꿈 수)
// 규칙: ① 줄바꿈으로 나뉜 글이 한 줄에 들어가면 한 줄로(안 들어가면 원래 줄바꿈 그대로)
//       ② 카드 안 글자(크기 · 줄 간격 · 들여쓰기)를 같은 배율로 키움(최대 1.45배, 위아래 간격은 그대로) — 카드 크기는 그대로, 글이 카드 폭 · 높이(위아래 24px 여유) 안에 들어가는 가장 큰 배율
//       ③ 원래 없던 자동 줄바꿈이 생기면 그 배율은 안 씀(단어 하나만 다음 줄로 넘어가는 일 없게)
//       ⑦ 작은 글씨(36px 미만)는 18 · 22 · 26 · 30 · 34px 5단계로, 한글 작은 글씨 자간 0(일관성)
//       ⑥ 저절로 줄이 바뀐 글은 의미 단위(' · ' ' → ' ' (' ', ')에서 끊어 줄바꿈(<br>)
//       ⑤ 가로 flex 안에 글 · 강조가 섞여 문장이 칸으로 끊기는 곳은 한 덩어리로 감쌈
//       ④ 칸 구성이 같은 나란한 카드(같은 줄 · 같은 높이)는 같은 배율로, 머리글(주황 작은 글)을 맨 위에 1.4배로, 칸 높이를 맞춰 가로줄을 맞춤
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [OUT, SPEC, ONE] = process.argv.slice(2);
const jobs = new Map();
for (const part of SPEC.split(',')) {
  const [r, dir] = part.split(':'); const [a, b] = r.split('-').map(Number);
  for (let n = a; n <= b; n++) jobs.set(n, path.resolve(dir, `v${String(n).padStart(3, '0')}.html`));
}
for (const part of (ONE || '').split(',').filter(Boolean)) { const [n, f] = part.split(':'); jobs.set(+n, path.resolve(f)); }

function fit() {
  const MAX = 1.45, STEP = 0.025, PADV = 24, TOP = 48, LABEL = 1.4;
  const KEYS = ['fontSize', 'lineHeight', 'paddingLeft', 'textIndent', 'letterSpacing'];   // 위아래 간격(margin · gap)은 그대로 — 글자 키울 자리를 남김
  const CSSK = { fontSize: 'font-size', lineHeight: 'line-height', paddingLeft: 'padding-left', textIndent: 'text-indent', letterSpacing: 'letter-spacing' };
  const BR = /\s*<br\b[^>]*>\s*/g;
  const isBlock = e => getComputedStyle(e).display !== 'inline';
  const blocksOf = c => { const s = new Set(), tw = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
    for (let t; (t = tw.nextNode());) { if (!t.nodeValue.trim()) continue; let e = t.parentElement; while (e !== c && !isBlock(e)) e = e.parentElement; s.add(e); } return [...s]; };
  const linesOf = el => { const tops = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), rg = document.createRange();
    for (let t; (t = tw.nextNode());) for (let i = 0; i < t.nodeValue.length; i++) { if (/\s/.test(t.nodeValue[i])) continue; rg.setStart(t, i); rg.setEnd(t, i + 1);
      const r = [...rg.getClientRects()].find(x => x.width > 0); if (!r) continue; const l = tops.find(l => r.top < l.b - (l.b - l.t) * 0.3 && r.bottom > l.t + (l.b - l.t) * 0.3);
      if (l) { l.b = Math.max(l.b, r.bottom); l.t = Math.min(l.t, r.top); } else tops.push({ t: r.top, b: r.bottom }); }
    return tops.length; };
  const textBox = c => { let L = 1e9, R = -1e9, T = 1e9, B = -1e9; const tw = document.createTreeWalker(c, NodeFilter.SHOW_TEXT), rg = document.createRange();
    for (let t; (t = tw.nextNode());) { if (!t.nodeValue.trim()) continue; rg.selectNodeContents(t); for (const r of rg.getClientRects()) if (r.width > 0) { L = Math.min(L, r.left); R = Math.max(R, r.right); T = Math.min(T, r.top); B = Math.max(B, r.bottom); } }
    return { L, R, T, B }; };
  const sameSize = b => { const z = new Set(); const tw = document.createTreeWalker(b, NodeFilter.SHOW_TEXT); for (let t; (t = tw.nextNode());) if (t.nodeValue.trim()) z.add(getComputedStyle(t.parentElement).fontSize); return z.size === 1; };
  // 가로 flex 안에 글과 강조(<b>)가 섞여 있으면 조각마다 칸이 나뉘어 문장이 끊김(82 · 83장 실측 띠) → 한 덩어리로 감쌈
  let mixed = 0;
  for (const e of document.querySelectorAll('#r *')) {
    const z = getComputedStyle(e); if (!/flex/.test(z.display) || /column/.test(z.flexDirection)) continue;
    if (![...e.childNodes].some(x => x.nodeType === 3 && x.nodeValue.trim())) continue;
    const w = document.createElement('span'); while (e.firstChild) w.appendChild(e.firstChild); e.appendChild(w); mixed++;
  }
  // 같은 줄에 나란히 놓인 같은 높이 카드는 한 묶음(같은 배율). 칸 수가 같으면 '나란한 카드': 머리글을 맨 위에 크게, 칸마다 높이를 맞춰 가로줄을 맞춤
  const cards = [...document.querySelectorAll('.card, .a.body')].filter(c => c.textContent.trim() && (c.classList.contains('card') || (/flex/.test(getComputedStyle(c).display) && getComputedStyle(c).flexDirection === 'column' && !c.closest('.card') && c.children.length >= 2)));
  const groups = [];
  for (const c of cards) { const q = c.getBoundingClientRect(); const g = groups.find(g => (Math.abs(g.top - q.top) < 3 && Math.abs(g.h - q.height) < 3) || (Math.abs(g.w - q.width) < 3 && Math.abs(g.bottom - q.bottom) < 3 && g.cards[0].children.length === c.children.length)); if (g) g.cards.push(c); else groups.push({ top: q.top, h: q.height, w: q.width, bottom: q.bottom, cards: [c] }); }   // 계단식(99장)도 한 묶음
  const isPar = C => { const n0 = C[0].children.length; return C.length >= 2 && C.every(c => c.children.length === n0 && n0 >= 2 && ((getComputedStyle(c).justifyContent === 'center' && getComputedStyle(c).flexDirection === 'column') || getComputedStyle(c).display === 'block'))   // 세로 flex 가운데 정렬, 또는 보통 블록(109장)
      && C.every(c => { const f = c.children[0]; return f.textContent.trim().length <= 20 && f.children.length === 0 && f.classList.contains('acc'); }); };   // 머리글 = 주황 글(acc)
  const units = []; for (const G of groups) { if (isPar(G.cards)) { const q = G.cards[0].getBoundingClientRect(); const same = units.find(u => u.length >= 2 && isPar([...u, ...G.cards]) && Math.abs(u[0].getBoundingClientRect().width - q.width) < 3 && Math.abs(u[0].getBoundingClientRect().height - q.height) < 3); if (same) same.push(...G.cards); else units.push(G.cards); } else G.cards.forEach(c => units.push([c])); }   // 같은 크기 카드 줄이 여럿이면(103장 2줄) 한 배율   // 나란한 카드만 묶음, 나머지는 카드마다 따로
  const report = [];
  for (const C of units) {
    const n0 = C[0].children.length, par = C.length >= 2;
    const st = C.map(c => ({ html: c.innerHTML, style: c.getAttribute('style') || '', q: c.getBoundingClientRect(), cs: getComputedStyle(c) }));
    const stair = par && C.some(c => Math.abs(c.getBoundingClientRect().top - C[0].getBoundingClientRect().top) > 3);
    const prep = () => C.forEach((c, k) => { c.innerHTML = st[k].html; c.setAttribute('style', st[k].style);
      if (par) { c.style.justifyContent = 'flex-start'; c.style.paddingTop = TOP + 'px'; const f = c.children[0]; f.style.fontSize = (parseFloat(getComputedStyle(f).fontSize) * (stair ? 1.7 : LABEL)).toFixed(1) + 'px'; } });
    prep();
    const info = C.map((c, k) => { const bl = blocksOf(c); const t0 = textBox(c); const inR = st[k].q.right - parseFloat(st[k].cs.paddingRight) - parseFloat(st[k].cs.borderRightWidth);
      return { base: bl.map(b => ({ lines: linesOf(b), br: b.querySelectorAll('br').length })), canJoin: bl.map(b => { if (!b.querySelector('br') || !sameSize(b)) return false; const keep = b.innerHTML; b.innerHTML = keep.replace(BR, ' '); const ok = linesOf(b) === 1; b.innerHTML = keep; return ok; }),
        inR, h0: t0.B - t0.T, t0, free0: (inR - t0.R) / Math.max(1, inR - t0.L) }; });
    function trial(s, force) {
      prep(); const out = [];
      for (let k = 0; k < C.length; k++) {
        const c = C[k], I = info[k];
        const all = [...c.querySelectorAll('*:not(br)')], vals = all.map(e => { const z = getComputedStyle(e); return KEYS.map(x => z[x]); });
        all.forEach((e, i) => KEYS.forEach((x, j) => { const v = vals[i][j]; if (/px$/.test(v) && parseFloat(v) !== 0) e.style.setProperty(CSSK[x], (parseFloat(v) * s).toFixed(2) + 'px'); }));
        const bl = blocksOf(c); if (bl.length !== I.base.length) return null;
        let joined = 0;
        for (let i = 0; i < bl.length; i++) {
          const b = bl[i];
          if (I.base[i].br && sameSize(b) && (!force || I.canJoin[i])) {
            const keep = b.innerHTML; b.innerHTML = keep.replace(BR, ' ');
            if (linesOf(b) === 1) { joined += I.base[i].br; continue; }
            if (force) return null;
            b.innerHTML = keep;
          }
          if (linesOf(b) > I.base[i].lines) return null;   // 새 자동 줄바꿈 → 이 배율은 안 씀
        }
        out.push({ joined });
      }
      if (par) {   // 줄(위끝이 같은 카드)마다: 칸 높이를 맞춰 가로줄을 맞추고, 가장 긴 카드 내용이 세로 가운데 오게 위 여백을 함께 정함
        const rows = []; C.forEach(c => { const t = c.getBoundingClientRect().top; const r = rows.find(r => Math.abs(r.t - t) < 3); if (r) r.cs.push(c); else rows.push({ t, cs: [c] }); });
        for (const { cs } of rows) {
          if (cs.length < 2) continue;
          for (let i = 0; i < n0 - 1; i++) { const h = Math.max(...cs.map(c => c.children[i].getBoundingClientRect().height)); cs.forEach(c => { c.children[i].style.minHeight = h.toFixed(1) + 'px'; }); }
          const H = Math.max(...cs.map(c => { const k = [...c.children]; return k[k.length - 1].getBoundingClientRect().bottom - k[0].getBoundingClientRect().top; }));
          const top = Math.max(PADV, (cs[0].getBoundingClientRect().height - H) / 2); cs.forEach(c => { c.style.paddingTop = top.toFixed(1) + 'px'; });
        }
      }
      for (let k = 0; k < C.length; k++) {
        const c = C[k], q = c.getBoundingClientRect(), t = textBox(c), I = info[k];
        if (Math.abs(q.width - st[k].q.width) > 1 || Math.abs(q.height - st[k].q.height) > 1) return null;   // 카드 크기 그대로
        if (t.R > I.inR + 1) return null;
        if (par ? t.B > q.bottom - PADV : t.B - t.T > Math.max(q.height - 2 * PADV, I.h0)) return null;
        if (t.B > Math.max(q.bottom - PADV, I.t0.B) + 1 || t.T < Math.min(q.top + PADV, I.t0.T) - 1) return null;   // 글이 카드 위아래 끝에 닿지 않게
        out[k].free = (I.inR - t.R) / Math.max(1, I.inR - t.L);
      }
      return out;
    }
    const anyJoin = info.some(I => I.canJoin.some(x => x));
    const search = force => { for (let s = MAX; s >= 1 - 1e-6; s -= STEP) { const r = trial(+s.toFixed(3), force); if (r) return { s: +s.toFixed(3), force, r }; } return null; };
    // 합칠 수 있는 줄바꿈을 모두 합쳤을 때 카드 폭을 거의 채우면(빈 곳 15% 이하) 그대로, 아니면 글자를 키우는 쪽(그 크기에서 한 줄에 들어가는 글만 합침)
    const A = anyJoin ? search(true) : null, Bv = search(false);
    let best = A && Math.max(...A.r.map(x => x.free)) <= 0.15 ? A : (Bv && (Bv.s > 1 || Bv.r.some(x => x.joined)) ? Bv : (A || Bv));
    if (!best || (best.s === 1 && !par && !best.r.some(x => x.joined))) { C.forEach((c, k) => { c.innerHTML = st[k].html; c.setAttribute('style', st[k].style); }); continue; }
    trial(best.s, best.force);   // 고른 배율로 다시 적용
    C.forEach((c, k) => report.push({ text: c.textContent.trim().slice(0, 16), s: best.s, joined: best.r[k].joined, row: par, free0: +info[k].free0.toFixed(2), free: +best.r[k].free.toFixed(2) }));
  }
  // 작은 글씨(36px 미만) 맞춤 — 크기를 5단계(18 · 22 · 26 · 30 · 34px)로 모으고, 한글 작은 글씨의 넓은 자간은 없앰(영문 대문자 머리말 · KEY는 그대로)
  const TIERS = [18, 22, 26, 30, 34]; let snapped = 0;
  for (const e of [...document.querySelectorAll('#r *')]) {
    if (e.closest('svg, .ghost') || e.tagName === 'BR' || e.tagName === 'IMG') continue;
    if (![...e.childNodes].some(x => x.nodeType === 3 && x.nodeValue.trim())) continue;   // 글이 직접 들어 있는 요소만
    const z = getComputedStyle(e), fs = parseFloat(z.fontSize); if (fs >= 35.5) continue;
    const blk = (() => { let b = e; while (b.parentElement && getComputedStyle(b).display === 'inline') b = b.parentElement; return b; })();
    const keep = e.getAttribute('style'), lines0 = linesOf(blk), box = blk.getBoundingClientRect(), par = blk.parentElement.getBoundingClientRect();
    const near = TIERS.reduce((a, t) => Math.abs(t - fs) < Math.abs(a - fs) ? t : a), floor = [...TIERS].reverse().find(t => t <= fs + 0.01) || TIERS[0];
    const hangul = /[가-힣]/.test(e.textContent), ls = parseFloat(z.letterSpacing) || 0;
    for (const t of near === floor ? [near] : [near, floor]) {
      e.setAttribute('style', keep || '');
      e.style.fontSize = t + 'px';
      if (/px$/.test(z.lineHeight)) e.style.lineHeight = (parseFloat(z.lineHeight) * t / fs).toFixed(2) + 'px';
      if (hangul && ls > 0 && !e.closest('.tag, .key')) e.style.letterSpacing = '0px';
      const nb = blk.getBoundingClientRect();
      if (linesOf(blk) <= lines0 && nb.right <= Math.max(box.right, par.right) + 1 && nb.bottom <= Math.max(box.bottom, par.bottom) + 1) { snapped++; break; }   // 줄이 늘거나 칸을 넘으면 다음 후보(내림)
      e.setAttribute('style', keep || ''); if (keep === null) e.removeAttribute('style');
    }
  }
  if (snapped) report.push({ snapSmall: snapped });
  let sem = 0;
  const avail = b => { const z = getComputedStyle(b); return b.clientWidth - parseFloat(z.paddingLeft) - parseFloat(z.paddingRight); };
  for (const b of [...new Set(blocksOf(document.getElementById('r')))]) {
    if (b.closest('svg, .ghost, .ttl')) continue;
    const segs = b.querySelectorAll('br').length + 1; if (linesOf(b) <= segs) continue;   // 저절로 바뀐 줄이 없으면 그대로
    // 글자마다 (텍스트 노드, 위치, 폭)
    const ch = []; const tw = document.createTreeWalker(b, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT), rg = document.createRange();
    for (let t; (t = tw.nextNode());) { if (t.nodeType === 1) { if (t.tagName === 'BR') ch.push({ br: true }); continue; }
      for (let i = 0; i < t.nodeValue.length; i++) { rg.setStart(t, i); rg.setEnd(t, i + 1); const r = [...rg.getClientRects()].find(x => x.width > 0); ch.push({ t, i, c: t.nodeValue[i], w: r ? r.width : 0 }); } }
    const W = avail(b) - 2, cuts = [];   // cuts: [시작, 끝) 글자를 지우고 그 자리에 줄바꿈
    let segStart = 0;
    const flush = end => {   // 한 덩어리(br 사이)를 의미 단위로 나눔
      const txt = ch.slice(segStart, end).map(x => x.c).join('');
      const cand = []; const re = /( · | → | \(|(?<=\S)\(|, | — | \/ )/g; let m;
      while ((m = re.exec(txt))) { const sep = m[1]; const a = segStart + m.index;
        const rank = sep.includes('(') ? 1 : (sep === ' → ' || sep === ' · ') ? 2 : 3;   // 괄호 앞 > 화살표 · 가운뎃점 > 쉼표
        if (sep === ' · ' || sep === ', ' || sep === ' — ' || sep === ' / ') cand.push({ rank, at: a + sep.length, del: [a + (sep === ', ' ? 1 : 0), a + sep.length] });   // ' · '는 지우고, ', '는 쉼표 남김
        else if (sep === '(') cand.push({ rank, at: a, del: [a, a] });   // 붙은 '(' 앞에서 줄바꿈(지우는 글자 없음)
        else cand.push({ rank, at: a + 1, del: [a, a + 1] }); }   // ' → ' · ' (' 앞에서 줄바꿈(기호는 다음 줄 첫머리)
      const wid = (i, j) => ch.slice(i, j).reduce((s, x) => s + (x.w || 0), 0);
      let lineStart = segStart;
      while (wid(lineStart, end) > W) {
        const ok = cand.filter(c => c.at > lineStart && wid(lineStart, c.del[0]) <= W); if (!ok.length) break;
        const good = ok.filter(c => wid(lineStart, c.del[0]) >= W * 0.4), pool = good.length ? good : ok, best = Math.min(...pool.map(c => c.rank));
        const c = pool.filter(c => c.rank === best).pop();   // 가장 의미가 큰 끊는 자리(첫 줄이 너무 짧지 않게) 중 뒤쪽
        cuts.push(c.del); lineStart = c.at;
      }
    };
    ch.forEach((x, k) => { if (x.br) { flush(k); segStart = k + 1; } }); flush(ch.length);
    if (!cuts.length) continue;
    const keep = b.innerHTML;
    for (const [a, e] of cuts.reverse()) {   // 뒤에서부터: 지울 글자 지우고 <br> 넣기
      for (let k = e - 1; k >= a; k--) { const x = ch[k]; x.t.nodeValue = x.t.nodeValue.slice(0, x.i) + x.t.nodeValue.slice(x.i + 1); }
      const x = ch[a] || ch[e]; if (!x || !x.t) continue; const node = x.t.splitText(Math.min(x.i, x.t.nodeValue.length)); node.parentNode.insertBefore(document.createElement('br'), node);
    }
    if (linesOf(b) > b.querySelectorAll('br').length + 1) { b.innerHTML = keep; continue; }   // 그래도 저절로 줄이 바뀌면 원래대로
    sem++;
  }
  if (sem) report.push({ semWrap: sem });
  if (mixed) report.push({ mixedFlex: mixed });
  return report;
}

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } }); const rep = {};
  for (const [n, f] of [...jobs].sort((a, b) => a[0] - b[0])) {
    const sub = path.join(OUT, path.basename(path.dirname(f)));
    if (!fs.existsSync(sub)) {   // 그림 · 글꼴은 원래 폴더 것을 링크로
      fs.mkdirSync(sub, { recursive: true });
      for (const x of fs.readdirSync(path.dirname(f))) if (!/^v\d{3}\.html$/.test(x)) fs.symlinkSync(path.join(path.dirname(f), x), path.join(sub, x));
    }
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready.then(() => 1)); await pg.waitForTimeout(100);
    const r = await pg.evaluate(fit); if (r.length) rep[n] = r;
    const html = await pg.evaluate(() => '<!doctype html>\n' + document.documentElement.outerHTML);
    fs.writeFileSync(path.join(sub, path.basename(f)), html);
  }
  fs.writeFileSync(path.join(OUT, 'fit.json'), JSON.stringify(rep, null, 1)); await br.close();
  const cards = Object.values(rep).flat().filter(c => !c.mixedFlex && !c.semWrap && !c.snapSmall);
  console.log('slides', Object.keys(rep).length, 'cards', cards.length, 'joined br', cards.reduce((a, c) => a + c.joined, 0));
})();
