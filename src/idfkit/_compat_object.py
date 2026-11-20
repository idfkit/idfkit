"""Eppy-compatibility helpers for [IDFObject][idfkit.objects.IDFObject].

This module contains properties and methods that exist **solely** to
ease migration from `eppy <https://github.com/santoshphilip/eppy>`_.
For each item there is a recommended idfkit alternative noted in the
docstring.

The mixin is mixed into [IDFObject][idfkit.objects.IDFObject] so that existing eppy code
continues to work.  In a future release the mixin may be deprecated and
eventually removed.

To opt out early, avoid importing or calling any symbol from this module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, cast

from ._eppy_names import eppy_field_name, group_number_position, idd_field_names, numbered_idd_name
from ._surface_types import VERTEX_SURFACE_TYPES

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .document import AnyIDFDocument, IDFDocument
    from .objects import IDFObject


#: eppy's geometry attributes of a surface, read through [idfkit.geometry][] on a surface with vertices.
EPPY_SURFACE_ATTRIBUTES: Final = frozenset({"area", "azimuth", "tilt", "height", "width", "coords"})

#: Types whose objects read eppy's geometry attributes: every surface type with vertices.
_EPPY_GEOMETRY_TYPES: Final = (*VERTEX_SURFACE_TYPES, "Wall:Detailed", "RoofCeiling:Detailed", "Floor:Detailed")

_SURFACE_REPLACEMENTS: Final = {
    "area": "idfkit.geometry.calculate_surface_area(surface), or calculate_zone_floor_area(doc, zone) for a zone",
    "azimuth": "idfkit.geometry.calculate_surface_azimuth(surface)",
    "tilt": "idfkit.geometry.calculate_surface_tilt(surface)",
    "coords": "idfkit.geometry.get_surface_coords(surface).as_tuple_list()",
    "true_azimuth": (
        "idfkit.geometry.calculate_surface_azimuth(surface), adding the zone's direction_of_relative_north "
        "and the Building's north_axis, or translate_to_world(doc) first"
    ),
}

#: eppy attributes idfkit has no counterpart of by that name, to the idfkit way.
_EPPY_ATTRIBUTE_HINTS: Final = {
    "obj": "'obj' is eppy's raw field list; read obj.fieldvalues (eppy's layout) or obj.data, and set fields by name.",
    "objidd": "'objidd' is eppy's IDD field list; use obj.get_field_idd(field) or obj.schema_dict.",
}


class EppyObjectMixin:
    """Eppy-compatibility properties and methods for [IDFObject][idfkit.objects.IDFObject].

    Mixed into [IDFObject][idfkit.objects.IDFObject] automatically.  Each item documents
    the preferred idfkit API in a tip admonition.
    """

    __slots__ = ()

    # -- TYPE_CHECKING interface (attributes provided by IDFObject) ----------
    if TYPE_CHECKING:
        _type: str
        _name: str
        _data: dict[str, Any]
        _schema: dict[str, Any] | None
        _document: AnyIDFDocument | None
        _field_order: list[str] | None
        _wrapper_key: str | None
        _ext_inner_names: tuple[str, ...]

        def _set_name(self, value: str) -> None: ...
        def _field_key(self, key: str) -> str: ...
        def get(self, key: str, default: Any = None) -> Any: ...

    # -- Properties ----------------------------------------------------------

    @property
    def key(self) -> str:
        """The object type (eppy compatibility).

        !!! tip
            Prefer [obj_type][] for new code.
        """
        return self._type

    @property
    def Name(self) -> str:
        """The object's name (eppy compatibility — capitalised).

        !!! tip
            Prefer [name][] for new code.
        """
        return self._name

    @Name.setter
    def Name(self, value: str) -> None:
        """Set the object's name (eppy compatibility)."""
        self._set_name(value)

    def _eppy_layout(self) -> tuple[list[str], list[Any]]:
        """eppy's field names and values: the key, the name, the fixed fields, then each group's fields."""
        legacy_raw: Any = (self._schema or {}).get("legacy_idd")
        legacy = cast("dict[str, Any] | None", legacy_raw if isinstance(legacy_raw, dict) else None)
        legacy_fields = list(cast("list[str]", legacy.get("fields", ()))) if legacy is not None else []
        has_name = legacy_fields[:1] == ["name"] if legacy is not None else True
        fixed = self._field_order if self._field_order is not None else legacy_fields[1 if has_name else 0 :]
        if not legacy_fields and self._field_order is None:
            fixed = list(self._data.keys())
        idd_names = idd_field_names(self._schema)

        def label(key: str, group: int = 0) -> str:
            idd = idd_names.get(key) or " ".join(word.capitalize() for word in key.split("_"))
            spelled = eppy_field_name(
                numbered_idd_name(idd, group, group_number_position(self._type, key)) if group else idd
            )
            # ``Name`` is the object's name; a nameless type's IDD ``Name`` field (``name_``) keeps its key.
            return key if spelled == "Name" else spelled

        names: list[str] = ["key"]
        values: list[Any] = [self._type]
        if has_name:
            names.append("Name")
            values.append(self._name)
        wrapper_key = self._wrapper_key
        for key in fixed:
            if key == "name" or key == wrapper_key:
                continue
            names.append(label(key))
            values.append(self._data.get(key))

        if wrapper_key is not None:
            inner = cast("list[str]", legacy.get("extensibles", ())) if legacy is not None else []
            inner_names = tuple(inner) or self._ext_inner_names
            groups_raw: Any = self._data.get(wrapper_key)
            groups = cast("list[dict[str, Any]]", groups_raw) if isinstance(groups_raw, list) else []
            for index in range(max(len(groups), 1)):
                group = groups[index] if index < len(groups) else {}
                for key in inner_names:
                    names.append(label(key, index + 1))
                    values.append(group.get(key))

        # Trailing blanks are trimmed, as in an IDF file: never the key or the name.
        while len(values) > (2 if has_name else 1) and values[-1] in (None, ""):
            values.pop()
        return names, values

    @property
    def fieldnames(self) -> list[str]:
        """Field names in eppy's layout (eppy compatibility).

        ``["key", "Name", <fixed fields>, <extensible fields, group by group>]``, each spelled as eppy
        spells it, from the IDD name with punctuation dropped: ``"Outside_Layer"``,
        ``"Vertex_1_Xcoordinate"``. A type without a Name field has no ``"Name"`` entry. Every
        fixed field is listed, and the fields of each extensible group present (of one group when
        there are none). Group fields carry their number where the IDD puts it (``"Field_3"``,
        ``"Branch_2_Name"``, ``"Value_Until_Time_1"``). Every name is accepted by attribute and item
        access and by ``obj.get(name)``, which reads the value ``zip(obj.fieldnames, obj.fieldvalues)``
        pairs it with. ``obj[name]`` reads the same value, except that it raises
        [MissingRequiredFieldError][idfkit.exceptions.MissingRequiredFieldError] for a blank
        required field, which ``fieldvalues`` and ``obj.get(name)`` read as ``None``.

        !!! tip
            Prefer ``obj.field_order`` (the snake_case keys) and the extensible wrapper
            (``obj.vertices``) for new code.
        """
        return self._eppy_layout()[0]

    @property
    def fieldvalues(self) -> list[Any]:
        """Field values in eppy's layout (eppy compatibility).

        ``fieldvalues[0]`` is the object type (``obj.key``), ``fieldvalues[1]`` the name for a type
        with a Name field, then the fixed fields in IDD order and the extensible groups flattened
        after them, so ``construction.fieldvalues[2:]`` lists the layers and a
        ``Schedule:Compact``'s ``fieldvalues[3:]`` lists its fields. A blank field reads ``None``,
        as ``obj.get(name)`` does (attribute access raises
        [MissingRequiredFieldError][idfkit.exceptions.MissingRequiredFieldError] for a blank required
        field instead), and trailing blanks are trimmed as in an IDF file. The list is a copy:
        changing it does not change the object.

        !!! tip
            Prefer ``obj.data`` and the extensible wrapper (``obj.vertices``) for new code.
        """
        return self._eppy_layout()[1]

    @property
    def theidf(self) -> IDFDocument | None:
        """Reference to parent document (eppy compatibility).

        !!! tip
            Prefer ``obj._document`` for new code.
        """
        # Typed for the latest release, as every document is unless its caller names a version.
        return cast("IDFDocument | None", self._document)

    # -- Surface geometry (eppy's surface functions) ---------------------------

    def _eppy_surface_attr(self, name: str) -> tuple[bool, Any]:
        """eppy's surface geometry attribute *name* of a surface with vertices, as ``(found, value)``.

        eppy gives every surface ``area``, ``azimuth``, ``tilt``, ``height``, ``width`` and ``coords``.
        They are not properties here, so that they can never hide a field of the same name on another
        type (``Window.height``): ``IDFObject.__getattr__`` asks for them only once *name* is not a
        field. A surface with fewer than three vertices reads ``0.0``, and ``[]`` for ``coords``, as
        the [idfkit.geometry][] functions do.

        !!! tip
            Prefer [calculate_surface_area][idfkit.geometry.calculate_surface_area],
            [calculate_surface_azimuth][idfkit.geometry.calculate_surface_azimuth],
            [calculate_surface_tilt][idfkit.geometry.calculate_surface_tilt] and
            [get_surface_coords][idfkit.geometry.get_surface_coords] for new code.
        """
        if name not in EPPY_SURFACE_ATTRIBUTES or self._type not in _EPPY_GEOMETRY_TYPES:
            return False, None
        from .geometry import get_surface_coords

        poly = get_surface_coords(cast("IDFObject", self))
        if name == "coords":
            return True, poly.as_tuple_list() if poly is not None else []
        if poly is None:
            return True, 0.0
        if name == "area":
            return True, poly.area
        if name == "azimuth":
            return True, poly.azimuth
        if name == "tilt":
            return True, poly.tilt
        # eppy's height and width: of the edges at the first vertex, the steeper is the height and
        # the flatter the width; with equal rises, the longer is the width.
        first, after, before = poly.vertices[0], poly.vertices[1], poly.vertices[-1]
        rise_before, rise_after = abs(before.z - first.z), abs(after.z - first.z)
        to_before, to_after = (before - first).length(), (after - first).length()
        if rise_before == rise_after:
            return True, (min if name == "height" else max)(to_before, to_after)
        before_is_steeper = rise_before > rise_after
        return True, to_before if before_is_steeper == (name == "height") else to_after

    def _eppy_attribute_hint(self, name: str) -> str | None:
        """Where an eppy-only attribute *name* lives in idfkit, for the error that refuses it."""
        if name in EPPY_SURFACE_ATTRIBUTES or name == "true_azimuth":
            replacement = _SURFACE_REPLACEMENTS.get(name, "idfkit.geometry.get_surface_coords(surface)")
            if self._type in _EPPY_GEOMETRY_TYPES:
                # true_azimuth: this surface reads area, azimuth, ... but not this one.
                return f"'{name}' is an eppy surface attribute idfkit does not provide. Use {replacement}."
            return (
                f"'{name}' is eppy's surface geometry attribute; {self._type} has no vertices to read it "
                f"from. Use {replacement}."
            )
        return _EPPY_ATTRIBUTE_HINTS.get(name)

    # -- Schema introspection ------------------------------------------------

    def get_field_idd(self, field_name: str) -> dict[str, Any] | None:
        """Get IDD/schema info for a field (eppy compatibility)."""
        if not self._schema:
            return None
        pattern_props: dict[str, Any] = self._schema.get("patternProperties", {})
        default: dict[str, Any] = {}
        inner: dict[str, Any] = next(iter(pattern_props.values()), default) if pattern_props else default
        return inner.get("properties", {}).get(self._field_key(field_name))

    def getfieldidd(self, field_name: str) -> dict[str, Any] | None:
        """Alias for [get_field_idd][] (eppy compatibility).

        !!! tip
            Prefer [get_field_idd][] for new code.
        """
        return self.get_field_idd(field_name)

    def getfieldidd_item(self, field_name: str, item: str) -> Any:
        """Get specific item from field IDD info (eppy compatibility).

        !!! tip
            Use ``obj.get_field_idd(name).get(item)`` for new code.
        """
        field_idd = self.get_field_idd(field_name)
        if field_idd:
            return field_idd.get(item)
        return None

    # -- Range checking ------------------------------------------------------

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
        field_idd = self.get_field_idd(field_name)
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

        value = self.get(field_name)  # None for an unset field, required or not
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

    # -- Reference navigation ------------------------------------------------

    def get_referenced_object(self, field_name: str) -> IDFObject | None:
        """Follow a reference field to the referenced object (eppy compatibility).

        Given a field that contains an object name (e.g. ``zone_name``),
        resolve and return the referenced object.

        Args:
            field_name: The reference field to follow.

        Returns:
            The referenced IDFObject, or ``None`` if not found.

        Examples:
            Follow a surface -> construction reference:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Material", "Concrete",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)  # doctest: +ELLIPSIS
            Material('Concrete')
            >>> model.add("Construction", "Ext_Wall",
            ...     outside_layer="Concrete", validate=False)  # doctest: +ELLIPSIS
            Construction('Ext_Wall')
            >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="Ext_Wall",
            ...     zone_name="", outside_boundary_condition="Outdoors",
            ...     validate=False)
            >>> wall.get_referenced_object("construction_name").name
            'Ext_Wall'
        """
        doc = self._document
        if doc is None:
            return None

        python_key = self._field_key(field_name)
        ref_name = getattr(self, python_key, None)
        if not ref_name or not isinstance(ref_name, str):
            return None

        # Try schema-based resolution
        schema = doc.schema
        if schema is not None:
            object_lists = schema.get_field_object_list(self._type, python_key)
            if object_lists:
                for obj_list in object_lists:
                    types = schema.get_types_providing_reference(obj_list)
                    for otype in types:
                        result = doc.getobject(otype, ref_name)
                        if result is not None:
                            return result

        # Fallback: scan all collections
        for collection in doc.collections.values():
            result = collection.get(ref_name)
            if result is not None:
                return result

        return None

    def getreferingobjs(  # noqa: C901
        self,
        iddgroups: list[str] | None = None,
        fields: list[str] | None = None,
    ) -> list[IDFObject]:
        """Find all objects that reference this object by name (eppy compatibility).

        !!! tip
            Prefer [get_referring_objects][] (correct spelling) for
            new code, or [IDFDocument.get_referencing][] for
            document-level queries.

        Args:
            iddgroups: Optional list of IDD group names to restrict the
                search to (e.g. ``["Thermal Zones and Surfaces"]``).
            fields: Optional list of field names to restrict the search
                to (e.g. ``["zone_name"]``).

        Returns:
            List of IDFObjects that reference this object's name.
        """
        from .objects import to_python_name

        doc = self._document
        if doc is None:
            return []
        name = self._name
        if not name:
            return []

        referencing = doc.get_referencing(name)
        if not referencing:
            return []

        result: list[IDFObject] = list(referencing)

        if iddgroups is not None and doc.schema is not None:
            iddgroups_upper = [g.upper() for g in iddgroups]
            filtered: list[IDFObject] = []
            for obj in result:
                group = doc.schema.get_group(obj.obj_type)
                if group and group.upper() in iddgroups_upper:
                    filtered.append(obj)
            result = filtered

        if fields is not None:
            # Each referencing type's trailing-underscore spellings (cond_flag_..._conditioned_).
            schema = doc.schema
            filtered = []
            for obj in result:
                pc = schema.get_parsing_cache(obj.obj_type) if schema is not None else None
                aliases: Mapping[str, str] = pc.field_aliases if pc is not None else {}
                for fld in fields:
                    python_fld = to_python_name(fld)
                    value = obj.data.get(aliases.get(fld) or aliases.get(python_fld, python_fld), "")
                    if isinstance(value, str) and value.upper() == name.upper():
                        filtered.append(obj)
                        break
            result = filtered

        return result

    def get_referring_objects(
        self,
        iddgroups: list[str] | None = None,
        fields: list[str] | None = None,
    ) -> list[IDFObject]:
        """Find all objects that reference this object (corrected spelling).

        Equivalent to [getreferingobjs][] with a corrected name.
        See that method for full documentation.
        """
        return self.getreferingobjs(iddgroups=iddgroups, fields=fields)
