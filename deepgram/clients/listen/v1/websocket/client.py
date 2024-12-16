# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
import time
import logging
from typing import Dict, Union, Optional, cast, Any, Callable, Type
from datetime import datetime
import threading

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import LiveTranscriptionEvents
from ....common import AbstractSyncWebSocketClient
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


class ListenWebSocketClient(
    AbstractSyncWebSocketClient
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

    _lock_flush: threading.Lock
    _event_handlers: Dict[LiveTranscriptionEvents, list]

    _keep_alive_thread: Union[threading.Thread, None]
    _flush_thread: Union[threading.Thread, None]
    _last_datagram: Optional[datetime] = None

    _thread_cls: Type[threading.Thread]

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    def __init__(
        self,
        config: DeepgramClientOptions,
        thread_cls: Type[threading.Thread] = threading.Thread,
    ):
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

        self._thread_cls = thread_cls

        # init handlers
        self._event_handlers = {
            event: [] for event in LiveTranscriptionEvents.__members__.values()
        }

        # call the parent constructor
        super().__init__(self._config, self._endpoint)

    # pylint: disable=too-many-statements,too-many-branches
    def start(
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
        self._logger.debug("ListenWebSocketClient.start ENTER")
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, ListenWebSocketOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("ListenWebSocketClient.start LEAVE")
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
                super().start(
                    self._options,
                    self._addons,
                    self._headers,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )
                is False
            ):
                self._logger.error("ListenWebSocketClient.start failed")
                self._logger.debug("ListenWebSocketClient.start LEAVE")
                return False

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # keepalive thread
            if self._config.is_keep_alive_enabled():
                self._logger.notice("keepalive is enabled")
                self._keep_alive_thread = self._thread_cls(target=self._keep_alive)
                self._keep_alive_thread.start()
            else:
                self._logger.notice("keepalive is disabled")

            # flush thread
            if self._config.is_auto_flush_reply_enabled():
                self._logger.notice("autoflush is enabled")
                self._flush_thread = self._thread_cls(target=self._flush)
                self._flush_thread.start()
            else:
                self._logger.notice("autoflush is disabled")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("start succeeded")
            self._logger.debug("ListenWebSocketClient.start LEAVE")
            return True

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in ListenWebSocketClient.start: %s", e
            )
            self._logger.debug("ListenWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") is True:
                raise e
            return False

    # pylint: enable=too-many-statements,too-many-branches

    def on(
        self, event: LiveTranscriptionEvents, handler: Callable
    ) -> None:  # registers event handlers for specific events
        """
        Registers event handlers for specific events.
        """
        self._logger.info("event subscribed: %s", event)
        if event in LiveTranscriptionEvents.__members__.values() and callable(handler):
            self._event_handlers[event].append(handler)

    def _emit(self, event: LiveTranscriptionEvents, *args, **kwargs) -> None:
        """
        Emits events to the registered event handlers.
        """
        self._logger.debug("ListenWebSocketClient._emit ENTER")
        self._logger.debug("callback handlers for: %s", event)

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.debug("callback handlers for: %s", event)
        for handler in self._event_handlers[event]:
            handler(self, *args, **kwargs)

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.debug("ListenWebSocketClient._emit LEAVE")

    # pylint: disable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches
    def _process_text(self, message: str) -> None:
        """
        Processes messages received over the WebSocket connection.
        """
        self._logger.debug("ListenWebSocketClient._process_text ENTER")

        try:
            if len(message) == 0:
                self._logger.debug("message is empty")
                self._logger.debug("ListenWebSocketClient._process_text LEAVE")
                return

            data = json.loads(message)
            response_type = data.get("type")
            self._logger.debug("response_type: %s, data: %s", response_type, data)

            match response_type:
                case LiveTranscriptionEvents.Open:
                    open_result: OpenResponse = OpenResponse.from_json(message)
                    self._logger.verbose("OpenResponse: %s", open_result)
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Open),
                        open=open_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Transcript:
                    msg_result: LiveResultResponse = LiveResultResponse.from_json(
                        message
                    )
                    self._logger.verbose("LiveResultResponse: %s", msg_result)

                    #  auto flush
                    if self._config.is_inspecting_listen():
                        inspect_res = self._inspect(msg_result)
                        if not inspect_res:
                            self._logger.error("inspect_res failed")

                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Transcript),
                        result=msg_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Metadata:
                    meta_result: MetadataResponse = MetadataResponse.from_json(message)
                    self._logger.verbose("MetadataResponse: %s", meta_result)
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Metadata),
                        metadata=meta_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.SpeechStarted:
                    ss_result: SpeechStartedResponse = SpeechStartedResponse.from_json(
                        message
                    )
                    self._logger.verbose("SpeechStartedResponse: %s", ss_result)
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.SpeechStarted),
                        speech_started=ss_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.UtteranceEnd:
                    ue_result: UtteranceEndResponse = UtteranceEndResponse.from_json(
                        message
                    )
                    self._logger.verbose("UtteranceEndResponse: %s", ue_result)
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.UtteranceEnd),
                        utterance_end=ue_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Close:
                    close_result: CloseResponse = CloseResponse.from_json(message)
                    self._logger.verbose("CloseResponse: %s", close_result)
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Close),
                        close=close_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case LiveTranscriptionEvents.Error:
                    err_error: ErrorResponse = ErrorResponse.from_json(message)
                    self._logger.verbose("ErrorResponse: %s", err_error)
                    self._emit(
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
                    self._emit(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.Unhandled),
                        unhandled=unhandled_error,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )

            self._logger.notice("_process_text Succeeded")
            self._logger.debug("SpeakStreamClient._process_text LEAVE")

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "Exception in ListenWebSocketClient._process_text: %s", e
            )
            e_error: ErrorResponse = ErrorResponse(
                "Exception in ListenWebSocketClient._process_text",
                f"{e}",
                "Exception",
            )
            self._logger.error(
                "Exception in ListenWebSocketClient._process_text: %s", str(e)
            )
            self._emit(
                LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                e_error,
                **dict(cast(Dict[Any, Any], self._kwargs)),
            )

            # signal exit and close
            super()._signal_exit()

            self._logger.debug("ListenWebSocketClient._process_text LEAVE")

            if self._config.options.get("termination_exception") is True:
                raise
            return

    # pylint: enable=too-many-return-statements,too-many-statements

    def _process_binary(self, message: bytes) -> None:
        raise NotImplementedError("no _process_binary method should be called")

    # pylint: disable=too-many-return-statements
    def _keep_alive(self) -> None:
        self._logger.debug("ListenWebSocketClient._keep_alive ENTER")

        counter = 0
        while True:
            try:
                counter += 1
                self._exit_event.wait(timeout=ONE_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_keep_alive exiting gracefully")
                    self._logger.debug("ListenWebSocketClient._keep_alive LEAVE")
                    return

                # deepgram keepalive
                if counter % DEEPGRAM_INTERVAL == 0:
                    self.keep_alive()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in ListenWebSocketClient._keep_alive: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in ListenWebSocketClient._keep_alive",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in ListenWebSocketClient._keep_alive: %s", str(e)
                )
                self._emit(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                    e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                super()._signal_exit()

                self._logger.debug("ListenWebSocketClient._keep_alive LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    ## pylint: disable=too-many-return-statements,too-many-statements
    def _flush(self) -> None:
        self._logger.debug("ListenWebSocketClient._flush ENTER")

        delta_in_ms_str = self._config.options.get("auto_flush_reply_delta")
        if delta_in_ms_str is None:
            self._logger.error("auto_flush_reply_delta is None")
            self._logger.debug("ListenWebSocketClient._flush LEAVE")
            return
        delta_in_ms = float(delta_in_ms_str)

        _flush_event = threading.Event()
        while True:
            try:
                _flush_event.wait(timeout=HALF_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_flush exiting gracefully")
                    self._logger.debug("ListenWebSocketClient._flush LEAVE")
                    return

                with self._lock_flush:
                    if self._last_datagram is None:
                        self._logger.debug("AutoFlush last_datagram is None")
                        continue

                    delta = datetime.now() - self._last_datagram
                    diff_in_ms = delta.total_seconds() * 1000
                    self._logger.debug("AutoFlush delta: %f", diff_in_ms)
                    if diff_in_ms < delta_in_ms:
                        self._logger.debug("AutoFlush delta is less than threshold")
                        continue

                    with self._lock_flush:
                        self._last_datagram = None
                    self.finalize()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("Exception in ListenWebSocketClient._flush: %s", e)
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in ListenWebSocketClient._flush",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in ListenWebSocketClient._flush: %s", str(e)
                )
                self._emit(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Error),
                    e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                super()._signal_exit()

                self._logger.debug("ListenWebSocketClient._flush LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    # pylint: enable=too-many-return-statements

    def keep_alive(self) -> bool:
        """
        Sends a KeepAlive message
        """
        self._logger.spam("ListenWebSocketClient.keep_alive ENTER")

        self._logger.notice("Sending KeepAlive...")
        ret = self.send(json.dumps({"type": "KeepAlive"}))

        if not ret:
            self._logger.error("keep_alive failed")
            self._logger.spam("ListenWebSocketClient.keep_alive LEAVE")
            return False

        self._logger.notice("keep_alive succeeded")
        self._logger.spam("ListenWebSocketClient.keep_alive LEAVE")

        return True

    def finalize(self) -> bool:
        """
        Finalizes the Transcript connection by flushing it
        """
        self._logger.spam("ListenWebSocketClient.finalize ENTER")

        self._logger.notice("Sending Finalize...")
        ret = self.send(json.dumps({"type": "Finalize"}))

        if not ret:
            self._logger.error("finalize failed")
            self._logger.spam("ListenWebSocketClient.finalize LEAVE")
            return False

        self._logger.notice("finalize succeeded")
        self._logger.spam("ListenWebSocketClient.finalize LEAVE")

        return True

    def _close_message(self) -> bool:
        return self.send(json.dumps({"type": "CloseStream"}))

    # closes the WebSocket connection gracefully
    def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.spam("ListenWebSocketClient.finish ENTER")

        # call parent finish
        if super().finish() is False:
            self._logger.error("ListenWebSocketClient.finish failed")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        # stop the threads
        self._logger.verbose("cancelling tasks...")
        if self._flush_thread is not None:
            self._flush_thread.join()
            self._flush_thread = None
            self._logger.notice("processing _flush_thread thread joined")

        if self._keep_alive_thread is not None:
            self._keep_alive_thread.join()
            self._keep_alive_thread = None
            self._logger.notice("processing _keep_alive_thread thread joined")

        if self._listen_thread is not None:
            self._listen_thread.join()
            self._listen_thread = None
        self._logger.notice("listening thread joined")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.notice("finish succeeded")
        self._logger.spam("ListenWebSocketClient.finish LEAVE")
        return True

    def _inspect(self, msg_result: LiveResultResponse) -> bool:
        # auto flush_inspect is generically used to track any messages you might want to snoop on
        # place additional logic here to inspect messages of interest

        # for auto flush functionality
        # set the last datagram
        sentence = msg_result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return True

        if msg_result.is_final:
            with self._lock_flush:
                self._logger.debug("AutoFlush is_final received")
                self._last_datagram = None
        else:
            with self._lock_flush:
                self._last_datagram = datetime.now()
                self._logger.debug(
                    "AutoFlush interim received: %s",
                    str(self._last_datagram),
                )

        return True
