# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional, TypedDict, Dict

# Async Prerecorded Response Types:


@dataclass_json
@dataclass
class AsyncPrerecordedResponse:
    request_id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


# Prerecorded Response Types:


@dataclass_json
@dataclass
class SummaryInfo:
    input_tokens: Optional[int] = 0
    output_tokens: Optional[int] = 0
    model_uuid: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
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
    transaction_key: Optional[str] = ""
    request_id: Optional[str] = ""
    sha256: Optional[str] = ""
    created: Optional[str] = ""
    duration: Optional[float] = 0
    channels: Optional[int] = 0
    models: Optional[List[str]] = None
    warnings: Optional[List[Warning]] = None
    model_info: Optional[Dict[str, ModelInfo]] = None
    summary_info: Optional[SummaryInfo] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["models"] is not None:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if _dict["model_info"] is not None:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info) for model_info in _dict["model_info"]
            ]
        if _dict["summary_info"] is not None:
            _dict["summary_info"] = SummaryInfo.from_dict(_dict["summary_info"])
        if _dict["warnings"] is not None:
            _dict["warnings"] = [
                Warning.from_dict(warning) for warning in _dict["warnings"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class SummaryV2:
    summary: Optional[str] = ""
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Summaries(SummaryV2):  # internal reference to old name
    summary: Optional[str] = ""
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Summary:
    result: Optional[str] = ""
    short: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Summary(Summary):  # internal reference to old name
    result: Optional[str] = ""
    short: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Hit:
    confidence: Optional[float] = 0
    start: Optional[float] = 0
    end: Optional[float] = 0
    snippet: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Word:
    word: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    punctuated_word: Optional[str] = ""
    speaker: Optional[int] = 0
    speaker_confidence: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Sentence:
    text: Optional[str] = ""
    start: Optional[float] = 0
    end: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Paragraph:
    sentences: Optional[List[Sentence]] = None
    start: Optional[float] = 0
    end: Optional[float] = 0
    num_words: Optional[float] = 0
    speaker: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["sentences"] is not None:
            _dict["sentences"] = [
                Sentence.from_dict(sentences) for sentences in _dict["sentences"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Paragraphs:
    transcript: Optional[str] = ""
    paragraphs: Optional[List[Paragraph]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["paragraphs"] is not None:
            _dict["paragraphs"] = [
                Paragraph.from_dict(paragraphs) for paragraphs in _dict["paragraphs"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Topic:
    topic: Optional[str] = ""
    confidence: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Topics:
    topics: Optional[List[Topic]] = None
    text: Optional[str] = ""
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["topics"] is not None:
            _dict["topics"] = [Topic.from_dict(topics) for topics in _dict["topics"]]
        return _dict[key]


@dataclass_json
@dataclass
class Translation:
    language: Optional[str] = ""
    translation: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Warning:
    parameter: Optional[str] = ""
    type: Optional[str] = ""
    message: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Search:
    query: Optional[str] = ""
    hits: Optional[List[Hit]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["hits"] is not None:
            _dict["hits"] = [Hit.from_dict(hits) for hits in _dict["hits"]]
        return _dict[key]


@dataclass_json
@dataclass
class Utterance:
    start: Optional[float] = 0
    end: Optional[float] = 0
    confidence: Optional[float] = 0
    channel: Optional[int] = 0
    transcript: Optional[str] = ""
    words: Optional[List[Word]] = None
    speaker: Optional[int] = 0
    id: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        return _dict[key]


@dataclass_json
@dataclass
class Entity:
    label: Optional[str] = ""
    value: Optional[str] = ""
    confidence: Optional[float] = 0
    start_word: Optional[float] = 0
    end_word: Optional[float] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Alternative:
    transcript: Optional[str] = ""
    confidence: Optional[float] = 0
    words: Optional[List[Word]] = None
    summaries: Optional[List[SummaryV2]] = None
    paragraphs: Optional[Paragraphs] = None
    entities: Optional[List[Entity]] = None
    translations: Optional[List[Translation]] = None
    topics: Optional[List[Topics]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["words"] is not None:
            _dict["words"] = [Word.from_dict(words) for words in _dict["words"]]
        if _dict["summaries"] is not None:
            _dict["summaries"] = [
                SummaryV2.from_dict(summaries) for summaries in _dict["summaries"]
            ]
        if _dict["paragraphs"] is not None:
            _dict["paragraphs"] = Paragraphs.from_dict(_dict["paragraphs"])
        if _dict["entities"] is not None:
            _dict["entities"] = [
                Entity.from_dict(entities) for entities in _dict["entities"]
            ]
        if _dict["translations"] is not None:
            _dict["translations"] = [
                Translation.from_dict(translations)
                for translations in _dict["translations"]
            ]
        if _dict["topics"] is not None:
            _dict["topics"] = [Topics.from_dict(topics) for topics in _dict["topics"]]
        return _dict[key]


@dataclass_json
@dataclass
class Channel:
    search: Optional[List[Search]] = None
    alternatives: Optional[List[Alternative]] = None
    detected_language: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["search"] is not None:
            _dict["search"] = [Search.from_dict(search) for search in _dict["search"]]
        if _dict["alternatives"] is not None:
            _dict["alternatives"] = [
                Alternative.from_dict(alternatives)
                for alternatives in _dict["alternatives"]
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Result:
    channels: Optional[List[Channel]] = None
    utterances: Optional[List[Utterance]] = None
    summary: Optional[Summary] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["channels"] is not None:
            _dict["channels"] = [
                Channel.from_dict(channels) for channels in _dict["channels"]
            ]
        if _dict["utterances"] is not None:
            _dict["utterances"] = [
                Utterance.from_dict(utterances) for utterances in _dict["utterances"]
            ]
        if _dict["summary"] is not None:
            _dict["summary"] = Summary.from_dict(_dict["summary"])
        return _dict[key]


# Prerecorded Response Result:


@dataclass_json
@dataclass
class PrerecordedResponse:
    metadata: Optional[Metadata] = None
    results: Optional[Result] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["metadata"] is not None:
            _dict["metadata"] = Metadata.from_dict(_dict["metadata"])
        if _dict["results"] is not None:
            _dict["results"] = Result.from_dict(_dict["results"])
        return _dict[key]
