# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pyaudio
import logging, verboselogs

LOGGING = logging.WARNING
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8194
