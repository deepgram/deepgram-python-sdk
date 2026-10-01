"""Compatibility coverage for the v7 direct Topics and Intents response shape."""

import httpx
import respx

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.environment import DeepgramClientEnvironment
from deepgram.requests import (
    SharedIntentsParams,
    SharedIntentsResultsIntentsParams,
    SharedIntentsResultsParams,
    SharedTopicsParams,
    SharedTopicsResultsParams,
    SharedTopicsResultsTopicsParams,
)
from deepgram.types import (
    SharedIntents,
    SharedIntentsResults,
    SharedIntentsResultsIntents,
    SharedTopics,
    SharedTopicsResults,
    SharedTopicsResultsTopics,
)

HOST = "compat.deepgram.test"
ENVIRONMENT = DeepgramClientEnvironment(
    base=f"https://{HOST}", production=f"wss://{HOST}", agent=f"wss://{HOST}", agent_rest=f"https://{HOST}"
)
TOPICS = {"segments": [{"text": "hello", "start_word": 0.0, "end_word": 0.5, "topics": [{"topic": "greeting", "confidence_score": 0.9}]}]}
INTENTS = {"segments": [{"text": "hello", "start_word": 0.0, "end_word": 0.5, "intents": [{"intent": "greet", "confidence_score": 0.8}]}]}
LISTEN_RESPONSE = {
    "metadata": {"request_id": "request", "sha256": "hash", "created": "2026-10-01T00:00:00Z", "duration": 0.5, "channels": 1, "models": ["nova-3"], "model_info": {}},
    "results": {"channels": [], "topics": TOPICS, "intents": INTENTS},
}
READ_RESPONSE = {"metadata": {}, "results": {"topics": TOPICS, "intents": INTENTS}}


def _assert_paths(response) -> None:
    assert response.results.topics.segments[0].topics[0].topic == "greeting"
    assert response.results.intents.segments[0].intents[0].intent == "greet"
    assert response.results.topics.results.topics.segments[0].topics[0].topic == "greeting"
    assert response.results.intents.results.intents.segments[0].intents[0].intent == "greet"


def _assert_legacy_construction_and_params() -> None:
    legacy_topics: SharedTopicsParams = {"results": {"topics": TOPICS}}
    legacy_intents: SharedIntentsParams = {"results": {"intents": INTENTS}}
    topics = SharedTopics(results=legacy_topics["results"])
    intents = SharedIntents(results=legacy_intents["results"])

    assert topics.segments[0].topics[0].topic == "greeting"
    assert topics.results.topics.segments[0].topics[0].topic == "greeting"
    assert intents.segments[0].intents[0].intent == "greet"
    assert intents.results.intents.segments[0].intents[0].intent == "greet"

    direct_topics = SharedTopics(segments=TOPICS["segments"], results={"topics": {"segments": []}})
    direct_intents = SharedIntents(segments=INTENTS["segments"], results={"intents": {"segments": []}})
    assert direct_topics.results.topics.segments[0].topics[0].topic == "greeting"
    assert direct_intents.results.intents.segments[0].intents[0].intent == "greet"


def test_sync_listen_and_read_preserve_direct_and_legacy_topics_intents_paths() -> None:
    with respx.mock:
        respx.post(f"https://{HOST}/v1/listen").mock(return_value=httpx.Response(200, json=LISTEN_RESPONSE))
        respx.post(f"https://{HOST}/v1/read").mock(return_value=httpx.Response(200, json=READ_RESPONSE))
        client = DeepgramClient(environment=ENVIRONMENT, api_key="test")
        _assert_paths(client.listen.v1.media.transcribe_url(url="https://example.test/audio.wav", topics=True, intents=True))
        _assert_paths(client.read.v1.text.analyze(request={"text": "hello"}, topics=True, intents=True))
    _assert_legacy_construction_and_params()


async def test_async_listen_and_read_preserve_direct_and_legacy_topics_intents_paths() -> None:
    with respx.mock:
        respx.post(f"https://{HOST}/v1/listen").mock(return_value=httpx.Response(200, json=LISTEN_RESPONSE))
        respx.post(f"https://{HOST}/v1/read").mock(return_value=httpx.Response(200, json=READ_RESPONSE))
        client = AsyncDeepgramClient(environment=ENVIRONMENT, api_key="test", httpx_client=httpx.AsyncClient())
        _assert_paths(await client.listen.v1.media.transcribe_url(url="https://example.test/audio.wav", topics=True, intents=True))
        _assert_paths(await client.read.v1.text.analyze(request={"text": "hello"}, topics=True, intents=True))
    _assert_legacy_construction_and_params()


def test_legacy_topics_and_intents_types_and_params_are_importable() -> None:
    assert SharedTopicsResults(topics=SharedTopicsResultsTopics(segments=[])).topics.segments == []
    assert SharedIntentsResults(intents=SharedIntentsResultsIntents(segments=[])).intents.segments == []
    topics: SharedTopicsResultsParams = {"topics": {"segments": []}}
    intents: SharedIntentsResultsParams = {"intents": {"segments": []}}
    topic_segments: SharedTopicsResultsTopicsParams = {"segments": []}
    intent_segments: SharedIntentsResultsIntentsParams = {"segments": []}
    assert topics["topics"] == topic_segments
    assert intents["intents"] == intent_segments


def test_empty_legacy_topics_and_intents_results_remain_none() -> None:
    assert SharedTopics().results is None
    assert SharedIntents().results is None
    assert SharedTopics(results=None).results is None
    assert SharedIntents(results=None).results is None
