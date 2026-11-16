"""Plan the ordered chain of transition steps between two EnergyPlus versions."""

from __future__ import annotations

import types
from typing import TYPE_CHECKING, Any, cast, get_origin

from ..exceptions import UnsupportedVersionError
from ..simulation.config import normalize_version
from ..versions import ENERGYPLUS_VERSIONS, is_supported_version

if TYPE_CHECKING:
    from ..document import AnyIDFDocument

#: A transition step: ``(from_version, to_version)``.
TransitionStep = tuple[tuple[int, int, int], tuple[int, int, int]]


def normalize_target(
    target_version: tuple[int, int, int] | str | type[AnyIDFDocument[Any]],
) -> tuple[int, int, int]:
    """Coerce a tuple, dotted-string version or document type into a normalized, supported tuple.

    Accepts a ``(major, minor, patch)`` tuple, a dotted string such as
    ``"25.2.0"`` / ``"25.2"``, or the document type of one release, such as
    ``IDFDocumentV24_1`` from [idfkit.versioned][] or ``IDFDocument`` for the
    latest. Raises on malformed input or unsupported versions.

    Raises:
        ValueError: If the string cannot be parsed.
        TypeError: If *target_version* is a type that is not the document
            type of a single release (``AnyIDFDocument``, a union, a class
            of its own).
        UnsupportedVersionError: If the parsed version is not in
            `ENERGYPLUS_VERSIONS`.
    """
    if not _is_version(target_version):
        from .._document_types import release_of

        return release_of(target_version)
    normalized = normalize_version(cast("tuple[int, int, int] | str", target_version))
    if not is_supported_version(normalized):
        raise UnsupportedVersionError(normalized, ENERGYPLUS_VERSIONS)
    return normalized


def _is_version(value: object) -> bool:
    """Whether *value* spells a version rather than a document type.

    A string, or a tuple none of whose items is a type, is a version, and goes to
    ``normalize_version`` as it always has, whatever its items are (numpy integers included). A
    tuple of document types, as ``as_version`` takes, is not: it goes to the document-type path,
    which refuses it for naming several releases.
    """
    if isinstance(value, str):
        return True
    return isinstance(value, tuple) and not any(_is_type(part) for part in cast("tuple[object, ...]", value))


def _is_type(value: object) -> bool:
    """Whether *value* is a class, a subscripted generic such as ``IDFDocumentV9_4[bool]``, or a union."""
    return isinstance(value, (type, types.UnionType)) or get_origin(value) is not None


def plan_migration_chain(
    source: tuple[int, int, int],
    target: tuple[int, int, int],
) -> tuple[TransitionStep, ...]:
    """Plan the ordered list of transition steps from *source* to *target*.

    The chain walks forward through `ENERGYPLUS_VERSIONS`
    from *source* to *target*, emitting a ``(from, to)`` pair for each
    consecutive version boundary.

    Args:
        source: The model's current version. Must be in ``ENERGYPLUS_VERSIONS``.
        target: The desired version. Must be in ``ENERGYPLUS_VERSIONS`` and
            ``>= source``.

    Returns:
        A tuple of ``(from, to)`` pairs. Empty when ``source == target``.

    Raises:
        UnsupportedVersionError: If *source* or *target* is not a supported version.
        ValueError: If ``target < source`` (backward migration is not supported).
    """
    if not is_supported_version(source):
        raise UnsupportedVersionError(source, ENERGYPLUS_VERSIONS)
    if not is_supported_version(target):
        raise UnsupportedVersionError(target, ENERGYPLUS_VERSIONS)

    if source == target:
        return ()
    if target < source:
        msg = (
            f"Backward migration is not supported: {source[0]}.{source[1]}.{source[2]}"
            f" -> {target[0]}.{target[1]}.{target[2]}."
        )
        raise ValueError(msg)

    source_idx = ENERGYPLUS_VERSIONS.index(source)
    target_idx = ENERGYPLUS_VERSIONS.index(target)
    steps: list[TransitionStep] = []
    for i in range(source_idx, target_idx):
        steps.append((ENERGYPLUS_VERSIONS[i], ENERGYPLUS_VERSIONS[i + 1]))
    return tuple(steps)
