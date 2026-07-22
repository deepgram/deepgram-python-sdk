"""Regression tests for the `stt_latency` backward-compat shim on AgentV1LatencyReport.

The API spec removed `stt_latency` from the LatencyReport schema (deepgram-docs #1006).
LatencyReport is a server-emitted (read-only) message, so we re-add the field by hand
(frozen in .fernignore) to keep `report.stt_latency` resolving instead of raising
AttributeError — avoiding a major-version break. These tests lock that behavior in.
"""

from deepgram.agent.v1.socket_client import V1SocketClientResponse
from deepgram.agent.v1.types import AgentV1LatencyReport
from deepgram.core.unchecked_base_model import construct_type


def test_stt_latency_defaults_to_none() -> None:
    """The shimmed field exists and defaults to None (no AttributeError)."""
    report = AgentV1LatencyReport()
    assert report.stt_latency is None


def test_latency_report_without_stt_latency_parses_with_none() -> None:
    """A real inbound message lacking stt_latency (current server behavior) keeps
    the attribute accessible as None rather than raising."""
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={
            "type": "LatencyReport",
            "ttt_token_latency": 0.12,
            "tts_latency": 0.34,
            "total_latency": 0.56,
        },
    )

    assert isinstance(parsed, AgentV1LatencyReport)
    assert parsed.stt_latency is None
    assert parsed.ttt_token_latency == 0.12
    assert parsed.total_latency == 0.56


def test_latency_report_with_stt_latency_still_populates() -> None:
    """If the server ever re-emits stt_latency, the shimmed field captures it."""
    parsed = construct_type(
        type_=V1SocketClientResponse,
        object_={"type": "LatencyReport", "stt_latency": 0.42},
    )

    assert isinstance(parsed, AgentV1LatencyReport)
    assert parsed.stt_latency == 0.42
