"""Defines the main driver for spot-key."""

from spotKeys import core, speech


def main() -> None:
	"""Initializes the core logic and runs the app."""

	core.initialize()
	core.run()
	core.exit()


if __name__ == '__main__':
	main()
