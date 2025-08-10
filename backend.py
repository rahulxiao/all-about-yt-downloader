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
        print("✅ yt-dlp is installed")
        
        # Check if yt-dlp is up to date
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "pip", "show", "yt-dlp"], 
                                  capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore', timeout=10)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                version_line = [line for line in lines if line.startswith('Version:')]
                if version_line:
                    version = version_line[0].split(':')[1].strip()
                    print(f"📦 yt-dlp version: {version}")
                    
                    # Suggest update if version is old
                    if version < '2023.12.30':
                        print("⚠️  yt-dlp version is old. YouTube may block requests.")
                        print("   Consider updating: pip install --upgrade yt-dlp")
        except Exception:
            pass
            
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
    # Common FFmpeg locations on Windows
    ffmpeg_paths = [
        'ffmpeg',  # If in PATH
        r'C:\ffmpeg\bin\ffmpeg.exe',  # Common installation path
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
        # Winget installation path
        os.path.expanduser(r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg.exe'),
    ]
    
    for ffmpeg_path in ffmpeg_paths:
        try:
            # Try to run ffmpeg -version
            result = subprocess.run([ffmpeg_path, '-version'], 
                                  capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore', timeout=10)
            if result.returncode == 0:
                print(f"✅ FFmpeg found at: {ffmpeg_path}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    
    print("❌ FFmpeg not found in common locations")
    print("   Please ensure FFmpeg is installed and in your PATH")
    return False

def get_video_info(url):
    """Get video information from YouTube URL"""
    try:
        import yt_dlp
        
        # Use the most reliable options to avoid 403 errors
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Simple but effective headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            # Remove problematic options that can cause 403 errors
            'extractor_retries': 5,
            'fragment_retries': 5,
            'retries': 5,
            # Force IPv4 to avoid some network issues
            'source_address': '0.0.0.0',
            # Disable cookies to avoid decryption issues
            'cookiefile': None,
            'cookiesfrombrowser': None,
        }
        
        print("🔍 Fetching video information...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
                
    except Exception as e:
        print(f"❌ Error getting video info: {e}")
        # Try one more time with minimal options
        try:
            print("🔄 Retrying with minimal options...")
            import yt_dlp
            
            ydl_opts_minimal = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_minimal) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e2:
            print(f"❌ Retry also failed: {e2}")
            return None

def get_available_formats(info):
    """Get available video and audio formats with accurate resolution detection"""
    formats = info.get('formats', [])
    
    video_formats = []
    audio_formats = []
    
    for fmt in formats:
        # Skip formats with no format_id
        if not fmt.get('format_id'):
            continue
            
        # Video formats (including video-only streams)
        if (fmt.get('vcodec') and fmt.get('vcodec') != 'none'):
            # Extract actual dimensions
            width = fmt.get('width', 0)
            height = fmt.get('height', 0)
            
            # Build accurate resolution string
            resolution = "unknown"
            if width and height:
                # Use actual dimensions for precise resolution
                resolution = f"{width}x{height}"
                
                # Also add standard quality label
                if height >= 4320:
                    quality_label = "8K"
                elif height >= 2160:
                    quality_label = "4K"
                elif height >= 1440:
                    quality_label = f"{height}p"
                elif height >= 720:
                    quality_label = f"{height}p"
                else:
                    quality_label = f"{height}p"
                
                # Store both precise and standard labels
                resolution_precise = resolution
                resolution_standard = quality_label
            elif height:
                # Only height available
                if height >= 4320:
                    resolution = "8K"
                    resolution_precise = f"unknownx{height}"
                    resolution_standard = "8K"
                elif height >= 2160:
                    resolution = "4K"
                    resolution_precise = f"unknownx{height}"
                    resolution_standard = "4K"
                elif height >= 1440:
                    resolution = f"{height}p"
                    resolution_precise = f"unknownx{height}"
                    resolution_standard = f"{height}p"
                else:
                    resolution = f"{height}p"
                    resolution_precise = f"unknownx{height}"
                    resolution_standard = f"{height}p"
            else:
                # Fallback to format note or resolution field
                resolution = fmt.get('resolution', 'unknown')
                resolution_precise = resolution
                resolution_standard = resolution
            
            # Determine if format has audio
            has_audio = (fmt.get('acodec') and 
                        fmt.get('acodec') != 'none' and 
                        fmt.get('acodec') != '')
            
            video_formats.append({
                'format_id': str(fmt['format_id']),
                'ext': fmt.get('ext', 'unknown'),
                'resolution': resolution,  # Standard resolution (e.g., "1080p")
                'resolution_precise': resolution_precise,  # Exact dimensions (e.g., "1920x1080")
                'resolution_standard': resolution_standard,  # Standard quality label
                'filesize': fmt.get('filesize', 0),
                'vcodec': fmt.get('vcodec', 'unknown'),
                'acodec': fmt.get('acodec', 'unknown'),
                'fps': fmt.get('fps', 0),
                'height': height,
                'width': width,
                'has_audio': has_audio,
                'tbr': fmt.get('tbr', 0),  # Total bitrate
                'vbr': fmt.get('vbr', 0),  # Video bitrate
                'abr': fmt.get('abr', 0),  # Audio bitrate
                'format_note': fmt.get('format_note', ''),
                'quality': fmt.get('quality', 0)
            })
        
        # Audio formats (audio-only streams)
        if (fmt.get('acodec') and fmt.get('acodec') != 'none' and 
            (not fmt.get('vcodec') or fmt.get('vcodec') == 'none')):
            
            # Get audio bitrate
            abr = fmt.get('abr', 0)
            if not abr:
                # Try to extract from format note
                format_note = fmt.get('format_note', '')
                if 'kbps' in format_note:
                    try:
                        abr = int(''.join(filter(str.isdigit, format_note)))
                    except ValueError:
                        abr = 0
            
            audio_formats.append({
                'format_id': str(fmt['format_id']),
                'ext': fmt.get('ext', 'unknown'),
                'filesize': fmt.get('filesize', 0),
                'acodec': fmt.get('acodec', 'unknown'),
                'abr': abr,
                'format_note': fmt.get('format_note', ''),
                'quality': fmt.get('quality', 0)
            })
        
        # Handle YouTube's special audio-only formats (ACodec: N/A but resolution: "audio only")
        elif (fmt.get('resolution') == 'audio only' and 
              (not fmt.get('vcodec') or fmt.get('vcodec') == 'none')):
            
            # Get audio bitrate
            abr = fmt.get('abr', 0)
            if not abr:
                # Try to extract from format note
                format_note = fmt.get('format_note', '')
                if 'kbps' in format_note:
                    try:
                        abr = int(''.join(filter(str.isdigit, format_note)))
                    except ValueError:
                        abr = 0
                
                # If still no bitrate, try to infer from format note
                if not abr and format_note:
                    format_note_lower = format_note.lower()
                    if 'low' in format_note_lower:
                        abr = 64  # Default low quality
                    elif 'high' in format_note_lower:
                        abr = 128  # Default high quality
                    elif 'medium' in format_note_lower:
                        abr = 96  # Default medium quality
                    elif 'default' in format_note_lower:
                        if 'low' in format_note_lower:
                            abr = 64
                        elif 'high' in format_note_lower:
                            abr = 128
                        else:
                            abr = 96  # Default medium quality
                    else:
                        abr = 96  # Default medium quality
                
                # If still no bitrate, try to extract from format_id patterns
                if not abr:
                    format_id = str(fmt.get('format_id', ''))
                    # YouTube often uses format IDs that indicate quality
                    if format_id in ['233', '234']:  # Common audio format IDs
                        if 'low' in format_note.lower():
                            abr = 64
                        elif 'high' in format_note.lower():
                            abr = 128
                        else:
                            abr = 96
            
            audio_formats.append({
                'format_id': str(fmt['format_id']),
                'ext': fmt.get('ext', 'unknown'),
                'filesize': fmt.get('filesize', 0),
                'acodec': 'unknown',  # YouTube doesn't provide codec info for these
                'abr': abr,
                'format_note': fmt.get('format_note', ''),
                'quality': fmt.get('quality', 0)
            })
    
    # Sort video formats by quality (height first, then fps, then bitrate)
    def video_quality_sort_key(fmt):
        height = fmt.get('height', 0)
        fps = fmt.get('fps', 0)
        tbr = fmt.get('tbr', 0)
        return (height, fps, tbr)
    
    video_formats.sort(key=video_quality_sort_key, reverse=True)
    
    # Sort audio formats by bitrate (prioritize formats with actual bitrate info)
    def audio_quality_sort_key(fmt):
        abr = fmt.get('abr', 0)
        # Prioritize formats with actual bitrate info
        if abr > 0:
            return (1, abr)  # Has bitrate info, sort by bitrate
        else:
            return (0, 0)  # No bitrate info, sort to end
    
    audio_formats.sort(key=audio_quality_sort_key, reverse=True)
    
    return video_formats, audio_formats

def find_best_audio_for_video(video_fmt, audio_formats):
    """Find the best audio format for a specific video format"""
    if not audio_formats:
        return None
    
    # Sort audio formats by bitrate (highest first) and prioritize formats with actual bitrate info
    sorted_audio = sorted(audio_formats, key=lambda x: (x.get('abr', 0) > 0, x.get('abr', 0)), reverse=True)
    
    if sorted_audio:
        return sorted_audio[0]  # This will be the highest bitrate audio with actual bitrate info
    
    return None

def find_best_video_audio_combination(video_formats, audio_formats, target_resolution=None):
    """Find the best video+audio combination for a given resolution"""
    if not video_formats or not audio_formats:
        return None, None
    
    # If no target resolution, use the highest quality video
    if not target_resolution:
        best_video = video_formats[0]
    else:
        # Find video with closest resolution match
        best_video = None
        min_diff = float('inf')
        
        # Handle different resolution formats
        target_height = None
        if isinstance(target_resolution, str):
            if target_resolution.endswith('p'):
                try:
                    target_height = int(target_resolution[:-1])
                except ValueError:
                    pass
            elif 'x' in target_resolution:
                try:
                    parts = target_resolution.split('x')
                    if len(parts) == 2:
                        target_height = int(parts[1])
                except ValueError:
                    pass
            elif target_resolution.upper() == '4K':
                target_height = 2160
            elif target_resolution.upper() == '8K':
                target_height = 4320
        else:
            target_height = target_resolution
        
        if target_height:
            for fmt in video_formats:
                if fmt.get('height'):
                    diff = abs(fmt['height'] - target_height)
                    if diff < min_diff:
                        min_diff = diff
                        best_video = fmt
                        
                    # Exact match takes priority
                    if fmt['height'] == target_height:
                        best_video = fmt
                        break
        else:
            # Fallback: try to match resolution string
            for fmt in video_formats:
                if fmt.get('resolution') == target_resolution:
                    best_video = fmt
                    break
    
    if not best_video:
        best_video = video_formats[0]  # Fallback to highest quality
    
    # Find best audio (highest bitrate, prioritizing formats with actual bitrate info)
    best_audio = None
    
    # Sort audio formats by bitrate (highest first) and prioritize formats with actual bitrate info
    sorted_audio = sorted(audio_formats, key=lambda x: (x.get('abr', 0) > 0, x.get('abr', 0)), reverse=True)
    
    if sorted_audio:
        best_audio = sorted_audio[0]  # This will be the highest bitrate audio with actual bitrate info
    
    return best_video, best_audio

def get_downloadable_video_formats(video_formats, audio_formats):
    """Get video formats that can be downloaded (with audio if available)"""
    downloadable_formats = []
    
    for video_fmt in video_formats:
        # Get the standard quality label (e.g., "1080p", "4K")
        quality_label = video_fmt.get('resolution_standard', video_fmt.get('resolution', 'unknown'))
        precise_resolution = video_fmt.get('resolution_precise', video_fmt.get('resolution', 'unknown'))
        
        # If video has audio, it's directly downloadable
        if video_fmt.get('has_audio'):
            downloadable_formats.append({
                'format_id': video_fmt['format_id'],
                'ext': video_fmt['ext'],
                'resolution': quality_label,  # Use standard quality label (e.g., "1080p")
                'resolution_precise': precise_resolution,  # Keep precise dimensions
                'filesize': video_fmt['filesize'],
                'vcodec': video_fmt['vcodec'],
                'acodec': video_fmt['acodec'],
                'fps': video_fmt['fps'],
                'height': video_fmt['height'],
                'width': video_fmt['width'],
                'download_type': 'single_format',
                'description': f"{quality_label} with audio ({precise_resolution})",
                'tbr': video_fmt.get('tbr', 0),
                'vbr': video_fmt.get('vbr', 0),
                'abr': video_fmt.get('abr', 0)
            })
        else:
            # Video-only format - find best audio companion
            best_audio = find_best_audio_for_video(video_fmt, audio_formats)
            if best_audio:
                audio_bitrate = best_audio.get('abr', 0)
                audio_quality = f"{audio_bitrate}kbps" if audio_bitrate > 0 else "unknown"
                downloadable_formats.append({
                    'format_id': f"{video_fmt['format_id']}+{best_audio['format_id']}",
                    'ext': 'mp4',  # Force MP4 output for merged streams
                    'resolution': quality_label,  # Use standard quality label
                    'resolution_precise': precise_resolution,  # Keep precise dimensions
                    'filesize': video_fmt['filesize'],
                    'vcodec': video_fmt['vcodec'],
                    'acodec': best_audio['acodec'],
                    'fps': video_fmt['fps'],
                    'height': video_fmt['height'],
                    'width': video_fmt['width'],
                    'download_type': 'combined_format',
                    'description': f"{quality_label} + {audio_quality} audio ({precise_resolution})",
                    'tbr': video_fmt.get('tbr', 0),
                    'vbr': video_fmt.get('vbr', 0),
                    'abr': audio_bitrate,  # Store the actual audio bitrate
                    'audio_format_id': best_audio['format_id'],  # Store audio format ID for merging
                    'audio_ext': best_audio['ext']  # Store audio extension
                })
    
    # Sort by quality (height first, then fps)
    downloadable_formats.sort(key=lambda x: (x.get('height', 0), x.get('fps', 0)), reverse=True)
    
    return downloadable_formats

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
        has_audio = "✅" if fmt.get('has_audio') else "❌"
        
        print(f"{i:2d}. {fmt['format_id']:>8} | {resolution:>12} | "
              f"{ext:>4} | {fps:>3}fps | {size_mb:>6.1f}MB | Audio: {has_audio}")
    
    print("\n🎵 AVAILABLE AUDIO FORMATS:")
    print("-" * 60)
    for i, fmt in enumerate(audio_formats, 1):
        size_mb = fmt.get('filesize', 0) / (1024 * 1024) if fmt.get('filesize') else 0
        abr = fmt.get('abr', 0) or 0  # Handle None values
        ext = fmt.get('ext', 'unknown')
        
        print(f"{i:2d}. {fmt['format_id']:>8} | {ext:>4} | "
              f"{abr:>4}kbps | {size_mb:>6.1f}MB")

def display_downloadable_formats(video_formats, audio_formats):
    """Display downloadable video formats (with audio combinations)"""
    downloadable_formats = get_downloadable_video_formats(video_formats, audio_formats)
    
    print("\n📥 DOWNLOADABLE VIDEO FORMATS:")
    print("-" * 80)
    for i, fmt in enumerate(downloadable_formats, 1):
        size_mb = fmt.get('filesize', 0) / (1024 * 1024) if fmt.get('filesize') else 0
        resolution = fmt.get('resolution', 'unknown')
        ext = fmt.get('ext', 'unknown')
        fps = fmt.get('fps', 0)
        download_type = fmt.get('download_type', 'unknown')
        description = fmt.get('description', '')
        
        print(f"{i:2d}. {fmt['format_id']:>12} | {resolution:>12} | "
              f"{ext:>4} | {fps:>3}fps | {size_mb:>6.1f}MB | {download_type:>15} | {description}")
    
    return downloadable_formats

def get_all_raw_formats(info):
    """Get all raw format information for debugging"""
    formats = info.get('formats', [])
    raw_formats = []
    
    for fmt in formats:
        raw_formats.append({
            'format_id': fmt.get('format_id', 'N/A'),
            'ext': fmt.get('ext', 'N/A'),
            'resolution': fmt.get('resolution', 'N/A'),
            'height': fmt.get('height', 'N/A'),
            'width': fmt.get('width', 'N/A'),
            'fps': fmt.get('fps', 'N/A'),
            'vcodec': fmt.get('vcodec', 'N/A'),
            'acodec': fmt.get('acodec', 'N/A'),
            'filesize': fmt.get('filesize', 'N/A'),
            'abr': fmt.get('abr', 'N/A'),
            'tbr': fmt.get('tbr', 'N/A'),  # Total bitrate
            'format_note': fmt.get('format_note', 'N/A'),
            'quality': fmt.get('quality', 'N/A'),
            'url': fmt.get('url', 'N/A')[:100] + '...' if fmt.get('url') else 'N/A'
        })
    
    return raw_formats

def display_all_raw_formats(info):
    """Display all raw formats from yt-dlp for debugging"""
    formats = info.get('formats', [])
    
    print("\n🔍 ALL RAW FORMATS (DEBUG):")
    print("-" * 100)
    print(f"{'ID':>6} | {'Ext':>4} | {'Resolution':>12} | {'FPS':>4} | {'VCodec':>15} | {'ACodec':>15} | {'Size':>8}")
    print("-" * 100)
    
    for fmt in formats:
        format_id = fmt.get('format_id', 'N/A')
        ext = fmt.get('ext', 'N/A')
        resolution = fmt.get('resolution', 'N/A')
        fps = fmt.get('fps', 'N/A')
        vcodec = fmt.get('vcodec', 'N/A')
        acodec = fmt.get('acodec', 'N/A')
        filesize = fmt.get('filesize', 0)
        
        if filesize:
            if filesize > 1024 * 1024 * 1024:  # GB
                size_str = f"{filesize / (1024 * 1024 * 1024):.1f}GB"
            elif filesize > 1024 * 1024:  # MB
                size_str = f"{filesize / (1024 * 1024):.1f}MB"
            elif filesize > 1024:  # KB
                size_str = f"{filesize / 1024:.1f}KB"
            else:
                size_str = f"{filesize}B"
        else:
            size_str = 'N/A'
        
        print(f"{format_id:>6} | {ext:>4} | {resolution:>12} | {fps:>4} | {vcodec:>15} | {acodec:>15} | {size_str:>8}")

def validate_format_availability(info, format_id):
    """Validate if the requested format is available"""
    formats = info.get('formats', [])
    available_format_ids = [str(fmt.get('format_id', '')) for fmt in formats if fmt.get('format_id')]
    
    # Check if it's a combined format (e.g., "137+140")
    if '+' in str(format_id):
        video_id, audio_id = str(format_id).split('+', 1)
        if video_id in available_format_ids and audio_id in available_format_ids:
            return True, available_format_ids
        else:
            return False, available_format_ids
    
    if str(format_id) not in available_format_ids:
        return False, available_format_ids
    return True, available_format_ids

def find_best_fallback_format(info, format_type="audio"):
    """Find the best fallback format when the requested format is unavailable"""
    video_formats, audio_formats = get_available_formats(info)
    
    if format_type == "audio":
        if audio_formats:
            return audio_formats[0]['format_id']
        # If no audio formats, try to find a video format with audio
        for fmt in info.get('formats', []):
            if (fmt.get('vcodec') and fmt.get('vcodec') != 'none' and 
                fmt.get('acodec') and fmt.get('acodec') != 'none'):
                return str(fmt.get('format_id'))
    else:  # video
        if video_formats:
            # Try to find a format with audio first
            for fmt in video_formats:
                if fmt.get('has_audio'):
                    return fmt['format_id']
            # If no formats with audio, return the highest quality video
            return video_formats[0]['format_id']
    
    return None

def find_best_format_for_quality(info, target_quality):
    """Find the best format for a specific quality (e.g., '1080p', '720p')"""
    video_formats, audio_formats = get_available_formats(info)
    
    if not video_formats:
        return None
    
    # Convert target quality to height for comparison
    target_height = None
    if isinstance(target_quality, str):
        if target_quality.endswith('p'):
            try:
                target_height = int(target_quality[:-1])
            except ValueError:
                pass
        elif 'x' in target_quality:
            try:
                parts = target_quality.split('x')
                if len(parts) == 2:
                    target_height = int(parts[1])
            except ValueError:
                pass
        elif target_quality.upper() == '4K':
            target_height = 2160
        elif target_quality.upper() == '8K':
            target_height = 4320
    
    # Find ALL video formats for the target quality
    matching_formats = []
    
    for fmt in video_formats:
        if fmt.get('height'):
            if target_height:
                if fmt['height'] == target_height:
                    matching_formats.append(fmt)
            else:
                # If no target height, check resolution string
                if fmt.get('resolution') == target_quality:
                    matching_formats.append(fmt)
    
    if not matching_formats:
        # No exact match, find closest
        if target_height:
            min_diff = float('inf')
            best_format = None
            for fmt in video_formats:
                if fmt.get('height'):
                    diff = abs(fmt['height'] - target_height)
                    if diff < min_diff:
                        min_diff = diff
                        best_format = fmt
            if best_format:
                matching_formats = [best_format]
    
    if not matching_formats:
        return None
    
    # Now find the BEST quality among matching formats
    # Sort by multiple quality factors: bitrate, fps, codec quality
    def quality_score(fmt):
        score = 0
        
        # Height score (exact match gets bonus)
        if fmt.get('height') == target_height:
            score += 10000
        
        # FPS score (higher is better)
        fps = fmt.get('fps', 0)
        if fps >= 60:
            score += 1000
        elif fps >= 30:
            score += 500
        elif fps >= 25:
            score += 250
        
        # Codec quality score
        vcodec = fmt.get('vcodec', '').lower()
        if 'av1' in vcodec:
            score += 800  # AV1 is highest quality
        elif 'vp9' in vcodec:
            score += 600  # VP9 is good quality
        elif 'h264' in vcodec or 'avc' in vcodec:
            score += 400  # H.264 is standard
        elif 'h265' in vcodec or 'hevc' in vcodec:
            score += 700  # H.265 is high quality
        
        # File size score (larger usually means better quality)
        filesize = fmt.get('filesize', 0)
        if filesize > 0:
            score += min(filesize // 1000000, 1000)  # Cap at 1000 points
        
        # Width score (wider is better for same height)
        width = fmt.get('width', 0)
        if width > 0:
            score += min(width // 100, 500)  # Cap at 500 points
        
        return score
    
    # Sort by quality score (highest first)
    matching_formats.sort(key=quality_score, reverse=True)
    
    # Get the best quality format
    best_video = matching_formats[0]
    
    print(f"🎯 Quality Analysis for {target_quality}:")
    print(f"   Found {len(matching_formats)} matching formats")
    print(f"   Best format: {best_video['format_id']} ({best_video['resolution']})")
    print(f"   Codec: {best_video.get('vcodec', 'N/A')}")
    print(f"   FPS: {best_video.get('fps', 'N/A')}")
    print(f"   Size: {best_video.get('filesize', 'N/A')} bytes")
    
    # If the best video doesn't have audio, combine it with the best audio
    if not best_video.get('has_audio') and audio_formats:
        best_audio = audio_formats[0]  # Highest quality audio
        combined_format = f"{best_video['format_id']}+{best_audio['format_id']}"
        print(f"   Audio: Adding {best_audio['format_id']} ({best_audio.get('abr', 'N/A')}kbps)")
        return combined_format
    else:
        print(f"   Audio: Built-in ({best_video.get('acodec', 'N/A')})")
        return best_video['format_id']

def analyze_quality_details(info, target_quality):
    """Analyze and display detailed quality information for a specific resolution"""
    video_formats, audio_formats = get_available_formats(info)
    
    print(f"\n🔍 QUALITY ANALYSIS FOR {target_quality.upper()}")
    print("=" * 60)
    
    # Convert target quality to height
    target_height = None
    if isinstance(target_quality, str):
        if target_quality.endswith('p'):
            try:
                target_height = int(target_quality[:-1])
            except ValueError:
                pass
        elif 'x' in target_quality:
            try:
                parts = target_quality.split('x')
                if len(parts) == 2:
                    target_height = int(parts[1])
            except ValueError:
                pass
        elif target_quality.upper() == '4K':
            target_height = 2160
        elif target_quality.upper() == '8K':
            target_height = 4320
    
    if not target_height:
        print(f"❌ Could not parse quality: {target_quality}")
        return
    
    # Find all formats matching this resolution
    matching_formats = []
    for fmt in video_formats:
        if fmt.get('height') == target_height:
            matching_formats.append(fmt)
    
    if not matching_formats:
        print(f"❌ No formats found for {target_quality}")
        return
    
    print(f"📊 Found {len(matching_formats)} format(s) for {target_quality}")
    print()
    
    # Sort by quality score
    def quality_score(fmt):
        score = 0
        
        # FPS score
        fps = fmt.get('fps', 0)
        if fps >= 60:
            score += 1000
        elif fps >= 30:
            score += 500
        elif fps >= 25:
            score += 250
        
        # Codec quality score
        vcodec = fmt.get('vcodec', '').lower()
        if 'av1' in vcodec:
            score += 800
        elif 'vp9' in vcodec:
            score += 600
        elif 'h265' in vcodec or 'hevc' in vcodec:
            score += 700
        elif 'h264' in vcodec or 'avc' in vcodec:
            score += 400
        
        # File size score
        filesize = fmt.get('filesize', 0)
        if filesize > 0:
            score += min(filesize // 1000000, 1000)
        
        return score
    
    matching_formats.sort(key=quality_score, reverse=True)
    
    # Display detailed information for each format
    for i, fmt in enumerate(matching_formats):
        print(f"🎯 Format #{i+1} (Quality Score: {quality_score(fmt)})")
        print(f"   ID: {fmt['format_id']}")
        print(f"   Resolution: {fmt['resolution']}")
        print(f"   Codec: {fmt.get('vcodec', 'N/A')}")
        print(f"   FPS: {fmt.get('fps', 'N/A')}")
        print(f"   Width x Height: {fmt.get('width', 'N/A')} x {fmt.get('height', 'N/A')}")
        print(f"   File Size: {fmt.get('filesize', 'N/A')} bytes")
        print(f"   Has Audio: {'Yes' if fmt.get('has_audio') else 'No'}")
        print(f"   Audio Codec: {fmt.get('acodec', 'N/A')}")
        print()
    
    # Show the best format
    best_format = matching_formats[0]
    print(f"🏆 RECOMMENDED FORMAT:")
    print(f"   {best_format['format_id']} - {best_format['resolution']}")
    print(f"   Codec: {best_format.get('vcodec', 'N/A')}")
    print(f"   FPS: {best_format.get('fps', 'N/A')}")
    print(f"   Quality: {'High' if quality_score(best_format) > 1000 else 'Medium' if quality_score(best_format) > 500 else 'Low'}")
    
    if not best_format.get('has_audio') and audio_formats:
        best_audio = audio_formats[0]
        print(f"   Audio: Will add {best_audio['format_id']} ({best_audio.get('abr', 'N/A')}kbps)")
    
    print("=" * 60)

def download_video(url, format_id, output_path="downloads", progress_callback=None):
    """Download video with specified format"""
    try:
        import yt_dlp
        
        # Ensure format_id is a string
        format_id = str(format_id)
        
        # Always get fresh video info right before downloading
        print("🔍 Getting fresh video information...")
        info = get_video_info(url)
        if not info:
            print("❌ Failed to get video info for format validation")
            return False
        
        # Check if format_id is a quality specification (e.g., "1080p", "720p")
        quality_formats = ['1080p', '720p', '480p', '360p', '240p', '144p', '4K', '8K']
        if format_id in quality_formats:
            print(f"🎯 Quality selected: {format_id}")
            print("   Finding best available format for this quality...")
            
            # Show detailed quality analysis
            analyze_quality_details(info, format_id)
            
            # Try to find the best possible quality
            format_id = find_best_format_for_quality(info, format_id)
            if not format_id:
                print("❌ No suitable format found for the selected quality")
                return False
            
            # Double-check if we can get better quality
            video_formats, audio_formats = get_available_formats(info)
            target_height = None
            if format_id.endswith('p'):
                try:
                    target_height = int(format_id[:-1])
                except ValueError:
                    pass
            
            if target_height:
                # Look for even better formats with the same height
                better_formats = []
                for fmt in video_formats:
                    if (fmt.get('height') == target_height and 
                        fmt.get('filesize', 0) > 0 and
                        fmt.get('fps', 0) >= 30):
                        better_formats.append(fmt)
                
                if better_formats:
                    # Sort by quality (file size, FPS, codec)
                    def enhanced_quality_score(fmt):
                        score = 0
                        score += fmt.get('filesize', 0) // 1000000  # File size in MB
                        score += fmt.get('fps', 0) * 10  # FPS bonus
                        
                        vcodec = fmt.get('vcodec', '').lower()
                        if 'av1' in vcodec:
                            score += 1000
                        elif 'vp9' in vcodec:
                            score += 800
                        elif 'h265' in vcodec or 'hevc' in vcodec:
                            score += 600
                        elif 'h264' in vcodec or 'avc' in vcodec:
                            score += 400
                        
                        return score
                    
                    better_formats.sort(key=enhanced_quality_score, reverse=True)
                    best_enhanced = better_formats[0]
                    
                    if enhanced_quality_score(best_enhanced) > enhanced_quality_score(video_formats[0]):
                        print(f"🚀 Found better quality format: {best_enhanced['format_id']}")
                        print(f"   Enhanced quality score: {enhanced_quality_score(best_enhanced)}")
                        format_id = best_enhanced['format_id']
            
            print(f"✅ Selected format: {format_id}")
        
        # Validate if the requested format is available
        is_available, available_formats = validate_format_availability(info, format_id)
        if not is_available:
            print(f"⚠️  Requested format {format_id} is not available!")
            print(f"   Available formats: {', '.join(available_formats[:10])}{'...' if len(available_formats) > 10 else ''}")
            
            # Try to find a fallback format
            fallback_format = find_best_fallback_format(info, "video")
            if fallback_format:
                print(f"🔄 Using fallback format: {fallback_format}")
                format_id = fallback_format
            else:
                print("❌ No suitable fallback format found")
                return False
        
        # Create output directory
        Path(output_path).mkdir(exist_ok=True)
        
        # Handle combined format IDs (e.g., "137+140" for video+audio)
        if '+' in format_id:
            print(f"🎬 Downloading combined format: {format_id}")
            print("   This will download video and audio separately and merge them.")
        else:
            # Check if this is a video-only format and needs audio
            video_formats, audio_formats = get_available_formats(info)
            selected_format = None
            
            # Find the selected format
            for fmt in video_formats:
                if str(fmt['format_id']) == format_id:
                    selected_format = fmt
                    break
            
            if selected_format and not selected_format.get('has_audio') and audio_formats:
                # This is a video-only format, automatically add best audio
                best_audio = audio_formats[0]  # Highest quality audio
                format_id = f"{format_id}+{best_audio['format_id']}"
                print(f"🎵 Auto-adding audio: {format_id}")
                print("   This ensures the downloaded video has audio.")
        
        # Use custom progress callback if provided, otherwise use default
        progress_hooks = [progress_callback] if progress_callback else [progress_hook]
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks,
            # Force merge of video and audio streams
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            # Ensure proper merging of separate streams
            'postprocessor_args': {
                'ffmpeg': ['-c:v', 'copy', '-c:a', 'copy'],
            },
            # Simple but effective headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            # Remove problematic options that can cause 403 errors
            'extractor_retries': 5,
            'fragment_retries': 5,
            'retries': 5,
            # Force IPv4 to avoid some network issues
            'source_address': '0.0.0.0',
            # Disable cookies to avoid decryption issues
            'cookiefile': None,
            'cookiesfrombrowser': None,
        }
        
        print(f"\n📥 Downloading video with format {format_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Video download completed!")
        
        # Verify the downloaded video has audio
        print("🔍 Verifying downloaded video...")
        # Find the downloaded file
        downloaded_files = [f for f in os.listdir(output_path) if f.endswith('.mp4')]
        if downloaded_files:
            # Sort by modification time to get the most recent
            downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_path, x)), reverse=True)
            latest_file = os.path.join(output_path, downloaded_files[0])
            verify_downloaded_video(latest_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        print(f"   URL: {url}")
        print(f"   Format ID: {format_id} (type: {type(format_id)})")
        print(f"   Output path: {output_path}")
        return False

def download_audio(url, format_id, output_path="downloads", progress_callback=None):
    """Download audio with specified format and convert to MP3"""
    try:
        import yt_dlp
        
        # Ensure format_id is a string
        format_id = str(format_id)
        
        # Always get fresh video info right before downloading
        print("🔍 Getting fresh video information...")
        info = get_video_info(url)
        if not info:
            print("❌ Failed to get video info for format validation")
            return False
        
        # Validate if the requested format is available
        is_available, available_formats = validate_format_availability(info, format_id)
        if not is_available:
            print(f"⚠️  Requested format {format_id} is not available!")
            print(f"   Available formats: {', '.join(available_formats[:10])}{'...' if len(available_formats) > 10 else ''}")
            
            # Try to find a fallback format
            fallback_format = find_best_fallback_format(info, "audio")
            if fallback_format:
                print(f"🔄 Using fallback format: {fallback_format}")
                format_id = fallback_format
            else:
                print("❌ No suitable fallback format found")
                return False
        
        # Create output directory
        Path(output_path).mkdir(exist_ok=True)
        
        # Use custom progress callback if provided, otherwise use default
        progress_hooks = [progress_callback] if progress_callback else [progress_hook]
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Simple but effective headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            # Remove problematic options that can cause 403 errors
            'extractor_retries': 5,
            'fragment_retries': 5,
            'retries': 5,
            # Force IPv4 to avoid some network issues
            'source_address': '0.0.0.0',
            # Disable cookies to avoid decryption issues
            'cookiefile': None,
            'cookiesfrombrowser': None,
        }
        
        print(f"\n🎵 Downloading audio with format {format_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Audio download completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        print(f"   URL: {url}")
        print(f"   Format ID: {format_id} (type: {type(format_id)})")
        print(f"   Output path: {output_path}")
        return False

def download_audio_raw(url, format_id, output_path="downloads", progress_callback=None):
    """Download audio with specified format without conversion"""
    try:
        import yt_dlp
        
        # Ensure format_id is a string
        format_id = str(format_id)
        
        # Always get fresh video info right before downloading
        print("🔍 Getting fresh video information...")
        info = get_video_info(url)
        if not info:
            print("❌ Failed to get video info for format validation")
            return False
        
        # Validate if the requested format is available
        is_available, available_formats = validate_format_availability(info, format_id)
        if not is_available:
            print(f"⚠️  Requested format {format_id} is not available!")
            print(f"   Available formats: {', '.join(available_formats[:10])}{'...' if len(available_formats) > 10 else ''}")
            
            # Try to find a fallback format
            fallback_format = find_best_fallback_format(info, "audio")
            if fallback_format:
                print(f"🔄 Using fallback format: {fallback_format}")
                format_id = fallback_format
            else:
                print("❌ No suitable fallback format found")
                return False
        
        # Create output directory
        Path(output_path).mkdir(exist_ok=True)
        
        # Use custom progress callback if provided, otherwise use default
        progress_hooks = [progress_callback] if progress_callback else [progress_hook]
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks,
            # Simple but effective headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            # Remove problematic options that can cause 403 errors
            'extractor_retries': 5,
            'fragment_retries': 5,
            'retries': 5,
            # Force IPv4 to avoid some network issues
            'source_address': '0.0.0.0',
            # Disable cookies to avoid decryption issues
            'cookiefile': None,
            'cookiesfrombrowser': None,
        }
        
        print(f"\n🎵 Downloading audio with format {format_id} (no conversion)...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Audio download completed! (Note: File is not converted to MP3)")
        print("💡 To convert to MP3, install FFmpeg and use the 'Audio' download type.")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        print(f"   URL: {url}")
        print(f"   Format ID: {format_id} (type: {type(format_id)})")
        print(f"   Output path: {output_path}")
        return False

def verify_downloaded_video(file_path):
    """Verify that the downloaded video has audio"""
    try:
        import subprocess
        
        # Check if FFmpeg is available
        if not check_ffmpeg():
            print("⚠️  FFmpeg not available - cannot verify audio")
            return True
        
        # Use FFmpeg to check audio streams
        cmd = ['ffmpeg', '-i', file_path, '-hide_banner', '-f', 'null', '-']
        
        # Use encoding='utf-8' and errors='ignore' to handle Unicode issues
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              encoding='utf-8', errors='ignore', timeout=30)
        
        if result.returncode == 0:
            # Check if there are audio streams
            stderr_output = result.stderr or ""
            if 'Audio:' in stderr_output:
                print("✅ Downloaded video has audio")
                return True
            else:
                print("❌ Downloaded video has NO audio!")
                print("   This usually means the video and audio streams weren't properly merged.")
                return False
        else:
            print("⚠️  Could not verify audio - FFmpeg error")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not verify audio: {e}")
        return True

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
                    print("\n💡 Alternative: You can still download audio without conversion")
                    print("   by selecting 'Video' download type and choosing a format with audio.")
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