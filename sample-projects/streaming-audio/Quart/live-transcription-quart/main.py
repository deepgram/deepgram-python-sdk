from quart import Quart, render_template, websocket
from deepgram import Deepgram
from dotenv import load_dotenv
from typing import Dict, Callable

import os

load_dotenv()

app = Quart(__name__)

dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))

async def process_audio(fast_socket):
    async def get_transcript(data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']
        
            if transcript:
                await fast_socket.send(transcript)

    deepgram_socket = await connect_to_deepgram(get_transcript)

    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None]) -> str:
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'interim_results': False})
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')

@app.route('/')
async def index():
    return await render_template('index.html')

@app.websocket('/listen')
async def websocket_endpoint():
 
   try:
       deepgram_socket = await process_audio(websocket)

       while True:
           data = await websocket.receive()
           deepgram_socket.send(data)
   except Exception as e:
       raise Exception(f'Could not process audio: {e}')
   finally:
       websocket.close(1000)



if __name__ == "__main__":
    app.run('localhost', port=3000, debug=True)