#!/usr/bin/env python3
"""
YouTube Downloader Launcher
Quick launch script for different modes
"""

import sys
from backend import check_dependencies, run_cli
from frontend import run_gui

def main():
    """Quick launcher for different modes"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode in ['gui', 'g', '--gui', '-g']:
            print("🚀 Launching GUI Mode...")
            run_gui()
        elif mode in ['cli', 'c', '--cli', '-c']:
            print("🚀 Launching CLI Mode...")
            run_cli()
        elif mode in ['help', 'h', '--help', '-h']:
            print("Usage:")
            print("  python launch.py          - Show main menu")
            print("  python launch.py gui      - Launch GUI directly")
            print("  python launch.py cli      - Launch CLI directly")
            print("  python launch.py help     - Show this help")
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Use 'python launch.py help' for usage information")
    else:
        # No arguments, show main menu
        from youtube_downloader import main
        main()

if __name__ == "__main__":
    main() 