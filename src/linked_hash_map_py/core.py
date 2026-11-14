"""Core implementation of the linked hash map."""

from collections import OrderedDict
from typing import Any, Iterator, Optional, TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')


class LinkedHashMap(Generic[K, V]):
    """A hash map that preserves insertion order and supports access-order.

    This class wraps ``collections.OrderedDict`` to provide a simple
    interface for moving existing keys to the end.  The underlying
    ``OrderedDict`` already maintains insertion order and supports
    ``move_to_end``, so we delegate to it rather than implementing a
    linked list ourselves.  This keeps the code small and leverages a
    well-tested standard library type.

    The map can operate in two modes: insertion order (default) and
    access order.  In access-order mode, every successful lookup via
    ``get`` moves the key to the end, so iteration reflects least
    recently used to most recently used.  This is useful for building
    LRU caches.

    Args:
        access_order: If True, ``get`` moves the key to the end.
            Defaults to False (insertion order).
    """

    def __init__(self, access_order: bool = False) -> None:
        self._data: OrderedDict[K, V] = OrderedDict()
        self._access_order = access_order

    def __setitem__(self, key: K, value: V) -> None:
        """Set the value for *key*.

        If *key* already exists, its value is updated and its position
        is unchanged.  If *key* is new, it is appended to the end.
        """
        self._data[key] = value

    def __getitem__(self, key: K) -> V:
        """Return the value for *key*.

        Raises KeyError if *key* is not present.  In access-order mode,
        a successful lookup moves the key to the end.
        """
        value = self._data[key]
        if self._access_order:
            self._data.move_to_end(key)
        return value

    def __delitem__(self, key: K) -> None:
        """Remove *key* from the map.  Raises KeyError if not present."""
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        """Return True if *key* is in the map."""
        return key in self._data

    def __iter__(self) -> Iterator[K]:
        """Iterate over keys in their current order."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of entries."""
        return len(self._data)

    def __repr__(self) -> str:
        """Return a string representation of the map."""
        return f"{self.__class__.__name__}({dict(self._data)!r})"

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Return the value for *key* if present, else *default*.

        In access-order mode, a successful lookup moves the key to the
        end.  A lookup that falls back to *default* does not move
        anything.
        """
        if key in self._data:
            value = self._data[key]
            if self._access_order:
                self._data.move_to_end(key)
            return value
        return default

    def move_to_end(self, key: K) -> None:
        """Move an existing *key* to the end of the order.

        Raises KeyError if *key* is not present.  This is the building
        block for access-order iteration and is also useful when the
        caller wants to explicitly refresh a key's position.
        """
        self._data.move_to_end(key)

    def popitem(self, last: bool = True) -> tuple[K, V]:
        """Remove and return a (key, value) pair.

        Args:
            last: If True (default), remove the last item; if False,
                remove the first item.

        Raises KeyError if the map is empty.
        """
        return self._data.popitem(last=last)

    def keys(self) -> Iterator[K]:
        """Return an iterator over the keys."""
        return iter(self._data.keys())

    def values(self) -> Iterator[V]:
        """Return an iterator over the values."""
        return iter(self._data.values())

    def items(self) -> Iterator[tuple[K, V]]:
        """Return an iterator over (key, value) pairs."""
        return iter(self._data.items())

    def clear(self) -> None:
        """Remove all entries."""
        self._data.clear()
