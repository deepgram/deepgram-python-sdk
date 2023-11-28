# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import inspect
import asyncio
import threading
import pyaudio
from array import array
from sys import byteorder

from .errors import DeepgramMicrophoneError

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000


class Microphone:
    """
    TODO
    """

    def __init__(
        self, push_callback, format=FORMAT, rate=RATE, chunk=CHUNK, channels=CHANNELS
    ):
        self.audio = pyaudio.PyAudio()
        self.chunk = chunk
        self.rate = rate
        self.format = format
        self.channels = channels
        self.push_callback = push_callback
        self.stream = None

    def is_active(self):
        if self.stream is None:
            return False
        return self.stream.is_active()

    def start(self):
        if self.stream is not None:
            raise DeepgramMicrophoneError("Microphone already started")

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=CHUNK,
        )

        self.exit = False
        self.lock = threading.Lock()

        self.stream.start_stream()
        self.thread = threading.Thread(target=self.processing)
        self.thread.start()

    def processing(self):
        try:
            while True:
                data = self.stream.read(self.chunk)

                self.lock.acquire()
                localExit = self.exit
                self.lock.release()
                if localExit:
                    break
                if data is None:
                    continue

                if inspect.iscoroutinefunction(self.push_callback):
                    asyncio.run(self.push_callback(data))
                else:
                    self.push_callback(data)

        except Exception as e:
            print(f"Error while sending: {str(e)}")
            raise

    def finish(self):
        self.lock.acquire()
        self.exit = True
        self.lock.release()

        self.thread.join()
        self.thread = None

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
