from typing import assert_type

from deepgram.agent.v1.requests import (
    AgentV1HistoryContentParams,
    AgentV1HistoryFunctionCallsParams,
    ConversationHistoryMessageParams,
    FunctionCallHistoryMessageParams,
)
from deepgram.requests import CreateKeyV1RequestOneParams, CreateKeyV1RequestParams

create_key_request: CreateKeyV1RequestOneParams = {"key": "value"}
history_content: AgentV1HistoryContentParams = {
    "type": "History",
    "role": "user",
    "content": "hello",
}
history_function_calls: AgentV1HistoryFunctionCallsParams = {
    "type": "History",
    "function_calls": [
        {
            "id": "fc_123",
            "name": "lookup_weather",
            "client_side": True,
            "arguments": '{"city":"London"}',
            "response": "sunny",
        }
    ],
}

assert_type(create_key_request, CreateKeyV1RequestParams)
assert_type(history_content, ConversationHistoryMessageParams)
assert_type(history_function_calls, FunctionCallHistoryMessageParams)

# language_hint backward-compat: the deprecated singular kwarg (str or list) must
# keep type-checking on the V2 listen provider, alongside the canonical plural.
# If the deprecated `language_hint` field is ever dropped, these fail type-checking
# and gate the regression (this file is type-checked by CI, not executed).
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2

_language_hint_str = DeepgramListenProviderV2(model="flux-general-multi", language_hint="en")
_language_hint_list = DeepgramListenProviderV2(model="flux-general-multi", language_hint=["en", "de"])
_language_hints_plural = DeepgramListenProviderV2(model="flux-general-multi", language_hints=["fr"])
