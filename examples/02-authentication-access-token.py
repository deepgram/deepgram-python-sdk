"""
Example: Authentication with Access Token

This example shows how to authenticate using an access token.
Access tokens are useful for client-side applications and have a limited lifetime.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

# First, grant an access token using your API key
auth_client = DeepgramClient()

print("Requesting access token...")
auth_response = auth_client.auth.v1.tokens.grant()
print(f"Access token received (expires in {auth_response.expires_in} seconds)")

# Create a client with the access token
client = DeepgramClient(access_token=auth_response.access_token)

# Or use environment variable: DEEPGRAM_TOKEN
# client = DeepgramClient()

print("Client initialized with access token")

