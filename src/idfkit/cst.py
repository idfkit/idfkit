"""Concrete Syntax Tree (CST) for lossless IDF round-tripping.

A CST preserves all formatting, comments, and whitespace from the original
source file. When combined with mutation tracking on
:class:`~idfkit.objects.IDFObject`, it enables a parse-write loop that
produces byte-identical output for unmodified content while applying standard
formatting only to objects that were actually changed.

The CST is built during parsing and stored on the
:class:`~idfkit.document.IDFDocument`. Each node is either a verbatim
**text** segment (comments, blank lines, preamble) or an **object** anchor
that maps to a parsed :class:`~idfkit.objects.IDFObject`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .objects import IDFObject


def _empty_node_list() -> list[CSTNode]:
    return []


@dataclass(slots=True)
class CSTNode:
    """A single node in the concrete syntax tree.

    Attributes:
        text: The original source text for this node (verbatim).
        obj: If this node represents a parsed object, the corresponding
            :class:`~idfkit.objects.IDFObject`.  ``None`` for pure-text
            nodes (comments, blank lines, preamble/postamble).
    """

    text: str
    obj: IDFObject | None = field(default=None, repr=False)


@dataclass(slots=True)
class DocumentCST:
    """Ordered list of CST nodes representing an entire IDF source file.

    The nodes alternate between text segments and object anchors so that
    the original file can be reconstructed by concatenating the ``text``
    attributes of all nodes (replacing object nodes whose backing
    :class:`~idfkit.objects.IDFObject` was mutated with freshly
    formatted output).

    Attributes:
        nodes: Ordered list of :class:`CSTNode` instances.
        encoding: The encoding used when the file was read.
    """

    nodes: list[CSTNode] = field(default_factory=_empty_node_list)
    encoding: str = "latin-1"
