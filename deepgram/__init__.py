# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# version
__version__ = "0.0.0"

# entry point for the deepgram python sdk
from .client import DeepgramClient, DeepgramApiKeyError
from .options import DeepgramClientOptions

# live
from .clients.live.enums import LiveTranscriptionEvents
from .clients.live.client import LiveClient, AsyncLiveClient, LiveOptions

# onprem
from .clients.onprem.client import (
    OnPremClient,
    AsyncOnPremClient,
)

# prerecorded
from .clients.prerecorded.client import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    PrerecordedOptions,
    PrerecordedSource,
    FileSource,
    UrlSource,
)

# manage
from .clients.manage.client import (
    ManageClient,
    AsyncManageClient,
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)

# utilities
from .audio.microphone.microphone import Microphone
from .audio.microphone.microphone import (
    LOGGING,
    FORMAT,
    CHANNELS,
    RATE,
    CHUNK,
)
