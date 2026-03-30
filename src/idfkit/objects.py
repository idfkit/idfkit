"""
Core object classes for IDF representation.

IDFObject: Thin wrapper around a dict with attribute access.
IDFCollection: Indexed collection of IDFObjects with O(1) lookup.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from ._compat_object import EppyObjectMixin
from .exceptions import InvalidFieldError

__all__ = ["IDFCollection", "IDFObject", "to_python_name"]

if TYPE_CHECKING:
    from .document import IDFDocument

# Field name conversion patterns
_FIELD_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9]+")

# Matches a numbered extensible field like "vertex_1_x_coordinate" -> "vertex_x_coordinate"
_EXTENSIBLE_NUMBER_PATTERN = re.compile(r"^(.+?)_(\d+)_(.+)$")


def parse_extensible_index(field_name: str, extensibles: frozenset[str]) -> tuple[str | None, int]:
    """Extract the base name and 1-based group index from an extensible field name.

    Handles both naming conventions:
    - ``field_1`` / ``field_2`` (user style, base ``field``)
    - ``vertex_1_x_coordinate`` / ``vertex_2_x_coordinate`` (user style)
    - ``field`` / ``field_2`` (schema style, first group has no number)
    - ``vertex_x_coordinate`` / ``vertex_x_coordinate_2`` (schema style)

    Returns ``(base_name, group_index)`` or ``(None, 0)`` if not extensible.
    """
    if field_name in extensibles:
        return field_name, 1

    last_underscore = field_name.rfind("_")
    if last_underscore > 0 and field_name[last_underscore + 1 :].isdigit():
        base = field_name[:last_underscore]
        num = int(field_name[last_underscore + 1 :])
        if base in extensibles:
            return base, num

    m = _EXTENSIBLE_NUMBER_PATTERN.match(field_name)
    if m:
        base = f"{m.group(1)}_{m.group(3)}"
        if base in extensibles:
            return base, int(m.group(2))

    return None, 0


def extensible_schema_name(base: str, group: int) -> str:
    """Generate the epJSON schema-convention name: base for group 1, base_N for N>=2."""
    return base if group == 1 else f"{base}_{group}"


def normalize_extensible_name(field_name: str, extensibles: frozenset[str]) -> str:
    """Normalize an extensible field name to the epJSON schema convention.

    Converts ``field_1`` → ``field``, ``vertex_1_x_coordinate`` → ``vertex_x_coordinate``,
    ``vertex_2_x_coordinate`` → ``vertex_x_coordinate_2``, etc.
    Returns the name unchanged if it is not extensible.
    """
    base, group = parse_extensible_index(field_name, extensibles)
    if base is None:
        return field_name
    return extensible_schema_name(base, group)


def to_python_name(idf_name: str) -> str:
    """Convert IDF field name to Python-friendly name.

    'Direction of Relative North' -> 'direction_of_relative_north'
    'X Origin' -> 'x_origin'
    """
    return _FIELD_NAME_PATTERN.sub("_", idf_name.lower()).strip("_")


def to_idf_name(python_name: str) -> str:
    """Convert Python name back to IDF-style name.

    'direction_of_relative_north' -> 'Direction of Relative North'
    """
    return " ".join(word.capitalize() for word in python_name.split("_"))


class IDFObject(EppyObjectMixin):
    """
    Lightweight wrapper around a dict representing an EnergyPlus object.

    Uses __slots__ for memory efficiency - each object is ~200 bytes.
    Provides attribute access to fields via __getattr__/__setattr__.

    Examples:
        Create a rigid insulation material and access its properties:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> insulation = model.add("Material", "XPS_50mm",
        ...     roughness="Rough", thickness=0.05,
        ...     conductivity=0.034, density=35.0, specific_heat=1400.0)

        Read thermal properties as attributes:

        >>> insulation.conductivity
        0.034
        >>> insulation.thickness
        0.05

        Modify for parametric analysis (double the insulation):

        >>> insulation.thickness = 0.1
        >>> insulation.thickness
        0.1

        Export to a dictionary for use with external tools:

        >>> d = insulation.to_dict()
        >>> d["conductivity"]
        0.034

    Attributes:
        _type: The IDF object type (e.g., "Zone", "Material")
        _name: The object's name (first field)
        _data: Dict of field_name -> value
        _schema: Optional schema dict for validation
        _document: Reference to parent document (for reference resolution)
        _field_order: Ordered list of field names from schema
    """

    __slots__ = (
        "__weakref__",
        "_data",
        "_document",
        "_extensibles",
        "_field_order",
        "_name",
        "_ref_fields",
        "_schema",
        "_source_text",
        "_type",
        "_version",
    )

    _type: str
    _name: str
    _data: dict[str, Any]
    _schema: dict[str, Any] | None
    _document: IDFDocument[bool] | None
    _field_order: list[str] | None
    _ref_fields: frozenset[str] | None
    _source_text: str | None

    def __init__(
        self,
        obj_type: str,
        name: str,
        data: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        document: IDFDocument[bool] | None = None,
        field_order: list[str] | None = None,
        ref_fields: frozenset[str] | None = None,
        source_text: str | None = None,
        extensibles: frozenset[str] | None = None,
    ) -> None:
        object.__setattr__(self, "_type", obj_type)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_data", data if data is not None else {})
        object.__setattr__(self, "_schema", schema)
        object.__setattr__(self, "_document", document)
        object.__setattr__(self, "_extensibles", extensibles or frozenset())
        object.__setattr__(self, "_field_order", field_order)
        object.__setattr__(self, "_ref_fields", ref_fields)
        object.__setattr__(self, "_source_text", source_text)
        object.__setattr__(self, "_version", 0)

    @property
    def obj_type(self) -> str:
        """The IDF object type (e.g., 'Zone', 'Material')."""
        return self._type

    @property
    def mutation_version(self) -> int:
        """Monotonically increasing counter bumped on every field write.

        Useful for caches that need to detect whether an object has been
        modified since a cached value was computed.
        """
        return self._version

    @property
    def data(self) -> dict[str, Any]:
        """The field data dictionary."""
        return self._data

    @property
    def schema_dict(self) -> dict[str, Any] | None:
        """The schema dict for this object type."""
        return self._schema

    @property
    def source_text(self) -> str | None:
        """Original source text from parsing, or ``None`` if the object was mutated or created programmatically."""
        return self._source_text

    @property
    def field_order(self) -> list[str] | None:
        """Ordered list of field names from schema."""
        return self._field_order

    def _is_known_field(self, python_key: str, field_order: list[str]) -> bool:
        """Check if a field name is valid for this object type.

        Checks the base field order first, then extensible field patterns.
        Handles both ``vertex_1_x_coordinate`` -> ``vertex_x_coordinate``
        and ``field_1`` -> ``field``.
        """
        if python_key in field_order:
            return True
        extensibles = self._extensibles
        if not extensibles:
            return False
        # Try "prefix_N_suffix" -> "prefix_suffix" (e.g. vertex_1_x_coordinate -> vertex_x_coordinate)
        m = _EXTENSIBLE_NUMBER_PATTERN.match(python_key)
        if m and f"{m.group(1)}_{m.group(3)}" in extensibles:
            return True
        # Try "base_N" -> "base" (e.g. field_1461 -> field)
        last_underscore = python_key.rfind("_")
        if last_underscore > 0 and python_key[last_underscore + 1 :].isdigit():
            base = python_key[:last_underscore]
            if base in extensibles:
                return True
        return False

    @property
    def name(self) -> str:
        """The object's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the object's name."""
        self._set_name(value)

    def __getattr__(self, key: str) -> Any:
        """Get field value by attribute name.

        When the parent document has ``strict=True``, accessing a field
        name that is neither present in the data dict nor recognised by
        the schema raises ``AttributeError`` instead of returning
        ``None``.  This catches typos during migration.
        """
        if key.startswith("_"):
            raise AttributeError(key)

        # Try exact match first
        data = object.__getattribute__(self, "_data")
        if key in data:
            return data[key]

        # Try lowercase version
        key_lower = key.lower()
        if key_lower in data:
            return data[key_lower]

        # Try python name conversion
        python_key = to_python_name(key)
        if python_key in data:
            return data[python_key]

        # Try normalizing extensible field name to schema convention
        schema_key = self._normalize_extensible_key(python_key)
        if schema_key != python_key and schema_key in data:
            return data[schema_key]

        # Field not found — check strict mode
        doc = object.__getattribute__(self, "_document")
        if doc is not None and getattr(doc, "_strict", False):
            # In strict mode, only allow known schema fields
            field_order = object.__getattribute__(self, "_field_order")
            if field_order is not None and not self._is_known_field(python_key, field_order):
                obj_type = object.__getattribute__(self, "_type")
                ver: tuple[int, int, int] | None = object.__getattribute__(doc, "version")
                raise InvalidFieldError(
                    obj_type,
                    key,
                    available_fields=list(field_order),
                    version=ver,
                    extensible_fields=object.__getattribute__(self, "_extensibles"),
                )

        # Default: return None (eppy behaviour)
        return None

    def __setattr__(self, key: str, value: Any) -> None:
        """Set field value by attribute name.

        Extensible field names are normalized to the epJSON schema convention
        (``field``, ``field_2``; ``vertex_x_coordinate``, ``vertex_x_coordinate_2``).
        """
        if key.startswith("_"):
            object.__setattr__(self, key, value)
        elif key.lower() == "name":
            self._set_name(value)
        else:
            # Normalize key to python style
            python_key = to_python_name(key)
            # Validate in strict mode
            doc = self._document
            if doc is not None and getattr(doc, "_strict", False):
                field_order = self._field_order
                if field_order is not None and not self._is_known_field(python_key, field_order):
                    ver: tuple[int, int, int] | None = object.__getattribute__(doc, "version")
                    raise InvalidFieldError(
                        self._type,
                        key,
                        available_fields=list(field_order),
                        version=ver,
                        extensible_fields=self._extensibles,
                    )
            # Normalize extensible field names to schema convention.
            python_key = self._normalize_extensible_key(python_key)
            self._set_field(python_key, value)

    def __getitem__(self, key: str | int) -> Any:
        """Get field value by name or index."""
        if isinstance(key, int):
            if key == 0:
                return self._name
            if self._field_order and 0 < key <= len(self._field_order):
                field_name = self._field_order[key - 1]
                return self._data.get(field_name)
            raise IndexError(f"Field index {key} out of range")  # noqa: TRY003
        return getattr(self, key)

    def __setitem__(self, key: str | int, value: Any) -> None:
        """Set field value by name or index."""
        if isinstance(key, int):
            if key == 0:
                self._set_name(value)
            elif self._field_order and 0 < key <= len(self._field_order):
                field_name = self._field_order[key - 1]
                self._set_field(field_name, value)
            else:
                raise IndexError(f"Field index {key} out of range")  # noqa: TRY003
        else:
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"{self._type}('{self._name}')"

    def __str__(self) -> str:
        return f"{self._type}: {self._name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IDFObject):
            return NotImplemented
        return self._type == other._type and self._name == other._name and self._data == other._data

    def __hash__(self) -> int:
        return id(self)

    def _set_name(self, value: str) -> None:
        """Centralized name-change logic with document notification."""
        old = self._name
        if old == value:
            return
        object.__setattr__(self, "_name", value)
        object.__setattr__(self, "_version", self._version + 1)
        object.__setattr__(self, "_source_text", None)
        doc = self._document
        if doc is not None:
            doc.notify_name_change(self, old, value)

    def _set_field(self, python_key: str, value: Any) -> None:
        """Centralized data-field write with reference graph notification.

        When an extensible field is written that is not yet in ``field_order``,
        all intermediate gap fields are created (with ``None`` values) so that
        writers and iterators see a contiguous sequence.
        """
        doc = self._document
        ref_fields = self._ref_fields
        if doc is not None and ref_fields is not None and python_key in ref_fields:
            old = self._data.get(python_key)
            self._data[python_key] = value
            if old != value:
                doc.notify_reference_change(self, python_key, old, value)
        else:
            self._data[python_key] = value

        # Maintain field_order for new extensible fields, filling any gaps.
        field_order = self._field_order
        if field_order is not None and python_key not in field_order:
            extensibles = self._extensibles
            if extensibles and self._is_known_field(python_key, field_order):
                self._fill_extensible_gap(python_key, field_order, extensibles)

        object.__setattr__(self, "_version", self._version + 1)
        object.__setattr__(self, "_source_text", None)

    def _fill_extensible_gap(
        self,
        python_key: str,
        field_order: list[str],
        extensibles: frozenset[str],
    ) -> None:
        """Append extensible fields to ``field_order``, filling gaps with ``None``.

        Given a new extensible field like ``field_41``, determines the group
        index (41 for a single-field group), finds the current highest group
        index in ``field_order``, and generates all intermediate groups so
        that the field sequence is contiguous.

        For multi-field groups (e.g. vertices with x/y/z), all fields in each
        gap group are created.
        """
        ext_names = sorted(extensibles)  # stable order

        # Parse the target field to find its base name and group index.
        target_base, target_group = parse_extensible_index(python_key, extensibles)
        if target_base is None:
            # Couldn't parse — just append as-is.
            field_order.append(python_key)
            return

        # Find the current highest group index already in field_order.
        max_group = 0
        for name in field_order:
            base, group = parse_extensible_index(name, extensibles)
            if base is not None and group > max_group:
                max_group = group

        # Generate all groups from max_group+1 through target_group
        # using the epJSON schema naming convention.
        existing = set(field_order)
        schema_key = extensible_schema_name(target_base, target_group)
        for g in range(max_group + 1, target_group + 1):
            for base in ext_names:
                field_name = extensible_schema_name(base, g)
                if field_name not in existing:
                    field_order.append(field_name)
                    existing.add(field_name)
                    # Fill gap fields with None in data (don't overwrite the
                    # target field which was already written above).
                    if field_name != schema_key and field_name not in self._data:
                        self._data[field_name] = None

    def _normalize_extensible_key(self, python_key: str) -> str:
        """Normalize an extensible field name to the epJSON schema convention."""
        extensibles = self._extensibles
        if not extensibles:
            return python_key
        return normalize_extensible_name(python_key, extensibles)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Useful for serializing EnergyPlus objects to JSON, CSV, or
        DataFrames for post-processing.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> d = mat.to_dict()
            >>> d["name"], d["thickness"], d["conductivity"]
            ('Concrete_200mm', 0.2, 1.4)
        """
        return {"name": self._name, **self._data}

    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with default.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> mat.get("conductivity")
            1.4
            >>> mat.get("thermal_absorptance", 0.9)
            0.9
        """
        value = getattr(self, key)
        return value if value is not None else default

    def copy(self) -> IDFObject:
        """Create a copy of this object."""
        return IDFObject(
            obj_type=self._type,
            name=self._name,
            data=dict(self._data),
            schema=self._schema,
            document=None,  # Don't copy document reference
            field_order=list(self._field_order) if self._field_order is not None else None,
            ref_fields=self._ref_fields,
            source_text=None,  # copy is a new object; don't carry over verbatim text
            extensibles=self._extensibles,
        )

    def __dir__(self) -> list[str]:
        """Return attributes for tab completion (includes schema field names)."""
        attrs = [
            "obj_type",
            "name",
            "data",
            "key",
            "Name",
            "fieldnames",
            "fieldvalues",
            "theidf",
            "schema_dict",
            "field_order",
            "to_dict",
            "get",
            "copy",
            "get_field_idd",
            "get_referenced_object",
            "getfieldidd",
            "getfieldidd_item",
            "getrange",
            "checkrange",
            "getreferingobjs",
        ]
        field_order = object.__getattribute__(self, "_field_order")
        if field_order:
            attrs.extend(field_order)
        else:
            data = object.__getattribute__(self, "_data")
            attrs.extend(data.keys())
        return attrs

    def _repr_svg_(self) -> str | None:
        """Return SVG representation for Jupyter/IPython display.

        Currently supports Construction objects, rendering a cross-section
        diagram showing layer sequence, thicknesses, and thermal properties.

        Returns:
            SVG string for Construction objects, None for other types.
        """
        if self._type != "Construction":
            return None

        if self._document is None:
            # Need document to resolve material references
            return None

        try:
            from .visualization.svg import construction_to_svg

            return construction_to_svg(self)
        except Exception:
            # Fail gracefully - fall back to text repr
            return None


_T = TypeVar("_T", bound=IDFObject)


class IDFCollection(Generic[_T]):
    """
    Indexed collection of IDFObjects with O(1) lookup by name.

    Provides list-like iteration and dict-like access by name.

    Examples:
        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
        Zone('Core_ZN')
        >>> zones = model["Zone"]
        >>> len(zones)
        2

        O(1) lookup by name:

        >>> zones["Perimeter_ZN_1"].name
        'Perimeter_ZN_1'
        >>> zones[0].name
        'Perimeter_ZN_1'

    Attributes:
        _type: The object type this collection holds
        _by_name: Dict mapping uppercase names to objects
        _items: Ordered list of objects
    """

    __slots__ = ("_by_name", "_items", "_type")

    _type: str
    _by_name: dict[str, _T]
    _items: list[_T]

    def __init__(self, obj_type: str) -> None:
        self._type = obj_type
        self._by_name: dict[str, _T] = {}
        self._items: list[_T] = []

    @property
    def obj_type(self) -> str:
        """The object type this collection holds."""
        return self._type

    @property
    def by_name(self) -> dict[str, _T]:
        """Dict mapping uppercase names to objects."""
        return self._by_name

    def add(self, obj: _T) -> _T:
        """
        Add an object to the collection.

        Args:
            obj: The IDFObject to add

        Returns:
            The added object

        Raises:
            DuplicateObjectError: If an object with the same name exists
        """
        from .exceptions import DuplicateObjectError

        key = obj.name.upper() if obj.name else ""
        if key and key in self._by_name:
            raise DuplicateObjectError(self._type, obj.name)

        if key:
            self._by_name[key] = obj
        self._items.append(obj)
        return obj

    def remove(self, obj: _T) -> None:
        """Remove an object from the collection."""
        key = obj.name.upper() if obj.name else ""
        if key in self._by_name:
            del self._by_name[key]
        if obj in self._items:
            self._items.remove(obj)

    def __getitem__(self, key: str | int) -> _T:
        """Get object by name or index."""
        if isinstance(key, int):
            return self._items[key]
        if not key:
            # Unnamed/singleton objects are not indexed in _by_name;
            # fall back to the first item in the ordered list.
            if self._items:
                return self._items[0]
            raise KeyError(f"No {self._type} with name '{key}'")  # noqa: TRY003
        result = self._by_name.get(key.upper())
        if result is None:
            raise KeyError(f"No {self._type} with name '{key}'")  # noqa: TRY003
        return result

    def __iter__(self) -> Iterator[_T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: str | _T) -> bool:
        if isinstance(key, IDFObject):
            return key in self._items
        if not key:
            # Unnamed/singleton objects: check if any items exist
            return len(self._items) > 0
        return key.upper() in self._by_name

    def __bool__(self) -> bool:
        return len(self._items) > 0

    def __repr__(self) -> str:
        return f"IDFCollection({self._type}, count={len(self._items)})"

    def get(self, name: str, default: _T | None = None) -> _T | None:
        """Get object by name with default.

        For unnamed/singleton object types (e.g. SimulationControl), pass an
        empty string to retrieve the first object in the collection.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model["Zone"].get("Perimeter_ZN_1").name
            'Perimeter_ZN_1'
            >>> model["Zone"].get("NonExistent") is None
            True
            >>> model["SimulationControl"].get("") is not None
            True
        """
        if not name:
            return self._items[0] if self._items else default
        return self._by_name.get(name.upper(), default)

    def first(self) -> _T | None:
        """Get the first object or None.

        Examples:
            Quickly grab a singleton like Building or SimulationControl:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
            Zone('Core_ZN')
            >>> model["Zone"].first().name
            'Core_ZN'
            >>> model["Material"].first() is None
            True
        """
        return self._items[0] if self._items else None

    def to_list(self) -> list[_T]:
        """Convert to list.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
            Zone('Core_ZN')
            >>> [z.name for z in model["Zone"].to_list()]
            ['Perimeter_ZN_1', 'Core_ZN']
        """
        return list(self._items)

    def to_dict(self) -> list[dict[str, Any]]:
        """Convert all objects to list of dicts (eppy compatibility).

        Useful for feeding zone/material data into pandas or other
        analysis tools.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1", x_origin=0.0)  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> dicts = model["Zone"].to_dict()
            >>> dicts[0]["name"]
            'Perimeter_ZN_1'
        """
        return [obj.to_dict() for obj in self._items]

    def filter(self, predicate: Callable[[_T], bool]) -> list[_T]:
        """Filter objects by predicate function.

        Examples:
            Find zones on upper floors of a multi-story building:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Ground_Office", z_origin=0.0)  # doctest: +ELLIPSIS
            Zone('Ground_Office')
            >>> model.add("Zone", "Floor2_Office", z_origin=3.5)  # doctest: +ELLIPSIS
            Zone('Floor2_Office')
            >>> upper = model["Zone"].filter(lambda z: (z.z_origin or 0) > 0)
            >>> [z.name for z in upper]
            ['Floor2_Office']
        """
        return [obj for obj in self._items if predicate(obj)]
