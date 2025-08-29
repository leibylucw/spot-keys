"""Configures keyboard shortcut bindings."""

from collections.abc import Callable

import keyboard

from spotKeys import controls, help

DEFAULT_KEYBOARD_MODIFIERS = 'alt+shift'

DEFAULT_KEYBOARD_SHORTCUTS: dict[str, Callable[[], None]] = {
	'p': controls.playOrPause,
	'left': controls.previousTrack,
	'right': controls.nextTrack,
	'down': controls.decreaseVolume,
	'up': controls.increaseVolume,
	'[': controls.rewind,
	']': controls.fastForward,
	'm': controls.muteOrUnmute,
	'n': controls.getCurrentTrackName,
	'r': controls.getCurrentTrackArtistNames,
	'a': controls.getCurrentTrackAlbumName,
	'i': controls.getCurrentTrackDetails,
	'l': controls.likeCurrentTrack,
	'd': controls.dislikeCurrentTrack,
	'u': controls.copyCurrentTrackURL,
	'f1': help.openHelpPage,
}

QUIT_SHORTCUT = f'{DEFAULT_KEYBOARD_MODIFIERS}+q'


def registerKeyboardShortcuts() -> None:
	"""Register built-in keyboard shortcuts with the keyboard library."""

	for key, control in DEFAULT_KEYBOARD_SHORTCUTS.items():
		keyboard.add_hotkey(f'{DEFAULT_KEYBOARD_MODIFIERS}+{key}', control, suppress=True)


def waitForInput() -> None:
	"""Block until the quit shortcut is pressed."""

	keyboard.wait(QUIT_SHORTCUT)
