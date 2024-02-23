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

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class ModelInfo:
    name: Optional[str] = ""
    version: Optional[str] = ""
    arch: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class IntentsInfo:
    model_uuid: Optional[str] = ""
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class SentimentInfo:
    model_uuid: Optional[str] = 0
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class TopicsInfo:
    model_uuid: Optional[str] = ""
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Metadata:
    transaction_key: Optional[str] = ""
    request_id: Optional[str] = ""
    sha256: Optional[str] = ""
    created: Optional[str] = ""
    duration: Optional[float] = 0
    channels: Optional[int] = 0
    models: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    warnings: Optional[List[Warning]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model_info: Optional[Dict[str, ModelInfo]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
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
    extra: Optional[Dict] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "models" in _dict:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if "warnings" in _dict:
            _dict["warnings"] = [
                Warning.from_dict(warnings) for warnings in _dict["warnings"]
            ]
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        if "summary_info" in _dict:
            _dict["summary_info"] = SummaryInfo.from_dict(_dict["summary_info"])
        if "intents_info" in _dict:
            _dict["intents_info"] = IntentsInfo.from_dict(_dict["intents_info"])
        if "sentiment_info" in _dict:
            _dict["sentiment_info"] = SentimentInfo.from_dict(_dict["sentiment_info"])
        if "topics_info" in _dict:
            _dict["topics_info"] = TopicsInfo.from_dict(_dict["topics_info"])
        if "extra" in _dict:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class SummaryV1:
    summary: Optional[str] = ""
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Word:
    word: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    punctuated_word: Optional[str] = ""
    speaker: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    speaker_confidence: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Sentence:
    text: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Paragraph:
    sentences: Optional[List[Sentence]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    start: Optional[float] = 0
    end: Optional[float] = 0
    num_words: Optional[float] = 0
    speaker: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentences" in _dict:
            _dict["sentences"] = [
                Sentence.from_dict(sentences) for sentences in _dict["sentences"]
            ]
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Paragraphs:
    transcript: Optional[str] = ""
    paragraphs: Optional[List[Paragraph]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "paragraphs" in _dict:
            _dict["paragraphs"] = [
                Paragraph.from_dict(paragraphs) for paragraphs in _dict["paragraphs"]
            ]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Translation:
    language: Optional[str] = ""
    translation: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Warning:
    parameter: Optional[str] = ""
    type: Optional[str] = ""
    message: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Search:
    query: Optional[str] = ""
    hits: Optional[List[Hit]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "hits" in _dict:
            _dict["hits"] = [Hit.from_dict(hits) for hits in _dict["hits"]]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Utterance:
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    channel: Optional[int] = 0
    transcript: Optional[str] = ""
    words: Optional[List[Word]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    speaker: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "words" in _dict:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Alternative:
    transcript: Optional[str] = ""
    confidence: Optional[float] = 0
    words: Optional[List[Word]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    summaries: Optional[List[SummaryV1]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    paragraphs: Optional[Paragraphs] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    entities: Optional[List[Entity]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    translations: Optional[List[Translation]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "words" in _dict:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        if "summaries" in _dict:
            _dict["summaries"] = [
                SummaryV1.from_dict(summaries) for summaries in _dict["summaries"]
            ]
        if "paragraphs" in _dict:
            _dict["paragraphs"] = Paragraphs.from_dict(_dict["paragraphs"])
        if "entities" in _dict:
            _dict["entities"] = [
                Entity.from_dict(entities) for entities in _dict["entities"]
            ]
        if "translations" in _dict:
            _dict["translations"] = [
                Translation.from_dict(translations)
                for translations in _dict["translations"]
            ]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Channel:
    search: Optional[List[Search]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    alternatives: Optional[List[Alternative]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    detected_language: Optional[str] = ""
    language_confidence: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "search" in _dict:
            _dict["search"] = [Search.from_dict(search) for search in _dict["search"]]
        if "alternatives" in _dict:
            _dict["alternatives"] = [
                Alternative.from_dict(alternatives)
                for alternatives in _dict["alternatives"]
            ]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Intent:
    intent: Optional[str] = ""
    confidence_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Average:
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Topic:
    topic: Optional[str] = ""
    confidence_score: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Segment:
    text: Optional[str] = ""
    start_word: Optional[int] = 0
    end_word: Optional[int] = 0
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    intents: Optional[List[Intent]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics: Optional[List[Topic]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        if "intents" in _dict:
            _dict["intents"] = [
                Intent.from_dict(intents) for intents in _dict["intents"]
            ]
        if "topics" in _dict:
            _dict["topics"] = [Topic.from_dict(topics) for topics in _dict["topics"]]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Sentiments:
    segments: Optional[List[Segment]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    average: Optional[Average] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        if "average" in _dict:
            _dict["average"] = Average.from_dict(_dict["average"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Topics:
    segments: Optional[List[Segment]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Intents:
    segments: Optional[List[Segment]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Results:
    channels: Optional[List[Channel]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
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
        if "channels" in _dict:
            _dict["channels"] = [
                Channel.from_dict(channels) for channels in _dict["channels"]
            ]
        if "utterances" in _dict:
            _dict["utterances"] = [
                Utterance.from_dict(utterances) for utterances in _dict["utterances"]
            ]
        if "summary" in _dict:
            _dict["summary"] = SummaryV2.from_dict(_dict["summary"])
        if "sentiments" in _dict:
            _dict["sentiments"] = Sentiments.from_dict(_dict["sentiments"])
        if "topics" in _dict:
            _dict["topics"] = Topics.from_dict(_dict["topics"])
        if "intents" in _dict:
            _dict["intents"] = Intents.from_dict(_dict["intents"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Prerecorded Response Result:


@dataclass_json
@dataclass
class PrerecordedResponse:
    metadata: Optional[Metadata] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    results: Optional[Results] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "metadata" in _dict:
            _dict["metadata"] = Metadata.from_dict(_dict["metadata"])
        if "results" in _dict:
            _dict["results"] = Results.from_dict(_dict["results"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class SyncPrerecordedResponse(PrerecordedResponse):
    pass
