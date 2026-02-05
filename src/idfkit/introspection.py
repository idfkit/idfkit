"""
Introspection utilities for discovering EnergyPlus object fields.

Provides detailed information about object types and their fields
for improved user experience in REPLs and Jupyter notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .schema import EpJSONSchema


@dataclass
class FieldDescription:
    """Description of a single field in an EnergyPlus object type.

    Attributes:
        name: Field name (python-style, e.g., "x_origin")
        field_type: Type of the field ("number", "string", "integer", etc.)
        required: Whether the field is required
        default: Default value, if any
        units: Units string, if any (e.g., "m", "W/m-K")
        enum_values: List of allowed values for enum fields
        minimum: Minimum value for numeric fields
        maximum: Maximum value for numeric fields
        exclusive_minimum: Exclusive minimum for numeric fields
        exclusive_maximum: Exclusive maximum for numeric fields
        note: Field documentation/note
        is_reference: Whether this field references another object
        object_list: Reference list names if this is a reference field
    """

    name: str
    field_type: str | None = None
    required: bool = False
    default: Any = None
    units: str | None = None
    enum_values: list[str] | None = None
    minimum: float | None = None
    maximum: float | None = None
    exclusive_minimum: float | None = None
    exclusive_maximum: float | None = None
    note: str | None = None
    is_reference: bool = False
    object_list: list[str] | None = None

    def __str__(self) -> str:
        """Return a formatted string representation of the field."""
        parts: list[str] = [f"  {self.name}"]
        self._append_type_info(parts)
        self._append_constraints(parts)
        if self.is_reference:
            parts.append(" (reference)")
        return "".join(parts)

    def _append_type_info(self, parts: list[str]) -> None:
        """Append type, units, and enum info to parts list."""
        if self.required:
            parts.append(" [REQUIRED]")
        if self.field_type:
            parts.append(f" ({self.field_type})")
        if self.units:
            parts.append(f" [{self.units}]")
        if self.enum_values:
            if len(self.enum_values) <= 4:
                parts.append(f" choices={self.enum_values}")
            else:
                shown = self.enum_values[:3]
                parts.append(f" choices={shown}+{len(self.enum_values) - 3} more")

    def _append_constraints(self, parts: list[str]) -> None:
        """Append default and range constraints to parts list."""
        if self.default is not None:
            parts.append(f" default={self.default}")
        if self.minimum is not None:
            parts.append(f" min={self.minimum}")
        if self.exclusive_minimum is not None:
            parts.append(f" min>{self.exclusive_minimum}")
        if self.maximum is not None:
            parts.append(f" max={self.maximum}")
        if self.exclusive_maximum is not None:
            parts.append(f" max<{self.exclusive_maximum}")


@dataclass
class ObjectDescription:
    """Description of an EnergyPlus object type.

    Attributes:
        obj_type: Object type name (e.g., "Zone", "Material")
        memo: Object description/memo from schema
        fields: List of field descriptions
        required_fields: List of required field names
        has_name: Whether this object type has a name field
        is_extensible: Whether this object has extensible fields
        extensible_size: Size of extensible groups, if any
    """

    obj_type: str
    memo: str | None = None
    fields: list[FieldDescription] = field(default_factory=lambda: [])
    required_fields: list[str] = field(default_factory=lambda: [])
    has_name: bool = True
    is_extensible: bool = False
    extensible_size: int | None = None

    def __str__(self) -> str:
        """Return a formatted string representation for terminal output."""
        lines: list[str] = [f"=== {self.obj_type} ==="]

        if self.memo:
            lines.append(self.memo)
            lines.append("")

        if self.required_fields:
            lines.append(f"Required fields: {', '.join(self.required_fields)}")
            lines.append("")

        lines.append(f"Fields ({len(self.fields)}):")
        for f in self.fields:
            lines.append(str(f))

        if self.is_extensible:
            lines.append("")
            lines.append(f"(Extensible object - groups of {self.extensible_size})")

        return "\n".join(lines)

    def _repr_html_(self) -> str:
        """Return an HTML representation for Jupyter notebooks."""
        html_parts: list[str] = [f"<h3>{self.obj_type}</h3>"]

        if self.memo:
            html_parts.append(f"<p><em>{self.memo}</em></p>")

        if self.required_fields:
            html_parts.append(f"<p><strong>Required:</strong> {', '.join(self.required_fields)}</p>")

        html_parts.append("<table>")
        html_parts.append("<tr><th>Field</th><th>Type</th><th>Units</th><th>Default</th><th>Notes</th></tr>")

        for f in self.fields:
            required_marker = " <strong>*</strong>" if f.required else ""
            ftype = f.field_type or ""
            units = f.units or ""
            default = str(f.default) if f.default is not None else ""

            notes_parts: list[str] = []
            if f.enum_values:
                if len(f.enum_values) <= 4:
                    notes_parts.append(f"choices: {', '.join(f.enum_values)}")
                else:
                    notes_parts.append(f"choices: {', '.join(f.enum_values[:3])}... ({len(f.enum_values)} total)")
            if f.minimum is not None:
                notes_parts.append(f"min: {f.minimum}")
            if f.maximum is not None:
                notes_parts.append(f"max: {f.maximum}")
            if f.is_reference:
                notes_parts.append("reference")
            notes = "; ".join(notes_parts)

            html_parts.append(
                f"<tr><td>{f.name}{required_marker}</td><td>{ftype}</td>"
                f"<td>{units}</td><td>{default}</td><td>{notes}</td></tr>"
            )

        html_parts.append("</table>")

        if self.is_extensible:
            html_parts.append(f"<p><em>Extensible object (groups of {self.extensible_size})</em></p>")

        return "\n".join(html_parts)


def describe_object_type(schema: EpJSONSchema, obj_type: str) -> ObjectDescription:
    """Get a detailed description of an EnergyPlus object type.

    Args:
        schema: The EpJSON schema to query
        obj_type: Object type name (e.g., "Zone", "Material")

    Returns:
        ObjectDescription with detailed field information

    Raises:
        KeyError: If the object type is not found in the schema
    """
    obj_schema = schema.get_object_schema(obj_type)
    if not obj_schema:
        msg = f"Unknown object type: {obj_type}"
        raise KeyError(msg)

    inner_schema = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner_schema.get("properties", {}) if inner_schema else {}
    required_list: list[str] = inner_schema.get("required", []) if inner_schema else []
    required_set: set[str] = set(required_list)

    # Get ordered field names
    field_names: list[str] = schema.get_field_names(obj_type)
    if not field_names:
        # Fallback to properties keys if no legacy_idd
        field_names = list(properties.keys())

    fields: list[FieldDescription] = []
    for field_name in field_names:
        field_schema: dict[str, Any] = properties.get(field_name, {})

        # Determine field type
        field_type = _get_field_type(field_schema)

        # Get enum values
        enum_values: list[str] | None = field_schema.get("enum")
        if enum_values is None and "anyOf" in field_schema:
            any_of: list[dict[str, Any]] = field_schema["anyOf"]
            for sub in any_of:
                if "enum" in sub:
                    enum_values = sub["enum"]
                    break

        # Check if reference field
        object_list: list[str] | None = field_schema.get("object_list")
        is_reference = object_list is not None

        fields.append(
            FieldDescription(
                name=field_name,
                field_type=field_type,
                required=field_name in required_set,
                default=field_schema.get("default"),
                units=field_schema.get("units"),
                enum_values=enum_values,
                minimum=field_schema.get("minimum"),
                maximum=field_schema.get("maximum"),
                exclusive_minimum=field_schema.get("exclusiveMinimum"),
                exclusive_maximum=field_schema.get("exclusiveMaximum"),
                note=field_schema.get("note"),
                is_reference=is_reference,
                object_list=object_list,
            )
        )

    return ObjectDescription(
        obj_type=obj_type,
        memo=schema.get_object_memo(obj_type),
        fields=fields,
        required_fields=required_list,
        has_name=schema.has_name(obj_type),
        is_extensible=schema.is_extensible(obj_type),
        extensible_size=schema.get_extensible_size(obj_type),
    )


def _get_field_type(field_schema: dict[str, Any]) -> str | None:
    """Extract the field type from a field schema."""
    if "type" in field_schema:
        result: str = field_schema["type"]
        return result

    if "anyOf" in field_schema:
        any_of: list[dict[str, Any]] = field_schema["anyOf"]
        # Look for a primary type (prefer number/integer over string)
        for sub in any_of:
            if sub.get("type") in ("number", "integer"):
                result = sub["type"]
                return result
        for sub in any_of:
            if sub.get("type") == "string":
                return "string"

    if "enum" in field_schema:
        return "string"

    return None
