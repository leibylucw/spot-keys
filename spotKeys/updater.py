import json
from pathlib import Path

import pyperclip
import requests

from spotKeys import speech

LIVE_MANIFEST_URL = 'https://raw.githubusercontent.com/leibylucw/spot-keys/main/manifest.json'
LOCAL_MANIFEST_PATH = Path(__file__).resolve().parent.parent / 'manifest.json'


def getLiveManifest() -> str | None:
	"""Return the live `manifest.json` as text, or None on failure."""

	try:
		response = requests.get(LIVE_MANIFEST_URL, timeout=10)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException:
		return None


def getLocalManifest() -> str | None:
	"""Read manifest.json from the repo root; return its text or None."""

	try:
		return LOCAL_MANIFEST_PATH.read_text(encoding='utf-8')
	except OSError:
		return None


def loadManifest(manifestText: str) -> dict:
	"""Parse manifest text into a dict. Returns {} on JSON error."""

	try:
		return json.loads(manifestText)
	except json.JSONDecodeError:
		return {}


def getVersion(manifestJSON: dict) -> str:
	"""Extract version string from a parsed manifest dict ('' if missing)."""

	return manifestJSON.get('version', '')


def parseVersion(version: str) -> tuple[int, int, int, tuple[int, ...]]:
	"""Normalize a version string to a tuple for comparison."""

	return tuple(version.split('.'))


def compareVersions(version1: tuple, version2: tuple) -> bool:
	"""Determine if the current version is less than or equal to the latest version."""

	return version1 < version2


def checkForUpdate() -> None:
	"""Compare local version to live; speak only if an update is available, else confirm up-to-date."""

	localText = getLocalManifest()
	if localText is None:
		speech.say('Could not find the local manifest.')
		return

	localManifest = loadManifest(localText)
	localVersion = getVersion(localManifest)
	if not localVersion:
		speech.say('Local version is missing or invalid.')
		return

	liveText = getLiveManifest()
	if liveText is None:
		speech.say('Could not check for updates.')
		return

	liveManifest = loadManifest(liveText)
	liveVersion = getVersion(liveManifest)
	if not liveVersion:
		speech.say('Latest version is missing or invalid.')
		return

	if compareVersions(localVersion, liveVersion):
		updateLink = (
			f'https://github.com/leibylucw/spot-keys/releases/download/v{liveVersion}/SpotKeys_v{liveVersion}.exe'
		)

		speech.say('An update is available.')
		speech.say(f'The latest version is {liveVersion}.')
		speech.say(f'You have version {localVersion}.')

		pyperclip.copy(updateLink)

		speech.say('The link to download the latest version has been copied to your clipboard.')
		speech.say('Remember to unload this version of SpotKeys before updating.')
		speech.say('To do so, press alt+shift+q.')
		return

	speech.say('SpotKeys is up to date.')
