# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import asyncio
import json
import logging
from typing import Dict, Union, Optional, cast, Any
import threading

import websockets
from websockets.client import WebSocketClientProtocol

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import SpeakWebSocketEvents
from .helpers import convert_to_websocket_url, append_query_params
from ...errors import DeepgramError

from .response import (
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    WarningResponse,
    ErrorResponse,
    UnhandledResponse,
)
from ..options import SpeakOptions


class AsyncSpeakWebSocketClient:  # pylint: disable=too-many-instance-attributes
    """
    Client for interacting with Deepgram's text-to-speech services over WebSockets.

     This class provides methods to establish a WebSocket connection for TTS synthesis and handle real-time TTS synthesis events.

     Args:
         config (DeepgramClientOptions): all the options for the client.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str
    _websocket_url: str

    _socket: WebSocketClientProtocol
    _event_handlers: Dict[SpeakWebSocketEvents, list]

    _listen_thread: Union[asyncio.Task, None]

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config are required")

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config
        self._endpoint = "v1/speak"

        self._listen_thread = None

        # exit
        self._exit_event = asyncio.Event()

        self._event_handlers = {
            event: [] for event in SpeakWebSocketEvents.__members__.values()
        }
        self._websocket_url = convert_to_websocket_url(self._config.url, self._endpoint)

    # pylint: disable=too-many-branches,too-many-statements
    async def start(
        self,
        options: Optional[Union[SpeakOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for text-to-speech synthesis.
        """
        self._logger.debug("AsyncSpeakStreamClient.start ENTER")
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, SpeakOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("SpeakStreamClient.start LEAVE")
            raise DeepgramError("Fatal text-to-speech options error")

        self._addons = addons
        self._headers = headers

        # add "members" as members of the class
        if members is not None:
            self.__dict__.update(members)

        # set kwargs as members of the class
        if kwargs is not None:
            self._kwargs = kwargs
        else:
            self._kwargs = {}

        if isinstance(options, SpeakOptions):
            self._logger.info("SpeakOptions switching class -> dict")
            self._options = options.to_dict()
        elif options is not None:
            self._options = options
        else:
            self._options = {}

        combined_options = self._options
        if self._addons is not None:
            self._logger.info("merging addons to options")
            combined_options.update(self._addons)
            self._logger.info("new options: %s", combined_options)
        self._logger.debug("combined_options: %s", combined_options)

        combined_headers = self._config.headers
        if self._headers is not None:
            self._logger.info("merging headers to options")
            combined_headers.update(self._headers)
            self._logger.info("new headers: %s", combined_headers)
        self._logger.debug("combined_headers: %s", combined_headers)

        url_with_params = append_query_params(self._websocket_url, combined_options)

        try:
            self._socket = await websockets.connect(
                url_with_params, extra_headers=combined_headers
            )
            self._exit_event.clear()

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # listen thread
            self._listen_thread = asyncio.create_task(self._listening())

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # push open event
            await self._emit(
                SpeakWebSocketEvents(SpeakWebSocketEvents.Open),
                OpenResponse(type=SpeakWebSocketEvents.Open),
            )

            self._logger.notice("start succeeded")
            self._logger.debug("AsyncSpeakStreamClient.start LEAVE")
            return True
        except websockets.ConnectionClosed as e:
            self._logger.error(
                "ConnectionClosed in AsyncSpeakStreamClient.start: %s", e
            )
            self._logger.debug("AsyncSpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise
            return False
        except websockets.exceptions.WebSocketException as e:
            self._logger.error(
                "WebSocketException in AsyncSpeakStreamClient.start: %s", e
            )
            self._logger.debug("AsyncSpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise
            return False
        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in AsyncSpeakStreamClient.start: %s", e
            )
            self._logger.debug("AsyncSpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise
            return False

    # pylint: enable=too-many-branches,too-many-statements

    def on(self, event: SpeakWebSocketEvents, handler) -> None:
        """
        Registers event handlers for specific events.
        """
        self._logger.info("event subscribed: %s", event)
        if event in SpeakWebSocketEvents.__members__.values() and callable(handler):
            if handler not in self._event_handlers[event]:
                self._event_handlers[event].append(handler)

    # triggers the registered event handlers for a specific event
    async def _emit(self, event: SpeakWebSocketEvents, *args, **kwargs) -> None:
        """
        Emits events to the registered event handlers.
        """
        self._logger.debug("AsyncSpeakStreamClient._emit ENTER")
        self._logger.debug("callback handlers for: %s", event)

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        tasks = []
        for handler in self._event_handlers[event]:
            task = asyncio.create_task(handler(self, *args, **kwargs))
            tasks.append(task)

        if tasks:
            self._logger.debug("waiting for tasks to finish...")
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks.clear()

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.debug("AsyncSpeakStreamClient._emit LEAVE")

    # pylint: disable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches
    async def _listening(self) -> None:
        """
        Listens for messages from the WebSocket connection.
        """
        self._logger.debug("AsyncSpeakStreamClient._listening ENTER")

        while True:
            try:
                if self._exit_event.is_set():
                    self._logger.notice("_listening exiting gracefully")
                    self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")
                    return

                if self._socket is None:
                    self._logger.warning("socket is empty")
                    self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")
                    return

                message = await self._socket.recv()

                if message is None:
                    self._logger.spam("message is None")
                    continue

                if isinstance(message, bytes):
                    self._logger.debug("Binary data received")
                    await self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.AudioData),
                        data=message,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                else:
                    data = json.loads(message)
                    response_type = data.get("type")
                    self._logger.debug(
                        "response_type: %s, data: %s", response_type, data
                    )

                    match response_type:
                        case SpeakWebSocketEvents.Open:
                            open_result: OpenResponse = OpenResponse.from_json(message)
                            self._logger.verbose("OpenResponse: %s", open_result)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Open),
                                open=open_result,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case SpeakWebSocketEvents.Metadata:
                            meta_result: MetadataResponse = MetadataResponse.from_json(
                                message
                            )
                            self._logger.verbose("MetadataResponse: %s", meta_result)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Metadata),
                                metadata=meta_result,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case SpeakWebSocketEvents.Flush:
                            fl_result: FlushedResponse = FlushedResponse.from_json(
                                message
                            )
                            self._logger.verbose("FlushedResponse: %s", fl_result)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Flush),
                                flushed=fl_result,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case SpeakWebSocketEvents.Close:
                            close_result: CloseResponse = CloseResponse.from_json(
                                message
                            )
                            self._logger.verbose("CloseResponse: %s", close_result)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Close),
                                close=close_result,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case SpeakWebSocketEvents.Warning:
                            war_warning: WarningResponse = WarningResponse.from_json(
                                message
                            )
                            self._logger.verbose("WarningResponse: %s", war_warning)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Warning),
                                warning=war_warning,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case SpeakWebSocketEvents.Error:
                            err_error: ErrorResponse = ErrorResponse.from_json(message)
                            self._logger.verbose("ErrorResponse: %s", err_error)
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                                error=err_error,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )
                        case _:
                            self._logger.warning(
                                "Unknown Message: response_type: %s, data: %s",
                                response_type,
                                data,
                            )
                            unhandled_error: UnhandledResponse = UnhandledResponse(
                                type=SpeakWebSocketEvents(
                                    SpeakWebSocketEvents.Unhandled
                                ),
                                raw=message,
                            )
                            await self._emit(
                                SpeakWebSocketEvents(SpeakWebSocketEvents.Unhandled),
                                unhandled=unhandled_error,
                                **dict(cast(Dict[Any, Any], self._kwargs)),
                            )

            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice(f"_listening({e.code}) exiting gracefully")
                self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")
                return

            except websockets.exceptions.ConnectionClosed as e:
                if e.code == 1000:
                    self._logger.notice(f"_listening({e.code}) exiting gracefully")
                    self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")
                    return

                self._logger.error(
                    "ConnectionClosed in AsyncSpeakStreamClient._listening with code %s: %s",
                    e.code,
                    e.reason,
                )
                cc_error: ErrorResponse = ErrorResponse(
                    "ConnectionClosed in AsyncSpeakStreamClient._listening",
                    f"{e}",
                    "ConnectionClosed",
                )
                await self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=cc_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await self._signal_exit()

                self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except websockets.exceptions.WebSocketException as e:
                self._logger.error(
                    "WebSocketException in AsyncSpeakStreamClient._listening: %s", e
                )
                ws_error: ErrorResponse = ErrorResponse(
                    "WebSocketException in AsyncSpeakStreamClient._listening",
                    f"{e}",
                    "WebSocketException",
                )
                await self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=ws_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await self._signal_exit()

                self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in AsyncSpeakStreamClient._listening: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in AsyncSpeakStreamClient._listening",
                    f"{e}",
                    "Exception",
                )
                await self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await self._signal_exit()

                self._logger.debug("AsyncSpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

    # pylint: disable=too-many-return-statements

    async def send(self, text_input: str) -> bool:
        """
        Sends data over the WebSocket connection.
        """
        self._logger.spam("AsyncSpeakStreamClient.send ENTER")

        if self._exit_event.is_set():
            self._logger.notice("send exiting gracefully")
            self._logger.debug("AsyncSpeakStreamClient.send LEAVE")
            return False

        if self._socket is not None:
            try:
                await self._socket.send(
                    json.dumps({"type": "Speak", "text": text_input})
                )
            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice(f"send() exiting gracefully: {e.code}")
                self._logger.debug("AsyncSpeakStreamClient.send LEAVE")
                if self._config.options.get("termination_exception_send") == "true":
                    raise
                return True
            except websockets.exceptions.ConnectionClosed as e:
                if e.code in [1000, 1001]:
                    self._logger.notice(f"send({e.code}) exiting gracefully")
                    self._logger.debug("AsyncSpeakStreamClient.send LEAVE")
                    if self._config.options.get("termination_exception_send") == "true":
                        raise
                    return True

                self._logger.error("send() failed - ConnectionClosed: %s", str(e))
                self._logger.spam("AsyncSpeakStreamClient.send LEAVE")
                if self._config.options.get("termination_exception_send") == "true":
                    raise
                return False
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("send() failed - WebSocketException: %s", str(e))
                self._logger.spam("AsyncSpeakStreamClient.send LEAVE")
                if self._config.options.get("termination_exception_send") == "true":
                    raise
                return False
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("send() failed - Exception: %s", str(e))
                self._logger.spam("AsyncSpeakStreamClient.send LEAVE")
                if self._config.options.get("termination_exception_send") == "true":
                    raise
                return False

            self._logger.spam("send() succeeded")
            self._logger.spam("AsyncSpeakStreamClient.send LEAVE")
            return True

        self._logger.spam("send() failed. socket is None")
        self._logger.spam("AsyncSpeakStreamClient.send LEAVE")
        return False

    # pylint: enable=too-many-return-statements

    async def flush(self) -> bool:
        """
        Flushes the current buffer and returns generated audio
        """
        self._logger.spam("AsyncSpeakStreamClient.flush ENTER")

        if self._exit_event.is_set():
            self._logger.notice("flush exiting gracefully")
            self._logger.debug("AsyncSpeakStreamClient.flush LEAVE")
            return False

        if self._socket is None:
            self._logger.notice("socket is not intialized")
            self._logger.debug("AsyncSpeakStreamClient.flush LEAVE")
            return False

        self._logger.notice("Sending Flush...")
        ret = self.send(json.dumps({"type": "Flush"}))

        if not ret:
            self._logger.error("flush failed")
            self._logger.spam("AsyncSpeakStreamClient.flush LEAVE")
            return False

        self._logger.notice("flush succeeded")
        self._logger.spam("AsyncSpeakStreamClient.flush LEAVE")

        return True

    async def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.debug("AsyncSpeakStreamClient.finish ENTER")

        # signal exit
        await self._signal_exit()

        # stop the threads
        self._logger.verbose("cancelling tasks...")
        try:
            # Before cancelling, check if the tasks were created
            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("before running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            tasks = []

            if self._listen_thread is not None:
                self._listen_thread.cancel()
                tasks.append(self._listen_thread)
                self._logger.notice("processing _listen_thread cancel...")

            # Use asyncio.gather to wait for tasks to be cancelled
            await asyncio.wait_for(
                asyncio.gather(*tasks), timeout=10
            )  # Prevent indefinite waiting
            self._logger.notice("threads joined")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("finish succeeded")
            self._logger.spam("AsyncSpeakStreamClient.finish LEAVE")
            return True

        except asyncio.CancelledError as e:
            self._logger.error("tasks cancelled error: %s", e)
            self._logger.debug("AsyncSpeakStreamClient.finish LEAVE")
            return False

        except asyncio.TimeoutError as e:
            self._logger.error("tasks cancellation timed out: %s", e)
            self._logger.debug("AsyncSpeakStreamClient.finish LEAVE")
            return False

    async def _signal_exit(self) -> None:
        # send close event
        self._logger.verbose("closing socket...")
        if self._socket is not None:
            self._logger.verbose("send CloseStream...")
            try:
                # if the socket connection is closed, the following line might throw an error
                await self.send(json.dumps({"type": "CloseStream"}))
            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice("_signal_exit  - ConnectionClosedOK: %s", e.code)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.notice("_signal_exit  - ConnectionClosed: %s", e.code)
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("_signal_exit - WebSocketException: %s", str(e))
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_signal_exit - Exception: %s", str(e))

            # push close event
            try:
                await self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Close),
                    close=CloseResponse(type=SpeakWebSocketEvents.Close),
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_emit - Exception: %s", e)

            # wait for task to send
            await asyncio.sleep(0.5)

        # signal exit
        self._exit_event.set()

        # closes the WebSocket connection gracefully
        self._logger.verbose("clean up socket...")
        if self._socket is not None:
            self._logger.verbose("socket.wait_closed...")
            try:
                await self._socket.close()
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("socket.wait_closed failed: %s", e)

        self._socket = None  # type: ignore
