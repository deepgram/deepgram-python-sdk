"""
Coverage for assorted helpers: the query encoder, the custom client
constructors (access token / session id / transport factory / log redaction),
and the TTS ``TextBuilder``/SSML helpers.
"""

import typing

import pytest

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.query_encoder import encode_query, single_query_encoder, traverse_query_dict
from deepgram.environment import DeepgramClientEnvironment
from deepgram.helpers.text_builder import (
    TextBuilder,
    add_pronunciation,
    ssml_to_deepgram,
    validate_ipa,
    validate_pause,
)

BASE = "https://test.deepgram.local"


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


# --------------------------------------------------------------------------- #
# query_encoder
# --------------------------------------------------------------------------- #
def test_encode_query_none_and_empty() -> None:
    assert encode_query(None) is None
    assert encode_query({}) == []


def test_query_encoder_shapes() -> None:
    # bool coercion to lowercase
    assert ("flag", "true") in encode_query({"flag": True})
    assert ("flag", "false") in encode_query({"flag": False})
    # nested dict flattening
    assert ("a[b]", 1) in traverse_query_dict({"a": {"b": 1}})
    # list of scalars and list of dicts
    assert single_query_encoder("k", [1, 2]) == [("k", 1), ("k", 2)]
    assert single_query_encoder("k", [{"x": 1}]) == [("k[x]", 1)]
    # plain scalar
    assert single_query_encoder("k", "v") == [("k", "v")]


# --------------------------------------------------------------------------- #
# custom client constructors
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("client_cls", [DeepgramClient, AsyncDeepgramClient])
def test_client_with_access_token_and_session_id(client_cls: typing.Any) -> None:
    client = client_cls(environment=_environment(), access_token="my-token", session_id="sid-123")
    assert client.session_id == "sid-123"


@pytest.mark.parametrize("client_cls", [DeepgramClient, AsyncDeepgramClient])
def test_client_generates_session_id_and_opts_out_of_redaction(client_cls: typing.Any) -> None:
    client = client_cls(environment=_environment(), api_key="k", redact_credentials_in_logs=False)
    assert client.session_id  # auto-generated UUID


@pytest.mark.parametrize("client_cls", [DeepgramClient, AsyncDeepgramClient])
def test_client_with_transport_factory_disables_reconnect(client_cls: typing.Any) -> None:
    from deepgram.transport import restore_transport

    def _factory(url: str, headers: typing.Dict[str, str]) -> typing.Any:  # pragma: no cover - not invoked
        raise NotImplementedError

    try:
        client = client_cls(environment=_environment(), api_key="k", transport_factory=_factory)
        assert client.reconnect is False
    finally:
        # Transport patching is global; undo it so it does not leak into other tests.
        restore_transport()


# --------------------------------------------------------------------------- #
# text_builder / SSML helpers
# --------------------------------------------------------------------------- #
def test_text_builder_fluent_build() -> None:
    text = (
        TextBuilder()
        .text("Take ")
        .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
        .pause(500)
        .text(" daily.")
        .build()
    )
    assert "pronounce" in text and "{pause:500}" in text


def test_text_builder_validation_errors() -> None:
    with pytest.raises(ValueError):
        TextBuilder().pronunciation("w", 'has"quote')  # invalid IPA char
    with pytest.raises(ValueError):
        TextBuilder().pause(123)  # not a 100ms increment


def test_validate_ipa_and_pause() -> None:
    assert validate_ipa("")[0] is False
    assert validate_ipa('a"b')[0] is False
    assert validate_ipa("x" * 101)[0] is False
    assert validate_ipa("ˈtest")[0] is True
    assert validate_pause(400)[0] is False
    assert validate_pause(6000)[0] is False
    assert validate_pause(550)[0] is False  # not 100ms increment
    assert validate_pause(500)[0] is True


def test_add_pronunciation_and_ssml() -> None:
    out = add_pronunciation("Take azathioprine daily", "azathioprine", "ˌæzəˈθaɪəpriːn")
    assert "pronounce" in out
    with pytest.raises(ValueError):
        add_pronunciation("x", "x", 'bad"ipa')

    ssml = '<speak>Take <phoneme alphabet="ipa" ph="ˌæz">azathioprine</phoneme> <break time="0.5s"/> now</speak>'
    converted = ssml_to_deepgram(ssml)
    assert "pronounce" in converted and "{pause:500}" in converted

    # break in milliseconds + an out-of-range value that gets rounded to a valid one
    rounded = ssml_to_deepgram('Wait <break time="123ms"/> here')
    assert "{pause:" in rounded


def test_text_builder_from_ssml_updates_counts() -> None:
    builder = TextBuilder().from_ssml('Hi <break time="500ms"/> there')
    assert "{pause:500}" in builder.build()
