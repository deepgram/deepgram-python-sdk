# Proxy Feature — Required Changes to Existing Files

These changes are needed in Fern-generated or config files that aren't modified
by the proxy implementation itself.

## pyproject.toml

Add PyJWT as an optional dependency and create the `proxy` extra:

```toml
[tool.poetry.dependencies]
# ... existing deps ...
PyJWT = {version = ">=2.0.0", optional = true}

[tool.poetry.extras]
proxy = ["PyJWT"]
```

This allows users to install with:
```
pip install "deepgram-sdk[proxy]"
```

## Optional runtime dependencies (not in pyproject.toml)

These are NOT added as project dependencies — users install them directly:

- **websockets** — required for WebSocket proxying
- **fastapi** — for the FastAPI adapter
- **flask** / **flask-sock** — for the Flask adapter (flask-sock for WS)
- **django** / **channels** — for the Django adapter (channels for WS)
