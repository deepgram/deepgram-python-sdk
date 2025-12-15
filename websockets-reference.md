# WebSockets Reference

## Listen V1 Connect

<details><summary><code>client.listen.v1.<a href="src/deepgram/listen/v1/client.py">connect</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe audio and video using Deepgram's speech-to-text WebSocket

</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Results,
    ListenV1Metadata,
    ListenV1UtteranceEnd,
    ListenV1SpeechStarted,
)

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.listen.v1.connect(model="nova-2") as socket:
    def on_message(message):
        if isinstance(message, ListenV1Results):
            print(f"Received Results: {message}")
        elif isinstance(message, ListenV1Metadata):
            print(f"Received Metadata: {message}")
        elif isinstance(message, ListenV1UtteranceEnd):
            print(f"Received UtteranceEnd: {message}")
        elif isinstance(message, ListenV1SpeechStarted):
            print(f"Received SpeechStarted: {message}")

    socket.on(EventType.OPEN, lambda _: print("Connection opened"))
    socket.on(EventType.MESSAGE, on_message)
    socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
    socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening
    import threading
    listener_thread = threading.Thread(target=socket.start_listening, daemon=True)
    listener_thread.start()

    # Send audio data (read from file or microphone)
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()
    socket.send_listen_v_1_media(audio_data)

    # Send control messages
    from deepgram.listen.v1.types import ListenV1Finalize
    socket.send_listen_v_1_finalize(ListenV1Finalize(type="Finalize"))

```

</dd>
</dl>
</dd>
</dl>

#### 🔌 Async Usage

<dl>
<dd>

<dl>
<dd>

```python
import asyncio
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Results,
    ListenV1Metadata,
    ListenV1UtteranceEnd,
    ListenV1SpeechStarted,
)

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.listen.v1.connect(model="nova-2") as socket:
        def on_message(message):
            if isinstance(message, ListenV1Results):
                print(f"Received Results: {message}")
            elif isinstance(message, ListenV1Metadata):
                print(f"Received Metadata: {message}")
            elif isinstance(message, ListenV1UtteranceEnd):
                print(f"Received UtteranceEnd: {message}")
            elif isinstance(message, ListenV1SpeechStarted):
                print(f"Received SpeechStarted: {message}")

        socket.on(EventType.OPEN, lambda _: print("Connection opened"))
        socket.on(EventType.MESSAGE, on_message)
        socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
        socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(socket.start_listening())

        # Send audio data (read from file or microphone)
        with open("audio.wav", "rb") as audio_file:
            audio_data = audio_file.read()
        await socket.send_listen_v_1_media(audio_data)

        # Send control messages
        from deepgram.listen.v1.types import ListenV1Finalize
        await socket.send_listen_v_1_finalize(ListenV1Finalize(type="Finalize"))

        await listen_task

asyncio.run(main())

```

</dd>
</dl>
</dd>
</dl>

#### 📤 Send Methods

<dl>
<dd>

<dl>
<dd>

**`socket.send_listen_v_1_media(message: bytes)`** — Send binary audio data for transcription

- `message` — Audio data as bytes

</dd>
</dl>

<dl>
<dd>

**`socket.send_listen_v_1_finalize(message: ListenV1Finalize)`** — Send a finalize message to complete transcription

- `ListenV1Finalize(type="Finalize")` — Finalize the transcription

</dd>
</dl>

<dl>
<dd>

**`socket.send_listen_v_1_close_stream(message: ListenV1CloseStream)`** — Send a close stream message to close the audio stream

- `ListenV1CloseStream(type="CloseStream")` — Close the audio stream

</dd>
</dl>

<dl>
<dd>

**`socket.send_listen_v_1_keep_alive(message: ListenV1KeepAlive)`** — Send a keep-alive message to maintain the connection

- `ListenV1KeepAlive(type="KeepAlive")` — Keep the connection alive

</dd>
</dl>

<dl>
<dd>

**`socket.recv() -> V1SocketClientResponse`** — Receive a single message from the WebSocket connection

- Returns one of: `ListenV1Results`, `ListenV1Metadata`, `ListenV1UtteranceEnd`, or `ListenV1SpeechStarted`

</dd>
</dl>

<dl>
<dd>

**`socket.start_listening() -> None`** — Start listening for messages and emit events

- Emits `EventType.OPEN`, `EventType.MESSAGE`, `EventType.ERROR`, and `EventType.CLOSE` events

</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `str` — AI model used to process submitted audio

</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[str]` — URL to which we'll make the callback request

</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[str]` — HTTP method by which the callback request will be made

</dd>
</dl>

<dl>
<dd>

**channels:** `typing.Optional[str]` — Number of independent audio channels contained in submitted audio

</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[str]` — Recognize speaker changes. Each word in the transcript will be assigned a speaker number starting at 0

</dd>
</dl>

<dl>
<dd>

**dictation:** `typing.Optional[str]` — Dictation mode for controlling formatting with dictated speech

</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[str]` — Specify the expected encoding of your submitted audio

</dd>
</dl>

<dl>
<dd>

**endpointing:** `typing.Optional[str]` — Control when speech recognition ends

</dd>
</dl>

<dl>
<dd>

**extra:** `typing.Optional[str]` — Arbitrary key-value pairs that are attached to the API response

</dd>
</dl>

<dl>
<dd>

**interim_results:** `typing.Optional[str]` — Return partial transcripts as audio is being processed

</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[str]` — Key term prompting can boost or suppress specialized terminology and brands

</dd>
</dl>

<dl>
<dd>

**keywords:** `typing.Optional[str]` — Keywords can boost or suppress specialized terminology and brands

</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — BCP-47 language tag that hints at the primary spoken language

</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[str]` — Opts out requests from the Deepgram Model Improvement Program

</dd>
</dl>

<dl>
<dd>

**multichannel:** `typing.Optional[str]` — Transcribe each audio channel independently

</dd>
</dl>

<dl>
<dd>

**numerals:** `typing.Optional[str]` — Convert numbers from written format to numerical format

</dd>
</dl>

<dl>
<dd>

**profanity_filter:** `typing.Optional[str]` — Remove profanity from transcripts

</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[str]` — Add punctuation and capitalization to the transcript

</dd>
</dl>

<dl>
<dd>

**redact:** `typing.Optional[str]` — Redaction removes sensitive information from your transcripts

</dd>
</dl>

<dl>
<dd>

**replace:** `typing.Optional[str]` — Search for terms or phrases in submitted audio and replaces them

</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[str]` — Sample rate of the submitted audio

</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search for terms or phrases in submitted audio

</dd>
</dl>

<dl>
<dd>

**smart_format:** `typing.Optional[str]` — Apply formatting to transcript output for improved readability

</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[str]` — Label your requests for the purpose of identification during usage reporting

</dd>
</dl>

<dl>
<dd>

**utterance_end_ms:** `typing.Optional[str]` — Length of time in milliseconds of silence to wait for before finalizing speech

</dd>
</dl>

<dl>
<dd>

**vad_events:** `typing.Optional[str]` — Return Voice Activity Detection events via the websocket

</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[str]` — Version of the model to use

</dd>
</dl>

<dl>
<dd>

**authorization:** `typing.Optional[str]` — Use your API key for authentication, or alternatively generate a temporary token and pass it via the token query parameter.

**Example:** `token %DEEPGRAM_API_KEY%` or `bearer %DEEPGRAM_TOKEN%`

</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>

## Speak V1 Connect

<details><summary><code>client.speak.v1.<a href="src/deepgram/speak/v1/client.py">connect</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Convert text into natural-sounding speech using Deepgram's TTS WebSocket

</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v1.types import (
    SpeakV1Metadata,
    SpeakV1Flushed,
    SpeakV1Cleared,
    SpeakV1Warning,
)

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.speak.v1.connect(
    model="aura-2",
    encoding="linear16",
    sample_rate=24000
) as socket:
    def on_message(message):
        if isinstance(message, str):
            print("Received audio event")
        elif isinstance(message, SpeakV1Metadata):
            print(f"Received Metadata: {message}")
        elif isinstance(message, SpeakV1Flushed):
            print(f"Received Flushed: {message}")
        elif isinstance(message, SpeakV1Cleared):
            print(f"Received Cleared: {message}")
        elif isinstance(message, SpeakV1Warning):
            print(f"Received Warning: {message}")

    socket.on(EventType.OPEN, lambda _: print("Connection opened"))
    socket.on(EventType.MESSAGE, on_message)
    socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
    socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening
    import threading
    listener_thread = threading.Thread(target=socket.start_listening, daemon=True)
    listener_thread.start()

    # Send text to be converted to speech
    from deepgram.speak.v1.types import SpeakV1Text
    socket.send_speak_v_1_text(SpeakV1Text(text="Hello, world!"))

    # Send control messages
    from deepgram.speak.v1.types import SpeakV1Flush
    socket.send_speak_v_1_flush(SpeakV1Flush(type="Flush"))

```

</dd>
</dl>
</dd>
</dl>

#### 🔌 Async Usage

<dl>
<dd>

<dl>
<dd>

```python
import asyncio
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v1.types import (
    SpeakV1Metadata,
    SpeakV1Flushed,
    SpeakV1Cleared,
    SpeakV1Warning,
)

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.speak.v1.connect(
        model="aura-2",
        encoding="linear16",
        sample_rate=24000
    ) as socket:
        def on_message(message):
            if isinstance(message, str):
                print("Received audio event")
            elif isinstance(message, SpeakV1Metadata):
                print(f"Received Metadata: {message}")
            elif isinstance(message, SpeakV1Flushed):
                print(f"Received Flushed: {message}")
            elif isinstance(message, SpeakV1Cleared):
                print(f"Received Cleared: {message}")
            elif isinstance(message, SpeakV1Warning):
                print(f"Received Warning: {message}")

        socket.on(EventType.OPEN, lambda _: print("Connection opened"))
        socket.on(EventType.MESSAGE, on_message)
        socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
        socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(socket.start_listening())

        # Send text to be converted to speech
        from deepgram.speak.v1.types import SpeakV1Text
        await socket.send_speak_v_1_text(SpeakV1Text(text="Hello, world!"))

        # Send control messages
        from deepgram.speak.v1.types import SpeakV1Flush
        await socket.send_speak_v_1_flush(SpeakV1Flush(type="Flush"))

        await listen_task

asyncio.run(main())

```

</dd>
</dl>
</dd>
</dl>

#### 📤 Send Methods

<dl>
<dd>

<dl>
<dd>

**`socket.send_speak_v_1_text(message: SpeakV1Text)`** — Send text to be converted to speech

- `SpeakV1Text(text="Hello, world!")` — Text content to convert

</dd>
</dl>

<dl>
<dd>

**`socket.send_speak_v_1_flush(message: SpeakV1Flush)`** — Send a flush message to flush the audio buffer

- `SpeakV1Flush(type="Flush")` — Process all queued text immediately

</dd>
</dl>

<dl>
<dd>

**`socket.send_speak_v_1_clear(message: SpeakV1Clear)`** — Send a clear message to clear the text queue

- `SpeakV1Clear(type="Clear")` — Clear the text queue

</dd>
</dl>

<dl>
<dd>

**`socket.send_speak_v_1_close(message: SpeakV1Close)`** — Send a close message to close the connection

- `SpeakV1Close(type="Close")` — Close the connection

</dd>
</dl>

<dl>
<dd>

**`socket.recv() -> V1SocketClientResponse`** — Receive a single message from the WebSocket connection

- Returns one of: `str` (audio data), `SpeakV1Metadata`, `SpeakV1Flushed`, `SpeakV1Cleared`, or `SpeakV1Warning`

</dd>
</dl>

<dl>
<dd>

**`socket.start_listening() -> None`** — Start listening for messages and emit events

- Emits `EventType.OPEN`, `EventType.MESSAGE`, `EventType.ERROR`, and `EventType.CLOSE` events

</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**encoding:** `typing.Optional[str]` — Specify the expected encoding of your output audio

</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[str]` — Opts out requests from the Deepgram Model Improvement Program

</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[str]` — AI model used to process submitted text

</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[str]` — Sample rate for the output audio

</dd>
</dl>

<dl>
<dd>

**authorization:** `typing.Optional[str]` — Use your API key for authentication, or alternatively generate a temporary token and pass it via the token query parameter.

**Example:** `token %DEEPGRAM_API_KEY%` or `bearer %DEEPGRAM_TOKEN%`

</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>

## Listen V2 Connect

<details><summary><code>client.listen.v2.<a href="src/deepgram/listen/v2/client.py">connect</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Real-time conversational speech recognition with contextual turn detection for natural voice conversations

</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2Connected,
    ListenV2TurnInfo,
    ListenV2FatalError,
)

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate="16000"
) as socket:
    def on_message(message):
        if isinstance(message, ListenV2Connected):
            print(f"Received Connected: {message}")
        elif isinstance(message, ListenV2TurnInfo):
            print(f"Received TurnInfo: {message}")
        elif isinstance(message, ListenV2FatalError):
            print(f"Received FatalError: {message}")

    socket.on(EventType.OPEN, lambda _: print("Connection opened"))
    socket.on(EventType.MESSAGE, on_message)
    socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
    socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening
    import threading
    listener_thread = threading.Thread(target=socket.start_listening, daemon=True)
    listener_thread.start()

    # Send audio data (read from file or microphone)
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()
    socket.send_listen_v_2_media(audio_data)

    # Send control messages
    from deepgram.listen.v2.types import ListenV2CloseStream
    socket.send_listen_v_2_close_stream(ListenV2CloseStream(type="CloseStream"))

```

</dd>
</dl>
</dd>
</dl>

#### 🔌 Async Usage

<dl>
<dd>

<dl>
<dd>

```python
import asyncio
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2Connected,
    ListenV2TurnInfo,
    ListenV2FatalError,
)

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="16000"
    ) as socket:
        def on_message(message):
            if isinstance(message, ListenV2Connected):
                print(f"Received Connected: {message}")
            elif isinstance(message, ListenV2TurnInfo):
                print(f"Received TurnInfo: {message}")
            elif isinstance(message, ListenV2FatalError):
                print(f"Received FatalError: {message}")

        socket.on(EventType.OPEN, lambda _: print("Connection opened"))
        socket.on(EventType.MESSAGE, on_message)
        socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
        socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(socket.start_listening())

        # Send audio data (read from file or microphone)
        with open("audio.wav", "rb") as audio_file:
            audio_data = audio_file.read()
        await socket.send_listen_v_2_media(audio_data)

        # Send control messages
        from deepgram.listen.v2.types import ListenV2CloseStream
        await socket.send_listen_v_2_close_stream(ListenV2CloseStream(type="CloseStream"))

        await listen_task

asyncio.run(main())

```

</dd>
</dl>
</dd>
</dl>

#### 📤 Send Methods

<dl>
<dd>

<dl>
<dd>

**`socket.send_listen_v_2_media(message: bytes)`** — Send binary audio data for transcription

- `message` — Audio data as bytes

</dd>
</dl>

<dl>
<dd>

**`socket.send_listen_v_2_close_stream(message: ListenV2CloseStream)`** — Send a close stream message to close the audio stream

- `ListenV2CloseStream(type="CloseStream")` — Close the audio stream

</dd>
</dl>

<dl>
<dd>

**`socket.recv() -> V2SocketClientResponse`** — Receive a single message from the WebSocket connection

- Returns one of: `ListenV2Connected`, `ListenV2TurnInfo`, or `ListenV2FatalError`

</dd>
</dl>

<dl>
<dd>

**`socket.start_listening() -> None`** — Start listening for messages and emit events

- Emits `EventType.OPEN`, `EventType.MESSAGE`, `EventType.ERROR`, and `EventType.CLOSE` events

</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `str` — AI model used to process submitted audio

</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[str]` — Specify the expected encoding of your submitted audio

</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[str]` — Sample rate of the submitted audio

</dd>
</dl>

<dl>
<dd>

**eager_eot_threshold:** `typing.Optional[str]` — Threshold for eager end-of-turn detection

</dd>
</dl>

<dl>
<dd>

**eot_threshold:** `typing.Optional[str]` — Threshold for end-of-turn detection

</dd>
</dl>

<dl>
<dd>

**eot_timeout_ms:** `typing.Optional[str]` — Timeout in milliseconds for end-of-turn detection

</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[str]` — Key term prompting can boost or suppress specialized terminology and brands

</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[str]` — Opts out requests from the Deepgram Model Improvement Program

</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[str]` — Label your requests for the purpose of identification during usage reporting

</dd>
</dl>

<dl>
<dd>

**authorization:** `typing.Optional[str]` — Use your API key for authentication, or alternatively generate a temporary token and pass it via the token query parameter.

**Example:** `token %DEEPGRAM_API_KEY%` or `bearer %DEEPGRAM_TOKEN%`

</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>

## Agent V1 Connect

<details><summary><code>client.agent.v1.<a href="src/deepgram/agent/v1/client.py">connect</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Build a conversational voice agent using Deepgram's Voice Agent WebSocket

</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1Welcome,
    AgentV1SettingsApplied,
    AgentV1ConversationText,
    AgentV1UserStartedSpeaking,
    AgentV1AgentThinking,
    AgentV1FunctionCallRequest,
    AgentV1AgentStartedSpeaking,
    AgentV1AgentAudioDone,
    AgentV1Error,
    AgentV1Warning,
)

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.agent.v1.connect() as socket:
    def on_message(message):
        if isinstance(message, str):
            print("Received audio event")
        elif isinstance(message, AgentV1Welcome):
            print(f"Received Welcome: {message}")
        elif isinstance(message, AgentV1SettingsApplied):
            print(f"Received SettingsApplied: {message}")
        elif isinstance(message, AgentV1ConversationText):
            print(f"Received ConversationText: {message}")
        elif isinstance(message, AgentV1FunctionCallRequest):
            print(f"Received FunctionCallRequest: {message}")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    socket.on(EventType.OPEN, lambda _: print("Connection opened"))
    socket.on(EventType.MESSAGE, on_message)
    socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
    socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening
    import threading
    listener_thread = threading.Thread(target=socket.start_listening, daemon=True)
    listener_thread.start()

    # Send settings
    from deepgram.agent.v1.types import (
        AgentV1Settings,
        AgentV1SettingsAudio,
        AgentV1SettingsAudioInput,
        AgentV1SettingsAgent,
        AgentV1SettingsAgentListen,
        AgentV1SettingsAgentListenProvider,
    )
    settings = AgentV1Settings(
        audio=AgentV1SettingsAudio(
            input=AgentV1SettingsAudioInput(
                encoding="linear16",
                sample_rate=16000,
            )
        ),
        agent=AgentV1SettingsAgent(
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider(
                    type="deepgram",
                    model="nova-3",
                )
            ),
        ),
    )
    socket.send_agent_v_1_settings(settings)

    # Send audio data (read from file or microphone)
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()
    socket.send_agent_v_1_media(audio_data)

    # Send keep-alive
    from deepgram.agent.v1.types import AgentV1KeepAlive
    socket.send_agent_v_1_keep_alive(AgentV1KeepAlive())

```

</dd>
</dl>
</dd>
</dl>

#### 🔌 Async Usage

<dl>
<dd>

<dl>
<dd>

```python
import asyncio
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1Welcome,
    AgentV1SettingsApplied,
    AgentV1ConversationText,
    AgentV1UserStartedSpeaking,
    AgentV1AgentThinking,
    AgentV1FunctionCallRequest,
    AgentV1AgentStartedSpeaking,
    AgentV1AgentAudioDone,
    AgentV1Error,
    AgentV1Warning,
)

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.agent.v1.connect() as socket:
        def on_message(message):
            if isinstance(message, str):
                print("Received audio event")
            elif isinstance(message, AgentV1Welcome):
                print(f"Received Welcome: {message}")
            elif isinstance(message, AgentV1SettingsApplied):
                print(f"Received SettingsApplied: {message}")
            elif isinstance(message, AgentV1ConversationText):
                print(f"Received ConversationText: {message}")
            elif isinstance(message, AgentV1FunctionCallRequest):
                print(f"Received FunctionCallRequest: {message}")
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")

        socket.on(EventType.OPEN, lambda _: print("Connection opened"))
        socket.on(EventType.MESSAGE, on_message)
        socket.on(EventType.CLOSE, lambda _: print("Connection closed"))
        socket.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(socket.start_listening())

        # Send settings
        from deepgram.agent.v1.types import (
            AgentV1Settings,
            AgentV1SettingsAudio,
            AgentV1SettingsAudioInput,
            AgentV1SettingsAgent,
            AgentV1SettingsAgentListen,
            AgentV1SettingsAgentListenProvider,
        )
        settings = AgentV1Settings(
            audio=AgentV1SettingsAudio(
                input=AgentV1SettingsAudioInput(
                    encoding="linear16",
                    sample_rate=16000,
                )
            ),
            agent=AgentV1SettingsAgent(
                listen=AgentV1SettingsAgentListen(
                    provider=AgentV1SettingsAgentListenProvider(
                        type="deepgram",
                        model="nova-3",
                    )
                ),
            ),
        )
        await socket.send_agent_v_1_settings(settings)

        # Send audio data (read from file or microphone)
        with open("audio.wav", "rb") as audio_file:
            audio_data = audio_file.read()
        await socket.send_agent_v_1_media(audio_data)

        # Send keep-alive
        from deepgram.agent.v1.types import AgentV1KeepAlive
        await socket.send_agent_v_1_keep_alive(AgentV1KeepAlive())

        await listen_task

asyncio.run(main())

```

</dd>
</dl>
</dd>
</dl>

#### 📤 Send Methods

<dl>
<dd>

<dl>
<dd>

**`socket.send_agent_v_1_settings(message: AgentV1Settings)`** — Send initial agent configuration settings

- `AgentV1Settings(...)` — Configure audio, listen, think, and speak providers

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_media(message: bytes)`** — Send binary audio data to the agent

- `message` — Audio data as bytes

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_keep_alive(message: AgentV1KeepAlive)`** — Send a keep-alive message to maintain the connection

- `AgentV1KeepAlive()` — Keep the connection alive (type defaults to "KeepAlive")

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_update_speak(message: AgentV1UpdateSpeak)`** — Update the agent's speech synthesis settings

- `AgentV1UpdateSpeak(...)` — Modify TTS configuration during conversation

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_update_prompt(message: AgentV1UpdatePrompt)`** — Update the agent's system prompt

- `AgentV1UpdatePrompt(...)` — Change the agent's behavior instructions

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_inject_user_message(message: AgentV1InjectUserMessage)`** — Inject a user message into the conversation

- `AgentV1InjectUserMessage(...)` — Add a simulated user input

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_inject_agent_message(message: AgentV1InjectAgentMessage)`** — Inject an agent message into the conversation

- `AgentV1InjectAgentMessage(...)` — Add a simulated agent response

</dd>
</dl>

<dl>
<dd>

**`socket.send_agent_v_1_send_function_call_response(message: AgentV1SendFunctionCallResponse)`** — Send the result of a function call back to the agent

- `AgentV1SendFunctionCallResponse(...)` — Provide function execution results

</dd>
</dl>

<dl>
<dd>

**`socket.recv() -> V1SocketClientResponse`** — Receive a single message from the WebSocket connection

- Returns one of: `str` (audio data), `AgentV1Welcome`, `AgentV1SettingsApplied`, `AgentV1ConversationText`, `AgentV1UserStartedSpeaking`, `AgentV1AgentThinking`, `AgentV1FunctionCallRequest`, `AgentV1AgentStartedSpeaking`, `AgentV1AgentAudioDone`, `AgentV1Error`, `AgentV1Warning`, or other agent message types

</dd>
</dl>

<dl>
<dd>

**`socket.start_listening() -> None`** — Start listening for messages and emit events

- Emits `EventType.OPEN`, `EventType.MESSAGE`, `EventType.ERROR`, and `EventType.CLOSE` events

</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**authorization:** `typing.Optional[str]` — Use your API key for authentication, or alternatively generate a temporary token and pass it via the token query parameter.

**Example:** `token %DEEPGRAM_API_KEY%` or `bearer %DEEPGRAM_TOKEN%`

</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>
