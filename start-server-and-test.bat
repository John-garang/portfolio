@echo off
echo ========================================
echo Server Status Check and Startup
echo ========================================
echo.

echo Checking if server is running on port 3000...
netstat -ano | findstr :3000 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo Server is already running!
) else (
    echo Server is NOT running. Starting server...
    echo.
    start "Portfolio Server" cmd /k "node server.js"
    echo Waiting 3 seconds for server to start...
    timeout /t 3 /nobreak >nul
)

echo.
echo ========================================
echo Opening test page in browser...
echo ========================================
start test-poems-fix.html

echo.
echo Done! Check the browser window to test the API.
pause
