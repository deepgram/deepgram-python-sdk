import asyncio

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import SpeakV1SocketClientResponse

client = AsyncDeepgramClient()

async def main() -> None:
    try:
        async with client.speak.v1.connect(model="aura-2-asteria-en", encoding="linear16", sample_rate=24000) as connection:
            def on_message(message: SpeakV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    print("Received audio event")
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    print(f"Received {msg_type} event")
            
            connection.on(EventType.OPEN, lambda _: print("Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
            connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

            # EXAMPLE ONLY: Start listening task and cancel after brief demo
            # In production, you would typically await connection.start_listening() directly
            # which runs until the connection closes or is interrupted
            listen_task = asyncio.create_task(connection.start_listening())

            # Send text to be converted to speech
            from deepgram.extensions.types.sockets import SpeakV1ControlMessage
            print("Send Flush message")
            await connection.send_control(SpeakV1ControlMessage(type="Flush"))
            print("Send Close message")
            await connection.send_control(SpeakV1ControlMessage(type="Close"))

            await asyncio.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
            listen_task.cancel()
    except Exception as e:
        print(f"Caught: {e}")

asyncio.run(main())
