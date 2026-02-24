"""Tests for custom WebSocket transport support."""

import json
import sys
from typing import Any, Dict, Iterator, List
from unittest.mock import MagicMock

import pytest

from deepgram.transport import (
    AsyncTransport,
    SyncTransport,
    _AsyncTransportShim,
    _SyncTransportShim,
    _TARGET_MODULES,
    install_transport,
    restore_transport,
)


# ---------------------------------------------------------------------------
# Mock transport implementations
# ---------------------------------------------------------------------------

class MockSyncTransport:
    """Minimal sync transport that satisfies the SyncTransport protocol."""

    def __init__(self, messages: List[str] = None):
        self._messages = list(messages or [])
        self._sent: List[Any] = []
        self._closed = False

    def send(self, data: Any) -> None:
        self._sent.append(data)

    def recv(self) -> str:
        if self._messages:
            return self._messages.pop(0)
        raise StopIteration

    def __iter__(self) -> Iterator:
        return iter(self._messages)

    def close(self) -> None:
        self._closed = True


class MockAsyncTransport:
    """Minimal async transport that satisfies the AsyncTransport protocol."""

    def __init__(self, messages: List[str] = None):
        self._messages = list(messages or [])
        self._sent: List[Any] = []
        self._closed = False

    async def send(self, data: Any) -> None:
        self._sent.append(data)

    async def recv(self) -> str:
        if self._messages:
            return self._messages.pop(0)
        raise StopAsyncIteration

    async def __aiter__(self):
        for msg in self._messages:
            yield msg

    async def close(self) -> None:
        self._closed = True


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _restore_after_test():
    """Ensure transport patches are cleaned up after every test."""
    yield
    restore_transport()


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------

class TestProtocolConformance:
    def test_sync_transport_protocol(self):
        transport = MockSyncTransport()
        assert isinstance(transport, SyncTransport)

    def test_async_transport_protocol(self):
        transport = MockAsyncTransport()
        assert isinstance(transport, AsyncTransport)

    def test_object_not_conforming_sync(self):
        assert not isinstance(object(), SyncTransport)

    def test_object_not_conforming_async(self):
        assert not isinstance(object(), AsyncTransport)


# ---------------------------------------------------------------------------
# Sync shim
# ---------------------------------------------------------------------------

class TestSyncTransportShim:
    def test_connect_calls_factory(self):
        transport = MockSyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _SyncTransportShim(factory)

        with shim.connect("wss://example.com", additional_headers={"Authorization": "token xyz"}) as t:
            assert t is transport

        factory.assert_called_once_with("wss://example.com", {"Authorization": "token xyz"})

    def test_connect_closes_transport(self):
        transport = MockSyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _SyncTransportShim(factory)

        with shim.connect("wss://example.com"):
            assert not transport._closed

        assert transport._closed

    def test_connect_default_headers(self):
        transport = MockSyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _SyncTransportShim(factory)

        with shim.connect("wss://example.com"):
            pass

        factory.assert_called_once_with("wss://example.com", {})


# ---------------------------------------------------------------------------
# Async shim
# ---------------------------------------------------------------------------

class TestAsyncTransportShim:
    async def test_connect_calls_factory(self):
        transport = MockAsyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _AsyncTransportShim(factory)

        async with shim("wss://example.com", extra_headers={"Authorization": "token xyz"}) as t:
            assert t is transport

        factory.assert_called_once_with("wss://example.com", {"Authorization": "token xyz"})

    async def test_connect_closes_transport(self):
        transport = MockAsyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _AsyncTransportShim(factory)

        async with shim("wss://example.com"):
            assert not transport._closed

        assert transport._closed

    async def test_connect_default_headers(self):
        transport = MockAsyncTransport()
        factory = MagicMock(return_value=transport)
        shim = _AsyncTransportShim(factory)

        async with shim("wss://example.com"):
            pass

        factory.assert_called_once_with("wss://example.com", {})


# ---------------------------------------------------------------------------
# install_transport / restore_transport
# ---------------------------------------------------------------------------

def _ensure_modules_loaded():
    """Force-import all target modules so they appear in sys.modules."""
    for mod_path in _TARGET_MODULES:
        if mod_path not in sys.modules:
            __import__(mod_path)


class TestInstallRestore:
    def test_install_sync_patches_all_modules(self):
        _ensure_modules_loaded()

        factory = MagicMock()
        install_transport(sync_factory=factory)

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if hasattr(mod, "websockets_sync_client"):
                assert isinstance(mod.websockets_sync_client, _SyncTransportShim), (
                    f"{mod_path}.websockets_sync_client was not patched"
                )

    def test_install_async_patches_all_modules(self):
        _ensure_modules_loaded()

        factory = MagicMock()
        install_transport(async_factory=factory)

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if hasattr(mod, "websockets_client_connect"):
                assert isinstance(mod.websockets_client_connect, _AsyncTransportShim), (
                    f"{mod_path}.websockets_client_connect was not patched"
                )

    def test_restore_undoes_patches(self):
        _ensure_modules_loaded()

        # Capture originals
        originals = {}
        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            originals[mod_path] = {
                "sync": getattr(mod, "websockets_sync_client", None),
                "async": getattr(mod, "websockets_client_connect", None),
            }

        install_transport(sync_factory=MagicMock(), async_factory=MagicMock())
        restore_transport()

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if originals[mod_path]["sync"] is not None:
                assert mod.websockets_sync_client is originals[mod_path]["sync"], (
                    f"{mod_path}.websockets_sync_client was not restored"
                )
            if originals[mod_path]["async"] is not None:
                assert mod.websockets_client_connect is originals[mod_path]["async"], (
                    f"{mod_path}.websockets_client_connect was not restored"
                )

    def test_install_only_sync_leaves_async_untouched(self):
        _ensure_modules_loaded()

        originals = {}
        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            originals[mod_path] = getattr(mod, "websockets_client_connect", None)

        install_transport(sync_factory=MagicMock())

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if originals[mod_path] is not None:
                assert mod.websockets_client_connect is originals[mod_path]

    def test_install_only_async_leaves_sync_untouched(self):
        _ensure_modules_loaded()

        originals = {}
        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            originals[mod_path] = getattr(mod, "websockets_sync_client", None)

        install_transport(async_factory=MagicMock())

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if originals[mod_path] is not None:
                assert mod.websockets_sync_client is originals[mod_path]


# ---------------------------------------------------------------------------
# Conflict guard
# ---------------------------------------------------------------------------

class TestConflictGuard:
    def test_same_sync_factory_is_idempotent(self):
        _ensure_modules_loaded()
        factory = MagicMock()
        install_transport(sync_factory=factory)
        install_transport(sync_factory=factory)  # should not raise

    def test_same_async_factory_is_idempotent(self):
        _ensure_modules_loaded()
        factory = MagicMock()
        install_transport(async_factory=factory)
        install_transport(async_factory=factory)  # should not raise

    def test_different_sync_factory_raises(self):
        _ensure_modules_loaded()
        install_transport(sync_factory=MagicMock())
        with pytest.raises(RuntimeError, match="different sync transport factory"):
            install_transport(sync_factory=MagicMock())

    def test_different_async_factory_raises(self):
        _ensure_modules_loaded()
        install_transport(async_factory=MagicMock())
        with pytest.raises(RuntimeError, match="different async transport factory"):
            install_transport(async_factory=MagicMock())

    def test_restore_then_reinstall_different_factory(self):
        _ensure_modules_loaded()
        install_transport(sync_factory=MagicMock())
        restore_transport()
        install_transport(sync_factory=MagicMock())  # should not raise

    def test_sync_and_async_factories_are_independent(self):
        _ensure_modules_loaded()
        install_transport(sync_factory=MagicMock())
        install_transport(async_factory=MagicMock())  # should not raise


# ---------------------------------------------------------------------------
# End-to-end: sync listen with mock transport
# ---------------------------------------------------------------------------

def _valid_metadata_json() -> str:
    """Return a JSON string that matches the ListenV1Metadata Pydantic model."""
    return json.dumps({
        "type": "Metadata",
        "transaction_key": "test-txn-key",
        "request_id": "req-001",
        "sha256": "abc123",
        "created": "2024-01-01T00:00:00Z",
        "duration": 1.5,
        "channels": 1,
    })


class TestSyncEndToEnd:
    def test_listen_v1_with_mock_transport(self):
        """Verify a mock transport receives messages through the event system."""
        from deepgram.core.events import EventEmitterMixin, EventType
        from deepgram.listen.v1.socket_client import V1SocketClient

        transcript_json = _valid_metadata_json()

        transport = MockSyncTransport(messages=[transcript_json])
        client = V1SocketClient(websocket=transport)

        received = []
        errors = []
        client.on(EventType.MESSAGE, lambda msg: received.append(msg))
        client.on(EventType.ERROR, lambda err: errors.append(err))

        client.start_listening()

        assert len(errors) == 0
        assert len(received) == 1

    def test_custom_transport_error_emits_error_event(self):
        """When the transport raises, EventType.ERROR should fire."""
        from deepgram.core.events import EventType
        from deepgram.listen.v1.socket_client import V1SocketClient

        class FailingTransport:
            def send(self, data): pass
            def recv(self): raise ConnectionError("boom")
            def close(self): pass
            def __iter__(self):
                raise ConnectionError("boom")

        client = V1SocketClient(websocket=FailingTransport())

        errors = []
        closed = []
        client.on(EventType.ERROR, lambda err: errors.append(err))
        client.on(EventType.CLOSE, lambda _: closed.append(True))

        client.start_listening()

        assert len(errors) == 1
        assert isinstance(errors[0], ConnectionError)
        assert len(closed) == 1


# ---------------------------------------------------------------------------
# End-to-end: async listen with mock transport
# ---------------------------------------------------------------------------

class TestAsyncEndToEnd:
    async def test_listen_v1_async_with_mock_transport(self):
        """Verify a mock async transport works through the event system."""
        from deepgram.core.events import EventType
        from deepgram.listen.v1.socket_client import AsyncV1SocketClient

        transcript_json = _valid_metadata_json()

        class AsyncMockWS:
            def __init__(self):
                self._messages = [transcript_json]

            async def send(self, data): pass
            async def recv(self): return self._messages.pop(0)
            async def close(self): pass

            async def __aiter__(self):
                for msg in list(self._messages):
                    yield msg

        transport = AsyncMockWS()
        client = AsyncV1SocketClient(websocket=transport)

        received = []
        errors = []
        client.on(EventType.MESSAGE, lambda msg: received.append(msg))
        client.on(EventType.ERROR, lambda err: errors.append(err))

        await client.start_listening()

        assert len(errors) == 0
        assert len(received) == 1

    async def test_async_transport_error_emits_error_event(self):
        """When the async transport raises, EventType.ERROR should fire."""
        from deepgram.core.events import EventType
        from deepgram.listen.v1.socket_client import AsyncV1SocketClient

        class FailingAsyncTransport:
            async def send(self, data): pass
            async def recv(self): raise ConnectionError("async boom")
            async def close(self): pass

            async def __aiter__(self):
                raise ConnectionError("async boom")
                yield  # unreachable — makes this an async generator

        client = AsyncV1SocketClient(websocket=FailingAsyncTransport())

        errors = []
        closed = []
        client.on(EventType.ERROR, lambda err: errors.append(err))
        client.on(EventType.CLOSE, lambda _: closed.append(True))

        await client.start_listening()

        assert len(errors) == 1
        assert isinstance(errors[0], ConnectionError)
        assert len(closed) == 1


# ---------------------------------------------------------------------------
# DeepgramClient construction triggers patching
# ---------------------------------------------------------------------------

class TestClientConstruction:
    def test_deepgram_client_installs_sync_transport(self):
        _ensure_modules_loaded()

        factory = MagicMock()
        from deepgram.client import DeepgramClient
        DeepgramClient(api_key="test-key", transport_factory=factory)

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if hasattr(mod, "websockets_sync_client"):
                assert isinstance(mod.websockets_sync_client, _SyncTransportShim)

    def test_deepgram_client_without_factory_does_not_patch(self):
        _ensure_modules_loaded()

        # Ensure clean state
        restore_transport()

        from deepgram.client import DeepgramClient
        DeepgramClient(api_key="test-key")

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if hasattr(mod, "websockets_sync_client"):
                assert not isinstance(mod.websockets_sync_client, _SyncTransportShim)

    def test_async_deepgram_client_installs_async_transport(self):
        _ensure_modules_loaded()

        factory = MagicMock()
        from deepgram.client import AsyncDeepgramClient
        AsyncDeepgramClient(api_key="test-key", transport_factory=factory)

        for mod_path in _TARGET_MODULES:
            mod = sys.modules[mod_path]
            if hasattr(mod, "websockets_client_connect"):
                assert isinstance(mod.websockets_client_connect, _AsyncTransportShim)
