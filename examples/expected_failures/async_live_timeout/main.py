import asyncio
import time
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


async def main():
    config = DeepgramClientOptions(verbose=logging.DEBUG)
    deepgram = DeepgramClient("", config)

    deepgram_connection = deepgram.listen.asynclive.v("1")

    await deepgram_connection.start(LiveOptions())

    time.sleep(
        30
    )  # Deepgram will close the connection after 10-15s of silence, followed with another 5 seconds for a ping

    print("deadlock!")
    try:
        await deepgram_connection.finish()
    finally:
        print("no deadlock...")


asyncio.run(main())
