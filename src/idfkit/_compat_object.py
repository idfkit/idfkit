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

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .document import IDFDocument
    from .objects import IDFObject


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
        _document: IDFDocument | None
        _field_order: list[str] | None

        def _set_name(self, value: str) -> None: ...

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

    @property
    def fieldnames(self) -> list[str]:
        """List of field names (eppy compatibility).

        !!! tip
            Prefer ``list(obj.data.keys())`` for new code.
        """
        if self._field_order:
            return ["Name", *list(self._field_order)]
        return ["Name", *list(self._data.keys())]

    @property
    def fieldvalues(self) -> list[Any]:
        """List of field values in order (eppy compatibility).

        !!! tip
            Prefer ``list(obj.data.values())`` for new code.
        """
        if self._field_order:
            return [self._name] + [self._data.get(f) for f in self._field_order]
        return [self._name, *list(self._data.values())]

    @property
    def theidf(self) -> IDFDocument | None:
        """Reference to parent document (eppy compatibility).

        !!! tip
            Prefer ``obj._document`` for new code.
        """
        return self._document

    # -- Schema introspection ------------------------------------------------

    def get_field_idd(self, field_name: str) -> dict[str, Any] | None:
        """Get IDD/schema info for a field (eppy compatibility)."""
        from .objects import to_python_name

        if not self._schema:
            return None
        pattern_props: dict[str, Any] = self._schema.get("patternProperties", {})
        default: dict[str, Any] = {}
        inner: dict[str, Any] = next(iter(pattern_props.values()), default) if pattern_props else default
        return inner.get("properties", {}).get(to_python_name(field_name))

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
        from .objects import to_python_name

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
        from .objects import to_python_name

        doc = self._document
        if doc is None:
            return None

        python_key = to_python_name(field_name)
        ref_name = getattr(self, python_key)
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
            fields_python = [to_python_name(f) for f in fields]
            filtered = []
            for obj in result:
                for fld in fields_python:
                    value = obj.data.get(fld, "")
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
