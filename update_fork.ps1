function Update-Fork {
    param(
        [string]$GitDirectory = (Get-Location)  # Параметр с дефолтным значением текущей директории
    )

    Write-Host "🔄 Начинаем обновление форка в директории: $GitDirectory" -ForegroundColor Cyan

    # Переходим в указанную директорию (если она отличается от текущей)
    Set-Location -Path $GitDirectory

    $currentBranch = git rev-parse --abbrev-ref HEAD


    Write-Host "📥 Забираем изменения из upstream..." -ForegroundColor Cyan
    git fetch upstream

    Write-Host "🛠  Делаем rebase с upstream/master..." -ForegroundColor Cyan
    git rebase upstream/master

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❗ При ребейсе возникли конфликты. Разреши их и выполни: git rebase --continue" -ForegroundColor Red
        return
    }

    Write-Host "🚀 Пушим изменения в свой форк (с --force)..." -ForegroundColor Cyan
    git push origin master --force

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Форк успешно обновлён!" -ForegroundColor Green
        New-BurntToastNotification -Text "✅ Форк обновлён!", "Можешь продолжать работу!"
    } else {
        Write-Host "❌ Не удалось запушить. Проверь ошибки." -ForegroundColor Red
        New-BurntToastNotification -Text "❌ Ошибка при пуше!", "П

роверь конфликты вручную."
    }
}

Update-Fork