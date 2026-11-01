# 「따라 하기」 컷 — 시연 녹화에서 누르는 순간을 뽑아 빨간 테두리를 그린 그림 (슬라이드 4컷씩)
# 사용: python3 cuts1105.py <출력폴더(cuts)>   환경: W1030, UPD (clip2_1105.py와 같음)
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W1030 = os.environ.get('W1030', '/home/user/ppt-auto-html-/data/west')
UPD = os.environ.get('UPD', '/home/user/ppt-auto-html-/data/upd')
G = f'{W1030}/Screen_Recording_20261030_205508_Google.mp4'
FO = f'{W1030}/Screen_Recording_20261030_210531_Flow.mp4'
FN = f'{UPD}/Screen_Recording_20261101_104717_Flow.mp4'
SW, SH, CH = 1080, 2340, 1400          # 원본 크기, 잘라 낼 높이
FB = '/root/.fonts/Pretendard-Bold.otf'
HIDE = {FO: [(45.3, 50.0, 0, 0, 1080, 2340), (43.5, 56.0, 0, 1760, 1080, 220)]}   # 계정 목록(이메일) 가림

# (파일, 초, x, y, w, h, 설명)
CUTS = {
 'g': [(G, 0.5, 570, 960, 190, 230, 'Play 스토어 열기'), (G, 5.0, 440, 2000, 190, 150, '아래 「검색」 누르기'),
       (G, 14.2, 870, 1660, 150, 140, '「제미나이」 입력 → 검색'), (G, 23.0, 545, 810, 495, 115, '「열기」'),
       (G, 26.6, 880, 465, 125, 125, '안내창 닫기(X)'), (G, 31.8, 50, 150, 130, 120, '왼쪽 위 메뉴(☰)'),
       (G, 35.0, 20, 605, 740, 115, '「이미지」 고르기'), (G, 58.3, 840, 945, 125, 125, '“세종대왕이 책을 읽는 사진” → 보내기'),
       (G, 76.8, 60, 650, 960, 540, '만든 사진 누르기'), (G, 87.4, 790, 2000, 200, 120, '「저장」'),
       (G, 117.3, 830, 940, 130, 130, '“책 읽는 상황 말고 노트북하는 상황으로 교체” → 보내기'), (G, 167.4, 830, 1090, 130, 130, '“낚시하는 상황으로 교체” → 보내기')],
 'f': [(FO, 4.2, 445, 2000, 190, 150, 'Play 스토어 「검색」'), (FO, 21.7, 15, 470, 1050, 215, '「Google Flow」 고르기'),
       (FO, 26.6, 35, 805, 1010, 120, '「설치」'), (FO, 39.9, 545, 560, 495, 135, '「열기」'),
       (FO, 53.2, 60, 2005, 960, 125, '구글 계정으로 계속'), (FO, 57.3, 60, 2000, 960, 120, '「시작하기」'),
       (FO, 62.5, 760, 1095, 290, 125, '「+ 신규」 프로젝트'), (FN, 1.5, 590, 1990, 240, 110, '「이미지」 설정 열기'),
       (FN, 14.0, 850, 1880, 130, 100, '「x4」 — 4장 만들기'), (FN, 31.7, 870, 1095, 130, 130, '“조선시대 열심히 공부하는 학자들” → 보내기'),
       (FN, 85.1, 40, 2010, 470, 110, '사진 고르고 「수정」'), (FN, 125.4, 870, 1100, 130, 130, '“공부 후 휴식을 취하는 학자들, 저녁 배경으로” → 보내기'),
       (FN, 209.9, 560, 2010, 480, 110, '「애니메이션」'), (FN, 255.0, 870, 995, 130, 130, '“신이 나서 흥이 나는 분위기” → 보내기'),
       (FN, 337.4, 380, 850, 520, 90, '영상 ⋮ → 「다운로드」'), (FN, 343.1, 370, 1380, 520, 90, '720p → 「업스케일 및 다운로드」')],
}

def grab(src, t):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       stdout=subprocess.PIPE, check=True)
    return Image.frombuffer('RGB', (SW, SH), r.stdout, 'raw', 'RGB', 0, 1).copy()

meta = {}
for k, cuts in CUTS.items():
    meta[k] = []
    for i, (src, t, x, y, w, h, lab) in enumerate(cuts):
        im = grab(src, t); d = ImageDraw.Draw(im)
        for h0, h1, hx, hy, hw, hh in HIDE.get(src, []):
            if h0 <= t <= h1: d.rectangle([hx, hy, hx + hw, hy + hh], fill=(29, 26, 25))
        m = Image.new('L', im.size, 95); ImageDraw.Draw(m).rounded_rectangle([x, y, x + w, y + h], 18, fill=0)
        im = Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, m); d = ImageDraw.Draw(im)
        d.rounded_rectangle([x - 10, y - 10, x + w + 10, y + h + 10], 26, outline=(255, 30, 30), width=18)
        cy = y + h / 2; top = int(min(max(cy - CH / 2, 0), SH - CH))
        f = f'{k}{i+1:02d}.png'; im.crop((0, top, SW, top + CH)).resize((540, 700), Image.LANCZOS).save(os.path.join(OUT, f))
        meta[k].append((f, lab))

# Gemini 결과 사진 3장 (사진 보기 화면에서 그림 부분만)
for i, t in enumerate([77.6, 135.0, 190.0]):
    im = grab(G, t)   # 사진 보기 화면: 그림은 (48,900)-(1032,1432)
    im.crop((48, 902, 1032, 1430)).save(os.path.join(OUT, f'gres{i+1}.jpg'), quality=92)
json.dump(meta, open(os.path.join(OUT, 'cuts.json'), 'w'), ensure_ascii=False)
print({k: len(v) for k, v in meta.items()})
