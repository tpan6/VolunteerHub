@echo off
REM VolunteerHub Setup Script for Windows
REM This script automates the setup process for the VolunteerHub application

echo.
echo ========================================
echo    VolunteerHub Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is not installed.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo ✓ Python 3 found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
flask init-db

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run the application:
echo      python app.py
echo.
echo   3. Open your browser to http://localhost:5000
echo.
echo Happy volunteering!
echo.
pause
