from dotenv import load_dotenv

print("Starting read v1 text analyze with auth token example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

try:
    # Using access token instead of API key
    print("Initializing DeepgramClient for authentication")
    authClient = DeepgramClient()
    print("Auth client initialized")

    print("Requesting access token")
    authResponse = authClient.auth.v1.tokens.grant()
    print("Access token received successfully")
    print(f"Token type: {type(authResponse.access_token)}")

    print("Initializing DeepgramClient with access token")
    client = DeepgramClient(access_token=authResponse.access_token)
    print("Client initialized with access token")

    text = "Hello, world!"
    language = "en"
    print(f"Sending text analysis request - Language: {language}, Text: {text}")
    print(f"  - Sentiment analysis: enabled")
    print(f"  - Summarization: enabled")
    print(f"  - Topics extraction: enabled")
    print(f"  - Intents detection: enabled")
    response = client.read.v1.text.analyze(
        request={"text": text},
        language=language,
        sentiment=True,
        summarize=True,
        topics=True,
        intents=True,
    )
    print("Response received successfully")
    print(f"Response type: {type(response)}")
    print(f"Response body: {response}")
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
