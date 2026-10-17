# 분해판 2단계 — 사진(img 개체)을 화면에 보이는 부분만 잘라 저장하고, 둥근 액자 바깥 모서리는 바탕색으로 채운다.
# 사용: python3 split_prep.py <split_extract 결과 폴더> <원본 장면 그림 폴더(s###.jpg)>   → c###_i.jpg(또는 .png) 만들고 o###.json에 file 기록
# 모서리 밖은 원본 장면에서 같은 자리 색을 가져와 채움(흰 액자는 흰색, 어두운 액자는 어두운색).
import sys, os, json, glob
from PIL import Image, ImageDraw
D, ORIG = sys.argv[1], sys.argv[2]
for f in sorted(glob.glob(os.path.join(D, 'o*.json'))):
    n = os.path.basename(f)[1:4]; ops = json.load(open(f)); bg = Image.open(os.path.join(ORIG, f's{n}.jpg')).convert('RGB').resize((1920, 1080)); i = 0
    for o in ops:
        if o['t'] != 'img': continue
        i += 1
        im = Image.open(o['src']); alpha = im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info or im.mode in ('RGBA', 'LA')
        im = im.convert('RGBA' if alpha else 'RGB')
        box = (max(0, round(o['sx'])), max(0, round(o['sy'])), min(im.width, round(o['sx'] + o['sw'])), min(im.height, round(o['sy'] + o['sh'])))
        im = im.crop(box)
        W, H = max(1, round(o['w'] * 1.5)), max(1, round(o['h'] * 1.5))   # 화면 크기의 1.5배까지만(용량)
        if im.width > W or im.height > H: im = im.resize((min(im.width, W), min(im.height, H)), Image.LANCZOS)
        if o.get('rad', 0) > 0.5 and not alpha:   # 둥근 모서리 밖을 원본 화면 색으로
            k = im.width / o['w']; r = round(o['rad'] * k)
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
            back = bg.crop((round(o['x']), round(o['y']), round(o['x'] + o['w']), round(o['y'] + o['h']))).resize(im.size)
            im = Image.composite(im, back, m)
        name = f'c{n}_{i}.' + ('png' if alpha else 'jpg')
        (im.save(os.path.join(D, name)) if alpha else im.save(os.path.join(D, name), quality=88))
        o['file'] = name
    json.dump(ops, open(f, 'w'))
print('ok')
