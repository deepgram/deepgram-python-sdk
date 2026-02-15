# Changelog

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
