Get-ChildItem -Recurse -File |
Where-Object { -not $_.Name.Contains('.') } |
ForEach-Object {
    $newName = "$($_.FullName).json"
    Rename-Item -Path $_.FullName -NewName $newName
}