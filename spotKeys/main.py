"""Defines the main driver for spot-key."""

import os

import environs
import keyboard
import spotipy
import tolk
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


# Store any app-level state
playbackState = {}


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
		tolk.speak('Paused')
	else:
		spotify.start_playback()
		tolk.speak('Playing')


def previousTrack() -> None:
	"""Moves to the previous track."""
	spotify.previous_track()
	tolk.speak('Previous track')


def nextTrack():
	"""Moves to the next track."""
	spotify.next_track()
	tolk.speak('Next track')


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


def decreaseVolume(percentage=10) -> None:
	"""
	Decreases the volume of the current track by the given percentage.

	If the new volume is negative, it sets the volume to 0.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	currentVolume = currentPlayback['device']['volume_percent']

	# Either 0, or the difference between the current volume and the percentage specified
	newVolume = max(0, currentVolume - percentage)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotify.volume(newVolume)
	tolk.speak(f'{newVolume}% volume')


def increaseVolume(percentage=10) -> None:
	"""
	Increases the volume of the current track by the given percentage.

	If the new volume exceeds 100, it sets the volume to 100.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	currentVolume = currentPlayback['device']['volume_percent']

	# Either 0, or the sum of the current volume and the percentage specified
	newVolume = min(currentVolume + percentage, 100)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotify.volume(newVolume)
	tolk.speak(f'{newVolume}% volume')


def muteOrUnmute() -> None:
	"""
	Dynamically mutes or unmutes the current track.

	If the current volume is greater than 0,
	it stores the current volume in the app's state dictionary,
	'then sets the new volume to 0.

	Otherwise, it sets the new volume to the volume before it was muted.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	currentVolume = currentPlayback['device']['volume_percent']

	if currentVolume > 0:
		playbackState['preMuteVolume'] = currentVolume
		spotify.volume(0)
		tolk.speak('Muted')
	else:
		spotify.volume(playbackState['preMuteVolume'])
		tolk.speak('Unmuted')


def getTrackDescription() -> None:
	"""
	Gets the current track info, including:
	* Track name;
	* Artist names; and
	* Album name.

	Artist names are separated by commas.
	"""

	# Get the current playback context
	currentPlayback = spotify.current_playback()

	trackName = currentPlayback['item']['name']
	artistNames = ', '.join(artist['name'] for artist in currentPlayback['item']['artists'])
	albumName = currentPlayback['item']['album']['name']

	tolk.speak(f'{trackName} by {artistNames} from {albumName}')


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
	keyboard.add_hotkey('ctrl+win+alt+down', decreaseVolume)
	keyboard.add_hotkey('ctrl+win+alt+up', increaseVolume)
	keyboard.add_hotkey('ctrl+win+alt+m', muteOrUnmute)
	keyboard.add_hotkey('ctrl+win+alt+t', getTrackDescription)


def main() -> None:
	tolk.load()
	tolk.speak('Spot Keys is ready')
	registerKeyboardShortcuts()
	keyboard.wait()


if __name__ == '__main__':
	main()
