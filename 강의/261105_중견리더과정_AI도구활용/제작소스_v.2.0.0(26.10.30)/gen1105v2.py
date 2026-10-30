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


PHONE = os.environ.get('PHONE', os.path.join(os.path.dirname(OUT), 'phone'))   # Flow 폰 화면(fp0~fp5.png)

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
        ('STEP 1', '만들기', '조선 시대 방에서 세종대왕이 책을 읽고 있는 사진을 만들어 줘', '사진이 없어도 **글로 사진**을 만듭니다'),
        ('STEP 2', '고치기', '책 대신 노트북으로 일하는 모습으로 바꿔 줘', '마음에 안 들면 **이어서 말하면** 고쳐집니다')]):
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
    items = [('fp0.png', '설치', 'Play 스토어<br>「Google Flow」 설치'), ('fp1.png', '새로 만들기', '구글 로그인 →<br><b>+ New</b>'),
             ('fp2.png', '말로 만들기', '<b>Image</b> 고르고<br>만들 장면을 입력'), ('fp3.png', '내 사진 올리기', '<b>+</b> → 갤러리에서<br>미션 2 사진'),
             ('fp5.png', '영상으로', '<b>Animate</b> → 영상<br><b>Download</b> → 카톡')]
    b = G.B(8); G.header(b, 'PART 2 · 미션 3', '폰에서 이렇게 — Google Flow', 'Flow.', '설치부터 이미지·영상까지, 폰 화면으로', 'chars')
    for i, (img, t, cap) in enumerate(items):
        x = 110 + i * 344
        b.add(f'a ph ph{i}', f'left:{x}px;top:270px;width:320px',
              f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px"><span style="width:46px;height:46px;border-radius:50%;background:{"#ff5a1f" if i==4 else "#3a3533"};color:{"#111" if i==4 else "#f4f4f2"};font-size:26px;font-weight:900;display:flex;align-items:center;justify-content:center">{i+1}</span><span style="font-size:32px;font-weight:800">{t}</span></div>'
              f'<div style="width:320px;height:520px;border-radius:28px;overflow:hidden;background:#fff;border:6px solid #2a2523"><img src="{img}" style="width:100%;height:100%;object-fit:cover;object-position:top"/></div>'
              f'<div style="margin-top:14px;font-size:24px;line-height:1.4;color:#d6d2c9">{cap}</div>')
    b.add('a src', 'left:110px;top:1040px;font-size:18px;color:#8a847e', '화면: Google Play 「Google Flow」 페이지 · 앱 공식 스크린샷(영문 화면) — 실제 앱은 한국어로 보일 수 있음 · 아이폰은 앱이 없으면 flow.google.com')
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
            [('01', '무엇', '**행정안전부**가\nAI를 업무에 잘 쓰는\n**공무원을 인증**합니다'), ('02', '등급', '**그린 → 블루 → 블랙**\n최고 등급은\n**BLACK**'),
             ('03', '혜택', '**5급 조기승진**\n성과심사 가점\n포상금 · 연수 지원'), ('04', '목표', '2030년까지\n**2만 명**\n(전체 공무원 약 2%)')],
            hi=1, key='AI 역량이 이제 **공식 경력**이 됩니다', fx='rise', head='blur', kfx='sweep', numsize=80)
    m('champ')
    slot('p_art1', '기사 — AI 잘 쓰는 공무원에 승진·포상 인센티브', '10.20 워크숍 PPT 43장 · 파이낸셜뉴스 — 5급 조기승진 성과심사 가점')
    slot('p_art2', '기사 — 경기도 AI 챔피언 실적 가산점', '10.20 워크숍 PPT 44장')
    slot('p_art3', '기사 — 병무청장, AI 챔피언 간담회', '10.20 워크숍 PPT 45장 (사진)')
    big('reveal_black', '그 최고 등급 BLACK,', '오늘 이 자리에', '서 있습니다', 'Black.', ['119종합상황실', '수상 7건', '27곳 출강·자문', '여러분과 같은 공무원'])
    slot('p_prof1', '강사 소개 1', '10.20 워크숍 PPT 4장 (사진·지표·수상)')
    slot('p_prof2', '강사 소개 2', '10.20 워크숍 PPT 5장 (강의·자격·언론)')

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
              ['세종대왕이 방에서 책을 읽는 사진', '책 대신 노트북으로 일하게 바꿔 줘', '배경을 진주성 야경으로 바꿔 줘'],
              '저장한 사진은\n**미션 3에서 영상으로** 만듭니다', 'scale')
    m('m_photo')
    steps2('photo_steps')
    clip('v_flow')
    G.mission('m_flow', 3, '설치부터\n영상까지', 'Google Flow', ['Play 스토어 **「Google Flow」 설치**', '**+ New** → Image로 **말로 만들기**', '**미션 2 사진** 올려 **Animate**(영상)'],
              ['한옥 마루에 앉은 세종대왕 그림', '세종대왕이 웃으며 손을 흔들게', '카메라가 천천히 다가가게'],
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
    rc('sum01', [('PART 4 · 정리', 'PART 3 · 정리')]); rc('ladder', [('PART 4 · 신문물', 'PART 3 · 신문물')])
    for n, t in (('06', 'Aside'), ('07', 'Muse'), ('08', 'Dots')):
        slot('p_n' + n, f'📰 {t} 기사', '10.20 워크숍 PPT'); slot('p_c' + n, f'🎬 {t} 영상', '10.20 워크숍 PPT')
        rc10('sum' + n, [('PART 1 · 정리', 'PART 3 · 정리')])
    rc('compare', [('PART 4 · 신문물', 'PART 3 · 신문물')])

    # ── PART 4 말로 만든 업무 도구
    G.intro('pd_in', 4, '말로 만든<br>업무 도구', '코딩은 모릅니다 — 업무가 불편해서 말로 만들었습니다', ['엑셀 → 그래프', '취합 검증', '민원 답변', '오늘 이 화면'], 1, 'blur')
    m('pd_in')
    G.cards('mo06', 'PART 4 · 왜 만들었나', '매달 같은 일', 'Again.', '매달 반복되는 엑셀 취합, 바꾸고 싶지 않으신가요?',
            [('17곳', '양식이 제각각', '기관마다 **다른 양식**\n열 순서·이름도 다름'), ('3시간', '복사·붙여넣기', '**단순 반복**에\n오후가 사라짐'), ('매달', '또 처음부터', '**똑같은 작업**을\n다음 달에 또')],
            hi=1, key='불편함이 곧 **만들 거리**입니다', fx='rise', head='mask', kfx='type', numsize=100)
    m('mo06')
    G.cards('mo07', 'PART 4 · 현실의 벽', '공공기관에서 AI를 쓰려면', 'Wall.', '좋은 건 아는데, 우리 사무실에선 막힙니다',
            [('01', '개인정보', '외부 AI에\n**업로드 불가**'), ('02', '업무망', '내부망에서\n**접속 차단**'), ('03', '설치 승인', '새 프로그램은\n**승인이 필요**')],
            hi=1, key='그래서 **다른 길**을 찾았습니다', fx='flip', head='chars', kfx='sweep', numsize=100)
    m('mo07')
    G.cards('mo08', 'PART 4 · 왜 HTML인가', 'AI를 못 쓰는 환경이라서', 'HTML.', 'AI를 못 쓰는 환경이라서, HTML',
            [('01', '설치 없이', '인터넷 창만 있으면\n**바로 실행**'), ('02', '파일 하나', '메신저·메일로\n**부서와 공유**'), ('03', '내 PC 안에서', '자료가 밖으로 안 나가고\n**안전하게 계산**')],
            hi=2, key='AI는 **만들 때만**, 쓰는 건 **내 PC 안에서**', fx='wipe', head='mask', kfx='type', numsize=100)
    m('mo08')
    G.cards('mo09', 'PART 4 · HTML의 새로운 활용', '화면 + 기능 = 작은 프로그램', 'Build.', '웹 화면에 계산 기능을 더하면, 작은 프로그램',
            [('화면', '인터넷 문서', '글·표·그림이 보이는\n**웹 화면**'), ('+ 기능', '계산·버튼', '버튼 누르면\n**계산·정리**'), ('= 도구', '작은 프로그램', '문법은 몰라도\n**말로 주문**')],
            hi=2, key='코딩 대신 **“이렇게 만들어 줘”**', fx='zoom', head='blur', kfx='pop', numsize=100)
    m('mo09')
    G.cards('mo10', 'PART 4 · 활용 범위', '어디까지 쓰면 좋을까', 'Scope.', '개인과 팀의 반복 업무에 쓰는 것이 가장 좋습니다',
            [('O', '적합', '팀 **반복 작업**\n자료 **취합·정리**\n보고서용 **그래프**'), ('X', '부적합', '**여러 명 동시 접속** 시스템\n**공식 시스템**은 정보화부서로')],
            hi=0, key='작게, 내 업무부터 — **큰 시스템은 정보화부서**와', fx='split', head='mask', kfx='sweep', numsize=110)
    m('mo10')
    G.cards('tools', 'PART 4 · 말로 만든 업무 도구', '강사가 업무에 쓰려고 만든 것', 'Made.', '업무가 불편해서, 말로 만들었습니다',
            [('01', '엑셀 → 그래프', '엑셀을 넣으면\n**보고서용 그래프**\n국토부 실습 도구'), ('02', '취합 검증', '여러 곳 취합 파일의\n**틀린 숫자** 찾기\n국토부 실습 도구'),
             ('03', '민원 답변', '**AI 기반 소방 민원\n답변 자동화**\n수상작'), ('04', '오늘 이 화면', '움직이는 강의 화면도\n**말로 주문**했습니다')],
            hi=1, key='지금부터 **실제 화면**으로 보여 드립니다', fx='wipe', head='mask', kfx='type', numsize=80)
    m('tools')
    shot('mo12', 'PART 4 · 도구 1', '엑셀 데이터 시각화', 'Chart.', '엑셀만 넣으면, 보고서용 그래프',
         [('엑셀 올리기', '파일을 끌어다 놓기'), ('항목 고르기', '보여 줄 열 선택'), ('그래프 만들기', '막대·선·원형'), ('그림 저장', 'PNG → 한글에 붙이기')],
         'tool1.png', '도구1_시각화 자료만들기.html', '')
    beforeafter('mo20')
    big('demo1', '지금부터 제 노트북에서', '직접', '보여 드립니다', 'Demo.', ['엑셀 올리기', '그래프 고르기', 'PNG 저장', '한글에 붙이기'], dur=5)
    shot('mo30', 'PART 4 · 도구 3', '제출자료 취합·검증기', 'Merge.', '여러 곳에서 온 파일, 한 번에 모으고 검사',
         [('파일 여러 개', '한꺼번에 선택'), ('오류 검사', '빈칸·틀린 숫자 표시'), ('자동 합치기', '양식 맞춰 병합'), ('완성본 저장', '엑셀로 내려받기')],
         'tool3.png', '도구3_취합검증기.html', '')
    big('demo2', '여러 곳에서 온 취합 파일,', '틀린 숫자를', '찾아 줍니다', 'Check.', ['파일 여러 개', '오류 검증', '자동 병합', '완성본 저장'], dur=5)
    prompts('mo45')

    # ── PART 5 우리 사정은 우리가 안다
    G.intro('pe_in', 5, '우리 사정은<br>우리가 안다', '사무실 PC에서 안 열리죠 — 저도 그렇습니다', ['막힌 사이트', '넣으면 안 되는 것', '정부 방향', '확인은 사람이'], 1, 'spin')
    m('pe_in')
    big('blocked', '사무실 PC에서 챗GPT,', '열리시나요?', '', 'Blocked.', ['업무망·인터넷망 분리', '생성형 AI 차단', '그래서 오늘은 폰으로', '폰이라도 지킬 것'], dur=5)
    G.cards('safe2', 'PART 5 · 정보보안', '우리 서류로 보면', 'Safe.', '넣어도 되는 것, 넣으면 안 되는 것',
            [('O', '넣어도 됩니다', '이미 배포한 **보도자료**\n공개된 **법령·지침**\n홈페이지 **공지**'),
             ('X', '넣으면 안 됩니다', '**민원인** 이름·연락처\n**내부 보고서** 원문\n**결재 전** 계획·예산')],
            hi=1, key='꼭 필요하면 **가명 · 요약**으로 바꿔서', fx='split', head='blur', kfx='sweep', numsize=110)
    m('safe2')
    G.cards('n2sf', 'PART 5 · 정부 방향', '국가망보안체계(N2SF)', 'Grade.', '‘쓰지 마라’에서 ‘등급 보고 써라’로',
            [('C', '기밀', '외부 AI에\n**절대 넣지 않음**'), ('S', '민감', '엄격한 통제 안에서만\n**기관 지침 확인**'), ('O', '공개', '승인된 생성형 AI로\n**활용 가능**')],
            hi=2, key='정확한 적용은 **소속 기관 지침**을 확인하세요', fx='flip', head='chars', kfx='type', numsize=110)
    m('n2sf')
    rc('m4', [('PART 2 · 미션 4', 'PART 5 · 확인은 사람이')])
    rc('m4ans', [('PART 2 · 미션 4', 'PART 5 · 확인은 사람이')])

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
