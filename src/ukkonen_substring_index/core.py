from __future__ import annotations


class _Node:
    __slots__ = ("children", "link", "start", "end", "suffix_index")

    def __init__(self, start: int, end: int) -> None:
        self.children: dict[str, _Node] = {}
        self.link: _Node | None = None
        self.start = start
        self.end = end
        self.suffix_index: int = -1


class SuffixTree:
    _SENTINEL = "\x00"

    def __init__(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        if self._SENTINEL in text:
            raise ValueError(
                "input must not contain the internal sentinel "
                f"{self._SENTINEL!r}; reserved for suffix termination"
            )
        self._original = text
        self._text = text + self._SENTINEL
        self._length = len(self._text)
        self._end_ref = [0]
        self._root = _Node(-1, -1)
        self._active_node: _Node = self._root
        self._active_edge = -1
        self._active_length = 0
        self._remaining = 0
        self._build()

    def _build(self) -> None:
        for i in range(self._length):
            self._end_ref[0] = i
            self._remaining += 1
            last_new: _Node | None = None
            while self._remaining > 0:
                if self._active_length == 0:
                    self._active_edge = i
                edge_char = self._text[self._active_edge]
                child = self._active_node.children.get(edge_char)
                if child is None:
                    leaf = _Node(i, -1)
                    leaf.suffix_index = i
                    self._active_node.children[edge_char] = leaf
                    if last_new is not None:
                        last_new.link = self._active_node
                        last_new = None
                else:
                    edge_len = self._edge_length(child)
                    if self._active_length >= edge_len:
                        self._active_edge += edge_len
                        self._active_length -= edge_len
                        self._active_node = child
                        continue
                    if self._text[child.start + self._active_length] == self._text[i]:
                        if (
                            last_new is not None
                            and self._active_node is not self._root
                        ):
                            last_new.link = self._active_node
                            last_new = None
                        self._active_length += 1
                        break
                    split = _Node(child.start, child.start + self._active_length - 1)
                    self._active_node.children[edge_char] = split
                    child.start += self._active_length
                    leaf = _Node(i, -1)
                    leaf.suffix_index = i
                    split.children[self._text[i]] = leaf
                    split.children[self._text[child.start]] = child
                    if last_new is not None:
                        last_new.link = split
                    last_new = split
                    if split is self._root:
                        self._root.link = self._root
                self._remaining -= 1
                if self._active_node is self._root and self._active_length > 0:
                    self._active_length -= 1
                    self._active_edge = i - self._remaining + 1
                elif self._active_node.link is not None:
                    self._active_node = self._active_node.link
                else:
                    self._active_node = self._root

    def _edge_length(self, node: _Node) -> int:
        if node.end == -1:
            return self._end_ref[0] - node.start + 1
        return node.end - node.start + 1

    def _edge_label(self, node: _Node) -> str:
        if node.end == -1:
            return self._text[node.start : self._end_ref[0] + 1]
        return self._text[node.start : node.end + 1]

    def contains(self, pattern: str) -> bool:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a str")
        return self._match(pattern) is not None

    def _min_leaf_index(self, node: _Node) -> int:
        if node.suffix_index >= 0:
            return node.suffix_index
        best = None
        for child in node.children.values():
            val = self._min_leaf_index(child)
            if best is None or val < best:
                best = val
        return best if best is not None else 0

    def _match(self, pattern: str) -> int | None:
        if pattern == "":
            return 0
        node = self._root
        pos = 0
        n = len(pattern)
        child = node.children.get(pattern[pos])
        if child is None:
            return None
        while pos < n:
            node = child
            label = self._edge_label(node)
            for lc in label:
                if pos >= n:
                    return self._min_leaf_index(node)
                if lc != pattern[pos]:
                    return None
                pos += 1
            if pos >= n:
                return self._min_leaf_index(node)
            child = node.children.get(pattern[pos])
            if child is None:
                return None
        return None

    def find(self, pattern: str) -> int | None:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a str")
        return self._match(pattern)
