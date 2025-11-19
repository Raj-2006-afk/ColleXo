@echo off
REM ColleXo - Quick Setup Script for Windows

echo ======================================
echo ColleXo - College Societies Platform
echo Setup Script for Windows
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version

if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo Error: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your database credentials.
)

REM Create uploads directory
echo.
echo Creating uploads directory...
if not exist uploads mkdir uploads
if not exist uploads\logos mkdir uploads\logos
if not exist uploads\form_submissions mkdir uploads\form_submissions
if not exist static\images mkdir static\images

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Open phpMyAdmin (http://localhost/phpmyadmin)
echo 3. Import schema.sql into collexo_db database
echo 4. (Optional) Import seed_data.sql for sample data
echo 5. Run the application:
echo    python app.py
echo.
echo Default admin login:
echo Email: admin@college.edu
echo Password: admin123
echo.
echo Application will be available at: http://127.0.0.1:5000
echo.
pause
