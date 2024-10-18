# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import inspect
import queue
import threading
from typing import Optional, Callable, Union, TYPE_CHECKING
import logging
from datetime import datetime

import websockets

from ...utils import verboselogs
from .constants import LOGGING, CHANNELS, RATE, CHUNK, TIMEOUT, PLAYBACK_DELTA

from ..microphone import Microphone

if TYPE_CHECKING:
    import pyaudio

HALF_SECOND = 0.5


class Speaker:  # pylint: disable=too-many-instance-attributes
    """
    This implements a speaker for local audio output. This uses PyAudio under the hood.
    """

    _logger: verboselogs.VerboseLogger

    _audio: Optional["pyaudio.PyAudio"] = None
    _stream: Optional["pyaudio.Stream"] = None

    _chunk: int
    _rate: int
    _channels: int
    _output_device_index: Optional[int] = None

    # last time we received audio
    _last_datagram: datetime = datetime.now()
    _last_play_delta_in_ms: int
    _lock_wait: threading.Lock

    _queue: queue.Queue
    _exit: threading.Event

    _thread: Optional[threading.Thread] = None
    # _asyncio_loop: asyncio.AbstractEventLoop
    # _asyncio_thread: threading.Thread
    _receiver_thread: Optional[threading.Thread] = None

    _loop: Optional[asyncio.AbstractEventLoop] = None

    _push_callback_org: Optional[Callable] = None
    _push_callback: Optional[Callable] = None
    _pull_callback_org: Optional[Callable] = None
    _pull_callback: Optional[Callable] = None

    _microphone: Optional[Microphone] = None

    def __init__(
        self,
        pull_callback: Optional[Callable] = None,
        push_callback: Optional[Callable] = None,
        verbose: int = LOGGING,
        rate: int = RATE,
        chunk: int = CHUNK,
        channels: int = CHANNELS,
        last_play_delta_in_ms: int = PLAYBACK_DELTA,
        output_device_index: Optional[int] = None,
        microphone: Optional[Microphone] = None,
    ):  # pylint: disable=too-many-positional-arguments
        # dynamic import of pyaudio as not to force the requirements on the SDK (and users)
        import pyaudio  # pylint: disable=import-outside-toplevel

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(verbose)

        self._exit = threading.Event()
        self._queue = queue.Queue()

        self._last_datagram = datetime.now()
        self._lock_wait = threading.Lock()

        self._microphone = microphone

        self._audio = pyaudio.PyAudio()
        self._chunk = chunk
        self._rate = rate
        self._format = pyaudio.paInt16
        self._channels = channels
        self._last_play_delta_in_ms = last_play_delta_in_ms
        self._output_device_index = output_device_index

        self._push_callback_org = push_callback
        self._pull_callback_org = pull_callback

    def set_push_callback(self, push_callback: Callable) -> None:
        """
        set_push_callback - sets the callback function to be called when data is sent.

        Args:
            push_callback (Callable): The callback function to be called when data is send.
                                      This should be the websocket handle message function.

        Returns:
            None
        """
        self._push_callback_org = push_callback

    def set_pull_callback(self, pull_callback: Callable) -> None:
        """
        set_pull_callback - sets the callback function to be called when data is received.

        Args:
            pull_callback (Callable): The callback function to be called when data is received.
                                      This should be the websocket recv function.

        Returns:
            None
        """
        self._pull_callback_org = pull_callback

    def start(self, active_loop: Optional[asyncio.AbstractEventLoop] = None) -> bool:
        """
        starts - starts the Speaker stream

        Args:
            socket (Union[SyncClientConnection, AsyncClientConnection]): The socket to receive audio data from.

        Returns:
            bool: True if the stream was started, False otherwise
        """
        self._logger.debug("Speaker.start ENTER")

        self._logger.info("format: %s", self._format)
        self._logger.info("channels: %d", self._channels)
        self._logger.info("rate: %d", self._rate)
        self._logger.info("chunk: %d", self._chunk)
        # self._logger.info("output_device_id: %d", self._output_device_index)

        # Automatically get the current running event loop
        if inspect.iscoroutinefunction(self._push_callback_org) and active_loop is None:
            self._logger.verbose("get default running asyncio loop")
            self._loop = asyncio.get_running_loop()

        self._exit.clear()
        self._queue = queue.Queue()

        if self._audio is not None:
            self._stream = self._audio.open(
                format=self._format,
                channels=self._channels,
                rate=self._rate,
                input=False,
                output=True,
                frames_per_buffer=self._chunk,
                output_device_index=self._output_device_index,
            )

        if self._stream is None:
            self._logger.error("start failed. No stream created.")
            self._logger.debug("Speaker.start LEAVE")
            return False

        self._push_callback = self._push_callback_org
        self._pull_callback = self._pull_callback_org

        # start the play thread
        self._thread = threading.Thread(
            target=self._play, args=(self._queue, self._stream, self._exit), daemon=True
        )
        self._thread.start()

        # Start the stream
        if self._stream is not None:
            self._stream.start_stream()

        # Start the receiver thread within the start function
        self._logger.verbose("Starting receiver thread...")
        self._receiver_thread = threading.Thread(target=self._start_receiver)
        self._receiver_thread.start()

        self._logger.notice("start succeeded")
        self._logger.debug("Speaker.start LEAVE")

        return True

    def wait_for_complete_with_mute(self, mic: Microphone):
        """
        This method will mute/unmute a Microphone and block until the speak is done playing sound.
        """
        self._logger.debug("Speaker.wait_for_complete ENTER")

        if self._microphone is not None:
            mic.mute()
        self.wait_for_complete()
        if self._microphone is not None:
            mic.unmute()

        self._logger.debug("Speaker.wait_for_complete LEAVE")

    def wait_for_complete(self):
        """
        This method will block until the speak is done playing sound.
        """
        self._logger.debug("Speaker.wait_for_complete ENTER")

        delta_in_ms = float(self._last_play_delta_in_ms)
        self._logger.debug("Last Play delta: %f", delta_in_ms)

        # set to now
        with self._lock_wait:
            self._last_datagram = datetime.now()

        while True:
            # sleep for a bit
            self._exit.wait(HALF_SECOND)

            # check if we should exit
            if self._exit.is_set():
                self._logger.debug("Exiting wait_for_complete _exit is set")
                break

            # check the time
            with self._lock_wait:
                delta = datetime.now() - self._last_datagram
                diff_in_ms = delta.total_seconds() * 1000
                if diff_in_ms < delta_in_ms:
                    self._logger.debug("LastPlay delta is less than threshold")
                    continue

            # if we get here, we are done playing audio
            self._logger.debug("LastPlay delta is greater than threshold. Exit wait!")
            break

        self._logger.debug("Speaker.wait_for_complete LEAVE")

    def _start_receiver(self):
        # Check if the socket is an asyncio WebSocket
        if inspect.iscoroutinefunction(self._pull_callback_org):
            self._logger.verbose("Starting asyncio receiver...")
            asyncio.run_coroutine_threadsafe(self._start_asyncio_receiver(), self._loop)
        else:
            self._logger.verbose("Starting threaded receiver...")
            self._start_threaded_receiver()

    async def _start_asyncio_receiver(self):
        try:
            while True:
                if self._exit.is_set():
                    self._logger.verbose("Exiting receiver thread...")
                    break

                message = await self._pull_callback()
                if message is None:
                    self._logger.verbose("No message received...")
                    continue

                if isinstance(message, str):
                    self._logger.verbose("Received control message...")
                    await self._push_callback(message)
                elif isinstance(message, bytes):
                    self._logger.verbose("Received audio data...")
                    self.add_audio_to_queue(message)
        except websockets.exceptions.ConnectionClosedOK as e:
            self._logger.debug("send() exiting gracefully: %d", e.code)
        except websockets.exceptions.ConnectionClosed as e:
            if e.code in [1000, 1001]:
                self._logger.debug("send() exiting gracefully: %d", e.code)
                return
            self._logger.error("_start_asyncio_receiver - ConnectionClosed: %s", str(e))
        except websockets.exceptions.WebSocketException as e:
            self._logger.error(
                "_start_asyncio_receiver- WebSocketException: %s", str(e)
            )
        except Exception as e:  # pylint: disable=broad-except
            self._logger.error("_start_asyncio_receiver exception: %s", str(e))

    def _start_threaded_receiver(self):
        try:
            while True:
                if self._exit.is_set():
                    self._logger.verbose("Exiting receiver thread...")
                    break

                message = self._pull_callback()
                if message is None:
                    self._logger.verbose("No message received...")
                    continue

                if isinstance(message, str):
                    self._logger.verbose("Received control message...")
                    self._push_callback(message)
                elif isinstance(message, bytes):
                    self._logger.verbose("Received audio data...")
                    self.add_audio_to_queue(message)
        except Exception as e:  # pylint: disable=broad-except
            self._logger.notice("_start_threaded_receiver exception: %s", str(e))

    def add_audio_to_queue(self, data: bytes) -> None:
        """
        add_audio_to_queue - adds audio data to the Speaker queue

        Args:
            data (bytes): The audio data to add to the queue
        """
        self._queue.put(data)

    def finish(self) -> bool:
        """
        finish - stops the Speaker stream

        Returns:
            bool: True if the stream was stopped, False otherwise
        """
        self._logger.debug("Speaker.finish ENTER")

        self._logger.notice("signal exit")
        self._exit.set()

        if self._stream is not None:
            self._logger.notice("stopping stream...")
            self._stream.stop_stream()
            self._stream.close()
            self._logger.notice("stream stopped")

        if self._thread is not None:
            self._logger.notice("joining _thread...")
            self._thread.join()
            self._logger.notice("thread stopped")

        if self._receiver_thread is not None:
            self._logger.notice("stopping _receiver_thread...")
            self._receiver_thread.join()
            self._logger.notice("_receiver_thread joined")

        with self._queue.mutex:
            self._queue.queue.clear()

        self._stream = None
        self._thread = None
        self._receiver_thread = None

        self._logger.notice("finish succeeded")
        self._logger.debug("Speaker.finish LEAVE")

        return True

    def _play(self, audio_out, stream, stop):
        """
        _play - plays audio data from the Speaker queue callback for portaudio
        """
        while not stop.is_set():
            try:
                if self._microphone is not None and self._microphone.is_muted():
                    with self._lock_wait:
                        delta = datetime.now() - self._last_datagram
                        diff_in_ms = delta.total_seconds() * 1000
                        if diff_in_ms > float(self._last_play_delta_in_ms):
                            self._logger.debug(
                                "LastPlay delta is greater than threshold. Unmute!"
                            )
                            self._microphone.unmute()
                data = audio_out.get(True, TIMEOUT)
                with self._lock_wait:
                    self._last_datagram = datetime.now()
                    if self._microphone is not None and not self._microphone.is_muted():
                        self._logger.debug("New speaker sound detected. Mute!")
                        self._microphone.mute()
                stream.write(data)
            except queue.Empty:
                pass
            except Exception as e:  # pylint: disable=broad-except
                self._logger.error("_play exception: %s", str(e))
