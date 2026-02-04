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
    """Check if a version is in the supported set."""
    return version in _VERSION_SET


def version_string(version: tuple[int, int, int]) -> str:
    """Format a version tuple as a human-readable string (e.g. '24.1.0')."""
    return f"{version[0]}.{version[1]}.{version[2]}"


def version_dirname(version: tuple[int, int, int]) -> str:
    """Return the schema directory name for a version (e.g. 'V24-1-0')."""
    return f"V{version[0]}-{version[1]}-{version[2]}"


def find_closest_version(version: tuple[int, int, int]) -> tuple[int, int, int] | None:
    """
    Find the closest supported version that is <= the given version.

    This is useful when a file specifies a patch version that doesn't
    exactly match a supported version (e.g. 9.0.0 -> 9.0.1).

    Returns:
        The closest supported version, or None if no suitable version exists.
    """
    best: tuple[int, int, int] | None = None
    for v in ENERGYPLUS_VERSIONS:
        if v <= version:
            best = v
    return best


def github_release_tag(version: tuple[int, int, int]) -> str:
    """Return the GitHub release tag for a version (e.g. 'v24.1.0')."""
    return f"v{version[0]}.{version[1]}.{version[2]}"
