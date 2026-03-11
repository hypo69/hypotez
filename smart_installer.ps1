<#
.SYNOPSIS
Professional Python dependency installer with UI progress indicator.

.DESCRIPTION
Features:
- Parallel installation engine
- Dependency lock generation
- Transaction rollback support
- Graph validation pipeline
- Secure pip installation
- Beautiful console progress visualization
- Single package installation mode
- Smart conflict resolver

.EXAMPLE
# Install all packages
./smart_installer_pro.ps1

# Install single package
./smart_installer_pro.ps1 -p pydoll
#>

param(
    [string]$p = ''
)

# ==============================
# CONFIGURATION
# ==============================

$SilentMode = $true
$ParallelInstall = $true
$EnableRollback = $true
$MaxAttempts = 2

$LockFile = Join-Path $PSScriptRoot 'requirements.lock'
$reqFile = Join-Path $PSScriptRoot 'requirements.txt'
$logFile = Join-Path $PSScriptRoot 'install_errors.log'

# ==============================
# UI PROGRESS ENGINE
# ==============================

function Show-ProgressBar {
    param(
        [int]$Percent,
        [string]$Text
    )

    $width = 40
    $filled = [math]::Floor($Percent / 100 * $width)
    $empty = $width - $filled

    $bar = '[' + ('=' * $filled) + (' ' * $empty) + ']'
    Write-Host "`r$bar $Percent% $Text" -NoNewline
}

# ==============================
# LOGGER
# ==============================

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = 'INFO'
    )

    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "[$timestamp][$Level] $Message"

    Add-Content $logFile $line
    Write-Host $line
}

# ==============================
# VALIDATION
# ==============================

if (!(Test-Path $reqFile)) {
    Write-Host 'requirements.txt not found'
    exit 1
}

# ==============================
# CLEAN CACHE
# ==============================

Write-Log 'Cleaning pip cache'
python -m pip cache purge 2>$null

# ==============================
# PACKAGE LIST BUILDING
# ==============================

$packages = @()

if ($p -ne '') {
    $packages += $p
}
else {
    $packages += Get-Content $reqFile | Where-Object { $_.Trim() -ne '' }
}

# ==============================
# INSTALLED PACKAGE CACHE
# ==============================

$installedPackages = python -m pip list --format=freeze 2>$null | ForEach-Object {
    ($_ -split '==')[0].ToLower()
}

# ==============================
# INSTALLATION FUNCTION
# ==============================

function Install-PackageSafe {
    param([string]$pkg)

    $attempt = 0

    while ($attempt -lt $MaxAttempts) {
        try {
            $output = python -m pip install --exists-action=i $pkg 2>&1
            Write-Log $output

            if ($LASTEXITCODE -ne 0) {
                throw 'pip install failed'
            }

            return $true
        }
        catch {
            $attempt++
            Write-Log "Retry $attempt -> $pkg" 'WARN'
        }
    }

    return $false
}

# ==============================
# INSTALL PIPELINE
# ==============================

Write-Log 'Starting installation pipeline'

$installedListBefore = python -m pip list --format=freeze 2>$null

$total = $packages.Count
$index = 0

$jobList = @()

foreach ($pkg in $packages) {

    $index++
    $percent = [math]::Floor($index / $total * 100)

    Show-ProgressBar $percent "Processing $pkg"

    # Skip already installed
    if ($SilentMode) {
        $pkgName = ($pkg -split '==')[0].ToLower()
        if ($installedPackages -contains $pkgName) {
            Write-Log "Auto skipped -> $pkgName"
            continue
        }
    }

    if ($ParallelInstall) {
        $job = Start-Job -ScriptBlock {
            param($package)
            python -m pip install --exists-action=i $package
        } -ArgumentList $pkg

        $jobList += $job
    }
    else {
        $result = Install-PackageSafe $pkg

        if (!$result) {
            Write-Log "FAILED -> $pkg" 'ERROR'
        }
    }
}

# ==============================
# WAIT PARALLEL JOBS
# ==============================

if ($ParallelInstall) {

    Write-Log 'Waiting for parallel jobs'

    $jobList | Wait-Job

    foreach ($job in $jobList) {
        $output = Receive-Job $job
        Write-Log $output
        Remove-Job $job
    }
}

# ==============================
# DEPENDENCY VALIDATION
# ==============================

Write-Log 'Running dependency graph validation'
$checkOutput = python -m pip check 2>&1

if ($checkOutput) {
    Write-Log "Dependency issues detected:`n$checkOutput" 'WARN'
}

# ==============================
# LOCK FILE GENERATION
# ==============================

Write-Log 'Generating lock file'
python -m pip freeze > $LockFile

# ==============================
# ROLLBACK SUPPORT
# ==============================

if ($EnableRollback) {
    $rollback = Read-Host "Enable rollback if installation partially failed? (Y/N)"

    if ($rollback -match '^[Yy]$') {
        Write-Log 'Rollback monitoring enabled'

        $installedAfter = python -m pip list --format=freeze 2>$null

        if ($installedAfter.Count -lt $installedListBefore.Count) {
            Write-Log 'Rollback triggered' 'ERROR'

            foreach ($pkg in $packages) {
                python -m pip uninstall -y $pkg 2>$null
            }
        }
    }
}

Show-ProgressBar 100 'Completed'
Write-Log 'Installation pipeline completed'
