@echo off
echo.
echo ============================================================
echo   Safe Flask Server Startup
echo ============================================================
echo.
echo Checking database backup...
if exist database.json.backup (
    echo [OK] Master backup exists: database.json.backup
) else (
    echo [WARNING] Master backup not found!
    echo Creating master backup now...
    copy database.json database.json.backup
)
echo.
echo Starting Flask server with auto-backup protection...
echo - Every change creates automatic backup
echo - Backups saved to: database_backups\
echo - Press Ctrl+C to stop server
echo.
echo ============================================================
echo.
python app.py
