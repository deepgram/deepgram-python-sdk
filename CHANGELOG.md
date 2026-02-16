# Changelog

## [5.3.2](https://github.com/deepgram/deepgram-python-sdk/compare/v6.0.0-rc.1...v5.3.2) (2026-02-16)


### ⚠ BREAKING CHANGES

* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640))
* This is a significant breaking change, and should be carried out in conjunction with our migration guide.

### Features

* Add dictation option to LiveOptions class ([8939e59](https://github.com/deepgram/deepgram-python-sdk/commit/8939e5960d4d11122db9a261ee9c237dfd3081d7))
* Add dictation option to LiveOptions class ([d3b2dcc](https://github.com/deepgram/deepgram-python-sdk/commit/d3b2dcc6867cfe0f73f3af472edc60176745aacb))
* add projects billing fields list methods ([#621](https://github.com/deepgram/deepgram-python-sdk/issues/621)) ([10d67cd](https://github.com/deepgram/deepgram-python-sdk/commit/10d67cd91aef1436a9e85e3b607dc7b81eebba43))
* add support for agent tags ([#559](https://github.com/deepgram/deepgram-python-sdk/issues/559)) ([d605248](https://github.com/deepgram/deepgram-python-sdk/commit/d605248f472945c0dead41391bdcce57212a0e3e))
* adds support for agent mip_opt_out ([#558](https://github.com/deepgram/deepgram-python-sdk/issues/558)) ([3e8a3dd](https://github.com/deepgram/deepgram-python-sdk/commit/3e8a3dd4dc4b191e9eea815502cb52caa0cc7a88))
* Adds support for IUM ([#546](https://github.com/deepgram/deepgram-python-sdk/issues/546)) ([232ee05](https://github.com/deepgram/deepgram-python-sdk/commit/232ee0579a8b3685157c372a18f0271924ffaf35))
* adds support for speak fallback ([#548](https://github.com/deepgram/deepgram-python-sdk/issues/548)) ([cab41fa](https://github.com/deepgram/deepgram-python-sdk/commit/cab41facb615fa2784cb78c51cbd3ecc3254a890))
* adds ttl_seconds support ([#557](https://github.com/deepgram/deepgram-python-sdk/issues/557)) ([e9bedf2](https://github.com/deepgram/deepgram-python-sdk/commit/e9bedf2ecf02673dba7256719efe9d917a2d1610))
* apply latest spec changes ([4ad9eb7](https://github.com/deepgram/deepgram-python-sdk/commit/4ad9eb75ae74c0e840ffc0b34d31abbe0ee5fb3a))
* **auth:** adding token-based auth to the SDK so access tokens can be used in requests ([#543](https://github.com/deepgram/deepgram-python-sdk/issues/543)) ([1200c83](https://github.com/deepgram/deepgram-python-sdk/commit/1200c832fc28b366405bdead7e82ae06abc74308))
* **helpers:** add TextBuilder class for TTS pronunciation and pause controls ([#660](https://github.com/deepgram/deepgram-python-sdk/issues/660)) ([4324120](https://github.com/deepgram/deepgram-python-sdk/commit/43241200a7e025bdc4633bdb47f6708921c82ad1))
* implements new generated SDK architecture, all call signatures ([#572](https://github.com/deepgram/deepgram-python-sdk/issues/572)) ([768d514](https://github.com/deepgram/deepgram-python-sdk/commit/768d51492bf7414067266cdc2cf7b98f1f3981dc))
* make all providers generic ([2c92d67](https://github.com/deepgram/deepgram-python-sdk/commit/2c92d676a8611e997c2abde05943df092644f7ea))
* make provider objects generic ([4521048](https://github.com/deepgram/deepgram-python-sdk/commit/45210488c05b2aad5db3671c732888542a5afe91))
* mention keep alive in migration guide ([#594](https://github.com/deepgram/deepgram-python-sdk/issues/594)) ([5a8c79e](https://github.com/deepgram/deepgram-python-sdk/commit/5a8c79e814e3efeb81a8c51a0a05d93bc17e6bb5))
* officially enable aura-2 in live text-to-speech ([052aadd](https://github.com/deepgram/deepgram-python-sdk/commit/052aaddd9ff17dd4acfccbac0dcaa66c792d63f0))
* officially enable aura-2 in live text-to-speech ([ba4124a](https://github.com/deepgram/deepgram-python-sdk/commit/ba4124a503376b2cf22fae6e87ab59de18c59c22))
* **sagemaker:** add optional extras group for SageMaker dependencies ([#659](https://github.com/deepgram/deepgram-python-sdk/issues/659)) ([2046175](https://github.com/deepgram/deepgram-python-sdk/commit/204617538339b1958e2fe562dc94c8887de94a5d))
* SDK regeneration (21 Oct 2025) ([#609](https://github.com/deepgram/deepgram-python-sdk/issues/609)) ([5b21460](https://github.com/deepgram/deepgram-python-sdk/commit/5b2146058842fe4dc6d6ef4bd9c0777b08f48fab))
* support arbitrary attributes for speak provider ([1973bbc](https://github.com/deepgram/deepgram-python-sdk/commit/1973bbcc6fb5c111c991c2b807ec3573e77ec516))
* support context length option ([14ea4bf](https://github.com/deepgram/deepgram-python-sdk/commit/14ea4bfdb52ce6e291ea599d8ed72aadc85bc39b))
* support context length option ([3735cc0](https://github.com/deepgram/deepgram-python-sdk/commit/3735cc0c74f79a2e857448a44492fa84c633e43a))
* support for agent v1 ([5945c56](https://github.com/deepgram/deepgram-python-sdk/commit/5945c56d1d50f255ff6bb90f5a18b98fd51eda3a))
* support for agent v1 ([7ad48ea](https://github.com/deepgram/deepgram-python-sdk/commit/7ad48eae86373a41cbc04705e9e4be4b9b442d5f))
* support short-lived tokens endpoint ([016bd4d](https://github.com/deepgram/deepgram-python-sdk/commit/016bd4da4f18c6f859f7082944fb976de8d37cf3))
* support short-lived tokens endpoint ([3474a88](https://github.com/deepgram/deepgram-python-sdk/commit/3474a88884694c8cd955f45fcefd15e4373c20fa))
* update the SDK with upstream spec changes ([d77ad96](https://github.com/deepgram/deepgram-python-sdk/commit/d77ad966db62e068fb6e346d247299bc9efd1bd5))
* updateinstructions to updateprompt ([a269dc7](https://github.com/deepgram/deepgram-python-sdk/commit/a269dc7f2ee49d8058234dc062cc8da8286d82b7))
* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640)) ([bc918fe](https://github.com/deepgram/deepgram-python-sdk/commit/bc918fe23e92eefb5e4c24cbfaad369d4e2818f3))
* **websockets:** add custom WebSocket transport support ([#658](https://github.com/deepgram/deepgram-python-sdk/issues/658)) ([f6cf0fb](https://github.com/deepgram/deepgram-python-sdk/commit/f6cf0fbc9aaaa844e475e014560cc377819ec1f9))


### Bug Fixes

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
* moves agent tags to settings ([4fc8756](https://github.com/deepgram/deepgram-python-sdk/commit/4fc875613d4f2e33e05663746c35b2526b78616a))
* moves agent tags to settings ([e15781d](https://github.com/deepgram/deepgram-python-sdk/commit/e15781df21174f46a620a8458121ebe75c666d2d))
* release-please config fixes ([#579](https://github.com/deepgram/deepgram-python-sdk/issues/579)) ([a603806](https://github.com/deepgram/deepgram-python-sdk/commit/a6038067596f1643cd5c7255f0e5a7ede1ff43fb))
* remove testpypi we don't need it in the workflow ([#582](https://github.com/deepgram/deepgram-python-sdk/issues/582)) ([b2e2538](https://github.com/deepgram/deepgram-python-sdk/commit/b2e2538cb9528f48e9a20a839763ff82fe40ab8b))
* remove the keyterms check ([4ab6cba](https://github.com/deepgram/deepgram-python-sdk/commit/4ab6cba0a5bdb604a5db56d45aab2dfb8b711f73))
* resolve lint issue ([b21005a](https://github.com/deepgram/deepgram-python-sdk/commit/b21005a8aa81ae86e9b32245ff9f43a8b0410aa0))
* shut up linter ([4cf0542](https://github.com/deepgram/deepgram-python-sdk/commit/4cf0542775ee33ac2ffeb4b9f81674a10859f571))
* **speak:** correct TTS warning event field names to match API response ([#653](https://github.com/deepgram/deepgram-python-sdk/issues/653)) ([f7ab1da](https://github.com/deepgram/deepgram-python-sdk/commit/f7ab1daac4f6777b806fb1cdaaf1d1084b280506))
* support multiple keyterms for v2 listen client ([#595](https://github.com/deepgram/deepgram-python-sdk/issues/595)) ([7a9d41d](https://github.com/deepgram/deepgram-python-sdk/commit/7a9d41d2b5a48dd094ca20e7f5a227afbdd46dc0))
* **types:** change speaker and related fields from float to int ([#652](https://github.com/deepgram/deepgram-python-sdk/issues/652)) ([00ee485](https://github.com/deepgram/deepgram-python-sdk/commit/00ee485252dc7fb3a37914f261a0752469c33553)), closes [#641](https://github.com/deepgram/deepgram-python-sdk/issues/641)
* update error handling in async_client.py and client.py ([4f78e8e](https://github.com/deepgram/deepgram-python-sdk/commit/4f78e8ed1d30a352f5c647d6644606e8f5d9ed7a))
* updates examples to aura-2 [WIP] ([#514](https://github.com/deepgram/deepgram-python-sdk/issues/514)) ([e48e415](https://github.com/deepgram/deepgram-python-sdk/commit/e48e4152ed65f8e58a75545b9b296af9aa09a497))
* **websockets:** support array parameters in Listen v1 and v2 clients ([#650](https://github.com/deepgram/deepgram-python-sdk/issues/650)) ([38cc1e5](https://github.com/deepgram/deepgram-python-sdk/commit/38cc1e5903df1eb7bcf8729361be8c25042216af))


### Reverts

* keyterm -&gt; keyterms ([601c558](https://github.com/deepgram/deepgram-python-sdk/commit/601c55868ab52214c8f35abdc3a1b71770baaee9))
* keyterm -&gt; keyterms ([a391e19](https://github.com/deepgram/deepgram-python-sdk/commit/a391e191e590b4f3a25fc11cafa32ed44136d8d7))


### Miscellaneous Chores

* release 5.3.2 ([d61ce8c](https://github.com/deepgram/deepgram-python-sdk/commit/d61ce8c504030e7b6ea7ee3b7be8a642d5f0ee53))

## [6.0.0-rc.1](https://github.com/deepgram/deepgram-python-sdk/compare/v5.3.2...v6.0.0-rc.1) (2026-02-16)


### ⚠ BREAKING CHANGES

* v6 — fully generated SDK with latest APIs and WebSocket support ([#640](https://github.com/deepgram/deepgram-python-sdk/issues/640))

### Features

* **helpers:** add TextBuilder class for TTS pronunciation and pause controls ([#660](https://github.com/deepgram/deepgram-python-sdk/issues/660)) ([4324120](https://github.com/deepgram/deepgram-python-sdk/commit/43241200a7e025bdc4633bdb47f6708921c82ad1))
* **sagemaker:** add SageMaker transport for running Deepgram on AWS SageMaker endpoints ([#659](https://github.com/deepgram/deepgram-python-sdk/issues/659)) ([2046175](https://github.com/deepgram/deepgram-python-sdk/commit/204617538339b1958e2fe562dc94c8887de94a5d))
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
