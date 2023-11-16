# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, TypedDict, Dict

# Async Prerecorded Response Types:

class AsyncPrerecordedResponse(TypedDict):
    request_id: str

# Sync Prerecorded Response Types:

class Metadata(TypedDict):
    transaction_key: str
    request_id: str
    sha256: str
    created: str
    duration: float
    channels: int
    models: List[str]
    model_info: Dict[str, 'ModelInfo']
    warnings: Optional[List['Warning']]

class ModelInfo(TypedDict):
    name: str
    version: str
    arch: str

class Summary(TypedDict):
    summary: Optional[str]
    start_word: Optional[float]
    end_word: Optional[float]

class TranscriptionSummary(TypedDict):
    result: str
    short: str

class Hit(TypedDict):
    confidence: float
    start: float
    end: float
    snippet: str

class WordBase(TypedDict):
    word: str
    start: float
    end: float
    confidence: float
    punctuated_word: Optional[str]
    speaker: Optional[int]
    speaker_confidence: Optional[float]

class Sentence(TypedDict):
    text: str
    start: float
    end: float

class Paragraph(TypedDict):
    sentences: List[Sentence]
    start: float
    end: float
    num_words: float

class ParagraphGroup(TypedDict):
    transcript: str
    paragraphs: List[Paragraph]

class Topic(TypedDict):
    topic: str
    confidence: float

class TopicGroup(TypedDict):
    topics: List[Topic]
    text: str
    start_word: float
    end_word: float

class Translation(TypedDict):
    language: str
    translation: str

class Warning(TypedDict):
    parameter: str
    type: str
    message: str

class Search(TypedDict):
    query: str
    hits: List[Hit]

class Utterance(TypedDict):
    start: float
    end: float
    confidence: float
    channel: int
    transcript: str
    words: List[WordBase]
    speaker: Optional[int]
    id: str

class Entity(TypedDict):
    label: str
    value: str
    confidence: float
    start_word: float
    end_word: float

class Alternative(TypedDict):
    transcript: str
    confidence: float
    words: List[WordBase]
    summaries: Optional[List[Summary]]
    paragraphs: Optional[ParagraphGroup]
    entities: Optional[List[Entity]]
    translations: Optional[List[Translation]]
    topics: Optional[List[TopicGroup]]

class Channel(TypedDict):
    search: Optional[List[Search]]
    alternatives: List[Alternative]
    detected_language: Optional[str]

class Result(TypedDict):
    channels: List[Channel]
    utterances: Optional[List[Utterance]]
    summary: Optional[TranscriptionSummary]

class SyncPrerecordedResponse(TypedDict):
    metadata: Metadata
    results: Result
