# Backward-compatibility shim. Fern removed the generated
# DeepgramListenProviderV2LanguageHintParams type in the 2026-06-15 regen, but the
# public import path (and the AgentV1SettingsAgent[Context]ListenProviderV2LanguageHint
# compat aliases that import from here) must keep working. Hand-maintained.

import typing

DeepgramListenProviderV2LanguageHintParams = typing.Union[str, typing.Sequence[str]]
