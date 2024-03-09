# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import asyncio
import json
import websockets
import logging, verboselogs
from typing import Dict, Union, Optional

from ....options import DeepgramClientOptions
from ..enums import LiveTranscriptionEvents
from ..helpers import convert_to_websocket_url, append_query_params
from ..errors import DeepgramError, DeepgramWebsocketError

from .response import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    ErrorResponse,
    CloseResponse,
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
        self.exit_event = None

    # starts the WebSocket connection for live transcription
    async def start(
        self,
        options: Optional[Union[LiveOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        self.logger.debug("AsyncLiveClient.start ENTER")
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        self.logger.info("members: %s", members)
        self.logger.info("kwargs: %s", kwargs)

        if isinstance(options, LiveOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            raise DeepgramError("Fatal transcription options error")

        if self._socket is not None:
            self.logger.error("socket is already initialized")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            raise DeepgramWebsocketError("Websocket already started")

        self.options = options
        self.addons = addons

        # add "members" as members of the class
        if members is not None:
            self.__dict__.update(members)

        # set kwargs as members of the class
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
        self.exit_event = asyncio.Event()

        try:
            self._socket = await _socket_connect(url_with_params, self.config.headers)

            self._listen_thread = asyncio.create_task(self._listening())
            self._keep_alive_thread = asyncio.create_task(self._keep_alive())

            # push open event
            await self._emit(
                LiveTranscriptionEvents.Open,
                OpenResponse(type=LiveTranscriptionEvents.Open.value),
            )

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

        while True:
            try:
                if self.exit_event.is_set():
                    self.logger.notice("_listening exiting gracefully")
                    self.logger.debug("AsyncLiveClient._listening LEAVE")
                    return

                if self._socket is None:
                    self.logger.warning("socket is empty")
                    self.logger.debug("AsyncLiveClient._listening LEAVE")
                    return

                message = await self._socket.recv()

                if message is None:
                    self.logger.spam("message is None")
                    continue

                data = json.loads(message)
                response_type = data.get("type")
                self.logger.debug("response_type: %s, data: %s", response_type, data)

                match response_type:
                    case LiveTranscriptionEvents.Open.value:
                        result = OpenResponse.from_json(message)
                        self.logger.verbose("OpenResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Open,
                            open=result,
                            **dict(self.kwargs),
                        )
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
                    case LiveTranscriptionEvents.Close.value:
                        result = CloseResponse.from_json(message)
                        self.logger.verbose("CloseResponse: %s", result)
                        await self._emit(
                            LiveTranscriptionEvents.Close,
                            close=result,
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

            except websockets.exceptions.WebSocketException as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "WebSocketException in AsyncLiveClient._listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.notice(
                    f"WebSocket exception in AsyncLiveClient._listening with code {e.code}: {e.reason}"
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
                    "description": "Exception in AsyncLiveClient._listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error("Exception in AsyncLiveClient._listening: %s", str(e))
                await self._emit(LiveTranscriptionEvents.Error, error)

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
            try:
                counter += 1
                await asyncio.sleep(ONE_SECOND)

                if self.exit_event.is_set():
                    self.logger.notice("_keep_alive exiting gracefully")
                    self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                    return

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

            except websockets.exceptions.ConnectionClosedOK as e:
                self.logger.notice(f"_keep_alive({e.code}) exiting gracefully")
                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                return

            except websockets.exceptions.WebSocketException as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "WebSocketException in AsyncLiveClient._keep_alive",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error(
                    f"WebSocket connection closed in AsyncLiveClient._keep_alive with code {e.code}: {e.reason}"
                )
                await self._emit(LiveTranscriptionEvents.Error, error)

                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

                if (
                    "termination_exception" in self.options
                    and self.options["termination_exception"] == "true"
                ):
                    raise
                return

            except Exception as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Exception in _keep_alive",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error(
                    "Exception in AsyncLiveClient._keep_alive: %s", str(e)
                )
                await self._emit(LiveTranscriptionEvents.Error, error)

                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

                if (
                    "termination_exception" in self.options
                    and self.options["termination_exception"] == "true"
                ):
                    raise
                return

        self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

    # sends data over the WebSocket connection
    async def send(self, data: Union[str, bytes]) -> bool:
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("AsyncLiveClient.send ENTER")

        if self._socket is not None:
            try:
                await self._socket.send(data)
            except websockets.exceptions.WebSocketException as e:
                self.logger.error("send() failed - WebSocketException: %s", str(e))
                self.logger.spam("AsyncLiveClient.send LEAVE")
                return False
            except Exception as e:
                self.logger.error("send() failed - Exception: %s", str(e))
                self.logger.spam("AsyncLiveClient.send LEAVE")
                return False

            self.logger.spam(f"send() succeeded")
            self.logger.spam("AsyncLiveClient.send LEAVE")
            return True

        self.logger.error("send() failed. socket is None")
        self.logger.spam("AsyncLiveClient.send LEAVE")
        return False

    async def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.debug("AsyncLiveClient.finish ENTER")

        # signal exit
        self.exit_event.set()

        # close the stream
        self.logger.verbose("closing socket...")
        if self._socket is not None:
            self.logger.verbose("send CloseStream...")
            await self._socket.send(json.dumps({"type": "CloseStream"}))

            await asyncio.sleep(0.5)

            # push close event
            await self._emit(
                LiveTranscriptionEvents.Close,
                CloseResponse(type=LiveTranscriptionEvents.Close.value),
            )

            self.logger.verbose("socket.wait_closed...")
            try:
                await self._socket.wait_closed()
            except websockets.exceptions.WebSocketException as e:
                self.logger.error("socket.wait_closed failed: %s", e)
        self._socket = None

        self.logger.verbose("cancelling tasks...")
        try:
            # Before cancelling, check if the tasks were created
            if self._listen_thread is not None:
                self._listen_thread.cancel()
            if self._keep_alive_thread is not None:
                self._keep_alive_thread.cancel()

            # Use asyncio.gather to wait for tasks to be cancelled
            tasks = [self._listen_thread, self._keep_alive_thread]
            await asyncio.gather(*filter(None, tasks), return_exceptions=True)

        except asyncio.CancelledError as e:
            self.logger.error("tasks cancelled error: %s", e)

        self.logger.info("finish succeeded")
        self.logger.debug("AsyncLiveClient.finish LEAVE")
        return True


async def _socket_connect(websocket_url, headers) -> websockets.WebSocketClientProtocol:
    destination = websocket_url
    updated_headers = headers
    return await websockets.connect(
        destination, extra_headers=updated_headers, ping_interval=PING_INTERVAL
    )
