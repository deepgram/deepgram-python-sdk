# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .listen import ListenClient
from ..options import DeepgramClientOptions


def listen(config: DeepgramClientOptions):
    return ListenClient(config)
