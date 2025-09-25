import threading
import time

from dotenv import load_dotenv

load_dotenv()

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

client = DeepgramClient()

try:
    with client.agent.v1.connect() as agent:
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

        print("Send SettingsConfiguration message")
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

        # EXAMPLE ONLY: Start listening in a background thread for demo purposes
        # In production, you would typically call agent.start_listening() directly
        # which blocks until the connection closes, or integrate into your async event loop
        threading.Thread(target=agent.start_listening, daemon=True).start()
        time.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
except Exception as e:
    print(f"Caught: {e}")
