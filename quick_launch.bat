@echo off
title YouTube Downloader - Quick Launch
color 0D

echo.
echo ========================================
echo   YouTube Downloader - Quick Launch
echo ========================================
echo.
echo 🚀 Quick launch options:
echo.
echo 1. 🖥️  GUI Mode (Direct)
echo 2. 💻 CLI Mode (Direct)
echo 3. 🎯 Main Menu
echo 4. 🔧 Install Dependencies
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Launching GUI Mode directly...
    python launch.py --gui
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Launching CLI Mode directly...
    python launch.py --cli
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Launching Main Menu...
    python launch.py
) else if "%choice%"=="4" (
    echo.
    echo 🔧 Installing dependencies...
    call install_dependencies.bat
) else (
    echo.
    echo ❌ Invalid choice. Launching Main Menu...
    python launch.py
)

echo.
echo ========================================
echo   Press any key to exit...
echo ========================================
pause >nul 