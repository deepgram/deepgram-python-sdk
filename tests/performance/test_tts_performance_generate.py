"""
TTS Performance Test (Non-Streaming): SDK vs Raw httpx

Compares performance of Deepgram SDK vs raw httpx for Text-to-Speech requests
using the NON-STREAMING approach (reading entire response at once).

Key Metrics:
- TTFB (Time to First Byte): When first chunk arrives
- TTLB (Time to Last Byte): When all data has been received
- Total bytes received

Usage:
    pytest tests/performance/test_tts_performance_generate.py -v

Requirements:
    - DEEPGRAM_API_KEY environment variable must be set (or in .env file)
    - Test will be skipped if API key is not available
"""

import time
from dataclasses import dataclass

import httpx
import pytest


@dataclass
class Metrics:
    """Performance metrics for a TTS request"""

    test_type: str  # "SDK" or "Raw httpx"
    ttfb_ms: float  # Time to First Byte (milliseconds)
    ttlb_ms: float  # Time to Last Byte (milliseconds)
    total_bytes: int  # Total bytes received
    error: str = None  # Error message if any


def _test_raw_httpx_generate(api_key: str, text: str, chunk_size: int = 8192) -> Metrics:
    """
    Test raw httpx TTS request (non-streaming but reading in chunks to measure TTFB)

    Timing:
    - Start timer when request begins
    - TTFB: Record when first chunk of response body arrives
    - TTLB: Record when all bytes have been read

    Args:
        api_key: Deepgram API key
        text: Text to convert to speech
        chunk_size: Size of chunks to read

    Returns:
        Metrics object with timing data
    """
    start_time = time.perf_counter()
    ttfb_ms = 0.0
    ttlb_ms = 0.0
    total_bytes = 0
    error = None

    try:
        with httpx.Client(http2=False) as client:
            url = "https://api.deepgram.com/v1/speak"
            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json",
            }
            json_data = {"text": text}

            # Use streaming to measure TTFB properly, but consume all chunks
            with client.stream("POST", url, json=json_data, headers=headers) as response:
                response.raise_for_status()

                chunk_count = 0
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    current_time = time.perf_counter()

                    if chunk_count == 0:
                        # First chunk received
                        ttfb_ms = (current_time - start_time) * 1000

                    chunk_count += 1
                    total_bytes += len(chunk)

                # All bytes received
                ttlb_ms = (time.perf_counter() - start_time) * 1000

    except Exception as e:
        error = str(e)
        ttlb_ms = (time.perf_counter() - start_time) * 1000

    return Metrics(
        test_type="Raw httpx (generate)",
        ttfb_ms=ttfb_ms,
        ttlb_ms=ttlb_ms,
        total_bytes=total_bytes,
        error=error,
    )


def _test_sdk_generate(client, text: str) -> Metrics:
    """
    Test SDK TTS request (generate returns iterator - must consume it)

    Timing:
    - Start timer when request begins
    - TTFB: When first chunk arrives from iterator
    - TTLB: When all chunks have been consumed

    Args:
        client: DeepgramClient instance
        text: Text to convert to speech

    Returns:
        Metrics object with timing data
    """
    start_time = time.perf_counter()
    ttfb_ms = 0.0
    ttlb_ms = 0.0
    total_bytes = 0
    error = None

    try:
        # generate() returns an iterator - must consume it to get actual data
        response_iterator = client.speak.v1.audio.generate(text=text)

        # Consume the iterator to actually fetch the data
        chunk_count = 0
        for chunk in response_iterator:
            current_time = time.perf_counter()

            if chunk_count == 0:
                # First chunk received
                ttfb_ms = (current_time - start_time) * 1000

            chunk_count += 1
            total_bytes += len(chunk)

        # All chunks received
        ttlb_ms = (time.perf_counter() - start_time) * 1000

    except Exception as e:
        error = str(e)
        ttlb_ms = (time.perf_counter() - start_time) * 1000

    return Metrics(
        test_type="SDK (generate)",
        ttfb_ms=ttfb_ms,
        ttlb_ms=ttlb_ms,
        total_bytes=total_bytes,
        error=error,
    )


@pytest.mark.performance
@pytest.mark.requires_api_key
def test_tts_generate_performance(api_key, deepgram_client, generate_test_text):
    """
    Compare TTS generate (non-streaming) performance between SDK and raw httpx.

    This test measures and compares:
    - Time to First Byte (TTFB)
    - Time to Last Byte (TTLB)
    - Total bytes received

    The test will be skipped if DEEPGRAM_API_KEY is not set.
    """
    # Generate test text
    text = generate_test_text(1000)
    chunk_size = 8192

    # Test raw httpx
    raw_metrics = _test_raw_httpx_generate(api_key, text, chunk_size)
    assert raw_metrics.error is None, f"Raw httpx test failed: {raw_metrics.error}"
    assert raw_metrics.total_bytes > 0, "Raw httpx received no data"

    # Test SDK
    sdk_metrics = _test_sdk_generate(deepgram_client, text)
    assert sdk_metrics.error is None, f"SDK test failed: {sdk_metrics.error}"
    assert sdk_metrics.total_bytes > 0, "SDK received no data"

    # Verify both received the same amount of data
    assert (
        sdk_metrics.total_bytes == raw_metrics.total_bytes
    ), f"Data size mismatch: SDK={sdk_metrics.total_bytes}, Raw={raw_metrics.total_bytes}"

    # Calculate differences
    ttfb_diff = sdk_metrics.ttfb_ms - raw_metrics.ttfb_ms
    ttlb_diff = sdk_metrics.ttlb_ms - raw_metrics.ttlb_ms

    # Print performance comparison
    print("\n" + "=" * 70)
    print("TTS GENERATE (NON-STREAMING) PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"\nRaw httpx (generate):")
    print(f"  TTFB: {raw_metrics.ttfb_ms:>8.1f} ms")
    print(f"  TTLB: {raw_metrics.ttlb_ms:>8.1f} ms")
    print(f"  Bytes: {raw_metrics.total_bytes:>7,} bytes")
    print(f"\nSDK (generate):")
    print(f"  TTFB: {sdk_metrics.ttfb_ms:>8.1f} ms")
    print(f"  TTLB: {sdk_metrics.ttlb_ms:>8.1f} ms")
    print(f"  Bytes: {sdk_metrics.total_bytes:>7,} bytes")
    print(f"\nDifferences (SDK - Raw):")
    print(f"  TTFB: {ttfb_diff:>+8.1f} ms")
    print(f"  TTLB: {ttlb_diff:>+8.1f} ms")
    print("=" * 70)

    # Performance assertions (warnings, not failures)
    # We expect SDK to be within reasonable overhead
    if ttfb_diff > 100:
        print(
            f"\n⚠️  Warning: SDK TTFB is {ttfb_diff:.0f}ms slower than raw httpx"
        )
    if ttlb_diff > 200:
        print(
            f"\n⚠️  Warning: SDK TTLB is {ttlb_diff:.0f}ms slower than raw httpx"
        )


@pytest.mark.performance
@pytest.mark.requires_api_key
@pytest.mark.parametrize("text_length", [100, 500, 1000, 2000])
def test_tts_generate_performance_various_lengths(
    api_key, deepgram_client, generate_test_text, text_length
):
    """
    Test TTS generate (non-streaming) performance with various text lengths.

    This test ensures the SDK performs reasonably across different text sizes.
    The test will be skipped if DEEPGRAM_API_KEY is not set.
    """
    # Generate test text
    text = generate_test_text(text_length)

    # Test SDK
    sdk_metrics = _test_sdk_generate(deepgram_client, text)
    assert sdk_metrics.error is None, f"SDK test failed: {sdk_metrics.error}"
    assert sdk_metrics.total_bytes > 0, "SDK received no data"

    print(f"\n[Text length: {text_length}]")
    print(f"  TTFB: {sdk_metrics.ttfb_ms:.1f} ms")
    print(f"  TTLB: {sdk_metrics.ttlb_ms:.1f} ms")
    print(f"  Bytes: {sdk_metrics.total_bytes:,}")

