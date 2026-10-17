// 분해판 3단계 — split_extract.js · split_prep.py 결과로 모든 요소가 따로 나뉜 PPT를 만든다(영상은 넣지 않고 첫 화면만).
// 사용: NODE_PATH=<pptxgenjs가 있는 node_modules> node split_build.js <분해 폴더> <영상 첫 화면 폴더> <OUT.pptx>
// 개체: 바탕 그림 1장 → 도형(카드 · 테두리 · 선 · 띠, 색 · 크기 수정 가능) · 사진(보이는 부분만 잘라 넣음) · 장식 그림(투명 PNG) · 글상자 순서로 쌓음.
// 줄바꿈은 화면 그대로, 자동 줄바꿈은 끔. 1px = 1/144in = 0.5pt.
const fs = require('fs'), path = require('path');
const pptxgen = require('pptxgenjs');
const [E, MEDIA, OUT] = process.argv.slice(2);
const X = px => px / 144, PT = px => Math.round(px * 0.5 * 10) / 10;

// 영상 장: [영상 번호, 파일 이름, 첫 화면]
const VIDEO = {
  2: [1, '1.오프닝 모션(2장).mp4', 'ws2.png'], 3: [2, '2.국무회의 영상(3장).mp4', 'ws3.png'],
  4: [3, '3.강사 소개1(4장).mp4', 'ws4.png'], 5: [4, '4.강사 소개2(5장).mp4', 'ws5.png'],
  62: [5, '5.AI 농골길 코치 GPTs 화면(62장).mp4', 'gpts.png'], 70: [6, '6.농골길 웹 화면(70장).mp4', 'web.png'],
  119: [7, '7.강사 소개 영상(119장).mp4', 'promo.png'],
};
const ART = { 88: 'http://www.fpn119.co.kr/sub_read.html?uid=240575', 89: 'https://www.idomin.com/news/articleView.html?idxno=946953',
  90: 'https://www.heraldk.com/article/2026032322064737999', 91: 'https://v.daum.net/v/20260324163020234', 92: 'https://www.fpn119.co.kr/249649',
  93: 'https://www.jeonmae.co.kr/news/articleView.html?idxno=1276072', 94: 'https://nocutnews.co.kr/news/6557511' };
const LINKS = [];
Object.entries(ART).forEach(([n, u], i) => { n = +n; LINKS.push([n, 110, 280, 900, 620, u], [n, 1060, 290, 750, 480, u], [n, 1060, 800, 750, 160, u], [87, 110 + i * 246, 300, 226, 560, u]); });
LINKS.push([37, 110, 900, 820, 70, ART[88]], [37, 930, 900, 880, 70, ART[89]], [71, 110, 290, 1150, 647, 'https://nonggolgil.pages.dev/'], [71, 1300, 290, 520, 647, 'https://nonggolgil.pages.dev/'],
  [73, 110, 1030, 1700, 50, 'https://www.kukinews.com/article/view/kuk202512310207'], [120, 1000, 300, 800, 540, 'https://ssca1612.pages.dev/'], [120, 150, 790, 780, 60, 'https://ssca1612.pages.dev/']);

const face = w => w >= 850 ? ['Pretendard Black', false] : w >= 750 ? ['Pretendard ExtraBold', false] : w >= 650 ? ['Pretendard', true]
  : w >= 550 ? ['Pretendard SemiBold', false] : w >= 450 ? ['Pretendard Medium', false] : w >= 350 ? ['Pretendard', false] : ['Pretendard Light', false];
function color(c) {
  const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/); if (!m) return ['F4F4F2', 0];
  const h = [1, 2, 3].map(i => (+m[i]).toString(16).padStart(2, '0')).join('').toUpperCase();
  return [h, m[4] === undefined ? 0 : Math.round((1 - +m[4]) * 100)];
}


function shadowOf(s) {   // "rgba(255, 90, 31, 0.18) 0px 18px 50px 0px" → PowerPoint 바깥 그림자
  const m = s && s.match(/(rgba?\([^)]+\))\s+(-?[\d.]+)px\s+(-?[\d.]+)px\s+([\d.]+)px/); if (!m) return null;
  const [c, tr] = color(m[1]); const dx = +m[2], dy = +m[3];
  return { type: 'outer', color: c, opacity: Math.max(0.01, (100 - tr) / 100), blur: PT(+m[4]), offset: PT(Math.hypot(dx, dy)) || 0.01, angle: Math.round((Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360) };
}

// 개체 이름(선택 창에 보이는 이름) — 무엇인지 알 수 있게
const STEM = f => path.basename(f || '').replace(/\.[^.]+$/, '');
const CUT = (t, n = 14) => { t = (t || '').replace(/\s+/g, ' ').trim(); return t.length > n ? t.slice(0, n) + '…' : t; };
function nameOf(o) {
  const c = ' ' + (o.cls || '') + ' ';
  if (o.t === 'shape') {
    if (o.side) return / key /.test(c) ? 'KEY 띠_주황선' : /^(td|th|tr)$/.test(o.tag) ? '표 줄선' : / shot /.test(c) ? `사진 액자 테두리_${o.side}` : `테두리선_${o.side}`;
    if (/ card hi /.test(c) || (/ card /.test(c) && / hi /.test(c))) return '카드_강조(주황 테두리)';
    if (/ card /.test(c)) return '카드';
    if (/ hl /.test(c)) return '구분선';
    if (/ key /.test(c)) return 'KEY 띠';
    if (/ shot /.test(c)) return / paper /.test(c) ? '문서 액자' : '사진 액자';
    if (/ chip /.test(c)) return '칩';
    if (/ note /.test(c)) return '표시 띠';
    if (/ hlbox /.test(c)) return '강조 상자';
    if (/^(td|th|tr|table)$/.test(o.tag)) return '표 칸';
    if (o.h <= 4 || o.w <= 4) return '선';
    if (o.w <= 60 && o.h <= 60) return o.rad >= Math.min(o.w, o.h) / 2 - 1 ? '점' : '작은 도형';
    return '도형';
  }
  if (o.t === 'img') return (/ paper /.test(c) ? '문서 그림_' : '사진_') + (CUT(o.label, 16) || STEM(o.src));
  if (o.t === 'raster') {
    if (/ ghost /.test(c)) return `영문 제목_${CUT(o.text, 16)}`;
    if (/ lbl /.test(c)) return '사진 설명 띠';
    if (o.cls === 'svg') return o.w <= 80 && o.h <= 80 ? '모서리 마크' : '그래프·도식';
    return '장식';
  }
  return '개체';
}
const textName = b => `${b.role || '글자'}_${CUT(b.lines.map(l => l.map(r => r.text).join('')).join(' '), 18)}`;
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; pres.title = '현장의 문제가 훈련이 된다 — 직장훈련 우수사례 특강(분해판)'; pres.author = '김경훈';
const SECTION = n => (n <= 6 ? '오프닝' : n <= 40 ? 'PART 1 농골길' : n <= 86 ? 'PART 2 AI 농골길 코치' : n <= 116 ? 'PART 3 조직과 관할로' : '마무리 · Q&A');
const cnt = { shape: 0, img: 0, raster: 0, text: 0 };
let last = ''; const TITLES = {};
for (let n = 1; n <= 120; n++) {
  const id = String(n).padStart(3, '0'), sec = SECTION(n);
  if (sec !== last) { pres.addSection({ title: sec }); last = sec; }
  const s = pres.addSlide({ sectionTitle: sec }); s.background = { color: '0C0B0B' };
  if (VIDEO[n]) {
    const [k, name, cov] = VIDEO[n];
    s.addImage({ path: path.join(MEDIA, cov), x: 0, y: 0, w: 13.333, h: 7.5, altText: `영상 ${k} 자리: ${name}`, objectName: `영상 ${k} 자리(첫 화면)` });
    s.addText(`영상 ${k} — ${name.replace(/^\d+\./, '').replace(/\.mp4$/, '')}`, { x: 13.6, y: 0.2, w: 6, h: 0.6, fontFace: 'Pretendard', fontSize: 18, color: 'FFFFFF', objectName: '슬라이드 제목(화면 밖)' });
    TITLES[n] = `영상 ${k} — ${name.replace(/^\d+\./, '').replace(/\.mp4$/, '')}`;
    s.addNotes(`▶ 영상 ${k} 자리 — ${name} (영상 zip에 들어 있음). 이 장에 영상을 넣고, 들어오면 자동 재생으로 맞춥니다.`);
  } else {
    s.addImage({ path: path.join(E, `b${id}.jpg`), x: 0, y: 0, w: 13.333, h: 7.5, altText: '바탕', objectName: '바탕' });
    for (const o of JSON.parse(fs.readFileSync(path.join(E, `o${id}.json`), 'utf8'))) {
      if (o.t === 'shape') {
        const opt = { x: X(o.x), y: X(o.y), w: X(Math.max(o.w, 0.5)), h: X(Math.max(o.h, 0.5)) };
        if (o.fill) { const [c, tr] = color(o.fill); opt.fill = { color: c, transparency: Math.min(100, tr + Math.round((1 - o.op) * 100)) }; } else opt.fill = { type: 'none' };
        if (o.line) { const [c, tr] = color(o.line.c); opt.line = { color: c, width: PT(o.line.w), transparency: tr }; } else opt.line = { type: 'none' };
        const r = Math.min(o.rad, o.w / 2, o.h / 2);
        if (r > 0.5) opt.rectRadius = X(r);
        const sh = shadowOf(o.shadow); if (sh) opt.shadow = sh;
        opt.objectName = nameOf(o); s.addShape(r > 0.5 ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, opt); cnt.shape++;
      } else if (o.t === 'img' && o.file) {
        const opt = { path: path.join(E, o.file), x: X(o.x), y: X(o.y), w: X(o.w), h: X(o.h), altText: '사진', objectName: nameOf(o) };
        if (o.op < 1) opt.transparency = Math.round((1 - o.op) * 100);
        s.addImage(opt); cnt.img++;
      } else if (o.t === 'raster' && o.file && fs.existsSync(path.join(E, o.file))) {
        s.addImage({ path: path.join(E, o.file), x: X(o.x), y: X(o.y), w: X(o.w), h: X(o.h), altText: nameOf(o), objectName: nameOf(o) }); cnt.raster++;
      }
    }
    const tx = JSON.parse(fs.readFileSync(path.join(E, `o${id}.json`), 'utf8')).filter(o => o.t === 'text');
    const tb = tx.find(b => b.role === '제목') || tx.slice().sort((a, b) => (b.fsMax || 0) - (a.fsMax || 0))[0];
    if (tb) { tb.isTitle = true; TITLES[n] = tb.lines.map(l => l.map(r => r.text).join('')).join(' '); }
    for (const b of tx) {
      const fsMax = Math.max(...b.lines.flat().map(r => r.fs));
      const pitch = b.pitch > 0 ? b.pitch : fsMax * 1.25, glyph = fsMax * 1.2;
      const y = b.y - Math.max(0, (pitch - glyph) / 2), h = b.lines.length * pitch;
      const extra = Math.max(b.w * 0.06, fsMax * 0.6);
      const align = b.align === 'center' ? 'center' : (b.align === 'right' || b.align === 'end') ? 'right' : 'left';
      let x = b.x, w = b.w + extra;
      if (align === 'center') x = b.x - extra / 2; else if (align === 'right') x = b.x - extra;
      x = Math.max(0, x); w = Math.min(w, 1920 - x);
      const runs = [];
      b.lines.forEach((line, li) => line.forEach((r, ri) => {
        const [ff, bold] = face(r.fw), [c, tr] = color(r.color);
        const o = { fontFace: ff, bold, italic: r.it, fontSize: PT(r.fs), color: c, charSpacing: PT(r.ls) || 0 };
        if (tr) o.transparency = tr;
        if (ri === line.length - 1 && li < b.lines.length - 1) o.breakLine = true;
        runs.push({ text: r.text, options: o });
      }));
      s.addText(runs, { x: X(x), y: X(y), w: X(w), h: X(h), margin: 0, valign: 'top', align, lineSpacing: PT(pitch), fit: 'none', wrap: false, autoFit: false, objectName: b.isTitle ? '슬라이드 제목' : textName(b) });
      cnt.text++;
    }
  }
  LINKS.filter(l => l[0] === n).forEach(([, x, y, w, h, u]) =>
    s.addShape(pres.shapes.RECTANGLE, { x: X(x), y: X(y), w: X(w), h: X(h), fill: { color: 'FFFFFF', transparency: 100 }, line: { type: 'none' }, hyperlink: { url: u, tooltip: '원문 열기' }, objectName: '링크_원문 열기' }));
}
fs.writeFileSync(OUT.replace(/\.pptx$/, '_titles.json'), JSON.stringify(TITLES));   // split_titles.py가 슬라이드 이름 · 제목 자리로 씀
pres.writeFile({ fileName: OUT }).then(f => console.log('ok', f, JSON.stringify(cnt)));
