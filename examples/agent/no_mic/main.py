# Copyright 2025 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import requests
import wave
import io
import time
from datetime import datetime
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
)
from deepgram.clients.agent.v1.websocket.options import SettingsOptions

# Add debug prints for imports
print("Checking imports...")

def create_wav_header(sample_rate=24000, bits_per_sample=16, channels=1):
    """Create a WAV header with the specified parameters"""
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)

    header = bytearray(44)
    # RIFF header
    header[0:4] = b'RIFF'
    header[4:8] = b'\x00\x00\x00\x00'  # File size (to be updated later)
    header[8:12] = b'WAVE'
    # fmt chunk
    header[12:16] = b'fmt '
    header[16:20] = b'\x10\x00\x00\x00'  # Subchunk1Size (16 for PCM)
    header[20:22] = b'\x01\x00'  # AudioFormat (1 for PCM)
    header[22:24] = channels.to_bytes(2, 'little')  # NumChannels
    header[24:28] = sample_rate.to_bytes(4, 'little')  # SampleRate
    header[28:32] = byte_rate.to_bytes(4, 'little')  # ByteRate
    header[32:34] = block_align.to_bytes(2, 'little')  # BlockAlign
    header[34:36] = bits_per_sample.to_bytes(2, 'little')  # BitsPerSample
    # data chunk
    header[36:40] = b'data'
    header[40:44] = b'\x00\x00\x00\x00'  # Subchunk2Size (to be updated later)

    return header

def update_wav_header(file_path, data_size):
    """Update the WAV header with the correct file size"""
    with open(file_path, 'r+b') as f:
        # Update file size in RIFF header (file size - 8)
        f.seek(4)
        f.write((data_size + 36).to_bytes(4, 'little'))
        # Update data size in data chunk
        f.seek(40)
        f.write(data_size.to_bytes(4, 'little'))

def convert_audio_to_linear16(audio_data, input_sample_rate=24000, output_sample_rate=24000):
    """Convert audio data to linear16 format with the correct sample rate"""
    print(f"Converting audio data from {input_sample_rate}Hz to {output_sample_rate}Hz")
    print(f"Input audio data length: {len(audio_data)} bytes")

    # Create a temporary WAV file in memory
    with io.BytesIO() as wav_buffer:
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(input_sample_rate)
            wav_file.writeframes(audio_data)

        # Read the WAV file
        wav_buffer.seek(0)
        with wave.open(wav_buffer, 'rb') as wav_file:
            # Get the audio data
            audio_data = wav_file.readframes(wav_file.getnframes())
            print(f"Converted audio data length: {len(audio_data)} bytes")
            return audio_data

def main():
    try:
        print("Starting main function...")
        # URL of the audio file to process
        url = "https://dpgr.am/spacewalk.wav"
        chatlog_file = "chatlog.txt"

        # Initialize variables for audio handling
        last_audio_time = datetime.now()
        audio_file_count = 0

        # Initialize Deepgram client
        config: DeepgramClientOptions = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "speaker_playback": "true",
            },
        )
        print("Created DeepgramClientOptions...")

        deepgram: DeepgramClient = DeepgramClient("", config)
        print("Created DeepgramClient...")

        dg_connection = deepgram.agent.websocket.v("1")
        print("Created WebSocket connection...")

        # Open chatlog file for writing
        with open(chatlog_file, 'w') as chatlog:
            def on_open(self, open, **kwargs):
                print(f"\n\nConnection opened: {open}\n\n")
                chatlog.write(f"Connection opened: {open}\n")

            def on_audio_data(self, data, **kwargs):
                nonlocal last_audio_time, audio_file_count
                print("Received audio data, length:", len(data))

                try:
                    # If the last audio response is more than 7 seconds ago, create a new file
                    if (datetime.now() - last_audio_time).total_seconds() > 7:
                        audio_file_count += 1
                        output_file = f"output_{audio_file_count}.wav"

                        # Create new WAV file with header
                        with open(output_file, 'wb') as f:
                            f.write(create_wav_header())
                            f.write(data)
                    else:
                        # Append audio data to the current file
                        with open(f"output_{audio_file_count}.wav", 'ab') as f:
                            f.write(data)

                    last_audio_time = datetime.now()
                except IOError as e:
                    print(f"Error writing to file: {e}")
                except Exception as e:
                    print(f"Unexpected error handling audio data: {e}")

            def on_agent_audio_done(self, agent_audio_done, **kwargs):
                print(f"\n\n{agent_audio_done}\n\n")
                chatlog.write(f"Agent audio done: {agent_audio_done}\n")

                # Update the WAV header with the correct file size
                if audio_file_count > 0:
                    try:
                        output_file = f"output_{audio_file_count}.wav"
                        with open(output_file, 'rb') as f:
                            f.seek(0, 2)  # Seek to end of file
                            file_size = f.tell()
                        update_wav_header(output_file, file_size - 44)  # Subtract header size
                    except IOError as e:
                        print(f"Error updating WAV header: {e}")
                    except Exception as e:
                        print(f"Unexpected error updating WAV header: {e}")

            def on_welcome(self, welcome, **kwargs):
                print(f"\n\n{welcome}\n\n")
                chatlog.write(f"Welcome message: {welcome}\n")

            def on_settings_applied(self, settings_applied, **kwargs):
                print(f"\n\n{settings_applied}\n\n")
                chatlog.write(f"Settings applied: {settings_applied}\n")

            def on_conversation_text(self, conversation_text, **kwargs):
                print(f"\n\n{conversation_text}\n\n")
                chatlog.write(f"Conversation: {conversation_text}\n")

            def on_user_started_speaking(self, user_started_speaking, **kwargs):
                print(f"\n\n{user_started_speaking}\n\n")
                chatlog.write(f"User started speaking: {user_started_speaking}\n")

            def on_agent_thinking(self, agent_thinking, **kwargs):
                print(f"\n\n{agent_thinking}\n\n")
                chatlog.write(f"Agent thinking: {agent_thinking}\n")

            def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
                print(f"\n\n{agent_started_speaking}\n\n")
                chatlog.write(f"Agent started speaking: {agent_started_speaking}\n")

            def on_close(self, close, **kwargs):
                print(f"\n\n{close}\n\n")
                chatlog.write(f"Connection closed: {close}\n")

            def on_error(self, error, **kwargs):
                print(f"\n\nError occurred: {error}\n\n")
                chatlog.write(f"Error: {error}\n")

            def on_unhandled(self, unhandled, **kwargs):
                print(f"\n\n{unhandled}\n\n")
                chatlog.write(f"Unhandled event: {unhandled}\n")

            # Register event handlers
            dg_connection.on(AgentWebSocketEvents.Open, on_open)
            dg_connection.on(AgentWebSocketEvents.AudioData, on_audio_data)
            dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
            dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
            dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
            dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
            dg_connection.on(AgentWebSocketEvents.UserStartedSpeaking, on_user_started_speaking)
            dg_connection.on(AgentWebSocketEvents.AgentThinking, on_agent_thinking)
            dg_connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
            dg_connection.on(AgentWebSocketEvents.Close, on_close)
            dg_connection.on(AgentWebSocketEvents.Error, on_error)
            dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

            # Configure agent settings
            options: SettingsOptions = SettingsOptions()
            # Audio input configuration
            options.audio.input.encoding = "linear16"
            options.audio.input.sample_rate = 24000
            # Audio output configuration
            options.audio.output.encoding = "linear16"
            options.audio.output.sample_rate = 24000
            options.audio.output.container = "wav"
            # Agent configuration
            options.agent.language = "en"
            options.agent.listen.provider.type = "deepgram"
            options.agent.listen.model = "nova-3"
            options.agent.think.provider.type = "open_ai"
            options.agent.think.model = "gpt-4o-mini"
            options.agent.think.prompt = "You are a friendly AI assistant."
            options.agent.speak.provider.type = "deepgram"
            options.agent.speak.model = "aura-2-thalia-en"
            options.agent.greeting = "Hello! How can I help you today?"

            if dg_connection.start(options) is False:
                print("Failed to start connection")
                return

            # Download and send audio data
            print("Downloading and sending audio...")
            response = requests.get(url, stream=True)
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    dg_connection.send(chunk)

            # Wait for processing to complete
            print("Waiting for processing to complete...")
            time.sleep(5)  # Give some time for processing

            print("\n\nProcessing complete. Check output_*.wav and chatlog.txt for results.\n\n")

            # Close the connection
            dg_connection.finish()

            print("Finished")

    except ImportError as e:
        print(f"Import Error Details: {e}")
        print(f"Error occurred in module: {getattr(e, 'name', 'unknown')}")
        print(f"Path that failed: {getattr(e, 'path', 'unknown')}")
    except Exception as e:
        print(f"Unexpected error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Error occurred in: {__file__}")

if __name__ == "__main__":
    main()
