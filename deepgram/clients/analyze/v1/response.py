# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, Optional, TypedDict, Dict
from ..enums import Sentiment


# Async Analyze Response Types:


@dataclass_json
@dataclass
class AsyncAnalyzeResponse:
    request_id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Analyze Response Types:


@dataclass_json
@dataclass
class IntentsInfo:
    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class SentimentInfo:
    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class SummaryInfo:
    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class TopicsInfo:
    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Metadata:
    request_id: str = ""
    created: str = ""
    language: str = ""
    intents_info: Optional[IntentsInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_info: Optional[SentimentInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    summary_info: Optional[SummaryInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics_info: Optional[TopicsInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "intents_info" in _dict:
            _dict["intents_info"] = IntentsInfo.from_dict(_dict["intents_info"])
        if "sentiment_info" in _dict:
            _dict["sentiment_info"] = SentimentInfo.from_dict(_dict["sentiment_info"])
        if "summary_info" in _dict:
            _dict["summary_info"] = SummaryInfo.from_dict(_dict["summary_info"])
        if "topics_info" in _dict:
            _dict["topics_info"] = TopicsInfo.from_dict(_dict["topics_info"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Average:
    sentiment: Sentiment = None
    sentiment_score: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Summary:
    text: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Topic:
    topic: str = ""
    confidence_score: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Intent:
    intent: str = ""
    confidence_score: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Segment:
    text: str = ""
    start_word: int = 0
    end_word: int = 0
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = 0
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
            _dict["intents"] = Intent.from_dict(_dict["intents"])
        if "topics" in _dict:
            _dict["topics"] = Topic.from_dict(_dict["topics"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Sentiments:
    segments: List[Segment] = None
    average: Average = None

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
    segments: List[Segment] = None

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
    segments: List[Segment] = None

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
    summary: Optional[Summary] = field(
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
        if "summary" in _dict:
            _dict["summary"] = Summary.from_dict(_dict["summary"])
        if "sentiments" in _dict:
            _dict["sentiments"] = Sentiments.from_dict(_dict["sentiments"])
        if "topics" in _dict:
            _dict["topics"] = Topics.from_dict(_dict["topics"])
        if "intents" in _dict:
            _dict["intents"] = Intents.from_dict(_dict["intents"])
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Analyze Response Result:


@dataclass_json
@dataclass
class AnalyzeResponse:
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
class SyncAnalyzeResponse(AnalyzeResponse):
    pass
