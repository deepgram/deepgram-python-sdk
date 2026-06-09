# 60db sub-client. Exposes TTS via REST (one-shot + NDJSON stream) and
# WebSocket. Lazy-loaded from DeepgramClient.sixty_db.

from .client import AsyncSixtyDbClient, SixtyDbClient

__all__ = ["AsyncSixtyDbClient", "SixtyDbClient"]
