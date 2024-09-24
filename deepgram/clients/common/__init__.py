# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1 import DeepgramError, DeepgramTypeError

from .v1 import (
    TextSource as TextSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    UrlSource as UrlSourceLatest,
)

# shared
from .v1 import (
    BaseResponse as BaseResponseLatest,
    ModelInfo as ModelInfoLatest,
    Word as WordLatest,
    Alternative as AlternativeLatest,
    Hit as HitLatest,
    Search as SearchLatest,
    Channel as ChannelLatest,
)

# rest
from .v1 import (
    Average as AverageLatest,
    Intent as IntentLatest,
    Intents as IntentsLatest,
    IntentsInfo as IntentsInfoLatest,
    Segment as SegmentLatest,
    SentimentInfo as SentimentInfoLatest,
    Sentiment as SentimentLatest,
    Sentiments as SentimentsLatest,
    SummaryInfo as SummaryInfoLatest,
    Topic as TopicLatest,
    Topics as TopicsLatest,
    TopicsInfo as TopicsInfoLatest,
)

# websocket
from .v1 import (
    OpenResponse as OpenResponseLatest,
    CloseResponse as CloseResponseLatest,
    ErrorResponse as ErrorResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
)

# export
UrlSource = UrlSourceLatest
TextSource = TextSourceLatest
BufferSource = BufferSourceLatest
StreamSource = StreamSourceLatest
FileSource = FileSourceLatest

BaseResponse = BaseResponseLatest
ModelInfo = ModelInfoLatest
Word = WordLatest
Alternative = AlternativeLatest
Hit = HitLatest
Search = SearchLatest
Channel = ChannelLatest

Average = AverageLatest
Intent = IntentLatest
Intents = IntentsLatest
IntentsInfo = IntentsInfoLatest
Segment = SegmentLatest
SentimentInfo = SentimentInfoLatest
Sentiment = SentimentLatest
Sentiments = SentimentsLatest
SummaryInfo = SummaryInfoLatest
Topic = TopicLatest
Topics = TopicsLatest
TopicsInfo = TopicsInfoLatest

OpenResponse = OpenResponseLatest
CloseResponse = CloseResponseLatest
ErrorResponse = ErrorResponseLatest
UnhandledResponse = UnhandledResponseLatest
