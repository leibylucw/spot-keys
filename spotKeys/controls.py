"""Defines user-facing controls to use Spotify."""

import logging
from functools import wraps

import pyperclip
from spotipy.exceptions import SpotifyException

from spotKeys import speech, updater
from spotKeys.spotify import SPOTIFY_HANDLER as spotifyHandler

# Spotify URL partitions
SPOTIFY_URL = 'https://open.spotify.com'
TRACK_URL = f'{SPOTIFY_URL}/track'

# Store default values
VOLUME_PERCENTAGE_INTERVAL = 10

# Store any app-level state
APP_STATE = {}

# Repeat cycle mapping (off -> track -> context -> off)
REPEAT_STATES = {
	'off': 'track',
	'track': 'context',
	'context': 'off',
}

# silence Spotipy + urllib3 loggers
logging.getLogger('spotipy').setLevel(logging.CRITICAL)
logging.getLogger('spotipy').propagate = False
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').propagate = False


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
			speech.say('No media playing', interrupt=True)
			return

	return wrapper


# The following functions do not check if media is playing
# They simply return data from a given playback context payload
# They also can be used to compose larger forms of text like long trac descriptions


def getTrackName(currentPlaybackContext) -> str:
	"""Gets the name of the track from the given playback context."""

	return currentPlaybackContext['item']['name']


def getTrackArtistNames(currentPlaybackContext) -> list:
	"""Gets a list of the artist name(s) of the track from the given playback context."""

	return [artist['name'] for artist in currentPlaybackContext['item']['artists']]


def getTrackAlbumName(currentPlaybackContext) -> str:
	"""Gets the album name of the track from the given playback context."""

	return currentPlaybackContext['item']['album']['name']


def getTrackID(currentPlaybackContext) -> str:
	"""Gets the ID of the track from the given playback context."""

	return currentPlaybackContext['item']['id']


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
		speech.say('Paused', interrupt=True)
	else:
		spotifyHandler.start_playback()
		speech.say('Playing', interrupt=True)


@checkForPlayingMedia
def previousTrack(currentPlaybackContext) -> None:
	"""Moves to the previous track."""

	spotifyHandler.previous_track()
	speech.say('Previous track', interrupt=True)


@checkForPlayingMedia
def nextTrack(currentPlaybackContext) -> None:
	"""Moves to the next track."""

	spotifyHandler.next_track()
	speech.say('Next track', interrupt=True)


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


# Spotify API Volume Control Issues
#
# Fetching and setting the volume through Spotify's Web API can be unreliable and inconsistent.
# This module encapsulates functions that handle the volume management via Spotify's API, addressing known issues.
#
# Known Issues:
# 1. The `GET /v1/me/player` endpoint might not always return accurate volume levels
# after using the `PUT /v1/me/player/volume` to set the volume.
# Users have reported that the volume level returned does not always match the volume level set,
# especially when changing volume through different devices or interfaces (GitHub Issue #1317).
# 2. Desynchronisation issues occur when adjusting the volume via the Spotify Connect Web Playback SDK.
# Adjustments made from one device (like the native Spotify app) might not be reflected or cause the player to
# report incorrect playback states (GitHub Issue #788).
# 3. No direct method to retrieve the current volume percentage from the API,
# as developers have noted the absence of a straightforward `GET` method
# to fetch the current volume (GitHub Issue #252).
#
# Potential Workarounds:
# - Continuously monitor the device's playback state to verify volume changes.
# - Use device-specific commands to manage volume when possible to ensure consistency across different interfaces.
# - Implement additional checks and balances within the app to handle discrepancies in volume data reported by the API.
#
# Implemented Solution:
#


@checkForPlayingMedia
def decreaseVolume(currentPlaybackContext, percentage=VOLUME_PERCENTAGE_INTERVAL) -> None:
	"""
	Decreases the volume of the current track by the given percentage.
	If the new volume is negative, it sets the volume to 0.
	"""

	currentVolume = currentPlaybackContext['device']['volume_percent']

	if APP_STATE.get('preMuteVolume'):
		muteOrUnmute()

	else:
		# Either 0, or the difference between the current volume and the VOLUME_PERCENTAGE_INTERVAL specified
		newVolume = max(0, currentVolume - percentage)

		# Ensure it's always rounded to the closest VOLUME_PERCENTAGE_INTERVAL
		newVolume = round(newVolume / percentage) * percentage

		spotifyHandler.volume(newVolume)
		speech.say(f'{newVolume}% volume', interrupt=True)


@checkForPlayingMedia
def increaseVolume(currentPlaybackContext, percentage=VOLUME_PERCENTAGE_INTERVAL) -> None:
	"""
	Increases the volume of the current track by the given percentage.
	If the new volume exceeds 100, it sets the volume to 100.
	"""

	currentVolume = currentPlaybackContext['device']['volume_percent']

	if APP_STATE.get('preMuteVolume'):
		muteOrUnmute()

	else:
		# Either 0, or the sum of the current volume and the VOLUME_PERCENTAGE_INTERVAL specified
		newVolume = min(currentVolume + percentage, 100)

		# Ensure it's always rounded to the closest VOLUME_PERCENTAGE_INTERVAL
		newVolume = round(newVolume / percentage) * percentage

		spotifyHandler.volume(newVolume)
		speech.say(f'{newVolume}% volume', interrupt=True)


@checkForPlayingMedia
def likeCurrentTrack(currentPlaybackContext) -> None:
	"""Adds the currently-playing track to the user's Liked Songs."""
	track = currentPlaybackContext['item']
	trackID = track['id']
	trackName = track['name']

	if spotifyHandler.current_user_saved_tracks_contains([trackID])[0]:
		speech.say(f'{trackName} is already in your Liked Songs', interrupt=True)
	else:
		spotifyHandler.current_user_saved_tracks_add([trackID])
		speech.say(f'Added {trackName} to Liked Songs', interrupt=True)


@checkForPlayingMedia
def dislikeCurrentTrack(currentPlaybackContext) -> None:
	"""Removes the currently-playing track from the user's Liked Songs."""
	track = currentPlaybackContext['item']
	trackID = track['id']
	trackName = track['name']

	if not spotifyHandler.current_user_saved_tracks_contains([trackID])[0]:
		speech.say(f'{trackName} is not in your Liked Songs', interrupt=True)
	else:
		spotifyHandler.current_user_saved_tracks_delete([trackID])
		speech.say(f'Removed {trackName} from Liked Songs', interrupt=True)


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
		speech.say('Muted', interrupt=True)
	else:
		spotifyHandler.volume(APP_STATE['preMuteVolume'])
		del APP_STATE['preMuteVolume']
		speech.say('Unmuted', interrupt=True)


@checkForPlayingMedia
def getCurrentTrackName(currentPlaybackContext) -> None:
	"""Gets the name of the currently-playing track."""

	speech.say(getTrackName(currentPlaybackContext), interrupt=True)


@checkForPlayingMedia
def getCurrentTrackArtistNames(currentPlaybackContext) -> None:
	"""Get the list of artist name(s) of the currently-playing track."""

	speech.say(', '.join(getTrackArtistNames(currentPlaybackContext)), interrupt=True)


@checkForPlayingMedia
def getCurrentTrackAlbumName(currentPlaybackContext) -> None:
	"""Gets the album name of the currently-playing track."""

	speech.say(getTrackAlbumName(currentPlaybackContext), interrupt=True)


@checkForPlayingMedia
def getCurrentTrackDetails(currentPlaybackContext) -> None:
	"""
	Gets the current track details as a single announcement, including:
	* Track name;
	* Artist names; and
	* Album name.
	"""

	trackName = getTrackName(currentPlaybackContext)
	artistNames = ', '.join(getTrackArtistNames(currentPlaybackContext))
	albumName = getTrackAlbumName(currentPlaybackContext)

	speech.say(f'{trackName} by {artistNames} from {albumName}', interrupt=True)


@checkForPlayingMedia
def copyCurrentTrackURL(currentPlaybackContext) -> None:
	"""
	Copies the Spotify URL of the currently-playing track to the clipboard.
	"""

	trackName = getTrackName(currentPlaybackContext)
	trackID = getTrackID(currentPlaybackContext)

	speech.say(f'URL copied to clipboard: {trackName}', interrupt=True)

	pyperclip.copy(f'{TRACK_URL}/{trackID}')


@checkForPlayingMedia
def cycleRepeat(currentPlaybackContext) -> None:
	"""
	Cycles repeat with fallbacks when a mode is disallowed by the current context.
	Order preference: off -> track -> context -> off
	"""

	state = currentPlaybackContext.get('repeat_state')
	nextState = REPEAT_STATES.get(state)

	try:
		spotifyHandler.repeat(nextState)

		if 'context' in nextState:
			nextState = 'all'

		speech.say(f'Repeat {nextState}')
	except Exception:
		speech.say('Repeat is not available in this context.')
		speech.say('You must be listening to a collection like an album, a playlist, etc.')


@checkForPlayingMedia
def toggleShuffle(currentPlaybackContext) -> None:
	"""Toggles shuffle between on and off."""

	shuffleState = currentPlaybackContext.get('shuffle_state')
	newShuffleState = not shuffleState

	try:
		spotifyHandler.shuffle(newShuffleState)
	except Exception:
		speech.say('Shuffle is unavailable.')
		return

	if newShuffleState:
		speech.say('Shuffle on')
	else:
		speech.say('Shuffle off')


def checkForUpdate() -> None:
	"""Checks if there's an available app update."""

	updater.checkForUpdate()
