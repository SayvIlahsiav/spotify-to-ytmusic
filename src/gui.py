import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient

class SpotifyToYouTubeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spotify to YouTube Music Transfer")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Make window resizable
        self.root.minsize(800, 600)
        
        # Center window on screen
        self.center_window()
        
        self.spotify_client = None
        self.youtube_client = None
        self.playlists = []
        
        # Configure styles
        self.configure_styles()
        
        # Create main UI
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure notebook style
        style.configure("TNotebook", background='#f0f0f0', borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background='#e0e0e0', 
                       padding=[20, 12], 
                       font=('Segoe UI', 10))
        style.map("TNotebook.Tab",
                 background=[("selected", "#1DB954"), ("active", "#1ed760")],
                 foreground=[("selected", "white"), ("active", "black")])
        
        # Configure button styles
        style.configure("Connect.TButton",
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure("Transfer.TButton",
                       font=('Segoe UI', 11, 'bold'),
                       padding=12,
                       background='#1DB954')
        
        # Configure frame styles
        style.configure("Card.TFrame", 
                       background='white', 
                       relief='solid',
                       borderwidth=1)
        
        # Configure label styles
        style.configure("Title.TLabel",
                       font=('Segoe UI', 16, 'bold'),
                       background='white')
        
        style.configure("Status.TLabel",
                       font=('Segoe UI', 10),
                       background='white')
        
        style.configure("Success.TLabel",
                       font=('Segoe UI', 10),
                       background='white',
                       foreground='#1DB954')
        
        style.configure("Error.TLabel",
                       font=('Segoe UI', 10),
                       background='white',
                       foreground='#e74c3c')
    
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                               text="Spotify to YouTube Music Transfer", 
                               font=('Segoe UI', 24, 'bold'),
                               foreground='#1DB954')
        title_label.pack(side="left")
        
        # Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.create_spotify_tab()
        self.create_youtube_tab()
        self.create_transfer_tab()
    
    def create_spotify_tab(self):
        spotify_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(spotify_tab, text="Spotify Setup")
        
        # Spotify card
        spotify_card = ttk.Frame(spotify_tab, style="Card.TFrame", padding="30")
        spotify_card.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(spotify_card, 
                 text="Connect to Spotify", 
                 style="Title.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Instructions
        ttk.Label(spotify_card, 
                 text="Enter your Spotify API credentials to access your playlists.",
                 font=('Segoe UI', 10),
                 background='white',
                 foreground='#666666').pack(anchor="w", pady=(0, 20))
        
        # Credentials frame
        creds_frame = ttk.Frame(spotify_card, style="Card.TFrame")
        creds_frame.pack(fill="x", pady=(0, 20))
        
        # Client ID
        ttk.Label(creds_frame, 
                 text="Client ID", 
                 font=('Segoe UI', 10, 'bold'),
                 background='white').grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.spotify_client_id = ttk.Entry(creds_frame, width=50, font=('Segoe UI', 10))
        self.spotify_client_id.grid(row=1, column=0, pady=(0, 15), ipady=5)
        
        # Client Secret
        ttk.Label(creds_frame, 
                 text="Client Secret", 
                 font=('Segoe UI', 10, 'bold'),
                 background='white').grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.spotify_client_secret = ttk.Entry(creds_frame, width=50, show="*", font=('Segoe UI', 10))
        self.spotify_client_secret.grid(row=3, column=0, ipady=5)
        
        # Connect button
        self.spotify_connect_btn = ttk.Button(spotify_card, 
                                            text="Connect to Spotify", 
                                            style="Connect.TButton",
                                            command=self.connect_spotify)
        self.spotify_connect_btn.pack(pady=20)
        
        # Status
        self.spotify_status = ttk.Label(spotify_card, 
                                      text="Not connected", 
                                      style="Status.TLabel")
        self.spotify_status.pack()
        
        # Help link
        help_text = ttk.Label(spotify_card, 
                            text="Need help? Visit the Spotify Developer Dashboard",
                            font=('Segoe UI', 9, 'underline'),
                            background='white',
                            foreground='#1DB954',
                            cursor="hand2")
        help_text.pack(pady=(20, 0))
        help_text.bind("<Button-1>", lambda e: self.open_link("https://developer.spotify.com/dashboard"))
    
    def create_youtube_tab(self):
        youtube_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(youtube_tab, text="YouTube Music Setup")
        
        # YouTube card
        youtube_card = ttk.Frame(youtube_tab, style="Card.TFrame", padding="30")
        youtube_card.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(youtube_card, 
                 text="Connect to YouTube Music", 
                 style="Title.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Instructions
        ttk.Label(youtube_card, 
                 text="Enter your YouTube API credentials to transfer playlists.",
                 font=('Segoe UI', 10),
                 background='white',
                 foreground='#666666').pack(anchor="w", pady=(0, 20))
        
        # Warning box
        warning_frame = ttk.Frame(youtube_card, style="Card.TFrame")
        warning_frame.pack(fill="x", pady=(0, 20))
        warning_frame.configure(style="Warning.TFrame")
        
        warning_label = ttk.Label(warning_frame,
                                text="⚠️ Important: Make sure you've run setup_youtube_auth.bat first!",
                                font=('Segoe UI', 10, 'bold'),
                                background='#fff3cd',
                                foreground='#856404',
                                padding=10)
        warning_label.pack(fill="x")
        
        # Credentials frame
        creds_frame = ttk.Frame(youtube_card, style="Card.TFrame")
        creds_frame.pack(fill="x", pady=(0, 20))
        
        # Client ID
        ttk.Label(creds_frame, 
                 text="Client ID", 
                 font=('Segoe UI', 10, 'bold'),
                 background='white').grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.youtube_client_id = ttk.Entry(creds_frame, width=50, font=('Segoe UI', 10))
        self.youtube_client_id.grid(row=1, column=0, pady=(0, 15), ipady=5)
        
        # Client Secret
        ttk.Label(creds_frame, 
                 text="Client Secret", 
                 font=('Segoe UI', 10, 'bold'),
                 background='white').grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.youtube_client_secret = ttk.Entry(creds_frame, width=50, show="*", font=('Segoe UI', 10))
        self.youtube_client_secret.grid(row=3, column=0, ipady=5)
        
        # Connect button
        self.youtube_connect_btn = ttk.Button(youtube_card, 
                                            text="Connect to YouTube Music", 
                                            style="Connect.TButton",
                                            command=self.connect_youtube)
        self.youtube_connect_btn.pack(pady=20)
        
        # Status
        self.youtube_status = ttk.Label(youtube_card, 
                                      text="Not connected", 
                                      style="Status.TLabel")
        self.youtube_status.pack()
        
        # Help link
        help_text = ttk.Label(youtube_card, 
                            text="Need help? Visit the Google Cloud Console",
                            font=('Segoe UI', 9, 'underline'),
                            background='white',
                            foreground='#ff0000',
                            cursor="hand2")
        help_text.pack(pady=(20, 0))
        help_text.bind("<Button-1>", lambda e: self.open_link("https://console.cloud.google.com/"))
    
    def create_transfer_tab(self):
        transfer_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(transfer_tab, text="Transfer")
        
        # Transfer card
        transfer_card = ttk.Frame(transfer_tab, style="Card.TFrame", padding="30")
        transfer_card.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(transfer_card, 
                 text="Select Playlists to Transfer", 
                 style="Title.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Playlist selection frame
        selection_frame = ttk.Frame(transfer_card, style="Card.TFrame")
        selection_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Playlist listbox with scrollbar
        list_frame = ttk.Frame(selection_frame)
        list_frame.pack(fill="both", expand=True)
        
        self.playlist_listbox = tk.Listbox(list_frame, 
                                         selectmode="multiple",
                                         font=('Segoe UI', 10),
                                         borderwidth=1,
                                         highlightthickness=0,
                                         selectbackground='#1DB954',
                                         selectforeground='white')
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.playlist_listbox.yview)
        
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)
        
        # Transfer button and progress
        controls_frame = ttk.Frame(transfer_card, style="Card.TFrame")
        controls_frame.pack(fill="x", pady=(0, 20))
        
        self.transfer_btn = ttk.Button(controls_frame, 
                                     text="Start Transfer", 
                                     style="Transfer.TButton",
                                     command=self.start_transfer)
        self.transfer_btn.pack(pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(controls_frame, mode='determinate', length=400)
        self.progress.pack(pady=10)
        
        # Progress label
        self.progress_label = ttk.Label(controls_frame, 
                                      text="", 
                                      font=('Segoe UI', 10),
                                      background='white')
        self.progress_label.pack()
        
        # Status text area
        status_label = ttk.Label(transfer_card, 
                               text="Transfer Log", 
                               font=('Segoe UI', 12, 'bold'),
                               background='white')
        status_label.pack(anchor="w", pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(transfer_card, 
                                                   height=8,
                                                   font=('Consolas', 9),
                                                   borderwidth=1,
                                                   highlightthickness=0)
        self.status_text.pack(fill="both", expand=True)
    
    def open_link(self, url):
        import webbrowser
        webbrowser.open_new(url)
    
    def connect_spotify(self):
        client_id = self.spotify_client_id.get()
        client_secret = self.spotify_client_secret.get()
        
        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter Spotify credentials")
            return
        
        self.spotify_connect_btn.config(state="disabled", text="Connecting...")
        
        def connect():
            try:
                self.spotify_client = SpotifyClient(client_id, client_secret)
                self.spotify_client.authenticate()
                self.playlists = self.spotify_client.get_playlists()
                
                self.root.after(0, lambda: self.spotify_status.config(
                    text=f"✓ Connected - Found {len(self.playlists)} playlists",
                    style="Success.TLabel"))
                self.root.after(0, self.update_playlist_list)
                self.root.after(0, lambda: messagebox.showinfo("Success", "Connected to Spotify successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.spotify_status.config(
                    text=f"✗ Connection failed: {str(e)}",
                    style="Error.TLabel"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to connect to Spotify: {str(e)}"))
            finally:
                self.root.after(0, lambda: self.spotify_connect_btn.config(
                    state="normal", text="Connect to Spotify"))
        
        thread = threading.Thread(target=connect)
        thread.start()
    
    def connect_youtube(self):
        client_id = self.youtube_client_id.get()
        client_secret = self.youtube_client_secret.get()
        
        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter YouTube credentials")
            return
        
        self.youtube_connect_btn.config(state="disabled", text="Connecting...")
        
        def connect():
            try:
                self.youtube_client = YouTubeClient(client_id, client_secret)
                self.youtube_client.authenticate()
                
                self.root.after(0, lambda: self.youtube_status.config(
                    text="✓ Connected to YouTube Music",
                    style="Success.TLabel"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Connected to YouTube Music successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.youtube_status.config(
                    text=f"✗ Connection failed: {str(e)}",
                    style="Error.TLabel"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to connect to YouTube Music: {str(e)}"))
            finally:
                self.root.after(0, lambda: self.youtube_connect_btn.config(
                    state="normal", text="Connect to YouTube Music"))
        
        thread = threading.Thread(target=connect)
        thread.start()
    
    def update_playlist_list(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, f"  {playlist['name']} ({playlist['tracks']['total']} tracks)")
    
    def start_transfer(self):
        if not self.spotify_client or not self.youtube_client:
            messagebox.showerror("Error", "Please connect to both Spotify and YouTube Music first")
            return
        
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one playlist")
            return
        
        self.transfer_btn.config(state="disabled")
        self.progress['value'] = 0
        thread = threading.Thread(target=self.transfer_playlists, args=(selected_indices,))
        thread.start()
    
    def transfer_playlists(self, selected_indices):
        total_playlists = len(selected_indices)
        
        for idx, playlist_idx in enumerate(selected_indices):
            playlist = self.playlists[playlist_idx]
            name = playlist['name']
            
            self.update_status(f"\n🎵 Transferring: {name}")
            self.progress_label.config(text=f"Processing playlist {idx + 1} of {total_playlists}")
            
            tracks = self.spotify_client.get_playlist_tracks(playlist['id'])
            self.update_status(f"📋 Found {len(tracks)} tracks in '{name}'")
            
            def progress_callback(current, total, status):
                progress_value = ((idx * 100) + (current / total * 100)) / total_playlists
                self.progress['value'] = progress_value
                
                if "Added" in status:
                    self.update_status(f"✓ {status}")
                else:
                    self.update_status(f"⚠️ {status}")
            
            success, transferred_count = self.youtube_client.create_playlist_and_add_tracks(
                name, tracks, progress_callback
            )
            
            if success:
                self.update_status(f"✅ Successfully transferred '{name}' ({transferred_count}/{len(tracks)} tracks)\n")
            else:
                self.update_status(f"❌ Failed to transfer '{name}'\n")
        
        self.update_status("\n🎉 Transfer complete!")
        self.progress_label.config(text="Transfer completed!")
        self.transfer_btn.config(state="normal")
        messagebox.showinfo("Complete", "Transfer completed!")
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def run(self):
        self.root.mainloop()