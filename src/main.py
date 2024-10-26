"""Defines the main driver for spot-key."""

import os

import environs
import keyboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Read environment variables from `.env`
environs.Env().read_env()


# Initialize spotipy
spotify = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		client_id=os.getenv('CLIENT_ID'),
		client_secret=os.getenv('CLIENT_SECRET'),
		redirect_uri=os.getenv('REDIRECT_URI'),
		scope=os.getenv('SCOPES'),
	)
)


def playOrPause() -> None:
	"""
	Plays or pauses the current track dynamically.

	If media is playing, it will be paused.
	Conversely, if it is paused, it will be resumed.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	# Determine if media is currently playing
	isPlaying = currentPlayback['is_playing']

	if isPlaying:
		spotify.pause_playback()
		print('Paused')
	else:
		spotify.start_playback()
		print('Playing')


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	These are hard-coded for now.
	"""

	keyboard.add_hotkey('ctrl+win+alt+p', playOrPause)


def main() -> None:
	registerKeyboardShortcuts()
	keyboard.wait()


if __name__ == '__main__':
	main()
