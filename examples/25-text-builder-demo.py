#!/usr/bin/env python3
"""
TextBuilder Demo - Interactive demonstration of all TextBuilder features

This demo script showcases all TextBuilder capabilities without requiring
an API key. It generates the formatted text that would be sent to the API.
"""

from deepgram import (
    TextBuilder,
    add_pronunciation,
    ssml_to_deepgram,
    validate_ipa,
    validate_pause,
)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_text_builder():
    """Demonstrate basic TextBuilder usage"""
    print_section("1. Basic TextBuilder Usage")

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

    print("\nCode:")
    print("""
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
    """)

    print("\nGenerated TTS Text:")
    print(f"  {text}")


def demo_standalone_functions():
    """Demonstrate standalone helper functions"""
    print_section("2. Standalone Helper Functions")

    # add_pronunciation
    print("\n▸ add_pronunciation()")
    text = "The patient should take methotrexate weekly."
    print(f"  Original: {text}")

    text = add_pronunciation(text, "methotrexate", "mɛθəˈtrɛkseɪt")
    print(f"  Modified: {text}")


def demo_ssml_conversion():
    """Demonstrate SSML to Deepgram conversion"""
    print_section("3. SSML Migration")

    ssml = """<speak>
    Welcome to your medication guide.
    <break time="500ms"/>
    Take <phoneme alphabet="ipa" ph="ˌæzəˈθaɪəpriːn">azathioprine</phoneme>
    as prescribed.
    <break time="1s"/>
    Contact your doctor if you experience side effects.
</speak>"""

    print("\nOriginal SSML:")
    print(ssml)

    text = ssml_to_deepgram(ssml)
    print("\nConverted to Deepgram Format:")
    print(f"  {text}")


def demo_mixed_usage():
    """Demonstrate mixing SSML with builder methods"""
    print_section("4. Mixed SSML + Builder Methods")

    ssml = '<speak>Take <phoneme alphabet="ipa" ph="test">medicine</phoneme> daily.</speak>'

    text = (
        TextBuilder()
        .from_ssml(ssml)
        .pause(500)
        .text(" Store at room temperature.")
        .pause(500)
        .text(" Keep out of reach of children.")
        .build()
    )

    print("\nStarting SSML:")
    print(f"  {ssml}")

    print("\nAdded via builder:")
    print("  .pause(500)")
    print("  .text(' Store at room temperature.')")
    print("  .pause(500)")
    print("  .text(' Keep out of reach of children.')")

    print("\nFinal Result:")
    print(f"  {text}")


def demo_validation():
    """Demonstrate validation functions"""
    print_section("5. Validation Functions")

    print("\n▸ validate_ipa()")

    # Valid IPA
    is_valid, msg = validate_ipa("ˌæzəˈθaɪəpriːn")
    print(f"  validate_ipa('ˌæzəˈθaɪəpriːn'): {is_valid} {msg}")

    # Invalid IPA (contains quote)
    is_valid, msg = validate_ipa('test"quote')
    print(f"  validate_ipa('test\"quote'): {is_valid} - {msg}")

    # Too long
    is_valid, msg = validate_ipa("x" * 101)
    print(f"  validate_ipa('x' * 101): {is_valid} - {msg}")

    print("\n▸ validate_pause()")

    # Valid pauses
    is_valid, msg = validate_pause(500)
    print(f"  validate_pause(500): {is_valid}")

    is_valid, msg = validate_pause(5000)
    print(f"  validate_pause(5000): {is_valid}")

    # Invalid pauses
    is_valid, msg = validate_pause(400)
    print(f"  validate_pause(400): {is_valid} - {msg}")

    is_valid, msg = validate_pause(550)
    print(f"  validate_pause(550): {is_valid} - {msg}")


def demo_error_handling():
    """Demonstrate error handling"""
    print_section("6. Error Handling")

    print("\n▸ Pronunciation limit (500 max)")
    try:
        builder = TextBuilder()
        for i in range(501):
            builder.pronunciation(f"word{i}", "test")
        builder.build()
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")

    print("\n▸ Pause limit (50 max)")
    try:
        builder = TextBuilder()
        for i in range(51):
            builder.pause(500)
        builder.build()
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")

    print("\n▸ Character limit (2000 max)")
    try:
        builder = TextBuilder()
        builder.text("x" * 2001)
        builder.build()
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")

    print("\n▸ Invalid pause duration")
    try:
        builder = TextBuilder()
        builder.pause(450)
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")


def demo_real_world_examples():
    """Demonstrate real-world use cases"""
    print_section("7. Real-World Examples")

    print("\n▸ Pharmacy Prescription Instructions")
    text = (
        TextBuilder()
        .text("Prescription for ")
        .pronunciation("lisinopril", "laɪˈsɪnəprɪl")
        .pause(500)
        .text(" Take one tablet daily for hypertension.")
        .pause(500)
        .text(" Common side effects may include ")
        .pronunciation("hypotension", "ˌhaɪpoʊˈtɛnʃən")
        .text(" or dizziness.")
        .build()
    )
    print(f"\n  {text}")

    print("\n▸ Medical Device Instructions")
    text = (
        TextBuilder()
        .text("Insert the ")
        .pronunciation("cannula", "ˈkænjʊlə")
        .text(" at a forty-five degree angle.")
        .pause(1000)
        .text(" Ensure the ")
        .pronunciation("catheter", "ˈkæθɪtər")
        .text(" is properly secured.")
        .build()
    )
    print(f"\n  {text}")

    print("\n▸ Scientific Terminology")
    text = (
        TextBuilder()
        .text("The study examined ")
        .pronunciation("mitochondrial", "ˌmaɪtəˈkɑːndriəl")
        .text(" function in ")
        .pronunciation("erythrocytes", "ɪˈrɪθrəsaɪts")
        .pause(500)
        .text(" using advanced imaging.")
        .build()
    )
    print(f"\n  {text}")


def demo_api_limits():
    """Display API limits summary"""
    print_section("8. API Limits Summary")

    print("\n  Limit Type                    Maximum      Unit")
    print("  " + "-" * 60)
    print("  Pronunciations per request    500          count")
    print("  Pauses per request            50           count")
    print("  Total characters              2000         characters*")
    print("  IPA string length             100          characters")
    print("  Pause duration (min)          500          milliseconds")
    print("  Pause duration (max)          5000         milliseconds")
    print("  Pause increment               100          milliseconds")
    print("\n  * Character count excludes pronunciation IPA and control syntax")


def main():
    """Run all demonstrations"""
    print("\n" + "█" * 70)
    print("  DEEPGRAM TEXTBUILDER - COMPREHENSIVE DEMONSTRATION")
    print("█" * 70)

    demo_basic_text_builder()
    demo_standalone_functions()
    demo_ssml_conversion()
    demo_mixed_usage()
    demo_validation()
    demo_error_handling()
    demo_real_world_examples()
    demo_api_limits()

    print("\n" + "=" * 70)
    print("  Demo Complete!")
    print("=" * 70)
    print("\n  For live TTS generation, see: examples/25-text-builder-helper.py")
    print("  For documentation, see: docs/TextBuilder-Guide.md")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
