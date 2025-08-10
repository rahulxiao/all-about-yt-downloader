# VideoHub Desktop Suite - YouTube Video Downloader

A modern, feature-rich YouTube video downloader with an elegant dark theme interface and automatic clipboard detection.

## ✨ Features

- **🎨 Modern Dark Theme UI** - Beautiful VideoHub-inspired design
- **📋 Automatic Clipboard Detection** - Auto-pastes YouTube URLs from clipboard
- **🔍 Smart Format Detection** - Automatically identifies video and audio formats
- **📊 Quality Analysis** - Detailed analysis of available video qualities
- **⬇️ Multiple Download Options** - Video, audio, and raw audio downloads
- **📁 Flexible Output Management** - Custom save locations and file naming
- **🔄 Real-time Progress** - Live download progress with detailed status
- **🎯 Quality Filtering** - Filter formats by resolution and quality

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- FFmpeg (for audio processing)

### Installation
1. **Clone or download** this repository
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install FFmpeg** (run `install_ffmpeg.bat` on Windows)
4. **Launch the application:**
   ```bash
   python frontend.py
   ```
   Or use the provided batch file: `run_gui_simple.bat`

## 🎮 How to Use

1. **Copy a YouTube URL** to your clipboard
2. **Launch VideoHub** - URLs are automatically detected and pasted
3. **Click "Fetch Video Info"** to analyze available formats
4. **Select quality and download type** (video/audio)
5. **Choose output location** and click "Download"
6. **Monitor progress** in real-time

## 🏗️ Project Structure

```
📁 VideoHub Desktop Suite/
├── 🐍 frontend.py          # Main GUI application
├── 🐍 backend.py           # Core download logic
├── 📋 requirements.txt     # Python dependencies
├── 🚀 run_gui_simple.bat  # Windows launcher
├── 🔧 install_ffmpeg.bat  # FFmpeg installer
├── 📚 README.md           # This file
├── 📄 LICENSE            # MIT License
└── 📁 downloads/         # Download output folder
```

## 🎨 UI Features

- **Dark Theme** - Easy on the eyes with modern aesthetics
- **Responsive Layout** - Adapts to different window sizes
- **Smart Notifications** - Subtle feedback for clipboard operations
- **Progress Tracking** - Real-time download progress display
- **Format Tree View** - Organized display of available formats

## 🔧 Technical Details

- **Frontend**: Tkinter with custom styling
- **Backend**: yt-dlp for YouTube processing
- **Audio Processing**: FFmpeg for format conversion
- **Clipboard**: pyperclip for automatic URL detection
- **Threading**: Non-blocking UI with background operations

## 📋 Requirements

```
yt-dlp>=2023.12.30
pyperclip>=1.8.2
```

## 🐛 Troubleshooting

### Common Issues
- **FFmpeg not found**: Run `install_ffmpeg.bat`
- **Download errors**: Check internet connection and URL validity
- **Format issues**: Try refreshing formats or different quality selection

### Getting Help
- Check that all dependencies are installed
- Ensure FFmpeg is properly installed
- Verify YouTube URL is accessible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve VideoHub Desktop Suite.

---

**Made with ❤️ for content creators and video enthusiasts** 