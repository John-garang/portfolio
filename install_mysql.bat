@echo off
echo ============================================
echo MySQL Installation Guide
echo ============================================
echo.
echo Step 1: Download MySQL
echo Opening MySQL download page...
start https://dev.mysql.com/downloads/installer/
echo.
echo Step 2: Installation Instructions
echo 1. Download "mysql-installer-community" (Windows MSI Installer)
echo 2. Run the installer
echo 3. Choose "Developer Default" setup type
echo 4. Click "Execute" to install all components
echo 5. Set a ROOT PASSWORD (remember this!)
echo 6. Complete the installation
echo.
echo Step 3: After Installation
echo Press any key after MySQL is installed...
pause > nul
echo.
echo Installing Python MySQL connector...
pip install mysql-connector-python
echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit migrate_to_mysql.py and set your MySQL password
echo 2. Run: python migrate_to_mysql.py
echo.
pause
