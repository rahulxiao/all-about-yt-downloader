@echo off
title YouTube Video and Audio Downloader (Auto Python Finder)
color 0E

echo.
echo ========================================
echo   YouTube Video and Audio Downloader
echo ========================================
echo.
echo This script offers both GUI and CLI modes!
echo Choose your preferred interface when prompted.
echo.

echo 🔍 Searching for Python installation...
echo.

set "python_found="
set "python_path="

REM Try different Python commands
python --version >nul 2>&1
if not errorlevel 1 (
    set "python_found=1"
    set "python_cmd=python"
    echo ✅ Found Python using 'python' command
    goto :check_files
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set "python_found=1"
    set "python_cmd=python3"
    echo ✅ Found Python using 'python3' command
    goto :check_files
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "python_found=1"
    set "python_cmd=py"
    echo ✅ Found Python using 'py' command
    goto :check_files
)

REM Search common installation directories
echo 🔍 Searching common Python installation directories...
for %%p in (C:\Python* C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python* C:\Program Files\Python* C:\Program Files (x86)\Python*) do (
    if exist "%%p\python.exe" (
        set "python_found=1"
        set "python_cmd=%%p\python.exe"
        echo ✅ Found Python at: %%p
        goto :check_files
    )
)

REM If still not found, try to find in PATH
echo 🔍 Searching PATH for Python...
for %%i in (python.exe python3.exe) do (
    where %%i >nul 2>&1
    if not errorlevel 1 (
        set "python_found=1"
        set "python_cmd=%%i
        echo ✅ Found Python using: %%i
        goto :check_files
    )
)

:python_not_found
echo.
echo ❌ Python not found!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
echo.
echo After installation, restart your computer and try again.
echo.
pause
exit /b 1

:check_files
echo.
echo ✅ Using Python command: %python_cmd%
echo.

REM Check if all required files exist
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
    %python_cmd% frontend.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Starting CLI Mode...
    %python_cmd% backend.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Starting Main Menu...
    %python_cmd% youtube_downloader.py
) else (
    echo.
    echo ❌ Invalid choice. Starting Main Menu...
    %python_cmd% youtube_downloader.py
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