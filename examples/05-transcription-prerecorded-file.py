"""
Example: Transcribe Prerecorded Audio from File

This example shows how to transcribe audio from a local file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    # Path to audio file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(script_dir, "fixtures", "audio.wav")
    
    print(f"Reading audio file: {audio_path}")
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    print("Sending transcription request...")
    response = client.listen.v1.media.transcribe_file(
        request=audio_data,
        model="nova-3",
    )
    
    # For large files, you can stream the file instead of loading it all into memory:
    # def read_file_in_chunks(file_path, chunk_size=8192):
    #     with open(file_path, "rb") as f:
    #         while True:
    #             chunk = f.read(chunk_size)
    #             if not chunk:
    #                 break
    #             yield chunk
    # response = client.listen.v1.media.transcribe_file(
    #     request=read_file_in_chunks(audio_path),
    #     model="nova-3",
    # )
    
    print("Transcription received:")
    if response.results and response.results.channels:
        transcript = response.results.channels[0].alternatives[0].transcript
        print(transcript)
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.listen.v1.media.transcribe_file(...)
    
except Exception as e:
    print(f"Error: {e}")

