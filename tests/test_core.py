import unittest

from ukkonen_substring_index import SuffixTree


class TestConstruction(unittest.TestCase):
    def test_empty_string(self):
        tree = SuffixTree("")
        self.assertTrue(tree.contains(""))
        self.assertFalse(tree.contains("a"))

    def test_single_char(self):
        tree = SuffixTree("a")
        self.assertTrue(tree.contains("a"))
        self.assertFalse(tree.contains("b"))

    def test_all_identical(self):
        tree = SuffixTree("aaaaa")
        for length in range(1, 6):
            self.assertTrue(tree.contains("a" * length))
        self.assertFalse(tree.contains("aaab"))


class TestContains(unittest.TestCase):
    def test_present_and_absent(self):
        tree = SuffixTree("banana")
        for s in ("banana", "anana", "nana", "ana", "na", "a", "ban"):
            with self.subTest(s=s):
                self.assertTrue(tree.contains(s))
        for s in ("x", "bananas", "banann", "ab"):
            with self.subTest(s=s):
                self.assertFalse(tree.contains(s))

    def test_full_match_only(self):
        tree = SuffixTree("abc")
        self.assertTrue(tree.contains("abc"))
        self.assertFalse(tree.contains("abcd"))
        self.assertFalse(tree.contains("abx"))


class TestFind(unittest.TestCase):
    def test_returns_first_position(self):
        tree = SuffixTree("banana")
        self.assertEqual(tree.find("banana"), 0)
        self.assertEqual(tree.find("anana"), 1)
        self.assertEqual(tree.find("nana"), 2)
        self.assertEqual(tree.find("ana"), 1)
        self.assertEqual(tree.find("na"), 2)
        self.assertEqual(tree.find("a"), 1)
        self.assertEqual(tree.find("ban"), 0)

    def test_returns_zero_for_empty(self):
        tree = SuffixTree("abc")
        self.assertEqual(tree.find(""), 0)

    def test_returns_none_when_absent(self):
        tree = SuffixTree("banana")
        self.assertIsNone(tree.find("xyz"))
        self.assertIsNone(tree.find("bananaX"))

    def test_find_when_substring_spans_multiple_edges(self):
        # "ssissi" forces a match across an internal-node boundary.
        tree = SuffixTree("mississippi")
        self.assertEqual(tree.find("issi"), 1)
        self.assertEqual(tree.find("ssissi"), 2)
        self.assertEqual(tree.find("ississi"), 1)


class TestEdgeCases(unittest.TestCase):
    def test_repeated_prefix(self):
        tree = SuffixTree("abcabcabc")
        self.assertEqual(tree.find("abcabc"), 0)
        self.assertTrue(tree.contains("abcabcabc"))
        self.assertFalse(tree.contains("abcabcabca"))

    def test_overlapping_repeats(self):
        tree = SuffixTree("ababab")
        self.assertEqual(tree.find("ababab"), 0)
        self.assertEqual(tree.find("abab"), 0)
        self.assertEqual(tree.find("baba"), 1)
        self.assertTrue(tree.contains("babab"))

    def test_unicode_input(self):
        tree = SuffixTree("\u00e9\u00e9abc\u00e9")
        self.assertTrue(tree.contains("\u00e9\u00e9"))
        self.assertEqual(tree.find("abc"), 2)
        self.assertEqual(tree.find("\u00e9"), 0)

    def test_rejects_sentinel_character(self):
        with self.assertRaises(ValueError):
            SuffixTree("a\x00b")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            SuffixTree(123)  # type: ignore[arg-type]

    def test_query_rejects_non_string(self):
        tree = SuffixTree("abc")
        with self.assertRaises(TypeError):
            tree.contains(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tree.find(None)  # type: ignore[arg-type]


class TestLongInput(unittest.TestCase):
    def test_long_repeating_string(self):
        s = "abcdefgh" * 100
        tree = SuffixTree(s)
        self.assertTrue(tree.contains("abcdefgh" * 50))
        self.assertEqual(tree.find("fghabcd"), 5)
        self.assertIsNone(tree.find("notthere"))


if __name__ == "__main__":
    unittest.main()
