import json  # noqa: F401
import time

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.extensions.types.sockets import (
    AgentV1Agent,
    AgentV1AudioConfig,
    AgentV1AudioInput,
    AgentV1DeepgramSpeakProvider,
    AgentV1Listen,
    AgentV1ListenProvider,
    AgentV1OpenAiThinkProvider,
    AgentV1SettingsMessage,
    AgentV1SpeakProviderConfig,
    AgentV1Think,
)

client = DeepgramClient()

try:
    with client.agent.v1.with_raw_response.connect() as agent:
        # Send minimal settings to configure the agent per the latest spec
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

        # Send settings using raw method
        print("Send SettingsConfiguration message")
        agent._send_model(settings)

        # EXAMPLE ONLY: Manually read messages for demo purposes
        # In production, you would use the standard event handlers and start_listening()
        print("Connection opened")
        try:
            start = time.time()
            while time.time() - start < 3:
                raw = agent._websocket.recv()  # type: ignore[attr-defined]
                if isinstance(raw, (bytes, bytearray)):
                    print("Received audio event")
                    continue
                try:
                    data = json.loads(raw)
                    msg_type = data.get("type", "Unknown")
                    print(f"Received {msg_type} event")
                    if msg_type == "AgentAudioDone":
                        break
                except Exception:
                    print("Received message event")
        except Exception as e:
            print(f"Caught: {e}")
        finally:
            print("Connection closed")
except Exception as e:
    print(f"Caught: {e}")