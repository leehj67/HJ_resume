# 이력서 프로젝트 - 변경 감지 시 자동 커밋 스크립트
# 사용법: PowerShell에서 이 스크립트 실행 (백그라운드로 유지)
# 종료: Ctrl+C

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "이력서 프로젝트 자동 커밋 감시 시작: $projectRoot" -ForegroundColor Cyan
Write-Host "변경 시 5초 후 자동 커밋됩니다. 종료하려면 Ctrl+C" -ForegroundColor Gray
Write-Host ""

$lastCommit = ""
$debounceSeconds = 5
$lastChangeTime = $null

while ($true) {
    $status = git status --porcelain 2>$null
    if ($status) {
        $now = Get-Date
        if (-not $lastChangeTime) {
            $lastChangeTime = $now
        }
        $elapsed = ($now - $lastChangeTime).TotalSeconds
        if ($elapsed -ge $debounceSeconds) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 변경 감지 - 커밋 중..." -ForegroundColor Yellow
            git add -A 2>$null
            $msg = "자동 커밋: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
            $result = git commit -m $msg 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  커밋 완료: $msg" -ForegroundColor Green
                $pushResult = git push origin main 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "  푸시 완료" -ForegroundColor Green
                } else {
                    Write-Host "  푸시 실패: $pushResult" -ForegroundColor Red
                }
            }
            $lastChangeTime = $null
        }
    } else {
        $lastChangeTime = $null
    }
    Start-Sleep -Seconds 2
}
