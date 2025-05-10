import PyInstaller.__main__
import os

def build_exe():
    PyInstaller.__main__.run([
        'src/main.py',
        '--name=SpotifyToYTMusic',
        '--onefile',
        '--windowed',
        '--add-data=assets/icon.ico;assets',
        '--add-data=src/gui.py;src',
        '--add-data=src/spotify_client.py;src',
        '--add-data=src/youtube_client.py;src',
        '--hidden-import=tkinter',
        '--hidden-import=spotipy',
        '--hidden-import=ytmusicapi',
        '--hidden-import=google.auth',
        '--hidden-import=google_auth_oauthlib',
        '--hidden-import=google.auth.transport.requests',
        '--hidden-import=gui',
        '--hidden-import=spotify_client',
        '--hidden-import=youtube_client',
        '--paths=src',
        '--clean',
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ])

if __name__ == "__main__":
    build_exe()