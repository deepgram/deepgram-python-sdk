"""Regression tests for query_encoder boolean coercion.

Python's str(True) returns "True" (capitalized), and urllib.parse.urlencode
falls back to str() for scalar values. The Deepgram API rejects "True"/"False"
on websocket query strings, so query_encoder coerces booleans to lowercase
before they reach urlencode.
"""

import urllib.parse

from deepgram.core.query_encoder import encode_query, single_query_encoder


class TestBoolCoercion:
    def test_top_level_true_becomes_lowercase(self):
        assert single_query_encoder("diarize", True) == [("diarize", "true")]

    def test_top_level_false_becomes_lowercase(self):
        assert single_query_encoder("diarize", False) == [("diarize", "false")]

    def test_encode_query_lowercases_bools(self):
        result = encode_query({"diarize": True, "smart_format": False, "model": "nova-3"})
        assert result is not None
        assert ("diarize", "true") in result
        assert ("smart_format", "false") in result
        assert ("model", "nova-3") in result

    def test_urlencode_roundtrip_produces_lowercase(self):
        encoded = encode_query({"diarize": True, "smart_format": False})
        assert encoded is not None
        query_string = urllib.parse.urlencode(encoded)
        assert "diarize=true" in query_string
        assert "smart_format=false" in query_string
        assert "True" not in query_string
        assert "False" not in query_string

    def test_bools_in_list_value_coerced(self):
        result = single_query_encoder("flags", [True, False])
        assert result == [("flags", "true"), ("flags", "false")]

    def test_bools_in_nested_dict_coerced(self):
        result = single_query_encoder("opts", {"a": True, "b": False})
        assert ("opts[a]", "true") in result
        assert ("opts[b]", "false") in result

    def test_bools_in_nested_list_of_dicts_coerced(self):
        result = single_query_encoder("items", [{"flag": True}])
        assert ("items[flag]", "true") in result


class TestNonBoolValuesPreserved:
    def test_int_preserved(self):
        assert single_query_encoder("count", 5) == [("count", 5)]

    def test_string_preserved(self):
        assert single_query_encoder("name", "foo") == [("name", "foo")]

    def test_float_preserved(self):
        assert single_query_encoder("rate", 1.5) == [("rate", 1.5)]

    def test_string_true_preserved(self):
        assert single_query_encoder("diarize", "true") == [("diarize", "true")]

    def test_int_one_not_coerced_to_bool(self):
        # bool is a subclass of int — make sure we don't accidentally coerce 1/0.
        assert single_query_encoder("count", 1) == [("count", 1)]
        assert single_query_encoder("count", 0) == [("count", 0)]
