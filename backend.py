#!/usr/bin/env python3
"""
YouTube Video and Audio Downloader - Backend
Core functionality for downloading YouTube videos and audio
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("❌ yt-dlp is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("✅ yt-dlp installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install yt-dlp. Please install it manually:")
            print("   pip install yt-dlp")
            return False

def check_ffmpeg():
    """Check if FFmpeg is available for audio conversion"""
    try:
        # Try to run ffmpeg -version
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True
        else:
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

def get_video_info(url):
    """Get video information from YouTube URL"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"❌ Error getting video info: {e}")
        return None

def get_available_formats(info):
    """Get available video and audio formats"""
    formats = info.get('formats', [])
    
    video_formats = []
    audio_formats = []
    
    for fmt in formats:
        # Skip formats with no format_id
        if not fmt.get('format_id'):
            continue
            
        # Video with audio (both video and audio codecs)
        if (fmt.get('vcodec') and fmt.get('vcodec') != 'none' and 
            fmt.get('acodec') and fmt.get('acodec') != 'none'):
            video_formats.append({
                'format_id': fmt['format_id'],
                'ext': fmt.get('ext', 'unknown'),
                'resolution': fmt.get('resolution', 'unknown'),
                'filesize': fmt.get('filesize', 0),
                'vcodec': fmt.get('vcodec', 'unknown'),
                'acodec': fmt.get('acodec', 'unknown'),
                'fps': fmt.get('fps', 0),
                'height': fmt.get('height', 0),
                'width': fmt.get('width', 0)
            })
        # Audio only (has audio codec but no video codec)
        elif (fmt.get('acodec') and fmt.get('acodec') != 'none' and 
              (not fmt.get('vcodec') or fmt.get('vcodec') == 'none')):
            audio_formats.append({
                'format_id': fmt['format_id'],
                'ext': fmt.get('ext', 'unknown'),
                'filesize': fmt.get('filesize', 0),
                'acodec': fmt.get('acodec', 'unknown'),
                'abr': fmt.get('abr', 0)  # Audio bitrate
            })
    
    # Sort formats by quality (higher resolution/bitrate first)
    video_formats.sort(key=lambda x: (x.get('height', 0), x.get('fps', 0)), reverse=True)
    audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
    
    return video_formats, audio_formats

def display_video_info(info):
    """Display video information"""
    print("\n" + "="*60)
    print("📹 VIDEO INFORMATION")
    print("="*60)
    
    title = info.get('title', 'Unknown')
    duration = info.get('duration', 0)
    uploader = info.get('uploader', 'Unknown')
    view_count = info.get('view_count', 0)
    upload_date = info.get('upload_date', 'Unknown')
    
    print(f"Title: {title}")
    if duration:
        print(f"Duration: {duration // 60} minutes")
    else:
        print("Duration: Unknown")
    print(f"Uploader: {uploader}")
    if view_count:
        print(f"Views: {view_count:,}")
    else:
        print("Views: Unknown")
    print(f"Upload Date: {upload_date}")
    print("="*60)

def display_formats(video_formats, audio_formats):
    """Display available formats"""
    print("\n🎬 AVAILABLE VIDEO FORMATS:")
    print("-" * 60)
    for i, fmt in enumerate(video_formats, 1):
        size_mb = fmt.get('filesize', 0) / (1024 * 1024) if fmt.get('filesize') else 0
        resolution = fmt.get('resolution', 'unknown')
        ext = fmt.get('ext', 'unknown')
        fps = fmt.get('fps', 0)
        
        print(f"{i:2d}. {fmt['format_id']:>8} | {resolution:>12} | "
              f"{ext:>4} | {fps:>3}fps | {size_mb:>6.1f}MB")
    
    print("\n🎵 AVAILABLE AUDIO FORMATS:")
    print("-" * 60)
    for i, fmt in enumerate(audio_formats, 1):
        size_mb = fmt.get('filesize', 0) / (1024 * 1024) if fmt.get('filesize') else 0
        abr = fmt.get('abr', 0) or 0  # Handle None values
        ext = fmt.get('ext', 'unknown')
        
        print(f"{i:2d}. {fmt['format_id']:>8} | {ext:>4} | "
              f"{abr:>4}kbps | {size_mb:>6.1f}MB")

def download_video(url, format_id, output_path="downloads"):
    """Download video with specified format"""
    try:
        import yt_dlp
        
        # Create output directory
        Path(output_path).mkdir(exist_ok=True)
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
        
        print(f"\n📥 Downloading video with format {format_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Video download completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return False

def download_audio(url, format_id, output_path="downloads"):
    """Download audio with specified format and convert to MP3"""
    try:
        import yt_dlp
        
        # Check if FFmpeg is available
        if not check_ffmpeg():
            print("❌ FFmpeg is not installed or not in PATH!")
            print("   FFmpeg is required for MP3 conversion.")
            print("   Please install FFmpeg:")
            print("   - Windows: Download from https://ffmpeg.org/download.html")
            print("   - Windows (winget): winget install ffmpeg")
            print("   - macOS: brew install ffmpeg")
            print("   - Ubuntu/Debian: sudo apt install ffmpeg")
            print("   After installation, restart your terminal/command prompt.")
            return False
        
        # Create output directory
        Path(output_path).mkdir(exist_ok=True)
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        print(f"\n🎵 Downloading audio with format {format_id} and converting to MP3...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Audio download and MP3 conversion completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        return False

def progress_hook(d):
    """Progress hook for download progress"""
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        
        if total > 0:
            percentage = (downloaded / total) * 100
            speed = d.get('speed', 0)
            if speed:
                speed_mb = speed / (1024 * 1024)
                print(f"\r📥 Progress: {percentage:.1f}% | Speed: {speed_mb:.1f} MB/s", end='', flush=True)
    
    elif d['status'] == 'finished':
        print(f"\n✅ Downloaded: {d['filename']}")

def run_cli():
    """Run the CLI version of the downloader"""
    print("🎬 YouTube Video and Audio Downloader (CLI Mode)")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Download Video")
        print("2. Download Audio")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '3':
            print("👋 Returning to main menu...")
            break
        
        elif choice in ['1', '2']:
            url = input("\nEnter YouTube URL: ").strip()
            
            if not url:
                print("❌ Please enter a valid URL")
                continue
            
            # Get video info
            print("🔍 Getting video information...")
            info = get_video_info(url)
            
            if not info:
                print("❌ Could not get video information. Please check the URL.")
                continue
            
            # Display video info
            display_video_info(info)
            
            # Get available formats
            video_formats, audio_formats = get_available_formats(info)
            
            if choice == '1':  # Download Video
                if not video_formats:
                    print("❌ No video formats available")
                    continue
                
                display_formats(video_formats, audio_formats)
                
                try:
                    format_choice = int(input(f"\nSelect video format (1-{len(video_formats)}): "))
                    if 1 <= format_choice <= len(video_formats):
                        selected_format = video_formats[format_choice - 1]
                        output_path = input("Enter output directory (default: downloads): ").strip() or "downloads"
                        download_video(url, selected_format['format_id'], output_path)
                    else:
                        print("❌ Invalid format choice")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            elif choice == '2':  # Download Audio
                if not audio_formats:
                    print("❌ No audio formats available")
                    continue
                
                # Check FFmpeg availability for audio downloads
                if not check_ffmpeg():
                    print("\n❌ FFmpeg is not installed or not in PATH!")
                    print("   FFmpeg is required for MP3 conversion.")
                    print("   Please install FFmpeg:")
                    print("   - Windows: Download from https://ffmpeg.org/download.html")
                    print("   - Windows (winget): winget install ffmpeg")
                    print("   - macOS: brew install ffmpeg")
                    print("   - Ubuntu/Debian: sudo apt install ffmpeg")
                    print("   After installation, restart your terminal/command prompt.")
                    continue
                
                display_formats(video_formats, audio_formats)
                
                try:
                    format_choice = int(input(f"\nSelect audio format (1-{len(audio_formats)}): "))
                    if 1 <= format_choice <= len(audio_formats):
                        selected_format = audio_formats[format_choice - 1]
                        output_path = input("Enter output directory (default: downloads): ").strip() or "downloads"
                        download_audio(url, selected_format['format_id'], output_path)
                    else:
                        print("❌ Invalid format choice")
                except ValueError:
                    print("❌ Please enter a valid number")
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.") 