# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pyaudio
import logging, verboselogs

from .microphone import microphone
from .microphone import (
    LOGGING as iLOGGING,
    FORMAT as iFORMAT,
    CHANNELS as iCHANNELS,
    RATE as iRATE,
    CHUNK as iCHUNK,
)

LOGGING = iLOGGING
FORMAT = iFORMAT
CHANNELS = iCHANNELS
RATE = iRATE
CHUNK = iCHUNK


def microphone(
    push_callback,
    verbose=LOGGING,
    format=FORMAT,
    rate=RATE,
    chunk=CHUNK,
    channels=CHANNELS,
):
    return microphone(push_callback, verbose, format, rate, chunk, channels)
