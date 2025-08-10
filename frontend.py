#!/usr/bin/env python3
"""
YouTube Video and Audio Downloader - Frontend
Modern GUI interface for the YouTube downloader
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import sys
import re
import pyperclip  # For clipboard access
from backend import (get_video_info, get_available_formats, 
                     get_downloadable_video_formats, download_video, 
                     download_audio, download_audio_raw)

class ModernButton(tk.Button):
    """Custom modern button with hover effects"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=self.master.master.colors['accent'])
    
    def on_leave(self, e):
        self.configure(bg=self.master.master.colors['button_bg'])

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VideoHub Desktop Suite")
        
        # Initialize variables
        self.downloadable_video_formats = []
        self.audio_formats = []
        self.video_info = {}
        self.quality_var = tk.StringVar()
        self.download_type = tk.StringVar(value="video")
        self.last_clipboard_content = ""  # Track clipboard changes
        
        # Color scheme matching VideoHub design
        self.colors = {
            'bg': '#1a1a1a',           # Very dark grey/black background
            'card_bg': '#2d2d2d',      # Slightly lighter dark grey for cards
            'border': '#404040',       # Light grey borders
            'accent': '#00d4aa',       # Vibrant teal/cyan accent
            'text': '#ffffff',         # White text
            'text_secondary': '#cccccc', # Light grey text
            'button_bg': '#404040',    # Dark grey buttons
            'button_fg': '#ffffff',    # White button text
            'entry_bg': '#1a1a1a',    # Dark entry backgrounds
            'entry_fg': '#ffffff',     # White entry text
            'tree_bg': '#2d2d2d',     # Tree background
            'tree_fg': '#ffffff',     # Tree text
            'tree_selected': '#00d4aa', # Selected tree item
            'success': '#28a745',      # Green for success actions
            'warning': '#ffc107',      # Yellow for warnings
            'error': '#dc3545'        # Red for errors
        }
        
        # Apply theme first
        self.apply_modern_theme()
        
        # Setup UI
        self.setup_ui()
        
        # Initialize backend
        self.downloader = None  # We'll use functions directly
        
        # Center window
        self.center_window()
        
        # Start clipboard monitoring
        self._start_clipboard_monitoring()
    
    def center_window(self):
        """Center the window on screen with VideoHub dimensions"""
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Try to set icon
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def setup_ui(self):
        """Setup the main UI with VideoHub design"""
        # Main container with dark background
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_videohub_header(main_container)
        
        # Content area with left and right columns
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left column (Input and Progress)
        left_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Right column (Video Info and Formats)
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        # Create sections
        self.create_input_section(left_frame)
        self.create_action_buttons(left_frame)
        self.create_progress_section(left_frame)
        
        self.create_video_info_section(right_frame)
        self.create_flexible_format_section(right_frame)
    
    def create_videohub_header(self, parent):
        """Create VideoHub header with branding"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side - VideoHub branding
        branding_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        branding_frame.pack(side=tk.LEFT)
        
        # Main title
        title_label = tk.Label(branding_frame, 
                              text="VideoHub", 
                              font=('Segoe UI', 32, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['text'])
        title_label.pack(anchor=tk.W)
        
        # Subtitle
        subtitle_label = tk.Label(branding_frame,
                                 text="Desktop Suite",
                                 font=('Segoe UI', 14),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(anchor=tk.W)
        
        # Right side - Settings button
        settings_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        settings_frame.pack(side=tk.RIGHT)
        
        settings_button = tk.Button(settings_frame,
                                   text="⚙",
                                   font=('Segoe UI', 16),
                                   bg=self.colors['button_bg'],
                                   fg=self.colors['text'],
                                   relief=tk.FLAT,
                                   bd=0,
                                   padx=12,
                                   pady=8,
                                   cursor='hand2')
        settings_button.pack()
        
        # Hover effect
        settings_button.bind('<Enter>', lambda e: settings_button.configure(bg=self.colors['accent']))
        settings_button.bind('<Leave>', lambda e: settings_button.configure(bg=self.colors['button_bg']))
    
    def create_input_section(self, parent):
        """Create input section with URL entry and paste from clipboard"""
        input_frame = tk.Frame(parent, bg=self.colors['bg'])
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Title
        title_label = tk.Label(input_frame, text="Video URL", 
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['bg'], fg=self.colors['text'])
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # URL input frame
        url_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        url_frame.pack(fill=tk.X)
        
        # URL entry
        url_entry_frame = tk.Frame(url_frame, bg=self.colors['entry_bg'], padx=15, pady=12)
        url_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.url_entry = tk.Entry(url_entry_frame, font=('Segoe UI', 11),
                                 bg=self.colors['entry_bg'], fg=self.colors['text'],
                                 insertbackground=self.colors['text'],
                                 relief=tk.FLAT, bd=0)
        self.url_entry.pack(fill=tk.BOTH, expand=True)
        self.url_entry.insert(0, "Enter a YouTube URL")
        self.url_entry.bind('<FocusIn>', self._on_url_focus_in)
        self.url_entry.bind('<FocusOut>', self._on_url_focus_out)
        self.url_entry.bind('<Return>', lambda e: self.get_video_info())
        self.url_entry.bind('<Control-v>', self._manual_paste_from_clipboard)
        
        # Auto-paste from clipboard when URL field gains focus
        self.url_entry.bind('<Button-1>', self._check_clipboard_on_click)
        
        # Output path frame
        path_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        path_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Output path label
        path_label = tk.Label(path_frame, text="Save to", 
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['bg'], fg=self.colors['text'])
        path_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Path input frame
        path_input_frame = tk.Frame(path_frame, bg=self.colors['bg'])
        path_input_frame.pack(fill=tk.X)
        
        # Path entry
        path_entry_frame = tk.Frame(path_input_frame, bg=self.colors['entry_bg'], padx=15, pady=12)
        path_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.path_entry = tk.Entry(path_entry_frame, font=('Segoe UI', 11),
                                  bg=self.colors['entry_bg'], fg=self.colors['text'],
                                  insertbackground=self.colors['text'],
                                  relief=tk.FLAT, bd=0)
        self.path_entry.pack(fill=tk.BOTH, expand=True)
        self.path_entry.insert(0, os.getcwd())
        
        # Browse button
        browse_button = tk.Button(path_input_frame, text="Browse", 
                                 font=('Segoe UI', 10),
                                 bg=self.colors['button_bg'], fg=self.colors['text'],
                                 relief=tk.FLAT, bd=0, padx=15, pady=12,
                                 cursor='hand2',
                                 command=self.browse_output_path)
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_action_buttons(self, parent):
        """Create action buttons section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Download type selection
        type_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        type_label = tk.Label(type_frame, text="Download Type", 
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['bg'], fg=self.colors['text'])
        type_label.pack(anchor=tk.W, pady=(0, 8))
        
        self.type_combo = ttk.Combobox(type_frame, textvariable=self.download_type,
                                       values=["video", "audio"], state="readonly",
                                       font=('Segoe UI', 11), width=15)
        self.type_combo.pack(anchor=tk.W)
        self.type_combo.bind('<<ComboboxSelected>>', self._on_download_type_change)
        
        # Action buttons
        action_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        action_frame.pack(fill=tk.X)
        
        # Fetch button
        self.fetch_button = tk.Button(action_frame, text="🔍 Fetch Video Info", 
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=self.colors['accent'], fg=self.colors['text'],
                                     relief=tk.FLAT, bd=0, padx=25, pady=12,
                                     cursor='hand2', command=self.get_video_info)
        self.fetch_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Download button
        self.download_button = tk.Button(action_frame, text="⬇️ Download", 
                                        font=('Segoe UI', 11, 'bold'),
                                        bg=self.colors['success'], fg=self.colors['text'],
                                        relief=tk.FLAT, bd=0, padx=25, pady=12,
                                        cursor='hand2', command=self.start_download,
                                        state=tk.DISABLED)
        self.download_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Refresh button
        self.refresh_button = tk.Button(action_frame, text="🔄 Refresh", 
                                       font=('Segoe UI', 11),
                                       bg=self.colors['button_bg'], fg=self.colors['text'],
                                       relief=tk.FLAT, bd=0, padx=20, pady=12,
                                       cursor='hand2', command=self._refresh_formats,
                                       state=tk.DISABLED)
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Analyze button
        self.analyze_button = tk.Button(action_frame, text="📊 Analyze", 
                                        font=('Segoe UI', 11),
                                        bg=self.colors['button_bg'], fg=self.colors['text'],
                                        relief=tk.FLAT, bd=0, padx=20, pady=12,
                                        cursor='hand2', command=self.analyze_quality,
                                        state=tk.DISABLED)
        self.analyze_button.pack(side=tk.LEFT)
    
    def create_progress_section(self, parent):
        """Create progress section with VideoHub styling"""
        # Card container
        progress_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        progress_frame.pack(fill=tk.BOTH, expand=True)
        progress_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Progress label
        progress_label = tk.Label(progress_frame, text="Progress", font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['card_bg'], fg=self.colors['text'])
        progress_label.pack(anchor=tk.W, pady=(20, 10), padx=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(anchor=tk.W, pady=(0, 15), padx=20, fill=tk.X)
        
        # Progress display (terminal-like)
        progress_display_frame = tk.Frame(progress_frame, bg=self.colors['card_bg'])
        progress_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.progress_display = tk.Text(progress_display_frame, 
                                       bg=self.colors['entry_bg'], fg=self.colors['text'],
                                       font=('Consolas', 10), relief=tk.FLAT, bd=0,
                                       highlightthickness=1, highlightbackground=self.colors['border'],
                                       wrap=tk.WORD, height=8)
        self.progress_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for progress display
        progress_scrollbar = ttk.Scrollbar(progress_display_frame, orient=tk.VERTICAL,
                                          command=self.progress_display.yview)
        progress_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.progress_display.configure(yscrollcommand=progress_scrollbar.set)
        
        # Initial message
        self.progress_display.insert(tk.END, "Ready to download...\n")
        self.progress_display.config(state=tk.DISABLED)
    
    def create_video_info_section(self, parent):
        """Create video info section with VideoHub styling"""
        # Card container
        info_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        info_frame.pack(fill=tk.X, pady=(0, 20))
        info_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Info label
        info_label = tk.Label(info_frame, text="Video Info", font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['card_bg'], fg=self.colors['text'])
        info_label.pack(anchor=tk.W, pady=(20, 15), padx=20)
        
        # Video info labels
        self.title_label = tk.Label(info_frame, text="Title: No video selected",
                                   font=('Segoe UI', 11), bg=self.colors['card_bg'],
                                   fg=self.colors['text'], wraplength=300, justify=tk.LEFT)
        self.title_label.pack(anchor=tk.W, pady=(0, 8), padx=20)
        
        self.duration_label = tk.Label(info_frame, text="Duration: --",
                                      font=('Segoe UI', 11), bg=self.colors['card_bg'],
                                      fg=self.colors['text'])
        self.duration_label.pack(anchor=tk.W, pady=(0, 8), padx=20)
        
        self.views_label = tk.Label(info_frame, text="Views: --",
                                   font=('Segoe UI', 11), bg=self.colors['card_bg'],
                                   fg=self.colors['text'])
        self.views_label.pack(anchor=tk.W, pady=(0, 8), padx=20)
        
        self.channel_label = tk.Label(info_frame, text="Channel: --",
                                     font=('Segoe UI', 11), bg=self.colors['card_bg'],
                                     fg=self.colors['text'])
        self.channel_label.pack(anchor=tk.W, pady=(0, 20), padx=20)
    
    def create_flexible_format_section(self, parent):
        """Create flexible format section with VideoHub styling"""
        # Card container
        format_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        format_frame.pack(fill=tk.BOTH, expand=True)
        format_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Format label
        format_label = tk.Label(format_frame, text="Formats", font=('Segoe UI', 12, 'bold'),
                               bg=self.colors['card_bg'], fg=self.colors['text'])
        format_label.pack(anchor=tk.W, pady=(20, 15), padx=20)
        
        # Quality selection
        quality_label = tk.Label(format_frame, text="Quality", font=('Segoe UI', 11),
                                bg=self.colors['card_bg'], fg=self.colors['text'])
        quality_label.pack(anchor=tk.W, pady=(0, 8), padx=20)
        
        self.quality_combo = ttk.Combobox(format_frame, textvariable=self.quality_var,
                                         font=('Segoe UI', 11), width=30, state="readonly")
        self.quality_combo.pack(anchor=tk.W, pady=(0, 15), padx=20)
        self.quality_combo.set("Select quality after fetching")
        
        # Available formats label
        formats_label = tk.Label(format_frame, text="Available Formats", font=('Segoe UI', 11),
                                bg=self.colors['card_bg'], fg=self.colors['text'])
        formats_label.pack(anchor=tk.W, pady=(0, 10), padx=20)
        
        # Create flexible format tree
        self.create_format_tree(format_frame)
        
        # Debug button
        debug_button = tk.Button(format_frame, text="Debug Formats",
                                font=('Segoe UI', 9),
                                bg=self.colors['button_bg'], fg=self.colors['text'],
                                relief=tk.FLAT, bd=0, padx=15, pady=6,
                                cursor='hand2', command=self._show_debug_formats)
        debug_button.pack(anchor=tk.W, pady=(15, 20), padx=20)
        
        # Hover effect
        debug_button.bind('<Enter>', lambda e: debug_button.configure(bg=self.colors['accent']))
        debug_button.bind('<Leave>', lambda e: debug_button.configure(bg=self.colors['button_bg']))
    
    def create_format_tree(self, parent):
        """Create flexible format tree with better organization"""
        # Tree container with scrollbars
        tree_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create treeview with more flexible columns
        self.format_tree = ttk.Treeview(tree_frame, columns=("ID", "Quality", "Resolution", "Size", "Codec", "FPS", "Details"),
                                       show="headings", height=10)
        
        # Configure columns with flexible widths
        self.format_tree.heading("ID", text="ID")
        self.format_tree.heading("Quality", text="Quality")
        self.format_tree.heading("Resolution", text="Resolution")
        self.format_tree.heading("Size", text="Size")
        self.format_tree.heading("Codec", text="Codec")
        self.format_tree.heading("FPS", text="FPS")
        self.format_tree.heading("Details", text="Details")
        
        # Set column widths (more flexible)
        self.format_tree.column("ID", width=60, minwidth=50)
        self.format_tree.column("Quality", width=80, minwidth=70)
        self.format_tree.column("Resolution", width=100, minwidth=80)
        self.format_tree.column("Size", width=80, minwidth=60)
        self.format_tree.column("Codec", width=100, minwidth=80)
        self.format_tree.column("FPS", width=60, minwidth=50)
        self.format_tree.column("Details", width=200, minwidth=150)
        
        # Scrollbars
        tree_v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.format_tree.yview)
        tree_h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.format_tree.xview)
        self.format_tree.configure(yscrollcommand=tree_v_scrollbar.set, xscrollcommand=tree_h_scrollbar.set)
        
        # Pack tree and scrollbars
        self.format_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click event
        self.format_tree.bind('<Double-1>', self.on_format_double_click)
        
        # Setup tree styling
        self.setup_treeview_style()
        
        # Initial message
        self.format_tree.insert("", "end", values=("", "", "", "", "", "", "No formats loaded"))
        
        # Bind quality change
        self.quality_combo.bind('<<ComboboxSelected>>', self._on_quality_change)
        self.download_type.trace('w', self._on_download_type_change)
    
    def setup_treeview_style(self):
        """Setup modern treeview styling"""
        # Configure modern treeview colors
        self.format_tree.tag_configure('even', background=self.colors['card_bg'])
        self.format_tree.tag_configure('odd', background=self.colors['entry_bg'])
        self.format_tree.tag_configure('selected', background=self.colors['tree_selected'])
        
        # Bind hover effects
        self.format_tree.bind('<Motion>', self._on_treeview_hover)
        
        # Configure alternating row colors
        self.format_tree.tag_configure('alternate', background=self.colors['entry_bg'])
    
    def _on_treeview_hover(self, event):
        """Handle treeview hover effects"""
        item = self.format_tree.identify_row(event.y)
        if item:
            self.format_tree.selection_set(item)
        else:
            self.format_tree.selection_remove(self.format_tree.selection())
    
    def apply_modern_theme(self):
        """Apply VideoHub modern theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progress bar
        style.configure('Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['entry_bg'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
        # Configure treeview
        style.configure('Treeview',
                       background=self.colors['tree_bg'],
                       foreground=self.colors['tree_fg'],
                       fieldbackground=self.colors['tree_bg'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure('Treeview.Heading',
                       background=self.colors['button_bg'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure combobox
        style.configure('TCombobox',
                       background=self.colors['entry_bg'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['entry_bg'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['text'])
        
        # Configure scrollbar
        style.configure('Vertical.TScrollbar',
                       background=self.colors['button_bg'],
                       troughcolor=self.colors['entry_bg'],
                       borderwidth=0,
                       arrowcolor=self.colors['text'],
                       width=12)
        
        style.configure('Horizontal.TScrollbar',
                       background=self.colors['button_bg'],
                       troughcolor=self.colors['entry_bg'],
                       borderwidth=0,
                       arrowcolor=self.colors['text'],
                       width=12)
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
    
    def on_format_double_click(self, event):
        """Handle format double-click for quick download"""
        selection = self.format_tree.selection()
        if selection:
            item = self.format_tree.item(selection[0])
            format_id = item['values'][0]
            if format_id:
                self.start_download()
    
    def browse_output_path(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)
    
    def get_video_info(self):
        """Get video information"""
        url = self.url_entry.get().strip()
        if not url or url == "Enter a YouTube URL":
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        # Clear previous data
        self._reset_progress()
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, "🔍 Fetching video information...\n")
        self.progress_display.config(state=tk.DISABLED)
        
        # Disable buttons during fetch
        self.fetch_button.config(state=tk.DISABLED)
        
        # Start fetch in thread
        thread = threading.Thread(target=self._get_video_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _get_video_info_thread(self, url):
        """Thread for fetching video information"""
        try:
            # Get video info
            info = get_video_info(url)
            if not info:
                self.root.after(0, lambda: self._show_error("Failed to get video information"))
                return
            
            # Get available formats
            video_formats, audio_formats = get_available_formats(info)
            downloadable_formats = get_downloadable_video_formats(video_formats, audio_formats)
            if not video_formats and not audio_formats:
                self.root.after(0, lambda: self._show_error("No formats available for this video"))
                return
            
            # Update GUI on main thread
            self.root.after(0, lambda: self._update_formats_data(
                video_formats, audio_formats, downloadable_formats, info))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, lambda: self.fetch_button.config(state=tk.NORMAL))
    
    def _update_formats_data(self, video_formats, audio_formats, downloadable_formats, info):
        """Update all format data and GUI elements"""
        # Store formats
        self.video_formats = video_formats
        self.audio_formats = audio_formats
        self.downloadable_video_formats = downloadable_formats
        self.video_info = info
        
        # Update video info
        self._update_video_info()
        
        # Update quality dropdown
        self._update_quality_dropdown()
        
        # Update format tree
        self._update_format_tree(downloadable_formats)
        
        # Enable buttons
        self._enable_buttons()
        
        # Update progress
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, "✅ Video information loaded successfully!\n")
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
    
    def _update_video_info(self):
        """Update video information display"""
        if self.video_info:
            title = self.video_info.get('title', 'Unknown')
            duration = self.video_info.get('duration', 0)
            views = self.video_info.get('view_count', 0)
            channel = self.video_info.get('uploader', 'Unknown')
            
            # Format duration
            if duration:
                minutes = duration // 60
                seconds = duration % 60
                duration_str = f"{minutes}:{seconds:02d}"
            else:
                duration_str = "--"
            
            # Format views
            if views:
                if views >= 1000000:
                    views_str = f"{views/1000000:.1f}M"
                elif views >= 1000:
                    views_str = f"{views/1000:.1f}K"
                else:
                    views_str = str(views)
            else:
                views_str = "--"
            
            self.title_label.config(text=f"Title: {title}")
            self.duration_label.config(text=f"Duration: {duration_str}")
            self.views_label.config(text=f"Views: {views_str}")
            self.channel_label.config(text=f"Channel: {channel}")
    
    def _update_quality_dropdown(self):
        """Update quality dropdown with available qualities"""
        if not hasattr(self, 'downloadable_video_formats') or not self.downloadable_video_formats:
            self.quality_combo['values'] = ["No formats available"]
            self.quality_combo.set("No formats available")
            return
        
        # Get unique qualities
        qualities = set()
        for fmt in self.downloadable_video_formats:
            if fmt.get('resolution_standard') and fmt['resolution_standard']:
                qualities.add(fmt['resolution_standard'])
        
        if not qualities:
            qualities = set()
            for fmt in self.downloadable_video_formats:
                if fmt.get('resolution_precise') and fmt['resolution_precise']:
                    qualities.add(fmt['resolution_precise'])
        
        if qualities:
            # Sort qualities logically
            def sort_resolution(res):
                if 'p' in res:
                    try:
                        return int(res.replace('p', ''))
                    except:
                        return 0
                elif 'k' in res:
                    try:
                        return int(res.replace('k', ''))
                    except:
                        return 0
                return 0
            
            sorted_qualities = sorted(qualities, key=sort_resolution, reverse=True)
            self.quality_combo['values'] = sorted_qualities
            self.quality_combo.set(sorted_qualities[0])
        else:
            self.quality_combo['values'] = ["No quality info"]
            self.quality_combo.set("No quality info")
    
    def _filter_formats_by_quality(self):
        """Filter formats by selected quality"""
        if not hasattr(self, 'downloadable_video_formats') or not self.downloadable_video_formats:
            return []
        
        selected_quality = self.quality_var.get()
        if not selected_quality or selected_quality in ["Select quality after fetching", "No formats available", "No quality info"]:
            return self.downloadable_video_formats
        
        filtered_formats = []
        for fmt in self.downloadable_video_formats:
            if self._quality_matches(selected_quality, fmt):
                filtered_formats.append(fmt)
        
        return filtered_formats
    
    def _quality_matches(self, selected_quality, format_obj):
        """Check if format quality matches selected quality"""
        if format_obj.get('resolution_standard') and format_obj['resolution_standard']:
            return format_obj['resolution_standard'] == selected_quality
        elif format_obj.get('resolution_precise') and format_obj['resolution_precise']:
            return format_obj['resolution_precise'] == selected_quality
        return False
    
    def _on_quality_change(self, *args):
        """Handle quality filter change"""
        # Only filter if we have formats loaded
        if (self.download_type.get() == "video" and 
            hasattr(self, 'downloadable_video_formats') and self.downloadable_video_formats):
            filtered_formats = self._filter_formats_by_quality()
            self._update_format_tree(filtered_formats)
        elif (self.download_type.get() == "audio" and 
              hasattr(self, 'audio_formats') and self.audio_formats):
            # For audio, show all audio formats
            self._update_format_tree(self.audio_formats)
    
    def _on_download_type_change(self, *args):
        """Handle download type change"""
        # Only update if we have formats loaded
        if hasattr(self, 'downloadable_video_formats') and self.downloadable_video_formats:
            if self.download_type.get() == "video":
                self._update_format_tree(self.downloadable_video_formats)
                self._update_quality_dropdown()
            else:
                if hasattr(self, 'audio_formats') and self.audio_formats:
                    self._update_format_tree(self.audio_formats)
                    self.quality_combo['values'] = ["All audio formats"]
                    self.quality_combo.set("All audio formats")
    
    def _update_format_tree(self, formats):
        """Update format tree with flexible display"""
        # Clear existing items
        for item in self.format_tree.get_children():
            self.format_tree.delete(item)
        
        if not formats:
            self.format_tree.insert("", "end", values=("", "", "", "", "", "", "No formats available"))
            return
        
        # Add formats with alternating row colors
        for i, fmt in enumerate(formats):
            # Get format details
            format_id = fmt.get('format_id', 'N/A')
            quality = fmt.get('resolution_standard', fmt.get('resolution_precise', 'N/A'))
            resolution = fmt.get('resolution_precise', 'N/A')
            filesize = fmt.get('filesize', 0)
            codec = fmt.get('vcodec', fmt.get('acodec', 'N/A'))
            fps = fmt.get('fps', 'N/A')
            
            # Format filesize
            if filesize:
                if filesize >= 1024*1024:
                    size_str = f"{filesize/(1024*1024):.1f}MB"
                elif filesize >= 1024:
                    size_str = f"{filesize/1024:.1f}KB"
                else:
                    size_str = f"{filesize}B"
            else:
                size_str = "N/A"
            
            # Format FPS
            if fps and fps != 'N/A':
                fps_str = f"{fps}fps"
            else:
                fps_str = "N/A"
            
            # Get additional details
            details = []
            if fmt.get('abr'):
                details.append(f"Audio: {fmt['abr']}kbps")
            if fmt.get('vbr'):
                details.append(f"Video: {fmt['vbr']}kbps")
            if fmt.get('ext'):
                details.append(f"Ext: {fmt['ext']}")
            
            details_str = " | ".join(details) if details else "Standard quality"
            
            # Insert with alternating colors
            tag = 'even' if i % 2 == 0 else 'odd'
            self.format_tree.insert("", "end", values=(
                format_id, quality, resolution, size_str, codec, fps_str, details_str
            ), tags=(tag,))
    
    def _get_resolution_height(self, resolution):
        """Extract height from resolution string"""
        if not resolution:
            return 0
        
        # Handle common resolution formats
        if 'x' in resolution:
            try:
                return int(resolution.split('x')[1])
            except:
                pass
        
        # Handle p/k suffixes
        if 'p' in resolution:
            try:
                return int(resolution.replace('p', ''))
            except:
                pass
        elif 'k' in resolution:
            try:
                return int(resolution.replace('k', ''))
            except:
                pass
        
        return 0
    
    def start_download(self):
        """Start the download process"""
        url = self.url_entry.get().strip()
        if not url or url == "Enter a YouTube URL":
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        # Get selected format
        selection = self.format_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a format to download")
            return
        
        item = self.format_tree.item(selection[0])
        format_id = item['values'][0]
        
        if not format_id or format_id == "N/A":
            messagebox.showerror("Error", "Please select a valid format")
            return
        
        # Get output path
        output_path = self.path_entry.get().strip()
        if not output_path:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        # Clear progress and start download
        self._reset_progress()
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, f"🎬 Downloading format: {format_id}\n")
        
        if '+' in format_id:
            self.progress_display.insert(tk.END, "   This will download video and audio separately and merge them.\n")
        
        self.progress_display.config(state=tk.DISABLED)
        
        # Disable buttons during download
        self._disable_buttons()
        
        # Start download in thread
        thread = threading.Thread(target=self._download_thread, args=(url, format_id, output_path))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url, format_id, output_path):
        """Thread for downloading video"""
        try:
            if self.download_type.get() == "audio":
                download_audio(url, format_id, output_path, self._progress_callback)
            else:
                download_video(url, format_id, output_path, self._progress_callback)
            
            self.root.after(0, self._download_complete)
            
        except Exception as e:
            error_msg = f"Download error: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, self._enable_buttons)
    
    def _show_format_error(self, url, format_id):
        """Show format-specific error with retry option"""
        error_msg = f"Error downloading format {format_id}.\n\n"
        error_msg += "This might be due to:\n"
        error_msg += "• Format restrictions\n"
        error_msg += "• Age restrictions\n"
        error_msg += "• Regional limitations\n"
        error_msg += "• YouTube policy changes\n\n"
        error_msg += "Try:\n"
        error_msg += "• Refreshing formats\n"
        error_msg += "• Selecting a different quality\n"
        error_msg += "• Using a different format type"
        
        result = messagebox.askyesno("Format Error", 
                                   error_msg + "\n\nWould you like to refresh formats?")
        if result:
            self._refresh_formats()
    
    def _download_complete(self):
        """Handle download completion"""
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, "✅ Download completed successfully!\n")
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
        
        # Reset progress bar
        self.progress_bar['value'] = 0
        
        # Show completion message
        messagebox.showinfo("Download Complete", "Video downloaded successfully!")
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, f"❌ {error_msg}\n")
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
        
        # Reset progress bar
        self.progress_bar['value'] = 0
        
        # Show error message box
        messagebox.showerror("Error", error_msg)
    
    def _enable_buttons(self):
        """Enable all buttons"""
        self.download_button.config(state=tk.NORMAL)
        self.refresh_button.config(state=tk.NORMAL)
        self.analyze_button.config(state=tk.NORMAL)
    
    def _disable_buttons(self):
        """Disable all buttons during download"""
        self.download_button.config(state=tk.DISABLED)
        self.refresh_button.config(state=tk.DISABLED)
        self.analyze_button.config(state=tk.DISABLED)
        self.fetch_button.config(state=tk.DISABLED)
    
    def _update_progress(self, message):
        """Update progress display"""
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, f"{message}\n")
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
    
    def _progress_callback(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            # Update progress bar
            if 'total_bytes' in d and d['total_bytes']:
                percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.root.after(0, lambda: self._update_progress_bar(percentage))
            
            # Update progress details
            details = f"[{d.get('_percent_str', '0%')}] "
            details += f"Downloading... "
            
            if 'speed' in d and d['speed']:
                speed_mb = d['speed'] / (1024 * 1024)
                details += f"Speed: {speed_mb:.1f} MB/s "
            
            if 'eta' in d and d['eta']:
                details += f"ETA: {d['eta']}s"
            
            self.root.after(0, lambda: self._update_progress_details(details))
            
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self._show_processing_status("Processing downloaded file..."))
    
    def _update_progress_bar(self, percentage):
        """Update progress bar value"""
        self.progress_bar['value'] = percentage
    
    def _update_progress_details(self, details):
        """Update progress details in terminal display"""
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, f"{details}\n")
        
        # Keep only last 50 lines for performance
        lines = self.progress_display.get('1.0', tk.END).split('\n')
        if len(lines) > 50:
            self.progress_display.delete('1.0', f"{len(lines)-50}.0")
        
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
    
    def _show_processing_status(self, message):
        """Show processing status"""
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, f"⚙️ {message}\n")
        self.progress_display.config(state=tk.DISABLED)
        self.progress_display.see(tk.END)
    
    def _reset_progress(self):
        """Reset progress display and bar"""
        self.progress_bar['value'] = 0
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.delete('1.0', tk.END)
        self.progress_display.config(state=tk.DISABLED)
    
    def _refresh_formats(self):
        """Refresh available formats"""
        url = self.url_entry.get().strip()
        if not url or url == "Enter a YouTube URL":
            messagebox.showerror("Error", "Please enter a valid YouTube URL first")
            return
        
        # Clear previous data
        self._reset_progress()
        self.progress_display.config(state=tk.NORMAL)
        self.progress_display.insert(tk.END, "🔍 Getting fresh video information...\n")
        self.progress_display.config(state=tk.DISABLED)
        
        # Disable buttons during refresh
        self.refresh_button.config(state=tk.DISABLED)
        
        # Start refresh in thread
        thread = threading.Thread(target=self._refresh_formats_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _refresh_formats_thread(self, url):
        """Thread for refreshing formats"""
        try:
            # Get fresh video info first
            info = get_video_info(url)
            if not info:
                self.root.after(0, lambda: self._show_error("Failed to refresh video information"))
                return
            
            # Get fresh formats
            video_formats, audio_formats = get_available_formats(info)
            downloadable_formats = get_downloadable_video_formats(video_formats, audio_formats)
            
            # Update GUI on main thread
            self.root.after(0, lambda: self._update_formats_data(
                video_formats, audio_formats, downloadable_formats, info))
            
        except Exception as e:
            error_msg = f"Refresh error: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, lambda: self.refresh_button.config(state=tk.NORMAL))
    
    def _show_debug_formats(self):
        """Show debug information for formats"""
        if not hasattr(self, 'video_formats') or not self.video_formats:
            messagebox.showinfo("Debug", "No video formats loaded yet")
            return
        
        # Create debug window
        debug_window = tk.Toplevel(self.root)
        debug_window.title("Debug: Available Formats")
        debug_window.geometry("800x600")
        debug_window.configure(bg=self.colors['bg'])
        
        # Debug content
        debug_frame = tk.Frame(debug_window, bg=self.colors['bg'])
        debug_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(debug_frame, text="Debug: Available Formats", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg'], fg=self.colors['text'])
        title_label.pack(pady=(0, 20))
        
        # Raw formats display
        raw_label = tk.Label(debug_frame, text="Raw Format Data:", 
                            font=('Segoe UI', 12, 'bold'),
                            bg=self.colors['bg'], fg=self.colors['text'])
        raw_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Raw text area
        raw_text = scrolledtext.ScrolledText(debug_frame, height=15, width=80,
                                            bg=self.colors['entry_bg'], fg=self.colors['text'],
                                            font=('Consolas', 9))
        raw_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Populate raw data
        raw_data = "Video Formats:\n"
        raw_data += "=" * 50 + "\n"
        for fmt in self.video_formats[:20]:  # Show first 20
            raw_data += f"Format ID: {fmt.get('format_id', 'N/A')}\n"
            raw_data += f"  Resolution: {fmt.get('resolution', 'N/A')}\n"
            raw_data += f"  Filesize: {fmt.get('filesize', 'N/A')}\n"
            raw_data += f"  Codec: {fmt.get('vcodec', 'N/A')}\n"
            raw_data += f"  FPS: {fmt.get('fps', 'N/A')}\n"
            raw_data += f"  Ext: {fmt.get('ext', 'N/A')}\n"
            raw_data += "-" * 30 + "\n"
        
        raw_data += "\nAudio Formats:\n"
        raw_data += "=" * 50 + "\n"
        for fmt in self.audio_formats[:10]:  # Show first 10
            raw_data += f"Format ID: {fmt.get('format_id', 'N/A')}\n"
            raw_data += f"  Filesize: {fmt.get('filesize', 'N/A')}\n"
            raw_data += f"  Codec: {fmt.get('acodec', 'N/A')}\n"
            raw_data += f"  Bitrate: {fmt.get('abr', 'N/A')}kbps\n"
            raw_data += f"  Ext: {fmt.get('ext', 'N/A')}\n"
            raw_data += "-" * 30 + "\n"
        
        raw_text.insert(tk.END, raw_data)
        raw_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(debug_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        copy_button = tk.Button(button_frame, text="Copy to Clipboard",
                               font=('Segoe UI', 11),
                               bg=self.colors['accent'], fg=self.colors['text'],
                               relief=tk.FLAT, bd=0, padx=20, pady=8,
                               cursor='hand2',
                               command=lambda: self._copy_debug_to_clipboard(raw_data, ""))
        copy_button.pack(side=tk.LEFT, padx=(0, 10))
        
        close_button = tk.Button(button_frame, text="Close",
                                font=('Segoe UI', 11),
                                bg=self.colors['button_bg'], fg=self.colors['text'],
                                relief=tk.FLAT, bd=0, padx=20, pady=8,
                                cursor='hand2',
                                command=debug_window.destroy)
        close_button.pack(side=tk.LEFT)
    
    def _copy_debug_to_clipboard(self, raw_text, processed_text):
        """Copy debug text to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(raw_text)
            messagebox.showinfo("Copied", "Debug information copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def _show_ffmpeg_warning(self, url, format_id, output_path):
        """Show FFmpeg warning for combined formats"""
        warning_msg = f"Downloading combined format {format_id} requires FFmpeg for merging.\n\n"
        warning_msg += "This will:\n"
        warning_msg += "1. Download video and audio separately\n"
        warning_msg += "2. Use FFmpeg to merge them\n"
        warning_msg += "3. Verify the final file\n\n"
        warning_msg += "Make sure FFmpeg is installed and accessible.\n\n"
        warning_msg += "Continue with download?"
        
        result = messagebox.askyesno("FFmpeg Required", warning_msg)
        if result:
            # Start download with FFmpeg
            thread = threading.Thread(target=self._download_thread, args=(url, format_id, output_path))
            thread.daemon = True
            thread.start()
    
    def _download_raw_audio(self, url, format_id, output_path):
        """Download raw audio format"""
        try:
            download_audio_raw(url, format_id, output_path, self._progress_callback)
            self.root.after(0, self._download_complete)
        except Exception as e:
            error_msg = f"Audio download error: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))
    
    def _raw_audio_download_thread(self, url, format_id, output_path):
        """Thread for raw audio download"""
        try:
            self._download_raw_audio(url, format_id, output_path)
        except Exception as e:
            error_msg = f"Audio download error: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, self._enable_buttons)
    
    def analyze_quality(self):
        """Analyze video quality and provide recommendations"""
        if not hasattr(self, 'downloadable_video_formats') or not self.downloadable_video_formats:
            messagebox.showinfo("Quality Analysis", "No formats loaded yet. Please fetch video info first.")
            return
        
        # Create analysis window
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Quality Analysis")
        analysis_window.geometry("700x500")
        analysis_window.configure(bg=self.colors['bg'])
        
        # Analysis content
        analysis_frame = tk.Frame(analysis_window, bg=self.colors['bg'])
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(analysis_frame, text="Quality Analysis & Recommendations", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg'], fg=self.colors['text'])
        title_label.pack(pady=(0, 20))
        
        # Analysis text
        analysis_text = scrolledtext.ScrolledText(analysis_frame, height=20, width=70,
                                                bg=self.colors['entry_bg'], fg=self.colors['text'],
                                                font=('Segoe UI', 10))
        analysis_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Perform analysis
        def analyze_thread():
            try:
                analysis = self._perform_quality_analysis()
                analysis_window.after(0, lambda: analysis_text.insert(tk.END, analysis))
                analysis_window.after(0, lambda: analysis_text.config(state=tk.DISABLED))
            except Exception as e:
                error_msg = f"Analysis error: {str(e)}"
                analysis_window.after(0, lambda: analysis_text.insert(tk.END, error_msg))
        
        # Start analysis
        analysis_text.insert(tk.END, "Analyzing video quality...\n\n")
        thread = threading.Thread(target=analyze_thread)
        thread.daemon = True
        thread.start()
        
        # Close button
        close_button = tk.Button(analysis_frame, text="Close",
                                font=('Segoe UI', 11),
                                bg=self.colors['accent'], fg=self.colors['text'],
                                relief=tk.FLAT, bd=0, padx=20, pady=8,
                                cursor='hand2',
                                command=analysis_window.destroy)
        close_button.pack()
    
    def _perform_quality_analysis(self):
        """Perform quality analysis and return recommendations"""
        analysis = "📊 Quality Analysis Report\n"
        analysis += "=" * 40 + "\n\n"
        
        if not hasattr(self, 'downloadable_video_formats'):
            return "No formats available for analysis."
        
        formats = self.downloadable_video_formats
        
        # Resolution analysis
        resolutions = {}
        for fmt in formats:
            res = fmt.get('resolution_standard', fmt.get('resolution_precise', 'Unknown'))
            if res not in resolutions:
                resolutions[res] = 0
            resolutions[res] += 1
        
        analysis += "📺 Resolution Distribution:\n"
        for res, count in sorted(resolutions.items(), key=lambda x: self._get_resolution_height(x[0]), reverse=True):
            analysis += f"  {res}: {count} format(s)\n"
        
        # Quality recommendations
        analysis += "\n💡 Quality Recommendations:\n"
        
        # Find best quality options
        high_quality = [f for f in formats if f.get('resolution_standard') and 
                       '1080' in str(f['resolution_standard']) or '1440' in str(f['resolution_standard'])]
        medium_quality = [f for f in formats if f.get('resolution_standard') and 
                         '720' in str(f['resolution_standard'])]
        low_quality = [f for f in formats if f.get('resolution_standard') and 
                       '480' in str(f['resolution_standard']) or '360' in str(f['resolution_standard'])]
        
        if high_quality:
            analysis += "  🎯 High Quality (1080p+): Available\n"
            best_high = max(high_quality, key=lambda x: x.get('filesize', 0))
            analysis += f"    Recommended: {best_high.get('resolution_standard', 'N/A')} "
            analysis += f"(ID: {best_high.get('format_id', 'N/A')})\n"
        
        if medium_quality:
            analysis += "  📱 Medium Quality (720p): Available\n"
            best_medium = max(medium_quality, key=lambda x: x.get('filesize', 0))
            analysis += f"    Recommended: {best_medium.get('resolution_standard', 'N/A')} "
            analysis += f"(ID: {best_medium.get('format_id', 'N/A')})\n"
        
        if low_quality:
            analysis += "  ⚡ Low Quality (480p/360p): Available\n"
            best_low = max(low_quality, key=lambda x: x.get('filesize', 0))
            analysis += f"    Recommended: {best_low.get('resolution_standard', 'N/A')} "
            analysis += f"(ID: {best_low.get('format_id', 'N/A')})\n"
        
        # Audio analysis
        audio_formats = [f for f in formats if f.get('audio_format_id') and f['audio_format_id']]
        if audio_formats:
            analysis += "\n🎵 Audio Quality:\n"
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
            analysis += f"  Best audio bitrate: {best_audio.get('abr', 'N/A')}kbps\n"
        
        analysis += "\n🔍 Tips:\n"
        analysis += "  • Higher resolution = Better quality but larger file size\n"
        analysis += "  • Combined formats (video+audio) provide best quality\n"
        analysis += "  • Audio-only formats are smaller and faster to download\n"
        analysis += "  • Use 'Analyze' button for detailed format information\n"
        
        return analysis

    def _on_url_focus_in(self, event):
        """Clear URL entry when it gains focus and check clipboard"""
        if self.url_entry.get() == "Enter a YouTube URL":
            self.url_entry.delete(0, tk.END)
        
        # Check clipboard for YouTube URL when focusing
        self._check_clipboard_on_focus()
    
    def _on_url_focus_out(self, event):
        """Restore default text if URL entry is empty"""
        if not self.url_entry.get():
            self.url_entry.insert(0, "Enter a YouTube URL")
    
    def _is_youtube_url(self, url):
        """Check if the given URL is a valid YouTube URL"""
        if not url:
            return False
        
        # Convert to lowercase for easier matching
        url_lower = url.lower().strip()
        
        # Check for various YouTube URL patterns
        youtube_patterns = [
            'youtube.com',
            'youtu.be',
            'm.youtube.com',
            'www.youtube.com'
        ]
        
        return any(pattern in url_lower for pattern in youtube_patterns)
    
    def _check_clipboard_on_focus(self):
        """Check clipboard when URL field gains focus"""
        try:
            clipboard_url = pyperclip.paste()
            if clipboard_url and self._is_youtube_url(clipboard_url):
                # Only paste if it's different from what's already there
                current_url = self.url_entry.get()
                if current_url != clipboard_url and current_url != "Enter a YouTube URL":
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, clipboard_url)
                    
                    # Show notification
                    self._show_clipboard_notification(f"Pasted from clipboard: {clipboard_url[:50]}...")
        except Exception as e:
            # Silently handle clipboard errors
            pass
    
    def _check_clipboard_on_click(self, event):
        """Check if clipboard contains a YouTube URL and paste it"""
        clipboard_url = pyperclip.paste()
        if clipboard_url and self._is_youtube_url(clipboard_url):
            # Only paste if it's different from what's already there
            current_url = self.url_entry.get()
            if current_url != clipboard_url and current_url != "Enter a YouTube URL":
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_url)
        elif self.url_entry.get() == "Enter a YouTube URL":
            self.url_entry.delete(0, tk.END)
    
    def _manual_paste_from_clipboard(self, event):
        """Handle manual Ctrl+V paste from clipboard"""
        try:
            clipboard_url = pyperclip.paste()
            if clipboard_url and self._is_youtube_url(clipboard_url):
                # Only paste if it's different from what's already there
                current_url = self.url_entry.get()
                if current_url != clipboard_url and current_url != "Enter a YouTube URL":
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, clipboard_url)
                    
                    # Show notification
                    self._show_clipboard_notification(f"Pasted from clipboard: {clipboard_url[:50]}...")
        except Exception as e:
            # Silently handle clipboard errors
            pass
    
    def _start_clipboard_monitoring(self):
        """Start monitoring clipboard for YouTube URLs"""
        self._check_clipboard_periodically()
    
    def _check_clipboard_periodically(self):
        """Check clipboard every 2 seconds for new YouTube URLs"""
        try:
            current_clipboard = pyperclip.paste()
            
            # Check if clipboard contains a new YouTube URL
            if (current_clipboard and 
                self._is_youtube_url(current_clipboard) and 
                current_clipboard != self.last_clipboard_content):
                
                # Update last clipboard content
                self.last_clipboard_content = current_clipboard
                
                # Auto-paste if URL field is empty or has placeholder
                current_url = self.url_entry.get()
                if current_url == "" or current_url == "Enter a YouTube URL":
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, current_clipboard)
                    
                    # Show a subtle notification
                    self._show_clipboard_notification(f"Auto-pasted: {current_clipboard[:50]}...")
            
        except Exception as e:
            # Silently handle clipboard errors
            pass
        
        # Schedule next check in 2 seconds
        self.root.after(2000, self._check_clipboard_periodically)
    
    def _show_clipboard_notification(self, message):
        """Show a subtle notification about clipboard auto-paste"""
        # Create a temporary notification label
        notification = tk.Label(self.root, text=message, 
                               bg=self.colors['accent'], fg=self.colors['text'],
                               font=('Segoe UI', 9), padx=10, pady=5)
        
        # Position it near the URL field
        notification.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # Remove after 3 seconds
        self.root.after(3000, notification.destroy)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 