@echo off
title Kuno Studio Launcher
echo ===================================================
echo           Starting Kuno Studio AI...
echo ===================================================

echo.
echo [1/3] Starting Backend Server...
start "Kuno Backend" /min cmd /k "cd backend && python -m app.main"

echo.
echo [2/3] Starting Frontend Interface...
start "Kuno Frontend" /min cmd /k "cd frontend && npm run dev"

echo.
echo [3/3] Waiting for services to initialize...
timeout /t 5 /nobreak >nul

echo.
echo Opening Studio in your browser...
start http://localhost:3000

echo.
echo ===================================================
echo        Kuno Studio is running!
echo    Close this window to keep servers running,
echo    or manually close the other windows to stop.
echo ===================================================
pause
