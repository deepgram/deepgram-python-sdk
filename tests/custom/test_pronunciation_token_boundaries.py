import pytest

from deepgram.helpers import add_pronunciation


@pytest.mark.parametrize("word", ["C++", "C#", ".NET"])
def test_pronunciation_matches_punctuated_names(word):
    result = add_pronunciation(f"Use {word} today.", word, "test")
    assert '"pronounce": "test"' in result
    assert f'"word": "{word}"' in result


@pytest.mark.parametrize("text,word", [("XC++", "C++"), ("C++17", "C++"), ("C#script", "C#"), ("ASP.NET", ".NET")])
def test_pronunciation_does_not_replace_inside_longer_tokens(text, word):
    assert add_pronunciation(text, word, "test") == text
