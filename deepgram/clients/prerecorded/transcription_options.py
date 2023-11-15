from typing import Union, List, TypedDict

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
