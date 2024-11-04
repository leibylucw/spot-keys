"""Sets up Spotify-related config."""

import sys
from pathlib import Path

import spotipy
from environs import Env
from spotipy.oauth2 import SpotifyOAuth

# Check if the application is frozen
appPath = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent

env = Env()
env.read_env(path=appPath / '.env')

homeDirectory = Path.home()
spotifyCachePath = homeDirectory / '.spotify_cache'

# Initialize spotipy with environment variables
SPOTIFY_HANDLER = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		client_id=env('CLIENT_ID'),
		client_secret=env('CLIENT_SECRET'),
		redirect_uri=env('REDIRECT_URI'),
		scope=env('SCOPES'),
		cache_path=str(spotifyCachePath),
	)
)
