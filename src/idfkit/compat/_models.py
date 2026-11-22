"""Data models for the version compatibility checker."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class CompatSeverity(Enum):
    """Severity level for compatibility diagnostics."""

    ERROR = "error"
    WARNING = "warning"


class LiteralKind(Enum):
    """What a extracted string literal represents in schema terms."""

    OBJECT_TYPE = "object_type"
    CHOICE_VALUE = "choice_value"
    FIELD_NAME = "field_name"


@dataclass(frozen=True, slots=True)
class ExtractedLiteral:
    """A string literal extracted from Python source that may refer to a schema concept.

    Attributes:
        value: The literal string value.
        kind: Whether this represents an object type or a choice value.
        line: 1-based line number in source.
        col: 0-based column offset of the literal start.
        end_col: 0-based column offset of the literal end.
        obj_type: For CHOICE_VALUE and FIELD_NAME, the object type context (e.g. ``"Material"``).
        field_name: For CHOICE_VALUE, the field name context (e.g. ``"roughness"``).
        call: The method the literal is an argument of (``"add"`` or ``"get_collection"``), or
            ``None`` for a subscript.
        receiver: Source text of the object the method was called on or subscripted
            (``"doc"`` for ``doc.get_collection("Zone")`` and ``doc["Zone"]``), or ``None``.
        in_idfkit_add: Whether the literal is an argument of idfkit's ``add()`` that raises when no
            release accepts it, the only literals reported as ``C006``. The file imports idfkit;
            an object type is on a receiver known to be a document with a schema (a collection's
            ``add()`` takes a name first); a choice value is in a call given more than its first
            argument (``set.add`` takes one) and without ``validate=False``; a field name is in a
            call given more than its first argument, with or without ``validate=False``, which
            refuses an unknown field too.
        releases: The supported releases the literal's code can run against, when the code
            around it narrows the document (``as_version(doc, IDFDocumentV9_4)[...]``, or a lookup
            inside ``if doc.version >= (9, 4, 0):``); ``None`` when nothing narrows it.
        keyword: For FIELD_NAME, whether the name was passed as a keyword argument
            (``ceiling_height=3.0``) rather than as a key of a dict of fields.
    """

    value: str
    kind: LiteralKind
    line: int
    col: int
    end_col: int
    obj_type: str | None = None
    field_name: str | None = None
    call: str | None = None
    receiver: str | None = None
    releases: frozenset[tuple[int, int, int]] | None = None
    in_idfkit_add: bool = False
    keyword: bool = False


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A compatibility issue found in a Python source file.

    Attributes:
        code: Machine-readable diagnostic code (e.g. ``"C001"``).
        message: Human-readable description of the issue.
        severity: Issue severity (error or warning).
        filename: Path to the source file.
        line: 1-based line number.
        col: 0-based column offset.
        end_col: 0-based end column offset.
        from_version: Version string where the literal is valid. For a rule that is not about a
            difference between versions (``C003``, ``C004``, ``C006``), the lowest target version.
        to_version: Version string where the literal is invalid: for ``C001`` and ``C002``, the
            earliest of [missing_in][idfkit.compat.Diagnostic.missing_in]. For a rule that is not about a difference
            between versions, the highest target version.
        suggested_fix: Optional suggested replacement or action.
        missing_in: For ``C001`` and ``C002``, every target release (in the code's scope) that
            lacks the literal, oldest first. One finding covers all of them.
    """

    code: str
    message: str
    severity: CompatSeverity
    filename: str
    line: int
    col: int
    end_col: int
    from_version: str
    to_version: str
    suggested_fix: str | None = None
    missing_in: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary for JSON output."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
            "filename": self.filename,
            "line": self.line,
            "col": self.col,
            "end_col": self.end_col,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "suggested_fix": self.suggested_fix,
            "missing_in": list(self.missing_in),
        }

    def __str__(self) -> str:
        return f"{self.filename}:{self.line}:{self.col}: {self.code} [{self.severity.value}] {self.message}"


DIAGNOSTIC_CODES: dict[str, str] = {
    "C001": "Object type exists in one schema version but not another",
    "C002": "Enumerated choice value for a field exists in one version but not another",
    "C003": "Object type passed to get_collection exists in none of the target versions",
    "C004": "Literal object type passed to get_collection, whose result is untyped; index the document instead",
    "C005": "Suppression comment that silences nothing, or names an unknown rule",
    "C006": "Object type, field name or choice value passed to add() that none of the target versions accepts",
}

RULE_SEVERITIES: dict[str, CompatSeverity] = {
    "C001": CompatSeverity.WARNING,
    "C002": CompatSeverity.WARNING,
    "C003": CompatSeverity.ERROR,
    "C004": CompatSeverity.WARNING,
    "C005": CompatSeverity.WARNING,
    "C006": CompatSeverity.ERROR,
}
"""The severity each rule reports at, keyed like [DIAGNOSTIC_CODES][idfkit.compat.DIAGNOSTIC_CODES]."""

DEFAULT_RULES: frozenset[str] = frozenset({"C001", "C002", "C003", "C005", "C006"})
"""The rules checked unless a selection says otherwise.

``C004`` is opt-in (``--extend-select C004``): it reports correct code that has a better-typed
spelling, not a release incompatibility.
"""
