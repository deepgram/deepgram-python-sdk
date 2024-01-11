# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional, TypedDict, Dict
from ..enums import Sentiment


# Async Analyze Response Types:


@dataclass_json
@dataclass
class AsyncAnalyzeResponse:
    request_id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


# Analyze Response Types:


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
    model_uuid: Optional[str] = ""
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class SummaryInfo:
    model_uuid: Optional[str] = ""
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
    request_id: Optional[str] = ""
    created: Optional[str] = ""
    language: Optional[str] = ""
    intents_info: Optional[IntentsInfo] = None
    sentiment_info: Optional[SentimentInfo] = None
    summary_info: Optional[SummaryInfo] = None
    topics_info: Optional[TopicsInfo] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["intents_info"] is not None:
            _dict["intents_info"] = IntentsInfo.from_dict(_dict["intents_info"])
        if _dict["sentiment_info"] is not None:
            _dict["sentiment_info"] = SentimentInfo.from_dict(_dict["sentiment_info"])
        if _dict["summary_info"] is not None:
            _dict["summary_info"] = SummaryInfo.from_dict(_dict["summary_info"])
        if _dict["topics_info"] is not None:
            _dict["topics_info"] = TopicsInfo.from_dict(_dict["topics_info"])
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
class Summary:
    text: Optional[str] = ""

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
class Intent:
    intent: Optional[str] = ""
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
    intents: Optional[List[Intent]] = None
    topics: Optional[List[Topic]] = None

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
    summary: Optional[Summary] = None
    sentiments: Optional[Sentiments] = None
    topics: Optional[Topics] = None
    intents: Optional[Intents] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["summary"] is not None:
            _dict["summary"] = Summary.from_dict(_dict["summary"])
        if _dict["sentiments"] is not None:
            _dict["sentiments"] = Sentiments.from_dict(_dict["sentiments"])
        if _dict["topics"] is not None:
            _dict["topics"] = Topics.from_dict(_dict["topics"])
        if _dict["intents"] is not None:
            _dict["intents"] = Intents.from_dict(_dict["intents"])
        return _dict[key]


# Analyze Response Result:


@dataclass_json
@dataclass
class AnalyzeResponse:
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
class SyncAnalyzeResponse(AnalyzeResponse):
    pass
