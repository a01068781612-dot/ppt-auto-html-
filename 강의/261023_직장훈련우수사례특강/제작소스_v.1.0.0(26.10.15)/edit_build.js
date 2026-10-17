// 글자 수정판 2단계 — edit_extract.js 결과(b###.jpg 배경 + t###.json 글상자)로 글자를 고칠 수 있는 PPT를 만든다. 영상은 넣지 않고 첫 화면만.
// 사용: NODE_PATH=<pptxgenjs가 있는 node_modules> node edit_build.js <추출폴더> <영상 첫 화면 폴더> <OUT.pptx>
// 줄바꿈은 화면 그대로 넣고 자동 줄바꿈은 끔(PowerPoint · LibreOffice 글자 폭 차이로 줄이 밀리지 않게).
// 단위: 1920px = 13.333in → 1px = 1/144in = 0.5pt. 글꼴은 Pretendard 굵기별 이름(Pretendard Black · ExtraBold · SemiBold …).
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

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; pres.title = '현장의 문제가 훈련이 된다 — 직장훈련 우수사례 특강(글자 수정판)'; pres.author = '김경훈';
const SECTION = n => (n <= 6 ? '오프닝' : n <= 40 ? 'PART 1 농골길' : n <= 86 ? 'PART 2 AI 농골길 코치' : n <= 116 ? 'PART 3 조직과 관할로' : '마무리 · Q&A');
let last = '', nbox = 0;
for (let n = 1; n <= 120; n++) {
  const id = String(n).padStart(3, '0'), sec = SECTION(n);
  if (sec !== last) { pres.addSection({ title: sec }); last = sec; }
  const s = pres.addSlide({ sectionTitle: sec }); s.background = { color: '0C0B0B' };
  if (VIDEO[n]) {
    const [k, name, cov] = VIDEO[n];
    s.addImage({ path: path.join(MEDIA, cov), x: 0, y: 0, w: 13.333, h: 7.5, altText: `영상 ${k} 자리: ${name}` });
    s.addNotes(`▶ 영상 ${k} 자리 — ${name} (영상 zip에 들어 있음). 이 장에 영상을 넣고, 들어오면 자동 재생으로 맞춥니다.`);
  } else {
    s.addImage({ path: path.join(E, `b${id}.jpg`), x: 0, y: 0, w: 13.333, h: 7.5 });
    for (const b of JSON.parse(fs.readFileSync(path.join(E, `t${id}.json`), 'utf8'))) {
      const fsMax = Math.max(...b.lines.flat().map(r => r.fs));
      const pitch = b.pitch > 0 ? b.pitch : fsMax * 1.25;
      const glyph = fsMax * 1.2;   // Pretendard 글자 칸 높이(대략)
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
      s.addText(runs, { x: X(x), y: X(y), w: X(w), h: X(h), margin: 0, valign: 'top', align, lineSpacing: PT(pitch), fit: 'none', wrap: false, autoFit: false });
      nbox++;
    }
  }
  LINKS.filter(l => l[0] === n).forEach(([, x, y, w, h, u]) =>
    s.addShape(pres.shapes.RECTANGLE, { x: X(x), y: X(y), w: X(w), h: X(h), fill: { color: 'FFFFFF', transparency: 100 }, line: { type: 'none' }, hyperlink: { url: u, tooltip: '원문 열기' } }));
}
pres.writeFile({ fileName: OUT }).then(f => console.log('ok', f, 'textboxes', nbox));
