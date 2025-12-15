import threading
import time

from dotenv import load_dotenv

print("Starting agent v1 connect example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.agent.v1.types import (
    AgentV1AgentAudioDone,
    AgentV1AgentStartedSpeaking,
    AgentV1AgentThinking,
    AgentV1ConversationText,
    AgentV1Error,
    AgentV1FunctionCallRequest,
    AgentV1InjectionRefused,
    AgentV1PromptUpdated,
    AgentV1ReceiveFunctionCallResponse,
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider,
    AgentV1SettingsAgentSpeak,
    AgentV1SettingsAgentSpeakOneItem,
    AgentV1SettingsAgentSpeakOneItemProvider_Deepgram,
    AgentV1SettingsAgentThink,
    AgentV1SettingsAgentThinkProviderZero,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
    AgentV1SettingsApplied,
    AgentV1SpeakUpdated,
    AgentV1UserStartedSpeaking,
    AgentV1Warning,
    AgentV1Welcome,
)
from typing import Union

AgentV1SocketClientResponse = Union[
    AgentV1ReceiveFunctionCallResponse,
    AgentV1PromptUpdated,
    AgentV1SpeakUpdated,
    AgentV1InjectionRefused,
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
    str,
]

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    print("Establishing agent connection")
    with client.agent.v1.connect() as agent:
        print("Agent connection context entered")

        # Send minimal settings to configure the agent per the latest spec
        print("Creating agent settings configuration")
        settings = AgentV1Settings(
            audio=AgentV1SettingsAudio(
                input=AgentV1SettingsAudioInput(
                    encoding="linear16",
                    sample_rate=44100,
                )
            ),
            agent=AgentV1SettingsAgent(
                listen=AgentV1SettingsAgentListen(
                    provider=AgentV1SettingsAgentListenProvider(
                        type="deepgram",
                        model="nova-3",
                        smart_format=True,
                    )
                ),
                think=AgentV1SettingsAgentThink(
                    provider=AgentV1SettingsAgentThinkProviderZero(
                        type="open_ai",
                        model="gpt-4o-mini",
                        temperature=0.7,
                    ),
                    prompt='Reply only and explicitly with "OK".',
                ),
                speak=[
                    AgentV1SettingsAgentSpeakOneItem(
                        provider=AgentV1SettingsAgentSpeakOneItemProvider_Deepgram(
                            type="deepgram",
                            model="aura-2-asteria-en",
                        )
                    )
                ],
            ),
        )
        print("Settings configuration created")
        print(f"  - Audio: encoding=linear16, sample_rate=44100")
        print(f"  - Listen: type=deepgram, model=nova-3")
        print(f"  - Think: type=open_ai, model=gpt-4o-mini")
        print(f"  - Speak: type=deepgram, model=aura-2-asteria-en")

        print("Sending SettingsConfiguration message")
        agent.send_agent_v_1_settings(settings)
        print("Settings sent successfully")

        def on_message(message: AgentV1SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print("Received audio event")
                print(f"Event body (audio data length): {len(message)} bytes")
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")
                # For transcription events, extract full transcription; otherwise show full event body
                if msg_type == "Results" or (hasattr(message, "type") and str(message.type) == "Results"):
                    # Extract transcription from Results event
                    if hasattr(message, "channel") and message.channel:
                        channel = message.channel
                        if hasattr(channel, "alternatives") and channel.alternatives:
                            alt = channel.alternatives[0]
                            if hasattr(alt, "transcript") and alt.transcript:
                                print(f"Full transcription: {alt.transcript}")
                            else:
                                print(f"Event body: {message}")
                        else:
                            print(f"Event body: {message}")
                    else:
                        print(f"Event body: {message}")
                else:
                    print(f"Event body: {message}")

        print("Registering event handlers")
        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda error: print(f"Connection error: {error}"))
        print("Event handlers registered")

        # EXAMPLE ONLY: Start listening in a background thread for demo purposes
        # In production, you would typically call agent.start_listening() directly
        # which blocks until the connection closes, or integrate into your async event loop
        print("Starting listening thread")
        threading.Thread(target=agent.start_listening, daemon=True).start()
        print("Waiting 3 seconds for events...")
        time.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
        print("Exiting agent connection context")
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
