# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT
import json
import time
import logging
from typing import Dict, Union, Optional, cast, Any, Callable, Type
from datetime import datetime
import threading
from abc import ABC, abstractmethod

from websockets.sync.client import connect, ClientConnection
import websockets

from ....audio import Speaker
from ....utils import verboselogs
from ....options import DeepgramClientOptions
from .helpers import convert_to_websocket_url, append_query_params
from .errors import DeepgramError

from .websocket_response import (
    OpenResponse,
    CloseResponse,
    ErrorResponse,
)
from .websocket_events import WebSocketEvents


ONE_SECOND = 1
HALF_SECOND = 0.5
DEEPGRAM_INTERVAL = 5
PING_INTERVAL = 20


class AbstractSyncWebSocketClient(ABC):  # pylint: disable=too-many-instance-attributes
    """
    Abstract class for using WebSockets.

    This class provides methods to establish a WebSocket connection generically for
    use in all WebSocket clients.

    Args:
        config (DeepgramClientOptions): all the options for the client
        endpoint (str): the endpoint to connect to
        thread_cls (Type[threading.Thread]): optional thread class to use for creating threads,
            defaults to threading.Thread. Useful for custom thread management like ContextVar support.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str
    _websocket_url: str

    _socket: Optional[ClientConnection] = None
    _exit_event: threading.Event
    _lock_send: threading.Lock

    _listen_thread: Union[threading.Thread, None]
    _delegate: Optional[Speaker] = None

    _thread_cls: Type[threading.Thread]

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    _options: Optional[Dict] = None
    _headers: Optional[Dict] = None

    def __init__(
        self,
        config: DeepgramClientOptions,
        endpoint: str = "",
        thread_cls: Type[threading.Thread] = threading.Thread,
    ):
        if config is None:
            raise DeepgramError("Config is required")
        if endpoint == "":
            raise DeepgramError("endpoint is required")

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config
        self._endpoint = endpoint
        self._lock_send = threading.Lock()

        self._listen_thread = None

        self._thread_cls = thread_cls

        # exit
        self._exit_event = threading.Event()

        # set websocket url
        self._websocket_url = convert_to_websocket_url(self._config.url, self._endpoint)

    def delegate_listening(self, delegate: Speaker) -> None:
        """
        Delegate the listening thread to the main thread.
        """
        self._delegate = delegate

    # pylint: disable=too-many-statements,too-many-branches
    def start(
        self,
        options: Optional[Any] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for live transcription.
        """
        self._logger.debug("AbstractSyncWebSocketClient.start ENTER")
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("kwargs: %s", kwargs)

        self._addons = addons
        self._headers = headers

        # set kwargs
        if kwargs is not None:
            self._kwargs = kwargs
        else:
            self._kwargs = {}

        if not isinstance(options, dict):
            self._logger.error("options is not a dict")
            self._logger.debug("AbstractSyncWebSocketClient.start LEAVE")
            return False

        # set options
        if options is not None:
            self._options = options
        else:
            self._options = {}

        combined_options = self._options.copy()
        if self._addons is not None:
            self._logger.info("merging addons to options")
            combined_options.update(self._addons)
            self._logger.info("new options: %s", combined_options)
        self._logger.debug("combined_options: %s", combined_options)

        combined_headers = self._config.headers.copy()
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

            # delegate the listening thread to external object
            if self._delegate is not None:
                self._logger.notice("_delegate is enabled. this is usually the speaker")
                self._delegate.set_pull_callback(self._socket.recv)
                self._delegate.set_push_callback(self._process_message)
            else:
                self._logger.notice("create _listening thread")
                self._listen_thread = self._thread_cls(target=self._listening)
                self._listen_thread.start()

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # push open event
            self._emit(
                WebSocketEvents(WebSocketEvents.Open),
                OpenResponse(type=WebSocketEvents.Open),
            )

            self._logger.notice("start succeeded")
            self._logger.debug("AbstractSyncWebSocketClient.start LEAVE")
            return True
        except websockets.ConnectionClosed as e:
            self._logger.error(
                "ConnectionClosed in AbstractSyncWebSocketClient.start: %s", e
            )
            self._logger.debug("AbstractSyncWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect", False):
                raise e
            return False
        except websockets.exceptions.WebSocketException as e:
            self._logger.error(
                "WebSocketException in AbstractSyncWebSocketClient.start: %s", e
            )
            self._logger.debug("AbstractSyncWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect", False):
                raise e
            return False
        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in AbstractSyncWebSocketClient.start: %s", e
            )
            self._logger.debug("AbstractSyncWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect", False):
                raise e
            return False

    def is_connected(self) -> bool:
        """
        Returns the connection status of the WebSocket.
        """
        return self._socket is not None

    # pylint: enable=too-many-statements,too-many-branches

    @abstractmethod
    def on(self, event: WebSocketEvents, handler: Callable) -> None:
        """
        Registers an event handler for the WebSocket connection.
        """
        raise NotImplementedError("no on method")

    @abstractmethod
    def _emit(self, event: WebSocketEvents, *args, **kwargs) -> None:
        """
        Emits an event to the WebSocket connection.
        """
        raise NotImplementedError("no _emit method")

    # pylint: disable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches
    def _listening(
        self,
    ) -> None:
        """
        Listens for messages from the WebSocket connection.
        """
        self._logger.debug("AbstractSyncWebSocketClient._listening ENTER")

        while True:
            try:
                if self._exit_event.is_set():
                    self._logger.notice("_listening exiting gracefully")
                    self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")
                    return

                if self._socket is None:
                    self._logger.warning("socket is empty")
                    self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")
                    return

                message = self._socket.recv()

                if message is None:
                    self._logger.info("message is None")
                    continue

                self._logger.spam("data type: %s", type(message))

                if isinstance(message, bytes):
                    self._logger.debug("Binary data received")
                    self._process_binary(message)
                else:
                    self._logger.debug("Text data received")
                    self._process_text(message)

                self._logger.notice("_listening Succeeded")
                self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")

            except websockets.exceptions.ConnectionClosedOK as e:
                # signal exit and close
                self._signal_exit()

                self._logger.notice(f"_listening({e.code}) exiting gracefully")
                self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")
                return

            except websockets.exceptions.ConnectionClosed as e:
                if e.code in [1000, 1001]:
                    # signal exit and close
                    self._signal_exit()

                    self._logger.notice(f"_listening({e.code}) exiting gracefully")
                    self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")
                    return

                # we need to explicitly call self._signal_exit() here because we are hanging on a recv()
                # note: this is different than the speak websocket client
                self._logger.error(
                    "ConnectionClosed in AbstractSyncWebSocketClient._listening with code %s: %s",
                    e.code,
                    e.reason,
                )
                cc_error: ErrorResponse = ErrorResponse(
                    "ConnectionClosed in AbstractSyncWebSocketClient._listening",
                    f"{e}",
                    "ConnectionClosed",
                )
                self._emit(
                    WebSocketEvents(WebSocketEvents.Error),
                    cc_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                self._signal_exit()

                self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")

                if self._config.options.get("termination_exception_connect") is True:
                    raise
                return

            except websockets.exceptions.WebSocketException as e:
                self._logger.error(
                    "WebSocketException in AbstractSyncWebSocketClient._listening with: %s",
                    e,
                )
                ws_error: ErrorResponse = ErrorResponse(
                    "WebSocketException in AbstractSyncWebSocketClient._listening",
                    f"{e}",
                    "WebSocketException",
                )
                self._emit(
                    WebSocketEvents(WebSocketEvents.Error),
                    ws_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                self._signal_exit()

                self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")

                if self._config.options.get("termination_exception_connect") is True:
                    raise
                return

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in AbstractSyncWebSocketClient._listening: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in AbstractSyncWebSocketClient._listening",
                    f"{e}",
                    "Exception",
                )
                self._emit(
                    WebSocketEvents(WebSocketEvents.Error),
                    e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                self._signal_exit()

                self._logger.debug("AbstractSyncWebSocketClient._listening LEAVE")

                if self._config.options.get("termination_exception_connect") is True:
                    raise
                return

    # pylint: enable=too-many-return-statements,too-many-statements,too-many-locals,too-many-branches

    def _process_message(self, message: Union[str, bytes]) -> None:
        if isinstance(message, bytes):
            self._process_binary(message)
        else:
            self._process_text(message)

    @abstractmethod
    def _process_text(self, message: str) -> None:
        raise NotImplementedError("no _process_text method")

    @abstractmethod
    def _process_binary(self, message: bytes) -> None:
        raise NotImplementedError("no _process_binary method")

    @abstractmethod
    def _close_message(self) -> bool:
        raise NotImplementedError("no _close_message method")

    # pylint: disable=too-many-return-statements,too-many-branches
    def send(self, data: Union[str, bytes]) -> bool:
        """
        Sends data over the WebSocket connection.
        """
        self._logger.spam("AbstractSyncWebSocketClient.send ENTER")

        if self._exit_event.is_set():
            self._logger.notice("send exiting gracefully")
            self._logger.debug("AbstractSyncWebSocketClient.send LEAVE")
            return False

        if not self.is_connected():
            self._logger.notice("is_connected is False")
            self._logger.debug("AbstractSyncWebSocketClient.send LEAVE")
            return False

        if self._socket is not None:
            with self._lock_send:
                try:
                    self._socket.send(data)
                except websockets.exceptions.ConnectionClosedOK as e:
                    self._logger.notice(f"send() exiting gracefully: {e.code}")
                    self._logger.debug("AbstractSyncWebSocketClient.send LEAVE")
                    if self._config.options.get("termination_exception_send") is True:
                        raise
                    return True
                except websockets.exceptions.ConnectionClosed as e:
                    if e.code in [1000, 1001]:
                        self._logger.notice(f"send({e.code}) exiting gracefully")
                        self._logger.debug("AbstractSyncWebSocketClient.send LEAVE")
                        if (
                            self._config.options.get("termination_exception_send")
                            == "true"
                        ):
                            raise
                        return True
                    self._logger.error("send() failed - ConnectionClosed: %s", str(e))
                    self._logger.spam("AbstractSyncWebSocketClient.send LEAVE")
                    if self._config.options.get("termination_exception_send") is True:
                        raise
                    return False
                except websockets.exceptions.WebSocketException as e:
                    self._logger.error("send() failed - WebSocketException: %s", str(e))
                    self._logger.spam("AbstractSyncWebSocketClient.send LEAVE")
                    if self._config.options.get("termination_exception_send") is True:
                        raise
                    return False
                except Exception as e:  # pylint: disable=broad-except
                    self._logger.error("send() failed - Exception: %s", str(e))
                    self._logger.spam("AbstractSyncWebSocketClient.send LEAVE")
                    if self._config.options.get("termination_exception_send") is True:
                        raise
                    return False

            self._logger.spam("send() succeeded")
            self._logger.spam("AbstractSyncWebSocketClient.send LEAVE")
            return True

        self._logger.spam("send() failed. socket is None")
        self._logger.spam("AbstractSyncWebSocketClient.send LEAVE")
        return False

    # pylint: enable=too-many-return-statements,too-many-branches

    def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.spam("AbstractSyncWebSocketClient.finish ENTER")

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("before running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        # signal exit
        self._signal_exit()

        # stop the threads
        self._logger.verbose("cancelling tasks...")
        if self._listen_thread is not None:
            self._listen_thread.join()
            self._listen_thread = None
        self._logger.notice("listening thread joined")

        # debug the threads
        for thread in threading.enumerate():
            if thread is not None and thread.name is not None:
                self._logger.debug("before running thread: %s", thread.name)
            else:
                self._logger.debug("after running thread: unknown_thread_name")
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.notice("finish succeeded")
        self._logger.spam("AbstractSyncWebSocketClient.finish LEAVE")
        return True

    # signals the WebSocket connection to exit
    def _signal_exit(self) -> None:
        # closes the WebSocket connection gracefully
        self._logger.notice("closing socket...")
        if self._socket is not None:
            self._logger.notice("sending Close...")
            try:
                # if the socket connection is closed, the following line might throw an error
                self._close_message()
            except websockets.exceptions.ConnectionClosedOK as e:
                self._logger.notice("_signal_exit  - ConnectionClosedOK: %s", e.code)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.error("_signal_exit  - ConnectionClosed: %s", e.code)
            except websockets.exceptions.WebSocketException as e:
                self._logger.error("_signal_exit - WebSocketException: %s", str(e))
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_signal_exit - Exception: %s", str(e))

            # push close event
            try:
                self._emit(
                    WebSocketEvents(WebSocketEvents.Close),
                    CloseResponse(type=WebSocketEvents.Close),
                    **dict(cast(Dict[Any, Any], self._kwargs)),
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

        self._socket = None
