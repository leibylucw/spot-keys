# spot-keys
An applet to define global Spotify keyboard shortcuts for screen reader users

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
### Create a Virtual Environment (virtualenv)
Using a virtual environment (virtualenv) is necessary when developing against the project. This ensures that `healing-hearts-minds-bot` has its own isolated environment, separate from your global Python and Pip, to manage its dependencies and such. It is assumed in the subsequent system-wide sections that you have created and activated one. To create one:

```shell
python -m venv .venv
```

### Activate the Virtualenv
For Command Prompt on Windows:

```cmd
.\.venv\Scripts\activate.bat
```

For PowerShell on Windows:

```powershell
.\.venv\Scripts\activate.ps1
```

For Linux/MacOS:

```sh
source .venv/bin/activate
```

To deactivate the virtualenv on all platforms:

```shell
deactivate
```

### Install Requirements
Next, upgrade Pip and install requirements:

```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
