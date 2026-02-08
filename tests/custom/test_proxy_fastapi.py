"""End-to-end tests for the FastAPI proxy adapter."""

import httpx
import pytest

from deepgram.proxy import DeepgramProxy, Scope

API_KEY = "test-api-key-for-fastapi"


@pytest.fixture
def app():
    """Create a FastAPI app with the proxy router and mocked upstream."""
    from fastapi import FastAPI

    from deepgram.proxy.adapters.fastapi import create_deepgram_router

    proxy = DeepgramProxy(api_key=API_KEY, require_auth=True)
    router = create_deepgram_router(proxy)

    application = FastAPI()
    application.include_router(router, prefix="/deepgram")

    # Mock the async HTTP client on the proxy
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b'{"results": "ok"}',
            headers={"content-type": "application/json"},
        )

    proxy._async_client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    application.state.proxy = proxy
    return application


@pytest.fixture
def client(app):
    from starlette.testclient import TestClient
    return TestClient(app)


class TestRESTProxy:
    def _make_token(self):
        proxy = DeepgramProxy(api_key=API_KEY)
        return proxy.create_token([Scope.LISTEN, Scope.SPEAK])

    def test_authenticated_request(self, client):
        token = self._make_token()
        resp = client.post(
            "/deepgram/v1/listen",
            headers={"Authorization": f"Bearer {token}"},
            content=b"audio data",
        )
        assert resp.status_code == 200
        assert resp.json() == {"results": "ok"}

    def test_missing_auth(self, client):
        resp = client.post("/deepgram/v1/listen", content=b"audio data")
        assert resp.status_code == 401

    def test_invalid_token(self, client):
        resp = client.post(
            "/deepgram/v1/listen",
            headers={"Authorization": "Bearer invalid.jwt.token"},
            content=b"audio data",
        )
        assert resp.status_code == 401

    def test_scope_mismatch(self, client):
        """Token scoped to LISTEN can't access /v1/agent."""
        proxy = DeepgramProxy(api_key=API_KEY)
        token = proxy.create_token([Scope.LISTEN])  # no AGENT scope
        resp = client.post(
            "/deepgram/v1/agent",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403

    def test_get_request(self, client):
        token = self._make_token()
        resp = client.get(
            "/deepgram/v1/listen",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
