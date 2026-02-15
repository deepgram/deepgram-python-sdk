"""Interface definitions for custom WebSocket transports.

Implement one of these protocols to provide a custom transport to the
Deepgram SDK via the ``transport_factory`` parameter::

    from deepgram import DeepgramClient
    from deepgram.transport_interface import SyncTransport

    class MyTransport:
        \"\"\"Custom transport — must satisfy SyncTransport.\"\"\"

        def __init__(self, url: str, headers: dict):
            ...  # establish your connection here

        def send(self, data):
            ...  # send text (str) or binary (bytes) data

        def recv(self):
            ...  # return the next message (str or bytes)

        def __iter__(self):
            ...  # yield messages until the connection closes

        def close(self):
            ...  # tear down the connection

    client = DeepgramClient(api_key="...", transport_factory=MyTransport)

The transport factory is the **class itself** (or any callable). The SDK
calls ``factory(url, headers)`` and gets back a transport object. The SDK
handles context-manager wrapping and calls ``close()`` automatically.
"""

from typing import Any, Iterator

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class SyncTransport(Protocol):
    """Protocol that sync transport objects must satisfy.

    Methods
    -------
    send(data)
        Send text (``str``) or binary (``bytes``) data over the connection.
    recv()
        Block until the next message arrives and return it.
    __iter__()
        Yield messages until the connection closes.
    close()
        Tear down the connection and release resources.
    """

    def send(self, data: Any) -> None: ...
    def recv(self) -> Any: ...
    def __iter__(self) -> Iterator: ...
    def close(self) -> None: ...


@runtime_checkable
class AsyncTransport(Protocol):
    """Protocol that async transport objects must satisfy.

    Methods
    -------
    send(data)
        Send text (``str``) or binary (``bytes``) data over the connection.
    recv()
        Await the next message and return it.
    __aiter__()
        Async-yield messages until the connection closes.
    close()
        Tear down the connection and release resources.
    """

    async def send(self, data: Any) -> None: ...
    async def recv(self) -> Any: ...
    def __aiter__(self) -> Any: ...
    async def close(self) -> None: ...
