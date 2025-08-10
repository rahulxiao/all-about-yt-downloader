#!/usr/bin/env python3
"""
YouTube Video and Audio Downloader - Frontend
Modern GUI interface for the YouTube downloader
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import os

# Import backend functions
from backend import get_video_info, get_available_formats, download_video, download_audio, check_ffmpeg

class ModernButton(tk.Button):
    """Custom modern button with hover effects"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=self.hover_color if hasattr(self, 'hover_color') else self.cget('bg'))
    
    def on_leave(self, e):
        self.configure(bg=self.original_color if hasattr(self, 'original_color') else self.cget('bg'))

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Downloader")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Modern color scheme
        self.colors = {
            'bg': '#0f0f23',           # Dark navy background
            'card_bg': '#1a1a2e',      # Card background
            'fg': '#ffffff',            # White text
            'accent': '#00d4aa',        # Teal accent
            'accent_hover': '#00b894',  # Darker teal for hover
            'button_bg': '#16213e',     # Button background
            'button_fg': '#ffffff',     # Button text
            'entry_bg': '#0f3460',      # Input field background
            'entry_fg': '#ffffff',      # Input field text
            'success': '#00b894',       # Success green
            'warning': '#f39c12',       # Warning orange
            'error': '#e74c3c',         # Error red
            'border': '#2d3748',        # Border color
            'text_bg': '#1a1a2e',      # Text area background
            'text_fg': '#e2e8f0'       # Text area text
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        self.download_type = tk.StringVar(value="video")
        self.progress_var = tk.StringVar(value="Ready to download")
        self.video_formats = []
        self.audio_formats = []
        self.current_info = None
        
        self.setup_ui()
        self.apply_modern_theme()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Input section
        self.create_input_section(main_container)
        
        # Action buttons
        self.create_action_buttons(main_container)
        
        # Progress section
        self.create_progress_section(main_container)
        
        # Content sections
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left side - Video info
        left_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.create_video_info_section(left_frame)
        
        # Right side - Format selection
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        self.create_format_section(right_frame)
    
    def create_header(self, parent):
        """Create the header section with title and subtitle"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title
        title_label = tk.Label(header_frame, 
                              text="🎬 YouTube Downloader", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg=self.colors['bg'], 
                              fg=self.colors['accent'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, 
                                 text="Download videos and audio in high quality", 
                                 font=('Segoe UI', 12), 
                                 bg=self.colors['bg'], 
                                 fg=self.colors['fg'])
        subtitle_label.pack(pady=(5, 0))
    
    def create_input_section(self, parent):
        """Create the input section with URL, type, and path"""
        input_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # URL input
        url_frame = tk.Frame(input_frame, bg=self.colors['card_bg'])
        url_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(url_frame, text="🔗 YouTube URL", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['fg']).pack(anchor=tk.W)
        
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, 
                           font=('Segoe UI', 11), 
                           bg=self.colors['entry_bg'], 
                           fg=self.colors['entry_fg'],
                           insertbackground=self.colors['accent'],
                           relief=tk.FLAT,
                           bd=0)
        url_entry.pack(fill=tk.X, pady=(8, 0), ipady=12)
        
        # Download type and output path in a row
        options_frame = tk.Frame(input_frame, bg=self.colors['card_bg'])
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Download type (left side)
        type_frame = tk.Frame(options_frame, bg=self.colors['card_bg'])
        type_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(type_frame, text="📁 Download Type", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['fg']).pack(anchor=tk.W)
        
        type_buttons_frame = tk.Frame(type_frame, bg=self.colors['card_bg'])
        type_buttons_frame.pack(anchor=tk.W, pady=(8, 0))
        
        # Custom radio buttons
        self.video_radio = tk.Radiobutton(type_buttons_frame, text="🎥 Video", 
                                         variable=self.download_type, value="video",
                                         bg=self.colors['card_bg'], fg=self.colors['fg'],
                                         selectcolor=self.colors['accent'],
                                         font=('Segoe UI', 10),
                                         activebackground=self.colors['card_bg'],
                                         activeforeground=self.colors['fg'])
        self.video_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        self.audio_radio = tk.Radiobutton(type_buttons_frame, text="🎵 Audio (MP3)", 
                                         variable=self.download_type, value="audio",
                                         bg=self.colors['card_bg'], fg=self.colors['fg'],
                                         selectcolor=self.colors['accent'],
                                         font=('Segoe UI', 10),
                                         activebackground=self.colors['card_bg'],
                                         activeforeground=self.colors['fg'])
        self.audio_radio.pack(side=tk.LEFT)
        
        # Output path (right side)
        path_frame = tk.Frame(options_frame, bg=self.colors['card_bg'])
        path_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        tk.Label(path_frame, text="📂 Output Directory", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['fg']).pack(anchor=tk.W)
        
        path_input_frame = tk.Frame(path_frame, bg=self.colors['card_bg'])
        path_input_frame.pack(fill=tk.X, pady=(8, 0))
        
        path_entry = tk.Entry(path_input_frame, textvariable=self.output_path_var,
                            font=('Segoe UI', 10),
                            bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                            insertbackground=self.colors['accent'],
                            relief=tk.FLAT, bd=0)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        browse_btn = ModernButton(path_input_frame, text="Browse", 
                                command=self.browse_output_path,
                                bg=self.colors['accent'], fg=self.colors['fg'],
                                font=('Segoe UI', 9, 'bold'),
                                relief=tk.FLAT, bd=0,
                                padx=15, pady=6)
        browse_btn.original_color = self.colors['accent']
        browse_btn.hover_color = self.colors['accent_hover']
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_action_buttons(self, parent):
        """Create the action buttons section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Get Info button
        self.info_button = ModernButton(button_frame, text="🔍 Get Video Info", 
                                      command=self.get_video_info,
                                      bg=self.colors['accent'], fg=self.colors['fg'],
                                      font=('Segoe UI', 12, 'bold'),
                                      relief=tk.FLAT, bd=0,
                                      padx=25, pady=12)
        self.info_button.original_color = self.colors['accent']
        self.info_button.hover_color = self.colors['accent_hover']
        self.info_button.pack(side=tk.LEFT)
        
        # Download button
        self.download_button = ModernButton(button_frame, text="📥 Download", 
                                          command=self.start_download,
                                          state='disabled',
                                          bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                          font=('Segoe UI', 12, 'bold'),
                                          relief=tk.FLAT, bd=0,
                                          padx=25, pady=12)
        self.download_button.pack(side=tk.LEFT, padx=(20, 0))
    
    def create_progress_section(self, parent):
        """Create the progress/status section"""
        progress_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0)
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        progress_inner = tk.Frame(progress_frame, bg=self.colors['card_bg'])
        progress_inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(progress_inner, text="📊 Status", 
                font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.progress_label = tk.Label(progress_inner, textvariable=self.progress_var,
                                     font=('Segoe UI', 10),
                                     bg=self.colors['card_bg'], 
                                     fg=self.colors['accent'])
        self.progress_label.pack(anchor=tk.W, pady=(8, 0))
    
    def create_video_info_section(self, parent):
        """Create the video information section"""
        info_frame = tk.LabelFrame(parent, text="📹 Video Information", 
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['card_bg'], fg=self.colors['accent'],
                                 bd=0, relief=tk.FLAT)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure label frame style
        info_frame.configure(bg=self.colors['card_bg'])
        for child in info_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=self.colors['card_bg'])
        
        self.info_text = ScrolledText(info_frame, 
                                    font=('Consolas', 10),
                                    bg=self.colors['text_bg'], fg=self.colors['text_fg'],
                                    insertbackground=self.colors['accent'],
                                    relief=tk.FLAT, bd=0,
                                    padx=15, pady=15)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_format_section(self, parent):
        """Create the format selection section"""
        format_frame = tk.LabelFrame(parent, text="🎯 Available Formats", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['card_bg'], fg=self.colors['accent'],
                                   bd=0, relief=tk.FLAT)
        format_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure label frame style
        format_frame.configure(bg=self.colors['card_bg'])
        for child in format_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=self.colors['card_bg'])
        
        # Quality selection section
        quality_frame = tk.Frame(format_frame, bg=self.colors['card_bg'])
        quality_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(quality_frame, text="🎚️ Quality Filter:", 
                font=('Segoe UI', 10, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['fg']).pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                         font=('Segoe UI', 10),
                                         state='readonly',
                                         width=20)
        self.quality_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.quality_combo.bind('<<ComboboxSelected>>', self._on_quality_change)
        
        # Help text for quality filter
        help_text = tk.Label(quality_frame, 
                            text="💡 Select a quality to filter formats, or choose 'All Qualities' to see everything",
                            font=('Segoe UI', 8), 
                            bg=self.colors['card_bg'], 
                            fg=self.colors['text_fg'])
        help_text.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create Treeview with custom style
        self.setup_treeview_style()
        
        self.format_tree = ttk.Treeview(format_frame, 
                                      columns=('ID', 'Quality', 'Format', 'Size', 'Details'), 
                                      show='headings', height=15)
        self.format_tree.heading('ID', text='Format ID')
        self.format_tree.heading('Quality', text='Quality')
        self.format_tree.heading('Format', text='Format')
        self.format_tree.heading('Size', text='Size')
        self.format_tree.heading('Details', text='Details')
        
        self.format_tree.column('ID', width=80, minwidth=80)
        self.format_tree.column('Quality', width=120, minwidth=120)
        self.format_tree.column('Format', width=80, minwidth=80)
        self.format_tree.column('Size', width=100, minwidth=100)
        self.format_tree.column('Details', width=150, minwidth=150)
        
        self.format_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Bind double-click event
        self.format_tree.bind('<Double-1>', self.on_format_double_click)
        
        # Download type change handler
        self.download_type.trace_add('write', self._on_download_type_change)
    
    def setup_treeview_style(self):
        """Setup custom treeview styling"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure treeview style
        style.configure("Treeview", 
                      background=self.colors['text_bg'],
                      foreground=self.colors['text_fg'],
                      fieldbackground=self.colors['text_bg'],
                      rowheight=30,
                      font=('Segoe UI', 9))
        
        # Configure treeview heading style
        style.configure("Treeview.Heading", 
                      background=self.colors['accent'],
                      foreground=self.colors['fg'],
                      relief="flat",
                      font=('Segoe UI', 9, 'bold'))
        
        # Configure treeview selection
        style.map("Treeview", 
                 background=[('selected', self.colors['accent'])])
    
    def apply_modern_theme(self):
        """Apply modern theme to all widgets"""
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure frame style
        style.configure('TFrame', background=self.colors['bg'])
        
        # Configure label style
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        
        # Configure button style
        style.configure('TButton', 
                      background=self.colors['button_bg'],
                      foreground=self.colors['button_fg'],
                      borderwidth=0,
                      focuscolor='none',
                      font=('Segoe UI', 10))
        
        style.map('TButton',
                 background=[('active', self.colors['accent'])])
        
        # Configure label frame style
        style.configure('TLabelframe', 
                      background=self.colors['card_bg'],
                      foreground=self.colors['accent'],
                      borderwidth=0,
                      relief='flat')
        
        style.configure('TLabelframe.Label', 
                      background=self.colors['card_bg'],
                      foreground=self.colors['accent'],
                      font=('Segoe UI', 12, 'bold'))
        
        # Configure combobox style
        style.configure('TCombobox', 
                      background=self.colors['entry_bg'],
                      foreground=self.colors['entry_fg'],
                      fieldbackground=self.colors['entry_bg'],
                      borderwidth=0,
                      relief='flat',
                      font=('Segoe UI', 10))
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.colors['entry_bg'])],
                 selectbackground=[('readonly', self.colors['accent'])],
                 selectforeground=[('readonly', self.colors['fg'])])
    
    def on_format_double_click(self, event):
        """Handle double-click on format selection"""
        selection = self.format_tree.selection()
        if selection:
            self.start_download()
    
    def browse_output_path(self):
        """Browse for output directory"""
        path = filedialog.askdirectory()
        if path:
            self.output_path_var.set(path)
    
    def get_video_info(self):
        """Get video information from URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        self.progress_var.set("🔍 Getting video information...")
        self.root.update()
        
        # Disable buttons during operation
        self.info_button.configure(state='disabled')
        self.download_button.configure(state='disabled')
        
        # Run in thread to prevent GUI freezing
        thread = threading.Thread(target=self._get_video_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _get_video_info_thread(self, url):
        """Thread function for getting video info"""
        try:
            info = get_video_info(url)
            self.root.after(0, self._update_video_info, info)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, self._enable_buttons)
    
    def _update_video_info(self, info):
        """Update video information display"""
        self.current_info = info
        
        # Update info text
        info_text = f"Title: {info.get('title', 'N/A')}\n"
        info_text += f"Duration: {info.get('duration', 'N/A')} seconds\n"
        info_text += f"Uploader: {info.get('uploader', 'N/A')}\n"
        info_text += f"View Count: {info.get('view_count', 'N/A'):,}\n"
        info_text += f"Upload Date: {info.get('upload_date', 'N/A')}\n"
        info_text += f"Description: {info.get('description', 'N/A')[:200]}...\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
        
        # Get available formats
        self.progress_var.set("📋 Getting available formats...")
        self.root.update()
        
        thread = threading.Thread(target=self._get_formats_thread, args=(info['webpage_url'],))
        thread.daemon = True
        thread.start()
    
    def _get_formats_thread(self, url):
        """Thread function for getting formats"""
        try:
            # Get all formats first
            info = get_video_info(url)
            if info:
                video_formats, audio_formats = get_available_formats(info)
                
                # Store formats for later use
                self.video_formats = video_formats
                self.audio_formats = audio_formats
                
                # Update quality dropdown
                self.root.after(0, self._update_quality_dropdown)
                
                # Show formats based on current selection
                if self.download_type.get() == "video":
                    formats = video_formats
                else:
                    formats = audio_formats
                
                self.root.after(0, self._update_format_tree, formats)
            else:
                self.root.after(0, self._show_error, "Could not get video information")
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_quality_dropdown(self):
        """Update quality dropdown based on download type"""
        if self.download_type.get() == "video":
            # Get unique resolutions for video
            resolutions = []
            for fmt in self.video_formats:
                res = fmt.get('resolution', 'unknown')
                if res not in resolutions and res != 'unknown':
                    resolutions.append(res)
            
            # Sort resolutions (highest first)
            resolutions.sort(key=lambda x: int(x.split('x')[1]) if 'x' in x else 0, reverse=True)
            
            # Update quality dropdown
            self.quality_var.set('')  # Clear current selection
            self.quality_combo['values'] = ['All Qualities'] + resolutions
            self.quality_combo.set('All Qualities')
        else:
            # Get unique bitrates for audio
            bitrates = []
            for fmt in self.audio_formats:
                abr = fmt.get('abr', 0)
                if abr > 0 and abr not in bitrates:
                    bitrates.append(abr)
            
            # Sort bitrates (highest first)
            bitrates.sort(reverse=True)
            
            # Update quality dropdown
            self.quality_var.set('')  # Clear current selection
            self.quality_combo['values'] = ['All Qualities'] + [f"{br} kbps" for br in bitrates]
            self.quality_combo.set('All Qualities')
    
    def _filter_formats_by_quality(self):
        """Filter formats based on selected quality"""
        if self.download_type.get() == "video":
            formats = self.video_formats
        else:
            formats = self.audio_formats
        
        selected_quality = self.quality_var.get()
        
        if selected_quality == 'All Qualities' or not selected_quality:
            return formats
        
        if self.download_type.get() == "video":
            # Filter by resolution
            filtered_formats = [fmt for fmt in formats if fmt.get('resolution') == selected_quality]
        else:
            # Filter by bitrate
            selected_bitrate = int(selected_quality.split()[0])  # Extract number from "128 kbps"
            filtered_formats = [fmt for fmt in formats if fmt.get('abr') == selected_bitrate]
        
        return filtered_formats
    
    def _on_quality_change(self, event=None):
        """Handle quality selection change"""
        filtered_formats = self._filter_formats_by_quality()
        self._update_format_tree(filtered_formats)
    
    def _on_download_type_change(self, event=None):
        """Handle download type change"""
        # Update quality dropdown
        self._update_quality_dropdown()
        
        # Update formats display
        filtered_formats = self._filter_formats_by_quality()
        self._update_format_tree(filtered_formats)
    
    def _update_format_tree(self, formats):
        """Update format tree with available formats"""
        # Clear existing items
        for item in self.format_tree.get_children():
            self.format_tree.delete(item)
        
        # Add new formats
        for fmt in formats:
            # Format quality information
            if self.download_type.get() == "video":
                quality = fmt.get('resolution', 'N/A')
                details = f"FPS: {fmt.get('fps', 'N/A')}"
                if fmt.get('width') and fmt.get('height'):
                    details += f" | {fmt.get('width')}x{fmt.get('height')}"
            else:
                quality = f"{fmt.get('abr', 'N/A')} kbps" if fmt.get('abr') else 'N/A'
                details = f"Codec: {fmt.get('acodec', 'N/A')}"
            
            # File size
            filesize = fmt.get('filesize', 0)
            if filesize:
                if filesize > 1024 * 1024 * 1024:  # GB
                    size_str = f"{filesize / (1024 * 1024 * 1024):.1f} GB"
                elif filesize > 1024 * 1024:  # MB
                    size_str = f"{filesize / (1024 * 1024):.1f} MB"
                elif filesize > 1024:  # KB
                    size_str = f"{filesize / 1024:.1f} KB"
                else:
                    size_str = f"{filesize} B"
            else:
                size_str = 'N/A'
            
            self.format_tree.insert('', 'end', values=(
                fmt.get('format_id', 'N/A'),
                quality,
                fmt.get('ext', 'N/A'),
                size_str,
                details
            ))
        
        self.progress_var.set(f"✅ Found {len(formats)} formats. Double-click to download or use Download button.")
        
        # Enable download button
        self.download_button.configure(state='normal', bg=self.colors['accent'])
        self.download_button.original_color = self.colors['accent']
        self.download_button.hover_color = self.colors['accent_hover']
    
    def start_download(self):
        """Start the download process"""
        selection = self.format_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a format to download")
            return
        
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        format_id = self.format_tree.item(selection[0])['values'][0]
        output_path = self.output_path_var.get()
        
        self.progress_var.set("📥 Starting download...")
        self.download_button.configure(state='disabled')
        
        # Run download in thread
        thread = threading.Thread(target=self._download_thread, args=(url, format_id, output_path))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url, format_id, output_path):
        """Thread function for downloading"""
        try:
            if self.download_type.get() == "video":
                download_video(url, format_id, output_path)
            else:
                # Check FFmpeg for audio downloads
                if not check_ffmpeg():
                    error_msg = ("FFmpeg is not installed or not in PATH!\n\n"
                               "FFmpeg is required for MP3 conversion.\n\n"
                               "Please install FFmpeg:\n"
                               "• Windows: Download from https://ffmpeg.org/download.html\n"
                               "• Windows (winget): winget install ffmpeg\n"
                               "• macOS: brew install ffmpeg\n"
                               "• Ubuntu/Debian: sudo apt install ffmpeg\n\n"
                               "After installation, restart your terminal/command prompt.")
                    self.root.after(0, self._show_error, error_msg)
                    return
                
                download_audio(url, format_id, output_path)
            
            self.root.after(0, self._download_complete)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _download_complete(self):
        """Handle download completion"""
        self.progress_var.set("✅ Download completed successfully!")
        self.download_button.configure(state='normal')
        messagebox.showinfo("Success", "Download completed successfully!")
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.progress_var.set(f"❌ Error: {error_msg}")
        self.download_button.configure(state='normal')
        messagebox.showerror("Error", error_msg)
    
    def _enable_buttons(self):
        """Re-enable buttons after operation"""
        self.info_button.configure(state='normal')
        self.download_button.configure(state='disabled')

def run_gui():
    """Launch the GUI application"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui() 