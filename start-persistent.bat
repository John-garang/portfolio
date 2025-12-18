@echo off
echo Installing dependencies...
npm install

echo.
echo Migrating existing data...
node migrate-data.js

echo.
echo Starting persistent server...
node server-persistent.js

pause