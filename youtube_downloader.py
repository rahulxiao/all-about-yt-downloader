#!/usr/bin/env python3
"""
YouTube Video and Audio Downloader - Main Entry Point
Main menu for choosing between CLI and GUI modes
"""

# Import backend and frontend modules
from backend import check_dependencies, run_cli
from frontend import run_gui

def main():
    """Main function with mode selection"""
    print("🎬 YouTube Video and Audio Downloader")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    while True:
        print("\nChoose Interface Mode:")
        print("1. 🖥️  GUI Mode (Graphical Interface)")
        print("2. 💻 CLI Mode (Command Line Interface)")
        print("3. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n🚀 Starting GUI Mode...")
            run_gui()
        elif choice == '2':
            print("\n🚀 Starting CLI Mode...")
            run_cli()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 