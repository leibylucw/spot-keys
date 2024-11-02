"""Facilitates app logic."""

import keyboard

from spotKeys import controls, speech


def registerKeyboardShortcuts() -> None:
	"""
	Registers keyboard shortcuts with the keyboard library.

	Each shortcut is assigned a wrapper function that represents a high-level playback function

	These are hard-coded for now.
	"""

	keyboard.add_hotkey('ctrl+win+alt+p', controls.playOrPause)
	keyboard.add_hotkey('ctrl+win+alt+left', controls.previousTrack)
	keyboard.add_hotkey('ctrl+win+alt+[', controls.rewind)
	keyboard.add_hotkey('ctrl+win+alt+]', controls.fastForward)
	keyboard.add_hotkey('ctrl+win+alt+right', controls.nextTrack)
	keyboard.add_hotkey('ctrl+win+alt+down', controls.decreaseVolume)
	keyboard.add_hotkey('ctrl+win+alt+up', controls.increaseVolume)
	keyboard.add_hotkey('ctrl+win+alt+m', controls.muteOrUnmute)
	keyboard.add_hotkey('ctrl+win+alt+t', controls.getTrackDescription)


def initialize() -> None:
	"""Initializes the core logic by initializing speech and registering keyboard shortcuts."""
	speech.initialize()
	registerKeyboardShortcuts()


def run() -> None:
	"""Awaits user input."""
	keyboard.wait('ctrl+win+alt+q')
