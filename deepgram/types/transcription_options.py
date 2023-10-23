from typing import Union, List, TypedDict

class TranscriptionOptions(TypedDict, total=False):
    callback: str
    diarize: bool
    keywords: Union[List[str], str]
    language: str
    model: str
    multichannel: bool
    numerals: bool
    punctuate: bool
    profanity_filter: bool
    redact: Union[List[str], List[bool], bool]
    replace: Union[List[str], str]
    search: Union[List[str], str]
    smart_format: bool
    tag: List[str]
    tier: str
    version: str


class PrerecordedOptions(TypedDict, total=False):
    alternatives: int
    callback: str
    detect_entities: bool
    detect_language: bool
    detect_topics: bool
    diarize: bool
    keywords: Union[list, str]
    language: str
    model: str
    multichannel: bool
    numerals: bool
    paragraphs: bool
    profanity_filter: bool
    punctuate: bool
    redact: Union[List[str], bool, str]
    replace: Union[list, str]
    search: Union[list, str]
    smart_format: bool
    summarize: Union[bool, str]
    tag: list
    tier: str
    utt_split: int
    utterances: bool
    version: str


class LiveOptions(TypedDict, total=False):
    callback: str
    channels: int
    diarize: bool
    encoding: str
    endpointing: int
    interim_results: bool
    keywords: str
    language: str
    model: str
    multichannel: bool
    numerals: bool
    punctuate: bool
    profanity_filter: bool
    redact: bool
    replace: str
    sample_rate: int
    search: str
    smart_format: bool
    tag: list
    tier: str
    version: str

