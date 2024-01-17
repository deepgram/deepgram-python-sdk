# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
from websockets.sync.client import connect
import websockets
import threading
import time
import logging, verboselogs

from ....options import DeepgramClientOptions
from ..enums import LiveTranscriptionEvents
from ..helpers import convert_to_websocket_url, append_query_params
from ..errors import DeepgramError, DeepgramWebsocketError

from .response import (
    LiveResultResponse,
    MetadataResponse,
    UtteranceEndResponse,
    ErrorResponse,
)
from .options import LiveOptions

PING_INTERVAL = 5


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
        self.exit = False
        self._event_handlers = {event: [] for event in LiveTranscriptionEvents}
        self.websocket_url = convert_to_websocket_url(self.config.url, self.endpoint)

    def start(self, options: LiveOptions = None, addons: dict = None, **kwargs):
        """
        Starts the WebSocket connection for live transcription.
        """
        self.logger.debug("LiveClient.start ENTER")
        self.logger.info("kwargs: %s", options)
        self.logger.info("addon: %s", addons)
        self.logger.info("options: %s", kwargs)

        if options is not None and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("LiveClient.start LEAVE")
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

        if self._socket is not None:
            self.logger.error("socket is already initialized")
            self.logger.debug("LiveClient.start LEAVE")
            raise DeepgramWebsocketError("Websocket already started")

        url_with_params = append_query_params(self.websocket_url, self.options)
        self._socket = connect(url_with_params, additional_headers=self.config.headers)

        self.exit = False
        self.lock_exit = threading.Lock()
        self.lock_send = threading.Lock()

        # listening thread
        self.listening = threading.Thread(target=self._listening)
        self.listening.start()

        # keepalive thread
        self.processing = threading.Thread(target=self._processing)
        self.processing.start()

        self.logger.notice("start succeeded")
        self.logger.debug("LiveClient.start LEAVE")

    def on(self, event, handler):
        """
        Registers event handlers for specific events.
        """
        self.logger.info("event fired: %s", event)
        if event in LiveTranscriptionEvents and callable(handler):
            self._event_handlers[event].append(handler)

    def _emit(self, event, *args, **kwargs):
        for handler in self._event_handlers[event]:
            handler(self, *args, **kwargs)

    def _listening(self) -> None:
        self.logger.debug("LiveClient._listening ENTER")

        while True:
            try:
                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    self.logger.notice("_listening exiting gracefully")
                    self.logger.debug("LiveClient._listening LEAVE")
                    return

                message = self._socket.recv()
                if len(message) == 0:
                    self.logger.info("message is empty")
                    continue

                data = json.loads(message)
                response_type = data.get("type")
                self.logger.verbose("response_type: %s", response_type)

                match response_type:
                    case LiveTranscriptionEvents.Transcript.value:
                        self.logger.debug(
                            "response_type: %s, data: %s", response_type, data
                        )
                        result = LiveResultResponse.from_json(message)
                        if result is None:
                            self.logger.error("LiveResultResponse.from_json is None")
                            continue
                        self._emit(
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
                        self._emit(
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
                        self._emit(
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
                        self._emit(
                            LiveTranscriptionEvents.Error,
                            error=result,
                            **dict(self.kwargs),
                        )
                    case _:
                        self.logger.warning(
                            "Unknown Message: response_type: %s, data: %s",
                            response_type,
                            data,
                        )

            except websockets.exceptions.ConnectionClosedOK as e:
                if e.code == 1000:
                    self.logger.notice("_listening(1000) exiting gracefully")
                    self.logger.debug("LiveClient._listening LEAVE")
                    return
                else:
                    error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                    self.logger.error(f"WebSocket connection closed with code {e.code}: {e.reason}")
                    self._emit(LiveTranscriptionEvents.Error, error)
                    self.logger.debug("LiveClient._listening LEAVE")
                    raise

            except Exception as e:
                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)
                self.logger.error("Exception in _listening: %s", str(e))
                self.logger.debug("LiveClient._listening LEAVE")
                raise

    def _processing(self) -> None:
        self.logger.debug("LiveClient._processing ENTER")

        counter = 0

        while True:
            try:
                time.sleep(PING_INTERVAL)
                counter += 1

                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    self.logger.notice("_processing exiting gracefully")
                    self.logger.debug("LiveClient._processing LEAVE")
                    return

                # deepgram keepalive
                if self.config.options.get("keepalive") == "true":
                    self.logger.debug("Sending KeepAlive...")
                    self.send(json.dumps({"type": "KeepAlive"}))

                # websocket keepalive
                if counter % 4 == 0:
                    self.logger.debug("Sending Ping...")
                    self.send_ping()

            except Exception as e:
                if e.code == 1000:
                    self.logger.notice("_processing(1000) exiting gracefully")
                    self.logger.debug("LiveClient._processing LEAVE")
                    return

                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error in _processing",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)

                self.logger.error("Exception in _processing: %s", str(e))
                self.logger.debug("LiveClient._processing LEAVE")

    def send(self, data) -> int:
        """
        Sends data over the WebSocket connection.
        """
        self.logger.spam("LiveClient.send ENTER")
        self.logger.spam("data: %s", data)

        if self._socket:
            self.lock_send.acquire()
            ret = self._socket.send(data)
            self.lock_send.release()

            self.logger.spam(f"send bytes: {ret}")
            self.logger.spam("LiveClient.send LEAVE")
            return ret

        self.logger.spam("message is empty")
        self.logger.spam("LiveClient.send LEAVE")
        return 0

    def send_ping(self) -> None:
        """
        Sends a ping over the WebSocket connection.
        """
        self.logger.spam("LiveClient.send_ping ENTER")

        if self._socket:
            self.lock_send.acquire()
            self._socket.ping()
            self.lock_send.release()

        self.logger.spam("LiveClient.send_ping LEAVE")

    def finish(self):
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.spam("LiveClient.finish ENTER")

        if self._socket:
            self.logger.notice("sending CloseStream...")
            self.send(json.dumps({"type": "CloseStream"}))
            time.sleep(0.5)

        self.lock_exit.acquire()
        self.logger.notice("signal exit")
        self.exit = True
        self.lock_exit.release()

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
        self.lock_exit = None
        self.lock_send = None

        self.logger.notice("finish succeeded")
        self.logger.spam("LiveClient.finish LEAVE")
