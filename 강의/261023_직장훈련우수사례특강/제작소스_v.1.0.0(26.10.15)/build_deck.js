// 직장훈련특강 전체 PPT(114장) 조립 — 기획안 v.3.3.0 기준
// 사용: NODE_PATH=<node_modules> node build_deck.js <작업폴더> <raw.pptx>
//   작업폴더/img/s001.jpg … s114.jpg  : p1_v32 · p2_v32 · p3_v35 로 렌더한 1920×1080 장면
//   작업폴더/media/                   : 영상(op2~op5 · 농골길 GPTs/웹 무음 · 홍보 영상)과 첫 화면 이미지
// 영상 장은 들어오면 자동 재생(timing.py가 p:timing 추가). 기사 장은 사진 · 제목 · QR을 누르면 원문이 열림.
const path = require("path");
const pptxgen = require("pptxgenjs");
const W = process.argv[2], OUT = process.argv[3];
const X = px => px / 144;                         // 1920×1080 px → 13.333×7.5 in
const img = n => path.join(W, "img", `s${String(n).padStart(3, "0")}.jpg`);
const med = f => path.join(W, "media", f);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "현장의 문제가 훈련이 된다 — 직장훈련 우수사례 특강";
pres.author = "김경훈";

// 영상 장: [장 번호, 영상, 첫 화면, 이름(timing.py 길이 표), 메모]
const VIDEO = {
  2: ["op2.mp4", "op2.png", "op2_motion", "구조구급 PPT 2번 그대로 — 국무회의 영상 소개 모션"],
  3: ["op3.mp4", "op3.png", "intro_video", "구조구급 PPT 3번 — 국무회의 영상(2:44) 자동 재생"],
  4: ["op4.mp4", "op4.png", "op4_motion", "강사 소개 1 (10.08판 모션 — 워크숍판 파일 받으면 교체)"],
  5: ["op5.mp4", "op5.png", "op5_motion", "강사 소개 2 (10.08판 모션 — 워크숍판 파일 받으면 교체)"],
  56: ["농골길_gpts_무음.mp4", "gpts.png", "gpts_video", "AI 농골길 코치(GPTs) 실제 화면 — 무음, 자동 재생"],
  64: ["농골길_웹_무음.mp4", "web.png", "web_video", "농골길 웹 화면 녹화 — 무음, 자동 재생. 다음 장에서 실제 접속(비밀번호는 강사가 입력)"],
  113: ["promo.mp4", "promo.png", "promo_video", "강사 홍보 영상(1:22) — 자동 재생, 마지막 장면(명함·QR)에서 멈춤. 끝나면 클릭해서 Q&A"],
};

// 링크: [장 번호, x, y, w, h(px), 주소]
const ART = {
  82: "http://www.fpn119.co.kr/sub_read.html?uid=240575",
  83: "https://www.idomin.com/news/articleView.html?idxno=946953",
  84: "https://www.heraldk.com/article/2026032322064737999",
  85: "https://v.daum.net/v/20260324163020234",
  86: "https://www.fpn119.co.kr/249649",
  87: "https://www.jeonmae.co.kr/news/articleView.html?idxno=1276072",
  88: "https://nocutnews.co.kr/news/6557511",
};
const LINKS = [];
Object.entries(ART).forEach(([n, u], i) => {
  n = +n;
  LINKS.push([n, 110, 280, 900, 620, u], [n, 1060, 290, 750, 480, u], [n, 1060, 800, 750, 160, u]);
  LINKS.push([81, 110 + i * 246, 300, 226, 560, u]);
});
LINKS.push([37, 110, 875, 820, 50, ART[82]], [37, 930, 875, 880, 50, ART[83]]);
LINKS.push([65, 110, 290, 1150, 647, "https://nonggolgil.pages.dev/"], [65, 1300, 340, 510, 60, "https://nonggolgil.pages.dev/"]);
LINKS.push([67, 110, 1030, 1700, 50, "https://www.kukinews.com/article/view/kuk202512310207"]);
LINKS.push([114, 1000, 300, 800, 540, "https://ssca1612.pages.dev/"], [114, 150, 790, 780, 60, "https://ssca1612.pages.dev/"]);

const SECTION = n => (n <= 6 ? "오프닝" : n <= 40 ? "PART 1 농골길" : n <= 80 ? "PART 2 AI 농골길 코치" : n <= 110 ? "PART 3 조직과 관할로" : "마무리 · Q&A");
let last = "";
for (let n = 1; n <= 114; n++) {
  const sec = SECTION(n);
  if (sec !== last) { pres.addSection({ title: sec }); last = sec; }
  const s = pres.addSlide({ sectionTitle: sec });
  s.background = { color: "0C0B0B" };
  if (VIDEO[n]) {
    const [v, cov, name, note] = VIDEO[n];
    s.addMedia({ type: "video", path: med(v), cover: "image/png;base64," + require("fs").readFileSync(med(cov)).toString("base64"),
      x: 0, y: 0, w: 13.333, h: 7.5, objectName: name });
    s.addNotes(note);
  } else {
    s.addImage({ path: img(n), x: 0, y: 0, w: 13.333, h: 7.5 });
  }
  LINKS.filter(l => l[0] === n).forEach(([, x, y, w, h, u]) =>
    s.addShape(pres.shapes.RECTANGLE, { x: X(x), y: X(y), w: X(w), h: X(h), fill: { color: "FFFFFF", transparency: 100 }, line: { type: "none" }, hyperlink: { url: u, tooltip: "원문 열기" } }));
}
pres.writeFile({ fileName: OUT }).then(f => console.log("ok", f));
