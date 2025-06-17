"""Deepgram Python SDK - Initialization"""

# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

__version__ = "0.0.0"

from .utils import (
    VerboseLogger,
    NOTICE,
    SPAM,
    SUCCESS,
    VERBOSE,
    WARNING,
    ERROR,
    FATAL,
    CRITICAL,
    INFO,
    DEBUG,
    NOTSET,
)

from .client import *
from .errors import DeepgramApiKeyError
from .audio import (
    Microphone,
    DeepgramMicrophoneError,
    INPUT_LOGGING,
    INPUT_CHANNELS,
    INPUT_RATE,
    INPUT_CHUNK,
    Speaker,
    OUTPUT_LOGGING,
    OUTPUT_CHANNELS,
    OUTPUT_RATE,
    OUTPUT_CHUNK,
)

LOGGING = INPUT_LOGGING
CHANNELS = INPUT_CHANNELS
RATE = INPUT_RATE
CHUNK = INPUT_CHUNK

# Dynamically build __all__ from imported symbols
__all__ = [
    "__version__",
    "VerboseLogger",
    "NOTICE",
    "SPAM",
    "SUCCESS",
    "VERBOSE",
    "WARNING",
    "ERROR",
    "FATAL",
    "CRITICAL",
    "INFO",
    "DEBUG",
    "NOTSET",
    "DeepgramApiKeyError",
    "Microphone",
    "DeepgramMicrophoneError",
    "INPUT_LOGGING",
    "INPUT_CHANNELS",
    "INPUT_RATE",
    "INPUT_CHUNK",
    "Speaker",
    "OUTPUT_LOGGING",
    "OUTPUT_CHANNELS",
    "OUTPUT_RATE",
    "OUTPUT_CHUNK",
    "LOGGING",
    "CHANNELS",
    "RATE",
    "CHUNK",
]

# Add all public symbols from .client
from . import client as _client
__all__ += [name for name in dir(_client) if not name.startswith("_")]

del _client
