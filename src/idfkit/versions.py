"""
EnergyPlus version registry.

Defines all supported EnergyPlus versions since v8.9 (the first to publish
epJSON schema) and provides utilities for version manipulation.
"""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Iterable

__all__ = [
    "ENERGYPLUS_VERSIONS",
    "LATEST_VERSION",
    "MINIMUM_VERSION",
    "find_closest_version",
    "find_release",
    "is_supported_version",
    "object_type_releases",
    "releases_between",
    "version_string",
]

# All EnergyPlus versions since v8.9.0 that publish an epJSON schema.
# Each entry is a (major, minor, patch) tuple.
ENERGYPLUS_VERSIONS: Final[tuple[tuple[int, int, int], ...]] = (
    (8, 9, 0),
    (9, 0, 1),
    (9, 1, 0),
    (9, 2, 0),
    (9, 3, 0),
    (9, 4, 0),
    (9, 5, 0),
    (9, 6, 0),
    (22, 1, 0),
    (22, 2, 0),
    (23, 1, 0),
    (23, 2, 0),
    (24, 1, 0),
    (24, 2, 0),
    (25, 1, 0),
    (25, 2, 0),
    (26, 1, 0),
    (26, 2, 0),
)

#: The latest supported EnergyPlus version.
LATEST_VERSION: Final[tuple[int, int, int]] = ENERGYPLUS_VERSIONS[-1]

#: Minimum supported version (first with epJSON schema).
MINIMUM_VERSION: Final[tuple[int, int, int]] = ENERGYPLUS_VERSIONS[0]

# Set for O(1) membership checks
_VERSION_SET: Final[frozenset[tuple[int, int, int]]] = frozenset(ENERGYPLUS_VERSIONS)

# Mapping from GitHub release tags to version tuples
_TAG_TO_VERSION: Final[dict[str, tuple[int, int, int]]] = {f"v{v[0]}.{v[1]}.{v[2]}": v for v in ENERGYPLUS_VERSIONS}

# Mapping from version tuple to the directory name used for bundled schemas
_VERSION_TO_DIRNAME: Final[dict[tuple[int, int, int], str]] = {v: f"V{v[0]}-{v[1]}-{v[2]}" for v in ENERGYPLUS_VERSIONS}


def reject_version_string(version: object) -> None:
    """Raise TypeError if *version* is a string such as ``"26.1"``, naming the tuple to pass instead.

    The version arguments of the core API (``new_document``, ``get_schema``, ``load_idf`` and the
    helpers here) take a ``(major, minor, patch)`` tuple. A string used to be read as a sequence of
    characters, which reported the version as ``2.6..``, failed comparing ``str`` with ``tuple``,
    or answered ``False``.

    Raises:
        TypeError: If *version* is a string.

    Examples:
        >>> reject_version_string((24, 1, 0))
        >>> reject_version_string("26.1")
        Traceback (most recent call last):
        ...
        TypeError: version must be a (major, minor, patch) tuple, e.g. (26, 1, 0); got '26.1'
    """
    if isinstance(version, str):
        msg = f"version must be a (major, minor, patch) tuple, e.g. {_example_tuple(version)}; got {version!r}"
        raise TypeError(msg)


def _example_tuple(version: str) -> tuple[int, int, int]:
    """The tuple a dotted string such as ``"26.1"`` means, else [LATEST_VERSION][idfkit.versions.LATEST_VERSION], for an error message."""
    parts = version.strip().lstrip("vV").replace("-", ".").split(".")
    if len(parts) == 2:
        parts.append("0")
    if len(parts) == 3 and all(part.isdigit() for part in parts):
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    return LATEST_VERSION


def is_supported_version(version: tuple[int, int, int]) -> bool:
    """Check if a version is in the supported set.

    Examples:
        >>> is_supported_version((24, 1, 0))
        True
        >>> is_supported_version((99, 0, 0))
        False
        >>> is_supported_version(MINIMUM_VERSION)
        True

    Raises:
        TypeError: If *version* is a string such as ``"24.1.0"`` rather than a tuple.
    """
    reject_version_string(version)
    return version in _VERSION_SET


def version_string(version: tuple[int, int, int]) -> str:
    """Format a version tuple as a human-readable string.

    Examples:
        >>> version_string((24, 1, 0))
        '24.1.0'
        >>> version_string((9, 6, 0))
        '9.6.0'
    """
    return f"{version[0]}.{version[1]}.{version[2]}"


def format_releases(releases: Iterable[tuple[int, int, int]]) -> str:
    """*releases*, oldest first, with each run of three or more consecutive supported releases as a range.

    Consecutive means adjacent in [ENERGYPLUS_VERSIONS][idfkit.versions.ENERGYPLUS_VERSIONS], not in the list given, so a range
    never covers a release that was not checked: ``8.9.0 to 9.5.0`` names seven releases, and
    ``8.9.0, 9.5.0`` the two of a run of targets that skipped the ones between.

    Examples:
        >>> format_releases([(9, 6, 0), (9, 5, 0), (9, 4, 0), (24, 1, 0)])
        '9.4.0 to 9.6.0, 24.1.0'
    """
    order: dict[tuple[int, int, int], int] = {v: i for i, v in enumerate(ENERGYPLUS_VERSIONS)}
    ordered = sorted(set(releases))
    runs: list[list[tuple[int, int, int]]] = []
    for v in ordered:
        if runs and v in order and runs[-1][-1] in order and order[v] == order[runs[-1][-1]] + 1:
            runs[-1].append(v)
        else:
            runs.append([v])
    parts: list[str] = []
    for run in runs:
        if len(run) >= 3:
            parts.append(f"{version_string(run[0])} to {version_string(run[-1])}")
        else:
            parts.extend(version_string(v) for v in run)
    return ", ".join(parts)


def _adjacent(earlier: tuple[int, int, int], later: tuple[int, int, int]) -> bool:
    """Whether *later* is the supported release right after *earlier*."""
    try:
        return ENERGYPLUS_VERSIONS.index(later) == ENERGYPLUS_VERSIONS.index(earlier) + 1
    except ValueError:
        return False


def describe_presence(present: Iterable[tuple[int, int, int]], absent: Iterable[tuple[int, int, int]]) -> str:
    """Which releases have something, as briefly as is still exact; both arguments must be non-empty.

    ``added in 9.6.0`` when every release lacking it comes before every release having it and the
    two meet, ``removed in 23.1.0`` for the reverse, and otherwise ``exists in`` the releases that
    have it.

    Examples:
        >>> describe_presence([(26, 1, 0), (26, 2, 0)], [(25, 2, 0)])
        'added in 26.1.0'
        >>> describe_presence([(9, 5, 0)], [(9, 6, 0), (22, 1, 0)])
        'removed in 9.6.0'
    """
    has = sorted(present)
    lacks = sorted(absent)
    if lacks[-1] < has[0] and _adjacent(lacks[-1], has[0]):
        return f"added in {version_string(has[0])}"
    if lacks[0] > has[-1] and _adjacent(has[-1], lacks[0]):
        return f"removed in {version_string(lacks[0])}"
    return f"exists in {format_releases(has)}"


def object_type_releases(obj_type: str) -> tuple[tuple[int, int, int], ...]:
    """The bundled releases that have *obj_type*, matched case-insensitively, oldest first.

    Empty when no bundled release has it. Answered from a generated table, without loading a schema.

    Examples:
        >>> object_type_releases("Lights:Definition")
        ((26, 2, 0),)
        >>> object_type_releases("Zoen")
        ()
    """
    from ._object_types import PARTIAL_OBJECT_TYPES

    folded = obj_type.casefold()
    runs = PARTIAL_OBJECT_TYPES.get(folded)
    if runs is None:
        return ENERGYPLUS_VERSIONS if folded in _folded_object_types() else ()
    order: dict[tuple[int, int, int], int] = {v: i for i, v in enumerate(ENERGYPLUS_VERSIONS)}
    return tuple(v for first, last in runs for v in ENERGYPLUS_VERSIONS[order[first] : order[last] + 1])


@functools.cache
def _folded_object_types() -> dict[str, str]:
    """Every bundled object type, keyed by its case-folded name, built once."""
    from ._object_types import ALL_OBJECT_TYPES

    return {t.casefold(): t for t in ALL_OBJECT_TYPES}


def not_in_release_message(obj_type: str, version: tuple[int, int, int]) -> str | None:
    """Why *obj_type* is missing from *version*, when another bundled release has it, else None.

    Names the releases that have the type and, where a later release has it, how to get there:
    migrate a model, or create one at that release. The wording names no document, since a schema
    lookup (``describe_object_type``) raises it too.

    Examples:
        >>> msg = not_in_release_message("Lights:Definition", (26, 1, 0))
        >>> msg.splitlines()[0] if msg else None
        "'Lights:Definition' is not an object type of EnergyPlus 26.1.0: it was added in 26.2.0."
        >>> not_in_release_message("Zone", (26, 1, 0)) is None
        True
    """
    present = object_type_releases(obj_type)
    if not present or version in present or version not in ENERGYPLUS_VERSIONS:
        return None
    spelling = _folded_object_types().get(obj_type.casefold(), obj_type)
    absent = [v for v in ENERGYPLUS_VERSIONS if v not in present]
    presence = describe_presence(present, absent)
    msg = (
        f"{spelling!r} is not an object type of EnergyPlus {version_string(version)}: "
        f"it {presence if presence.startswith('exists') else 'was ' + presence}."
    )
    # The rest of the message goes on its own line, so the first states the fact.
    later = [v for v in present if v > version]
    if later:
        target = later[-1]
        create = (
            "new_document()"
            if target == LATEST_VERSION
            else f"new_document(IDFDocumentV{target[0]}_{target[1]}) (from idfkit.versioned)"
        )
        msg += (
            f"\n  To use it, migrate a model to that release (idfkit.migrate(doc, {target!r})) "
            f"or create one there with {create}."
        )
    return msg


def version_dirname(version: tuple[int, int, int]) -> str:
    """Return the schema directory name for a version.

    Examples:
        >>> version_dirname((24, 1, 0))
        'V24-1-0'
        >>> version_dirname((9, 6, 0))
        'V9-6-0'
    """
    return f"V{version[0]}-{version[1]}-{version[2]}"


def find_release(version: tuple[int, int, int]) -> tuple[int, int, int] | None:
    """
    Find the supported release a version names, without any fallback.

    This is the release-line half of [find_closest_version][idfkit.versions.find_closest_version]: the version
    itself when it is a supported release, else the highest supported release of
    the same major and minor (a file headed ``Version, 9.0;`` reads as
    ``(9, 0, 0)`` and names the 9.0.1 release). Unlike
    [find_closest_version][idfkit.versions.find_closest_version], a version newer than every supported release is
    not snapped to the latest one, which is what a migration source needs: a
    model of a release idfkit does not know cannot be migrated from a neighbour.

    Returns:
        The supported release, or None if no release of that line is supported.

    Examples:
        >>> find_release((9, 0, 0))
        (9, 0, 1)
        >>> find_release((24, 1, 0))
        (24, 1, 0)
        >>> find_release((27, 1, 0)) is None
        True
        >>> find_release((8, 8, 0)) is None
        True
    """
    reject_version_string(version)
    if version in _VERSION_SET:
        return version
    same_line = [v for v in ENERGYPLUS_VERSIONS if v[:2] == version[:2]]
    return max(same_line) if same_line else None


def releases_between(
    since: tuple[int, int, int] | None, before: tuple[int, int, int] | None
) -> list[tuple[int, int, int]]:
    """
    Every supported release from *since* (inclusive) to *before* (exclusive).

    This is the range ``as_version(doc, since=..., before=...)`` accepts, and the one
    ``idfkit check`` reads statically; either bound may be ``None`` for an open end.

    Examples:
        >>> releases_between((22, 1, 0), (23, 2, 0))
        [(22, 1, 0), (22, 2, 0), (23, 1, 0)]
    """
    return [v for v in ENERGYPLUS_VERSIONS if (since is None or v >= since) and (before is None or v < before)]


def find_closest_version(version: tuple[int, int, int]) -> tuple[int, int, int] | None:
    """
    Find the supported version to use for a version read from a file.

    A release line is matched before a version number is. An IDF file writes its
    version with two components, ``Version, 9.0;``, which arrives here as
    ``(9, 0, 0)``, so an exact match fails on the patch component for any release
    whose patch is not zero. Matching on major and minor first, and taking the
    highest patch in that line, is what makes a two-component header resolve to
    the release it names.

    Crossing a minor boundary is not a fallback, it is a different EnergyPlus
    release. Ten object types reorder their fields between 8.9.0 and 9.0.1 alone,
    ``RunPeriod`` and ``GlazedDoor`` among them, and IDF is positional: reading a
    9.0 file against the 8.9.0 schema does not fail, it loads ``begin_year`` into
    ``end_month`` and succeeds against a corrupted model. Only a version newer
    than every supported release degrades to the newest one, which is a forward
    tolerance the compatibility checker relies on and which never silently
    reinterprets a release that exists.

    Returns:
        The supported version to use, or None if no suitable version exists.

    Examples:
        >>> find_closest_version((24, 1, 5))
        (24, 1, 0)
        >>> find_closest_version((9, 0, 0))
        (9, 0, 1)
        >>> find_closest_version((1, 0, 0)) is None
        True
        >>> find_closest_version((10, 0, 0)) is None
        True
    """
    release = find_release(version)
    if release is not None:
        return release

    if version > ENERGYPLUS_VERSIONS[-1]:
        return ENERGYPLUS_VERSIONS[-1]
    return None


def github_release_tag(version: tuple[int, int, int]) -> str:
    """Return the GitHub release tag for a version.

    Examples:
        >>> github_release_tag((24, 1, 0))
        'v24.1.0'
        >>> github_release_tag((9, 2, 0))
        'v9.2.0'
    """
    return f"v{version[0]}.{version[1]}.{version[2]}"
