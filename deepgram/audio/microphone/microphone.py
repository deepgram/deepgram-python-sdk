# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import inspect
import asyncio
import threading
import pyaudio
from array import array
import logging, verboselogs

from .errors import DeepgramMicrophoneError

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8194


class Microphone:
    """
    TODO
    """

    def __init__(
        self,
        push_callback,
        verbose=logging.WARNING,
        format=FORMAT,
        rate=RATE,
        chunk=CHUNK,
        channels=CHANNELS,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(verbose)

        self.audio = pyaudio.PyAudio()
        self.chunk = chunk
        self.rate = rate
        self.format = format
        self.channels = channels
        self.push_callback = push_callback
        self.stream = None

    def is_active(self):
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
        self.thread = threading.Thread(target=self.processing)
        self.thread.start()

        self.logger.notice("start succeeded")
        self.logger.debug("Microphone.start LEAVE")

    def processing(self):
        self.logger.debug("Microphone.processing ENTER")

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

            self.logger.notice("processing exiting...")
            self.logger.debug("Microphone.processing LEAVE")

        except Exception as e:
            self.logger.error("Error while sending: %s", str(e))
            self.logger.debug("Microphone.processing LEAVE")
            raise

    def finish(self):
        self.logger.debug("Microphone.finish ENTER")

        self.lock.acquire()
        self.logger.notice("signal exit")
        self.exit = True
        self.lock.release()

        if self.thread is not None:
            self.thread.join()
            self.thread = None
        self.logger.notice("processing/send thread joined")

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.logger.notice("stream/recv thread joined")

        self.logger.notice("finish succeeded")
        self.logger.debug("Microphone.finish LEAVE")
