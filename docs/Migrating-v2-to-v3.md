# v2 to v3+ Migration Guide

This guide helps you migrate from Deepgram Python SDK v2 to v3+ (versions 3.0.0 and above). The v3+ release introduces significant improvements including better structure, sync/async support, improved error handling, and support for future products.

## Table of Contents

- [Installation](#installation)
- [Configuration Changes](#configuration-changes)
- [API Method Changes](#api-method-changes)
  - [Listen V1](#listen-v1)
  - [Manage V1](#manage-v1)
- [Breaking Changes Summary](#breaking-changes-summary)

## Installation

The package name remains the same:

```bash
pip install deepgram-sdk
```

To upgrade from v2 to v3+:

```bash
pip install --upgrade deepgram-sdk
```

## Configuration Changes

### v2 Client Initialization

```python
from deepgram import Deepgram

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'

# Initialize the Deepgram SDK
deepgram = Deepgram(DEEPGRAM_API_KEY)
```

### v3+ Client Initialization

```python
from deepgram import DeepgramClient

# Create a Deepgram client using the DEEPGRAM_API_KEY from environment variables
deepgram = DeepgramClient()

# Or with explicit API key
deepgram = DeepgramClient(api_key="YOUR_API_KEY")
```

## API Method Changes

### Listen V1

#### Transcribe File

**v2**

```python
FILE = 'interview_speech-analytics.wav'

# Open the audio file
audio = open(FILE, 'rb')

# Set the source
source = {
    'buffer': audio,
}

# Send the audio to Deepgram and get the response
response = await asyncio.create_task(
    deepgram.transcription.prerecorded(
        source,
        {
            'smart_format': "true",
            'summarize': "v2",
        }
    )
)

# Write the response to the console
print(json.dumps(response, indent=4))
```

**v3+**

```python
from deepgram import PrerecordedOptions, FileSource

AUDIO_FILE = "preamble.wav"

# Call the transcribe_file method on the prerecorded class
with open(AUDIO_FILE, "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(
    smart_format=True,
    summarize="v2",
)
file_response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

json = file_response.to_json()
print(f"{json}")
```

#### Transcribe URL

**v2**

```python
URL = 'https://static.deepgram.com/examples/interview_speech-analytics.wav'

# Set the source
source = {
    'url': URL,
}

# Send the audio to Deepgram and get the response
response = await asyncio.create_task(
    deepgram.transcription.prerecorded(
        source,
        {
            'smart_format': "true",
            'summarize': "v2",
        }
    )
)

# Write the response to the console
print(json.dumps(response, indent=4))
```

**v3+**

```python
from deepgram import PrerecordedOptions, UrlSource

AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}

options = PrerecordedOptions(
    smart_format=True,
    summarize="v2",
)
url_response = deepgram.listen.rest.v("1").transcribe_url(AUDIO_URL, options)

json = url_response.to_json()
print(f"{json}")
```

#### WebSocket Streaming (Listen V1)

**v2**

```python
try:
    deepgramLive = await deepgram.transcription.live({
        'smart_format': True,
        'interim_results': False,
        'language': 'en-US',
        'model': 'nova-3',
    })
except Exception as e:
    print(f'Could not open socket: {e}')
    return

# Listen for the connection to close
deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(
    f'Connection closed with code {c}.'))

# Listen for any transcripts received from Deepgram and write them to the console
deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)

# Listen for the connection to open and send streaming audio from the URL to Deepgram
async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
        while True:
            data = await audio.content.readany()
            deepgramLive.send(data)

            # If no data is being sent from the live stream, then break out of the loop.
            if not data:
                break

# Indicate that we've finished sending data
await deepgramLive.finish()
```

**v3+**

```python
import threading
import httpx
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

try:
    deepgram: DeepgramClient = DeepgramClient()

    dg_connection = deepgram.listen.websocket.v("1")

    # define callbacks for transcription messages
    def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        print(f"speaker: {sentence}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # connect to websocket
    options = LiveOptions(model="nova-3", interim_results=False, language="en-US")
    dg_connection.start(options)

    lock_exit = threading.Lock()
    exit = False

    # define a worker thread
    def myThread():
        with httpx.stream("GET", URL) as r:
            for data in r.iter_bytes():
                lock_exit.acquire()
                if exit:
                    break
                lock_exit.release()

                dg_connection.send(data)

    # start the worker thread
    myHttp = threading.Thread(target=myThread)
    myHttp.start()

    # signal finished
    input("Press Enter to stop recording...\n\n")
    lock_exit.acquire()
    exit = True
    lock_exit.release()

    # Wait for the HTTP thread to close and join
    myHttp.join()

    # Indicate that we've finished
    dg_connection.finish()

except Exception as e:
    print(f"Could not open socket: {e}")
    return
```

### Manage V1

#### Projects

**v2**

```python
# Get projects
result = await deepgram.projects.list()

# Get project
result = await deepgram.projects.get("550e8400-e29b-41d4-a716-446655440000")

# Update project
result = await deepgram.projects.update(object)

# Delete project
result = await deepgram.projects.delete("550e8400-e29b-41d4-a716-446655440000")
```

**v3+**

```python
# Get projects
result = deepgram.manage.v("1").get_projects()

# Get project
result = deepgram.manage.v("1").get_project("550e8400-e29b-41d4-a716-446655440000")

# Update project
result = deepgram.manage.v("1").update_project("550e8400-e29b-41d4-a716-446655440000", name="My TEST RENAME Example")

# Delete project
result = deepgram.manage.v("1").delete_project("550e8400-e29b-41d4-a716-446655440000")
```

#### Keys

**v2**

```python
# List keys
result = await deepgram.keys.list("550e8400-e29b-41d4-a716-446655440000")

# Get key
result = await deepgram.keys.get("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")

# Create key
result = await deepgram.keys.create("550e8400-e29b-41d4-a716-446655440000", "MyTestKey", ["member"])

# Delete key
result = await deepgram.keys.delete("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")
```

**v3+**

```python
from deepgram import KeyOptions

# List keys
result = deepgram.manage.v("1").get_keys("550e8400-e29b-41d4-a716-446655440000")

# Get key
result = deepgram.manage.v("1").get_key("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")

# Create key
options = KeyOptions(
    comment="MyTestKey",
    scopes=["member"],
)
result = deepgram.manage.v("1").create_key("550e8400-e29b-41d4-a716-446655440000", options)

# Delete key
result = deepgram.manage.v("1").delete_key("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")
```

#### Members

**v2**

```python
# Get members
result = await deepgram.members.list_members("550e8400-e29b-41d4-a716-446655440000")

# Remove member
result = await deepgram.members.remove_member("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")
```

**v3+**

```python
# Get members
result = deepgram.manage.v("1").get_members("550e8400-e29b-41d4-a716-446655440000")

# Remove member
result = deepgram.manage.v("1").remove_member("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")
```

#### Scopes

**v2**

```python
# Get member scopes
result = await deepgram.scopes.get_scope("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")

# Update scope
result = await deepgram.scopes.update_scope("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8", 'member')
```

**v3+**

```python
from deepgram import ScopeOptions

# Get member scopes
result = deepgram.manage.v("1").get_member_scopes("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")

# Update scope
options = ScopeOptions(
    scope="admin"
)
result = deepgram.manage.v("1").update_member_scope("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8", options)
```

#### Invitations

**v2**

```python
# List invites
result = await deepgram.invitations.list_invitations("550e8400-e29b-41d4-a716-446655440000")

# Send invite
result = await deepgram.invitations.send_invitation("550e8400-e29b-41d4-a716-446655440000", {
    'email': 'hello@deepgram.com',
    'scope': 'member',
})

# Delete invite
result = await deepgram.invitations.remove_invitation("550e8400-e29b-41d4-a716-446655440000", 'hello@deepgram.com')

# Leave project
result = await deepgram.invitation.leave_project("550e8400-e29b-41d4-a716-446655440000")
```

**v3+**

```python
from deepgram import InviteOptions

# List invites
result = deepgram.manage.v("1").get_invites("550e8400-e29b-41d4-a716-446655440000")

# Send invite
options = InviteOptions(
    email="hello@deepgram.com",
    scope="member"
)
result = deepgram.manage.v("1").send_invite_options("550e8400-e29b-41d4-a716-446655440000", options)

# Delete invite
result = deepgram.manage.v("1").delete_invite("550e8400-e29b-41d4-a716-446655440000", "hello@deepgram.com")

# Leave project
result = deepgram.manage.v("1").leave_project("550e8400-e29b-41d4-a716-446655440000")
```

#### Usage

**v2**

```python
# Get all requests
result = await deepgram.usage.list_requests("550e8400-e29b-41d4-a716-446655440000", {
    'limit': 10,
    # other options are available
})

# Get request
result = await deepgram.usage.get_request("550e8400-e29b-41d4-a716-446655440000", "6ba7b812-9dad-11d1-80b4-00c04fd430c8")

# Get usage summary
result = await deepgram.usage.get_usage("550e8400-e29b-41d4-a716-446655440000", {
    'start': '2020-01-01T00:00:00+00:00',
    # other options are available
})

# Get usage fields
result = await deepgram.usage.get_fields("550e8400-e29b-41d4-a716-446655440000", {
    'start': '2020-01-01T00:00:00+00:00',
    # other options are available
})
```

**v3+**

```python
# Get all requests
result = deepgram.manage.v("1").get_usage_requests("550e8400-e29b-41d4-a716-446655440000", options)

# Get request
result = deepgram.manage.v("1").get_usage_request("550e8400-e29b-41d4-a716-446655440000", "6ba7b812-9dad-11d1-80b4-00c04fd430c8")

# Get usage summary
result = deepgram.manage.v("1").get_usage_summary("550e8400-e29b-41d4-a716-446655440000", options)

# Get usage fields
result = deepgram.manage.v("1").get_usage_fields("550e8400-e29b-41d4-a716-446655440000", options)
```

#### Billing

**v2**

```python
# Get all balances
result = await deepgram.billing.list_balance("550e8400-e29b-41d4-a716-446655440000")

# Get balance
result = await deepgram.billing.get_balance("550e8400-e29b-41d4-a716-446655440000", "6ba7b813-9dad-11d1-80b4-00c04fd430c8")
```

**v3+**

```python
# Get all balances
result = deepgram.manage.v("1").get_balances("550e8400-e29b-41d4-a716-446655440000")

# Get balance
result = deepgram.manage.v("1").get_balance("550e8400-e29b-41d4-a716-446655440000", "6ba7b813-9dad-11d1-80b4-00c04fd430c8")
```

## Breaking Changes Summary

### Major Changes

1. **SDK Structure**: Complete restructure with improved organization
2. **Client Initialization**: New `DeepgramClient` class with environment variable support
3. **API Structure**: New versioned API structure with `v("1")` pattern
4. **Sync/Async Support**: Both synchronous and asynchronous classes and methods
5. **Options Objects**: New typed options objects for better parameter management
6. **WebSocket Implementation**: Improved live client with better abstractions
7. **Error Handling**: Enhanced error handling and logging capabilities

### Removed Features

- Old `Deepgram` client class (replaced with `DeepgramClient`)
- Direct async/await methods on main client (moved to versioned structure)
- Old event handling system (replaced with new event system)

### New Features in v3+

- **Improved Live Client**: Better WebSocket abstractions
- **Verbosity Logging**: Enhanced logging levels for troubleshooting
- **Custom Headers/Query Parameters**: Support for custom API parameters
- **Future Product Support**: Architecture ready for new APIs
- **Better Type Safety**: Typed options objects and responses

### Migration Checklist

- [ ] Upgrade to latest version: `pip install --upgrade deepgram-sdk`
- [ ] Replace `Deepgram` with `DeepgramClient`
- [ ] Update API method calls to new versioned structure
- [ ] Replace direct parameters with options objects
- [ ] Update WebSocket event handling to new system
- [ ] Update error handling for new exception types
- [ ] Test all functionality with new API structure

### Notes

- WebVTT and SRT captions are now available as a standalone package: [deepgram-python-captions](https://github.com/deepgram/deepgram-python-captions)
- Self-hosted API functionality remains unchanged but may have breaking changes in v4
