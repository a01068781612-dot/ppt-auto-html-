// 75 · 84 · 99 · 117장만 손보기(사용자 지시 26.10.17)
const { chromium } = require('playwright'); const fs = require('fs'); const F = process.argv[2];
const jobs = { 75: 'h2/v075.html', 84: 'h2/v084.html', 99: 'h3/v099.html', 117: 'h3/v117.html' };
(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [n, f] of Object.entries(jobs)) {
    await pg.goto('file://' + F + '/' + f); await pg.evaluate(() => document.fonts.ready);
    const r = await pg.evaluate((n) => {
      const R = document.getElementById('r'), cards = [...R.querySelectorAll('.card')];
      const fits = el => { const p = el.parentElement, z = getComputedStyle(p); const inner = p.getBoundingClientRect().right - parseFloat(z.paddingRight) - parseFloat(z.borderRightWidth);
        const rg = document.createRange(); rg.selectNodeContents(el); const rs = [...rg.getClientRects()].filter(x => x.width > 0); const tops = new Set(rs.map(x => Math.round(x.top / 10)));
        return { right: Math.max(...rs.map(x => x.right)), inner, lines: tops.size }; };
      if (n == 75) {   // 대상: "마을 3곳 / 1회 훈련"
        const t = cards[2].children[1]; t.innerHTML = '마을 3곳<br>/ 1회 훈련';
        let k = fits(t); if (k.right > k.inner) { t.innerHTML = '마을 3곳 /<br>1회 훈련'; k = fits(t); }
        return { text: t.innerText, ok: k.right <= k.inner + 1 };
      }
      if (n == 84) {   // 오른쪽 세 칸 글자 크기 통일: 머리글 34px · 본문 46px, 넘치면 의미 단위(가운뎃점)에서 줄바꿈
        const out = [];
        for (const c of cards) {
          const [lab, body] = c.children; lab.style.fontSize = '34px'; body.style.fontSize = '46px'; body.style.lineHeight = '62px';
          let k = fits(body);
          if (k.right > k.inner + 1 || k.lines > (body.querySelectorAll('br').length + 1)) { body.innerHTML = body.innerHTML.replace(' · ', '<br>'); k = fits(body); }
          out.push({ t: body.innerText, ok: k.right <= k.inner + 1, h: c.scrollHeight <= c.clientHeight + 1 });
        }
        return out;
      }
      if (n == 99) {   // 제목 한 줄(계획 수립 · 제출 / 정보공유 · 설명회) — 네 칸 같은 크기로, 회색 설명은 제목 바로 아래 같은 간격
        const titles = cards.map(c => c.children[1]);
        titles.forEach(t => { t.innerHTML = t.innerHTML.replace(/\s*<br[^>]*>\s*/g, ' '); });
        let fs = parseFloat(getComputedStyle(titles[0]).fontSize);
        while (titles.some(t => { const k = fits(t); return k.right > k.inner + 1 || k.lines > 1; }) && fs > 30) { fs -= 0.5; titles.forEach(t => { t.style.fontSize = fs + 'px'; t.style.lineHeight = (fs * 1.25).toFixed(1) + 'px'; }); }
        cards.forEach(c => { c.children[1].style.margin = '16px 0'; c.children[1].style.minHeight = ''; c.children[0].style.minHeight = ''; });
        return { fs, titles: titles.map(t => t.innerText) };
      }
      if (n == 117) {   // 모서리 마크: 다른 장과 같은 크기(43px) · 위치(글자 왼쪽 위)로
        const svg = R.querySelector('svg.a'), head = [...R.querySelectorAll('div.a')].find(d => d.textContent.includes('그래서')); const q = head.getBoundingClientRect();
        svg.outerHTML = `<svg class="a" style="left:${Math.round(q.left - 40)}px;top:${Math.round(q.top - 9)}px" width="43" height="43"><path d="M41.5,11.5 L41.5,1.5 L1.5,1.5 L1.5,41.5 L13.5,41.5" fill="none" stroke="#f4f4f2" stroke-width="3"/></svg>`;
        return { mark: [Math.round(q.left - 40), Math.round(q.top - 9)] };
      }
    }, n);
    console.log(n, JSON.stringify(r));
    fs.writeFileSync(F + '/' + f, '<!doctype html>\n' + await pg.evaluate(() => document.documentElement.outerHTML));
  }
  await br.close();
})();
