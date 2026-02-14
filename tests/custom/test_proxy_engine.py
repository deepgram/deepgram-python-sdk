"""Tests for the core DeepgramProxy engine."""

import httpx
import pytest

from deepgram.proxy import DeepgramProxy, Scope
from deepgram.proxy.errors import AuthenticationError, AuthorizationError, UpstreamError

API_KEY = "test-api-key-for-engine"


@pytest.fixture
def proxy():
    p = DeepgramProxy(api_key=API_KEY, require_auth=True)
    yield p
    p.close()


@pytest.fixture
def proxy_no_auth():
    p = DeepgramProxy(api_key=API_KEY, require_auth=False)
    yield p
    p.close()


class TestInit:
    def test_requires_api_key(self):
        import os
        old = os.environ.pop("DEEPGRAM_API_KEY", None)
        try:
            with pytest.raises(ValueError, match="api_key is required"):
                DeepgramProxy(api_key="")
        finally:
            if old:
                os.environ["DEEPGRAM_API_KEY"] = old

    def test_env_var_fallback(self):
        import os
        os.environ["DEEPGRAM_API_KEY"] = "env-key"
        try:
            p = DeepgramProxy()
            assert p.api_key == "env-key"
        finally:
            del os.environ["DEEPGRAM_API_KEY"]


class TestCreateToken:
    def test_returns_string(self, proxy):
        token = proxy.create_token([Scope.LISTEN])
        assert isinstance(token, str)


class TestAuthenticate:
    def test_missing_header_required(self, proxy):
        with pytest.raises(AuthenticationError, match="Missing"):
            proxy.authenticate(None)

    def test_missing_header_not_required(self, proxy_no_auth):
        result = proxy_no_auth.authenticate(None)
        assert result is None

    def test_valid_token(self, proxy):
        token = proxy.create_token([Scope.LISTEN, Scope.SPEAK])
        scopes = proxy.authenticate(f"Bearer {token}")
        assert Scope.LISTEN in scopes
        assert Scope.SPEAK in scopes

    def test_invalid_token(self, proxy):
        with pytest.raises(AuthenticationError, match="Invalid token"):
            proxy.authenticate("Bearer bad.token.here")


class TestAuthorize:
    def test_permits_matching_scope(self, proxy):
        # Should not raise
        proxy.authorize("/v1/listen", [Scope.LISTEN])

    def test_rejects_wrong_scope(self, proxy):
        with pytest.raises(AuthorizationError, match="do not permit"):
            proxy.authorize("/v1/listen", [Scope.SPEAK])

    def test_none_scopes_allows_all(self, proxy):
        # None means auth was not required and no token was provided
        proxy.authorize("/v1/listen", None)


class TestForwardRestSync:
    def test_strips_auth_header_and_injects_api_key(self, proxy):
        """Verify the proxy replaces Authorization header with its own."""
        captured = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured["auth"] = request.headers.get("authorization")
            captured["url"] = str(request.url)
            return httpx.Response(200, content=b'{"ok": true}')

        proxy._sync_client = httpx.Client(transport=httpx.MockTransport(handler))

        status, headers, body = proxy.forward_rest_sync(
            method="POST",
            path="/v1/listen",
            headers={"Authorization": "Bearer client-jwt", "Content-Type": "application/json"},
            query_string="model=nova-3",
            body=b'{"url": "https://example.com/audio.wav"}',
        )

        assert status == 200
        assert captured["auth"] == f"Token {API_KEY}"
        assert "api.deepgram.com" in captured["url"]
        assert "model=nova-3" in captured["url"]

    def test_upstream_error_passthrough(self, proxy):
        """Upstream 4xx/5xx are returned as-is."""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(400, content=b"Bad Request")

        proxy._sync_client = httpx.Client(transport=httpx.MockTransport(handler))

        status, headers, body = proxy.forward_rest_sync(
            method="POST", path="/v1/listen", headers={}, body=b"",
        )
        assert status == 400
        assert body == b"Bad Request"

    def test_connect_error_raises_upstream_error(self, proxy):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("Connection refused")

        proxy._sync_client = httpx.Client(transport=httpx.MockTransport(handler))

        with pytest.raises(UpstreamError, match="Failed to connect"):
            proxy.forward_rest_sync(method="GET", path="/v1/listen", headers={})

    def test_agent_path_routes_to_agent_host(self, proxy):
        captured = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured["url"] = str(request.url)
            return httpx.Response(200, content=b"ok")

        proxy._sync_client = httpx.Client(transport=httpx.MockTransport(handler))
        proxy.forward_rest_sync(method="POST", path="/v1/agent", headers={})

        assert "agent.deepgram.com" in captured["url"]


class TestForwardRestAsync:
    @pytest.mark.asyncio
    async def test_async_forward(self, proxy):
        captured = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured["auth"] = request.headers.get("authorization")
            return httpx.Response(200, content=b'{"result": "ok"}')

        proxy._async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

        status, headers, body = await proxy.forward_rest_async(
            method="POST",
            path="/v1/speak",
            headers={"Authorization": "Bearer jwt"},
            body=b"Hello world",
        )

        assert status == 200
        assert captured["auth"] == f"Token {API_KEY}"
