@echo off
title YouTube Video and Audio Downloader
color 0A

echo.
echo ========================================
echo   YouTube Video and Audio Downloader
echo ========================================
echo.
echo This script offers both GUI and CLI modes!
echo Choose your preferred interface when prompted.
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

REM Check if the required files exist
if not exist "youtube_downloader.py" (
    echo ❌ youtube_downloader.py not found in current directory
    echo.
    echo Please make sure you're running this batch file from the same
    echo directory as the Python script.
    echo.
    pause
    exit /b 1
)

if not exist "frontend.py" (
    echo ❌ frontend.py not found in current directory
    echo.
    echo Please make sure you're running this batch file from the same
    echo directory as the Python script.
    echo.
    pause
    exit /b 1
)

if not exist "backend.py" (
    echo ❌ backend.py not found in current directory
    echo.
    echo Please make sure you're running this batch file from the same
    echo directory as the Python script.
    echo.
    pause
    exit /b 1
)

echo ✅ All required files found!
echo.
echo Choose your preferred mode:
echo.
echo 1. 🖥️  GUI Mode (Graphical Interface)
echo 2. 💻 CLI Mode (Command Line Interface)
echo 3. 🎯 Main Menu (Choose from both)
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting GUI Mode...
    python frontend.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Starting CLI Mode...
    python backend.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Starting Main Menu...
    python youtube_downloader.py
) else (
    echo.
    echo ❌ Invalid choice. Starting Main Menu...
    python youtube_downloader.py
)

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo ❌ The script encountered an error
    echo.
    echo Common solutions:
    echo - Make sure you have internet connection
    echo - Try running as administrator if you get permission errors
    echo - Check if the YouTube URL is valid
    echo - Make sure all required dependencies are installed
    echo.
)

echo.
echo ========================================
echo   Press any key to exit...
echo ========================================
pause >nul 