# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
from websockets.sync.client import connect
import threading
import time

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

     Attributes:
         endpoint (str): The API endpoint for live transcription.
         _socket (websockets.WebSocketClientProtocol): The WebSocket connection object.
         _event_handlers (dict): Dictionary of event handlers for specific events.
         websocket_url (str): The WebSocket URL used for connection.

     Methods:
         __call__: Establishes a WebSocket connection for live transcription.
         on: Registers event handlers for specific events.
         send: Sends data over the WebSocket connection.
         finish: Closes the WebSocket connection gracefully.
    """

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config are required")

        self.config = config
        self.endpoint = "v1/listen"
        self._socket = None
        self.exit = False
        self._event_handlers = {event: [] for event in LiveTranscriptionEvents}
        self.websocket_url = convert_to_websocket_url(self.config.url, self.endpoint)

    def start(self, options: LiveOptions = None):
        self.options = options

        if self._socket is not None:
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
            self.processing = threading.Thread(target=self._processing)
            self.processing.start()

    def on(self, event, handler):  # registers event handlers for specific events
        if event in LiveTranscriptionEvents and callable(handler):
            self._event_handlers[event].append(handler)

    def _emit(
        self, event, *args, **kwargs
    ):  # triggers the registered event handlers for a specific event
        for handler in self._event_handlers[event]:
            handler(*args, **kwargs)

    def _listening(self) -> None:
        while True:
            try:
                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    return

                message = self._socket.recv()
                if len(message) == 0:
                    #    print("empty message")
                    continue

                data = json.loads(message)
                response_type = data.get("type")
                # print(f"response_type: {response_type}")

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
                # print(f"Exception in _listening: {e}")
                if e.code == 1000:
                    # print("Websocket closed")
                    return

                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error _listening",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)

    def _processing(self) -> None:
        # print("Starting KeepAlive")
        while True:
            try:
                time.sleep(PING_INTERVAL)

                self.lock_exit.acquire()
                myExit = self.exit
                self.lock_exit.release()
                if myExit:
                    return

                # deepgram keepalive
                # print("Sending KeepAlive")
                self.send(json.dumps({"type": "KeepAlive"}))

            except Exception as e:
                # print(f"Exception in _processing: {e}")
                if e.code == 1000:
                    # print("Websocket closed")
                    return

                error: ErrorResponse = {
                    "type": "Exception",
                    "description": "Unknown error in _processing",
                    "message": f"{e}",
                    "variant": "",
                }
                self._emit(LiveTranscriptionEvents.Error, error)

    def send(self, data) -> int:
        if self._socket:
            self.lock_send.acquire()
            ret = self._socket.send(data)
            self.lock_send.release()
            return ret
        return 0

    def finish(self):
        #   print("Send CloseStream")
        if self._socket:
            self._socket.send(json.dumps({"type": "CloseStream"}))
            time.sleep(1)

        #   print("Closing connection...")
        self.lock_exit.acquire()
        self.exit = True
        self.lock_exit.release()

        #   print("Waiting for threads to finish...")
        if self.processing is not None:
            self.processing.join()
            self.processing = None

        #   print("Waiting for threads to finish...")
        if self.listening is not None:
            self.listening.join()
            self.listening = None

        if self._socket:
            self._socket.close()

        self._socket = None
        self.lock_exit = None
