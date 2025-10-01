# Speak V1 Audio Chunk Event - protected from auto-generation

# This represents binary audio data received from the WebSocket
# The actual data is bytes, but we define this as a type alias for clarity
SpeakV1AudioChunkEvent = bytes
"""
Audio data in the format specified by the request parameters.
Content-Type: application/octet-stream
"""
