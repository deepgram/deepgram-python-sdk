"""
Forward-feature coverage for the Flux end-of-turn tuning fields added in the
2026-07-08 regen: ``eot_threshold``, ``eager_eot_threshold`` (floats) and
``eot_timeout_ms`` (int). These are real wire fields and MUST serialize.

Covered on all three listen-provider models that carry them — the top-level
``DeepgramListenProviderV2`` plus the two Voice Agent listen-provider variants —
with kwargs and dict, asserting the values land on the wire and are omitted when
absent. The frozen ``language_hint`` back-compat shim on these same models must
not interfere (see test_language_hint_compat.py).
"""

from deepgram.agent.v1.types.agent_v1settings_agent_context_listen_provider import (
    AgentV1SettingsAgentContextListenProvider_V2,
)
from deepgram.agent.v1.types.agent_v1settings_agent_listen_provider import (
    AgentV1SettingsAgentListenProvider_V2,
)
from deepgram.core.pydantic_utilities import IS_PYDANTIC_V2
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2


def _from_dict(cls, payload):
    return cls.model_validate(payload) if IS_PYDANTIC_V2 else cls.parse_obj(payload)


class TestEotThresholdsProvider:
    """DeepgramListenProviderV2 — the top-level Flux STT provider."""

    def test_all_three_serialize(self):
        dumped = DeepgramListenProviderV2(
            model="flux-general-en",
            eot_threshold=0.7,
            eager_eot_threshold=0.4,
            eot_timeout_ms=5000,
        ).dict()
        assert dumped["eot_threshold"] == 0.7
        assert dumped["eager_eot_threshold"] == 0.4
        assert dumped["eot_timeout_ms"] == 5000

    def test_from_dict(self):
        provider = _from_dict(
            DeepgramListenProviderV2,
            {"model": "flux-general-en", "eot_threshold": 0.65, "eot_timeout_ms": 4000},
        )
        assert provider.eot_threshold == 0.65
        assert provider.eot_timeout_ms == 4000

    def test_omitted_when_absent(self):
        dumped = DeepgramListenProviderV2(model="flux-general-en").dict()
        assert dumped.get("eot_threshold") is None
        assert dumped.get("eager_eot_threshold") is None
        assert dumped.get("eot_timeout_ms") is None


class TestEotThresholdsAgentProviders:
    """The two Voice Agent listen-provider V2 variants carry the same fields."""

    def test_context_listen_provider_serializes(self):
        dumped = AgentV1SettingsAgentContextListenProvider_V2(
            model="flux-general-en", eot_threshold=0.8, eot_timeout_ms=6000
        ).dict()
        assert dumped["eot_threshold"] == 0.8
        assert dumped["eot_timeout_ms"] == 6000

    def test_agent_listen_provider_serializes(self):
        dumped = AgentV1SettingsAgentListenProvider_V2(
            model="flux-general-en", eager_eot_threshold=0.35
        ).dict()
        assert dumped["eager_eot_threshold"] == 0.35
