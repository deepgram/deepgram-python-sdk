import json

from deepgram.extensions.core.binary_message_mixin import BinaryMessageMixin
from deepgram.extensions.types.sockets import (
    AgentSocketClientResponse,
    ListenSocketClientResponse,
    SpeakSocketClientResponse,
    SpeakV1MetadataEvent,
    SpeakV1TextMessage,
)


def test_speak_v1_metadata_event_roundtrip_and_frozen():
    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="name",
        model_version="v",
        model_uuid="uuid",
    )
    # Round trip dict/json
    d = meta.dict()
    assert d["type"] == "Metadata" and d["request_id"] == "r1"
    j = meta.json()
    assert "\"Metadata\"" in j

    # Frozen model (immutable)
    try:
        meta.request_id = "r2"  # type: ignore[misc]
        mutated = False
    except Exception:
        mutated = True
    assert mutated


def test_binary_message_mixin_unions_accept_bytes_and_models():
    class M(BinaryMessageMixin):
        pass

    m = M()
    # JSON: Speak metadata
    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="name",
        model_version="v",
        model_uuid="uuid",
    )
    raw = json.dumps(meta.dict())
    parsed, is_binary = m._process_message(raw, SpeakSocketClientResponse)
    assert not is_binary and isinstance(parsed, SpeakV1MetadataEvent)

    # Binary
    data = b"abc"
    parsed_b, is_binary_b = m._process_message(data, AgentSocketClientResponse)
    assert is_binary_b and parsed_b == data


