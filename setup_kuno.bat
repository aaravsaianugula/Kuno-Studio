@echo off
title Kuno Studio Setup
echo ===================================================
echo          Setting up Kuno Studio Environment
echo ===================================================

echo.
echo [1/5] Checking Prerequisites...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Node.js (npm) is not installed or not in PATH.
    pause
    exit /b
)


echo.
echo [2/5] Checking for Updates...
if exist ".git" (
    echo pulling latest changes from GitHub...
    git pull origin main
) else (
    echo Not a git repository. Skipping update check.
)

echo.
echo [3/5] Installing Backend Dependencies...
cd backend
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
)
call env\Scripts\activate
echo Installing/Updating Python packages...
pip install -r requirements.txt --upgrade
if %errorlevel% neq 0 (
    echo Error installing backend requirements.
    pause
    exit /b
)
call deactivate
cd ..

echo.
echo [4/5] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Error installing frontend packages.
    pause
    exit /b
)
cd ..

echo.
echo [5/5] Creating Desktop Shortcut...
set "TARGET=%~dp0start_kuno.bat"
set "ICON=%~dp0frontend\public\favicon.ico"
set "SHORTCUT=%USERPROFILE%\Desktop\Kuno Studio.lnk"
set "PWS=powershell.exe -ExecutionPolicy Bypass -NoProfile -NonInteractive -Command"

%PWS% "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%');$s.TargetPath='%TARGET%';$s.WorkingDirectory='%~dp0';$s.IconLocation='%ICON%';$s.Save()"

if exist "%SHORTCUT%" (
    echo Shortcut created successfully on Desktop!
) else (
    echo Failed to create shortcut. You can manually create a shortcut to 'start_kuno.bat'.
)

echo.
echo ===================================================
echo             Setup Complete! 
echo    Run 'Kuno Studio' from your Desktop to start.
echo ===================================================
pause
