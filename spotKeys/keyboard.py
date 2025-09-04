"""Configures keyboard shortcut bindings using Windows system hotkeys (no QUIT_SHORTCUT)."""

import ctypes
from collections.abc import Callable
from ctypes import wintypes

from spotKeys import controls, help

# --- Config (put first) -----------------------------------------------------

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
	'q': lambda: ctypes.windll.user32.PostQuitMessage(0),  # quit as a normal control
}

# --- Win32 bits -------------------------------------------------------------

MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN = 0x0001, 0x0002, 0x0004, 0x0008
WM_HOTKEY = 0x0312

# Only a few specials need hard-coding; everything else comes from VkKeyScanW
_SPECIAL_VK = {
	'left': 0x25,
	'up': 0x26,
	'right': 0x27,
	'down': 0x28,
	'f1': 0x70,
}

user32 = ctypes.windll.user32
RegisterHotKey = user32.RegisterHotKey
UnregisterHotKey = user32.UnregisterHotKey
GetMessageW = user32.GetMessageW

# Use the built-in MSG structure
MSG = wintypes.MSG

# --- Module state -----------------------------------------------------------

_idToHandler: dict[int, Callable[[], None]] = {}

# --- Helpers ----------------------------------------------------------------


def _modifierMask(mods: str) -> int:
	"""Convert e.g. 'alt+shift' to a MOD_* bitmask."""

	mask = 0
	for m in mods.lower().split('+'):
		m = m.strip()
		if m == 'alt':
			mask |= MOD_ALT
		elif m in ('ctrl', 'control'):
			mask |= MOD_CONTROL
		elif m == 'shift':
			mask |= MOD_SHIFT
		elif m in ('win', 'meta'):
			mask |= MOD_WIN
	return mask


def _vkFor(key: str) -> int | None:
	"""Resolve a key name to a virtual-key code using VkKeyScanW for printables."""

	k = key.lower()
	if k in _SPECIAL_VK:
		return _SPECIAL_VK[k]
	code = user32.VkKeyScanW(ord(k))
	if code == -1:
		return None
	return code & 0xFF  # low byte holds the VK code


def _register(hotkeyId: int, modsMask: int, key: str, handler: Callable[[], None]) -> bool:
	"""Register one hotkey; return True on success."""

	vk = _vkFor(key)
	if vk is None:
		return False
	if RegisterHotKey(None, hotkeyId, modsMask, vk):
		_idToHandler[hotkeyId] = handler
		return True
	return False


# --- Public API -------------------------------------------------------------


def registerKeyboardShortcuts() -> None:
	"""Register built-in keyboard shortcuts as system hotkeys (no pass-through)."""

	modsMask = _modifierMask(DEFAULT_KEYBOARD_MODIFIERS)
	nextId = 1
	for key, handler in DEFAULT_KEYBOARD_SHORTCUTS.items():
		_register(nextId, modsMask, key, handler)
		nextId += 1


def waitForInput() -> None:
	"""Block on the Windows message loop until the quit control posts WM_QUIT."""

	msg = MSG()
	while GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
		if msg.message == WM_HOTKEY:
			hotId = int(msg.wParam)
			fn = _idToHandler.get(hotId)
			if fn:
				try:
					fn()
				except Exception:
					pass
	destroy()


def destroy() -> None:
	"""Unregister all system hotkeys registered by this module."""

	for hotId in list(_idToHandler.keys()):
		try:
			UnregisterHotKey(None, hotId)
		except Exception:
			pass
	_idToHandler.clear()
