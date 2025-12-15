from dotenv import load_dotenv

print("Starting read v1 text analyze with raw response example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    text = "Hello, world!"
    language = "en"
    print(f"Sending text analysis request with raw response - Language: {language}, Text: {text}")
    print(f"  - Sentiment analysis: enabled")
    print(f"  - Summarization: enabled")
    print(f"  - Topics extraction: enabled")
    print(f"  - Intents detection: enabled")
    response = client.read.v1.text.with_raw_response.analyze(
        request={"text": text},
        language=language,
        sentiment=True,
        summarize=True,
        topics=True,
        intents=True,
    )
    print("Raw response received successfully")
    print(f"Response type: {type(response)}")
    if hasattr(response, "status_code"):
        print(f"Status code: {response.status_code}")
    if hasattr(response, "headers"):
        print(f"Response headers: {response.headers}")
    if hasattr(response, "parsed"):
        print(f"Response body: {response.parsed}")
    elif hasattr(response, "body"):
        print(f"Response body: {response.body}")
    else:
        print(f"Response: {response}")
except Exception as e:
    print(f"Error occurred: {type(e).__name__}")
    # Log request headers if available
    if hasattr(e, "request_headers"):
        print(f"Request headers: {e.request_headers}")
    elif hasattr(e, "request") and hasattr(e.request, "headers"):
        print(f"Request headers: {e.request.headers}")
    # Log response headers if available
    if hasattr(e, "headers"):
        print(f"Response headers: {e.headers}")
    # Log status code if available
    if hasattr(e, "status_code"):
        print(f"Status code: {e.status_code}")
    # Log body if available
    if hasattr(e, "body"):
        print(f"Response body: {e.body}")
    print(f"Caught: {e}")
print("Script completed")
