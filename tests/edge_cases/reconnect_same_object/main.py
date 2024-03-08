import time
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


def main():
    # config: DeepgramClientOptions = DeepgramClientOptions(verbose=logging.DEBUG)
    config: DeepgramClientOptions = DeepgramClientOptions()
    deepgram: DeepgramClient = DeepgramClient("", config)
    options: LiveOptions = LiveOptions()

    dg_connection = deepgram.listen.live.v("1")

    for x in range(0, 10):
        if x > 0:
            # wait for the connection to close
            time.sleep(5)

        if x == 0:
            print(f"Starting connection #{x}...")
        else:
            print(f"Restarting connection #{x}...")

        dg_connection.start(options)
        time.sleep(15)
        print("Calling stop...")
        dg_connection.finish()

    print("Finished")


if __name__ == "__main__":
    main()
