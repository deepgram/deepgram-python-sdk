from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
from deepgram import Deepgram
from typing import Dict

import os

load_dotenv()

class TranscriptConsumer(AsyncWebsocketConsumer):
   dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))

   async def get_transcript(self, data: Dict) -> None:
       if 'channel' in data:
           transcript = data['channel']['alternatives'][0]['transcript']
      
           if transcript:
               await self.send(transcript)


   async def connect_to_deepgram(self):
       try:
           self.socket = await self.dg_client.transcription.live({'punctuate': True, 'interim_results': False})
           self.socket.registerHandler(self.socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
           self.socket.registerHandler(self.socket.event.TRANSCRIPT_RECEIVED, self.get_transcript)

       except Exception as e:
           raise Exception(f'Could not open socket: {e}')

   async def connect(self):
       await self.connect_to_deepgram()
       await self.accept()
          

   async def disconnect(self, close_code):
       await self.channel_layer.group_discard(
           self.room_group_name,
           self.channel_name
       )

   async def receive(self, bytes_data):
       self.socket.send(bytes_data)
