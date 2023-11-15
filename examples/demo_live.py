from dotenv import load_dotenv
import asyncio
import aiohttp
import os

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()

base_url = "api.beta.deepgram.com" # will change to https://api.beta.deepgram.com
beta_url = "https://api.beta.deepgram.com" # will stay as to https://api.beta.deepgram.com
testing_url = "http://localhost:8080" # will stay as http://api.deepgram.com

config_headers = {
    "header_key": "header value",
}
    
config_options = {
    "global_options" : {
        "url": beta_url, 
        "headers": config_headers
        }
    }

options: LiveOptions = {
      'model': 'nova',
      'interim_results': False,
      'language': 'en-US'
    }

# URL for the realtime streaming audio you would like to transcribe
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'

deepgram_api_key = os.getenv('DG_API_KEY')


async def main():
  deepgram: DeepgramClient = DeepgramClient(deepgram_api_key)

  # Create a websocket connection to Deepgram
  try:
    dg_connection = await deepgram.listen.live(options)
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

  # Listen for transcripts received from Deepgram and write them to the console
  dg_connection.on(LiveTranscriptionEvents.Transcript, print)

  # Listen for metadata received from Deepgram and write to the console
  dg_connection.on(LiveTranscriptionEvents.Metadata, print)

  # Listen for the connection to close
  dg_connection.on(LiveTranscriptionEvents.Close, lambda c: print(f'Connection closed with code {c}.'))


  # Send streaming audio from the URL to Deepgram
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
      while True:
        data = await audio.content.readany()
        # send audio data through the socket
        await dg_connection.send(data)
        # If no data is being sent from the live stream, then break out of the loop.
        if not data:
            break

  # Indicate that we've finished sending data by sending the {"type": "CloseStream"}
  await dg_connection.finish()

asyncio.run(main())