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

    @property
    def body_length(self) -> int:
        """Length of the node's text up to whatever separates it from the next node.

        The one place the boundary between an object and the gap after it is defined. A preserving
        write REPLACES the body and LEAVES the separator, so the same number decides where a
        rewritten object's characters end and how many newlines follow it; stating it twice is how
        the two stop agreeing, and their agreement is what makes a rendered object splice back into
        the range it came from.

        Counted rather than measured off a stripped copy: ``len(text.rstrip("\n"))`` allocates a
        second copy of every object in the file to look at its last few characters.
        """
        end = len(self.text)
        while end and self.text[end - 1] == "\n":
            end -= 1
        return end

    @property
    def separator(self) -> str:
        """Whatever ran between this node and the next, which a preserving write leaves alone."""
        return self.text[self.body_length :]


@dataclass(frozen=True, slots=True)
class SourceSpan:
    """A half-open range of :attr:`IDFDocument.raw_text`, ``end`` exclusive.

    What :meth:`IDFDocument.region_of` answers with. A frozen record rather than a tuple so that a
    reader cannot transpose the two offsets, and so that anything added beside them later is not a
    breaking change.

    Named a span rather than a region because in a building energy library "region" reads as a
    piece of a surface. The TypeScript core calls the same thing ``Region``, where it has meant a
    span of the syntax layer since that reader was written.

    Attributes:
        start: Offset of the first character, counting from zero.
        end: Offset one past the last character.
    """

    start: int
    end: int


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
