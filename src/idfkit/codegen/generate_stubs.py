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
from idfkit.versions import LATEST_VERSION

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
    """
    if has_any_of and field_schema is not None:
        types = [
            _ANY_OF_TYPE_MAP[sub["type"]]
            for sub in field_schema.get("anyOf", [])
            if sub.get("type") in _ANY_OF_TYPE_MAP
        ]
        if types:
            return " | ".join(dict.fromkeys(types))
        return "str | float"

    return _SIMPLE_TYPE_MAP.get(field_type, "str | float")


# ---- object class generation ----------------------------------------------


def _generate_object_class(
    schema: EpJSONSchema,
    obj_type: str,
    *,
    indent: str = "",
) -> list[str]:
    """Generate a typed IDFObject subclass for *obj_type*.

    Args:
        indent: Prefix for each line (e.g. ``""`` for top-level, ``"    "``
            for nested inside a block).
    """
    cls_name = _to_class_name(obj_type)
    lines: list[str] = []
    lines.append(f"{indent}class {cls_name}(IDFObject):")

    field_names = schema.get_field_names(obj_type)

    # For extensible types, add base extensible field names
    if schema.is_extensible(obj_type):
        for ext_name in schema.get_extensible_field_names(obj_type):
            if ext_name not in field_names:
                field_names.append(ext_name)

    body_indent = indent + "    "

    if not field_names:
        lines.append(f"{body_indent}...")
        return lines

    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}

    for field_name in field_names:
        # Skip field names that aren't valid Python identifiers (e.g. "100_outdoor_air_in_cooling")
        if not field_name.isidentifier():
            continue

        field_schema = properties.get(field_name)
        field_type = schema.get_field_type(obj_type, field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        py_type = _schema_type_to_python(field_schema, field_type, has_any_of)

        # Use simple annotated attributes (compact, 1 line per field instead of 4)
        lines.append(f"{body_indent}{field_name}: {py_type} | None")

    return lines


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
        lines.append("        @property")
        lines.append(f"        def {py_name}(self) -> IDFCollection[{cls_name}]: ...")
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

    parts: list[str] = []
    parts.append(f'"""Auto-generated type stubs for EnergyPlus {version_str} object types.')
    parts.append("")
    parts.append("DO NOT EDIT — regenerate with:")
    parts.append(f"    python -m idfkit.codegen.generate_stubs {version_str}")
    parts.append('"""')
    parts.append("")
    parts.append("from typing import Any, TypedDict")
    parts.append("")
    parts.append("from .objects import IDFCollection, IDFObject")
    parts.append("")
    parts.append("# =========================================================================")
    parts.append("# Typed object classes (one per EnergyPlus object type)")
    parts.append("# =========================================================================")
    parts.append("")

    # Generate all typed object classes at top-level
    for obj_type in schema.object_types:
        class_lines = _generate_object_class(schema, obj_type)
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
    lines.append("from ._generated_types import *  # noqa: F401,F403")
    lines.append("from ._generated_types import _ObjectTypeMap")
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
    lines.append("    version: tuple[int, int, int]")
    lines.append("    filepath: Path | None")
    lines.append("")
    lines.append("    def __init__(")
    lines.append("        self,")
    lines.append("        version: tuple[int, int, int] | None = ...,")
    lines.append("        schema: EpJSONSchema | None = ...,")
    lines.append("        filepath: Path | str | None = ...,")
    lines.append("        *,")
    lines.append("        strict: Strict = ...,  # type: ignore[assignment]")
    lines.append("    ) -> None: ...")
    lines.append("")

    # Properties
    lines.append("    @property")
    lines.append("    def strict(self) -> Strict: ...")
    lines.append("    @property")
    lines.append("    def schema(self) -> EpJSONSchema | None: ...")
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
        "data: dict[str, Any] | None = ..., *, validate: bool = ..., "
        "**kwargs: Any) -> IDFObject: ..."
    )
    lines.append("")

    # Remaining methods
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
    attr_lines = _generate_attr_properties(_PYTHON_TO_IDF)
    for line in attr_lines:
        lines.append(line.replace("        ", "    ", 1))
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point."""
    import importlib.resources
    from pathlib import Path

    version: tuple[int, int, int] | None = None
    if len(sys.argv) > 1:
        version_parts = sys.argv[1].split(".")
        version = (int(version_parts[0]), int(version_parts[1]), int(version_parts[2]))

    content = generate_stubs(version)
    doc_pyi = generate_document_pyi(version)

    # Write to src/idfkit/
    pkg_dir = importlib.resources.files("idfkit")
    base_path = Path(str(getattr(pkg_dir, "_path", pkg_dir)))

    types_path = base_path / "_generated_types.pyi"
    types_path.write_text(content, encoding="utf-8")
    print(f"Generated {types_path} ({len(content):,} bytes)")

    pyi_path = base_path / "document.pyi"
    pyi_path.write_text(doc_pyi, encoding="utf-8")
    print(f"Generated {pyi_path} ({len(doc_pyi):,} bytes)")


if __name__ == "__main__":
    main()
