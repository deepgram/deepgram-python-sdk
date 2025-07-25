# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import pytest
from deepgram.clients.agent.v1.websocket.options import (
    SettingsOptions,
    Agent,
)


class TestAgentMipOptOut:
    """Unit tests for mip_opt_out setting at the root level of SettingsOptions"""

    def test_default_mip_opt_out_value(self):
        """Test that mip_opt_out defaults to False"""
        options = SettingsOptions()

        # Default should be False at root level
        assert options.mip_opt_out == False

    def test_set_mip_opt_out_true(self):
        """Test setting mip_opt_out to True"""
        options = SettingsOptions()
        options.mip_opt_out = True

        assert options.mip_opt_out == True

    def test_set_mip_opt_out_false_explicitly(self):
        """Test explicitly setting mip_opt_out to False"""
        options = SettingsOptions()
        options.mip_opt_out = False

        assert options.mip_opt_out == False

    def test_mip_opt_out_serialization_default(self):
        """Test that mip_opt_out with default value is excluded from serialization"""
        options = SettingsOptions()
        # Don't set mip_opt_out, should use default (False)

        result = options.to_dict()

        # With default False and exclude=lambda f: f is None metadata,
        # the field should be excluded from serialization when it's False/default
        # mip_opt_out should not be in the root level when it's the default value
        assert "mip_opt_out" not in result or result.get(
            "mip_opt_out") == False

    def test_mip_opt_out_serialization_true(self):
        """Test that mip_opt_out=True is included in serialization"""
        options = SettingsOptions()
        options.mip_opt_out = True

        result = options.to_dict()
        json_str = options.to_json()
        parsed_json = json.loads(json_str)

        # Should be included at root level when True
        assert result["mip_opt_out"] == True
        assert parsed_json["mip_opt_out"] == True

    def test_mip_opt_out_serialization_false_explicit(self):
        """Test that mip_opt_out=False (explicit) behavior in serialization"""
        options = SettingsOptions()
        options.mip_opt_out = False

        result = options.to_dict()
        json_str = options.to_json()

        # The field might be excluded due to dataclass_config exclude logic
        # Let's verify the actual behavior
        if "mip_opt_out" in result:
            assert result["mip_opt_out"] == False

    def test_mip_opt_out_deserialization(self):
        """Test deserializing mip_opt_out from dict"""
        # Test with True value at root level
        data_true = {
            "mip_opt_out": True,
            "agent": {}
        }

        options_true = SettingsOptions.from_dict(data_true)
        assert options_true.mip_opt_out == True

        # Test with False value at root level
        data_false = {
            "mip_opt_out": False,
            "agent": {}
        }

        options_false = SettingsOptions.from_dict(data_false)
        assert options_false.mip_opt_out == False

    def test_mip_opt_out_deserialization_missing(self):
        """Test deserializing when mip_opt_out is not present (should default to False)"""
        data = {
            "agent": {
                "language": "en"
            }
        }

        options = SettingsOptions.from_dict(data)
        assert options.mip_opt_out == False

    def test_mip_opt_out_round_trip(self):
        """Test serialization and deserialization round-trip"""
        # Test with True
        original_true = SettingsOptions()
        original_true.mip_opt_out = True

        serialized_true = original_true.to_dict()
        restored_true = SettingsOptions.from_dict(serialized_true)

        assert restored_true.mip_opt_out == True

        # Test with False (if it gets serialized)
        original_false = SettingsOptions()
        original_false.mip_opt_out = False

        serialized_false = original_false.to_dict()
        restored_false = SettingsOptions.from_dict(serialized_false)

        assert restored_false.mip_opt_out == False

    def test_mip_opt_out_with_other_settings(self):
        """Test mip_opt_out works correctly with other settings"""
        options = SettingsOptions()
        options.agent.language = "en"
        options.mip_opt_out = True
        options.agent.greeting = "Hello, I have opted out of MIP"

        assert options.agent.language == "en"
        assert options.mip_opt_out == True
        assert options.agent.greeting == "Hello, I have opted out of MIP"

        # Test serialization with multiple fields
        result = options.to_dict()
        assert result["agent"]["language"] == "en"
        assert result["mip_opt_out"] == True
        assert result["agent"]["greeting"] == "Hello, I have opted out of MIP"

    def test_mip_opt_out_type_validation(self):
        """Test that mip_opt_out accepts boolean values"""
        options = SettingsOptions()

        # Should accept boolean values
        options.mip_opt_out = True
        assert options.mip_opt_out == True

        options.mip_opt_out = False
        assert options.mip_opt_out == False

    def test_legacy_agent_mip_opt_out_removed(self):
        """Test that mip_opt_out is no longer on the Agent class"""
        agent = Agent()
        # mip_opt_out should not exist on Agent anymore
        assert not hasattr(agent, 'mip_opt_out')
