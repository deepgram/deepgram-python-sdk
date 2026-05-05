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
