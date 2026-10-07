import json
from typing import Any, cast

from deepgram.agent import AgentV1CustomFromThinkProvider as AgentCustomFromThinkProvider
from deepgram.agent.v1 import AgentV1CustomToThinkProvider as V1CustomToThinkProvider
from deepgram.agent.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.agent.v1.types import AgentV1CustomFromThinkProvider, AgentV1CustomToThinkProvider
from deepgram.core.unchecked_base_model import construct_type


class _FakeWebSocket:
    def __init__(self, response: dict | None = None) -> None:
        self.response = response
        self.sent: list[str] = []

    def recv(self) -> str:
        assert self.response is not None
        return json.dumps(self.response)

    def send(self, data: str) -> None:
        self.sent.append(data)


class _FakeAsyncWebSocket:
    def __init__(self, response: dict | None = None) -> None:
        self.response = response
        self.sent: list[str] = []

    async def recv(self) -> str:
        assert self.response is not None
        return json.dumps(self.response)

    async def send(self, data: str) -> None:
        self.sent.append(data)


def test_custom_think_provider_messages_are_exported() -> None:
    assert AgentCustomFromThinkProvider is AgentV1CustomFromThinkProvider
    assert V1CustomToThinkProvider is AgentV1CustomToThinkProvider


def test_sync_custom_think_provider_messages_serialize_and_parse() -> None:
    content = {"tool": "lookup_weather", "arguments": {"city": "London"}}
    websocket = _FakeWebSocket({"type": "__customFromThinkProvider", "content": content})
    client = V1SocketClient(websocket=cast(Any, websocket))

    client.send_custom_to_think_provider(AgentV1CustomToThinkProvider(content=content))

    assert json.loads(websocket.sent[0]) == {"type": "__customToThinkProvider", "content": content}
    received = client.recv()
    assert isinstance(received, AgentV1CustomFromThinkProvider)
    assert received.content == content


async def test_async_custom_think_provider_messages_serialize_and_parse() -> None:
    content = {"progress": 0.5, "complete": False}
    websocket = _FakeAsyncWebSocket({"type": "__customFromThinkProvider", "content": content})
    client = AsyncV1SocketClient(websocket=cast(Any, websocket))

    await client.send_custom_to_think_provider(AgentV1CustomToThinkProvider(content=content))

    assert json.loads(websocket.sent[0]) == {"type": "__customToThinkProvider", "content": content}
    received = await client.recv()
    assert isinstance(received, AgentV1CustomFromThinkProvider)
    assert received.content == content


def test_custom_think_provider_response_parses_from_socket_union() -> None:
    content = ["token", {"complete": True}]
    parsed = construct_type(
        type_=cast(Any, V1SocketClientResponse),
        object_={"type": "__customFromThinkProvider", "content": content},
    )

    assert isinstance(parsed, AgentV1CustomFromThinkProvider)
    assert parsed.type == "__customFromThinkProvider"
    assert parsed.content == content
