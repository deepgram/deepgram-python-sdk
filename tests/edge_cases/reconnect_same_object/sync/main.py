import time
import logging
from deepgram.utils import verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions, Microphone


def main():
    config: DeepgramClientOptions = DeepgramClientOptions(verbose=verboselogs.DEBUG)
    # config: DeepgramClientOptions = DeepgramClientOptions()
    deepgram: DeepgramClient = DeepgramClient("", config)
    options: LiveOptions = LiveOptions(
        model="nova-2",
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )

    dg_connection = deepgram.listen.live.v("1")

    for x in range(0, 10):
        if x > 0:
            # wait for the connection to close
            time.sleep(5)

        if x == 0:
            print(f"Starting connection #{x}...")
        else:
            print(f"Restarting connection #{x}...")

        if dg_connection.start(options) is False:
            print("Failed to connect to Deepgram")
            continue

        microphone = Microphone(dg_connection.send)
        microphone.start()

        time.sleep(15)

        print("Calling stop...")
        microphone.finish()
        dg_connection.finish()

    print("Finished")


if __name__ == "__main__":
    main()
