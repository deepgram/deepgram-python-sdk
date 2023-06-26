import json
import pytest
import sys

# from .conftest import option
from deepgram import Deepgram
from .mock_response import MOCK_RESPONSE

api_key = pytest.api_key
assert api_key, "Pass Deepgram API key as an argument: `pytest --api-key <key> tests/`"

deepgram = Deepgram(api_key)

MOCK_SRT = "1\n00:00:05,519 --> 00:00:06,019\nYep.\n\n2\n00:00:07,094 --> 00:00:08,615\nI said it before, and I'll say it\n\n3\n00:00:08,615 --> 00:00:09,115\nagain.\n\n4\n00:00:09,974 --> 00:00:11,514\nLife moves pretty fast.\n\n5\n00:00:11,974 --> 00:00:13,654\nYou don't stop and look around once in\n\n6\n00:00:13,654 --> 00:00:15,701\na while. you could miss it."
MOCK_WEBVTT = "1\n00:00:05.519 --> 00:00:06.019\n- Yep.\n\n2\n00:00:07.094 --> 00:00:08.615\n- I said it before, and I'll say it\n\n3\n00:00:08.615 --> 00:00:09.115\n- again.\n\n4\n00:00:09.974 --> 00:00:11.514\n- Life moves pretty fast.\n\n5\n00:00:11.974 --> 00:00:13.654\n- You don't stop and look around once in\n\n6\n00:00:13.654 --> 00:00:15.701\n- a while. you could miss it."

"""
Happy case of captions in SRT format.
"""
def test_get_SRT():
    assert deepgram.extra.to_SRT(MOCK_RESPONSE, readable=False) == MOCK_SRT

"""
Happy case of captions in WebVTT format.
"""
def test_get_WebVTT():
    assert deepgram.extra.to_WebVTT(MOCK_RESPONSE, readable=False) == MOCK_WEBVTT

"""
A response without Utterances cannot be captioned.
"""
def test_get_SRT_no_utterances():
    response_no_utts = MOCK_RESPONSE
    del response_no_utts["results"]["utterances"]
    with pytest.warns(UserWarning):
        deepgram.extra.to_SRT(response_no_utts)
