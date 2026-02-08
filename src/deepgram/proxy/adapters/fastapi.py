"""FastAPI adapter for the Deepgram proxy."""

from typing import TYPE_CHECKING

from ..errors import ProxyError

if TYPE_CHECKING:
    from ..engine import DeepgramProxy
    from fastapi import APIRouter


def create_deepgram_router(proxy: "DeepgramProxy") -> "APIRouter":
    """Create a FastAPI APIRouter that proxies requests to Deepgram.

    Usage::

        from fastapi import FastAPI
        from deepgram.proxy import DeepgramProxy
        from deepgram.proxy.adapters.fastapi import create_deepgram_router

        proxy = DeepgramProxy(api_key="dg-xxx")
        app = FastAPI()
        app.include_router(create_deepgram_router(proxy), prefix="/deepgram")
    """
    from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect

    router = APIRouter()

    @router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    async def proxy_rest(request: Request, path: str) -> Response:
        full_path = f"/{path}"
        authorization = request.headers.get("authorization")

        try:
            scopes = proxy.authenticate(authorization)
            proxy.authorize(full_path, scopes)
        except ProxyError as exc:
            return Response(content=exc.message, status_code=exc.status_code)

        headers = dict(request.headers)
        body = await request.body()
        query_string = str(request.query_params)

        try:
            status, resp_headers, resp_body = await proxy.forward_rest_async(
                method=request.method,
                path=full_path,
                headers=headers,
                query_string=query_string,
                body=body,
            )
        except ProxyError as exc:
            return Response(content=exc.message, status_code=exc.status_code)

        return Response(content=resp_body, status_code=status, headers=resp_headers)

    @router.websocket("/{path:path}")
    async def proxy_websocket(ws: WebSocket, path: str) -> None:
        full_path = f"/{path}"

        # Extract subprotocol from Sec-WebSocket-Protocol header
        subprotocol = ws.headers.get("sec-websocket-protocol")

        await ws.accept(subprotocol=subprotocol)

        async def client_receive():
            try:
                data = await ws.receive()
                if data.get("type") == "websocket.disconnect":
                    return None
                return data.get("text") or data.get("bytes")
            except WebSocketDisconnect:
                return None

        async def client_send(msg):
            if isinstance(msg, bytes):
                await ws.send_bytes(msg)
            else:
                await ws.send_text(str(msg))

        async def client_close(code: int, reason: str = ""):
            try:
                await ws.close(code=code, reason=reason)
            except Exception:
                pass

        query_string = str(ws.query_params)

        await proxy.forward_websocket(
            path=full_path,
            query_string=query_string,
            client_receive=client_receive,
            client_send=client_send,
            client_close=client_close,
            subprotocol=subprotocol,
        )

    return router
