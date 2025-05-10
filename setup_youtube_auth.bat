@echo off
echo Setting up YouTube Music authentication...
echo.
echo This will open your browser for authentication.
echo.
pip install ytmusicapi
ytmusicapi oauth
echo.
echo Setup complete! You can now run SpotifyToYTMusic.exe
pause