# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .microphone import Microphone
from .microphone import DeepgramMicrophoneError
from .microphone import (
    LOGGING as INPUT_LOGGING,
    CHANNELS as INPUT_CHANNELS,
    RATE as INPUT_RATE,
    CHUNK as INPUT_CHUNK,
)

from .speaker import Speaker
from .speaker import DeepgramSpeakerError
from .speaker import (
    LOGGING as OUTPUT_LOGGING,
    CHANNELS as OUTPUT_CHANNELS,
    RATE as OUTPUT_RATE,
    CHUNK as OUTPUT_CHUNK,
)
