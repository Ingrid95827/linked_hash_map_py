import unittest

from linked_hash_map_py import LinkedHashMap


class TestLinkedHashMap(unittest.TestCase):
    def test_insertion_order(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        self.assertEqual(list(m), ["a", "b", "c"])
        self.assertEqual(list(m.keys()), ["a", "b", "c"])
        self.assertEqual(list(m.values()), [1, 2, 3])
        self.assertEqual(list(m.items()), [("a", 1), ("b", 2), ("c", 3)])

    def test_update_existing_key_keeps_position(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        m["a"] = 10
        self.assertEqual(list(m), ["a", "b"])
        self.assertEqual(m["a"], 10)

    def test_delete_key(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        del m["a"]
        self.assertEqual(list(m), ["b"])
        with self.assertRaises(KeyError):
            del m["a"]

    def test_contains(self):
        m = LinkedHashMap()
        m["x"] = 1
        self.assertIn("x", m)
        self.assertNotIn("y", m)

    def test_len_and_clear(self):
        m = LinkedHashMap()
        self.assertEqual(len(m), 0)
        m["a"] = 1
        m["b"] = 2
        self.assertEqual(len(m), 2)
        m.clear()
        self.assertEqual(len(m), 0)
        self.assertEqual(list(m), [])

    def test_get_default(self):
        m = LinkedHashMap()
        m["a"] = 1
        self.assertEqual(m.get("a"), 1)
        self.assertIsNone(m.get("b"))
        self.assertEqual(m.get("b", 99), 99)

    def test_move_to_end(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        m.move_to_end("a")
        self.assertEqual(list(m), ["b", "c", "a"])
        with self.assertRaises(KeyError):
            m.move_to_end("z")

    def test_popitem(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        self.assertEqual(m.popitem(), ("c", 3))
        self.assertEqual(m.popitem(last=False), ("a", 1))
        self.assertEqual(list(m), ["b"])
        m.popitem()
        with self.assertRaises(KeyError):
            m.popitem()

    def test_access_order_get(self):
        m = LinkedHashMap(access_order=True)
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        self.assertEqual(list(m), ["a", "b", "c"])
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(list(m), ["b", "c", "a"])
        self.assertEqual(m.get("b"), 2)
        self.assertEqual(list(m), ["c", "a", "b"])
        # get with default on missing key should not move anything
        self.assertEqual(m.get("z", 99), 99)
        self.assertEqual(list(m), ["c", "a", "b"])

    def test_access_order_getitem(self):
        m = LinkedHashMap(access_order=True)
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        self.assertEqual(m["a"], 1)
        self.assertEqual(list(m), ["b", "c", "a"])
        self.assertEqual(m["b"], 2)
        self.assertEqual(list(m), ["c", "a", "b"])

    def test_access_order_does_not_affect_insertion_order(self):
        m = LinkedHashMap(access_order=False)
        m["a"] = 1
        m["b"] = 2
        m["c"] = 3
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(list(m), ["a", "b", "c"])
        self.assertEqual(m["b"], 2)
        self.assertEqual(list(m), ["a", "b", "c"])

    def test_repr(self):
        m = LinkedHashMap()
        m["a"] = 1
        m["b"] = 2
        self.assertEqual(repr(m), "LinkedHashMap({'a': 1, 'b': 2})")


if __name__ == "__main__":
    unittest.main()
