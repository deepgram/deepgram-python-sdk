# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
from websockets.sync.client import connect
import websockets
import threading
import time
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


class LiveClient:
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
        self.exit_event = None
        self._event_handlers = {event: [] for event in LiveTranscriptionEvents}
        self.websocket_url = convert_to_websocket_url(self.config.url, self.endpoint)

    # starts the WebSocket connection for live transcription
    def start(
        self,
        options: Optional[Union[LiveOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for live transcription.
        """
        self.logger.debug("LiveClient.start ENTER")
        self.logger.info("kwargs: %s", options)
        self.logger.info("addons: %s", addons)
        self.logger.info("members: %s", members)
        self.logger.info("options: %s", kwargs)

        if isinstance(options, LiveOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("LiveClient.start LEAVE")
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
        self._socket = connect(url_with_params, additional_headers=self.config.headers)

        self.exit_event = threading.Event()
        self.lock_send = threading.Lock()

        # listening thread
        self.listening = threading.Thread(target=self._listening)
        self.listening.start()

        # keepalive thread
        self.processing = threading.Thread(target=self._keep_alive)
        self.processing.start()

        # push open event
        self._emit(
            LiveTranscriptionEvents.Open,
            OpenResponse(type=LiveTranscriptionEvents.Open.value),
        )

        self.logger.notice("start succeeded")
        self.logger.debug("LiveClient.start LEAVE")
        return True

    # registers event handlers for specific events
    def on(self, event, handler):
        """
        Registers event handlers for specific events.
        """
        self.logger.info("event fired: %s", event)
        if event in LiveTranscriptionEvents and callable(handler):
            self._event_handlers[event].append(handler)

    # unregisters event handlers for specific events
    def _emit(self, event, *args, **kwargs):
        for handler in self._event_handlers[event]:
            handler(self, *args, **kwargs)

    # main loop for handling incoming messages
    def _listening(self) -> None:
        self.logger.debug("LiveClient._listening ENTER")

        while True:
            try:
                message = self._socket.recv()

                if self.exit_event.is_set():
                    self.logger.notice("_listening exiting gracefully")
                    self.logger.debug("LiveClient._listening LEAVE")
                    return

                if len(message) == 0:
                    self.logger.info("message is empty")
                    continue

                data = json.loads(message)
                response_type = data.get("type")
                self.logger.debug("response_type: %s, data: %s", response_type, data)

                match response_type:
                    case LiveTranscriptionEvents.Open.value:
                        result = OpenResponse.from_json(message)
                        self.logger.verbose("OpenResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.Open,
                            open=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Transcript.value:
                        result = LiveResultResponse.from_json(message)
                        self.logger.verbose("LiveResultResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.Transcript,
                            result=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Metadata.value:
                        result = MetadataResponse.from_json(message)
                        self.logger.verbose("MetadataResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.Metadata,
                            metadata=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.SpeechStarted.value:
                        result = SpeechStartedResponse.from_json(message)
                        self.logger.verbose("SpeechStartedResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.SpeechStarted,
                            speech_started=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.UtteranceEnd.value:
                        result = UtteranceEndResponse.from_json(message)
                        self.logger.verbose("UtteranceEndResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.UtteranceEnd,
                            utterance_end=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Error.value:
                        result = ErrorResponse.from_json(message)
                        self.logger.verbose("ErrorResponse: %s", result)
                        self._emit(
                            LiveTranscriptionEvents.Error,
                            error=result,
                            **dict(self.kwargs),
                        )
                    case LiveTranscriptionEvents.Close.value:
                        result = CloseResponse.from_json(message)
                        self.logger.verbose("CloseResponse: %s", result)
                        self._emit(
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

            except websockets.exceptions.ConnectionClosedOK as e:
                self.logger.notice(f"_listening({e.code}) exiting gracefully")

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._listening LEAVE")
                return

            except websockets.exceptions.ConnectionClosedError as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "ConnectionClosedError in _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.notice(
                    f"WebSocket connection in _listening closed with code {e.code}: {e.reason}"
                )
                self._emit(LiveTranscriptionEvents.Error, error)

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._listening LEAVE")

                if (
                    "termination_exception" in self.options
                    and self.options["termination_exception"] == "true"
                ):
                    raise
                return

            except Exception as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Exception in _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error("Exception in _listening: %s", str(e))
                self._emit(LiveTranscriptionEvents.Error, error)

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._listening LEAVE")
                if (
                    "termination_exception" in self.options
                    and self.options["termination_exception"] == "true"
                ):
                    raise
                return

    def _keep_alive(self) -> None:
        self.logger.debug("LiveClient._keep_alive ENTER")

        counter = 0

        while True:
            try:
                counter += 1

                self.exit_event.wait(timeout=ONE_SECOND)
                if self.exit_event.is_set():
                    self.logger.notice("_keep_alive exiting gracefully")
                    self.logger.debug("LiveClient._keep_alive LEAVE")
                    return

                # deepgram keepalive
                if (
                    counter % DEEPGRAM_INTERVAL == 0
                    and self.config.options.get("keepalive") == "true"
                ):
                    self.logger.verbose("Sending KeepAlive...")
                    try:
                        self.send(json.dumps({"type": "KeepAlive"}))
                    except websockets.exceptions.WebSocketException as e:
                        self.logger.error("KeepAlive failed: %s", e)

                # websocket keepalive
                if counter % PING_INTERVAL == 0:
                    self.logger.verbose("Sending Protocol Ping...")
                    self.send_ping()

            except websockets.exceptions.ConnectionClosedOK as e:
                self.logger.notice(f"_keep_alive({e.code}) exiting gracefully")

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._keep_alive LEAVE")
                return

            except websockets.exceptions.ConnectionClosedError as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "ConnectionClosedError in _keep_alive",
                    "message": f"{e}",
                    "variant": "",
                }
                self.logger.error(
                    f"WebSocket connection closed in _keep_alive with code {e.code}: {e.reason}"
                )
                self._emit(LiveTranscriptionEvents.Error, error)

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._keep_alive LEAVE")

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
                self._emit(LiveTranscriptionEvents.Error, error)
                self.logger.error("Exception in _keep_alive: %s", str(e))

                # signal exit and close
                self.signal_exit()

                self.logger.debug("LiveClient._keep_alive LEAVE")

                if (
                    "termination_exception" in self.options
                    and self.options["termination_exception"] == "true"
                ):
                    raise
                return

    # sends data over the WebSocket connection
    def send(self, data: Union[str, bytes]) -> int:
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("LiveClient.send ENTER")
        self.logger.spam("data: %s", data)

        if self._socket:
            with self.lock_send:
                cnt = self._socket.send(data)

            self.logger.spam(f"send() succeeded. bytes: {cnt}")
            self.logger.spam("LiveClient.send LEAVE")
            return cnt

        self.logger.spam("send() failed. socket is empty")
        self.logger.spam("LiveClient.send LEAVE")
        return 0

    # sends a ping over the WebSocket connection
    def send_ping(self) -> None:
        """
        Sends a ping over the WebSocket connection.
        """
        self.logger.spam("LiveClient.send_ping ENTER")

        if self._socket:
            with self.lock_send:
                self.logger.debug("socket.ping() succeeded.")
                self._socket.ping()

        self.logger.spam("LiveClient.send_ping LEAVE")

    # closes the WebSocket connection gracefully
    def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.spam("LiveClient.finish ENTER")

        if self._socket:
            self.logger.notice("sending CloseStream...")
            self.send(json.dumps({"type": "CloseStream"}))

            time.sleep(0.5)

            # push close event
            self._emit(
                LiveTranscriptionEvents.Close,
                CloseResponse(type=LiveTranscriptionEvents.Close.value),
            )

        # signal exit
        self.signal_exit()

        if self.processing is not None:
            self.processing.join()
            self.processing = None
        self.logger.notice("processing thread joined")

        if self.listening is not None:
            self.listening.join()
            self.listening = None
        self.logger.notice("listening thread joined")

        if self._socket is not None:
            self.logger.notice("closing socket...")
            self._socket.close()

        self._socket = None
        self.exit_event = None
        self.lock_send = None

        self.logger.notice("finish succeeded")
        self.logger.spam("LiveClient.finish LEAVE")
        return True

    # signals the WebSocket connection to exit
    def signal_exit(self) -> None:
        # signal exit
        self.exit_event.set()

        self.logger.notice("closing socket...")
        if self._socket:
            self.logger.debug("calling socket.close()")
            self._socket.close()
        self._socket = None
