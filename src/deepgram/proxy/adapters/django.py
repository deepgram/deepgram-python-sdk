"""Django adapter for the Deepgram proxy."""

import asyncio
from typing import TYPE_CHECKING, Any, List

from ..errors import ProxyError

if TYPE_CHECKING:
    from ..engine import DeepgramProxy


def deepgram_proxy_urls(proxy: "DeepgramProxy") -> List[Any]:
    """Create Django URL patterns that proxy requests to Deepgram.

    REST views are CSRF-exempt. Optional WebSocket support requires
    Django Channels (``pip install channels``).

    Usage::

        from django.urls import path, include
        from deepgram.proxy import DeepgramProxy
        from deepgram.proxy.adapters.django import deepgram_proxy_urls

        proxy = DeepgramProxy(api_key="dg-xxx")
        urlpatterns = [path("deepgram/", include(deepgram_proxy_urls(proxy)))]

    Returns:
        List of URL patterns. If Django Channels is installed, the list also
        has a ``websocket_consumer`` attribute containing the ASGI consumer class.
    """
    from django.http import HttpRequest, HttpResponse
    from django.urls import re_path
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def proxy_rest(request: HttpRequest, path: str) -> HttpResponse:
        full_path = f"/{path}"
        authorization = request.headers.get("Authorization")

        try:
            scopes = proxy.authenticate(authorization)
            proxy.authorize(full_path, scopes)
        except ProxyError as exc:
            return HttpResponse(exc.message, status=exc.status_code)

        headers = dict(request.headers)
        body = request.body
        query_string = request.META.get("QUERY_STRING", "")

        try:
            status, resp_headers, resp_body = proxy.forward_rest_sync(
                method=request.method,
                path=full_path,
                headers=headers,
                query_string=query_string,
                body=body,
            )
        except ProxyError as exc:
            return HttpResponse(exc.message, status=exc.status_code)

        response = HttpResponse(resp_body, status=status)
        for k, v in resp_headers.items():
            if k.lower() not in ("content-length", "content-encoding"):
                response[k] = v
        return response

    patterns: Any = [
        re_path(r"^(?P<path>.+)$", proxy_rest, name="deepgram_proxy_rest"),
    ]

    # Optional WebSocket support via Django Channels
    try:
        from channels.generic.websocket import AsyncWebsocketConsumer

        class DeepgramProxyConsumer(AsyncWebsocketConsumer):
            """ASGI WebSocket consumer for Deepgram proxy."""

            async def connect(self) -> None:
                self._path = "/" + self.scope.get("path", "").lstrip("/")
                # Remove the URL prefix to get the API path
                query_string = self.scope.get("query_string", b"").decode("utf-8")
                subprotocol = None
                for header_name, header_value in self.scope.get("headers", []):
                    if header_name == b"sec-websocket-protocol":
                        subprotocol = header_value.decode("utf-8")
                        break

                self._subprotocol = subprotocol
                self._query_string = query_string
                self._message_queue: asyncio.Queue = asyncio.Queue()

                await self.accept(subprotocol=subprotocol)

                # Start the relay
                asyncio.ensure_future(self._relay())

            async def _relay(self) -> None:
                async def client_receive():
                    msg = await self._message_queue.get()
                    return msg

                async def client_send(msg):
                    if isinstance(msg, bytes):
                        await self.send(bytes_data=msg)
                    else:
                        await self.send(text_data=str(msg))

                async def client_close(code: int, reason: str = ""):
                    await self.close(code=code)

                await proxy.forward_websocket(
                    path=self._path,
                    query_string=self._query_string,
                    client_receive=client_receive,
                    client_send=client_send,
                    client_close=client_close,
                    subprotocol=self._subprotocol,
                )

            async def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:  # type: ignore[assignment]
                await self._message_queue.put(text_data or bytes_data)

            async def disconnect(self, close_code: int) -> None:
                await self._message_queue.put(None)

        patterns.websocket_consumer = DeepgramProxyConsumer  # type: ignore[attr-defined]

    except ImportError:
        pass  # Django Channels not installed

    return patterns
