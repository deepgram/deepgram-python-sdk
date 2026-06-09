# Contributing

Contributions are welcome. This is a generated library, and changes to core files should be promoted to our generator code.


## Prerequisites

- Python 3.10+
- Docker Desktop

Some integration tests use WireMock containers. Ensure Docker Desktop is installed and running before executing the test suite.


## Fork Repository

Fork this repo on GitHub.


## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/deepgram-python-sdk.git
cd deepgram-python-sdk
```


## Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python - -y --version 1.5.1
```

Ensure Poetry is in your `$PATH`.

**Note for Windows users:** If `poetry --version` is not recognized, add Poetry's Scripts directory to your PATH and restart the terminal.

Typical Windows location:

```text
C:\Users\<username>\AppData\Roaming\Python\Scripts
```


## Verify Installation

```bash
poetry --version
docker ps
```

If Docker is running correctly, `docker ps` should return a container listing (which may be empty).


## Install Dependencies

```bash
poetry install
```


## Run Tests

```bash
poetry run pytest -rP .
```


## Install Example Dependencies

```bash
poetry run pip install -r examples/requirements.txt
```


## Configure Deepgram API Key

Create an API key in the Deepgram Console.


### Windows

```cmd
set DEEPGRAM_API_KEY=YOUR_API_KEY
```


### Linux/macOS

```bash
export DEEPGRAM_API_KEY=YOUR_API_KEY
```


## Run Example

```bash
poetry run python -u examples/listen/v1/media/transcribe_url/with_additional_query_parameters.py
```

A successful run will display a transcription response from the Deepgram API.


## Commit Changes

```bash
git add .
git commit -m "feat: your change description"
```


## Push to Fork

```bash
git push origin main
```


## Create Pull Request

Open a pull request from your fork to the main repository.