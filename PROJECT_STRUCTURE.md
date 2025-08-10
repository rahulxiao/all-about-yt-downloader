# Project Structure Overview

## 📁 Core Files

### 🐍 Python Application
- **`frontend.py`** - Main GUI application with VideoHub theme
- **`backend.py`** - Core download logic and yt-dlp integration

### 🚀 Launchers & Installers
- **`run_gui_simple.bat`** - Windows launcher for the GUI
- **`install_ffmpeg.bat`** - FFmpeg installer for Windows

### 📋 Configuration & Documentation
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Main project documentation
- **`LICENSE`** - MIT License
- **`PROJECT_STRUCTURE.md`** - This file

## 📁 Directories

### 📥 Downloads
- **`downloads/`** - Default download output folder (empty by default)

### 🔧 Development
- **`.git/`** - Git version control (if using git)

## 🎯 File Purposes

### Frontend (`frontend.py`)
- Modern VideoHub-themed GUI
- Automatic clipboard detection
- Real-time progress tracking
- Format quality analysis
- Responsive dark theme design

### Backend (`backend.py`)
- YouTube video processing
- Format detection and filtering
- Download management
- FFmpeg integration
- Error handling and fallbacks

### Batch Files
- **`run_gui_simple.bat`** - Simple one-click launcher
- **`install_ffmpeg.bat`** - Automated FFmpeg installation

## 🔄 Development Workflow

1. **Edit** `frontend.py` for UI changes
2. **Edit** `backend.py` for core functionality
3. **Test** with `python frontend.py`
4. **Deploy** using `run_gui_simple.bat`

## 📝 Notes

- All temporary and test files have been removed
- Documentation has been cleaned and updated
- Project is now organized and production-ready
- Core functionality remains intact 