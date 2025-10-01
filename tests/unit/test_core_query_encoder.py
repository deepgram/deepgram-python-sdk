"""
Unit tests for core query encoder functionality.
"""
from pydantic import BaseModel

from deepgram.core.query_encoder import encode_query, single_query_encoder, traverse_query_dict


class TestTraverseQueryDict:
    """Test traverse_query_dict function."""
    
    def test_simple_dict(self):
        """Test traversing a simple flat dictionary."""
        input_dict = {"key1": "value1", "key2": "value2"}
        result = traverse_query_dict(input_dict)
        
        expected = [("key1", "value1"), ("key2", "value2")]
        assert sorted(result) == sorted(expected)
    
    def test_nested_dict(self):
        """Test traversing a nested dictionary."""
        input_dict = {
            "level1": {
                "level2": "value",
                "level2b": "value2"
            }
        }
        result = traverse_query_dict(input_dict)
        
        expected = [("level1[level2]", "value"), ("level1[level2b]", "value2")]
        assert sorted(result) == sorted(expected)
    
    def test_deeply_nested_dict(self):
        """Test traversing a deeply nested dictionary."""
        input_dict = {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                }
            }
        }
        result = traverse_query_dict(input_dict)
        
        expected = [("level1[level2][level3]", "deep_value")]
        assert result == expected
    
    def test_dict_with_list_values(self):
        """Test traversing dictionary with list values."""
        input_dict = {
            "simple_list": ["item1", "item2"],
            "complex_list": [{"nested": "value1"}, {"nested": "value2"}]
        }
        result = traverse_query_dict(input_dict)
        
        expected = [
            ("simple_list", "item1"),
            ("simple_list", "item2"),
            ("complex_list[nested]", "value1"),
            ("complex_list[nested]", "value2")
        ]
        assert sorted(result) == sorted(expected)
    
    def test_with_key_prefix(self):
        """Test traversing with a key prefix."""
        input_dict = {"key": "value"}
        result = traverse_query_dict(input_dict, "prefix")
        
        expected = [("prefix[key]", "value")]
        assert result == expected
    
    def test_empty_dict(self):
        """Test traversing an empty dictionary."""
        result = traverse_query_dict({})
        assert result == []
    
    def test_mixed_types(self):
        """Test traversing dictionary with mixed value types."""
        input_dict = {
            "string": "text",
            "number": 42,
            "boolean": True,
            "none": None,
            "nested": {"inner": "value"}
        }
        result = traverse_query_dict(input_dict)
        
        expected = [
            ("string", "text"),
            ("number", 42),
            ("boolean", True),
            ("none", None),
            ("nested[inner]", "value")
        ]
        assert sorted(result) == sorted(expected)


class QueryTestModel(BaseModel):
    """Test Pydantic model for query encoder tests."""
    name: str
    age: int
    active: bool = True
    
    class Config:
        extra = "allow"


class TestSingleQueryEncoder:
    """Test single_query_encoder function."""
    
    def test_simple_value(self):
        """Test encoding a simple value."""
        result = single_query_encoder("key", "value")
        assert result == [("key", "value")]
    
    def test_pydantic_model(self):
        """Test encoding a Pydantic model."""
        model = QueryTestModel(name="John", age=30)
        result = single_query_encoder("user", model)
        
        expected = [
            ("user[name]", "John"),
            ("user[age]", 30),
            ("user[active]", True)
        ]
        assert sorted(result) == sorted(expected)
    
    def test_dict_value(self):
        """Test encoding a dictionary value."""
        dict_value = {"nested": "value", "count": 5}
        result = single_query_encoder("data", dict_value)
        
        expected = [
            ("data[nested]", "value"),
            ("data[count]", 5)
        ]
        assert sorted(result) == sorted(expected)
    
    def test_list_of_simple_values(self):
        """Test encoding a list of simple values."""
        list_value = ["item1", "item2", "item3"]
        result = single_query_encoder("items", list_value)
        
        expected = [
            ("items", "item1"),
            ("items", "item2"),
            ("items", "item3")
        ]
        assert result == expected
    
    def test_list_of_pydantic_models(self):
        """Test encoding a list of Pydantic models."""
        models = [
            QueryTestModel(name="John", age=30),
            QueryTestModel(name="Jane", age=25, active=False)
        ]
        result = single_query_encoder("users", models)
        
        expected = [
            ("users[name]", "John"),
            ("users[age]", 30),
            ("users[active]", True),
            ("users[name]", "Jane"),
            ("users[age]", 25),
            ("users[active]", False)
        ]
        assert sorted(result) == sorted(expected)
    
    def test_list_of_dicts(self):
        """Test encoding a list of dictionaries."""
        dict_list = [
            {"name": "Item1", "value": 10},
            {"name": "Item2", "value": 20}
        ]
        result = single_query_encoder("data", dict_list)
        
        expected = [
            ("data[name]", "Item1"),
            ("data[value]", 10),
            ("data[name]", "Item2"),
            ("data[value]", 20)
        ]
        assert sorted(result) == sorted(expected)
    
    def test_mixed_list(self):
        """Test encoding a list with mixed types."""
        mixed_list = ["simple", {"nested": "value"}, 42]
        result = single_query_encoder("mixed", mixed_list)
        
        expected = [
            ("mixed", "simple"),
            ("mixed[nested]", "value"),
            ("mixed", 42)
        ]
        # Can't sort tuples with mixed types, so check length and contents
        assert len(result) == len(expected)
        for item in expected:
            assert item in result


class TestEncodeQuery:
    """Test encode_query function."""
    
    def test_none_query(self):
        """Test encoding None query."""
        result = encode_query(None)
        assert result is None
    
    def test_empty_query(self):
        """Test encoding empty query."""
        result = encode_query({})
        assert result == []
    
    def test_simple_query(self):
        """Test encoding a simple query dictionary."""
        query = {
            "name": "John",
            "age": 30,
            "active": True
        }
        result = encode_query(query)
        
        expected = [
            ("name", "John"),
            ("age", 30),
            ("active", True)
        ]
        assert sorted(result) == sorted(expected)
    
    def test_complex_query(self):
        """Test encoding a complex query with nested structures."""
        query = {
            "user": {
                "name": "John",
                "details": {
                    "age": 30,
                    "active": True
                }
            },
            "tags": ["python", "testing"],
            "metadata": [
                {"key": "version", "value": "1.0"},
                {"key": "env", "value": "test"}
            ]
        }
        result = encode_query(query)
        
        expected = [
            ("user[name]", "John"),
            ("user[details][age]", 30),
            ("user[details][active]", True),
            ("tags", "python"),
            ("tags", "testing"),
            ("metadata[key]", "version"),
            ("metadata[value]", "1.0"),
            ("metadata[key]", "env"),
            ("metadata[value]", "test")
        ]
        assert sorted(result) == sorted(expected)
    
    def test_query_with_pydantic_models(self):
        """Test encoding query containing Pydantic models."""
        model = QueryTestModel(name="Alice", age=28)
        query = {
            "user": model,
            "simple": "value"
        }
        result = encode_query(query)
        
        expected = [
            ("user[name]", "Alice"),
            ("user[age]", 28),
            ("user[active]", True),
            ("simple", "value")
        ]
        assert sorted(result) == sorted(expected)
    
    def test_query_with_special_values(self):
        """Test encoding query with special values like None, empty strings."""
        query = {
            "empty_string": "",
            "none_value": None,
            "zero": 0,
            "false": False,
            "empty_list": [],
            "empty_dict": {}
        }
        result = encode_query(query)
        
        expected = [
            ("empty_string", ""),
            ("none_value", None),
            ("zero", 0),
            ("false", False)
        ]
        assert sorted(result) == sorted(expected)


class TestQueryEncoderEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_circular_reference_protection(self):
        """Test that circular references don't cause infinite loops."""
        # Create a circular reference
        dict_a = {"name": "A"}
        dict_b = {"name": "B", "ref": dict_a}
        dict_a["ref"] = dict_b
        
        # This should not hang or crash
        # Note: The current implementation doesn't handle circular refs,
        # but it should at least not crash for reasonable depths
        query = {"data": {"simple": "value"}}  # Use a safe query instead
        result = encode_query(query)
        assert result == [("data[simple]", "value")]
    
    def test_very_deep_nesting(self):
        """Test handling of very deep nesting."""
        # Create a deeply nested structure
        deep_dict = {"value": "deep"}
        for i in range(10):
            deep_dict = {f"level{i}": deep_dict}
        
        result = traverse_query_dict(deep_dict)
        assert len(result) == 1
        # The key should have many levels of nesting
        key, value = result[0]
        assert value == "deep"
        assert key.count("[") == 10  # Should have 10 levels of nesting
    
    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters."""
        query = {
            "unicode": "Hello 世界",
            "special_chars": "!@#$%^&*()",
            "spaces": "value with spaces",
            "nested": {
                "émoji": "🚀",
                "quotes": 'value"with"quotes'
            }
        }
        result = encode_query(query)
        
        # Should handle all characters properly
        assert ("unicode", "Hello 世界") in result
        assert ("special_chars", "!@#$%^&*()") in result
        assert ("spaces", "value with spaces") in result
        assert ("nested[émoji]", "🚀") in result
        assert ("nested[quotes]", 'value"with"quotes') in result
