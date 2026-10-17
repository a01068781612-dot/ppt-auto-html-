@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 조각 확인 중...
set OK=1
if not exist part_00 (echo [없음] part_00 & set OK=0)
for %%A in (part_00) do if not "%%~zA"=="30408704" (echo [크기 다름] part_00 : %%~zA / 30408704 & set OK=0)
if not exist part_01 (echo [없음] part_01 & set OK=0)
for %%A in (part_01) do if not "%%~zA"=="30408704" (echo [크기 다름] part_01 : %%~zA / 30408704 & set OK=0)
if not exist part_02 (echo [없음] part_02 & set OK=0)
for %%A in (part_02) do if not "%%~zA"=="30408704" (echo [크기 다름] part_02 : %%~zA / 30408704 & set OK=0)
if not exist part_03 (echo [없음] part_03 & set OK=0)
for %%A in (part_03) do if not "%%~zA"=="30408704" (echo [크기 다름] part_03 : %%~zA / 30408704 & set OK=0)
if not exist part_04 (echo [없음] part_04 & set OK=0)
for %%A in (part_04) do if not "%%~zA"=="30408704" (echo [크기 다름] part_04 : %%~zA / 30408704 & set OK=0)
if not exist part_05 (echo [없음] part_05 & set OK=0)
for %%A in (part_05) do if not "%%~zA"=="30408704" (echo [크기 다름] part_05 : %%~zA / 30408704 & set OK=0)
if not exist part_06 (echo [없음] part_06 & set OK=0)
for %%A in (part_06) do if not "%%~zA"=="10645375" (echo [크기 다름] part_06 : %%~zA / 10645375 & set OK=0)
if "%OK%"=="0" (echo 조각이 빠졌거나 덜 받아졌습니다. 다시 받아 주세요. & pause & exit /b 1)
copy /b part_00+part_01+part_02+part_03+part_04+part_05+part_06 "직장훈련특강_모션슬라이드_v.1.0.0(26.10.15).pptx" >nul
for %%A in ("직장훈련특강_모션슬라이드_v.1.0.0(26.10.15).pptx") do if "%%~zA"=="193097599" (echo 완료: 직장훈련특강_모션슬라이드_v.1.0.0(26.10.15).pptx) else (echo [오류] 합친 파일 크기가 다릅니다: %%~zA / 193097599)
pause
