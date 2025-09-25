import asyncio

from dotenv import load_dotenv

load_dotenv()

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

client = AsyncDeepgramClient()

async def main() -> None:
    try:
        async with client.agent.v1.connect() as agent:
            # Send minimal settings to configure the agent per the latest spec
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

            print("Send SettingsConfiguration message")
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

            # EXAMPLE ONLY: Start listening task and cancel after brief demo
            # In production, you would typically await agent.start_listening() directly
            # which runs until the connection closes or is interrupted
            listen_task = asyncio.create_task(agent.start_listening())
            await asyncio.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
            listen_task.cancel()
    except Exception as e:
        print(f"Caught: {e}")

asyncio.run(main())
