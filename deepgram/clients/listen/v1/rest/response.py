# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

# between analyze and listen
from ....common import (
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

# between rest and websocket
from ....common import (
    ModelInfo,
    Alternative,
    Channel,
    Hit,
    Search,
    Word,
)

# Async Prerecorded Response Types:


@dataclass
class AsyncPrerecordedResponse(BaseResponse):
    """
    The response object for the async prerecorded API.
    """

    request_id: str = ""


# Prerecorded Response Types:

ModelInfo = ModelInfo
Alternative = Alternative
Channel = Channel
Hit = Hit
Search = Search
Word = Word


@dataclass
class Metadata(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    The metadata for the response.
    """

    transaction_key: str = ""
    request_id: str = ""
    sha256: str = ""
    created: str = ""
    duration: float = 0
    channels: int = 0
    models: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    # pylint: disable=used-before-assignment
    warnings: Optional[List[Warning]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    # pylint: enable=used-before-assignment
    model_info: Optional[Dict[str, ModelInfo]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summary_info: Optional[SummaryInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents_info: Optional[IntentsInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_info: Optional[SentimentInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics_info: Optional[TopicsInfo] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    extra: Optional[Dict] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class SummaryV1(BaseResponse):
    """
    The summary information for the response.
    """

    summary: str = ""
    start_word: float = 0
    end_word: float = 0


Summaries = SummaryV1


@dataclass
class SummaryV2(BaseResponse):
    """
    The summary information for the response.
    """

    result: str = ""
    short: str = ""


Summary = SummaryV2


@dataclass
class ListenRestWord(Word):  # pylint: disable=too-many-instance-attributes
    """
    The word information for the response.
    """

    speaker_confidence: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]


@dataclass
class Sentence(BaseResponse):
    """
    The sentence information for the response.
    """

    text: str = ""
    start: float = 0
    end: float = 0
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]


@dataclass
class Paragraph(BaseResponse):
    """
    The paragraph information for the response.
    """

    sentences: List[Sentence] = field(default_factory=list)
    start: float = 0
    end: float = 0
    num_words: int = 0
    speaker: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class Paragraphs(BaseResponse):
    """
    The paragraphs information for the response.
    """

    transcript: Optional[str] = ""
    paragraphs: Optional[List[Paragraph]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "paragraphs" in _dict:
            _dict["paragraphs"] = [
                Paragraph.from_dict(paragraphs) for paragraphs in _dict["paragraphs"]
            ]
        return _dict[key]


@dataclass
class Translation(BaseResponse):
    """
    The translation information for the response.
    """

    language: Optional[str] = ""
    translation: Optional[str] = ""


@dataclass
class Warning(BaseResponse):  # pylint: disable=used-before-assignment,redefined-builtin
    """
    The warning information for the response.
    """

    parameter: str = ""
    type: str = ""
    message: str = ""


@dataclass
class Utterance(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    The utterance information for the response.
    """

    start: float = 0
    end: float = 0
    confidence: float = 0
    channel: int = 0
    transcript: str = ""
    words: List[Word] = field(default_factory=list)
    speaker: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "words" in _dict:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]


@dataclass
class Entity(BaseResponse):
    """
    The entity information for the response.
    """

    label: str = ""
    value: str = ""
    confidence: float = 0
    start_word: float = 0
    end_word: float = 0


@dataclass
class ListenRESTAlternative(
    Alternative
):  # pylint: disable=too-many-instance-attributes
    """
    The alternative information for the response.
    """

    summaries: Optional[List[SummaryV1]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    paragraphs: Optional[Paragraphs] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    entities: Optional[List[Entity]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    translations: Optional[List[Translation]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class ListenRESTChannel(Channel):
    """
    The channel information for the response.
    """

    search: Optional[List[Search]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    alternatives: List[Alternative] = field(default_factory=list)
    detected_language: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language_confidence: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

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


@dataclass
class Results(BaseResponse):
    """
    The results information for the response.
    """

    channels: Optional[List[Channel]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utterances: Optional[List[Utterance]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summary: Optional[SummaryV2] = field(
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


# Prerecorded Response Result:


@dataclass
class PrerecordedResponse(BaseResponse):
    """
    The response object for the prerecorded API.
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


SyncPrerecordedResponse = PrerecordedResponse
