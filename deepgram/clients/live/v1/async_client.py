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
        self._exit_event = None
        self._event_handlers = {event: [] for event in LiveTranscriptionEvents}
        self.websocket_url = convert_to_websocket_url(self.config.url, self.endpoint)

    # starts the WebSocket connection for live transcription
    async def start(
        self,
        options: Optional[Union[LiveOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for live transcription.
        """
        self.logger.debug("AsyncLiveClient.start ENTER")
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        self.logger.info("headers: %s", headers)
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
        self.headers = headers

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
            combined_options.update(self.addons)
            self.logger.info("new options: %s", combined_options)
        self.logger.debug("combined_options: %s", combined_options)

        combined_headers = self.config.headers
        if headers is not None:
            self.logger.info("merging headers to options")
            combined_headers.update(self.headers)
            self.logger.info("new headers: %s", combined_headers)
        self.logger.debug("combined_headers: %s", combined_headers)

        url_with_params = append_query_params(self.websocket_url, combined_options)

        try:
            self._socket = await websockets.connect(
                url_with_params,
                extra_headers=combined_headers,
                ping_interval=PING_INTERVAL,
            )
            self._exit_event = asyncio.Event()

            # listen thread
            self._listen_thread = asyncio.create_task(self._listening())

            # keepalive thread
            if self.config.options.get("keepalive") == "true":
                self.logger.notice("keepalive is disabled")
                self._keep_alive_thread = asyncio.create_task(self._keep_alive())
            else:
                self.logger.notice("keepalive is disabled")
                self._keep_alive_thread = None

            # push open event
            await self._emit(
                LiveTranscriptionEvents.Open,
                OpenResponse(type=LiveTranscriptionEvents.Open.value),
            )

            self.logger.notice("start succeeded")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            return True
        except websockets.ConnectionClosed as e:
            self.logger.error("exception: websockets.ConnectionClosed")
            self.logger.debug("AsyncLiveClient.start LEAVE")
            if self.config.options.get("termination_exception_connect") == "true":
                raise
            return False
        except websockets.exceptions.WebSocketException as e:
            self.logger.error("WebSocketException in AsyncLiveClient.start: %s", e)
            self.logger.debug("AsyncLiveClient.start LEAVE")
            if self.config.options.get("termination_exception_connect") == "true":
                raise
            return False
        except Exception as e:
            self.logger.error("WebSocketException in AsyncLiveClient.start: %s", e)
            self.logger.debug("AsyncLiveClient.start LEAVE")
            if self.config.options.get("termination_exception_connect") == "true":
                raise
            return False

    # registers event handlers for specific events
    def on(self, event: LiveTranscriptionEvents, handler) -> None:
        """
        Registers event handlers for specific events.
        """
        self.logger.info("event fired: %s", event)
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
                if self._exit_event.is_set():
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
                        self.logger.warning(
                            "Unknown Message: response_type: %s, data: %s",
                            response_type,
                            data,
                        )
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
                self.logger.error(
                    "WebSocketException in AsyncLiveClient._listening: %s", e
                )
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

                # signal exit and close
                await self._signal_exit()

                self.logger.debug("AsyncLiveClient._listening LEAVE")

                if self.config.options.get("termination_exception") == "true":
                    raise
                return

            except Exception as e:
                self.logger.error("Exception in AsyncLiveClient._listening: %s", e)
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Exception in AsyncLiveClient._listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error("Exception in AsyncLiveClient._listening: %s", str(e))
                await self._emit(LiveTranscriptionEvents.Error, error)

                # signal exit and close
                await self._signal_exit()

                self.logger.debug("AsyncLiveClient._listening LEAVE")

                if self.config.options.get("termination_exception") == "true":
                    raise
                return

    # keep the connection alive by sending keepalive messages
    async def _keep_alive(self) -> None:
        self.logger.debug("AsyncLiveClient._keep_alive ENTER")

        counter = 0
        while True:
            try:
                counter += 1
                await asyncio.sleep(ONE_SECOND)

                if self._exit_event.is_set():
                    self.logger.notice("_keep_alive exiting gracefully")
                    self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                    return

                if self._socket is None:
                    self.logger.notice("socket is None, exiting keep_alive")
                    self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                    return

                # deepgram keepalive
                if counter % DEEPGRAM_INTERVAL == 0:
                    self.logger.verbose("Sending KeepAlive...")
                    await self.send(json.dumps({"type": "KeepAlive"}))

            except websockets.exceptions.ConnectionClosedOK as e:
                self.logger.notice(f"_keep_alive({e.code}) exiting gracefully")
                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                return

            except websockets.exceptions.WebSocketException as e:
                self.logger.error(
                    "WebSocketException in AsyncLiveClient._keep_alive: %s", e
                )
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

                # signal exit and close
                await self._signal_exit()

                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

                if self.config.options.get("termination_exception") == "true":
                    raise
                return

            except Exception as e:
                self.logger.error("Exception in AsyncLiveClient._keep_alive: %s", e)
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

                # signal exit and close
                await self._signal_exit()

                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")

                if self.config.options.get("termination_exception") == "true":
                    raise
                return

    # sends data over the WebSocket connection
    async def send(self, data: Union[str, bytes]) -> bool:
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("AsyncLiveClient.send ENTER")

        if self._exit_event.is_set():
            self.logger.notice("send exiting gracefully")
            self.logger.debug("AsyncLiveClient.send LEAVE")
            return False

        if self._socket is not None:
            try:
                await self._socket.send(data)
            except websockets.exceptions.ConnectionClosedOK as e:
                self.logger.notice(f"send() exiting gracefully: {e.code}")
                self.logger.debug("AsyncLiveClient._keep_alive LEAVE")
                if self.config.options.get("termination_exception_send") == "true":
                    raise
                return True
            except websockets.exceptions.WebSocketException as e:
                self.logger.error("send() failed - WebSocketException: %s", str(e))
                self.logger.spam("AsyncLiveClient.send LEAVE")
                if self.config.options.get("termination_exception_send") == "true":
                    raise
                return False
            except Exception as e:
                self.logger.error("send() failed - Exception: %s", str(e))
                self.logger.spam("AsyncLiveClient.send LEAVE")
                if self.config.options.get("termination_exception_send") == "true":
                    raise
                return False

            self.logger.spam(f"send() succeeded")
            self.logger.spam("AsyncLiveClient.send LEAVE")
            return True

        self.logger.spam("send() failed. socket is None")
        self.logger.spam("AsyncLiveClient.send LEAVE")
        return False

    # closes the WebSocket connection gracefully
    async def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.debug("AsyncLiveClient.finish ENTER")

        # signal exit
        await self._signal_exit()

        # stop the threads
        self.logger.verbose("cancelling tasks...")
        try:
            # Before cancelling, check if the tasks were created
            tasks = []
            if self._keep_alive_thread is not None:
                self._keep_alive_thread.cancel()
                tasks.append(self._keep_alive_thread)
            if self._listen_thread is not None:
                self._listen_thread.cancel()
                tasks.append(self._listen_thread)

            # Use asyncio.gather to wait for tasks to be cancelled
            await asyncio.gather(*filter(None, tasks), return_exceptions=True)
            self.logger.notice("threads joined")
            self._listen_thread = None
            self._keep_alive_thread = None

            self._socket = None

            self.logger.notice("finish succeeded")
            self.logger.spam("AsyncLiveClient.finish LEAVE")
            return True

        except asyncio.CancelledError as e:
            self.logger.error("tasks cancelled error: %s", e)
            self.logger.debug("AsyncLiveClient.finish LEAVE")
            return False

    # signals the WebSocket connection to exit
    async def _signal_exit(self) -> None:
        # send close event
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

        # signal exit
        self._exit_event.set()

        # closes the WebSocket connection gracefully
        self.logger.verbose("clean up socket...")
        if self._socket is not None:
            self.logger.verbose("socket.wait_closed...")
            try:
                await self._socket.close()
                self._socket = None
            except websockets.exceptions.WebSocketException as e:
                self.logger.error("socket.wait_closed failed: %s", e)
