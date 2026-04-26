"""Generate type stubs from EnergyPlus epJSON schemas.

This module generates ``_generated_types.pyi`` containing:
- Typed subclasses of IDFObject for every EnergyPlus object type
- A ``TypedDict`` mapping for ``__getitem__`` dispatch on IDFDocument
- Typed attribute accessors for IDFDocument

The TypedDict approach gives pyright O(1) per-key type resolution instead
of O(n) overload matching, yielding ~3x faster type-checking.

The generated file is designed to be committed and shipped with the package.
The ``.pyi`` file is a stub — it has zero runtime cost by design.

Usage::

    python -m idfkit.codegen.generate_stubs          # latest version
    python -m idfkit.codegen.generate_stubs 24.1.0   # specific version
"""

from __future__ import annotations

import re
import sys
from typing import Any

from idfkit.schema import EpJSONSchema, get_schema
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION

# ---- helpers ---------------------------------------------------------------

_CLASS_NAME_RE = re.compile(r"[^A-Za-z0-9]")


def _to_class_name(obj_type: str) -> str:
    """Convert an IDF object type to a valid Python class name.

    'BuildingSurface:Detailed' -> 'BuildingSurfaceDetailed'
    'Material:AirGap'          -> 'MaterialAirGap'
    'OS:Zone'                  -> 'OSZone'
    """
    return _CLASS_NAME_RE.sub("", obj_type)


_ANY_OF_TYPE_MAP = {"number": "float", "integer": "int", "string": "str"}
_SIMPLE_TYPE_MAP: dict[str | None, str] = {
    "number": "float",
    "integer": "int",
    "string": "str",
    "array": "list[Any]",
}


def _schema_type_to_python(
    field_schema: dict[str, Any] | None,
    field_type: str | None,
    has_any_of: bool = False,
) -> str:
    """Map an epJSON schema field type to a Python type annotation.

    Returns the *value* type (without ``| None``).
    Uses ``Literal[...]`` for fields with ``enum`` values.
    """
    if field_schema is not None:
        # Direct enum — use Literal
        if "enum" in field_schema:
            return _enum_to_literal(field_schema["enum"])

        # anyOf — combine numeric types with Literal for string enums
        if has_any_of:
            return _anyof_to_python(field_schema)

    if has_any_of:
        return "str | float"

    return _SIMPLE_TYPE_MAP.get(field_type, "str | float")


def _enum_to_literal(values: list[Any]) -> str:
    """Convert a list of enum values to a ``Literal[...]`` type annotation."""
    parts: list[str] = []
    for v in values:
        if isinstance(v, str):
            if v == "":
                parts.append('""')
            else:
                parts.append(f'"{v}"')
        else:
            parts.append(repr(v))
    return f"Literal[{', '.join(parts)}]"


def _anyof_to_python(field_schema: dict[str, Any]) -> str:
    """Convert an ``anyOf`` field to a Python type annotation.

    Combines numeric types with ``Literal[...]`` for string enum branches.
    """
    numeric_types: list[str] = []
    literal_values: list[str] = []
    for sub in field_schema.get("anyOf", []):
        sub_type = sub.get("type")
        if sub_type in _ANY_OF_TYPE_MAP:
            if "enum" in sub:
                # String branch with specific enum values (e.g. "Autocalculate")
                for v in sub["enum"]:
                    if isinstance(v, str):
                        literal_values.append('""' if v == "" else f'"{v}"')
                    else:
                        literal_values.append(repr(v))
            else:
                numeric_types.append(_ANY_OF_TYPE_MAP[sub_type])

    parts: list[str] = list(dict.fromkeys(numeric_types))  # dedupe, preserve order
    if literal_values:
        parts.append(f"Literal[{', '.join(literal_values)}]")
    return " | ".join(parts) if parts else "str | float"


# ---- version availability --------------------------------------------------


def _build_version_availability() -> tuple[
    dict[str, tuple[int, int, int]], dict[tuple[str, str], tuple[int, int, int]]
]:
    """Compute earliest version for each object type and field.

    Iterates all supported EnergyPlus versions (oldest first) and records the
    first version where each type/field appears.

    Returns:
        A ``(type_since, field_since)`` pair where *type_since* maps object
        type names to their earliest version and *field_since* maps
        ``(obj_type, field_name)`` pairs to theirs.
    """
    type_since: dict[str, tuple[int, int, int]] = {}
    field_since: dict[tuple[str, str], tuple[int, int, int]] = {}

    for ver in ENERGYPLUS_VERSIONS:
        schema = get_schema(ver)
        for obj_type in schema.object_types:
            if obj_type not in type_since:
                type_since[obj_type] = ver

            for field_name in schema.get_field_names(obj_type):
                key = (obj_type, field_name)
                if key not in field_since:
                    field_since[key] = ver

            # Also check extensible field names
            if schema.is_extensible(obj_type):
                for ext_name in schema.get_extensible_field_names(obj_type):
                    key = (obj_type, ext_name)
                    if key not in field_since:
                        field_since[key] = ver

    return type_since, field_since


# ---- docstring generation --------------------------------------------------


def _format_constraints(field_schema: dict[str, Any]) -> str | None:
    """Format min/max constraints from a field schema, or ``None`` if unconstrained."""
    parts: list[str] = []
    if "minimum" in field_schema:
        parts.append(f">= {field_schema['minimum']}")
    if "exclusiveMinimum" in field_schema:
        parts.append(f"> {field_schema['exclusiveMinimum']}")
    if "maximum" in field_schema:
        parts.append(f"<= {field_schema['maximum']}")
    if "exclusiveMaximum" in field_schema:
        parts.append(f"< {field_schema['exclusiveMaximum']}")
    return f"Range: {', '.join(parts)}" if parts else None


def _field_docstring(
    field_schema: dict[str, Any] | None,
    since_version: tuple[int, int, int] | None = None,
) -> str | None:
    """Build a single-line docstring from field metadata.

    Args:
        field_schema: The field's JSON schema fragment.
        since_version: If set, appends ``Since: X.Y.Z`` to the docstring.

    Returns ``None`` if there is nothing useful to document.
    """
    if field_schema is None and since_version is None:
        return None

    parts: list[str] = []

    if field_schema is not None:
        # Primary description
        note = field_schema.get("note")
        if note:
            note_text = " ".join(note.split())
            if len(note_text) > 120:
                note_text = note_text[:117] + "..."
            parts.append(note_text)

        # Units
        units = field_schema.get("units")
        ip_units = field_schema.get("ip-units")
        if units:
            parts.append(f"[{units}] ({ip_units})" if ip_units else f"[{units}]")

        # Default value
        default = field_schema.get("default")
        if default is not None:
            parts.append(f"Default: {default}")

        # Constraints
        constraint_str = _format_constraints(field_schema)
        if constraint_str:
            parts.append(constraint_str)

    # Version availability
    if since_version is not None:
        parts.append(f"Since: {since_version[0]}.{since_version[1]}.{since_version[2]}")

    if not parts:
        return None

    text = "; ".join(parts)
    return _sanitize_docstring(text)


# ---- object class generation ----------------------------------------------


def _sanitize_docstring(text: str) -> str:
    """Replace characters that would break triple-quoted docstrings or ruff checks."""
    text = text.replace('"', "'")
    # Replace ambiguous Unicode quotes/dashes with ASCII equivalents (ruff RUF001)
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", "'").replace("\u201d", "'")
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return text


def _truncate_text(text: str, max_len: int = 120) -> str:
    """Collapse whitespace and truncate *text*, replacing quotes for docstring safety."""
    collapsed = " ".join(text.split())
    if len(collapsed) > max_len:
        collapsed = collapsed[: max_len - 3] + "..."
    return _sanitize_docstring(collapsed)


def _class_docstring(
    memo: str | None,
    since: tuple[int, int, int] | None,
) -> str | None:
    """Build a class-level docstring from memo and version info, or ``None``."""
    parts: list[str] = []
    if memo:
        parts.append(_truncate_text(memo))
    if since is not None and since > ENERGYPLUS_VERSIONS[0]:
        parts.append(f"Since: {since[0]}.{since[1]}.{since[2]}")
    return "; ".join(parts) if parts else None


def _generate_object_class(
    schema: EpJSONSchema,
    obj_type: str,
    *,
    indent: str = "",
    type_since: dict[str, tuple[int, int, int]] | None = None,
    field_since: dict[tuple[str, str], tuple[int, int, int]] | None = None,
) -> list[str]:
    """Generate a typed IDFObject subclass for *obj_type*.

    For extensible types, also generates a per-type :class:`ExtensibleGroup`
    subclass listing the inner field names with their schema-derived types,
    and exposes the wrapper attribute on the parent class typed as
    ``ExtensibleList[GroupClass]``. This gives IDEs full autocomplete on
    ``surface.vertices[0].vertex_x_coordinate`` etc.

    Args:
        indent: Prefix for each line.
        type_since: Mapping of object type -> earliest version it appeared.
        field_since: Mapping of ``(obj_type, field)`` -> earliest version.
    """
    cls_name = _to_class_name(obj_type)
    lines: list[str] = []

    # Pull per-object schema bits.
    pc = schema.get_parsing_cache(obj_type)
    wrapper_key = pc.ext_wrapper_key if pc is not None else None
    ext_inner_props = dict(pc.ext_inner_props) if pc is not None else {}
    field_names = schema.get_field_names(obj_type)

    # If this type has a canonical wrapper, emit a typed ExtensibleGroup
    # subclass before the parent class so the parent can reference it.
    group_cls_name: str | None = None
    if wrapper_key and ext_inner_props:
        group_cls_name = f"{cls_name}{_to_class_name(wrapper_key.title())}Group"
        lines.append(f"{indent}class {group_cls_name}(ExtensibleGroup):")
        lines.append(f'{indent}    """One {wrapper_key} group inside :class:`{cls_name}`."""')
        for inner_name, inner_schema in ext_inner_props.items():
            if not inner_name.isidentifier():
                continue
            has_any_of = "anyOf" in inner_schema
            py_type = _schema_type_to_python(inner_schema, _schema_field_type(inner_schema), has_any_of)
            lines.append(f"{indent}    {inner_name}: {py_type} | None")
        lines.append("")

    lines.append(f"{indent}class {cls_name}(IDFObject):")

    body_indent = indent + "    "

    # Add object-level docstring from schema memo + version info
    obj_since = type_since.get(obj_type) if type_since else None
    cls_doc = _class_docstring(schema.get_object_memo(obj_type), obj_since)
    has_body = False
    if cls_doc:
        lines.append(f'{body_indent}"""{cls_doc}"""')
        has_body = True

    if not field_names and not group_cls_name:
        if not has_body:
            lines[-1] = f"{indent}class {cls_name}(IDFObject): ..."
        else:
            lines.append("")
        return lines

    if field_names:
        _generate_fields(lines, schema, obj_type, field_names, body_indent, obj_since, field_since)

    # Add the canonical wrapper attribute typed as ExtensibleList[<GroupCls>].
    if group_cls_name and wrapper_key:
        lines.append(f"{body_indent}{wrapper_key}: ExtensibleList[{group_cls_name}]")

    return lines


def _schema_field_type(field_schema: dict[str, Any]) -> str | None:
    """Pull the direct schema 'type' string from a property schema."""
    t = field_schema.get("type")
    if isinstance(t, str):
        return t
    return None


def _generate_fields(
    lines: list[str],
    schema: EpJSONSchema,
    obj_type: str,
    field_names: list[str],
    indent: str,
    obj_since: tuple[int, int, int] | None,
    field_since: dict[tuple[str, str], tuple[int, int, int]] | None,
) -> None:
    """Append typed field declarations to *lines*."""
    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}

    for field_name in field_names:
        if not field_name.isidentifier():
            continue

        field_schema = properties.get(field_name)
        field_type = schema.get_field_type(obj_type, field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        py_type = _schema_type_to_python(field_schema, field_type, has_any_of)

        lines.append(f"{indent}{field_name}: {py_type} | None")

        # Determine field "Since:" — only if the field appeared after the type itself
        fld_since: tuple[int, int, int] | None = None
        if field_since is not None and obj_since is not None:
            fld_ver = field_since.get((obj_type, field_name))
            if fld_ver is not None and fld_ver > obj_since:
                fld_since = fld_ver

        docstring = _field_docstring(field_schema, since_version=fld_since)
        if docstring:
            lines.append(f'{indent}"""{docstring}"""')


# ---- TypedDict mapping generation ------------------------------------------


def _generate_object_type_map(
    schema: EpJSONSchema,
) -> list[str]:
    """Generate a ``TypedDict`` mapping EnergyPlus type names to typed collections.

    This replaces 858 ``@overload`` decorators with a single ``TypedDict``.
    Pyright resolves ``td["Zone"]`` in O(1) via hash lookup vs O(n) overload
    matching, giving ~3x faster type-checking.
    """
    lines: list[str] = []
    lines.append('_ObjectTypeMap = TypedDict("_ObjectTypeMap", {')
    for obj_type in schema.object_types:
        cls_name = _to_class_name(obj_type)
        lines.append(f'    "{obj_type}": IDFCollection[{cls_name}],')
    lines.append("}, total=False)")
    return lines


_RESERVED_ATTRS = frozenset({
    "version",
    "filepath",
    "strict",
    "schema",
    "collections",
    "references",
    "copy",
    "keys",
    "values",
    "items",
})


def _generate_attr_properties(
    python_to_idf: dict[str, str],
    indent: str = "    ",
) -> list[str]:
    """Generate typed ``@property`` accessors for IDFDocument.

    These correspond to the ``_PYTHON_TO_IDF`` mapping in document.py.
    Skips names that conflict with real instance attributes or methods.
    """
    lines: list[str] = []
    for py_name, idf_type in python_to_idf.items():
        if py_name in _RESERVED_ATTRS:
            continue
        cls_name = _to_class_name(idf_type)
        lines.append(f"{indent}@property")
        lines.append(f"{indent}def {py_name}(self) -> IDFCollection[{cls_name}]: ...")
    return lines


# ---- main generation -------------------------------------------------------


def generate_stubs(version: tuple[int, int, int] | None = None) -> str:
    """Generate the full ``_generated_types.pyi`` content.

    Args:
        version: EnergyPlus version tuple.  Defaults to *LATEST_VERSION*.

    Returns:
        Complete Python source for the generated types module.
    """
    ver = version or LATEST_VERSION
    schema = get_schema(ver)
    version_str = f"{ver[0]}.{ver[1]}.{ver[2]}"

    # Compute version availability for "Since:" annotations
    type_since, field_since = _build_version_availability()

    parts: list[str] = []
    parts.append(f'"""Auto-generated type stubs for EnergyPlus {version_str} object types.')
    parts.append("")
    parts.append("DO NOT EDIT — regenerate with:")
    parts.append(f"    python -m idfkit.codegen.generate_stubs {version_str}")
    parts.append('"""')
    parts.append("")
    parts.append("from __future__ import annotations")
    parts.append("")
    parts.append("from typing import Any, Literal, TypedDict")
    parts.append("")
    parts.append("from .objects import ExtensibleGroup, ExtensibleList, IDFCollection, IDFObject")
    parts.append("")
    parts.append("# =========================================================================")
    parts.append("# Typed object classes (one per EnergyPlus object type)")
    parts.append("# =========================================================================")
    parts.append("")

    # Generate all typed object classes at top-level
    for obj_type in schema.object_types:
        class_lines = _generate_object_class(
            schema,
            obj_type,
            type_since=type_since,
            field_since=field_since,
        )
        parts.extend(class_lines)
        parts.append("")

    # Generate the TypedDict mapping for __getitem__ dispatch
    parts.append("# =========================================================================")
    parts.append("# TypedDict mapping for IDFDocument.__getitem__ dispatch")
    parts.append("# =========================================================================")
    parts.append("")
    parts.extend(_generate_object_type_map(schema))
    parts.append("")

    return "\n".join(parts)


def generate_document_pyi(version: tuple[int, int, int] | None = None) -> str:
    """Generate ``document.pyi`` — a type stub for ``document.py``.

    The stub declares ``IDFDocument`` as inheriting from ``_ObjectTypeMap``
    (a ``TypedDict``), which gives pyright O(1) per-key type resolution for
    ``__getitem__`` without any ``@overload`` decorators.
    """
    ver = version or LATEST_VERSION
    version_str = f"{ver[0]}.{ver[1]}.{ver[2]}"

    from idfkit.document import _PYTHON_TO_IDF  # pyright: ignore[reportPrivateUsage]

    lines: list[str] = []

    # Header
    lines.append(f'"""Auto-generated type stub for IDFDocument (EnergyPlus {version_str}).')
    lines.append("")
    lines.append("DO NOT EDIT — regenerate with:")
    lines.append(f"    python -m idfkit.codegen.generate_stubs {version_str}")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from collections.abc import Iterator")
    lines.append("from pathlib import Path")
    lines.append("from typing import Any, Generic, TypeVar")
    lines.append("")
    lines.append("from ._compat import EppyDocumentMixin")
    lines.append("from ._generated_types import *  # noqa: F403")
    lines.append("from ._generated_types import _ObjectTypeMap")
    lines.append("from .cst import DocumentCST")
    lines.append("from .introspection import ObjectDescription")
    lines.append("from .objects import IDFCollection, IDFObject")
    lines.append("from .references import ReferenceGraph")
    lines.append("from .schema import EpJSONSchema")
    lines.append("from .simulation.config import EnergyPlusConfig")
    lines.append("")
    lines.append("Strict = TypeVar('Strict', bound=bool, default=bool, covariant=True)")
    lines.append("")
    lines.append("_PYTHON_TO_IDF: dict[str, str]")
    lines.append("_IDF_TO_PYTHON: dict[str, str]")
    lines.append("")

    # Class definition — inherit from _ObjectTypeMap (TypedDict) for __getitem__ dispatch
    lines.append("class IDFDocument(_ObjectTypeMap, EppyDocumentMixin, Generic[Strict]):  # type: ignore[misc]")
    lines.append("    filepath: Path | None")
    lines.append("")
    lines.append("    def __init__(")
    lines.append("        self,")
    lines.append("        version: tuple[int, int, int] | None = ...,")
    lines.append("        schema: EpJSONSchema | None = ...,")
    lines.append("        filepath: Path | str | None = ...,")
    lines.append("        *,")
    lines.append("        strict: Strict = ...,")
    lines.append("    ) -> None: ...")
    lines.append("")

    # Properties
    lines.append("    @property")
    lines.append("    def version(self) -> tuple[int, int, int]: ...")
    lines.append("    @property")
    lines.append("    def strict(self) -> Strict: ...")
    lines.append("    @property")
    lines.append("    def schema(self) -> EpJSONSchema | None: ...")
    lines.append("    @property")
    lines.append("    def cst(self) -> DocumentCST | None: ...")
    lines.append("    @property")
    lines.append("    def raw_text(self) -> str | None: ...")
    lines.append("    @property")
    lines.append("    def collections(self) -> dict[str, IDFCollection[IDFObject]]: ...")
    lines.append("    @property")
    lines.append("    def references(self) -> ReferenceGraph: ...")
    lines.append("")

    # get_collection — typed access for dynamic string keys (avoids TypedDict Unknown)
    lines.append("    def get_collection(self, obj_type: str) -> IDFCollection[IDFObject]: ...")
    # __getattr__ — fallback for object types not covered by the generated @property
    # accessors below.  Keeps the stub open to custom/uncommon EnergyPlus types;
    # the typed properties still provide autocomplete for the ~90 most common types.
    lines.append("    def __getattr__(self, name: str) -> IDFCollection[IDFObject]: ...")
    lines.append("    def __contains__(self, obj_type: str) -> bool: ...  # type: ignore[override]")
    lines.append("    def __iter__(self) -> Iterator[str]: ...  # type: ignore[override]")
    lines.append("    def __len__(self) -> int: ...")
    lines.append("    def keys(self) -> list[str]: ...  # type: ignore[override]")
    lines.append("    def values(self) -> list[IDFCollection[IDFObject]]: ...  # type: ignore[override]")
    lines.append("    def items(self) -> list[tuple[str, IDFCollection[IDFObject]]]: ...  # type: ignore[override]")
    lines.append("    def describe(self, obj_type: str) -> ObjectDescription: ...")
    lines.append("")

    # add() — no overloads, returns IDFObject
    lines.append(
        "    def add(self, obj_type: str, name: str = ..., "
        "fields: dict[str, Any] | None = ..., *, validate: bool = ..., "
        "**kwargs: Any) -> IDFObject: ..."
    )
    lines.append("")

    # Remaining methods
    lines.append("    def addidfobject(self, obj: IDFObject) -> IDFObject: ...")
    lines.append("    def removeidfobject(self, obj: IDFObject) -> None: ...")
    lines.append("    def rename(self, obj_type: str, old_name: str, new_name: str) -> None: ...")
    lines.append("    def notify_name_change(self, obj: IDFObject, old_name: str, new_name: str) -> None: ...")
    lines.append(
        "    def notify_reference_change(self, obj: IDFObject, field_name: str, old_value: Any, new_value: Any) -> None: ..."
    )
    lines.append("    def get_referencing(self, name: str) -> set[IDFObject]: ...")
    lines.append("    def get_references(self, obj: IDFObject) -> set[str]: ...")
    lines.append("    @property")
    lines.append("    def schedules_dict(self) -> dict[str, IDFObject]: ...")
    lines.append("    def get_schedule(self, name: str) -> IDFObject | None: ...")
    lines.append("    def get_used_schedules(self) -> set[str]: ...")
    lines.append("    def get_zone_surfaces(self, zone_name: str) -> list[IDFObject]: ...")
    lines.append("    @property")
    lines.append("    def all_objects(self) -> Iterator[IDFObject]: ...")
    lines.append("    def objects_by_type(self) -> Iterator[tuple[str, IDFCollection[IDFObject]]]: ...")
    lines.append(
        "    def expand(self, *, energyplus: EnergyPlusConfig | None = ..., timeout: float = ...) -> IDFDocument[Strict]: ..."
    )
    lines.append("    def copy(self) -> IDFDocument[Strict]: ...")
    lines.append("")

    # Attribute accessor properties
    lines.extend(_generate_attr_properties(_PYTHON_TO_IDF, indent="    "))
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point."""
    from pathlib import Path

    version: tuple[int, int, int] | None = None
    if len(sys.argv) > 1:
        version_parts = sys.argv[1].split(".")
        version = (int(version_parts[0]), int(version_parts[1]), int(version_parts[2]))

    content = generate_stubs(version)
    doc_pyi = generate_document_pyi(version)

    # Write to src/idfkit/
    base_path = Path(__file__).resolve().parent.parent

    types_path = base_path / "_generated_types.pyi"
    types_path.write_text(content, encoding="utf-8")

    pyi_path = base_path / "document.pyi"
    pyi_path.write_text(doc_pyi, encoding="utf-8")

    # Run ruff format so regenerated stubs match the committed (ruff-formatted) versions
    import subprocess

    subprocess.run(  # noqa: S603
        [sys.executable, "-m", "ruff", "format", str(types_path), str(pyi_path)],
        check=False,
    )
    print(f"Generated {types_path} ({types_path.stat().st_size:,} bytes)")
    print(f"Generated {pyi_path} ({pyi_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
