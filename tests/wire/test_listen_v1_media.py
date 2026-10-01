from .conftest import get_client, verify_request_count


def test_listen_v1_media_transcribe_url() -> None:
    """Test transcribeUrl endpoint with WireMock"""
    test_id = "listen.v1.media.transcribe_url.0"
    client = get_client(test_id)
    client.listen.v1.media.transcribe_url(
        url="https://dpgr.am/spacewalk.wav",
    )
    verify_request_count(test_id, "POST", "/v1/listen", None, 1)
