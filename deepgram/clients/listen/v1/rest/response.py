# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

from ....common import Sentiment


# Base Classes:


@dataclass
class BaseResponse(DataClassJsonMixin):
    """
    BaseResponse class used to define the common methods and properties for all response classes.
    """

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)

    def eval(self, key: str) -> str:
        """
        This method is used to evaluate a key in the response object using a dot notation style method.
        """
        keys = key.split(".")
        result: Dict[Any, Any] = self.to_dict()
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            elif isinstance(result, list) and k.isdigit() and int(k) < len(result):
                result = result[int(k)]
            else:
                return ""
        return str(result)


# Async Prerecorded Response Types:


@dataclass
class AsyncPrerecordedResponse(BaseResponse):
    """
    The response object for the async prerecorded API.
    """

    request_id: str = ""


# Prerecorded Response Types:


@dataclass
class SummaryInfo(BaseResponse):
    """
    The summary information for the response.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    model_uuid: str = ""


@dataclass
class ModelInfo(BaseResponse):
    """
    The model information for the response.
    """

    name: str = ""
    version: str = ""
    arch: str = ""


@dataclass
class IntentsInfo(BaseResponse):
    """
    The intents information for the response.
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class SentimentInfo(BaseResponse):
    """
    The sentiment information for the response.
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class TopicsInfo(BaseResponse):
    """
    The topics information for the response.
    """

    model_uuid: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


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
class Hit(BaseResponse):
    """
    The hit information for the response.
    """

    confidence: float = 0
    start: float = 0
    end: float = 0
    snippet: Optional[str] = ""


@dataclass
class Word(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    The word information for the response.
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
    speaker_confidence: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[Sentiment] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment_score: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
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
class Warning(
    DataClassJsonMixin
):  # pylint: disable=used-before-assignment,redefined-builtin
    """
    The warning information for the response.
    """

    parameter: str = ""
    type: str = ""
    message: str = ""


@dataclass
class Search(BaseResponse):
    """
    The search information for the response.
    """

    query: str = ""
    hits: List[Hit] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "hits" in _dict:
            _dict["hits"] = [Hit.from_dict(hits) for hits in _dict["hits"]]
        return _dict[key]


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
class Alternative(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    The alternative information for the response.
    """

    transcript: str = ""
    confidence: float = 0
    words: List[Word] = field(default_factory=list)
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
    languages: Optional[List[str]] = field(
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
class Channel(BaseResponse):
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
class Intent(BaseResponse):
    """
    The intent information for the response.
    """

    intent: str = ""
    confidence_score: float = 0


@dataclass
class Average(BaseResponse):
    """
    The average information for the response.
    """

    sentiment: Sentiment
    sentiment_score: float

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "sentiment" in _dict:
            _dict["sentiment"] = Sentiment.from_dict(_dict["sentiment"])
        return _dict[key]


@dataclass
class Topic(BaseResponse):
    """
    The topic information for the response.
    """

    topic: str = ""
    confidence_score: float = 0


@dataclass
class Segment(BaseResponse):
    """
    The segment information for the response.
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
            _dict["intents"] = [
                Intent.from_dict(intents) for intents in _dict["intents"]
            ]
        if "topics" in _dict:
            _dict["topics"] = [Topic.from_dict(topics) for topics in _dict["topics"]]
        return _dict[key]


@dataclass
class Sentiments(BaseResponse):
    """
    The sentiments information for the response.
    """

    segments: Optional[List[Segment]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    average: Optional[Average] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

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
    The topics information for the response.
    """

    segments: Optional[List[Segment]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

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
    The intents information for the response.
    """

    segments: Optional[List[Segment]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "segments" in _dict:
            _dict["segments"] = [
                Segment.from_dict(segments) for segments in _dict["segments"]
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
