"""
EnergyPlus version registry.

Defines all supported EnergyPlus versions since v8.9 (the first to publish
epJSON schema) and provides utilities for version manipulation.
"""

from __future__ import annotations

from typing import Final

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


def is_supported_version(version: tuple[int, int, int]) -> bool:
    """Check if a version is in the supported set.

    Examples:
        >>> is_supported_version((24, 1, 0))
        True
        >>> is_supported_version((99, 0, 0))
        False
        >>> is_supported_version(MINIMUM_VERSION)
        True
    """
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

    This is the release-line half of :func:`find_closest_version`: the version
    itself when it is a supported release, else the highest supported release of
    the same major and minor (a file headed ``Version, 9.0;`` reads as
    ``(9, 0, 0)`` and names the 9.0.1 release). Unlike
    :func:`find_closest_version`, a version newer than every supported release is
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
