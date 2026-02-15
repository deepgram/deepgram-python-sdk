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
    if response.results.sentiments:
        print(f"Sentiment: {response.results.sentiments.average}")
    if response.results.summary:
        print(f"Summary: {response.results.summary.text}")
    if response.results.topics:
        print(f"Topics: {response.results.topics.segments}")
    if response.results.intents:
        print(f"Intents: {response.results.intents.segments}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.read.v1.text.analyze(...)

except Exception as e:
    print(f"Error: {e}")
