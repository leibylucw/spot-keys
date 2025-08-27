"""Sets up Spotify-related config."""

import os
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyPKCE

clientID = 'b2064896aaa54957abee65a77f706933'
redirectURI = 'http://localhost:1234'
scopes = 'user-read-playback-state user-modify-playback-state user-library-read user-library-modify'
cachePath = str(Path(Path.home() / '.spot_keys_cache'))

authManager = SpotifyPKCE(
	client_id=clientID, redirect_uri=redirectURI, scope=scopes, cache_path=cachePath, open_browser=True
)


def isLoggedIn() -> bool:
	return bool(authManager.get_cached_token())


def ensureLogin():
	if not isLoggedIn():
		# Trigger browser login and cache tokens immediately on startup
		spotipy.Spotify(auth_manager=authManager).me()


# Auto-login on import if no cached token exists
ensureLogin()

SPOTIFY_HANDLER = spotipy.Spotify(auth_manager=authManager)
