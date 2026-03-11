<#
.SYNOPSIS
Enterprise-grade Python dependency installer.

.DESCRIPTION
Interactive CLI dependency manager with safe retry logic.
Supports:
- Interactive argument wizard
- Optional multithreading
- Force latest mode
- Smart retry WITHOUT pinned version
- Rollback
- Lock file generation
#>

param(
    [Alias('p')]
    [string]$Package = '',

    [switch]$Parallel,
    [switch]$ForceLatest,
    [switch]$Rollback,
    [switch]$NoCacheClean,
    [switch]$VerboseMode
)

# ==============================
# INTERACTIVE ARGUMENT WIZARD
# ==============================

if ($PSBoundParameters.Count -eq 0) {

    Write-Host '=== Smart Installer Interactive Mode ==='

    $PackageInput = Read-Host 'Install single package (leave empty for requirements.txt)'
    if ($PackageInput -ne '') {
        $Package = $PackageInput
    }

    $ParallelInput = Read-Host 'Enable parallel mode? (Y/N)'
    if ($ParallelInput -match '^[Yy]$') {
        $Parallel = $true
    }

    $LatestInput = Read-Host 'Force latest versions? (Y/N)'
    if ($LatestInput -match '^[Yy]$') {
        $ForceLatest = $true
    }

    $RollbackInput = Read-Host 'Enable rollback on failure? (Y/N)'
    if ($RollbackInput -match '^[Yy]$') {
        $Rollback = $true
    }

    $VerboseInput = Read-Host 'Enable verbose logging? (Y/N)'
    if ($VerboseInput -match '^[Yy]$') {
        $VerboseMode = $true
    }
}

# ==============================
# CONFIGURATION
# ==============================

$ParallelInstall = $Parallel.IsPresent
$EnableRollback = $Rollback.IsPresent
$MaxAttempts = 2

$LockFile = Join-Path $PSScriptRoot 'requirements.lock'
$reqFile = Join-Path $PSScriptRoot 'requirements.txt'
$logFile = Join-Path $PSScriptRoot 'install_errors.log'

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

    if ($VerboseMode -or $Level -ne 'INFO') {
        Write-Host $line
    }
}

# ==============================
# PROGRESS BAR
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
# LATEST VERSION RESOLVER
# ==============================

function Get-LatestVersion {
    param([string]$PackageName)

    $output = python -m pip index versions $PackageName 2>$null

    if ($output -match 'Available versions: (.+)') {
        $versionsLine = $Matches[1]
        $latest = ($versionsLine -split ',')[0].Trim()
        return $latest
    }

    return ''
}

# ==============================
# PRECHECK
# ==============================

if ($Package -eq '' -and !(Test-Path $reqFile)) {
    Write-Host 'requirements.txt not found'
    exit 1
}

if (!$NoCacheClean) {
    Write-Log 'Cleaning pip cache'
    python -m pip cache purge 2>$null
}

# ==============================
# PACKAGE LIST
# ==============================

$packages = @()

if ($Package -ne '') {
    $packages += $Package
}
else {
    $packages += Get-Content $reqFile | Where-Object { $_.Trim() -ne '' }
}

# ==============================
# INSTALL FUNCTION
# ==============================

function Install-PackageSafe {
    param([string]$Entry)

    $attempt = 0
    $pkgName = ($Entry -split '==')[0]

    while ($attempt -lt $MaxAttempts) {
        try {
            $output = python -m pip install --exists-action=i $Entry 2>&1
            Write-Log $output

            if ($LASTEXITCODE -ne 0) {
                throw 'pip install failed'
            }

            return $true
        }
        catch {
            $attempt++
            Write-Log "Retry $attempt -> $pkgName" 'WARN'

            # Retry WITHOUT pinned version
            $Entry = $pkgName
        }
    }

    return $false
}

# ==============================
# INSTALLATION PIPELINE
# ==============================

Write-Log 'Starting installation pipeline'

$total = $packages.Count
$index = 0

foreach ($entry in $packages) {

    $index++
    $percent = [math]::Floor($index / $total * 100)

    $pkgName = ($entry -split '==')[0].Trim()

    if ($ForceLatest) {
        $latest = Get-LatestVersion $pkgName
        if ($latest -ne '') {
            Write-Log "Force latest version -> $pkgName==$latest"
            $entry = "$pkgName==$latest"
        }
    }

    Show-ProgressBar $percent "Processing $pkgName"

    if ($ParallelInstall) {
        Start-Job -ScriptBlock {
            param($package)
            python -m pip install --exists-action=i $package
        } -ArgumentList $entry | Out-Null
    }
    else {
        $result = Install-PackageSafe $entry
        if (!$result) {
            Write-Log "FAILED -> $pkgName" 'ERROR'
        }
    }
}

Write-Log 'Running dependency validation'
$checkOutput = python -m pip check 2>&1

if ($checkOutput) {
    Write-Log "Dependency issues detected:`n$checkOutput" 'WARN'

    if ($EnableRollback) {
        Write-Log 'Rollback initiated' 'ERROR'
        foreach ($entry in $packages) {
            $pkgName = ($entry -split '==')[0]
            python -m pip uninstall -y $pkgName 2>$null
        }
    }
}

Write-Log 'Generating lock file'
python -m pip freeze > $LockFile

Show-ProgressBar 100 'Completed'
Write-Log 'Installation pipeline completed'
