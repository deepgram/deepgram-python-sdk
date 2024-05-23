# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1 import (
    TextSource as TextSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    UrlSource as UrlSourceLatest,
    Sentiment as SentimentLatest,
)

UrlSource = UrlSourceLatest
TextSource = TextSourceLatest
BufferSource = BufferSourceLatest
StreamSource = StreamSourceLatest


Sentiment = SentimentLatest
FileSource = FileSourceLatest
