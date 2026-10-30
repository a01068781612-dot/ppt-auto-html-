// 슬라이드 v.2.0.0 조립 (기획안 v.3.2.0) — order.json 순서대로
// 사용: NODE_PATH=<node_modules> HF=<v2 렌더> HF1=<v1 렌더> W1020=<10.20 PPT 압축 푼 폴더> [KAKAO_URL=<오픈채팅 링크>] node build1105v2.cjs raw.pptx
//       → python3 ../제작소스_v.1.0.0(26.10.29)/timing1105.py raw.pptx 최종.pptx
const path = require("path");
const fs = require("fs");
const { execFileSync } = require("child_process");
const pptxgen = require("pptxgenjs");

const HF = process.env.HF, HF1 = process.env.HF1, W1020 = process.env.W1020;
const KAKAO_URL = process.env.KAKAO_URL || "";
const OUT = process.argv[2];
const TMP = path.join(path.dirname(path.resolve(OUT)), "_media"); fs.mkdirSync(TMP, { recursive: true });
const X = px => px / 144, F = px => px / 2;
const QRBOX = { x: 1330, y: 330, s: 420 };
const COL = { fg: "F4F4F2", cap: "A59F98", dim: "8A847E", acc: "FF5A1F", card: "1D1A19", line: "3A3533" };
const b64 = f => "image/png;base64," + fs.readFileSync(f).toString("base64");
const order = JSON.parse(fs.readFileSync(path.join(HF, "order.json"), "utf8"));

// 10.20 워크숍 PPT에서 가져올 장 (장 번호)
const W = { p_vintro: 2, p_intro: 3, p_prof1: 4, p_prof2: 5, p_n01: 9, p_c01: 10, p_art1: 43, p_art2: 44, p_art3: 45, p_promo: 50 };
const FULLVIDEO = new Set(["p_intro", "p_c01", "p_promo"]);   // 영상 장 = 검은 바탕 전체화면

const NOTES = {
  cover: "표지 — 제23기 중견리더과정 · 공무원을 위한 AI 도구 활용법",
  p_vintro: "국무회의 영상 소개 — 다음 장에서 영상이 전체화면 자동 재생",
  p_intro: "🎬 국무회의 인트로 — 끝날 때까지 기다렸다가 클릭",
  room: "단톡방 입장 — QR 찍고 오픈프로필로 입장, 참여코드 안내. 오늘 만든 것을 여기에 올립니다. (카톡 투표 「AI 얼마나 써 보셨나요?」는 선택)",
  toc2: "목차 — 01 정부가 인정한 AI 인재 · 02 폰으로 해 보기(강조) · 03 요즘 AI 트렌드 · 04 말로 만든 업무 도구 · 05 우리 사정은 우리가 안다",
  pa_in: "PART 1 — AI를 잘 쓰는 공무원, 이제 정부가 공식으로 인정합니다",
  champ: "AI 챔피언 — 행안부 인증, 그린→블루→블랙, 5급 조기승진 가점·포상금·연수, 2030년 2만 명. KEY: AI 역량이 공식 경력이 된다",
  p_art1: "📰 AI 잘 쓰는 공무원에 승진·포상 인센티브 (파이낸셜뉴스) — 5급 조기승진 성과심사에서 블랙 가점. 6급에게 가장 와닿는 장",
  p_art2: "📰 경기도 — AI 챔피언 블루·블랙에 실적 가산점 0.5점",
  p_art3: "📰 병무청장 AI 챔피언 간담회 — 기관장이 직접",
  reveal_black: "공개 — “그 최고 등급 BLACK, 오늘 이 자리에 서 있습니다.” 외부와 비교하는 말은 하지 않음",
  p_prof1: "강사 소개 1", p_prof2: "강사 소개 2 — 자세한 자료는 ssca1612.pages.dev",
  pb_in: "PART 2 — 폰을 꺼내 주세요. 막히면 옆 사람과",
  m_ocr: "미션 1 OCR — 교육생: Gemini 카메라로 공문 찍기 → “텍스트로만 줘” → 복사 → 단톡방에 붙이기",
  ocr_flow: "강사 실시간 시연 — 폰 Gemini 촬영 → 노트북 gemini.google.com(같은 계정) → 복사 → 한글 붙여 넣기. 예비: 멀티 컨트롤 복사·붙여 넣기",
  v_gemini: "🎬 Gemini 사진 편집 소개 영상 자리 — 강사가 내려받은 영상으로 교체",
  m_photo: "미션 2 사진 — 배경 바꾸기·흑백 복원·포스터. 다 되면 저장(미션 3에서 씀) → 단톡방",
  v_flow: "🎬 Flow 소개 영상 자리 — 강사가 내려받은 영상으로 교체",
  m_flow: "미션 3 Flow — 앱 설치(안 되면 labs.google/flow) → 로그인 → 새로 만들기 → 미션 2 사진 + 움직임 → 빠른 품질 → 만드는 동안 쉬는 시간",
  break: "쉬는 시간 — 영상 완성되면 단톡방에",
  flow_show: "Flow 결과 보기 — 단톡방 영상 몇 편 화면으로, 잘 된 요청문 나누기",
  pc_in: "PART 3 — 방금 쉬는 동안에도 AI가 일했습니다",
  p_n01: "📰 AI 에이전트 기사", p_c01: "🎬 AI 에이전트란 · 코딩알려주는누나",
  sum01: "정리 — 프로그램에 두뇌가 생겼습니다", ladder: "신문물 지도 1분", compare: "우리 일에 빗대면 — 시간 없으면 넘김",
  pd_in: "PART 4 — 코딩은 모릅니다. 업무가 불편해서 말로 만들었습니다",
  tools: "업무 도구 소개 → 노트북으로 전환해 국토부 도구 1·3 실제 시연. (선택) 「작업」 모드",
  pe_in: "PART 5 — 사무실 PC에서 안 열리죠. 저도 그렇습니다",
  blocked: "손들기: 사무실 PC에서 챗GPT 열리시나요? → 업무망·인터넷망 분리",
  safe2: "넣어도 되는 것 / 안 되는 것 — 오늘 OCR·단톡방과 연결",
  n2sf: "국가망보안체계(N2SF) — 기밀·민감·공개. 정확한 적용은 소속 기관 지침",
  m4: "AI가 틀린 곳 찾기 — 손들고 말하기", m4ans: "정답 — 숫자·출처는 사람이",
  act: "일단 써 보세요. 작은 것부터.",
  next: "“정부가 인정한 AI 인재, 다음은 여러분입니다.” 단톡방에 「내일 해 볼 것 하나」",
  closing: "마무리", p_promo: "🎬 강사 홍보 영상 — 끝나면 Q&A", qna: "Q&A",
};
const SEC = id => (["cover", "p_vintro", "p_intro", "room", "toc2"].includes(id) ? "오프닝" :
  ["pa_in", "champ", "p_art1", "p_art2", "p_art3", "reveal_black", "p_prof1", "p_prof2"].includes(id) ? "PART 1 정부가 인정한 AI 인재" :
  ["pb_in", "m_ocr", "ocr_flow", "v_gemini", "m_photo", "v_flow", "m_flow", "break", "flow_show"].includes(id) ? "PART 2 폰으로 해 보기" :
  ["pc_in", "p_n01", "p_c01", "sum01", "ladder", "compare"].includes(id) ? "PART 3 요즘 AI 트렌드" :
  ["pd_in", "tools"].includes(id) ? "PART 4 말로 만든 업무 도구" :
  ["pe_in", "blocked", "safe2", "n2sf", "m4", "m4ans"].includes(id) ? "PART 5 우리 사정은 우리가 안다" : "마무리");

const dur = f => Math.round(parseFloat(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString()) * 1000);
const frame = (f, out, last) => { execFileSync("ffmpeg", ["-loglevel", "error", "-y", ...(last ? ["-sseof", "-0.1"] : ["-ss", "0.5"]), "-i", f, "-frames:v", "1", out]); return out; };

function qrImage(name, url, label) {
  const out = path.join(TMP, name + ".png");
  execFileSync("python3", ["-c", `
import sys
from PIL import Image, ImageDraw, ImageFont
out,url,label,font=sys.argv[1:5]
if url:
    import qrcode
    im=qrcode.make(url,border=1,box_size=14,error_correction=qrcode.constants.ERROR_CORRECT_M).convert('RGB').resize((840,840),Image.NEAREST)
else:
    im=Image.new('RGB',(840,840),'#f4f4f2'); d=ImageDraw.Draw(im)
    d.rectangle([30,30,810,810],outline='#ff5a1f',width=10)
    d.text((420,370),label,font=ImageFont.truetype(font,60),fill='#111',anchor='mm'); d.text((420,470),'링크를 받으면 교체',font=ImageFont.truetype(font,40),fill='#8a847e',anchor='mm')
im.save(out)`, out, url, label, process.env.KFONT || "/root/.fonts/Pretendard-Bold.otf"]);
  return out;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; pres.title = "공무원을 위한 AI도구 활용법"; pres.author = "김경훈";
pres.theme = { headFontFace: "Pretendard", bodyFontFace: "Pretendard" };
pres.defineSlideMaster({ title: "DARK", background: { path: path.join(__dirname, "bg.png") } });
pres.defineSlideMaster({ title: "MOTION", background: { color: "0C0B0B" } });
const secs = []; order.forEach(([id]) => { const s = SEC(id); if (!secs.includes(s)) secs.push(s); });
secs.forEach(t => pres.addSection({ title: t }));

let N = 0; const VIDS = []; const LOG = [];
for (const [id, kind] of order) {
  N++;
  const sec = SEC(id); const note = NOTES[id] || id;
  if (kind === "v") {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: sec });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X(110), y: X(110), w: X(1700), h: X(860), fill: { color: COL.card }, line: { color: COL.acc, width: 2, dashType: "dash" }, rectRadius: 0.3 });
    s.addText("📌 새 소개 영상 자리", { x: X(190), y: X(230), w: X(1500), h: X(50), fontSize: F(30), bold: true, color: COL.acc, fontFace: "Pretendard", margin: 0 });
    s.addText(note.replace(/ 자리.*$/, ""), { x: X(190), y: X(310), w: X(1540), h: X(200), fontSize: F(76), bold: true, color: COL.fg, fontFace: "Pretendard", margin: 0, valign: "top" });
    s.addText("강사님이 내려받은 영상 파일을 이 장에 넣어 주세요 (전체 화면 · 자동 재생)", { x: X(190), y: X(600), w: X(1540), h: X(100), fontSize: F(34), color: COL.cap, fontFace: "Pretendard", margin: 0 });
    s.addNotes(note); LOG.push(`${N}\t${id}\t📌 새 영상 자리`); continue;
  }
  let mp4, poster, name;
  if (kind === "p") {
    mp4 = path.join(W1020, "ppt/media", `media-${W[id]}-1.mp4`);
    poster = frame(mp4, path.join(TMP, id + ".png"), !FULLVIDEO.has(id));
    name = (FULLVIDEO.has(id) ? "clip_" : "w_") + id;
  } else {
    const d = path.join(kind === "r" ? HF1 : HF, id);
    mp4 = path.join(d, "out.mp4"); poster = path.join(d, "last.png"); name = "m_" + id;
  }
  const s = pres.addSlide({ masterName: "MOTION", sectionTitle: sec });
  if (FULLVIDEO.has(id)) s.background = { color: "000000" };
  s.addMedia({ type: "video", path: mp4, cover: b64(poster), x: 0, y: 0, w: 13.333, h: 7.5, objectName: name });
  VIDS.push({ n: N, name, dur: dur(mp4) + (FULLVIDEO.has(id) ? 500 : 0) });
  if (id === "room") {
    s.addImage({ path: qrImage("kakao_qr", KAKAO_URL, "단톡방 QR 자리"), x: X(QRBOX.x), y: X(QRBOX.y), w: X(QRBOX.s), h: X(QRBOX.s), objectName: "kakao_qr",
      hyperlink: KAKAO_URL ? { url: KAKAO_URL } : undefined });
  }
  s.addNotes(note); LOG.push(`${N}\t${id}\t${kind}`);
}
fs.writeFileSync(path.join(path.dirname(path.resolve(OUT)), "vids.json"), JSON.stringify(VIDS));
fs.writeFileSync(path.join(path.dirname(path.resolve(OUT)), "slides.tsv"), LOG.join("\n") + "\n");
pres.writeFile({ fileName: OUT }).then(f => console.log("ok", f, N, "slides"));
