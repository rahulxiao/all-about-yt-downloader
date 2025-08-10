@echo off
title Python Installation Checker
color 0B

echo.
echo ========================================
echo      Python Installation Checker
echo ========================================
echo.

echo Checking Python installation...
echo.

REM Check multiple Python commands
echo 1. Checking 'python' command...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ 'python' command not found
) else (
    echo    ✅ 'python' command found
    python --version
)

echo.
echo 2. Checking 'python3' command...
python3 --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ 'python3' command not found
) else (
    echo    ✅ 'python3' command found
    python3 --version
)

echo.
echo 3. Checking 'py' command (Windows Python Launcher)...
py --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ 'py' command not found
) else (
    echo    ✅ 'py' command found
    py --version
)

echo.
echo ========================================
echo Checking common Python installation paths...
echo ========================================

REM Check common Python installation directories
set "python_paths=C:\Python* C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python* C:\Program Files\Python* C:\Program Files (x86)\Python*"

for %%p in (%python_paths%) do (
    if exist "%%p\python.exe" (
        echo Found Python at: %%p
        echo Python version: 
        "%%p\python.exe" --version 2>nul
        echo.
    )
)

echo.
echo ========================================
echo Current PATH environment variable:
echo ========================================
echo %PATH%

echo.
echo ========================================
echo Recommendations:
echo ========================================
echo.
echo If Python is installed but not in PATH:
echo 1. Find your Python installation directory
echo 2. Add it to your system PATH environment variable
echo 3. Or use the full path to python.exe
echo.
echo If Python is not installed:
echo 1. Download from https://www.python.org/downloads/
echo 2. Check "Add Python to PATH" during installation
echo 3. Restart your computer
echo.

pause 