import json
from pathlib import Path

import pyperclip
import requests

from spotKeys import speech

LIVE_MANIFEST_URL = 'https://raw.githubusercontent.com/leibylucw/spot-keys/main/manifest.json'
LOCAL_MANIFEST_PATH = Path(__file__).resolve().parent.parent / 'manifest.json'
DOCUMENTS_PATH = Path.home() / 'Documents'


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
	"""Determine if the current version is less than the latest version."""

	return version1 < version2


def downloadUpdate(updateLink: str, version: str) -> bool:
	"""Compare local version to live; download update if available."""

	try:
		DOCUMENTS_PATH.mkdir(parents=True, exist_ok=True)
		filePath = DOCUMENTS_PATH / f'SpotKeys_v{version}.exe'

		if filePath.exists():
			return True

		with requests.get(updateLink, stream=True, timeout=30) as r:
			r.raise_for_status()
			with open(filePath, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192):
					f.write(chunk)
		return True
	except requests.exceptions.RequestException as e:
		return False


def checkForUpdate() -> None:
	"""Compare local version to live; download update if available."""

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

	if compareVersions(parseVersion(localVersion), parseVersion(liveVersion)):
		updateLink = (
			f'https://github.com/leibylucw/spot-keys/releases/download/v{liveVersion}/SpotKeys_v{liveVersion}.exe'
		)

		speech.say('An update is available.')
		speech.say(f'The latest version is {liveVersion}.')
		speech.say(f'You have version {localVersion}.')

		if downloadUpdate(updateLink, liveVersion):
			speech.say(f'The update has been downloaded to your Documents folder as SpotKeys_v{liveVersion}.exe.')
			speech.say('Remember to unload this version of SpotKeys before updating.')
			speech.say('To do so, press alt+shift+q.')
		else:
			pyperclip.copy(updateLink)
			speech.say('The update could not be downloaded automatically.')
			speech.say('The link has been copied to your clipboard so you can download it manually.')
		return

	speech.say('SpotKeys is up to date.')
