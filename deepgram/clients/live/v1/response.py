# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
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
    speaker: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

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

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "words" in _dict:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Channel:
    alternatives: Optional[List[Alternative]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "alternatives" in _dict:
            _dict["alternatives"] = [
                Alternative.from_dict(alternatives)
                for alternatives in _dict["alternatives"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

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

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Metadata:
    request_id: Optional[str] = ""
    model_info: Optional[ModelInfo] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model_uuid: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info) for model_info in _dict["model_info"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


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
    channel: Optional[Channel] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    metadata: Optional[Metadata] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "channel" in _dict:
            _dict["channel"] = [
                Channel.from_dict(channel) for channel in _dict["channel"]
            ]
        if "metadata" in _dict:
            _dict["metadata"] = [
                Metadata.from_dict(metadata) for metadata in _dict["metadata"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


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
    models: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model_info: Optional[Dict[str, ModelInfo]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    extra: Optional[Dict] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "models" in _dict:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        if "extra" in _dict:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Speech Started Message


@dataclass_json
@dataclass
class SpeechStartedResponse:
    """
    SpeechStartedResponse Message from the Deepgram Platform
    """

    type: Optional[str] = ""
    channel: Optional[List[int]] = None
    timestamp: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


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

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
