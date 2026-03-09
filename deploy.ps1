# HJ_resume GitHub 배포 스크립트
# 사용법: 저장소를 생성한 후 이 스크립트를 실행하세요

$ErrorActionPreference = "Stop"
$repoPath = "c:\Users\USER\Downloads\개인 페이지 & 공유된 페이지"

Write-Host "=== HJ_resume GitHub 배포 ===" -ForegroundColor Cyan
Write-Host ""

# 1. 푸시
Write-Host "GitHub에 푸시 중..." -ForegroundColor Yellow
Push-Location $repoPath
try {
    git push -u origin main
    Write-Host "푸시 완료!" -ForegroundColor Green
} catch {
    Write-Host "푸시 실패. 저장소가 생성되었는지 확인하세요." -ForegroundColor Red
    Write-Host "https://github.com/new?name=HJ_resume 에서 저장소를 생성한 후 다시 시도하세요." -ForegroundColor Yellow
    exit 1
} finally {
    Pop-Location
}

# 2. GitHub Pages 설정 페이지 열기
Write-Host ""
Write-Host "GitHub Pages 설정 페이지를 엽니다..." -ForegroundColor Yellow
Start-Process "https://github.com/leehj67/HJ_resume/settings/pages"

Write-Host ""
Write-Host "=== 다음 단계 ===" -ForegroundColor Cyan
Write-Host "1. 열린 페이지에서 Source를 'GitHub Actions'로 선택"
Write-Host "2. 저장 후 1-2분 대기"
Write-Host "3. https://leehj67.github.io/HJ_resume/ 에서 확인"
Write-Host ""
