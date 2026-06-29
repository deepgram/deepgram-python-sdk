---
title: "Text Builder"
description: "Use the TextBuilder helper to assemble Deepgram TTS markup with pronunciations, pauses, and SSML conversion."
---

`TextBuilder` is the main hand-written helper outside the root client layer. It exists because Deepgram's text-to-speech APIs support inline pronunciation and pause controls, but writing those control markers by hand is error-prone.

## What It Is

The helper lives in `src/deepgram/helpers/text_builder.py` and is exported through `deepgram.helpers`. It solves three problems:

- building inline pronunciation JSON snippets without manual string escaping,
- validating pause durations and IPA values before you hit the API,
- converting a small SSML subset into Deepgram's inline TTS format.

It relates directly to `client.speak.v1.audio.generate(...)` and `client.speak.v1.connect(...)`, because those methods ultimately need a text string that may contain pronunciation and pause controls.

## How It Works Internally

`TextBuilder` keeps an internal `_parts` list plus counters for pronunciations, pauses, and effective character count. `pronunciation(...)` validates IPA with `validate_ipa(...)`, enforces a 500-pronunciation limit, JSON-encodes the control block, and increments the logical character count by the original word length. `pause(...)` validates the range and increment rules, enforces a 50-pause limit, and appends a `{pause:duration}` marker.

`from_ssml(...)` calls `ssml_to_deepgram(...)`, which strips an outer `<speak>` tag, converts IPA `<phoneme>` tags into inline JSON markers, and maps `<break time="..."/>` tags into pause markers. `build()` finally joins the parts and raises if the effective text exceeds 2000 characters.

```mermaid
flowchart TD
  A[TextBuilder] --> B[text()]
  A --> C[pronunciation()]
  A --> D[pause()]
  A --> E[from_ssml()]
  B --> F[_parts]
  C --> F
  D --> F
  E --> F
  F --> G[build()]
  G --> H[Deepgram TTS-ready string]
```

## Basic Usage

```python
from deepgram.helpers import TextBuilder

text = (
    TextBuilder()
    .text("Take ")
    .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
    .text(" twice daily.")
    .pause(500)
    .text(" Do not exceed the prescribed dosage.")
    .build()
)
```

## Advanced Usage

```python
from deepgram.helpers import TextBuilder

ssml = """
<speak>
  Welcome back.
  <break time="700ms"/>
  The drug name is <phoneme alphabet="ipa" ph="ˌædəˈljuːməb">adalimumab</phoneme>.
</speak>
"""

text = TextBuilder().from_ssml(ssml).build()
print(text)
```

<Callout type="warn">The helper enforces limits in user space before you call the API: maximum 500 pronunciations, maximum 50 pauses, and maximum 2000 effective characters. Pause duration must stay between 500 and 5000 milliseconds in 100-millisecond increments, so `pause(750)` is invalid even though it looks reasonable.</Callout>

## When To Use It

Use `TextBuilder` any time your application needs stable pronunciation for medical, legal, or brand terminology. It is also the best path when your source material begins as SSML but your delivery target is Deepgram's inline TTS format. If you only ever send plain text, the helper is optional.

## Trade-Offs

<Accordions>
<Accordion title="TextBuilder vs writing inline markers manually">
Manual inline markers give you total control over the final string, but they are also easy to break because you have to keep JSON escaping, pause syntax, and character limits straight yourself. `TextBuilder` trades some raw flexibility for safer composition and better validation, which is almost always the right trade in production code. It also makes intent obvious when another engineer reads the code, because `pronunciation(...)` communicates meaning more clearly than a pasted JSON fragment inside a long string. Manual formatting is still acceptable for tiny one-off demos, but it scales poorly once you have many terms to control.
</Accordion>
<Accordion title="SSML conversion vs authoring Deepgram format directly">
SSML conversion is useful when content already comes from another speech system or a CMS that stores SSML fragments. It lets you preserve upstream authoring patterns while still targeting Deepgram's TTS API, and the conversion step is intentionally narrow so the supported tags are predictable. Authoring the Deepgram format directly is simpler when your application owns the content end to end and only needs pronunciations and pauses. In that case, `text()`, `pronunciation()`, and `pause()` are usually clearer than maintaining a parallel SSML representation.
</Accordion>
</Accordions>
