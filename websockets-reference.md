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

    # Start listening
    connection.start_listening()

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
        await connection.start_listening()

        # Send audio data
        from deepgram.extensions.types.sockets import ListenV1MediaMessage
        await connection.send_media(ListenV1MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import ListenV1ControlMessage
        await connection.send_control(ListenV1ControlMessage(type="KeepAlive"))

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

**`send_media(message)`** — Send binary audio data for transcription

- `ListenV1MediaMessage(data=audio_bytes)`

</dd>
</dl>

<dl>
<dd>

**`send_control(message)`** — Send control messages to manage the connection

- `ListenV1ControlMessage(type="KeepAlive")` — Keep the connection alive
- `ListenV1ControlMessage(type="Finalize")` — Finalize the transcription

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

    # Start listening
    connection.start_listening()

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
        await connection.start_listening()

        # Send audio data
        from deepgram.extensions.types.sockets import ListenV2MediaMessage
        await connection.send_media(ListenV2MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import ListenV2ControlMessage
        await connection.send_control(ListenV2ControlMessage(type="CloseStream"))

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

**`send_media(message)`** — Send binary audio data for transcription

- `ListenV2MediaMessage(data=audio_bytes)`

</dd>
</dl>

<dl>
<dd>

**`send_control(message)`** — Send control messages to manage the connection

- `ListenV2ControlMessage(type="CloseStream")` — Close the audio stream

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

    # Start listening
    connection.start_listening()

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
        await connection.start_listening()

        # Send text to be converted to speech
        from deepgram.extensions.types.sockets import SpeakV1TextMessage
        await connection.send_text(SpeakV1TextMessage(text="Hello, world!"))

        # Send control messages
        from deepgram.extensions.types.sockets import SpeakV1ControlMessage
        await connection.send_control(SpeakV1ControlMessage(type="Flush"))
        await connection.send_control(SpeakV1ControlMessage(type="Close"))

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

**`send_text(message)`** — Send text to be converted to speech

- `SpeakV1TextMessage(text="Hello, world!")`

</dd>
</dl>

<dl>
<dd>

**`send_control(message)`** — Send control messages to manage speech synthesis

- `SpeakV1ControlMessage(type="Flush")` — Process all queued text immediately
- `SpeakV1ControlMessage(type="Clear")` — Clear the text queue
- `SpeakV1ControlMessage(type="Close")` — Close the connection

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

    # Start listening
    agent.start_listening()

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
        await agent.start_listening()

        # Send audio data
        from deepgram.extensions.types.sockets import AgentV1MediaMessage
        await agent.send_media(AgentV1MediaMessage(data=audio_bytes))

        # Send control messages
        from deepgram.extensions.types.sockets import AgentV1ControlMessage
        await agent.send_control(AgentV1ControlMessage(type="KeepAlive"))

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

#### 📤 Send Methods

<dl>
<dd>

<dl>
<dd>

**`send_settings(message)`** — Send initial agent configuration settings

- `AgentV1SettingsMessage(...)` — Configure audio, listen, think, and speak providers

</dd>
</dl>

<dl>
<dd>

**`send_media(message)`** — Send binary audio data to the agent

- `AgentV1MediaMessage(data=audio_bytes)`

</dd>
</dl>

<dl>
<dd>

**`send_control(message)`** — Send control messages (keep_alive, etc.)

- `AgentV1ControlMessage(type="KeepAlive")`

</dd>
</dl>

<dl>
<dd>

**`send_update_speak(message)`** — Update the agent's speech synthesis settings

- `AgentV1UpdateSpeakMessage(...)` — Modify TTS configuration during conversation

</dd>
</dl>

<dl>
<dd>

**`send_update_prompt(message)`** — Update the agent's system prompt

- `AgentV1UpdatePromptMessage(...)` — Change the agent's behavior instructions

</dd>
</dl>

<dl>
<dd>

**`send_inject_user_message(message)`** — Inject a user message into the conversation

- `AgentV1InjectUserMessageMessage(...)` — Add a simulated user input

</dd>
</dl>

<dl>
<dd>

**`send_inject_agent_message(message)`** — Inject an agent message into the conversation

- `AgentV1InjectAgentMessageMessage(...)` — Add a simulated agent response

</dd>
</dl>

<dl>
<dd>

**`send_function_call_response(message)`** — Send the result of a function call back to the agent

- `AgentV1FunctionCallResponseMessage(...)` — Provide function execution results

</dd>
</dl>
</dd>
</dl>

</dd>
</dl>
</details>
