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
    
    # Access results from the response.results object
    if response.results.sentiments:
        if response.results.sentiments.average:
            print(f"Average Sentiment: {response.results.sentiments.average.sentiment} (score: {response.results.sentiments.average.sentiment_score})")
        if response.results.sentiments.segments:
            print(f"Sentiment segments: {len(response.results.sentiments.segments)} found")
    
    if response.results.summary:
        if response.results.summary.results and response.results.summary.results.summary:
            print(f"Summary: {response.results.summary.results.summary.summary}")
    
    if response.results.topics:
        if response.results.topics.results and response.results.topics.results.topics:
            segments = response.results.topics.results.topics.segments
            if segments:
                print(f"Topics found: {len(segments)} segments")
                # Access topics from segments
                for segment in segments[:3]:  # Show first 3 segments
                    if segment.topics:
                        topic_names = [topic.topic for topic in segment.topics if hasattr(topic, 'topic')]
                        if topic_names:
                            print(f"  - {', '.join(topic_names)}")
    
    if response.results.intents:
        if response.results.intents.results and response.results.intents.results.intents:
            segments = response.results.intents.results.intents.segments
            if segments:
                print(f"Intents found: {len(segments)} segments")
                # Access intents from segments
                for segment in segments[:3]:  # Show first 3 segments
                    if segment.intents:
                        intent_names = [intent.intent for intent in segment.intents if hasattr(intent, 'intent')]
                        if intent_names:
                            print(f"  - {', '.join(intent_names)}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.read.v1.text.analyze(
    #     request={"text": "Hello, world! This is a sample text for analysis."},
    #     language="en",
    #     sentiment=True,
    #     summarize=True,
    #     topics=True,
    #     intents=True,
    # )

    # With access token:
    # client = DeepgramClient(access_token="your-access-token")

except Exception as e:
    print(f"Error: {e}")
