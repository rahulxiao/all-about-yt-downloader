@echo off
title YouTube Downloader - Main Launcher
color 0F

:menu
cls
echo.
echo ========================================
echo   🎬 YouTube Video Downloader
echo ========================================
echo.
echo 📁 Available Launch Options:
echo.
echo 🖥️  GUI Mode:
echo    1. Quick GUI Launch
echo    2. GUI with Dependencies Check
echo.
echo 💻 CLI Mode:
echo    3. Quick CLI Launch
echo    4. CLI with Dependencies Check
echo.
echo 🎯 Other Options:
echo    5. Main Menu (Choose Mode)
echo    6. Install/Update Dependencies
echo    7. Check Python Installation
echo    8. Exit
echo.
echo ========================================
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Quick GUI Launch...
    python frontend.py
    goto :menu
) else if "%choice%"=="2" (
    echo.
    echo 🚀 GUI with Dependencies Check...
    call run_gui.bat
    goto :menu
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Quick CLI Launch...
    python backend.py
    goto :menu
) else if "%choice%"=="4" (
    echo.
    echo 🚀 CLI with Dependencies Check...
    call run_cli.bat
    goto :menu
) else if "%choice%"=="5" (
    echo.
    echo 🚀 Main Menu...
    python youtube_downloader.py
    goto :menu
) else if "%choice%"=="6" (
    echo.
    echo 🔧 Installing Dependencies...
    call install_dependencies.bat
    goto :menu
) else if "%choice%"=="7" (
    echo.
    echo 🔍 Checking Python Installation...
    call check_python.bat
    goto :menu
) else if "%choice%"=="8" (
    echo.
    echo 👋 Goodbye!
    echo.
    pause
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please enter 1-8.
    echo.
    pause
    goto :menu
) 