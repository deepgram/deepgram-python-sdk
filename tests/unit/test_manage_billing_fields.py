"""
Unit tests for manage projects billing fields models and methods.

This module tests the billing fields list methods including:
- ListBillingFieldsV1Response model validation
- Sync and async client methods
- Request parameter handling
- Error scenarios
"""

import pytest
from pydantic import ValidationError

from deepgram.types.list_billing_fields_v1response import ListBillingFieldsV1Response
from deepgram.types.list_billing_fields_v1response_deployments_item import (
    ListBillingFieldsV1ResponseDeploymentsItem,
)


class TestListBillingFieldsV1Response:
    """Test ListBillingFieldsV1Response model."""

    def test_valid_billing_fields_response_full(self):
        """Test creating a valid billing fields response with all fields."""
        response_data = {
            "accessors": [
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321",
            ],
            "deployments": ["hosted", "beta", "self-hosted", "dedicated"],
            "tags": ["tag1", "tag2", "production"],
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming",
                "batch::nova-2": "Nova-2 Batch",
                "streaming::enhanced": "Enhanced Streaming",
            },
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert len(response.accessors) == 2
        assert response.accessors[0] == "12345678-1234-1234-1234-123456789012"
        assert response.deployments is not None
        assert len(response.deployments) == 4
        assert "hosted" in response.deployments
        assert response.tags is not None
        assert len(response.tags) == 3
        assert "production" in response.tags
        assert response.line_items is not None
        assert len(response.line_items) == 3
        assert response.line_items["streaming::nova-3"] == "Nova-3 Streaming"

    def test_valid_billing_fields_response_minimal(self):
        """Test creating a billing fields response with minimal fields."""
        response_data = {}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is None
        assert response.deployments is None
        assert response.tags is None
        assert response.line_items is None

    def test_billing_fields_response_empty_lists(self):
        """Test billing fields response with empty lists."""
        response_data = {
            "accessors": [],
            "deployments": [],
            "tags": [],
            "line_items": {},
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors == []
        assert response.deployments == []
        assert response.tags == []
        assert response.line_items == {}

    def test_billing_fields_response_with_accessors_only(self):
        """Test billing fields response with only accessors."""
        response_data = {
            "accessors": [
                "11111111-1111-1111-1111-111111111111",
                "22222222-2222-2222-2222-222222222222",
            ]
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert len(response.accessors) == 2
        assert response.deployments is None
        assert response.tags is None
        assert response.line_items is None

    def test_billing_fields_response_with_deployments_only(self):
        """Test billing fields response with only deployments."""
        response_data = {"deployments": ["hosted", "dedicated"]}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is None
        assert response.deployments is not None
        assert len(response.deployments) == 2
        assert "hosted" in response.deployments
        assert "dedicated" in response.deployments
        assert response.tags is None
        assert response.line_items is None

    def test_billing_fields_response_with_tags_only(self):
        """Test billing fields response with only tags."""
        response_data = {"tags": ["development", "staging", "production"]}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is None
        assert response.deployments is None
        assert response.tags is not None
        assert len(response.tags) == 3
        assert "production" in response.tags
        assert response.line_items is None

    def test_billing_fields_response_with_line_items_only(self):
        """Test billing fields response with only line_items."""
        response_data = {
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming",
                "batch::whisper": "Whisper Batch",
            }
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is None
        assert response.deployments is None
        assert response.tags is None
        assert response.line_items is not None
        assert len(response.line_items) == 2
        assert response.line_items["batch::whisper"] == "Whisper Batch"

    def test_billing_fields_response_serialization(self):
        """Test billing fields response serialization."""
        response_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "deployments": ["hosted"],
            "tags": ["test-tag"],
            "line_items": {"streaming::nova-3": "Nova-3 Streaming"},
        }

        response = ListBillingFieldsV1Response(**response_data)

        # Test dict conversion
        response_dict = response.model_dump()
        assert "accessors" in response_dict
        assert "deployments" in response_dict
        assert "tags" in response_dict
        assert "line_items" in response_dict
        assert response_dict["accessors"][0] == "12345678-1234-1234-1234-123456789012"

        # Test JSON serialization
        json_str = response.model_dump_json()
        assert '"accessors"' in json_str
        assert '"deployments"' in json_str
        assert '"tags"' in json_str
        assert '"line_items"' in json_str
        assert "12345678-1234-1234-1234-123456789012" in json_str

    def test_billing_fields_response_immutability(self):
        """Test that billing fields response is immutable (frozen)."""
        response = ListBillingFieldsV1Response(
            accessors=["12345678-1234-1234-1234-123456789012"]
        )

        with pytest.raises((AttributeError, ValidationError)):
            response.accessors = ["new-accessor"]

    def test_billing_fields_response_extra_fields_allowed(self):
        """Test that billing fields response allows extra fields."""
        response_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "extra_field": "extra_value",
            "custom_data": {"nested": "value"},
        }

        # Should not raise an error due to extra="allow"
        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert hasattr(response, "extra_field")
        assert hasattr(response, "custom_data")

    def test_billing_fields_response_roundtrip_serialization(self):
        """Test that billing fields response can be serialized and deserialized."""
        original_data = {
            "accessors": [
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321",
            ],
            "deployments": ["hosted", "beta"],
            "tags": ["tag1", "tag2"],
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming",
                "batch::nova-2": "Nova-2 Batch",
            },
        }

        original_response = ListBillingFieldsV1Response(**original_data)

        # Serialize to JSON and back
        json_str = original_response.model_dump_json()
        import json

        parsed_data = json.loads(json_str)
        reconstructed_response = ListBillingFieldsV1Response(**parsed_data)

        assert original_response.accessors == reconstructed_response.accessors
        assert original_response.deployments == reconstructed_response.deployments
        assert original_response.tags == reconstructed_response.tags
        assert original_response.line_items == reconstructed_response.line_items

    def test_billing_fields_response_with_many_accessors(self):
        """Test billing fields response with many accessors."""
        # Simulate a response with many accessors
        accessors = [
            f"{i:08x}-1234-1234-1234-123456789012" for i in range(100)
        ]
        response_data = {"accessors": accessors}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert len(response.accessors) == 100
        assert response.accessors[0] == "00000000-1234-1234-1234-123456789012"
        assert response.accessors[99] == "00000063-1234-1234-1234-123456789012"

    def test_billing_fields_response_with_many_tags(self):
        """Test billing fields response with many tags."""
        # Simulate a response with many tags
        tags = [f"tag-{i}" for i in range(50)]
        response_data = {"tags": tags}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.tags is not None
        assert len(response.tags) == 50
        assert "tag-0" in response.tags
        assert "tag-49" in response.tags

    def test_billing_fields_response_with_many_line_items(self):
        """Test billing fields response with many line_items."""
        # Simulate a response with many line items
        line_items = {
            f"streaming::model-{i}": f"Model {i} Streaming" for i in range(20)
        }
        response_data = {"line_items": line_items}

        response = ListBillingFieldsV1Response(**response_data)

        assert response.line_items is not None
        assert len(response.line_items) == 20
        assert response.line_items["streaming::model-0"] == "Model 0 Streaming"
        assert response.line_items["streaming::model-19"] == "Model 19 Streaming"

    def test_billing_fields_response_with_special_characters_in_tags(self):
        """Test billing fields response with special characters in tags."""
        response_data = {
            "tags": [
                "tag-with-dashes",
                "tag_with_underscores",
                "tag.with.dots",
                "tag:with:colons",
                "tag/with/slashes",
            ]
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.tags is not None
        assert len(response.tags) == 5
        assert "tag-with-dashes" in response.tags
        assert "tag/with/slashes" in response.tags

    def test_billing_fields_response_with_unicode_in_line_items(self):
        """Test billing fields response with unicode characters."""
        response_data = {
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming 🚀",
                "batch::model-测试": "Test Model 测试",
                "streaming::émoji": "Émoji Model with accénts",
            }
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.line_items is not None
        assert response.line_items["streaming::nova-3"] == "Nova-3 Streaming 🚀"
        assert response.line_items["batch::model-测试"] == "Test Model 测试"
        assert response.line_items["streaming::émoji"] == "Émoji Model with accénts"

    def test_billing_fields_response_comparison(self):
        """Test billing fields response equality comparison."""
        response_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "deployments": ["hosted"],
            "tags": ["tag1"],
            "line_items": {"streaming::nova-3": "Nova-3 Streaming"},
        }

        response1 = ListBillingFieldsV1Response(**response_data)
        response2 = ListBillingFieldsV1Response(**response_data)

        # Same data should be equal
        assert response1 == response2

        # Different data should not be equal
        different_data = response_data.copy()
        different_data["accessors"] = ["87654321-4321-4321-4321-210987654321"]
        response3 = ListBillingFieldsV1Response(**different_data)
        assert response1 != response3


class TestListBillingFieldsV1ResponseDeploymentsItem:
    """Test ListBillingFieldsV1ResponseDeploymentsItem type."""

    def test_deployments_item_literal_values(self):
        """Test that deployments item accepts literal values."""
        valid_deployments = ["hosted", "beta", "self-hosted", "dedicated"]

        for deployment in valid_deployments:
            deployment_value: ListBillingFieldsV1ResponseDeploymentsItem = deployment
            assert isinstance(deployment_value, str)

    def test_deployments_item_custom_value(self):
        """Test that deployments item accepts custom values due to typing.Any."""
        # String not in literals
        custom_deployment: ListBillingFieldsV1ResponseDeploymentsItem = (
            "custom-deployment"
        )
        assert isinstance(custom_deployment, str)
        assert custom_deployment == "custom-deployment"

    def test_deployments_item_in_response(self):
        """Test deployments item usage within a response."""
        response_data = {
            "deployments": ["hosted", "beta", "custom-deployment", "self-hosted"]
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.deployments is not None
        assert len(response.deployments) == 4
        assert "hosted" in response.deployments
        assert "custom-deployment" in response.deployments


class TestBillingFieldsResponseIntegration:
    """Integration tests for billing fields response models."""

    def test_realistic_billing_fields_response(self):
        """Test a realistic billing fields response with typical data."""
        response_data = {
            "accessors": [
                "a1b2c3d4-5678-90ab-cdef-1234567890ab",
                "b2c3d4e5-6789-01bc-def0-234567890abc",
                "c3d4e5f6-7890-12cd-ef01-34567890abcd",
            ],
            "deployments": ["hosted", "self-hosted"],
            "tags": [
                "production",
                "customer-123",
                "region-us-east",
                "team-engineering",
            ],
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming Transcription",
                "streaming::nova-2": "Nova-2 Streaming Transcription",
                "batch::nova-3": "Nova-3 Batch Transcription",
                "batch::whisper": "Whisper Batch Transcription",
                "streaming::enhanced": "Enhanced Streaming Transcription",
                "tts::aura": "Aura Text-to-Speech",
            },
        }

        response = ListBillingFieldsV1Response(**response_data)

        # Verify all fields are present and correct
        assert len(response.accessors) == 3
        assert len(response.deployments) == 2
        assert len(response.tags) == 4
        assert len(response.line_items) == 6

        # Verify specific values
        assert "customer-123" in response.tags
        assert "hosted" in response.deployments
        assert response.line_items["tts::aura"] == "Aura Text-to-Speech"

    def test_billing_fields_response_with_date_filters(self):
        """Test billing fields response scenario with date-filtered data."""
        # This represents a response for a specific date range
        response_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "deployments": ["hosted"],
            "tags": ["q1-2024", "january"],
            "line_items": {
                "streaming::nova-3": "Nova-3 Streaming",
                "batch::nova-2": "Nova-2 Batch",
            },
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert len(response.accessors) == 1
        assert "q1-2024" in response.tags
        assert len(response.line_items) == 2

    def test_billing_fields_response_empty_results(self):
        """Test billing fields response with no data for the period."""
        # This represents a response for a period with no billing data
        response_data = {
            "accessors": [],
            "deployments": [],
            "tags": [],
            "line_items": {},
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors == []
        assert response.deployments == []
        assert response.tags == []
        assert response.line_items == {}

    def test_billing_fields_response_partial_data(self):
        """Test billing fields response with partial data."""
        # Some projects might only have certain fields populated
        response_data = {
            "deployments": ["hosted"],
            "line_items": {"streaming::nova-3": "Nova-3 Streaming"},
        }

        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is None
        assert response.deployments is not None
        assert response.tags is None
        assert response.line_items is not None

    def test_multiple_billing_fields_responses_comparison(self):
        """Test comparing multiple billing fields responses."""
        response1_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "tags": ["january"],
        }

        response2_data = {
            "accessors": [
                "12345678-1234-1234-1234-123456789012",
                "87654321-4321-4321-4321-210987654321",
            ],
            "tags": ["february"],
        }

        response1 = ListBillingFieldsV1Response(**response1_data)
        response2 = ListBillingFieldsV1Response(**response2_data)

        # Verify they are different
        assert response1 != response2
        assert len(response1.accessors) == 1
        assert len(response2.accessors) == 2

    def test_billing_fields_response_model_evolution(self):
        """Test that the model handles potential future fields gracefully."""
        # Simulate a response with additional fields that might be added in the future
        response_data = {
            "accessors": ["12345678-1234-1234-1234-123456789012"],
            "deployments": ["hosted"],
            "tags": ["tag1"],
            "line_items": {"streaming::nova-3": "Nova-3 Streaming"},
            # Future fields
            "future_field_1": "some_value",
            "future_field_2": {"nested": "data"},
            "future_field_3": [1, 2, 3],
        }

        # Should not raise an error due to extra="allow"
        response = ListBillingFieldsV1Response(**response_data)

        assert response.accessors is not None
        assert response.deployments is not None
        assert response.tags is not None
        assert response.line_items is not None
        assert hasattr(response, "future_field_1")
        assert hasattr(response, "future_field_2")
        assert hasattr(response, "future_field_3")

