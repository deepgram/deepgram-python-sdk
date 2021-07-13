from __future__ import annotations

from ._types import Options, PrerecordedOptions, LiveOptions, TranscriptionSource, PrerecordedTranscriptionResponse, LiveTranscriptionResponse, Metadata, EventHandler
from ._enums import LiveTranscriptionEvent
from ._utils import _request, _make_query_string, _socket_connect
from typing import Any, Union, Tuple, List
import json, asyncio, inspect
from enum import Enum
import websockets.client

class PrerecordedTranscription:
    _root = "/listen"

    def __init__(self, options: Options, transcription_options: PrerecordedOptions) -> None:
        self.options = options
        self.transcription_options = transcription_options
    async def __call__(self, source: TranscriptionSource) -> PrerecordedTranscriptionResponse:
        if 'buffer' in source and 'mimetype' not in source:
            raise Exception('DG: Mimetype must be provided if the source is bytes')
        payload = source.get('buffer', {'url': source.get('url')}) 
        return await _request(f'{self._root}{_make_query_string(self.transcription_options)}', self.options, method='POST', payload=payload, headers={'Content-Type': source['mimetype'] or 'audio/wav'})

class LiveTranscription:
    _root = "/listen"

    def __init__(self, options: Options, transcription_options: LiveOptions) -> None:
        self.options = options
        self.transcription_options = transcription_options
        self.handlers: List[EventHandler] = []
        self.received: List = [] # all received messages
        self.done: bool = False # is the transcription job done?
        self._socket: Union[None, websockets.client.WebSocketClientProtocol] = None
        self._queue: asyncio.Queue[Tuple[bool, Any]] = asyncio.Queue()

    async def __call__(self) -> LiveTranscription:
        self._socket = await _socket_connect(f'{self._root}{_make_query_string(self.transcription_options)}', self.options)
        asyncio.create_task(self._start())
        return self

    async def _start(self) -> None:
        asyncio.create_task(self._receiver())
        self._pingHandlers(LiveTranscriptionEvent.OPEN, self)
        while not self.done:
            incoming, body = await self._queue.get()
            if incoming:
                try:
                    parsed: Union[LiveTranscriptionResponse, Metadata] = json.loads(body)
                    # Stream-ending response is only a metadata object
                    self._pingHandlers(LiveTranscriptionEvent.TRANSCRIPT_RECEIVED, parsed)
                    self.received.append(parsed)
                    if 'transaction_key' in parsed:
                        self.done = True
                except json.decoder.JSONDecodeError:
                    self._pingHandlers(LiveTranscriptionEvent.ERROR, f'Couldn\'t parse response JSON: {body}')
            else:
                await self._socket.send(body)
        self._pingHandlers(LiveTranscriptionEvent.CLOSE, self._socket.close_code)

    async def _receiver(self) -> None:
        while not self.done:
            try:
                body = await self._socket.recv()
                self._queue.put_nowait((True, body))
            except:
                pass # socket closed, will terminate on next loop

    def _pingHandlers(self, event_type: LiveTranscriptionEvent, body: Any) -> None:
        for handled_type, func in self.handlers:
            if handled_type is event_type:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(body))
                else:
                    func(body)

    # Public

    def registerHandler(self, event_type: LiveTranscriptionEvent, handler: EventHandler) -> None:
        """Adds an event handler to the transcription client."""
        self.handlers.append((event_type, handler))

    def deregisterHandler(self, event_type: LiveTranscriptionEvent, handler: EventHandler) -> None:
        """Removes an event handler from the transcription client."""
        self.handlers.remove((event_type, handler))

    def send(self, data: Union[bytes, str]) -> None:
        """Sends data to the Deepgram endpoint."""
        self._queue.put_nowait((False, data))

    async def finish(self) -> None:
        """Closes the connection to the Deepgram endpoint, waiting until ASR is complete on all submitted data."""
        self.send(b'') # Set message for "data is finished sending"
        while not self.done:
            await asyncio.sleep(0.1)

    @property
    def event(self) -> Enum:
        """An enum representing different possible transcription events that handlers can be registered against."""
        return LiveTranscriptionEvent

class Transcription:
    def __init__(self, options: Options) -> None:
        self.options = options

    async def prerecorded(self, source: TranscriptionSource, options: PrerecordedOptions = {}) -> PrerecordedTranscriptionResponse:
        """Retrieves a transcription for an already-existing audio file, local or web-hosted."""
        return await PrerecordedTranscription(self.options, options)(source)

    async def live(self, options: LiveOptions = {}) -> LiveTranscription:
        """Provides a client to send raw audio data to be transcribed."""
        return await LiveTranscription(self.options, options)()
