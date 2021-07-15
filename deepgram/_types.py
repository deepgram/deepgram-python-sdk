# We want these types to be flexible to allow for updated API responses
# or cutting-edge options to not break the client for older SDK versions;
# as such, everything is implemented using TypedDicts instead of, say, dataclasses.

from typing import Optional, List, Union, Any, Dict
try:
    from typing import TypedDict, Literal
except:
    from typing_extensions import TypedDict, Literal # pre-Py3.8 compatibility
try:
    from collections.abc import Callable, Awaitable
except:
    from typing import Callable, Awaitable # pre-Py3.9 compatibility
from datetime import datetime

# Transcription

class Options(TypedDict):
    api_key: str
    api_url: Optional[str] # this URL should /not/ include a trailing slash

class UrlSource(TypedDict):
    url: str

class BufferSource(TypedDict):
    buffer: bytes
    mimetype: str

TranscriptionSource = Union[UrlSource, BufferSource]

Keyword = Union[str, TypedDict('Keyword', {
    'word': str,
    'boost': float,
})]

class TranscriptionOptions(TypedDict):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeAudio
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeStreamingAudio
    model: Optional[str]
    version: Optional[str]
    language: Optional[str]
    punctuate: Optional[bool]
    profanity_filter: Optional[bool]
    redact: Optional[List[str]]
    diarize: Optional[bool]
    multichannel: Optional[bool]
    alternatives: Optional[int]
    numerals: Optional[bool]
    search: Optional[List[str]]
    callback: Optional[str]
    keywords: Optional[List[str]]

class PrerecordedOptions(TranscriptionOptions):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeAudio
    utterances: Optional[bool]
    utt_split: Optional[float]

class LiveOptions(TranscriptionOptions):
    # References for the different meanings and values of these properties
    # can be found in the Deepgram docs:
    # https://developers.deepgram.com/api-reference/speech-recognition-api#operation/transcribeStreamingAudio
    interim_results: Optional[bool]
    endpointing: Optional[bool]
    vad_turnoff: Optional[int]
    encoding: Optional[str]
    channels: Optional[int]
    sample_rate: Optional[int]

class WordBase(TypedDict):
    word: str
    start: float
    end: float
    confidence: float

class Hit(TypedDict):
    confidence: float
    start: float
    end: float
    snippet: str

class Search(TypedDict):
    query: str
    hits: List[Hit]

class Channel(TypedDict):
    search: Optional[List[Search]]
    alternatives: List[TypedDict('Alternative', {
        'transcript': str,
        'confidence': float,
        'words': List[WordBase],
    })]

class Metadata(TypedDict):
    request_id: str
    transaction_key: str
    sha256: str
    created: str
    duration: float
    channels: int

class PrerecordedTranscriptionResponse(TypedDict):
    request_id: Optional[str]
    metadata: Optional[Metadata]
    results: Optional[TypedDict('ResultChannels', {
        'channels': List[Channel],
    })]

class LiveTranscriptionResponse(TypedDict):
    channel_index: List[int]
    duration: float
    start: float
    is_final: bool
    speech_final: bool
    channel: Channel

EventHandler = Union[Callable[[Any], None], Callable[[Any], Awaitable[None]]]

# Keys

class Key(TypedDict):
    api_key_id: str
    key: Optional[str]
    comment: str
    created: datetime
    scopes: List[str]

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

class UsageRequestDetail(TypedDict):
    details: TypedDict("UsageRequestDetails", {
        'usd': float,
        'duration': float,
        'total_audio': float,
        'channels': int,
        'streams': int,
        'model': str,
        'method': Literal['sync', 'async', 'streaming'],
        'tags': List[str],
        'features': List[str],
        'config': Dict[str, bool] # TODO: add all possible request options
    })

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

class UsageOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]
    accessor: Optional[str]
    tag: Optional[List[str]]
    method: Optional[Literal['sync', 'async', 'streaming']]
    model: Optional[str]
    multichannel: Optional[bool]
    interim_results: Optional[bool]
    punctuate: Optional[bool]
    ner: Optional[bool]
    utterances: Optional[bool]
    replace: Optional[bool]
    profanity_filter: Optional[bool]
    keywords: Optional[bool]
    sentiment: Optional[bool]
    diarize: Optional[bool]
    detect_language: Optional[bool]
    search: Optional[bool]
    redact: Optional[bool]
    alternatives: Optional[bool]
    numerals: Optional[bool]

class UsageResponseDetail(TypedDict):
    start: str
    end: str
    hours: float
    requests: int

class UsageResponse(TypedDict):
    start: str
    end: str
    resolution: TypedDict("UsageResponseResolution", {
        'units': str,
        'amount': int
    })
    results: List[UsageResponseDetail]

class UsageFieldOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]

class UsageField(TypedDict):
    tags: List[str]
    models: List[str]
    processing_methods: List[str]
    languages: List[str]
    features: List[str]
