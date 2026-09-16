"""Regression coverage for the generated deferred-function-call setting."""

from deepgram.types.think_settings_v1functions_item import ThinkSettingsV1FunctionsItem


def test_defer_until_eot_serializes() -> None:
    function = ThinkSettingsV1FunctionsItem(name="transfer_call", defer_until_eot=True)

    assert function.dict()["defer_until_eot"] is True
