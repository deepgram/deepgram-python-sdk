"""Deepgram Proxy — drop-in proxy middleware for web applications."""

from .engine import DeepgramProxy
from .scopes import Scope

__all__ = ["DeepgramProxy", "Scope"]
