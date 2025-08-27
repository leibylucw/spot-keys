"""Sets up Spotify-related config (PKCE + keyring cache)."""

import json

import keyring
import spotipy
from spotipy.cache_handler import CacheHandler
from spotipy.oauth2 import SpotifyPKCE


class KeyringCache(CacheHandler):
	"""CacheHandler that stores Spotipy token_info in the OS keychain."""

	def __init__(self, serviceName: str = 'spotKeys', userKey: str = 'tokens'):
		"""Initialize the keyring cache with a service name and user key."""

		self.serviceName = serviceName
		self.userKey = userKey

	def get_cached_token(self):
		"""Retrieve token_info from keyring as a dict, or None if not present."""

		raw = keyring.get_password(self.serviceName, self.userKey)
		return json.loads(raw) if raw else None

	def save_token_to_cache(self, tokenInfo):
		"""Persist token_info (dict) to keyring as a JSON string."""

		keyring.set_password(self.serviceName, self.userKey, json.dumps(tokenInfo))

	def delete_cached_token(self):
		"""Remove the stored token_info from keyring."""

		try:
			keyring.delete_password(self.serviceName, self.userKey)
		except keyring.errors.PasswordDeleteError:
			pass


clientID = 'b2064896aaa54957abee65a77f706933'
redirectURI = 'http://localhost:1234'
scopes = 'user-read-playback-state user-modify-playback-state user-library-read user-library-modify'

authManager = SpotifyPKCE(
	client_id=clientID,
	redirect_uri=redirectURI,
	scope=scopes,
	open_browser=True,
	cache_handler=KeyringCache(serviceName='spotKeys', userKey='tokens'),
)


def isLoggedIn() -> bool:
	"""Return True if a cached token exists (user is authenticated)."""

	return bool(authManager.get_cached_token())


def ensureLogin():
	"""Trigger browser login on startup if no cached token is available."""

	if not isLoggedIn():
		spotipy.Spotify(auth_manager=authManager).me()


def signOut():
	"""Clear cached tokens so the next use prompts for login again."""

	authManager.cache_handler.delete_cached_token()


# Auto-login on import if no cached token exists
ensureLogin()

SPOTIFY_HANDLER = spotipy.Spotify(auth_manager=authManager)
