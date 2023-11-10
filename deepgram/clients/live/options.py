from typing import Union, List, TypedDict

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

