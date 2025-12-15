import json  # noqa: F401
import time

from dotenv import load_dotenv

print("Starting agent v1 connect with raw response example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
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
)

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    print("Establishing agent connection with raw response")
    with client.agent.v1.with_raw_response.connect() as agent:
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

        # Send settings using raw method
        print("Sending SettingsConfiguration message using raw method")
        agent._send_model(settings)
        print("Settings sent successfully")

        # EXAMPLE ONLY: Manually read messages for demo purposes
        # In production, you would use the standard event handlers and start_listening()
        print("Connection opened")
        print("Starting raw message reading loop (3 seconds)")
        try:
            start = time.time()
            while time.time() - start < 3:
                raw = agent._websocket.recv()  # type: ignore[attr-defined]
                if isinstance(raw, (bytes, bytearray)):
                    print("Received audio event")
                    print(f"Event body (audio data length): {len(raw)} bytes")
                    continue
                try:
                    data = json.loads(raw)
                    msg_type = data.get("type", "Unknown")
                    print(f"Received {msg_type} event")
                    # For transcription events, extract full transcription; otherwise show full event body
                    if msg_type == "Results":
                        # Extract transcription from Results event
                        if "channel" in data and data["channel"]:
                            channel = data["channel"]
                            if "alternatives" in channel and channel["alternatives"]:
                                alt = channel["alternatives"][0]
                                if "transcript" in alt and alt["transcript"]:
                                    print(f"Full transcription: {alt['transcript']}")
                                else:
                                    print(f"Event body: {data}")
                            else:
                                print(f"Event body: {data}")
                        else:
                            print(f"Event body: {data}")
                    else:
                        print(f"Event body: {data}")
                    if msg_type == "AgentAudioDone":
                        print("AgentAudioDone received, breaking loop")
                        break
                except Exception as e:
                    print(f"Error parsing message: {e}")
                    print(f"Received raw message: {raw}")
        except Exception as e:
            print(f"Error occurred during message reading: {type(e).__name__}")
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
        finally:
            print("Connection closed")
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
