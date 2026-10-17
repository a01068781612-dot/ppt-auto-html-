// 직장훈련특강 모션 프리셋 v.1.0.0 — 정적 장면(HTML)에 GSAP 3.13(SplitText · DrawSVG · ScrambleText, 무료 플러그인) 등장 효과를 입힌다.
// render_motion.js가 페이지에 gsap → 플러그인 → 이 파일을 차례로 넣고 window.__build(장 번호)를 부른 뒤, 만들어진 timeline을 프레임마다 seek해서 찍는다.
// 원칙: 마지막 프레임 = 정적 장면 그대로(모든 tween은 from → 원래 상태). 장마다 효과 조합이 달라지도록 장 번호로 프리셋을 고른다.
(function () {
  gsap.registerPlugin(SplitText, DrawSVGPlugin, ScrambleTextPlugin, CustomEase);
  CustomEase.create('snap', 'M0,0 C0.2,0 0.1,1 1,1');

  // 덩어리(카드 · 사진 · 글 상자) 등장 16가지
  const ITEM = [
    { name: 'fadeUp',     from: { y: 70, opacity: 0 }, ease: 'power3.out' },
    { name: 'slideBlur',  from: { x: -140, opacity: 0, filter: 'blur(14px)' }, ease: 'power3.out' },
    { name: 'pop',        from: { scale: .55, opacity: 0 }, ease: 'back.out(1.9)' },
    { name: 'wipeRight',  from: { clipPath: 'inset(0% 100% 0% 0%)' }, to: { clipPath: 'inset(0% 0% 0% 0%)' }, ease: 'power4.inOut' },
    { name: 'flipY',      from: { rotationY: -95, transformPerspective: 1400, transformOrigin: 'left center', opacity: 0 }, ease: 'power3.out' },
    { name: 'maskUp',     from: { clipPath: 'inset(100% 0% 0% 0%)', y: 50 }, to: { clipPath: 'inset(0% 0% 0% 0%)', y: 0 }, ease: 'expo.out' },
    { name: 'drop',       from: { y: -220, opacity: 0 }, ease: 'elastic.out(1, .65)' },
    { name: 'zoomOut',    from: { scale: 1.35, opacity: 0, filter: 'blur(10px)' }, ease: 'power2.out' },
    { name: 'slideRight', from: { x: 180, opacity: 0 }, ease: 'snap' },
    { name: 'skew',       from: { x: -120, skewX: 22, opacity: 0 }, ease: 'power4.out' },
    { name: 'flipX',      from: { rotationX: 90, transformPerspective: 1100, transformOrigin: 'top center', opacity: 0 }, ease: 'back.out(1.4)' },
    { name: 'iris',       from: { clipPath: 'circle(0% at 50% 50%)' }, to: { clipPath: 'circle(75% at 50% 50%)' }, ease: 'power2.inOut' },
    { name: 'diagonal',   from: { x: -90, y: 90, rotation: -7, opacity: 0 }, ease: 'power3.out' },
    { name: 'rise3D',     from: { z: -500, rotationX: 28, transformPerspective: 1500, opacity: 0 }, ease: 'power3.out' },
    { name: 'stretch',    from: { scaleX: 0, transformOrigin: 'left center', opacity: .2 }, ease: 'expo.out' },
    { name: 'blurIn',     from: { opacity: 0, filter: 'blur(24px)', scale: 1.06 }, ease: 'sine.out' },
  ];
  const ORDER = ['start', 'center', 'end', 'edges'];

  // 제목 글자 효과 7가지
  function title(tl, el, kind, at) {
    if (!el) return;
    if (kind === 5) {   // 스크램블(영문 · 숫자 섞임 → 원문)
      const txt = el.textContent; tl.from(el, { duration: 1.0, scrambleText: { text: txt, chars: '01#%·', revealDelay: .2, speed: .6 } }, at)
        .set(el, { textContent: txt }); return;
    }
    const s = new SplitText(el, { type: kind === 1 || kind === 6 ? 'words' : 'chars', tag: 'span' });
    const t = kind === 1 || kind === 6 ? s.words : s.chars;
    if (kind === 0) tl.from(t, { yPercent: 110, opacity: 0, duration: .7, stagger: .028, ease: 'power4.out' }, at);
    if (kind === 1) tl.from(t, { opacity: 0, filter: 'blur(12px)', y: 20, duration: .7, stagger: .08, ease: 'power2.out' }, at);
    if (kind === 2) tl.from(t, { scale: 0, opacity: 0, duration: .5, stagger: .025, ease: 'back.out(2.2)', transformOrigin: '50% 80%' }, at);
    if (kind === 3) tl.from(t, { opacity: 0, duration: .01, stagger: .035, ease: 'none' }, at);                       // 타자기
    if (kind === 4) tl.from(t, { rotationX: -100, transformPerspective: 600, opacity: 0, duration: .6, stagger: .03, ease: 'power3.out', transformOrigin: '50% 50% -20px' }, at);
    if (kind === 6) tl.from(t, { x: 60, opacity: 0, duration: .6, stagger: .07, ease: 'power3.out' }, at);
  }

  // 큰 숫자는 0부터 세어 올라간다
  function counters(tl, root, at) {
    root.querySelectorAll('div,span').forEach(el => {
      const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 96) return;
      const n = el.firstChild; if (!n || n.nodeType !== 3) return;
      const m = n.nodeValue.trim().match(/^(\d+(?:\.\d+)?)$/); if (!m) return;
      const end = parseFloat(m[1]), dec = (m[1].split('.')[1] || '').length, o = { v: 0 };
      tl.to(o, { v: end, duration: 1.3, ease: 'power2.out', onUpdate: () => { n.nodeValue = o.v.toFixed(dec); } }, at);
    });
  }

  window.__build = function (no) {
    const R = document.getElementById('r');
    const tl = gsap.timeline({ paused: true });
    const ip = ITEM[(no * 7) % ITEM.length], ip2 = ITEM[(no * 7 + 5) % ITEM.length];
    const tk = no % 7, order = ORDER[no % 4];
    const kids = [...R.children].filter(e => !e.classList.contains('pg'));
    const tag = R.querySelector('.tag'), ghost = R.querySelector('.ghost'), ttl = R.querySelector('.ttl'), hl = R.querySelector('.hl'), key = R.querySelector('.key');
    const deco = kids.filter(e => e.tagName.toLowerCase() === 'svg');
    const rest = kids.filter(e => ![tag, ghost, ttl, hl, key].includes(e) && !deco.includes(e) && e.tagName.toLowerCase() !== 'style');
    let t = 0;
    if (tag) tl.from(tag, { opacity: 0, letterSpacing: '.6em', duration: .7, ease: 'power2.out' }, 0);
    if (ghost) tl.from(ghost, { x: 160, opacity: 0, duration: 1.6, ease: 'power2.out' }, 0);
    deco.forEach(d => { const p = d.querySelectorAll('path'); if (p.length) tl.from(p, { drawSVG: '0%', duration: .7, ease: 'power2.inOut' }, .05); });
    if (ttl) { title(tl, ttl, tk, .1); t = .45; }
    if (hl) tl.from(hl, { scaleX: 0, transformOrigin: 'left center', duration: .9, ease: 'expo.inOut' }, .2);
    // 본문 덩어리: 카드 · 사진이 많으면 두 프리셋을 번갈아, 표는 줄마다
    const st = rest.length > 6 ? .07 : .14;
    rest.forEach((el, i) => {
      const p = (i % 2 && rest.length > 3) ? ip2 : ip;
      const vars = Object.assign({ duration: .85, ease: p.ease, clearProps: 'filter,clipPath,transform' }, p.from);
      const at = t + (order === 'end' ? (rest.length - 1 - i) : order === 'center' ? Math.abs(i - (rest.length - 1) / 2) : order === 'edges' ? Math.min(i, rest.length - 1 - i) : i) * st;
      if (p.to) { delete vars.clearProps; tl.fromTo(el, vars, Object.assign({ duration: .85, ease: p.ease, clearProps: 'clipPath,transform' }, p.to), at); } else tl.from(el, vars, at);
      el.querySelectorAll(':scope tr').forEach((tr, j) => tl.from(tr, { x: -50, opacity: 0, duration: .5, ease: 'power3.out' }, at + .15 + j * .08));
      const img = el.matches('.shot') ? el.querySelector('img') : null;
      if (img) tl.from(img, { scale: el.classList.contains('paper') ? 1.06 : 1.14, duration: 3.2, ease: 'sine.out' }, at);   // 켄 번스
    });
    counters(tl, R, t + .2);
    if (key) tl.fromTo(key, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: .8, ease: 'power3.inOut', clearProps: 'clipPath' }, Math.max(1.1, tl.duration() - .5));
    window.__tl = tl;
    return { dur: tl.duration(), item: ip.name + '/' + ip2.name, title: tk, order };
  };
})();
