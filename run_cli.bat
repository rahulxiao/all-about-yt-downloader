@echo off
title YouTube Downloader - CLI Mode
color 0E

echo.
echo ========================================
echo   YouTube Downloader - CLI Mode
echo ========================================
echo.
echo 💻 Starting Command Line Interface...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Check if backend.py exists
if not exist "backend.py" (
    echo ❌ backend.py not found in current directory
    echo.
    echo Please make sure you're running this batch file from the same
    echo directory as the Python script.
    echo.
    pause
    exit /b 1
)

echo ✅ CLI file found!
echo 🚀 Launching CLI...
echo.

python backend.py

echo.
echo ========================================
echo   CLI closed. Press any key to exit...
echo ========================================
pause >nul 