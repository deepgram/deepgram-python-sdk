# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import asyncio
import json
import websockets
import logging, verboselogs

from ....options import DeepgramClientOptions
from ..enums import LiveTranscriptionEvents
from ..helpers import convert_to_websocket_url, append_query_params
from ..errors import DeepgramError

from .response import (
    LiveResultResponse,
    MetadataResponse,
    UtteranceEndResponse,
    ErrorResponse,
)
from .options import LiveOptions


class AsyncLiveClient:
    """
    Client for interacting with Deepgram's live transcription services over WebSockets.

     This class provides methods to establish a WebSocket connection for live transcription and handle real-time transcription events.

     Args:
         config (DeepgramClientOptions): all the options for the client.
    """

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config are required")

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)

        self.config = config
        self.endpoint = "v1/listen"
        self._socket = None
        self._event_handlers = {event: [] for event in LiveTranscriptionEvents}
        self.websocket_url = convert_to_websocket_url(self.config.url, self.endpoint)

    async def start(self, options: LiveOptions = None, addons: dict = None, **kwargs):
        self.logger.debug("AsyncLiveClient.start ENTER")
        self.logger.info("kwargs: %s", options)
        self.logger.info("addons: %s", addons)
        self.logger.info("options: %s", kwargs)

        if options is not None and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self.options = options
        if addons is not None:
            self.__dict__.update(addons)
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = dict()

        if isinstance(options, LiveOptions):
            self.logger.info("LiveOptions switching class -> json")
            self.options = self.options.to_dict()

        url_with_params = append_query_params(self.websocket_url, self.options)
        try:
            self._socket = await _socket_connect(url_with_params, self.config.headers)
            asyncio.create_task(self._start())

            self.logger.notice("start succeeded")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            return self
        except websockets.ConnectionClosed as e:
            await self._emit(LiveTranscriptionEvents.Close, e.code)
            self.logger.notice("exception: websockets.ConnectionClosed")
            self.logger.debug("AsyncLiveClient.start LEAVE")

    def on(self, event, handler):
        """
        Registers event handlers for specific events.
        """
        if event in LiveTranscriptionEvents and callable(handler):
            self._event_handlers[event].append(handler)

    async def _emit(
        self, event, *args, **kwargs
    ):  # triggers the registered event handlers for a specific event
        for handler in self._event_handlers[event]:
            await handler(self, *args, **kwargs)

    async def _start(self) -> None:
        self.logger.debug("AsyncLiveClient._start ENTER")

        async for message in self._socket:
            try:
                data = json.loads(message)
                response_type = data.get("type")
                match response_type:
                    case LiveTranscriptionEvents.Transcript.value:
                        self.logger.debug(
                            "response_type: %s, data: %s", response_type, data
                        )
                        result = LiveResultResponse.from_json(message)
                        if result is None:
                            self.logger.error("LiveResultResponse.from_json is None")
                            continue
                        self.logger.verbose("result: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Transcript,
                            result=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Metadata.value:
                        self.logger.debug(
                            "response_type: %s, data: %s", response_type, data
                        )
                        result = MetadataResponse.from_json(message)
                        if result is None:
                            self.logger.error("MetadataResponse.from_json is None")
                            continue
                        self.logger.verbose("result: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Metadata,
                            metadata=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.UtteranceEnd.value:
                        self.logger.debug(
                            "response_type: %s, data: %s", response_type, data
                        )
                        result = UtteranceEndResponse.from_json(message)
                        if result is None:
                            self.logger.error("UtteranceEndResponse.from_json is None")
                            continue
                        self.logger.verbose("result: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.UtteranceEnd,
                            utterance_end=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Error.value:
                        self.logger.debug(
                            "response_type: %s, data: %s", response_type, data
                        )
                        result = ErrorResponse.from_json(message)
                        if result is None:
                            self.logger.error("ErrorResponse.from_json is None")
                            continue
                        self.logger.verbose("result: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Error,
                            error=result,
                            **dict(self.kwargs),
                        )
                    case _:
                        self.logger.error(
                            "response_type: %s, data: %s", response_type, data
                        )
                        error = ErrorResponse(
                            type="UnhandledMessage",
                            description="Unknown message type",
                            message=f"Unhandle message type: {response_type}",
                        )
                        await self._emit(LiveTranscriptionEvents.Error, error=error)
            except json.JSONDecodeError as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error("exception: json.JSONDecodeError: %s", str(e))
                await self._emit(LiveTranscriptionEvents.Error, error=error)
                self.logger.debug("AsyncLiveClient._start LEAVE")
            except websockets.exceptions.ConnectionClosedOK as e:
                if e.code == 1000:
                    self.logger.notice("_start(1000) exiting gracefully")
                    self.logger.debug("AsyncLiveClient._start LEAVE")
                    return
                else:
                    error: ErrorResponse = {
                        "type": "Exception",
                        "description": "Unknown error _start",
                        "message": f"{e}",
                        "variant": "",
                    }
                    self.logger.error(
                        f"WebSocket connection closed with code {e.code}: {e.reason}"
                    )
                    self._emit(LiveTranscriptionEvents.Error, error=error)
                    self.logger.debug("AsyncLiveClient._start LEAVE")
                    raise
            except Exception as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _start",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)
                self.logger.error("Exception in _start: %s", error=error)
                self.logger.debug("AsyncLiveClient._start LEAVE")
                raise

    async def send(self, data):
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("AsyncLiveClient.send ENTER")
        self.logger.spam("data: %s", data)

        if self._socket:
            await self._socket.send(data)
            self.logger.spam("data sent")

        self.logger.spam("AsyncLiveClient.send LEAVE")

    async def finish(self):
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.debug("AsyncLiveClient.finish LEAVE")

        if self._socket:
            self.logger.notice("send CloseStream...")
            await self._socket.send(json.dumps({"type": "CloseStream"}))
            self.logger.notice("socket.wait_closed...")
            await self._socket.wait_closed()
            self.logger.notice("socket.wait_closed succeeded")

        self._socket = None

        self.logger.notice("finish succeeded")
        self.logger.debug("AsyncLiveClient.finish LEAVE")


async def _socket_connect(websocket_url, headers):
    destination = websocket_url
    updated_headers = headers
    return await websockets.connect(
        destination, extra_headers=updated_headers, ping_interval=5
    )
