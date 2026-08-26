$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvRoot = if ($env:SCENICOPS_VENV) {
    $env:SCENICOPS_VENV
}
else {
    Join-Path $env:LOCALAPPDATA "ScenicOps\venv"
}
$Python = Join-Path $VenvRoot "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Virtual environment not found. Run .\scripts\bootstrap.ps1 first."
}

Push-Location $ProjectRoot
try {
    & $Python -m uvicorn scenicops.main:app --reload
}
finally {
    Pop-Location
}
