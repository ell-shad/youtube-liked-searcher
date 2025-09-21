#!/usr/bin/env python3
"""
YouTube Liked Videos Search Tool
A simple GUI application to search through your YouTube liked videos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import webbrowser
from datetime import datetime
import re
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    print("Please install required packages:")
    print("pip install google-api-python-client google-auth google-auth-oauthlib")
    exit(1)

class YouTubeLikedSearcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Liked Videos Searcher")
        self.root.geometry("1200x800")  # Increased default size for description column
        
        # YouTube API setup
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.CLIENT_SECRETS_FILE = 'client_secret.json'  # You need to download this
        self.credentials_file = 'token.json'
        
        self.youtube = None
        self.liked_videos = []
        self.filtered_videos = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI components"""
        # Create menu bar
        self.create_menu_bar()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Make treeview column expandable
        main_frame.rowconfigure(3, weight=1)     # Make treeview row expandable
        
        # Authentication section
        auth_frame = ttk.LabelFrame(main_frame, text="Authentication", padding="5")
        auth_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.auth_button = ttk.Button(auth_frame, text="Authenticate & Load Liked Videos", 
                                     command=self.authenticate_and_load)
        self.auth_button.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(auth_frame, text="Not authenticated")
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Search section
        search_frame = ttk.LabelFrame(main_frame, text="Search", padding="5")
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_videos)
        self.search_button.grid(row=0, column=2)
        
        # Results info
        self.results_label = ttk.Label(main_frame, text="No videos loaded")
        self.results_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Results list with description column
        columns = ('title', 'channel', 'date', 'description')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Define headings with sorting functionality
        self.tree.heading('title', text='Title', command=lambda: self.sort_column('title', False))
        self.tree.heading('channel', text='Channel', command=lambda: self.sort_column('channel', False))
        self.tree.heading('date', text='Date Liked', command=lambda: self.sort_column('date', False))
        self.tree.heading('description', text='Description', command=lambda: self.sort_column('description', False))
        
        # Configure column widths (resizable)
        self.tree.column('title', width=300, minwidth=200)
        self.tree.column('channel', width=150, minwidth=100)
        self.tree.column('date', width=120, minwidth=100)
        self.tree.column('description', width=250, minwidth=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))
        
        # Make sure scrollbar column doesn't expand
        main_frame.columnconfigure(1, weight=0)
        
        # Bind double-click to open video
        self.tree.bind('<Double-1>', self.open_video)
        # Bind single-click to show details
        self.tree.bind('<<TreeviewSelect>>', self.on_video_select)
        
        # Details pane (fixed size, non-resizable)
        details_frame = ttk.LabelFrame(main_frame, text="Video Details", padding="5")
        details_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        
        # Video details labels and content
        # Title
        ttk.Label(details_frame, text="Title:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
        self.detail_title = ttk.Label(details_frame, text="", wraplength=800, justify=tk.LEFT)
        self.detail_title.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Channel and Date in same row
        info_frame = ttk.Frame(details_frame)
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Channel:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.detail_channel = ttk.Label(info_frame, text="")
        self.detail_channel.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(info_frame, text="Date:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=2, sticky=tk.W)
        self.detail_date = ttk.Label(info_frame, text="")
        self.detail_date.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # URL
        ttk.Label(details_frame, text="URL:", font=('TkDefaultFont', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(0, 2))
        self.detail_url = ttk.Label(details_frame, text="", foreground="blue", cursor="hand2")
        self.detail_url.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.detail_url.bind("<Button-1>", self.open_url_from_details)
        
        # Description
        ttk.Label(details_frame, text="Description:", font=('TkDefaultFont', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(0, 2))
        
        # Scrollable text widget for description (fixed height)
        desc_frame = ttk.Frame(details_frame)
        desc_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        desc_frame.columnconfigure(0, weight=1)
        
        self.detail_description = tk.Text(desc_frame, height=6, wrap=tk.WORD, font=('TkDefaultFont', 9))
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient=tk.VERTICAL, command=self.detail_description.yview)
        self.detail_description.configure(yscrollcommand=desc_scrollbar.set)
        
        self.detail_description.grid(row=0, column=0, sticky=(tk.W, tk.E))
        desc_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize with empty details
        self.clear_details()
        
        # Bottom buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Open Selected Video", 
                  command=self.open_video).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Refresh Videos", 
                  command=self.load_liked_videos).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export Results", 
                  command=self.export_results).pack(side=tk.LEFT)
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="Load Videos from Cache", command=self.load_from_cache_menu)
        file_menu.add_command(label="Refresh Videos from YouTube", command=self.load_liked_videos)
        file_menu.add_separator()
        file_menu.add_command(label="Export Current Results...", command=self.export_results)
        file_menu.add_command(label="Export All Videos...", command=self.export_all_videos)
        file_menu.add_separator()
        file_menu.add_command(label="Clear Cache", command=self.clear_cache)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="How to Use", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-r>', lambda e: self.load_liked_videos())
        self.root.bind('<Control-e>', lambda e: self.export_results())
        self.root.bind('<F1>', lambda e: self.show_help())
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_from_cache_menu(self):
        """Load videos from cache via menu"""
        if self.load_cache():
            messagebox.showinfo("Cache Loaded", f"Successfully loaded {len(self.liked_videos)} videos from cache.")
        else:
            messagebox.showwarning("Cache Not Found", "No cache file found. Please authenticate and load videos from YouTube first.")
    
    def export_all_videos(self):
        """Export all liked videos (not just current search results)"""
        if not self.liked_videos:
            messagebox.showwarning("Warning", "No videos to export. Please load videos first.")
            return
        
        try:
            filename = f"youtube_all_liked_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.liked_videos, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Export Complete", f"All {len(self.liked_videos)} liked videos exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def clear_cache(self):
        """Clear the local cache file"""
        try:
            if os.path.exists('liked_videos_cache.json'):
                result = messagebox.askyesno("Clear Cache", 
                    "Are you sure you want to clear the cache?\n\n"
                    "This will delete the locally stored video data. "
                    "You'll need to reload from YouTube next time.")
                
                if result:
                    os.remove('liked_videos_cache.json')
                    messagebox.showinfo("Cache Cleared", "Cache file deleted successfully.")
            else:
                messagebox.showinfo("No Cache", "No cache file found to clear.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """Keyboard Shortcuts:

Main Functions:
  Ctrl+Q          Quit application
  Ctrl+R          Refresh videos from YouTube
  Ctrl+E          Export current search results
  F1              Show help

Navigation:
  Double-click    Open video in browser
  Single-click    Show video details
  Type in search  Real-time search

Tips:
  • Click column headers to sort
  • Use search to filter, then sort results
  • All columns are resizable by dragging borders
  • Details pane shows full video information"""
        
        # Create a custom shortcuts dialog
        shortcuts_window = tk.Toplevel(self.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("480x350")
        shortcuts_window.transient(self.root)
        shortcuts_window.grab_set()
        shortcuts_window.resizable(False, False)
        
        # Center the window
        shortcuts_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Create main frame with padding
        main_frame = ttk.Frame(shortcuts_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add text with proper font
        text_label = tk.Label(main_frame, text=shortcuts_text, justify=tk.LEFT, 
                             font=('Courier', 10), anchor=tk.NW)
        text_label.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Close", command=shortcuts_window.destroy).pack(anchor=tk.E)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """YouTube Liked Videos Searcher - Help

Getting Started:
1. Click 'Authenticate & Load Liked Videos'
2. Sign in to your Google account
3. Wait for videos to load (may take a few minutes)
4. Start searching and exploring!

Features:
• Real-time search through titles, channels, and descriptions
• Sort by any column (click headers)
• Details pane shows full video information
• Local caching for faster subsequent loads
• Export search results or all videos

Tips:
• Use specific keywords for better search results
• Sort by date to find recently liked videos
• Double-click videos to open in browser
• Data is cached locally for offline browsing
• Click video URLs in details pane to open

Troubleshooting:
• If videos won't load, check your internet connection
• If authentication fails, try clearing cache and re-authenticating
• For API quota issues, wait 24 hours for quota reset
• Make sure your client_secret.json file is in the same folder

Files Created:
• liked_videos_cache.json - Local video cache
• token.json - Authentication tokens
• youtube_liked_search_results_*.json - Export files"""
        
        # Create a custom dialog for better text display
        help_window = tk.Toplevel(self.root)
        help_window.title("How to Use - YouTube Liked Videos Searcher")
        help_window.geometry("650x520")
        help_window.transient(self.root)
        help_window.grab_set()
        help_window.resizable(False, False)
        
        # Center the window
        help_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Create scrollable text
        text_frame = ttk.Frame(help_window, padding="20")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('TkDefaultFont', 10))
        help_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=help_text_widget.yview)
        help_text_widget.configure(yscrollcommand=help_scrollbar.set)
        
        help_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        help_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        # Close button
        button_frame = ttk.Frame(help_window, padding="20")
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Close", command=help_window.destroy).pack(anchor=tk.E)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """YouTube Liked Videos Searcher
Version 1.0

A desktop application to search and browse your YouTube liked videos with advanced filtering and sorting capabilities.

Features:
• Search through video titles, channels, and descriptions
• Sort by title, channel, date, or description
• Fixed details pane with full video information
• Local caching for offline browsing
• Export functionality for backup and sharing

Built with:
• Python 3.7+
• tkinter (GUI framework)
• YouTube Data API v3
• Google OAuth 2.0

Created for users who want better control over their YouTube liked videos collection.

Privacy:
This application only accesses your liked videos (read-only) and stores data locally on your computer. No data is sent to third parties.

Requirements:
• Python 3.7 or higher
• Google Cloud Project with YouTube Data API enabled
• Valid OAuth 2.0 credentials (client_secret.json)
• Internet connection for initial video loading

For support and updates, please refer to the setup documentation."""
        
        # Create a custom about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title("About - YouTube Liked Videos Searcher")
        about_window.geometry("550x470")
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.resizable(False, False)
        
        # Center the window
        about_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Create scrollable text
        text_frame = ttk.Frame(about_window, padding="25")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        about_text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('TkDefaultFont', 10))
        about_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=about_text_widget.yview)
        about_text_widget.configure(yscrollcommand=about_scrollbar.set)
        
        about_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        about_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        about_text_widget.insert(1.0, about_text)
        about_text_widget.config(state=tk.DISABLED)
        
        # Close button
        button_frame = ttk.Frame(about_window, padding="25")
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Close", command=about_window.destroy).pack(anchor=tk.E)
    
    def on_closing(self):
        """Handle application closing"""
        # Could add save preferences or cleanup here if needed
        self.root.destroy()
        
    def authenticate_and_load(self):
        """Authenticate with YouTube API and load liked videos"""
        try:
            if not os.path.exists(self.CLIENT_SECRETS_FILE):
                messagebox.showerror("Error", 
                    f"Please download your OAuth 2.0 client secret file from Google Cloud Console\n"
                    f"and save it as '{self.CLIENT_SECRETS_FILE}' in the same directory as this script.")
                return
                
            self.authenticate()
            if self.youtube:
                self.load_liked_videos()
        except Exception as e:
            messagebox.showerror("Authentication Error", str(e))
    
    def authenticate(self):
        """Authenticate with YouTube Data API"""
        creds = None
        if os.path.exists(self.credentials_file):
            creds = Credentials.from_authorized_user_file(self.credentials_file, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.credentials_file, 'w') as token:
                token.write(creds.to_json())
        
        self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
        self.status_label.config(text="Authenticated successfully")
    
    def load_liked_videos(self):
        """Load all liked videos from YouTube"""
        if not self.youtube:
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        self.status_label.config(text="Loading liked videos...")
        self.root.update()
        
        try:
            self.liked_videos = []
            next_page_token = None
            
            while True:
                request = self.youtube.videos().list(
                    part="snippet,statistics",
                    myRating="like",
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for video in response.get('items', []):
                    video_info = {
                        'id': video['id'],
                        'title': video['snippet']['title'],
                        'channel': video['snippet']['channelTitle'],
                        'published_at': video['snippet']['publishedAt'],
                        'description': video['snippet'].get('description', ''),
                        'url': f"https://www.youtube.com/watch?v={video['id']}"
                    }
                    self.liked_videos.append(video_info)
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
                self.status_label.config(text=f"Loading... {len(self.liked_videos)} videos loaded")
                self.root.update()
            
            # Sort by published date (most recent first)
            self.liked_videos.sort(key=lambda x: x['published_at'], reverse=True)
            
            self.filtered_videos = self.liked_videos.copy()
            self.update_results_display()
            self.status_label.config(text=f"Loaded {len(self.liked_videos)} liked videos")
            
            # Save to local cache
            self.save_cache()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load videos: {str(e)}")
    
    def save_cache(self):
        """Save videos to local cache"""
        try:
            with open('liked_videos_cache.json', 'w', encoding='utf-8') as f:
                json.dump(self.liked_videos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save cache: {e}")
    
    def load_cache(self):
        """Load videos from local cache"""
        try:
            if os.path.exists('liked_videos_cache.json'):
                with open('liked_videos_cache.json', 'r', encoding='utf-8') as f:
                    self.liked_videos = json.load(f)
                    self.filtered_videos = self.liked_videos.copy()
                    self.update_results_display()
                    self.status_label.config(text=f"Loaded {len(self.liked_videos)} videos from cache")
                    return True
        except Exception as e:
            print(f"Failed to load cache: {e}")
        return False
    
    def on_search_change(self, event):
        """Handle search input changes"""
        # Add small delay to avoid too frequent searches
        self.root.after(300, self.search_videos)
    
    def search_videos(self):
        """Search through liked videos"""
        query = self.search_var.get().lower().strip()
        
        if not query:
            self.filtered_videos = self.liked_videos.copy()
        else:
            self.filtered_videos = []
            for video in self.liked_videos:
                # Search in title, channel name, and description
                searchable_text = f"{video['title']} {video['channel']} {video['description']}".lower()
                if query in searchable_text:
                    self.filtered_videos.append(video)
        
        self.update_results_display()
    
    def sort_column(self, col, reverse):
        """Sort treeview column"""
        try:
            # Get data from treeview
            data = []
            for child in self.tree.get_children(''):
                values = self.tree.item(child)['values']
                tags = self.tree.item(child)['tags']
                data.append((values, tags))
            
            # Sort based on column
            if col == 'date':
                # Sort by date (convert to comparable format)
                def date_key(item):
                    try:
                        # Assuming format YYYY-MM-DD
                        date_str = item[0][2]  # Date is in column index 2
                        return datetime.strptime(date_str, '%Y-%m-%d')
                    except:
                        return datetime.min
                data.sort(key=date_key, reverse=reverse)
            elif col == 'title':
                data.sort(key=lambda item: item[0][0].lower(), reverse=reverse)
            elif col == 'channel':
                data.sort(key=lambda item: item[0][1].lower(), reverse=reverse)
            elif col == 'description':
                data.sort(key=lambda item: item[0][3].lower(), reverse=reverse)
            
            # Clear and repopulate treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for values, tags in data:
                self.tree.insert('', tk.END, values=values, tags=tags)
            
            # Update sort indicators in headers
            for column in ('title', 'channel', 'date', 'description'):
                if column == col:
                    # Add sort indicator to current column
                    indicator = ' ↓' if reverse else ' ↑'
                    current_text = self.tree.heading(column)['text']
                    # Remove existing indicators
                    clean_text = current_text.replace(' ↑', '').replace(' ↓', '')
                    self.tree.heading(column, text=clean_text + indicator)
                    # Update command for next click (toggle reverse)
                    self.tree.heading(column, command=lambda c=column, r=not reverse: self.sort_column(c, r))
                else:
                    # Remove indicators from other columns
                    current_text = self.tree.heading(column)['text']
                    clean_text = current_text.replace(' ↑', '').replace(' ↓', '')
                    self.tree.heading(column, text=clean_text)
                    # Reset command for other columns
                    self.tree.heading(column, command=lambda c=column: self.sort_column(c, False))
                    
        except Exception as e:
            print(f"Sort error: {e}")
    
    def on_video_select(self, event):
        """Handle video selection to show details"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            video_id = item['tags'][0]
            
            # Find the full video data
            selected_video = None
            for video in self.filtered_videos:
                if video['id'] == video_id:
                    selected_video = video
                    break
            
            if selected_video:
                self.show_video_details(selected_video)
        else:
            self.clear_details()
    
    def show_video_details(self, video):
        """Display detailed information for selected video"""
        # Update title
        self.detail_title.config(text=video['title'])
        
        # Update channel and date
        self.detail_channel.config(text=video['channel'])
        
        # Format date nicely
        try:
            date_obj = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%B %d, %Y at %H:%M')
        except:
            formatted_date = video['published_at']
        self.detail_date.config(text=formatted_date)
        
        # Update URL (clickable)
        self.detail_url.config(text=video['url'])
        self.current_video_url = video['url']  # Store for click handler
        
        # Update description
        self.detail_description.config(state=tk.NORMAL)
        self.detail_description.delete(1.0, tk.END)
        description = video['description'] if video['description'] else "No description available."
        self.detail_description.insert(1.0, description)
        self.detail_description.config(state=tk.DISABLED)  # Make read-only
    
    def clear_details(self):
        """Clear the details pane"""
        self.detail_title.config(text="Select a video to view details")
        self.detail_channel.config(text="")
        self.detail_date.config(text="")
        self.detail_url.config(text="")
        self.current_video_url = ""
        
        self.detail_description.config(state=tk.NORMAL)
        self.detail_description.delete(1.0, tk.END)
        self.detail_description.insert(1.0, "Video description will appear here when you select a video from the list above.")
        self.detail_description.config(state=tk.DISABLED)
    
    def open_url_from_details(self, event):
        """Open URL when clicked in details pane"""
        if hasattr(self, 'current_video_url') and self.current_video_url:
            webbrowser.open(self.current_video_url)
    
    def update_results_display(self):
        """Update the results treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered videos
        for video in self.filtered_videos:
            # Format date
            try:
                date_obj = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = video['published_at'][:10]
            
            # Truncate description for display
            description = video['description'][:200] + ('...' if len(video['description']) > 200 else '')
            # Remove newlines from description for better display
            description = description.replace('\n', ' ').replace('\r', '')
            
            self.tree.insert('', tk.END, values=(
                video['title'][:100] + ('...' if len(video['title']) > 100 else ''),
                video['channel'],
                formatted_date,
                description
            ), tags=(video['id'],))
        
        # Update results label
        total = len(self.liked_videos)
        showing = len(self.filtered_videos)
        if total == showing:
            self.results_label.config(text=f"Showing all {total} videos")
        else:
            self.results_label.config(text=f"Showing {showing} of {total} videos")
        
        # Clear details when results change
        self.clear_details()
    
    def open_video(self, event=None):
        """Open selected video in browser"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            video_id = item['tags'][0]
            
            # Find video in filtered list
            for video in self.filtered_videos:
                if video['id'] == video_id:
                    webbrowser.open(video['url'])
                    break
    
    def export_results(self):
        """Export current search results to JSON"""
        if not self.filtered_videos:
            messagebox.showwarning("Warning", "No videos to export")
            return
        
        try:
            filename = f"youtube_liked_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.filtered_videos, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Export Complete", f"Results exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def run(self):
        """Start the application"""
        # Try to load from cache first
        if self.load_cache():
            pass
        else:
            messagebox.showinfo("Welcome", 
                "Welcome to YouTube Liked Videos Searcher!\n\n"
                "To get started:\n"
                "1. Set up YouTube Data API credentials\n"
                "2. Click 'Authenticate & Load Liked Videos'\n"
                "3. Start searching your liked videos!")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeLikedSearcher()
    app.run()