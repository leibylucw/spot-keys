"""Facilitates app logic."""

import os

import environs
import keyboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotKeys import controls, speech

# Read environment variables from `.env`
environs.Env().read_env()


# Initialize spotipy
spotifyHandler = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		client_id=os.getenv('CLIENT_ID'),
		client_secret=os.getenv('CLIENT_SECRET'),
		redirect_uri=os.getenv('REDIRECT_URI'),
		scope=os.getenv('SCOPES'),
	)
)


# Store any app-level state
playbackState = {}


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	These are hard-coded for now.
	"""

	keyboard.add_hotkey('ctrl+win+alt+p', lambda: controls.playOrPause(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+left', lambda: controls.previousTrack(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+[', lambda: controls.rewind(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+]', lambda: controls.fastForward(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+right', lambda: controls.nextTrack(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+down', lambda: controls.decreaseVolume(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+up', lambda: controls.increaseVolume(spotifyHandler))
	keyboard.add_hotkey('ctrl+win+alt+m', lambda: controls.muteOrUnmute(spotifyHandler, playbackState))
	keyboard.add_hotkey('ctrl+win+alt+t', lambda: controls.getTrackDescription(spotifyHandler))


def initialize() -> None:
	"""Initializes the core logic by initializing speech and registering keyboard shortcuts."""
	speech.initialize()
	registerKeyboardShortcuts()


def run() -> None:
	"""Awaits user input."""
	keyboard.wait()
