from dotenv import load_dotenv
import asyncio
from websockets.exceptions import ConnectionClosedError
from deepgram.utils import verboselogs
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    SpeakWebSocketEvents,
    SpeakOptions,
)

load_dotenv()

TTS_TEXT = "Hello, this is a text to speech example using Deepgram."
AUDIO_FILE = "output.mp3"


async def main():
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        config: DeepgramClientOptions = DeepgramClientOptions(
            url="api.beta.deepgram.com", verbose=verboselogs.DEBUG
        )
        deepgram: DeepgramClient = DeepgramClient("", config)
        # otherwise, use default config
        # deepgram: DeepgramClient = DeepgramClient()

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.speak.asyncwebsocket.v("1")

        async def on_open(client, open_response, **kwargs):
            print(f"\n\nOpen: {open_response}\n\n")
            await send_tts_text(client)

        async def on_binary_data(client, data, **kwargs):
            print("Received binary data")
            await write_binary_to_mp3(data)

        async def on_metadata(client, metadata, **kwargs):
            print(f"\n\nMetadata: {metadata}\n\n")

        async def on_flush(client, flush, **kwargs):
            print(f"\n\nFlush: {flush}\n\n")

        async def on_close(client, close, **kwargs):
            print(f"\n\nClose: {close}\n\n")

        async def on_warning(client, warning, **kwargs):
            print(f"\n\nWarning: {warning}\n\n")

        async def on_error(client, error, **kwargs):
            print(f"\n\nError: {error}\n\n")

        async def on_unhandled(client, unhandled, **kwargs):
            print(f"\n\nUnhandled: {unhandled}\n\n")

        async def write_binary_to_mp3(data):
            loop = asyncio.get_running_loop()
            try:
                with open(AUDIO_FILE, "ab") as f:
                    await loop.run_in_executor(None, f.write, data)
            except Exception as e:
                print(f"Failed to write data to file: {e}")
            finally:
                print("File operation completed.")

        dg_connection.on(SpeakWebSocketEvents.Open, on_open)
        dg_connection.on(SpeakWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(SpeakWebSocketEvents.Metadata, on_metadata)
        dg_connection.on(SpeakWebSocketEvents.Flush, on_flush)
        dg_connection.on(SpeakWebSocketEvents.Close, on_close)
        dg_connection.on(SpeakWebSocketEvents.Warning, on_warning)
        dg_connection.on(SpeakWebSocketEvents.Error, on_error)
        dg_connection.on(SpeakWebSocketEvents.Unhandled, on_unhandled)

        async def send_tts_text(client):
            await client.send(TTS_TEXT)

        # Connect to the WebSocket
        options = SpeakOptions(model="aura-asteria-en")

        if not await dg_connection.start(options):
            print("Failed to start connection")
            return

        # Wait for user input to finish
        await asyncio.get_event_loop().run_in_executor(
            None, input, "\n\nPress Enter to stop...\n\n"
        )
        await dg_connection.finish()

        print("Finished")

    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except asyncio.CancelledError as e:
        print(f"Asyncio task was cancelled: {e}")
    except OSError as e:
        print(f"File operation failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
