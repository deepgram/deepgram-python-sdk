"""
Unit tests for core utility functions.
"""
import pytest
from typing import Dict, Any, Optional, Mapping

from deepgram.core.remove_none_from_dict import remove_none_from_dict


class TestRemoveNoneFromDict:
    """Test remove_none_from_dict function."""
    
    def test_empty_dict(self):
        """Test removing None values from empty dictionary."""
        result = remove_none_from_dict({})
        assert result == {}
    
    def test_no_none_values(self):
        """Test dictionary with no None values."""
        input_dict = {
            "string": "value",
            "number": 42,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        result = remove_none_from_dict(input_dict)
        assert result == input_dict
    
    def test_all_none_values(self):
        """Test dictionary with all None values."""
        input_dict = {
            "key1": None,
            "key2": None,
            "key3": None
        }
        result = remove_none_from_dict(input_dict)
        assert result == {}
    
    def test_mixed_none_and_values(self):
        """Test dictionary with mix of None and non-None values."""
        input_dict = {
            "keep_string": "value",
            "remove_none": None,
            "keep_number": 42,
            "remove_another_none": None,
            "keep_boolean": False,
            "keep_empty_string": "",
            "keep_zero": 0
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            "keep_string": "value",
            "keep_number": 42,
            "keep_boolean": False,
            "keep_empty_string": "",
            "keep_zero": 0
        }
        assert result == expected
    
    def test_preserve_falsy_values(self):
        """Test that falsy values (except None) are preserved."""
        input_dict = {
            "empty_string": "",
            "zero": 0,
            "false": False,
            "empty_list": [],
            "empty_dict": {},
            "none_value": None
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            "empty_string": "",
            "zero": 0,
            "false": False,
            "empty_list": [],
            "empty_dict": {}
        }
        assert result == expected
    
    def test_nested_structures_with_none(self):
        """Test that nested structures containing None are preserved."""
        input_dict = {
            "nested_dict": {"inner": None, "keep": "value"},
            "nested_list": [None, "keep", None],
            "remove_this": None
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            "nested_dict": {"inner": None, "keep": "value"},
            "nested_list": [None, "keep", None]
        }
        assert result == expected
    
    def test_complex_data_types(self):
        """Test with complex data types."""
        class CustomObject:
            def __init__(self, value):
                self.value = value
            
            def __eq__(self, other):
                return isinstance(other, CustomObject) and self.value == other.value
        
        custom_obj = CustomObject("test")
        input_dict = {
            "custom_object": custom_obj,
            "tuple": (1, 2, 3),
            "set": {1, 2, 3},
            "none_value": None
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            "custom_object": custom_obj,
            "tuple": (1, 2, 3),
            "set": {1, 2, 3}
        }
        assert result == expected
    
    def test_original_dict_unchanged(self):
        """Test that original dictionary is not modified."""
        original = {
            "keep": "value",
            "remove": None
        }
        original_copy = original.copy()
        
        result = remove_none_from_dict(original)
        
        # Original should be unchanged
        assert original == original_copy
        
        # Result should be different
        assert result == {"keep": "value"}
        assert result != original
    
    def test_return_type(self):
        """Test that function returns correct type."""
        input_dict = {"key": "value", "none_key": None}
        result = remove_none_from_dict(input_dict)
        
        # Should return a Dict, not the original Mapping type
        assert isinstance(result, dict)
        assert not isinstance(result, type(input_dict)) or isinstance(input_dict, dict)
    
    def test_with_mapping_input(self):
        """Test with different Mapping types as input."""
        from collections import OrderedDict, defaultdict
        
        # Test with OrderedDict
        ordered_dict = OrderedDict([("keep", "value"), ("remove", None)])
        result = remove_none_from_dict(ordered_dict)
        assert result == {"keep": "value"}
        assert isinstance(result, dict)  # Should return regular dict
        
        # Test with defaultdict
        default_dict = defaultdict(str)
        default_dict["keep"] = "value"
        default_dict["remove"] = None
        result = remove_none_from_dict(default_dict)
        assert result == {"keep": "value"}
        assert isinstance(result, dict)  # Should return regular dict
    
    def test_unicode_keys(self):
        """Test with unicode keys."""
        input_dict = {
            "english": "value",
            "中文": "chinese",
            "español": None,
            "русский": "russian",
            "العربية": None,
            "🔑": "emoji_key"
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            "english": "value",
            "中文": "chinese",
            "русский": "russian",
            "🔑": "emoji_key"
        }
        assert result == expected
    
    def test_numeric_and_special_keys(self):
        """Test with numeric and special character keys."""
        input_dict = {
            1: "numeric_key",
            "normal_key": "value",
            (1, 2): "tuple_key",
            "remove_me": None,
            42: None
        }
        result = remove_none_from_dict(input_dict)
        
        expected = {
            1: "numeric_key",
            "normal_key": "value",
            (1, 2): "tuple_key"
        }
        assert result == expected


class TestRemoveNoneFromDictEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_very_large_dict(self):
        """Test with a very large dictionary."""
        # Create a large dictionary with alternating None and non-None values
        large_dict = {}
        for i in range(1000):
            if i % 2 == 0:
                large_dict[f"key_{i}"] = f"value_{i}"
            else:
                large_dict[f"key_{i}"] = None
        
        result = remove_none_from_dict(large_dict)
        
        # Should have 500 items (half of original)
        assert len(result) == 500
        
        # All values should be non-None
        for value in result.values():
            assert value is not None
        
        # All keys should be even-numbered
        for key in result.keys():
            key_num = int(key.split("_")[1])
            assert key_num % 2 == 0
    
    def test_deeply_nested_with_none_values(self):
        """Test that function only processes top level (doesn't recurse)."""
        input_dict = {
            "level1": {
                "level2": {
                    "level3": None,
                    "keep": "value"
                },
                "also_none": None
            },
            "top_level_none": None
        }
        result = remove_none_from_dict(input_dict)
        
        # Only top-level None should be removed
        expected = {
            "level1": {
                "level2": {
                    "level3": None,  # This None should remain
                    "keep": "value"
                },
                "also_none": None  # This None should remain
            }
        }
        assert result == expected
    
    def test_performance_with_many_none_values(self):
        """Test performance with dictionary having many None values."""
        import time
        
        # Create dictionary with mostly None values
        large_dict = {f"key_{i}": None for i in range(10000)}
        large_dict.update({f"keep_{i}": f"value_{i}" for i in range(100)})
        
        start_time = time.time()
        result = remove_none_from_dict(large_dict)
        end_time = time.time()
        
        # Should complete quickly (less than 1 second)
        assert (end_time - start_time) < 1.0
        
        # Should only have the 100 non-None values
        assert len(result) == 100
        
        # All remaining values should be non-None
        for key, value in result.items():
            assert key.startswith("keep_")
            assert value is not None
