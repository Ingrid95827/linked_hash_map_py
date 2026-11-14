"""Linked hash map implementation.

This package provides a hash map that preserves insertion order of keys and
supports moving existing keys to the end to implement access-order iteration.
"""

from .core import LinkedHashMap

__all__ = ["LinkedHashMap"]
