"""
Example: Voice Agent (Agent V1) - Basic Connection

This example shows how to connect to the Deepgram Voice Agent WebSocket endpoint.
Connects to agent.deepgram.com/v1/agent/converse
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    # Connect to agent.deepgram.com/v1/agent/converse WebSocket endpoint
    with client.agent.v1.connect() as agent:
        print("Connected to Voice Agent WebSocket")
        print("Connection ready")

        # Connection will remain open until context manager exits
        # In a real application, you would register event handlers and start listening here

except Exception as e:
    import traceback

    print(f"Error: {e}")
    traceback.print_exc()
