"""Plan the ordered chain of transition steps between two EnergyPlus versions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from .._document_types import is_type_form, release_of
from ..exceptions import UnsupportedVersionError
from ..simulation.config import normalize_version
from ..versions import ENERGYPLUS_VERSIONS, find_release, is_supported_version

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
    ``IDFDocumentV24_1`` from ``idfkit.versioned`` or ``IDFDocument`` for the
    latest. Raises on malformed input or unsupported versions.

    Raises:
        ValueError: If the string cannot be parsed.
        TypeError: If *target_version* is a type that is not the document
            type of a single release (``AnyIDFDocument``, a union, a class
            of its own), a tuple of document types (even of one), or neither
            a version nor a type.
        UnsupportedVersionError: If the parsed version is not in
            `ENERGYPLUS_VERSIONS`.
    """
    if is_type_form(target_version):
        return release_of(target_version)
    # A tuple of document types is what as_version takes for several releases. A migration reaches
    # one, so it is refused whatever its length, a one-member tuple included. A tuple none of whose
    # items is a type is a version and goes to normalize_version as it always has, whatever its
    # items are (numpy integers included).
    if isinstance(target_version, tuple) and any(is_type_form(part) for part in target_version):
        msg = (
            f"{target_version!r} is a tuple of document types, which as_version takes for several releases;"
            " a migration reaches one, so name one, such as IDFDocumentV24_1"
        )
        raise TypeError(msg)
    # Typed callers cannot get here (is_type_form narrowed the types away); untyped ones pass anything.
    if not isinstance(cast("object", target_version), (str, tuple)):
        msg = (
            "target_version must be a (major, minor, patch) tuple, a dotted string or a document type such as"
            f" IDFDocumentV24_1, not {target_version!r}"
        )
        raise TypeError(msg)
    normalized = normalize_version(target_version)
    if not is_supported_version(normalized):
        raise UnsupportedVersionError(normalized, ENERGYPLUS_VERSIONS)
    return normalized


def resolve_source_version(version: tuple[int, int, int]) -> tuple[int, int, int]:
    """Resolve a model's version to the supported release a migration starts from.

    An IDF file states its version with two components, so a document loaded from
    a file headed ``Version, 9.0;`` carries ``(9, 0, 0)`` while the release is
    9.0.1. The rest of idfkit (schema selection, ``as_version``) matches the
    version to its release line; a migration does the same, with
    [find_release][idfkit.versions.find_release]. Unlike schema selection, a
    version newer than every supported release is not snapped to the latest: a
    model of an unknown release cannot be migrated from a neighbouring one.

    Examples:
        >>> resolve_source_version((9, 0, 0))
        (9, 0, 1)
        >>> resolve_source_version((24, 1, 0))
        (24, 1, 0)

    Raises:
        UnsupportedVersionError: If no supported release has *version*'s major and minor.
    """
    release = find_release(version)
    if release is None:
        raise UnsupportedVersionError(version, ENERGYPLUS_VERSIONS)
    return release


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
