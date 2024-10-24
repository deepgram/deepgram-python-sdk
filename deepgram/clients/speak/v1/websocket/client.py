# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import time
import logging
from typing import Dict, Union, Optional, cast, Any, Callable
from datetime import datetime
import threading

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import SpeakWebSocketEvents, SpeakWebSocketMessage
from ....common import AbstractSyncWebSocketClient
from ....common import DeepgramError

from .response import (
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    ClearedResponse,
    CloseResponse,
    WarningResponse,
    ErrorResponse,
    UnhandledResponse,
)
from .options import SpeakWSOptions

from .....audio.microphone import Microphone
from .....audio.speaker import Speaker, RATE, CHANNELS, PLAYBACK_DELTA

ONE_SECOND = 1
HALF_SECOND = 0.5
DEEPGRAM_INTERVAL = 5
PING_INTERVAL = 20


class SpeakWSClient(
    AbstractSyncWebSocketClient
):  # pylint: disable=too-many-instance-attributes
    """
    Client for interacting with Deepgram's text-to-speech services over WebSockets.

     This class provides methods to establish a WebSocket connection for TTS synthesis and handle real-time TTS synthesis events.

     Args:
         config (DeepgramClientOptions): all the options for the client.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    _event_handlers: Dict[SpeakWebSocketEvents, list]

    _flush_thread: Union[threading.Thread, None]
    _lock_flush: threading.Lock
    _last_datagram: Optional[datetime] = None
    _flush_count: int

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    _speaker_created: bool = False
    _speaker: Optional[Speaker] = None
    _microphone: Optional[Microphone] = None

    def __init__(
        self, config: DeepgramClientOptions, microphone: Optional[Microphone] = None
    ):
        if config is None:
            raise DeepgramError("Config is required")

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config
        self._endpoint = "v1/speak"
        self._lock_flush = threading.Lock()

        self._flush_thread = None

        # auto flush
        self._last_datagram = None
        self._flush_count = 0

        # microphone
        self._microphone = microphone

        # init handlers
        self._event_handlers = {
            event: [] for event in SpeakWebSocketEvents.__members__.values()
        }

        if self._config.options.get("speaker_playback") == "true":
            self._logger.info("speaker_playback is enabled")
            rate = self._config.options.get("speaker_playback_rate")
            if rate is None:
                rate = RATE
            channels = self._config.options.get("speaker_playback_channels")
            if channels is None:
                channels = CHANNELS
            playback_delta_in_ms = self._config.options.get(
                "speaker_playback_delta_in_ms"
            )
            if playback_delta_in_ms is None:
                playback_delta_in_ms = PLAYBACK_DELTA
            device_index = self._config.options.get("speaker_playback_device_index")

            self._logger.debug("rate: %s", rate)
            self._logger.debug("channels: %s", channels)
            self._logger.debug("device_index: %s", device_index)

            self._speaker_created = True

            if device_index is not None:
                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    last_play_delta_in_ms=playback_delta_in_ms,
                    verbose=self._config.verbose,
                    output_device_index=device_index,
                    microphone=self._microphone,
                )
            else:
                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    last_play_delta_in_ms=playback_delta_in_ms,
                    verbose=self._config.verbose,
                    microphone=self._microphone,
                )

        # call the parent constructor
        super().__init__(self._config, self._endpoint)

    # pylint: disable=too-many-statements,too-many-branches
    def start(
        self,
        options: Optional[Union[SpeakWSOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for text-to-speech synthesis.
        """
        self._logger.debug("SpeakWebSocketClient.start ENTER")
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, SpeakWSOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("SpeakWebSocketClient.start LEAVE")
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

        if isinstance(options, SpeakWSOptions):
            self._logger.info("SpeakWSOptions switching class -> dict")
            self._options = options.to_dict()
        elif options is not None:
            self._options = options
        else:
            self._options = {}

        try:
            # speaker substitutes the listening thread
            if self._speaker is not None:
                self._logger.notice("passing speaker to delegate_listening")
                super().delegate_listening(self._speaker)

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
                self._logger.error("SpeakWebSocketClient.start failed")
                self._logger.debug("SpeakWebSocketClient.start LEAVE")
                return False

            if self._speaker is not None:
                self._logger.notice("start delegate_listening thread")
                self._speaker.start()

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # flush thread
            if self._config.is_auto_flush_speak_enabled():
                self._logger.notice("autoflush is enabled")
                self._flush_thread = threading.Thread(target=self._flush)
                self._flush_thread.start()
            else:
                self._logger.notice("autoflush is disabled")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("start succeeded")
            self._logger.debug("SpeakWebSocketClient.start LEAVE")
            return True

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in SpeakWebSocketClient.start: %s", e
            )
            self._logger.debug("SpeakWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") is True:
                raise
            return False

    # pylint: enable=too-many-statements,too-many-branches

    def on(self, event: SpeakWebSocketEvents, handler: Callable) -> None:
        """
        Registers event handlers for specific events.
        """
        self._logger.info("event subscribed: %s", event)
        if event in SpeakWebSocketEvents.__members__.values() and callable(handler):
            self._event_handlers[event].append(handler)

    def _emit(self, event: SpeakWebSocketEvents, *args, **kwargs) -> None:
        """
        Emits events to the registered event handlers.
        """
        self._logger.debug("SpeakWebSocketClient._emit ENTER")
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

    def _process_text(self, message: str) -> None:
        """
        Processes messages received over the WebSocket connection.
        """
        self._logger.debug("SpeakWebSocketClient._process_text ENTER")

        try:
            self._logger.debug("Text data received")

            if len(message) == 0:
                self._logger.debug("message is empty")
                self._logger.debug("SpeakWebSocketClient._process_text LEAVE")
                return

            data = json.loads(message)
            response_type = data.get("type")
            self._logger.debug("response_type: %s, data: %s", response_type, data)

            match response_type:
                case SpeakWebSocketEvents.Open:
                    open_result: OpenResponse = OpenResponse.from_json(message)
                    self._logger.verbose("OpenResponse: %s", open_result)
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Open),
                        open=open_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Metadata:
                    meta_result: MetadataResponse = MetadataResponse.from_json(message)
                    self._logger.verbose("MetadataResponse: %s", meta_result)
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Metadata),
                        metadata=meta_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Flushed:
                    fl_result: FlushedResponse = FlushedResponse.from_json(message)
                    self._logger.verbose("FlushedResponse: %s", fl_result)

                    # auto flush
                    if self._config.is_inspecting_speak():
                        with self._lock_flush:
                            self._flush_count -= 1
                            self._logger.debug(
                                "Decrement Flush count: %d",
                                self._flush_count,
                            )

                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Flushed),
                        flushed=fl_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Cleared:
                    clear_result: ClearedResponse = ClearedResponse.from_json(message)
                    self._logger.verbose("ClearedResponse: %s", meta_result)
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Cleared),
                        cleared=clear_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Close:
                    close_result: CloseResponse = CloseResponse.from_json(message)
                    self._logger.verbose("CloseResponse: %s", close_result)
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Close),
                        close=close_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Warning:
                    war_warning: WarningResponse = WarningResponse.from_json(message)
                    self._logger.verbose("WarningResponse: %s", war_warning)
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Warning),
                        warning=war_warning,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case SpeakWebSocketEvents.Error:
                    err_error: ErrorResponse = ErrorResponse.from_json(message)
                    self._logger.verbose("ErrorResponse: %s", err_error)
                    self._emit(
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
                        type=SpeakWebSocketEvents(SpeakWebSocketEvents.Unhandled),
                        raw=message,
                    )
                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.Unhandled),
                        unhandled=unhandled_error,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )

            self._logger.notice("_process_text Succeeded")
            self._logger.debug("SpeakWebSocketClient._process_text LEAVE")

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error("Exception in SpeakWebSocketClient._process_text: %s", e)
            e_error: ErrorResponse = ErrorResponse(
                "Exception in SpeakWebSocketClient._process_text",
                f"{e}",
                "Exception",
            )
            self._logger.error(
                "Exception in SpeakWebSocketClient._process_text: %s", str(e)
            )
            self._emit(
                SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                e_error,
                **dict(cast(Dict[Any, Any], self._kwargs)),
            )

            # signal exit and close
            super()._signal_exit()

            self._logger.debug("SpeakWebSocketClient._process_text LEAVE")

            if self._config.options.get("termination_exception") is True:
                raise
            return

    # pylint: enable=too-many-return-statements,too-many-statements

    def _process_binary(self, message: bytes) -> None:
        self._logger.debug("SpeakWebSocketClient._process_binary ENTER")
        self._logger.debug("Binary data received")

        self._emit(
            SpeakWebSocketEvents(SpeakWebSocketEvents.AudioData),
            data=message,
            **dict(cast(Dict[Any, Any], self._kwargs)),
        )

        self._logger.notice("_process_binary Succeeded")
        self._logger.debug("SpeakWebSocketClient._process_binary LEAVE")

    # pylint: disable=too-many-return-statements
    def _flush(self) -> None:
        self._logger.debug("SpeakWebSocketClient._flush ENTER")

        delta_in_ms_str = self._config.options.get("auto_flush_speak_delta")
        if delta_in_ms_str is None:
            self._logger.error("auto_flush_speak_delta is None")
            self._logger.debug("SpeakWebSocketClient._flush LEAVE")
            return
        delta_in_ms = float(delta_in_ms_str)

        while True:
            try:
                self._exit_event.wait(timeout=HALF_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_flush exiting gracefully")
                    self._logger.debug("ListenWebSocketClient._flush LEAVE")
                    return

                if self._last_datagram is None:
                    self._logger.debug("AutoFlush last_datagram is None")
                    continue

                with self._lock_flush:
                    delta = datetime.now() - self._last_datagram
                    diff_in_ms = delta.total_seconds() * 1000
                    self._logger.debug("AutoFlush delta: %f", diff_in_ms)
                    if diff_in_ms < delta_in_ms:
                        self._logger.debug("AutoFlush delta is less than threshold")
                        continue

                self.flush()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("Exception in SpeakWebSocketClient._flush: %s", e)
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in SpeakWebSocketClient._flush",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in SpeakWebSocketClient._flush: %s", str(e)
                )
                self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                super()._signal_exit()

                self._logger.debug("SpeakWebSocketClient._flush LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    # pylint: enable=too-many-return-statements

    def send_text(self, text_input: str) -> bool:
        """
        Sends text to the WebSocket connection to generate audio.

        Args:
            text_input (str): The raw text to be synthesized. This function will automatically wrap
                the text in a JSON object of type "Speak" with the key "text".

        Returns:
            bool: True if the text was successfully sent, False otherwise.
        """
        return self.send_raw(json.dumps({"type": "Speak", "text": text_input}))

    def send(self, data: Union[str, bytes]) -> bool:
        """
        Alias for send_text. Please see send_text for more information.
        """
        if isinstance(data, bytes):
            self._logger.error("send() failed - data is bytes")
            return False

        return self.send_text(data)

    # pylint: disable=unused-argument
    def send_control(
        self, msg_type: Union[SpeakWebSocketMessage, str], data: Optional[str] = ""
    ) -> bool:
        """
        Sends a control message consisting of type SpeakWebSocketEvents over the WebSocket connection.

        Args:
            msg_type (SpeakWebSocketEvents): The type of control message to send.
            (Optional) data (str): The data to send with the control message.

        Returns:
            bool: True if the control message was successfully sent, False otherwise.
        """
        control_msg = json.dumps({"type": msg_type})
        return self.send_raw(control_msg)

    # pylint: enable=unused-argument

    # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
    def send_raw(self, msg: str) -> bool:
        """
        Sends a raw/control message over the WebSocket connection. This message must contain a valid JSON object.

        Args:
            msg (str): The raw message to send over the WebSocket connection.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """
        self._logger.spam("SpeakWebSocketClient.send_raw ENTER")

        if self._config.is_inspecting_speak():
            try:
                _tmp_json = json.loads(msg)
                if "type" in _tmp_json:
                    self._logger.debug(
                        "Inspecting Message: Sending %s", _tmp_json["type"]
                    )
                    match _tmp_json["type"]:
                        case SpeakWebSocketMessage.Speak:
                            inspect_res = self._inspect()
                            if not inspect_res:
                                self._logger.error("inspect_res failed")
                        case SpeakWebSocketMessage.Flush:
                            with self._lock_flush:
                                self._last_datagram = None
                                self._flush_count += 1
                                self._logger.debug(
                                    "Increment Flush count: %d", self._flush_count
                                )
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("send_raw() failed - Exception: %s", str(e))

        try:
            if super().send(msg) is False:
                self._logger.error("send_raw() failed")
                self._logger.spam("SpeakWebSocketClient.send_raw LEAVE")
                return False
            self._logger.spam("send_raw() succeeded")
            self._logger.spam("SpeakWebSocketClient.send_raw LEAVE")
            return True
        except Exception as e:  # pylint: disable=broad-except
            self._logger.error("send_raw() failed - Exception: %s", str(e))
            self._logger.spam("SpeakWebSocketClient.send_raw LEAVE")
            if self._config.options.get("termination_exception_send") is True:
                raise
            return False

    # pylint: enable=too-many-return-statements,too-many-branches

    def flush(self) -> bool:
        """
        Flushes the current buffer and returns generated audio
        """
        self._logger.spam("SpeakWebSocketClient.flush ENTER")

        self._logger.notice("Sending Flush...")
        ret = self.send_control(SpeakWebSocketMessage.Flush)

        if not ret:
            self._logger.error("flush failed")
            self._logger.spam("SpeakWebSocketClient.flush LEAVE")
            return False

        self._logger.notice("flush succeeded")
        self._logger.spam("SpeakWebSocketClient.flush LEAVE")

        return True

    def clear(self) -> bool:
        """
        Clears the current buffer on the server
        """
        self._logger.spam("SpeakWebSocketClient.clear ENTER")

        self._logger.notice("Sending Clear...")
        ret = self.send_control(SpeakWebSocketMessage.Clear)

        if not ret:
            self._logger.error("clear failed")
            self._logger.spam("SpeakWebSocketClient.clear LEAVE")
            return False

        self._logger.notice("clear succeeded")
        self._logger.spam("SpeakWebSocketClient.clear LEAVE")

        return True

    def wait_for_complete(self):
        """
        This method will block until the speak is done playing sound.
        """
        self._logger.spam("SpeakWebSocketClient.wait_for_complete ENTER")

        if self._speaker is None:
            self._logger.error("speaker is None. Return immediately")
            raise DeepgramError("Speaker is not initialized")

        self._speaker.wait_for_complete()
        self._logger.notice("wait_for_complete succeeded")
        self._logger.spam("SpeakWebSocketClient.wait_for_complete LEAVE")

    def _close_message(self) -> bool:
        return self.send_control(SpeakWebSocketMessage.Close)

    # closes the WebSocket connection gracefully
    def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.spam("SpeakWebSocketClient.finish ENTER")

        # call parent finish which calls signal_exit
        if super().finish() is False:
            self._logger.error("ListenWebSocketClient.finish failed")

        if self._speaker is not None and self._speaker_created:
            self._speaker.finish()
            self._speaker_created = False

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        # stop the threads
        if self._speaker is not None:
            self._logger.verbose("stopping speaker...")
            self._speaker.finish()
            self._speaker = None
            self._logger.notice("speaker stopped")

        if self._flush_thread is not None:
            self._logger.verbose("sdtopping _flush_thread...")
            self._flush_thread.join()
            self._flush_thread = None
            self._logger.notice("_flush_thread joined")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.notice("finish succeeded")
        self._logger.spam("SpeakWebSocketClient.finish LEAVE")
        return True

    def _inspect(self) -> bool:
        # auto flush_inspect is generically used to track any messages you might want to snoop on
        # place additional logic here to inspect messages of interest

        # for auto flush functionality
        # set the last datagram
        with self._lock_flush:
            self._last_datagram = datetime.now()
            self._logger.debug(
                "AutoFlush last received: %s",
                str(self._last_datagram),
            )

        return True


SpeakWebSocketClient = SpeakWSClient
