@echo off
title Kuno Studio Native Launcher
echo ===================================================
echo           Starting Kuno Studio (Native)...
echo ===================================================

cd frontend
call npm run electron-dev

pause
