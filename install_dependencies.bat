@echo off
title YouTube Downloader - Install Dependencies
color 0C

echo.
echo ========================================
echo   YouTube Downloader - Install Dependencies
echo ========================================
echo.
echo 🔧 Setting up the environment...
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
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    echo.
    echo Please ensure pip is installed with Python
    echo.
    pause
    exit /b 1
)

echo ✅ pip found!
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    echo.
    echo Creating basic requirements.txt...
    echo yt-dlp > requirements.txt
    echo.
)

echo 📦 Installing Python dependencies...
echo.

REM Upgrade pip first
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 📥 Installing required packages...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Some packages failed to install
    echo.
    echo Trying to install yt-dlp directly...
    python -m pip install yt-dlp
    
    if errorlevel 1 (
        echo.
        echo ❌ Failed to install yt-dlp
        echo.
        echo Please check your internet connection and try again
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ Dependencies installed successfully!
echo.

REM Check if FFmpeg is mentioned in requirements or if we should warn about it
echo 📋 Checking for FFmpeg...
echo.
echo Note: FFmpeg is required for MP3 audio conversion
echo If you haven't installed FFmpeg yet:
echo 1. Download from: https://ffmpeg.org/download.html
echo 2. Add to your system PATH
echo 3. Or place ffmpeg.exe in this directory
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo You can now run the downloader using:
echo - run_gui.bat (for GUI mode)
echo - run_cli.bat (for CLI mode)
echo - run_downloader.bat (for mode selection)
echo.
pause 