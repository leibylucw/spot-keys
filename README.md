# spot-keys
An app to define global Spotify keyboard shortcuts for screen reader users

## Setup and Quickstart
### Install System Dependencies
Make sure you have the following dependencies installed and available on your system:
* [Git](https://git-scm.com/): any recent version.
	* [GH CLI (the GitHub CLI)](https://cli.github.com/) (optional): any recent version.
* [CPython](https://www.python.org/): version 3.12 or higher.
* [pipx](https://github.com/pypa/pipx): any recent version.
	* Use the `ensurepath` subcommand as described in the installation documentation so you can run `pipx` from anywhere.

### Clone the Repo
With Git:

```shell
git clone https://github.com/leibylucw/spot-keys.git
cd spot-keys
```

Or with gh:

```shell
gh repo clone leibylucw/spot-keys
cd spot-keys
```

### Install pre-commit and Git Hooks
This repository requires [pre-commit](https://pre-commit.com/) for managing Git hooks.  Start by installing it with:

```shell
pipx install pre-commit
```

Then install the hooks from the root directory of the repository:

```shell
pre-commit install
```

## Development
### Install uv
The project uses [uv](https://github.com/astral-sh/uv). It manages project dependencies and its own virtual environment. To install, use pipx:

```shell
pipx install uv
```

Then, to install dependencies:

```shell
uv venv
uv sync
```

### Run the App
Finally, to run the main script:

```shell
uv run main
```

## Building
To build the app, use Pyinstaller:

```shell
uv run pyinstaller --noconfirm build.spec
```

Add the `--clean` flag to clear build caches.
