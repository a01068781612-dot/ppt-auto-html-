const { chromium } = require('playwright-core');
const dirs = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; pg.on('pageerror', e => errs.push(String(e)));
  await pg.addInitScript(() => { window.__timelines = {}; });
  for (const d of dirs) {
    await pg.goto('file://' + __dirname + '/' + d + '/index.html'); await pg.waitForTimeout(700);
    await pg.evaluate(() => { const tl = window.__timelines.main; tl.seek(tl.duration()); });
    await pg.waitForTimeout(150);
    await pg.screenshot({ path: d + '/shot_end.png' });
  }
  console.log('errors', errs); await b.close();
})();
