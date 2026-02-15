from .conftest import get_client, verify_request_count


def test_speak_v1_audio_generate() -> None:
    """Test generate endpoint with WireMock"""
    test_id = "speak.v1.audio.generate.0"
    client = get_client(test_id)
    for _ in client.speak.v1.audio.generate(text="text"):
        pass
    verify_request_count(test_id, "POST", "/v1/speak", None, 1)
