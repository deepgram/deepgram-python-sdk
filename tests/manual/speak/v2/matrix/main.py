"""Live check for the Flux TTS speed boundaries.

Requires `DEEPGRAM_API_KEY`. Run with:

    python tests/manual/speak/v2/matrix/main.py
    DEEPGRAM_BASE_URL=wss://<host> python tests/manual/speak/v2/matrix/main.py

The generated speed documentation permits values from 0.5 through 1.5 in 0.05
increments. This matrix verifies the server's typed reconfiguration responses
for representative endpoints, a valid historical value, and invalid
out-of-range and off-increment values.
"""

import asyncio
import os

from dotenv import load_dotenv

from deepgram import AsyncDeepgramClient
from deepgram.environment import DeepgramClientEnvironment
from deepgram.speak.v2.types import SpeakV2Configure, SpeakV2ConfigureFailure, SpeakV2ConfigureSuccess

ACCEPTED_SPEEDS = (0.5, 0.85, 1.15, 1.5)
REJECTED_SPEEDS = ((0.45, "SPEED_OUT_OF_RANGE"), (1.55, "SPEED_OUT_OF_RANGE"), (1.03, "SPEED_INCREMENT_INVALID"))
MODEL = "flux-alexis-en"


def _client_environment() -> DeepgramClientEnvironment:
    """Optionally direct the live check to a non-production WebSocket host."""
    base = os.environ.get("DEEPGRAM_BASE_URL")
    if not base:
        return DeepgramClientEnvironment.PRODUCTION
    base = base.replace("https://", "wss://").replace("http://", "ws://")
    https = base.replace("wss://", "https://").replace("ws://", "http://")
    return DeepgramClientEnvironment(base=https, production=base, agent=base, agent_rest=https)


async def _configure_speed(
    client: AsyncDeepgramClient, speed: float
) -> SpeakV2ConfigureSuccess | SpeakV2ConfigureFailure:
    async with client.speak.v2.connect(model=MODEL) as connection:
        await connection.send_configure(SpeakV2Configure(speed=speed))
        while True:
            try:
                message = await asyncio.wait_for(connection.recv(), timeout=10)
            except asyncio.TimeoutError as exc:
                raise AssertionError(f"timed out waiting for the speed={speed} response") from exc
            if isinstance(message, (SpeakV2ConfigureSuccess, SpeakV2ConfigureFailure)):
                return message
            if getattr(message, "type", None) == "Error":
                raise AssertionError(f"speed={speed} returned an unexpected error: {message}")


async def main() -> None:
    load_dotenv()
    if not os.environ.get("DEEPGRAM_API_KEY"):
        print("SKIP: DEEPGRAM_API_KEY not set")
        return

    environment = _client_environment()
    print(f"Testing {environment.production}/v2/speak with model={MODEL}")
    client = AsyncDeepgramClient(environment=environment)

    for speed in ACCEPTED_SPEEDS:
        response = await _configure_speed(client, speed)
        assert isinstance(response, SpeakV2ConfigureSuccess), f"speed={speed} should be accepted: {response}"
        assert response.applied.speed == speed, f"speed={speed} was applied as {response.applied.speed}"
        print(f"  PASS: speed={speed} accepted")
    for speed, expected_code in REJECTED_SPEEDS:
        response = await _configure_speed(client, speed)
        assert isinstance(response, SpeakV2ConfigureFailure), f"speed={speed} should be rejected: {response}"
        assert response.code == expected_code, f"speed={speed} returned {response.code}, expected {expected_code}"
        assert response.field == "speed", f"speed={speed} failure named field={response.field!r}"
        assert response.value == speed, f"speed={speed} failure echoed value={response.value}"
        print(f"  PASS: speed={speed} rejected with {expected_code}")

    print("Speed boundary matrix completed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
