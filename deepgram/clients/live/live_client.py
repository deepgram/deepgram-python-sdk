from .enums import LiveTranscriptionEvents
from .helpers import convert_to_websocket_url, append_query_params

from deepgram.errors import DeepgramApiError

import asyncio
import json
import websockets

class LiveClient:
  """
    Client for interacting with Deepgram's live transcription services over WebSockets.

    This class provides methods to establish a WebSocket connection for live transcription and handle real-time transcription events.

    Args:
        base_url (str): The base URL for WebSocket connection.
        api_key (str): The Deepgram API key used for authentication.
        headers (dict): Additional HTTP headers for WebSocket connection.

    Attributes:
        endpoint (str): The API endpoint for live transcription.
        _socket (websockets.WebSocketClientProtocol): The WebSocket connection object.
        _event_handlers (dict): Dictionary of event handlers for specific events.
        websocket_url (str): The WebSocket URL used for connection.

    Methods:
        __call__: Establishes a WebSocket connection for live transcription.
        on: Registers event handlers for specific events.
        send: Sends data over the WebSocket connection.
        finish: Closes the WebSocket connection gracefully.
    """
  def __init__(self, base_url, api_key, headers):
    self.base_url = base_url
    self.api_key = api_key
    self.headers = headers
    self.endpoint = "v1/listen"
    self._socket = None
    self._event_handlers = { event: [] for event in LiveTranscriptionEvents }
    self.websocket_url = convert_to_websocket_url(base_url, self.endpoint)
  
  async def __call__(self, options=None):
      url_with_params = append_query_params(self.websocket_url, options)
      try:
          self._socket = await _socket_connect(url_with_params, self.headers)
          asyncio.create_task(self._start())
          return self
      except websockets.ConnectionClosed as e:
          await self._emit(LiveTranscriptionEvents.Close, e.code)
  
  
  def on(self, event, handler): # registers event handlers for specific events
      if event in LiveTranscriptionEvents and callable(handler):
          self._event_handlers[event].append(handler)

  async def _emit(self, event, *args, **kwargs): # triggers the registered event handlers for a specific event
      for handler in self._event_handlers[event]:
          handler(*args, **kwargs)

  async def _start(self) -> None:
      async for message in self._socket:
        try:
            data = json.loads(message)
            response_type = data.get("type")
            if response_type == LiveTranscriptionEvents.Transcript.value:
                await self._emit(LiveTranscriptionEvents.Transcript, data)
            if "metadata" in data:
                await self._emit(LiveTranscriptionEvents.Metadata, data["metadata"])
        except json.JSONDecodeError as e:
            await self._emit(LiveTranscriptionEvents.Error, e.code)
  
  async def send(self, data):
      if self._socket:
          await self._socket.send(data)

  async def finish(self):
      if self._socket:
          await self._socket.send(json.dumps({"type": "CloseStream"}))
          # await self._socket.send("")  # Send a zero-byte message
          await self._socket.wait_closed()

async def _socket_connect(websocket_url, headers):
    destination = websocket_url
    updated_headers = headers

    async def attempt():
        try:
            return await websockets.connect(
                destination, extra_headers=updated_headers, ping_interval=5
            )
        except websockets.exceptions.InvalidHandshake as exc:
            raise DeepgramApiError(exc, http_library_error=exc) from exc

    # tries = 4
    # while tries > 0:
    #     try:
    #         return await attempt()
    #     except Exception as exc:
    #         tries -= 1
    #         continue
    return await attempt()