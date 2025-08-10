@echo off
title YouTube Video and Audio Downloader
color 0A

echo.
echo ========================================
echo   YouTube Video and Audio Downloader
echo ========================================
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

echo.
echo ========================================
echo   Press any key to exit...
echo ========================================
pause >nul 