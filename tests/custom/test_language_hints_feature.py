"""
Forward-feature coverage for ``language_hints`` (the current, correct field) —
distinct from the deprecated ``language_hint`` back-compat shim covered in
``test_language_hint_compat.py``.

Unlike ``language_hint`` (which is ``exclude=True`` and never serialized),
``language_hints`` is a real wire field and MUST serialize. Covered here on the
Flux STT reconfigure control message (``ListenV2Configure``, client-sent) and
the Voice Agent listen provider, with single and multiple codes, via kwargs and
dict, asserting the value lands on the wire.
"""

from deepgram.core.pydantic_utilities import IS_PYDANTIC_V2
from deepgram.listen.v2.types.listen_v2configure import ListenV2Configure
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2


def _from_dict(cls, payload):
    return cls.model_validate(payload) if IS_PYDANTIC_V2 else cls.parse_obj(payload)


class TestLanguageHintsFluxConfigure:
    """ListenV2Configure — Flux STT mid-stream reconfigure message (client-sent)."""

    def test_multiple_codes_serialize_on_the_wire(self):
        dumped = ListenV2Configure(language_hints=["en", "es", "fr"]).dict()
        assert dumped["language_hints"] == ["en", "es", "fr"]

    def test_single_code(self):
        assert ListenV2Configure(language_hints=["en"]).dict()["language_hints"] == ["en"]

    def test_from_dict(self):
        cfg = _from_dict(ListenV2Configure, {"language_hints": ["en", "es"]})
        assert cfg.language_hints == ["en", "es"]

    def test_omitted_when_absent(self):
        assert ListenV2Configure().dict().get("language_hints") is None


class TestLanguageHintsProviderForward:
    """DeepgramListenProviderV2 — ``language_hints`` (plural) is the real wire field."""

    def test_multiple_codes_serialize(self):
        dumped = DeepgramListenProviderV2(model="flux-general-multi", language_hints=["en", "es", "fr"]).dict()
        assert dumped["language_hints"] == ["en", "es", "fr"]

    def test_from_dict(self):
        provider = _from_dict(
            DeepgramListenProviderV2,
            {"model": "flux-general-multi", "language_hints": ["en", "es"]},
        )
        assert provider.language_hints == ["en", "es"]
