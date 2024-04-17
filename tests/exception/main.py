import time
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions

config = DeepgramClientOptions(verbose=logging.DEBUG)
deepgram = DeepgramClient("", config)

deepgram_connection = deepgram.listen.live.v("1")

deepgram_connection.start(LiveOptions())

time.sleep(
    30
)  # Deepgram will close the connection after 10-15s of silence, followed with another 5 seconds for a ping

print("deadlock!")
try:
    deepgram_connection.finish()
finally:
    print("no deadlock...")