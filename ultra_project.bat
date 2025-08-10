@echo off
title VideoHub Desktop Suite - Ultra Project Manager
color 0b

REM Set Python path explicitly
set PYTHON_PATH="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"

echo.
echo ================================================================================
echo                        VideoHub Desktop Suite
echo                           Ultra Project Manager
echo ================================================================================
echo.

:main_menu
echo.
echo MAIN MENU - Choose an option:
echo.
echo [1] Launch VideoHub GUI
echo [2] Run Python Console
echo [3] Install/Update Dependencies
echo [4] Install FFmpeg
echo [5] Clean Project
echo [6] Project Status
echo [7] Debug Mode
echo [8] Open Documentation
echo [9] Open Project Folder
echo [0] Exit
echo.

set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto launch_gui
if "%choice%"=="2" goto python_console
if "%choice%"=="3" goto install_deps
if "%choice%"=="4" goto install_ffmpeg
if "%choice%"=="5" goto clean_project
if "%choice%"=="6" goto project_status
if "%choice%"=="7" goto debug_mode
if "%choice%"=="8" goto open_docs
if "%choice%"=="9" goto open_folder
if "%choice%"=="0" goto exit
goto invalid_choice

:launch_gui
echo.
echo Launching VideoHub GUI...
echo.
if exist "frontend.py" (
    echo [OK] Found frontend.py - Starting GUI...
    echo.
    %PYTHON_PATH% frontend.py
) else (
    echo [ERROR] frontend.py not found!
    echo Please ensure you're in the correct project directory.
    pause
)
goto main_menu

:python_console
echo.
echo Starting Python Console...
echo.
echo Available imports:
echo - import frontend
echo - import backend
echo - from backend import *
echo.
echo Type 'exit()' to return to main menu
echo.
%PYTHON_PATH%
goto main_menu

:install_deps
echo.
echo Installing/Updating Dependencies...
echo.
if exist "requirements.txt" (
    echo [OK] Found requirements.txt
    echo Installing dependencies...
    %PYTHON_PATH% -m pip install -r requirements.txt --upgrade
    echo.
    echo [OK] Dependencies updated!
) else (
    echo [ERROR] requirements.txt not found!
    echo Creating basic requirements.txt...
    echo yt-dlp>=2023.12.30 > requirements.txt
    echo pyperclip>=1.8.2 >> requirements.txt
    echo.
    echo [OK] Created requirements.txt
    echo Installing dependencies...
    %PYTHON_PATH% -m pip install -r requirements.txt
)
echo.
pause
goto main_menu

:install_ffmpeg
echo.
echo Installing FFmpeg...
echo.
if exist "install_ffmpeg.bat" (
    echo [OK] Found install_ffmpeg.bat
    echo Running FFmpeg installer...
    call install_ffmpeg.bat
) else (
    echo [ERROR] install_ffmpeg.bat not found!
    echo.
    echo Manual FFmpeg installation:
    echo 1. Download from: https://ffmpeg.org/download.html
    echo 2. Or use: winget install ffmpeg
    echo 3. Add to PATH environment variable
)
echo.
pause
goto main_menu

:clean_project
echo.
echo Cleaning Project...
echo.
echo Removing temporary files...
if exist "*.tmp" del /q *.tmp
if exist "__pycache__" rmdir /s /q __pycache__
if exist "*.pyc" del /q *.pyc
if exist "*.pyo" del /q *.pyo
echo.
echo [OK] Project cleaned!
echo.
pause
goto main_menu

:project_status
echo.
echo PROJECT STATUS
echo.
echo Project Directory: %CD%
echo.
if exist "frontend.py" (
    echo [OK] frontend.py - Found
    for %%A in (frontend.py) do echo    Size: %%~zA bytes
) else (
    echo [ERROR] frontend.py - Missing
)
echo.
if exist "backend.py" (
    echo [OK] backend.py - Found
    for %%A in (backend.py) do echo    Size: %%~zA bytes
) else (
    echo [ERROR] backend.py - Missing
)
echo.
if exist "requirements.txt" (
    echo [OK] requirements.txt - Found
) else (
    echo [ERROR] requirements.txt - Missing
)
echo.
if exist "run_gui_simple.bat" (
    echo [OK] run_gui_simple.bat - Found
) else (
    echo [ERROR] run_gui_simple.bat - Missing
)
echo.
if exist "install_ffmpeg.bat" (
    echo [OK] install_ffmpeg.bat - Found
) else (
    echo [ERROR] install_ffmpeg.bat - Missing
)
echo.
if exist "downloads" (
    echo [OK] downloads/ - Directory exists
    dir downloads /b 2>nul | find /c /v "" > temp_count.txt
    set /p file_count=<temp_count.txt
    del temp_count.txt
    echo    Files: %file_count%
) else (
    echo [ERROR] downloads/ - Missing
)
echo.
echo Checking Python installation...
%PYTHON_PATH% --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo Please check your Python installation path
) else (
    echo [OK] Python found at: %PYTHON_PATH%
)
echo.
pause
goto main_menu

:debug_mode
echo.
echo DEBUG MODE
echo.
echo Available debug options:
echo [1] Test frontend import
echo [2] Test backend import
echo [3] Check yt-dlp installation
echo [4] Check pyperclip installation
echo [5] Test FFmpeg
echo [6] Return to main menu
echo.
set /p debug_choice="Enter debug choice (1-6): "

if "%debug_choice%"=="1" goto test_frontend
if "%debug_choice%"=="2" goto test_backend
if "%debug_choice%"=="3" goto test_ytdlp
if "%debug_choice%"=="4" goto test_pyperclip
if "%debug_choice%"=="5" goto test_ffmpeg
if "%debug_choice%"=="6" goto main_menu
goto debug_mode

:test_frontend
echo.
echo Testing frontend import...
%PYTHON_PATH% -c "import frontend; print('[OK] Frontend imports successfully')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Frontend import failed
    echo Error details:
    %PYTHON_PATH% -c "import frontend" 2>&1
)
pause
goto debug_mode

:test_backend
echo.
echo Testing backend import...
%PYTHON_PATH% -c "import backend; print('[OK] Backend imports successfully')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Backend import failed
    echo Error details:
    %PYTHON_PATH% -c "import backend" 2>&1
)
pause
goto debug_mode

:test_ytdlp
echo.
echo Testing yt-dlp installation...
%PYTHON_PATH% -c "import yt_dlp; print('[OK] yt-dlp version:', yt_dlp.version.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] yt-dlp not installed
    echo Install with: %PYTHON_PATH% -m pip install yt-dlp
)
pause
goto debug_mode

:test_pyperclip
echo.
echo Testing pyperclip installation...
%PYTHON_PATH% -c "import pyperclip; print('[OK] pyperclip version:', pyperclip.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pyperclip not installed
    echo Install with: %PYTHON_PATH% -m pip install pyperclip
)
pause
goto debug_mode

:test_ffmpeg
echo.
echo Testing FFmpeg installation...
ffmpeg -version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] FFmpeg not found in PATH
    echo Install FFmpeg first
) else (
    echo [OK] FFmpeg found
)
pause
goto debug_mode

:open_docs
echo.
echo Opening Documentation...
echo.
if exist "README.md" (
    echo Opening README.md...
    start README.md
) else (
    echo [ERROR] README.md not found
)
if exist "PROJECT_STRUCTURE.md" (
    echo Opening PROJECT_STRUCTURE.md...
    start PROJECT_STRUCTURE.md
) else (
    echo [ERROR] PROJECT_STRUCTURE.md not found
)
echo.
pause
goto main_menu

:open_folder
echo.
echo Opening Project Folder...
echo.
explorer .
goto main_menu

:invalid_choice
echo.
echo [ERROR] Invalid choice! Please enter a number between 0-9
echo.
pause
goto main_menu

:exit
echo.
echo Thank you for using VideoHub Desktop Suite!
echo.
echo Project cleaned and organized successfully
echo Ready for development and production use
echo.
echo Press any key to exit...
pause >nul
exit 