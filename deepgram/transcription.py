from typing import Any, Union, Tuple, List, Dict, Awaitable, cast
import json
import asyncio
import inspect
from enum import Enum
from warnings import warn
import websockets.client
from ._types import (Options, PrerecordedOptions, LiveOptions,
                     TranscriptionSource, PrerecordedTranscriptionResponse,
                     LiveTranscriptionResponse, Metadata, EventHandler)
from ._enums import LiveTranscriptionEvent
from ._utils import _request, _make_query_string, _socket_connect


class PrerecordedTranscription:
    _root = "/listen"

    def __init__(self, options: Options,
                 transcription_options: PrerecordedOptions) -> None:
        self.options = options
        self.transcription_options = transcription_options

    async def __call__(
        self, source: TranscriptionSource
    ) -> PrerecordedTranscriptionResponse:
        if 'buffer' in source and 'mimetype' not in source:
            raise Exception(
                'DG: Mimetype must be provided if the source is bytes'
            )
        payload = cast(
            Union[bytes, Dict],
            source.get('buffer', {'url': source.get('url')})
        )
        content_type = cast(str, source.get('mimetype', 'application/json'))
        return await _request(
            f'{self._root}{_make_query_string(self.transcription_options)}',
            self.options, method='POST', payload=payload,
            headers={'Content-Type': content_type}
        )


class LiveTranscription:
    _root = "/listen"
    MESSAGE_TIMEOUT = 1.0

    def __init__(self, options: Options,
                 transcription_options: LiveOptions) -> None:
        self.options = options
        self.transcription_options = transcription_options
        self.handlers: List[Tuple[LiveTranscriptionEvent, EventHandler]] = []
        # all received messages
        self.received: List[Union[LiveTranscriptionResponse, Metadata]] = []
        # is the transcription job done?
        self.done = False
        self._socket = cast(websockets.client.WebSocketClientProtocol, None)
        self._queue: asyncio.Queue[Tuple[bool, Any]] = asyncio.Queue()

    async def __call__(self) -> 'LiveTranscription':
        self._socket = await _socket_connect(
            f'{self._root}{_make_query_string(self.transcription_options)}',
            self.options
        )
        asyncio.create_task(self._start())
        return self

    async def _start(self) -> None:
        asyncio.create_task(self._receiver())
        self._ping_handlers(LiveTranscriptionEvent.OPEN, self)

        while not self.done:
            try:
                incoming, body = await asyncio.wait_for(self._queue.get(), self.MESSAGE_TIMEOUT)
            except asyncio.TimeoutError:
                if self._socket.closed:
                    self.done = True
                    break
                continue

            if incoming:
                try:
                    parsed: Union[
                        LiveTranscriptionResponse, Metadata
                    ] = json.loads(body)
                    # Stream-ending response is only a metadata object
                    self._ping_handlers(
                        LiveTranscriptionEvent.TRANSCRIPT_RECEIVED,
                        parsed
                    )
                    self.received.append(parsed)
                    if 'sha256' in parsed: 
                        self.done = True
                except json.decoder.JSONDecodeError:
                    self._ping_handlers(
                        LiveTranscriptionEvent.ERROR,
                        f'Couldn\'t parse response JSON: {body}'
                    )
            else:
                await self._socket.send(body)
        self._ping_handlers(
            LiveTranscriptionEvent.CLOSE,
            self._socket.close_code
        )

    async def _receiver(self) -> None:
        while not self.done:
            try:
                body = await self._socket.recv()
                self._queue.put_nowait((True, body))
            except Exception as exc:
                self.done = True # socket closed, will terminate on next loop

    def _ping_handlers(self, event_type: LiveTranscriptionEvent,
                       body: Any) -> None:
        for handled_type, func in self.handlers:
            if handled_type is event_type:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(cast(Awaitable[None], func(body)))
                else:
                    func(body)

    # Public

    def register_handler(self, event_type: LiveTranscriptionEvent,
                         handler: EventHandler) -> None:
        """Adds an event handler to the transcription client."""
        self.handlers.append((event_type, handler))

    # alias for incorrect method name in v0.1.x
    def registerHandler(self, *args, **kwargs):
        warn(
            (
                "This method name is deprecated, "
                "and will be removed in the future - "
                "use `register_handler`."
            ),
            DeprecationWarning
        )
        return self.register_handler(*args, **kwargs)

    def deregister_handler(self, event_type: LiveTranscriptionEvent,
                           handler: EventHandler) -> None:
        """Removes an event handler from the transcription client."""
        self.handlers.remove((event_type, handler))

    # alias for incorrect method name in v0.1.x
    def deregisterHandler(self, *args, **kwargs):
        warn(
            (
                "This method name is deprecated, "
                "and will be removed in the future - "
                "use `deregister_handler`."
            ),
            DeprecationWarning
        )
        return self.deregister_handler(*args, **kwargs)

    def send(self, data: Union[bytes, str]) -> None:
        """Sends data to the Deepgram endpoint."""
        self._queue.put_nowait((False, data))

    async def finish(self) -> None:
        """Closes the connection to the Deepgram endpoint,
        waiting until ASR is complete on all submitted data."""
        self.send(b'')  # Set message for "data is finished sending"
        while not self.done:
            await asyncio.sleep(0.1)

    @property
    def event(self) -> Enum:
        """An enum representing different possible transcription events
        that handlers can be registered against."""
        return cast(Enum, LiveTranscriptionEvent)


class Transcription:
    def __init__(self, options: Options) -> None:
        self.options = options

    async def prerecorded(
        self, source: TranscriptionSource,
        options: PrerecordedOptions = None, **kwargs
    ) -> PrerecordedTranscriptionResponse:
        """Retrieves a transcription for an already-existing audio file,
        local or web-hosted."""
        if options is None:
            options = {}
        full_options = cast(PrerecordedOptions, {**options, **kwargs})
        return await PrerecordedTranscription(
            self.options, full_options
        )(source)

    async def live(
        self, options: LiveOptions = None, **kwargs
    ) -> LiveTranscription:
        """Provides a client to send raw audio data to be transcribed."""
        if options is None:
            options = {}
        full_options = cast(LiveOptions, {**options, **kwargs})
        return await LiveTranscription(
            self.options, full_options
        )()
