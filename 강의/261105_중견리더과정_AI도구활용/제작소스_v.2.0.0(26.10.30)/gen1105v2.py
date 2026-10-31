# 슬라이드 v.2 (기획안 v.3.2.0) 장면 생성기 — gen1105.py의 레이아웃·모션 함수를 그대로 쓰고 내용만 바꿈
# 사용: python3 gen1105v2.py <출력폴더> <lib폴더>   → <출력>/<id>/index.html, <출력>/order.json (장 순서)
import os, sys, json, shutil
import gen1105 as G

OUT = G.OUT
ORDER = []   # (id, 종류) 종류: m=모션 새로 · r=v.1 장면 재사용 · p=📌 자리표시

V1 = os.environ.get('HF1', os.path.join(os.path.dirname(OUT), 'hf1105'))   # v.1 렌더 폴더

def m(id): ORDER.append((id, 'm'))
def r(id): ORDER.append((id, 'r'))   # v.1 렌더(out.mp4) 그대로

def rc(id, subs):
    """v.1 장면을 복사해 문구만 바꾸고 다시 렌더"""
    src = os.path.join(V1, id); dst = os.path.join(OUT, id)
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns('out.mp4', 'last.png'))
    h = open(dst + '/index.html').read()
    for a, b in subs:
        assert a in h, (id, a); h = h.replace(a, b)
    open(dst + '/index.html', 'w').write(h)
    m(id)

def v(id, title, src):
    """🎬 새 소개 영상 자리 (강사가 내려받아 주면 교체)"""
    slot(id, title, src)
    ORDER[-1] = (id, 'v')

def clip(id):
    """강사 폰 화면 녹화 영상 — clip1105.py가 <출력>/<id>/out.mp4로 만듦"""
    ORDER.append((id, 'm'))

def slot(id, title, src):
    """📌 10.20 PPT에서 가져올 장 — 미리보기용 자리표시 장면"""
    b = G.B(3)
    b.add('a', 'left:110px;top:110px;width:1700px;height:860px;border:3px dashed #ff5a1f;border-radius:36px;background:#1d1a19')
    b.add('a', 'left:190px;top:230px;font-size:30px;font-weight:800;letter-spacing:.2em;color:#ff5a1f', '📌 바꿔 끼울 장')
    b.add('a blk', 'left:190px;top:310px;width:1540px;font-size:84px;line-height:1.2', title)
    b.add('a', 'left:190px;top:600px;width:1540px;font-size:36px;color:#a59f98;line-height:1.5', src)
    G.write(id, 3, b, 'tl.from(".blk",{opacity:0,duration:.3},0);')
    ORDER.append((id, 'p'))

def big(id, small, line1, line2, ghost, chips=None, dur=6):
    """큰 문장 장면 (공개·메시지)"""
    b = G.B(dur)
    b.add('a s1', 'left:150px;top:230px;font-size:46px;font-weight:700;color:#a59f98', small)
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".s2" class="sq clip"')
    b.add('a s2 blk', 'left:150px;top:320px;font-size:150px;line-height:1.1;letter-spacing:-.045em', line1 + (f'<br><span class="acc">{line2}</span>' if line2 else ''))
    b.add('ghost', 'right:110px;top:90px;font-size:150px', ghost)
    js = ('tl.from(".s1",{opacity:0,y:20,duration:.6},.2).from(".s2",{opacity:0,scale:1.15,transformOrigin:"left center",filter:"blur(10px)",duration:.9,ease:"power3.out"},.8)'
          '.from(".ghost",{opacity:0,duration:1.2},.9);')
    if chips:
        cs = ''.join(f'<div class="chip{" c" if i == len(chips)-1 else ""}"><b>{i+1:02d}</b><span>{c}</span></div>' for i, c in enumerate(chips))
        b.add('a chips', f'left:150px;right:110px;bottom:120px;display:grid;grid-template-columns:repeat({len(chips)},1fr);gap:24px', cs)
        js += 'tl.from(".chip",{opacity:0,y:40,duration:.5,stagger:.15},1.8);'
    G.write(id, dur, b, js, rad=True)
    m(id)


PHONE = os.environ.get('PHONE', os.path.join(os.path.dirname(OUT), 'phone2'))   # Flow 폰 화면(k0~k4.png, 강사 녹화에서 뽑음)

def doc(id):
    """OCR 실습용 — 강사가 폰으로 찍을 4줄 보고서 (흰 종이)"""
    b = G.B(4)
    b.add('tag t-tag', '', '<b>PART 2 · 미션 1  </b><span>폰으로 이 화면을 찍어 보세요</span>')
    b.add('a paper', 'left:260px;top:150px;width:1400px;height:820px;background:#fbfaf7;border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.6);padding:80px 110px;color:#111;font-family:"Pretendard",sans-serif',
          '<div style="text-align:center;font-size:52px;font-weight:800;letter-spacing:-.01em">AI 활용 업무 개선 추진 계획(안)</div>'
          '<div style="margin:22px 0 46px;border-top:3px solid #111;border-bottom:1px solid #111;height:7px"></div>'
          '<div style="font-size:38px;line-height:1.95;font-weight:500">'
          '1. 추진 배경: 반복 문서 작업 증가로 직원 업무 부담 가중<br>'
          '2. 추진 내용: 생성형 AI로 보고서 초안·자료 정리 시범 운영<br>'
          '3. 추진 일정: 2026. 11. ~ 12.(2개월), 부서별 1개 업무 선정<br>'
          '4. 기대 효과: 문서 작성 시간 30% 단축, 민원 응대에 집중</div>'
          '<div style="position:absolute;right:110px;bottom:60px;font-size:26px;color:#666">※ 실습용 예시 문서</div>')
    G.write(id, 4, b, 'tl.from(".t-tag",{opacity:0,duration:.5},0).from(".paper",{opacity:0,y:60,rotation:-1.5,duration:1.0,ease:"power3.out"},.2);')
    m(id)

def steps2(id):
    """사진 만들기 → 고치기 2단계 (강사가 먼저, 같이 따라 하기)"""
    b = G.B(7); G.header(b, 'PART 2 · 미션 2', '강사가 먼저 → 같이 따라 하기', 'Create.', '만들고, 고칩니다 — 말 두 마디면 됩니다', 'mask')
    for i, (lab, t, say, note) in enumerate([
        ('STEP 1', '만들기', '세종대왕이 책을 읽는 사진', '사진이 없어도 **글로 사진**을 만듭니다'),
        ('STEP 2', '고치기', '책 읽는 상황 말고 노트북하는 상황으로 교체', '마음에 안 들면 **이어서 말하면** 고쳐집니다')]):
        x = 110 + i * 870
        b.add(f'card cd cd{i}' + (' hi' if i == 1 else ''), f'left:{x}px;top:300px;width:830px;height:600px',
              f'<div class="in a" style="left:44px;top:40px;font-size:26px;font-weight:800;letter-spacing:.25em;color:#ff5a1f">{lab}</div>'
              f'<div class="in a blk" style="left:44px;top:84px;font-size:72px">{t}</div>'
              f'<div class="in a" style="left:44px;top:220px;width:742px;background:#2a2523;border:1.5px solid #4a4340;border-radius:26px 26px 26px 6px;padding:30px 34px;font-size:36px;font-weight:700;line-height:1.45">“{say}”</div>'
              f'<div class="in a" style="left:44px;bottom:44px;width:742px;font-size:30px;color:#a59f98;line-height:1.4">{G.bold(note)}</div>')
    b.add('a arw', 'left:917px;top:568px;width:76px;height:76px;border-radius:50%;background:#ff5a1f;color:#111;font-size:44px;font-weight:900;display:flex;align-items:center;justify-content:center;z-index:5', '→')
    js = G.HEAD_JS['mask'] + 'tl.from(".cd0",{opacity:0,x:-80,duration:.7,ease:"power3.out"},.6).from(".arw",{opacity:0,scale:0,duration:.4,ease:"back.out(2)"},1.4).from(".cd1",{opacity:0,x:80,duration:.7,ease:"power3.out"},1.6).from(".cd .in",{opacity:0,y:16,duration:.4,stagger:.1},.9)'
    js += '.to(".cd.hi",{boxShadow:"0 0 0 10px rgba(255,90,31,.18), 0 30px 70px rgba(255,90,31,.25)",y:-10,duration:.6},3.0);'
    G.write(id, 7, b, js)
    m(id)

def phones(id):
    """Flow 폰 화면 5단계 (Play 스토어 실제 화면 + Google Play 공식 앱 스크린샷)"""
    items = [('k0.png', '설치', 'Play 스토어<br>「Google Flow」 설치'), ('k1.png', '시작', '구글 로그인 →<br><b>+ 신규</b>'),
             ('k2.png', '말로 이미지', '<b>이미지</b> 고르고<br>만들 장면 입력'), ('k3.png', '영상으로', '사진 고르고<br><b>애니메이션</b>으로 입력'),
             ('k4.png', '완성', '영상 재생 →<br><b>다운로드</b> → 카톡')]
    b = G.B(8); G.header(b, 'PART 2 · 미션 3', '폰에서 이렇게 — Google Flow', 'Flow.', '설치부터 이미지·영상까지, 폰 화면으로', 'chars')
    for i, (img, t, cap) in enumerate(items):
        x = 110 + i * 344
        b.add(f'a ph ph{i}', f'left:{x}px;top:270px;width:320px',
              f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px"><span style="width:46px;height:46px;border-radius:50%;background:{"#ff5a1f" if i==4 else "#3a3533"};color:{"#111" if i==4 else "#f4f4f2"};font-size:26px;font-weight:900;display:flex;align-items:center;justify-content:center">{i+1}</span><span style="font-size:32px;font-weight:800">{t}</span></div>'
              f'<div style="width:320px;height:520px;border-radius:28px;overflow:hidden;background:#fff;border:6px solid #2a2523"><img src="{img}" style="width:100%;height:100%;object-fit:cover;object-position:top"/></div>'
              f'<div style="margin-top:14px;font-size:24px;line-height:1.4;color:#d6d2c9">{cap}</div>')
    b.add('a src', 'left:110px;top:1040px;font-size:18px;color:#8a847e', '화면: 강사 갤럭시 실제 녹화(26.10.30) · 아이폰은 앱이 없으면 flow.google.com')
    js = G.HEAD_JS['chars'] + 'tl.from(".ph",{opacity:0,y:80,duration:.6,stagger:.35,ease:"power3.out"},.7).from(".src",{opacity:0,duration:.5},2.6);'
    G.write(id, 8, b, js, assets=[os.path.join(PHONE, it[0]) for it in items])
    m(id)


M1020 = os.environ.get('M1020', '')   # 10.20 워크숍 motion_html 폴더 (정리 장면 원본)

def rc10(id, subs):
    """10.20 워크숍 장면 HTML(텍스트만 git에 있음)을 가져와 문구만 바꾸고 렌더"""
    dst = os.path.join(OUT, id); os.makedirs(dst, exist_ok=True)
    h = open(os.path.join(M1020, 'st', id, 'index.html')).read()
    for a, b in subs:
        assert a in h, (id, a); h = h.replace(a, b)
    open(dst + '/index.html', 'w').write(h)
    for f in ['hyperframes.json', 'meta.json', 'package.json', 'bg.png']: shutil.copy(os.path.join(G.HERE, f), dst)
    for f in ['gsap.min.js', 'PretendardVariable.woff2']: shutil.copy(os.path.join(G.LIB, f), dst)
    m(id)

TOOLS = os.environ.get('TOOLS', os.path.join(os.path.dirname(OUT), 'tools'))   # 도구 화면 캡처(tool1·tool3·before·after.png)

def frame(img, w, h, label=''):
    """다크 브라우저 창 안에 캡처 화면"""
    return (f'<div style="width:{w}px;height:{h}px;border-radius:22px;overflow:hidden;background:#1d1a19;border:2px solid #3a3533;box-shadow:0 30px 80px rgba(0,0,0,.55)">'
            f'<div style="height:46px;display:flex;align-items:center;gap:10px;padding:0 20px;background:#262221;border-bottom:1px solid #3a3533">'
            '<i style="width:14px;height:14px;border-radius:50%;background:#ff5a1f"></i><i style="width:14px;height:14px;border-radius:50%;background:#55504c"></i><i style="width:14px;height:14px;border-radius:50%;background:#55504c"></i>'
            f'<span style="margin-left:14px;font-size:20px;color:#8a847e">{label}</span></div>'
            f'<img src="{img}" style="display:block;width:100%;height:{h-48}px;object-fit:cover;object-position:top;background:#fff"/></div>')

def shot(id, tag, sub, ghost, title, steps, img, label, key):
    """왼쪽 단계 + 오른쪽 실제 도구 화면 (국토부 실습 도구)"""
    b = G.B(7); G.header(b, tag, sub, ghost, title, 'mask')
    for i, (t, d) in enumerate(steps):
        last = i == len(steps) - 1
        b.add(f'a st st{i}', f'left:110px;top:{300 + i * 128}px;width:560px;height:110px;display:flex;align-items:center;gap:26px',
              f'<div style="flex:none;width:76px;height:76px;border-radius:50%;border:2.5px solid {"#ff5a1f" if last else "#55504c"};display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:{"#ff5a1f" if last else "#f4f4f2"}">{i+1}</div>'
              f'<div><div style="font-size:38px;font-weight:800">{t}</div><div style="font-size:24px;color:#a59f98;margin-top:4px">{d}</div></div>')
    b.add('a shot', 'left:720px;top:290px', frame(img, 1090, 690, label))
    js = G.HEAD_JS['mask'] + 'tl.from(".st",{opacity:0,x:-60,duration:.55,stagger:.25,ease:"power3.out"},.7).from(".shot",{opacity:0,x:120,scale:.94,duration:1.0,ease:"power3.out"},.9);'
    js += f'tl.to(".st{len(steps)-1}",{{x:12,duration:.4,ease:"power2.out"}},2.4);'
    G.write(id, 7, b, js, assets=[os.path.join(TOOLS, img)])
    m(id)

def beforeafter(id):
    b = G.B(7); G.header(b, 'PART 4 · 도구 1', '말 한 줄로 바뀐 그래프', 'After.', '“색을 고를 수 있게 해 줘” — 그 다음 화면', 'chars')
    b.add('a ba0', 'left:110px;top:300px', '<div style="font-size:30px;font-weight:800;letter-spacing:.25em;color:#8a847e;margin-bottom:16px">BEFORE</div>' + frame('before.png', 820, 560, '팔레트 고르기'))
    b.add('a ba1', 'left:990px;top:300px', '<div style="font-size:30px;font-weight:800;letter-spacing:.25em;color:#ff5a1f;margin-bottom:16px">AFTER</div>' + frame('after.png', 820, 560, '보고서용 그래프'))
    b.add('a arw', 'left:917px;top:610px;width:76px;height:76px;border-radius:50%;background:#ff5a1f;color:#111;font-size:44px;font-weight:900;display:flex;align-items:center;justify-content:center;z-index:5', '→')
    b.add('a cap', 'left:110px;top:950px;font-size:32px;color:#a59f98', G.bold('코드는 한 줄도 안 썼습니다 — **말로 고쳐 달라고** 했을 뿐'))
    js = G.HEAD_JS['chars'] + 'tl.from(".ba0",{opacity:0,x:-80,duration:.8,ease:"power3.out"},.7).from(".arw",{opacity:0,scale:0,duration:.4,ease:"back.out(2)"},1.5).from(".ba1",{opacity:0,x:80,duration:.8,ease:"power3.out"},1.7).from(".cap",{opacity:0,y:20,duration:.6},2.6);'
    G.write(id, 7, b, js, assets=[os.path.join(TOOLS, 'before.png'), os.path.join(TOOLS, 'after.png')])
    m(id)

def prompts(id):
    b = G.B(8); G.header(b, 'PART 4 · 혼자서 해 보기', '집에서·내 폰으로 이 순서대로', 'Try.', '이렇게 다섯 번 말하면 도구가 됩니다', 'blur')
    ps = ['엑셀 올리면 다양한 그래프 그려 주는 HTML 만들어 줘', '가로·세로·원형 그래프 추가해 줘', '그래프 색 선택 기능 추가해 줘', '그래프 배경 바꾸는 버튼 넣어 줘', '마우스 올리면 수치 뜨게 해 줘']
    for i, t in enumerate(ps):
        b.add(f'bub say say{i}', f'left:{110 + (i % 2) * 60}px;top:{300 + i * 118}px;font-size:40px', f'<b style="color:#ff5a1f;margin-right:22px">{i+1:02d}</b>“{t}”')
    b.add('a nt', 'left:1300px;top:300px;width:510px;font-size:30px;line-height:1.55;color:#a59f98', G.bold('한 번에 다 말하지 않아도 됩니다.<br><br>**하나 만들고 → 하나씩 더하기**<br><br>안 되면 “안 돼, 고쳐 줘” 한 마디'))
    js = G.HEAD_JS['blur'] + 'tl.from(".say",{opacity:0,y:30,scale:.92,transformOrigin:"left bottom",duration:.5,stagger:.4,ease:"back.out(1.8)"},.8).from(".nt",{opacity:0,x:40,duration:.7},3.0);'
    G.write(id, 8, b, js)
    m(id)

ART = os.environ.get('ART', os.path.join(os.path.dirname(OUT), 'art'))   # 기사 캡처(cap1·cap2·photo3.jpg) — 10.20 장 마지막 화면에서 잘라 냄

def art10(id, src, subs, imgs):
    """10.20 워크숍 기사 장면(art/pN)을 가져와 기사 원문과 맞게 문구를 고치고 렌더"""
    dst = os.path.join(OUT, id); os.makedirs(dst, exist_ok=True)
    h = open(os.path.join(M1020, 'art', src, 'index.html')).read()
    for a, b in subs:
        assert a in h, (id, a); h = h.replace(a, b)
    open(dst + '/index.html', 'w').write(h)
    for f in ['hyperframes.json', 'meta.json', 'package.json', 'bg.png']: shutil.copy(os.path.join(G.HERE, f), dst)
    for f in ['gsap.min.js', 'PretendardVariable.woff2']: shutil.copy(os.path.join(G.LIB, f), dst)
    for a, b in imgs: shutil.copy(os.path.join(ART, a), os.path.join(dst, b))
    m(id)

APPS = os.environ.get('APPS', os.path.join(os.path.dirname(OUT), 'apps'))   # Play 스토어 앱 아이콘·공식 스크린샷 (<앱>_icon.png, <앱>_s0~3.png)

def phone_img(img, w, h, rot=0, extra=''):
    return (f'<div style="width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;border:6px solid #2a2523;background:#fff;'
            f'box-shadow:0 30px 80px rgba(0,0,0,.6);transform:rotate({rot}deg);{extra}"><img src="{img}" style="width:100%;height:100%;object-fit:cover;object-position:top"/></div>')

def what_html(id):
    """HTML이 뭔가요 — 파일 하나 → 더블클릭 → 인터넷 창에 도구가 뜸"""
    b = G.B(7); G.header(b, 'PART 4 · HTML이 뭔가요?', '어렵지 않습니다', 'HTML.', '인터넷 창으로 여는 「파일 하나」', 'mask')
    b.add('a f1', 'left:150px;top:360px;width:330px;height:420px;border-radius:24px;background:#1d1a19;border:2px solid #3a3533;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px',
          '<div style="width:150px;height:190px;border-radius:14px;background:#f4f4f2;position:relative;display:flex;align-items:flex-end;justify-content:center;padding-bottom:22px;box-sizing:border-box">'
          '<div style="position:absolute;right:0;top:0;width:44px;height:44px;background:#c9c4bd;border-bottom-left-radius:12px"></div>'
          '<span style="font-size:34px;font-weight:900;color:#ff5a1f">.html</span></div>'
          '<div style="font-size:30px;font-weight:800">도구1_시각화.html</div><div style="font-size:24px;color:#a59f98">메일·메신저로 받은 파일 하나</div>')
    b.add('a ar1', 'left:520px;top:520px;font-size:70px;font-weight:900;color:#ff5a1f', '→')
    b.add('a f2', 'left:620px;top:470px;width:200px;text-align:center', '<div style="font-size:84px">🖱️</div><div style="font-size:30px;font-weight:800;margin-top:10px">더블클릭</div>')
    b.add('a ar2', 'left:850px;top:520px;font-size:70px;font-weight:900;color:#ff5a1f', '→')
    b.add('a f3', 'left:960px;top:330px', frame('tool1.png', 850, 520, '크롬·엣지 — 인터넷 창'))
    b.add('a nt', 'left:150px;top:900px;width:1660px;font-size:34px;font-weight:700',
          G.bold('설치도, 서버도, 인터넷 연결도 필요 없습니다 — **인터넷 창(크롬·엣지)이 있는 PC면 어디서나** 열립니다'))
    js = G.HEAD_JS['mask'] + ('tl.from(".f1",{opacity:0,y:60,duration:.7,ease:"power3.out"},.7).from(".ar1",{opacity:0,x:-30,duration:.4},1.3)'
          '.from(".f2",{opacity:0,scale:.5,duration:.5,ease:"back.out(2)"},1.5).from(".ar2",{opacity:0,x:-30,duration:.4},1.9)'
          '.from(".f3",{opacity:0,scale:.9,y:40,duration:.8,ease:"power3.out"},2.1).from(".nt",{opacity:0,y:20,duration:.6},3.0);')
    G.write(id, 7, b, js, assets=[os.path.join(TOOLS, 'tool1.png')])
    m(id)

def fullshot(id, tag, label, img, cap):
    """도구 결과 화면을 크게 — 화면 비율에 맞춰 가운데"""
    from PIL import Image as _I
    iw, ih = _I.open(os.path.join(TOOLS, img)).size
    h = 860; w = min(1700, int((h - 48) * iw / ih))
    b = G.B(6)
    b.add('tag t-tag', '', f'<b>{tag}  </b><span>{cap}</span>')
    b.add('a fs', f'left:{(1920 - w) // 2}px;top:160px', frame(img, w, h, label))
    js = 'tl.from(".t-tag",{opacity:0,x:-30,duration:.5},0).from(".fs",{opacity:0,y:50,scale:.97,duration:.9,ease:"power3.out"},.2);'
    G.write(id, 6, b, js, assets=[os.path.join(TOOLS, img)])
    m(id)

def app(id, key, name, maker, when, steps, free, warn, shots, ghost):
    """PART 5 앱 소개 — 왼쪽 설명, 오른쪽 실제 앱 화면 2장"""
    b = G.B(8)
    b.add('tag t-tag', '', f'<b>PART 5 · AI 앱 서랍  </b><span>{maker}</span>')
    b.add('ghost t-ghost', 'right:110px;top:62px;font-size:110px;text-align:right', ghost)
    b.add('a ic', 'left:110px;top:140px', f'<img src="{key}_icon.png" style="width:120px;height:120px;border-radius:28px;display:block"/>')
    b.add('sq', '', ''); b.items[-1] = b.items[-1].replace('class="sq clip"', 'data-sq=".nm" class="sq clip"')
    b.add('a nm blk', 'left:260px;top:150px;font-size:78px;line-height:1.1;white-space:nowrap', name)
    b.add('a wh', 'left:110px;top:310px;width:960px;font-size:38px;font-weight:700;line-height:1.4', G.bold(when))
    for i, st in enumerate(steps):
        b.add(f'a st st{i}', f'left:110px;top:{470 + i * 100}px;width:960px;height:84px;display:flex;align-items:center;gap:24px',
              f'<div style="flex:none;width:64px;height:64px;border-radius:50%;border:2.5px solid {"#ff5a1f" if i == len(steps)-1 else "#55504c"};display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:{"#ff5a1f" if i == len(steps)-1 else "#f4f4f2"}">{i+1}</div>'
              f'<div style="font-size:34px;font-weight:700">{G.bold(st)}</div>')
    b.add('a fr', 'left:110px;top:800px;display:flex;gap:16px;align-items:center',
          f'<span class="pill" style="background:#ff5a1f;color:#111;font-size:26px;font-weight:800;padding:10px 22px;border-radius:40px">무료</span><span style="font-size:28px;color:#d6d2c9">{free}</span>')
    b.add('a wn', 'left:110px;top:880px;width:960px;font-size:26px;color:#a59f98;line-height:1.4', '⚠ ' + G.bold(warn))
    b.add('a p1', 'left:1150px;top:170px', phone_img(f'{key}_s{shots[0]}.png', 330, 640, -3))
    b.add('a p2', 'left:1470px;top:250px', phone_img(f'{key}_s{shots[1]}.png', 330, 640, 3))
    b.add('a src', 'left:1150px;top:960px;font-size:18px;color:#8a847e', '화면: Google Play 공식 스크린샷')
    js = ('tl.from(".t-tag",{opacity:0,x:-30,duration:.5},0).from(".t-ghost",{opacity:0,x:80,duration:1.1},.2)'
          '.from(".ic",{opacity:0,scale:.3,rotation:-20,duration:.6,ease:"back.out(2)"},.2).from(".nm",{opacity:0,x:-40,duration:.7,ease:"power3.out"},.35)'
          '.from(".wh",{opacity:0,y:20,duration:.6},.8).from(".st",{opacity:0,x:-40,duration:.5,stagger:.25},1.2)'
          '.from(".fr,.wn",{opacity:0,y:20,duration:.5,stagger:.15},2.2)'
          '.from(".p1",{opacity:0,y:120,duration:.8,ease:"power3.out"},.6).from(".p2",{opacity:0,y:120,duration:.8,ease:"power3.out"},.85).from(".src",{opacity:0,duration:.5},1.6);')
    G.write(id, 8, b, js, assets=[os.path.join(APPS, f'{key}_icon.png')] + [os.path.join(APPS, f'{key}_s{i}.png') for i in shots])
    m(id)

APPLIST = [('clova', '클로바노트', '회의 기록', '회의·면담 녹음 → 글 → 요약'), ('voicenote', '갤럭시 녹음', '녹음 바로 요약', '설치 없이 기본 앱'),
           ('notebook', 'Gemini Notebook', '자료 정리 · PPT', '지침·보고서 PDF → 요약·슬라이드'), ('perplexity', '퍼플렉시티', '근거 찾기', '출처 링크 달린 답')]

def appmap(id):
    """상황별 앱 지도"""
    b = G.B(7); G.header(b, 'PART 5 · AI 앱 서랍', '상황별로 하나씩', 'Apps.', '이럴 땐, 이 앱', 'chars')
    for i, (k, nm, sit, desc) in enumerate(APPLIST):
        x = 110 + (i % 2) * 870; y = 300 + (i // 2) * 330
        b.add(f'card cd cd{i}', f'left:{x}px;top:{y}px;width:830px;height:290px',
              f'<div class="in a" style="left:40px;top:36px;font-size:26px;font-weight:800;letter-spacing:.2em;color:#ff5a1f">{sit}</div>'
              f'<img class="in a" src="{k}_icon.png" style="left:40px;top:90px;width:140px;height:140px;border-radius:32px"/>'
              f'<div class="in a" style="left:210px;top:100px;font-size:58px;font-weight:900;white-space:nowrap">{nm}</div>'
              f'<div class="in a" style="left:210px;top:182px;font-size:30px;color:#a59f98">{desc}</div>')
    js = G.HEAD_JS['chars'] + G.CARD_FX['zoom'] + G.INNER_FX
    G.write(id, 7, b, js, assets=[os.path.join(APPS, f'{k}_icon.png') for k, *_ in APPLIST])
    m(id)

def applinks(id):
    """단톡방·QR — 바로 설치"""
    import qrcode
    urls = {'clova': 'com.naver.clova.minute', 'voicenote': 'com.sec.android.app.voicenote', 'notebook': 'com.google.android.apps.labs.language.tailwind', 'perplexity': 'ai.perplexity.app.android'}
    b = G.B(6); G.header(b, 'PART 5 · AI 앱 서랍', '폰 카메라로 찍으면 설치 화면', 'Install.', '지금 바로 깔아 두세요', 'mask')
    assets = []
    for i, (k, nm, sit, desc) in enumerate(APPLIST):
        q = qrcode.make(f'https://play.google.com/store/apps/details?id={urls[k]}', border=1, box_size=10).convert('RGB').resize((300, 300))
        f = os.path.join(OUT, id + f'_{k}_qr.png'); q.save(f); assets.append(f)
        x = 110 + i * 435
        b.add(f'card cd cd{i}', f'left:{x}px;top:300px;width:400px;height:560px',
              f'<img class="in a" src="{k}_icon.png" style="left:40px;top:34px;width:80px;height:80px;border-radius:20px"/>'
              f'<div class="in a" style="left:136px;top:44px;font-size:34px;font-weight:900;white-space:nowrap">{nm}</div>'
              f'<div class="in a" style="left:136px;top:90px;font-size:22px;color:#ff5a1f;font-weight:700">{sit}</div>'
              f'<img class="in a" src="{id}_{k}_qr.png" style="left:50px;top:150px;width:300px;height:300px;border-radius:12px"/>'
              f'<div class="in a" style="left:40px;top:478px;width:320px;font-size:22px;color:#a59f98;text-align:center">Play 스토어</div>')
    b.add('a nt', 'left:110px;top:900px;font-size:30px;font-weight:700', G.bold('링크는 **단톡방에도** 올려 드립니다 · 아이폰은 App Store에서 같은 이름으로'))
    js = G.HEAD_JS['mask'] + G.CARD_FX['rise'] + G.INNER_FX + 'tl.from(".nt",{opacity:0,y:20,duration:.5},2.0);'
    G.write(id, 6, b, js, assets=[os.path.join(APPS, f'{k}_icon.png') for k, *_ in APPLIST] + assets)
    for f in assets: os.remove(f)
    m(id)

def three_only():
    """신문물 지도·비교표에서 Hermes·Jev를 빼고 오늘 소개하는 Aside·Muse·Dots만"""
    import re as _re
    f = os.path.join(OUT, 'ladder', 'index.html'); h = open(f).read()
    h = _re.sub(r'<div class="step s1 clip".*?</div>\n', '', h); h = _re.sub(r'<div class="step s3 clip".*?</div>\n', '', h)
    for cls, (left, top, hh, num) in {'s2': (110, 560, 380, '01'), 's4': (690, 440, 500, '02'), 's5 last': (1270, 320, 620, '03')}.items():
        h = _re.sub(rf'(<div class="step {cls} clip" style=")left:\d+px;top:\d+px;height:\d+px(".*?<b>)\d+(</b>)',
                    lambda m: f'{m.group(1)}left:{left}px;top:{top}px;height:{hh}px;width:540px{m.group(2)}{num}{m.group(3)}', h, count=1)
    open(f, 'w').write(h)
    f = os.path.join(OUT, 'compare', 'index.html'); h = open(f).read()
    h = h.replace('<span class="ch">다</span><span class="ch">섯</span>', '<span class="ch">세</span>')
    rows = _re.findall(r'<div class="a tr( last)? clip" style="left:110px;top:\d+px;.*?\n', h)
    lines = [l for l in h.split('\n') if 'class="a tr' in l]
    keep = [l for l in lines if '>Aside<' in l or '>Muse<' in l or '>Dots<' in l]
    for l in lines:
        if l not in keep: h = h.replace(l + '\n', '')
    for i, l in enumerate(keep):
        nl = _re.sub(r'top:\d+px;width:1700px;height:124px', f'top:{360 + i * 170}px;width:1700px;height:170px', l, count=1).replace('height:124px', 'height:170px')
        h = h.replace(l, nl)
    open(f, 'w').write(h)

def page(id, n):
    """국토부 실습 PPT(9.7판) 원본 장을 그림으로 그대로"""
    ORDER.append((id, 'i%d' % n))


def build():
    # ── 오프닝
    r('cover')
    slot('p_vintro', '영상 소개 — 국무회의', '10.20 워크숍 PPT 2장')
    slot('p_intro', '🎬 국무회의 인트로 영상', '10.20 워크숍 PPT 3장 (전체화면 자동 재생)')
    G.qrscene('room', 'OPENING · 단톡방', '카카오톡 오픈채팅', '오늘은 단톡방에서 함께합니다',
              ['폰 카메라로 **QR 찍기**', '**오픈프로필**로 입장 (번호 안 보임)', '참여코드 **1105**', '오늘 만든 것을 **여기에 올립니다**'],
              '카카오톡 오픈채팅\n**입장 QR**', head='chars', listfx='left')
    m('room')
    G.cards('toc2', 'CONTENTS', '오늘 강의는 이렇게 진행합니다', 'Contents.', '폰 하나로, 오늘부터',
            [('01', '정부가 인정한\nAI 인재', 'AI 챔피언과\n달라진 제도'), ('02', '폰으로\n해 보기', '글자 · 사진 · 영상\n직접 만들기'),
             ('03', '요즘\nAI 트렌드', '대답하는 AI에서\n일하는 AI로'), ('04', '말로 만든\n업무 도구', '코딩 없이\n만든 것들'),
             ('05', '우리 사정은\n우리가 안다', '막힌 사이트와\n정보보안')],
            hi=1, fx='build', head='mask', top=300, h=600, numsize=90)
    m('toc2')

    # ── A. 정부가 인정한 AI 인재
    G.intro('pa_in', 1, '정부가 인정한<br>AI 인재', 'AI를 잘 쓰는 공무원, 이제 정부가 공식으로 인정합니다', ['AI 챔피언', '승진·포상', '다른 기관', '그리고 오늘'], 3, 'right')
    m('pa_in')
    G.cards('champ', 'PART 1 · 정부가 인정한 AI 인재', '행정안전부 AI 챔피언', 'Champion.', 'AI 챔피언 — 정부가 인증하는 AI 인재',
            [('01', '무엇', '**행정안전부**가 운영하는\n**AI 챔피언 인증제**'), ('02', '등급', '**그린 → 블루 → 블랙**\n3단계, 최고 등급은\n**BLACK**'),
             ('03', '인사', '경기도: **블루·블랙**에\n**실적 가산점 0.5점**\n승진에 반영'), ('04', '정부 방향', 'AI 고숙련자\n**5급 조기승진 가점**\n2030년 **전문인재 2만 명**')],
            hi=1, key='AI 역량이 이제 **공식 경력**이 됩니다', fx='rise', head='blur', kfx='sweep', numsize=80)
    m('champ')
    # 기사 3건 — 문구는 기사 원문 기준 (26.10.30 확인: 파이낸셜뉴스 26.9.8 · 인천일보 26.9.30 · 병무청 간담회 26.9.30)
    art10('p_art1', 'p1', [('PART 2 · 01', 'PART 1 · 01'),
        ('2030년까지 AI 챔피언 양성 — 전체 공무원의 약 2%', '2030년까지 AI 직접 개발·현장 적용 전문인재 육성'),
        ('5급 조기승진 심사에 블랙 가점', '5급 조기승진 심사에 AI 고숙련자 가점'),
        ('특별성과 포상금 · 연수·학습비 지원', '특별성과 포상금 · 연수·학습 지원'),
        ('AI 정부 실험실 200명 → 6,000명', 'AI 정부 실험실 동시접속 200명 → 6,000명')], [('cap1.jpg', 'cap.jpg')])
    art10('p_art2', 'p2', [('PART 2 · 02', 'PART 1 · 02'),
        ("'실제로 만들 줄 아는 인재'를 우대", '승진에 반영되는 인사 가점')], [('cap2.jpg', 'cap.jpg')])
    art10('p_art3', 'p3', [('PART 2 · 03', 'PART 1 · 03'),
        ('직원의 아이디어가 기관의 과제로', '현장 의견을 실제 업무 개선으로'),
        ('반복 문서 작업을 AI로 줄여 민원과 적극행정에 더 집중하겠습니다', '반복적인 문서·자료 작업에 AI를 활용하니 처리 시간이 크게 줄었다 — 참석 직원'),
        ('<b>출처</b>신아일보', '<b>출처</b>신아일보 · 2026. 9. 30')], [('photo3.jpg', 'photo.jpg')])
    big('reveal_black', '그 최고 등급 BLACK,', '오늘 이 자리에', '서 있습니다', 'Black.', ['119종합상황실', '수상 7건', '27곳 출강·자문', '여러분과 같은 공무원'])
    clip('p_prof1')   # 강사 소개 1 — prof1105.py (웹 프로필 기준, 수상 8건)
    clip('p_prof2')   # 강사 소개 2 — prof1105.py

    # ── PART 2 폰으로 해 보기
    G.intro('pb_in', 2, '폰으로<br>해 봅시다', '폰을 꺼내 주세요 — 막히면 옆 사람과 함께', ['찍으면 글자', '사진을 바꾼다', '사진이 영상이 된다', '단톡방에 올리기'], 0, 'drop')
    m('pb_in')
    G.mission('m_ocr', 1, '찍으면\n글자가 됩니다', 'Gemini', ['Gemini에서 **+ → 카메라**', '**공문·회의 자료** 한 장 찍기', '아래처럼 **말하기**'],
              ['사진 속 글자를 텍스트로만 줘', '표로 정리해 줘', '세 줄로 요약해 줘'],
              '종이로 온 공문·취합 표\n**다시 타자 치지 마세요**', 'up')
    m('m_ocr')
    doc('ocr_doc')
    G.cards('ocr_flow', 'PART 2 · 미션 1', '강사 시연', 'Copy.', '폰에서 찍고, 노트북 한글에 붙입니다',
            [('01', '폰으로 찍기', 'Gemini 카메라로\n**종이 공문** 촬영'), ('02', '텍스트만', '“글자를\n**텍스트로만 줘**”'),
             ('03', '노트북 Gemini', '같은 계정이면\n**대화가 그대로**'), ('04', '한글에 붙이기', '복사 → **한글(HWP)**\n붙여 넣기 끝')],
            hi=3, key='종이 한 장, **다시 칠 필요 없습니다**', fx='left', head='chars', kfx='type', numsize=80)
    m('ocr_flow')
    clip('v_gemini')
    G.mission('m_photo', 2, '사진을 만들고\n고쳐 봅니다', 'Gemini', ['Gemini에 **글로 사진** 만들기', '나온 사진을 **말로 고치기**', '마음에 들면 **저장**'],
              ['세종대왕이 책을 읽는 사진', '책 읽는 상황 말고 노트북하는 상황으로 교체', '낚시하는 상황으로 교체'],
              '방금 영상에서 **강사가 쓴 문장 그대로**\n따라 쓰면 됩니다', 'scale')
    m('m_photo')
    steps2('photo_steps')
    clip('v_flow')
    G.mission('m_flow', 3, '설치부터\n영상까지', 'Google Flow', ['Play 스토어 **「Google Flow」 설치**', '**+ 신규** → **이미지**로 말로 만들기', '사진 골라 **애니메이션**(영상)'],
              ['경복궁 건설 과정을 처음부터 끝까지 이미지로 만들어 줘', '각 사진을 첫 프레임으로 경복궁 짓는 과정을 영상으로', '경남 서부청사를 짓는 과정을 미니어처 스타일로'],
              '무료 — 하루 쓸 수 있는 양이 정해져 있음\n아이폰은 앱이 없으면 **flow.google.com**', 'left')
    m('m_flow')
    phones('flow_phone')
    r('break')
    big('flow_show', '쉬는 동안 만들어진', '여러분의 영상,', '같이 봅니다', 'Video.', ['단톡방', '몇 편 골라', '화면으로', '요청문 나누기'], dur=5)

    # ── PART 3 요즘 AI 트렌드
    G.intro('pc_in', 3, '요즘<br>AI 트렌드', '방금 쉬는 동안에도 AI가 일했습니다', ['AI 에이전트', '신문물 지도', '우리 일에 빗대면', '그래서'], 0, 'scale')
    m('pc_in')
    slot('p_n01', '📰 AI 에이전트 기사', '10.20 워크숍 PPT 9장')
    slot('p_c01', '🎬 AI 에이전트란 · 코딩알려주는누나', '10.20 워크숍 PPT 10장 (영상)')
    rc('sum01', [('PART 4 · 정리', 'PART 3 · 정리')]); rc('ladder', [('PART 4 · 신문물', 'PART 3 · 신문물'), ('시간 순서로 본 다섯 가지 신문물', '오늘 볼 신문물 세 가지')])
    for n, t in (('06', 'Aside'), ('07', 'Muse'), ('08', 'Dots')):
        slot('p_n' + n, f'📰 {t} 기사', '10.20 워크숍 PPT'); slot('p_c' + n, f'🎬 {t} 영상', '10.20 워크숍 PPT')
        rc10('sum' + n, [('PART 1 · 정리', 'PART 3 · 정리'), ({'06': '② Aside', '07': '④ Muse', '08': '⑤ Dots'}[n], {'06': '① Aside', '07': '② Muse', '08': '③ Dots'}[n])])
    rc('compare', [('PART 4 · 신문물', 'PART 3 · 신문물')]); three_only()

    # ── PART 4 말로 만든 업무 도구
    G.intro('pd_in', 4, '말로 만든<br>업무 도구', '코딩은 모릅니다 — 업무가 불편해서 말로 만들었습니다', ['엑셀 → 그래프', '취합 검증', '민원 답변', '오늘 이 화면'], 1, 'blur')
    m('pd_in')
    G.cards('mo07', 'PART 4 · 현실의 벽', '공공기관에서 AI를 쓰려면', 'Wall.', '좋은 건 아는데, 우리 사무실에선 막힙니다',
            [('01', '개인정보', '외부 AI에\n**업로드 불가**'), ('02', '업무망', '내부망에서\n**접속 차단**'), ('03', '설치 승인', '새 프로그램은\n**승인이 필요**')],
            hi=1, key='좋은 건 알아도, **우리 사무실에선 못 씁니다**', fx='flip', head='chars', kfx='sweep', numsize=100)
    m('mo07')
    G.cards('mo06', 'PART 4 · 왜 만들었나', '매달 같은 일', 'Again.', '매달 반복되는 엑셀 취합, 바꾸고 싶지 않으신가요?',
            [('17곳', '양식이 제각각', '기관마다 **다른 양식**\n열 순서·이름도 다름'), ('3시간', '복사·붙여넣기', '**단순 반복**에\n오후가 사라짐'), ('매달', '또 처음부터', '**똑같은 작업**을\n다음 달에 또')],
            hi=1, key='그래서 **말로 도구를 만들었습니다**', fx='rise', head='mask', kfx='type', numsize=100)
    m('mo06')
    what_html('html_what')
    G.cards('mo08', 'PART 4 · HTML 특징', 'AI를 못 쓰는 환경이라서', 'Why.', 'HTML 특징 세 가지',
            [('01', '설치 없이', '인터넷 창만 있으면\n**바로 실행**'), ('02', '파일 하나', '메신저·메일로\n**부서와 공유**'), ('03', '내 PC 안에서', '자료가 밖으로 안 나가고\n**안전하게 계산**')],
            hi=2, key='AI는 **만들 때만**, 쓰는 건 **내 PC 안에서**', fx='wipe', head='mask', kfx='type', numsize=100)
    m('mo08')
    G.cards('tools', 'PART 4 · 말로 만든 업무 도구', '강사가 업무에 쓰려고 만든 것', 'Made.', '업무가 불편해서, 말로 만들었습니다',
            [('01', '엑셀 → 그래프', '엑셀을 넣으면\n**보고서용 그래프**\n국토부 실습 도구'), ('02', '취합 검증', '여러 곳 취합 파일의\n**틀린 숫자** 찾기\n국토부 실습 도구'),
             ('03', '민원 답변', '**AI 기반 소방 민원\n답변 자동화**\n수상작'), ('04', '오늘 이 화면', '움직이는 강의 화면도\n**말로 주문**했습니다')],
            hi=1, key='지금부터 **실제 화면**으로 보여 드립니다', fx='wipe', head='mask', kfx='type', numsize=80)
    m('tools')
    G.cards('t1_intro', 'PART 4 · 도구 1', '시각화 자료 만들기', 'Chart.', '엑셀만 넣으면, 보고서용 그래프',
            [('01', '엑셀 넣기', '취합한 엑셀을\n**끌어다 놓기**'), ('02', '그래프 자동', '항목을 고르면\n**막대·선·원형**'), ('03', '한글에 붙이기', '**PNG로 저장**해\n보고서에 바로')],
            hi=1, key='국토부 실습 자료를 넣으면 — **다음 화면처럼** 나옵니다', fx='rise', head='mask', kfx='type', numsize=100)
    m('t1_intro')
    fullshot('t1_full', 'PART 4 · 도구 1 결과', '도구1_시각화 자료만들기.html — test1 부산지방국토관리청.xlsx', 'tool1R.png', '국토부 실습 엑셀을 넣은 실제 화면')
    big('demo1', '지금부터 제 노트북에서', '직접', '보여 드립니다', 'Demo.', ['엑셀 올리기', '그래프 고르기', 'PNG 저장', '한글에 붙이기'], dur=5)
    G.cards('t3_intro', 'PART 4 · 도구 3', '제출자료 취합·검증기', 'Merge.', '여러 곳에서 온 파일, 한 번에 모으고 검사',
            [('01', '파일 여러 개', '기관별 엑셀을\n**한꺼번에 선택**'), ('02', '틀린 곳 찾기', '빈칸·형식 오류·중복\n**자동 표시**'), ('03', '한 파일로', '기준 양식에 맞춰\n**자동 합치기**')],
            hi=1, key='3개 기관 파일을 넣으면 — **다음 화면처럼** 나옵니다', fx='wipe', head='mask', kfx='type', numsize=100)
    m('t3_intro')
    fullshot('t3_full', 'PART 4 · 도구 3 결과', '도구3_취합검증기.html — test1·2·3 (부산·대전·익산청)', 'tool3R.png', '파일 3개 · 47행 · 확인 필요 7행')
    big('demo2', '여러 곳에서 온 취합 파일,', '틀린 숫자를', '찾아 줍니다', 'Check.', ['파일 여러 개', '오류 검증', '자동 병합', '완성본 저장'], dur=5)

    # ── PART 5 중견리더의 AI 앱 서랍 (무료 조건은 26.10 기준 — 강의 전 다시 확인)
    G.intro('pe_in', 5, '중견리더의<br>AI 앱 서랍', '폰에 깔아 두면, 내일부터 일이 줄어듭니다', ['회의 기록', '녹음 요약', '자료 정리 · PPT', '근거 찾기'], 0, 'spin')
    m('pe_in')
    appmap('app_map')
    app('app_clova', 'clova', '클로바노트', 'NAVER', '회의·면담·교육 녹음 → **글로 바꾸고 요약·다음 할 일**까지',
        ['회의 시작할 때 **녹음** 누르기', '끝나면 자동으로 **글 + 화자 구분**', '**AI 요약** → 결정 사항·할 일'],
        '개인 월 300분 (동의 시 600분) · AI 요약 월 15회', '**내부 회의·민원 면담**은 기관 지침 먼저 — 공개 회의·교육·내 메모부터', [1, 2], 'Note.')
    app('app_voicenote', 'voicenote', '갤럭시 녹음', 'Samsung · 기본 앱', '설치 없이 — 갤럭시 **기본 녹음 앱**에서 바로 **글 변환·요약**',
        ['기본 **음성 녹음** 앱으로 녹음', '**텍스트 변환** 누르기', '**요약** 누르면 핵심만'],
        '기본 앱 (Galaxy AI 지원 기종 — S24 이후)', '변환 글은 **틀릴 수 있음** — 이름·숫자는 다시 확인', [1, 3], 'Record.')
    app('app_notebook', 'notebook', 'Gemini Notebook', 'Google · 구 NotebookLM', '지침·보고서 **PDF 여러 개를 올리면** 요약·질문 답·**슬라이드(PPTX)**까지',
        ['**+ 새 노트북** → 자료 올리기', '“핵심 5줄로” — **자료 안에서만** 답', '**슬라이드** 만들기 → PPTX로'],
        'Gemini 앱 메뉴 「Notebooks」에서', '올리는 자료는 **공개된 지침·법령·보도자료**만', [1, 2], 'Notebook.')
    app('app_perplexity', 'perplexity', '퍼플렉시티', 'Perplexity', '질문하면 **출처 링크가 달린 답** — “근거 어디 있어?”에 강함',
        ['궁금한 것을 **말로 질문**', '답 아래 **출처 번호** 확인', '원문 링크로 **직접 확인**'],
        '기본 검색 무료', '출처가 있어도 **원문은 내가 한 번 더**', [1, 2], 'Search.')
    G.cards('app_safe', 'PART 5 · AI 앱 서랍', '앱 공통', 'Safe.', '넣기 전에, 한 번만 생각하세요',
            [('O', '넣어도 됩니다', '이미 배포한 **보도자료**\n공개된 **법령·지침**\n**내 메모**·교육 녹음'),
             ('X', '넣으면 안 됩니다', '**민원인** 이름·연락처\n**내부 보고서** 원문\n**결재 전** 계획·예산')],
            hi=1, key='앱이 정리해 줘도, **확인은 사람이** 합니다', fx='split', head='blur', kfx='sweep', numsize=110)
    m('app_safe')
    rc('m4', [('PART 2 · 미션 4', 'PART 5 · 확인은 사람이')])
    rc('m4ans', [('PART 2 · 미션 4', 'PART 5 · 확인은 사람이')])
    applinks('app_links')

    # ── 마무리
    r('act')
    big('next', '정부가 인정한 AI 인재,', '다음은', '여러분입니다', 'Next.', ['오늘 배운 한 가지', '내일 업무에', '옆 동료에게', '단톡방에 한 줄'])
    r('closing')
    slot('p_promo', '🎬 강사 홍보 영상', '10.20 워크숍 PPT 50장 (전체화면 자동 재생)')
    r('qna')


if __name__ == '__main__':
    build()
    json.dump(ORDER, open(os.path.join(OUT, 'order.json'), 'w'), ensure_ascii=False)
    print(len(ORDER), 'slides,', sum(1 for _, k in ORDER if k == 'm'), 'new motion →', OUT)
