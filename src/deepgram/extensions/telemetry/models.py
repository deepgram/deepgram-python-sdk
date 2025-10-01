"""
Generated Pydantic models from telemetry.proto
Auto-generated - do not edit manually
"""

from __future__ import annotations

import typing
from datetime import datetime
from enum import Enum

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ErrorSeverity(str, Enum):
    """Error severity level enum."""
    UNSPECIFIED = "ERROR_SEVERITY_UNSPECIFIED"
    INFO = "ERROR_SEVERITY_INFO"
    WARNING = "ERROR_SEVERITY_WARNING"
    ERROR = "ERROR_SEVERITY_ERROR"
    CRITICAL = "ERROR_SEVERITY_CRITICAL"


class TelemetryContext(UniversalBaseModel):
    """
    Represents common context about the SDK/CLI and environment producing telemetry.
    """
    
    package_name: typing.Optional[str] = None
    """e.g., "node-sdk", "python-sdk", "cli" """
    
    package_version: typing.Optional[str] = None
    """e.g., "3.2.1" """
    
    language: typing.Optional[str] = None
    """e.g., "node", "python", "go" """
    
    runtime_version: typing.Optional[str] = None
    """e.g., "node 20.11.1", "python 3.11.6" """
    
    os: typing.Optional[str] = None
    """e.g., "darwin", "linux", "windows" """
    
    arch: typing.Optional[str] = None
    """e.g., "arm64", "amd64" """
    
    app_name: typing.Optional[str] = None
    """host application name (if known) """
    
    app_version: typing.Optional[str] = None
    """host application version (if known) """
    
    environment: typing.Optional[str] = None
    """e.g., "prod", "staging", "dev" """
    
    session_id: typing.Optional[str] = None
    """client session identifier """
    
    installation_id: typing.Optional[str] = None
    """stable machine/install identifier when available """
    
    project_id: typing.Optional[str] = None
    """project/workspace identifier if applicable """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TelemetryEvent(UniversalBaseModel):
    """
    Telemetry event payload carrying arbitrary attributes and metrics.
    """
    
    name: str
    """event name, e.g., "request.start" """
    
    time: datetime
    """event timestamp (UTC) """
    
    attributes: typing.Optional[typing.Dict[str, str]] = None
    """string attributes (tags) """
    
    metrics: typing.Optional[typing.Dict[str, float]] = None
    """numeric metrics """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ErrorEvent(UniversalBaseModel):
    """
    Structured error event.
    """
    
    type: typing.Optional[str] = None
    """error type/class, e.g., "TypeError" """
    
    message: typing.Optional[str] = None
    """error message """
    
    stack_trace: typing.Optional[str] = None
    """stack trace if available """
    
    file: typing.Optional[str] = None
    """source file (if known) """
    
    line: typing.Optional[int] = None
    """source line number """
    
    column: typing.Optional[int] = None
    """source column number """
    
    severity: ErrorSeverity = ErrorSeverity.UNSPECIFIED
    """severity level """
    
    handled: bool = False
    """whether the error was handled """
    
    time: datetime
    """error timestamp (UTC) """
    
    attributes: typing.Optional[typing.Dict[str, str]] = None
    """additional context as key/value """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Record(UniversalBaseModel):
    """
    A single record may be telemetry or error.
    """
    
    telemetry: typing.Optional[TelemetryEvent] = None
    error: typing.Optional[ErrorEvent] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class TelemetryBatch(UniversalBaseModel):
    """
    Batch payload sent to the ingestion endpoint.
    The entire batch may be gzip-compressed; server accepts raw or gzip.
    """
    
    context: TelemetryContext
    """shared context for the batch """
    
    records: typing.List[Record]
    """telemetry and error records """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
