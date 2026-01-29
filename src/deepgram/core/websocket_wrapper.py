"""
WebSocket wrapper that provides drop-in replacements for websockets modules.

This module simply wraps websockets.sync.client and websockets.client to allow
for future transport customization without modifying auto-generated code.
"""

# Import the real websockets modules
import websockets
import websockets.exceptions
import websockets.sync.client as websockets_sync_client
import websockets.sync.connection as websockets_sync_connection

try:
    from websockets.legacy.client import WebSocketClientProtocol
    from websockets.legacy.client import connect as websockets_client_connect
except ImportError:
    from websockets import WebSocketClientProtocol
    from websockets import connect as websockets_client_connect

# Re-export everything that might be imported from this module
__all__ = [
    "websockets",
    "websockets_sync_client",
    "websockets_sync_connection",
    "websockets_client_connect",
    "WebSocketClientProtocol",
]
