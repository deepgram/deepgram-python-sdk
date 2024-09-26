# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import inspect
import asyncio
import threading
from typing import Optional, Callable, Union, TYPE_CHECKING
import logging

from ...utils import verboselogs
from .constants import LOGGING, CHANNELS, RATE, CHUNK

if TYPE_CHECKING:
    import pyaudio


class Microphone:  # pylint: disable=too-many-instance-attributes
    """
    This implements a microphone for local audio input. This uses PyAudio under the hood.
    """

    _logger: verboselogs.VerboseLogger

    _audio: "pyaudio.PyAudio"
    _stream: "pyaudio.Stream"

    _chunk: int
    _rate: int
    _format: int
    _channels: int
    _input_device_index: Optional[int]
    _is_muted: bool

    _asyncio_loop: asyncio.AbstractEventLoop
    _asyncio_thread: Optional[threading.Thread] = None
    _exit: threading.Event

    _push_callback_org: Optional[Callable] = None
    _push_callback: Optional[Callable] = None

    def __init__(
        self,
        push_callback: Optional[Callable] = None,
        verbose: int = LOGGING,
        rate: int = RATE,
        chunk: int = CHUNK,
        channels: int = CHANNELS,
        input_device_index: Optional[int] = None,
    ):  # pylint: disable=too-many-positional-arguments
        # dynamic import of pyaudio as not to force the requirements on the SDK (and users)
        import pyaudio  # pylint: disable=import-outside-toplevel

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(verbose)

        self._exit = threading.Event()

        self._audio = pyaudio.PyAudio()
        self._chunk = chunk
        self._rate = rate
        self._format = pyaudio.paInt16
        self._channels = channels
        self._is_muted = False

        self._input_device_index = input_device_index
        self._push_callback_org = push_callback

    def _start_asyncio_loop(self) -> None:
        self._asyncio_loop = asyncio.new_event_loop()
        self._asyncio_loop.run_forever()

    def is_active(self) -> bool:
        """
        is_active - returns the state of the stream

        Args:
            None

        Returns:
            True if the stream is active, False otherwise
        """
        self._logger.debug("Microphone.is_active ENTER")

        if self._stream is None:
            self._logger.error("stream is None")
            self._logger.debug("Microphone.is_active LEAVE")
            return False

        val = self._stream.is_active()
        self._logger.info("is_active: %s", val)
        self._logger.info("is_exiting: %s", self._exit.is_set())
        self._logger.debug("Microphone.is_active LEAVE")
        return val

    def set_callback(self, push_callback: Callable) -> None:
        """
        set_callback - sets the callback function to be called when data is received.

        Args:
            push_callback (Callable): The callback function to be called when data is received.
                                      This should be the websocket send function.

        Returns:
            None
        """
        self._push_callback_org = push_callback

    def start(self) -> bool:
        """
        starts - starts the microphone stream

        Returns:
            bool: True if the stream was started, False otherwise
        """
        self._logger.debug("Microphone.start ENTER")

        self._logger.info("format: %s", self._format)
        self._logger.info("channels: %d", self._channels)
        self._logger.info("rate: %d", self._rate)
        self._logger.info("chunk: %d", self._chunk)
        # self._logger.info("input_device_id: %d", self._input_device_index)

        if self._push_callback_org is None:
            self._logger.error("start failed. No callback set.")
            self._logger.debug("Microphone.start LEAVE")
            return False

        if inspect.iscoroutinefunction(self._push_callback_org):
            self._logger.verbose("async/await callback - wrapping")
            # Run our own asyncio loop.
            self._asyncio_thread = threading.Thread(target=self._start_asyncio_loop)
            self._asyncio_thread.start()

            self._push_callback = lambda data: (
                asyncio.run_coroutine_threadsafe(
                    self._push_callback_org(data), self._asyncio_loop
                ).result()
                if self._push_callback_org
                else None
            )
        else:
            self._logger.verbose("regular threaded callback")
            self._asyncio_thread = None
            self._push_callback = self._push_callback_org

        self._stream = self._audio.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            input_device_index=self._input_device_index,
            stream_callback=self._callback,
        )

        self._exit.clear()
        self._stream.start_stream()

        self._logger.notice("start succeeded")
        self._logger.debug("Microphone.start LEAVE")
        return True

    def _callback(
        self, input_data, frame_count, time_info, status_flags
    ):  # pylint: disable=unused-argument
        """
        The callback used to process data in callback mode.
        """
        # dynamic import of pyaudio as not to force the requirements on the SDK (and users)
        import pyaudio  # pylint: disable=import-outside-toplevel

        self._logger.debug("Microphone._callback ENTER")

        if self._exit.is_set():
            self._logger.info("exit is Set")
            self._logger.notice("_callback stopping...")
            self._logger.debug("Microphone._callback LEAVE")
            return None, pyaudio.paAbort

        if input_data is None:
            self._logger.warning("input_data is None")
            self._logger.debug("Microphone._callback LEAVE")
            return None, pyaudio.paContinue

        try:
            if self._is_muted:
                size = len(input_data)
                input_data = b"\x00" * size

            self._push_callback(input_data)
        except Exception as e:
            self._logger.error("Error while sending: %s", str(e))
            self._logger.debug("Microphone._callback LEAVE")
            raise

        self._logger.debug("Microphone._callback LEAVE")
        return input_data, pyaudio.paContinue

    def mute(self) -> bool:
        """
        mute - mutes the microphone stream

        Returns:
            bool: True if the stream was muted, False otherwise
        """
        self._logger.debug("Microphone.mute ENTER")

        if self._stream is None:
            self._logger.error("mute failed. Library not initialized.")
            self._logger.debug("Microphone.mute LEAVE")
            return False

        self._is_muted = True

        self._logger.notice("mute succeeded")
        self._logger.debug("Microphone.mute LEAVE")
        return True

    def unmute(self) -> bool:
        """
        unmute - unmutes the microphone stream

        Returns:
            bool: True if the stream was unmuted, False otherwise
        """
        self._logger.debug("Microphone.unmute ENTER")

        if self._stream is None:
            self._logger.error("unmute failed. Library not initialized.")
            self._logger.debug("Microphone.unmute LEAVE")
            return False

        self._is_muted = False

        self._logger.notice("unmute succeeded")
        self._logger.debug("Microphone.unmute LEAVE")
        return True

    def finish(self) -> bool:
        """
        finish - stops the microphone stream

        Returns:
            bool: True if the stream was stopped, False otherwise
        """
        self._logger.debug("Microphone.finish ENTER")

        self._logger.notice("signal exit")
        self._exit.set()

        # Stop the stream.
        if self._stream is not None:
            self._logger.notice("stopping stream...")
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None  # type: ignore
            self._logger.notice("stream stopped")

        # clean up the thread
        if (
            # inspect.iscoroutinefunction(self._push_callback_org)
            # and
            self._asyncio_thread
            is not None
        ):
            self._logger.notice("stopping asyncio loop...")
            self._asyncio_loop.call_soon_threadsafe(self._asyncio_loop.stop)
            self._asyncio_thread.join()
            self._asyncio_thread = None
            self._logger.notice("_asyncio_thread joined")

        self._logger.notice("finish succeeded")
        self._logger.debug("Microphone.finish LEAVE")

        return True
