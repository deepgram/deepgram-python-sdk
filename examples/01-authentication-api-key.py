"""
Example: Authentication with API Key

This example shows how to authenticate using an API key.
The API key can be provided via:
1. Environment variable: DEEPGRAM_API_KEY
2. Explicit parameter: DeepgramClient(api_key="your-api-key")
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

# API key is automatically loaded from DEEPGRAM_API_KEY environment variable
client = DeepgramClient()

# Or explicitly provide the API key:
# client = DeepgramClient(api_key="your-api-key-here")

print("Client initialized with API key")
