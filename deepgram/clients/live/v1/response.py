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
    word: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    punctuated_word: Optional[str] = ""
    speaker: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Alternative:
    transcript: Optional[str] = ""
    confidence: Optional[float] = 0
    words: Optional[List[Word]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [
                Word.from_dict(words) for _, words in _dict["words"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Channel:
    alternatives: Optional[List[Alternative]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["alternatives"] is not None:
            _dict["alternatives"] = [
                Alternative.from_dict(alternatives)
                for _, alternatives in _dict["alternatives"].items()
            ]
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
class Metadata:
    request_id: Optional[str] = ""
    model_info: Optional[ModelInfo] = None
    model_uuid: Optional[str] = ""


    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["model_info"] is not None:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class LiveResultResponse:
    """
    Result Message from the Deepgram Platform
    """

    type: Optional[str] = ""
    channel_index: Optional[List[int]] = None
    duration: Optional[float] = 0
    start: Optional[float] = 0
    is_final: Optional[bool] = False
    speech_final: Optional[bool] = False
    channel: Optional[Channel] = None
    metadata: Optional[Metadata] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["channel"] is not None:
            _dict["channel"] = [
                Channel.from_dict(channel) for _, channel in _dict["channel"].items()
            ]
        if _dict["metadata"] is not None:
            _dict["metadata"] = [
                Metadata.from_dict(metadata)
                for _, metadata in _dict["metadata"].items()
            ]
        return _dict[key]


# Metadata Message


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
class MetadataResponse:
    """
    Metadata Message from the Deepgram Platform
    """

    type: Optional[str] = ""
    transaction_key: Optional[str] = ""
    request_id: Optional[str] = ""
    sha256: Optional[str] = ""
    created: Optional[str] = ""
    duration: Optional[float] = 0
    channels: Optional[int] = 0
    models: Optional[List[str]] = None
    model_info: Optional[Dict[str, ModelInfo]] = None
    extra: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["models"] is not None:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if _dict["model_info"] is not None:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        return _dict[key]


# Utterance End Message


@dataclass_json
@dataclass
class UtteranceEndResponse:
    """
    UtteranceEnd Message from the Deepgram Platform
    """

    type: Optional[str] = ""
    channel: Optional[List[int]] = None
    last_word_end: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


# Error Message


@dataclass_json
@dataclass
class ErrorResponse:
    """
    Error Message from the Deepgram Platform
    """

    description: Optional[str] = ""
    message: Optional[str] = ""
    type: Optional[str] = ""
    variant: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]
