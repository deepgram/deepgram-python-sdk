"""
Tests for TextBuilder and TTS helper utilities
"""

import pytest
from deepgram.helpers import (
    TextBuilder,
    add_pronunciation,
    ssml_to_deepgram,
    validate_ipa,
    validate_pause,
)


class TestTextBuilder:
    """Tests for the TextBuilder class"""
    
    def test_basic_text(self):
        """Test adding plain text"""
        builder = TextBuilder()
        result = builder.text("Hello world").build()
        assert result == "Hello world"
    
    def test_multiple_text_parts(self):
        """Test chaining multiple text parts"""
        builder = TextBuilder()
        result = builder.text("Hello ").text("world").build()
        assert result == "Hello world"
    
    def test_pronunciation(self):
        """Test adding pronunciation"""
        builder = TextBuilder()
        result = builder.pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn").build()
        assert '"word": "azathioprine"' in result
        assert '"pronounce": "ˌæzəˈθaɪəpriːn"' in result
    
    def test_text_with_pronunciation(self):
        """Test mixing text and pronunciation"""
        builder = TextBuilder()
        result = (
            builder
            .text("Take ")
            .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
            .text(" twice daily")
            .build()
        )
        assert "Take " in result
        assert '"word": "azathioprine"' in result
        assert " twice daily" in result
    
    def test_pause(self):
        """Test adding pause"""
        builder = TextBuilder()
        result = builder.pause(500).build()
        assert result == "{pause:500}"
    
    def test_text_with_pause(self):
        """Test mixing text and pause"""
        builder = TextBuilder()
        result = (
            builder
            .text("Hello")
            .pause(1000)
            .text("world")
            .build()
        )
        assert result == "Hello{pause:1000}world"
    
    def test_complex_chain(self):
        """Test complex chaining with all features"""
        builder = TextBuilder()
        result = (
            builder
            .text("Take ")
            .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
            .text(" twice daily with ")
            .pronunciation("dupilumab", "duːˈpɪljuːmæb")
            .text(" injections")
            .pause(500)
            .text(" Do not exceed prescribed dosage.")
            .build()
        )
        
        assert "Take " in result
        assert '"word": "azathioprine"' in result
        assert " twice daily with " in result
        assert '"word": "dupilumab"' in result
        assert " injections" in result
        assert "{pause:500}" in result
        assert " Do not exceed prescribed dosage." in result
    
    def test_pronunciation_limit(self):
        """Test pronunciation count limit (500 max)"""
        builder = TextBuilder()
        
        # Add 500 pronunciations (should work)
        for i in range(500):
            builder.pronunciation(f"word{i}", "test")
        
        # 501st should raise error
        with pytest.raises(ValueError, match="Maximum 500 pronunciations"):
            builder.pronunciation("extra", "test")
    
    def test_pause_limit(self):
        """Test pause count limit (50 max)"""
        builder = TextBuilder()
        
        # Add 50 pauses (should work)
        for i in range(50):
            builder.pause(500)
        
        # 51st should raise error
        with pytest.raises(ValueError, match="Maximum 50 pauses"):
            builder.pause(500)
    
    def test_character_limit(self):
        """Test character count validation (2000 max)"""
        builder = TextBuilder()
        
        # Add text approaching the limit
        builder.text("x" * 2000)
        
        # Should work at exactly 2000
        result = builder.build()
        assert len(result) == 2000
        
        # Exceeding should raise error
        builder2 = TextBuilder()
        builder2.text("x" * 2001)
        with pytest.raises(ValueError, match="exceeds 2000 character limit"):
            builder2.build()
    
    def test_empty_builder(self):
        """Test building with no content"""
        builder = TextBuilder()
        result = builder.build()
        assert result == ""
    
    def test_invalid_ipa(self):
        """Test validation of IPA pronunciation"""
        builder = TextBuilder()
        
        # Should reject IPA with invalid characters
        with pytest.raises(ValueError, match="invalid character"):
            builder.pronunciation("word", 'invalid"quote')
        
        with pytest.raises(ValueError, match="invalid character"):
            builder.pronunciation("word", "invalid\nline")
    
    def test_invalid_pause_duration(self):
        """Test pause duration validation"""
        builder = TextBuilder()
        
        # Too short
        with pytest.raises(ValueError, match="at least 500ms"):
            builder.pause(400)
        
        # Too long
        with pytest.raises(ValueError, match="not exceed 5000ms"):
            builder.pause(5001)
        
        # Not in 100ms increments
        with pytest.raises(ValueError, match="100ms increments"):
            builder.pause(550)
    
    def test_pause_boundary_values(self):
        """Test pause at valid boundaries"""
        builder = TextBuilder()
        
        # Minimum valid
        result1 = builder.pause(500).build()
        assert "{pause:500}" in result1
        
        # Maximum valid
        builder2 = TextBuilder()
        result2 = builder2.pause(5000).build()
        assert "{pause:5000}" in result2


class TestAddPronunciation:
    """Tests for the add_pronunciation function"""
    
    def test_basic_replacement(self):
        """Test basic word replacement"""
        text = "Take azathioprine twice daily."
        result = add_pronunciation(text, "azathioprine", "ˌæzəˈθaɪəpriːn")
        
        assert '"word": "azathioprine"' in result
        assert '"pronounce": "ˌæzəˈθaɪəpriːn"' in result
        assert "Take " in result
        assert " twice daily." in result
    
    def test_multiple_replacements(self):
        """Test replacing multiple words"""
        text = "Take azathioprine twice daily with dupilumab injections."
        text = add_pronunciation(text, "azathioprine", "ˌæzəˈθaɪəpriːn")
        text = add_pronunciation(text, "dupilumab", "duːˈpɪljuːmæb")
        
        assert '"word": "azathioprine"' in text
        assert '"word": "dupilumab"' in text
    
    def test_whole_word_only(self):
        """Test that replacement only affects whole words"""
        text = "The therapist prescribed therapy."
        result = add_pronunciation(text, "The", "ðiː")
        
        # Should only replace "The", not "the" in "therapist" or "therapy"
        assert result.count('"word"') == 1
        assert "therapist" in result
        assert "therapy" in result
    
    def test_case_sensitive(self):
        """Test that replacement is case-sensitive"""
        text = "Take azathioprine. AZATHIOPRINE is different."
        result = add_pronunciation(text, "azathioprine", "test")
        
        # Should only replace lowercase version (first occurrence)
        assert result.count('"word"') == 1
        assert "AZATHIOPRINE" in result
    
    def test_word_not_found(self):
        """Test replacement when word is not in text"""
        text = "Hello world"
        result = add_pronunciation(text, "missing", "test")
        
        # Text should be unchanged
        assert result == text


class TestSsmlToDeepgram:
    """Tests for SSML conversion"""
    
    def test_basic_phoneme(self):
        """Test converting basic phoneme tag"""
        ssml = '<phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>'
        result = ssml_to_deepgram(ssml)
        
        assert '"word": "azathioprine"' in result
        assert '"pronounce": "ˌæzəˈθaɪəpriːn"' in result
    
    def test_basic_break(self):
        """Test converting break tag (milliseconds)"""
        ssml = '<break time="500ms"/>'
        result = ssml_to_deepgram(ssml)
        
        assert result == "{pause:500}"
    
    def test_break_seconds(self):
        """Test converting break tag (seconds)"""
        ssml = '<break time="0.5s"/>'
        result = ssml_to_deepgram(ssml)
        
        assert result == "{pause:500}"
    
    def test_speak_wrapper(self):
        """Test handling <speak> wrapper tag"""
        ssml = '<speak>Hello world</speak>'
        result = ssml_to_deepgram(ssml)
        
        assert result == "Hello world"
    
    def test_complex_ssml(self):
        """Test complex SSML with multiple elements"""
        ssml = '''<speak>
            Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>
            <break time="500ms"/> Do not exceed dosage.
        </speak>'''
        result = ssml_to_deepgram(ssml)
        
        assert '"word": "azathioprine"' in result
        assert "{pause:500}" in result
        assert "Do not exceed dosage." in result
    
    def test_multiple_phonemes(self):
        """Test multiple phoneme tags"""
        ssml = '''Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme> 
                  with <phoneme alphabet="ipa" ph="duːˈpɪljuːmæb">dupilumab</phoneme>'''
        result = ssml_to_deepgram(ssml)
        
        assert '"word": "azathioprine"' in result
        assert '"word": "dupilumab"' in result
    
    def test_plain_text(self):
        """Test plain text without SSML tags"""
        text = "Hello world"
        result = ssml_to_deepgram(text)
        
        assert result == text
    
    def test_break_out_of_range(self):
        """Test break with out-of-range duration (should round to valid)"""
        ssml = '<break time="250ms"/>'
        result = ssml_to_deepgram(ssml)
        
        # Should round to nearest valid value (500ms)
        assert "{pause:" in result


class TestFromSsml:
    """Tests for TextBuilder.from_ssml() method"""
    
    def test_from_ssml_basic(self):
        """Test parsing SSML into builder"""
        ssml = '<speak>Hello world</speak>'
        builder = TextBuilder()
        result = builder.from_ssml(ssml).build()
        
        assert "Hello world" in result
    
    def test_from_ssml_with_additional_text(self):
        """Test mixing SSML parsing with additional builder methods"""
        ssml = '<speak>Take <phoneme alphabet="ipa" ph="test">medicine</phoneme></speak>'
        builder = TextBuilder()
        result = (
            builder
            .from_ssml(ssml)
            .pause(500)
            .text(" Do not exceed dosage.")
            .build()
        )
        
        assert '"word": "medicine"' in result
        assert "{pause:500}" in result
        assert "Do not exceed dosage." in result
    
    def test_from_ssml_counts_pronunciations(self):
        """Test that from_ssml updates internal counters"""
        # Create SSML with pronunciations
        pronunciations = ''.join([
            f'<phoneme alphabet="ipa" ph="test">word{i}</phoneme> '
            for i in range(500)
        ])
        ssml = f'<speak>{pronunciations}</speak>'
        
        builder = TextBuilder()
        builder.from_ssml(ssml)
        
        # Should hit the limit
        with pytest.raises(ValueError, match="Maximum 500 pronunciations"):
            builder.pronunciation("extra", "test")


class TestValidateIpa:
    """Tests for IPA validation"""
    
    def test_valid_ipa(self):
        """Test valid IPA strings"""
        is_valid, msg = validate_ipa("ˌæzəˈθaɪəpriːn")
        assert is_valid is True
        assert msg == ""
    
    def test_empty_ipa(self):
        """Test empty IPA string"""
        is_valid, msg = validate_ipa("")
        assert is_valid is False
        assert "cannot be empty" in msg
    
    def test_invalid_characters(self):
        """Test IPA with invalid characters"""
        # Double quote
        is_valid, msg = validate_ipa('test"quote')
        assert is_valid is False
        assert "invalid character" in msg
        
        # Newline
        is_valid, msg = validate_ipa("test\nline")
        assert is_valid is False
        assert "invalid character" in msg
    
    def test_too_long(self):
        """Test IPA exceeding length limit"""
        is_valid, msg = validate_ipa("x" * 101)
        assert is_valid is False
        assert "exceeds 100 character limit" in msg
    
    def test_not_string(self):
        """Test non-string IPA"""
        is_valid, msg = validate_ipa(123)
        assert is_valid is False
        assert "must be a string" in msg


class TestValidatePause:
    """Tests for pause validation"""
    
    def test_valid_pauses(self):
        """Test valid pause durations"""
        # Minimum
        is_valid, msg = validate_pause(500)
        assert is_valid is True
        
        # Maximum
        is_valid, msg = validate_pause(5000)
        assert is_valid is True
        
        # Mid-range
        is_valid, msg = validate_pause(2500)
        assert is_valid is True
    
    def test_too_short(self):
        """Test pause below minimum"""
        is_valid, msg = validate_pause(400)
        assert is_valid is False
        assert "at least 500ms" in msg
    
    def test_too_long(self):
        """Test pause above maximum"""
        is_valid, msg = validate_pause(5001)
        assert is_valid is False
        assert "not exceed 5000ms" in msg
    
    def test_invalid_increment(self):
        """Test pause not in 100ms increments"""
        is_valid, msg = validate_pause(550)
        assert is_valid is False
        assert "100ms increments" in msg
    
    def test_not_integer(self):
        """Test non-integer pause"""
        is_valid, msg = validate_pause(500.5)
        assert is_valid is False
        assert "must be an integer" in msg


class TestIntegration:
    """Integration tests combining multiple features"""
    
    def test_medical_example(self):
        """Test the medical prescription example from the spec"""
        text = (
            TextBuilder()
            .text("Take ")
            .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
            .text(" twice daily with ")
            .pronunciation("dupilumab", "duːˈpɪljuːmæb")
            .text(" injections")
            .pause(500)
            .text(" Do not exceed prescribed dosage.")
            .build()
        )
        
        # Verify all components are present
        assert "Take " in text
        assert '"word": "azathioprine"' in text
        assert '"pronounce": "ˌæzəˈθaɪəpriːn"' in text
        assert " twice daily with " in text
        assert '"word": "dupilumab"' in text
        assert '"pronounce": "duːˈpɪljuːmæb"' in text
        assert " injections" in text
        assert "{pause:500}" in text
        assert " Do not exceed prescribed dosage." in text
    
    def test_ssml_migration(self):
        """Test SSML to Deepgram migration workflow"""
        ssml = '''<speak>
            Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>
            <break time="500ms"/> Do not exceed dosage.
        </speak>'''
        
        # Method 1: Direct conversion
        text1 = ssml_to_deepgram(ssml)
        
        # Method 2: Using builder
        text2 = TextBuilder().from_ssml(ssml).build()
        
        # Both should produce similar results
        assert '"word": "azathioprine"' in text1
        assert "{pause:500}" in text1
        assert '"word": "azathioprine"' in text2
        assert "{pause:500}" in text2
    
    def test_builder_with_ssml_and_additions(self):
        """Test the mixed usage example from the spec"""
        some_imported_ssml = '''<speak>
            Take <phoneme alphabet="ipa" ph="test">medicine</phoneme>
        </speak>'''
        
        text = (
            TextBuilder()
            .from_ssml(some_imported_ssml)
            .pause(500)
            .text(" Do not exceed prescribed dosage.")
            .build()
        )
        
        assert '"word": "medicine"' in text
        assert "{pause:500}" in text
        assert " Do not exceed prescribed dosage." in text
    
    def test_standalone_function_workflow(self):
        """Test using standalone add_pronunciation function"""
        text = "Take azathioprine twice daily with dupilumab injections."
        text = add_pronunciation(text, "azathioprine", "ˌæzəˈθaɪəpriːn")
        text = add_pronunciation(text, "dupilumab", "duːˈpɪljuːmæb")
        
        assert '"word": "azathioprine"' in text
        assert '"pronounce": "ˌæzəˈθaɪəpriːn"' in text
        assert '"word": "dupilumab"' in text
        assert '"pronounce": "duːˈpɪljuːmæb"' in text

