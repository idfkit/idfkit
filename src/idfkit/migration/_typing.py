"""Typing helpers shared by the sync and async migration entry points.

``typing.TypeVar`` takes ``default=`` only from Python 3.13, and idfkit has no run-time
dependencies, so the type checkers' spelling comes from ``typing_extensions`` and the run-time
stand-in has no default.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    StrictT = TypeVar("StrictT", bound=bool, default=bool)
    """The source document's ``strict``, which the migrated document keeps.

    Defaults to ``bool`` for a source whose strictness a checker cannot read off its type.
    """
else:
    from typing import TypeVar

    StrictT = TypeVar("StrictT", bound=bool)

__all__ = ["StrictT"]
