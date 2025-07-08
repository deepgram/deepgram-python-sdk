# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import asyncio
import json
import logging
from typing import Dict, Union, Optional, cast, Any, Callable
from datetime import datetime
import threading

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import LiveTranscriptionEvents
from ....common import AbstractAsyncWebSocketClient
from ....common import DeepgramError

from .response import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)
from .options import ListenWebSocketOptions

ONE_SECOND = 1
HALF_SECOND = 0.5
DEEPGRAM_INTERVAL = 5
PING_INTERVAL = 20


class AsyncListenWebSocketClient(
    AbstractAsyncWebSocketClient
):  # pylint: disable=too-many-instance-attributes
    """
    Client for interacting with Deepgram's live transcription services over WebSockets.

     This class provides methods to establish a WebSocket connection for live transcription and handle real-time transcription events.

     Args:
         config (DeepgramClientOptions): all the options for the client.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    _event_handlers: Dict[LiveTranscriptionEvents, list]

    _keep_alive_thread: Union[asyncio.Task, None]
    _flush_thread: Union[asyncio.Task, None]
    _last_datagram: Optional[datetime] = None

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config is required")

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config
        self._endpoint = "v1/listen"

        self._flush_thread = None
        self._keep_alive_thread = None

        # auto flush
        self._last_datagram = None
        self._lock_flush = threading.Lock()

        # init handlers
        self._event_handlers = {
            event: [] for event in LiveTranscriptionEvents.__members__.values()
        }

        # call the parent constructor
        super().__init__(self._config, self._endpoint)

    # pylint: disable=too-many-branches,too-many-statements
    async def start(
        self,
        options: Optional[Union[ListenWebSocketOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for live transcription.
        """
        self._logger.debug("AsyncListenWebSocketClient.start ENTER")
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, ListenWebSocketOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("AsyncListenWebSocketClient.start LEAVE")
            raise DeepgramError("Fatal transcription options error")

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

        if isinstance(options, ListenWebSocketOptions):
            self._logger.info("ListenWebSocketOptions switching class -> dict")
            self._options = options.to_dict()
        elif options is not None:
            self._options = options
        else:
            self._options = {}

        try:
            # call parent start
            if (
                await super().start(
                    self._options,
                    self._addons,
                    self._headers,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )
                is False
            ):
                self._logger.error("AsyncListenWebSocketClient.start failed")
                self._logger.debug("AsyncListenWebSocketClient.start LEAVE")
                return False

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # keepalive thread
            if self._config.is_keep_alive_enabled():
                self._logger.notice("keepalive is enabled")
                self._keep_alive_thread = asyncio.create_task(self._keep_alive())
            else:
                self._logger.notice("keepalive is disabled")

            # flush thread
            if self._config.is_auto_flush_reply_enabled():
                self._logger.notice("autoflush is enabled")
                self._flush_thread = asyncio.create_task(self._flush())
            else:
                self._logger.notice("autoflush is disabled")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("start succeeded")
            self._logger.debug("AsyncListenWebSocketClient.start LEAVE")
            return True

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in AsyncListenWebSocketClient.start: %s", e
            )
            self._logger.debug("AsyncListenWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") is True:
                raise
            return False

    # pylint: enable=too-many-branches,too-many-statements

    def on(self, event: LiveTranscriptionEvents, handler: Callable) -> None:
        """
        Registers event handlers for specific events.
        """
        self._logger.info("event subscribed: %s", event)
        if event in LiveTranscriptionEvents.__members__.values() and callable(handler):
            self._event_handlers[event].append(handler)

    # triggers the registered event handlers for a specific event
    async def _emit(self, event: LiveTranscriptionEvents, *args, **kwargs) -> None:
        """
        Emits events to the registered event handlers.
        """
        self._logger.debug("AsyncListenWebSocketClient._emit ENTER")
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

        self._logger.debug("AsyncListenWebSocketClient._emit LEAVE")

    async def _process_text(self, message: str) -> None:
        """
        Processes messages received over the WebSocket connection.
        """
        self._logger.debug("AsyncListenWebSocketClient._process_text ENTER")

        try:
            self._logger.debug("Text data received")
            if len(message) == 0:
                self._logger.debug("message is empty")
                self._logger.debug("AsyncListenWebSocketClient._process_text LEAVE")
                return

            data = json.loads(message)
            response_type = data.get("type")
            self._logger.debug("response_type: %s, data: %s", response_type, data)

            match response_type:
                case LiveTranscriptionEvents.Open:
                    open_result: OpenResponse = OpenResponse.from_json(message)
                    self._logger.verbose("OpenResponse: %s", open_result)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Open),
                        open=open_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Transcript:
                    msg_result: LiveResultResponse = LiveResultResponse.from_json(
                        message
                    )
                    self._logger.verbose("LiveResultResponse: %s", msg_result)

                    # auto flush
                    if self._config.is_inspecting_listen():
                        inspect_res = await self._inspect(msg_result)
                        if not inspect_res:
                            self._logger.error("inspect_res failed")

                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Transcript),
                        result=msg_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Metadata:
                    meta_result: MetadataResponse = MetadataResponse.from_json(message)
                    self._logger.verbose("MetadataResponse: %s", meta_result)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Metadata),
                        metadata=meta_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.SpeechStarted:
                    ss_result: SpeechStartedResponse = SpeechStartedResponse.from_json(
                        message
                    )
                    self._logger.verbose("SpeechStartedResponse: %s", ss_result)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.SpeechStarted),
                        speech_started=ss_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.UtteranceEnd:
                    ue_result: UtteranceEndResponse = UtteranceEndResponse.from_json(
                        message
                    )
                    self._logger.verbose("UtteranceEndResponse: %s", ue_result)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.UtteranceEnd),
                        utterance_end=ue_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Close:
                    close_result: CloseResponse = CloseResponse.from_json(message)
                    self._logger.verbose("CloseResponse: %s", close_result)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Close),
                        close=close_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Error:
                    err_error: ErrorResponse = ErrorResponse.from_json(message)
                    self._logger.verbose("ErrorResponse: %s", err_error)
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
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
                        type=LiveTranscriptionEvents(LiveTranscriptionEvents.Unhandled),
                        raw=message,
                    )
                    await self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Unhandled),
                        unhandled=unhandled_error,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )

            self._logger.notice("_process_text Succeeded")
            self._logger.debug("AsyncListenWebSocketClient._process_text LEAVE")

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "Exception in AsyncListenWebSocketClient._process_text: %s", e
            )
            e_error: ErrorResponse = ErrorResponse(
                "Exception in AsyncListenWebSocketClient._process_text",
                f"{e}",
                "Exception",
            )
            await self._emit(
                LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                error=e_error,
                **dict(cast(Dict[Any, Any], self._kwargs)),
            )

            # signal exit and close
            await super()._signal_exit()

            self._logger.debug("AsyncListenWebSocketClient._process_text LEAVE")

            if self._config.options.get("termination_exception") is True:
                raise
            return

    # pylint: enable=too-many-return-statements,too-many-statements

    async def _process_binary(self, message: bytes) -> None:
        raise NotImplementedError("no _process_binary method should be called")

    # pylint: disable=too-many-return-statements
    async def _keep_alive(self) -> None:
        """
        Sends keepalive messages to the WebSocket connection.
        """
        self._logger.debug("AsyncListenWebSocketClient._keep_alive ENTER")

        counter = 0
        while True:
            try:
                counter += 1
                await asyncio.sleep(ONE_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_keep_alive exiting gracefully")
                    self._logger.debug("AsyncListenWebSocketClient._keep_alive LEAVE")
                    return

                # deepgram keepalive
                if counter % DEEPGRAM_INTERVAL == 0:
                    await self.keep_alive()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in AsyncListenWebSocketClient._keep_alive: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in AsyncListenWebSocketClient._keep_alive",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in AsyncListenWebSocketClient._keep_alive: %s", str(e)
                )
                await self._emit(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await super()._signal_exit()

                self._logger.debug("AsyncListenWebSocketClient._keep_alive LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    ## pylint: disable=too-many-return-statements,too-many-statements
    async def _flush(self) -> None:
        self._logger.debug("AsyncListenWebSocketClient._flush ENTER")

        delta_in_ms_str = self._config.options.get("auto_flush_reply_delta")
        if delta_in_ms_str is None:
            self._logger.error("auto_flush_reply_delta is None")
            self._logger.debug("AsyncListenWebSocketClient._flush LEAVE")
            return
        delta_in_ms = float(delta_in_ms_str)

        while True:
            try:
                await asyncio.sleep(HALF_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_flush exiting gracefully")
                    self._logger.debug("AsyncListenWebSocketClient._flush LEAVE")
                    return

                if self._last_datagram is None:
                    self._logger.debug("AutoFlush last_datagram is None")
                    continue

                delta = datetime.now() - self._last_datagram
                diff_in_ms = delta.total_seconds() * 1000
                self._logger.debug("AutoFlush delta: %f", diff_in_ms)
                if diff_in_ms < delta_in_ms:
                    self._logger.debug("AutoFlush delta is less than threshold")
                    continue

                self._last_datagram = None
                await self.finalize()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in AsyncListenWebSocketClient._flush: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in AsyncListenWebSocketClient._flush",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in AsyncListenWebSocketClient._flush: %s", str(e)
                )
                await self._emit(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await super()._signal_exit()

                self._logger.debug("AsyncListenWebSocketClient._flush LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    # pylint: enable=too-many-return-statements

    async def keep_alive(self) -> bool:
        """
        Sends a KeepAlive message
        """
        self._logger.spam("AsyncListenWebSocketClient.keep_alive ENTER")

        self._logger.notice("Sending KeepAlive...")
        ret = await self.send(json.dumps({"type": "KeepAlive"}))

        if not ret:
            self._logger.error("keep_alive failed")
            self._logger.spam("AsyncListenWebSocketClient.keep_alive LEAVE")
            return False

        self._logger.notice("keep_alive succeeded")
        self._logger.spam("AsyncListenWebSocketClient.keep_alive LEAVE")

        return True

    async def finalize(self) -> bool:
        """
        Finalizes the Transcript connection by flushing it
        """
        self._logger.spam("AsyncListenWebSocketClient.finalize ENTER")

        self._logger.notice("Sending Finalize...")
        ret = await self.send(json.dumps({"type": "Finalize"}))

        if not ret:
            self._logger.error("finalize failed")
            self._logger.spam("AsyncListenWebSocketClient.finalize LEAVE")
            return False

        self._logger.notice("finalize succeeded")
        self._logger.spam("AsyncListenWebSocketClient.finalize LEAVE")

        return True

    async def _close_message(self) -> bool:
        return await self.send(json.dumps({"type": "CloseStream"}))

    async def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.debug("AsyncListenWebSocketClient.finish ENTER")

        # stop the threads
        self._logger.verbose("cancelling tasks...")
        try:
            # call parent finish
            if await super().finish() is False:
                self._logger.error("AsyncListenWebSocketClient.finish failed")

            # Before cancelling, check if the tasks were created
            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("before running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            tasks = []
            if self._keep_alive_thread is not None:
                self._keep_alive_thread.cancel()
                tasks.append(self._keep_alive_thread)
                self._logger.notice("processing _keep_alive_thread cancel...")

            if self._flush_thread is not None:
                self._flush_thread.cancel()
                tasks.append(self._flush_thread)
                self._logger.notice("processing _flush_thread cancel...")

            # Use asyncio.gather to wait for tasks to be cancelled
            # Prevent indefinite waiting by setting a timeout
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=10)
            self._logger.notice("threads joined")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("finish succeeded")
            self._logger.spam("AsyncListenWebSocketClient.finish LEAVE")
            return True

        except asyncio.CancelledError as e:
            self._logger.debug("tasks cancelled error: %s", e)
            self._logger.debug("AsyncListenWebSocketClient.finish LEAVE")
            return False

        except asyncio.TimeoutError as e:
            self._logger.error("tasks cancellation timed out: %s", e)
            self._logger.debug("AsyncListenWebSocketClient.finish LEAVE")
            return False

    async def _inspect(self, msg_result: LiveResultResponse) -> bool:
        # auto flush_inspect is generically used to track any messages you might want to snoop on
        # place additional logic here to inspect messages of interest

        # for auto flush functionality
        # set the last datagram
        sentence = msg_result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return True

        if msg_result.is_final:
            self._logger.debug("AutoFlush is_final received")
            self._last_datagram = None
        else:
            self._last_datagram = datetime.now()
            self._logger.debug(
                "AutoFlush interim received: %s",
                str(self._last_datagram),
            )

        return True
