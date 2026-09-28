# ==============================================================================
# ComicCraft — GitHub Upload Preparation & Packaging Script
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "     Preparing ComicCraft for Clean GitHub Upload       " -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

# 1. Clean temporary python and pytest cache files
Write-Host "[1/4] Cleaning cache files (__pycache__, .pytest_cache)..." -ForegroundColor White
Get-ChildItem -Path $root -Include "__pycache__", ".pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 2. Clean generated test panels and exports while preserving .gitkeep
Write-Host "[2/4] Cleaning generated media files in backend/storage..." -ForegroundColor White
if (Test-Path "$root\backend\storage\panels") {
    Get-ChildItem -Path "$root\backend\storage\panels" -Exclude ".gitkeep" | Remove-Item -Force -ErrorAction SilentlyContinue
}
if (Test-Path "$root\backend\storage\exports") {
    Get-ChildItem -Path "$root\backend\storage\exports" -Exclude ".gitkeep" | Remove-Item -Force -ErrorAction SilentlyContinue
}

# 3. Create a clean ZIP package for manual GitHub Web upload
$zipFile = "$root\comic-craft-github.zip"
if (Test-Path $zipFile) {
    Remove-Item -Force $zipFile
}

Write-Host "[3/4] Creating clean upload bundle: comic-craft-github.zip..." -ForegroundColor White

# Temporary staging directory for zip
$tempStage = "$root\.github_upload_staging"
if (Test-Path $tempStage) {
    Remove-Item -Recurse -Force $tempStage
}
New-Item -ItemType Directory -Path $tempStage | Out-Null

$itemsToCopy = @(
    "backend",
    "frontend",
    ".github",
    ".dockerignore",
    ".env.example",
    ".gitignore",
    "docker-compose.yml",
    "Dockerfile",
    "LICENSE",
    "pytest.ini",
    "README.md",
    "requirements.txt",
    "run_local.ps1",
    "run_local.sh",
    "comic craft prompt.md"
)

foreach ($item in $itemsToCopy) {
    $sourcePath = "$root\$item"
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination "$tempStage\$item" -Recurse -Force
    }
}

# Strictly ensure NO secret .env files are in the upload bundle
Get-ChildItem -Path $tempStage -Filter ".env" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $tempStage -Filter "*.env" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Force

# Compress staging directory
Compress-Archive -Path "$tempStage\*" -DestinationPath $zipFile -Force
Remove-Item -Recurse -Force $tempStage

Write-Host "[4/4] Done! Bundle created successfully at:" -ForegroundColor Green
Write-Host "      $zipFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "             HOW TO UPLOAD TO GITHUB                    " -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "METHOD A: Upload via GitHub Website (Drag and Drop)" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/new and create a new repository."
Write-Host "2. Click 'uploading an existing file'."
Write-Host "3. Extract or drag all folders ('backend', 'frontend', '.github', etc.)"
Write-Host "   and files from this project (or from comic-craft-github.zip) into GitHub."
Write-Host "4. Commit changes!"
Write-Host ""
Write-Host "METHOD B: Upload via Git CLI" -ForegroundColor Yellow
Write-Host "If you have Git installed, run:"
Write-Host "  git init" -ForegroundColor White
Write-Host "  git add ." -ForegroundColor White
Write-Host '  git commit -m "Initial commit: ComicCraft v2.0"' -ForegroundColor White
Write-Host "  git branch -M main" -ForegroundColor White
Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
Write-Host "  git push -u origin main" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
