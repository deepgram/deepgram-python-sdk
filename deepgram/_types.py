# We want these types to be flexible to allow for updated API responses
# or cutting-edge options to not break the client for older SDK versions;
# as such, everything is implemented using TypedDicts
# instead of, say, dataclasses.

import sys
from datetime import datetime
from typing import Optional, List, Union, Any, Dict
if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal
else:
    from typing_extensions import TypedDict, Literal
if sys.version_info >= (3, 9):
    from collections.abc import Callable, Awaitable
else:
    from typing import Callable, Awaitable


class UpdateResponse(TypedDict):
    message: str


# Transcription


class Options(TypedDict, total=False):
    api_key: str
    api_url: str  # this URL should /not/ include a trailing slash


class UrlSource(TypedDict):
    url: str


class BufferSource(TypedDict):
    buffer: bytes
    mimetype: str


TranscriptionSource = Union[UrlSource, BufferSource]


BoostedKeyword = TypedDict('BoostedKeyword', {
    'word': str,
    'boost': float,
})
Keyword = Union[str, BoostedKeyword]


class TranscriptionOptions(TypedDict, total=False):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeAudio
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeStreamingAudio
    model: str
    version: str
    language: str
    punctuate: bool
    profanity_filter: bool
    redact: List[str]
    diarize: Literal['false', 'true']
    diarize_version: str
    version: str
    multichannel: bool
    alternatives: int
    numerals: bool
    search: List[str]
    callback: str
    keywords: List[str]
    ner: str
    tier: str
    replace: str


class PrerecordedOptions(TranscriptionOptions, total=False):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeAudio
    utterances: bool
    utt_split: float
    detect_language: bool


class LiveOptions(TranscriptionOptions, total=False):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeStreamingAudio
    interim_results: bool
    endpointing: bool
    vad_turnoff: int
    encoding: str
    channels: int
    sample_rate: int


class WordBase(TypedDict):
    word: str
    start: float
    end: float
    confidence: float
    speaker: Optional[int]
    speaker_confidence: Optional[float]
    punctuated_word: Optional[str]


class Hit(TypedDict):
    confidence: float
    start: float
    end: float
    snippet: str


class Search(TypedDict):
    query: str
    hits: List[Hit]


class Alternative(TypedDict):
    transcript: str
    confidence: float
    words: List[WordBase]


class Channel(TypedDict):
    search: Optional[List[Search]]
    alternatives: List[Alternative]


class Utterance(TypedDict):
    start: float
    end: float
    confidence: float
    channel: int
    transcript: str
    words: List[WordBase]
    speaker: Optional[int]
    speaker_confidence: Optional[float]
    id: str


class Metadata(TypedDict):
    request_id: str
    transaction_key: str
    sha256: str
    created: str
    duration: float
    channels: int
    models: List[str]


TranscriptionResults = TypedDict('TranscriptionResults', {
    'channels': List[Channel],
    'utterances': Optional[List[Utterance]]
})


class PrerecordedTranscriptionResponse(TypedDict, total=False):
    request_id: str
    metadata: Metadata
    results: TranscriptionResults


StreamingMetadata = TypedDict('StreamingMetadata', {
    'request_id': str,
    'model_uuid': str,
})


class LiveTranscriptionResponse(TypedDict):
    channel_index: List[int]
    duration: float
    start: float
    is_final: bool
    speech_final: bool
    channel: Channel
    metadata: StreamingMetadata


EventHandler = Union[Callable[[Any], None], Callable[[Any], Awaitable[None]]]


# Keys


class Key(TypedDict):
    api_key_id: str
    key: Optional[str]
    comment: str
    created: datetime
    scopes: List[str]

# Members

class Member(TypedDict):
    email: str
    first_name: str
    last_name: str
    id: str
    scopes: Optional[List[str]]


class KeyBundle(TypedDict):
    api_key: Key
    member: Member


class KeyResponse(TypedDict):
    api_keys: List[KeyBundle]


# Projects


class Project(TypedDict):
    project_id: str
    name: str


class ProjectResponse(TypedDict):
    projects: List[Project]


# Usage


class UsageRequestListOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]
    page: Optional[int]
    limit: Optional[int]
    status: Literal['succeeded', 'failed']


class UsageRequestDetails(TypedDict):
    usd: float
    dutation: float
    total_audio: float
    channels: int
    streams: int
    model: str
    method: Literal['sync', 'async', 'streaming']
    tags: List[str]
    features: List[str]
    config: Dict[str, bool]  # TODO: add all possible request options


class UsageRequestDetail(TypedDict):
    details: UsageRequestDetails


class UsageRequestMessage(TypedDict):
    message: Optional[str]


class UsageCallback(TypedDict):
    code: int
    completed: str


class UsageRequest(TypedDict):
    request_id: str
    created: str
    path: str
    accessor: str
    response: Optional[Union[UsageRequestDetail, UsageRequestMessage]]
    callback: Optional[UsageCallback]


class UsageRequestList(TypedDict):
    page: int
    limit: int
    requests: Optional[List[UsageRequest]]


class UsageOptions(TypedDict, total=False):
    start: str
    end: str
    accessor: str
    tag: List[str]
    method: Literal['sync', 'async', 'streaming']
    model: str
    multichannel: bool
    interim_results: bool
    punctuate: bool
    ner: bool
    utterances: bool
    replace: bool
    profanity_filter: bool
    keywords: bool
    sentiment: bool
    diarize: bool
    detect_language: bool
    search: bool
    redact: bool
    alternatives: bool
    numerals: bool


class UsageResponseDetail(TypedDict):
    start: str
    end: str
    hours: float
    requests: int


UsageResponseResolution = TypedDict("UsageResponseResolution", {
    'units': str,
    'amount': int
})


class UsageResponse(TypedDict):
    start: str
    end: str
    resolution: UsageResponseResolution
    results: List[UsageResponseDetail]


class UsageFieldOptions(TypedDict, total=False):
    start: str
    end: str


class UsageField(TypedDict):
    tags: List[str]
    models: List[str]
    processing_methods: List[str]
    languages: List[str]
    features: List[str]

# Billing

class Balance(TypedDict):
    balance_id: str
    amount: float
    units: str
    purchase: str


class BalanceResponse(TypedDict):
    projects: List[Balance]


# Scope

class Scope(TypedDict):
    scopes: List[str]


# Invitation

class Invitation(TypedDict):
    email: str
    scope: str


class InvitationResponse(TypedDict):
    message: str
