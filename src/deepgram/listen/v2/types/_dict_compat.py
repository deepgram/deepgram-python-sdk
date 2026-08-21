import collections.abc
import functools
import typing
import warnings

from ....core.pydantic_utilities import IS_PYDANTIC_V2
from ....core.unchecked_base_model import UncheckedBaseModel


@functools.lru_cache(maxsize=None)
def _wire_key_to_field_name(model_type: typing.Type[typing.Any]) -> typing.Dict[str, str]:
    fields = model_type.model_fields if IS_PYDANTIC_V2 else model_type.__fields__
    return {typing.cast(str, field.alias or name): name for name, field in fields.items()}


class ListenV2ResponseDictCompatModel(  # type: ignore[misc]
    UncheckedBaseModel, collections.abc.Mapping[str, typing.Any]
):
    @staticmethod
    def _warn_deprecated() -> None:
        warnings.warn(
            "Dictionary-style access to Listen V2 responses is deprecated; "
            "use attribute access instead. Dictionary-style access will be removed in SDK 8.",
            DeprecationWarning,
            stacklevel=3,
        )

    def _iter_wire_keys(self) -> typing.Iterator[str]:
        model = typing.cast(typing.Any, self)
        field_names = _wire_key_to_field_name(type(self))
        fields_set = model.model_fields_set if IS_PYDANTIC_V2 else model.__fields_set__

        for wire_key, field_name in field_names.items():
            if field_name in fields_set:
                yield wire_key

        if IS_PYDANTIC_V2:
            yield from (model.__pydantic_extra__ or {}).keys()
        else:
            known_field_names = set(field_names.values())
            yield from (
                key for key in model.__dict__ if key in fields_set and key not in known_field_names
            )

    def __getitem__(self, key: str) -> typing.Any:
        self._warn_deprecated()
        return self._dict_compat_get_value(key)

    def _dict_compat_get_value(self, key: str) -> typing.Any:
        model = typing.cast(typing.Any, self)
        field_name = _wire_key_to_field_name(type(self)).get(key)
        fields_set = model.model_fields_set if IS_PYDANTIC_V2 else model.__fields_set__

        if field_name is not None:
            if field_name not in fields_set:
                raise KeyError(key)
            return getattr(model, field_name)

        if IS_PYDANTIC_V2:
            extras = model.__pydantic_extra__ or {}
            if key in extras:
                return extras[key]
        elif key in fields_set and key in model.__dict__:
            return model.__dict__[key]

        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        self._warn_deprecated()
        if not isinstance(key, str):
            return False
        try:
            self._dict_compat_get_value(key)
        except KeyError:
            return False
        return True

    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        self._warn_deprecated()
        try:
            return self._dict_compat_get_value(key)
        except KeyError:
            return default

    def __iter__(self) -> typing.Iterator[str]:  # type: ignore[override]
        self._warn_deprecated()
        return self._iter_wire_keys()

    def __len__(self) -> int:
        self._warn_deprecated()
        return sum(1 for _ in self._iter_wire_keys())
