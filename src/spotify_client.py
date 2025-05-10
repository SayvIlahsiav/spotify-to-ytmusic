import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.sp = None
    
    def authenticate(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="playlist-read-private"
        ))
    
    def get_playlists(self):
        if not self.sp:
            raise Exception("Not authenticated")
        
        playlists = []
        results = self.sp.current_user_playlists()
        while results:
            playlists.extend(results['items'])
            results = self.sp.next(results) if results['next'] else None
        return playlists
    
    def get_playlist_tracks(self, playlist_id):
        if not self.sp:
            raise Exception("Not authenticated")
        
        tracks = []
        results = self.sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track and track['id']:
                    tracks.append({
                        'title': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name']
                    })
            results = self.sp.next(results) if results['next'] else None
        return tracks