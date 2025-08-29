"""Facilitates app logic."""

from spotKeys import controls, keyboardHandler, speech


def initialize() -> None:
	"""Initializes the core logic by initializing speech and registering keyboard shortcuts."""

	keyboardHandler.registerKeyboardShortcuts()
	speech.initialize()
	speech.say('SpotKeys is ready.')
	speech.say('Press alt+shift+f1 to open the help page.')


def run() -> None:
	"""Awaits user input."""

	keyboardHandler.waitForInput()


def exit() -> None:
	"""Cleans up resources and provides feedback that the application is exiting."""

	speech.say('Exiting Spot Keys')

	while speech.isSpeaking():
		pass

	speech.destroy()
