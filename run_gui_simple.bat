@echo off
title YouTube Downloader - GUI
color 0B

echo.
echo ========================================
echo   YouTube Downloader - GUI Mode
echo ========================================
echo.
echo 🚀 Starting GUI...
echo.

REM Use the correct Python path
set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe

REM Launch GUI directly
%PYTHON_PATH% frontend.py

echo.
echo ========================================
echo   GUI closed. Press any key to exit...
echo ========================================
pause >nul 