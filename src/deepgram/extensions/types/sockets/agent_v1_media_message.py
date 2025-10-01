# Agent V1 Media Message - protected from auto-generation

# This represents binary media data sent to the Voice Agent WebSocket
# The actual data is bytes, but we define this as a type alias for clarity
AgentV1MediaMessage = bytes
"""
Raw binary audio data sent to Deepgram's Voice Agent API for processing.
Content-Type: application/octet-stream
"""
