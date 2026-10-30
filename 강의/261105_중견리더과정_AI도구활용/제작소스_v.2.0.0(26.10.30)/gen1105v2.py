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
    G.cards('ocr_flow', 'PART 2 · 미션 1', '강사 시연', 'Copy.', '폰에서 찍고, 노트북 한글에 붙입니다',
            [('01', '폰으로 찍기', 'Gemini 카메라로\n**종이 공문** 촬영'), ('02', '텍스트만', '“글자를\n**텍스트로만 줘**”'),
             ('03', '노트북 Gemini', '같은 계정이면\n**대화가 그대로**'), ('04', '한글에 붙이기', '복사 → **한글(HWP)**\n붙여 넣기 끝')],
            hi=3, key='종이 한 장, **다시 칠 필요 없습니다**', fx='left', head='chars', kfx='type', numsize=80)
    m('ocr_flow')
    v('v_gemini', '🎬 Gemini 사진 편집 소개 영상', '새 영상 — 강사가 내려받은 파일로 교체 (후보 링크는 진행요약)')
    G.mission('m_photo', 2, '사진을\n바꿔 봅니다', 'Gemini', ['Gemini에서 **+ → 사진** 고르기', '**셀카** 또는 앨범 속 사진', '바꾸고 싶은 모습을 **말로**'],
              ['배경을 진주성 야경으로 바꿔 줘', '흑백 사진을 컬러로 복원해 줘', '행사 포스터로 만들어 줘'],
              '다 되면 **저장** →\n**미션 3에서 영상으로** 만듭니다', 'scale')
    m('m_photo')
    v('v_flow', '🎬 Google Flow 사진 → 영상 소개 영상', '새 영상 — 강사가 내려받은 파일로 교체 (후보 링크는 진행요약)')
    G.mission('m_flow', 3, '그 사진이\n영상이 됩니다', 'Google Flow', ['**Flow 앱** 설치 (안 되면 labs.google/flow)', '구글 로그인 → **+ 새로 만들기**', '**미션 2 사진** 올리고 움직임을 말로'],
              ['사람이 웃으며 손을 흔들게', '눈이 내리고 하늘을 올려다보게', '카메라가 천천히 다가가게'],
              '무료 — 하루 **빠른 영상 2편** 정도\n만드는 동안 **쉬는 시간**', 'left')
    m('m_flow')
    r('break')
    big('flow_show', '쉬는 동안 만들어진', '여러분의 영상,', '같이 봅니다', 'Video.', ['단톡방', '몇 편 골라', '화면으로', '요청문 나누기'], dur=5)

    # ── PART 3 요즘 AI 트렌드
    G.intro('pc_in', 3, '요즘<br>AI 트렌드', '방금 쉬는 동안에도 AI가 일했습니다', ['AI 에이전트', '신문물 지도', '우리 일에 빗대면', '그래서'], 0, 'scale')
    m('pc_in')
    slot('p_n01', '📰 AI 에이전트 기사', '10.20 워크숍 PPT 9장')
    slot('p_c01', '🎬 AI 에이전트란 · 코딩알려주는누나', '10.20 워크숍 PPT 10장 (영상)')
    rc('sum01', [('PART 4 · 정리', 'PART 3 · 정리')]); rc('ladder', [('PART 4 · 신문물', 'PART 3 · 신문물')]); rc('compare', [('PART 4 · 신문물', 'PART 3 · 신문물')])

    # ── PART 4 말로 만든 업무 도구
    G.intro('pd_in', 4, '말로 만든<br>업무 도구', '코딩은 모릅니다 — 업무가 불편해서 말로 만들었습니다', ['엑셀 → 그래프', '취합 검증', '민원 답변', '오늘 이 화면'], 1, 'blur')
    m('pd_in')
    G.cards('tools', 'PART 4 · 말로 만든 업무 도구', '강사가 업무에 쓰려고 만든 것', 'Made.', '업무가 불편해서, 말로 만들었습니다',
            [('01', '엑셀 → 그래프', '엑셀을 넣으면\n**보고서용 그래프**\n국토부 실습 도구'), ('02', '취합 검증', '여러 곳 취합 파일의\n**틀린 숫자** 찾기\n국토부 실습 도구'),
             ('03', '민원 답변', '**AI 기반 소방 민원\n답변 자동화**\n수상작'), ('04', '오늘 이 화면', '움직이는 강의 화면도\n**말로 주문**했습니다')],
            hi=1, key='지금부터 **실제 화면**으로 보여 드립니다', fx='wipe', head='mask', kfx='type', numsize=80)
    m('tools')

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
