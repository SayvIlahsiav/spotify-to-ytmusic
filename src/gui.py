import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient

class SpotifyToYouTubeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spotify to YouTube Music Transfer")
        self.root.geometry("800x600")
        
        self.spotify_client = None
        self.youtube_client = None
        self.playlists = []
        
        self.create_widgets()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.spotify_frame = ttk.Frame(notebook)
        notebook.add(self.spotify_frame, text="Spotify Setup")
        
        self.youtube_frame = ttk.Frame(notebook)
        notebook.add(self.youtube_frame, text="YouTube Music Setup")
        
        self.transfer_frame = ttk.Frame(notebook)
        notebook.add(self.transfer_frame, text="Transfer")
        
        self.create_spotify_tab()
        self.create_youtube_tab()
        self.create_transfer_tab()
    
    def create_spotify_tab(self):
        ttk.Label(self.spotify_frame, text="Spotify Client ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.spotify_client_id = ttk.Entry(self.spotify_frame, width=50)
        self.spotify_client_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.spotify_frame, text="Spotify Client Secret:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.spotify_client_secret = ttk.Entry(self.spotify_frame, width=50, show="*")
        self.spotify_client_secret.grid(row=1, column=1, padx=10, pady=5)
        
        self.spotify_connect_btn = ttk.Button(self.spotify_frame, text="Connect to Spotify", command=self.connect_spotify)
        self.spotify_connect_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.spotify_status = ttk.Label(self.spotify_frame, text="Not connected")
        self.spotify_status.grid(row=3, column=0, columnspan=2)
    
    def create_youtube_tab(self):
        ttk.Label(self.youtube_frame, text="YouTube Client ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.youtube_client_id = ttk.Entry(self.youtube_frame, width=50)
        self.youtube_client_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.youtube_frame, text="YouTube Client Secret:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.youtube_client_secret = ttk.Entry(self.youtube_frame, width=50, show="*")
        self.youtube_client_secret.grid(row=1, column=1, padx=10, pady=5)
        
        self.youtube_connect_btn = ttk.Button(self.youtube_frame, text="Connect to YouTube Music", command=self.connect_youtube)
        self.youtube_connect_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.youtube_status = ttk.Label(self.youtube_frame, text="Not connected")
        self.youtube_status.grid(row=3, column=0, columnspan=2)
        
        ttk.Label(self.youtube_frame, text="Note: YouTube Music authentication will open in your browser.", 
                  wraplength=400).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_transfer_tab(self):
        ttk.Label(self.transfer_frame, text="Select playlists to transfer:").pack(pady=10)
        
        self.playlist_frame = ttk.Frame(self.transfer_frame)
        self.playlist_frame.pack(fill="both", expand=True, padx=20)
        
        self.playlist_listbox = tk.Listbox(self.playlist_frame, selectmode="multiple")
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)
        
        self.transfer_btn = ttk.Button(self.transfer_frame, text="Start Transfer", command=self.start_transfer)
        self.transfer_btn.pack(pady=20)
        
        self.progress = ttk.Progressbar(self.transfer_frame, mode='determinate')
        self.progress.pack(fill="x", padx=20, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(self.transfer_frame, height=10)
        self.status_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def connect_spotify(self):
        client_id = self.spotify_client_id.get()
        client_secret = self.spotify_client_secret.get()
        
        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter Spotify credentials")
            return
        
        try:
            self.spotify_client = SpotifyClient(client_id, client_secret)
            self.spotify_client.authenticate()
            self.playlists = self.spotify_client.get_playlists()
            
            self.spotify_status.config(text=f"Connected - Found {len(self.playlists)} playlists")
            self.update_playlist_list()
            
            messagebox.showinfo("Success", "Connected to Spotify successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to Spotify: {str(e)}")
    
    def connect_youtube(self):
        client_id = self.youtube_client_id.get()
        client_secret = self.youtube_client_secret.get()
        
        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter YouTube credentials")
            return
        
        try:
            self.youtube_client = YouTubeClient(client_id, client_secret)
            self.youtube_client.authenticate()
            
            self.youtube_status.config(text="Connected to YouTube Music")
            messagebox.showinfo("Success", "Connected to YouTube Music successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to YouTube Music: {str(e)}")
    
    def update_playlist_list(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist['name'])
    
    def start_transfer(self):
        if not self.spotify_client or not self.youtube_client:
            messagebox.showerror("Error", "Please connect to both Spotify and YouTube Music first")
            return
        
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one playlist")
            return
        
        self.transfer_btn.config(state="disabled")
        thread = threading.Thread(target=self.transfer_playlists, args=(selected_indices,))
        thread.start()
    
    def transfer_playlists(self, selected_indices):
        total_playlists = len(selected_indices)
        
        for idx, playlist_idx in enumerate(selected_indices):
            playlist = self.playlists[playlist_idx]
            name = playlist['name']
            
            self.update_status(f"\nTransferring: {name}")
            tracks = self.spotify_client.get_playlist_tracks(playlist['id'])
            self.update_status(f"Found {len(tracks)} tracks in '{name}'")
            
            def progress_callback(current, total, status):
                progress_value = ((idx * 100) + (current / total * 100)) / total_playlists
                self.progress['value'] = progress_value
                self.update_status(status)
            
            success, transferred_count = self.youtube_client.create_playlist_and_add_tracks(
                name, tracks, progress_callback
            )
            
            if success:
                self.update_status(f"Successfully transferred '{name}' ({transferred_count}/{len(tracks)} tracks)")
            else:
                self.update_status(f"Failed to transfer '{name}'")
        
        self.update_status("\nTransfer complete!")
        self.transfer_btn.config(state="normal")
        messagebox.showinfo("Complete", "Transfer completed!")
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def run(self):
        self.root.mainloop()