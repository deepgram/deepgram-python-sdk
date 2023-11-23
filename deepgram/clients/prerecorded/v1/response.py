# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, TypedDict, Dict

# Async Prerecorded Response Types:

class AsyncPrerecordedResponse(TypedDict):
    request_id: str

# Prerecorded Response Types:

class Metadata(TypedDict):
    transaction_key: Optional[str]
    request_id: Optional[str]
    sha256: Optional[str]
    created: Optional[str]
    duration: Optional[float]
    channels: Optional[int]
    models: Optional[List[str]]
    model_info: Optional[Dict[str, 'ModelInfo']]
    summary_info: Optional[Dict[str, 'SummaryV2']]
    warnings: Optional[List['Warning']]

class ModelInfo(TypedDict):
    name: Optional[str]
    version: Optional[str]
    arch: Optional[str]

class SummaryV2(TypedDict):
    summary: Optional[str]
    start_word: Optional[float]
    end_word: Optional[float]
class Summaries(SummaryV2): # internal reference to old name
    pass

class Summary(TypedDict):
    result: Optional[str]
    short: Optional[str]
class Summary(Summary): # internal reference to old name
    pass

class Hit(TypedDict):
    confidence: Optional[float]
    start: Optional[float]
    end: Optional[float]
    snippet: Optional[str]

class Word(TypedDict):
    word: Optional[str]
    start: Optional[float]
    end: Optional[float]
    confidence: Optional[float]
    punctuated_word: Optional[str]
    speaker: Optional[int]
    speaker_confidence: Optional[float]

class Sentence(TypedDict):
    text: Optional[str]
    start: Optional[float]
    end: Optional[float]

class Paragraph(TypedDict):
    sentences: Optional[List[Sentence]]
    start: Optional[float]
    end: Optional[float]
    num_words: Optional[float]
    speaker: Optional[int]

class Paragraphs(TypedDict):
    transcript: Optional[str]
    paragraphs: Optional[List[Paragraph]]

class Topic(TypedDict):
    topic: Optional[str]
    confidence: Optional[float]

class Topics(TypedDict):
    topics: Optional[List[Topic]]
    text: Optional[str]
    start_word: Optional[float]
    end_word: Optional[float]

class Translation(TypedDict):
    language: Optional[str]
    translation: Optional[str]

class Warning(TypedDict):
    parameter: Optional[str]
    type: Optional[str]
    message: Optional[str]

class Search(TypedDict):
    query: Optional[str]
    hits: Optional[List[Hit]]

class Utterance(TypedDict):
    start: Optional[float]
    end: Optional[float]
    confidence: Optional[float]
    channel: Optional[int]
    transcript: Optional[str]
    words: Optional[List[Word]]
    speaker: Optional[int]
    id: Optional[str]

class Entity(TypedDict):
    label: Optional[str]
    value: Optional[str]
    confidence: Optional[float]
    start_word: Optional[float]
    end_word: Optional[float]

class Alternative(TypedDict):
    transcript: Optional[str]
    confidence: Optional[float]
    words: Optional[List[Word]]
    summaries: Optional[List[SummaryV2]]
    paragraphs: Optional[Paragraphs]
    entities: Optional[List[Entity]]
    translations: Optional[List[Translation]]
    topics: Optional[List[Topics]]

class Channel(TypedDict):
    search: Optional[List[Search]]
    alternatives: Optional[List[Alternative]]
    detected_language: Optional[str]

class Result(TypedDict):
    channels: Optional[List[Channel]]
    utterances: Optional[List[Utterance]]
    summary: Optional[Summary]

class PrerecordedResponse(TypedDict):
    metadata: Optional[Metadata]
    results: Optional[Result]
