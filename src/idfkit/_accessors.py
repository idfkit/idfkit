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
from collections.abc import Iterable, Mapping

__all__ = [
    "MEMBER_CONFLICT",
    "AccessorAttributeError",
    "AccessorResolver",
    "pluralize",
    "snake_case",
]

# Last words whose English plural is not formed by rule
_IRREGULAR_PLURALS = {"people": "people", "gas": "gases", "hysteresis": "hystereses"}

# Small override for awkward cases
_SNAKE_OVERRIDES = {
    "Output:SQLite": "output_sqlite",
    "Site:GroundTemperature:FCfactorMethod": "site_ground_temperature_fcfactor_method",
    "Daylighting:DELight:ComplexFenestration": "daylighting_delight_complex_fenestration",
}

_SPLIT_BEFORE_WORD = re.compile(r"(.)([A-Z][a-z]+)")
_SPLIT_AFTER_LOWER = re.compile(r"([a-z0-9])([A-Z])")
_COLLAPSE = re.compile(r"_+")

MEMBER_CONFLICT = "<IDFDocument member>"
"""Marker in :attr:`AccessorResolver.conflicts` for a name owned by a real member."""


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
    ``HVAC_Template`` rather than ``HVACT_emplate``. That rule cannot tell where an
    acronym ends and a word begins in ``SQLite``, so the three types it gets wrong
    are named in ``_SNAKE_OVERRIDES``:

    >>> snake_case("Output:SQLite")
    'output_sqlite'
    """
    if obj_type in _SNAKE_OVERRIDES:
        return _SNAKE_OVERRIDES[obj_type]
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
    >>> pluralize("window_material_gas")   # singular noun ending in s, not already plural
    'window_material_gases'
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


def _raw_key(obj_type: str) -> str:
    """Key for a raw type name used as an attribute.

    Case-insensitive, matching idfkit's own type lookup. Only ``:`` is stripped,
    never ``_``, so ``z_o_n_e`` cannot reach ``Zone``.

    >>> _raw_key("AirLoopHVAC")
    'airloophvac'
    >>> _raw_key("Coil:Cooling:DX:SingleSpeed")
    'coilcoolingdxsinglespeed'
    >>> _raw_key("z_o_n_e")
    'z_o_n_e'
    """
    return obj_type.replace(":", "").lower()


def _underscore_key(obj_type: str) -> str:
    """Key for a raw type name written with ``_`` where it has ``:``.

    These spellings (``doc.Site_Location``, ``doc.BuildingSurface_Detailed``) resolved
    before schema-driven accessors existed, through a case-insensitive match that
    replaced ``:`` and spaces with ``_``. Registering them keeps that match working
    whether or not a schema is loaded. Underscores already in the name are the only
    ones kept, so ``z_o_n_e`` still reaches nothing.

    >>> _underscore_key("Site:Location")
    'site_location'
    >>> _underscore_key("BuildingSurface:Detailed")
    'buildingsurface_detailed'
    """
    return obj_type.replace(":", "_").replace(" ", "_").lower()


class AccessorResolver:
    """Maps attribute names to object types for one schema.

    Build once per schema and cache it on the schema (see
    :meth:`~idfkit.schema.EpJSONSchema.accessor_resolver`); construction is
    O(number of object types) and lookup is at most two dict hits.

    Applied precedence:

    1. A real ``IDFDocument`` member always wins, because ``__getattr__`` never
       fires for it. Any name that collides with one is recorded in ``conflicts``.
    2. Names derived from the schema win over hand-written shorthands. A shorthand
       that contradicts a derived name is recorded in ``conflicts`` and dropped.
    3. Shorthands fill in wherever they do not contradict a derived name.

    Args:
        obj_types: Every object type in the schema.
        shorthands: Hand-written attribute names, ``{attribute: object_type}``.
        reserved: Names owned by real ``IDFDocument`` members.

    Attributes:
        attr_for: Canonical attribute name for every object type.
        shorthands: The shorthands that were registered, after clashes were removed.
        conflicts: Every name claimed twice, as ``{name: (loser, winner)}``.
    """

    def __init__(
        self,
        obj_types: Iterable[str],
        shorthands: Mapping[str, str] | None = None,
        reserved: Iterable[str] = (),
    ) -> None:
        types = list(obj_types)
        present = set(types)
        reserved_set = set(reserved)
        self._reserved = frozenset(reserved_set)

        self.attr_for: dict[str, str] = {}
        self.shorthands: dict[str, str] = {}
        self.conflicts: dict[str, tuple[str, str]] = {}
        # snake_case plural and singular, plus shorthands, matched exactly
        self._exact: dict[str, str] = {}
        # Raw type names, case-insensitive, with ':' stripped or replaced by '_'
        self._raw: dict[str, str] = {}

        # Derived names first
        for obj_type in types:
            singular = snake_case(obj_type)
            plural = pluralize(singular)
            self.attr_for[obj_type] = plural
            for alias in (plural, singular):
                if alias in reserved_set:
                    self.conflicts[alias] = (obj_type, MEMBER_CONFLICT)
                    continue
                self._exact.setdefault(alias, obj_type)
            self._raw.setdefault(_raw_key(obj_type), obj_type)
            self._raw.setdefault(_underscore_key(obj_type), obj_type)

        # Shorthands only where they contradict neither a member nor a derived name.
        for alias, target in (shorthands or {}).items():
            if target not in present:
                continue  # exit early if the type does not exist in this schema version
            if alias in reserved_set:
                self.conflicts[alias] = (target, MEMBER_CONFLICT)
                continue
            derived = self._exact.get(alias)
            if derived is not None and derived != target:
                self.conflicts[alias] = (target, derived)
                continue
            self._exact[alias] = target
            self.shorthands[alias] = target

        # Suggestion and completion candidates
        self._candidates: dict[str, str] = {a: t for t, a in self.attr_for.items() if a not in reserved_set}
        self._candidates.update(self.shorthands)
        # Sorted once here: completion calls names() on every keystroke.
        self._names = sorted(self._candidates)

    def resolve(self, attr: str) -> str | None:
        """Return the object type an attribute name refers to, or ``None``.

        Snake_case forms match exactly. Raw type names match case-insensitively,
        written with the ``:`` kept, dropped or replaced by ``_``: ``doc.ZONE``
        works like ``doc["ZONE"]`` and ``doc.Site_Location`` reaches
        ``Site:Location``. Separator noise such as ``doc.z_o_n_e`` or
        ``doc.zone_`` does not resolve.

        A name owned by a real member never resolves, matching what ``conflicts``
        records. ``__getattr__`` only reaches such a name when the member's own
        getter raised ``AttributeError``, and answering with an object collection
        would hide that failure. ``doc.Version`` is not the member, so it still works.
        """
        if attr in self._reserved:
            return None
        hit = self._exact.get(attr)
        if hit is not None:
            return hit
        return self._raw.get(_raw_key(attr))

    def suggest(self, attr: str, n: int = 3) -> list[str]:
        """Closest canonical attribute names and shorthands, for an ``AttributeError`` message."""
        return difflib.get_close_matches(attr.lower(), self._candidates.keys(), n=n, cutoff=0.6)

    def names(self) -> list[str]:
        """Every canonical attribute name and shorthand, sorted, for ``__dir__``."""
        return list(self._names)


class AccessorAttributeError(AttributeError):
    """``AttributeError`` whose "Did you mean" suggestions are computed only when read.

    ``hasattr()`` and ``getattr(obj, name, default)`` catch this without ever
    calling ``__str__``, so the difflib cost is never paid on a silent probe.

    Pickles as a plain ``AttributeError`` carrying the final message, so it
    survives a trip from a worker process without shipping the resolver.
    """

    def __init__(self, owner: str, attr: str, resolver: AccessorResolver | None = None) -> None:
        super().__init__(attr)
        self.name = attr  # the standard AttributeError.name, typed str | None by the base class
        self._attr = attr  # a plain str copy for our own use, so pyright strict is satisfied
        self._owner = owner
        self._resolver = resolver
        self._message: str | None = None

    def __str__(self) -> str:
        if self._message is None:
            self._message = self._build()
        return self._message

    def __reduce__(self) -> tuple[type[AttributeError], tuple[str]]:
        # Rebuilding from self.args would call __init__ with one argument and fail.
        return (AttributeError, (str(self),))

    def _build(self) -> str:
        base = f"{self._owner!r} object has no attribute {self._attr!r}"
        if self._resolver is None:
            return base
        hits = self._resolver.suggest(self._attr)
        if not hits:
            return base
        width = max(len(h) for h in hits)
        lines = "\n".join(f"  {h:<{width}}  ({self._resolver.resolve(h)})" for h in hits)
        return f"{base}.\nDid you mean:\n{lines}"
