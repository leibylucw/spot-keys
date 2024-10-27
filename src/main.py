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


def previousTrack() -> None:
	"""Moves to the previous track."""
	spotify.previous_track()
	print('Previous track')


def nextTrack():
	"""Moves to the next track."""
	spotify.next_track()
	print('Next track')


def rewind(milliseconds=3000):
	"""
	Rewinds the current track by the given interval in milliseconds.

	If the new position is negative, it seeks to the beginning of the track.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	currentProgress = currentPlayback['progress_ms']

	# Either 0 (the beginning of the track), or the difference between the current progress and the interval specified
	newPosition = max(0, currentProgress - milliseconds)

	spotify.seek_track(newPosition)


def fastForward(milliseconds=3000):
	"""
	Fast-forwards the current track by the given interval in milliseconds.

	If the new position exceeds the track duration, it seeks to the end of the track.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	currentTrackProgress = currentPlayback['progress_ms']
	currentTrackDuration = currentPlayback['item']['duration_ms']

	# Either the track duration (the end of the track), or the sum of the current progress and the interval specified
	newPosition = min(currentTrackDuration, currentTrackProgress + milliseconds)

	spotify.seek_track(newPosition)


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	These are hard-coded for now.
	"""

	keyboard.add_hotkey('ctrl+win+alt+p', playOrPause)
	keyboard.add_hotkey('ctrl+win+alt+left', previousTrack)
	keyboard.add_hotkey('ctrl+win+alt+[', rewind)
	keyboard.add_hotkey('ctrl+win+alt+]', fastForward)
	keyboard.add_hotkey('ctrl+win+alt+right', nextTrack)


def main() -> None:
	registerKeyboardShortcuts()
	keyboard.wait()


if __name__ == '__main__':
	main()
