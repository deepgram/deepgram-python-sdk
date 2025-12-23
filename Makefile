.PHONY: patch-websockets

patch-websockets:
	poetry run python scripts/patch_websocket_transport.py

