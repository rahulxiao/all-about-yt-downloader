@echo off
title YouTube Downloader - GUI Mode
color 0B

echo.
echo ========================================
echo   YouTube Downloader - GUI Mode
echo ========================================
echo.
echo 🖥️  Starting Graphical User Interface...
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

REM Check if frontend.py exists
if not exist "frontend.py" (
    echo ❌ frontend.py not found in current directory
    echo.
    echo Please make sure you're running this batch file from the same
    echo directory as the Python script.
    echo.
    pause
    exit /b 1
)

echo ✅ GUI file found!
echo 🚀 Launching GUI...
echo.

python frontend.py

echo.
echo ========================================
echo   GUI closed. Press any key to exit...
echo ========================================
pause >nul 