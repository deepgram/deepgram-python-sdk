import typing
import warnings

from ....core.pydantic_utilities import IS_PYDANTIC_V2


class ListenV2ResponseDictCompatMixin:
    def __getitem__(self, key: str) -> typing.Any:
        warnings.warn(
            "Dictionary-style access to Listen V2 responses is deprecated; "
            "use attribute access instead. Dictionary-style access will be removed in SDK 8.",
            DeprecationWarning,
            stacklevel=2,
        )
        model = typing.cast(typing.Any, self)
        if IS_PYDANTIC_V2:
            values = model.model_dump(by_alias=True, exclude_unset=True)
        else:
            values = model.dict(by_alias=True, exclude_unset=True)
        return values[key]
