# Contributing

Contributions are welcome. This is a generated library, and changes to core files should be promoted to our generator code.

Requires Python 3.8+

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

## Run Example

```bash
poetry run python -u examples/listen/media/transcribe_url/main.py
```

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
