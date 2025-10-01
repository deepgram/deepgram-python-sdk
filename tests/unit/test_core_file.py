"""
Unit tests for core file handling utilities.
"""
import io
import pytest

from deepgram.core.file import (
    convert_file_dict_to_httpx_tuples,
    with_content_type
)


class TestConvertFileDictToHttpxTuples:
    """Test convert_file_dict_to_httpx_tuples function."""
    
    def test_simple_file_dict(self):
        """Test converting a simple file dictionary."""
        file_content = b"test content"
        file_dict = {"audio": file_content}
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        assert result == [("audio", file_content)]
    
    def test_multiple_files(self):
        """Test converting dictionary with multiple files."""
        file_dict = {
            "audio": b"audio content",
            "metadata": "metadata content"
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        expected = [
            ("audio", b"audio content"),
            ("metadata", "metadata content")
        ]
        assert sorted(result) == sorted(expected)
    
    def test_file_list(self):
        """Test converting dictionary with list of files."""
        file_dict = {
            "documents": [
                b"document1 content",
                b"document2 content",
                "document3 content"
            ]
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        expected = [
            ("documents", b"document1 content"),
            ("documents", b"document2 content"),
            ("documents", "document3 content")
        ]
        assert result == expected
    
    def test_mixed_files_and_lists(self):
        """Test converting dictionary with both single files and file lists."""
        file_dict = {
            "single_file": b"single content",
            "multiple_files": [
                b"multi1 content",
                b"multi2 content"
            ]
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        expected = [
            ("single_file", b"single content"),
            ("multiple_files", b"multi1 content"),
            ("multiple_files", b"multi2 content")
        ]
        assert sorted(result) == sorted(expected)
    
    def test_tuple_file_format(self):
        """Test converting files in tuple format."""
        file_dict = {
            "file_with_name": ("test.txt", b"content"),
            "file_with_content_type": ("test.json", b'{"key": "value"}', "application/json")
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        expected = [
            ("file_with_name", ("test.txt", b"content")),
            ("file_with_content_type", ("test.json", b'{"key": "value"}', "application/json"))
        ]
        assert sorted(result) == sorted(expected)
    
    def test_io_objects(self):
        """Test converting with IO objects."""
        file_content = io.BytesIO(b"io content")
        file_dict = {"io_file": file_content}
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        assert result == [("io_file", file_content)]
    
    def test_empty_dict(self):
        """Test converting empty dictionary."""
        result = convert_file_dict_to_httpx_tuples({})
        assert result == []
    
    def test_empty_list_value(self):
        """Test converting dictionary with empty list value."""
        file_dict = {"empty_files": []}
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        assert result == []


class TestWithContentType:
    """Test with_content_type function."""
    
    def test_simple_file_content(self):
        """Test adding content type to simple file content."""
        file_content = b"test content"
        
        result = with_content_type(file=file_content, default_content_type="application/octet-stream")
        
        expected = (None, file_content, "application/octet-stream")
        assert result == expected
    
    def test_string_file_content(self):
        """Test adding content type to string file content."""
        file_content = "test content"
        
        result = with_content_type(file=file_content, default_content_type="text/plain")
        
        expected = (None, file_content, "text/plain")
        assert result == expected
    
    def test_io_file_content(self):
        """Test adding content type to IO file content."""
        file_content = io.BytesIO(b"io content")
        
        result = with_content_type(file=file_content, default_content_type="application/octet-stream")
        
        expected = (None, file_content, "application/octet-stream")
        assert result == expected
    
    def test_two_element_tuple(self):
        """Test adding content type to (filename, content) tuple."""
        file_tuple = ("test.txt", b"file content")
        
        result = with_content_type(file=file_tuple, default_content_type="text/plain")
        
        expected = ("test.txt", b"file content", "text/plain")
        assert result == expected
    
    def test_three_element_tuple_with_content_type(self):
        """Test handling (filename, content, content_type) tuple."""
        file_tuple = ("test.json", b'{"key": "value"}', "application/json")
        
        result = with_content_type(file=file_tuple, default_content_type="text/plain")
        
        # Should keep the existing content type
        expected = ("test.json", b'{"key": "value"}', "application/json")
        assert result == expected
    
    def test_three_element_tuple_with_none_content_type(self):
        """Test handling tuple with None content type."""
        file_tuple = ("test.txt", b"content", None)
        
        result = with_content_type(file=file_tuple, default_content_type="text/plain")
        
        # Should use the default content type
        expected = ("test.txt", b"content", "text/plain")
        assert result == expected
    
    def test_four_element_tuple_with_headers(self):
        """Test handling (filename, content, content_type, headers) tuple."""
        headers = {"X-Custom": "value"}
        file_tuple = ("test.txt", b"content", "text/plain", headers)
        
        result = with_content_type(file=file_tuple, default_content_type="application/octet-stream")
        
        # Should keep the existing content type and headers
        expected = ("test.txt", b"content", "text/plain", headers)
        assert result == expected
    
    def test_four_element_tuple_with_none_content_type(self):
        """Test handling tuple with None content type and headers."""
        headers = {"X-Custom": "value"}
        file_tuple = ("test.txt", b"content", None, headers)
        
        result = with_content_type(file=file_tuple, default_content_type="application/json")
        
        # Should use default content type but keep headers
        expected = ("test.txt", b"content", "application/json", headers)
        assert result == expected
    
    def test_invalid_tuple_length(self):
        """Test handling tuple with invalid length."""
        invalid_tuple = ("a", "b", "c", "d", "e")  # 5 elements
        
        with pytest.raises(ValueError, match="Unexpected tuple length: 5"):
            with_content_type(file=invalid_tuple, default_content_type="text/plain")
    
    def test_single_element_tuple(self):
        """Test handling single element tuple."""
        invalid_tuple = ("only_one",)  # 1 element
        
        with pytest.raises(ValueError, match="Unexpected tuple length: 1"):
            with_content_type(file=invalid_tuple, default_content_type="text/plain")


class TestFileTyping:
    """Test file type definitions and edge cases."""
    
    def test_various_file_content_types(self):
        """Test that various FileContent types work correctly."""
        # Test bytes
        bytes_content = b"bytes content"
        result = with_content_type(file=bytes_content, default_content_type="application/octet-stream")
        assert result[1] == bytes_content
        
        # Test string
        string_content = "string content"
        result = with_content_type(file=string_content, default_content_type="text/plain")
        assert result[1] == string_content
        
        # Test IO
        io_content = io.BytesIO(b"io content")
        result = with_content_type(file=io_content, default_content_type="application/octet-stream")
        assert result[1] == io_content
    
    def test_file_dict_with_various_types(self):
        """Test file dict conversion with various file types."""
        string_io = io.StringIO("string io content")
        bytes_io = io.BytesIO(b"bytes io content")
        
        file_dict = {
            "bytes": b"bytes content",
            "string": "string content",
            "string_io": string_io,
            "bytes_io": bytes_io,
            "tuple_basic": ("file.txt", b"content"),
            "tuple_with_type": ("file.json", b'{}', "application/json"),
            "tuple_with_headers": ("file.xml", b"<xml/>", "application/xml", {"X-Custom": "header"})
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        # Should have 7 tuples
        assert len(result) == 7
        
        # Check that all keys are preserved
        keys = [item[0] for item in result]
        expected_keys = ["bytes", "string", "string_io", "bytes_io", "tuple_basic", "tuple_with_type", "tuple_with_headers"]
        assert sorted(keys) == sorted(expected_keys)
    
    def test_complex_file_combinations(self):
        """Test complex combinations of file types and lists."""
        file_dict = {
            "mixed_list": [
                b"raw bytes",
                ("named.txt", "string content"),
                ("typed.json", b'{"test": true}', "application/json"),
                io.BytesIO(b"io stream")
            ],
            "single_complex": ("complex.xml", io.StringIO("<xml>content</xml>"), "application/xml", {"Encoding": "utf-8"})
        }
        
        result = convert_file_dict_to_httpx_tuples(file_dict)
        
        # Should have 5 total items (4 from list + 1 single)
        assert len(result) == 5
        
        # All should have "mixed_list" or "single_complex" as key
        mixed_items = [item for item in result if item[0] == "mixed_list"]
        single_items = [item for item in result if item[0] == "single_complex"]
        
        assert len(mixed_items) == 4
        assert len(single_items) == 1
