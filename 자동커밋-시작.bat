@echo off
chcp 65001 >nul
echo 이력서 프로젝트 자동 커밋을 시작합니다.
echo 이 창을 닫으면 감시가 중단됩니다.
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0watch-and-commit.ps1"
pause
