"""Regression coverage for response fields added by the 2026-08-18 regen.

The models use UncheckedBaseModel with skip_validation, so response parsing is lenient:
if a future spec change drops one of these fields the attribute silently becomes None
and nothing fails. That is exactly how the `stt_latency` break shipped (deepgram-docs
PR #1006), and why tests/custom/test_latency_report_stt_compat.py exists. These tests
are the same guard for this cycle's new fields:

  - ListenV1Response/ResultsMetadata.diarize_info  (model_uuid, arch)
  - words item .speaker / .speaker_confidence
   - ListenV2TurnInfo.trigger
   - Listen V1 Nova-3 multilingual language result fields

The diarize fixtures are real payloads captured from the live API (POST /v1/listen
with diarize=true). The multilingual fixtures represent the streaming and
pre-recorded response shapes; the absent cases verify backward compatibility when
optional fields are omitted.
"""

from deepgram.listen.v1.types.listen_v1results import ListenV1Results
from deepgram.listen.v1.types.listen_v1results_metadata import ListenV1ResultsMetadata
from deepgram.listen.v1.types.listen_v1results_metadata_diarize_info import (
    ListenV1ResultsMetadataDiarizeInfo,
)
from deepgram.listen.v2.types.listen_v2turn_info import ListenV2TurnInfo
from deepgram.types.listen_v1response import ListenV1Response
from deepgram.types.listen_v1response_metadata import ListenV1ResponseMetadata
from deepgram.types.listen_v1response_metadata_diarize_info import (
    ListenV1ResponseMetadataDiarizeInfo,
)
from deepgram.types.listen_v1response_results_channels_item_alternatives_item_words_item import (
    ListenV1ResponseResultsChannelsItemAlternativesItemWordsItem,
)

# Observed live: metadata.diarize_info on a diarize=true pre-recorded request.
DIARIZE_INFO = {"model_uuid": "a9f85c2b-5afb-4b9d-b49b-492c43a01cfb", "arch": "v1"}

# Real POST /v1/listen response metadata (nova-3, diarize=true).
RESPONSE_METADATA = {
    "transaction_key": "deprecated",
    "request_id": "01a0159c-6f81-7fe3-ac3a-c03fcfbb3516",
    "sha256": "154e291ecfa8be6ab8343560bcc109008fa7853eb5372533e8efdefc9b504c33",
    "created": "2026-08-18T16:02:57.468000+00:00",
    "duration": 25.933313,
    "channels": 1,
    "models": ["2187e11a-3532-4498-b076-81fa530bdd49"],
    "model_info": {
        "2187e11a-3532-4498-b076-81fa530bdd49": {
            "name": "general-nova-3",
            "version": "2025-07-31.0",
            "arch": "nova-3",
        }
    },
    "diarize_info": DIARIZE_INFO,
}

# Streaming-side twin; model_info is a typed object here, not a dict of objects.
RESULTS_METADATA = {
    "request_id": "01a0159c-6f81-7fe3-ac3a-c03fcfbb3516",
    "model_uuid": "2187e11a-3532-4498-b076-81fa530bdd49",
    "model_info": {"name": "general-nova-3", "version": "2025-07-31.0", "arch": "nova-3"},
    "diarize_info": DIARIZE_INFO,
}

# Real word from the same response.
WORD = {
    "word": "yeah",
    "start": 0.0,
    "end": 0.48,
    "confidence": 0.99592924,
    "speaker": 0,
    "speaker_confidence": 1.0,
    "punctuated_word": "Yeah.",
}

STREAMING_MULTILINGUAL_RESULT = {
    "type": "Results",
    "channel_index": [0, 1],
    "duration": 1.2,
    "start": 0.0,
    "is_final": True,
    "speech_final": True,
    "channel": {
        "alternatives": [
            {
                "transcript": "hello hola",
                "confidence": 0.99,
                "languages": ["en", "es"],
                "languages_hinted": ["en", "es"],
                "words": [
                    {"word": "hello", "start": 0.0, "end": 0.4, "confidence": 0.99, "language": "en"},
                    {"word": "hola", "start": 0.5, "end": 0.9, "confidence": 0.99, "language": "es"},
                ],
            }
        ]
    },
    "metadata": RESULTS_METADATA,
}

PRERECORDED_MULTILINGUAL_RESPONSE = {
    "metadata": RESPONSE_METADATA,
    "results": {
        "channels": [
            {
                "alternatives": [
                    {
                        "transcript": "hello hola",
                        "confidence": 0.99,
                        "languages": ["en", "es"],
                        "languages_hinted": ["en", "es"],
                        "words": [
                            {
                                "word": "hello",
                                "start": 0.0,
                                "end": 0.4,
                                "confidence": 0.99,
                                "language": "en",
                            }
                        ],
                    }
                ]
            }
        ],
        "utterances": [
            {
                "start": 0.0,
                "end": 0.9,
                "confidence": 0.99,
                "channel": 0,
                "transcript": "hello hola",
                "languages": ["en", "es"],
                "words": [
                    {
                        "word": "hola",
                        "start": 0.5,
                        "end": 0.9,
                        "confidence": 0.99,
                        "language": "es",
                    }
                ],
            }
        ],
    },
}


class TestListenV1DiarizeInfo:
    def test_response_metadata_parses_diarize_info(self) -> None:
        md = ListenV1ResponseMetadata.model_validate(RESPONSE_METADATA)
        assert md.diarize_info is not None
        assert md.diarize_info.model_uuid == "a9f85c2b-5afb-4b9d-b49b-492c43a01cfb"
        assert md.diarize_info.arch == "v1"

    def test_results_metadata_parses_diarize_info(self) -> None:
        md = ListenV1ResultsMetadata.model_validate(RESULTS_METADATA)
        assert md.diarize_info is not None
        assert md.diarize_info.model_uuid == "a9f85c2b-5afb-4b9d-b49b-492c43a01cfb"
        assert md.diarize_info.arch == "v1"

    def test_diarize_info_absent_when_diarization_not_run(self) -> None:
        """Live behaviour: the key is omitted entirely when diarize is off."""
        without = {k: v for k, v in RESPONSE_METADATA.items() if k != "diarize_info"}
        assert ListenV1ResponseMetadata.model_validate(without).diarize_info is None

    def test_diarize_info_types_are_constructible(self) -> None:
        for cls in (ListenV1ResponseMetadataDiarizeInfo, ListenV1ResultsMetadataDiarizeInfo):
            info = cls.model_validate(DIARIZE_INFO)
            assert info.model_uuid == "a9f85c2b-5afb-4b9d-b49b-492c43a01cfb"
            assert info.arch == "v1"


class TestListenV1WordSpeakerFields:
    def test_word_parses_speaker_and_speaker_confidence(self) -> None:
        word = ListenV1ResponseResultsChannelsItemAlternativesItemWordsItem.model_validate(WORD)
        assert word.speaker == 0
        assert word.speaker_confidence == 1.0

    def test_speaker_fields_absent_without_diarization(self) -> None:
        """Live behaviour: keys are ['confidence', 'end', 'start', 'word'] with diarize off."""
        plain = {k: v for k, v in WORD.items() if k not in ("speaker", "speaker_confidence")}
        word = ListenV1ResponseResultsChannelsItemAlternativesItemWordsItem.model_validate(plain)
        assert word.speaker is None
        assert word.speaker_confidence is None

    def test_speaker_zero_is_preserved(self) -> None:
        """Speaker 0 is a real speaker; a falsy-check bug would drop it."""
        word = ListenV1ResponseResultsChannelsItemAlternativesItemWordsItem.model_validate(
            {**WORD, "speaker": 0, "speaker_confidence": 0.0}
        )
        assert word.speaker == 0
        assert word.speaker_confidence == 0.0


class TestListenV1MultilingualFields:
    def test_streaming_result_parses_languages_and_word_languages(self) -> None:
        result = ListenV1Results.model_validate(STREAMING_MULTILINGUAL_RESULT)
        alternative = result.channel.alternatives[0]

        assert alternative.languages == ["en", "es"]
        assert alternative.languages_hinted == ["en", "es"]
        assert [word.language for word in alternative.words] == ["en", "es"]

    def test_prerecorded_response_parses_alternative_and_utterance_languages(self) -> None:
        response = ListenV1Response.model_validate(PRERECORDED_MULTILINGUAL_RESPONSE)
        alternative = response.results.channels[0].alternatives[0]
        utterance = response.results.utterances[0]

        assert alternative.languages == ["en", "es"]
        assert alternative.languages_hinted == ["en", "es"]
        assert alternative.words[0].language == "en"
        assert utterance.languages == ["en", "es"]
        assert utterance.words[0].language == "es"

    def test_multilingual_fields_remain_optional_when_omitted(self) -> None:
        stream = ListenV1Results.model_validate(
            {
                **STREAMING_MULTILINGUAL_RESULT,
                "channel": {
                    "alternatives": [
                        {
                            "transcript": "hello",
                            "confidence": 0.99,
                            "words": [
                                {"word": "hello", "start": 0.0, "end": 0.4, "confidence": 0.99}
                            ],
                        }
                    ]
                },
            }
        )
        prerecorded = ListenV1Response.model_validate(
            {
                **PRERECORDED_MULTILINGUAL_RESPONSE,
                "results": {
                    "channels": [{"alternatives": [{"transcript": "hello", "confidence": 0.99}]}],
                    "utterances": [{"transcript": "hello", "words": [{"word": "hello"}]}],
                },
            }
        )

        stream_alternative = stream.channel.alternatives[0]
        prerecorded_alternative = prerecorded.results.channels[0].alternatives[0]
        utterance = prerecorded.results.utterances[0]
        assert stream_alternative.languages is None
        assert stream_alternative.languages_hinted is None
        assert stream_alternative.words[0].language is None
        assert prerecorded_alternative.languages is None
        assert prerecorded_alternative.languages_hinted is None
        assert utterance.languages is None
        assert utterance.words[0].language is None


class TestListenV2TurnInfoTrigger:
    BASE = {
        "type": "TurnInfo",
        "request_id": "01a01588-b48d-7c82-84ad-e0a091c9d5bd",
        "sequence_id": 13,
        "event": "EndOfTurn",
        "turn_index": 0,
        "audio_window_start": 0.0,
        "audio_window_end": 3.0,
        "transcript": "yeah as much as",
        "words": [{"word": "yeah", "confidence": 0.99}],
        "end_of_turn_confidence": 0.92,
    }

    def test_trigger_parses_documented_values(self) -> None:
        for value in ("model", "manual", "timeout"):
            info = ListenV2TurnInfo.model_validate({**self.BASE, "trigger": value})
            assert info.trigger == value

    def test_trigger_tolerates_unknown_values(self) -> None:
        """Documented as an open enum -- new server values must not raise."""
        info = ListenV2TurnInfo.model_validate({**self.BASE, "trigger": "some_future_cause"})
        assert info.trigger == "some_future_cause"

    def test_trigger_absent_parses_as_none(self) -> None:
        """The optional field remains backward-compatible when omitted."""
        assert ListenV2TurnInfo.model_validate(self.BASE).trigger is None
