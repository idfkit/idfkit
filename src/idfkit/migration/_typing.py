"""Type variables of the migration package, spelled once for type checkers and the run time.

``typing.TypeVar`` takes ``default=`` only from Python 3.13, and idfkit has no run-time
dependencies, so the type checkers' spelling comes from ``typing_extensions`` and the run-time
stand-ins have no default.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import TypeVar

    from ..document import AnyIDFDocument

    StrictT = TypeVar("StrictT", bound=bool, default=bool)
    """The source document's ``strict``, which the migrated document keeps.

    Defaults to ``bool`` for a source whose strictness a checker cannot read off its type.
    """

    DocumentT_co = TypeVar(
        "DocumentT_co",
        bound=AnyIDFDocument[Any],
        covariant=True,
        default=AnyIDFDocument,
    )
    """The type of a report's ``migrated_model``: the target release's document type when the
    caller named it, else ``AnyIDFDocument``. A bare ``MigrationReport`` means any of them."""
else:
    from typing import TypeVar

    StrictT = TypeVar("StrictT", bound=bool)
    DocumentT_co = TypeVar("DocumentT_co", covariant=True)

__all__ = ["DocumentT_co", "StrictT"]
