# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List, Optional, Dict

# Result Message


@dataclass_json
@dataclass
class Word:
    word: Optional[str]
    start: Optional[float]
    end: Optional[float]
    confidence: Optional[float]
    punctuated_word: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Alternative:
    transcript: Optional[str]
    confidence: Optional[float]
    words: Optional[List[Word]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [Word.from_dict(project) for project in _dict["words"]]
        return _dict[key]


@dataclass_json
@dataclass
class Channel:
    alternatives: Optional[List[Alternative]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["alternatives"] is not None:
            _dict["alternatives"] = [
                Alternative.from_dict(project) for project in _dict["alternatives"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class ModelInfo:
    name: Optional[str]
    version: Optional[str]
    arch: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Metadata:
    request_id: Optional[str]
    model_info: Optional[ModelInfo]
    model_uuid: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["model_info"] is not None:
            _dict["model_info"] = [
                ModelInfo.from_dict(project) for project in _dict["model_info"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class LiveResultResponse:
    type: Optional[str]
    channel_index: Optional[List[int]]
    duration: Optional[float]
    start: Optional[float]
    is_final: Optional[bool]
    speech_final: Optional[bool]
    channel: Optional[Channel]
    metadata: Optional[Metadata]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["channel"] is not None:
            _dict["channel"] = [
                Channel.from_dict(project) for project in _dict["channel"]
            ]
        if _dict["metadata"] is not None:
            _dict["metadata"] = [
                Metadata.from_dict(project) for project in _dict["metadata"]
            ]
        return _dict[key]


# Metadata Message


@dataclass_json
@dataclass
class ModelInfo:
    name: Optional[str]
    version: Optional[str]
    arch: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class MetadataResponse:
    type: Optional[str]
    transaction_key: Optional[str]
    request_id: Optional[str]
    sha256: Optional[str]
    created: Optional[str]
    duration: Optional[float]
    channels: Optional[int]
    models: Optional[List[str]]
    model_info: Optional[Dict[str, ModelInfo]]

    def __init__(
        self,
        type: str,
        transaction_key: str,
        request_id: str,
        sha256: str,
        created: datetime,
        duration: float,
        channels: int,
        models: List[str],
        model_info: Dict[str, ModelInfo],
    ) -> None:
        self.type = type
        self.transaction_key = transaction_key
        self.request_id = request_id
        self.sha256 = sha256
        self.created = created
        self.duration = duration
        self.channels = channels
        self.models = models
        self.model_info = model_info

    def __getitem__(self, key):
        _dict = self.to_dict()
        # TODO: fix this
        # if _dict["model_info"] is not None:
        #     _dict["model_info"] = [ModelInfo.from_dict(value) for value in _dict["model_info"]]
        return _dict[key]


# Error Message


@dataclass_json
@dataclass
class ErrorResponse:
    description: Optional[str]
    message: Optional[str]
    type: Optional[str]
    variant: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]
