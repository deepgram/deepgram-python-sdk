"""Live Flux TTS control check.

Requires ``DEEPGRAM_API_KEY``. Optionally set ``DEEPGRAM_BASE_URL`` to an
HTTP(S) or WS(S) target; the script normalizes the REST and WebSocket targets.
"""

import asyncio
import os

from deepgram import AsyncDeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment
from deepgram.speak.v2.types import SpeakV2Speak


def _environment() -> DeepgramClientEnvironment:
    target = os.environ.get("DEEPGRAM_BASE_URL", "https://api.deepgram.com").rstrip("/")
    rest = target.replace("wss://", "https://").replace("ws://", "http://")
    websocket = rest.replace("https://", "wss://").replace("http://", "ws://")
    print(f"REST target: {rest}/v2/speak")
    print(f"WebSocket target: {websocket}/v2/speak")
    return DeepgramClientEnvironment(base=rest, production=websocket, agent=websocket, agent_rest=rest)


async def _batch(client: AsyncDeepgramClient) -> None:
    async for _ in client.speak.v2.audio.generate(model="flux-alexis-en", text="Hello {pause:500}there."):
        break
    async for _ in client.speak.v2.audio.generate(
        model="flux-alexis-en", text='Hello {"word":"Deepgram","pronounce":"diːpɡræm"}.'
    ):
        break
    try:
        async for _ in client.speak.v2.audio.generate(
            model="flux-alexis-en", text='{"word":"Deepgram","pronounce":"diːpɡræm"}', speed=1.1
        ):
            pass
    except ApiError as exc:
        print(f"Expected batch control rejection: {exc.status_code}")
    else:
        raise AssertionError("batch speed plus pronunciation should be rejected")


async def _streaming(client: AsyncDeepgramClient) -> None:
    async with client.speak.v2.connect(model="flux-alexis-en") as connection:
        await connection.send_speak(SpeakV2Speak(text='{"word":"Deepgram","pronounce":"diːpɡræm"}'))
        await connection.send_flush()
        while True:
            message = await asyncio.wait_for(connection.recv(), timeout=10)
            if getattr(message, "type", None) == "SpeechMetadata":
                print(f"Streaming pronunciation controls: {message.controls_applied}")
                return


async def main() -> None:
    if not os.environ.get("DEEPGRAM_API_KEY"):
        print("SKIP: DEEPGRAM_API_KEY not set")
        return
    client = AsyncDeepgramClient(environment=_environment())
    await _batch(client)
    await _streaming(client)


if __name__ == "__main__":
    asyncio.run(main())
