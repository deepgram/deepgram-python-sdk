import asyncio
import time
import logging
from deepgram.utils import verboselogs
from signal import SIGINT, SIGTERM

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions, Microphone


async def main():
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    for signal in (SIGTERM, SIGINT):
        loop.add_signal_handler(
            signal,
            lambda: asyncio.create_task(
                shutdown(signal, loop, dg_connection, microphone, stop_event)
            ),
        )

    config: DeepgramClientOptions = DeepgramClientOptions(
        options={"keepalive": "true"}, verbose=verboselogs.SPAM
    )
    # config: DeepgramClientOptions = DeepgramClientOptions()
    deepgram: DeepgramClient = DeepgramClient("", config)
    options: LiveOptions = LiveOptions(
        model="nova-2",
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )

    dg_connection = deepgram.listen.asynclive.v("1")

    for x in range(0, 10):
        if stop_event.is_set():
            break
        if x > 0:
            # wait for the connection to close
            time.sleep(5)

        if x == 0:
            print(f"Starting connection #{x}...")
        else:
            print(f"Restarting connection #{x}...")

        await dg_connection.start(options)

        microphone = Microphone(dg_connection.send)

        if microphone.start() is False:
            print("Failed to start microphone")
            continue

        # wait until cancelled
        cnt = 0
        try:
            while cnt < 15:
                await asyncio.sleep(1)
                cnt += 1
        except asyncio.CancelledError:
            # This block will be executed when the shutdown coroutine cancels all tasks
            pass
        finally:
            microphone.finish()
            await dg_connection.finish()

    print("Finished")


async def shutdown(signal, loop, dg_connection, microphone, stop_event):
    print(f"Received exit signal {signal.name}...")
    stop_event.set()
    microphone.finish()
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")


asyncio.run(main())
