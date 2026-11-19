"""
EpJSON Schema loader and manager.

Handles loading and caching of Energy+.schema.epJSON files
for different EnergyPlus versions. Supports both uncompressed
and gzip-compressed schema files.
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, ClassVar, Final, cast

from ._forksafe import ForkSafeLock
from .exceptions import SchemaNotFoundError
from .versions import (
    ENERGYPLUS_VERSIONS,
    find_closest_version,
    reject_version_string,
    version_dirname,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from ._accessors import AccessorResolver

logger = logging.getLogger(__name__)


#: The two sizing sentinels, folded. A numeric field's schema names at most one of them.
SIZING_SENTINELS: Final = frozenset({"autosize", "autocalculate"})

#: ``{folded value: the spelling the schema declares}`` for one field.
ChoiceSpellings = Mapping[str, str]

_NO_SPELLINGS: Final[Mapping[str, ChoiceSpellings]] = MappingProxyType({})

#: The spelling tables of a type with no choice field; shared and read-only.
NO_CHOICE_SPELLINGS: Final[Mapping[str, ChoiceSpellings]] = _NO_SPELLINGS


def _no_spellings() -> Mapping[str, ChoiceSpellings]:
    """Return the shared empty spelling table.

    A ``default_factory``, because Python 3.11 refuses an unhashable dataclass default, and
    ``MappingProxyType`` is hashable only from Python 3.12.
    """
    return _NO_SPELLINGS


def _string_members(enum: Any) -> list[str]:
    """The non-empty string members of an ``enum`` value, or none when it is not a list."""
    if not isinstance(enum, list):
        return []
    return [m for m in cast("list[Any]", enum) if isinstance(m, str) and m]


def _choice_spellings(field_schema: dict[str, Any]) -> dict[str, str]:
    """Map each folded choice of a field to the spelling its schema declares; empty when it has none.

    A numeric field whose string branch names one sizing sentinel also maps the other sentinel to it,
    as ``ConvertInputFormat`` does (idfkit#181).
    """
    members = _string_members(field_schema.get("enum"))
    has_numeric_branch = False
    raw_branches = field_schema.get("anyOf")
    branches = cast("list[Any]", raw_branches) if isinstance(raw_branches, list) else []
    for raw in branches:
        if not isinstance(raw, dict):
            continue
        branch = cast("dict[str, Any]", raw)
        if branch.get("type") in ("number", "integer"):
            has_numeric_branch = True
        elif branch.get("type") == "string":
            members.extend(_string_members(branch.get("enum")))

    table: dict[str, str] = {}
    for member in members:
        table.setdefault(member.casefold(), member)
    declared = [m for m in members if m.casefold() in SIZING_SENTINELS]
    if has_numeric_branch and len(declared) == 1:
        for word in SIZING_SENTINELS:
            table.setdefault(word, declared[0])
    return table


def canonical_choice(spellings: ChoiceSpellings | None, value: Any) -> Any:
    """*value* in the spelling its field's schema declares, or unchanged when it is no listed choice.

    EnergyPlus matches choices case-insensitively, so ``"WALL"`` and ``"Wall"`` are the same value.
    The typed stubs declare the schema's spelling (``Literal["Wall", ...]``), so a value is stored
    in that spelling for the type to hold whatever case the source used. Only a string that folds
    to an entry of *spellings* changes; anything else, a number or an unlisted string, is returned
    as is. A numeric field that declares one sizing keyword also maps the other one to it
    (``Autocalculate`` reads ``"Autosize"`` where only ``Autosize`` is listed), as EnergyPlus's
    ``ConvertInputFormat`` does (see :func:`_choice_spellings`). A ``str`` subclass, such as a
    ``StrEnum`` member, is matched by its text and stored as a plain ``str``.
    """
    if spellings and isinstance(value, str):
        return spellings.get(value.casefold(), value)
    return value


def canonicalize_choices(data: dict[str, Any], pc: ParsingCache) -> None:
    """Rewrite, in place, every choice value of *data* in the spelling its schema declares.

    Covers the fixed fields and each group under the extensible wrapper. A group is rewritten only
    when it is a plain ``dict``; anything else is left for validation to report. A group that needs
    a change is replaced by a changed copy, in a new list, so dicts a caller passed to ``add()`` are
    never modified.
    """
    spellings = pc.choice_spellings
    if spellings:
        for key, value in data.items():
            table = spellings.get(key)
            if table is not None and isinstance(value, str):
                data[key] = table.get(value.casefold(), value)
    wrapper_key = pc.ext_wrapper_key
    if pc.ext_choice_spellings and wrapper_key is not None:
        groups = data.get(wrapper_key)
        if isinstance(groups, list):
            rewritten = _canonical_groups(cast("list[Any]", groups), pc.ext_choice_spellings)
            if rewritten is not None:
                data[wrapper_key] = rewritten


def _canonical_groups(groups: list[Any], spellings: Mapping[str, ChoiceSpellings]) -> list[Any] | None:
    """A copy of *groups* with each choice in its schema's spelling, or ``None`` when none changes."""
    rewritten: list[Any] | None = None
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            continue
        slots = cast("dict[str, Any]", group)
        changed = {
            key: canonical
            for key, value in slots.items()
            if (canonical := canonical_choice(spellings.get(key), value)) != value
        }
        if changed:
            if rewritten is None:
                rewritten = list(groups)
            rewritten[index] = {**slots, **changed}
    return rewritten


def trailing_underscore_aliases(field_names: Iterable[str]) -> dict[str, str]:
    """Map the spellings of a type's trailing-underscore fields to their epJSON keys.

    EnergyPlus derives an epJSON key from the IDD field name without trimming, so a name that
    ends in punctuation or a space ends in ``_``: ``"COND: Flag: Is the basement conditioned?"``
    is ``cond_flag_is_the_basement_conditioned_``. :func:`~idfkit.objects.to_python_name` trims
    that underscore, so both the key itself and the spelling without it are mapped here, the
    latter only when it is not a field of its own. ``name`` is never mapped: it means the
    object's name everywhere, including on the nameless ``Output:Table:ReportPeriod`` of
    22.2 to 25.1, whose IDD ``Name,`` field is ``name_``.

    The result is empty for nearly every type. It is shared by every object of the type and
    must not be changed; it is a plain dict so that objects holding it can be pickled.
    """
    names = set(field_names)
    aliases: dict[str, str] = {}
    for key in names:
        if key.endswith("_") and key[:-1] not in names:
            aliases[key] = key
            if key[:-1] != "name":
                aliases[key[:-1]] = key
    return aliases


def _spelling_tables(properties: Mapping[str, Any]) -> Mapping[str, ChoiceSpellings]:
    """The non-empty spelling tables of a set of field schemas, keyed by field name."""
    tables = {
        name: table
        for name, field_schema in properties.items()
        if isinstance(field_schema, dict) and (table := _choice_spellings(cast("dict[str, Any]", field_schema)))
    }
    return MappingProxyType(tables) if tables else _NO_SPELLINGS


@dataclass(frozen=True, slots=True)
class ParsingCache:
    """Pre-computed parsing metadata for a single object type.

    Built lazily on first access per object type and cached for reuse.
    Eliminates repeated nested dict traversals during parsing.
    """

    obj_schema: dict[str, Any]
    has_name: bool
    #: The positional fields after the name: ``all_field_names[1:]`` for a named type, and all
    #: of them for a type without a Name field, whose first field is an ordinary field.
    field_names: tuple[str, ...]
    all_field_names: tuple[str, ...]
    field_types: dict[str, str | None]
    ref_fields: frozenset[str]
    extensible: bool
    ext_size: int
    ext_field_names: tuple[str, ...]
    ext_wrapper_key: str | None
    ext_inner_props: Mapping[str, dict[str, Any]]
    #: Every key the type's epJSON properties name: the fixed fields plus the extensible wrapper
    #: key, never ``name``. The same set validation reports ``W003`` against.
    known_keys: frozenset[str] = frozenset()
    #: Choice spellings of the positional fields and of one extensible group (idfkit#180).
    choice_spellings: Mapping[str, ChoiceSpellings] = field(default_factory=_no_spellings)
    ext_choice_spellings: Mapping[str, ChoiceSpellings] = field(default_factory=_no_spellings)
    #: Trailing-underscore field spellings to their keys (see :func:`trailing_underscore_aliases`).
    field_aliases: Mapping[str, str] = field(default_factory=dict[str, str])


def type_family(obj_type: str) -> str:
    """The family of an object type: its name up to the first colon, uppercased.

    ``AirflowNetwork:MultiZone:Surface:Crack`` and ``AirflowNetwork:Distribution:Linkage`` are both
    ``AIRFLOWNETWORK``; ``Material`` and ``Construction`` are different families.
    """
    return obj_type.split(":", 1)[0].upper()


def _item_object_lists(array_schema: dict[str, Any]) -> set[str]:
    """The ``object_list`` entries of the fields inside an array property's item schema."""
    found: set[str] = set()
    items: Any = array_schema.get("items")
    if not isinstance(items, dict):
        return found
    item_props: Any = cast("dict[str, Any]", items).get("properties")
    if not isinstance(item_props, dict):
        return found
    for item_schema in cast("dict[str, Any]", item_props).values():
        if isinstance(item_schema, dict):
            found.update(cast("dict[str, Any]", item_schema).get("object_list") or ())
    return found


@dataclass(frozen=True, slots=True)
class ReferenceKin:
    """The object types a reference field's ``object_list`` is akin to.

    A field's ``object_list`` is sometimes narrower than what EnergyPlus accepts: it looks the
    name up among a wider set of related objects. ``SurfaceProperty:LocalEnvironment`` asks for
    ``SurfaceNames`` and EnergyPlus accepts a window there; ``AirflowNetwork:IntraZone:Linkage``
    asks for ``AirflowNetworkComponentNames`` and the shipped example files give it a crack.
    An object outside the lists is still akin when its name belongs to a reference list some type in
    the lists also belongs to (a window and a wall are both in ``AllHeatTranSurfNames``), or when
    its type is of the same [type_family][idfkit.schema.type_family] as one of them. A Material
    in a construction field, or a Zone in a schedule field, is neither.

    Two kinds of related type are never akin, because EnergyPlus looks them up elsewhere. A
    grouping type, whose repeated fields list the accepted objects, is not one of them: a
    ``ZoneList`` in a field that asks for ``ZoneNames``. Nor is a part the accepted types are
    built from, directly or through other parts, when its name shares no list with them: a
    ``Schedule:Day:Hourly`` or ``Schedule:Week:Daily`` in a field that asks for ``ScheduleNames``.

    Attributes:
        lists: Every reference list the names of the field's accepted types belong to.
        families: The [type_family][idfkit.schema.type_family] of each accepted type.
        excluded: The uppercased related types that are never akin: groupings and parts.
    """

    lists: frozenset[str]
    families: frozenset[str]
    excluded: frozenset[str] = frozenset()

    def admits(self, obj_type: str, name_lists: Iterable[str]) -> bool:
        """Whether an object of *obj_type*, whose name is in *name_lists*, is akin to the field."""
        if obj_type.upper() in self.excluded:
            return False
        return type_family(obj_type) in self.families or not self.lists.isdisjoint(name_lists)


def _resolve_field_type(
    field_name: str,
    props: dict[str, Any],
    field_info: dict[str, Any],
) -> str | None:
    """Resolve the type string for a single field from pre-extracted schema dicts."""
    field_schema = props.get(field_name)
    if field_schema is None:
        fi = field_info.get(field_name)
        if fi:
            ft = fi.get("field_type")
            if ft == "n":
                return "number"
            if ft == "a":
                return "string"
        return None

    if "anyOf" in field_schema:
        for sub in field_schema["anyOf"]:
            if sub.get("type") in ("number", "integer"):
                return sub["type"]
        return "string"

    return field_schema.get("type")


class EpJSONSchema:
    """
    Wrapper around Energy+.schema.epJSON providing easy access to object definitions.

    The schema contains:
    - Object definitions with field types, defaults, constraints
    - Reference lists (object-list) for cross-object validation
    - Legacy IDD info for IDF field ordering

    Examples:
        >>> from idfkit import get_schema, LATEST_VERSION
        >>> schema = get_schema(LATEST_VERSION)
        >>> "Zone" in schema
        True

        Check which IDD group a type belongs to:

        >>> schema.get_group("Zone")
        'Thermal Zones and Surfaces'

        Some object types (like Timestep) are singletons with no name field:

        >>> schema.has_name("Zone")
        True
        >>> schema.has_name("Timestep")
        False

    Attributes:
        version: The EnergyPlus version tuple
        _raw: The raw schema dict
        _properties: Object definitions
    """

    __slots__ = (
        "__weakref__",
        "_accessor_resolver",
        "_grouped_lists",
        "_kin_cache",
        "_name_reference_lists",
        "_object_lists",
        "_parsing_cache",
        "_pointed_lists",
        "_properties",
        "_raw",
        "_reference_lists",
        "_upper_to_canonical",
        "version",
    )

    version: tuple[int, int, int]
    _raw: dict[str, Any]
    _properties: dict[str, Any]
    _reference_lists: dict[str, list[str]]
    _object_lists: dict[str, set[str]]
    _name_reference_lists: dict[str, frozenset[str]]
    _pointed_lists: dict[str, frozenset[str]]
    _grouped_lists: dict[str, frozenset[str]]
    _kin_cache: dict[frozenset[str], ReferenceKin]
    _parsing_cache: dict[str, ParsingCache]
    _upper_to_canonical: dict[str, str]
    _accessor_resolver: AccessorResolver | None

    def __init__(self, version: tuple[int, int, int], schema_data: dict[str, Any]) -> None:
        self.version = version
        self._raw = schema_data
        self._properties: dict[str, Any] = schema_data.get("properties", {})

        # Case-insensitive lookup: UPPER → canonical type name
        self._upper_to_canonical: dict[str, str] = {k.upper(): k for k in self._properties}

        # Built on first attribute-style access; see accessor_resolver()
        self._accessor_resolver = None

        # Build reference indexes
        self._reference_lists: dict[str, list[str]] = {}
        self._object_lists: dict[str, set[str]] = {}
        self._name_reference_lists: dict[str, frozenset[str]] = {}
        # Type -> the lists its fields point into; and the lists its extensible groups point into.
        self._pointed_lists: dict[str, frozenset[str]] = {}
        self._grouped_lists: dict[str, frozenset[str]] = {}
        self._kin_cache: dict[frozenset[str], ReferenceKin] = {}
        self._parsing_cache: dict[str, ParsingCache] = {}
        self._build_reference_indexes()

    def __reduce__(self) -> tuple[Any, ...]:
        """Pickle by version, not by content, when this is the shared schema.

        A document carries its schema, so pickling a document (multiprocessing,
        joblib, ``copy.deepcopy``) would otherwise carry the full ~4 MB schema
        with it and come back as a private copy, breaking the one-schema-per-
        version invariant that :class:`SchemaManager` maintains.  The schema the
        manager handed out for this version is reconstructed by asking the
        manager again, which is a cache hit in the same process and a bundled
        load in a worker.

        A schema the manager does not know about -- built directly from custom
        schema data -- is pickled by content instead, minus ``_parsing_cache``:
        that is a rebuildable cache, and its ``MappingProxyType`` entries are
        the one part of the object pickle cannot handle (#217).
        """
        manager = _schema_manager
        if manager is not None and manager.owns(self):
            return (get_schema, (self.version,))
        # Every slot across the MRO, as ``object.__reduce_ex__`` collects them: ``type(self).__slots__``
        # alone is the most-derived declaration and would hide the base slots under a subclass.
        state = {
            name: getattr(self, name)
            for klass in reversed(type(self).__mro__)
            for name in klass.__dict__.get("__slots__", ())
            if name not in ("__weakref__", "_parsing_cache", "_accessor_resolver", "_kin_cache")
        }
        state["_parsing_cache"] = {}
        state["_kin_cache"] = {}
        state["_accessor_resolver"] = None
        return (_rebuild_schema, (type(self), state))

    def __deepcopy__(self, memo: dict[int, Any]) -> EpJSONSchema:
        """A deep copy of a schema is the schema itself.

        One schema per version is the invariant the package relies on, and a schema is read-only
        once built, so an object graph that holds one -- a document, its objects, a parser -- keeps
        sharing it under ``copy.deepcopy`` instead of each copy dragging a private clone along.
        """
        return self

    def _build_reference_indexes(self) -> None:
        """Build indexes for reference and object lists."""
        for obj_type, obj_schema in self._properties.items():
            # Check if this object provides names for any reference lists
            name_info = obj_schema.get("name", {})
            if "reference" in name_info:
                self._name_reference_lists[obj_type] = frozenset(name_info["reference"])
                for ref_list in name_info["reference"]:
                    if ref_list not in self._reference_lists:
                        self._reference_lists[ref_list] = []
                    self._reference_lists[ref_list].append(obj_type)

            # Find fields that reference object lists
            pattern_props: dict[str, Any] = obj_schema.get("patternProperties", {})
            default_dict: dict[str, Any] = {}
            inner: dict[str, Any] = next(iter(pattern_props.values()), default_dict) if pattern_props else default_dict
            self._index_reference_fields(obj_type, inner.get("properties", {}))

    def _index_reference_fields(self, obj_type: str, props: dict[str, Any]) -> None:
        """Index the lists *obj_type*'s fields, and its extensible groups' fields, point into."""
        pointed: set[str] = set()
        grouped: set[str] = set()
        for field_name, field_schema in props.items():
            field_schema_dict: dict[str, Any] = field_schema
            if "object_list" in field_schema_dict:
                pointed.update(field_schema_dict["object_list"])
                for obj_list in field_schema_dict["object_list"]:
                    if obj_list not in self._object_lists:
                        self._object_lists[obj_list] = set()
                    self._object_lists[obj_list].add(f"{obj_type}.{field_name}")
            elif field_schema_dict.get("type") == "array":
                grouped.update(_item_object_lists(field_schema_dict))
        pointed |= grouped
        if pointed:
            self._pointed_lists[obj_type] = frozenset(pointed)
        if grouped:
            self._grouped_lists[obj_type] = frozenset(grouped)

    def get_object_schema(self, obj_type: str) -> dict[str, Any] | None:
        """Get the full schema for an object type.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> zone_schema = schema.get_object_schema("Zone")
            >>> zone_schema is not None
            True
            >>> schema.get_object_schema("NonExistent") is None
            True
        """
        return self._properties.get(obj_type)

    def get_inner_schema(self, obj_type: str) -> dict[str, Any] | None:
        """Get the inner schema (inside patternProperties) for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return None
        pattern_props = obj_schema.get("patternProperties", {})
        # The pattern key varies (e.g., ".*", "^.*\\S.*$") - get the first one
        for key in pattern_props:
            return pattern_props[key]
        return None

    def get_field_schema(self, obj_type: str, field_name: str) -> dict[str, Any] | None:
        """Get schema for a specific field of an object type."""
        inner = self.get_inner_schema(obj_type)
        if not inner:
            return None
        return inner.get("properties", {}).get(field_name)

    def get_field_names(self, obj_type: str) -> list[str]:
        """Get ordered list of field names for an object type (from legacy_idd).

        Useful for discovering valid field names when building objects
        programmatically.

        Examples:
            List the fields available on a Material object:

            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> "thickness" in schema.get_field_names("Material")
            True
        """
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return []
        legacy = obj_schema.get("legacy_idd", {})
        fields: list[str] = list(legacy.get("fields", []))
        # The first legacy field is the name only for a type that has one; for a type without
        # a Name field (Output:Meter, Timestep, ...) it is an ordinary field and stays.
        return fields[1:] if "name" in obj_schema else fields

    def get_all_field_names(self, obj_type: str) -> list[str]:
        """Get all field names including 'name'."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return []
        legacy = obj_schema.get("legacy_idd", {})
        return list(legacy.get("fields", []))

    def get_required_fields(self, obj_type: str) -> list[str]:
        """Get list of required field names for an object type.

        Check which fields must be supplied before a Material is valid:

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.get_required_fields("Material")
            ['roughness', 'thickness', 'conductivity', 'density', 'specific_heat']
        """
        inner = self.get_inner_schema(obj_type)
        if not inner:
            return []
        return inner.get("required", [])

    def get_field_default(self, obj_type: str, field_name: str) -> Any:
        """Get default value for a field."""
        field_schema = self.get_field_schema(obj_type, field_name)
        if field_schema:
            return field_schema.get("default")
        return None

    def get_field_type(self, obj_type: str, field_name: str) -> str | None:
        """Get the type of a field ('number', 'string', 'integer', 'array').

        Useful for dynamic type coercion when importing data from
        spreadsheets or CSV files.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.get_field_type("Material", "thickness")
            'number'
            >>> schema.get_field_type("Material", "roughness")
            'string'
        """
        field_schema = self.get_field_schema(obj_type, field_name)
        if not field_schema:
            # An extensible field is declared in its wrapper's item schema (idfkit#179)
            pc = self.get_parsing_cache(obj_type)
            field_schema = pc.ext_inner_props.get(field_name) if pc is not None else None
        if not field_schema:
            # Fall back to legacy_idd field_info for extensible fields
            obj_schema = self.get_object_schema(obj_type)
            if obj_schema:
                field_info = obj_schema.get("legacy_idd", {}).get("field_info", {}).get(field_name)
                if field_info:
                    ft = field_info.get("field_type")
                    if ft == "n":
                        return "number"
                    if ft == "a":
                        return "string"
            return None

        # Handle anyOf (e.g., number OR "Autocalculate")
        if "anyOf" in field_schema:
            for sub in field_schema["anyOf"]:
                if sub.get("type") in ("number", "integer"):
                    return sub["type"]
            return "string"

        return field_schema.get("type")

    def get_field_object_list(self, obj_type: str, field_name: str) -> list[str] | None:
        """Get the object_list(s) that a field references."""
        field_schema = self.get_field_schema(obj_type, field_name)
        if field_schema:
            return field_schema.get("object_list")
        return None

    def get_reference_field_object_list(self, obj_type: str, field_name: str) -> list[str] | None:
        """Get the object_list(s) of a reference field, looking inside extensible groups too.

        [get_field_object_list][idfkit.schema.EpJSONSchema.get_field_object_list] reads the
        top-level properties only; a reference field inside an extensible group (a
        ``Construction:...`` layer, a ``ZoneList`` member) is described under the group's item
        schema instead.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.get_reference_field_object_list("ZoneList", "zone_name")
            ['ZoneNames']
        """
        lists = self.get_field_object_list(obj_type, field_name)
        if lists is not None:
            return lists
        pc = self.get_parsing_cache(obj_type)
        if pc is None:
            return None
        inner = pc.ext_inner_props.get(field_name)
        return inner.get("object_list") if inner is not None else None

    def get_reference_field_contributed_lists(self, obj_type: str, field_name: str) -> list[str]:
        """The reference lists a field carrying ``reference`` declares its value into.

        Most names are declared by an object's Name field, but some fields both point at an object
        and re-declare its name into another list: an ``HVACTemplate:Zone:ConstantVolume``'s
        ``zone_name`` puts the zone into ``HVACTemplateConstantVolumeZones``. Looks inside
        extensible groups too.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.get_reference_field_contributed_lists("HVACTemplate:Zone:ConstantVolume", "zone_name")
            ['HVACTemplateConstantVolumeZones']
            >>> schema.get_reference_field_contributed_lists("People", "zone_or_zonelist_or_space_or_spacelist_name")
            []
        """
        spec = self.get_field_schema(obj_type, field_name)
        if spec is None:
            pc = self.get_parsing_cache(obj_type)
            spec = pc.ext_inner_props.get(field_name) if pc is not None else None
        if spec is None:
            return []
        return list(spec.get("reference") or [])

    def get_name_reference_lists(self, obj_type: str) -> frozenset[str]:
        """The reference lists an object type's name is a member of.

        A reference field accepts a name only from the lists in its ``object_list``, so these are
        the fields that can point at an object of *obj_type*.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> "ConstructionNames" in schema.get_name_reference_lists("Construction")
            True
            >>> "ConstructionNames" in schema.get_name_reference_lists("Material")
            False
        """
        canonical = self.resolve_type_name(obj_type) or obj_type
        return self._name_reference_lists.get(canonical, frozenset())

    def get_reference_kin(self, object_list: Iterable[str]) -> ReferenceKin:
        """The [ReferenceKin][idfkit.schema.ReferenceKin] of a field's ``object_list``.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> kin = schema.get_reference_kin(["SurfaceNames"])
            >>> kin.admits("FenestrationSurface:Detailed", schema.get_name_reference_lists("FenestrationSurface:Detailed"))
            True
            >>> schedule_kin = schema.get_reference_kin(["ScheduleNames"])
            >>> schedule_kin.admits("Zone", schema.get_name_reference_lists("Zone"))
            False
            >>> schedule_kin.admits("Schedule:Day:Hourly", schema.get_name_reference_lists("Schedule:Day:Hourly"))
            False
            >>> zone_kin = schema.get_reference_kin(["ZoneNames"])
            >>> zone_kin.admits("ZoneList", schema.get_name_reference_lists("ZoneList"))
            False
        """
        accepted = frozenset(object_list)
        cached = self._kin_cache.get(accepted)
        if cached is not None:
            return cached
        lists: set[str] = set()
        families: set[str] = set()
        providers: set[str] = set()
        for ref_list in accepted:
            for provider in self.get_types_providing_reference(ref_list):
                providers.add(provider)
                lists |= self._name_reference_lists.get(provider, frozenset())
                families.add(type_family(provider))
        excluded: set[str] = set()
        # Groupings: types whose repeated fields list the accepted objects (ZoneList for ZoneNames).
        for obj_type, grouped in self._grouped_lists.items():
            if obj_type not in providers and not grouped.isdisjoint(accepted):
                excluded.add(obj_type.upper())
        excluded |= self._part_types(providers, lists, accepted)
        kin = ReferenceKin(frozenset(lists), frozenset(families), frozenset(excluded))
        self._kin_cache[accepted] = kin
        return kin

    def _part_types(self, providers: set[str], lists: set[str], accepted: frozenset[str]) -> set[str]:
        """The uppercased types the *providers* are built from, directly or through other parts.

        Only parts whose names share none of *lists* (Schedule:Year -> week -> day schedules);
        a list the providers' own names are in is not followed.
        """
        parts: set[str] = set()
        seen = set(providers)
        frontier = list(providers)
        while frontier:
            part_lists = {
                ref_list
                for obj_type in frontier
                for ref_list in self._pointed_lists.get(obj_type, frozenset())
                if ref_list not in lists and ref_list not in accepted
            }
            found = {part for ref_list in part_lists for part in self.get_types_providing_reference(ref_list)}
            frontier = sorted(found - seen)
            seen |= found
            parts.update(
                part.upper() for part in frontier if self._name_reference_lists.get(part, frozenset()).isdisjoint(lists)
            )
        return parts

    def is_reference_field(self, obj_type: str, field_name: str) -> bool:
        """Check if a field is a reference to another object."""
        return self.get_field_object_list(obj_type, field_name) is not None

    def resolve_type_name(self, obj_type: str) -> str | None:
        """Resolve a possibly-miscased type name to its canonical schema form.

        EnergyPlus is case-insensitive for object type names, so IDF files may
        use ``ZONE``, ``zone``, or ``Zone`` interchangeably.  This method
        returns the canonical PascalCase name from the schema, or ``None`` if
        the type is not recognised.
        """
        if obj_type in self._properties:
            return obj_type  # Fast path: already canonical
        return self._upper_to_canonical.get(obj_type.upper())

    def get_parsing_cache(self, obj_type: str) -> ParsingCache | None:
        """Get or lazily build pre-computed parsing metadata for an object type.

        The lookup is case-insensitive: ``ZONE``, ``zone``, and ``Zone`` all
        resolve to the same cache entry.  Returns ``None`` if *obj_type* is
        not in the schema.
        """
        cached = self._parsing_cache.get(obj_type)
        if cached is not None:
            return cached

        canonical = self.resolve_type_name(obj_type)
        if canonical is None:
            return None

        # Check if the canonical form is already cached (different casing was
        # looked up before).
        cached = self._parsing_cache.get(canonical)
        if cached is None:
            cached = self._build_parsing_cache(canonical, self._properties[canonical])
            self._parsing_cache[canonical] = cached

        # Also cache under the original key for future fast-path hits.
        if obj_type != canonical:
            self._parsing_cache[obj_type] = cached
        return cached

    def _build_parsing_cache(self, obj_type: str, obj_schema: dict[str, Any]) -> ParsingCache:  # noqa: C901
        """Build parsing metadata for a single object type."""
        has_name = "name" in obj_schema

        legacy: dict[str, Any] = obj_schema.get("legacy_idd", {})
        all_fields_list: list[str] = legacy.get("fields", [])
        all_field_names = tuple(all_fields_list)
        field_names = tuple(all_fields_list[1:]) if has_name else all_field_names

        # Extract inner schema properties
        pattern_props: dict[str, Any] = obj_schema.get("patternProperties", {})
        default_dict: dict[str, Any] = {}
        inner: dict[str, Any] = next(iter(pattern_props.values()), default_dict) if pattern_props else default_dict
        props: dict[str, Any] = inner.get("properties", {})
        # Extract extensible field schemas from array items (for reference detection)
        ext_props: dict[str, Any] = {}
        for _pk in list(props):
            _pv: dict[str, Any] = props[_pk]
            _items = _pv.get("items")
            if isinstance(_items, dict):
                _ep = cast("dict[str, Any]", _items).get("properties")
                if isinstance(_ep, dict):
                    ext_props = cast("dict[str, Any]", _ep)

        field_info: dict[str, Any] = legacy.get("field_info", {})

        # Pre-compute field types and reference fields
        field_types: dict[str, str | None] = {}
        ref_fields_set: set[str] = set()
        target_fields = field_names if has_name else all_field_names
        for fname in target_fields:
            field_types[fname] = _resolve_field_type(fname, props, field_info)
            field_schema = props.get(fname)
            if field_schema is not None and "object_list" in field_schema:
                ref_fields_set.add(fname)

        # Extensible info
        extensible = "extensible_size" in obj_schema
        ext_size = int(obj_schema.get("extensible_size", 0))
        ext_field_names_list: list[str] = legacy.get("extensibles", [])

        # Pre-compute reference fields for extensible base names
        for ext_fname in ext_field_names_list:
            ext_field_schema = ext_props.get(ext_fname)
            if ext_field_schema is not None and "object_list" in ext_field_schema:
                ref_fields_set.add(ext_fname)

        # Find the wrapper key: the unique array-typed property whose item
        # schema covers the extensible field names (e.g. "vertices" for
        # BuildingSurface:Detailed, "data" for Schedule:Day:Interval).
        # Also capture the inner property schemas — used by extensible-array
        # consumers (canonical access API, validation, codegen) to know each
        # inner field's type without re-walking the schema.
        ext_wrapper_key: str | None = None
        ext_inner_props: dict[str, dict[str, Any]] = {}
        if extensible and ext_field_names_list:
            ext_set = set(ext_field_names_list)
            for pk, pv_any in props.items():
                if not isinstance(pv_any, dict):
                    continue
                pv = cast("dict[str, Any]", pv_any)
                if pv.get("type") != "array":
                    continue
                items_any = pv.get("items")
                if not isinstance(items_any, dict):
                    continue
                inner_any = cast("dict[str, Any]", items_any).get("properties")
                if not isinstance(inner_any, dict):
                    continue
                inner = cast("dict[str, Any]", inner_any)
                if ext_set.issubset(inner.keys()):
                    ext_wrapper_key = pk
                    ext_inner_props = {k: cast("dict[str, Any]", v) for k, v in inner.items()}
                    break

        # Type extensible fields from the wrapper's item schema, which declares them; the top level
        # does not, and the legacy IDD fallback has no integer type (idfkit#179).
        for ext_fname in ext_field_names_list:
            if ext_fname not in field_types:
                type_source = ext_inner_props if ext_fname in ext_inner_props else props
                field_types[ext_fname] = _resolve_field_type(ext_fname, type_source, field_info)

        return ParsingCache(
            obj_schema=obj_schema,
            has_name=has_name,
            field_names=field_names,
            all_field_names=all_field_names,
            field_types=field_types,
            ref_fields=frozenset(ref_fields_set),
            extensible=extensible,
            ext_size=ext_size,
            ext_field_names=tuple(ext_field_names_list),
            ext_wrapper_key=ext_wrapper_key,
            ext_inner_props=MappingProxyType(ext_inner_props),
            known_keys=frozenset(name for name, spec in props.items() if spec),
            choice_spellings=_spelling_tables(props),
            ext_choice_spellings=_spelling_tables(ext_inner_props),
            field_aliases=trailing_underscore_aliases(all_fields_list),
        )

    def get_types_providing_reference(self, ref_list: str) -> list[str]:
        """Get object types that provide names for a reference list."""
        return self._reference_lists.get(ref_list, [])

    def get_group(self, obj_type: str) -> str | None:
        """Get the IDD group name for an object type.

        Every object type in the EnergyPlus schema belongs to a group
        (e.g. ``"Thermal Zones and Surfaces"``, ``"HVAC Templates"``,
        ``"Detailed Ground Heat Transfer"``).  This method returns the
        group string, which is useful for classifying objects without
        relying on naming conventions.

        Args:
            obj_type: Case-sensitive EnergyPlus object type
                (e.g. ``"Zone"``, ``"HVACTemplate:Zone:IdealLoadsAirSystem"``).

        Returns:
            The group name, or ``None`` if *obj_type* is not in the schema.

        Examples:
            ```python
            schema = get_schema((24, 1, 0))
            schema.get_group("Zone")
            # "Thermal Zones and Surfaces"
            schema.get_group("HVACTemplate:Zone:IdealLoadsAirSystem")
            # "HVAC Templates"
            ```
        """
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return obj_schema.get("group")
        return None

    def get_object_memo(self, obj_type: str) -> str | None:
        """Get the memo/description for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return obj_schema.get("memo")
        return None

    def has_name(self, obj_type: str) -> bool:
        """Check if an object type has a name field (first IDF field is a name)."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return True  # Default: assume named (backward compat)
        return "name" in obj_schema

    def get_extensible_field_names(self, obj_type: str) -> list[str]:
        """Get extensible field names from legacy_idd.extensibles."""
        obj_schema = self.get_object_schema(obj_type)
        if not obj_schema:
            return []
        legacy = obj_schema.get("legacy_idd", {})
        return legacy.get("extensibles", [])

    def is_extensible(self, obj_type: str) -> bool:
        """Check if an object type has extensible fields.

        Extensible types (like surfaces) can have a variable number of
        vertices or layers.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.is_extensible("BuildingSurface:Detailed")
            True
            >>> schema.is_extensible("Zone")
            False
        """
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return "extensible_size" in obj_schema
        return False

    def get_extensible_size(self, obj_type: str) -> int | None:
        """Get the extensible group size for an object type."""
        obj_schema = self.get_object_schema(obj_type)
        if obj_schema:
            return obj_schema.get("extensible_size")
        return None

    def get_extensible_wrapper_key(self, obj_type: str) -> str | None:
        """Return the canonical epJSON wrapper key for an extensible type.

        For ``BuildingSurface:Detailed`` this is ``"vertices"``; for
        ``Schedule:Day:Interval`` it is ``"data"``. Returns ``None`` if the
        type is not extensible or its schema does not expose an array
        wrapper (e.g. types where extensibles are inlined alongside fixed
        fields, like ``Site:SpectrumData``).

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> schema.get_extensible_wrapper_key("BuildingSurface:Detailed")
            'vertices'
            >>> schema.get_extensible_wrapper_key("Schedule:Day:Interval")
            'data'
            >>> schema.get_extensible_wrapper_key("Zone") is None
            True
        """
        cache = self.get_parsing_cache(obj_type)
        return cache.ext_wrapper_key if cache else None

    @property
    def object_types(self) -> list[str]:
        """Get list of all object types in the schema.

        Examples:
            >>> from idfkit import get_schema, LATEST_VERSION
            >>> schema = get_schema(LATEST_VERSION)
            >>> "Zone" in schema.object_types
            True
            >>> len(schema.object_types) > 100
            True
        """
        return list(self._properties.keys())

    def accessor_resolver(self, build: Callable[[EpJSONSchema], AccessorResolver]) -> AccessorResolver:
        """Return this schema's attribute resolver, building it on first use.

        The resolver lives on the schema so it is released with it: dropping a
        schema from the manager's cache frees its resolver too. ``build`` is
        passed in so this module needs no runtime import of the accessor code.

        The slot is read with a default because a schema unpickled from state
        written before the slot existed does not have it set.
        """
        resolver: AccessorResolver | None = getattr(self, "_accessor_resolver", None)
        if resolver is None:
            resolver = build(self)
            self._accessor_resolver = resolver
        return resolver

    def __contains__(self, obj_type: str) -> bool:
        """Check if an object type exists in the schema."""
        return obj_type in self._properties

    def __len__(self) -> int:
        """Return number of object types."""
        return len(self._properties)


_SCHEMA_FILENAME = "Energy+.schema.epJSON"
_SCHEMA_FILENAME_GZ = "Energy+.schema.epJSON.gz"


def load_schema_json(path: Path) -> dict[str, Any]:
    """Load a schema JSON file, handling both plain and gzip-compressed files."""
    if path.suffix == ".gz" or path.name.endswith(".epJSON.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class SchemaManager:
    """
    Manages loading and caching of EpJSON schemas for different versions.

    Searches for schemas in the following order:
    1. Bundled schemas directory (shipped with idfkit) - both .gz and plain
    2. User cache directory (~/.idfkit/schemas/)
    3. EnergyPlus installation directories

    Supports gzip-compressed schema files (.epJSON.gz) to reduce package size.
    """

    # Common EnergyPlus installation paths by platform
    _INSTALL_PATHS: ClassVar[dict[str, list[str]]] = {
        "linux": ["/usr/local/EnergyPlus-{v}", "/opt/EnergyPlus-{v}"],
        "darwin": ["/Applications/EnergyPlus-{v}"],
        "win32": [
            "C:\\EnergyPlusV{v}",
            "C:\\EnergyPlus-{v}",
            os.path.expandvars("$LOCALAPPDATA\\EnergyPlusV{v}"),
        ],
    }

    def __init__(
        self,
        bundled_schema_dir: Path | None = None,
        cache_dir: Path | None = None,
    ):
        """
        Initialize the schema manager.

        Args:
            bundled_schema_dir: Path to directory with bundled schema files.
                               If None, uses default location next to this file.
            cache_dir: Path to user cache directory for downloaded schemas.
                       If None, uses ~/.idfkit/schemas/.
        """
        if bundled_schema_dir is None:
            bundled_schema_dir = Path(__file__).parent / "schemas"

        if cache_dir is None:
            cache_dir = Path.home() / ".idfkit" / "schemas"

        self._bundled_dir = bundled_schema_dir
        self._cache_dir = cache_dir
        self._cache: dict[tuple[int, int, int], EpJSONSchema] = {}
        # Upper-cased object type -> every field key it has had in any supported release; built
        # on first use by `field_names_in_any_release`.
        self._release_fields: dict[str, frozenset[str]] | None = None
        self._init_locks()

    def _init_locks(self) -> None:
        """Give this manager fresh locks and a fresh generation: at construction, copy and unpickle."""
        # One load lock per version: a miss loads once however many threads ask at the same time,
        # while two different versions still load in parallel. Reentrant, because the load runs
        # logging handlers, and one that asks for the same version again must not deadlock.
        self._load_locks: dict[tuple[int, int, int], ForkSafeLock] = {}
        # Bumped by `clear_cache`, under `_publish_lock`. A load that began before a clear must not
        # publish what it read: the clear would be undone, and a request made after the clear would
        # be handed the pre-clear schema.
        self._generation = 0
        self._publish_lock = ForkSafeLock()

    def __getstate__(self) -> dict[str, Any]:
        """Copy and pickle the paths and a snapshot of the cache, not the locks."""
        state = dict(self.__dict__)
        state["_cache"] = dict(self._cache)
        for name in ("_load_locks", "_generation", "_publish_lock"):
            state.pop(name, None)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Restore with locks of its own; state pickled by idfkit 1.2.0 has none to drop."""
        self.__dict__.update(state)
        self.__dict__.setdefault("_release_fields", None)
        self._init_locks()

    @property
    def bundled_dir(self) -> Path:
        """Path to the bundled schemas directory."""
        return self._bundled_dir

    @property
    def cache_dir(self) -> Path:
        """Path to the user cache directory for schemas."""
        return self._cache_dir

    def get_schema(self, version: tuple[int, int, int]) -> EpJSONSchema:
        """
        Load and return schema for a specific version.

        If the exact version is not found, attempts to find the closest
        supported version that is <= the requested version.

        Args:
            version: EnergyPlus version tuple (major, minor, patch)

        Returns:
            EpJSONSchema for the requested version

        Raises:
            SchemaNotFoundError: If schema cannot be found
            TypeError: If *version* is a string such as ``"24.1.0"`` rather than a tuple
        """
        cached = self._cache.get(version)
        if cached is not None:
            return cached
        reject_version_string(version)

        # Without this, threads that miss at the same time each load and build their own copy, and
        # each walks away with a different instance: the one-schema-per-version invariant breaks,
        # and pickling (see ``owns``) sends all but the last-cached by content.
        # ``dict.setdefault`` is atomic, with or without the GIL, so the lock table needs no lock.
        load_lock = self._load_locks.get(version)
        if load_lock is None:
            load_lock = self._load_locks.setdefault(version, ForkSafeLock(reentrant=True))
        with load_lock.lock:
            cached = self._cache.get(version)
            if cached is not None:
                return cached
            generation = self._generation
            t0 = time.perf_counter()
            schema = self._load_schema(version)
            with self._publish_lock.lock:
                if generation == self._generation:
                    # A re-entrant request for this version (from code the load ran) may have
                    # published first; keep its instance, so every caller holds the cached one.
                    schema = self._cache.setdefault(version, schema)
            # Logged only once published: a logging handler that asks for this version gets the
            # cached schema instead of starting another load.
            logger.info(
                "Loaded schema for version %d.%d.%d (%d object types) in %.3fs",
                *version,
                len(schema),
                time.perf_counter() - t0,
            )
            return schema

    def _load_schema(self, version: tuple[int, int, int]) -> EpJSONSchema:
        """Load *version* from disk. The caller holds that version's load lock, publishes the result and logs it."""
        # Try exact version first
        schema_path = self._find_schema_file(version)
        if schema_path is None:
            # Try closest supported version
            closest = find_closest_version(version)
            if closest is not None and closest != version:
                logger.debug(
                    "Exact schema not found for %d.%d.%d, falling back to closest %d.%d.%d",
                    *version,
                    *closest,
                )
                schema_path = self._find_schema_file(closest)

        if schema_path is None:
            searched = self._get_searched_paths(version)
            raise SchemaNotFoundError(version, searched)

        logger.debug("Loading schema from %s", schema_path)
        data = load_schema_json(schema_path)

        return EpJSONSchema(version, data)

    def _find_schema_file(self, version: tuple[int, int, int]) -> Path | None:
        """
        Find the schema file for a version.

        Searches bundled directory first (both compressed and plain),
        then user cache, then EnergyPlus installations.
        """
        # Try bundled schemas first
        for path in self._get_bundled_paths(version):
            if path.exists():
                return path

        # Try user cache
        for path in self._get_cache_paths(version):
            if path.exists():
                return path

        # Try EnergyPlus installation
        for path in self._get_install_paths(version):
            if path.exists():
                return path

        return None

    def _get_searched_paths(self, version: tuple[int, int, int]) -> list[str]:
        """Get all paths that would be searched for a version (for error messages)."""
        paths: list[str] = []
        for p in self._get_bundled_paths(version):
            paths.append(str(p))
        for p in self._get_cache_paths(version):
            paths.append(str(p))
        for p in self._get_install_paths(version):
            paths.append(str(p))
        return paths

    def _get_bundled_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential bundled schema paths for a version."""
        paths: list[Path] = []
        dirname = version_dirname(version)

        # Compressed first (preferred for bundled), then plain
        paths.append(self._bundled_dir / dirname / _SCHEMA_FILENAME_GZ)
        paths.append(self._bundled_dir / dirname / _SCHEMA_FILENAME)

        return paths

    def _get_cache_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential user cache schema paths for a version."""
        paths: list[Path] = []
        dirname = version_dirname(version)

        paths.append(self._cache_dir / dirname / _SCHEMA_FILENAME_GZ)
        paths.append(self._cache_dir / dirname / _SCHEMA_FILENAME)

        return paths

    def _get_install_paths(self, version: tuple[int, int, int]) -> list[Path]:
        """Get potential EnergyPlus installation schema paths."""
        import sys

        platform = sys.platform
        paths: list[Path] = []
        v = version

        # Get base paths for this platform
        base_patterns: list[str] = self._INSTALL_PATHS.get(platform, self._INSTALL_PATHS.get("linux", []))

        version_formats = [
            f"{v[0]}-{v[1]}-{v[2]}",
            f"{v[0]}.{v[1]}.{v[2]}",
            f"{v[0]}-{v[1]}",
        ]

        for base_pattern in base_patterns:
            for v_fmt in version_formats:
                base_path = Path(base_pattern.format(v=v_fmt))
                paths.append(base_path / _SCHEMA_FILENAME)

        return paths

    def get_available_versions(self) -> list[tuple[int, int, int]]:  # noqa: C901
        """
        Get list of versions with available schemas.

        Checks bundled schemas, user cache, and installed EnergyPlus versions.
        """
        versions: set[tuple[int, int, int]] = set()

        # Check bundled
        if self._bundled_dir.exists():
            for item in self._bundled_dir.iterdir():
                if item.is_dir():
                    version = self._parse_version_from_dirname(item.name)
                    if version and self._dir_has_schema(item):
                        versions.add(version)

        # Check user cache
        if self._cache_dir.exists():
            for item in self._cache_dir.iterdir():
                if item.is_dir():
                    version = self._parse_version_from_dirname(item.name)
                    if version and self._dir_has_schema(item):
                        versions.add(version)

        # Check installed EnergyPlus versions
        import sys

        platform = sys.platform
        base_patterns: list[str] = self._INSTALL_PATHS.get(platform, self._INSTALL_PATHS.get("linux", []))

        for pattern in base_patterns:
            # Look for existing directories matching the pattern
            parent = Path(pattern.split("{v}")[0])
            if parent.exists():
                for item in parent.iterdir():
                    if item.is_dir() and "EnergyPlus" in item.name:
                        version = self._parse_version_from_dirname(item.name)
                        if version:
                            schema_path = item / _SCHEMA_FILENAME
                            if schema_path.exists():
                                versions.add(version)

        return sorted(versions)

    @staticmethod
    def _dir_has_schema(directory: Path) -> bool:
        """Check if a directory contains a schema file (plain or compressed)."""
        return (directory / _SCHEMA_FILENAME).exists() or (directory / _SCHEMA_FILENAME_GZ).exists()

    @staticmethod
    def _parse_version_from_dirname(dirname: str) -> tuple[int, int, int] | None:
        """Parse version tuple from directory name."""
        import re

        # Match patterns like "9-2-0", "9.2.0", "V9-2-0", "EnergyPlus-9-2-0"
        match = re.search(r"(\d+)[-._](\d+)[-._]?(\d+)?", dirname)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3)) if match.group(3) else 0
            return (major, minor, patch)
        return None

    def field_names_in_any_release(self, obj_type: str) -> frozenset[str]:
        """Every field key *obj_type* has had in any supported EnergyPlus release.

        Tells a field a release removed (``availability_manager_list_name`` on
        ``AirLoopHVAC:OutdoorAirSystem``, still in EnergyPlus's own example files) from one no
        release ever had, which is a typo. The first call reads every schema file it can find,
        about a second and a half, without keeping them; the index it builds is kept.
        """
        index = self._release_fields
        if index is None:
            fields: dict[str, set[str]] = {}
            for version in ENERGYPLUS_VERSIONS:
                path = self._find_schema_file(version)
                if path is None:
                    continue
                properties: dict[str, Any] = load_schema_json(path).get("properties", {})
                no_fields: dict[str, Any] = {}
                for type_name, spec in properties.items():
                    pattern: dict[str, Any] = spec.get("patternProperties") or {}
                    inner: dict[str, Any] = next(iter(pattern.values()), no_fields)
                    fields.setdefault(type_name.upper(), set()).update(inner.get("properties", {}))
            index = {type_name: frozenset(names) for type_name, names in fields.items()}
            self._release_fields = index
        return index.get(obj_type.upper(), frozenset())

    def owns(self, schema: EpJSONSchema) -> bool:
        """Whether *schema* is the instance this manager currently hands out for its version.

        Pickling asks this: a schema the manager owns travels by version and is re-resolved through
        the manager on load, while any other instance travels by content (see
        :meth:`EpJSONSchema.__reduce__`).
        """
        return self._cache.get(schema.version) is schema

    def clear_cache(self) -> None:
        """Clear the schema cache.

        A load still in flight when this is called returns its schema to its caller but does not
        cache it, so every request made after the call loads afresh.
        """
        with self._publish_lock.lock:
            self._generation += 1
            self._cache.clear()

    def get_supported_versions(self) -> list[tuple[int, int, int]]:
        """Get list of all EnergyPlus versions that idfkit supports.

        This returns all versions in the registry, regardless of whether
        schema files are currently available locally.
        """
        return list(ENERGYPLUS_VERSIONS)


# Global schema manager instance
_schema_manager: SchemaManager | None = None
_schema_manager_lock = ForkSafeLock()


def get_schema_manager() -> SchemaManager:
    """Get the global schema manager instance."""
    global _schema_manager
    manager = _schema_manager
    if manager is None:
        # Checked again under the lock: without it, threads racing the first call on a
        # free-threaded build each create a manager, and each manager loads its own schemas.
        with _schema_manager_lock.lock:
            if _schema_manager is None:
                _schema_manager = SchemaManager()
            manager = _schema_manager
    return manager


def _rebuild_schema(cls: type[EpJSONSchema], state: dict[str, Any]) -> EpJSONSchema:
    """Unpickle a schema the manager does not own (see :meth:`EpJSONSchema.__reduce__`)."""
    schema = cls.__new__(cls)
    for name, value in state.items():
        setattr(schema, name, value)
    return schema


def get_schema(version: tuple[int, int, int]) -> EpJSONSchema:
    """Convenience function to get schema for a version.

    Examples:
        >>> from idfkit import get_schema, LATEST_VERSION
        >>> schema = get_schema(LATEST_VERSION)
        >>> "Zone" in schema
        True
        >>> schema = get_schema((24, 1, 0))
        >>> schema.version
        (24, 1, 0)
    """
    return get_schema_manager().get_schema(version)
