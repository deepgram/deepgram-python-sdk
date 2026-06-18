"""
Backward-compatibility coverage for the ``language_hint`` -> ``language_hints``
rename on the V2 Deepgram listen provider (Voice Agent settings).

Context: the public field was historically (and incorrectly) named
``language_hint`` and accepted a ``str`` or a ``list``. The API field is
``language_hints`` (a list), and the server rejects unknown fields
(``deny_unknown_fields``), so the legacy singular field never worked
end-to-end. The SDK now:

  * declares ``language_hints: Optional[List[str]]`` (the real field),
  * keeps a deprecated ``language_hint: Optional[Union[str, List[str]]]`` field
    (``exclude=True``) so legacy call sites still type-check, and
  * a ``model_validator(mode="before")`` remaps ``language_hint`` ->
    ``language_hints`` and drops the singular key so it never reaches the wire.

These tests assert all of that, on every public surface and both construction
paths (kwargs + dict), and verify ``language_hint`` is never serialized.
"""

import pydantic
import pytest

from deepgram.agent.v1.types.agent_v1settings_agent_context_listen_provider import (
    AgentV1SettingsAgentContextListenProvider,
    AgentV1SettingsAgentContextListenProvider_V2,
)
from deepgram.agent.v1.types.agent_v1settings_agent_context_listen_provider_v2 import (
    AgentV1SettingsAgentContextListenProviderV2,
)
from deepgram.agent.v1.types.agent_v1settings_agent_listen_provider import (
    AgentV1SettingsAgentListenProvider,
    AgentV1SettingsAgentListenProvider_V2,
)

# Public renamed-alias import paths (both resolve to DeepgramListenProviderV2).
from deepgram.agent.v1.types.agent_v1settings_agent_listen_provider_v2 import (
    AgentV1SettingsAgentListenProviderV2,
)
from deepgram.core.pydantic_utilities import IS_PYDANTIC_V2
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2

# Every public surface that carries the ``language_hints`` field and the shim.
DIRECT_MODELS = [
    pytest.param(DeepgramListenProviderV2, id="DeepgramListenProviderV2"),
    pytest.param(AgentV1SettingsAgentListenProvider_V2, id="AgentListenProvider_V2"),
    pytest.param(AgentV1SettingsAgentContextListenProvider_V2, id="AgentContextListenProvider_V2"),
    pytest.param(AgentV1SettingsAgentListenProviderV2, id="AgentListenProviderV2_alias"),
    pytest.param(AgentV1SettingsAgentContextListenProviderV2, id="AgentContextListenProviderV2_alias"),
]

UNION_TYPES = [
    pytest.param(AgentV1SettingsAgentListenProvider, id="AgentListenProvider_union"),
    pytest.param(AgentV1SettingsAgentContextListenProvider, id="AgentContextListenProvider_union"),
]


def _dump(model):
    # ``.dict()`` is the method the SDK uses on the wire (the socket send path),
    # so it is the faithful check for "did language_hint leak into the payload?".
    return model.dict()


def _from_dict(cls, payload):
    return cls.model_validate(payload) if IS_PYDANTIC_V2 else cls.parse_obj(payload)


def _from_union(union_type, payload):
    if IS_PYDANTIC_V2:
        return pydantic.TypeAdapter(union_type).validate_python(payload)
    return pydantic.parse_obj_as(union_type, payload)


class TestLanguageHintMapping:
    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_singular_str_kwarg_maps_to_list(self, cls):
        dumped = _dump(cls(model="flux-general-multi", language_hint="en"))
        assert dumped.get("language_hints") == ["en"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_singular_list_kwarg_passthrough(self, cls):
        dumped = _dump(cls(model="flux-general-multi", language_hint=["en", "de"]))
        assert dumped.get("language_hints") == ["en", "de"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_singular_str_from_dict_maps(self, cls):
        # Mirrors nested construction (e.g. settings.agent.listen.provider as a dict).
        dumped = _dump(_from_dict(cls, {"model": "flux-general-multi", "language_hint": "en"}))
        assert dumped.get("language_hints") == ["en"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_singular_list_from_dict_maps(self, cls):
        dumped = _dump(_from_dict(cls, {"model": "flux-general-multi", "language_hint": ["en", "de"]}))
        assert dumped.get("language_hints") == ["en", "de"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_plural_kwarg_unchanged(self, cls):
        dumped = _dump(cls(model="flux-general-multi", language_hints=["fr"]))
        assert dumped.get("language_hints") == ["fr"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_explicit_plural_wins_over_singular(self, cls):
        dumped = _dump(cls(model="flux-general-multi", language_hint="en", language_hints=["de"]))
        assert dumped.get("language_hints") == ["de"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_neither_is_none(self, cls):
        dumped = _dump(cls(model="flux-general-multi"))
        assert dumped.get("language_hints") is None
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("cls", DIRECT_MODELS)
    def test_singular_none_is_noop(self, cls):
        dumped = _dump(cls(model="flux-general-multi", language_hint=None))
        assert dumped.get("language_hints") is None
        assert "language_hint" not in dumped


class TestLanguageHintUnionRouting:
    @pytest.mark.parametrize("union_type", UNION_TYPES)
    def test_union_routes_to_v2_and_maps(self, union_type):
        model = _from_union(
            union_type,
            {"version": "v2", "type": "deepgram", "model": "flux-general-multi", "language_hint": "en"},
        )
        dumped = model.dict()
        assert dumped.get("language_hints") == ["en"]
        assert "language_hint" not in dumped

    @pytest.mark.parametrize("union_type", UNION_TYPES)
    def test_v1_member_unaffected_by_shim(self, union_type):
        # The v1 provider uses singular ``language`` and has no language_hints;
        # routing to it must not be perturbed by the v2 shim.
        model = _from_union(
            union_type,
            {"version": "v1", "type": "deepgram", "model": "nova-3", "language": "en"},
        )
        dumped = model.dict()
        assert dumped.get("language") == "en"
        assert dumped.get("language_hints") is None
        assert "language_hint" not in dumped
