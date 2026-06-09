# 60db WebSocket sample rate. Per docs: LINEAR16/PCM accept all four; MULAW/ULAW
# accept only 8000; OGG_OPUS only 24000. Validation lives server-side.

import typing

SixtyDbSampleRateHertz = typing.Union[typing.Literal[8000, 16000, 24000, 48000], int]
