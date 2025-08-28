"""Configures keyboard shortcut bindings."""

from typing import Callable, Dict

import keyboard

from spotKeys import controls

DEFAULT_KEYBOARD_MODIFIERS = 'alt+shift'
QUIT_SHORTCUT = f'{DEFAULT_KEYBOARD_MODIFIERS}+q'
DEFAULT_KEYBOARD_SHORTCUTS: Dict[str, Callable[[], None]] = {
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
}


def registerKeyboardShortcuts() -> None:
	"""Register built-in keyboard shortcuts with the keyboard library."""

	for key, function in DEFAULT_KEYBOARD_SHORTCUTS.items():
		keyboard.add_hotkey(f'{DEFAULT_KEYBOARD_MODIFIERS}+{key}', function)


def waitForInput() -> None:
	"""Block until the quit shortcut is pressed."""

	keyboard.wait(QUIT_SHORTCUT)
