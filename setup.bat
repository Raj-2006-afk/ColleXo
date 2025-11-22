@echo off
echo ========================================
echo ColleXo - Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
cd backend
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start XAMPP and ensure MySQL is running
echo 2. Run: python backend\app.py
echo 3. Open: http://localhost:5000
echo.
echo Default Login:
echo   Admin: admin@collexo.com / admin123
echo   Student: student@collexo.com / student123
echo   Society Head: john@collexo.com / head123
echo.
pause
