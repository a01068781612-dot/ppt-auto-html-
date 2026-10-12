// 상황관리 공감 워크숍 AI 특강(26.10.20) v.1.0.0 — AI특강 v.1.7.2 기반: PART 1(국토부) 삭제, PART 번호 1·2로, 표지·목차 수정, 기사 소개·정리 문구를 영상 내용 기준 문장형(굵게)으로
const path = require("path");
const fs = require("fs");
const pptxgen = require("/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/hf/node_modules/pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/719e1caa-5f70-4d40-92b1-55656730d2af_53739935-c265-48e3-b4de-491f3ca06b06/pptx/scripts/apply_theme.js");

const A = "/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/deck_op2/assets/";
const OUT = process.argv[2];
const M3 = "/tmp/vids/m1020/";
const ST = "/tmp/claude-0/-home-user-ppt-auto-html-/01f805d1-d26c-5b66-83a4-df70d421d547/scratchpad/hf1020/st/";
const b64 = f => "image/png;base64," + fs.readFileSync(f).toString("base64");

// 1920×1080 디자인 기준 → 13.333×7.5in (144px = 1in, 글자 px/2 = pt)
const X = px => px / 144;
const F = px => px / 2;

const THEME = {
  name: "AI Lecture Dark",
  headFontFace: "Pretendard",
  bodyFontFace: "Pretendard",
  colors: {
    dk1: "0C0B0B", lt1: "F4F4F2", dk2: "1D1A19", lt2: "D6D2C9",
    accent1: "FF5A1F", accent2: "A59F98", accent3: "8A847E", accent4: "262321", accent5: "3A3533", accent6: "FF7A45",
    hlink: "FF5A1F", folHlink: "FF7A45",
  },
};
const COL = { fg: "F4F4F2", body: "D6D2C9", cap: "A59F98", dim: "8A847E", acc: "FF5A1F", card: "1D1A19", line: "3A3533", line2: "55504C", bg: "0C0B0B" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "업무 효율을 높이는 AI 활용";
pres.author = "김경훈";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

let N = 0; const VIDS = [];
const ONLY = process.env.ONLY ? process.env.ONLY.split(",").map(Number) : null;
const DUMMY = new Proxy({}, { get: (t, k) => (k === "background" ? undefined : () => DUMMY), set: () => true });
const _addSlide = pres.addSlide.bind(pres); pres.addSlide = (o) => { N++; return (!ONLY || ONLY.includes(N)) ? _addSlide(o) : DUMMY; };
const CLIPDUR = fs.existsSync("/tmp/vids/clips/dur.json") ? JSON.parse(fs.readFileSync("/tmp/vids/clips/dur.json", "utf8")) : {};
pres.defineSlideMaster({ title: "DARK", background: { path: path.join(__dirname, "bg.png") } });
pres.defineSlideMaster({ title: "MOTION", background: { color: "0C0B0B" } });

const T = (slide, text, o) => slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Pretendard", color: COL.fg, valign: "top" }, o));
const line = (slide, x, y, w, h, color) => slide.addShape(pres.shapes.LINE, { x: X(x), y: X(y), w: X(w), h: X(h), line: { color: color || COL.line, width: 0.75 } });

pres.addSection({ title: "오프닝" });

/* 01 기관 표지 — HyperFrames 모션(자동 재생) */
{
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: "오프닝" });
  s.addMedia({ type: "video", path: M3 + "op_cover.mp4", cover: b64(M3 + "op_cover.png"), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "motion_cover" });
  s.addNotes("기관 표지 — 슬라이드에 들어오면 모션이 자동 재생되고 마지막 장면에서 멈춥니다. 2026 하반기 상황관리 공감 워크숍 · AI, 지금 어디까지 왔나 · 업무 효율을 높이는 AI 활용");
}

/* 02 국무회의 인트로 영상 — 클릭하면 전체화면 재생 */
motion(ST + "vintro/out.mp4", ST + "vintro/last.png", "st_vintro", "영상 소개 화면. 다음 클릭(→)에 다음 슬라이드에서 영상이 전체화면으로 자동 재생됩니다.", "오프닝", 7000);

/* 03 인트로 영상 — 슬라이드 전체를 채운 영상, 들어오면 자동 재생 */
{
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: "오프닝" });
  s.background = { color: "000000" };
  s.addMedia({ type: "video", path: A + "video/intro.mp4", cover: b64(path.join(__dirname, "intro_first.png")), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "intro_video" });
  s.addNotes("인트로 영상 — 슬라이드에 들어오면 화면 전체로 자동 재생됩니다. 재생 중에 클릭하면 다음 장으로 넘어가니, 끝날 때까지 기다렸다가 클릭하세요. 블랙 과정 이야기는 영상 뒤에 구두로 설명.");
}

/* 03 강사 소개 1 — 사진 · 지표 · 수상 */
motion(ST + "prof1/out.mp4", ST + "prof1/last.png", "st_prof1", "강사 소개 1. 블랙은 과정 선발·이수 중으로 표기 — 구두로 설명.", "오프닝", 7000);

/* 04 강사 소개 2 — 강의 · 자격 · 언론 */
motion(ST + "prof2/out.mp4", ST + "prof2/last.png", "st_prof2", "강사 소개 2 — 강의·자격·언론. 자세한 자료는 ssca1612.pages.dev 안내.", "오프닝", 7000);

/* 05 목차 — HyperFrames 모션(자동 재생) */
{
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: "오프닝" });
  s.addMedia({ type: "video", path: M3 + "op_toc.mp4", cover: b64(M3 + "op_toc.png"), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "motion_toc" });
  s.addNotes("목차 — 01 2026 AI 트렌드(메인) · 02 기관도 변하고 있다. 모션이 자동 재생됩니다.");
}

/* ───────── PART 1 (AI 트렌드) ───────── */
pres.addSection({ title: "PART 1 AI 트렌드" });
const SEC2 = "PART 1 AI 트렌드";
const CLIPS = "/tmp/vids/clips/";

function motion(file, poster, name, note, sec, dur) {
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: sec });
  s.addMedia({ type: "video", path: file, cover: b64(poster), x: 0, y: 0, w: 13.333, h: 7.5, objectName: name });
  if (!ONLY || ONLY.includes(N)) VIDS.push({ n: N, name, dur: dur || 6000 });
  s.addNotes(note);
  return s;
}
const MOT = "/tmp/vids/m1020/";
function news(id, note) { return motion(MOT + id + ".mp4", MOT + id + ".png", "news_" + id, "📰 영상 소개(실제 기사) — " + note + " → 다음 장에서 영상 재생", SEC2); }
function clip(id, label, note) {
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: SEC2 });
  s.background = { color: "000000" };
  const name = "clip_" + id;
  s.addMedia({ type: "video", path: CLIPS + id + ".mp4", cover: b64(CLIPS + id + ".png"), x: 0, y: 0, w: 13.333, h: 7.5, objectName: name });
  VIDS.push({ n: N, name, dur: Math.round(CLIPDUR[id] * 1000) + 500 });
  s.addNotes("🎬 " + label + " — 들어오면 화면 전체로 자동 재생. 끝까지 본 뒤 클릭. " + (note || ""));
  return s;
}
function summary(o) { return motion(ST + o.id + "/out.mp4", ST + o.id + "/last.png", "st_" + o.id, "📝 정리 — " + o.title + " / KEY: " + o.key, SEC2, 7000); }

// 13 PART 2 인트로
motion(M3 + "p2_intro.mp4", M3 + "p2_intro.png", "motion_p2", "PART 1 인트로 — 1막 왜 → 2막 무엇이 → 3막 신문물", SEC2);

// 14 9월 한 달
motion(ST + "sep/out.mp4", ST + "sep/last.png", "st_sep", "9월 한 달의 신문물 다섯 가지 — 공통점은 대답에서 실행으로. 타임라인이 그려지며 차례로 등장.", "PART 1 AI 트렌드", 7000);

news("n01", "AI 에이전트");
clip("01", "AI 에이전트란 · 코딩알려주는누나");
summary({ id: "sum01", title: "프로그램에 두뇌가 생겼습니다", key: "시키는 프로그램에서, 생각하는 AI로" });
news("n02a", "AX");
clip("02a", "AX · 커리어해커 알렉스");
summary({ id: "sum02a", title: "AI 도입과 AX는 다릅니다", key: "바꿀 것은 도구가 아니라 일하는 방식" });
news("n03", "프롬프트 그다음");
clip("03", "프롬프트 시대는 끝났다 · 커리어해커 알렉스");
summary({ id: "sum03", title: "잘 쓰는 것에서, 맡기는 것으로", key: "잘 묻는 사람보다, 잘 맡기는 사람" });
news("n04", "하네스");
clip("04", "하네스란 · 코딩알려주는누나");
summary({ id: "sum04", title: "프롬프트 → 컨텍스트 → 하네스", key: "AI가 틀 안에서 스스로 고치며 일하게" });

// 23 신문물 지도
motion(M3 + "p2_ladder.mp4", M3 + "p2_ladder.png", "motion_ladder", "3막 신문물 지도 — 시간 순서로 다섯 가지 (Hermes → Aside → Jev → Muse → Dots)", SEC2);

news("n09", "Hermes");
clip("09", "Hermes · Jay Choi");
summary({ id: "sum09", title: "Hermes — 쓸수록 나에게 맞춰지는 AI", key: "한 번 세팅하면, 결과만 받아 봅니다" });
news("n06", "Aside");
clip("06", "Aside · 서퍼스", "세 구간을 이어 붙인 영상입니다.");
summary({ id: "sum06", title: "Aside — 웹을 직접 움직이는 AI", key: "보는 AI에서, 손을 움직이는 AI로" });
news("n05", "Jev");
clip("05", "Jev · 스마트대디");
summary({ id: "sum05", title: "Jev — 빠르게 고르는 AI", key: "빠르게 고르는 반복 업무에 맞습니다" });
news("n07", "Muse");
clip("07", "Muse · Play with AI Lab");
summary({ id: "sum07", title: "Muse — 생활을 대신하는 AI", key: "말하는 AI에서, 일하는 AI로" });
news("n08", "Dots");
clip("08", "Dots · 커리어해커 알렉스 (쇼츠)");
summary({ id: "sum08", title: "Dots — 24시간 일하는 비서", key: "물으면 답하는 AI에서, 알아서 하는 비서로" });

// 34 한눈에 보기
motion(ST + "compare/out.mp4", ST + "compare/last.png", "st_compare", "다섯 가지 비교 — 공통점은 맡기는 구조(하네스). 행이 하나씩 들어오고 Hermes가 강조됩니다.", "PART 1 AI 트렌드", 7000);

news("n10", "리더십·행동");
clip("02b", "기술보다 리더십 · 커리어해커 알렉스");
clip("10", "두려움 없는 행동 · 커리어해커 알렉스");
summary({ id: "sum10", title: "도구보다, 일하는 방식", key: "→ PART 2  다른 기관은 이미 움직이고 있습니다" });

/* ───────── PART 2 (기관의 변화) ───────── */
pres.addSection({ title: "PART 2 기관의 변화" });
{
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: "PART 2 기관의 변화" });
  s.addMedia({ type: "video", path: M3 + "p3_intro.mp4", cover: b64(M3 + "p3_intro.png"), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "motion_p3" });
  s.addNotes("PART 2 인트로 — 제도 → 인사 → 기관장 → 현장 → 한 사람 순서로 보여 줍니다.");
}

// 기사 화면 공통 틀
function article(o) {
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "PART 2 기관의 변화" });
  T(s, [{ text: "PART 3 · " + o.no + "  ", options: { color: COL.acc, bold: true } }, { text: o.tag, options: { color: COL.dim } }], { x: X(110), y: X(92), w: X(1200), h: X(32), fontSize: F(22), charSpacing: 5 });
  const dots = [0, 1, 2, 3, 4, 5].map(i => i);
  dots.forEach(i => s.addShape(pres.shapes.OVAL, { x: X(1810 - (5 - i) * 26 - 12), y: X(100), w: X(12), h: X(12), fill: { color: i === o.idx ? COL.acc : "0C0B0B", transparency: i === o.idx ? 0 : 100 }, line: { color: i === o.idx ? COL.acc : "9A948E", width: 1 } }));
  T(s, o.title, { x: X(110), y: X(134), w: X(1700), h: X(84), fontSize: F(66), fontFace: "Pretendard Black" });
  line(s, 110, 244, 1700, 0, COL.line2);
  const imgLeft = o.imgSide !== "right";
  const ix = imgLeft ? 110 : 1060, tx = imgLeft ? 1000 : 110, tw = 810;
  // 사진 프레임
  s.addShape(pres.shapes.RECTANGLE, { x: X(ix), y: X(290), w: X(750), h: X(560), fill: { type: "none" }, line: { color: COL.line2, width: 1 } });
  s.addShape(pres.shapes.RECTANGLE, { x: X(ix + (imgLeft ? -24 : 750 - 46)), y: X(266), w: X(70), h: X(70), fill: { type: "none" }, line: { color: COL.fg, width: 2.25 } });
  s.addImage({ path: path.join(__dirname, "art", o.img), x: X(ix + 18), y: X(308), w: X(714), h: X(524), sizing: { type: "cover", w: X(714), h: X(524) }, objectName: "article_photo" });
  // 핵심 수치
  let y = 290;
  if (o.big) {
    T(s, [{ text: o.big[0], options: { fontFace: "Pretendard Black", color: COL.acc } }, { text: o.big[1], options: { fontSize: F(48), bold: true, color: COL.fg } }], { x: X(tx), y: X(y), w: X(tw), h: X(150), fontSize: F(140) });
    T(s, o.big[2], { x: X(tx), y: X(y + 156), w: X(tw), h: X(40), fontSize: F(28), color: COL.cap });
    y += 230;
  }
  line(s, tx, y, tw, 0, COL.line2);
  const qh = o.quote ? 190 : 0;
  const rh = Math.min(150, (850 - y - qh) / o.points.length);
  o.points.forEach(([k, v]) => {
    const top = y + (rh - (v ? 84 : 40)) / 2;
    T(s, k, { x: X(tx), y: X(top), w: X(tw), h: X(40), fontSize: F(32), bold: true });
    if (v) T(s, v, { x: X(tx), y: X(top + 48), w: X(tw), h: X(34), fontSize: F(24), color: COL.cap });
    y += rh; line(s, tx, y, tw, 0, COL.line);
  });
  if (o.quote) {
    s.addShape(pres.shapes.RECTANGLE, { x: X(tx), y: X(y + 30), w: X(tw), h: X(150), fill: { color: COL.card }, line: { color: COL.line, width: 0.75 } });
    T(s, "“", { x: X(tx + 28), y: X(y + 30), w: X(60), h: X(90), fontSize: F(90), fontFace: "Pretendard Black", color: COL.acc });
    T(s, o.quote, { x: X(tx + 96), y: X(y + 30), w: X(tw - 124), h: X(150), fontSize: F(30), bold: true, lineSpacingMultiple: 1.25, valign: "middle" });
  }
  // 출처
  line(s, 110, 930, 1700, 0, COL.line);
  T(s, [{ text: "출처  ", options: { color: COL.dim, bold: true } }, { text: o.src, options: { color: COL.cap } }], { x: X(110), y: X(948), w: X(1700), h: X(34), fontSize: F(20) });
  s.addNotes(o.notes);
  return s;
}

["p1","p2","p3","p4","p5"].forEach((p, i) => motion(MOT + "a_" + p + ".mp4", MOT + "a_" + p + ".png", "art_" + p, "PART 2 기사 " + (i + 1) + " — 실제 기사 화면이 들어오고 핵심이 나타납니다.", "PART 2 기관의 변화"));
motion(MOT + "a_act.mp4", MOT + "a_act.png", "art_act", "그래서, 우리 조직은? — 일단 써 보세요. 작은 것부터. (보고서 초안 한 장 · 반복 업무 하나 · 잘 된 것은 공유)", "PART 2 기관의 변화");

/* ───────── 마무리 ───────── */
pres.addSection({ title: "마무리" });
motion(ST + "closing/out.mp4", ST + "closing/last.png", "st_closing", "마무리 메시지 — AI는 선택이 아닌 필수입니다. 도구보다 일하는 방식, 변화는 리더에게서.", "마무리", 7000);
{
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: "마무리" });
  s.background = { color: "000000" };
  s.addMedia({ type: "video", path: A + "video/promo.mp4", cover: b64(path.join(__dirname, "promo_first.png")), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "promo_video" });
  s.addNotes("강사 홍보 영상 — 들어오면 화면 전체로 자동 재생, 마지막 장면(명함·QR)에서 멈춥니다. 끝난 뒤 클릭하면 Q&A.");
}
motion(ST + "qna/out.mp4", ST + "qna/last.png", "st_qna", "Q&A — 명함 QR로 자료 안내. (모션 자동 재생 후 마지막 장면에서 멈춤)", "마무리", 6000);

(async () => {
  fs.writeFileSync(path.join(__dirname, "vids.json"), JSON.stringify(VIDS));
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
