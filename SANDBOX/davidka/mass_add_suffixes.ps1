<#
.SYNOPSIS
Adds the .json suffix to files in a specified directory.

.DESCRIPTION
This script iterates through all files in a given directory and renames them by appending the .json suffix.
By default, it skips files that already have the .json extension. Use the -Force switch to override this behavior.
Supports -WhatIf and -Confirm common parameters for safety.

.PARAMETER DirectoryPath
The path to the directory containing the files to rename. This parameter is mandatory.

.PARAMETER Force
If specified, the script will add the .json suffix even to files that already have a .json extension (e.g., file.json -> file.json.json).
By default, files ending in .json are skipped.

.EXAMPLE
.\mass_add_json_suffix.ps1 -DirectoryPath "C:\MyData\NeedsJson"
Description: Adds .json suffix to all files in C:\MyData\NeedsJson, skipping any existing .json files.

.EXAMPLE
.\mass_add_json_suffix.ps1 -DirectoryPath "C:\MyData\NeedsJson" -Force
Description: Adds .json suffix to ALL files in C:\MyData\NeedsJson, including those that might already end in .json.

.EXAMPLE
.\mass_add_json_suffix.ps1 -DirectoryPath "C:\MyData\NeedsJson" -WhatIf
Description: Shows what files WOULD be renamed, without actually renaming them.

.NOTES
Author: Your Name / AI Assistant
Date:   2023-10-27
#>
[CmdletBinding(SupportsShouldProcess = $true)] # Enables -WhatIf and -Confirm
param(
    [Parameter(Mandatory = $true, Position = 0, HelpMessage = "Specify the path to the directory containing the files.")]
    [ValidateScript({
            if (-not (Test-Path $_ -PathType Container)) {
                throw "The specified path '$_' does not exist or is not a directory."
            }
            return $true
        })]
    [string]$DirectoryPath,

    [Parameter(HelpMessage = "Add .json suffix even if the file already has it.")]
    [switch]$Force
)

# Resolve the path to ensure it's absolute (optional, but good practice)
$resolvedPath = Resolve-Path -Path $DirectoryPath

Write-Verbose "Target directory: $resolvedPath"

# Get all files in the directory
try {
    $files = Get-ChildItem -Path $resolvedPath -File -ErrorAction Stop
}
catch {
    Write-Error "Failed to get files from directory '$resolvedPath'. Error: $($_.Exception.Message)"
    # Exit script if we can't get files
    exit 1
}


if ($null -eq $files -or $files.Count -eq 0) {
    Write-Host "No files found in directory '$resolvedPath'."
    exit 0
}

Write-Host "Found $($files.Count) file(s) in '$resolvedPath'."

# Process each file
$filesToProcess = $files

# Filter out files already ending in .json unless -Force is used
if (-not $Force.IsPresent) {
    $filesToProcess = $files | Where-Object { $_.Extension -ne ".json" }
    $skippedCount = $files.Count - $filesToProcess.Count
    if ($skippedCount -gt 0) {
        Write-Verbose "Skipping $skippedCount file(s) that already have the .json extension. Use -Force to include them."
    }
}
else {
    Write-Verbose "-Force switch specified. Processing all files, including existing .json files."
}

if ($null -eq $filesToProcess -or $filesToProcess.Count -eq 0) {
    Write-Host "No files require renaming in '$resolvedPath' based on the current criteria."
    exit 0
}

Write-Host "Attempting to rename $($filesToProcess.Count) file(s)..."

$renameCount = 0
$errorCount = 0

foreach ($file in $filesToProcess) {
    $currentName = $file.Name
    $newName = $currentName + ".json"
    $currentFullName = $file.FullName

    Write-Verbose "Processing file: '$currentFullName'"

    # Use ShouldProcess for -WhatIf/-Confirm support
    if ($PSCmdlet.ShouldProcess($currentFullName, "Rename to '$newName'")) {
        try {
            Rename-Item -Path $currentFullName -NewName $newName -ErrorAction Stop
            Write-Host "Renamed '$currentName' -> '$newName'"
            $renameCount++
        }
        catch {
            Write-Error "Failed to rename '$currentFullName' to '$newName'. Error: $($_.Exception.Message)"
            $errorCount++
        }
    }
}

Write-Host "----------------------------------------"
Write-Host "Script finished."
Write-Host "Successfully renamed: $renameCount file(s)."
if ($errorCount -gt 0) {
    Write-Warning "Failed to rename: $errorCount file(s)."
}
Write-Host "----------------------------------------"