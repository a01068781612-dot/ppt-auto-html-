# AI 특강 슬라이드 제작 소스 (v.1.5.0 · 26.10.05)

`AI특강_슬라이드_v.1.5.0(26.10.05).pptx`(53장)을 만든 스크립트 모음입니다.
영상·사진·기사 캡처·글꼴(Pretendard woff2)·GSAP 같은 **미디어/외부 파일은 저작권 문제로 저장소에 넣지 않았습니다.**
스크립트 안의 경로(`/tmp/claude-0/.../scratchpad/...`, `/tmp/vids/...`)는 작업 컨테이너 기준입니다.

## 변경 이력
| 버전 | 날짜 | 수정 내용 |
|---|---|---|
| v.1.7.0 | 26.10.06 | 슬라이드 v.1.7.0 생성기 반영: keep-all, 정리 카드 효과 10종·KEY 4종, 기사 소개 6종(`ASSIGN`), PART 3 장별 효과(`EXTRA`), PART 인트로·act 모션, 카운트업 innerText 방식 |
| v.1.6.2 | 26.10.05 | 발표 대본 도구 추가: `script/extract_text.py`(화면 글자 뽑기) · `fill_times.py`(⏱ 시작 시각·처음/중간/끝) · `md2pdf.py`(A4 가로 PDF) · `durations_예시_AI특강.json`. 기준 문서 `발표대본_작성가이드_v.1.0.0` |
| v.1.6.1 | 26.10.05 | 재사용용 파일 추가: `motion/base/`(HyperFrames 설정), `assets/bg.png`·`fade.png`(배경), build.js `ONLY=` 옵션(일부 장만 담은 교체용 PPT). 디자인 기준은 `PPT디자인시스템_v.1.0.0` |
| v.1.6.0 | 26.10.05 | PART 3 기사 3·4·5(47~49장)를 기사 사진 + 사진 설명 레이아웃으로(`motion/article/gen.py`의 `photo`·`photo_cap`) |
| v.1.5.0 | 26.10.05 | 최초 저장 — 슬라이드 v.1.5.0 기준 스크립트 일체 |

## 폴더
| 폴더 | 내용 |
|---|---|
| `pptx/build.js` | pptxgenjs로 53장 PPT 생성(1920×1080 기준 px → in 변환). 영상·모션은 전부 슬라이드 전체 크기 영상 |
| `pptx/timing.py` | 영상 슬라이드에 **들어오면 자동 재생** 설정(`p:timing`) 추가. 클릭+전체화면 방식은 PowerPoint '복구' 문제로 폐기 |
| `video/` | 유튜브 원본에서 구간 자르기(ffmpeg) 스크립트와 잘린 길이(`dur.json`) |
| `motion/news/` | 📰 PART 2 기사 소개 모션 10장 생성기. `topics.json` = 기사 제목·출처·주소·요점·강조 박스 좌표 |
| `motion/article/` | PART 3 기사 모션 5장 생성기 + '일단 써 보세요' 장면 |
| `motion/static/` | 영상 소개·강사 소개·PART 1 END·타임라인·정리 10장·비교표·마무리·Q&A 모션 생성기 |
| `motion/opening/` | 표지·목차·PART 인트로 3장·신문물 지도 모션(HTML) |
| `motion/sqfix.py` | **사각 장식 규칙**: 제목 첫 글자의 대각선 왼쪽 위, 글자 쪽 모서리(오른쪽 아래)를 끊은 모양. 크기 = 글자 크기 × 0.45 (40~90px). 표지는 A 꼭짓점 쪽으로 보정(`data-dx/dy`) |
| `motion/render3.sh` | HyperFrames 렌더(3개 동시, `--crf 24`) |
| `script/` | **발표 대본** 도구 — 화면 글자 뽑기, ⏱ 채우기, PDF 만들기 (`발표대본_작성가이드` 4장) |
| `motion/allshot.js` | 렌더 전 마지막 장면 스크린샷 확인 |
| `motion/base/` | HyperFrames 프로젝트 설정(hyperframes.json·meta.json·package.json) — 모션 폴더마다 복사. gsap.min.js·PretendardVariable.woff2는 따로 받아 같이 둠 |
| `assets/` | `bg.png`(1920×1080 배경), `fade.png`(강사 사진 오른쪽 흐림) |

## 다시 만드는 순서
1. 모션 HTML 생성: `python3 motion/static/gen.py`, `cd motion/news && python3 gen.py`, `cd motion/article && python3 gen.py`
2. 사각 장식 적용: `python3 motion/sqfix.py <index.html> <제목 클래스>`
3. 렌더: `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell npx hyperframes render --crf 24 -o out.mp4` (GSAP은 CDN 대신 로컬 파일)
4. PPT: `NODE_PATH=<node_modules> node pptx/build.js raw.pptx && python3 pptx/timing.py raw.pptx "AI특강_슬라이드_v.X.Y.Z(YY.MM.DD).pptx"`
5. 전달: 29MB 조각으로 `split` + 크기 확인 기능이 있는 `0_합치기.bat` (반디집 없이 윈도우에서 합침)
