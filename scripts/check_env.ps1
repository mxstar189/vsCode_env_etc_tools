<#
Check .env vs current environment for Windows PowerShell

Usage: ./scripts/check_env.ps1
#>

# Find repo root by moving up from script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

$envFile = Join-Path $repoRoot ".env"
if (-not (Test-Path $envFile)) {
    Write-Output ".env file not found at $envFile"
    exit 1
}

$lines = Get-Content $envFile | ForEach-Object { $_.Trim() } | Where-Object { $_ -and (-not $_.StartsWith('#')) }

Write-Output "Comparing .env -> process environment (mismatches):"
foreach ($line in $lines) {
    if ($line -notmatch "=") { continue }
    $parts = $line -split "=",2
    $k = $parts[0].Trim()
    $v = $parts[1].Trim().Trim('"')
    $proc = [Environment]::GetEnvironmentVariable($k)
    if ($proc -ne $v) {
        Write-Output "$k : file='$v' process='${proc}'"
    }
}

# show .vscode settings if present
$vscode = Join-Path $repoRoot ".vscode\settings.json"
if (Test-Path $vscode) {
    Write-Output "Found .vscode/settings.json:" 
    Get-Content $vscode | Out-String
} else {
    Write-Output "No .vscode/settings.json found"
}
