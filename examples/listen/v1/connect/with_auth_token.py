import threading
import time

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import ListenV1SocketClientResponse

try:
    # Using access token instead of API key
    authClient = DeepgramClient()

    print("Request sent")
    authResponse = authClient.auth.v1.tokens.grant()
    print("Response received")

    client = DeepgramClient(access_token=authResponse.access_token)

    with client.listen.v1.connect(model="nova-3") as connection:
        def on_message(message: ListenV1SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")
        
        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # EXAMPLE ONLY: Start listening in a background thread for demo purposes
        # In production, you would typically call connection.start_listening() directly
        # which blocks until the connection closes, or integrate into your async event loop
        threading.Thread(target=connection.start_listening, daemon=True).start()
        time.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
except Exception as e:
    print(f"Caught: {e}")
