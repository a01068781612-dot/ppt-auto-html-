// 직장훈련특강 모션 렌더 v.1.0.0 — 정적 장면 HTML에 motion_presets.js를 입혀 장마다 mp4(1920×1080 · 25fps · crf 24)로 찍는다.
// 사용: NODE_PATH=<playwright 있는 node_modules> node render_motion.js <장면 html 폴더들(쉼표)> <gsap dist 폴더> <출력 폴더> <장 번호 목록(1-120 또는 3,5,7)> [동시 수]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const [dirs, GS, OUT, list, par = '3'] = process.argv.slice(2);
const DIRS = dirs.split(','), FPS = 25, HOLD = .8, MAXD = 6.5;
const nums = list.includes('-') ? (([a, b]) => Array.from({ length: b - a + 1 }, (_, i) => a + i))(list.split('-').map(Number)) : list.split(',').map(Number);
const find = n => DIRS.map(d => path.join(d, `v${String(n).padStart(3, '0')}.html`)).find(f => fs.existsSync(f));
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--no-sandbox', '--force-device-scale-factor=1'] });
  const log = [];
  async function one(n) {
    const f = find(n); if (!f) { log.push(`${n} 없음`); return; }
    const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
    await pg.goto('file://' + f, { waitUntil: 'load' });
    for (const s of ['gsap.min.js', 'SplitText.min.js', 'DrawSVGPlugin.min.js', 'ScrambleTextPlugin.min.js', 'CustomEase.min.js']) await pg.addScriptTag({ path: path.join(GS, s) });
    await pg.addScriptTag({ path: path.join(__dirname, 'motion_presets.js') });
    await pg.evaluate(() => document.fonts.ready.then(() => 1));
    const info = await pg.evaluate(no => window.__build(no), n);
    const dur = Math.min(MAXD, Math.max(2.4, info.dur + HOLD)), frames = Math.round(dur * FPS);
    const mp4 = path.join(OUT, `m${String(n).padStart(3, '0')}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'veryfast', '-movflags', '+faststart', mp4]);
    let last;
    for (let i = 0; i < frames; i++) {
      await pg.evaluate(t => { window.__tl.seek(t, false); }, Math.min(i / FPS, info.dur));
      last = await pg.screenshot({ type: 'jpeg', quality: 90 });
      if (!ff.stdin.write(last)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    fs.writeFileSync(path.join(OUT, `m${String(n).padStart(3, '0')}.jpg`), last);
    log.push(`${n}\t${dur.toFixed(1)}s\t${info.item}\tT${info.title}\t${info.order}`);
    await pg.close();
  }
  const q = [...nums];
  await Promise.all(Array.from({ length: +par }, async () => { while (q.length) await one(q.shift()); }));
  await br.close();
  fs.appendFileSync(path.join(OUT, 'log.tsv'), log.sort((a, b) => parseInt(a) - parseInt(b)).join('\n') + '\n');
  console.log('done', log.length);
})();
