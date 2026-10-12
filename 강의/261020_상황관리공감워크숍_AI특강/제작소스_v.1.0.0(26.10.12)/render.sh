cd "$(dirname "$0")"
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
r(){ (cd $1 && rm -f out.mp4 && timeout 400 npx hyperframes render --crf 24 -o out.mp4 >/dev/null 2>&1); }
lane(){ for d in $(awk "NR%3==$1" rl.txt); do r $d; [ -s $d/out.mp4 ] || r $d; echo "$d $(stat -c %s $d/out.mp4 2>/dev/null || echo FAIL)"; done; }
lane 0 & sleep 5; lane 1 & sleep 5; lane 2 & wait; echo ALLDONE
