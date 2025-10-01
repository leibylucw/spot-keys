"""Facilitates app logic."""

import time

from spotKeys import controls, keyboard, speech, updater


def initialize() -> None:
	"""Initializes the core logic by initializing speech and registering keyboard shortcuts."""

	keyboard.registerKeyboardShortcuts()
	speech.initialize()

	updater.checkForUpdate()

	speech.say('Press alt+shift+f1 to open the help page')
	speech.say('Press alt+shift+o to open the donations page')


def run() -> None:
	"""Awaits user input."""

	keyboard.waitForInput()


def exit() -> None:
	"""Cleans up resources and provides feedback that the application is exiting."""

	speech.say('Exiting Spot Keys')

	while speech.isSpeaking():
		pass

	speech.destroy()
	keyboard.destroy()
