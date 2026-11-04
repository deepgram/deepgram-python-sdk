"""
Coverage for the retry behaviour in ``deepgram.core.http_client``.

The retry path (exponential backoff, ``Retry-After`` / ``X-RateLimit-Reset``
header handling, connection-error retries, and retry exhaustion) is otherwise
not reached by the endpoint tests, which only return single responses. Sleeps
are patched out so the suite stays fast.
"""

import typing
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import respx

import deepgram.core.http_client as http_client_module
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(http_client_module.time, "sleep", lambda _s: None)

    async def _async_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(http_client_module.asyncio, "sleep", _async_sleep)


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


def _sync_client() -> DeepgramClient:
    return DeepgramClient(environment=_environment(), api_key="test_api_key")


def _async_client() -> AsyncDeepgramClient:
    return AsyncDeepgramClient(environment=_environment(), api_key="test_api_key", httpx_client=httpx.AsyncClient())


class _Response:
    status_code = 200
    headers: typing.Dict[str, str] = {}


def _sync_http_client(client: typing.Any) -> http_client_module.HttpClient:
    return http_client_module.HttpClient(
        httpx_client=client,
        base_timeout=lambda: None,
        base_headers=lambda: {},
        base_url=lambda: BASE,
    )


def _async_http_client(client: typing.Any) -> http_client_module.AsyncHttpClient:
    return http_client_module.AsyncHttpClient(
        httpx_client=client,
        base_timeout=lambda: None,
        base_headers=lambda: {},
        base_url=lambda: BASE,
        async_base_headers=None,
    )


@pytest.mark.parametrize(
    "headers",
    [
        {},  # exponential backoff branch
        {"retry-after": "1"},  # Retry-After seconds branch
        {"retry-after-ms": "10"},  # Retry-After-ms branch
        {"x-ratelimit-reset": "1"},  # X-RateLimit-Reset branch
    ],
)
def test_retry_then_exhaust_sync(headers: typing.Dict[str, str]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(500, headers=headers, json={"e": 1}))
        with pytest.raises(ApiError):
            _sync_client().manage.v1.projects.list(request_options={"max_retries": 2})


def test_retry_recovers_after_retryable_status_sync() -> None:
    with respx.mock:
        route = respx.route(host=HOST)
        route.side_effect = [httpx.Response(429, json={}), httpx.Response(200, json={})]
        # Should retry the 429 and then succeed on the 200.
        assert _sync_client().manage.v1.projects.list(request_options={"max_retries": 2}) is not None


def test_retry_on_connect_error_then_success_sync() -> None:
    with respx.mock:
        route = respx.route(host=HOST)
        route.side_effect = [httpx.ConnectError("boom"), httpx.Response(200, json={})]
        assert _sync_client().manage.v1.projects.list(request_options={"max_retries": 2}) is not None


def test_connect_error_exhausts_and_raises_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(side_effect=httpx.ConnectError("boom"))
        with pytest.raises(httpx.ConnectError):
            _sync_client().manage.v1.projects.list(request_options={"max_retries": 1})


def test_no_retries_when_max_retries_zero_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(500, json={}))
        with pytest.raises(ApiError):
            _sync_client().manage.v1.projects.list(request_options={"max_retries": 0})


@pytest.mark.parametrize("first_attempt", [httpx.Response(500), httpx.ConnectError("boom")])
def test_sync_retry_preserves_omitted_optional_body(first_attempt: typing.Any) -> None:
    client = MagicMock()
    client.request.side_effect = [first_attempt, _Response()]
    omit = typing.cast(typing.Any, ...)

    _sync_http_client(client).request(
        path="/test",
        method="POST",
        json={"value": omit},
        omit=omit,
        optional_body=True,
        request_options={"max_retries": 1},
    )

    retry = client.request.call_args_list[1].kwargs
    assert retry["json"] is None
    assert "content-type" not in {name.lower() for name in retry["headers"]}


async def test_retry_then_exhaust_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(500, headers={"retry-after": "1"}, json={}))
        with pytest.raises(ApiError):
            await _async_client().manage.v1.projects.list(request_options={"max_retries": 2})


async def test_retry_recovers_async() -> None:
    with respx.mock:
        route = respx.route(host=HOST)
        route.side_effect = [httpx.Response(500, json={}), httpx.Response(200, json={})]
        assert await _async_client().manage.v1.projects.list(request_options={"max_retries": 2}) is not None


async def test_retry_on_connect_error_async() -> None:
    with respx.mock:
        route = respx.route(host=HOST)
        route.side_effect = [httpx.ConnectError("boom"), httpx.Response(200, json={})]
        assert await _async_client().manage.v1.projects.list(request_options={"max_retries": 2}) is not None


@pytest.mark.parametrize("first_attempt", [httpx.Response(500), httpx.ConnectError("boom")])
async def test_async_retry_preserves_omitted_optional_body(first_attempt: typing.Any) -> None:
    client = MagicMock()
    client.request = AsyncMock(side_effect=[first_attempt, _Response()])
    omit = typing.cast(typing.Any, ...)

    await _async_http_client(client).request(
        path="/test",
        method="POST",
        json={"value": omit},
        omit=omit,
        optional_body=True,
        request_options={"max_retries": 1},
    )

    retry = client.request.call_args_list[1].kwargs
    assert retry["json"] is None
    assert "content-type" not in {name.lower() for name in retry["headers"]}
