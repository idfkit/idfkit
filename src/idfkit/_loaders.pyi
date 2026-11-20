"""Types of the public loaders, whose run-time half is ``_loaders.py``.

A model's EnergyPlus release is read from its file, so a loaded document is typed as
``AnyIDFDocument``: through it, only what every supported release accepts type-checks. Naming
the release with ``as_type=``, or a range of releases with ``since=``/``before=``, types it for
that release, as ``idfkit.versioned.as_version`` does, and is checked when the file is read.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypeVar, overload

from typing_extensions import Unpack

from .document import AnyIDFDocument, IDFDocument
from .idf_parser import ParseResult
from .versioned import (
    IDFDocumentBefore9_0,
    IDFDocumentBefore9_1,
    IDFDocumentBefore9_2,
    IDFDocumentBefore9_3,
    IDFDocumentBefore9_4,
    IDFDocumentBefore9_5,
    IDFDocumentBefore9_6,
    IDFDocumentBefore22_1,
    IDFDocumentBefore22_2,
    IDFDocumentBefore23_1,
    IDFDocumentBefore23_2,
    IDFDocumentBefore24_1,
    IDFDocumentBefore24_2,
    IDFDocumentBefore25_1,
    IDFDocumentBefore25_2,
    IDFDocumentBefore26_1,
    IDFDocumentBefore26_2,
    IDFDocumentSince8_9,
    IDFDocumentSince9_0,
    IDFDocumentSince9_1,
    IDFDocumentSince9_2,
    IDFDocumentSince9_3,
    IDFDocumentSince9_4,
    IDFDocumentSince9_5,
    IDFDocumentSince9_6,
    IDFDocumentSince22_1,
    IDFDocumentSince22_2,
    IDFDocumentSince23_1,
    IDFDocumentSince23_2,
    IDFDocumentSince24_1,
    IDFDocumentSince24_2,
    IDFDocumentSince25_1,
    IDFDocumentSince25_2,
    IDFDocumentSince26_1,
    IDFDocumentSince26_2,
    IDFDocumentV8_9,
    IDFDocumentV9_0,
    IDFDocumentV9_1,
    IDFDocumentV9_2,
    IDFDocumentV9_3,
    IDFDocumentV9_4,
    IDFDocumentV9_5,
    IDFDocumentV9_6,
    IDFDocumentV22_1,
    IDFDocumentV22_2,
    IDFDocumentV23_1,
    IDFDocumentV23_2,
    IDFDocumentV24_1,
    IDFDocumentV24_2,
    IDFDocumentV25_1,
    IDFDocumentV25_2,
    IDFDocumentV26_1,
)

_D = TypeVar("_D", bound=AnyIDFDocument)

def check_supported_version(version: tuple[int, int, int]) -> None: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict_parsing: bool = ...,
    strict: Literal[True] = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument[Literal[True]]:
    """Load an IDF file and return its document.

    A model's EnergyPlus release is read from its file, so a type checker cannot know it: the
    document is typed as ``AnyIDFDocument``, which offers what every supported release has. Name
    the release with ``as_type=``, or a range of releases with ``since=`` and ``before=``, to type
    it for that release; the release is checked once the file is read, as
    :func:`idfkit.versioned.as_version` checks it.

    Args:
        path: Path to the IDF file
        version: Optional version override (major, minor, patch): the release whose schema the
            file is read with. A ``Version`` object in the file still sets ``doc.version``, and
            that is what ``as_type=``, ``since=`` and ``before=`` are checked against.
        as_type: The document type of the release the file must be, such as ``IDFDocumentV9_4``
            from :mod:`idfkit.versioned`, or a tuple of them. The document is returned typed as
            it, or as the union of the tuple's types. A type argument states the strictness:
            ``IDFDocumentV9_4[Literal[False]]`` loads a non-strict document, as ``strict=False`` does.
        since: The first release of a range the file must be in: its document type,
            ``"major.minor"`` or a version tuple. The document is typed as the union of the
            range's releases.
        before: The release that range stops before, the same way.
        strict_parsing: If True, fail fast on malformed IDF objects (default: True)
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        preserve_formatting: When ``True``, build a Concrete Syntax Tree
            (CST) so that :func:`write_idf` and :func:`save_idf`
            reproduce the original
            formatting, comments, and whitespace for unmodified objects. Choice
            normalization does not affect this: an unmodified object is written as read.
        normalize_choices: When ``True`` (the default), each choice value is stored in the
            spelling its schema declares, whatever case the file used: a surface the file
            calls ``WALL`` has ``surface_type == "Wall"``, as its ``Literal`` type says, so an
            exhaustive ``match`` holds on models you did not write. EnergyPlus reads choices
            case-insensitively, so no simulation changes. ``False`` keeps the file's text, and
            a choice field's ``Literal`` type then does not hold; see
            :attr:`IDFDocument.normalize_choices <idfkit.document.IDFDocument.normalize_choices>`.

    Returns:
        The parsed document: an ``AnyIDFDocument``, or typed as ``as_type=`` or the
        ``since=``/``before=`` range when one is given.

    Raises:
        TypeError: If the file's release is not the one ``as_type=`` names or is outside the
            ``since=``/``before=`` range; or, before the file is read, if both ``as_type=`` and a
            range are given, ``as_type=`` is not a document type, or its type argument states a
            strict document while ``strict=False``.
        ValueError: Before the file is read, if ``since=`` or ``before=`` names no supported
            release, or the range holds none.

    Examples:
        Load a DOE reference building and list its zones:

            ```python
            model = load_idf("RefBldgSmallOfficeNew2004.idf")
            print(f"Loaded {len(model)} objects")
            for zone in model["Zone"]:
                print(zone.name)
            ```

        State the release, so the model is checked against that release's object types:

            ```python
            from idfkit.versioned import IDFDocumentV9_4

            legacy = load_idf("legacy.idf", as_type=IDFDocumentV9_4)
            recent = load_idf("model.idf", since="9.6")  # 9.6, 22.1, ... and the latest
            recent["Space"].first()  # Space exists in every one of those releases
            ```

        Override the version for a legacy model:

            ```python
            model = load_idf("pre_v9_building.idf", version=(9, 6, 0))
            ```

        Lossless round-trip:

            ```python
            model = load_idf("building.idf", preserve_formatting=True)
            save_idf(model, "building_copy.idf")  # byte-identical
            ```
    """

@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict_parsing: bool = ...,
    strict: Literal[False],
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument[Literal[False]]: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: type[_D],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> _D: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: tuple[type[_D], Unpack[tuple[type[_D], ...]]],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> _D: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince8_9: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_0: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince26_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_0: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore26_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1
): ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_2: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV26_1: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None = None,
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument: ...
@overload
def load_idf(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict: Literal[True] = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[AnyIDFDocument[Literal[True]]]:
    """Load an IDF file, keeping the findings that did not stop the parse.

    `load_idf` hands back the document and drops the recoverable findings; this hands back both.
    The findings were always produced, but they went to the logging module and nowhere else, so
    reaching them meant installing a handler before the parse. That is not one call, and it is not
    the same findings the other language returns.

    There is no `strict_parsing` parameter. A strict parse has no recoverable findings by
    definition: the first one stops it. Findings that stop a parse still raise `IDFParseError`,
    which carries them on `.diagnostics`, and that path is unchanged.

    Every logging announcement still fires. A caller who installed a handler sees exactly what they
    saw before.

    The document is typed as ``AnyIDFDocument`` unless ``as_type=``, ``since=`` or ``before=``
    names its release, as for :func:`load_idf`.

    Args:
        path: Path to the IDF file
        version: Optional version override (major, minor, patch)
        as_type: The document type of the release the file must be, or a tuple of them, as for
            :func:`load_idf`.
        since: The first release of a range the file must be in, as for :func:`load_idf`.
        before: The release that range stops before, as for :func:`load_idf`.
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        preserve_formatting: When ``True``, build a Concrete Syntax Tree (CST) so that
            :func:`write_idf` and :func:`save_idf` reproduce the original formatting.
        normalize_choices: When ``True`` (the default), each choice value is stored in the
            spelling its schema declares, whatever case the file used: a surface the file
            calls ``WALL`` has ``surface_type == "Wall"``, as its ``Literal`` type says, so an
            exhaustive ``match`` holds on models you did not write. EnergyPlus reads choices
            case-insensitively, so no simulation changes. ``False`` keeps the file's text, and
            a choice field's ``Literal`` type then does not hold; see
            :attr:`IDFDocument.normalize_choices <idfkit.document.IDFDocument.normalize_choices>`.

    Returns:
        A :class:`~idfkit.idf_parser.ParseResult`: the document, and the recoverable findings.

    Raises:
        TypeError: As :func:`load_idf` raises it.
        ValueError: As :func:`load_idf` raises it.

    Examples:
        Read a model that may be imperfect, and show what was wrong with it:

            ```python
            from idfkit import load_idf_with_diagnostics

            result = load_idf_with_diagnostics("hand_edited.idf")
            print(f"Loaded {len(result.document)} objects")
            for finding in result.diagnostics:
                print(f"{finding.code} at line {finding.line}: {finding.message}")
            ```
    """

@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict: Literal[False],
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[AnyIDFDocument[Literal[False]]]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: type[_D],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[_D]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: tuple[type[_D], Unpack[tuple[type[_D], ...]]],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[_D]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince8_9]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_0]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentSince26_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_0]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentBefore26_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV8_9]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV8_9 | IDFDocumentV9_0]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_0]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_0 | IDFDocumentV9_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_1 | IDFDocumentV9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_2 | IDFDocumentV9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_3]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_3 | IDFDocumentV9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_4]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_4 | IDFDocumentV9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_5]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_5 | IDFDocumentV9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_6]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_6 | IDFDocumentV22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_1 | IDFDocumentV22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_2 | IDFDocumentV23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_1 | IDFDocumentV23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_2 | IDFDocumentV24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[
    IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1
]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_1 | IDFDocumentV24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_2 | IDFDocumentV25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV25_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV25_1 | IDFDocumentV25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV25_2]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV25_2 | IDFDocumentV26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[IDFDocumentV26_1]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None = None,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[AnyIDFDocument]: ...
@overload
def load_idf_with_diagnostics(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> ParseResult[AnyIDFDocument]: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict_parsing: bool = ...,
    strict: Literal[True] = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument[Literal[True]]:
    """Load an epJSON file and return its document.

    The document is typed as ``AnyIDFDocument`` unless ``as_type=``, ``since=`` or ``before=``
    names its release, as for :func:`load_idf`.

    Args:
        path: Path to the epJSON file
        version: Optional version override (major, minor, patch)
        as_type: The document type of the release the file must be, or a tuple of them, as for
            :func:`load_idf`.
        since: The first release of a range the file must be in, as for :func:`load_idf`.
        before: The release that range stops before, as for :func:`load_idf`.
        strict_parsing: When ``True`` (the default), an object type the schema does not
            have raises :class:`~idfkit.exceptions.IDFParseError`, as :func:`load_idf` does,
            and the message suggests the closest type; EnergyPlus refuses such a file. ``False``
            skips it with a logged warning.
        strict: When ``True``, accessing or setting an unknown field name on any
            IDFObject raises :class:`~idfkit.exceptions.InvalidFieldError` instead
            of returning ``None``.
        preserve_formatting: When ``True``, store the raw JSON text so
            that :func:`write_epjson` and :func:`save_epjson` can
            reproduce it byte-for-byte
            when no objects have been modified.
        normalize_choices: When ``True`` (the default), each choice value is stored in the
            spelling its schema declares, whatever case the file used: a surface the file
            calls ``WALL`` has ``surface_type == "Wall"``, as its ``Literal`` type says, so an
            exhaustive ``match`` holds on models you did not write. EnergyPlus reads choices
            case-insensitively, so no simulation changes. ``False`` keeps the file's text, and
            a choice field's ``Literal`` type then does not hold; see
            :attr:`IDFDocument.normalize_choices <idfkit.document.IDFDocument.normalize_choices>`.

    Returns:
        The parsed document: an ``AnyIDFDocument``, or typed as ``as_type=`` or the
        ``since=``/``before=`` range when one is given.

    Raises:
        IDFParseError: For an object type the schema does not have, with *strict_parsing*.
        TypeError: As :func:`load_idf` raises it.
        ValueError: As :func:`load_idf` raises it.

    Examples:
        Load an epJSON model and iterate over zones:

            ```python
            model = load_epjson("SmallOffice.epJSON")
            for zone in model["Zone"]:
                print(zone.name, zone.x_origin)
            ```

        Load it typed for the release it must be:

            ```python
            from idfkit.versioned import IDFDocumentV24_1

            model = load_epjson("SmallOffice.epJSON", as_type=IDFDocumentV24_1)
            ```

        Specify an explicit EnergyPlus version:

            ```python
            model = load_epjson("SmallOffice.epJSON", version=(24, 1, 0))
            ```
    """

@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: None = ...,
    since: None = ...,
    before: None = ...,
    strict_parsing: bool = ...,
    strict: Literal[False],
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument[Literal[False]]: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: type[_D],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> _D: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    as_type: tuple[type[_D], Unpack[tuple[type[_D], ...]]],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> _D: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince8_9: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_0: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentSince26_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_0: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentBefore26_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV8_9 | IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV8_9] | Literal["8.9", "8.9.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV8_9
    | IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_0 | IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_0] | Literal["9.0", "9.0.1"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_0
    | IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_1 | IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_1] | Literal["9.1", "9.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_1
    | IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_2 | IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_2] | Literal["9.2", "9.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_2
    | IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_3 | IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_3] | Literal["9.3", "9.3.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_3
    | IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_4 | IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_4] | Literal["9.4", "9.4.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_4
    | IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_5 | IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_5] | Literal["9.5", "9.5.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_5
    | IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV9_6 | IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV9_6] | Literal["9.6", "9.6.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV9_6
    | IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1 | IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_1] | Literal["22.1", "22.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_1
    | IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2 | IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV22_2] | Literal["22.2", "22.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV22_2
    | IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_1 | IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_1] | Literal["23.1", "23.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_1
    | IDFDocumentV23_2
    | IDFDocumentV24_1
    | IDFDocumentV24_2
    | IDFDocumentV25_1
    | IDFDocumentV25_2
    | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV23_2] | Literal["23.2", "23.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> (
    IDFDocumentV23_2 | IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1
): ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_1] | Literal["24.1", "24.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_1 | IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV24_2] | Literal["24.2", "24.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV24_2 | IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1 | IDFDocumentV25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_1] | Literal["25.1", "25.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_1 | IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_2: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV25_2] | Literal["25.2", "25.2.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV25_2 | IDFDocumentV26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[IDFDocumentV26_1] | Literal["26.1", "26.1.0"],
    before: type[IDFDocument] | Literal["26.2", "26.2.0"],
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> IDFDocumentV26_1: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    since: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None = None,
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument: ...
@overload
def load_epjson(
    path: Path | str,
    version: tuple[int, int, int] | None = ...,
    *,
    before: type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int] | None,
    strict_parsing: bool = ...,
    strict: bool = ...,
    preserve_formatting: bool = ...,
    normalize_choices: bool = ...,
) -> AnyIDFDocument: ...
