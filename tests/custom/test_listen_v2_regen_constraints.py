"""
Coverage for V2 / Flux listen constraints introduced or corrected in the regen.

  * TurnInfo word ``start`` / ``end`` are OPTIONAL — the API models them as
    ``Option<f32>`` (it may omit them on some words/paths), so the SDK must
    accept a word with neither. Modelling them as required would mis-type
    omitted timings on a response model.
  * ``ListenV2CloseStreamType`` is the corrected single value ``"CloseStream"``
    — the v2 spec wrongly copied v1's ``Finalize`` / ``CloseStream`` /
    ``KeepAlive`` control-message enum; only ``"CloseStream"`` is valid for a
    CloseStream message.
  * v2 ``profanity_filter`` is exposed (``"true"`` / ``"false"``).
"""

import typing

from deepgram.listen.v2.types.listen_v2close_stream import ListenV2CloseStream
from deepgram.listen.v2.types.listen_v2close_stream_type import ListenV2CloseStreamType
from deepgram.listen.v2.types.listen_v2turn_info_words_item import ListenV2TurnInfoWordsItem
from deepgram.types.listen_v2profanity_filter import ListenV2ProfanityFilter


class TestWordTimingsOptional:
    def test_word_without_timings_is_valid(self):
        # The server may omit start/end; a word with neither must validate.
        word = ListenV2TurnInfoWordsItem(word="hello", confidence=0.99)
        assert word.start is None
        assert word.end is None

    def test_word_without_timings_from_dict(self):
        word = ListenV2TurnInfoWordsItem.model_validate({"word": "hello", "confidence": 0.99}) \
            if hasattr(ListenV2TurnInfoWordsItem, "model_validate") \
            else ListenV2TurnInfoWordsItem.parse_obj({"word": "hello", "confidence": 0.99})
        assert word.start is None and word.end is None

    def test_word_with_timings(self):
        word = ListenV2TurnInfoWordsItem(word="hello", confidence=0.99, start=0.0, end=0.42)
        assert word.start == 0.0
        assert word.end == 0.42


class TestCloseStreamTypeShim:
    def test_only_close_stream_value(self):
        # The shim narrows the type to the single valid literal; the bogus
        # Finalize / KeepAlive values (copied from v1) are gone.
        assert typing.get_args(ListenV2CloseStreamType) == ("CloseStream",)

    def test_close_stream_message_default_and_roundtrip(self):
        assert ListenV2CloseStream().dict().get("type") == "CloseStream"
        assert ListenV2CloseStream(type="CloseStream").dict().get("type") == "CloseStream"


class TestProfanityFilterV2:
    def test_literal_values(self):
        # Union[Literal["true", "false"], Any] — assert the documented literals.
        literal = typing.get_args(ListenV2ProfanityFilter)[0]
        assert set(typing.get_args(literal)) == {"true", "false"}
