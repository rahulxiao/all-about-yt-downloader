# 🎬 YouTube Video and Audio Downloader

A comprehensive Python application for downloading YouTube videos and audio with a modern dark-themed GUI and CLI interface.

## ✨ Features

- **🎥 Video Downloads**: Download videos in various formats and qualities
- **🎵 Audio Downloads**: Download audio and automatically convert to MP3
- **🌙 Dark Theme**: Modern, eye-friendly dark interface
- **🖥️ GUI Mode**: Intuitive graphical user interface
- **💻 CLI Mode**: Command-line interface for automation
- **📊 Format Selection**: Choose from available video/audio formats
- **📁 Custom Output**: Select custom download directories
- **⚡ Progress Tracking**: Real-time download progress and speed

## 🎵 MP3 Audio Downloads

**Important**: MP3 functionality requires FFmpeg to be installed on your system!

- **Automatic Conversion**: All audio downloads are automatically converted to MP3 format
- **Quality**: 192kbps MP3 output for optimal file size and quality
- **Format Support**: Downloads from any available audio format and converts to MP3

### Installing FFmpeg for MP3 Support

#### Windows (Recommended)
```bash
# Using winget (Windows 10/11)
winget install ffmpeg

# Or download manually from: https://ffmpeg.org/download.html
```

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

**After installing FFmpeg, restart your terminal/command prompt for changes to take effect.**

## 🏗️ Project Structure

The application is now organized into separate modules for better maintainability:

```
youtube-downloader/
├── backend.py           # Core functionality (downloads, format handling)
├── frontend.py          # GUI interface (dark theme, user interactions)
├── youtube_downloader.py # Main entry point with mode selection
├── launch.py            # Quick launcher for direct mode access
├── install_ffmpeg.bat   # Windows FFmpeg installer (winget)
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Internet connection
- **FFmpeg** (for audio conversion to MP3) - see installation above

### Installation

1. **Clone or download** the project files
2. **Install Python dependencies** (automatic on first run):
   ```bash
   pip install yt-dlp
   ```
3. **Install FFmpeg** (required for MP3):
   - Windows: Run `install_ffmpeg.bat` or use `winget install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt install ffmpeg`
4. **Run the application**:
   ```bash
   python youtube_downloader.py
   ```

## 🎯 Usage

### Main Menu
The main application provides a menu to choose between GUI and CLI modes:

```bash
python youtube_downloader.py
```

### Direct Mode Launch
Use the launcher script for quick access to specific modes:

```bash
# Launch GUI directly
python launch.py gui

# Launch CLI directly  
python launch.py cli

# Show help
python launch.py help
```

### GUI Mode
1. **Enter YouTube URL** in the URL field
2. **Select download type**: Video or Audio (MP3)
3. **Click "🔍 Get Video Info"** to fetch available formats
4. **Choose format** from the list
5. **Set output directory** (optional)
6. **Click "📥 Download"** to start

### CLI Mode
1. **Choose option**: Download Video (1) or Audio (2)
2. **Enter YouTube URL**
3. **Select format** from the numbered list
4. **Set output directory** (optional)
5. **Wait for completion**

## 🔧 Technical Details

### Backend (`backend.py`)
- **Core Functions**: Video info extraction, format parsing, downloads
- **Dependencies**: yt-dlp, FFmpeg (for MP3 conversion)
- **Features**: Progress tracking, error handling, format sorting

### Frontend (`frontend.py`)
- **GUI Framework**: tkinter with custom dark theme
- **Threading**: Non-blocking downloads and API calls
- **Responsive Design**: Modern UI with proper spacing and typography

### Audio Conversion
- **Automatic MP3**: All audio downloads are converted to MP3
- **Quality**: 192kbps MP3 output
- **FFmpeg Integration**: Uses FFmpeg for reliable audio conversion

## 🎨 Dark Theme Colors

The GUI uses a carefully designed dark color scheme:

- **Background**: `#1e1e1e` (Dark gray)
- **Secondary**: `#2d2d2d` (Medium gray)
- **Input Fields**: `#3d3d3d` (Light gray)
- **Text**: `#ffffff` (White)
- **Accent**: `#007acc` (Blue)

## 📁 File Organization

- **Downloads**: Saved to `downloads/` folder by default
- **Custom Paths**: Users can specify custom output directories
- **File Naming**: Uses video title + extension format

## 🛠️ Troubleshooting

### Common Issues

1. **yt-dlp not found**: The app will automatically install it on first run
2. **FFmpeg missing**: Install FFmpeg for audio conversion to MP3
3. **tkinter errors**: Use CLI mode if GUI is not available
4. **Download failures**: Check internet connection and URL validity

### MP3 Download Issues

**Problem**: "I can't see MP3 there" or MP3 downloads not working

**Solution**: Install FFmpeg - it's required for MP3 conversion!

1. **Windows**: Run `install_ffmpeg.bat` or use `winget install ffmpeg`
2. **macOS**: `brew install ffmpeg`
3. **Ubuntu/Debian**: `sudo apt install ffmpeg`
4. **Restart your terminal/command prompt** after installation

**Why FFmpeg?**: Your downloader automatically converts any audio format to MP3, but this conversion requires FFmpeg. Without it, audio downloads will fail.

### Error Messages

- **❌ Error getting video info**: Invalid URL or network issue
- **❌ No formats available**: Video may be restricted or unavailable
- **❌ Download failed**: Check disk space and permissions
- **❌ FFmpeg is not installed**: Install FFmpeg for MP3 conversion (see above)

## 🔄 Updates and Maintenance

The modular structure makes it easy to:
- **Update backend logic** without affecting the UI
- **Modify the GUI** without touching core functionality
- **Add new features** in isolated modules
- **Test components** independently

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! The modular structure makes it easy to:
- Add new download formats
- Improve the UI design
- Enhance error handling
- Add new features

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the console
3. Ensure all dependencies are installed
4. Verify YouTube URL accessibility

---

**Enjoy downloading your favorite YouTube content! 🎉** 