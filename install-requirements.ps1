# Сброс лога
"log start: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File install.log

# Установка зависимостей
Get-Content requirements.txt | ForEach-Object {
    $package = $_.Trim()
    if (-not $package) { return }  # пропустить пустые строки

    Write-Host "Installing $package ..." -ForegroundColor Cyan
    pip install $package 2>&1 | Tee-Object -Variable output | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Success: $package" -ForegroundColor Green
        "OK     $package" | Out-File install.log -Append
    }
    else {
        Write-Host "✗ Failed: $package" -ForegroundColor Red
        "FAIL   $package`n$output`n" | Out-File install.log -Append
    }
}

Write-Host "`nDone. See install.log for details." -ForegroundColor Yellow
