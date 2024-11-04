"""Configures keyboard shortcut bindings."""

import json

import keyboard

from spotKeys import controls

# Default keyboard modifiers
DEFAULT_KEYBOARD_MODIFIERS = 'alt+shift'

# Default mapping of shortcuts to function names
DEFAULT_KEYBOARD_SHORTCUTS = {
	'p': 'playOrPause',
	'left': 'previousTrack',
	'right': 'nextTrack',
	'down': 'decreaseVolume',
	'up': 'increaseVolume',
	'[': 'rewind',
	']': 'fastForward',
	'm': 'muteOrUnmute',
	'n': 'getCurrentTrackName',
	'r': 'getCurrentTrackArtistNames',
	'a': 'getCurrentTrackAlbumName',
	'i': 'getLongTrackDescription',
}

DEFAULT_QUIT_KEYBOARD_SHORTCUT = f'{DEFAULT_KEYBOARD_MODIFIERS}+q'

# Maps function names to controls
functionsToControls = {
	'playOrPause': controls.playOrPause,
	'previousTrack': controls.previousTrack,
	'nextTrack': controls.nextTrack,
	'decreaseVolume': controls.decreaseVolume,
	'increaseVolume': controls.increaseVolume,
	'rewind': controls.rewind,
	'fastForward': controls.fastForward,
	'muteOrUnmute': controls.muteOrUnmute,
	'getCurrentTrackName': controls.getCurrentTrackName,
	'getCurrentTrackArtistNames': controls.getCurrentTrackArtistNames,
	'getCurrentTrackAlbumName': controls.getCurrentTrackAlbumName,
	'getLongTrackDescription': controls.getLongTrackDescription,
}

DEFAULT_JSON_CONFIG_PATH = 'data/config.json'


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	It first attempts to load the default JSON config,
	otherwise, it uses the hard-coded values in code.
	"""

	# Get keyboard shortcuts
	# Not the right place, but it'll be fixed later
	try:
		with open(DEFAULT_JSON_CONFIG_PATH, 'r') as file:
			config = json.loads(file.read())

		keyboardModifiers = config['keyboardModifiers']
		keyboardShortcuts = config['keyboardShortcuts']
	except FileNotFoundError:
		keyboardModifiers = DEFAULT_KEYBOARD_MODIFIERS
		keyboardShortcuts = DEFAULT_KEYBOARD_SHORTCUTS

	for shortcut, control in keyboardShortcuts.items():
		keyboard.add_hotkey(f'{keyboardModifiers}+{shortcut}', functionsToControls[control])


def waitForInput() -> None:
	"""Blocks using the keyboard library's `wait` loop."""

	# Get keyboard shortcuts
	# Not the right place, but it'll be fixed later
	try:
		with open(DEFAULT_JSON_CONFIG_PATH, 'r') as file:
			config = json.loads(file.read())

		keyboardModifiers = config['keyboardModifiers']
		quitKeyboardShortcut = f'{keyboardModifiers}+q'
	except FileNotFoundError:
		keyboardModifiers = DEFAULT_KEYBOARD_MODIFIERS
		quitKeyboardShortcut = DEFAULT_QUIT_KEYBOARD_SHORTCUT

	keyboard.wait(quitKeyboardShortcut)
