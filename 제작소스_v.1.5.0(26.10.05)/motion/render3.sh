cd "$(dirname "$0")"
render(){ for d in $(awk "NR%3==$1" render_list.txt); do (cd $d && rm -f out.mp4 && timeout 400 npx hyperframes render --crf 24 -o out.mp4 >/dev/null 2>&1; echo "$d $(stat -c %s out.mp4 2>/dev/null || echo FAIL)"); done; }
render 0 & render 1 & render 2 & wait
