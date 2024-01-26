# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, Optional, TypedDict, Dict
from ..enums import Sentiment

# Async Prerecorded Response Types:


@dataclass_json
@dataclass
class AsyncPrerecordedResponse:
    request_id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


# Prerecorded Response Types:


@dataclass_json
@dataclass
class SummaryInfo:
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0
    model_uuid: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class ModelInfo:
    name: Optional[str] = ""
    version: Optional[str] = ""
    arch: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class IntentsInfo:
    model_uuid: Optional[str] = ""
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class SentimentInfo:
    model_uuid: Optional[str] = 0
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class TopicsInfo:
    model_uuid: Optional[str] = ""
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Metadata:
    transaction_key: Optional[str] = ""
    request_id: Optional[str] = ""
    sha256: Optional[str] = ""
    created: Optional[str] = ""
    duration: Optional[float] = 0
    channels: Optional[int] = 0
    models: Optional[List[str]] = None
    warnings: Optional[List[Warning]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model_info: Optional[Dict[str, ModelInfo]] = None
    summary_info: Optional[SummaryInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    intents_info: Optional[IntentsInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_info: Optional[SentimentInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics_info: Optional[TopicsInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    extra: Optional[Dict[str, str]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["models"] is not None:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if _dict["warnings"] is not None:
            _dict["warnings"] = [
                Warning.from_dict(warnings) for _, warnings in _dict["warnings"].items()
            ]
        if _dict["model_info"] is not None:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        if _dict["summary_info"] is not None:
            _dict["summary_info"] = SummaryInfo.from_dict(_dict["summary_info"])
        if _dict["intents_info"] is not None:
            _dict["intents_info"] = IntentsInfo.from_dict(_dict["intents_info"])
        if _dict["sentiment_info"] is not None:
            _dict["sentiment_info"] = SentimentInfo.from_dict(_dict["sentiment_info"])
        if _dict["topics_info"] is not None:
            _dict["topics_info"] = TopicsInfo.from_dict(_dict["topics_info"])
        if _dict["extra"] is not None:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
        return _dict[key]


@dataclass_json
@dataclass
class SummaryV1:
    summary: Optional[str] = ""
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Summaries(SummaryV1):  # internal reference to old name
    pass


@dataclass_json
@dataclass
class SummaryV2:
    result: Optional[str] = ""
    short: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Summary(SummaryV2):  # internal reference to old name
    pass


@dataclass_json
@dataclass
class Hit:
    confidence: Optional[float] = 0
    start: Optional[float] = 0
    end: Optional[float] = 0
    snippet: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Word:
    word: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    punctuated_word: Optional[str] = ""
    speaker: Optional[int] = 0
    speaker_confidence: Optional[float] = 0
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Sentence:
    text: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Paragraph:
    sentences: Optional[List[Sentence]] = None
    start: Optional[float] = 0
    end: Optional[float] = 0
    num_words: Optional[float] = 0
    speaker: Optional[int] = 0
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["sentences"] is not None:
            _dict["sentences"] = [
                Sentence.from_dict(sentences)
                for _, sentences in _dict["sentences"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Paragraphs:
    transcript: Optional[str] = ""
    paragraphs: Optional[List[Paragraph]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["paragraphs"] is not None:
            _dict["paragraphs"] = [
                Paragraph.from_dict(paragraphs)
                for _, paragraphs in _dict["paragraphs"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Translation:
    language: Optional[str] = ""
    translation: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Warning:
    parameter: Optional[str] = ""
    type: Optional[str] = ""
    message: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Search:
    query: Optional[str] = ""
    hits: Optional[List[Hit]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["hits"] is not None:
            _dict["hits"] = [Hit.from_dict(hits) for _, hits in _dict["hits"].items()]
        return _dict[key]


@dataclass_json
@dataclass
class Utterance:
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    channel: Optional[int] = 0
    transcript: Optional[str] = ""
    words: Optional[List[Word]] = None
    speaker: Optional[int] = 0
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = 0
    id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [
                Word.from_dict(words) for _, words in _dict["words"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Entity:
    label: Optional[str] = ""
    value: Optional[str] = ""
    confidence: Optional[float] = 0
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Alternative:
    transcript: Optional[str] = ""
    confidence: Optional[float] = 0
    words: Optional[List[Word]] = None
    summaries: Optional[List[SummaryV1]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    paragraphs: Optional[Paragraphs] = None
    entities: Optional[List[Entity]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    translations: Optional[List[Translation]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [
                Word.from_dict(words) for _, words in _dict["words"].items()
            ]
        if _dict["summaries"] is not None:
            _dict["summaries"] = [
                SummaryV1.from_dict(summaries)
                for _, summaries in _dict["summaries"].items()
            ]
        if _dict["paragraphs"] is not None:
            _dict["paragraphs"] = Paragraphs.from_dict(_dict["paragraphs"])
        if _dict["entities"] is not None:
            _dict["entities"] = [
                Entity.from_dict(entities) for _, entities in _dict["entities"].items()
            ]
        if _dict["translations"] is not None:
            _dict["translations"] = [
                Translation.from_dict(translations)
                for _, translations in _dict["translations"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Channel:
    search: Optional[List[Search]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    alternatives: Optional[List[Alternative]] = None
    detected_language: Optional[str] = ""
    language_confidence: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["search"] is not None:
            _dict["search"] = [
                Search.from_dict(search) for _, search in _dict["search"].items()
            ]
        if _dict["alternatives"] is not None:
            _dict["alternatives"] = [
                Alternative.from_dict(alternatives)
                for _, alternatives in _dict["alternatives"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Intent:
    intent: Optional[str] = ""
    confidence_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Average:
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Topic:
    topic: Optional[str] = ""
    confidence_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Segment:
    text: Optional[str] = ""
    start_word: Optional[int] = 0
    end_word: Optional[int] = 0
    sentiment: Optional[Sentiment] = ""
    sentiment_score: Optional[float] = 0
    intents: Optional[List[Intent]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics: Optional[List[Topic]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["intents"] is not None:
            _dict["intents"] = Intent.from_dict(_dict["intents"])
        if _dict["topics"] is not None:
            _dict["topics"] = Topic.from_dict(_dict["topics"])
        return _dict[key]


@dataclass_json
@dataclass
class Sentiments:
    segments: Optional[List[Segment]] = None
    average: Optional[Average] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["segments"] is not None:
            _dict["segments"] = [
                Segment.from_dict(segments) for _, segments in _dict["segments"].items()
            ]
        if _dict["average"] is not None:
            _dict["average"] = Average.from_dict(_dict["average"])
        return _dict[key]


@dataclass_json
@dataclass
class Topics:
    segments: Optional[List[Segment]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["segments"] is not None:
            _dict["segments"] = [
                Segment.from_dict(segments) for _, segments in _dict["segments"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Intents:
    segments: Optional[List[Segment]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["segments"] is not None:
            _dict["segments"] = [
                Segment.from_dict(segments) for _, segments in _dict["segments"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Results:
    channels: Optional[List[Channel]] = None
    utterances: Optional[List[Utterance]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    summary: Optional[SummaryV2] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiments: Optional[Sentiments] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics: Optional[Topics] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    intents: Optional[Intents] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["channels"] is not None:
            _dict["channels"] = [
                Channel.from_dict(channels) for _, channels in _dict["channels"].items()
            ]
        if _dict["utterances"] is not None:
            _dict["utterances"] = [
                Utterance.from_dict(utterances)
                for _, utterances in _dict["utterances"].items()
            ]
        if _dict["summary"] is not None:
            _dict["summary"] = SummaryV2.from_dict(_dict["summary"])
        if _dict["sentiments"] is not None:
            _dict["sentiments"] = Sentiments.from_dict(_dict["sentiments"])
        if _dict["topics"] is not None:
            _dict["topics"] = Topics.from_dict(_dict["topics"])
        if _dict["intents"] is not None:
            _dict["intents"] = Intents.from_dict(_dict["intents"])
        return _dict[key]


# Prerecorded Response Result:


@dataclass_json
@dataclass
class PrerecordedResponse:
    metadata: Optional[Metadata] = None
    results: Optional[Results] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["metadata"] is not None:
            _dict["metadata"] = Metadata.from_dict(_dict["metadata"])
        if _dict["results"] is not None:
            _dict["results"] = Results.from_dict(_dict["results"])
        return _dict[key]


@dataclass_json
@dataclass
class SyncPrerecordedResponse(PrerecordedResponse):
    pass
