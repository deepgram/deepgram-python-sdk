"""
``DEEPGRAM_API_KEY`` is read when the client is constructed, not when the module
is imported.

The generated base client takes ``os.getenv("DEEPGRAM_API_KEY")`` as a default
argument, which Python evaluates once at import. These tests pin the custom
client's re-read so the common ``load_dotenv()``-below-the-imports layout keeps
working (issue #734).
"""

import os
import subprocess
import sys
import textwrap
import typing

import pytest

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError


@pytest.fixture
def no_env_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEEPGRAM_API_KEY", raising=False)


def _auth(client: typing.Any) -> typing.Optional[str]:
    return client._client_wrapper.api_key


def test_env_key_set_after_import_is_used() -> None:
    """Exercise the load_dotenv ordering in a process that starts without a key."""
    env = os.environ.copy()
    env.pop("DEEPGRAM_API_KEY", None)
    code = textwrap.dedent(
        """
        import os

        from deepgram import AsyncDeepgramClient, DeepgramClient

        os.environ["DEEPGRAM_API_KEY"] = "set-after-import"
        assert DeepgramClient()._client_wrapper.api_key == "set-after-import"
        assert AsyncDeepgramClient()._client_wrapper.api_key == "set-after-import"
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_explicit_api_key_beats_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPGRAM_API_KEY", "from-env")
    assert _auth(DeepgramClient(api_key="explicit")) == "explicit"
    assert _auth(AsyncDeepgramClient(api_key="explicit")) == "explicit"


def test_explicit_none_does_not_fall_back_to_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPGRAM_API_KEY", "from-env")
    with pytest.raises(ApiError):
        DeepgramClient(api_key=None)
    with pytest.raises(ApiError):
        AsyncDeepgramClient(api_key=None)


def test_access_token_still_takes_precedence(monkeypatch: pytest.MonkeyPatch) -> None:
    """access_token callers get the placeholder, not the environment key."""
    monkeypatch.setenv("DEEPGRAM_API_KEY", "from-env")
    assert _auth(DeepgramClient(access_token="tok")) == "token"
    assert _auth(AsyncDeepgramClient(access_token="tok")) == "token"


def test_no_key_anywhere_still_raises(no_env_key: None) -> None:
    with pytest.raises(ApiError):
        DeepgramClient()
    with pytest.raises(ApiError):
        AsyncDeepgramClient()
