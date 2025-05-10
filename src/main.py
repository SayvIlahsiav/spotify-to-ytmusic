import sys
import os

if getattr(sys, 'frozen', False):
    # If running as compiled executable
    application_path = sys._MEIPASS
else:
    # If running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from gui import SpotifyToYouTubeApp

if __name__ == "__main__":
    app = SpotifyToYouTubeApp()
    app.run()