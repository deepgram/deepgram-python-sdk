# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import pytest
from deepgram.clients.agent.v1.websocket.options import (
    SettingsOptions,
    Agent,
)


class TestAgentTags:
    """Unit tests for tags agent setting"""

    def test_default_tags_value(self):
        """Test that tags defaults to None"""
        options = SettingsOptions()

        # Default should be None
        assert options.agent.tags is None

        # Verify it's accessible through the agent directly
        agent = Agent()
        assert agent.tags is None

    def test_set_tags_list(self):
        """Test setting tags to a list of strings"""
        options = SettingsOptions()
        test_tags = ["tag1", "tag2", "tag3"]
        options.agent.tags = test_tags

        assert options.agent.tags == test_tags
        assert len(options.agent.tags) == 3
        assert "tag1" in options.agent.tags
        assert "tag2" in options.agent.tags
        assert "tag3" in options.agent.tags

    def test_set_tags_empty_list(self):
        """Test setting tags to an empty list"""
        options = SettingsOptions()
        options.agent.tags = []

        assert options.agent.tags == []
        assert len(options.agent.tags) == 0

    def test_set_tags_single_item(self):
        """Test setting tags to a list with single item"""
        options = SettingsOptions()
        options.agent.tags = ["single-tag"]

        assert options.agent.tags == ["single-tag"]
        assert len(options.agent.tags) == 1

    def test_tags_serialization_default(self):
        """Test that tags with default value (None) is excluded from serialization"""
        options = SettingsOptions()
        # Don't set tags, should use default (None)

        result = options.to_dict()

        # With default None and exclude=lambda f: f is None metadata,
        # the field should be excluded from serialization entirely when it's None
        assert "agent" in result
        assert "tags" not in result["agent"], "tags field should be excluded when None"

    def test_tags_serialization_with_values(self):
        """Test that tags with values is included in serialization"""
        options = SettingsOptions()
        test_tags = ["production", "customer-support", "high-priority"]
        options.agent.tags = test_tags

        result = options.to_dict()
        json_str = options.to_json()
        parsed_json = json.loads(json_str)

        # Should be included when set
        assert result["agent"]["tags"] == test_tags
        assert parsed_json["agent"]["tags"] == test_tags

    def test_tags_serialization_empty_list(self):
        """Test that tags=[] (empty list) behavior in serialization"""
        options = SettingsOptions()
        options.agent.tags = []

        result = options.to_dict()
        json_str = options.to_json()
        parsed_json = json.loads(json_str)

        # Empty list should be included in serialization
        assert "tags" in result["agent"]
        assert result["agent"]["tags"] == []
        assert parsed_json["agent"]["tags"] == []

    def test_tags_deserialization(self):
        """Test deserializing tags from dict"""
        # Test with multiple values
        data_multiple = {
            "agent": {
                "tags": ["test", "demo", "validation"]
            }
        }

        options_multiple = SettingsOptions.from_dict(data_multiple)
        assert options_multiple.agent.tags == ["test", "demo", "validation"]

        # Test with single value
        data_single = {
            "agent": {
                "tags": ["single"]
            }
        }

        options_single = SettingsOptions.from_dict(data_single)
        assert options_single.agent.tags == ["single"]

        # Test with empty array
        data_empty = {
            "agent": {
                "tags": []
            }
        }

        options_empty = SettingsOptions.from_dict(data_empty)
        assert options_empty.agent.tags == []

    def test_tags_deserialization_missing(self):
        """Test deserializing when tags is not present (should default to None)"""
        data = {
            "agent": {
                "language": "en"
            }
        }

        options = SettingsOptions.from_dict(data)
        assert options.agent.tags is None

    def test_tags_round_trip(self):
        """Test serialization and deserialization round-trip"""
        # Test with multiple tags
        original_multiple = SettingsOptions()
        test_tags = ["env:production", "team:backend", "priority:high"]
        original_multiple.agent.tags = test_tags

        serialized_multiple = original_multiple.to_dict()
        restored_multiple = SettingsOptions.from_dict(serialized_multiple)

        assert restored_multiple.agent.tags == test_tags

        # Test with empty list
        original_empty = SettingsOptions()
        original_empty.agent.tags = []

        serialized_empty = original_empty.to_dict()
        restored_empty = SettingsOptions.from_dict(serialized_empty)

        assert restored_empty.agent.tags == []

    def test_tags_with_other_agent_settings(self):
        """Test tags works correctly with other agent settings"""
        options = SettingsOptions()
        options.agent.language = "en"
        options.agent.tags = ["integration", "test"]
        options.agent.greeting = "Hello, this is a tagged conversation"
        options.agent.mip_opt_out = True

        assert options.agent.language == "en"
        assert options.agent.tags == ["integration", "test"]
        assert options.agent.greeting == "Hello, this is a tagged conversation"
        assert options.agent.mip_opt_out == True

        # Test serialization with multiple fields
        result = options.to_dict()
        assert result["agent"]["language"] == "en"
        assert result["agent"]["tags"] == ["integration", "test"]
        assert result["agent"]["greeting"] == "Hello, this is a tagged conversation"
        assert result["agent"]["mip_opt_out"] == True

    def test_tags_type_validation(self):
        """Test that tags accepts list of strings"""
        options = SettingsOptions()

        # Should accept list of strings
        options.agent.tags = ["string1", "string2"]
        assert options.agent.tags == ["string1", "string2"]

        # Should accept empty list
        options.agent.tags = []
        assert options.agent.tags == []

        # Should accept None
        options.agent.tags = None
        assert options.agent.tags is None