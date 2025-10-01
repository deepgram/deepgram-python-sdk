"""Shared configuration and fixtures for integration tests."""

import os
import pytest
from unittest.mock import Mock, AsyncMock
import asyncio
from typing import Optional, Dict, Any

# Mock environment variables for testing
TEST_API_KEY = "test_api_key_12345"
TEST_ACCESS_TOKEN = "test_access_token_67890"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return TEST_API_KEY

@pytest.fixture
def mock_access_token():
    """Provide a mock access token for testing."""
    return TEST_ACCESS_TOKEN

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv("DEEPGRAM_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("DEEPGRAM_ENV", "test")

@pytest.fixture
def mock_websocket():
    """Mock websocket connection for testing."""
    mock_ws = Mock()
    mock_ws.send = Mock()
    mock_ws.recv = Mock()
    mock_ws.__enter__ = Mock(return_value=mock_ws)
    mock_ws.__exit__ = Mock(return_value=None)
    return mock_ws

@pytest.fixture
def mock_async_websocket():
    """Mock async websocket connection for testing."""
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock()
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    return mock_ws

@pytest.fixture
def sample_audio_data():
    """Sample audio data for testing."""
    return b'\x00\x01\x02\x03\x04\x05' * 100  # 600 bytes of sample audio

@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "Hello, this is a test message for speech synthesis."

@pytest.fixture
def mock_http_response():
    """Mock HTTP response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "message": "Test response"}
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response
