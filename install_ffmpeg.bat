@echo off
title Install FFmpeg for YouTube Downloader
color 0A

echo.
echo ========================================
echo   Installing FFmpeg for MP3 Support
echo ========================================
echo.
echo 🎵 FFmpeg is required to convert audio to MP3 format
echo.
echo 📥 Attempting to install FFmpeg using winget...
echo.

REM Check if winget is available
winget --version >nul 2>&1
if errorlevel 1 (
    echo ❌ winget is not available on this system
    echo.
    echo Please install FFmpeg manually:
    echo 1. Go to: https://ffmpeg.org/download.html
    echo 2. Download the Windows version
    echo 3. Extract to a folder (e.g., C:\ffmpeg)
    echo 4. Add C:\ffmpeg\bin to your PATH environment variable
    echo.
    pause
    exit /b 1
)

echo ✅ winget found! Installing FFmpeg...
echo.

REM Install FFmpeg
winget install ffmpeg

if errorlevel 1 (
    echo.
    echo ❌ Failed to install FFmpeg using winget
    echo.
    echo Please try installing manually:
    echo 1. Go to: https://ffmpeg.org/download.html
    echo 2. Download the Windows version
    echo 3. Extract to a folder (e.g., C:\ffmpeg)
    echo 4. Add C:\ffmpeg\bin to your PATH environment variable
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ FFmpeg installed successfully!
echo.
echo 🔄 Please restart your terminal/command prompt for changes to take effect
echo.
echo 🎵 You can now use the MP3 download feature in your YouTube Downloader!
echo.
pause 