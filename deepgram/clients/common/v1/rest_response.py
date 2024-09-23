# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from .enums import Sentiment
from .shared_response import BaseResponse


# Analyze Response Types:


@dataclass
class IntentsInfo(BaseResponse):
    """
    Intents Info
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class SentimentInfo(BaseResponse):
    """
    Sentiment Info
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class SummaryInfo(BaseResponse):
    """
    Summary Info
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class TopicsInfo(BaseResponse):
    """
    Topics Info
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class Average(BaseResponse):
    """
    Average
    """

    sentiment: Sentiment
    sentiment_score: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]


@dataclass
class Topic(BaseResponse):
    """
    Topic
    """

    topic: str = ""
    confidence_score: float = 0


@dataclass
class Intent(BaseResponse):
    """
    Intent
    """

    intent: str = ""
    confidence_score: float = 0


@dataclass
class Segment(BaseResponse):
    """
    Segment
    """

    text: str = ""
    start_word: int = 0
    end_word: int = 0
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents: Optional[List[Intent]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics: Optional[List[Topic]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class Sentiments(BaseResponse):
    """
    Sentiments
    """

    average: Average
    segments: List[Segment] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        if "average" in _dict:
            _dict["average"] = Average.from_dict(_dict["average"])
        return _dict[key]


@dataclass
class Topics(BaseResponse):
    """
    Topics
    """

    segments: List[Segment] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        return _dict[key]


@dataclass
class Intents(BaseResponse):
    """
    Intents
    """

    segments: List[Segment] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
            ]
        return _dict[key]
