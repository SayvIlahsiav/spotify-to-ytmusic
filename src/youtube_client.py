import time
import os
import sys
import subprocess
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from ytmusicapi import YTMusic

class YouTubeClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.ytmusic = None
        self.oauth_file = "oauth.json"
    
    def authenticate(self):
        # Check if oauth.json exists and is valid
        if os.path.exists(self.oauth_file):
            try:
                self.ytmusic = YTMusic(self.oauth_file)
                return
            except Exception as e:
                print(f"Existing oauth.json is invalid: {e}")
                os.remove(self.oauth_file)
        
        # Try automatic authentication
        try:
            self._auto_authenticate()
        except Exception as e:
            print(f"Auto authentication failed: {e}")
            raise Exception(
                "YouTube authentication failed. Please ensure:\n"
                "1. You have ytmusicapi installed\n"
                "2. Your credentials are correct\n"
                "3. You have internet connection\n\n"
                f"Error: {str(e)}"
            )
    
    def _auto_authenticate(self):
        """Automatically handle YouTube Music authentication"""
        # First, ensure ytmusicapi is installed
        try:
            import ytmusicapi
        except ImportError:
            self._install_ytmusicapi()
        
        # Create oauth.json using ytmusicapi
        self._run_oauth_process()
        
        # Initialize YTMusic with the created oauth.json
        if os.path.exists(self.oauth_file):
            self.ytmusic = YTMusic(self.oauth_file)
        else:
            raise Exception("Failed to create oauth.json")
    
    def _install_ytmusicapi(self):
        """Install ytmusicapi if not present"""
        print("Installing ytmusicapi...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ytmusicapi"])
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install ytmusicapi: {e}")
    
    def _run_oauth_process(self):
        """Run the ytmusicapi oauth process"""
        print("Starting YouTube Music authentication...")
        
        # Set environment variables for ytmusicapi
        env = os.environ.copy()
        env['YTMUSICAPI_CLIENT_ID'] = self.client_id
        env['YTMUSICAPI_CLIENT_SECRET'] = self.client_secret
        
        # Create a simple server to capture the oauth response
        server_thread = None
        auth_code = None
        
        class OAuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                nonlocal auth_code
                query = urlparse(self.path).query
                params = parse_qs(query)
                
                if 'code' in params:
                    auth_code = params['code'][0]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"""
                        <html>
                        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                        <h2>Authorization Successful!</h2>
                        <p>You can close this window and return to the application.</p>
                        <script>window.close();</script>
                        </body>
                        </html>
                    """)
                else:
                    self.send_response(400)
                    self.end_headers()
            
            def log_message(self, format, *args):
                pass  # Suppress server logs
        
        # Start local server
        server = HTTPServer(('localhost', 8080), OAuthHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Build OAuth URL
        oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            f"response_type=code&"
            f"redirect_uri=http://localhost:8080&"
            f"scope=https://www.googleapis.com/auth/youtube&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        # Open browser for authentication
        print("Opening browser for authentication...")
        webbrowser.open(oauth_url)
        
        # Wait for authentication (max 5 minutes)
        timeout = 300
        start_time = time.time()
        
        while auth_code is None and (time.time() - start_time) < timeout:
            time.sleep(1)
        
        server.shutdown()
        
        if auth_code:
            # Create oauth.json with the received code
            self._create_oauth_json(auth_code)
        else:
            raise Exception("Authentication timeout - no authorization code received")
    
    def _create_oauth_json(self, auth_code):
        """Create oauth.json file from authorization code"""
        import requests
        
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'http://localhost:8080',
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            tokens = response.json()
            
            # Create oauth.json in the format ytmusicapi expects
            oauth_data = {
                "access_token": tokens.get('access_token'),
                "refresh_token": tokens.get('refresh_token'),
                "expires_at": time.time() + tokens.get('expires_in', 3600),
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            with open(self.oauth_file, 'w') as f:
                json.dump(oauth_data, f, indent=2)
            
            print("Authentication successful! oauth.json created.")
        else:
            raise Exception(f"Failed to exchange code for tokens: {response.text}")
    
    def search_track(self, track_info):
        if not self.ytmusic:
            raise Exception("Not authenticated")
        
        query = f"{track_info['title']} {track_info['artist']}"
        try:
            search_results = self.ytmusic.search(query, filter="songs", limit=1)
            return search_results[0]['videoId'] if search_results else None
        except Exception as e:
            print(f"Error searching for {query}: {str(e)}")
            return None
    
    def create_playlist_and_add_tracks(self, playlist_name, tracks, progress_callback=None):
        if not self.ytmusic:
            raise Exception("Not authenticated")
        
        try:
            playlist_id = self.ytmusic.create_playlist(
                playlist_name, 
                "Imported from Spotify"
            )
            video_ids = []
            
            for idx, track in enumerate(tracks, 1):
                video_id = self.search_track(track)
                if video_id:
                    video_ids.append(video_id)
                    status = f"Added {track['title']} ({idx}/{len(tracks)})"
                else:
                    status = f"Not found: {track['title']} - {track['artist']}"
                
                if progress_callback:
                    progress_callback(idx, len(tracks), status)
                
                time.sleep(1.2)
            
            if video_ids:
                self.ytmusic.add_playlist_items(playlist_id, video_ids)
                return True, len(video_ids)
            return False, 0
        
        except Exception as e:
            print(f"Error transferring playlist {playlist_name}: {str(e)}")
            return False, 0