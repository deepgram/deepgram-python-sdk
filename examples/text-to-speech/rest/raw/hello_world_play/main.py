# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import sounddevice as sd
import numpy as np
import queue
import threading

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

SPEAK_TEXT = {"text": "Hello world!"}


# Define a queue to manage audio data
audio_queue = queue.Queue(maxsize=20)  # Adjust size as needed

element_size = np.dtype(np.int16).itemsize  # Element size for np.int16 (16-bit integer)
CHUNK_SIZE = 32768  # Desired size of each audio chunk in bytes


def fetch_audio(response):
    try:
        buffer = bytearray()  # Buffer to accumulate data
        for data in response.iter_bytes():
            buffer.extend(data)  # Add incoming data to buffer
            while len(buffer) >= CHUNK_SIZE:
                # Extract a chunk of the desired size
                chunk = buffer[:CHUNK_SIZE]
                buffer = buffer[CHUNK_SIZE:]  # Remove the chunk from the buffer

                # Ensure the chunk is aligned to the element size
                buffer_size = len(chunk) - (len(chunk) % element_size)

                if buffer_size > 0:
                    audio_data = np.frombuffer(chunk[:buffer_size], dtype=np.int16)
                    audio_queue.put(audio_data)
                    print(
                        f"Queued audio data of size: {audio_data.size * element_size} bytes"
                    )

        # Process any remaining data in the buffer
        if buffer:
            audio_data = np.frombuffer(buffer, dtype=np.int16)
            audio_queue.put(audio_data)
            print(
                f"Queued remaining audio data of size: {audio_data.size * element_size} bytes"
            )

        # Signal the end of the stream
        audio_queue.put(None)
        print("End of audio stream.")
    except Exception as e:
        print(f"Fetch audio exception: {e}")


def main():
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram: DeepgramClient = DeepgramClient()

        # STEP 2: Call the save method on the speak property
        options = SpeakOptions(
            model="aura-2-thalia-en",
            encoding="linear16",
            container="none",
            sample_rate=48000,
        )

        response = deepgram.speak.rest.v("1").stream_raw(SPEAK_TEXT, options)

        # Display response headers
        print("Response headers:")
        for header in response.headers:
            print(f"{header}: {response.headers[header]}")

        # Create and start a separate thread for fetching audio
        fetch_thread = threading.Thread(target=fetch_audio, args=(response,))
        fetch_thread.start()

        # Play audio data from the queue
        while True:
            audio_data = audio_queue.get()
            if audio_data is None:
                break  # End of stream

            # Play audio data using sounddevice
            sd.play(audio_data, samplerate=48000)
            sd.wait()  # Wait for the audio to finish playing

        fetch_thread.join()

        print("Audio playback finished.")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
