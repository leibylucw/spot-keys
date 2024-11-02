"""Defines the main driver for spot-key."""

from spotKeys import core, speech


def main() -> None:
	"""Initializes the core logic and runs the app."""
	core.initialize()
	speech.say('Spot Keys is ready')
	core.run()
	speech.say('Exiting Spot Keys')


if __name__ == '__main__':
	main()
