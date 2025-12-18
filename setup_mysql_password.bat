@echo off
echo ============================================
echo MySQL Password Setup
echo ============================================
echo.
echo You need to set a MySQL root password.
echo.
echo Option 1: Use MySQL Command Line Client
echo 1. Open "MySQL 8.0 Command Line Client" from Start Menu
echo 2. Enter the password you set during installation
echo 3. Run: ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
echo.
echo Option 2: Set password to 'admin123' (recommended for development)
echo.
set /p choice="Do you want to set password to 'admin123'? (Y/N): "
if /i "%choice%"=="Y" (
    echo.
    echo Opening MySQL Command Line Client...
    echo Please enter your CURRENT MySQL root password when prompted.
    echo Then run this command:
    echo ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin123';
    echo.
    start "" "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
) else (
    echo.
    echo Please remember your MySQL password and update these files:
    echo 1. migrate_to_mysql.py - line 8
    echo 2. app_mysql.py - line 13
    echo.
)
pause
