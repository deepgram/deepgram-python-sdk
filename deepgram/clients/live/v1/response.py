# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

# Result Message


@dataclass
class OpenResponse(DataClassJsonMixin):
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


@dataclass
class Word(DataClassJsonMixin):
    """
    Word object
    """

    word: str = ""
    start: float = 0
    end: float = 0
    confidence: float = 0
    punctuated_word: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    speaker: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class Alternative(DataClassJsonMixin):
    """
    Alternative object
    """

    transcript: str = ""
    confidence: float = 0
    words: List[Word] = field(default_factory=list)
    languages: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class Channel(DataClassJsonMixin):
    """
    Channel object
    """

    alternatives: List[Alternative] = field(default_factory=list)

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


@dataclass
class ModelInfo(DataClassJsonMixin):
    """
    ModelInfo object
    """

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


@dataclass
class Metadata(DataClassJsonMixin):
    """
    Metadata object
    """

    model_info: ModelInfo
    request_id: str = ""
    model_uuid: str = ""
    extra: Optional[Dict[str, str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class LiveResultResponse(
    DataClassJsonMixin
):  # pylint: disable=too-many-instance-attributes
    """
    Result Message from the Deepgram Platform
    """

    channel: Channel
    metadata: Metadata
    type: str = ""
    channel_index: List[int] = field(default_factory=list)
    duration: float = 0
    start: float = 0
    is_final: bool = False
    from_finalize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    speech_final: bool = False

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


@dataclass
class MetadataResponse(
    DataClassJsonMixin
):  # pylint: disable=too-many-instance-attributes
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
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    model_info: Optional[Dict[str, ModelInfo]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    extra: Optional[Dict] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class SpeechStartedResponse(DataClassJsonMixin):
    """
    SpeechStartedResponse Message from the Deepgram Platform
    """

    type: str = ""
    channel: List[int] = field(default_factory=list)
    timestamp: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Utterance End Message


@dataclass
class UtteranceEndResponse(DataClassJsonMixin):
    """
    UtteranceEnd Message from the Deepgram Platform
    """

    type: str = ""
    channel: List[int] = field(default_factory=list)
    last_word_end: float = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Close Message


@dataclass
class CloseResponse(DataClassJsonMixin):
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


@dataclass
class ErrorResponse(DataClassJsonMixin):
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


@dataclass
class UnhandledResponse(DataClassJsonMixin):
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
