"""Stores speech-related functionality."""

import tolk


def initialize() -> None:
	"""Initializes Tolk."""
	tolk.load()


def say(text: str) -> None:
	"""Speaks the given text with Tolk."""
	tolk.speak(text)
