from .conftest import get_client, verify_request_count


def test_speak_v2_audio_generate() -> None:
    """Test generate endpoint with WireMock"""
    test_id = "speak.v2.audio.generate.0"
    client = get_client(test_id)
    for _ in client.speak.v2.audio.generate(
        model="model",
        text="text",
    ):
        pass
    verify_request_count(test_id, "POST", "/v2/speak", {"model": "model"}, 1)
