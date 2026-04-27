from deepgram.agent.v1.socket_client import V1SocketClientResponse
from deepgram.agent.v1.types import AgentV1HistoryContent, AgentV1HistoryFunctionCalls
from deepgram.core.unchecked_base_model import construct_type


def test_agent_history_content_parses_from_socket_union() -> None:
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={"type": "History", "role": "user", "content": "hello"},
    )

    assert isinstance(parsed, AgentV1HistoryContent)
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

    assert isinstance(parsed, AgentV1HistoryFunctionCalls)
    assert parsed.type == "History"
    assert len(parsed.function_calls) == 1

    function_call = parsed.function_calls[0]
    assert function_call.id == "fc_123"
    assert function_call.name == "lookup_weather"
    assert function_call.client_side is True
    assert function_call.arguments == '{"city":"London"}'
    assert function_call.response == "sunny"
