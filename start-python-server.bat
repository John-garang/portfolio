@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server on port 3000...
python app.py

pause
