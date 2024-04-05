# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from datetime import datetime
from typing import List, Optional, Dict

# Result Message


@dataclass_json
@dataclass
class OpenResponse:
    """
    Open Message from the Deepgram Platform
    """

    type: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Word:
    word: str = ""
    start: float = 0
    end: float = 0
    confidence: float = 0
    punctuated_word: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
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
    transcript: str = ""
    confidence: float = 0
    words: List[Word] = None

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
    alternatives: List[Alternative] = None

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
    name: str = ""
    version: str = ""
    arch: str = ""

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
    request_id: str = ""
    model_info: ModelInfo = None
    model_uuid: str = ""
    extra: Optional[Dict[str, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info) for model_info in _dict["model_info"]
            ]
        if "extra" in _dict:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
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

    type: str = ""
    channel_index: List[int] = None
    duration: float = 0
    start: float = 0
    is_final: bool = False
    speech_final: bool = False
    channel: Channel = None
    metadata: Metadata = None

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
    name: str = ""
    version: str = ""
    arch: str = ""

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

    type: str = ""
    transaction_key: str = ""
    request_id: str = ""
    sha256: str = ""
    created: str = ""
    duration: float = 0
    channels: int = 0
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

    type: str = ""
    channel: List[int] = None
    timestamp: float = 0

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

    type: str = ""
    channel: List[int] = None
    last_word_end: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Close Message


@dataclass_json
@dataclass
class CloseResponse:
    """
    Close Message from the Deepgram Platform
    """

    type: str = ""

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

    description: str = ""
    message: str = ""
    type: str = ""
    variant: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Unhandled Message


@dataclass_json
@dataclass
class UnhandledResponse:
    """
    Unhandled Message from the Deepgram Platform
    """

    type: str = ""
    raw: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
