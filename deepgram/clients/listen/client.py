# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# rest
from .v1 import (
    ListenRESTClient as ListenRESTClientLatest,
    AsyncListenRESTClient as AsyncListenRESTClientLatest,
)
from .v1 import (
    PrerecordedOptions as PrerecordedOptionsLatest,
    ListenRESTOptions as ListenRESTOptionsLatest,
)

from .v1 import (
    UrlSource as UrlSourceLatest,
    TextSource as TextSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    PreRecordedStreamSource as PreRecordedStreamSourceLatest,
    PrerecordedSource as PrerecordedSourceLatest,
    ListenRestSource as ListenRestSourceLatest,
)
from .v1 import (
    AsyncPrerecordedResponse as AsyncPrerecordedResponseLatest,
    PrerecordedResponse as PrerecordedResponseLatest,
    SyncPrerecordedResponse as SyncPrerecordedResponseLatest,
    # shared
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
    # between rest and websocket
    ModelInfo as ModelInfoLatest,
    Hit as HitLatest,
    Search as SearchLatest,
    # unique
    ListenRESTMetadata as ListenRESTMetadataLatest,
    Entity as EntityLatest,
    Paragraph as ParagraphLatest,
    Paragraphs as ParagraphsLatest,
    ListenRESTResults as ListenRESTResultsLatest,
    Sentence as SentenceLatest,
    Summaries as SummariesLatest,
    SummaryV1 as SummaryV1Latest,
    SummaryV2 as SummaryV2Latest,
    Translation as TranslationLatest,
    Utterance as UtteranceLatest,
    Warning as WarningLatest,
    ListenRESTAlternative as ListenRESTAlternativeLatest,
    ListenRESTChannel as ListenRESTChannelLatest,
    ListenRESTWord as ListenRESTWordLatest,
)

# websocket
from .v1 import (
    ListenWebSocketClient as ListenWebSocketClientLatest,
    AsyncListenWebSocketClient as AsyncListenWebSocketClientLatest,
)
from .v1 import (
    LiveOptions as LiveOptionsLatest,
    ListenWebSocketOptions as ListenWebSocketOptionsLatest,
)
from .v1 import (
    OpenResponse as OpenResponseLatest,
    LiveResultResponse as LiveResultResponseLatest,
    ListenWSMetadataResponse as ListenWSMetadataResponseLatest,
    SpeechStartedResponse as SpeechStartedResponseLatest,
    UtteranceEndResponse as UtteranceEndResponseLatest,
    CloseResponse as CloseResponseLatest,
    ErrorResponse as ErrorResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
    ListenWSMetadata as ListenWSMetadataLatest,
    ListenWSAlternative as ListenWSAlternativeLatest,
    ListenWSChannel as ListenWSChannelLatest,
    ListenWSWord as ListenWSWordLatest,
)

# The vX/client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.

# shared
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

# between rest and websocket
Hit = HitLatest
ModelInfo = ModelInfoLatest
Search = SearchLatest

# websocket common
OpenResponse = OpenResponseLatest
CloseResponse = CloseResponseLatest
ErrorResponse = ErrorResponseLatest
UnhandledResponse = UnhandledResponseLatest


# backward compat
PreRecordedClient = ListenRESTClientLatest
AsyncPreRecordedClient = AsyncListenRESTClientLatest
LiveClient = ListenWebSocketClientLatest
AsyncLiveClient = ListenWebSocketClientLatest

# rest
## common
UrlSource = UrlSourceLatest
TextSource = TextSourceLatest
BufferSource = BufferSourceLatest
StreamSource = StreamSourceLatest
FileSource = FileSourceLatest

# input
ListenRESTOptions = ListenRESTOptionsLatest
PrerecordedOptions = PrerecordedOptionsLatest
PreRecordedStreamSource = PreRecordedStreamSourceLatest
PrerecordedSource = PrerecordedSourceLatest
ListenRestSource = ListenRestSourceLatest

## output
AsyncPrerecordedResponse = AsyncPrerecordedResponseLatest
PrerecordedResponse = PrerecordedResponseLatest
SyncPrerecordedResponse = SyncPrerecordedResponseLatest
# unique
Entity = EntityLatest
ListenRESTMetadata = ListenRESTMetadataLatest
Paragraph = ParagraphLatest
Paragraphs = ParagraphsLatest
ListenRESTResults = ListenRESTResultsLatest
Sentence = SentenceLatest
Summaries = SummariesLatest
SummaryV1 = SummaryV1Latest
SummaryV2 = SummaryV2Latest
Translation = TranslationLatest
Utterance = UtteranceLatest
Warning = WarningLatest
ListenRESTAlternative = ListenRESTAlternativeLatest
ListenRESTChannel = ListenRESTChannelLatest
ListenRESTWord = ListenRESTWordLatest

# websocket
## input
ListenWebSocketOptions = ListenWebSocketOptionsLatest
LiveOptions = LiveOptionsLatest

## output
LiveResultResponse = LiveResultResponseLatest
ListenWSMetadataResponse = ListenWSMetadataResponseLatest
SpeechStartedResponse = SpeechStartedResponseLatest
UtteranceEndResponse = UtteranceEndResponseLatest

## unique
ListenWSMetadata = ListenWSMetadataLatest
ListenWSAlternative = ListenWSAlternativeLatest
ListenWSChannel = ListenWSChannelLatest
ListenWSWord = ListenWSWordLatest

# clients
ListenRESTClient = ListenRESTClientLatest
AsyncListenRESTClient = AsyncListenRESTClientLatest
ListenWebSocketClient = ListenWebSocketClientLatest
AsyncListenWebSocketClient = AsyncListenWebSocketClientLatest
