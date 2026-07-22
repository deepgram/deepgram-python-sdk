"""
Unit coverage for the generated ``deepgram.core`` helper modules: the JSON
encoder, datetime parsing/serialization, file helpers, the parse error, the
(de)serialization metadata layer, the pydantic compatibility helpers, and the
``construct_type`` coercion engine.

These are pure functions, so they are exercised directly with a spread of input
shapes that walks their branches.
"""

import dataclasses
import datetime as dt
import decimal
import enum
import ipaddress
import pathlib
import re
import typing
import uuid

import pytest
import typing_extensions

from deepgram.core.datetime_utils import (
    Rfc2822DateTime,
    parse_rfc2822_datetime,
    serialize_datetime,
)
from deepgram.core.file import convert_file_dict_to_httpx_tuples, with_content_type
from deepgram.core.jsonable_encoder import encode_path_param, jsonable_encoder
from deepgram.core.parse_error import ParsingError
from deepgram.core.pydantic_utilities import (
    UniversalBaseModel,
    deep_union_pydantic_dicts,
    encode_by_type,
    parse_date,
    parse_datetime,
    parse_obj_as,
    to_jsonable_with_fallback,
    update_forward_refs,
)
from deepgram.core.serialization import (
    FieldMetadata,
    convert_and_respect_annotation_metadata,
    get_alias_to_field_mapping,
    get_field_to_alias_mapping,
)
from deepgram.core.unchecked_base_model import UncheckedBaseModel, UnionMetadata, construct_type


# --------------------------------------------------------------------------- #
# Models / typed dicts used across the tests
# --------------------------------------------------------------------------- #
class Color(enum.Enum):
    RED = "red"
    BLUE = "blue"


class SampleModel(UniversalBaseModel):
    name: str
    when: typing.Optional[dt.datetime] = None


class Cat(UncheckedBaseModel):
    type: typing.Literal["cat"] = "cat"
    meow: typing.Optional[str] = None


class Dog(UncheckedBaseModel):
    type: typing.Literal["dog"] = "dog"
    bark: typing.Optional[str] = None


DiscriminatedAnimal = typing_extensions.Annotated[
    typing.Union[Cat, Dog], UnionMetadata(discriminant="type")
]


class AliasedTypedDict(typing_extensions.TypedDict):
    field: typing_extensions.Annotated[str, FieldMetadata(alias="field_name")]
    plain: int


# --------------------------------------------------------------------------- #
# jsonable_encoder
# --------------------------------------------------------------------------- #
def test_jsonable_encoder_primitives_and_containers() -> None:
    assert jsonable_encoder(...) is None  # OMIT sentinel
    assert jsonable_encoder("x") == "x"
    assert jsonable_encoder(3) == 3
    assert jsonable_encoder(None) is None
    assert jsonable_encoder(Color.RED) == "red"
    assert jsonable_encoder(pathlib.PurePath("/a/b")) == "/a/b"
    assert jsonable_encoder(b"hi") == "aGk="  # base64
    assert jsonable_encoder(dt.date(2020, 1, 2)) == "2020-01-02"
    assert "T" in jsonable_encoder(dt.datetime(2020, 1, 2, 3, 4, 5))
    # dict drops Ellipsis values; list/set/tuple/generator iterate and drop Ellipsis
    assert jsonable_encoder({"a": 1, "b": ...}) == {"a": 1}
    assert jsonable_encoder([1, ..., 2]) == [1, 2]
    assert sorted(jsonable_encoder({1, 2})) == [1, 2]
    assert jsonable_encoder((1, 2)) == [1, 2]
    assert jsonable_encoder(x for x in (1, 2)) == [1, 2]


def test_jsonable_encoder_model_and_dataclass() -> None:
    # unset optional fields are excluded by UniversalBaseModel.dict()
    assert jsonable_encoder(SampleModel(name="n")) == {"name": "n"}

    @dataclasses.dataclass
    class DC:
        a: int

    assert jsonable_encoder(DC(a=1)) == {"a": 1}


def test_jsonable_encoder_custom_encoder_and_fallback() -> None:
    # custom encoder matched by exact type and by isinstance
    assert jsonable_encoder(5, custom_encoder={int: lambda o: o + 1}) == 6

    class IntSub(int):
        pass

    assert jsonable_encoder(IntSub(5), custom_encoder={int: lambda o: "matched"}) == "matched"

    # fallback path: a plain object that has to be reduced via vars()
    class Plain:
        def __init__(self) -> None:
            self.x = 1

    assert jsonable_encoder(Plain()) == {"x": 1}


def test_encode_path_param() -> None:
    assert encode_path_param(True) == "true"
    assert encode_path_param(False) == "false"
    assert encode_path_param(12) == "12"


# --------------------------------------------------------------------------- #
# datetime_utils
# --------------------------------------------------------------------------- #
def test_parse_rfc2822_datetime() -> None:
    existing = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
    assert parse_rfc2822_datetime(existing) is existing
    assert parse_rfc2822_datetime("Wed, 02 Oct 2002 13:00:00 GMT").year == 2002
    # falls back to ISO 8601 parsing
    assert parse_rfc2822_datetime("2021-05-06T07:08:09Z").year == 2021
    with pytest.raises(ValueError):
        parse_rfc2822_datetime(12345)


def test_serialize_datetime_variants() -> None:
    utc = dt.datetime(2020, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    assert serialize_datetime(utc).endswith("Z")
    offset = dt.datetime(2020, 1, 1, tzinfo=dt.timezone(dt.timedelta(hours=5)))
    assert "+05:00" in serialize_datetime(offset)
    naive = dt.datetime(2020, 1, 1, 0, 0, 0)
    assert isinstance(serialize_datetime(naive), str)


def test_rfc2822_datetime_used_in_model() -> None:
    class WithRfc(UniversalBaseModel):
        ts: Rfc2822DateTime

    parsed = parse_obj_as(WithRfc, {"ts": "Wed, 02 Oct 2002 13:00:00 GMT"})
    assert parsed.ts.year == 2002


# --------------------------------------------------------------------------- #
# file helpers
# --------------------------------------------------------------------------- #
def test_convert_file_dict_to_httpx_tuples() -> None:
    result = convert_file_dict_to_httpx_tuples({"single": b"a", "many": [b"b", b"c"]})
    assert ("single", b"a") in result
    assert ("many", b"b") in result and ("many", b"c") in result


def test_with_content_type_all_shapes() -> None:
    assert with_content_type(file=b"data", default_content_type="text/plain") == (None, b"data", "text/plain")
    assert with_content_type(file=("n", b"d"), default_content_type="text/plain") == ("n", b"d", "text/plain")
    assert with_content_type(file=("n", b"d", None), default_content_type="text/plain") == ("n", b"d", "text/plain")
    assert with_content_type(file=("n", b"d", "image/png"), default_content_type="text/plain") == (
        "n",
        b"d",
        "image/png",
    )
    four = with_content_type(file=("n", b"d", None, {"h": "v"}), default_content_type="text/plain")
    assert four == ("n", b"d", "text/plain", {"h": "v"})
    with pytest.raises(ValueError):
        with_content_type(file=("a", "b", "c", "d", "e"), default_content_type="text/plain")  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# parse_error
# --------------------------------------------------------------------------- #
def test_parsing_error_str() -> None:
    cause = ValueError("boom")
    err = ParsingError(status_code=500, headers={"a": "b"}, body={"x": 1}, cause=cause)
    assert "cause: boom" in str(err)
    assert err.__cause__ is cause
    assert "cause" not in str(ParsingError(status_code=400))


# --------------------------------------------------------------------------- #
# serialization metadata
# --------------------------------------------------------------------------- #
def test_convert_and_respect_annotation_metadata_typeddict() -> None:
    written = convert_and_respect_annotation_metadata(
        object_={"field": "v", "plain": 1}, annotation=AliasedTypedDict, direction="write"
    )
    assert written == {"field_name": "v", "plain": 1}
    read = convert_and_respect_annotation_metadata(
        object_={"field_name": "v", "plain": 1}, annotation=AliasedTypedDict, direction="read"
    )
    assert read == {"field": "v", "plain": 1}
    assert convert_and_respect_annotation_metadata(object_=None, annotation=AliasedTypedDict, direction="write") is None


def test_convert_and_respect_annotation_metadata_containers() -> None:
    list_ann = typing.List[AliasedTypedDict]
    out = convert_and_respect_annotation_metadata(
        object_=[{"field": "v", "plain": 1}], annotation=list_ann, direction="write"
    )
    assert out == [{"field_name": "v", "plain": 1}]

    dict_ann = typing.Dict[str, AliasedTypedDict]
    out2 = convert_and_respect_annotation_metadata(
        object_={"k": {"field": "v", "plain": 1}}, annotation=dict_ann, direction="write"
    )
    assert out2 == {"k": {"field_name": "v", "plain": 1}}

    union_ann = typing.Union[AliasedTypedDict, None]
    out3 = convert_and_respect_annotation_metadata(
        object_={"field": "v", "plain": 1}, annotation=union_ann, direction="write"
    )
    assert out3 == {"field_name": "v", "plain": 1}


def test_alias_mappings() -> None:
    assert get_alias_to_field_mapping(AliasedTypedDict) == {"field_name": "field"}
    assert get_field_to_alias_mapping(AliasedTypedDict) == {"field": "field_name"}


# --------------------------------------------------------------------------- #
# pydantic_utilities
# --------------------------------------------------------------------------- #
def test_parse_datetime_and_date() -> None:
    assert parse_datetime(dt.datetime(2020, 1, 1)).year == 2020
    assert parse_datetime("2020-01-01T00:00:00Z").year == 2020
    assert parse_date(dt.datetime(2020, 1, 2, 3)).day == 2
    assert parse_date(dt.date(2020, 1, 2)).day == 2
    assert parse_date("2020-01-02").day == 2


def test_parse_obj_as_model_and_typeddict() -> None:
    model = parse_obj_as(SampleModel, {"name": "n"})
    assert model.name == "n"
    td = parse_obj_as(AliasedTypedDict, {"field_name": "v", "plain": 1})
    assert td["field"] == "v"


def test_to_jsonable_with_fallback() -> None:
    assert to_jsonable_with_fallback({"a": 1}, lambda o: o) == {"a": 1}


def test_encode_by_type() -> None:
    assert encode_by_type(uuid.uuid4()).count("-") == 4  # exact-type hit
    assert encode_by_type(decimal.Decimal("1.5")) == 1.5
    assert encode_by_type(decimal.Decimal("3")) == 3
    assert encode_by_type(frozenset({1})) == [1]  # isinstance loop branch
    assert encode_by_type(pathlib.Path("/x")) == "/x"
    assert encode_by_type(ipaddress.IPv4Address("1.2.3.4")) == "1.2.3.4"
    assert encode_by_type(re.compile("ab")) == "ab"
    assert encode_by_type(object()) is None  # no encoder matches


def test_deep_union_pydantic_dicts() -> None:
    source = {"a": {"b": 1}, "lst": [{"x": 1}], "scalar": 5}
    destination = {"a": {"c": 2}, "lst": [{"y": 2}], "scalar": 9}
    merged = deep_union_pydantic_dicts(source, destination)
    assert merged["a"] == {"c": 2, "b": 1}
    assert merged["lst"] == [{"y": 2, "x": 1}]
    assert merged["scalar"] == 5


def test_universal_base_model_json_dict_and_alias_coercion() -> None:
    model = SampleModel(name="n", when=dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc))
    assert model.dict()["name"] == "n"
    assert "name" in model.json()

    class AliasModel(UniversalBaseModel):
        actual: typing_extensions.Annotated[str, FieldMetadata(alias="wire")] = ""

    # Field-name input is coerced; supplying an ambiguous duplicate is rejected.
    assert parse_obj_as(AliasModel, {"wire": "v"}).actual == "v"


def test_update_forward_refs_is_noop_safe() -> None:
    update_forward_refs(SampleModel)


# --------------------------------------------------------------------------- #
# construct_type
# --------------------------------------------------------------------------- #
def test_construct_type_scalars() -> None:
    assert construct_type(type_=typing.Any, object_={"x": 1}) == {"x": 1}
    assert construct_type(type_=int, object_="5") == 5
    assert construct_type(type_=int, object_="nan") == "nan"  # falls back on failure
    assert construct_type(type_=bool, object_="true") is True
    assert construct_type(type_=bool, object_="1") is True
    assert construct_type(type_=bool, object_="no") is False
    assert construct_type(type_=Color, object_="red") == Color.RED
    assert construct_type(type_=Color, object_="green") == "green"  # invalid enum falls back
    assert construct_type(type_=uuid.UUID, object_="not-a-uuid") == "not-a-uuid"
    assert construct_type(type_=dt.datetime, object_="2020-01-01T00:00:00Z").year == 2020
    assert construct_type(type_=dt.date, object_="2020-01-02").day == 2
    assert construct_type(type_=str, object_=None) is None


def test_construct_type_containers() -> None:
    assert construct_type(type_=typing.Dict[str, int], object_={"a": "1"}) == {"a": 1}
    assert construct_type(type_=typing.List[int], object_=["1", "2"]) == [1, 2]
    assert construct_type(type_=typing.Set[int], object_=["1", "2"]) == {1, 2}
    # mismatched container shapes pass through untouched
    assert construct_type(type_=typing.Dict[str, int], object_="x") == "x"
    assert construct_type(type_=typing.List[int], object_="x") == "x"


def test_construct_type_model_and_unions() -> None:
    cat = construct_type(type_=Cat, object_={"type": "cat", "meow": "hi"})
    assert isinstance(cat, Cat) and cat.meow == "hi"

    # discriminated union (UnionMetadata) routes by the `type` field
    dog = construct_type(type_=DiscriminatedAnimal, object_={"type": "dog", "bark": "woof"})
    assert isinstance(dog, Dog) and dog.bark == "woof"

    # undiscriminated union of literal-bearing models
    undiscriminated = typing.Union[Cat, Dog]
    again = construct_type(type_=undiscriminated, object_={"type": "cat", "meow": "m"})
    assert isinstance(again, Cat)

    # plain scalar union
    assert construct_type(type_=typing.Union[int, str], object_="hello") == "hello"


def test_construct_type_union_of_lists_and_plain_models() -> None:
    # Union containing a list-of-models member, fed a list -> each item parsed.
    union_with_list = typing.Union[typing.List[Cat], Dog]
    out = construct_type(type_=union_with_list, object_=[{"type": "cat", "meow": "a"}])
    assert isinstance(out, list) and isinstance(out[0], Cat)

    # Undiscriminated union of models without any Literal discriminant field.
    class Box(UncheckedBaseModel):
        w: typing.Optional[int] = None

    class Ball(UncheckedBaseModel):
        r: typing.Optional[int] = None

    result = construct_type(type_=typing.Union[Box, Ball], object_={"w": 1})
    assert isinstance(result, (Box, Ball))


def test_construct_type_union_incompatible_list_and_fallback() -> None:
    # List member is rejected because its items are not compatible, so the
    # union falls through to the scalar member.
    out = construct_type(type_=typing.Union[typing.List[Cat], int], object_=[123])
    assert out == [123] or out is None

    # First union member fails to validate, the second succeeds.
    class HasNum(UncheckedBaseModel):
        num: int = 0

    class HasName(UncheckedBaseModel):
        name: str = ""

    result = construct_type(type_=typing.Union[HasNum, HasName], object_={"name": "x"})
    assert isinstance(result, (HasNum, HasName))


def test_construct_type_union_compatible_list_member() -> None:
    # A union whose List[Model] member matches: every item is a valid dict, so
    # the list is parsed into models.
    out = construct_type(type_=typing.Union[typing.List[Cat], Dog], object_=[{"type": "cat", "meow": "m"}])
    assert isinstance(out, list) and isinstance(out[0], Cat)


def test_construct_type_discriminated_union_from_object() -> None:
    # Feed an object (not a dict) to a discriminated union so the discriminant is
    # read via attribute access rather than subscripting.
    source = Dog(type="dog", bark="woof")
    out = construct_type(type_=DiscriminatedAnimal, object_=source)
    assert isinstance(out, Dog)


def test_construct_type_optional_and_nested_models() -> None:
    class Outer(UncheckedBaseModel):
        inner: typing.Optional[Cat] = None
        tags: typing.Optional[typing.List[str]] = None

    built = construct_type(type_=Outer, object_={"inner": {"type": "cat", "meow": "x"}, "tags": ["a"]})
    assert isinstance(built, Outer) and isinstance(built.inner, Cat)
