# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
from websockets.sync.client import connect
import threading
import time
import logging, verboselogs

from ....options import DeepgramClientOptions
from ..enums import LiveTranscriptionEvents
from ..helpers import convert_to_websocket_url, append_query_params
from ..errors import DeepgramError, DeepgramWebsocketError

from .response import LiveResultResponse, MetadataResponse, ErrorResponse
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

    def start(self, options: LiveOptions = None):
        """
        Starts the WebSocket connection for live transcription.
        """
        self.logger.debug("LiveClient.start ENTER")
        self.logger.info("options: %s", options)

        self.options = options
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
        self.processing = None
        if self.config.options.get("keepalive") == "true":
            self.logger.info("KeepAlive enabled")
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

    def _emit(
        self, event, *args, **kwargs
    ):
        for handler in self._event_handlers[event]:
            handler(*args, **kwargs)

    def _listening(self) -> None:
        self.logger.debug("LiveClient._listening ENTER")

        while True:
            try:
                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    self.logger.notice("exiting gracefully")
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
                        result = LiveResultResponse.from_json(message)
                        self._emit(LiveTranscriptionEvents.Transcript, result=result)
                    case LiveTranscriptionEvents.Metadata.value:
                        result = MetadataResponse.from_json(message)
                        self._emit(LiveTranscriptionEvents.Metadata, metadata=result)
                    case LiveTranscriptionEvents.Error.value:
                        result = ErrorResponse.from_json(message)
                        self._emit(LiveTranscriptionEvents.Error, error=result)
                    case _:
                        error: ErrorResponse = {
                            "type": "UnhandledMessage",
                            "description": "Unknown message type",
                            "message": f"Unhandle message type: {response_type}",
                            "variant": "",
                        }
                        self._emit(LiveTranscriptionEvents.Error, error)

            except Exception as e:
                if e.code == 1000:
                    self.logger.notice("exiting thread gracefully")
                    self.logger.debug("LiveClient._listening LEAVE")
                    return

                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)

                self.logger.error("Exception in _listening: %s", str(e))
                self.logger.debug("LiveClient._listening LEAVE")

    def _processing(self) -> None:
        self.logger.debug("LiveClient._processing ENTER")

        while True:
            try:
                time.sleep(PING_INTERVAL)

                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    self.logger.notice("exiting gracefully")
                    self.logger.debug("LiveClient._processing LEAVE")
                    return

                # deepgram keepalive
                self.logger.debug("Sending KeepAlive...")
                self.send(json.dumps({"type": "KeepAlive"}))

            except Exception as e:
                if e.code == 1000:
                    self.logger.notice("exiting thread gracefully")
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

            self.logger.spam("send bytes: %d", ret)
            self.logger.spam("LiveClient.send LEAVE")
            return ret

        self.logger.spam("message is empty")
        self.logger.spam("LiveClient.send LEAVE")
        return 0

    def finish(self):
        """
        Closes the WebSocket connection gracefully.
        """
        self.logger.spam("LiveClient.finish ENTER")

        if self._socket:
            self.logger.notice("sending CloseStream...")
            self._socket.send(json.dumps({"type": "CloseStream"}))
            time.sleep(1)

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

        if self._socket:
            self.logger.notice("closing socket...")
            self._socket.close()

        self._socket = None
        self.lock_exit = None

        self.logger.notice("finish succeeded")
        self.logger.spam("LiveClient.finish LEAVE")
