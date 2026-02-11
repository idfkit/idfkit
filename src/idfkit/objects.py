"""
Core object classes for IDF representation.

IDFObject: Thin wrapper around a dict with attribute access.
IDFCollection: Indexed collection of IDFObjects with O(1) lookup.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .document import IDFDocument

# Field name conversion patterns
_FIELD_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9]+")


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


class IDFObject:
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

    __slots__ = ("_data", "_document", "_field_order", "_name", "_ref_fields", "_schema", "_type", "_version")

    _type: str
    _name: str
    _data: dict[str, Any]
    _schema: dict[str, Any] | None
    _document: IDFDocument | None
    _field_order: list[str] | None
    _ref_fields: frozenset[str] | None

    def __init__(
        self,
        obj_type: str,
        name: str,
        data: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        document: IDFDocument | None = None,
        field_order: list[str] | None = None,
        ref_fields: frozenset[str] | None = None,
    ) -> None:
        object.__setattr__(self, "_type", obj_type)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_data", data if data is not None else {})
        object.__setattr__(self, "_schema", schema)
        object.__setattr__(self, "_document", document)
        object.__setattr__(self, "_field_order", field_order)
        object.__setattr__(self, "_ref_fields", ref_fields)
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
    def field_order(self) -> list[str] | None:
        """Ordered list of field names from schema."""
        return self._field_order

    @property
    def name(self) -> str:
        """The object's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the object's name."""
        self._set_name(value)

    @property
    def key(self) -> str:
        """The object type (alias for eppy compatibility)."""
        return self._type

    @property
    def Name(self) -> str:
        """The object's name (eppy compatibility - capitalized)."""
        return self._name

    @Name.setter
    def Name(self, value: str) -> None:
        """Set the object's name (eppy compatibility)."""
        self._set_name(value)

    @property
    def fieldnames(self) -> list[str]:
        """List of field names (eppy compatibility)."""
        if self._field_order:
            return ["Name", *list(self._field_order)]
        return ["Name", *list(self._data.keys())]

    @property
    def fieldvalues(self) -> list[Any]:
        """List of field values in order (eppy compatibility)."""
        if self._field_order:
            return [self._name] + [self._data.get(f) for f in self._field_order]
        return [self._name, *list(self._data.values())]

    @property
    def theidf(self) -> IDFDocument | None:
        """Reference to parent document (eppy compatibility)."""
        return self._document

    def __getattr__(self, key: str) -> Any:
        """Get field value by attribute name."""
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

        # Field not found - return None (eppy behavior)
        return None

    def __setattr__(self, key: str, value: Any) -> None:
        """Set field value by attribute name."""
        if key.startswith("_"):
            object.__setattr__(self, key, value)
        elif key.lower() == "name":
            self._set_name(value)
        else:
            # Normalize key to python style
            python_key = to_python_name(key)
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
        doc = self._document
        if doc is not None:
            doc.notify_name_change(self, old, value)

    def _set_field(self, python_key: str, value: Any) -> None:
        """Centralized data-field write with reference graph notification."""
        doc = self._document
        ref_fields = self._ref_fields
        if doc is not None and ref_fields is not None and python_key in ref_fields:
            old = self._data.get(python_key)
            self._data[python_key] = value
            if old != value:
                doc.notify_reference_change(self, python_key, old, value)
        else:
            self._data[python_key] = value
        object.__setattr__(self, "_version", self._version + 1)

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

    # -----------------------------------------------------------------
    # eppy compatibility: cross-referencing
    # -----------------------------------------------------------------

    def get_referenced_object(self, field_name: str) -> IDFObject | None:
        """Follow a reference field and return the referenced object.

        Given a field that contains the *name* of another object (e.g.
        ``construction_name``), look up and return the actual
        :class:`IDFObject` that it points to.

        This mirrors ``epbunch.get_referenced_object(fieldname)`` in eppy.

        Args:
            field_name: The field whose value is the name of the target
                object (e.g. ``"zone_name"``, ``"construction_name"``).

        Returns:
            The referenced :class:`IDFObject`, or ``None`` if the field is
            empty, the document is not attached, or the target cannot be
            found.

        Examples:
            Follow a surface's ``zone_name`` reference to retrieve the
            Zone object it belongs to:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="",
            ...     zone_name="Perimeter_ZN_1",
            ...     outside_boundary_condition="Outdoors",
            ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
            ...     validate=False)
            >>> zone = wall.get_referenced_object("zone_name")
            >>> zone.name
            'Perimeter_ZN_1'
        """
        doc = self._document
        if doc is None:
            return None

        # Resolve the field value
        value = getattr(self, field_name)
        if not value or not isinstance(value, str):
            return None

        # Use schema to find which object types could provide this name
        schema = doc.schema
        if schema is not None:
            python_key = to_python_name(field_name)
            object_lists = schema.get_field_object_list(self._type, python_key)
            if object_lists:
                for obj_list in object_lists:
                    provider_types = schema.get_types_providing_reference(obj_list)
                    for ptype in provider_types:
                        found = doc.getobject(ptype, value)
                        if found is not None:
                            return found

        # Fallback: scan all collections for an object with this name
        for collection in doc.collections.values():
            result = collection.get(value)
            if result is not None:
                return result

        return None

    def getreferingobjs(
        self,
        iddgroups: list[str] | None = None,
        fields: list[str] | None = None,
    ) -> list[IDFObject]:
        """Find all objects that reference this object by name.

        This mirrors ``epbunch.getreferingobjs()`` in eppy.

        Args:
            iddgroups: Optional list of IDD group names to restrict the
                search to (e.g. ``["Thermal Zones and Surfaces"]``).
            fields: Optional list of field names to restrict the search to.

        Returns:
            List of :class:`IDFObject` instances that reference this
            object's name.
        """
        doc = self._document
        if doc is None or not self._name:
            return []

        refs_with_fields = doc.references.get_referencing_with_fields(self._name)
        if not refs_with_fields:
            return []

        group_filter = self._build_group_filter(iddgroups)
        normalized_fields = {to_python_name(f) for f in fields} if fields is not None else None

        results: list[IDFObject] = []
        seen: set[int] = set()
        for obj, field_name in refs_with_fields:
            obj_id = id(obj)
            if obj_id in seen:
                continue
            if normalized_fields is not None and to_python_name(field_name) not in normalized_fields:
                continue
            if group_filter is not None and obj.obj_type not in group_filter:
                continue
            seen.add(obj_id)
            results.append(obj)

        return results

    def _build_group_filter(self, iddgroups: list[str] | None) -> set[str] | None:
        """Build a set of object types belonging to the given IDD groups."""
        doc = self._document
        if iddgroups is None or doc is None or doc.schema is None:
            return None
        result: set[str] = set()
        for obj_type in doc.schema.object_types:
            grp = doc.schema.get_group(obj_type)
            if grp and grp in iddgroups:
                result.add(obj_type)
        return result

    def get_referring_objects(
        self,
        iddgroups: list[str] | None = None,
        fields: list[str] | None = None,
    ) -> list[IDFObject]:
        """Properly-spelled alias for :meth:`getreferingobjs`."""
        return self.getreferingobjs(iddgroups=iddgroups, fields=fields)

    # -----------------------------------------------------------------
    # eppy compatibility: range checking
    # -----------------------------------------------------------------

    def getrange(self, field_name: str) -> dict[str, Any]:
        """Return the valid range constraints for *field_name* from the schema.

        Mirrors ``epbunch.getrange(fieldname)`` in eppy.

        Returns a dict which may contain keys ``minimum``,
        ``exclusiveMinimum``, ``maximum``, ``exclusiveMaximum``, and
        ``type``.

        Examples:
            Check valid thickness bounds before setting a new value:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Insulation_Board",
            ...     roughness="MediumRough", thickness=0.05,
            ...     conductivity=0.04, density=30.0, specific_heat=1500.0)
            >>> rng = mat.getrange("thickness")
            >>> rng["exclusiveMinimum"]
            0.0
        """
        result: dict[str, Any] = {}
        field_idd = self.get_field_idd(to_python_name(field_name))
        if not field_idd:
            return result

        for key in ("minimum", "exclusiveMinimum", "maximum", "exclusiveMaximum", "type"):
            if key in field_idd:
                result[key] = field_idd[key]

        # Also check inside anyOf
        if "anyOf" in field_idd:
            for sub in field_idd["anyOf"]:
                for key in ("minimum", "exclusiveMinimum", "maximum", "exclusiveMaximum"):
                    if key in sub and key not in result:
                        result[key] = sub[key]

        return result

    def checkrange(self, field_name: str) -> bool:
        """Validate that the current value of *field_name* is within range.

        Mirrors ``epbunch.checkrange(fieldname)`` in eppy.

        Returns:
            ``True`` if the value is within the valid range.

        Raises:
            RangeError: If the value is outside the valid range.

        Examples:
            Verify a material's thickness is within EnergyPlus limits:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> mat.checkrange("thickness")
            True
        """
        from .exceptions import RangeError

        value = getattr(self, field_name)
        if value is None or not isinstance(value, (int, float)):
            return True

        constraints = self.getrange(field_name)
        if not constraints:
            return True

        if "minimum" in constraints and value < constraints["minimum"]:
            msg = f"Value {value} for '{field_name}' is below minimum {constraints['minimum']}"
            raise RangeError(self._type, self._name, field_name, msg)

        if "exclusiveMinimum" in constraints and value <= constraints["exclusiveMinimum"]:
            msg = f"Value {value} for '{field_name}' must be > {constraints['exclusiveMinimum']}"
            raise RangeError(self._type, self._name, field_name, msg)

        if "maximum" in constraints and value > constraints["maximum"]:
            msg = f"Value {value} for '{field_name}' is above maximum {constraints['maximum']}"
            raise RangeError(self._type, self._name, field_name, msg)

        if "exclusiveMaximum" in constraints and value >= constraints["exclusiveMaximum"]:
            msg = f"Value {value} for '{field_name}' must be < {constraints['exclusiveMaximum']}"
            raise RangeError(self._type, self._name, field_name, msg)

        return True

    # -----------------------------------------------------------------
    # Schema introspection
    # -----------------------------------------------------------------

    def get_field_idd(self, field_name: str) -> dict[str, Any] | None:
        """Get IDD/schema info for a field (eppy compatibility)."""
        if not self._schema:
            return None
        pattern_props: dict[str, Any] = self._schema.get("patternProperties", {})
        # The pattern key varies (e.g. ".*", "^.*\\S.*$") - get the first one
        default: dict[str, Any] = {}
        inner: dict[str, Any] = next(iter(pattern_props.values()), default) if pattern_props else default
        return inner.get("properties", {}).get(to_python_name(field_name))

    def getfieldidd(self, field_name: str) -> dict[str, Any] | None:
        """Alias for get_field_idd (eppy compatibility)."""
        return self.get_field_idd(field_name)

    def getfieldidd_item(self, field_name: str, item: str) -> Any:
        """Get specific item from field IDD info (eppy compatibility)."""
        field_idd = self.get_field_idd(field_name)
        if field_idd:
            return field_idd.get(item)
        return None

    def copy(self) -> IDFObject:
        """Create a copy of this object."""
        return IDFObject(
            obj_type=self._type,
            name=self._name,
            data=dict(self._data),
            schema=self._schema,
            document=None,  # Don't copy document reference
            field_order=self._field_order,
            ref_fields=self._ref_fields,
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


class IDFCollection:
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
    _by_name: dict[str, IDFObject]
    _items: list[IDFObject]

    def __init__(self, obj_type: str) -> None:
        self._type = obj_type
        self._by_name: dict[str, IDFObject] = {}
        self._items: list[IDFObject] = []

    @property
    def obj_type(self) -> str:
        """The object type this collection holds."""
        return self._type

    @property
    def by_name(self) -> dict[str, IDFObject]:
        """Dict mapping uppercase names to objects."""
        return self._by_name

    def add(self, obj: IDFObject) -> IDFObject:
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

    def remove(self, obj: IDFObject) -> None:
        """Remove an object from the collection."""
        key = obj.name.upper() if obj.name else ""
        if key in self._by_name:
            del self._by_name[key]
        if obj in self._items:
            self._items.remove(obj)

    def __getitem__(self, key: str | int) -> IDFObject:
        """Get object by name or index."""
        if isinstance(key, int):
            return self._items[key]
        result = self._by_name.get(key.upper())
        if result is None:
            raise KeyError(f"No {self._type} with name '{key}'")  # noqa: TRY003
        return result

    def __iter__(self) -> Iterator[IDFObject]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: str | IDFObject) -> bool:
        if isinstance(key, IDFObject):
            return key in self._items
        return key.upper() in self._by_name

    def __bool__(self) -> bool:
        return len(self._items) > 0

    def __repr__(self) -> str:
        return f"IDFCollection({self._type}, count={len(self._items)})"

    def get(self, name: str, default: IDFObject | None = None) -> IDFObject | None:
        """Get object by name with default.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model["Zone"].get("Perimeter_ZN_1").name
            'Perimeter_ZN_1'
            >>> model["Zone"].get("NonExistent") is None
            True
        """
        return self._by_name.get(name.upper(), default)

    def first(self) -> IDFObject | None:
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

    def to_list(self) -> list[IDFObject]:
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

    def filter(self, predicate: Callable[[IDFObject], bool]) -> list[IDFObject]:
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
