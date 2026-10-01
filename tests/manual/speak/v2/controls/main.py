"""Live Flux TTS control check.

Requires ``DEEPGRAM_API_KEY``. Optionally set ``DEEPGRAM_BASE_URL`` to an
HTTP(S) or WS(S) target; the script normalizes the REST and WebSocket targets.
"""

import asyncio
import os

from deepgram import AsyncDeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment
from deepgram.speak.v2.types import SpeakV2Error, SpeakV2Speak


def _environment() -> DeepgramClientEnvironment:
    target = os.environ.get("DEEPGRAM_BASE_URL", "https://api.deepgram.com").rstrip("/")
    rest = target.replace("wss://", "https://").replace("ws://", "http://")
    websocket = rest.replace("https://", "wss://").replace("http://", "ws://")
    print(f"REST target: {rest}/v2/speak")
    print(f"WebSocket target: {websocket}/v2/speak")
    return DeepgramClientEnvironment(base=rest, production=websocket, agent=websocket, agent_rest=rest)


async def _batch(client: AsyncDeepgramClient) -> None:
    async for _ in client.speak.v2.audio.generate(model="flux-alexis-en", text=r"Hello \{pause:500ms\}there."):
        break
    async for _ in client.speak.v2.audio.generate(
        model="flux-alexis-en", text=r'Hello \{"word": "Deepgram", "pronounce": "diːpɡræm"\}.'
    ):
        break
    try:
        async for _ in client.speak.v2.audio.generate(
            model="flux-alexis-en", text=r'\{"word": "Deepgram", "pronounce": "diːpɡræm"\}', speed=1.1
        ):
            pass
    except ApiError as exc:
        if exc.status_code != 400 or exc.body.get("err_code") != "CONTROL_COMBINATION_INVALID":
            raise AssertionError(f"expected CONTROL_COMBINATION_INVALID, received {exc}") from exc
        print(f"Expected batch control rejection: {exc.status_code}")
    else:
        raise AssertionError("batch speed plus pronunciation should be rejected")


async def _streaming(client: AsyncDeepgramClient) -> None:
    async with client.speak.v2.connect(model="flux-alexis-en") as connection:
        await connection.send_speak(SpeakV2Speak(text=r'\{"word": "Deepgram", "pronounce": "diːpɡræm"\}'))
        await connection.send_flush()
        while True:
            message = await asyncio.wait_for(connection.recv(), timeout=10)
            if getattr(message, "type", None) == "SpeechMetadata":
                print(f"Streaming pronunciation controls: {message.controls_applied}")
                break

        await connection.send_speak(SpeakV2Speak(text=r"\{pause:500ms\}"))
        await connection.send_flush()
        while True:
            message = await asyncio.wait_for(connection.recv(), timeout=10)
            if isinstance(message, SpeakV2Error):
                if message.code != "DATA-0002":
                    raise AssertionError(f"expected DATA-0002 for a streaming pause, received {message.code}")
                print("Streaming pauses rejected with DATA-0002")
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
