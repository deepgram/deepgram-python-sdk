# Changelog

## [6.0.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.7.0...v6.0.0) (2026-08-12)


### ⚠ BREAKING CHANGES

* sdk regeneration 2026-04-24 ([#696](https://github.com/deepgram/deepgram-python-sdk/issues/696))
* sdk regeneration 2026-04-14 ([#690](https://github.com/deepgram/deepgram-python-sdk/issues/690))
* promote v6.0.0-rc.2 to v6.0.0 stable
* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640))
* This is a significant breaking change, and should be carried out in conjunction with our migration guide.

### Features

* (regen) diarization v2 batch GA, listen-provider dedup, think/models route fix ([#714](https://github.com/deepgram/deepgram-python-sdk/issues/714)) ([9d9a43d](https://github.com/deepgram/deepgram-python-sdk/commit/9d9a43dbc2bd739068b05e5d136f487b56ef5b7c))
* add declarative reconnect flag with transport-factory auto-disable ([#720](https://github.com/deepgram/deepgram-python-sdk/issues/720)) ([b5d5905](https://github.com/deepgram/deepgram-python-sdk/commit/b5d590577429adeacfe2068df4c33201a158c9de))
* Add dictation option to LiveOptions class ([8939e59](https://github.com/deepgram/deepgram-python-sdk/commit/8939e5960d4d11122db9a261ee9c237dfd3081d7))
* Add dictation option to LiveOptions class ([d3b2dcc](https://github.com/deepgram/deepgram-python-sdk/commit/d3b2dcc6867cfe0f73f3af472edc60176745aacb))
* add projects billing fields list methods ([#621](https://github.com/deepgram/deepgram-python-sdk/issues/621)) ([10d67cd](https://github.com/deepgram/deepgram-python-sdk/commit/10d67cd91aef1436a9e85e3b607dc7b81eebba43))
* add support for agent tags ([#559](https://github.com/deepgram/deepgram-python-sdk/issues/559)) ([d605248](https://github.com/deepgram/deepgram-python-sdk/commit/d605248f472945c0dead41391bdcce57212a0e3e))
* adds support for agent mip_opt_out ([#558](https://github.com/deepgram/deepgram-python-sdk/issues/558)) ([3e8a3dd](https://github.com/deepgram/deepgram-python-sdk/commit/3e8a3dd4dc4b191e9eea815502cb52caa0cc7a88))
* Adds support for IUM ([#546](https://github.com/deepgram/deepgram-python-sdk/issues/546)) ([232ee05](https://github.com/deepgram/deepgram-python-sdk/commit/232ee0579a8b3685157c372a18f0271924ffaf35))
* adds support for speak fallback ([#548](https://github.com/deepgram/deepgram-python-sdk/issues/548)) ([cab41fa](https://github.com/deepgram/deepgram-python-sdk/commit/cab41facb615fa2784cb78c51cbd3ecc3254a890))
* adds ttl_seconds support ([#557](https://github.com/deepgram/deepgram-python-sdk/issues/557)) ([e9bedf2](https://github.com/deepgram/deepgram-python-sdk/commit/e9bedf2ecf02673dba7256719efe9d917a2d1610))
* **agent:** support multi-provider speak/think configuration and typed listen parameters ([#676](https://github.com/deepgram/deepgram-python-sdk/issues/676)) ([5dfb1aa](https://github.com/deepgram/deepgram-python-sdk/commit/5dfb1aa9a2357f8cfc0e08f55284fd8521446bf7))
* apply latest spec changes ([4ad9eb7](https://github.com/deepgram/deepgram-python-sdk/commit/4ad9eb75ae74c0e840ffc0b34d31abbe0ee5fb3a))
* **auth:** adding token-based auth to the SDK so access tokens can be used in requests ([#543](https://github.com/deepgram/deepgram-python-sdk/issues/543)) ([1200c83](https://github.com/deepgram/deepgram-python-sdk/commit/1200c832fc28b366405bdead7e82ae06abc74308))
* **helpers:** add TextBuilder class for TTS pronunciation and pause controls ([#660](https://github.com/deepgram/deepgram-python-sdk/issues/660)) ([4324120](https://github.com/deepgram/deepgram-python-sdk/commit/43241200a7e025bdc4633bdb47f6708921c82ad1))
* implements new generated SDK architecture, all call signatures ([#572](https://github.com/deepgram/deepgram-python-sdk/issues/572)) ([768d514](https://github.com/deepgram/deepgram-python-sdk/commit/768d51492bf7414067266cdc2cf7b98f1f3981dc))
* make all providers generic ([2c92d67](https://github.com/deepgram/deepgram-python-sdk/commit/2c92d676a8611e997c2abde05943df092644f7ea))
* make provider objects generic ([4521048](https://github.com/deepgram/deepgram-python-sdk/commit/45210488c05b2aad5db3671c732888542a5afe91))
* mention keep alive in migration guide ([#594](https://github.com/deepgram/deepgram-python-sdk/issues/594)) ([5a8c79e](https://github.com/deepgram/deepgram-python-sdk/commit/5a8c79e814e3efeb81a8c51a0a05d93bc17e6bb5))
* officially enable aura-2 in live text-to-speech ([052aadd](https://github.com/deepgram/deepgram-python-sdk/commit/052aaddd9ff17dd4acfccbac0dcaa66c792d63f0))
* officially enable aura-2 in live text-to-speech ([ba4124a](https://github.com/deepgram/deepgram-python-sdk/commit/ba4124a503376b2cf22fae6e87ab59de18c59c22))
* promote v6.0.0-rc.2 to v6.0.0 stable ([34f543e](https://github.com/deepgram/deepgram-python-sdk/commit/34f543e2e2ca0f5f073ff87158ae1263445b4d48))
* **regen:** add Flux TTS batch (REST) endpoint and agent latency report ([#744](https://github.com/deepgram/deepgram-python-sdk/issues/744)) ([6ca71c4](https://github.com/deepgram/deepgram-python-sdk/commit/6ca71c40e158f5bdf084e6b55572deca1532c465))
* **regen:** add Speak V2 streaming, agent update-listen, and Flux EOT tuning ([#742](https://github.com/deepgram/deepgram-python-sdk/issues/742)) ([69a2445](https://github.com/deepgram/deepgram-python-sdk/commit/69a2445c7c0c5ce1726566331f13030df64062e5))
* **regen:** flux stt numerals and aura-2 multilingual tts voices ([#746](https://github.com/deepgram/deepgram-python-sdk/issues/746)) ([17a1deb](https://github.com/deepgram/deepgram-python-sdk/commit/17a1deb43705f0d9c667f12c72a585159a71ad8f))
* **regen:** listen v2 force-end-turn and redaction, listen v1 diarize metadata ([#750](https://github.com/deepgram/deepgram-python-sdk/issues/750)) ([4678f0e](https://github.com/deepgram/deepgram-python-sdk/commit/4678f0e230d590e1ad473ae2f3452619d21d3d6b))
* **regen:** speak v2 barge-in and speed/expressivity controls, listen v2 redaction ([#758](https://github.com/deepgram/deepgram-python-sdk/issues/758)) ([aab1eae](https://github.com/deepgram/deepgram-python-sdk/commit/aab1eae8704d50aba5d8823ef09b7278ff03580c))
* **regen:** v2 language_hints, profanity filter, word timings, diarize_model ([#730](https://github.com/deepgram/deepgram-python-sdk/issues/730)) ([da6b7ba](https://github.com/deepgram/deepgram-python-sdk/commit/da6b7ba8b5583a9dcddfd3950b4abd4d2645c9fa))
* **sagemaker:** add optional extras group for SageMaker dependencies ([#659](https://github.com/deepgram/deepgram-python-sdk/issues/659)) ([2046175](https://github.com/deepgram/deepgram-python-sdk/commit/204617538339b1958e2fe562dc94c8887de94a5d))
* SDK regeneration (21 Oct 2025) ([#609](https://github.com/deepgram/deepgram-python-sdk/issues/609)) ([5b21460](https://github.com/deepgram/deepgram-python-sdk/commit/5b2146058842fe4dc6d6ef4bd9c0777b08f48fab))
* sdk regeneration 2026-04-14 ([#690](https://github.com/deepgram/deepgram-python-sdk/issues/690)) ([d4d129f](https://github.com/deepgram/deepgram-python-sdk/commit/d4d129f74edb479a3d34c125cc46412c25e072ff))
* sdk regeneration 2026-04-24 ([#696](https://github.com/deepgram/deepgram-python-sdk/issues/696)) ([4714207](https://github.com/deepgram/deepgram-python-sdk/commit/47142072be6e674d518791579529d67e2555dcc0))
* support arbitrary attributes for speak provider ([1973bbc](https://github.com/deepgram/deepgram-python-sdk/commit/1973bbcc6fb5c111c991c2b807ec3573e77ec516))
* support context length option ([14ea4bf](https://github.com/deepgram/deepgram-python-sdk/commit/14ea4bfdb52ce6e291ea599d8ed72aadc85bc39b))
* support context length option ([3735cc0](https://github.com/deepgram/deepgram-python-sdk/commit/3735cc0c74f79a2e857448a44492fa84c633e43a))
* support for agent v1 ([5945c56](https://github.com/deepgram/deepgram-python-sdk/commit/5945c56d1d50f255ff6bb90f5a18b98fd51eda3a))
* support for agent v1 ([7ad48ea](https://github.com/deepgram/deepgram-python-sdk/commit/7ad48eae86373a41cbc04705e9e4be4b9b442d5f))
* support short-lived tokens endpoint ([016bd4d](https://github.com/deepgram/deepgram-python-sdk/commit/016bd4da4f18c6f859f7082944fb976de8d37cf3))
* support short-lived tokens endpoint ([3474a88](https://github.com/deepgram/deepgram-python-sdk/commit/3474a88884694c8cd955f45fcefd15e4373c20fa))
* update generated SDK models and restore agent settings compatibility ([#705](https://github.com/deepgram/deepgram-python-sdk/issues/705)) ([0b820c9](https://github.com/deepgram/deepgram-python-sdk/commit/0b820c900b886eb18da4cc88af7de6e10d1926a6))
* update the SDK with upstream spec changes ([d77ad96](https://github.com/deepgram/deepgram-python-sdk/commit/d77ad966db62e068fb6e346d247299bc9efd1bd5))
* updateinstructions to updateprompt ([a269dc7](https://github.com/deepgram/deepgram-python-sdk/commit/a269dc7f2ee49d8058234dc062cc8da8286d82b7))
* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640)) ([bc918fe](https://github.com/deepgram/deepgram-python-sdk/commit/bc918fe23e92eefb5e4c24cbfaad369d4e2818f3))
* **websockets:** add custom WebSocket transport support ([#658](https://github.com/deepgram/deepgram-python-sdk/issues/658)) ([f6cf0fb](https://github.com/deepgram/deepgram-python-sdk/commit/f6cf0fbc9aaaa844e475e014560cc377819ec1f9))


### Bug Fixes

* :herb: skip_validation:true to allow unknown messages back from the API ([#669](https://github.com/deepgram/deepgram-python-sdk/issues/669)) ([48354d2](https://github.com/deepgram/deepgram-python-sdk/commit/48354d2b6990684092ec7d6b78878ac8427d4c23))
* (regen) route think/models to env.agent_rest ([#715](https://github.com/deepgram/deepgram-python-sdk/issues/715)) ([ffd2e7d](https://github.com/deepgram/deepgram-python-sdk/commit/ffd2e7d7e0e0ea2d72e13e1d4c91ac52e97a5ee8))
* adds inject agent message method ([#555](https://github.com/deepgram/deepgram-python-sdk/issues/555)) ([c0e864b](https://github.com/deepgram/deepgram-python-sdk/commit/c0e864b71a0b41cffc1c1130113542639a646439))
* **agent:** move mip_opt_out field to root level of SettingsOptions ([#561](https://github.com/deepgram/deepgram-python-sdk/issues/561)) ([eca802a](https://github.com/deepgram/deepgram-python-sdk/commit/eca802ad2eff7f660c4166bd50cc545ef56a8c7a))
* **ci:** reference the correct secret ([#585](https://github.com/deepgram/deepgram-python-sdk/issues/585)) ([09550c7](https://github.com/deepgram/deepgram-python-sdk/commit/09550c7c43b6778d52030bd70a48905c425d1365))
* coderabbit gave some good tips this time ([eb03638](https://github.com/deepgram/deepgram-python-sdk/commit/eb0363830dd63ceb4450aaa26138b890aa496a0f))
* correct the language property location and type ([6380b56](https://github.com/deepgram/deepgram-python-sdk/commit/6380b56f810b31323aedf7b644c5a0466f48a1ee))
* corrects order to the release workflow ([#583](https://github.com/deepgram/deepgram-python-sdk/issues/583)) ([3abbac3](https://github.com/deepgram/deepgram-python-sdk/commit/3abbac3271e77e718dde19580a16cdf915c263df))
* couple more issues ([8e066ce](https://github.com/deepgram/deepgram-python-sdk/commit/8e066ce57dbe9f4e1ccdeb93a5d29bf89a789b09))
* default value ([72e61a2](https://github.com/deepgram/deepgram-python-sdk/commit/72e61a2cd3b55b1fd10ee6a8aa9374f0987decef))
* do coderabbit's stuff ([d062caf](https://github.com/deepgram/deepgram-python-sdk/commit/d062cafd6695b96032ccda1f0e45275f255943b1))
* downgrade 'tasks cancelled error' to debug log ([#550](https://github.com/deepgram/deepgram-python-sdk/issues/550)) ([eca4b1e](https://github.com/deepgram/deepgram-python-sdk/commit/eca4b1e16c9e97d02ed00c3af7108e99bcbf352a))
* endpoint class fix ([#551](https://github.com/deepgram/deepgram-python-sdk/issues/551)) ([1cc054f](https://github.com/deepgram/deepgram-python-sdk/commit/1cc054f51e0133b805a0dfc842ac51b694057120))
* function calls ([#556](https://github.com/deepgram/deepgram-python-sdk/issues/556)) ([20fb81c](https://github.com/deepgram/deepgram-python-sdk/commit/20fb81c46180886d3952896f7320f7622862324e))
* handle empty objects for providers ([a2d66fe](https://github.com/deepgram/deepgram-python-sdk/commit/a2d66fe3461d6610af97c48b7c8731939776a377))
* handle empty objects for providers ([eddcf18](https://github.com/deepgram/deepgram-python-sdk/commit/eddcf18379e32123a1542ea18119ea59a4728287))
* handle socket connection closed error in _signal_exit ([5dee108](https://github.com/deepgram/deepgram-python-sdk/commit/5dee1080f158a9956f6298a1f585a977abb3d65b))
* handle socket connection closed error in _signal_exit ([2ca6dbd](https://github.com/deepgram/deepgram-python-sdk/commit/2ca6dbdab7571a58d61fd1ff96fb2589103feb17))
* issue of exception on websocket closing ([bdbc10a](https://github.com/deepgram/deepgram-python-sdk/commit/bdbc10a0aa0562755e83713e3e93157bb30dddee))
* lint ([d647d63](https://github.com/deepgram/deepgram-python-sdk/commit/d647d63a4012fa459d3b8182bd711406fd52a25e))
* lowercase bool query params on websocket connect ([#712](https://github.com/deepgram/deepgram-python-sdk/issues/712)) ([8899609](https://github.com/deepgram/deepgram-python-sdk/commit/88996096c6114e2f3a5d25ecf9e2128b11ca07f7))
* moves agent tags to settings ([4fc8756](https://github.com/deepgram/deepgram-python-sdk/commit/4fc875613d4f2e33e05663746c35b2526b78616a))
* moves agent tags to settings ([e15781d](https://github.com/deepgram/deepgram-python-sdk/commit/e15781df21174f46a620a8458121ebe75c666d2d))
* redact Authorization header from websockets DEBUG logs ([#731](https://github.com/deepgram/deepgram-python-sdk/issues/731)) ([029d877](https://github.com/deepgram/deepgram-python-sdk/commit/029d8771a2957fd5ffbc3c50fb40550098fcfad3))
* release-please config fixes ([#579](https://github.com/deepgram/deepgram-python-sdk/issues/579)) ([a603806](https://github.com/deepgram/deepgram-python-sdk/commit/a6038067596f1643cd5c7255f0e5a7ede1ff43fb))
* remove testpypi we don't need it in the workflow ([#582](https://github.com/deepgram/deepgram-python-sdk/issues/582)) ([b2e2538](https://github.com/deepgram/deepgram-python-sdk/commit/b2e2538cb9528f48e9a20a839763ff82fe40ab8b))
* remove the keyterms check ([4ab6cba](https://github.com/deepgram/deepgram-python-sdk/commit/4ab6cba0a5bdb604a5db56d45aab2dfb8b711f73))
* resolve lint issue ([b21005a](https://github.com/deepgram/deepgram-python-sdk/commit/b21005a8aa81ae86e9b32245ff9f43a8b0410aa0))
* **sagemaker:** extract SageMaker transport to separate deepgram-sagemaker package ([#665](https://github.com/deepgram/deepgram-python-sdk/issues/665)) ([e6317c5](https://github.com/deepgram/deepgram-python-sdk/commit/e6317c507c7b5536aa5a485abc54a50318baff2b))
* shut up linter ([4cf0542](https://github.com/deepgram/deepgram-python-sdk/commit/4cf0542775ee33ac2ffeb4b9f81674a10859f571))
* **speak:** correct TTS warning event field names to match API response ([#653](https://github.com/deepgram/deepgram-python-sdk/issues/653)) ([f7ab1da](https://github.com/deepgram/deepgram-python-sdk/commit/f7ab1daac4f6777b806fb1cdaaf1d1084b280506))
* support multiple keyterms for v2 listen client ([#595](https://github.com/deepgram/deepgram-python-sdk/issues/595)) ([7a9d41d](https://github.com/deepgram/deepgram-python-sdk/commit/7a9d41d2b5a48dd094ca20e7f5a227afbdd46dc0))
* **types:** change speaker and related fields from float to int ([#652](https://github.com/deepgram/deepgram-python-sdk/issues/652)) ([00ee485](https://github.com/deepgram/deepgram-python-sdk/commit/00ee485252dc7fb3a37914f261a0752469c33553)), closes [#641](https://github.com/deepgram/deepgram-python-sdk/issues/641)
* update error handling in async_client.py and client.py ([4f78e8e](https://github.com/deepgram/deepgram-python-sdk/commit/4f78e8ed1d30a352f5c647d6644606e8f5d9ed7a))
* updates examples to aura-2 [WIP] ([#514](https://github.com/deepgram/deepgram-python-sdk/issues/514)) ([e48e415](https://github.com/deepgram/deepgram-python-sdk/commit/e48e4152ed65f8e58a75545b9b296af9aa09a497))
* **websockets:** restore optional message param on control send_ methods ([#680](https://github.com/deepgram/deepgram-python-sdk/issues/680)) ([0018fc4](https://github.com/deepgram/deepgram-python-sdk/commit/0018fc489dd05f81773086044ff476514ceed0e0))
* **websockets:** support array parameters in Listen v1 and v2 clients ([#650](https://github.com/deepgram/deepgram-python-sdk/issues/650)) ([38cc1e5](https://github.com/deepgram/deepgram-python-sdk/commit/38cc1e5903df1eb7bcf8729361be8c25042216af))
* widen pydantic-core bound via fern 5.14.8 regen (closes [#701](https://github.com/deepgram/deepgram-python-sdk/issues/701)) ([#724](https://github.com/deepgram/deepgram-python-sdk/issues/724)) ([5c1e845](https://github.com/deepgram/deepgram-python-sdk/commit/5c1e845e677f4dc2aa44695e4c2f6366136f3f75))


### Reverts

* keyterm -&gt; keyterms ([601c558](https://github.com/deepgram/deepgram-python-sdk/commit/601c55868ab52214c8f35abdc3a1b71770baaee9))
* keyterm -&gt; keyterms ([a391e19](https://github.com/deepgram/deepgram-python-sdk/commit/a391e191e590b4f3a25fc11cafa32ed44136d8d7))
* listen v2 force-end-turn/redaction + diarize regen ([#750](https://github.com/deepgram/deepgram-python-sdk/issues/750)) ([#757](https://github.com/deepgram/deepgram-python-sdk/issues/757)) ([48c88fc](https://github.com/deepgram/deepgram-python-sdk/commit/48c88fcd7a319fb57c579201fc392936d7c8d97e))


### Documentation

* improve contributor onboarding and setup instructions ([#718](https://github.com/deepgram/deepgram-python-sdk/issues/718)) ([3f7398a](https://github.com/deepgram/deepgram-python-sdk/commit/3f7398a9782a1efcfd99408f1392907aa4e68cf3))
* target Context7 benchmark gaps in Python skills [no-ci] ([#699](https://github.com/deepgram/deepgram-python-sdk/issues/699)) ([a232eb8](https://github.com/deepgram/deepgram-python-sdk/commit/a232eb8c62df2da98cef13c71e33f0b3b78f1095))


### Miscellaneous Chores

* release 5.3.2 ([d61ce8c](https://github.com/deepgram/deepgram-python-sdk/commit/d61ce8c504030e7b6ea7ee3b7be8a642d5f0ee53))

## [7.7.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.6.0...v7.7.0) (2026-08-12)

Flux TTS streaming controls and Listen v2 redaction.


### Features

* **Speak v2 (Flux TTS streaming):** barge-in via `send_interrupt()` (optional `playback_offset`, `{type: "time_ms", value: N}`), answered by a `SpeechInterrupted` server message whose metadata carries the new `controls_applied.breaks_applied` counter; mid-stream `send_configure()` to change `speed`, acknowledged by `ConfigureSuccess` / `ConfigureFailure`; new `speed` and `expressivity` connect query parameters. Inline pause and pronunciation controls are not applied at launch — they are stripped before synthesis and support is coming soon. ([#758](https://github.com/deepgram/deepgram-python-sdk/issues/758)) ([aab1eae](https://github.com/deepgram/deepgram-python-sdk/commit/aab1eae8704d50aba5d8823ef09b7278ff03580c))
* **Listen v2:** `redact` connect parameter (`ListenV2Redact`: `numbers`, `aggressive_numbers`); `send_configure()` is now properly typed (`ListenV2Configure` + `ListenV2ConfigureSuccess` in the response union), replacing the previous `typing.Any` shim. ([#758](https://github.com/deepgram/deepgram-python-sdk/issues/758)) ([aab1eae](https://github.com/deepgram/deepgram-python-sdk/commit/aab1eae8704d50aba5d8823ef09b7278ff03580c))
* **Other:** `GoogleThinkProviderVersion` adds `ai-studio-v1beta` and `gemini-enterprise-agent-v1`; `AgentV1UpdateListenListenProvider` discriminated union (`_V1` / `_V2`, discriminant `version`); `client_wrapper` now derives its version from `importlib.metadata` rather than a hardcoded string. ([#758](https://github.com/deepgram/deepgram-python-sdk/issues/758)) ([aab1eae](https://github.com/deepgram/deepgram-python-sdk/commit/aab1eae8704d50aba5d8823ef09b7278ff03580c))


### Compatibility

* No breaking changes against v7.6.0: 0 removed public exports, 0 deleted modules, baseline socket-client signatures intact, and enum changes are widenings only.
* The `deepgram` speak provider `version` widens from `Literal["v1"]` to `str`.
* `AgentV1UpdateListenListen.provider` moves from a bare `DeepgramListenProviderV2` to a required discriminated union; a compatibility validator coerces a legacy provider instance or bare dict into the new shape (both serialize to `version: "v2"`), so existing callers are unaffected.

## [7.6.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.5.0...v7.6.0) (2026-07-22)


### Features

* **regen:** flux stt numerals and aura-2 multilingual tts voices ([#746](https://github.com/deepgram/deepgram-python-sdk/issues/746)) ([17a1deb](https://github.com/deepgram/deepgram-python-sdk/commit/17a1deb43705f0d9c667f12c72a585159a71ad8f))

## [7.5.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.4.0...v7.5.0) (2026-07-14)


### Features

* **Streaming text-to-speech (Flux) via `speak.v2`** — new WebSocket TTS: `client.speak.v2.connect(...)` streams `Speak`/`Flush`/`Close` and returns audio frames plus control messages. Also adds **agent `UpdateListen`/`ListenUpdated`** (swap the listen provider mid-session) and **Flux end-of-turn tuning** (`eot_threshold`, `eager_eot_threshold`, `eot_timeout_ms`). ([#742](https://github.com/deepgram/deepgram-python-sdk/issues/742)) ([69a2445](https://github.com/deepgram/deepgram-python-sdk/commit/69a2445c7c0c5ce1726566331f13030df64062e5))
* **Flux text-to-speech batch (REST)** endpoint and agent latency report. ([#744](https://github.com/deepgram/deepgram-python-sdk/issues/744)) ([6ca71c4](https://github.com/deepgram/deepgram-python-sdk/commit/6ca71c40e158f5bdf084e6b55572deca1532c465))

## [7.4.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.3.1...v7.4.0) (2026-06-26)


### Features

* **regen:** v2 language_hints, profanity filter, word timings, diarize_model ([#730](https://github.com/deepgram/deepgram-python-sdk/issues/730)) ([da6b7ba](https://github.com/deepgram/deepgram-python-sdk/commit/da6b7ba8b5583a9dcddfd3950b4abd4d2645c9fa))


### Bug Fixes

* redact Authorization header from websockets DEBUG logs ([#731](https://github.com/deepgram/deepgram-python-sdk/issues/731)) ([029d877](https://github.com/deepgram/deepgram-python-sdk/commit/029d8771a2957fd5ffbc3c50fb40550098fcfad3))


### Documentation

* improve contributor onboarding and setup instructions ([#718](https://github.com/deepgram/deepgram-python-sdk/issues/718)) ([3f7398a](https://github.com/deepgram/deepgram-python-sdk/commit/3f7398a9782a1efcfd99408f1392907aa4e68cf3))

## [7.3.1](https://github.com/deepgram/deepgram-python-sdk/compare/v7.3.0...v7.3.1) (2026-06-03)


### Bug Fixes

* widen pydantic-core bound via fern 5.14.8 regen (closes [#701](https://github.com/deepgram/deepgram-python-sdk/issues/701)) ([#724](https://github.com/deepgram/deepgram-python-sdk/issues/724)) ([5c1e845](https://github.com/deepgram/deepgram-python-sdk/commit/5c1e845e677f4dc2aa44695e4c2f6366136f3f75))

## [7.3.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.2.0...v7.3.0) (2026-06-01)


### Features

* **client:** add a declarative `reconnect` flag with transport-factory auto-disable. `DeepgramClient` / `AsyncDeepgramClient` now accept `reconnect: bool = True` (exposed read-only as `client.reconnect`). When a custom `transport_factory` is supplied, `reconnect` auto-sets to `False` to signal that the transport owns its own retry/reconnect lifecycle — e.g. the SageMaker transport's jittered backoff + replay buffers — so SDK-level retries don't stack on top and cause storm-on-storm under burst load. Pass `reconnect=True` explicitly to opt back in. Declarative only for now (the Python SDK has no wrapper reconnect layer; `websockets` doesn't auto-reconnect), fully backwards-compatible, and parity with the same flag in the JS ([#492](https://github.com/deepgram/deepgram-js-sdk/issues/492)) and Java SDKs ([#720](https://github.com/deepgram/deepgram-python-sdk/issues/720)) ([b5d5905](https://github.com/deepgram/deepgram-python-sdk/commit/b5d590577429adeacfe2068df4c33201a158c9de))

## [7.2.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.1.1...v7.2.0) (2026-05-18)


### Features

* **agent:** Diarization v2 is now GA for batch transcription via the listen REST API ([#714](https://github.com/deepgram/deepgram-python-sdk/issues/714)) ([9d9a43d](https://github.com/deepgram/deepgram-python-sdk/commit/9d9a43dbc2bd739068b05e5d136f487b56ef5b7c))
* **agent:** rename listen-provider types to `DeepgramListenProviderV1`, `DeepgramListenProviderV2`, and `DeepgramListenProviderV2LanguageHint`. The old `AgentV1SettingsAgent[Context]ListenProvider*` names continue to work as backward-compatible aliases ([#714](https://github.com/deepgram/deepgram-python-sdk/issues/714)) ([9d9a43d](https://github.com/deepgram/deepgram-python-sdk/commit/9d9a43dbc2bd739068b05e5d136f487b56ef5b7c))


### Bug Fixes

* **agent:** route `agent.v1.settings.think.models.list()` to the correct REST host. Previously this endpoint resolved against the wrong base URL and was unusable ([#715](https://github.com/deepgram/deepgram-python-sdk/issues/715)) ([ffd2e7d](https://github.com/deepgram/deepgram-python-sdk/commit/ffd2e7d7e0e0ea2d72e13e1d4c91ac52e97a5ee8))
* **environment:** replace `DeepgramClientEnvironment.AGENT` with a new `agent_rest` slot on `DeepgramClientEnvironment`. Callers constructing a custom environment should pass `agent_rest=` instead of `agent=` ([#715](https://github.com/deepgram/deepgram-python-sdk/issues/715)) ([ffd2e7d](https://github.com/deepgram/deepgram-python-sdk/commit/ffd2e7d7e0e0ea2d72e13e1d4c91ac52e97a5ee8))

## [7.1.1](https://github.com/deepgram/deepgram-python-sdk/compare/v7.1.0...v7.1.1) (2026-05-12)


### Bug Fixes

* lowercase bool query params on websocket connect ([#712](https://github.com/deepgram/deepgram-python-sdk/issues/712)) ([8899609](https://github.com/deepgram/deepgram-python-sdk/commit/88996096c6114e2f3a5d25ecf9e2128b11ca07f7))

## [7.1.0](https://github.com/deepgram/deepgram-python-sdk/compare/v7.0.0...v7.1.0) (2026-05-06)


### Features

* update generated SDK models and restore agent settings compatibility ([#705](https://github.com/deepgram/deepgram-python-sdk/issues/705)) ([0b820c9](https://github.com/deepgram/deepgram-python-sdk/commit/0b820c900b886eb18da4cc88af7de6e10d1926a6))


### Documentation

* target Context7 benchmark gaps in Python skills [no-ci] ([#699](https://github.com/deepgram/deepgram-python-sdk/issues/699)) ([a232eb8](https://github.com/deepgram/deepgram-python-sdk/commit/a232eb8c62df2da98cef13c71e33f0b3b78f1095))

## [7.0.0](https://github.com/deepgram/deepgram-python-sdk/compare/v6.1.1...v7.0.0) (2026-04-27)


### ⚠ BREAKING CHANGES

* sdk regeneration 2026-04-24 ([#696](https://github.com/deepgram/deepgram-python-sdk/issues/696))
* sdk regeneration 2026-04-14 ([#690](https://github.com/deepgram/deepgram-python-sdk/issues/690))

### Features

* sdk regeneration 2026-04-14 ([#690](https://github.com/deepgram/deepgram-python-sdk/issues/690)) ([d4d129f](https://github.com/deepgram/deepgram-python-sdk/commit/d4d129f74edb479a3d34c125cc46412c25e072ff))
* sdk regeneration 2026-04-24 ([#696](https://github.com/deepgram/deepgram-python-sdk/issues/696)) ([4714207](https://github.com/deepgram/deepgram-python-sdk/commit/47142072be6e674d518791579529d67e2555dcc0))

## [6.1.1](https://github.com/deepgram/deepgram-python-sdk/compare/v6.1.0...v6.1.1) (2026-03-27)


### Bug Fixes

* **websockets:** restore optional message param on control send_ methods ([#680](https://github.com/deepgram/deepgram-python-sdk/issues/680)) ([0018fc4](https://github.com/deepgram/deepgram-python-sdk/commit/0018fc489dd05f81773086044ff476514ceed0e0))

## [6.1.0](https://github.com/deepgram/deepgram-python-sdk/compare/v6.0.1...v6.1.0) (2026-03-26)


### Features

* **agent:** support multi-provider speak/think configuration and typed listen parameters ([#676](https://github.com/deepgram/deepgram-python-sdk/issues/676)) ([5dfb1aa](https://github.com/deepgram/deepgram-python-sdk/commit/5dfb1aa9a2357f8cfc0e08f55284fd8521446bf7))

## [6.0.1](https://github.com/deepgram/deepgram-python-sdk/compare/v6.0.0...v6.0.1) (2026-02-24)


### Bug Fixes

* :herb: skip_validation:true to allow unknown messages back from the API ([#669](https://github.com/deepgram/deepgram-python-sdk/issues/669)) ([48354d2](https://github.com/deepgram/deepgram-python-sdk/commit/48354d2b6990684092ec7d6b78878ac8427d4c23))

## [6.0.0](https://github.com/deepgram/deepgram-python-sdk/compare/v6.0.0-rc.2...v6.0.0) (2026-02-23)


### ⚠ BREAKING CHANGES

* promote v6.0.0-rc.2 to v6.0.0 stable

### Features

* promote v6.0.0-rc.2 to v6.0.0 stable ([34f543e](https://github.com/deepgram/deepgram-python-sdk/commit/34f543e2e2ca0f5f073ff87158ae1263445b4d48))

## [6.0.0-rc.2](https://github.com/deepgram/deepgram-python-sdk/compare/v6.0.0-rc.1...v6.0.0-rc.2) (2026-02-18)


### Bug Fixes

* **sagemaker:** extract SageMaker transport to separate deepgram-sagemaker package ([#665](https://github.com/deepgram/deepgram-python-sdk/issues/665)) ([e6317c5](https://github.com/deepgram/deepgram-python-sdk/commit/e6317c507c7b5536aa5a485abc54a50318baff2b))


### Refactors

* **sagemaker:** extract SageMaker transport to separate package ([#663](https://github.com/deepgram/deepgram-python-sdk/issues/663)) ([d82b699](https://github.com/deepgram/deepgram-python-sdk/commit/d82b6993ff2e6e1b4e67e8da3b2f33b13f2da33d))
* **sagemaker:** move SageMaker transport to separate package ([#662](https://github.com/deepgram/deepgram-python-sdk/issues/662)) ([16d500e](https://github.com/deepgram/deepgram-python-sdk/commit/16d500eca8e88e54e6d0fbf2b11bb2e8e0de5f48))

## [6.0.0-rc.1](https://github.com/deepgram/deepgram-python-sdk/compare/v5.3.2...v6.0.0-rc.1) (2026-02-16)


### ⚠ BREAKING CHANGES

* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640))

### Features

* **helpers:** add TextBuilder class for TTS pronunciation and pause controls ([#660](https://github.com/deepgram/deepgram-python-sdk/issues/660)) ([4324120](https://github.com/deepgram/deepgram-python-sdk/commit/43241200a7e025bdc4633bdb47f6708921c82ad1))
* **sagemaker:** add SageMaker transport support via the separate [`deepgram-sagemaker`](https://pypi.org/project/deepgram-sagemaker/) package (`pip install deepgram-sagemaker`) ([#659](https://github.com/deepgram/deepgram-python-sdk/issues/659))
* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640)) ([bc918fe](https://github.com/deepgram/deepgram-python-sdk/commit/bc918fe23e92eefb5e4c24cbfaad369d4e2818f3))
* **websockets:** add custom WebSocket transport support ([#658](https://github.com/deepgram/deepgram-python-sdk/issues/658)) ([f6cf0fb](https://github.com/deepgram/deepgram-python-sdk/commit/f6cf0fbc9aaaa844e475e014560cc377819ec1f9))

## [5.3.2](https://github.com/deepgram/deepgram-python-sdk/compare/v5.3.0...v5.3.2) (2026-01-29)


### Bug Fixes

* **speak:** correct TTS warning event field names to match API response ([#653](https://github.com/deepgram/deepgram-python-sdk/issues/653)) ([f7ab1da](https://github.com/deepgram/deepgram-python-sdk/commit/f7ab1daac4f6777b806fb1cdaaf1d1084b280506))
* **types:** change speaker and related fields from float to int ([#652](https://github.com/deepgram/deepgram-python-sdk/issues/652)) ([00ee485](https://github.com/deepgram/deepgram-python-sdk/commit/00ee485252dc7fb3a37914f261a0752469c33553)), closes [#641](https://github.com/deepgram/deepgram-python-sdk/issues/641)
* **websockets:** support array parameters in Listen v1 and v2 clients ([#650](https://github.com/deepgram/deepgram-python-sdk/issues/650)) ([38cc1e5](https://github.com/deepgram/deepgram-python-sdk/commit/38cc1e5903df1eb7bcf8729361be8c25042216af))


### Miscellaneous Chores

* release 5.3.2 ([d61ce8c](https://github.com/deepgram/deepgram-python-sdk/commit/d61ce8c504030e7b6ea7ee3b7be8a642d5f0ee53))

## [5.3.0](https://github.com/deepgram/deepgram-python-sdk/compare/v5.2.0...v5.3.0) (2025-10-30)


### Features

* add projects billing fields list methods ([#621](https://github.com/deepgram/deepgram-python-sdk/issues/621)) ([10d67cd](https://github.com/deepgram/deepgram-python-sdk/commit/10d67cd91aef1436a9e85e3b607dc7b81eebba43))

## [5.2.0](https://github.com/deepgram/deepgram-python-sdk/compare/v5.1.0...v5.2.0) (2025-10-21)


### Features

* SDK regeneration (21 Oct 2025) ([#609](https://github.com/deepgram/deepgram-python-sdk/issues/609)) ([5b21460](https://github.com/deepgram/deepgram-python-sdk/commit/5b2146058842fe4dc6d6ef4bd9c0777b08f48fab))

## [5.1.0](https://github.com/deepgram/deepgram-python-sdk/compare/v5.0.0...v5.1.0) (2025-10-16)


### Features

* mention keep alive in migration guide ([#594](https://github.com/deepgram/deepgram-python-sdk/issues/594)) ([5a8c79e](https://github.com/deepgram/deepgram-python-sdk/commit/5a8c79e814e3efeb81a8c51a0a05d93bc17e6bb5))
* update the SDK with upstream spec changes ([d77ad96](https://github.com/deepgram/deepgram-python-sdk/commit/d77ad966db62e068fb6e346d247299bc9efd1bd5))


### Bug Fixes

* **ci:** reference the correct secret ([#585](https://github.com/deepgram/deepgram-python-sdk/issues/585)) ([09550c7](https://github.com/deepgram/deepgram-python-sdk/commit/09550c7c43b6778d52030bd70a48905c425d1365))
* corrects order to the release workflow ([#583](https://github.com/deepgram/deepgram-python-sdk/issues/583)) ([3abbac3](https://github.com/deepgram/deepgram-python-sdk/commit/3abbac3271e77e718dde19580a16cdf915c263df))
* remove testpypi we don't need it in the workflow ([#582](https://github.com/deepgram/deepgram-python-sdk/issues/582)) ([b2e2538](https://github.com/deepgram/deepgram-python-sdk/commit/b2e2538cb9528f48e9a20a839763ff82fe40ab8b))
* support multiple keyterms for v2 listen client ([#595](https://github.com/deepgram/deepgram-python-sdk/issues/595)) ([7a9d41d](https://github.com/deepgram/deepgram-python-sdk/commit/7a9d41d2b5a48dd094ca20e7f5a227afbdd46dc0))

## [5.0.0](https://github.com/deepgram/deepgram-python-sdk/compare/v4.8.1...v5.0.0) (2025-10-02)


### ⚠ BREAKING CHANGES

* This is a significant breaking change, and should be carried out in conjunction with our migration guide.

### Features

* implements new generated SDK architecture, all call signatures ([#572](https://github.com/deepgram/deepgram-python-sdk/issues/572)) ([768d514](https://github.com/deepgram/deepgram-python-sdk/commit/768d51492bf7414067266cdc2cf7b98f1f3981dc))


### Bug Fixes

* release-please config fixes ([#579](https://github.com/deepgram/deepgram-python-sdk/issues/579)) ([a603806](https://github.com/deepgram/deepgram-python-sdk/commit/a6038067596f1643cd5c7255f0e5a7ede1ff43fb))
