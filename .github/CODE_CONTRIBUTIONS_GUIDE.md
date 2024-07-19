# Development Guide

- [Development Guide](#development-guide)
  - [Welcome](#welcome)
  - [Preparing Your Local Operating System](#preparing-your-local-operating-system)
    - [Setting Up macOS](#setting-up-macos)
    - [(Optionally) Setting Up Windows](#optional-setting-up-windows)
  - [Installing Required Software](#installing-required-software)
    - [Installing on macOS](#installing-on-macos)
    - [Installing on Linux](#installing-on-linux)
  - [Installing Python](#installing-python)
  - [(Optionally) Virtual Environment Manager](#optionally-virtual-environment-manager)
  - [Installing Docker](#installing-docker)
  - [GitHub Workflow](#github-workflow)

## Welcome

This document is the canonical source of truth for building and contributing to the [Python SDK][project].

Please submit an [issue] on GitHub if you:

- Notice a requirement that this doc does not capture.
- Find a different doc that specifies requirements (the doc should instead link here).

## Preparing Your Local Operating System

Where needed, each piece of required software will have separate instructions for Linux, Windows, or macOS.

### Setting Up macOS

Parts of this project assume you are using GNU command line tools; you will need to install those tools on your system. [Follow these directions to install the tools](https://ryanparman.com/posts/2019/using-gnu-command-line-tools-in-macos-instead-of-freebsd-tools/).

In particular, this command installs the necessary packages:

```bash
brew install coreutils ed findutils gawk gnu-sed gnu-tar grep make jq
```

You will want to include this block or something similar at the end of your `.bashrc` or shell init script:

```bash
GNUBINS="$(find `brew --prefix`/opt -type d -follow -name gnubin -print)"

for bindir in ${GNUBINS[@]}
do
  export PATH=$bindir:$PATH
done

export PATH
```

This ensures that the GNU tools are found first in your path. Note that shell init scripts work a little differently for macOS. [This article can help you figure out what changes to make.](https://scriptingosx.com/2017/04/about-bash_profile-and-bashrc-on-macos/)

### (Optional) Setting Up Windows

If you are running Windows, you can contribute to the SDK without requiring a Linux-based operating system. However, it is **HIGHLY** recommended that you have access to a Linux terminal or command prompt. Is this absolutely necessary? No. Will this help out sometime down the road? Yes!

There are two recommended methods to set up your machine. To determine which method is the best choice, you must first determine which version of Windows you are running. To do this, press Windows logo key + R, type winver, and click OK. You may also enter the ver command at the Windows Command Prompt.

- If you're using Windows 10, Version 2004, Build 19041 or higher, you can use Windows Subsystem for Linux (WSL) to perform various tasks. [Follow these instructions to install WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).
- If you're using an earlier version of Windows, create a Linux virtual machine with at least 8GB of memory and 60GB of disk space.

Once you have finished setting up your WSL2 installation or Linux VM, follow the instructions below to configure your system for building and developing code.

**NOTE:** Some `examples` at the root of the repo *may* require modification as they implement Linux SIGTERM signals. This typically tends to be code using the Async IO threading model. Those examples will work on Windows if that code is removed.

## Installing Required Software

After setting up your operating system, you will be required to install software dependencies required to run examples, perform static checks, linters, execute tests, etc.

### Installing on macOS

Some build tools were installed when you prepared your system with the GNU command line tools earlier. However, you will also need to install the [Command Line Tools for Xcode](https://developer.apple.com/library/archive/technotes/tn2339/_index.html).

### Installing on Linux

All Linux distributions have the GNU tools available. Below are the most popular distributions and commands used to install these tools.

- Debian/Ubuntu

  ```bash
  sudo apt update
  sudo apt install build-essential
  ```

- Fedora/RHEL/CentOS

  ```bash
  sudo yum update
  sudo yum groupinstall "Development Tools"
  ```

- OpenSUSE

  ```bash
  sudo zypper update
  sudo zypper install -t pattern devel_C_C++
  ```

- Arch

  ```bash
  sudo pacman -Sy base-devel
  ```

### Installing Python

The Python SDK is written in [Python](https://www.python.org/downloads/). To set up a Python development environment, please follow the instructions in this [Python 3 Installation guide](https://realpython.com/installing-python/).

#### (Optionally) Virtual Environment Manager

Once you have installed Python, an optional but **HIGHLY** recommended piece of software is something that will manage virtual environments. This is important because Python projects tend to have software requirements that vary widely between projects, and even those that use the same package may require running different versions of those dependencies.

This will allow you to have multiple environments co-exist together, making it easy to switch between environments as required. There are a number of different options for virtual environment software out there. You can find a list of recommended ones below.

##### Miniconda

Miniconda is a free minimal installer for conda. It is a small bootstrap version of Anaconda that includes only conda.

[https://docs.anaconda.com/miniconda/](https://docs.anaconda.com/miniconda/)

##### venv

The venv module supports creating lightweight "virtual environments", each with their own independent set of Python packages installed in their site directories.

[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

##### pyenv

pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

### Installing Docker

Some aspects of development require Docker. To install Docker in your development environment, [follow the instructions from the Docker website](https://docs.docker.com/get-docker/).

**Note:** If you are running macOS, ensure that `/usr/local/bin` is in your `PATH`.

### Project Specific Software

Once you have the basics, you can download and install any project specific dependencies by navigating to the root your fork and running:

```bash
make ensure-deps
```

If you have not forked and `git clone`'ed your fork, please review the next section.

## GitHub Workflow

To check out code to work on, please refer to [this guide][github_workflow].

> Attribution: This was in part borrowed from this [document](https://github.com/kubernetes/community/blob/master/contributors/devel/development.md) but tailored for our use case.

[project]: https://github.com/deepgram/deepgram-python-sdk
[issue]: https://github.com/deepgram/deepgram-python-sdk/issues
[github_workflow]: https://github.com/deepgram/deepgram-python-sdk/.github/GITHUB_WORKFLOW.md
