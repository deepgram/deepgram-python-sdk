#!/usr/bin/env python3
"""
Example: TextBuilder with REST API TTS

This example demonstrates using TextBuilder with the REST API to generate
complete audio files with custom pronunciations and pauses.
"""

import os

from deepgram import DeepgramClient
from deepgram.helpers import TextBuilder, add_pronunciation, ssml_to_deepgram
from deepgram.speak.v1.audio.types import (
    AudioGenerateRequestEncoding,
    AudioGenerateRequestModel,
)


def example_basic_text_builder():
    """Example 1: Basic TextBuilder usage with pronunciations and pauses"""
    print("Example 1: Basic TextBuilder Usage")
    print("-" * 50)

    # Build text with pronunciations and pauses
    text = (
        TextBuilder()
        .text("Take ")
        .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
        .text(" twice daily with ")
        .pronunciation("dupilumab", "duːˈpɪljuːmæb")
        .text(" injections")
        .pause(500)
        .text(" Do not exceed prescribed dosage.")
        .build()
    )

    print(f"Generated text: {text}\n")

    # Use with Deepgram client
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = DeepgramClient(api_key=api_key)

        # Generate speech with custom pronunciations
        response = client.speak.v1.generate(
            text,
            model=AudioGenerateRequestModel.AURA_ASTERIA_EN,
            encoding=AudioGenerateRequestEncoding.LINEAR16,
        )

        # Save to file
        with open("output_example1.wav", "wb") as f:
            f.write(response)

        print("✓ Audio saved to output_example1.wav")
    else:
        print("ℹ Set DEEPGRAM_API_KEY to generate audio")


def example_add_pronunciation_function():
    """Example 2: Using add_pronunciation standalone function"""
    print("\nExample 2: Standalone add_pronunciation Function")
    print("-" * 50)

    # Start with plain text
    text = "The patient should take methotrexate weekly and adalimumab biweekly."

    # Add pronunciations for medical terms
    text = add_pronunciation(text, "methotrexate", "mɛθəˈtrɛkseɪt")
    text = add_pronunciation(text, "adalimumab", "ˌædəˈljuːməb")

    print(f"Generated text: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = DeepgramClient(api_key=api_key)

        response = client.speak.v1.generate(
            text,
            model=AudioGenerateRequestModel.AURA_ASTERIA_EN,
        )

        with open("output_example2.wav", "wb") as f:
            f.write(response)

        print("✓ Audio saved to output_example2.wav")
    else:
        print("ℹ Set DEEPGRAM_API_KEY to generate audio")


def example_ssml_migration():
    """Example 3: Migrating from SSML to Deepgram format"""
    print("\nExample 3: SSML Migration")
    print("-" * 50)

    # Existing SSML from another TTS provider
    ssml = """<speak>
        Welcome to your medication guide.
        <break time="500ms"/>
        Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme> 
        as prescribed.
        <break time="1000ms"/>
        Contact your doctor if you experience side effects.
    </speak>"""

    # Convert to Deepgram format
    text = ssml_to_deepgram(ssml)

    print(f"Converted SSML: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = DeepgramClient(api_key=api_key)

        response = client.speak.v1.generate(
            text,
            model=AudioGenerateRequestModel.AURA_ASTERIA_EN,
        )

        with open("output_example3.wav", "wb") as f:
            f.write(response)

        print("✓ Audio saved to output_example3.wav")
    else:
        print("ℹ Set DEEPGRAM_API_KEY to generate audio")


def example_mixed_ssml_and_builder():
    """Example 4: Mixing SSML parsing with additional builder methods"""
    print("\nExample 4: Mixed SSML and Builder")
    print("-" * 50)

    # Start with some SSML content
    ssml = '<speak>Take <phoneme alphabet="ipa" ph="test">medicine</phoneme> daily.</speak>'

    # Use builder to add more content
    text = (
        TextBuilder()
        .from_ssml(ssml)
        .pause(500)
        .text(" Store at room temperature.")
        .pause(500)
        .text(" Keep out of reach of children.")
        .build()
    )

    print(f"Generated text: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = DeepgramClient(api_key=api_key)

        response = client.speak.v1.generate(
            text,
            model=AudioGenerateRequestModel.AURA_ASTERIA_EN,
        )

        with open("output_example4.wav", "wb") as f:
            f.write(response)

        print("✓ Audio saved to output_example4.wav")
    else:
        print("ℹ Set DEEPGRAM_API_KEY to generate audio")


def example_pharmacy_instructions():
    """Example 5: Complete pharmacy instruction with multiple pronunciations"""
    print("\nExample 5: Pharmacy Instructions")
    print("-" * 50)

    text = (
        TextBuilder()
        .text("Prescription for ")
        .pronunciation("lisinopril", "laɪˈsɪnəprɪl")
        .pause(300)
        .text(" Take one tablet by mouth daily for hypertension.")
        .pause(500)
        .text(" Common side effects may include ")
        .pronunciation("hypotension", "ˌhaɪpoʊˈtɛnʃən")
        .text(" or dizziness.")
        .pause(500)
        .text(" Do not take with ")
        .pronunciation("aliskiren", "əˈlɪskɪrɛn")
        .text(" or ")
        .pronunciation("sacubitril", "səˈkjuːbɪtrɪl")
        .pause(500)
        .text(" Call your doctor if symptoms worsen.")
        .build()
    )

    print(f"Generated text: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = DeepgramClient(api_key=api_key)

        response = client.speak.v1.generate(
            text,
            model=AudioGenerateRequestModel.AURA_ASTERIA_EN,
            encoding=AudioGenerateRequestEncoding.LINEAR16,
        )

        with open("output_example5.wav", "wb") as f:
            f.write(response)

        print("✓ Audio saved to output_example5.wav")
    else:
        print("ℹ Set DEEPGRAM_API_KEY to generate audio")


def main():
    """Run all examples"""
    example_basic_text_builder()
    example_add_pronunciation_function()
    example_ssml_migration()
    example_mixed_ssml_and_builder()
    example_pharmacy_instructions()

    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
