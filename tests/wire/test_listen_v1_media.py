from .conftest import get_client, verify_request_count


def test_listen_v1_media_transcribe_url() -> None:
    """Test transcribeUrl endpoint with WireMock"""
    test_id = "listen.v1.media.transcribe_url.0"
    client = get_client(test_id)
    client.listen.v1.media.transcribe_url(
        url="https://dpgr.am/spacewalk.wav",
    )
    verify_request_count(test_id, "POST", "/v1/listen", None, 1)


def test_listen_v1_media_transcribe_url_serializes_all_query_params() -> None:
    """All 37 optional query params must reach the wire, with bools lowercased.

    The 2026-08-18 regen simplified the upstream spec *example* for this endpoint,
    and Fern derives the wire test from that example -- so the generated test
    dropped every query parameter, leaving their serialization unverified while
    the client signature still forwards all 37. This restores that coverage; the
    file is frozen in .fernignore so a future regen cannot silently drop it again.

    Same failure mode as tests/wire/test_manage_v1_projects_keys.py and
    tests/wire/test_manage_v1_projects_requests.py, which are frozen for this reason.
    """
    test_id = "listen.v1.media.transcribe_url.query_params"
    client = get_client(test_id)
    client.listen.v1.media.transcribe_url(
        callback="callback",
        callback_method="POST",
        extra=["extra"],
        sentiment=True,
        summarize="v2",
        tag=["tag"],
        topics=True,
        custom_topic=["custom_topic"],
        custom_topic_mode="extended",
        intents=True,
        custom_intent=["custom_intent"],
        custom_intent_mode="extended",
        detect_entities=True,
        detect_language=True,
        diarize=True,
        diarize_model="latest",
        dictation=True,
        encoding="linear16",
        filler_words=True,
        keyterm=["keyterm"],
        keywords=["keywords"],
        language="language",
        measurements=True,
        model="nova-3",
        multichannel=True,
        numerals=True,
        paragraphs=True,
        profanity_filter=True,
        punctuate=True,
        redact="redact",
        replace=["replace"],
        search=["search"],
        smart_format=True,
        utterances=True,
        utt_split=1.1,
        version="latest",
        mip_opt_out=True,
        url="https://dpgr.am/spacewalk.wav",
    )
    verify_request_count(
        test_id,
        "POST",
        "/v1/listen",
        {
            "callback": "callback",
            "callback_method": "POST",
            "extra": "extra",
            "sentiment": "true",
            "summarize": "v2",
            "tag": "tag",
            "topics": "true",
            "custom_topic": "custom_topic",
            "custom_topic_mode": "extended",
            "intents": "true",
            "custom_intent": "custom_intent",
            "custom_intent_mode": "extended",
            "detect_entities": "true",
            "detect_language": "true",
            "diarize": "true",
            "diarize_model": "latest",
            "dictation": "true",
            "encoding": "linear16",
            "filler_words": "true",
            "keyterm": "keyterm",
            "keywords": "keywords",
            "language": "language",
            "measurements": "true",
            "model": "nova-3",
            "multichannel": "true",
            "numerals": "true",
            "paragraphs": "true",
            "profanity_filter": "true",
            "punctuate": "true",
            "redact": "redact",
            "replace": "replace",
            "search": "search",
            "smart_format": "true",
            "utterances": "true",
            "utt_split": "1.1",
            "version": "latest",
            "mip_opt_out": "true",
        },
        1,
    )
