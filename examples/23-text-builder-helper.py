#!/usr/bin/env python3
"""
Example: TextBuilder with Flux batch REST TTS

This example demonstrates using TextBuilder with English Flux batch REST
synthesis for custom pronunciations.
"""

import os

from deepgram import DeepgramClient
from deepgram.environment import DeepgramClientEnvironment
from deepgram.helpers import TextBuilder, add_pronunciation, ssml_to_deepgram


def build_client(api_key: str) -> DeepgramClient:
    """Use staging when DEEPGRAM_BASE_URL is set; otherwise use production."""
    target = os.getenv("DEEPGRAM_BASE_URL")
    if not target:
        return DeepgramClient(api_key=api_key)

    rest = target.rstrip("/").replace("wss://", "https://").replace("ws://", "http://")
    websocket = rest.replace("https://", "wss://").replace("http://", "ws://")
    return DeepgramClient(
        api_key=api_key,
        environment=DeepgramClientEnvironment(base=rest, production=websocket, agent=websocket, agent_rest=rest),
    )


def example_basic_text_builder():
    """Example 1: Basic TextBuilder usage with pronunciations"""
    print("Example 1: Basic TextBuilder Usage")
    print("-" * 50)

    # Pronunciation controls are supported on complete Flux batch requests.
    text = (
        TextBuilder()
        .text("Take ")
        .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
        .text(" twice daily with ")
        .pronunciation("dupilumab", "duːˈpɪljuːmæb")
        .text(" injections.")
        .text(" Do not exceed prescribed dosage.")
        .build()
    )

    print(f"Generated text: {text}\n")

    # Use with Deepgram client
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = build_client(api_key)

        # Generate speech with custom pronunciations
        response = client.speak.v2.audio.generate(
            text=text,
            model="flux-alexis-en",
            encoding="linear16",
        )

        # Save to file
        with open("output_example1.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)

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
        client = build_client(api_key)

        response = client.speak.v2.audio.generate(
            text=text,
            model="flux-alexis-en",
        )

        with open("output_example2.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)

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
        Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>
        as prescribed.
        Contact your doctor if you experience side effects.
    </speak>"""

    # Convert to Deepgram format
    text = ssml_to_deepgram(ssml)

    print(f"Converted SSML: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = build_client(api_key)

        response = client.speak.v2.audio.generate(
            text=text,
            model="flux-alexis-en",
        )

        with open("output_example3.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)

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
        .text(" Store at room temperature.")
        .text(" Keep out of reach of children.")
        .build()
    )

    print(f"Generated text: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = build_client(api_key)

        response = client.speak.v2.audio.generate(
            text=text,
            model="flux-alexis-en",
        )

        with open("output_example4.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)

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
        .text(". Take one tablet by mouth daily for hypertension.")
        .text(" Common side effects may include ")
        .pronunciation("hypotension", "ˌhaɪpoʊˈtɛnʃən")
        .text(" or dizziness.")
        .text(" Do not take with ")
        .pronunciation("aliskiren", "əˈlɪskɪrɛn")
        .text(" or ")
        .pronunciation("sacubitril", "səˈkjuːbɪtrɪl")
        .text(". Call your doctor if symptoms worsen.")
        .build()
    )

    print(f"Generated text: {text}")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if api_key:
        client = build_client(api_key)

        response = client.speak.v2.audio.generate(
            text=text,
            model="flux-alexis-en",
            encoding="linear16",
        )

        with open("output_example5.wav", "wb") as f:
            for chunk in response:
                f.write(chunk)

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
