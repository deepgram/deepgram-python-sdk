"""
WebSocket client abstraction layer.

This module provides a protocol-based abstraction for WebSocket clients,
allowing users to provide custom implementations (e.g., AWS SageMaker)
while maintaining a consistent interface for socket clients.
"""

from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Dict, Iterator, Optional, Protocol, runtime_checkable

import websockets.sync.client as websockets_sync_client

try:
    from websockets.legacy.client import WebSocketClientProtocol  # type: ignore
except ImportError:
    from websockets import WebSocketClientProtocol  # type: ignore

try:
    from websockets.client import connect as websockets_client_connect  # type: ignore
except ImportError:
    from websockets.legacy.client import connect as websockets_client_connect  # type: ignore

import websockets.sync.connection as websockets_sync_connection


@runtime_checkable
class WebSocketProtocol(Protocol):
    """
    Protocol defining the minimal interface required for WebSocket connections.

    Custom WebSocket implementations (e.g., AWS SageMaker) should implement
    this protocol to be compatible with Deepgram socket clients.
    """

    async def send(self, message: Any) -> None:
        """Send a message through the WebSocket."""
        ...

    async def recv(self) -> Any:
        """Receive a message from the WebSocket."""
        ...

    def __aiter__(self):
        """Async iteration over messages."""
        ...


@runtime_checkable
class SyncWebSocketProtocol(Protocol):
    """
    Protocol defining the minimal interface required for synchronous WebSocket connections.
    """

    def send(self, message: Any) -> None:
        """Send a message through the WebSocket."""
        ...

    def recv(self) -> Any:
        """Receive a message from the WebSocket."""
        ...

    def __iter__(self):
        """Iteration over messages."""
        ...


class WebSocketFactory(Protocol):
    """
    Protocol for WebSocket connection factories.

    Users can implement this protocol to provide custom WebSocket clients
    (e.g., for AWS SageMaker bidirectional streaming).
    """

    @asynccontextmanager
    async def connect_async(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncIterator[WebSocketProtocol]:
        """
        Create an async WebSocket connection.

        Args:
            url: The WebSocket URL to connect to
            headers: Optional headers to include in the connection request

        Yields:
            A WebSocket connection implementing WebSocketProtocol
        """
        ...

    @contextmanager
    def connect_sync(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[SyncWebSocketProtocol]:
        """
        Create a synchronous WebSocket connection.

        Args:
            url: The WebSocket URL to connect to
            headers: Optional headers to include in the connection request

        Yields:
            A WebSocket connection implementing SyncWebSocketProtocol
        """
        ...


class DefaultWebSocketFactory:
    """
    Default WebSocket factory using the standard websockets library.

    This is the default implementation used when no custom factory is provided.
    """

    @asynccontextmanager
    async def connect_async(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncIterator[WebSocketClientProtocol]:
        """
        Create an async WebSocket connection using the websockets library.
        """
        async with websockets_client_connect(url, extra_headers=headers) as protocol:
            yield protocol

    @contextmanager
    def connect_sync(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[websockets_sync_connection.Connection]:
        """
        Create a synchronous WebSocket connection using the websockets library.
        """
        with websockets_sync_client.connect(url, additional_headers=headers) as protocol:
            yield protocol


# Global default factory instance
_default_factory = DefaultWebSocketFactory()


def get_default_factory() -> DefaultWebSocketFactory:
    """Get the default WebSocket factory."""
    return _default_factory
