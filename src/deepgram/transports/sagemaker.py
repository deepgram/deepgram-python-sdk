"""
SageMaker transport for the Deepgram Python SDK.

Uses AWS SageMaker's HTTP/2 bidirectional streaming API as an alternative to
WebSocket, allowing transparent switching between Deepgram Cloud and Deepgram
on SageMaker.

**Async-only** — the underlying ``sagemaker-runtime-http2`` library is entirely
async, so this transport implements ``AsyncTransport`` and must be used with
``AsyncDeepgramClient``. It cannot be used with the sync ``DeepgramClient``.

Requirements::

    pip install sagemaker-runtime-http2 boto3

Usage::

    from deepgram import AsyncDeepgramClient
    from deepgram.transports.sagemaker import SageMakerTransportFactory

    factory = SageMakerTransportFactory(
        endpoint_name="my-deepgram-endpoint",
        region="us-west-2",
    )
    client = AsyncDeepgramClient(
        api_key="unused",  # SageMaker uses AWS credentials, not API keys
        transport_factory=factory,
    )

    async with client.listen.v1.connect(model="nova-3") as connection:
        connection.on(EventType.MESSAGE, handler)
        await connection.start_listening()
"""

import asyncio
import json
import logging
import os
from typing import Any
from urllib.parse import urlparse

from ..transport_interface import AsyncTransport
from sagemaker_runtime_http2.client import SageMakerRuntimeHTTP2Client
from sagemaker_runtime_http2.config import Config, HTTPAuthSchemeResolver
from sagemaker_runtime_http2.models import (
    InvokeEndpointWithBidirectionalStreamInput,
    RequestPayloadPart,
    RequestStreamEventPayloadPart,
)
from smithy_aws_core.auth.sigv4 import SigV4AuthScheme
from smithy_aws_core.identity import EnvironmentCredentialsResolver

try:
    import boto3

    _BOTO3_AVAILABLE = True
except ImportError:
    _BOTO3_AVAILABLE = False

logger = logging.getLogger(__name__)


class SageMakerTransport(AsyncTransport):
    """SageMaker BiDi streaming transport implementing ``AsyncTransport``.

    Connection is established lazily on the first ``send()`` or ``recv()`` call,
    since the transport is constructed synchronously by the SDK's shim layer.

    Parameters
    ----------
    endpoint_name : str
        Name of the SageMaker endpoint running Deepgram.
    region : str
        AWS region where the endpoint is deployed.
    invocation_path : str
        Model invocation path (e.g. ``"v1/listen"``). Extracted from the
        WebSocket URL by :class:`SageMakerTransportFactory`.
    query_string : str
        URL-encoded query parameters (e.g. ``"model=nova-3&interim_results=true"``).
        Extracted from the WebSocket URL by :class:`SageMakerTransportFactory`.
    """

    def __init__(
        self,
        endpoint_name: str,
        region: str,
        invocation_path: str,
        query_string: str,
    ) -> None:
        self.endpoint_name = endpoint_name
        self.region = region
        self.invocation_path = invocation_path
        self.query_string = query_string
        self._stream: Any = None
        self._output_stream: Any = None
        self._connected = False
        self._closed = False

        self._setup_credentials()

    def _setup_credentials(self) -> None:
        """Resolve AWS credentials via boto3 (if available) into env vars.

        The ``EnvironmentCredentialsResolver`` used by the SageMaker HTTP/2
        client reads ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, and
        optionally ``AWS_SESSION_TOKEN`` from the environment. This method
        uses boto3's credential chain (env vars, shared credentials file,
        IAM role, etc.) and writes the resolved values back to the
        environment so the resolver can find them.
        """
        if not _BOTO3_AVAILABLE:
            return
        try:
            session = boto3.Session(region_name=self.region)
            creds = session.get_credentials()
            if creds is None:
                return
            frozen = creds.get_frozen_credentials()
            os.environ["AWS_ACCESS_KEY_ID"] = frozen.access_key
            os.environ["AWS_SECRET_ACCESS_KEY"] = frozen.secret_key
            if frozen.token:
                os.environ["AWS_SESSION_TOKEN"] = frozen.token
        except Exception as exc:
            logger.debug("Could not load boto3 credentials: %s", exc)

    async def _ensure_connected(self) -> None:
        """Lazily establish the SageMaker BiDi stream on first use."""
        if self._connected:
            return

        logger.info("Connecting to SageMaker endpoint: %s in %s", self.endpoint_name, self.region)

        config = Config(
            endpoint_uri=f"https://runtime.sagemaker.{self.region}.amazonaws.com:8443",
            region=self.region,
            aws_credentials_identity_resolver=EnvironmentCredentialsResolver(),
            auth_scheme_resolver=HTTPAuthSchemeResolver(),
            auth_schemes={"aws.auth#sigv4": SigV4AuthScheme(service="sagemaker")},
        )
        client = SageMakerRuntimeHTTP2Client(config=config)

        stream_input = InvokeEndpointWithBidirectionalStreamInput(
            endpoint_name=self.endpoint_name,
            model_invocation_path=self.invocation_path,
            model_query_string=self.query_string,
        )

        self._stream = await client.invoke_endpoint_with_bidirectional_stream(stream_input)

        # Await the output stream before sending any data (critical ordering)
        output = await asyncio.wait_for(self._stream.await_output(), timeout=10.0)
        self._output_stream = output[1]
        self._connected = True

        logger.info("Connected to SageMaker endpoint: %s", self.endpoint_name)

    async def send(self, data: Any) -> None:
        """Send text, bytes, or dict data to SageMaker.

        The SDK calls this with:
        - ``bytes`` for audio media (from ``send_media``)
        - ``str`` for JSON control messages (from ``_send_model`` after ``json.dumps``)
        """
        await self._ensure_connected()

        if isinstance(data, (bytes, bytearray)):
            raw = bytes(data)
        elif isinstance(data, str):
            raw = data.encode("utf-8")
        elif isinstance(data, dict):
            raw = json.dumps(data).encode("utf-8")
        else:
            raw = str(data).encode("utf-8")

        payload = RequestPayloadPart(bytes_=raw)
        event = RequestStreamEventPayloadPart(value=payload)
        await self._stream.input_stream.send(event)

    async def recv(self) -> Any:
        """Receive the next message from SageMaker.

        Returns a decoded UTF-8 string when possible (so the SDK can
        JSON-parse it), or raw bytes for binary data. Returns ``None``
        when the stream ends.
        """
        await self._ensure_connected()

        result = await self._output_stream.receive()
        if result is None:
            return None

        if result.value and result.value.bytes_:
            raw = result.value.bytes_
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError:
                return raw

        return None

    async def __aiter__(self):
        """Async-iterate over messages until the stream ends.

        The SDK's ``start_listening()`` drives the event loop by calling
        ``async for raw_message in self._websocket:``, which invokes this
        method on the transport.
        """
        while not self._closed:
            msg = await self.recv()
            if msg is None:
                break
            yield msg

    async def close(self) -> None:
        """Close the SageMaker stream and release resources."""
        if self._closed:
            return
        self._closed = True
        if self._stream:
            try:
                await self._stream.input_stream.close()
            except Exception:
                pass
        logger.info("Closed SageMaker connection: %s", self.endpoint_name)


class SageMakerTransportFactory:
    """Factory callable for ``AsyncDeepgramClient(transport_factory=...)``.

    **Async-only** — must be used with ``AsyncDeepgramClient``, not the sync
    ``DeepgramClient``. Passing this factory to ``DeepgramClient`` will raise
    a ``TypeError``.

    When the SDK calls ``factory(url, headers)``, this extracts the invocation
    path and query string from the URL and creates a :class:`SageMakerTransport`.

    The URL is the WebSocket URL the SDK would normally connect to, e.g.::

        wss://api.deepgram.com/v1/listen?model=nova-3&interim_results=true

    From this, the factory extracts:
    - ``invocation_path`` = ``"v1/listen"``
    - ``query_string`` = ``"model=nova-3&interim_results=true"``

    Parameters
    ----------
    endpoint_name : str
        Name of the SageMaker endpoint running Deepgram.
    region : str
        AWS region (default ``"us-west-2"``).

    Example
    -------
    ::

        from deepgram import AsyncDeepgramClient
        from deepgram.transports.sagemaker import SageMakerTransportFactory

        factory = SageMakerTransportFactory("my-endpoint", region="us-east-1")
        client = AsyncDeepgramClient(api_key="unused", transport_factory=factory)

        async with client.listen.v1.connect(model="nova-3") as connection:
            connection.on(EventType.MESSAGE, handler)
            await connection.start_listening()
    """

    _SYNC_ERROR = (
        "SageMakerTransportFactory is async-only and cannot be used with the "
        "sync DeepgramClient. Use AsyncDeepgramClient instead."
    )

    def __init__(self, endpoint_name: str, region: str = "us-west-2") -> None:
        self.endpoint_name = endpoint_name
        self.region = region

    def __call__(self, url: str, headers: dict) -> SageMakerTransport:
        """Create a transport instance from the SDK-provided WebSocket URL.

        Raises
        ------
        TypeError
            If called outside an async context (i.e. from the sync
            ``DeepgramClient``), since SageMaker streaming is async-only.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            raise TypeError(self._SYNC_ERROR) from None

        parsed = urlparse(url)
        # Strip leading slash — SageMaker expects "v1/listen" not "/v1/listen"
        invocation_path = parsed.path.lstrip("/")
        query_string = parsed.query  # already URL-encoded

        return SageMakerTransport(
            endpoint_name=self.endpoint_name,
            region=self.region,
            invocation_path=invocation_path,
            query_string=query_string,
        )
