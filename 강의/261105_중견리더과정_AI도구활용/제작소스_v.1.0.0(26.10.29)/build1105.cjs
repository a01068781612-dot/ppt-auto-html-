// 중견리더과정 「공무원을 위한 AI도구 활용법 소개」(26.11.05) PPT 조립 v.1.0.0
// 사용: NODE_PATH=<node_modules> HF=<모션 렌더 폴더> [VOTE_URL=<투표 배포 주소>] node build1105.cjs raw.pptx
//       → python3 timing1105.py raw.pptx 최종.pptx  (모션 자동 재생)
// 10.20 워크숍 PPT에 있는 영상·사진 장면은 📌 자리표시 슬라이드로 넣는다 (강사가 그 장을 복사해 바꿔 끼움)
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const HF = process.env.HF;
const OUT = process.argv[2];
const VOTE_URL = process.env.VOTE_URL || "";
const HERE = __dirname;
const X = px => px / 144;          // 1920×1080 px → 13.333×7.5 in
const F = px => px / 2;            // px → pt
const QRBOX = { x: 1330, y: 330, s: 420 };   // gen1105.py의 QRBOX와 같게
const COL = { fg: "F4F4F2", body: "D6D2C9", cap: "A59F98", dim: "8A847E", acc: "FF5A1F", card: "1D1A19", line: "3A3533" };
const b64 = f => "image/png;base64," + fs.readFileSync(f).toString("base64");
const scenes = Object.fromEntries(JSON.parse(fs.readFileSync(path.join(HF, "scenes.json"), "utf8")));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "공무원을 위한 AI도구 활용법";
pres.author = "김경훈";
pres.theme = { headFontFace: "Pretendard", bodyFontFace: "Pretendard" };
pres.defineSlideMaster({ title: "DARK", background: { path: path.join(HERE, "bg.png") } });
pres.defineSlideMaster({ title: "MOTION", background: { color: "0C0B0B" } });

let N = 0; const VIDS = []; const LOG = [];
const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Pretendard", color: COL.fg, valign: "top" }, o));

// 투표 QR (배포 주소가 없으면 자리표시 그림)
let VOTE_QR = path.join(HF, "_qr", "vote.png");
function voteQR() {
  if (fs.existsSync(VOTE_QR) && fs.statSync(VOTE_QR).mtimeMs > Date.now() - 60e3) return VOTE_QR;
  const { execFileSync } = require("child_process");
  execFileSync("python3", ["-c", `
import sys
from PIL import Image, ImageDraw, ImageFont
url=sys.argv[2]
if url:
    import qrcode
    im=qrcode.make(url,border=1,box_size=14,error_correction=qrcode.constants.ERROR_CORRECT_M).convert('RGB')
    im=im.resize((840,840),Image.NEAREST)
else:
    im=Image.new('RGB',(840,840),'#f4f4f2'); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(sys.argv[3],64); g=ImageFont.truetype(sys.argv[3],40)
    d.rectangle([30,30,810,810],outline='#ff5a1f',width=10)
    d.text((420,360),'투표 QR 자리',font=f,fill='#111',anchor='mm'); d.text((420,470),'배포 주소를 받으면 교체',font=g,fill='#8a847e',anchor='mm')
im.save(sys.argv[1])`, VOTE_QR, VOTE_URL, process.env.KFONT || "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"]);
  return VOTE_QR;
}

function motion(id, sec, note, opt = {}) {
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: sec }); N++;
  const d = path.join(HF, id);
  s.addMedia({ type: "video", path: path.join(d, "out.mp4"), cover: b64(path.join(d, "last.png")), x: 0, y: 0, w: 13.333, h: 7.5, objectName: "m_" + id });
  VIDS.push({ n: N, name: "m_" + id, dur: Math.round(scenes[id] * 1000) });
  if (opt.qr) {
    s.addImage({ path: voteQR(), x: X(QRBOX.x), y: X(QRBOX.y), w: X(QRBOX.s), h: X(QRBOX.s), objectName: "vote_qr",
      hyperlink: VOTE_URL ? { url: VOTE_URL + "?v=screen", tooltip: "강사 화면(실시간 결과) 열기" } : undefined });
  }
  s.addNotes(note);
  LOG.push(`${N}\t${id}\t${note.split("\n")[0]}`);
  return s;
}

// 📌 10.20 PPT·원본 자리표시
function slot(sec, title, from, note) {
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: sec }); N++;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X(110), y: X(110), w: X(1700), h: X(860), fill: { color: "1D1A19" }, line: { color: COL.acc, width: 2, dashType: "dash" }, rectRadius: 0.3 });
  T(s, "📌 바꿔 끼울 장", { x: X(190), y: X(220), w: X(1500), h: X(50), fontSize: F(30), bold: true, color: COL.acc, charSpacing: 4 });
  T(s, title, { x: X(190), y: X(300), w: X(1540), h: X(200), fontSize: F(84), bold: true });
  T(s, from, { x: X(190), y: X(560), w: X(1540), h: X(260), fontSize: F(36), color: COL.cap, lineSpacingMultiple: 1.4 });
  s.addNotes("📌 자리표시 — " + from + "\n" + (note || ""));
  LOG.push(`${N}\t📌\t${title} ← ${from}`);
  return s;
}

// AI 사진 퀴즈 (사진은 강사가 넣음)
function photo(n) {
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "오프닝" }); N++;
  T(s, [{ text: "OPENING · 퀴즈  ", options: { color: COL.acc, bold: true } }, { text: `AI 사진 vs 진짜 사진`, options: { color: COL.dim } }],
    { x: X(110), y: X(80), w: X(900), h: X(40), fontSize: F(22), charSpacing: 2 });
  T(s, `Q${n}`, { x: X(110), y: X(140), w: X(400), h: X(200), fontSize: F(190), bold: true, color: COL.acc });
  T(s, "AI가 만든 사진일까,\n진짜 사진일까?", { x: X(110), y: X(400), w: X(560), h: X(220), fontSize: F(56), bold: true, lineSpacingMultiple: 1.25 });
  T(s, [{ text: "폰에서 ", options: {} }, { text: "1 AI다", options: { bold: true, color: COL.fg } }, { text: "  /  ", options: {} }, { text: "2 진짜다", options: { bold: true, color: COL.fg } }],
    { x: X(110), y: X(700), w: X(560), h: X(60), fontSize: F(36), color: COL.cap });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X(760), y: X(110), w: X(1050), h: X(860), fill: { color: "1D1A19" }, line: { color: COL.line, width: 1.5 }, rectRadius: 0.25 });
  T(s, `사진 ${n} 넣기\n(이 상자 위에 사진을 놓고 상자는 지우세요)`, { x: X(760), y: X(470), w: X(1050), h: X(140), fontSize: F(34), color: COL.dim, align: "center" });
  s.addNotes(`사진 퀴즈 Q${n} — 강사 화면(?v=screen)에서 '${n}번 사진은?' 문제로 넘긴 뒤 투표. 정답 공개는 강사 화면에서 R.\n사진 고르는 법: 진짜 3장 + AI 2장 정도. 마지막 Q5는 강사 본인 사진(AI 편집본)으로 반전.`);
  LOG.push(`${N}\t퀴즈\tQ${n} 사진 자리`);
}

const S0 = "오프닝", S1 = "PART 1 도구 지도", S2 = "PART 2 폰 실습", S3 = "PART 3 만들기", S4 = "PART 4 AI는 지금", S5 = "PART 5 리더", S6 = "마무리";
[S0, S1, S2, S3, S4, S5, S6].forEach(t => pres.addSection({ title: t }));

/* ───── 오프닝 ───── */
motion("cover", S0, "표지 — 제23기 중견리더과정 · 공무원을 위한 AI 도구 활용법. 모션이 자동 재생되고 마지막 장면에서 멈춥니다.");
slot(S0, "영상 소개 — 국무회의", "10.20 워크숍 PPT 2장 (영상 소개 모션)");
slot(S0, "🎬 국무회의 인트로 영상", "10.20 워크숍 PPT 3장 (전체화면 자동 재생 영상)");
motion("poll1", S0, "📱 실시간 투표 ① — 강사 화면(?v=screen)에서 'AI, 얼마나 써 보셨나요?'로 넘긴 뒤 QR을 찍게 합니다.\n결과는 강사 화면으로 전환(Alt+Tab)해서 보여 주고 다시 PPT로. 이 결과는 마무리에서 다시 비교합니다.", { qr: true });
motion("quiz", S0, "AI 사진 vs 진짜 사진 퀴즈 안내 — 사진 다섯 장, 폰으로 하나씩 투표. 정답률이 절반을 넘을까요?");
[1, 2, 3, 4, 5].forEach(photo);
slot(S0, "강사 소개 1", "10.20 워크숍 PPT 4장 (사진·지표·수상 모션)");
slot(S0, "강사 소개 2", "10.20 워크숍 PPT 5장 (강의·자격·언론 모션)");
motion("toc", S0, "목차 — 01 도구 지도 · 02 폰으로 해 보기(강조) · 03 노트북으로 만들기 · 04 AI는 지금 어디까지 · 05 리더가 알아야 할 것");

/* ───── PART 1 도구 지도 ───── */
motion("p1in", S1, "PART 1 인트로 — 도구가 너무 많습니다. 딱 이것만 아시면 됩니다.");
motion("toolmap", S1, "용도별 도구 지도 — 묻고 쓰기 / 자료 정리 / 만들기 / 그림·영상. Flow는 유료 위주라 강사 시연만.");
slot(S1, "국토부 실습 원본 ★장면", "「AI 활용 보고서 PPT 작성_국토부_26.9.7._v.2.0」 ★50 프롬프트 6요소 · ★57 딥리서치 · ★65 캔버스 · ★75 Gems · ★85 스튜디오 · ★101 결과물 5종 · ★20 Before/After", "원본에서 해당 장을 복사해 이 자리에 붙여 넣고, 2~4초씩 빠르게 넘깁니다.");
motion("freepaid", S1, "무료 vs 유료 — 오늘 실습은 전부 무료. 유료(월 3만 원 안팎)는 더 많이·더 빠르게. 매일 쓰게 되면 그때.");
motion("apps", S1, "오늘 폰에 깔 앱 — ChatGPT·Gemini(필수), NotebookLM·클로바노트(선택). 각 QR을 찍으면 바로 열립니다. 구글 계정 하나면 Gemini·NotebookLM 로그인.");

/* ───── PART 2 폰 실습 ───── */
motion("p2in", S2, "PART 2 인트로 — 폰을 꺼내 주세요. 막히면 옆 사람과 함께. (와이파이 이름·비밀번호를 말로 안내)");
motion("m1", S2, "미션 1 — ChatGPT 카메라로 실습 카드 뒷면 표를 찍고 '엑셀 표로 만들어 줘'. 강사가 먼저 시연 → 따라 하기 → 잘된 결과 1~2명 자랑.");
motion("m2", S2, "미션 2 — Gemini에서 내 사진 바꾸기(증명사진·캐리커처·여행 사진). 보너스: 흑백 가족사진 컬러 복원. 가장 반응이 좋은 미션 — 넉넉히.");
motion("m3", S2, "미션 3 — Gemini Live(물결 아이콘) 또는 ChatGPT 음성. 말로 묻기 → 카메라로 보여 주며 묻기. 사투리도 OK.");
motion("m4", S2, "미션 4 — AI가 틀린 곳 찾기. 세 카드를 읽고 어디가 틀렸는지 손들어 말하게 합니다.");
motion("m4ans", S2, "정답 — ① 맥북은 2006년(실제 화제가 된 AI 답변) ② 경남 인구 약 320만, 도청 본청은 창원(여기는 서부청사) ③ 2023년 미국 변호사가 AI가 지어낸 판례를 냈다가 벌금. → 확인은 사람이.");

/* ───── PART 3 노트북으로 만들기 ───── */
motion("p3in", S3, "PART 3 인트로 — 코딩 몰라도 말로 프로그램을 만듭니다.");
motion("showcase", S3, "강사 완성품 — 노트북으로 전환해 국토부 실습 도구 1(엑셀→그래프)·도구 3(취합 검증) 실제 시연.");
motion("order", S3, "주문 받기 — 손을 들어 고르거나 직접 주문. Claude에 요청을 넣고 바로 쉬는 시간으로. (실패 대비 완성본은 노트북에 준비)");
motion("break", S3, "쉬는 시간 — 이 화면을 띄워 두거나, Claude가 만드는 화면을 띄워 둡니다.");
motion("share", S3, "결과 공개 — Claude 게시(Publish) → 링크 복사 → 크롬 주소창 공유 → QR 코드 만들기 → 교육생이 폰으로 열기. 한 번 더 고쳐 달라고 해 보기.");
motion("reveal", S3, "반전 — 처음에 투표한 그 페이지도 AI가 만들었습니다. 요청문 한 줄을 읽어 줍니다.");
motion("sum_p3", S3, "정리 — 말로 주문 / 다시 말하면 됨 / 링크 하나로 공유. KEY: 만드는 사람에서, 맡기는 사람으로 → PART 4");

/* ───── PART 4 AI는 지금 어디까지 ───── */
motion("p4in", S4, "PART 4 인트로 — 방금 AI가 쉬는 시간에 일했습니다. 이게 요즘 AI입니다.");
slot(S4, "📰 AI 에이전트 기사", "10.20 워크숍 PPT 9장 (기사 소개 모션)");
slot(S4, "🎬 AI 에이전트란 · 코딩알려주는누나", "10.20 워크숍 PPT 10장 (영상)");
motion("sum01", S4, "정리 ① 프로그램에 두뇌가 생겼습니다 — KEY: 시키는 프로그램에서, 생각하는 AI로");
slot(S4, "📰 프롬프트 그다음 기사", "10.20 워크숍 PPT 15장 (기사 소개 모션)", "시간이 넘치면 이 장부터 38장까지(프롬프트 꼭지) 건너뜁니다.");
slot(S4, "🎬 프롬프트 시대는 끝났다 · 커리어해커 알렉스", "10.20 워크숍 PPT 16장 (영상)");
motion("sum03", S4, "정리 — 잘 쓰는 것에서, 맡기는 것으로. KEY: 잘 묻는 사람보다, 잘 맡기는 사람");
motion("ladder", S4, "신문물 지도 — 영상 없이 1분 설명: Hermes → Aside → Jev → Muse → Dots (시간 순서)");
motion("compare", S4, "다섯 가지 신문물, 우리 일에 빗대면 — 시간 남으면 짚고, 없으면 넘깁니다.");

/* ───── PART 5 리더가 알아야 할 것 ───── */
motion("p5in", S5, "PART 5 인트로 — 곧 결재하는 자리. AI를 어떻게 볼 것인가.");
slot(S5, "다른 기관 사례 ① 기관장", "10.20 워크숍 PPT 45장 (병무청 AI챔피언 간담회 기사 사진)");
slot(S5, "다른 기관 사례 ② 현장 공무원", "10.20 워크숍 PPT 46장 (「AI로 일하는 공무원들」 기사 사진)");
slot(S5, "다른 기관 사례 ③ 한 사람이 바꾼 판", "10.20 워크숍 PPT 47장 (기사 사진)");
motion("security", S5, "보안 3원칙 — 개인정보 / 비공개 문서 원문 / 결재 전 자료. 가명·요약으로 바꿔서, 기관 지침 먼저.");
motion("ox", S5, "📱 O/X 투표 — 강사 화면에서 O/X 1~4번 문제를 차례로 넘기며 투표 → R로 정답 공개.", { qr: true });
motion("oxans", S5, "정답 — 공개된 것은 O(보도자료·법령), 사람·비밀은 X(민원인 정보·결재 전 예산안).");
motion("review", S5, "직원이 AI로 만든 결과물 보는 법 — 출처 / 숫자 / 과정. AI를 썼는지보다 확인했는지를 물어보세요.");

/* ───── 마무리 ───── */
motion("poll2", S6, "📱 다시 투표 — 강사 화면에서 '처음과 지금, 달라졌나요?'로 넘기면 처음 투표 결과와 나란히 보입니다.", { qr: true });
motion("act", S6, "일단 써 보세요. 작은 것부터. — 보고서 초안 한 장 · 반복 업무 하나 · 잘 된 것은 공유");
motion("tomorrow", S6, "📱 한 줄 약속 — 강사 화면에서 '내일 출근해서 해 볼 것 하나'로 넘기면 적은 글이 화면에 모입니다. 두세 개 읽어 줍니다.", { qr: true });
motion("closing", S6, "마무리 — AI는 선택이 아닌 필수입니다. 써 보기 · 만들기 · 지키기");
slot(S6, "🎬 강사 홍보 영상", "10.20 워크숍 PPT 50장 (전체화면 자동 재생 영상)", "영상이 끝나면 다음 장 Q&A로.");
motion("qna", S6, "Q&A — 웹 프로필 QR(ssca1612.pages.dev)을 띄운 채로 질문을 받습니다.");

fs.writeFileSync(path.join(path.dirname(path.resolve(OUT)), "vids.json"), JSON.stringify(VIDS));
fs.writeFileSync(path.join(path.dirname(path.resolve(OUT)), "slides.tsv"), LOG.join("\n") + "\n");
pres.writeFile({ fileName: OUT }).then(f => console.log("ok", f, N, "slides"));
