@echo off
echo Killing all Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Starting Flask server...
start cmd /k "cd /d "%~dp0" && python app.py"

echo Server restart initiated!
timeout /t 3 /nobreak >nul
