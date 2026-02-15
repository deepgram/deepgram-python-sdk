"""Concrete transport implementations for the Deepgram Python SDK.

Each module provides a transport factory that can be passed to
``AsyncDeepgramClient(transport_factory=...)`` or
``DeepgramClient(transport_factory=...)``.

Available transports:

- :mod:`deepgram.transports.sagemaker` — AWS SageMaker HTTP/2 BiDi streaming (async-only)
"""

from .sagemaker import SageMakerTransport, SageMakerTransportFactory

__all__ = ["SageMakerTransport", "SageMakerTransportFactory"]
