import typing

from ....core.pydantic_utilities import IS_PYDANTIC_V2
from ....core.unchecked_base_model import UncheckedBaseModel


class ListenV2ResponseDictCompatModel(UncheckedBaseModel):
    def __getitem__(self, key: str) -> typing.Any:
        model = typing.cast(typing.Any, self)
        fields = type(model).model_fields if IS_PYDANTIC_V2 else type(model).__fields__
        fields_set = model.model_fields_set if IS_PYDANTIC_V2 else model.__fields_set__

        for field_name, field in fields.items():
            if (field.alias or field_name) == key:
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
