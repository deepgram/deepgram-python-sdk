"""
TTS Text Builder and Utilities

Provides helper methods for constructing TTS text with pronunciation, pause,
and speed controls for Deepgram's Text-to-Speech API.
"""

import json
import re
from typing import Tuple


class TextBuilder:
    """
    Fluent builder for constructing TTS text with pronunciation and pause controls.
    
    Example:
        text = TextBuilder() \\
            .text("Take ") \\
            .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn") \\
            .text(" twice daily with ") \\
            .pronunciation("dupilumab", "duːˈpɪljuːmæb") \\
            .text(" injections") \\
            .pause(500) \\
            .text(" Do not exceed prescribed dosage.") \\
            .build()
    """

    def __init__(self):
        """Initialize empty text builder."""
        self._parts = []
        self._pronunciation_count = 0
        self._pause_count = 0
        self._char_count = 0

    def text(self, content: str) -> "TextBuilder":
        """
        Add plain text. Returns self for chaining.

        Args:
            content: Plain text to add

        Returns:
            Self for method chaining
        """
        if content:
            self._parts.append(content)
            self._char_count += len(content)
        return self

    def pronunciation(self, word: str, ipa: str) -> "TextBuilder":
        """
        Add a word with custom pronunciation.
        Formats as: {"word": "word", "pronounce":"ipa"}
        Returns self for chaining.

        Args:
            word: The word to be pronounced
            ipa: IPA pronunciation string

        Returns:
            Self for method chaining

        Raises:
            ValueError: If pronunciation limit exceeded or validation fails
        """
        # Validate IPA
        is_valid, error_msg = validate_ipa(ipa)
        if not is_valid:
            raise ValueError(error_msg)

        # Check pronunciation limit
        if self._pronunciation_count >= 500:
            raise ValueError("Maximum 500 pronunciations per request exceeded")

        # Format as JSON (ensure proper escaping)
        pronunciation_json = json.dumps({"word": word, "pronounce": ipa}, ensure_ascii=False)
        self._parts.append(pronunciation_json)
        self._pronunciation_count += 1
        self._char_count += len(word)  # Count original word, not IPA

        return self

    def pause(self, duration_ms: int) -> "TextBuilder":
        """
        Add a pause in milliseconds.
        Formats as: {pause:duration_ms}
        Valid range: 500-5000ms in 100ms increments.
        Returns self for chaining.

        Args:
            duration_ms: Pause duration in milliseconds (500-5000, increments of 100)

        Returns:
            Self for method chaining

        Raises:
            ValueError: If pause limit exceeded or validation fails
        """
        # Validate pause
        is_valid, error_msg = validate_pause(duration_ms)
        if not is_valid:
            raise ValueError(error_msg)

        # Check pause limit
        if self._pause_count >= 50:
            raise ValueError("Maximum 50 pauses per request exceeded")

        # Format as JSON-style pause marker
        self._parts.append(f"{{pause:{duration_ms}}}")
        self._pause_count += 1

        return self

    def from_ssml(self, ssml_text: str) -> "TextBuilder":
        """
        Parse SSML and convert to Deepgram's inline format.
        Supports:
        - <phoneme alphabet="ipa" ph="...">word</phoneme> → pronunciation()
        - <break time="500ms"/> → pause()
        - Plain text → text()
        Returns self for chaining.

        Args:
            ssml_text: SSML-formatted text

        Returns:
            Self for method chaining
        """
        # Convert SSML to Deepgram format and append
        converted = ssml_to_deepgram(ssml_text)
        if converted:
            self._parts.append(converted)
            # Update counters by parsing the converted text
            self._update_counts_from_text(converted)

        return self

    def _update_counts_from_text(self, text: str) -> None:
        """Update internal counters from parsed text."""
        # Count pronunciations (JSON objects with "word" and "pronounce")
        pronunciation_pattern = r'\{"word":\s*"[^"]*",\s*"pronounce":\s*"[^"]*"\}'
        pronunciations = re.findall(pronunciation_pattern, text)
        self._pronunciation_count += len(pronunciations)

        # Count pauses
        pause_pattern = r"\{pause:\d+\}"
        pauses = re.findall(pause_pattern, text)
        self._pause_count += len(pauses)

        # Character count (approximate - remove control syntax)
        clean_text = re.sub(pronunciation_pattern, "", text)
        clean_text = re.sub(pause_pattern, "", clean_text)
        self._char_count += len(clean_text)

    def build(self) -> str:
        """
        Return the final formatted text string.

        Returns:
            The complete formatted text ready for TTS

        Raises:
            ValueError: If character limit exceeded
        """
        result = "".join(self._parts)

        # Validate character count (2000 max, excluding control syntax)
        if self._char_count > 2000:
            raise ValueError(f"Text exceeds 2000 character limit (current: {self._char_count} characters)")

        return result


def add_pronunciation(text: str, word: str, ipa: str) -> str:
    """
    Replace word in text with pronunciation control.

    Args:
        text: Source text containing the word
        word: Word to replace
        ipa: IPA pronunciation string

    Returns:
        Text with word replaced by {"word": "word", "pronounce":"ipa"}

    Example:
        text = "Take azathioprine twice daily with dupilumab injections."
        text = add_pronunciation(text, "azathioprine", "ˌæzəˈθaɪəpriːn")
        text = add_pronunciation(text, "dupilumab", "duːˈpɪljuːmæb")
    """
    # Validate IPA
    is_valid, error_msg = validate_ipa(ipa)
    if not is_valid:
        raise ValueError(error_msg)

    # Create pronunciation JSON
    pronunciation_json = json.dumps({"word": word, "pronounce": ipa}, ensure_ascii=False)

    # Replace word with pronunciation (case-sensitive, whole word only)
    pattern = r"\b" + re.escape(word) + r"\b"
    result = re.sub(pattern, pronunciation_json, text, count=1)

    return result


def ssml_to_deepgram(ssml_text: str) -> str:
    """
    Convert SSML markup to Deepgram's inline JSON format.

    Supports:
    - <phoneme alphabet="ipa" ph="...">word</phoneme>
    - <break time="500ms"/> or <break time="0.5s"/>
    - Strips <speak> wrapper tags

    Args:
        ssml_text: SSML-formatted text

    Returns:
        Deepgram-formatted text

    Example:
        ssml = '''<speak>
            Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>
            <break time="500ms"/> Do not exceed dosage.
        </speak>'''
        text = ssml_to_deepgram(ssml)
    """
    # Strip leading/trailing whitespace
    ssml_text = ssml_text.strip()

    # If wrapped in <speak> tags, extract content
    speak_pattern = r"<speak[^>]*>(.*?)</speak>"
    speak_match = re.search(speak_pattern, ssml_text, re.DOTALL)
    if speak_match:
        ssml_text = speak_match.group(1)

    # Process the SSML text
    # Parse XML fragments manually to handle mixed content
    # Use regex to find and replace SSML elements

    # Handle <phoneme> tags
    phoneme_pattern = r'<phoneme\s+alphabet=["\']ipa["\']\s+ph=["\'](.*?)["\']\s*>(.*?)</phoneme>'

    def replace_phoneme(match):
        ipa = match.group(1)
        word = match.group(2)
        return json.dumps({"word": word, "pronounce": ipa}, ensure_ascii=False)

    ssml_text = re.sub(phoneme_pattern, replace_phoneme, ssml_text)

    # Handle <break> tags
    break_pattern = r'<break\s+time=["\'](\d+(?:\.\d+)?)(ms|s)["\']\s*/>'

    def replace_break(match):
        value = float(match.group(1))
        unit = match.group(2)

        # Convert to milliseconds
        if unit == "s":
            duration_ms = int(value * 1000)
        else:
            duration_ms = int(value)

        # Validate
        is_valid, error_msg = validate_pause(duration_ms)
        if not is_valid:
            # Round to nearest valid value
            duration_ms = max(500, min(5000, round(duration_ms / 100) * 100))

        return f"{{pause:{duration_ms}}}"

    ssml_text = re.sub(break_pattern, replace_break, ssml_text)

    # Remove any remaining XML tags
    ssml_text = re.sub(r"<[^>]+>", "", ssml_text)

    return ssml_text.strip()


def validate_ipa(ipa: str) -> Tuple[bool, str]:
    """
    Validate IPA string format.

    Args:
        ipa: IPA pronunciation string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not ipa:
        return False, "IPA pronunciation cannot be empty"

    if not isinstance(ipa, str):
        return False, "IPA pronunciation must be a string"

    # IPA should not contain certain characters that would break JSON
    invalid_chars = ['"', "\\", "\n", "\r", "\t"]
    for char in invalid_chars:
        if char in ipa:
            return False, f"IPA pronunciation contains invalid character: {repr(char)}"

    # IPA should be reasonable length (max 100 characters)
    if len(ipa) > 100:
        return False, "IPA pronunciation exceeds 100 character limit"

    return True, ""


def validate_pause(duration_ms: int) -> Tuple[bool, str]:
    """
    Validate pause duration (500-5000ms, 100ms increments).

    Args:
        duration_ms: Pause duration in milliseconds

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(duration_ms, int):
        return False, "Pause duration must be an integer"

    if duration_ms < 500:
        return False, "Pause duration must be at least 500ms"

    if duration_ms > 5000:
        return False, "Pause duration must not exceed 5000ms"

    if duration_ms % 100 != 0:
        return False, "Pause duration must be in 100ms increments"

    return True, ""
