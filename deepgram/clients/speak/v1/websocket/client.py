# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import time
import logging
from typing import Dict, Union, Optional, cast, Any
from datetime import datetime
import threading

from websockets.sync.client import connect, ClientConnection
import websockets

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import SpeakWebSocketEvents, SpeakWebSocketMessage
from .helpers import convert_to_websocket_url, append_query_params
from ....common.v1.errors import DeepgramError

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

from .....audio.speaker import Speaker, RATE, CHANNELS

ONE_SECOND = 1
HALF_SECOND = 0.5
DEEPGRAM_INTERVAL = 5
PING_INTERVAL = 20


class SpeakWSClient:  # pylint: disable=too-many-instance-attributes
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

    _socket: ClientConnection
    _exit_event: threading.Event
    _lock_send: threading.Lock
    _event_handlers: Dict[SpeakWebSocketEvents, list]

    _listen_thread: Union[threading.Thread, None]
    _flush_thread: Union[threading.Thread, None]
    _lock_flush: threading.Lock
    _last_datagram: Optional[datetime] = None
    _flush_count: int

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    _speaker: Optional[Speaker] = None

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config
        self._endpoint = "v1/speak"
        self._lock_send = threading.Lock()
        self._lock_flush = threading.Lock()

        self._listen_thread = None
        self._flush_thread = None

        # exit
        self._exit_event = threading.Event()

        # flush
        self._last_datagram = None
        self._flush_count = 0

        # init handlers
        self._event_handlers = {
            event: [] for event in SpeakWebSocketEvents.__members__.values()
        }
        self._websocket_url = convert_to_websocket_url(self._config.url, self._endpoint)

        if self._config.options.get("speaker_playback") == "true":
            self._logger.info("speaker_playback is enabled")
            rate = self._config.options.get("speaker_playback_rate")
            if rate is None:
                rate = RATE
            channels = self._config.options.get("speaker_playback_channels")
            if channels is None:
                channels = CHANNELS
            device_index = self._config.options.get("speaker_playback_device_index")
            if device_index is not None:
                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    verbose=self._config.verbose,
                    output_device_index=device_index,
                )
            else:
                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    verbose=self._config.verbose,
                )

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
        self._logger.debug("SpeakStreamClient.start ENTER")
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, SpeakWSOptions) and not options.check():
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

        if isinstance(options, SpeakWSOptions):
            self._logger.info("SpeakWSOptions switching class -> dict")
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
            self._socket = connect(url_with_params, additional_headers=combined_headers)
            self._exit_event.clear()

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # listening thread
            if self._speaker is not None:
                self._logger.notice("speaker_playback is enabled")
                self._speaker.set_pull_callback(self._socket.recv)
                self._speaker.set_push_callback(self._process_message)
                self._speaker.start()
            else:
                self._logger.notice("create _listening thread")
                self._listen_thread = threading.Thread(target=self._listening)
                self._listen_thread.start()

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

            # push open event
            self._emit(
                SpeakWebSocketEvents(SpeakWebSocketEvents.Open),
                OpenResponse(type=SpeakWebSocketEvents.Open),
            )

            self._logger.notice("start succeeded")
            self._logger.debug("SpeakStreamClient.start LEAVE")
            return True

        except websockets.ConnectionClosed as e:
            self._logger.error("ConnectionClosed in SpeakStreamClient.start: %s", e)
            self._logger.debug("SpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise e
            return False
        except websockets.exceptions.WebSocketException as e:
            self._logger.error("WebSocketException in SpeakStreamClient.start: %s", e)
            self._logger.debug("SpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise e
            return False
        except Exception as e:  # pylint: disable=broad-except
            self._logger.error("WebSocketException in SpeakStreamClient.start: %s", e)
            self._logger.debug("SpeakStreamClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") == "true":
                raise e
            return False

    def is_connected(self) -> bool:
        """
        Returns the connection status of the WebSocket.
        """
        return self._socket is not None

    # pylint: enable=too-many-statements,too-many-branches

    def on(
        self, event: SpeakWebSocketEvents, handler
    ) -> None:  # registers event handlers for specific events
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
        self._logger.debug("callback handlers for: %s", event)
        for handler in self._event_handlers[event]:
            handler(self, *args, **kwargs)

    # pylint: disable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches
    def _listening(
        self,
    ) -> None:
        """
        Listens for messages from the WebSocket connection.
        """
        self._logger.debug("SpeakStreamClient._listening ENTER")

        while True:
            try:
                if self._exit_event.is_set():
                    self._logger.notice("_listening exiting gracefully")
                    self._logger.debug("SpeakStreamClient._listening LEAVE")
                    return

                if self._socket is None:
                    self._logger.warning("socket is empty")
                    self._logger.debug("SpeakStreamClient._listening LEAVE")
                    return

                message = self._socket.recv()

                if message is None:
                    self._logger.info("message is empty")
                    continue

                if isinstance(message, bytes):
                    self._logger.debug("Binary data received")

                    self._emit(
                        SpeakWebSocketEvents(SpeakWebSocketEvents.AudioData),
                        data=message,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                else:
                    self._logger.debug("Text data received")
                    self._process_message(message)

            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice(f"_listening({e.code}) exiting gracefully")
                self._logger.debug("SpeakStreamClient._listening LEAVE")
                return

            except websockets.exceptions.ConnectionClosed as e:
                if e.code in [1000, 1001]:
                    self._logger.notice(f"_listening({e.code}) exiting gracefully")
                    self._logger.debug("SpeakStreamClient._listening LEAVE")
                    return

                # no need to call self._signal_exit() here because we are already closed
                # note: this is different than the listen websocket client
                self._logger.notice(
                    "ConnectionClosed in SpeakStreamClient._listening with code %s: %s",
                    e.code,
                    e.reason,
                )
                self._logger.debug("SpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except websockets.exceptions.WebSocketException as e:
                self._logger.error(
                    "WebSocketException in SpeakStreamClient._listening with: %s", e
                )
                ws_error: ErrorResponse = ErrorResponse(
                    "WebSocketException in SpeakStreamClient._listening",
                    f"{e}",
                    "WebSocketException",
                )
                self._emit(SpeakWebSocketEvents(SpeakWebSocketEvents.Error), ws_error)

                # signal exit and close
                self._signal_exit()

                self._logger.debug("SpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("Exception in SpeakStreamClient._listening: %s", e)
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in SpeakStreamClient._listening",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in SpeakStreamClient._listening: %s", str(e)
                )
                self._emit(SpeakWebSocketEvents(SpeakWebSocketEvents.Error), e_error)

                # signal exit and close
                self._signal_exit()

                self._logger.debug("SpeakStreamClient._listening LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

    def _process_message(self, message: str) -> None:
        try:
            self._logger.debug("SpeakStreamClient._process_message ENTER")

            if len(message) == 0:
                self._logger.debug("message is empty")
                self._logger.debug("SpeakStreamClient._process_message LEAVE")
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

            self._logger.notice("_process_message Succeeded")
            self._logger.debug("SpeakStreamClient._process_message LEAVE")

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error("Exception in SpeakStreamClient._listening: %s", e)
            e_error: ErrorResponse = ErrorResponse(
                "Exception in SpeakStreamClient._listening",
                f"{e}",
                "Exception",
            )
            self._logger.error("Exception in SpeakStreamClient._listening: %s", str(e))
            self._emit(SpeakWebSocketEvents(SpeakWebSocketEvents.Error), e_error)

            # signal exit and close
            self._signal_exit()

            self._logger.debug("SpeakStreamClient._listening LEAVE")

            if self._config.options.get("termination_exception") == "true":
                raise
            return

    # pylint: enable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches

    # pylint: disable=too-many-return-statements,too-many-statements,too-many-branches
    def _flush(self) -> None:
        self._logger.debug("SpeakStreamClient._flush ENTER")

        delta_in_ms_str = self._config.options.get("auto_flush_speak_delta")
        if delta_in_ms_str is None:
            self._logger.error("auto_flush_speak_delta is None")
            self._logger.debug("SpeakStreamClient._flush LEAVE")
            return
        delta_in_ms = float(delta_in_ms_str)

        counter = 0
        while True:
            try:
                counter += 1
                self._exit_event.wait(timeout=HALF_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_flush exiting gracefully")
                    self._logger.debug("ListenWebSocketClient._flush LEAVE")
                    return

                if self._socket is None:
                    self._logger.notice("socket is None, exiting keep_alive")
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

            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice(f"_flush({e.code}) exiting gracefully")
                self._logger.debug("SpeakStreamClient._flush LEAVE")
                return

            except websockets.exceptions.ConnectionClosed as e:
                if e.code in [1000, 1001]:
                    self._logger.notice(f"_flush({e.code}) exiting gracefully")
                    self._logger.debug("SpeakStreamClient._flush LEAVE")
                    return

                # no need to call self._signal_exit() here because we are already closed
                # note: this is different than the listen websocket client
                self._logger.notice(
                    "ConnectionClosed in SpeakStreamClient._flush with code %s: %s",
                    e.code,
                    e.reason,
                )
                self._logger.debug("SpeakStreamClient._flush LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except websockets.exceptions.WebSocketException as e:
                self._logger.error(
                    "WebSocketException in SpeakStreamClient._flush: %s", e
                )
                ws_error: ErrorResponse = ErrorResponse(
                    "WebSocketException in SpeakStreamClient._flush",
                    f"{e}",
                    "Exception",
                )
                self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=ws_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                self._signal_exit()

                self._logger.debug("SpeakStreamClient._flush LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("Exception in SpeakStreamClient._flush: %s", e)
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in SpeakStreamClient._flush",
                    f"{e}",
                    "Exception",
                )
                self._logger.error("Exception in SpeakStreamClient._flush: %s", str(e))
                self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                self._signal_exit()

                self._logger.debug("SpeakStreamClient._flush LEAVE")

                if self._config.options.get("termination_exception") == "true":
                    raise
                return

    # pylint: enable=too-many-return-statements,too-many-statements,too-many-branches

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

    def send(self, text_input: str) -> bool:
        """
        Alias for send_text. Please see send_text for more information.
        """
        return self.send_text(text_input)

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
        self._logger.spam("SpeakStreamClient.send_raw ENTER")

        if self._exit_event.is_set():
            self._logger.notice("send exiting gracefully")
            self._logger.debug("SpeakStreamClient.send LEAVE")
            return False

        if not self.is_connected():
            self._logger.notice("is_connected is False")
            self._logger.debug("AsyncListenWebSocketClient.send LEAVE")
            return False

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

        if self._socket is not None:
            with self._lock_send:
                try:
                    self._socket.send(msg)
                except websockets.exceptions.ConnectionClosedOK as e:
                    self._logger.notice(f"send_raw() exiting gracefully: {e.code}")
                    self._logger.debug("SpeakStreamClient.send_raw LEAVE")
                    if self._config.options.get("termination_exception_send") == "true":
                        raise
                    return True
                except websockets.exceptions.ConnectionClosed as e:
                    if e.code in [1000, 1001]:
                        self._logger.notice(f"send_raw({e.code}) exiting gracefully")
                        self._logger.debug("SpeakStreamClient.send_raw LEAVE")
                        if (
                            self._config.options.get("termination_exception_send")
                            == "true"
                        ):
                            raise
                        return True
                    self._logger.error(
                        "send_raw() failed - ConnectionClosed: %s", str(e)
                    )
                    self._logger.spam("SpeakStreamClient.send_raw LEAVE")
                    if self._config.options.get("termination_exception_send") == "true":
                        raise
                    return False
                except websockets.exceptions.WebSocketException as e:
                    self._logger.error(
                        "send_raw() failed - WebSocketException: %s", str(e)
                    )
                    self._logger.spam("SpeakStreamClient.send_raw LEAVE")
                    if self._config.options.get("termination_exception_send") == "true":
                        raise
                    return False
                except Exception as e:  # pylint: disable=broad-except
                    self._logger.error("send_raw() failed - Exception: %s", str(e))
                    self._logger.spam("SpeakStreamClient.send_raw LEAVE")
                    if self._config.options.get("termination_exception_send") == "true":
                        raise
                    return False

            self._logger.spam("send_raw() succeeded")
            self._logger.spam("SpeakStreamClient.send_raw LEAVE")
            return True

        self._logger.spam("send_raw() failed. socket is None")
        self._logger.spam("SpeakStreamClient.send_raw LEAVE")
        return False

    # pylint: enable=too-many-return-statements,too-many-branches,too-many-statements

    def flush(self) -> bool:
        """
        Flushes the current buffer and returns generated audio
        """
        self._logger.spam("SpeakStreamClient.flush ENTER")

        if self._exit_event.is_set():
            self._logger.notice("flush exiting gracefully")
            self._logger.debug("SpeakStreamClient.flush LEAVE")
            return False

        if self._socket is None:
            self._logger.notice("socket is not intialized")
            self._logger.debug("SpeakStreamClient.flush LEAVE")
            return False

        self._logger.notice("Sending Flush...")
        ret = self.send_control(SpeakWebSocketMessage.Flush)

        if not ret:
            self._logger.error("flush failed")
            self._logger.spam("SpeakStreamClient.flush LEAVE")
            return False

        self._logger.notice("flush succeeded")
        self._logger.spam("SpeakStreamClient.flush LEAVE")

        return True

    def clear(self) -> bool:
        """
        Clears the current buffer on the server
        """
        self._logger.spam("SpeakStreamClient.clear ENTER")

        if self._exit_event.is_set():
            self._logger.notice("clear exiting gracefully")
            self._logger.debug("SpeakStreamClient.clear LEAVE")
            return False

        if self._socket is None:
            self._logger.notice("socket is not intialized")
            self._logger.debug("SpeakStreamClient.clear LEAVE")
            return False

        self._logger.notice("Sending Clear...")
        ret = self.send_control(SpeakWebSocketMessage.Clear)

        if not ret:
            self._logger.error("clear failed")
            self._logger.spam("SpeakStreamClient.clear LEAVE")
            return False

        self._logger.notice("clear succeeded")
        self._logger.spam("SpeakStreamClient.clear LEAVE")

        return True

    # closes the WebSocket connection gracefully
    def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.spam("SpeakStreamClient.finish ENTER")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        # signal exit
        self._signal_exit()

        # stop the threads
        if self._speaker is not None:
            self._logger.verbose("stopping speaker...")
            self._speaker.finish()
            self._speaker = None
            self._logger.notice("speaker stopped")

        if self._flush_thread is not None:
            self._logger.verbose("cancelling _flush_thread...")
            self._flush_thread.join()
            self._flush_thread = None
            self._logger.notice("_flush_thread joined")

        if self._listen_thread is not None:
            self._logger.verbose("cancelling _listen_thread...")
            self._listen_thread.join()
            self._listen_thread = None
            self._logger.notice("_listen_thread joined")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.notice("finish succeeded")
        self._logger.spam("SpeakStreamClient.finish LEAVE")
        return True

    # signals the WebSocket connection to exit
    def _signal_exit(self) -> None:
        # closes the WebSocket connection gracefully
        self._logger.notice("closing socket...")
        if self._socket is not None:
            self._logger.notice("sending Close...")
            try:
                # if the socket connection is closed, the following line might throw an error
                # need to explicitly use _socket.send (dont use self.send_raw)
                self._socket.send(json.dumps({"type": "CloseStream"}))
            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice("_signal_exit  - ConnectionClosedOK: %s", e.code)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.notice("_signal_exit  - ConnectionClosed: %s", e.code)
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("_signal_exit - WebSocketException: %s", str(e))
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_signal_exit - Exception: %s", str(e))

            # close the socket
            if self._socket is not None:
                self._socket.close()

            # push close event
            try:
                self._emit(
                    SpeakWebSocketEvents(SpeakWebSocketEvents.Close),
                    CloseResponse(type=SpeakWebSocketEvents.Close),
                )
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_signal_exit - Exception: %s", e)

            # wait for task to send
            time.sleep(0.5)

        # signal exit
        self._exit_event.set()

        # closes the WebSocket connection gracefully
        self._logger.verbose("clean up socket...")
        if self._socket is not None:
            self._logger.verbose("socket.wait_closed...")
            try:
                self._socket.close()
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("socket.wait_closed failed: %s", e)

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


class SpeakWebSocketClient(SpeakWSClient):
    """
    AsyncSpeakWebSocketClient is an alias for AsyncSpeakWSClient.
    """
