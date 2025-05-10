import time
import os
from ytmusicapi import YTMusic

class YouTubeClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.ytmusic = None
    
    def authenticate(self):
        oauth_file = "oauth.json"
        
        # Check if oauth.json exists
        if os.path.exists(oauth_file):
            try:
                self.ytmusic = YTMusic(oauth_file)
                return
            except Exception as e:
                print(f"Error loading existing oauth.json: {e}")
                # Delete invalid oauth.json
                os.remove(oauth_file)
        
        # If oauth.json doesn't exist, inform user to create it manually
        raise Exception(
            "YouTube authentication requires manual setup:\n\n"
            "1. Open a command prompt in this folder\n"
            "2. Run: ytmusicapi oauth\n"
            "3. Follow the browser instructions\n"
            "4. Once oauth.json is created, try connecting again"
        )
    
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