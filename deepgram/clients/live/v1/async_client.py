# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import asyncio
import json
import websockets
import logging, verboselogs
from typing import Dict, Union

from ....options import DeepgramClientOptions
from ..enums import LiveTranscriptionEvents
from ..helpers import convert_to_websocket_url, append_query_params
from ..errors import DeepgramError, DeepgramWebsocketError

from .response import (
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    ErrorResponse,
)
from .options import LiveOptions

ONE_SECOND = 1
DEEPGRAM_INTERVAL = 5
PING_INTERVAL = 20


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

    # starts the WebSocket connection for live transcription
    async def start(
        self,
        options: Union[LiveOptions, Dict] = None,
        addons: Dict = None,
        members: Dict = None,
        **kwargs,
    ) -> bool:
        self.logger.debug("AsyncLiveClient.start ENTER")
        self.logger.info("kwargs: %s", options)
        self.logger.info("addons: %s", addons)
        self.logger.info("members: %s", members)
        self.logger.info("options: %s", kwargs)

        if isinstance(options, LiveOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            raise DeepgramError("Fatal transcription options error")

        if self._socket is not None:
            self.logger.error("socket is already initialized")
            self.logger.debug("LiveClient.start LEAVE")
            raise DeepgramWebsocketError("Websocket already started")

        self.options = options
        self.addons = addons

        # add "members" as members of the class
        if members is not None:
            self.__dict__.update(members)

        # add "kwargs" as members of the class
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = dict()

        if isinstance(options, LiveOptions):
            self.logger.info("LiveOptions switching class -> dict")
            self.options = self.options.to_dict()

        combined_options = self.options
        if addons is not None:
            self.logger.info("merging addons to options")
            combined_options.update(addons)
            self.logger.info("new options: %s", combined_options)
        self.logger.debug("combined_options: %s", combined_options)

        url_with_params = append_query_params(self.websocket_url, combined_options)
        try:
            self._socket = await _socket_connect(url_with_params, self.config.headers)
            asyncio.create_task(self._listening())
            asyncio.create_task(self._keep_alive())

            self.logger.notice("start succeeded")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            return True
        except websockets.ConnectionClosed as e:
            await self._emit(LiveTranscriptionEvents.Close, e.code)
            self.logger.notice("exception: websockets.ConnectionClosed")
            self.logger.debug("AsyncLiveClient.start LEAVE")

    # registers event handlers for specific events
    def on(self, event: LiveTranscriptionEvents, handler) -> None:
        if event in LiveTranscriptionEvents and callable(handler):
            self._event_handlers[event].append(handler)

    # triggers the registered event handlers for a specific event
    async def _emit(self, event: LiveTranscriptionEvents, *args, **kwargs) -> None:
        for handler in self._event_handlers[event]:
            asyncio.create_task(handler(self, *args, **kwargs))

    # main loop for handling incoming messages
    async def _listening(self) -> None:
        self.logger.debug("AsyncLiveClient._listening ENTER")

        try:
            async for message in self._socket:
                data = json.loads(message)
                response_type = data.get("type")
                self.logger.debug("response_type: %s, data: %s", response_type, data)

                match response_type:
                    case LiveTranscriptionEvents.Transcript.value:
                        result = LiveResultResponse.from_json(message)
                        self.logger.verbose("LiveResultResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Transcript,
                            result=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Metadata.value:
                        result = MetadataResponse.from_json(message)
                        self.logger.verbose("MetadataResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Metadata,
                            metadata=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.SpeechStarted.value:
                        result = SpeechStartedResponse.from_json(message)
                        self.logger.verbose("SpeechStartedResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.SpeechStarted,
                            speech_started=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.UtteranceEnd.value:
                        result = UtteranceEndResponse.from_json(message)
                        self.logger.verbose("UtteranceEndResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.UtteranceEnd,
                            utterance_end=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Error.value:
                        result = ErrorResponse.from_json(message)
                        self.logger.verbose("LiveTranscriptionEvents: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Error,
                            error=result,
                            **dict(self.kwargs),
                        )
                    case _:
                        error = ErrorResponse(
                            type="UnhandledMessage",
                            description="Unknown message type",
                            message=f"Unhandle message type: {response_type}",
                        )
                        await self._emit(LiveTranscriptionEvents.Error, error=error)

        except websockets.exceptions.ConnectionClosedOK as e:
            self.logger.notice(f"_listening({e.code}) exiting gracefully")
            self.logger.debug("AsyncLiveClient._listening LEAVE")
            return

        except websockets.exceptions.ConnectionClosedError as e:
            error: ErrorResponse = {
                "type": "Exception",
                "description": "ConnectionClosedError in _listening",
                "message": f"{e}",
                "variant": "",
            }
            self.logger.error(
                f"WebSocket connection closed with code {e.code}: {e.reason}"
            )
            await self._emit(LiveTranscriptionEvents.Error, error)

            self.logger.debug("AsyncLiveClient._listening LEAVE")

            if (
                "termination_exception" in self.options
                and self.options["termination_exception"] == "true"
            ):
                raise

        except Exception as e:
            error: ErrorResponse = {
                "type": "Exception",
                "description": "Exception in _listening",
                "message": f"{e}",
                "variant": "",
            }
            await self._emit(LiveTranscriptionEvents.Error, error)

            self.logger.error("Exception in _listening: %s", error=error)
            self.logger.debug("AsyncLiveClient._listening LEAVE")

            if (
                "termination_exception" in self.options
                and self.options["termination_exception"] == "true"
            ):
                raise

    # keep the connection alive by sending keepalive messages
    async def _keep_alive(self) -> None:
        self.logger.debug("AsyncLiveClient._keep_alive ENTER")

        counter = 0
        while True:
            counter += 1
            await asyncio.sleep(ONE_SECOND)

            if self._socket is None:
                self.logger.notice("socket is None, exiting keep_alive")
                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                break

            # deepgram keepalive
            if (
                counter % DEEPGRAM_INTERVAL == 0
                and self.config.options.get("keepalive") == "true"
            ):
                self.logger.verbose("Sending KeepAlive...")
                await self.send(json.dumps({"type": "KeepAlive"}))

            # protocol level ping
            if counter % PING_INTERVAL == 0:
                self.logger.verbose("Sending Protocol Ping...")
                await self._socket.ping()

        self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

    # sends data over the WebSocket connection
    async def send(self, data: Union[str, bytes]) -> int:
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("AsyncLiveClient.send ENTER")
        self.logger.spam("data: %s", data)

        if self._socket is not None:
            cnt = await self._socket.send(data)
            self.logger.spam(f"send() succeeded. bytes: {cnt}")
            self.logger.spam("AsyncLiveClient.send LEAVE")
            return cnt

        self.logger.error("send() failed. socket is None")
        self.logger.spam("AsyncLiveClient.send LEAVE")
        return 0

    async def finish(self) -> bool:
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
        return True


async def _socket_connect(websocket_url, headers) -> websockets.WebSocketClientProtocol:
    destination = websocket_url
    updated_headers = headers
    return await websockets.connect(
        destination, extra_headers=updated_headers, ping_interval=5
    )
