$ErrorActionPreference = "Stop"

$Python = Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvRoot = if ($env:SCENICOPS_VENV) {
    $env:SCENICOPS_VENV
}
else {
    Join-Path $env:LOCALAPPDATA "ScenicOps\venv"
}
$VenvPython = Join-Path $VenvRoot "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python 3.13 not found at $Python. Install Python.Python.3.13 first."
}

if (-not (Test-Path -LiteralPath $VenvPython)) {
    & $Python -m venv $VenvRoot
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
}

& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Pip upgrade failed with exit code $LASTEXITCODE." }

& $VenvPython -m pip install -e "$ProjectRoot[dev]"
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed with exit code $LASTEXITCODE." }

Write-Host "ScenicOps development environment is ready."
Write-Host "Run .\scripts\check.ps1 before committing changes."
