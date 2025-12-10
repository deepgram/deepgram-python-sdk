from .conftest import get_client, verify_request_count


def test_read_v1_text_analyze() -> None:
    """Test analyze endpoint with WireMock"""
    test_id = "read.v1.text.analyze.0"
    client = get_client(test_id)
    client.read.v1.text.analyze(
        callback="callback",
        callback_method="POST",
        sentiment=True,
        summarize="v2",
        tag=["tag"],
        topics=True,
        custom_topic=["custom_topic"],
        custom_topic_mode="extended",
        intents=True,
        custom_intent=["custom_intent"],
        custom_intent_mode="extended",
        language="language",
        request={"url": "url"},
    )
    verify_request_count(
        test_id,
        "POST",
        "/v1/read",
        {
            "callback": "callback",
            "callback_method": "POST",
            "sentiment": "true",
            "summarize": "v2",
            "tag": "tag",
            "topics": "true",
            "custom_topic": "custom_topic",
            "custom_topic_mode": "extended",
            "intents": "true",
            "custom_intent": "custom_intent",
            "custom_intent_mode": "extended",
            "language": "language",
        },
        1,
    )
