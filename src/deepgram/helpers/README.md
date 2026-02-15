# Deepgram SDK Helpers

This module contains custom helper utilities for working with Deepgram APIs that are not auto-generated.

## TextBuilder

The `TextBuilder` class provides a fluent interface for constructing Text-to-Speech (TTS) text with pronunciation and pause controls.

### Quick Example

```python
from deepgram import DeepgramClient
from deepgram.helpers import TextBuilder

# Build text with pronunciations and pauses
text = (
    TextBuilder()
    .text("Take ")
    .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
    .pause(500)
    .text(" twice daily.")
    .build()
)

# Use with Deepgram TTS
client = DeepgramClient(api_key="YOUR_API_KEY")
response = client.speak.v1.generate(text, model="aura-asteria-en")
```

### Available Functions

#### TextBuilder Class

- `text(content: str)` - Add plain text
- `pronunciation(word: str, ipa: str)` - Add word with IPA pronunciation
- `pause(duration_ms: int)` - Add pause (500-5000ms, 100ms increments)
- `from_ssml(ssml_text: str)` - Parse and convert SSML markup
- `build()` - Return final formatted text

#### Standalone Functions

- `add_pronunciation(text, word, ipa)` - Replace word with pronunciation
- `ssml_to_deepgram(ssml_text)` - Convert SSML to Deepgram format
- `validate_ipa(ipa)` - Validate IPA pronunciation string
- `validate_pause(duration_ms)` - Validate pause duration

### Documentation

See [TextBuilder-Guide.md](../../../docs/TextBuilder-Guide.md) for comprehensive documentation.

### Examples

See [examples/25-text-builder-helper.py](../../../examples/25-text-builder-helper.py) for usage examples.

## Future Helpers

This module may be extended with additional helper utilities for other Deepgram features.
