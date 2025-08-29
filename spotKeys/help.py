"""Display a simple, accessible help dialog listing keyboard shortcuts."""

import webbrowser

from spotKeys import speech

SPOT_KEYS_HELP_PAGE = 'https://lukeleiby.com/spot-keys-v0-1-0-help'


def openHelpPage():
	try:
		webbrowser.open_new_tab(SPOT_KEYS_HELP_PAGE)
	except exception as e:
		speech.say(e)
