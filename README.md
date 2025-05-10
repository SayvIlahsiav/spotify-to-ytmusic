# Spotify to YouTube Music Playlist Transfer

A desktop application that allows you to transfer your playlists from Spotify to YouTube Music with a user-friendly interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)

## 🎵 Features

- Easy-to-use graphical interface
- Batch transfer multiple playlists
- Real-time transfer progress
- No coding required - just download and run
- Preserves playlist names and descriptions

## 🚀 Quick Start

### Option 1: Download Pre-built Executable (Recommended)

1. Go to the [Releases](https://github.com/sayvilahsiav/spotify-to-ytmusic/releases) page
2. Download the latest release package (includes `SpotifyToYTMusic.exe` and setup files)
3. **IMPORTANT**: Run `setup_youtube_auth.bat` first (included in the package)
4. Run `SpotifyToYTMusic.exe`

### Option 2: Run from Source

1. Clone the repository:
```bash
git clone https://github.com/sayvilahsiav/spotify-to-ytmusic.git
cd spotify-to-ytmusic
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up YouTube authentication:
```bash
ytmusicapi oauth
```

4. Run the application:
```bash
python src/main.py
```

## 📋 Prerequisites

Before using the application, you need to set up API credentials for both services:

### Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an app"
4. Enter an app name and description
5. Add `http://127.0.0.1:8888/callback` as a Redirect URI
6. Copy your `Client ID` and `Client Secret`

### YouTube Music API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Select "TVs and Limited Input devices" as the application type
5. Copy your `Client ID` and `Client Secret`

## 📖 How to Use

1. **Initial Setup (One-time only)**
   - If using the exe: Run `setup_youtube_auth.bat` from the release package
   - If running from source: Run `ytmusicapi oauth` in your terminal

2. **Launch the Application**
   - Run `SpotifyToYTMusic.exe` or `python src/main.py`

3. **Connect to Spotify**
   - Go to the "Spotify Setup" tab
   - Enter your Spotify Client ID and Client Secret
   - Click "Connect to Spotify"

4. **Connect to YouTube Music**
   - Go to the "YouTube Music Setup" tab
   - Enter your YouTube Client ID and Client Secret
   - Click "Connect to YouTube Music"

5. **Transfer Playlists**
   - Go to the "Transfer" tab
   - Select the playlists you want to transfer
   - Click "Start Transfer"
   - Monitor the progress in the status window

## 🛠️ Building from Source

To build your own executable:

```bash
python build.py
```

The executable will be created in the `dist` folder.

## 🏗️ Project Structure

```
spotify-to-ytmusic/
├── src/
│   ├── main.py           # Application entry point
│   ├── gui.py            # GUI implementation
│   ├── spotify_client.py # Spotify API wrapper
│   └── youtube_client.py # YouTube Music API wrapper
├── assets/
│   └── icon.ico         # Application icon
├── requirements.txt     # Python dependencies
├── build.py            # Build script for creating executable
├── setup_youtube_auth.bat # YouTube authentication setup script
└── README.md
```

## ⚠️ Known Issues & Troubleshooting

### YouTube Authentication Error
If you get an error about "Invalid auth JSON string or file path provided" when connecting to YouTube:

**Solution**: You must run `setup_youtube_auth.bat` (included in the release) before using the application. This is a one-time setup that creates the necessary authentication file.

### Common Issues
- YouTube Music API has rate limits - the app includes delays to prevent hitting these limits
- Some tracks might not be found on YouTube Music due to naming differences
- The app requires write permissions in its directory to save authentication files

### Troubleshooting Steps
1. Ensure you've run `setup_youtube_auth.bat` before first use
2. Make sure the app is in a folder where you have write permissions
3. Check that your API credentials are correct
4. Try running as administrator if you encounter permission issues
5. If all else fails, try the source code version for more control

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Spotipy](https://github.com/spotipy-dev/spotipy) - Spotify Web API wrapper
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - YouTube Music API wrapper

## 📧 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/sayvilahsiav/spotify-to-ytmusic/issues) on GitHub.

---

Made with 💚 by [Sayv Ilahsiav]