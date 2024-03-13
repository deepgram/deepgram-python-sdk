# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import inspect
import asyncio
import threading
from typing import Optional
import logging, verboselogs

from .errors import DeepgramMicrophoneError
from .constants import LOGGING, CHANNELS, RATE, CHUNK


class Microphone:
    """
    This implements a microphone for local audio input. This uses PyAudio under the hood.
    """

    def __init__(
        self,
        push_callback=None,
        verbose: int = LOGGING,
        rate: int = RATE,
        chunk: int = CHUNK,
        channels: int = CHANNELS,
        input_device_index: Optional[int] = None,
    ):
        # dynamic import of pyaudio as not to force the requirements on the SDK (and users)
        import pyaudio

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(verbose)
        self.exit = threading.Event()

        self.audio = pyaudio.PyAudio()
        self.chunk = chunk
        self.rate = rate
        self.format = pyaudio.paInt16
        self.channels = channels
        self.input_device_index = input_device_index
        self.push_callback_org = push_callback

        self.asyncio_loop = None
        self.asyncio_thread = None
        self.stream = None
        self.is_muted = False

    def _start_asyncio_loop(self) -> None:
        self.asyncio_loop = asyncio.new_event_loop()
        self.asyncio_loop.run_forever()

    def is_active(self) -> bool:
        """
        returns True if the stream is active, False otherwise
        """
        self.logger.debug("Microphone.is_active ENTER")
        if self.stream is None:
            self.logger.error("stream is None")
            self.logger.debug("Microphone.is_active LEAVE")
            return False

        val = self.stream.is_active()
        self.logger.info("is_active: %s", val)
        self.logger.info("is_exiting: %s", self.exit.is_set())
        self.logger.debug("Microphone.is_active LEAVE")
        return val

    def set_callback(self, push_callback) -> None:
        """
        Set the callback function to be called when data is received.
        """
        self.push_callback_org = push_callback

    def start(self) -> bool:
        """
        starts the microphone stream
        """
        self.logger.debug("Microphone.start ENTER")

        if self.stream is not None:
            self.logger.error("start() failed. Library already initialized.")
            self.logger.debug("Microphone.start LEAVE")
            return False

        self.logger.info("format: %s", self.format)
        self.logger.info("channels: %d", self.channels)
        self.logger.info("rate: %d", self.rate)
        self.logger.info("chunk: %d", self.chunk)
        self.logger.info("input_device_id: %d", self.input_device_index)

        if inspect.iscoroutinefunction(self.push_callback_org):
            self.logger.verbose("async/await callback - wrapping")
            # Run our own asyncio loop.
            self.asyncio_thread = threading.Thread(target=self._start_asyncio_loop)
            self.asyncio_thread.start()

            self.push_callback = lambda data: asyncio.run_coroutine_threadsafe(
                self.push_callback_org(data), self.asyncio_loop
            ).result()
        else:
            self.logger.verbose("regular threaded callback")
            self.push_callback = self.push_callback_org

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.input_device_index,
            stream_callback=self._callback,
        )

        self.exit.clear()
        self.stream.start_stream()

        self.logger.notice("start() succeeded")
        self.logger.debug("Microphone.start LEAVE")
        return True

    def _callback(self, input_data, frame_count, time_info, status_flags):
        """
        The callback used to process data in callback mode.
        """
        import pyaudio

        self.logger.debug("Microphone._callback ENTER")

        if self.exit.is_set():
            self.logger.info("exit is Set")
            self.logger.notice("_callback stopping...")
            self.logger.debug("Microphone._callback LEAVE")
            return None, pyaudio.paAbort

        if input_data is None:
            self.logger.warning("input_data is None")
            self.logger.debug("Microphone._callback LEAVE")
            return None, pyaudio.paContinue

        try:
            if self.is_muted:
                size = len(input_data)
                input_data = b"\x00" * size

            self.push_callback(input_data)
        except Exception as e:
            self.logger.error("Error while sending: %s", str(e))
            self.logger.debug("Microphone._callback LEAVE")
            raise

        self.logger.debug("Microphone._callback LEAVE")
        return input_data, pyaudio.paContinue

    def mute(self) -> bool:
        """
        Mutes the microphone stream
        """
        self.logger.debug("Microphone.mute ENTER")

        if self.stream is None:
            self.logger.error("mute() failed. Library not initialized.")
            self.logger.debug("Microphone.mute LEAVE")
            return False

        self.is_muted = True

        self.logger.notice("mute() succeeded")
        self.logger.debug("Microphone.mute LEAVE")
        return True

    def unmute(self) -> bool:
        """
        Unmutes the microphone stream
        """
        self.logger.debug("Microphone.unmute ENTER")

        if self.stream is None:
            self.logger.error("unmute() failed. Library not initialized.")
            self.logger.debug("Microphone.unmute LEAVE")
            return False

        self.is_muted = False

        self.logger.notice("unmute() succeeded")
        self.logger.debug("Microphone.unmute LEAVE")
        return True

    def finish(self) -> bool:
        """
        Stops the microphone stream
        """
        self.logger.debug("Microphone.finish ENTER")

        self.logger.notice("signal exit")
        self.exit.set()

        # Stop the stream.
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None

        # clean up the thread
        if self.asyncio_thread is not None:
            self.asyncio_loop.call_soon_threadsafe(self.asyncio_loop.stop)
            self.asyncio_thread.join()
            self.asyncio_thread = None
        self.logger.notice("stream/recv thread joined")

        self.logger.notice("finish succeeded")
        self.logger.debug("Microphone.finish LEAVE")

        return True
