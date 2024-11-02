"""Defines user-facing controls to use spotifyHandler."""

from spotKeys import speech
from spotKeys.spotify import SPOTIFY_HANDLER as spotifyHandler

# Store any app-level state
APP_STATE = {}


class NoMediaPlayingError(Exception):
	"""Exception raised when there is no media currently playing."""

	def __init__(self, message='No media is currently playing'):
		super().__init__(message)


def getCurrentPlaybackContext() -> dict:
	if not (currentPlaybackContext := spotifyHandler.current_playback()):
		raise NoMediaPlayingError()
	return currentPlaybackContext


def playOrPause() -> None:
	"""
	Plays or pauses the current track dynamically.

	If media is playing, it will be paused.
	Conversely, if it is paused, it will be resumed.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	# Determine if media is currently playing
	isPlaying = currentPlaybackContext['is_playing']

	if isPlaying:
		spotifyHandler.pause_playback()
		speech.say('Paused')
	else:
		spotifyHandler.start_playback()
		speech.say('Playing')


def previousTrack() -> None:
	"""Moves to the previous track."""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	spotifyHandler.previous_track()
	speech.say('Previous track')


def nextTrack() -> None:
	"""Moves to the next track."""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	spotifyHandler.next_track()
	speech.say('Next track')


def rewind(milliseconds=3000) -> None:
	"""
	Rewinds the current track by the given interval in milliseconds.

	If the new position is negative, it seeks to the beginning of the track.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	currentProgress = currentPlaybackContext['progress_ms']

	# Either 0 (the beginning of the track), or the difference between the current progress and the interval specified
	newPosition = max(0, currentProgress - milliseconds)

	spotifyHandler.seek_track(newPosition)


def fastForward(milliseconds=3000) -> None:
	"""
	Fast-forwards the current track by the given interval in milliseconds.

	If the new position exceeds the track duration, it seeks to the end of the track.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	currentTrackProgress = currentPlaybackContext['progress_ms']
	currentTrackDuration = currentPlaybackContext['item']['duration_ms']

	# Either the track duration (the end of the track), or the sum of the current progress and the interval specified
	newPosition = min(currentTrackDuration, currentTrackProgress + milliseconds)

	spotifyHandler.seek_track(newPosition)


def decreaseVolume(percentage=10) -> None:
	"""
	Decreases the volume of the current track by the given percentage.

	If the new volume is negative, it sets the volume to 0.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	currentVolume = currentPlaybackContext['device']['volume_percent']

	# Either 0, or the difference between the current volume and the percentage specified
	newVolume = max(0, currentVolume - percentage)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotifyHandler.volume(newVolume)
	speech.say(f'{newVolume}% volume')


def increaseVolume(percentage=10) -> None:
	"""
	Increases the volume of the current track by the given percentage.

	If the new volume exceeds 100, it sets the volume to 100.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	currentVolume = currentPlaybackContext['device']['volume_percent']

	# Either 0, or the sum of the current volume and the percentage specified
	newVolume = min(currentVolume + percentage, 100)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotifyHandler.volume(newVolume)
	speech.say(f'{newVolume}% volume')


def muteOrUnmute() -> None:
	"""
	Mutes or unmutes the current track dynamically.

	If the current volume is greater than 0,
	it stores the current volume in the app's state dictionary,
	'then sets the new volume to 0.

	Otherwise, it sets the new volume to the volume before it was muted.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	currentVolume = currentPlaybackContext['device']['volume_percent']

	if currentVolume > 0:
		APP_STATE['preMuteVolume'] = currentVolume
		spotifyHandler.volume(0)
		speech.say('Muted')
	else:
		spotifyHandler.volume(APP_STATE['preMuteVolume'])
		speech.say('Unmuted')


def getTrackDescription() -> None:
	"""
	Gets the current track info as a single string, including:
	* Track name;
	* Artist names; and
	* Album name.

	Artist names are separated by commas.
	"""

	# Get the current playback context
	try:
		currentPlaybackContext = getCurrentPlaybackContext()
	except NoMediaPlayingError:
		return

	trackName = currentPlaybackContext['item']['name']
	artistNames = ', '.join(artist['name'] for artist in currentPlaybackContext['item']['artists'])
	albumName = currentPlaybackContext['item']['album']['name']

	speech.say(f'{trackName} by {artistNames} from {albumName}')
