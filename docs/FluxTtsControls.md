# Flux TTS Controls

Pronunciation controls apply to Flux batch REST, Flux WebSocket, and Aura-2 `/v1/speak`. Pause controls apply to Flux batch REST only.

## Batch REST

Use `client.speak.v2.audio.generate()` for complete text. A pause is written as `\{pause:500ms\}` through `\{pause:3000ms\}` in 100 ms increments. A request accepts at most eight pauses. `TextBuilder` emits and validates this Flux batch syntax.

Pronunciation uses `\{"word": "...", "pronounce": "<IPA>"\}` and is Early Access. A pronunciation cannot be combined with any pause or with `speed` other than `1.0`. When a pause is present, `speed` cannot exceed `1.15`. Invalid combinations return a batch error, including `CONTROL_COMBINATION_INVALID` or `PAUSE_SPEED_CAP_EXCEEDED`.

Read batch control outcomes from raw response headers: `dg-pronunciations-applied`, `dg-breaks-applied`, and `dg-warnings`. Warnings report best-effort pronunciation handling.

## WebSocket

Use `client.speak.v2.connect()` for streaming Flux synthesis. WebSocket turns support pronunciation controls only. A pause marker such as `\{pause:500ms\}`, or a pronunciation marker such as `\{"word": "...", "pronounce": "<IPA>"\}` combined with non-default speed, closes the connection with `DATA-0002`.

`Configure` changes are buffered. Setting speed while a buffered turn contains pronunciation returns `ConfigureFailure` with `CONTROL_COMBINATION_INVALID`; flush that turn before changing speed.

`SpeechMetadata.controls_applied` reports pronunciation, pause, and warning counters. `Warning` messages report the associated warning code and description. WebSocket pauses are unsupported, so `breaks_applied` is always zero.

`TextBuilder` validates Flux batch constraints. Its pronunciation output is usable where pronunciation controls are supported, but do not use its pause output with the Flux WebSocket or assume Flux pause limits apply to non-Flux TTS endpoints.
