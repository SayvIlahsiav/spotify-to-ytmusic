# Spotify to YouTube Music Playlist

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
2. Download the latest `SpotifyToYTMusic.exe`
3. Run the executable - no installation required!

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

3. Run the application:
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
5. Copy your `Client ID` and `Client Secret`

### YouTube Music API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Select "TVs and Limited Input devices" as the application type
5. Copy your `Client ID` and `Client Secret`

## 📖 How to Use

1. **Launch the Application**
   - Run `SpotifyToYTMusic.exe` or `python src/main.py`

2. **Connect to Spotify**
   - Go to the "Spotify Setup" tab
   - Enter your Spotify Client ID and Client Secret
   - Click "Connect to Spotify"

3. **Connect to YouTube Music**
   - Go to the "YouTube Music Setup" tab
   - Enter your YouTube Client ID and Client Secret
   - Click "Connect to YouTube Music"
   - Follow the browser authentication process

4. **Transfer Playlists**
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
└── README.md
```

## ⚠️ Known Issues

- YouTube Music API may have rate limits - the app includes delays to prevent hitting these limits
- Some tracks might not be found on YouTube Music due to naming differences
- The first YouTube authentication may require manual browser interaction

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