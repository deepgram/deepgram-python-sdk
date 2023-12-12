# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .client import PreRecordedClient
from .async_client import AsyncPreRecordedClient
from .options import PrerecordedOptions
from ....options import DeepgramClientOptions


def prerecorded_options():
    return PrerecordedOptions()


def prerecorded(config: DeepgramClientOptions):
    return PreRecordedClient(config)


def asyncprerecorded(config: DeepgramClientOptions):
    return AsyncPreRecordedClient(config)
