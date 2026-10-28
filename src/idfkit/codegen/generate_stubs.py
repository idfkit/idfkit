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

import ast
import contextlib
import dataclasses
import functools
import keyword
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from idfkit.schema import EpJSONSchema, get_schema
from idfkit.versions import ENERGYPLUS_VERSIONS, version_string

# ---- helpers ---------------------------------------------------------------

Version = tuple[int, int, int]


@dataclasses.dataclass
class _SupportedVersions:
    """The releases the generated stubs describe: every bundled one, unless cut short."""

    versions: tuple[Version, ...] = ENERGYPLUS_VERSIONS

    @property
    def latest(self) -> Version:
        """The newest release described, which ``IDFDocument`` is typed for."""
        return self.versions[-1]


SUPPORTED = _SupportedVersions()


@contextlib.contextmanager
def supported_up_to(latest: Version) -> Iterator[None]:
    """Generate as if *latest* were the newest supported release.

    The stubs generated inside are those the package had before the releases after *latest*
    were adopted, so this is also how a test reproduces adopting a release.
    """
    if latest not in ENERGYPLUS_VERSIONS:
        msg = f"{latest} is not a bundled EnergyPlus release"
        raise ValueError(msg)
    saved = SUPPORTED.versions
    SUPPORTED.versions = tuple(ver for ver in ENERGYPLUS_VERSIONS if ver <= latest)
    _clear_version_caches()
    try:
        yield
    finally:
        SUPPORTED.versions = saved
        _clear_version_caches()


def _clear_version_caches() -> None:
    for cached in (_build_type_runs, _shared_layout, _class_assignment):
        cached.cache_clear()


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


# ---- source-docstring extraction -------------------------------------------


def _extract_class_docstrings(source_path: Path, class_name: str) -> dict[str, str]:
    """Parse *source_path* and return a map of qualified names to docstrings.

    Keys are ``class_name`` for the class docstring and ``class_name.method``
    for each method/property/static method/classmethod defined directly in
    that class.  Docstrings are returned as ``ast.get_docstring`` produces them
    (cleaned and dedented).
    """
    out: dict[str, str] = {}
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not (isinstance(node, ast.ClassDef) and node.name == class_name):
            continue
        cls_doc = ast.get_docstring(node)
        if cls_doc:
            out[class_name] = cls_doc
        for sub in node.body:
            if isinstance(sub, ast.FunctionDef | ast.AsyncFunctionDef):
                doc = ast.get_docstring(sub)
                if doc:
                    out[f"{class_name}.{sub.name}"] = doc
        break
    return out


def _format_docstring_for_stub(text: str, indent: str) -> list[str]:
    """Format *text* as triple-quoted docstring lines for inclusion in a stub.

    Returns a list of lines (without trailing newlines).  Single-line input
    becomes a one-line ``\"\"\"...\"\"\"``; multi-line input is reflowed with
    each line re-indented to *indent*.  Embedded triple quotes are sanitized.
    """
    text = text.strip()
    if not text:
        return []
    text = text.replace('"""', "'''")
    if "\n" not in text:
        return [f'{indent}"""{text}"""']
    in_lines = text.split("\n")
    out_lines: list[str] = [f'{indent}"""{in_lines[0]}']
    for ln in in_lines[1:]:
        out_lines.append(f"{indent}{ln}" if ln.strip() else "")
    out_lines.append(f'{indent}"""')
    return out_lines


def _emit_method(
    lines: list[str],
    signature: str,
    docstring: str | None,
    *,
    decorators: tuple[str, ...] = (),
    indent: str = "    ",
    suffix: str = "",
) -> None:
    """Append a method/property declaration to *lines*.

    *signature* should not include the trailing ``:`` or body.  When *docstring*
    is provided, it is emitted as the only body element (no ``...`` placeholder
    is needed in stubs since the docstring itself is a valid statement).
    *suffix* is appended to the line that ends with ``:`` or ``: ...`` -- use
    it for trailing comments such as ``# type: ignore[override]``.
    """
    for d in decorators:
        lines.append(f"{indent}{d}")
    if docstring:
        lines.append(f"{indent}{signature}:{suffix}")
        lines.extend(_format_docstring_for_stub(docstring, indent + "    "))
    else:
        lines.append(f"{indent}{signature}: ...{suffix}")


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
    suffix: str = "",
    class_doc: str | None = None,
    cls_name: str | None = None,
    base: str = "IDFObject",
    skip_fields: frozenset[str] = frozenset(),
    omit_group: bool = False,
    fields_base: str = "TypedDict",
    emit_update: bool = True,
    undocumented: frozenset[str] = frozenset(),
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
        suffix: Appended to the class names, for the classes of an older version range.
        class_doc: Replaces the class docstring built from the memo and *type_since*; ``""``
            emits none.
        cls_name: Replaces the class name derived from *obj_type* and *suffix*.
        base: The class's base, ``IDFObject`` unless the fields it shares with other versions
            live on a per-type base class.
        skip_fields: Fields left to *base*.
        omit_group: Leave the extensible group and its wrapper attribute to *base* (or out).
        fields_base: The ``TypedDict`` that ``update``'s keyword ``TypedDict`` extends.
        emit_update: Whether to type ``update`` on this class.
        undocumented: Fields declared without a docstring.
    """
    cls_name = cls_name or _to_class_name(obj_type) + suffix
    lines: list[str] = []

    # Pull per-object schema bits.
    pc = schema.get_parsing_cache(obj_type)
    wrapper_key = pc.ext_wrapper_key if pc is not None else None
    ext_inner_props = dict(pc.ext_inner_props) if pc is not None else {}
    field_names = [f for f in schema.get_field_names(obj_type) if f not in skip_fields]
    if omit_group:
        wrapper_key = None

    # If this type has a canonical wrapper, emit a typed ExtensibleGroup
    # subclass before the parent class so the parent can reference it.
    group_cls_name: str | None = None
    if wrapper_key and ext_inner_props:
        group_cls_name = f"{_to_class_name(obj_type)}{_to_class_name(wrapper_key.title())}Group{suffix}"
        lines.extend(_generate_group_class(group_cls_name, cls_name, wrapper_key, ext_inner_props, indent))

    lines.append(f"{indent}class {cls_name}({base}):")

    body_indent = indent + "    "

    # Add object-level docstring from schema memo + version info
    obj_since = type_since.get(obj_type) if type_since else None
    cls_doc = class_doc if class_doc is not None else _class_docstring(schema.get_object_memo(obj_type), obj_since)
    has_body = False
    if cls_doc:
        lines.append(f'{body_indent}"""{cls_doc}"""')
        has_body = True

    if not field_names and not group_cls_name:
        if emit_update and fields_base != "TypedDict":
            # Every field is on the shared base, but update still takes them all as keywords.
            lines.extend(_generate_update(cls_name, [], indent, fields_base))
        elif has_body:
            lines.append("")
        else:
            lines[-1] = f"{indent}class {cls_name}({base}): ..."
        return lines

    update_fields: list[tuple[str, str]] = []
    if field_names:
        update_fields = _generate_fields(
            lines, schema, obj_type, field_names, body_indent, obj_since, field_since, undocumented
        )

    # Add the canonical wrapper attribute typed as ExtensibleList[<GroupCls>].
    if group_cls_name and wrapper_key:
        lines.append(f"{body_indent}{wrapper_key}: ExtensibleList[{group_cls_name}]")
        update_fields.append((wrapper_key, "list[Any]"))

    if emit_update:
        lines.extend(_generate_update(cls_name, update_fields, indent, fields_base))
    return lines


def _generate_group_class(
    group_cls_name: str, cls_name: str, wrapper_key: str, inner_props: dict[str, Any], indent: str
) -> list[str]:
    """Generate the :class:`ExtensibleGroup` subclass of one extensible group, with its inner fields."""
    lines = [
        f"{indent}class {group_cls_name}(ExtensibleGroup):",
        f'{indent}    """One {wrapper_key} group inside :class:`{cls_name}`."""',
    ]
    for inner_name, inner_schema in inner_props.items():
        if not inner_name.isidentifier():
            continue
        has_any_of = "anyOf" in inner_schema
        py_type = _schema_type_to_python(inner_schema, _schema_field_type(inner_schema), has_any_of)
        lines.append(f"{indent}    {inner_name}: {py_type} | None")
    lines.append("")
    return lines


def _generate_update(
    cls_name: str, fields: list[tuple[str, str]], indent: str, fields_base: str = "TypedDict"
) -> list[str]:
    """Type ``update`` on *cls_name* with a private ``TypedDict`` of its fields.

    The ``TypedDict`` types the keywords (through ``Unpack``), so a type checker reports an unknown
    field name or a wrongly typed value given as a keyword. ``name`` is left out because ``update``
    refuses it. The positional mapping stays ``Mapping[str, Any] | None``, as at run time: a
    ``TypedDict`` there would reject a mapping built at run time, ``None``, and the spaced field
    names single assignment accepts, all of which the method accepts. The override narrows
    ``IDFObject.update``'s ``**kwargs: Any``, which mypy reports; pyright does not.
    """
    fields_cls = f"_{cls_name}Fields"
    lines = [
        "",
        f"{indent}    def update(self, values: Mapping[str, Any] | None = ..., /, **kwargs: Unpack[{fields_cls}]) "
        "-> None: ...  # type: ignore[override]",
        "",
        f"{indent}class {fields_cls}({fields_base}, total=False):",
    ]
    entries = [(name, py_type) for name, py_type in fields if name != "name"]
    if not entries:
        lines[-1] += " ..."
    lines.extend(f"{indent}    {name}: {py_type}" for name, py_type in entries)
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
    undocumented: frozenset[str] = frozenset(),
) -> list[tuple[str, str]]:
    """Append typed field declarations to *lines*; return each declared field with its value type.

    A field in *undocumented* gets no docstring, because the class that narrows it carries one.
    """
    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}
    declared: list[tuple[str, str]] = []

    for field_name in field_names:
        if not field_name.isidentifier():
            continue

        field_schema = properties.get(field_name)
        field_type = schema.get_field_type(obj_type, field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        py_type = _schema_type_to_python(field_schema, field_type, has_any_of)

        lines.append(f"{indent}{field_name}: {py_type} | None")
        declared.append((field_name, f"{py_type} | None"))

        # Determine field "Since:" — only if the field appeared after the type itself
        fld_since: tuple[int, int, int] | None = None
        if field_since is not None and obj_since is not None:
            fld_ver = field_since.get((obj_type, field_name))
            if fld_ver is not None and fld_ver > obj_since:
                fld_since = fld_ver

        docstring = None if field_name in undocumented else _field_docstring(field_schema, since_version=fld_since)
        if docstring:
            lines.append(f'{indent}"""{docstring}"""')
    return declared


# ---- TypedDict mapping generation ------------------------------------------


def _generate_object_type_map(
    schema: EpJSONSchema,
) -> list[str]:
    """Generate a ``TypedDict`` mapping EnergyPlus type names to typed collections.

    This replaces 858 ``@overload`` decorators with a single ``TypedDict``.
    Pyright resolves ``td["Zone"]`` in O(1) via hash lookup vs O(n) overload
    matching, giving ~3x faster type-checking.

    The map is emitted with ``total=True`` because :class:`IDFDocument` always
    returns a collection for any known object type (lazily creating an empty
    one if absent), so every key behaves as required.  ``total=False`` would
    cause pyright's ``reportTypedDictNotRequiredAccess`` to fire on every
    ``doc["Zone"]`` lookup.  The TypedDict is stub-only and never instantiated
    as a dict literal, so the construction semantics of ``total=True`` do not
    apply.
    """
    lines: list[str] = []
    lines.append('_ObjectTypeMap = TypedDict("_ObjectTypeMap", {')
    for obj_type in schema.object_types:
        cls_name = _to_class_name(obj_type)
        lines.append(f'    "{obj_type}": IDFCollection[{cls_name}],')
    lines.append("}, total=True)")
    return lines


def _generate_attr_properties(
    python_to_idf: dict[str, str],
    schema: EpJSONSchema,
    indent: str = "    ",
) -> list[str]:
    """Generate typed ``@property`` accessors for IDFDocument.

    These are the names the attribute resolver accepts as canonical: one
    ``snake_case`` plural per object type, plus the shorthands in
    ``_PYTHON_TO_IDF``.
    Skips every name that is a real member of ``IDFDocument``. That is the same
    set the attribute resolver treats as reserved, so the stub and the runtime
    cannot disagree about which of the two a name reaches.

    Each property gets a docstring derived from the EnergyPlus schema memo for
    the underlying object type, so IDEs surface a description on hover.
    """
    from idfkit.document import _RESERVED  # pyright: ignore[reportPrivateUsage]

    lines: list[str] = []
    for py_name, idf_type in python_to_idf.items():
        if py_name in _RESERVED:
            continue
        cls_name = _to_class_name(idf_type)
        memo = schema.get_object_memo(idf_type)
        doc_parts = [f"All ``{idf_type}`` objects in the document."]
        if memo:
            doc_parts.append(_truncate_text(memo, max_len=200))
        docstring = " ".join(doc_parts)
        _emit_method(
            lines,
            f"def {py_name}(self) -> IDFCollection[{cls_name}]",
            docstring,
            decorators=("@property",),
            indent=indent,
        )
    return lines


# ---- per-version typing ----------------------------------------------------


def _version_tag(ver: Version) -> str:
    """``(9, 4, 0)`` -> ``'9_4'``. Major and minor identify every supported release."""
    return f"{ver[0]}_{ver[1]}"


def _class_signature(lines: list[str]) -> tuple[str, ...]:
    """The declarations of a generated class, without docstrings, to compare across versions."""
    return tuple(ln for ln in lines if ln.strip() and not ln.strip().startswith('"""'))


@functools.cache
def _build_type_runs() -> dict[str, list[list[Version]]]:
    """Group, for each object type, the versions that declare it identically.

    Two versions declare a type identically when its generated class (field names, value types,
    choice lists and extensible group) is the same apart from docstrings. Every such group is a
    contiguous range of releases, so it is fully described by its two endpoints; the function
    asserts that rather than assuming it.

    Returns:
        Object type -> its ranges, oldest first, each the list of versions it covers.
    """
    signatures: dict[str, list[tuple[Version, tuple[str, ...]]]] = {}
    for ver in SUPPORTED.versions:
        schema = get_schema(ver)
        for obj_type in schema.object_types:
            signatures.setdefault(obj_type, []).append((
                ver,
                _class_signature(_generate_object_class(schema, obj_type)),
            ))

    order = {ver: i for i, ver in enumerate(SUPPORTED.versions)}
    runs: dict[str, list[list[Version]]] = {}
    for obj_type, entries in signatures.items():
        type_runs: list[tuple[list[Version], tuple[str, ...]]] = []
        for ver, sig in entries:
            if type_runs and type_runs[-1][1] == sig and order[type_runs[-1][0][-1]] + 1 == order[ver]:
                type_runs[-1][0].append(ver)
            else:
                type_runs.append(([ver], sig))
        seen = [sig for _, sig in type_runs]
        if len(set(seen)) != len(seen):  # pragma: no cover - a property of the bundled schemas
            msg = f"{obj_type} returns to an earlier declaration; its version ranges are not contiguous"
            raise ValueError(msg)
        runs[obj_type] = [vers for vers, _ in type_runs]
    return runs


def _field_decls(schema: EpJSONSchema, obj_type: str) -> dict[str, str]:
    """Each identifier field of *obj_type* with its generated value type."""
    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}
    decls: dict[str, str] = {}
    for field_name in schema.get_field_names(obj_type):
        if not field_name.isidentifier():
            continue
        field_schema = properties.get(field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        decls[field_name] = _schema_type_to_python(
            field_schema, schema.get_field_type(obj_type, field_name), has_any_of
        )
    return decls


def _group_decl(schema: EpJSONSchema, obj_type: str) -> tuple[str, tuple[tuple[str, str], ...]] | None:
    """The extensible wrapper key of *obj_type* and its inner fields' types, or ``None``."""
    pc = schema.get_parsing_cache(obj_type)
    if pc is None or not pc.ext_wrapper_key or not pc.ext_inner_props:
        return None
    inner = tuple(
        (name, _schema_type_to_python(sub, _schema_field_type(sub), "anyOf" in sub))
        for name, sub in pc.ext_inner_props.items()
        if name.isidentifier()
    )
    return pc.ext_wrapper_key, inner


def _split_union(type_text: str) -> list[str]:
    """Split a generated value type at its top-level ``|``."""
    parts: list[str] = []
    depth = 0
    start = 0
    for i, ch in enumerate(type_text):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch == "|" and depth == 0:
            parts.append(type_text[start:i].strip())
            start = i + 1
    parts.append(type_text[start:].strip())
    return parts


def _merge_types(type_texts: list[str]) -> str:
    """The union of generated value types, with every ``Literal`` member merged into one ``Literal``."""
    literals: list[str] = []
    others: list[str] = []
    for text in type_texts:
        for part in _split_union(text):
            if part.startswith("Literal[") and part.endswith("]"):
                literals.extend(m for m in _split_literal(part[len("Literal[") : -1]) if m not in literals)
            elif part not in others:
                others.append(part)
    if literals:
        others.append(f"Literal[{', '.join(literals)}]")
    return " | ".join(others)


def _split_literal(members: str) -> list[str]:
    """Split the members of a generated ``Literal[...]``; string members never contain a quote."""
    out: list[str] = []
    current = ""
    in_str = False
    for ch in members:
        if ch == '"':
            in_str = not in_str
        if ch == "," and not in_str:
            out.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        out.append(current.strip())
    return out


@dataclasses.dataclass(frozen=True)
class _SharedLayout:
    """What every supported version of one object type has in common.

    Attributes:
        fields: Every field present in all versions, with the union of its value types.
        identical: The fields declared identically in all versions; only the shared base declares them.
        group: Whether the extensible group is identical in all versions.
    """

    fields: dict[str, str]
    identical: frozenset[str]
    group: bool

    @property
    def varying(self) -> frozenset[str]:
        """Fields present in all versions with different value types; every class narrows them."""
        return frozenset(self.fields) - self.identical


@functools.cache
def _shared_layout() -> dict[str, _SharedLayout]:
    """For each type of the latest release that some older version declares differently.

    Such a type gets a private ``_<Class>Base``: the type as every supported version has it. The
    latest class and each older range's class derive from it, so they only declare what is theirs,
    and ``AnyIDFDocument`` types the type's collection with it.
    """
    runs = _build_type_runs()
    latest_types = set(get_schema(SUPPORTED.latest).object_types)
    layout: dict[str, _SharedLayout] = {}
    for obj_type, type_runs in runs.items():
        if obj_type not in latest_types or len(type_runs) == 1:
            continue
        schemas = [get_schema(run[0]) for run in type_runs]
        decls = [_field_decls(sc, obj_type) for sc in schemas]
        latest = decls[-1]
        fields = {name: _merge_types([d[name] for d in decls]) for name in latest if all(name in d for d in decls)}
        identical = frozenset(name for name in fields if all(d[name] == latest[name] for d in decls))
        groups = {_group_decl(sc, obj_type) for sc in schemas}
        layout[obj_type] = _SharedLayout(fields, identical, len(groups) == 1 and None not in groups)
    return layout


def _shared_class_name(obj_type: str) -> str:
    """The class ``AnyIDFDocument`` types *obj_type*'s collection with."""
    if obj_type in _shared_layout():
        return f"_{_to_class_name(obj_type)}Base"
    return _to_class_name(obj_type)


def _common_fields_name(obj_type: str) -> str:
    """The ``TypedDict`` of the ``update`` keywords every version of *obj_type* accepts alike."""
    return f"_{_to_class_name(obj_type)}CommonFields"


def _generate_base_class(
    schema: EpJSONSchema,
    obj_type: str,
    layout: _SharedLayout,
    type_since: dict[str, tuple[int, int, int]],
    field_since: dict[tuple[str, str], tuple[int, int, int]],
) -> list[str]:
    """Generate ``_<Class>Base``: the fields of *obj_type* present in every supported version.

    A field whose value type differs between versions is declared here with the union of them,
    and narrowed again, with its docstring, by each version's class. ``update`` is typed on those
    classes only: their keyword ``TypedDict`` extends ``_<Class>CommonFields``, which holds the
    fields declared identically everywhere, so those are written once.
    """
    base = _shared_class_name(obj_type)
    latest = _field_decls(schema, obj_type)
    common = [(name, f"{latest[name]} | None") for name in latest if name in layout.identical and name != "name"]
    group = _group_decl(schema, obj_type)
    if layout.group and group is not None:
        common.append((group[0], "list[Any]"))
    lines = [f"class {_common_fields_name(obj_type)}(TypedDict, total=False):"]
    lines.extend(f"    {name}: {py_type}" for name, py_type in common)
    if not common:
        lines[-1] += " ..."
    lines.append("")
    lines += _generate_object_class(
        schema,
        obj_type,
        type_since=type_since,
        field_since=field_since,
        cls_name=base,
        class_doc=f"``{obj_type}`` as every supported EnergyPlus version declares it.",
        skip_fields=frozenset(schema.get_field_names(obj_type)) - frozenset(layout.fields),
        omit_group=not layout.group,
        emit_update=False,
        undocumented=layout.varying,
    )
    widened = {
        f"    {name}: {latest[name]} | None": f"    {name}: {merged} | None" for name, merged in layout.fields.items()
    }
    return [widened.get(line, line) for line in lines]


def _run_suffix(run: list[Version]) -> str:
    """Class-name suffix for a version range that does not reach the latest release."""
    if len(run) == 1:
        return f"_v{_version_tag(run[0])}"
    return f"_v{_version_tag(run[0])}_to_v{_version_tag(run[-1])}"


def _common_object_types() -> list[str]:
    """Object types present in every supported version, in latest-schema order."""
    sets = [set(get_schema(ver).object_types) for ver in SUPPORTED.versions]
    common: set[str] = sets[0].intersection(*sets[1:])
    return [t for t in get_schema(SUPPORTED.latest).object_types if t in common]


def _generate_common_type_map() -> list[str]:
    """Generate the map behind :class:`AnyIDFDocument`: every type present in all versions.

    Each entry is ``ReadOnly[IDFCollection[<the type as every version has it>]]``. Read-only entries
    are covariant, and so is ``IDFCollection``, so the map of every version-specific document is
    assignable to it: one annotation accepts a document of any version, and code written against it
    sees exactly the fields it can rely on in all of them. A type that some version lacks cannot appear, because a document
    of that version would then be missing a required key.
    """
    lines = ['_CommonTypeMap = TypedDict("_CommonTypeMap", {']
    lines.extend(
        f'    "{obj_type}": ReadOnly[IDFCollection[{_shared_class_name(obj_type)}]],'
        for obj_type in _common_object_types()
    )
    lines.append("}, total=True)")
    return lines


def _typed_dict(name: str, entries: list[tuple[str, str]]) -> list[str]:
    """A ``TypedDict`` mapping each object type to a collection of its class.

    Class syntax when every key is an identifier, as ruff (UP013) requires; the functional form
    otherwise, since most object types contain a colon.
    """
    if all(key.isidentifier() and not keyword.iskeyword(key) for key, _ in entries):
        lines = [f"class {name}(TypedDict, total=True):"]
        lines.extend(f"    {key}: IDFCollection[{cls}]" for key, cls in entries)
        if not entries:
            lines[0] += " ..."
        return lines
    lines = [f'{name} = TypedDict("{name}", {{']
    lines.extend(f'    "{key}": IDFCollection[{cls}],' for key, cls in entries)
    lines.append("}, total=True)")
    return lines


Span = tuple[Version, Version]


def _span_name(prefix: str, span: Span) -> str:
    """``_Types_v8_9_to_v9_4``: a name for what holds from the first version of *span* to the last."""
    first, last = span
    if first == last:
        return f"{prefix}_v{_version_tag(first)}"
    return f"{prefix}_v{_version_tag(first)}_to_v{_version_tag(last)}"


def _group_by_span(per_version: dict[Version, dict[str, str]]) -> dict[Span, dict[str, str]]:
    """File every ``(key, value)`` pair under each maximal run of consecutive versions holding it.

    This is the endpoint encoding: a pair that holds from 8.9 to 9.4 is written once, under
    ``(8.9, 9.4)``, rather than once per version. A pair that stops and starts again is filed
    under each run, so the result is right whether or not every range is contiguous.
    """
    spans: dict[Span, dict[str, str]] = {}
    started: dict[tuple[str, str], Version] = {}
    previous: Version | None = None
    for ver in SUPPORTED.versions:
        pairs = set(per_version.get(ver, {}).items())
        for pair in [p for p in started if p not in pairs]:
            assert previous is not None  # noqa: S101 - a started pair has a previous version
            spans.setdefault((started.pop(pair), previous), {})[pair[0]] = pair[1]
        for pair in pairs:
            started.setdefault(pair, ver)
        previous = ver
    for pair, first in started.items():
        assert previous is not None  # noqa: S101
        spans.setdefault((first, previous), {})[pair[0]] = pair[1]
    return {span: dict(sorted(spans[span].items())) for span in sorted(spans)}


@functools.cache
def _class_assignment() -> tuple[dict[tuple[str, Version], str], tuple[tuple[str, tuple[Version, ...]], ...]]:
    """Which class types each object type in each version, and the older ranges that need one.

    Returns:
        ``(class_for, older_runs)``: *class_for* maps ``(obj_type, version)`` to a class name, the
        latest class (qualified ``_g.``) when the version declares the type as the latest release does; *older_runs*
        lists every ``(obj_type, versions)`` range that does not reach the latest release.
    """
    class_for: dict[tuple[str, Version], str] = {}
    older_runs: list[tuple[str, tuple[Version, ...]]] = []
    for obj_type, type_runs in _build_type_runs().items():
        for run in type_runs:
            if SUPPORTED.latest in run:
                cls = f"_g.{_to_class_name(obj_type)}"
            else:
                cls = _to_class_name(obj_type) + _run_suffix(run)
                older_runs.append((obj_type, tuple(run)))
            for ver in run:
                class_for[(obj_type, ver)] = cls
    return class_for, tuple(older_runs)


def _accessors(ver: Version) -> dict[str, str]:
    """The typed attribute accessors of a document of *ver*: name -> object type."""
    from idfkit.document import _build_resolver  # pyright: ignore[reportPrivateUsage]

    return _build_resolver(get_schema(ver)).accessors()


def _document_class_name(ver: Version) -> str:
    """``IDFDocumentV9_4``. Major and minor identify every supported release; checked when generating."""
    return f"IDFDocumentV{_version_tag(ver)}"


def _check_version_tags() -> None:
    """Refuse a version list in which two releases would share a document type name."""
    tags = [_version_tag(ver) for ver in SUPPORTED.versions]
    duplicates = sorted({tag for tag in tags if tags.count(tag) > 1})
    if duplicates:
        msg = f"Releases share a major.minor, so their document types would share a name: {duplicates}"
        raise ValueError(msg)


def generate_versioned_pyi() -> str:
    """Generate ``versioned.pyi``: an ``IDFDocument`` type for every supported older version.

    Everything below is derived from ``SUPPORTED.versions`` and the bundled schemas, so adopting
    a release is a regeneration: the previous latest release gains its own document type here,
    and a range of an older type that ends before the latest release keeps its name for good.

    * A type declared in some version exactly as in the latest release reuses the latest class
      from ``_generated_types``. Every other range of versions declaring a type alike gets one
      class here, named by its endpoints, deriving from the type's shared base.
    * A version's ``TypedDict`` map, and its typed attribute accessors, are assembled from pieces
      each filed under the version range they hold over, so each entry is written once.
    """
    _check_version_tags()
    layout = _shared_layout()
    class_for, older_runs = _class_assignment()
    older = [ver for ver in SUPPORTED.versions if ver != SUPPORTED.latest]

    parts: list[str] = [
        '"""Auto-generated ``IDFDocument`` types for each older EnergyPlus version.',
        "",
        "DO NOT EDIT — regenerate with:",
        "    python -m idfkit.codegen.generate_stubs",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from collections.abc import Mapping",
        "from typing import Any, Literal, TypedDict, TypeVar",
        "",
        "from typing_extensions import Unpack",
        "",
        "from . import _generated_types as _g",
        "from .document import AnyIDFDocument as AnyIDFDocument",
        "from .document import IDFDocument, Strict, _IDFDocumentMethods",
        "from .objects import ExtensibleGroup, ExtensibleList, IDFCollection, IDFObject",
        "",
        "# =========================================================================",
        "# Object classes of the version ranges that end before the latest release",
        "# =========================================================================",
        "",
    ]
    for obj_type, run in older_runs:
        schema = get_schema(run[-1])
        span = version_string(run[0]) if len(run) == 1 else f"{version_string(run[0])} to {version_string(run[-1])}"
        doc = f"``{obj_type}`` as declared in EnergyPlus {span}."
        memo = schema.get_object_memo(obj_type)
        if memo:
            doc = f"{doc} {_truncate_text(memo)}"
        shared = layout.get(obj_type)
        parts.extend(
            _generate_object_class(
                schema,
                obj_type,
                suffix=_run_suffix(list(run)),
                class_doc=doc,
                base=f"_g.{_shared_class_name(obj_type)}" if shared else "IDFObject",
                skip_fields=shared.identical if shared else frozenset(),
                omit_group=shared.group if shared else False,
                fields_base=f"_g.{_common_fields_name(obj_type)}" if shared else "TypedDict",
            )
        )
        parts.append("")

    # A piece that only the latest release holds is never used here: IDFDocument has its own map.
    def used(span: Span) -> bool:
        return span[0] != SUPPORTED.latest

    type_spans = _group_by_span({
        ver: {t: class_for[(t, ver)] for t in get_schema(ver).object_types} for ver in SUPPORTED.versions
    })
    accessor_types = {ver: _accessors(ver) for ver in SUPPORTED.versions}
    accessor_spans = _group_by_span({
        ver: {name: class_for[(t, ver)] for name, t in accessor_types[ver].items()} for ver in SUPPORTED.versions
    })

    parts.extend([
        "# =========================================================================",
        "# Object-type maps, one piece per version range",
        "# =========================================================================",
        "",
    ])
    for span, entries in type_spans.items():
        if used(span):
            parts.extend(_typed_dict(_span_name("_Types", span), list(entries.items())))
            parts.append("")

    parts.extend([
        "# =========================================================================",
        "# Attribute accessors, one piece per version range",
        "# =========================================================================",
        "",
    ])
    for span, entries in accessor_spans.items():
        if not used(span):
            continue
        parts.append(f"class {_span_name('_Accessors', span)}:")
        for name, cls in entries.items():
            parts.append("    @property")
            parts.append(f"    def {name}(self) -> IDFCollection[{cls}]: ...")
        parts.append("")

    parts.extend([
        "# =========================================================================",
        "# Document types",
        "# =========================================================================",
        "",
    ])
    for ver in older:
        tag = _version_tag(ver)
        maps = [_span_name("_Types", span) for span in type_spans if span[0] <= ver <= span[1]]
        mixins = [_span_name("_Accessors", span) for span in accessor_spans if span[0] <= ver <= span[1]]
        parts.append(f"class _ObjectTypeMapV{tag}({', '.join(maps)}): ...")
        parts.append("")
        bases = ", ".join([f"_ObjectTypeMapV{tag}", *mixins, "_IDFDocumentMethods[Strict]"])
        parts.append(f"class {_document_class_name(ver)}({bases}):  # type: ignore[misc]")
        parts.append(f'    """An :class:`~idfkit.document.IDFDocument` typed for EnergyPlus {version_string(ver)}."""')
        parts.append("")
    parts.append(f"{_document_class_name(SUPPORTED.latest)} = IDFDocument")
    parts.append("")
    parts.append('_D = TypeVar("_D", bound=AnyIDFDocument)')
    parts.append("")
    parts.extend(
        _format_def_with_doc("def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D", _AS_VERSION_DOC)
    )
    parts.append("")
    return "\n".join(parts)


def generate_versioned_py() -> str:
    """Generate ``versioned.py``, the run-time half of ``versioned.pyi``.

    At run time a per-version type is a stand-in: ``isinstance`` holds for a document of that
    version, and :func:`idfkit.versioned.as_version` checks against it. The classes with fields
    exist only for type checkers.
    """
    _check_version_tags()
    names = [_document_class_name(ver) for ver in SUPPORTED.versions]
    lines = [
        '"""Document types for each supported EnergyPlus version.',
        "",
        "Each ``IDFDocumentV<major>_<minor>`` types a document as that release declares its objects,",
        "for type checkers; ``IDFDocument`` is the latest release's. See ``versioned.pyi``.",
        "",
        "DO NOT EDIT — regenerate with:",
        "    python -m idfkit.codegen.generate_stubs",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from ._document_types import as_version, document_type",
        "from .document import AnyIDFDocument, IDFDocument",
        "",
        "__all__ = [",
        '    "AnyIDFDocument",',
        *(f'    "{name}",' for name in names),
        '    "as_version",',
        "]",
        "",
    ]
    for ver in SUPPORTED.versions:
        if ver == SUPPORTED.latest:
            lines.append(f"{_document_class_name(ver)} = IDFDocument")
        else:
            lines.append(f'{_document_class_name(ver)} = document_type("{_document_class_name(ver)}", {ver!r})')
    lines.append("")
    return "\n".join(lines)


_AS_VERSION_DOC = """Type *doc* as a document of the EnergyPlus version *document_type* stands for.

Returns *doc* itself. A document's version is read from its file, so a type checker cannot
know it; this states it, and checks it at run time.

Args:
    doc: A document of any supported version.
    document_type: ``IDFDocument`` for the latest release, or one of the
        ``IDFDocumentV<major>_<minor>`` types of this module.

Returns:
    *doc*, typed as *document_type*.

Raises:
    TypeError: If *doc* is not a document of that version.

Examples:
    ```python
    from idfkit import load_idf
    from idfkit.versioned import IDFDocumentV9_4, as_version

    model = as_version(load_idf("legacy.idf"), IDFDocumentV9_4)
    model["Zone"].first()  # typed as Zone was declared in 9.4
    ```
"""


def _format_def_with_doc(signature: str, doc: str) -> list[str]:
    """A top-level ``def`` whose body is its docstring."""
    return [f"{signature}:", *_format_docstring_for_stub(doc, "    ")]


# ---- main generation -------------------------------------------------------


def _as_latest(version: Version | None) -> contextlib.AbstractContextManager[None]:
    """Describe the releases up to *version*, or all of them when it is ``None`` or the latest."""
    if version is None or version == SUPPORTED.latest:
        return contextlib.nullcontext()
    return supported_up_to(version)


def generate_stubs(version: tuple[int, int, int] | None = None) -> str:
    """Generate the full ``_generated_types.pyi`` content.

    Args:
        version: The release to type ``IDFDocument`` for, as if it were the newest supported;
            defaults to the latest release.

    Returns:
        Complete Python source for the generated types module.
    """
    with _as_latest(version):
        return _generate_types_module()


def _generate_types_module() -> str:
    ver = SUPPORTED.latest
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
    parts.append("from collections.abc import Mapping")
    parts.append("from typing import Any, Literal, TypedDict")
    parts.append("")
    parts.append("from typing_extensions import ReadOnly, Unpack")
    parts.append("")
    parts.append("from .objects import ExtensibleGroup, ExtensibleList, IDFCollection, IDFObject")
    parts.append("")
    parts.append("# =========================================================================")
    parts.append("# Typed object classes (one per EnergyPlus object type)")
    parts.append("# =========================================================================")
    parts.append("")

    # Generate all typed object classes at top-level
    # A type some older version declares differently gets a private base holding what every
    # version shares; the older versions' classes in versioned.pyi derive from it too.
    layout = _shared_layout()
    for obj_type in schema.object_types:
        if obj_type in layout:
            parts.extend(_generate_base_class(schema, obj_type, layout[obj_type], type_since, field_since))
            parts.append("")
            class_lines = _generate_object_class(
                schema,
                obj_type,
                type_since=type_since,
                field_since=field_since,
                base=_shared_class_name(obj_type),
                skip_fields=layout[obj_type].identical,
                omit_group=layout[obj_type].group,
                fields_base=_common_fields_name(obj_type),
            )
        else:
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
    parts.extend(_generate_common_type_map())
    parts.append("")

    return "\n".join(parts)


_ANY_DOCUMENT_DOC = """A document of any supported EnergyPlus version.

:class:`IDFDocument`, typed for the latest release, and every older release's type in
:mod:`idfkit.versioned` are assignable to it, so annotate with it to accept a document whatever
its version. Through it, a document offers what every supported version has: the object types
present in all of them, each typed as all of them declare it, so a field whose choices changed
between releases reads as the union of them and a field some release lacks is not offered.
"""

_ANY_VERSION_DOCUMENT_DOC = """A document as every supported EnergyPlus version has it.

Indexing it, or reaching an accessor, with an object type that some supported version lacks is a
type error, as is a field some version lacks through ``update``. Annotate with ``AnyIDFDocument``,
the union of this and ``IDFDocument``, rather than with this class: a latest-release document then
matches ``IDFDocument`` directly. Narrow a document to its release with
``idfkit.versioned.as_version`` to reach what only that release has.
"""


def _generate_any_accessors() -> list[str]:
    """Typed accessors of ``AnyIDFDocument``: names that reach the same type in every version."""
    per_version = [_accessors(ver) for ver in SUPPORTED.versions]
    common = set(_common_object_types())
    lines: list[str] = []
    for name, obj_type in per_version[-1].items():
        if obj_type in common and all(accessors.get(name) == obj_type for accessors in per_version):
            lines.append("    @property")
            lines.append(f"    def {name}(self) -> IDFCollection[{_shared_class_name(obj_type)}]: ...")
    return lines


def generate_document_pyi(version: tuple[int, int, int] | None = None) -> str:
    """Generate ``document.pyi`` — a type stub for ``document.py``.

    The stub declares ``IDFDocument`` as inheriting from ``_ObjectTypeMap``
    (a ``TypedDict``), which gives pyright O(1) per-key type resolution for
    ``__getitem__`` without any ``@overload`` decorators.

    Method and property docstrings are extracted from ``document.py`` via AST
    so IDE hovers (which read from the ``.pyi`` when one exists) surface the
    same documentation as the source module.
    """
    with _as_latest(version):
        return _generate_document_module()


def _generate_document_module() -> str:
    ver = SUPPORTED.latest
    version_str = f"{ver[0]}.{ver[1]}.{ver[2]}"
    schema = get_schema(ver)

    import idfkit.document as _document_mod
    from idfkit.document import _build_resolver  # pyright: ignore[reportPrivateUsage]

    # Resolve document.py via the imported module rather than this file's
    # location, so test fixtures that patch __file__ on the codegen module
    # don't redirect docstring extraction to a non-existent path.
    source_path = Path(_document_mod.__file__).resolve()
    docs = _extract_class_docstrings(source_path, "IDFDocument")

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
    lines.append("from typing import Any, Generic, TypeAlias, TypeVar")
    lines.append("")
    lines.append("from typing_extensions import Self")
    lines.append("")
    lines.append("from ._accessors import AccessorResolver")
    lines.append("from ._compat import EppyDocumentMixin")
    lines.append("from ._generated_types import *  # noqa: F403")
    lines.append("from ._generated_types import _CommonTypeMap, _ObjectTypeMap")
    # Alphabetical, because the formatter that runs after this sorts them and the stub gate then
    # regenerates and diffs. An import emitted out of order is reordered on the way in and never
    # matches on the way back, which fails the gate everywhere except the machine that committed it.
    lines.append("from .cst import DocumentCST, SourceSpan")
    lines.append("from .introspection import ObjectDescription")
    lines.append("from .objects import IDFCollection, IDFObject")
    lines.append("from .references import ReferenceGraph")
    lines.append("from .schema import EpJSONSchema")
    lines.append("from .simulation.config import EnergyPlusConfig")
    lines.append("from .writers import FieldComments")
    lines.append("")
    lines.append("Strict = TypeVar('Strict', bound=bool, default=bool, covariant=True)")
    lines.append("")
    lines.append("_PYTHON_TO_IDF: dict[str, str]")
    lines.append("_IDF_TO_PYTHON: dict[str, str]")
    lines.append("_RESERVED: frozenset[str]")
    lines.append("")
    lines.append("def _build_resolver(schema: EpJSONSchema) -> AccessorResolver: ...")
    lines.append("")

    # The methods live on a plain mixin so that every document type -- the latest one, each older
    # version's, and AnyIDFDocument -- shares them while carrying its own TypedDict map.
    lines.append("class _IDFDocumentMethods(EppyDocumentMixin, Generic[Strict]):")
    lines.append("    filepath: Path | None")
    # Read by the writers and set by the epJSON parser; declared so it has its real type, since no
    # __getattr__ on this base answers undeclared names.
    lines.append("    _count_at_read: int | None")
    lines.append("")

    def emit(
        signature: str,
        doc_key: str,
        *,
        decorators: tuple[str, ...] = (),
        suffix: str = "",
    ) -> None:
        _emit_method(
            lines,
            signature,
            docs.get(doc_key),
            decorators=decorators,
            indent="    ",
            suffix=suffix,
        )

    # Properties
    emit("def version(self) -> tuple[int, int, int]", "IDFDocument.version", decorators=("@property",))
    emit("def strict(self) -> Strict", "IDFDocument.strict", decorators=("@property",))
    emit("def schema(self) -> EpJSONSchema | None", "IDFDocument.schema", decorators=("@property",))
    emit("def cst(self) -> DocumentCST | None", "IDFDocument.cst", decorators=("@property",))
    emit("def raw_text(self) -> str | None", "IDFDocument.raw_text", decorators=("@property",))
    emit(
        "def collections(self) -> dict[str, IDFCollection[IDFObject]]",
        "IDFDocument.collections",
        decorators=("@property",),
    )
    emit("def references(self) -> ReferenceGraph", "IDFDocument.references", decorators=("@property",))
    emit("def changed_objects(self) -> Iterator[IDFObject]", "IDFDocument.changed_objects")
    emit("def region_of(self, obj: IDFObject) -> SourceSpan | None", "IDFDocument.region_of")
    emit(
        'def render_object(self, obj: IDFObject, *, field_comments: FieldComments = "preserve") -> str | None',
        "IDFDocument.render_object",
    )
    lines.append("")

    # Collection access
    emit("def get_collection(self, obj_type: str) -> IDFCollection[IDFObject]", "IDFDocument.get_collection")
    emit(
        "def __contains__(self, obj_type: str) -> bool",
        "IDFDocument.__contains__",
        suffix="  # type: ignore[override]",
    )
    emit("def __iter__(self) -> Iterator[str]", "IDFDocument.__iter__", suffix="  # type: ignore[override]")
    emit("def __len__(self) -> int", "IDFDocument.__len__")
    emit("def keys(self) -> list[str]", "IDFDocument.keys", suffix="  # type: ignore[override]")
    emit(
        "def values(self) -> list[IDFCollection[IDFObject]]",
        "IDFDocument.values",
        suffix="  # type: ignore[override]",
    )
    emit(
        "def items(self) -> list[tuple[str, IDFCollection[IDFObject]]]",
        "IDFDocument.items",
        suffix="  # type: ignore[override]",
    )
    emit("def describe(self, obj_type: str) -> ObjectDescription", "IDFDocument.describe")
    lines.append("")

    # Object manipulation
    emit(
        "def add(self, obj_type: str, name: str = ..., fields: dict[str, Any] | None = ..., "
        "*, validate: bool = ..., **kwargs: Any) -> IDFObject",
        "IDFDocument.add",
    )
    emit("def addidfobject(self, obj: IDFObject) -> IDFObject", "IDFDocument.addidfobject")
    emit("def removeidfobject(self, obj: IDFObject) -> None", "IDFDocument.removeidfobject")
    emit("def rename(self, obj_type: str, old_name: str, new_name: str) -> None", "IDFDocument.rename")
    emit(
        "def notify_name_change(self, obj: IDFObject, old_name: str, new_name: str) -> None",
        "IDFDocument.notify_name_change",
    )
    emit(
        "def notify_reference_change(self, obj: IDFObject, field_name: str, old_value: Any, new_value: Any) -> None",
        "IDFDocument.notify_reference_change",
    )
    emit("def get_referencing(self, name: str) -> set[IDFObject]", "IDFDocument.get_referencing")
    emit("def get_references(self, obj: IDFObject) -> set[str]", "IDFDocument.get_references")

    # Schedules / surfaces / iteration / expand / copy
    emit(
        "def schedules_dict(self) -> dict[str, IDFObject]",
        "IDFDocument.schedules_dict",
        decorators=("@property",),
    )
    emit("def get_schedule(self, name: str) -> IDFObject | None", "IDFDocument.get_schedule")
    emit("def get_used_schedules(self) -> set[str]", "IDFDocument.get_used_schedules")
    emit(
        "def get_zone_surfaces(self, zone_name: str) -> list[IDFObject]",
        "IDFDocument.get_zone_surfaces",
    )
    emit(
        "def all_objects(self) -> Iterator[IDFObject]",
        "IDFDocument.all_objects",
        decorators=("@property",),
    )
    emit(
        "def objects_by_type(self) -> Iterator[tuple[str, IDFCollection[IDFObject]]]",
        "IDFDocument.objects_by_type",
    )
    emit(
        "def expand(self, *, energyplus: EnergyPlusConfig | None = ..., timeout: float = ...) -> Self",
        "IDFDocument.expand",
    )
    emit("def copy(self) -> Self", "IDFDocument.copy")
    lines.append("")

    # Class definition — inherit from _ObjectTypeMap (TypedDict) for __getitem__ dispatch
    lines.append("class IDFDocument(_ObjectTypeMap, _IDFDocumentMethods[Strict]):  # type: ignore[misc]")
    cls_doc = docs.get("IDFDocument")
    if cls_doc:
        lines.extend(_format_docstring_for_stub(cls_doc, "    "))
        lines.append("")

    # __init__ — emit multi-line for readability, then attach docstring if present
    init_doc = docs.get("IDFDocument.__init__")
    lines.append("    def __init__(")
    lines.append("        self,")
    lines.append("        version: tuple[int, int, int] | None = ...,")
    lines.append("        schema: EpJSONSchema | None = ...,")
    lines.append("        filepath: Path | str | None = ...,")
    lines.append("        *,")
    lines.append("        strict: Strict = ...,")
    if init_doc:
        lines.append("    ) -> None:")
        lines.extend(_format_docstring_for_stub(init_doc, "        "))
    else:
        lines.append("    ) -> None: ...")
    lines.append("")

    # The untyped fallback for the raw spellings (doc.Site_Location) is IDFDocument's alone. On the
    # shared methods base it would also answer, silently and untyped, every accessor that a
    # version-specific document type or IDFDocumentAllVersions leaves out because that type is
    # missing from the version, where at run time the access raises.
    _emit_method(
        lines,
        "def __getattr__(self, name: str) -> IDFCollection[IDFObject]",
        docs.get("IDFDocument.__getattr__"),
        indent="    ",
    )
    lines.append("")

    # Attribute accessor properties, one per object type plus the shorthands, with memo docstrings
    lines.extend(_generate_attr_properties(_build_resolver(schema).accessors(), schema, indent="    "))
    lines.append("")

    # AnyIDFDocument is a union whose first member is IDFDocument. Both checkers compare TypedDicts
    # key by key and pyright does not remember the outcome, so an annotation of the version-agnostic
    # class alone would cost every call that passes a latest-release document ~800 comparisons.
    # Through the union, such a document matches IDFDocument directly.
    # Its name is what a type checker prints when code reaches for an object type or an accessor some
    # supported version lacks ("... is not a defined key in IDFDocumentAllVersions[bool]"), so it
    # says what the type is rather than being private.
    lines.append("class IDFDocumentAllVersions(_CommonTypeMap, _IDFDocumentMethods[Strict]):  # type: ignore[misc]")
    lines.extend(_format_docstring_for_stub(_ANY_VERSION_DOCUMENT_DOC, "    "))
    lines.append("")
    lines.extend(_generate_any_accessors())
    lines.append("")
    lines.append("AnyIDFDocument: TypeAlias = IDFDocument[Strict] | IDFDocumentAllVersions[Strict]")
    lines.extend(_format_docstring_for_stub(_ANY_DOCUMENT_DOC, ""))
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point."""
    version: tuple[int, int, int] | None = None
    if len(sys.argv) > 1:
        version_parts = sys.argv[1].split(".")
        version = (int(version_parts[0]), int(version_parts[1]), int(version_parts[2]))

    with _as_latest(version):
        _write_stubs(Path(__file__).resolve().parent.parent)


def _write_stubs(base_path: Path) -> None:
    """Write, format and verify every generated stub under *base_path* (``src/idfkit``)."""
    content = _generate_types_module()
    doc_pyi = _generate_document_module()

    types_path = base_path / "_generated_types.pyi"
    types_path.write_text(content, encoding="utf-8")

    pyi_path = base_path / "document.pyi"
    pyi_path.write_text(doc_pyi, encoding="utf-8")

    versioned_path = base_path / "versioned.pyi"
    versioned_path.write_text(generate_versioned_pyi(), encoding="utf-8")

    versioned_runtime_path = base_path / "versioned.py"
    versioned_runtime_path.write_text(generate_versioned_py(), encoding="utf-8")

    # Run ruff format so regenerated stubs match the committed (ruff-formatted) versions
    import subprocess

    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            str(types_path),
            str(pyi_path),
            str(versioned_path),
            str(versioned_runtime_path),
        ],
        check=False,
    )
    from idfkit.codegen.verify_stubs import verify

    problems = verify(
        types_path.read_text(encoding="utf-8"),
        pyi_path.read_text(encoding="utf-8"),
        versioned_path.read_text(encoding="utf-8"),
        SUPPORTED.versions,
    )
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"The generated stubs misdescribe {len(problems)} version-specific declarations.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Generated {types_path} ({types_path.stat().st_size:,} bytes)")
    print(f"Generated {pyi_path} ({pyi_path.stat().st_size:,} bytes)")
    print(f"Generated {versioned_path} ({versioned_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
