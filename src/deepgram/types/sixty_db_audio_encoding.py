# 60db WebSocket audio encoding. Mirrors the API's supported values; Any for
# forward compatibility when 60db adds new codecs.

import typing

SixtyDbAudioEncoding = typing.Union[
    typing.Literal["LINEAR16", "PCM", "MULAW", "ULAW", "OGG_OPUS"], typing.Any
]
