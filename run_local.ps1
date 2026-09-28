# Localhost startup script for ComicCraft (PowerShell / Windows)
$ErrorActionPreference = "Stop"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Starting ComicCraft AI Studio on Localhost  " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# Set PYTHONPATH to include backend
$env:PYTHONPATH = "$PSScriptRoot\backend"
$env:HOST = "127.0.0.1"
$env:PORT = "8000"
$env:ENVIRONMENT = "development"

if (Test-Path "$PSScriptRoot\.venv\Scripts\python.exe") {
    $pythonCmd = "$PSScriptRoot\.venv\Scripts\python.exe"
} else {
    $pythonCmd = "python"
}

Write-Host "Running backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
& $pythonCmd -m uvicorn app.main:app --app-dir "$PSScriptRoot\backend" --host 127.0.0.1 --port 8000 --reload
