"""Attribute-name resolution for :class:`~idfkit.document.IDFDocument` collection accessors.

Lets every object type in a document's schema be reached as an attribute,

for example:

    doc.zones                            # Zone
    doc.air_loop_hvacs                   # AirLoopHVAC
    doc.coil_cooling_dx_single_speeds    # Coil:Cooling:DX:SingleSpeed
    doc.air_terminal_single_duct_vav_reheats
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schema import EpJSONSchema

__all__ = [
    "AccessorResolver",
    "accessor_resolver",
    "pluralize",
    "snake_case",
]

# Names whose English plural is not formed by rule
_IRREGULAR_PLURALS = {"people": "people"}

_SPLIT_BEFORE_WORD = re.compile(r"(.)([A-Z][a-z]+)")
_SPLIT_AFTER_LOWER = re.compile(r"([a-z0-9])([A-Z])")
_COLLAPSE = re.compile(r"_+")
_NON_ALNUM = re.compile(r"[^a-z0-9]")


def snake_case(obj_type: str) -> str:
    """Convert an EnergyPlus object type to its ``snake_case`` singular form.

    Both ``:`` and ``-`` are treated as separators. The hyphen matters for exactly
    one type in the schema, ``PhotovoltaicPerformance:EquivalentOne-Diode``; without
    splitting on it the result is not a valid Python identifier.

    >>> snake_case("AirLoopHVAC")
    'air_loop_hvac'
    >>> snake_case("Coil:Cooling:DX:SingleSpeed")
    'coil_cooling_dx_single_speed'
    >>> snake_case("HVACTemplate:Zone:VAV")
    'hvac_template_zone_vav'
    >>> snake_case("PhotovoltaicPerformance:EquivalentOne-Diode")
    'photovoltaic_performance_equivalent_one_diode'

    The two regexes handle acronyms between them. ``_SPLIT_BEFORE_WORD`` requires a
    lowercase run after the capital, which is what makes ``HVACTemplate`` split as
    ``HVAC_Template`` rather than ``HVACT_emplate``.
    """
    s = obj_type.replace(":", "_").replace("-", "_")
    s = _SPLIT_BEFORE_WORD.sub(r"\1_\2", s)
    s = _SPLIT_AFTER_LOWER.sub(r"\1_\2", s)
    return _COLLAPSE.sub("_", s).lower().strip("_")


def pluralize(singular: str) -> str:
    """Pluralize a ``snake_case`` name.

    Handles the cases EnergyPlus type names actually present:

    >>> pluralize("zone")            # ordinary
    'zones'
    >>> pluralize("branch")          # sibilant
    'branches'
    >>> pluralize("lights")          # already plural, must not become 'lightses'
    'lights'
    >>> pluralize("internal_mass")   # singular ending in ss
    'internal_masses'
    >>> pluralize("people")          # irregular, not 'peoples'
    'people'
    """
    tail = singular.rsplit("_", 1)[-1]
    if tail in _IRREGULAR_PLURALS:
        return singular[: len(singular) - len(tail)] + _IRREGULAR_PLURALS[tail]
    if singular.endswith(("ss", "x", "z", "ch", "sh")):
        return singular + "es"
    if singular.endswith("s"):
        # Lights, Output:Schedules, ConvergenceLimits: already plural.
        return singular
    if singular.endswith("y") and len(singular) > 1 and singular[-2] not in "aeiou":
        return singular[:-1] + "ies"
    return singular + "s"


def _key(name: str) -> str:
    """Normalise any spelling to a comparable key.

    This is what removes the need for acronym knowledge in the reverse direction:
    ``"air_loop_hvacs"`` and ``"AirLoopHVAC"`` both reduce to ``"airloophvac"`` (well,
    ``"airloophvacs"`` for the plural -- the plural, singular and raw forms are all
    registered as keys for each type).
    """
    return _NON_ALNUM.sub("", name.lower())


class AccessorResolver:
    """Maps attribute names to object types for one schema.

    Build once per schema and cache it (see :func:`accessor_resolver`); construction
    is O(number of object types) and lookup is a dict hit.
    """

    def __init__(self, obj_types: Iterable[str]) -> None:
        self.attr_for: dict[str, str] = {}
        self._index: dict[str, str] = {}

        for obj_type in obj_types:
            singular = snake_case(obj_type)
            attr = pluralize(singular)
            self.attr_for[obj_type] = attr
            # Accept the canonical plural, the singular, and the raw object type.
            for alias in (attr, singular, obj_type):
                self._index.setdefault(_key(alias), obj_type)

    def resolve(self, attr: str) -> str | None:
        """Return the object type for an attribute name, or ``None``."""
        return self._index.get(_key(attr))

    def suggest(self, attr: str, n: int = 3) -> list[str]:
        """Closest canonical attribute names, for an ``AttributeError`` message."""
        matches = difflib.get_close_matches(_key(attr), self._index.keys(), n=n * 2, cutoff=0.6)
        seen: set[str] = set()
        out: list[str] = []
        for m in matches:
            canonical = self.attr_for[self._index[m]]
            if canonical not in seen:
                seen.add(canonical)
                out.append(canonical)
            if len(out) >= n:
                break
        return out

    def attribute_error(self, owner: str, attr: str) -> AttributeError:
        """Build an ``AttributeError`` that names the likely intent.

        The schema knows what the user probably meant, so the error says it rather
        than leaving them to guess at casing and plurality.
        """
        suggestions = self.suggest(attr)
        if not suggestions:
            return AttributeError(f"{owner!r} object has no attribute {attr!r}")
        width = max(len(s) for s in suggestions)
        lines = "\n".join(f"  {s:<{width}}  ({self.resolve(s)})" for s in suggestions)
        return AttributeError(f"{owner!r} object has no attribute {attr!r}.\nDid you mean:\n{lines}")


# Cache one resolver per schema object
_RESOLVER_CACHE: dict[int, tuple[EpJSONSchema, AccessorResolver]] = {}


def accessor_resolver(schema: EpJSONSchema) -> AccessorResolver:
    """Return the (cached) :class:`AccessorResolver` for *schema*."""
    key = id(schema)
    hit = _RESOLVER_CACHE.get(key)
    if hit is not None and hit[0] is schema:
        return hit[1]
    resolver = AccessorResolver(schema.object_types)
    _RESOLVER_CACHE[key] = (schema, resolver)
    return resolver
