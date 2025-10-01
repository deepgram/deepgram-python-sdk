# Listen V1 Results Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ListenV1Word(UniversalBaseModel):
    """Word in transcription results"""
    word: str
    """The word of the transcription"""
    
    start: float
    """The start time of the word"""
    
    end: float
    """The end time of the word"""
    
    confidence: float
    """The confidence of the word"""
    
    language: typing.Optional[str] = None
    """The language of the word"""
    
    punctuated_word: typing.Optional[str] = None
    """The punctuated word of the word"""
    
    speaker: typing.Optional[int] = None
    """The speaker of the word"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ListenV1Alternative(UniversalBaseModel):
    """Alternative transcription result"""
    transcript: str
    """The transcript of the transcription"""
    
    confidence: float
    """The confidence of the transcription"""
    
    languages: typing.Optional[typing.List[str]] = None
    """The languages of the transcription"""
    
    words: typing.List[ListenV1Word]
    """Array of words in the transcription"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ListenV1Channel(UniversalBaseModel):
    """Channel transcription results"""
    alternatives: typing.List[ListenV1Alternative]
    """Array of alternative transcription results"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ListenV1ModelInfo(UniversalBaseModel):
    """Model information"""
    name: str
    """The name of the model"""
    
    version: str
    """The version of the model"""
    
    arch: str
    """The arch of the model"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ListenV1ResultsMetadata(UniversalBaseModel):
    """Results metadata"""
    request_id: str
    """The request ID"""
    
    model_info: ListenV1ModelInfo
    """Model information"""
    
    model_uuid: str
    """The model UUID"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ListenV1ResultsEvent(UniversalBaseModel):
    """
    Deepgram has responded with a transcription
    """
    
    type: typing.Literal["Results"]
    """Message type identifier"""
    
    channel_index: typing.List[int]
    """The index of the channel"""
    
    duration: float
    """The duration of the transcription"""
    
    start: float
    """The start time of the transcription"""
    
    is_final: typing.Optional[bool] = None
    """Whether the transcription is final"""
    
    speech_final: typing.Optional[bool] = None
    """Whether the transcription is speech final"""
    
    channel: ListenV1Channel
    """Channel transcription results"""
    
    metadata: ListenV1ResultsMetadata
    """Results metadata"""
    
    from_finalize: typing.Optional[bool] = None
    """Whether the transcription is from a finalize message"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
