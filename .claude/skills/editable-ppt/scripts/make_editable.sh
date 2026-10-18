#!/bin/bash
# 장면 HTML → 글자 고칠 수 있는 분해판 PPT 한 번에 만들기 (editable-ppt 스킬)
# 사용: make_editable.sh <장면 폴더 SPEC> <작업 폴더> <영상 첫 화면 폴더> <OUT.pptx> [건너뛸 영상 장(쉼표)]
#   SPEC 예: "1-40:p2/g1,41-86:p2/h2,87-120:p2/h3"   (장:폴더 — 폴더 안에 v###.html)
#   한 장만 다른 폴더면 "2-2:wsh,3-40:p2/g1"처럼 범위를 쪼갬
# 단계: ① 카드 글자 맞춤(fit_cards) ② 손볼 장 고치기(있으면 <작업 폴더>/fix.js 실행) ③ 본문 SemiBold(semibold)
#       ④ 장면 그림 찍기 ⑤ 분해(split_extract → split_prep → ghost_extract) ⑥ 조립(split_build → split_titles) ⑦ 검사(check_text · check_pptx)
# ※ split_build.js 맨 위 VIDEO · EMBED · ART · LINKS · NAME_FIX · SECTION은 강의마다 고쳐서 쓴다.
set -e
SPEC=$1; W=$2; MEDIA=$3; OUT=$4; SKIP=${5:-}
K="$(cd "$(dirname "$0")" && pwd)"; NP=/opt/node22/lib/node_modules
mkdir -p "$W"
# SPEC의 폴더들을 fit 폴더 기준 SPEC으로 바꿈(fit_cards는 <fit>/<폴더 이름>/v###.html로 씀)
FSPEC=$(python3 -c "
import sys,os
print(','.join(p.split(':')[0]+':'+os.path.join('$W/fit',os.path.basename(p.split(':')[1].rstrip('/'))) for p in sys.argv[1].split(',')))" "$SPEC")
echo "① 카드 글자 맞춤"; NODE_PATH=$NP node "$K/fit_cards.js" "$W/fit" "$SPEC"
if [ -f "$W/fix.js" ]; then echo "② 손볼 장"; NODE_PATH=$NP node "$W/fix.js" "$W/fit"; fi
echo "③ 본문 SemiBold"; NODE_PATH=$NP node "$K/semibold.js" "$W/fit"
echo "④ 장면 그림"; mkdir -p "$W/shots"; NODE_PATH=$NP node "$K/shot_all.js" "$W/shots" "$FSPEC"
echo "⑤ 분해"; NODE_PATH=$NP node "$K/split_extract.js" "$W/sp" "$FSPEC" > /dev/null
python3 -I "$K/split_prep.py" "$W/sp" "$W/shots"
NODE_PATH=$NP node "$K/ghost_extract.js" "$W/sp/gh.json" "$FSPEC"
echo "⑥ 조립"; NODE_PATH=${PPTXGEN_PATH:-$NP} node "$K/split_build.js" "$W/sp" "$MEDIA" "$W/sp/a.pptx"
python3 -I "$K/split_titles.py" "$W/sp/a.pptx" "$W/sp/a_titles.json" "$OUT"
echo "⑦ 검사"; NODE_PATH=$NP node "$K/check_text.js" "$OUT" "$FSPEC" "$SKIP"; python3 -I "$K/check_pptx.py" "$OUT" | grep -E "^slides|^runs|^bad|generic|theme"
echo DONE "$OUT"
