"""Equivalent pronunciation inputs must enforce the same spoken-text limit."""

import pytest

from deepgram.helpers import TextBuilder


@pytest.mark.parametrize("word", ["word", "café", 'a"b', r"a\b"])
@pytest.mark.parametrize("extra", [0, 1])
@pytest.mark.parametrize("mode", ["fluent", "inline", "ssml"])
def test_pronunciation_words_count_toward_character_limit(word, extra, mode):
    control = TextBuilder().pronunciation(word, "test").build()
    builder = TextBuilder().text("x" * (2000 - len(word) + extra))
    if mode == "fluent":
        builder.pronunciation(word, "test")
    elif mode == "inline":
        builder.text(control)
    else:
        builder.from_ssml(f'<phoneme alphabet="ipa" ph="test">{word}</phoneme>')
    if extra:
        with pytest.raises(ValueError, match="current: 2001 characters"):
            builder.build()
    else:
        assert builder.build().endswith(control)
