"""Sets up Spotify-related config."""

import os
from pathlib import Path

import environs
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Default values
USER_HOME_DIRECTORY = Path.home()
SPOTIPY_CACHE_PATH = USER_HOME_DIRECTORY / '.spot_keys_cache'

# Read environment variables from `.env`
environs.Env().read_env()


# Initialize spotipy
SPOTIFY_HANDLER = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		client_id=os.getenv('CLIENT_ID'),
		client_secret=os.getenv('CLIENT_SECRET'),
		redirect_uri=os.getenv('REDIRECT_URI'),
		scope=os.getenv('SCOPES'),
		cache_path=SPOTIPY_CACHE_PATH,
	)
)
