"""Defines user-facing controls to use spotifyHandler."""

from functools import wraps

from spotKeys import speech
from spotKeys.spotify import SPOTIFY_HANDLER as spotifyHandler

# Store any app-level state
APP_STATE = {}


class NoMediaPlayingError(Exception):
	"""Exception raised when there is no media currently playing."""

	def __init__(self, message='No media is currently playing'):
		super().__init__(message)


def getCurrentPlaybackContext() -> dict:
	"""
	Gets the context payload for the currently-playing media.

	If media is playing, the payload is returned.
	Otherwise, a NoMediaPlaying error is raised.
	"""

	if not (currentPlaybackContext := spotifyHandler.current_playback()):
		raise NoMediaPlayingError()
	return currentPlaybackContext


def checkForPlayingMedia(function):
	"""Decorator to check if media is playing before executing the function."""

	@wraps(function)
	def wrapper(*args, **kwargs):
		try:
			currentPlaybackContext = getCurrentPlaybackContext()
			return function(currentPlaybackContext, *args, **kwargs)
		except NoMediaPlayingError:
			speech.say('No media playing')
			return

	return wrapper


@checkForPlayingMedia
def playOrPause(currentPlaybackContext) -> None:
	"""
	Plays or pauses the current track dynamically.

	If media is playing, it will be paused.
	Conversely, if it is paused, it will be resumed.
	"""

	# Determine if media is currently playing
	isPlaying = currentPlaybackContext['is_playing']

	if isPlaying:
		spotifyHandler.pause_playback()
		speech.say('Paused')
	else:
		spotifyHandler.start_playback()
		speech.say('Playing')


@checkForPlayingMedia
def previousTrack(currentPlaybackContext) -> None:
	"""Moves to the previous track."""

	spotifyHandler.previous_track()
	speech.say('Previous track')


@checkForPlayingMedia
def nextTrack(currentPlaybackContext) -> None:
	"""Moves to the next track."""

	spotifyHandler.next_track()
	speech.say('Next track')


@checkForPlayingMedia
def rewind(currentPlaybackContext, milliseconds=3000) -> None:
	"""
	Rewinds the current track by the given interval in milliseconds.

	If the new position is negative, it seeks to the beginning of the track.
	"""

	currentProgress = currentPlaybackContext['progress_ms']

	# Either 0 (the beginning of the track), or the difference between the current progress and the interval specified
	newPosition = max(0, currentProgress - milliseconds)

	spotifyHandler.seek_track(newPosition)


@checkForPlayingMedia
def fastForward(currentPlaybackContext, milliseconds=3000) -> None:
	"""
	Fast-forwards the current track by the given interval in milliseconds.

	If the new position exceeds the track duration, it seeks to the end of the track.
	"""

	currentTrackProgress = currentPlaybackContext['progress_ms']
	currentTrackDuration = currentPlaybackContext['item']['duration_ms']

	# Either the track duration (the end of the track), or the sum of the current progress and the interval specified
	newPosition = min(currentTrackDuration, currentTrackProgress + milliseconds)

	spotifyHandler.seek_track(newPosition)


@checkForPlayingMedia
def decreaseVolume(currentPlaybackContext, percentage=10) -> None:
	"""
	Decreases the volume of the current track by the given percentage.

	If the new volume is negative, it sets the volume to 0.
	"""

	currentVolume = currentPlaybackContext['device']['volume_percent']

	# Either 0, or the difference between the current volume and the percentage specified
	newVolume = max(0, currentVolume - percentage)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotifyHandler.volume(newVolume)
	speech.say(f'{newVolume}% volume')


@checkForPlayingMedia
def increaseVolume(currentPlaybackContext, percentage=10) -> None:
	"""
	Increases the volume of the current track by the given percentage.

	If the new volume exceeds 100, it sets the volume to 100.
	"""

	currentVolume = currentPlaybackContext['device']['volume_percent']

	# Either 0, or the sum of the current volume and the percentage specified
	newVolume = min(currentVolume + percentage, 100)

	# Ensure it's always rounded to the closest percentage
	newVolume = round(newVolume / percentage) * percentage

	spotifyHandler.volume(newVolume)
	speech.say(f'{newVolume}% volume')


@checkForPlayingMedia
def muteOrUnmute(currentPlaybackContext) -> None:
	"""
	Mutes or unmutes the current track dynamically.

	If the current volume is greater than 0,
	it stores the current volume in the app's state dictionary,
	'then sets the new volume to 0.

	Otherwise, it sets the new volume to the volume before it was muted.
	"""

	currentVolume = currentPlaybackContext['device']['volume_percent']

	if currentVolume > 0:
		APP_STATE['preMuteVolume'] = currentVolume
		spotifyHandler.volume(0)
		speech.say('Muted')
	else:
		spotifyHandler.volume(APP_STATE['preMuteVolume'])
		speech.say('Unmuted')


@checkForPlayingMedia
def getTrackDescription(currentPlaybackContext) -> None:
	"""
	Gets the current track info as a single string, including:
	* Track name;
	* Artist names; and
	* Album name.

	Artist names are separated by commas.
	"""

	trackName = currentPlaybackContext['item']['name']
	artistNames = ', '.join(artist['name'] for artist in currentPlaybackContext['item']['artists'])
	albumName = currentPlaybackContext['item']['album']['name']

	speech.say(f'{trackName} by {artistNames} from {albumName}')
