"""
Example: Text Intelligence (Read V1)

This example shows how to analyze text for sentiment, topics, intents, and summaries.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Sending text analysis request...")
    response = client.read.v1.text.analyze(
        request={"text": "Hello, world! This is a sample text for analysis."},
        language="en",
        sentiment=True,
        summarize=True,
        topics=True,
        intents=True,
    )
    
    print("Analysis received:")
    print(f"Sentiment: {response.sentiment}")
    if response.summary:
        print(f"Summary: {response.summary}")
    if response.topics:
        print(f"Topics: {response.topics}")
    if response.intents:
        print(f"Intents: {response.intents}")
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.read.v1.text.analyze(...)
    
except Exception as e:
    print(f"Error: {e}")

