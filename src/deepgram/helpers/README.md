# Deepgram SDK Helpers

This module contains custom helper utilities for working with Deepgram APIs that are not auto-generated.

## TextBuilder

The `TextBuilder` class provides a fluent interface for constructing English Flux batch TTS text. Pronunciation controls also apply to Flux WebSocket and Aura-2 `/v1/speak`; pauses are Flux batch-only and are rejected by Flux WebSocket with `DATA-0002`.

### Quick Example

```python
from deepgram import DeepgramClient
from deepgram.helpers import TextBuilder

# Build text with pronunciations and pauses
text = (
    TextBuilder()
    .text("Take ")
    .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
    .text(" twice daily.")
    .build()
)

# Use with English Flux batch TTS
client = DeepgramClient(api_key="YOUR_API_KEY")
audio = client.speak.v2.audio.generate(model="flux-alexis-en", text=text)
```

### Available Functions

#### TextBuilder Class

- `text(content: str)` - Add plain text
- `pronunciation(word: str, ipa: str)` - Add an escaped `\{"word": "...", "pronounce": "..."\}` IPA pronunciation control
- `pause(duration_ms: int)` - Add a batch-only `\{pause:<N>ms\}` pause (500-3000ms, 100ms increments; eight per request)
- `from_ssml(ssml_text: str)` - Parse and convert SSML markup
- `build()` - Return final formatted text

#### Standalone Functions

- `add_pronunciation(text, word, ipa)` - Replace a word with an escaped pronunciation control
- `ssml_to_deepgram(ssml_text)` - Convert SSML to escaped Deepgram controls
- `validate_ipa(ipa)` - Validate IPA pronunciation string
- `validate_pause(duration_ms)` - Validate pause duration

### Documentation

See [FluxTtsControls.md](../../../docs/FluxTtsControls.md) for control combinations, English-only batch support, and WebSocket restrictions.

### Examples

See [23-text-builder-helper.py](../../../examples/23-text-builder-helper.py) for a batch example and [the live controls check](../../../tests/manual/speak/v2/controls/main.py) for server validation.

## Future Helpers

This module may be extended with additional helper utilities for other Deepgram features.
