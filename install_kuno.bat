@echo off
title Kuno Studio Installer
echo ===================================================
echo          Kuno Studio One-Click Installer
echo ===================================================

echo.
echo [1/3] Checking for Git...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH.
    echo Please install Git for Windows: https://git-scm.com/download/win
    echo After installing, run this script again.
    pause
    exit /b
)

echo.
echo [2/3] Downloading/Updating Kuno Studio...
if exist "Kuno-Studio" (
    echo Kuno-Studio folder found. Updating...
    cd Kuno-Studio
    git pull
) else (
    echo Cloning repository...
    git clone https://github.com/aaravsaianugula/Kuno-Studio.git
    cd Kuno-Studio
)

echo.
echo [3/3] Launching Setup...
if exist "setup_kuno.bat" (
    call setup_kuno.bat
) else (
    echo Error: Setup script not found in repository.
    pause
    exit /b
)
