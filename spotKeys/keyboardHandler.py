"""Configures keyboard shortcut bindings."""

import json

import keyboard

from spotKeys import controls

DEFAULT_KEYBOARD_MODIFIERS = 'alt+shift'
DEFAULT_KEYBOARD_SHORTCUTS = {
	'p': controls.playOrPause,
	'left': controls.previousTrack,
	'right': controls.nextTrack,
	'down': controls.decreaseVolume,
	'up': controls.increaseVolume,
	'[': controls.rewind,
	']': controls.fastForward,
	'm': controls.muteOrUnmute,
	't': controls.getTrackDescription,
}


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	It uses hard-coded defaults for now.
	"""

	for shortcut, control in DEFAULT_KEYBOARD_SHORTCUTS.items():
		keyboard.add_hotkey(f'{DEFAULT_KEYBOARD_MODIFIERS}+{shortcut}', control)


def waitForInput() -> None:
	"""Blocks using the keyboard library's `wait` loop."""

	keyboard.wait(f'{DEFAULT_KEYBOARD_MODIFIERS}+q')
