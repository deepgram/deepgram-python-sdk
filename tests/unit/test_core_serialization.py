"""
Unit tests for core serialization functionality.
"""
import pytest
import typing
from typing import Dict, List, Set, Optional, Union, Any
from typing_extensions import TypedDict, Annotated

from pydantic import BaseModel
from deepgram.core.serialization import (
    FieldMetadata,
    convert_and_respect_annotation_metadata
)


class TestFieldMetadata:
    """Test FieldMetadata class."""
    
    def test_field_metadata_creation(self):
        """Test creating FieldMetadata instance."""
        metadata = FieldMetadata(alias="field_name")
        assert metadata.alias == "field_name"
    
    def test_field_metadata_with_different_aliases(self):
        """Test FieldMetadata with various alias formats."""
        # Simple alias
        metadata1 = FieldMetadata(alias="simple_alias")
        assert metadata1.alias == "simple_alias"
        
        # Snake case
        metadata2 = FieldMetadata(alias="snake_case_alias")
        assert metadata2.alias == "snake_case_alias"
        
        # Camel case
        metadata3 = FieldMetadata(alias="camelCaseAlias")
        assert metadata3.alias == "camelCaseAlias"
        
        # With special characters
        metadata4 = FieldMetadata(alias="field-with-dashes")
        assert metadata4.alias == "field-with-dashes"


# Test models for serialization tests
class SimpleTestModel(BaseModel):
    name: str
    age: int
    active: bool = True


class SerializationTestTypedDict(TypedDict):
    name: str
    value: int
    optional_field: Optional[str]


class SerializationTestTypedDictWithAlias(TypedDict):
    name: Annotated[str, FieldMetadata(alias="display_name")]
    value: Annotated[int, FieldMetadata(alias="numeric_value")]
    normal_field: str


class TestConvertAndRespectAnnotationMetadata:
    """Test convert_and_respect_annotation_metadata function."""
    
    def test_none_object(self):
        """Test handling None object."""
        result = convert_and_respect_annotation_metadata(
            object_=None,
            annotation=str,
            direction="read"
        )
        assert result is None
    
    def test_simple_type_passthrough(self):
        """Test that simple types pass through unchanged."""
        # String
        result = convert_and_respect_annotation_metadata(
            object_="test_string",
            annotation=str,
            direction="read"
        )
        assert result == "test_string"
        
        # Integer
        result = convert_and_respect_annotation_metadata(
            object_=42,
            annotation=int,
            direction="read"
        )
        assert result == 42
        
        # Boolean
        result = convert_and_respect_annotation_metadata(
            object_=True,
            annotation=bool,
            direction="read"
        )
        assert result is True
    
    def test_pydantic_model_from_dict_read(self):
        """Test converting dict to Pydantic model (read direction)."""
        input_dict = {"name": "John", "age": 30, "active": False}
        
        result = convert_and_respect_annotation_metadata(
            object_=input_dict,
            annotation=SimpleTestModel,
            direction="read"
        )
        
        # Should process the dict for Pydantic model compatibility
        assert isinstance(result, dict)
        assert result["name"] == "John"
        assert result["age"] == 30
        assert result["active"] is False
    
    def test_pydantic_model_from_dict_write(self):
        """Test converting dict from Pydantic model (write direction)."""
        input_dict = {"name": "Alice", "age": 25}
        
        result = convert_and_respect_annotation_metadata(
            object_=input_dict,
            annotation=SimpleTestModel,
            direction="write"
        )
        
        # Should process the dict appropriately
        assert isinstance(result, dict)
        assert result["name"] == "Alice"
        assert result["age"] == 25
    
    def test_typed_dict_basic(self):
        """Test handling basic TypedDict."""
        input_dict = {"name": "Test", "value": 100, "optional_field": "optional"}
        
        result = convert_and_respect_annotation_metadata(
            object_=input_dict,
            annotation=SerializationTestTypedDict,
            direction="read"
        )
        
        assert isinstance(result, dict)
        assert result["name"] == "Test"
        assert result["value"] == 100
        assert result["optional_field"] == "optional"
    
    def test_dict_type_annotation(self):
        """Test handling Dict type annotation."""
        input_dict = {"key1": "value1", "key2": "value2"}
        
        result = convert_and_respect_annotation_metadata(
            object_=input_dict,
            annotation=Dict[str, str],
            direction="read"
        )
        
        assert isinstance(result, dict)
        assert result == input_dict
    
    def test_list_type_annotation(self):
        """Test handling List type annotation."""
        input_list = ["item1", "item2", "item3"]
        
        result = convert_and_respect_annotation_metadata(
            object_=input_list,
            annotation=List[str],
            direction="read"
        )
        
        assert isinstance(result, list)
        assert result == input_list
    
    def test_set_type_annotation(self):
        """Test handling Set type annotation."""
        input_set = {"item1", "item2", "item3"}
        
        result = convert_and_respect_annotation_metadata(
            object_=input_set,
            annotation=Set[str],
            direction="read"
        )
        
        assert isinstance(result, set)
        assert result == input_set
    
    def test_nested_dict_with_list(self):
        """Test handling nested Dict with List values."""
        input_dict = {
            "list1": ["a", "b", "c"],
            "list2": ["x", "y", "z"]
        }
        
        result = convert_and_respect_annotation_metadata(
            object_=input_dict,
            annotation=Dict[str, List[str]],
            direction="read"
        )
        
        assert isinstance(result, dict)
        assert result["list1"] == ["a", "b", "c"]
        assert result["list2"] == ["x", "y", "z"]
    
    def test_nested_list_with_dicts(self):
        """Test handling List containing dicts."""
        input_list = [
            {"name": "Item1", "value": 1},
            {"name": "Item2", "value": 2}
        ]
        
        result = convert_and_respect_annotation_metadata(
            object_=input_list,
            annotation=List[Dict[str, Any]],
            direction="read"
        )
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Item1"
        assert result[1]["value"] == 2
    
    def test_union_type_annotation(self):
        """Test handling Union type annotation."""
        # Test with string (first type in union)
        result1 = convert_and_respect_annotation_metadata(
            object_="test_string",
            annotation=Union[str, int],
            direction="read"
        )
        assert result1 == "test_string"
        
        # Test with int (second type in union)
        result2 = convert_and_respect_annotation_metadata(
            object_=42,
            annotation=Union[str, int],
            direction="read"
        )
        assert result2 == 42
    
    def test_optional_type_annotation(self):
        """Test handling Optional type annotation."""
        # Test with None
        result1 = convert_and_respect_annotation_metadata(
            object_=None,
            annotation=Optional[str],
            direction="read"
        )
        assert result1 is None
        
        # Test with actual value
        result2 = convert_and_respect_annotation_metadata(
            object_="test_value",
            annotation=Optional[str],
            direction="read"
        )
        assert result2 == "test_value"
    
    def test_string_not_treated_as_sequence(self):
        """Test that strings are not treated as sequences."""
        test_string = "hello"
        
        result = convert_and_respect_annotation_metadata(
            object_=test_string,
            annotation=str,
            direction="read"
        )
        
        # String should pass through unchanged, not be treated as sequence of chars
        assert result == "hello"
        assert isinstance(result, str)
    
    def test_complex_nested_structure(self):
        """Test handling complex nested data structures."""
        complex_data = {
            "users": [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25}
            ],
            "metadata": {
                "version": "1.0",
                "tags": ["python", "testing"]
            },
            "flags": {"active", "verified"}
        }
        
        result = convert_and_respect_annotation_metadata(
            object_=complex_data,
            annotation=Dict[str, Any],
            direction="read"
        )
        
        assert isinstance(result, dict)
        assert len(result["users"]) == 2
        assert result["users"][0]["name"] == "John"
        assert result["metadata"]["version"] == "1.0"
        assert "python" in result["metadata"]["tags"]
    
    def test_inner_type_parameter(self):
        """Test using inner_type parameter."""
        input_data = ["item1", "item2"]
        
        result = convert_and_respect_annotation_metadata(
            object_=input_data,
            annotation=List[str],
            inner_type=List[str],
            direction="read"
        )
        
        assert isinstance(result, list)
        assert result == input_data
    
    def test_both_read_and_write_directions(self):
        """Test that both read and write directions work."""
        test_dict = {"key": "value"}
        
        # Test read direction
        result_read = convert_and_respect_annotation_metadata(
            object_=test_dict,
            annotation=Dict[str, str],
            direction="read"
        )
        assert result_read == test_dict
        
        # Test write direction
        result_write = convert_and_respect_annotation_metadata(
            object_=test_dict,
            annotation=Dict[str, str],
            direction="write"
        )
        assert result_write == test_dict


class TestSerializationEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_collections(self):
        """Test handling empty collections."""
        # Empty dict
        result = convert_and_respect_annotation_metadata(
            object_={},
            annotation=Dict[str, str],
            direction="read"
        )
        assert result == {}
        
        # Empty list
        result = convert_and_respect_annotation_metadata(
            object_=[],
            annotation=List[str],
            direction="read"
        )
        assert result == []
        
        # Empty set
        result = convert_and_respect_annotation_metadata(
            object_=set(),
            annotation=Set[str],
            direction="read"
        )
        assert result == set()
    
    def test_mismatched_types(self):
        """Test handling when object type doesn't match annotation."""
        # This should generally pass through unchanged or handle gracefully
        result = convert_and_respect_annotation_metadata(
            object_="string_value",
            annotation=int,  # Annotation says int, but object is string
            direction="read"
        )
        # Should not crash and return something reasonable
        assert result == "string_value"
    
    def test_deeply_nested_structures(self):
        """Test handling deeply nested structures."""
        deep_structure = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": ["deep", "values"]
                    }
                }
            }
        }
        
        result = convert_and_respect_annotation_metadata(
            object_=deep_structure,
            annotation=Dict[str, Any],
            direction="read"
        )
        
        assert result["level1"]["level2"]["level3"]["level4"] == ["deep", "values"]
    
    def test_unicode_and_special_characters(self):
        """Test handling unicode and special characters."""
        unicode_data = {
            "chinese": "你好世界",
            "emoji": "🚀🌟",
            "special": "café naïve",
            "mixed": ["Hello", "世界", "🌍"]
        }
        
        result = convert_and_respect_annotation_metadata(
            object_=unicode_data,
            annotation=Dict[str, Any],
            direction="read"
        )
        
        assert result["chinese"] == "你好世界"
        assert result["emoji"] == "🚀🌟"
        assert result["special"] == "café naïve"
        assert "世界" in result["mixed"]
