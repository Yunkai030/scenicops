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
    & $Python -m ruff check .
    if ($LASTEXITCODE -ne 0) { throw "Ruff lint failed with exit code $LASTEXITCODE." }

    & $Python -m ruff format --check .
    if ($LASTEXITCODE -ne 0) { throw "Ruff format check failed with exit code $LASTEXITCODE." }

    & $Python -m mypy src
    if ($LASTEXITCODE -ne 0) { throw "Mypy failed with exit code $LASTEXITCODE." }

    & $Python -m pytest
    if ($LASTEXITCODE -ne 0) { throw "Pytest failed with exit code $LASTEXITCODE." }
}
finally {
    Pop-Location
}
