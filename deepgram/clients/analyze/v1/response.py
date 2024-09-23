# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from ...common import (
    BaseResponse,
    Average,
    Intent,
    Intents,
    IntentsInfo,
    Segment,
    SentimentInfo,
    Sentiment,
    Sentiments,
    SummaryInfo,
    Topic,
    Topics,
    TopicsInfo,
)


# Async Analyze Response Types:


@dataclass
class AsyncAnalyzeResponse(BaseResponse):
    """
    Async Analyze Response
    """

    request_id: str = ""


# Analyze Response Types:


@dataclass
class Metadata(BaseResponse):
    """
    Metadata
    """

    request_id: str = ""
    created: str = ""
    language: str = ""
    intents_info: Optional[IntentsInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_info: Optional[SentimentInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summary_info: Optional[SummaryInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics_info: Optional[TopicsInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class Summary(BaseResponse):
    """
    Summary
    """

    text: str = ""


@dataclass
class Results(BaseResponse):
    """
    Results
    """

    summary: Optional[Summary] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiments: Optional[Sentiments] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics: Optional[Topics] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents: Optional[Intents] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


# Analyze Response Result:


@dataclass
class AnalyzeResponse(BaseResponse):
    """
    Analyze Response
    """

    metadata: Optional[Metadata] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    results: Optional[Results] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "metadata" in _dict:
            _dict["metadata"] = Metadata.from_dict(_dict["metadata"])
        if "results" in _dict:
            _dict["results"] = Results.from_dict(_dict["results"])
        return _dict[key]


SyncAnalyzeResponse = AnalyzeResponse
