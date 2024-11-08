"""Stores speech-related functionality."""

import tolk


def initialize() -> None:
	"""Initializes Tolk."""

	tolk.load()


def say(text: str) -> None:
	"""Speaks the given text with Tolk."""

	tolk.speak(text)


def isSpeaking() -> bool:
	"""Returns whether or not Tolk is speaking."""

	return tolk.is_speaking()


def destroy() -> None:
	"""Unloads Tolk."""

	tolk.unload()
