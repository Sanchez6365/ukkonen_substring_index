# ukkonen_substring_index

A suffix-tree construction algorithm that builds the tree online, one input character at a time, walking the active-point state for each suffix extension. This gives O(n) construction and O(m) substring query for a pattern of length m.

## Usage

```python
from ukkonen_substring_index import SuffixTree

tree = SuffixTree("banana")
tree.contains("ana")   # True
tree.find("ana")       # 1 — index of first occurrence
tree.find("xyz")       # None
```

## Why this exists

The specific problem: building a substring index in a single left-to-right pass and querying it in time proportional to the pattern rather than the text. Ukkonen's algorithm solves the first half; the tree structure solves the second. Internal nodes are cached during construction so that descending the tree on a query avoids repeated dictionary allocations for the same branch points.

The trade-off: a suffix tree uses more memory than a suffix array for the same input, and this implementation stores children in plain `dict` objects keyed by single characters. That is fine for typical natural-language or DNA-style inputs; it would be wasteful for a very large alphabet where most nodes have one child.

## Edge cases

The input must not contain the NUL character (`\x00`); it is used internally as a sentinel to guarantee that every suffix ends at a distinct leaf. Passing a string that contains it raises `ValueError`. An empty pattern is defined to match at index 0.

Construction is deterministic and does not depend on wall-clock time.
