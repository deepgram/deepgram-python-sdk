import json
import os
import time

from websockets.sync.client import connect

DEFAULT_URL = "wss://api.beta.deepgram.com/v1/speak?encoding=linear16&container=none&sample_rate=48000"
DEFAULT_TOKEN = os.environ.get("DEEPGRAM_API_KEY", None)


def main():
    _socket = connect(
        DEFAULT_URL, additional_headers={"Authorization": f"Token {DEFAULT_TOKEN}"}
    )

    _story = "Hello world."
    msg = json.dumps({"type": "TextInput", "text": _story})
    _socket.send(msg)
    msg = json.dumps({"type": "Flush"})
    _socket.send(msg)

    # first byte
    start_time = time.time()
    message = _socket.recv()
    end_time = time.time()
    time_to_first_byte = end_time - start_time
    print(
        f"Connection time to first byte: {time_to_first_byte * 1000} milliseconds:\n\n{message}"
    )

    # first audio byte
    message = _socket.recv()
    end_time = time.time()
    time_to_first_byte = end_time - start_time
    print(
        f"First input time to first audio byte: {time_to_first_byte * 1000} milliseconds:\n\n{message[:20]}..."
    )

    _socket.close()


if __name__ == "__main__":
    main()
