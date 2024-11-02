"""Facilitates app logic."""

from spotKeys import controls, keyboardHandler, speech


def initialize() -> None:
	"""Initializes the core logic by initializing speech and registering keyboard shortcuts."""

	speech.initialize()
	keyboardHandler.registerKeyboardShortcuts()


def run() -> None:
	"""Awaits user input."""

	keyboardHandler.waitForInput()
