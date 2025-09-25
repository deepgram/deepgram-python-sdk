# Contributing

Contributions are welcome. This is a generated library, and changes to core files should be promoted to our generator code.

Requires Python 3.8+

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
python -u examples/listen/media/transcribe_url/main.py
```
