/**
 * 중견리더과정 AI 특강(26.11.05) 실시간 투표 — Google Apps Script 웹 앱 v.1.0.0
 *
 *  - 교육생 폰:  배포 주소 그대로            (…/exec)
 *  - 강사 화면:  배포 주소 뒤에 ?v=screen    (…/exec?v=screen)  → 문제 넘기기·정답 공개·초기화
 *
 * 설치: 같은 폴더의 설치안내 문서 참고 (script.google.com → 새 프로젝트 → 파일 3개 붙여 넣기 → 배포)
 */

// 강사 화면에서 처음 한 번 입력하는 비밀번호 (교육생이 문제를 넘기지 못하게)
const ADMIN_PIN = '1105';

// 문제 목록 — 순서 = 강의 순서. answer: 정답 보기 번호(0부터), 없으면 null
const QUESTIONS = [
  { id: 'q1', part: '오프닝', title: 'AI, 얼마나 써 보셨나요?', type: 'choice',
    options: ['아직 한 번도 안 써 봤다', '몇 번 써 봤다', '매주 쓴다', '업무에도 쓴다'], answer: null },

  // AI 사진 vs 진짜 사진 — 사진을 정하면 answer를 0(AI다) 또는 1(진짜다)로 바꾼다
  { id: 'p1', part: '사진 퀴즈', title: '1번 사진은?', type: 'choice', options: ['AI다', '진짜다'], answer: null },
  { id: 'p2', part: '사진 퀴즈', title: '2번 사진은?', type: 'choice', options: ['AI다', '진짜다'], answer: null },
  { id: 'p3', part: '사진 퀴즈', title: '3번 사진은?', type: 'choice', options: ['AI다', '진짜다'], answer: null },
  { id: 'p4', part: '사진 퀴즈', title: '4번 사진은?', type: 'choice', options: ['AI다', '진짜다'], answer: null },
  { id: 'p5', part: '사진 퀴즈', title: '5번 사진은? (강사 사진)', type: 'choice', options: ['AI다', '진짜다'], answer: null },

  // PART 5 — 이건 AI에 넣어도 될까?
  { id: 'o1', part: 'O / X', title: '이미 배포한 보도자료 요약', type: 'choice', options: ['O 넣어도 된다', 'X 안 된다'], answer: 0 },
  { id: 'o2', part: 'O / X', title: '민원인 이름·연락처가 있는 민원서', type: 'choice', options: ['O 넣어도 된다', 'X 안 된다'], answer: 1 },
  { id: 'o3', part: 'O / X', title: '누구나 보는 법령 질문', type: 'choice', options: ['O 넣어도 된다', 'X 안 된다'], answer: 0 },
  { id: 'o4', part: 'O / X', title: '결재 전 내년 예산안 원본', type: 'choice', options: ['O 넣어도 된다', 'X 안 된다'], answer: 1 },

  // 마무리
  { id: 'q2', part: '마무리', title: '처음과 지금, 달라졌나요?', type: 'choice',
    options: ['아직 잘 모르겠다', '집에 가서 다시 해 보겠다', '내일 업무에 써 보겠다', '오늘 처음 무언가 만들어 봤다'], answer: null, compare: 'q1' },
  { id: 't1', part: '마무리', title: '내일 출근해서 해 볼 것 하나', type: 'text', options: [], answer: null },
];

const MAX_TEXT = 60;      // 한 줄 약속 최대 글자 수
const MAX_TEXTS = 80;     // 화면에 모을 최대 개수
const CACHE_SEC = 21600;  // 6시간

function doGet(e) {
  const v = (e && e.parameter && e.parameter.v) || '';
  const t = HtmlService.createTemplateFromFile(v === 'screen' ? 'screen' : 'vote');
  t.questionsJson = JSON.stringify(QUESTIONS);
  t.voteUrl = ScriptApp.getService().getUrl();
  return t.evaluate()
    .setTitle(v === 'screen' ? 'AI 특강 — 강사 화면' : 'AI 특강 투표')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, maximum-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ───── 저장소: 캐시(빠름) + 스크립트 속성(보관) ─────
function load_(key, def) {
  const c = CacheService.getScriptCache().get(key);
  if (c) return JSON.parse(c);
  const p = PropertiesService.getScriptProperties().getProperty(key);
  if (p) { CacheService.getScriptCache().put(key, p, CACHE_SEC); return JSON.parse(p); }
  return def;
}
function save_(key, val) {
  const s = JSON.stringify(val);
  CacheService.getScriptCache().put(key, s, CACHE_SEC);
  PropertiesService.getScriptProperties().setProperty(key, s);
}
function q_(id) { return QUESTIONS.filter(q => q.id === id)[0]; }

// ───── 교육생 폰 ─────
function getState() {
  return load_('state', { cur: null, reveal: false, rev: 0 });
}

function submit(qid, uid, val) {
  const q = q_(qid); if (!q || !uid) return { ok: false, msg: '문제를 찾을 수 없습니다' };
  const st = getState(); if (st.cur !== qid) return { ok: false, msg: '지금은 다른 문제를 진행하고 있습니다' };
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(15000)) return { ok: false, msg: '잠시 후 다시 눌러 주세요' };
  try {
    const key = 'r_' + qid;
    const m = load_(key, {});
    if (q.type === 'text') {
      const s = String(val || '').replace(/\s+/g, ' ').trim().slice(0, MAX_TEXT);
      if (!s) return { ok: false, msg: '한 줄을 적어 주세요' };
      if (!(uid in m) && Object.keys(m).length >= MAX_TEXTS) return { ok: false, msg: '자리가 다 찼습니다. 감사합니다!' };
      m[uid] = s;
    } else {
      const n = Number(val);
      if (!(n >= 0 && n < q.options.length)) return { ok: false, msg: '보기를 골라 주세요' };
      m[uid.slice(0, 40)] = n;
    }
    save_(key, m);
    return { ok: true };
  } finally { lock.releaseLock(); }
}

// ───── 강사 화면 ─────
function results(qid) {
  const q = q_(qid); if (!q) return null;
  const m = load_('r_' + qid, {});
  const out = { id: qid, n: Object.keys(m).length };
  if (q.type === 'text') out.texts = Object.keys(m).map(k => m[k]);
  else {
    out.counts = q.options.map(() => 0);
    Object.keys(m).forEach(k => { out.counts[m[k]]++; });
    if (q.compare) {
      const c = load_('r_' + q.compare, {}); const cq = q_(q.compare);
      out.cmp = { title: cq.title, options: cq.options, counts: cq.options.map(() => 0), n: Object.keys(c).length };
      Object.keys(c).forEach(k => { out.cmp.counts[c[k]]++; });
    }
  }
  return out;
}

function admin(pin, action, arg) {
  if (String(pin) !== ADMIN_PIN) return { ok: false, msg: '비밀번호가 틀렸습니다' };
  const st = getState();
  if (action === 'check') return { ok: true };
  if (action === 'go') { st.cur = arg || null; st.reveal = false; }
  if (action === 'reveal') { st.reveal = !!arg; }
  if (action === 'reset') { save_('r_' + arg, {}); }
  if (action === 'resetAll') { QUESTIONS.forEach(q => save_('r_' + q.id, {})); st.cur = null; st.reveal = false; }
  st.rev = (st.rev || 0) + 1;
  save_('state', st);
  return { ok: true, state: st };
}

// 리허설 뒤 전체 초기화가 필요하면 편집기에서 이 함수를 한 번 실행
function 전체초기화() { admin(ADMIN_PIN, 'resetAll'); }
