import json

from deepgram.agent import AgentV1FunctionCallCancelled as AgentFunctionCallCancelled
from deepgram.agent.v1 import AgentV1FunctionCallCancelled as V1FunctionCallCancelled
from deepgram.agent.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.agent.v1.types import (
    AgentV1FunctionCallCancelled,
    ConversationHistoryMessage,
    FunctionCallHistoryMessage,
)
from deepgram.core.unchecked_base_model import construct_type


class _FakeWebSocket:
    def recv(self) -> str:
        return json.dumps({"type": "FunctionCallCancelled", "functions": [{"id": "fc_123", "name": "lookup_weather"}]})


class _FakeAsyncWebSocket:
    async def recv(self) -> str:
        return json.dumps({"type": "FunctionCallCancelled", "functions": [{"id": "fc_123", "name": "lookup_weather"}]})


def test_agent_history_content_parses_from_socket_union() -> None:
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={"type": "History", "role": "user", "content": "hello"},
    )

    assert isinstance(parsed, ConversationHistoryMessage)
    assert parsed.type == "History"
    assert parsed.role == "user"
    assert parsed.content == "hello"


def test_agent_history_function_calls_parse_from_socket_union() -> None:
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={
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
        },
    )

    assert isinstance(parsed, FunctionCallHistoryMessage)
    assert parsed.type == "History"
    assert len(parsed.function_calls) == 1

    function_call = parsed.function_calls[0]
    assert function_call.id == "fc_123"
    assert function_call.name == "lookup_weather"
    assert function_call.client_side is True
    assert function_call.arguments == '{"city":"London"}'
    assert function_call.response == "sunny"


def test_agent_function_call_cancelled_parses_from_socket_union() -> None:
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={
            "type": "FunctionCallCancelled",
            "functions": [{"id": "fc_123", "name": "lookup_weather"}],
        },
    )

    assert isinstance(parsed, AgentV1FunctionCallCancelled)
    assert parsed.type == "FunctionCallCancelled"
    assert len(parsed.functions) == 1
    assert parsed.functions[0].id == "fc_123"
    assert parsed.functions[0].name == "lookup_weather"


def test_agent_function_call_cancelled_is_exported_and_received() -> None:
    assert AgentFunctionCallCancelled is AgentV1FunctionCallCancelled
    assert V1FunctionCallCancelled is AgentV1FunctionCallCancelled

    message = V1SocketClient(websocket=_FakeWebSocket()).recv()
    assert isinstance(message, AgentV1FunctionCallCancelled)


async def test_agent_function_call_cancelled_is_received_async() -> None:
    message = await AsyncV1SocketClient(websocket=_FakeAsyncWebSocket()).recv()
    assert isinstance(message, AgentV1FunctionCallCancelled)
