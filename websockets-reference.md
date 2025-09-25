# WebSocket Reference

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
from deepgram.extensions.types.sockets import ListenV1SocketClientResponse

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.listen.v1.connect(model="nova-3") as connection:
    def on_message(message: ListenV1SocketClientResponse) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening in a background thread
    threading.Thread(target=connection.start_listening, daemon=True).start()

    # Send audio data
    from deepgram.extensions.types.sockets import ListenV1MediaMessage
    connection.send_media(ListenV1MediaMessage(data=audio_bytes))

    # Send control messages
    from deepgram.extensions.types.sockets import ListenV1ControlMessage
    connection.send_control(ListenV1ControlMessage(type="KeepAlive"))

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
from deepgram.extensions.types.sockets import ListenV1SocketClientResponse

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.listen.v1.connect(model="nova-3") as connection:
        def on_message(message: ListenV1SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(connection.start_listening())

        # Send audio data
        from deepgram.extensions.types.sockets import ListenV1MediaMessage
        await connection.send_media(ListenV1MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import ListenV1ControlMessage
        await connection.send_control(ListenV1ControlMessage(type="KeepAlive"))

        # Wait and cleanup
        await asyncio.sleep(3)
        listen_task.cancel()

asyncio.run(main())

```

</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `str` — AI model to use for the transcription

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

**filler_words:** `typing.Optional[str]` — Include filler words like "uh" and "um" in transcripts

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
from deepgram.extensions.types.sockets import ListenV2SocketClientResponse

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate="16000"
) as connection:
    def on_message(message: ListenV2SocketClientResponse) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening in a background thread
    threading.Thread(target=connection.start_listening, daemon=True).start()

    # Send audio data
    from deepgram.extensions.types.sockets import ListenV2MediaMessage
    connection.send_media(ListenV2MediaMessage(data=audio_bytes))

    # Send control messages
    from deepgram.extensions.types.sockets import ListenV2ControlMessage
    connection.send_control(ListenV2ControlMessage(type="CloseStream"))

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
from deepgram.extensions.types.sockets import ListenV2SocketClientResponse

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="16000"
    ) as connection:
        def on_message(message: ListenV2SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(connection.start_listening())

        # Send audio data
        from deepgram.extensions.types.sockets import ListenV2MediaMessage
        await connection.send_media(ListenV2MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import ListenV2ControlMessage
        await connection.send_control(ListenV2ControlMessage(type="CloseStream"))

        # Wait and cleanup
        await asyncio.sleep(3)
        listen_task.cancel()

asyncio.run(main())

```

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

**encoding:** `str` — Specify the expected encoding of your submitted audio

</dd>
</dl>

<dl>
<dd>

**sample_rate:** `str` — Sample rate of the submitted audio

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
from deepgram.extensions.types.sockets import SpeakV1SocketClientResponse

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.speak.v1.connect(
    model="aura-2-asteria-en",
    encoding="linear16",
    sample_rate=24000
) as connection:
    def on_message(message: SpeakV1SocketClientResponse) -> None:
        if isinstance(message, bytes):
            print("Received audio event")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening in a background thread
    threading.Thread(target=connection.start_listening, daemon=True).start()

    # Send text to be converted to speech
    from deepgram.extensions.types.sockets import SpeakV1TextMessage
    connection.send_text(SpeakV1TextMessage(text="Hello, world!"))

    # Send control messages
    from deepgram.extensions.types.sockets import SpeakV1ControlMessage
    connection.send_control(SpeakV1ControlMessage(type="Flush"))
    connection.send_control(SpeakV1ControlMessage(type="Close"))

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
from deepgram.extensions.types.sockets import SpeakV1SocketClientResponse

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.speak.v1.connect(
        model="aura-2-asteria-en",
        encoding="linear16",
        sample_rate=24000
    ) as connection:
        def on_message(message: SpeakV1SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print("Received audio event")
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(connection.start_listening())

        # Send text to be converted to speech
        from deepgram.extensions.types.sockets import SpeakV1TextMessage
        await connection.send_text(SpeakV1TextMessage(text="Hello, world!"))

        # Send control messages
        from deepgram.extensions.types.sockets import SpeakV1ControlMessage
        await connection.send_control(SpeakV1ControlMessage(type="Flush"))
        await connection.send_control(SpeakV1ControlMessage(type="Close"))

        # Wait and cleanup
        await asyncio.sleep(3)
        listen_task.cancel()

asyncio.run(main())

```

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
from deepgram.extensions.types.sockets import (
    AgentV1Agent,
    AgentV1AudioConfig,
    AgentV1AudioInput,
    AgentV1DeepgramSpeakProvider,
    AgentV1Listen,
    AgentV1ListenProvider,
    AgentV1OpenAiThinkProvider,
    AgentV1SettingsMessage,
    AgentV1SocketClientResponse,
    AgentV1SpeakProviderConfig,
    AgentV1Think,
)

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)

with client.agent.v1.connect() as agent:
    # Configure the agent
    settings = AgentV1SettingsMessage(
        audio=AgentV1AudioConfig(
            input=AgentV1AudioInput(
                encoding="linear16",
                sample_rate=44100,
            )
        ),
        agent=AgentV1Agent(
            listen=AgentV1Listen(
                provider=AgentV1ListenProvider(
                    type="deepgram",
                    model="nova-3",
                    smart_format=True,
                )
            ),
            think=AgentV1Think(
                provider=AgentV1OpenAiThinkProvider(
                    type="open_ai",
                    model="gpt-4o-mini",
                    temperature=0.7,
                ),
                prompt='Reply only and explicitly with "OK".',
            ),
            speak=AgentV1SpeakProviderConfig(
                provider=AgentV1DeepgramSpeakProvider(
                    type="deepgram",
                    model="aura-2-asteria-en",
                )
            ),
        ),
    )

    agent.send_settings(settings)

    def on_message(message: AgentV1SocketClientResponse) -> None:
        if isinstance(message, bytes):
            print("Received audio event")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    agent.on(EventType.OPEN, lambda _: print("Connection opened"))
    agent.on(EventType.MESSAGE, on_message)
    agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
    agent.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

    # Start listening in a background thread
    threading.Thread(target=agent.start_listening, daemon=True).start()

    # Send audio data
    from deepgram.extensions.types.sockets import AgentV1MediaMessage
    agent.send_media(AgentV1MediaMessage(data=audio_bytes))

    # Send control messages
    from deepgram.extensions.types.sockets import AgentV1ControlMessage
    agent.send_control(AgentV1ControlMessage(type="KeepAlive"))

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
from deepgram.extensions.types.sockets import (
    AgentV1Agent,
    AgentV1AudioConfig,
    AgentV1AudioInput,
    AgentV1DeepgramSpeakProvider,
    AgentV1Listen,
    AgentV1ListenProvider,
    AgentV1OpenAiThinkProvider,
    AgentV1SettingsMessage,
    AgentV1SocketClientResponse,
    AgentV1SpeakProviderConfig,
    AgentV1Think,
)

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)

async def main():
    async with client.agent.v1.connect() as agent:
        # Configure the agent
        settings = AgentV1SettingsMessage(
            audio=AgentV1AudioConfig(
                input=AgentV1AudioInput(
                    encoding="linear16",
                    sample_rate=16000,
                )
            ),
            agent=AgentV1Agent(
                listen=AgentV1Listen(
                    provider=AgentV1ListenProvider(
                        type="deepgram",
                        model="nova-3",
                        smart_format=True,
                    )
                ),
                think=AgentV1Think(
                    provider=AgentV1OpenAiThinkProvider(
                        type="open_ai",
                        model="gpt-4o-mini",
                        temperature=0.7,
                    )
                ),
                speak=AgentV1SpeakProviderConfig(
                    provider=AgentV1DeepgramSpeakProvider(
                        type="deepgram",
                        model="aura-2-asteria-en",
                    )
                ),
            ),
        )

        await agent.send_settings(settings)

        def on_message(message: AgentV1SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print("Received audio event")
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")

        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Start listening
        listen_task = asyncio.create_task(agent.start_listening())

        # Send audio data
        from deepgram.extensions.types.sockets import AgentV1MediaMessage
        await agent.send_media(AgentV1MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import AgentV1ControlMessage
        await agent.send_control(AgentV1ControlMessage(type="KeepAlive"))

        # Wait and cleanup
        await asyncio.sleep(3)
        listen_task.cancel()

asyncio.run(main())

```

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

#### 🔧 Agent Methods

<dl>
<dd>

<dl>
<dd>

**send_settings(message: AgentV1SettingsMessage)** — Send initial agent configuration settings

</dd>
</dl>

<dl>
<dd>

**send_control(message: AgentV1ControlMessage)** — Send a control message (keep_alive, etc.)

</dd>
</dl>

<dl>
<dd>

**send_update_speak(message: AgentV1UpdateSpeakMessage)** — Update the agent's speech synthesis settings

</dd>
</dl>

<dl>
<dd>

**send_update_prompt(message: AgentV1UpdatePromptMessage)** — Update the agent's system prompt

</dd>
</dl>

<dl>
<dd>

**send_inject_user_message(message: AgentV1InjectUserMessageMessage)** — Inject a user message into the conversation

</dd>
</dl>

<dl>
<dd>

**send_inject_agent_message(message: AgentV1InjectAgentMessageMessage)** — Inject an agent message into the conversation

</dd>
</dl>

<dl>
<dd>

**send_function_call_response(message: AgentV1FunctionCallResponseMessage)** — Send the result of a function call back to the agent

</dd>
</dl>

<dl>
<dd>

**send_media(message: AgentV1MediaMessage)** — Send binary audio data to the agent

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>

## Common WebSocket Methods

### Event Handling

All WebSocket connections support the following event handling pattern:

```python
from deepgram.core.events import EventType

# Set up event handlers
connection.on(EventType.OPEN, lambda _: print("Connection opened"))
connection.on(EventType.MESSAGE, on_message_handler)
connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

# Start listening for events
connection.start_listening()  # Synchronous
# or
await connection.start_listening()  # Asynchronous
```

### Authentication with Tokens

You can use temporary tokens for authentication instead of API keys:

```python
from deepgram import DeepgramClient

# Generate a temporary token
auth_client = DeepgramClient(api_key="YOUR_API_KEY")
token_response = auth_client.auth.v1.tokens.grant()

# Use the token for WebSocket connection
client = DeepgramClient(access_token=token_response.access_token)
with client.listen.v1.connect(model="nova-3") as connection:
    # Your WebSocket code here
    pass
```

### Raw Response Access

All WebSocket clients provide access to raw responses:

```python
# Access raw client for more control
with client.listen.v1.with_raw_response.connect(model="nova-3") as connection:
    # Raw connection handling
    pass
```

### Message Types

#### Listen V1/V2 Message Types

- **ListenV1MediaMessage** / **ListenV2MediaMessage** — Binary audio data
- **ListenV1ControlMessage** — Control messages (KeepAlive, Finalize, CloseStream)
- **ListenV2ControlMessage** — Control messages (CloseStream)

#### Speak V1 Message Types

- **SpeakV1TextMessage** — Text to be converted to speech
- **SpeakV1ControlMessage** — Control messages (Flush, Clear, Close)

#### Agent V1 Message Types

- **AgentV1SettingsMessage** — Initial configuration
- **AgentV1ControlMessage** — Control messages
- **AgentV1MediaMessage** — Binary audio data
- **AgentV1UpdateSpeakMessage** — Update speech settings
- **AgentV1UpdatePromptMessage** — Update system prompt
- **AgentV1InjectUserMessageMessage** — Inject user message
- **AgentV1InjectAgentMessageMessage** — Inject agent message
- **AgentV1FunctionCallResponseMessage** — Function call response
