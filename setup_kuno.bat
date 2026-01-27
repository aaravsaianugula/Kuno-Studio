@echo off
title Kuno Studio Setup
echo ===================================================
echo          Setting up Kuno Studio Environment
echo ===================================================

echo.
echo [1/4] Checking Prerequisites...
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
echo [2/4] Installing Backend Dependencies...
cd backend
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
)
call env\Scripts\activate
echo Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing backend requirements.
    pause
    exit /b
)
call deactivate
cd ..

echo.
echo [3/4] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Error installing frontend packages.
    pause
    exit /b
)
cd ..

echo.
echo [4/4] Creating Desktop Shortcut...
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
