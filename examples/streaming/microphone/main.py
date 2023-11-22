# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv

from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions, Microphone

load_dotenv()

options: LiveOptions = {
    'punctuate': True,
    'language': 'en-US',
    'encoding':  'linear16',
    'channels':  1,
    'sample_rate': 16000,
}

deepgram_api_key = os.getenv('DG_API_KEY')

def on_message(result=None):
    if result is None:
        return
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    print(f"speaker: {sentence}")

def on_metadata(metadata=None):
    if metadata is None:
        return
    print("")
    print(metadata)
    print("")

def on_error(error=None):
    if error is None:
        return
    print("")
    print(error)
    print("")

def main():
    
    # config: DeepgramClientOptions = DeepgramClientOptions(options={'keepalive': 'true'})
    deepgram: DeepgramClient = DeepgramClient(deepgram_api_key)

    try:
        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.live(options)
        dg_connection.start()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
    
        # Open a microphone stream
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")
        
        # Wait for the connection to close
        microphone.finish()

        # Indicate that we've finished sending data by sending the {"type": "CloseStream"}
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f'Could not open socket: {e}')
        return

if __name__ == "__main__":
    main()