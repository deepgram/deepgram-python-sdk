"""
Wire tests module.

This module patches datetime.fromisoformat() to handle 'Z' suffix for Python 3.10 compatibility.
Python 3.10's datetime.fromisoformat() doesn't support 'Z' suffix (added in 3.11),
so we convert 'Z' to '+00:00' automatically.

This uses a module-level import hook to intercept datetime imports.
"""

import sys
from datetime import datetime as _original_datetime

# Store original function
_original_fromisoformat = _original_datetime.fromisoformat


def _patched_fromisoformat(date_string: str) -> _original_datetime:
    """Patched version that converts 'Z' to '+00:00' for Python 3.10 compatibility."""
    if date_string.endswith("Z"):
        date_string = date_string[:-1] + "+00:00"
    return _original_fromisoformat(date_string)


# Create a wrapper datetime class that uses our patched fromisoformat
class _DatetimeWrapper(_original_datetime):
    """Wrapper class that patches fromisoformat for Python 3.10 compatibility."""

    @staticmethod
    def fromisoformat(date_string: str) -> _original_datetime:
        """Patched fromisoformat that handles 'Z' suffix."""
        return _patched_fromisoformat(date_string)


# Replace datetime in the datetime module's __dict__ by creating a wrapper module
# This intercepts imports of 'from datetime import datetime'
_datetime_module = sys.modules["datetime"]
_datetime_module.datetime = _DatetimeWrapper
