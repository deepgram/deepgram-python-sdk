"""Flask adapter for the Deepgram proxy."""

import asyncio
from typing import TYPE_CHECKING

from ..errors import ProxyError

if TYPE_CHECKING:
    from ..engine import DeepgramProxy
    from flask import Blueprint


def create_deepgram_blueprint(proxy: "DeepgramProxy") -> "Blueprint":
    """Create a Flask Blueprint that proxies requests to Deepgram.

    REST requests use synchronous forwarding. WebSocket support requires
    ``flask-sock`` (``pip install flask-sock``).

    Usage::

        from flask import Flask
        from deepgram.proxy import DeepgramProxy
        from deepgram.proxy.adapters.flask import create_deepgram_blueprint

        proxy = DeepgramProxy(api_key="dg-xxx")
        app = Flask(__name__)
        app.register_blueprint(create_deepgram_blueprint(proxy), url_prefix="/deepgram")
    """
    from flask import Blueprint, Response, request

    bp = Blueprint("deepgram_proxy", __name__)

    @bp.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    def proxy_rest(path: str) -> Response:
        full_path = f"/{path}"
        authorization = request.headers.get("Authorization")

        try:
            scopes = proxy.authenticate(authorization)
            proxy.authorize(full_path, scopes)
        except ProxyError as exc:
            return Response(exc.message, status=exc.status_code)

        headers = dict(request.headers)
        body = request.get_data()
        query_string = request.query_string.decode("utf-8")

        try:
            status, resp_headers, resp_body = proxy.forward_rest_sync(
                method=request.method,
                path=full_path,
                headers=headers,
                query_string=query_string,
                body=body,
            )
        except ProxyError as exc:
            return Response(exc.message, status=exc.status_code)

        return Response(resp_body, status=status, headers=resp_headers)

    # Optional WebSocket support via flask-sock
    try:
        from flask_sock import Sock

        sock = Sock()

        @sock.route("/<path:path>", bp=bp)
        def proxy_websocket(ws, path: str) -> None:  # type: ignore[no-untyped-def]
            full_path = f"/{path}"

            # flask-sock doesn't expose subprotocol headers easily;
            # read from the underlying environ
            subprotocol = ws.environ.get("HTTP_SEC_WEBSOCKET_PROTOCOL")
            query_string = ws.environ.get("QUERY_STRING", "")

            loop = asyncio.new_event_loop()

            async def client_receive():
                try:
                    data = await loop.run_in_executor(None, ws.receive)
                    return data
                except Exception:
                    return None

            async def client_send(msg):
                await loop.run_in_executor(None, ws.send, msg)

            async def client_close(code: int, reason: str = ""):
                try:
                    await loop.run_in_executor(None, ws.close, code, reason)
                except Exception:
                    pass

            try:
                loop.run_until_complete(
                    proxy.forward_websocket(
                        path=full_path,
                        query_string=query_string,
                        client_receive=client_receive,
                        client_send=client_send,
                        client_close=client_close,
                        subprotocol=subprotocol,
                    )
                )
            finally:
                loop.close()

    except ImportError:
        pass  # flask-sock not installed; WS support unavailable

    return bp
