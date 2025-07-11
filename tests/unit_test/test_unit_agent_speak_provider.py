#!/usr/bin/env python3
"""
Test script to verify both single provider and array provider formats work correctly
for agent speak configuration.
"""

import json
import pytest
from deepgram.clients.agent.v1.websocket.options import (
    SettingsOptions,
    UpdateSpeakOptions,
    Agent,
    Speak,
    Provider,
    Endpoint,
    Header
)


class TestAgentSpeakSingleProvider:
    """Test single provider format for agent speak configuration (backward compatibility)"""

    def test_single_provider_creation(self):
        """Test creating agent speak with single provider format"""
        options = SettingsOptions()
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-2-thalia-en"

        # Verify the speak field is a single Speak object
        assert isinstance(options.agent.speak, Speak)
        assert options.agent.speak.provider.type == "deepgram"
        assert options.agent.speak.provider.model == "aura-2-thalia-en"

    def test_single_provider_serialization(self):
        """Test serialization of single provider format"""
        options = SettingsOptions()
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-2-thalia-en"

        result = options.to_dict()
        speak_dict = result["agent"]["speak"]

        # Verify structure
        assert isinstance(speak_dict, dict)
        assert "provider" in speak_dict
        assert speak_dict["provider"]["type"] == "deepgram"
        assert speak_dict["provider"]["model"] == "aura-2-thalia-en"

    def test_single_provider_with_endpoint(self):
        """Test single provider with custom endpoint"""
        options = SettingsOptions()
        options.agent.speak.provider.type = "custom"
        options.agent.speak.provider.model = "custom-model"
        options.agent.speak.endpoint = Endpoint()
        options.agent.speak.endpoint.url = "https://custom.api.com/speak"
        options.agent.speak.endpoint.headers = [
            Header(key="authorization", value="Bearer custom-token")
        ]

        result = options.to_dict()
        speak_dict = result["agent"]["speak"]

        assert speak_dict["provider"]["type"] == "custom"
        assert speak_dict["endpoint"]["url"] == "https://custom.api.com/speak"
        assert len(speak_dict["endpoint"]["headers"]) == 1
        assert speak_dict["endpoint"]["headers"][0]["key"] == "authorization"

    def test_single_provider_from_dict(self):
        """Test deserialization of single provider format"""
        single_data = {
            "agent": {
                "speak": {
                    "provider": {"type": "deepgram", "model": "aura-2-thalia-en"}
                }
            }
        }

        options = SettingsOptions.from_dict(single_data)
        assert isinstance(options.agent.speak, Speak)
        assert options.agent.speak.provider.type == "deepgram"
        assert options.agent.speak.provider.model == "aura-2-thalia-en"


class TestAgentSpeakArrayProvider:
    """Test array provider format for agent speak configuration (new functionality)"""

    def test_array_provider_creation(self):
        """Test creating agent speak with array provider format"""
        # Create individual Speak objects
        deepgram_speak = Speak()
        deepgram_speak.provider.type = "deepgram"
        deepgram_speak.provider.model = "aura-2-zeus-en"

        openai_speak = Speak()
        openai_speak.provider.type = "open_ai"
        openai_speak.provider.model = "tts-1"
        openai_speak.provider.voice = "shimmer"

        # Create settings with array format
        options = SettingsOptions()
        options.agent.speak = [deepgram_speak, openai_speak]

        # Verify the speak field is a list of Speak objects
        assert isinstance(options.agent.speak, list)
        assert len(options.agent.speak) == 2
        assert isinstance(options.agent.speak[0], Speak)
        assert isinstance(options.agent.speak[1], Speak)

    def test_array_provider_serialization(self):
        """Test serialization of array provider format"""
        # Create individual Speak objects
        deepgram_speak = Speak()
        deepgram_speak.provider.type = "deepgram"
        deepgram_speak.provider.model = "aura-2-zeus-en"

        openai_speak = Speak()
        openai_speak.provider.type = "open_ai"
        openai_speak.provider.model = "tts-1"
        openai_speak.provider.voice = "shimmer"

        # Create endpoint for OpenAI
        openai_speak.endpoint = Endpoint()
        openai_speak.endpoint.url = "https://api.openai.com/v1/audio/speech"
        openai_speak.endpoint.headers = [
            Header(key="authorization", value="Bearer {{OPENAI_API_KEY}}")
        ]

        # Create settings with array format
        options = SettingsOptions()
        options.agent.speak = [deepgram_speak, openai_speak]

        result = options.to_dict()
        speak_array = result["agent"]["speak"]

        # Verify structure
        assert isinstance(speak_array, list)
        assert len(speak_array) == 2

        # Check first provider (Deepgram)
        assert speak_array[0]["provider"]["type"] == "deepgram"
        assert speak_array[0]["provider"]["model"] == "aura-2-zeus-en"

        # Check second provider (OpenAI)
        assert speak_array[1]["provider"]["type"] == "open_ai"
        assert speak_array[1]["provider"]["model"] == "tts-1"
        assert speak_array[1]["provider"]["voice"] == "shimmer"
        assert speak_array[1]["endpoint"]["url"] == "https://api.openai.com/v1/audio/speech"

    def test_array_provider_from_dict(self):
        """Test deserialization of array provider format"""
        array_data = {
            "agent": {
                "speak": [
                    {"provider": {"type": "deepgram", "model": "aura-2-zeus-en"}},
                    {"provider": {"type": "open_ai", "model": "tts-1", "voice": "shimmer"}}
                ]
            }
        }

        options = SettingsOptions.from_dict(array_data)
        assert isinstance(options.agent.speak, list)
        assert len(options.agent.speak) == 2
        assert options.agent.speak[0].provider.type == "deepgram"
        assert options.agent.speak[1].provider.type == "open_ai"
        assert options.agent.speak[1].provider.voice == "shimmer"

    def test_array_provider_with_multiple_endpoints(self):
        """Test array provider with different endpoints"""
        providers = []

        # Provider 1: Deepgram with custom endpoint
        deepgram_speak = Speak()
        deepgram_speak.provider.type = "deepgram"
        deepgram_speak.provider.model = "aura-2-zeus-en"
        deepgram_speak.endpoint = Endpoint()
        deepgram_speak.endpoint.url = "https://api.deepgram.com/v1/speak"
        providers.append(deepgram_speak)

        # Provider 2: OpenAI TTS
        openai_speak = Speak()
        openai_speak.provider.type = "open_ai"
        openai_speak.provider.model = "tts-1"
        openai_speak.endpoint = Endpoint()
        openai_speak.endpoint.url = "https://api.openai.com/v1/audio/speech"
        providers.append(openai_speak)

        # Provider 3: Custom TTS provider
        custom_speak = Speak()
        custom_speak.provider.type = "custom"
        custom_speak.provider.model = "custom-tts-v1"
        custom_speak.endpoint = Endpoint()
        custom_speak.endpoint.url = "https://custom-tts.example.com/v1/synthesize"
        custom_speak.endpoint.headers = [
            Header(key="x-api-key", value="custom-api-key"),
            Header(key="content-type", value="application/json")
        ]
        providers.append(custom_speak)

        options = SettingsOptions()
        options.agent.speak = providers

        result = options.to_dict()
        speak_array = result["agent"]["speak"]

        assert len(speak_array) == 3
        assert speak_array[0]["endpoint"]["url"] == "https://api.deepgram.com/v1/speak"
        assert speak_array[1]["endpoint"]["url"] == "https://api.openai.com/v1/audio/speech"
        assert speak_array[2]["endpoint"]["url"] == "https://custom-tts.example.com/v1/synthesize"
        assert len(speak_array[2]["endpoint"]["headers"]) == 2


class TestUpdateSpeakOptions:
    """Test UpdateSpeakOptions with both single and array formats"""

    def test_update_speak_single_provider(self):
        """Test UpdateSpeakOptions with single provider"""
        speak = Speak()
        speak.provider.type = "deepgram"
        speak.provider.model = "aura-2-hera-en"

        update_options = UpdateSpeakOptions()
        update_options.speak = speak

        result = update_options.to_dict()

        assert result["type"] == "UpdateSpeak"
        assert isinstance(result["speak"], dict)
        assert result["speak"]["provider"]["type"] == "deepgram"
        assert result["speak"]["provider"]["model"] == "aura-2-hera-en"

    def test_update_speak_array_providers(self):
        """Test UpdateSpeakOptions with array of providers"""
        provider1 = Speak()
        provider1.provider.type = "deepgram"
        provider1.provider.model = "aura-2-hera-en"

        provider2 = Speak()
        provider2.provider.type = "open_ai"
        provider2.provider.model = "tts-1"

        update_options = UpdateSpeakOptions()
        update_options.speak = [provider1, provider2]

        result = update_options.to_dict()

        assert result["type"] == "UpdateSpeak"
        assert isinstance(result["speak"], list)
        assert len(result["speak"]) == 2
        assert result["speak"][0]["provider"]["type"] == "deepgram"
        assert result["speak"][1]["provider"]["type"] == "open_ai"


class TestAgentSpeakRoundTrip:
    """Test serialization and deserialization round-trip for both formats"""

    def test_single_provider_round_trip(self):
        """Test round-trip serialization/deserialization for single provider"""
        # Create original
        original = SettingsOptions()
        original.agent.speak.provider.type = "deepgram"
        original.agent.speak.provider.model = "aura-2-thalia-en"
        original.agent.speak.endpoint = Endpoint()
        original.agent.speak.endpoint.url = "https://api.deepgram.com/v1/speak"

        # Serialize and deserialize
        serialized = original.to_dict()
        restored = SettingsOptions.from_dict(serialized)

        # Verify
        assert isinstance(restored.agent.speak, Speak)
        assert restored.agent.speak.provider.type == "deepgram"
        assert restored.agent.speak.provider.model == "aura-2-thalia-en"
        assert restored.agent.speak.endpoint.url == "https://api.deepgram.com/v1/speak"

    def test_array_provider_round_trip(self):
        """Test round-trip serialization/deserialization for array providers"""
        # Create original
        provider1 = Speak()
        provider1.provider.type = "deepgram"
        provider1.provider.model = "aura-2-zeus-en"

        provider2 = Speak()
        provider2.provider.type = "open_ai"
        provider2.provider.model = "tts-1"
        provider2.endpoint = Endpoint()
        provider2.endpoint.url = "https://api.openai.com/v1/audio/speech"

        original = SettingsOptions()
        original.agent.speak = [provider1, provider2]

        # Serialize and deserialize
        serialized = original.to_dict()
        restored = SettingsOptions.from_dict(serialized)

        # Verify
        assert isinstance(restored.agent.speak, list)
        assert len(restored.agent.speak) == 2
        assert restored.agent.speak[0].provider.type == "deepgram"
        assert restored.agent.speak[1].provider.type == "open_ai"
        assert restored.agent.speak[1].endpoint.url == "https://api.openai.com/v1/audio/speech"


class TestAgentSpeakProviderConfig:
    """Test various configuration scenarios"""

    def test_default_speak_configuration(self):
        """Test default speak configuration"""
        options = SettingsOptions()

        # Should default to single provider format
        assert isinstance(options.agent.speak, Speak)
        assert hasattr(options.agent.speak, 'provider')

    def test_arbitrary_provider_attributes(self):
        """Test that arbitrary provider attributes are preserved"""
        options = SettingsOptions()
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-2-thalia-en"
        options.agent.speak.provider.custom_attribute = "custom_value"
        options.agent.speak.provider.priority = 1

        result = options.to_dict()
        provider = result["agent"]["speak"]["provider"]

        assert provider["type"] == "deepgram"
        assert provider["model"] == "aura-2-thalia-en"
        assert provider["custom_attribute"] == "custom_value"
        assert provider["priority"] == 1

    def test_mixed_provider_attributes_in_array(self):
        """Test that different providers can have different attributes"""
        provider1 = Speak()
        provider1.provider.type = "deepgram"
        provider1.provider.model = "aura-2-zeus-en"
        provider1.provider.priority = 1

        provider2 = Speak()
        provider2.provider.type = "open_ai"
        provider2.provider.model = "tts-1"
        provider2.provider.voice = "shimmer"
        provider2.provider.speed = 1.0

        options = SettingsOptions()
        options.agent.speak = [provider1, provider2]

        result = options.to_dict()
        speak_array = result["agent"]["speak"]

        # First provider attributes
        assert speak_array[0]["provider"]["type"] == "deepgram"
        assert speak_array[0]["provider"]["priority"] == 1
        assert "voice" not in speak_array[0]["provider"]

        # Second provider attributes
        assert speak_array[1]["provider"]["type"] == "open_ai"
        assert speak_array[1]["provider"]["voice"] == "shimmer"
        assert speak_array[1]["provider"]["speed"] == 1.0
        assert "priority" not in speak_array[1]["provider"]

