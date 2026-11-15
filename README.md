# linked_hash_map_py

A hash map that preserves insertion order of keys and supports moving existing keys to the end to implement access-order iteration.

```python
from linked_hash_map_py import LinkedHashMap

# Insertion-order map
m = LinkedHashMap()
m["a"] = 1
m["b"] = 2
m["c"] = 3
assert list(m) == ["a", "b", "c"]
m.move_to_end("a")
assert list(m) == ["b", "c", "a"]

# Access-order map (e.g. for an LRU cache)
lru = LinkedHashMap(access_order=True)
lru["x"] = 10
lru["y"] = 20
lru["z"] = 30
assert list(lru) == ["x", "y", "z"]
_ = lru["x"]
assert list(lru) == ["y", "z", "x"]
```

## Why this library exists

Python's `collections.OrderedDict` already provides insertion order and a `move_to_end` method, but it does not automatically move keys on access.  Building an LRU cache or any access-order structure usually means either subclassing `OrderedDict` or writing a linked list by hand.  This library wraps `OrderedDict` and adds a simple `access_order` flag: when enabled, every successful `get` or `__getitem__` moves the key to the end.  The trade-off is a thin abstraction over a standard library type rather than a from-scratch implementation; this keeps the code small and correct, and it means the underlying `OrderedDict` semantics (such as `popitem` ordering) are preserved.

## Edge cases

- Updating an existing key with `__setitem__` does **not** change its position.
- `get` with a default value for a missing key does **not** move anything.
- `move_to_end` raises `KeyError` if the key is absent.
- `popitem` raises `KeyError` when the map is empty.
- In access-order mode, `__getitem__` also moves the key to the end.
