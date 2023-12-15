# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import inspect
import asyncio
import threading
from array import array
import logging, verboselogs

from .errors import DeepgramMicrophoneError
from .constants import LOGGING, CHANNELS, RATE, CHUNK

class Microphone:
    """
    This implements a microphone for local audio input. This uses PyAudio under the hood.
    """

    def __init__(
        self,
        push_callback,
        verbose=LOGGING,
        rate=RATE,
        chunk=CHUNK,
        channels=CHANNELS,
    ):
        # dynamic import of pyaudio as not to force the requirements on the SDK (and users)
        import pyaudio

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(verbose)

        self.audio = pyaudio.PyAudio()
        self.chunk = chunk
        self.rate = rate
        self.format = pyaudio.paInt16
        self.channels = channels
        self.push_callback = push_callback
        self.stream = None

    def is_active(self):
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
        self.logger.debug("Microphone.is_active LEAVE")
        return

    def start(self):
        """
        starts the microphone stream
        """
        self.logger.debug("Microphone.start ENTER")

        if self.stream is not None:
            self.logger.error("stream is None")
            self.logger.debug("Microphone.start LEAVE")
            raise DeepgramMicrophoneError("Microphone already started")

        self.logger.info("format: %s", self.format)
        self.logger.info("channels: %d", self.channels)
        self.logger.info("rate: %d", self.rate)
        self.logger.info("chunk: %d", self.chunk)

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        self.exit = False
        self.lock = threading.Lock()

        self.stream.start_stream()
        self.thread = threading.Thread(target=self._processing)
        self.thread.start()

        self.logger.notice("start succeeded")
        self.logger.debug("Microphone.start LEAVE")

    def _processing(self):
        """
        the main processing loop for the microphone
        """
        self.logger.debug("Microphone._processing ENTER")

        try:
            while True:
                data = self.stream.read(self.chunk)

                self.lock.acquire()
                localExit = self.exit
                self.lock.release()
                if localExit:
                    self.logger.info("exit is True")
                    break
                if data is None:
                    self.logger.info("data is None")
                    continue

                if inspect.iscoroutinefunction(self.push_callback):
                    self.logger.verbose("async/await callback")
                    asyncio.run(self.push_callback(data))
                else:
                    self.logger.verbose("regular threaded callback")
                    self.push_callback(data)

            self.logger.notice("_processing exiting...")
            self.logger.debug("Microphone._processing LEAVE")

        except Exception as e:
            self.logger.error("Error while sending: %s", str(e))
            self.logger.debug("Microphone._processing LEAVE")
            raise

    def finish(self):
        """
        Stops the microphone stream
        """
        self.logger.debug("Microphone.finish ENTER")

        self.lock.acquire()
        self.logger.notice("signal exit")
        self.exit = True
        self.lock.release()

        if self.thread is not None:
            self.thread.join()
            self.thread = None
        self.logger.notice("_processing/send thread joined")

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.logger.notice("stream/recv thread joined")

        self.logger.notice("finish succeeded")
        self.logger.debug("Microphone.finish LEAVE")
