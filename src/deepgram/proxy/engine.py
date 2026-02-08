"""Core proxy engine for forwarding requests to Deepgram."""

import asyncio
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import httpx
from .errors import AuthenticationError, AuthorizationError, UpstreamError
from .scopes import Scope, get_target_base_url, path_matches_any_scope

# Headers that should not be forwarded to upstream
_HOP_BY_HOP = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
        "host",
        "authorization",
    }
)

# Default max body size: 200 MB
_DEFAULT_MAX_BODY = 200 * 1024 * 1024


class DeepgramProxy:
    """Proxy that authenticates clients and forwards requests to Deepgram.

    Args:
        api_key: Deepgram API key. Falls back to ``DEEPGRAM_API_KEY`` env var.
        require_auth: If True (default), requests must carry a valid JWT.
        production_url: Override the default ``https://api.deepgram.com`` base URL.
        agent_url: Override the default ``https://agent.deepgram.com`` base URL.
        timeout: HTTP timeout in seconds for upstream requests.
        max_body_size: Maximum request body size in bytes.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        require_auth: bool = True,
        production_url: Optional[str] = None,
        agent_url: Optional[str] = None,
        timeout: float = 60.0,
        max_body_size: int = _DEFAULT_MAX_BODY,
    ):
        resolved_key = api_key or os.environ.get("DEEPGRAM_API_KEY", "")
        if not resolved_key:
            raise ValueError("api_key is required (or set DEEPGRAM_API_KEY env var)")
        self.api_key: str = resolved_key

        self.require_auth = require_auth
        self.production_url = production_url
        self.agent_url = agent_url
        self.timeout = timeout
        self.max_body_size = max_body_size

        self._jwt_manager: Any = None
        self._sync_client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    @property
    def jwt_manager(self) -> Any:
        """Lazily initialise the JWT manager (defers PyJWT import)."""
        if self._jwt_manager is None:
            from .jwt import JWTManager

            self._jwt_manager = JWTManager(self.api_key)
        return self._jwt_manager

    # ------------------------------------------------------------------
    # Token helpers
    # ------------------------------------------------------------------

    def create_token(self, scopes: List[Scope], expires_in: int = 3600) -> str:
        """Create a signed JWT for client-side use.

        Args:
            scopes: Scopes the token grants (e.g. ``[Scope.LISTEN, Scope.SPEAK]``).
            expires_in: Token lifetime in seconds.

        Returns:
            Encoded JWT string.
        """
        return self.jwt_manager.create_token(scopes, expires_in)

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def authenticate(self, authorization: Optional[str]) -> Optional[List[Scope]]:
        """Validate a Bearer JWT from an Authorization header.

        Returns:
            List of granted scopes, or None if auth is not required and no token
            was provided.

        Raises:
            AuthenticationError: If a token is required but missing/invalid.
        """
        from .jwt import JWTManager

        token = JWTManager.extract_token_from_header(authorization)

        if token is None:
            if self.require_auth:
                raise AuthenticationError("Missing Authorization header")
            return None

        try:
            payload = self.jwt_manager.validate_token(token)
        except Exception as exc:
            raise AuthenticationError(f"Invalid token: {exc}") from exc

        return [Scope(s) for s in payload.scopes if s in Scope._value2member_map_]

    def authorize(self, path: str, scopes: Optional[List[Scope]]) -> None:
        """Check that scopes permit accessing *path*.

        When *scopes* is None (unauthenticated, auth not required), access is
        allowed to all paths.

        Raises:
            AuthorizationError: If the token's scopes don't cover the path.
        """
        if scopes is None:
            return
        if not path_matches_any_scope(path, scopes):
            raise AuthorizationError(f"Token scopes {[s.value for s in scopes]} do not permit access to {path}")

    # ------------------------------------------------------------------
    # REST forwarding
    # ------------------------------------------------------------------

    def _prepare_upstream(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        query_string: str = "",
        body: bytes = b"",
    ) -> Tuple[str, Dict[str, str], str]:
        """Build the upstream URL and sanitised headers."""
        base = get_target_base_url(path, self.production_url, self.agent_url)
        url = f"{base}{path}"
        if query_string:
            url = f"{url}?{query_string}"

        out_headers: Dict[str, str] = {}
        for k, v in headers.items():
            if k.lower() not in _HOP_BY_HOP:
                out_headers[k] = v
        out_headers["Authorization"] = f"Token {self.api_key}"

        return url, out_headers, method.upper()

    def forward_rest_sync(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        query_string: str = "",
        body: bytes = b"",
    ) -> Tuple[int, Dict[str, str], bytes]:
        """Synchronously forward an HTTP request to Deepgram.

        Returns:
            ``(status_code, response_headers, response_body)``
        """
        url, out_headers, method = self._prepare_upstream(method, path, headers, query_string, body)

        if self._sync_client is None:
            self._sync_client = httpx.Client(timeout=self.timeout)

        try:
            resp = self._sync_client.request(method, url, headers=out_headers, content=body)
        except httpx.ConnectError as exc:
            raise UpstreamError("Failed to connect to Deepgram", status_code=502, detail=str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise UpstreamError("Upstream request timed out", status_code=504, detail=str(exc)) from exc

        resp_headers = dict(resp.headers)
        # Remove hop-by-hop from response too
        for h in ("transfer-encoding", "connection"):
            resp_headers.pop(h, None)

        return resp.status_code, resp_headers, resp.content

    async def forward_rest_async(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        query_string: str = "",
        body: bytes = b"",
    ) -> Tuple[int, Dict[str, str], bytes]:
        """Asynchronously forward an HTTP request to Deepgram.

        Returns:
            ``(status_code, response_headers, response_body)``
        """
        url, out_headers, method = self._prepare_upstream(method, path, headers, query_string, body)

        if self._async_client is None:
            self._async_client = httpx.AsyncClient(timeout=self.timeout)

        try:
            resp = await self._async_client.request(method, url, headers=out_headers, content=body)
        except httpx.ConnectError as exc:
            raise UpstreamError("Failed to connect to Deepgram", status_code=502, detail=str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise UpstreamError("Upstream request timed out", status_code=504, detail=str(exc)) from exc

        resp_headers = dict(resp.headers)
        for h in ("transfer-encoding", "connection"):
            resp_headers.pop(h, None)

        return resp.status_code, resp_headers, resp.content

    # ------------------------------------------------------------------
    # WebSocket forwarding
    # ------------------------------------------------------------------

    async def forward_websocket(
        self,
        path: str,
        query_string: str,
        client_receive: Callable,
        client_send: Callable,
        client_close: Callable,
        subprotocol: Optional[str] = None,
    ) -> None:
        """Bidirectional WebSocket relay between client and Deepgram.

        Auth is handled via the ``subprotocol`` value:
        - ``"proxy,<JWT>"`` — validate JWT, connect upstream with ``token,<API_KEY>``
        - ``"token,<KEY>"`` / ``"bearer,<KEY>"`` — passthrough to Deepgram
        - None + require_auth → close 4003

        Args:
            path: The API path (e.g. ``/v1/listen``).
            query_string: URL query string to forward.
            client_receive: Async callable that returns the next message from the client.
            client_send: Async callable that sends a message to the client.
            client_close: Async callable that closes the client connection, accepts (code, reason).
            subprotocol: The ``Sec-WebSocket-Protocol`` value from the handshake.
        """
        try:
            import websockets
        except ImportError:
            raise ImportError(
                "The 'websockets' package is required for WebSocket proxying. "
                "Install it with: pip install websockets"
            )

        upstream_subprotocol: Optional[str] = None
        scopes: Optional[List[Scope]] = None

        if subprotocol:
            if subprotocol.startswith("proxy,"):
                token = subprotocol[len("proxy,") :]
                try:
                    payload = self.jwt_manager.validate_token(token)
                except Exception:
                    await client_close(4003, "Invalid token")
                    return

                scopes = [Scope(s) for s in payload.scopes if s in Scope._value2member_map_]
                try:
                    self.authorize(path, scopes)
                except AuthorizationError:
                    await client_close(4003, "Insufficient scope")
                    return

                upstream_subprotocol = f"token,{self.api_key}"

            elif subprotocol.startswith(("token,", "bearer,")):
                # Direct passthrough — forward the client's subprotocol as-is
                upstream_subprotocol = subprotocol
            else:
                if self.require_auth:
                    await client_close(4003, "Unrecognised subprotocol")
                    return
        else:
            if self.require_auth:
                await client_close(4003, "Authentication required")
                return

        base = get_target_base_url(path, self.production_url, self.agent_url)
        ws_base = base.replace("https://", "wss://").replace("http://", "ws://")
        upstream_url = f"{ws_base}{path}"
        if query_string:
            upstream_url = f"{upstream_url}?{query_string}"

        extra_headers = {"Authorization": f"Token {self.api_key}"}

        connect_kwargs: dict = {
            "additional_headers": extra_headers,
        }
        if upstream_subprotocol:
            connect_kwargs["subprotocols"] = [upstream_subprotocol]

        try:
            async with websockets.connect(upstream_url, **connect_kwargs) as upstream:

                async def client_to_upstream() -> None:
                    try:
                        while True:
                            msg = await client_receive()
                            if msg is None:
                                break
                            await upstream.send(msg)
                    except Exception:
                        pass

                async def upstream_to_client() -> None:
                    try:
                        async for msg in upstream:
                            await client_send(msg)
                    except Exception:
                        pass

                tasks = [
                    asyncio.create_task(client_to_upstream()),
                    asyncio.create_task(upstream_to_client()),
                ]
                # Wait until either side disconnects, then cancel the other
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for t in pending:
                    t.cancel()

        except Exception as exc:
            await client_close(1011, f"Proxy error: {exc}")

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the synchronous HTTP client."""
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None

    async def aclose(self) -> None:
        """Close the asynchronous HTTP client."""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None
