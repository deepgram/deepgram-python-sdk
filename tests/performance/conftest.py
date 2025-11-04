"""Shared configuration and fixtures for performance tests."""

import os

import pytest

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def pytest_configure(config):
    """Register custom markers for performance tests."""
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "requires_api_key: mark test as requiring a real API key")


@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment, skip test if not available."""
    api_key = os.getenv("TEST_DEEPGRAM_API_KEY")
    if not api_key:
        pytest.skip("TEST_DEEPGRAM_API_KEY environment variable not set")
    return api_key


@pytest.fixture(scope="session")
def deepgram_client(api_key):
    """Create a DeepgramClient instance for testing."""
    from deepgram import DeepgramClient

    return DeepgramClient(api_key=api_key)


@pytest.fixture
def generate_test_text():
    """Factory fixture to generate test text of specified length."""

    def _generate(length: int = 1000) -> str:
        """Generate test text of approximately the specified length."""
        base_text = (
            "The quick brown fox jumps over the lazy dog. "
            "This is a test of the text to speech system. "
            "We are measuring performance metrics including time to first byte and time to last byte. "
        )

        # Repeat base text to reach desired length
        repetitions = (length // len(base_text)) + 1
        text = (base_text * repetitions)[:length]

        return text.strip()

    return _generate
