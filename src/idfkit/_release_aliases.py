"""The types of the release arguments ``as_type=``, ``since=`` and ``before=``.

Re-exported from [idfkit.versioned][], for a function of your own that takes a release the way the
loaders and [as_version][idfkit.versioned.as_version] do and passes it on.

They live in a module of their own because they name ``AnyIDFDocument`` unquoted: a quoted name
inside ``type[...]`` is resolved by ``typing.get_type_hints`` in the module of whoever uses the
alias (Python 3.11 and later), where ``AnyIDFDocument`` is usually not defined. Importing it needs
``idfkit.document``, which ``_document_types`` cannot import, since ``document`` imports it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from .document import AnyIDFDocument

__all__ = ["DocumentTypeTarget", "ReleaseBound"]

if TYPE_CHECKING:
    from typing_extensions import Unpack

    DocumentTypeTarget: TypeAlias = (
        type[AnyIDFDocument] | tuple[type[AnyIDFDocument], Unpack[tuple[type[AnyIDFDocument], ...]]]
    )
else:
    # ``Unpack`` is in ``typing`` only from Python 3.11, and idfkit has no dependencies. At run time
    # the alias is read by introspection, never enforced, so the tuple's non-emptiness goes unsaid
    # there; type checkers read the branch above.
    DocumentTypeTarget = type[AnyIDFDocument] | tuple[type[AnyIDFDocument], ...]
    """The release a document must be, as ``as_type=`` and [as_version][idfkit.versioned.as_version] take it.

    A release's document type from [idfkit.versioned][], such as ``IDFDocumentV9_4``, or a non-empty
    tuple of them for any one of several releases. The document is typed as that release, or as the
    union of the tuple's releases.
    """

ReleaseBound: TypeAlias = type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int]
"""One end of a range of releases, as ``since=`` and ``before=`` take it.

A release's document type (``IDFDocumentV9_6``), its number (``"9.6"``) or its version tuple
(``(9, 6)`` or ``(9, 6, 0)``). ``since=`` includes the release it names and ``before=`` excludes it.
"""
