"""Generate type stubs from EnergyPlus epJSON schemas.

This module generates ``_generated_types.pyi`` containing typed subclasses of IDFObject for every
EnergyPlus object type, and ``document.pyi``, ``versioned.pyi`` and ``_versioned/`` containing the
document types: each types ``doc["Zone"]`` with one ``__getitem__`` overload per object type
(:func:`_generate_getitem`) and carries typed attribute accessors.

The generated files are designed to be committed and shipped with the package.
The ``.pyi`` files are stubs — they have zero runtime cost by design.

Usage::

    python -m idfkit.codegen.generate_stubs          # latest version
    python -m idfkit.codegen.generate_stubs 24.1.0   # specific version
"""

from __future__ import annotations

import ast
import contextlib
import dataclasses
import functools
import re
import sys
import textwrap
import zlib
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, TypeAlias

from idfkit.docs import io_reference_url
from idfkit.schema import EpJSONSchema, get_schema, trailing_underscore_aliases
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
    for cached in (
        _build_type_runs,
        _shared_layout,
        _merged_groups,
        _class_assignment,
        _accessor_spans,
        _release_creation,
        _creation_pieces,
        _piece_classes,
        read_required,
    ):
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
    # The empty string is how a schema lets a choice be left blank; a blank field is stored as
    # absent and reads None (idfkit#183), so "" is never a value of the field.
    parts: list[str] = []
    for v in values:
        if isinstance(v, str):
            if v != "":
                parts.append(f'"{v}"')
        else:
            parts.append(repr(v))
    return f"Literal[{', '.join(parts)}]" if parts else "str"


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
                        if v != "":  # blank: stored as absent, so never read back (see _enum_to_literal)
                            literal_values.append(f'"{v}"')
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

# Every typed class derives from one of these stub-only bases instead of IDFObject / ExtensibleGroup.
# The runtime ``__getattr__``/``__setattr__`` take any ``str`` and return ``Any``, so a type checker
# would resolve any undeclared name through them and accept ``material.thermal_resistance = 1.0`` on
# a type that has no such field. Re-declaring both with a ``Never`` name turns that off: pyright
# reports every undeclared name, read or assigned, and mypy reports every undeclared assignment.
# Declared fields still resolve to their annotated types, because attribute lookup only falls back
# to ``__getattr__`` for names the class does not declare. ``__getattr__`` returns ``object``, not
# ``Never``: mypy does not check the name argument, and a ``Never`` read would fit anywhere and make
# mypy treat the code after ``obj.typo()`` as unreachable, while ``object`` makes it report each use.
# Plain ``IDFObject`` keeps the permissive signatures, so ``IDFCollection[IDFObject]`` is unaffected.
# ``typing.Never`` is 3.11+, hence ``typing_extensions``; the import only exists in the stub, which
# the type checker reads from its bundled typeshed, so it adds no runtime dependency.
#
# The ``Never`` is spelled through a type alias named for the mistake. pyright prints a parameter's
# alias, so a misspelled field reads ``parameter "key" of type "_NotAFieldOfThisObjectType"`` rather
# than ``of type "Never"``; mypy expands the alias, so what it reports is unchanged.
_TYPED_OBJECT_BASE = "_TypedIDFObject"
_TYPED_GROUP_BASE = "_TypedExtensibleGroup"
_NOT_A_FIELD = "_NotAFieldOfThisObjectType"
_NOT_A_GROUP_FIELD = "_NotAFieldOfThisExtensibleGroup"
# A type without a Name field takes no name. Its creation signature has a positional-only parameter
# typed with this alias of ``Never``, which nothing satisfies, so a name passed by mistake
# (``doc.output_variables.add("*", ...)``) reads ``parameter "this_type_has_no_name_field" of type
# "_PassFieldsAsKeywords"`` under pyright, and ``expected "Never"`` under mypy, where both used to
# report the arguments instead (``Expected 0 positional arguments``; mypy's ``gets multiple values
# for keyword argument``, naming a field the call did pass).
_NO_NAME_FIELD = "_PassFieldsAsKeywords"
_NO_NAME_PARAM = "this_type_has_no_name_field"

# The document methods every document type shares, through IDFDocumentAllVersions, which every
# document type derives from (_generate_document_module).
_METHODS_BASE = "_IDFDocumentMethods[Strict]"
_ALL_VERSIONS_BASE = "IDFDocumentAllVersions[Strict]"


def _generate_typed_bases() -> list[str]:
    """Emit the stub-only base classes that turn off the catch-all attribute access."""
    return [
        f"{_NOT_A_FIELD}: TypeAlias = Never",
        '"""No name is one: a type checker reports an undeclared field of a typed object against this type."""',
        "",
        f"{_NOT_A_GROUP_FIELD}: TypeAlias = Never",
        '"""No name is one: a type checker reports an undeclared field of a typed group against this type."""',
        "",
        f"{_NO_NAME_FIELD}: TypeAlias = Never",
        '"""No value is one: a type checker reports a name given to a type without a Name field against this."""',
        "",
        f"class {_TYPED_OBJECT_BASE}(IDFObject):",
        '    """Stub-only base: an undeclared field name is a type error on a typed object."""',
        "",
        f"    def __getattr__(self, key: {_NOT_A_FIELD}) -> object: ...",
        f"    def __setattr__(self, key: {_NOT_A_FIELD}, value: {_NOT_A_FIELD}) -> None: ...",
        "",
        f"class {_TYPED_GROUP_BASE}(ExtensibleGroup):",
        '    """Stub-only base: an undeclared field name is a type error on a typed extensible group."""',
        "",
        f"    def __getattr__(self, name: {_NOT_A_GROUP_FIELD}) -> object: ...",
        f"    def __setattr__(self, name: {_NOT_A_GROUP_FIELD}, value: {_NOT_A_GROUP_FIELD}) -> None: ...",
        "",
    ]


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
    base: str = _TYPED_OBJECT_BASE,
    group_base: str = _TYPED_GROUP_BASE,
    skip_fields: frozenset[str] = frozenset(),
    omit_group: bool = False,
    fields_base: str = "TypedDict",
    emit_update: bool = True,
    undocumented: frozenset[str] = frozenset(),
    properties: Mapping[str, tuple[str, str]] | None = None,
    inherited: Iterable[tuple[str, str]] = (),
    sink: _CreationModules | None = None,
    creation: _Creation | None = None,
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
        base: The class's base, ``_TypedIDFObject`` unless the fields it shares with other versions
            live on a per-type base class.
        group_base: The extensible group class's base, ``_TypedExtensibleGroup`` as reached from
            the module the class is emitted in.
        skip_fields: Fields left to *base*.
        omit_group: Leave the extensible group and its wrapper attribute to *base* (or out).
        fields_base: The ``TypedDict`` that ``update``'s keyword ``TypedDict`` extends.
        emit_update: Whether to type ``update`` on this class.
        undocumented: Fields declared without a docstring.
        properties: Fields declared as a property instead of an attribute, each with the value type
            reading it gives and the one assigning to it accepts (see :func:`_generate_base_class`).
        inherited: The ``update`` keywords *fields_base* already holds, with their annotations; with
            the class's own, they make its ``_creation_signature`` (:func:`_creation_lines`).
        sink: Where the creation signature is filed; a throwaway one when ``None``.
        creation: How the class creates its objects (:func:`_class_creation`); *schema*'s release's
            own when ``None``.
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
        group_cls_name = _group_class_name(obj_type, wrapper_key, suffix)
        lines.extend(_generate_group_class(group_cls_name, cls_name, wrapper_key, ext_inner_props, indent, group_base))

    lines.append(f"{indent}class {cls_name}({base}):")

    body_indent = indent + "    "

    # Add object-level docstring from schema memo + version info
    obj_since = type_since.get(obj_type) if type_since else None
    cls_doc = class_doc if class_doc is not None else _class_docstring(schema.get_object_memo(obj_type), obj_since)
    has_body = False
    if cls_doc:
        lines.append(f'{body_indent}"""{cls_doc}"""')
        has_body = True

    inherited = list(inherited)
    sink = sink if sink is not None else _CreationModules()
    creation = creation if creation is not None else _creation_info(schema, obj_type)
    if not field_names and not group_cls_name:
        if not emit_update:
            lines[-1:] = [lines[-1], ""] if has_body else [f"{indent}class {cls_name}({base}): ..."]
            return lines
        declared = _creation_lines(
            cls_name, _in_field_order(schema, obj_type, inherited), creation, body_indent, sink, schema, obj_type
        )
        if fields_base != "TypedDict":
            # Every field is on the shared base, but update still takes them all as keywords.
            lines.extend(_generate_update(cls_name, [], indent, fields_base, declared))
        else:
            # No field at all (a type with only a name): update stays IDFObject's, add() takes the name.
            lines.extend(["", *declared])
        return lines

    update_fields: list[tuple[str, str]] = []
    if field_names:
        update_fields = _generate_fields(
            lines, schema, obj_type, field_names, body_indent, obj_since, field_since, undocumented, properties
        )

    # Add the canonical wrapper attribute typed as ExtensibleList[<GroupCls>].
    if group_cls_name and wrapper_key:
        lines.append(f"{body_indent}{wrapper_key}: ExtensibleList[{group_cls_name}]")
        update_fields.append((wrapper_key, _group_items(group_cls_name)))

    if emit_update:
        declared = _creation_lines(
            cls_name,
            _in_field_order(schema, obj_type, [*inherited, *update_fields]),
            creation,
            body_indent,
            sink,
            schema,
            obj_type,
        )
        lines.extend(_generate_update(cls_name, update_fields, indent, fields_base, declared))
    return lines


def _in_field_order(schema: EpJSONSchema, obj_type: str, entries: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """*entries* (``update`` keywords) in *obj_type*'s field order, without ``name``; the group wrapper last."""
    order = {name: i for i, name in enumerate(_field_decls(schema, obj_type))}
    # The first entry for a name wins: a release whose key ends in "_" (9.0's
    # construction_with_shading_name_) declares its alias, which the shared base already holds.
    kept = dict(reversed([(name, annotation) for name, annotation in entries if name != "name"]))
    return sorted(kept.items(), key=lambda entry: order.get(entry[0], len(order)))


def _group_class_name(obj_type: str, wrapper_key: str, suffix: str = "") -> str:
    """``BuildingSurfaceDetailedVerticesGroup``: the group class of *obj_type*'s extensible group."""
    return f"{_to_class_name(obj_type)}{_to_class_name(wrapper_key.title())}Group{suffix}"


def _group_item_name(group_cls: str) -> str:
    """``BuildingSurfaceDetailedVerticesItem``: the dict type of one group of *group_cls*."""
    head, _, tail = group_cls.rpartition("Group")
    return f"{head}Item{tail}"


def _group_items(group_cls: str, prefix: str = "") -> str:
    """The value of a group's wrapper keyword in ``update`` and ``add``: a sequence of its groups.

    Each is a dict, typed by the group's item type (:func:`_group_item_class`), so a misspelled key
    or a wrong value is a type error, or a group object (``list(wall.vertices)``), as the run time
    takes both. A ``Sequence``, not a ``list``: a ``list[<Item>]`` (what ``as_list()`` gives) or a
    list of groups is one, where an invariant ``list`` of the union would refuse both. *prefix*
    qualifies the names (``_g.``) as the module the annotation is written in reaches them.
    """
    return f"Sequence[{prefix}{_group_item_name(group_cls)} | {prefix}{group_cls}]"


def _group_item_class(group_cls: str, fields: Iterable[tuple[str, str]], indent: str = "") -> list[str]:
    """One group of *group_cls* as a dict: a ``TypedDict`` of its fields, each optional.

    It is public, so code that builds groups ahead of a call can annotate them
    (``points: list[BuildingSurfaceDetailedVerticesItem]``). *fields* are the group's fields with
    the value type writing one accepts.
    """
    fields = list(fields)
    lines = [
        f"{indent}class {_group_item_name(group_cls)}(TypedDict, total=False):",
        f'{indent}    """One group of :class:`{group_cls}` as a dict, as ``add()`` and ``update()`` take it."""',
        "",
    ]
    lines += [f"{indent}    {name}: {_or_none(value_type)}" for name, value_type in fields]
    lines.append("")
    return lines


def _generate_group_class(
    group_cls_name: str,
    cls_name: str,
    wrapper_key: str,
    inner_props: dict[str, Any],
    indent: str,
    group_base: str = _TYPED_GROUP_BASE,
) -> list[str]:
    """Generate the :class:`ExtensibleGroup` subclass of one extensible group, with its inner fields."""
    lines = [
        f"{indent}class {group_cls_name}({group_base}):",
        f'{indent}    """One {wrapper_key} group inside :class:`{cls_name}`."""',
    ]
    item_fields: list[tuple[str, str]] = []
    for inner_name, inner_schema in inner_props.items():
        if not inner_name.isidentifier():
            continue
        has_any_of = "anyOf" in inner_schema
        py_type = _schema_type_to_python(inner_schema, _schema_field_type(inner_schema), has_any_of)
        lines.append(f"{indent}    {inner_name}: {py_type} | None")
        item_fields.append((inner_name, py_type))
    lines.append(f"{indent}    def as_dict(self) -> {_group_item_name(group_cls_name)}: ...  # type: ignore[override]")
    lines.append("")
    lines += _group_item_class(group_cls_name, item_fields, indent)
    return lines


def _generate_update(
    cls_name: str,
    fields: list[tuple[str, str]],
    indent: str,
    fields_base: str = "TypedDict",
    creation: Iterable[str] = (),
) -> list[str]:
    """Type ``update`` on *cls_name* with a private ``TypedDict`` of its fields.

    The ``TypedDict`` types the keywords (through ``Unpack``), so a type checker reports an unknown
    field name or a wrongly typed value given as a keyword. ``name`` is left out because ``update``
    refuses it. The positional mapping stays ``Mapping[str, Any] | None``, as at run time: a
    ``TypedDict`` there would reject a mapping built at run time, ``None``, and the spaced field
    names single assignment accepts, all of which the method accepts. The override narrows
    ``IDFObject.update``'s ``**kwargs: Any``, which mypy reports; pyright does not.

    *creation* is the class's ``_creation_signature`` (:func:`_creation_lines`), emitted after it.
    """
    fields_cls = f"_{cls_name}Fields"
    lines = [
        "",
        f"{indent}    def update(self, values: Mapping[str, Any] | None = ..., /, **kwargs: Unpack[{fields_cls}]) "
        "-> None: ...  # type: ignore[override]",
        *creation,
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
    as_properties: Mapping[str, tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Append typed field declarations to *lines*; return each declared field with its value type.

    A field in *undocumented* gets no docstring, because the class that narrows it carries one. A
    field in *as_properties* is declared as a property, read and written with the two value types
    given for it, instead of as an attribute of its own value type.
    """
    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}
    as_properties = as_properties or {}
    declared: list[tuple[str, str]] = []

    for field_name in field_names:
        if not field_name.isidentifier():
            continue

        field_schema = properties.get(field_name)
        field_type = schema.get_field_type(obj_type, field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        py_type = _schema_type_to_python(field_schema, field_type, has_any_of)

        read_type = py_type if field_name in read_required().get(obj_type, ()) else f"{py_type} | None"
        if field_name in as_properties:
            lines.extend(_property_lines(field_name, *as_properties[field_name], indent, read_type == py_type))
        else:
            lines.append(f"{indent}{field_name}: {read_type}")
        declared.append((field_name, read_type))

        # Determine field "Since:" — only if the field appeared after the type itself
        fld_since: tuple[int, int, int] | None = None
        if field_since is not None and obj_since is not None:
            fld_ver = field_since.get((obj_type, field_name))
            if fld_ver is not None and fld_ver > obj_since:
                fld_since = fld_ver

        docstring = None if field_name in undocumented else _field_docstring(field_schema, since_version=fld_since)
        if docstring:
            lines.append(f'{indent}"""{docstring}"""')

    declared.extend(_generate_field_aliases(lines, field_names, dict(declared), indent, as_properties))
    return declared


def _property_lines(name: str, read: str, write: str, indent: str, required: bool = False) -> list[str]:
    """A field declared as a property: reading it gives *read* or ``None``, assigning to it accepts *write*.

    A *required* field (:func:`read_required`) reads *read* alone and is not cleared by assignment.
    """
    return [
        f"{indent}@property",
        f"{indent}def {name}(self) -> {read if required else read + ' | None'}: ...",
        f"{indent}@{name}.setter",
        f"{indent}def {name}(self, value: {write if required else _or_none(write)}) -> None: ...",
    ]


def _generate_field_aliases(
    lines: list[str],
    field_names: list[str],
    typed: dict[str, str],
    indent: str,
    as_properties: Mapping[str, tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Declare the spelling without the trailing underscore of each field whose key ends in ``_``.

    The runtime reaches such a field by both spellings (``IDFObject._field_key``), so the typed
    class declares both, or it would reject the one without the underscore. Emitted in field
    order, because the alias map's own order is not stable between runs. An alias in
    *as_properties* is declared as a property, as :func:`_generate_fields` declares a field.
    """
    as_properties = as_properties or {}
    alias_of = {
        key: alias
        for alias, key in trailing_underscore_aliases(field_names).items()
        if alias != key and alias.isidentifier() and alias not in typed
    }
    declared: list[tuple[str, str]] = []
    for key in field_names:
        alias = alias_of.get(key)
        if alias is not None and key in typed:
            if alias in as_properties:
                required = not typed[key].endswith("| None")
                lines.extend(_property_lines(alias, *as_properties[alias], indent, required))
            else:
                lines.append(f"{indent}{alias}: {typed[key]}")
                lines.append(f'{indent}"""Alias of :attr:`{key}`, the same field without the trailing underscore."""')
            declared.append((alias, typed[key]))
    return declared


# ---- __getitem__ dispatch -------------------------------------------------


def _not_an_object_type(label: str) -> str:
    """The parameter type of a document's last ``__getitem__`` overload, which no object type name matches.

    A type checker that finds no overload for ``doc["Space"]`` reports the last one it tried, so this
    one's type is named for what went wrong: ``"Literal['Space']" cannot be assigned to parameter
    "obj_type" of type "_NotAnObjectTypeOfEnergyPlus9_4"``.
    """
    return f"_NotAnObjectTypeOf{label}"


def _generate_not_an_object_type(label: str, what: str) -> list[str]:
    """The class behind :func:`_not_an_object_type`: never instantiated, so no argument matches it."""
    return [
        f"class {_not_an_object_type(label)}:",
        f'    """Not a name of an object type {what}: indexing a document with one is a type error.',
        "",
        "    The last ``__getitem__`` overload of a document type takes this class, which no string is, so",
        "    a type checker that finds no overload for an object type name reports it against this type.",
        '    """',
        "",
    ]


def _generate_getitem(entries: Iterable[tuple[str, str]], label: str, doc: str | None = None) -> list[str]:
    """Type ``doc["Zone"]`` on a document class: one overload per object type, then one that matches nothing.

    The document types are plain classes, not ``TypedDict``\\ s. pyright narrows a ``TypedDict`` on
    ``"Zone" in doc`` by rules of its own, which are not what ``IDFDocument.__contains__`` answers
    (whether the document holds objects of the type): a document typed as one lost its type, or a
    branch, under such a test, and was given ``get``, ``setdefault``, ``pop`` and ``|``, which a
    document does not have. An overload is resolved, never narrowed on.

    Overloads do not merge across base classes, so each document class lists all of its own. Each
    older release's class lives in a module of its own (:func:`generate_versioned_documents`), so a
    file that does not name it does not pay to read its overloads.

    Args:
        entries: ``(object type, class)`` pairs, in schema order.
        label: What :func:`_not_an_object_type` names the class of the last overload for.
        doc: The docstring of the first overload, which an editor shows on hover.
    """
    lines: list[str] = []
    for index, (obj_type, cls) in enumerate(entries):
        signature = f'    def __getitem__(self, obj_type: Literal["{obj_type}"], /) -> IDFCollection[{cls}]:'
        lines.append("    @overload")
        if index == 0 and doc:
            lines.append(signature)
            lines.extend(_format_docstring_for_stub(doc, "        "))
        else:
            lines.append(f"{signature} ...")
    lines.append("    @overload")
    lines.append(f"    def __getitem__(self, obj_type: {_not_an_object_type(label)}, /) -> Never: ...")
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


_Signature: TypeAlias = tuple[tuple[tuple[str, str], ...], tuple[str, frozenset[tuple[str, str]]] | None]


def _class_signature(schema: EpJSONSchema, obj_type: str) -> _Signature:
    """What a version's class for *obj_type* declares, to compare across versions.

    Its fields with their value types, in order, and its extensible group with the group's fields
    as a set: some versions list a group's fields in another order (8.9's vertices), which changes
    nothing a type checker sees, so it does not make a second class. How an object is created is not
    part of it: releases that declare the fields alike but require different ones share the range's
    class, and each gets a subclass with its own creation signature (:func:`_creation_pieces`), so
    a range's class keeps its name whatever its releases require.
    """
    return tuple(_field_decls(schema, obj_type).items()), _group_key(_group_decl(schema, obj_type))


# ---- the creation signature ------------------------------------------------

# A string default longer than this is shown as ``...``: the signature is read in a tooltip.
_MAX_DEFAULT_LENGTH = 40


@dataclasses.dataclass(frozen=True)
class _Creation:
    """How an object of one type is created in one release, as ``_creation_signature`` spells it.

    Attributes:
        name: ``"required"`` for a type whose schema requires a name (``name: str``), ``"optional"``
            for a named type whose name may be left empty (``name: str = ""``), ``"none"`` for a type
            without a Name field, which takes no name.
        required: The fields the schema requires and gives no default: the run-time validator
            refuses an object missing one (``E001``), so the signature has them without a default.
        defaults: Each field's schema default as Python source (``0.9``, ``"Rough"``), for the
            defaults that are a number or a short plain string; others are shown as ``...``. It is
            the value EnergyPlus applies to a field left empty, not one ``add()`` stores.
        hidden: The spellings without the trailing underscore of fields whose key ends in ``_``
            (``gas_or_gas_mixture`` for ``gas_or_gas_mixture_``). The run time accepts either
            spelling but not both, so the signature names only the key, which a type checker can then
            hold to one.
        name_conflict: Whether the releases served disagree on the name so that no call suits them
            all: one requires it, another has no Name field and refuses any.
    """

    name: str
    required: frozenset[str]
    defaults: tuple[tuple[str, str], ...]
    hidden: frozenset[str] = frozenset()
    name_conflict: bool = False

    @property
    def key(self) -> tuple[str, frozenset[str]]:
        """What tells two releases' creation apart for a type checker: the name and the required fields.

        A default only changes a tooltip, so releases that differ in defaults alone share a class,
        which shows the defaults they agree on.
        """
        return self.name, self.required


def _render_default(value: object) -> str | None:
    """A schema default as the Python source a signature shows, or ``None`` when it is not shown.

    Numbers and short plain strings only: a boolean, a list, a long string or one with a quote,
    backslash or non-printable character is shown as ``...``.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # 2.0 is written 2: some releases give an integer field's default as a float, and an int
        # default fits a float annotation as well as an int one.
        text = str(int(value)) if value.is_integer() else repr(value)
        # repr() uses exponent notation for very large and small numbers; those stay "...".
        return text if text.lstrip("-").replace(".", "", 1).isdigit() else None
    if isinstance(value, str):
        if len(value) > _MAX_DEFAULT_LENGTH or not value.isprintable() or any(c in value for c in "\"'\\"):
            return None
        return f'"{value}"'
    return None


def _name_kind(schema: EpJSONSchema, obj_type: str) -> str:
    """``"required"``, ``"optional"`` or ``"none"``: how ``add()`` takes the name of *obj_type*."""
    if not schema.has_name(obj_type):
        return "none"
    object_schema: dict[str, Any] = schema.get_object_schema(obj_type) or {}
    name_schema: dict[str, Any] = object_schema.get("name") or {}
    return "required" if name_schema.get("is_required") else "optional"


def _creation_info(schema: EpJSONSchema, obj_type: str) -> _Creation:
    """How *obj_type* is created in *schema*'s release (see :class:`_Creation`)."""
    inner: dict[str, Any] = schema.get_inner_schema(obj_type) or {}
    properties: dict[str, dict[str, Any]] = inner.get("properties", {})
    listed: list[str] = inner.get("required", [])
    required = frozenset(f for f in listed if f.isidentifier() and "default" not in properties.get(f, {}))
    defaults: list[tuple[str, str]] = []
    for field_name, field_schema in properties.items():
        if field_name.isidentifier() and "default" in field_schema:
            rendered = _render_default(field_schema["default"])
            if rendered is not None:
                defaults.append((field_name, rendered))
    aliases = trailing_underscore_aliases(schema.get_field_names(obj_type))
    hidden = frozenset(alias for alias, key in aliases.items() if alias != key)
    return _Creation(_name_kind(schema, obj_type), required, tuple(sorted(defaults)), hidden)


@functools.cache
def read_required() -> dict[str, frozenset[str]]:
    """The fields reading gives a value for, by object type: required with no default wherever they exist.

    A field is in it when every supported release that has the field requires it and gives it no
    default (the set ``add()`` requires and the validator reports as ``E001``). Its read type drops
    ``| None`` in every class that declares it, whichever releases the class covers, and the run
    time raises :class:`~idfkit.exceptions.MissingRequiredFieldError` instead of returning ``None``
    when it is absent, so the two agree whatever static type the object is seen through.
    """
    required: dict[str, set[str]] = {}
    optional: dict[str, set[str]] = {}
    for ver in SUPPORTED.versions:
        schema = get_schema(ver)
        for obj_type in schema.object_types:
            info = _creation_info(schema, obj_type)
            names = [f for f in schema.get_field_names(obj_type) if f.isidentifier()]
            # Fields only: an extensible group's wrapper (``lines``) reads as a list view, never None.
            required.setdefault(obj_type, set()).update(f for f in info.required if f in names)
            optional.setdefault(obj_type, set()).update(f for f in names if f not in info.required)
    return {
        obj_type: frozenset(fields - optional.get(obj_type, set()))
        for obj_type, fields in sorted(required.items())
        if fields - optional.get(obj_type, set())
    }


@functools.cache
def _release_creation(ver: Version, obj_type: str) -> _Creation:
    """:func:`_creation_info` of *obj_type* in release *ver*, computed once per generation."""
    return _creation_info(get_schema(ver), obj_type)


def _creation_for(obj_type: str, versions: Iterable[Version]) -> _Creation:
    """How a class serving *versions* creates *obj_type*: only what every one of them accepts.

    A field is required where any of the releases requires it, so a call that type-checks is not
    refused for a missing field by any of them; passing a field a release does not require is
    harmless. A default is shown only where every release has the same one. The name is refused
    where some release has no Name field and none requires one, required where any release requires
    it, and optional otherwise; where one release requires it and another refuses it, no call suits
    them all (:attr:`_Creation.name_conflict`). For the
    releases of one :func:`_creation_pieces` piece this is their own creation.
    """
    infos = [_release_creation(ver, obj_type) for ver in versions]
    first = infos[0]
    required = first.required.union(*(info.required for info in infos[1:]))
    hidden = first.hidden.union(*(info.hidden for info in infos[1:]))
    common = set(first.defaults).intersection(*(set(info.defaults) for info in infos[1:]))
    defaults = tuple(item for item in first.defaults if item in common)
    kinds = {info.name for info in infos}
    if kinds <= {"none", "optional"} and "none" in kinds:
        # A call without a name suits both; a name is refused where there is no Name field.
        name = "none"
    elif "required" in kinds:
        name = "required"
    else:
        name = "optional"
    return _Creation(name, required, defaults, hidden, name_conflict=kinds >= {"none", "required"})


def _versions_with(obj_type: str) -> list[Version]:
    """Every supported release whose schema has *obj_type*, oldest first."""
    return [ver for run in _build_type_runs()[obj_type] for ver in run]


_Piece: TypeAlias = tuple[tuple[Version, ...], tuple[Version, ...]]


@functools.cache
def _creation_pieces() -> dict[str, list[_Piece]]:
    """Split each version range (:func:`_build_type_runs`) where its releases create the type differently.

    Returns:
        Object type -> its pieces, oldest first, each ``(run, piece)``: the range and the
        consecutive releases of it that take the same name and require the same fields
        (:attr:`_Creation.key`). A range whose releases all create alike is one piece, itself.
    """
    out: dict[str, list[_Piece]] = {}
    for obj_type, runs in _build_type_runs().items():
        pieces: list[_Piece] = []
        for run in runs:
            current: list[Version] = []
            for ver in run:
                if current and _release_creation(ver, obj_type).key != _release_creation(current[0], obj_type).key:
                    pieces.append((tuple(run), tuple(current)))
                    current = []
                current.append(ver)
            pieces.append((tuple(run), tuple(current)))
        out[obj_type] = pieces
    return out


def _class_creation(obj_type: str, run: Iterable[Version]) -> _Creation:
    """The creation signature of the class of range *run*.

    The latest class creates as the latest release does (older releases of its range that require
    other fields have classes of their own, :func:`_piece_classes`); an older range's class serves
    all its releases.
    """
    run = tuple(run)
    if SUPPORTED.latest in run:
        latest = next(piece for _, piece in _creation_pieces()[obj_type] if SUPPORTED.latest in piece)
        return _creation_for(obj_type, latest)
    return _creation_for(obj_type, run)


def _relaxes(sub: _Creation, base: _Creation) -> bool:
    """Whether a class creating as *sub* may derive from one creating as *base*.

    ``IDFCollection`` is covariant, so a collection of the subclass passes where one of the base is
    expected, and ``add()`` is then checked against the base's signature: *sub* must accept every
    call *base* does, requiring no field *base* does not and taking the name as *base* does or
    leaving optional one *base* requires.
    """
    if not sub.required <= base.required or (sub.name_conflict and not base.name_conflict):
        return False
    return sub.name == base.name or (base.name, sub.name) == ("required", "optional")


def _strip_none(annotation: str) -> str:
    """*annotation* without its trailing ``| None``: the value a required field must be given."""
    return annotation.removesuffix(" | None")


# The parameter a creation signature requires when no call can satisfy every release it serves.
_NARROW_FIRST = "narrow_with_as_version_first"


# A group wrapper's annotation, as _group_items writes it.
_GROUP_ITEMS = re.compile(r"Sequence\[([\w.]+) \| ([\w.]+)\]")

# How many modules the creation signatures of one family of classes are spread over.
_CREATION_BUCKETS = 128


@dataclasses.dataclass
class _CreationModules:
    """The creation signatures of one family of classes, filed in ``idfkit/_creation`` modules.

    A class does not declare its creation signature itself: it declares ``_creation_signature`` as
    an instance of a class whose ``__call__`` has that signature, defined in one of
    :data:`_CREATION_BUCKETS` modules of ``idfkit/_creation`` chosen from the class name. A type
    checker reads such a module only when it resolves the signature, which it does to check an
    ``add()`` call on that type. The signatures repeat every field's annotation and are as large as
    the classes themselves: declared in the class, they would be parsed and bound in every file that
    imports idfkit, which is most of a cold ``pyright`` run.

    Attributes:
        module: The module name prefix, ``_b`` (latest and ``Any<Class>`` classes) or ``_v`` (the
            classes of older ranges, read only where a file names an older release).
        alias: The prefix the generated stub imports the modules under (``_c``, ``_cv``).
        classes: Each module's class definitions, by bucket.
        signatures: Each module's signatures alone, by bucket: the names a module imports are those
            its signatures use, whatever a docstring says (a memo's "Any number of ...").
    """

    module: str = "_b"
    alias: str = "_c"
    classes: dict[int, list[str]] = dataclasses.field(default_factory=dict[int, list[str]])
    signatures: dict[int, list[str]] = dataclasses.field(default_factory=dict[int, list[str]])

    @property
    def home(self) -> str:
        """How the modules name the stub whose classes they serve: ``_g`` (``_generated_types``) or
        ``_vd`` (``versioned``), for the group classes and group dicts a signature names."""
        return "_g" if self.module == "_b" else "_vd"

    def qualify(self, annotation: str) -> str:
        """*annotation*, written in the classes' stub, as the creation modules reach its names.

        Only a group wrapper's ``Sequence[<Item> | <Group>]`` (:func:`_group_items`) names classes
        of the stub; a name already qualified ``_g.`` (``versioned.pyi`` reaching
        ``_generated_types``) stays, and any other annotation is returned as it is.
        """
        match = _GROUP_ITEMS.fullmatch(annotation)
        if match is None:
            return annotation
        item, group = (name if "." in name else f"{self.home}.{name}" for name in match.groups())
        return f"Sequence[{item} | {group}]"

    def add(self, cls_name: str, params: str, doc: str) -> str:
        """File the signature (*params*, without parentheses) of *cls_name*, documented with *doc*.

        Returns the annotation the class declares ``_creation_signature`` with.
        """
        bucket = zlib.crc32(cls_name.encode()) % _CREATION_BUCKETS
        self.classes.setdefault(bucket, []).extend([
            f"class {cls_name}:",
            f"    def __call__({params}) -> None:",
            textwrap.indent(f'"""{doc}\n"""', "        "),
            "",
        ])
        self.signatures.setdefault(bucket, []).append(params)
        return f"{self.alias}{bucket}.{cls_name}"

    def _stubs(self) -> list[tuple[str, str]]:
        """The stubs whose group classes a module of this family may name: module, alias."""
        return (
            [("_generated_types", "_g")] if self.module == "_b" else [("_generated_types", "_g"), ("versioned", "_vd")]
        )

    def imports(self) -> list[str]:
        """The import of every module, for the stub whose classes annotate with them.

        Emitted before the classes are; :meth:`drop_unused_imports` then takes out those of the
        modules no class of the stub names.
        """
        return [f"from ._creation import {self.module}{k} as {self.alias}{k}" for k in range(_CREATION_BUCKETS)]

    def drop_unused_imports(self, parts: list[str]) -> list[str]:
        """*parts*, a stub's lines, without the imports of modules its classes do not name."""
        text = "\n".join(parts)
        return [
            line
            for line in parts
            if not line.startswith("from ._creation import ") or f"{line.rpartition(' as ')[2]}." in text
        ]

    def sources(self) -> dict[str, str]:
        """Each module's source by file name (``_b7.pyi``), every bucket included, empty or not."""
        out: dict[str, str] = {}
        for k in range(_CREATION_BUCKETS):
            body = "\n".join(self.classes.get(k, []))
            used = "\n".join(self.signatures.get(k, []))
            typing_names = [n for n in ("Any", "Literal") if re.search(rf"\b{n}\b", used)]
            header = [
                '"""Creation signatures of generated classes (stub only).',
                "",
                "DO NOT EDIT — regenerate with:",
                "    python -m idfkit.codegen.generate_stubs",
                '"""',
                "",
                "from __future__ import annotations",
                "",
            ]
            standard_library = len(header)
            if re.search(r"\bSequence\[", used):
                header.append("from collections.abc import Sequence")
            if typing_names:
                header.append(f"from typing import {', '.join(typing_names)}")
            if re.search(r"\bNever\b", used):
                # A third-party import, in a block of its own after the standard library's (isort).
                header.extend(
                    ["", "from typing_extensions import Never"]
                    if len(header) > standard_library
                    else ["from typing_extensions import Never"]
                )
            own = [f"from .. import {name} as {alias}" for name, alias in self._stubs() if f"{alias}." in used]
            if own:
                header.extend(["", *own])
            out[f"{self.module}{k}.pyi"] = "\n".join([*header, "", body]).rstrip() + "\n"
        return out


def _creation_docstring(schema: EpJSONSchema, obj_type: str, *, narrow_first: bool) -> str:
    """The docstring of *obj_type*'s creation signature in *schema*'s release.

    An editor shows it for ``add()`` on a collection of the type, in hover and signature help:
    pyright gives a call the docstring of the signature ``IDFCollection.add`` takes its parameters
    from, because ``add`` declares none for type checkers. It names the type, gives the schema's
    memo whole (the class docstring truncates it) and the type's page in the EnergyPlus I/O
    Reference on docs.idfkit.com. Field notes stay on the class's attributes, which hover shows:
    here they would double the size of the ``_creation`` modules, and pyright would not show them
    beside the parameter, only in the block. What a shown default means is said once, on
    ``IDFCollection.add``, not in each of 1,700 signatures. *narrow_first* says why the signature
    requires ``narrow_with_as_version_first``.
    """
    lines = [f"Create a new ``{obj_type}`` and add it to the document."]
    memo = schema.get_object_memo(obj_type)
    if memo:
        lines += ["", _sanitize_docstring(" ".join(memo.split())).replace("\\", "\\\\")]
    if narrow_first:
        lines += ["", "No call suits every release: narrow the document with ``as_version`` first."]
    url = io_reference_url(obj_type, schema.version, schema)
    if url is not None:
        lines += ["", f"EnergyPlus I/O Reference: {url.url}"]
    return "\n".join(lines)


def _creation_lines(
    cls_name: str,
    fields: Iterable[tuple[str, str]],
    creation: _Creation,
    indent: str,
    sink: _CreationModules,
    schema: EpJSONSchema,
    obj_type: str,
) -> list[str]:
    """Declare *cls_name*'s ``_creation_signature``, the signature ``IDFCollection.add`` captures.

    The class body at *indent* gets the attribute; the signature itself goes to *sink*
    (:class:`_CreationModules`). *fields* are the keywords with the annotations the class's
    ``update`` ``TypedDict`` gives them, in field order. The name comes first, positional-only, when
    the type has one; a type without one takes ``this_type_has_no_name_field`` there instead, typed
    with an alias of ``Never`` so that a name passed by mistake is reported as such. The fields follow, keyword-only: the required ones without a default and with
    ``None`` taken out (leaving one empty is what makes it missing), then the others with their
    schema default where the annotation admits it, and ``...`` otherwise.

    A required field the class cannot be given a value for (one ``Any<Class>`` does not declare,
    because a release names it differently, or whose only value safe in every release is ``None``),
    or a name one release requires and another refuses, makes every call wrong for some release. The signature then also requires
    ``narrow_with_as_version_first: Never``, which no argument satisfies, so the type checker names
    the way out (narrow the document with ``as_version``) instead of accepting a call some release
    refuses.

    The signature carries the docstring an editor shows for the call (:func:`_creation_docstring`),
    from *schema*, the release the class declares *obj_type* as.
    """
    params = ["self"]
    if creation.name == "required":
        params.append("name: str")
    elif creation.name == "optional":
        params.append('name: str = ""')
    else:
        params.append(f"{_NO_NAME_PARAM}: _g.{_NO_NAME_FIELD} = ...")
    params.append("/")
    defaults = dict(creation.defaults)
    required: list[str] = []
    optional: list[str] = []
    fields = list(fields)
    settable = {name for name, annotation in fields if _strip_none(annotation) != "None"}
    narrow_first = bool(creation.required - settable) or creation.name_conflict
    if narrow_first:
        required.append(f"{_NARROW_FIRST}: Never")
    fields = [(name, sink.qualify(annotation)) for name, annotation in fields]
    for name, annotation in fields:
        value_type = _strip_none(annotation)
        if name in creation.hidden:
            continue
        if name in creation.required and value_type != "None":
            required.append(f"{name}: {value_type}")
            continue
        default = defaults.get(name)
        shown = default if default is not None and _admits(_split_union(value_type), default) else "..."
        optional.append(f"{name}: {annotation} = {shown}")
    if required or optional:
        params.append("*")
    params += required + optional
    doc = _creation_docstring(schema, obj_type, narrow_first=narrow_first)
    # Each class's signature is its own, unrelated to its base's: an override mypy reports as an
    # incompatible assignment (pyright does not), as the generated update and as_dict overrides are.
    annotation = sink.add(cls_name, ", ".join(params), doc)
    return [f"{indent}_creation_signature: {annotation}  # type: ignore[assignment]"]


@functools.cache
def _build_type_runs() -> dict[str, list[list[Version]]]:
    """Group, for each object type, the versions that declare it identically.

    Two versions declare a type identically when its fields, value types, choice lists and
    extensible group are the same (:func:`_class_signature`), docstrings and the order of a
    group's fields aside. Every such group is a
    contiguous range of releases, so it is fully described by its two endpoints; the function
    asserts that rather than assuming it.

    Returns:
        Object type -> its ranges, oldest first, each the list of versions it covers.
    """
    signatures: dict[str, list[tuple[Version, _Signature]]] = {}
    for ver in SUPPORTED.versions:
        schema = get_schema(ver)
        for obj_type in schema.object_types:
            signatures.setdefault(obj_type, []).append((
                ver,
                _class_signature(schema, obj_type),
            ))

    order = {ver: i for i, ver in enumerate(SUPPORTED.versions)}
    runs: dict[str, list[list[Version]]] = {}
    for obj_type, entries in signatures.items():
        type_runs: list[tuple[list[Version], _Signature]] = []
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
    """Each identifier field of *obj_type* with its generated value type.

    A field whose key ends in ``_`` is followed, after every key, by its spelling without the
    underscore, with the same type, as :func:`_generate_field_aliases` declares it; the classes
    that share fields between versions, and the check of them, then treat the alias as a field.
    """
    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}
    field_names = schema.get_field_names(obj_type)
    decls: dict[str, str] = {}
    for field_name in field_names:
        if not field_name.isidentifier():
            continue
        field_schema = properties.get(field_name)
        has_any_of = field_schema is not None and "anyOf" in field_schema
        decls[field_name] = _schema_type_to_python(
            field_schema, schema.get_field_type(obj_type, field_name), has_any_of
        )
    # In field order: the alias map's own order is not stable between runs.
    alias_of = {key: alias for alias, key in trailing_underscore_aliases(field_names).items() if alias != key}
    for key in field_names:
        alias = alias_of.get(key)
        if alias is not None and alias.isidentifier() and alias not in decls and key in decls:
            decls[alias] = decls[key]
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


def _group_key(
    decl: tuple[str, tuple[tuple[str, str], ...]] | None,
) -> tuple[str, frozenset[tuple[str, str]]] | None:
    """A group declaration with its fields' order dropped, for comparing versions."""
    return None if decl is None else (decl[0], frozenset(decl[1]))


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


def _admits(parts: list[str], value: str) -> bool:
    """Whether a value type, split at its ``|``, admits *value*: a member type or one ``Literal`` member."""
    if value in parts:
        return True
    if value == "int" and "float" in parts:
        return True
    literals = [m for p in parts if p.startswith("Literal[") for m in _split_literal(p[len("Literal[") : -1])]
    if value in literals:
        return True
    if value.startswith('"'):
        return "str" in parts
    if value.lstrip("-").replace(".", "", 1).isdigit():
        return "float" in parts or ("int" in parts and "." not in value)
    return False


def _intersect_types(type_texts: list[str]) -> str:
    """The values every one of the generated value types admits, as one value type.

    What is safe to write into a document of any supported version: a ``Literal`` member that every
    version lists or admits through a plain ``str``/``float``, and a plain type every version has.
    ``Never`` when nothing is admitted everywhere (the caller adds ``| None``, which clears a field).
    """
    split = [_split_union(text) for text in type_texts]
    candidates: list[str] = []
    literals: list[str] = []
    for parts in split:
        for part in parts:
            if part.startswith("Literal[") and part.endswith("]"):
                literals.extend(m for m in _split_literal(part[len("Literal[") : -1]) if m not in literals)
            elif part not in candidates:
                candidates.append(part)
    others = [part for part in candidates if all(_admits(parts, part) for parts in split)]
    kept = [m for m in literals if all(_admits(parts, m) for parts in split) and not _admits(others, m)]
    if kept:
        others.append(f"Literal[{', '.join(kept)}]")
    return " | ".join(others) if others else "Never"


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
        fields: Every field present in all versions, with the union of its value types: what
            reading it can give.
        writable: Every field present in all versions, with the intersection of its value types:
            what every version accepts, so what is safe to write.
        identical: The fields declared identically in all versions; only the shared base declares them.
        group: Whether the extensible group is identical in all versions.
    """

    fields: dict[str, str]
    writable: dict[str, str]
    identical: frozenset[str]
    group: bool

    @property
    def varying(self) -> frozenset[str]:
        """Fields present in all versions with different value types; every class narrows them."""
        return frozenset(self.fields) - self.identical


@functools.cache
def _shared_layout() -> dict[str, _SharedLayout]:
    """For each type of the latest release that some older version declares or creates differently.

    Such a type gets ``Any<Class>``: the type as every supported version that has it declares it,
    created as they all accept. A type every version declares alike gets one only where some
    release requires what the latest does not (a field, or the name), so that ``AnyIDFDocument``'s
    ``add()`` asks for it.
    The latest class and each older range's class derive from it, so they only declare what is
    theirs, ``AnyIDFDocument`` types the type's collection with it, and code for any release
    annotates a parameter with it.
    """
    runs = _build_type_runs()
    latest_types = set(get_schema(SUPPORTED.latest).object_types)
    layout: dict[str, _SharedLayout] = {}
    for obj_type, type_runs in runs.items():
        # The latest class serves every release only if they declare the type alike, and a call it
        # accepts suits them all: no release requires a field (or the name) the latest does not.
        if obj_type not in latest_types or (
            len(type_runs) == 1
            and _relaxes(_creation_for(obj_type, type_runs[0]), _class_creation(obj_type, type_runs[0]))
        ):
            continue
        schemas = [get_schema(run[0]) for run in type_runs]
        decls = [_field_decls(sc, obj_type) for sc in schemas]
        latest = decls[-1]
        fields = {name: _merge_types([d[name] for d in decls]) for name in latest if all(name in d for d in decls)}
        writable = {name: _intersect_types([d[name] for d in decls]) for name in fields}
        identical = frozenset(name for name in fields if all(d[name] == latest[name] for d in decls))
        # Compared as sets: some versions list a group's fields in another order (8.9's vertices).
        groups = {_group_key(_group_decl(sc, obj_type)) for sc in schemas}
        layout[obj_type] = _SharedLayout(fields, writable, identical, len(groups) == 1 and None not in groups)
    return layout


def _shared_class_name(obj_type: str) -> str:
    """The class ``AnyIDFDocument`` types *obj_type*'s collection with.

    ``Any<Class>`` for a type some version declares differently; the latest class itself for one
    every version declares alike, which ``Any<Class>`` then names as an alias (see
    :func:`_generate_any_aliases`).
    """
    if obj_type in _shared_layout():
        return _any_class_name(obj_type)
    return _to_class_name(obj_type)


def _any_class_name(obj_type: str) -> str:
    """The public name of *obj_type* as every version that has it declares it: ``Any<Class>``."""
    return f"Any{_to_class_name(obj_type)}"


@dataclasses.dataclass(frozen=True)
class _MergedGroup:
    """An extensible group every version has under one wrapper key, though not declared alike.

    Attributes:
        wrapper: The wrapper key, such as ``vertices``.
        cls_name: ``Any<Class><Wrapper>Group``, the group as every version declares it.
        fields: Each inner field every version has, in the latest version's order, with what
            reading it gives (the union of the versions' types) and what writing it accepts (their
            intersection).
    """

    wrapper: str
    cls_name: str
    fields: tuple[tuple[str, str, str], ...]


@functools.cache
def _merged_groups() -> dict[str, _MergedGroup]:
    """The groups ``Any<Class>`` declares for types whose group differs between versions.

    A type whose group is declared alike everywhere has it on ``Any<Class>`` already, and one that
    some version declares without a group, or under another wrapper key, gets none: a file of that
    version has no such list.
    """
    runs = _build_type_runs()
    merged: dict[str, _MergedGroup] = {}
    for obj_type, layout in _shared_layout().items():
        if layout.group:
            continue
        decls = [_group_decl(get_schema(run[0]), obj_type) for run in runs[obj_type]]
        if any(d is None for d in decls) or len({d[0] for d in decls if d is not None}) != 1:
            continue
        inner = [dict(d[1]) for d in decls if d is not None]
        names = [name for name in inner[-1] if all(name in i for i in inner)]
        wrapper = decls[-1][0] if decls[-1] is not None else ""
        cls_name = f"{_any_class_name(obj_type)}{_to_class_name(wrapper.title())}Group"
        fields = tuple(
            (name, _merge_types([i[name] for i in inner]), _intersect_types([i[name] for i in inner])) for name in names
        )
        merged[obj_type] = _MergedGroup(wrapper, cls_name, fields)
    return merged


def _generate_merged_group(group: _MergedGroup, owner: str) -> list[str]:
    """The group class of a :class:`_MergedGroup`: reads give the union, writes the intersection."""
    lines = [
        f"class {group.cls_name}({_TYPED_GROUP_BASE}):",
        f'    """One {group.wrapper} group inside :class:`{owner}`, as every supported version declares it."""',
    ]
    for name, read, write in group.fields:
        if read == write:
            lines.append(f"    {name}: {read} | None")
        else:
            lines += _property_lines(name, read, write, "    ")
    # Typed with the item, so as_list() passes back to add() and update() through AnyIDFDocument as
    # it does through a release's document. The item types what writing accepts, every release's
    # values; reading one of the few fields whose releases accept different values can give another.
    lines.append(f"    def as_dict(self) -> {_group_item_name(group.cls_name)}: ...  # type: ignore[override]")
    lines.append("")
    # A dict written into a document of any release holds only what every release accepts.
    lines += _group_item_class(group.cls_name, [(name, write) for name, _, write in group.fields])
    return lines


def _group_base_for(obj_type: str, prefix: str = "") -> str:
    """The base of *obj_type*'s per-version group classes: its merged group, if it has one."""
    group = _merged_groups().get(obj_type)
    return f"{prefix}{group.cls_name}" if group is not None else f"{prefix}{_TYPED_GROUP_BASE}"


def _any_class_doc(obj_type: str) -> str:
    """The docstring of ``Any<Class>``, which names the releases it covers when not all of them.

    A type that arrived after the oldest supported release is reached only through a document of a
    release that has it, so the hover says which releases those are.
    """
    first = _build_type_runs()[obj_type][0][0]
    if first == SUPPORTED.versions[0]:
        return f"``{obj_type}`` as every supported EnergyPlus version declares it."
    return (
        f"``{obj_type}`` as every supported EnergyPlus version that has it declares it: "
        f"{version_string(first)} and later."
    )


def _generate_any_aliases(schema: EpJSONSchema) -> list[str]:
    """``Any<Class> = <Class>`` for each type every version that has it declares alike.

    So every object type has an ``Any<Class>`` to annotate code for any release with, and a caller
    need not know which types changed between releases. A type that did change has a class of that
    name instead (:func:`_generate_base_class`).
    """
    layout = _shared_layout()
    return [f"{_any_class_name(t)}: TypeAlias = {_to_class_name(t)}" for t in schema.object_types if t not in layout]


def _common_fields_name(obj_type: str) -> str:
    """The ``TypedDict`` of the ``update`` keywords every version of *obj_type* accepts alike."""
    return f"_{_to_class_name(obj_type)}CommonFields"


def _generate_base_class(
    schema: EpJSONSchema,
    obj_type: str,
    layout: _SharedLayout,
    type_since: dict[str, tuple[int, int, int]],
    field_since: dict[tuple[str, str], tuple[int, int, int]],
    sink: _CreationModules,
) -> list[str]:
    r"""Generate ``Any<Class>``: the fields of *obj_type* present in every supported version.

    A field whose value type differs between versions is a property here: reading it gives the
    union of the versions' value types, since a document of any of them can hold any of those
    values, and assigning to it accepts only their intersection, the values every version accepts.
    Each version's class narrows it again, with its docstring, to that version's own type, which it
    both reads and writes. ``update`` on the base takes the same intersection; each version's class
    types its own. Their keyword ``TypedDict``\ s extend ``_<Class>CommonFields``, which holds the
    fields declared identically everywhere, so those are written once.
    """
    base = _shared_class_name(obj_type)
    common = _common_entries(schema, obj_type, layout)
    lines = [f"class {_common_fields_name(obj_type)}(TypedDict, total=False):"]
    lines.extend(f"    {name}: {py_type}" for name, py_type in common)
    if not common:
        lines[-1] += " ..."
    lines.append("")
    merged_group = _merged_groups().get(obj_type)
    if merged_group is not None:
        lines += _generate_merged_group(merged_group, base)
    lines += _generate_object_class(
        schema,
        obj_type,
        type_since=type_since,
        field_since=field_since,
        cls_name=base,
        class_doc=_any_class_doc(obj_type),
        skip_fields=frozenset(schema.get_field_names(obj_type)) - frozenset(layout.fields),
        omit_group=not layout.group,
        emit_update=False,
        undocumented=layout.varying,
        properties={
            name: (merged, layout.writable[name]) for name, merged in layout.fields.items() if name in layout.varying
        },
    )
    if lines[-1].startswith("class ") and lines[-1].endswith(": ..."):
        lines[-1] = lines[-1][: -len(" ...")]  # update is about to give the class a body
    always = read_required().get(obj_type, frozenset())
    varying = [
        (name, layout.writable[name] if name in always else _or_none(layout.writable[name]))
        for name in layout.fields
        if name in layout.varying
    ]
    if merged_group is not None:
        lines.append(f"    {merged_group.wrapper}: ExtensibleList[{merged_group.cls_name}]")
        varying.append((merged_group.wrapper, _group_items(merged_group.cls_name)))
    creation = _creation_lines(
        base,
        _in_field_order(schema, obj_type, [*common, *varying]),
        _creation_for(obj_type, _versions_with(obj_type)),
        "    ",
        sink,
        schema,
        obj_type,
    )
    lines.extend(_generate_update(base, varying, "", _common_fields_name(obj_type), creation))
    return lines


def _common_entries(
    schema: EpJSONSchema, obj_type: str, layout: _SharedLayout, prefix: str = ""
) -> list[tuple[str, str]]:
    """The ``update`` keywords of ``_<Class>CommonFields``: the fields every version declares alike.

    *prefix* qualifies the group's names as the module reading them reaches ``_generated_types``.
    """
    decls = _field_decls(schema, obj_type)
    always = read_required().get(obj_type, frozenset())
    common = [
        (name, decls[name] if name in always else f"{decls[name]} | None")
        for name in decls
        if name in layout.identical and name != "name"
    ]
    group = _group_decl(schema, obj_type)
    if layout.group and group is not None:
        # Any<Class> declares the group, under the unsuffixed name.
        common.append((group[0], _group_items(_group_class_name(obj_type, group[0]), prefix)))
    return common


def _or_none(value_type: str) -> str:
    """*value_type* or ``None``, the value that clears a field; just ``None`` when nothing else is safe."""
    return "None" if value_type == "Never" else f"{value_type} | None"


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
    for obj_type, _, piece, cls_name, _ in _piece_classes():
        for ver in piece:
            class_for[(obj_type, ver)] = cls_name
    return class_for, tuple(older_runs)


@functools.cache
def _piece_classes() -> tuple[tuple[str, tuple[Version, ...], tuple[Version, ...], str, str], ...]:
    """The classes of the releases of a range that create its type differently from its class.

    A range's class (:func:`_class_assignment`) declares the fields; when its releases require
    different fields or take the name differently (:func:`_creation_pieces`), each piece but the
    latest release's gets a class with its own creation signature, so each release's ``add()``
    requires what its validator does while the range's class keeps its name. An older range's class
    requires what any of its releases requires, so each of its pieces is a subclass of it that
    requires less. The latest class creates as the latest release does: a piece of its range that
    requires no more is a subclass of it, and one that requires more (25.1's BuildingSurface:Detailed
    requires construction_name) derives from ``Any<Class>`` beside it instead, as an older range's
    class does, since as a subclass it would pass for the latest class and ``add()`` would then be
    checked against what 26.2 requires.

    Returns:
        ``(obj_type, run, piece, class_name, base)`` for each, ``base`` qualified as
        ``versioned.pyi`` reaches it: the range's class, or ``_g.Any<Class>``.
    """
    out: list[tuple[str, tuple[Version, ...], tuple[Version, ...], str, str]] = []
    for obj_type, pieces in _creation_pieces().items():
        for run, piece in pieces:
            if piece == run or SUPPORTED.latest in piece:
                continue
            if SUPPORTED.latest not in run:
                base = _to_class_name(obj_type) + _run_suffix(list(run))
            elif _relaxes(_creation_for(obj_type, piece), _class_creation(obj_type, run)):
                base = f"_g.{_to_class_name(obj_type)}"
            else:
                base = f"_g.{_any_class_name(obj_type)}"
            out.append((obj_type, run, piece, _to_class_name(obj_type) + _run_suffix(list(piece)), base))
    return tuple(out)


def _generate_piece_class(
    obj_type: str,
    run: tuple[Version, ...],
    piece: tuple[Version, ...],
    cls_name: str,
    base: str,
    sink: _CreationModules,
) -> list[str]:
    """The class of releases of a range that create the type differently (:func:`_piece_classes`).

    A subclass of the range's class declares nothing but its creation signature: the fields are the
    range's, and so are the ``update`` keywords, which the signature names with the range's
    annotations. One deriving from ``Any<Class>`` is declared as an older range's class is.
    """
    schema = get_schema(piece[-1])
    if base == f"_g.{_any_class_name(obj_type)}":
        return _generate_range_class(obj_type, piece, sink, _creation_for(obj_type, piece))
    span = version_string(piece[0]) if len(piece) == 1 else f"{version_string(piece[0])} to {version_string(piece[-1])}"
    doc = (
        f"``{obj_type}`` as declared in EnergyPlus {span}: the fields of :class:`{base.removeprefix('_g.')}`, "
        "with the fields these releases require."
    )
    entries = _update_entries(schema, obj_type, run)
    fields_base = (
        f"{'_g.' if base.startswith('_g.') else ''}_{base.removeprefix('_g.')}Fields" if entries else "TypedDict"
    )
    return _generate_object_class(
        schema,
        obj_type,
        cls_name=cls_name,
        class_doc=doc,
        base=base,
        skip_fields=frozenset(schema.get_field_names(obj_type)),
        omit_group=True,
        fields_base=fields_base,
        inherited=entries,
        sink=sink,
        creation=_creation_for(obj_type, piece),
    )


def _generate_range_class(
    obj_type: str, run: tuple[Version, ...], sink: _CreationModules, creation: _Creation
) -> list[str]:
    """The class of the releases *run* of *obj_type*, declared on ``Any<Class>`` (or on its own).

    It declares the fields its releases do not share with every other release, and creates as
    *creation* says.
    """
    schema = get_schema(run[-1])
    span = version_string(run[0]) if len(run) == 1 else f"{version_string(run[0])} to {version_string(run[-1])}"
    doc = f"``{obj_type}`` as declared in EnergyPlus {span}."
    memo = schema.get_object_memo(obj_type)
    if memo:
        doc = f"{doc} {_truncate_text(memo)}"
    shared = _shared_layout().get(obj_type)
    return _generate_object_class(
        schema,
        obj_type,
        suffix=_run_suffix(list(run)),
        class_doc=doc,
        base=f"_g.{_shared_class_name(obj_type)}" if shared else f"_g.{_TYPED_OBJECT_BASE}",
        group_base=_group_base_for(obj_type, "_g."),
        skip_fields=shared.identical if shared else frozenset(),
        omit_group=shared.group if shared else False,
        fields_base=f"_g.{_common_fields_name(obj_type)}" if shared else "TypedDict",
        inherited=_common_entries(schema, obj_type, shared, "_g.") if shared else (),
        sink=sink,
        creation=creation,
    )


def _update_entries(schema: EpJSONSchema, obj_type: str, run: tuple[Version, ...]) -> list[tuple[str, str]]:
    """Every ``update`` keyword of the class of range *run* of *obj_type*, annotated, as ``versioned.pyi`` reads it.

    What its ``_<Class>Fields`` and the ``_<Class>CommonFields`` it extends hold together: each
    field and alias as its value type or ``None``, and the group's wrapper as a list of its groups.
    The group class is the unsuffixed one in ``_generated_types`` (on ``Any<Class>`` or the latest
    class) unless the range is an older one that declares its own group.
    """
    entries = [
        (name, f"{py_type} | None") for name, py_type in _field_decls(schema, obj_type).items() if name != "name"
    ]
    group = _group_decl(schema, obj_type)
    if group is not None:
        layout = _shared_layout().get(obj_type)
        if SUPPORTED.latest in run or (layout is not None and layout.group):
            entries.append((group[0], _group_items(_group_class_name(obj_type, group[0]), "_g.")))
        else:
            entries.append((group[0], _group_items(_group_class_name(obj_type, group[0], _run_suffix(list(run))))))
    return entries


def _accessors(ver: Version) -> dict[str, str]:
    """The typed attribute accessors of a document of *ver*: name -> object type."""
    from idfkit.document import _build_resolver  # pyright: ignore[reportPrivateUsage]

    return _build_resolver(get_schema(ver)).accessors()


def _document_class_name(ver: Version) -> str:
    """``IDFDocumentV9_4``. Major and minor identify every supported release; checked when generating."""
    return f"IDFDocumentV{_version_tag(ver)}"


def _check_version_tags(versions: tuple[Version, ...] | None = None) -> None:
    """Refuse a version list in which two releases would share a document type name.

    Args:
        versions: The releases to check; the supported ones when ``None``.
    """
    tags = [_version_tag(ver) for ver in (SUPPORTED.versions if versions is None else versions)]
    duplicates = sorted({tag for tag in tags if tags.count(tag) > 1})
    if duplicates:
        msg = f"Releases share a major.minor, so their document types would share a name: {duplicates}"
        raise ValueError(msg)


def generate_versioned_pyi(sink: _CreationModules | None = None) -> str:
    """Generate ``versioned.pyi``: an ``IDFDocument`` type for every supported older version.

    Everything below is derived from ``SUPPORTED.versions`` and the bundled schemas, so adopting
    a release is a regeneration: the previous latest release gains its own document type here,
    and a range of an older type that ends before the latest release keeps its name for good.

    * A type declared in some version exactly as in the latest release reuses the latest class
      from ``_generated_types``. Every other range of versions declaring a type alike gets one
      class here, named by its endpoints, deriving from the type's shared base.
    * A version's typed attribute accessors are assembled from pieces each filed under the version
      range they hold over, so each entry is written once.
    * Each version's document type is defined in a module of its own under ``_versioned``
      (:func:`generate_versioned_documents`) and re-exported here.
    * The classes' creation signatures are filed in *sink*, the ``_v`` modules of ``_creation``
      (:class:`_CreationModules`), so a file naming an older release reads only those it checks.
    """
    sink = sink if sink is not None else _CreationModules("_v", "_cv")
    _check_version_tags()
    _, older_runs = _class_assignment()
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
        "from collections.abc import Mapping, Sequence",
        "from typing import Any, Literal, TypeAlias, TypeVar, overload",
        "",
        "from typing_extensions import TypedDict, Unpack",
        "",
        "from . import _generated_types as _g",
        *sink.imports(),
        *(
            f"from ._versioned.{_versioned_module(ver)} import {_document_class_name(ver)} as {_document_class_name(ver)}"
            for ver in older
        ),
        "from .document import AnyIDFDocument as AnyIDFDocument",
        "from .document import IDFDocument",
        "from .objects import ExtensibleList, IDFCollection",
        "",
        "# =========================================================================",
        "# Object classes of the version ranges that end before the latest release",
        "# =========================================================================",
        "",
    ]
    for obj_type, run in older_runs:
        parts.extend(_generate_range_class(obj_type, run, sink, _class_creation(obj_type, run)))
        parts.append("")

    parts.extend([
        "# =========================================================================",
        "# Releases that create a range's type differently: a subclass each",
        "# =========================================================================",
        "",
    ])
    for obj_type, run, piece, cls_name, base in _piece_classes():
        parts.extend(_generate_piece_class(obj_type, run, piece, cls_name, base, sink))
        parts.append("")

    accessor_spans = _accessor_spans()

    parts.extend([
        "# =========================================================================",
        "# Attribute accessors, one piece per version range",
        "# =========================================================================",
        "",
    ])
    for span, entries in accessor_spans.items():
        if span[0] == SUPPORTED.latest:
            continue  # only the latest release holds it, and IDFDocument declares its own accessors
        parts.append(f"class {_span_name('_Accessors', span)}:")
        for name, cls in entries.items():
            parts.append("    @property")
            parts.append(f"    def {name}(self) -> IDFCollection[{cls}]: ...")
        parts.append("")

    parts.append(f"{_document_class_name(SUPPORTED.latest)} = IDFDocument")
    parts.append("")
    parts.append('_D = TypeVar("_D", bound=AnyIDFDocument)')
    parts.append("")
    releases = ", ".join([*(_document_class_name(ver) for ver in older), "IDFDocument"])
    parts.append(f'ReleaseDocumentT = TypeVar("ReleaseDocumentT", {releases})')
    parts.extend(_RELEASE_DOCUMENT_T_DOC)
    parts.append("")
    # The aliases come first: mypy reads only the first run of overloads, so they must be contiguous.
    aliases, overloads = _range_typing([*older, SUPPORTED.latest])
    parts.extend(aliases)
    parts.extend([
        "@overload",
        *_format_def_with_doc(
            "def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D",
            # The latest release's type by name, so the advice moves on when a release is adopted.
            _AS_VERSION_DOC.replace("{latest}", _document_class_name(SUPPORTED.latest)).replace(
                "{latest_number}", f"{SUPPORTED.latest[0]}.{SUPPORTED.latest[1]}"
            ),
        ),
        "@overload",
        # Non-empty: an empty tuple raises at run time, so the checker reports it.
        "def as_version(doc: AnyIDFDocument, document_type: tuple[type[_D], Unpack[tuple[type[_D], ...]]]) -> _D: ...",
    ])
    parts.extend(overloads)
    return "\n".join(sink.drop_unused_imports(parts))


def _versioned_module(ver: Version) -> str:
    """``v9_4``: the module under ``idfkit/_versioned`` that defines the document type of *ver*."""
    return f"v{_version_tag(ver)}"


@functools.cache
def _accessor_spans() -> dict[Span, dict[str, str]]:
    """Every version's typed attribute accessors, name -> class, filed under the range holding each."""
    class_for, _ = _class_assignment()
    return _group_by_span({
        ver: {name: class_for[(t, ver)] for name, t in _accessors(ver).items()} for ver in SUPPORTED.versions
    })


def _qualified(cls: str) -> str:
    """*cls* as a per-version document module names it: ``_g.Zone`` stays, an older class is ``_v.``'s."""
    return cls if cls.startswith("_g.") else f"_v.{cls}"


_VERSIONED_PACKAGE_DOC = '''"""The document type of each older EnergyPlus release, one module per release (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs

Import them from :mod:`idfkit.versioned`. Each is kept apart so that a type checker reads a
release's ``__getitem__`` overloads only in a file that names that release.
"""
'''


def generate_versioned_documents() -> dict[str, str]:
    """Generate ``_versioned/``: one stub module per older release, defining its document type.

    Each ``IDFDocumentV<major>_<minor>`` derives from its accessor pieces in ``versioned.pyi`` and
    from ``IDFDocumentAllVersions``, so it is assignable to ``AnyIDFDocument`` by name, and types
    ``doc["Zone"]`` with overloads of its own (:func:`_generate_getitem`). Its own module, because the
    overloads of every release are as long as the rest of ``versioned.pyi``, and a type checker binds
    a whole module even to read one class of it.

    Returns:
        File name under ``_versioned`` -> source, ``__init__.pyi`` included.
    """
    _check_version_tags()
    class_for, _ = _class_assignment()
    accessor_spans = _accessor_spans()
    modules = {"__init__.pyi": _VERSIONED_PACKAGE_DOC}
    for ver in SUPPORTED.versions:
        if ver == SUPPORTED.latest:
            continue
        name = _document_class_name(ver)
        label = f"EnergyPlus{_version_tag(ver)}"
        mixins = [f"_v.{_span_name('_Accessors', span)}" for span in accessor_spans if span[0] <= ver <= span[1]]
        entries = [(t, _qualified(class_for[(t, ver)])) for t in get_schema(ver).object_types]
        lines = [
            f'"""``{name}``: an ``IDFDocument`` typed for EnergyPlus {version_string(ver)} (stub only).',
            "",
            "DO NOT EDIT — regenerate with:",
            "    python -m idfkit.codegen.generate_stubs",
            "",
            "Import it from :mod:`idfkit.versioned`.",
            '"""',
            "",
            "from __future__ import annotations",
            "",
            "from typing import Literal, overload",
            "",
            "from typing_extensions import Never",
            "",
            "from .. import _generated_types as _g",
            "from .. import versioned as _v",
            "from ..document import IDFDocumentAllVersions, Strict",
            "from ..objects import IDFCollection",
            "",
            *_generate_not_an_object_type(label, f"EnergyPlus {version_string(ver)} has"),
            "",
            # The accessor pieces come first, so that each of their accessors, typed for this
            # release, wins over IDFDocumentAllVersions' accessor of the same name.
            f"class {name}({', '.join([*mixins, _ALL_VERSIONS_BASE])}):",
            f'    """An :class:`~idfkit.document.IDFDocument` typed for EnergyPlus {version_string(ver)}."""',
            "",
            *_generate_getitem(entries, label),
            "",
        ]
        modules[f"{_versioned_module(ver)}.pyi"] = "\n".join(lines)
    return modules


def _range_alias(kind: str, ver: Version) -> str:
    """``IDFDocumentSince9_6`` or ``IDFDocumentBefore9_6``."""
    return f"IDFDocument{kind}{_version_tag(ver)}"


def _range_typing(versions: list[Version]) -> tuple[list[str], list[str]]:
    """The stub's range aliases, and the ``as_version`` overloads for ``since=`` and ``before=``.

    Every range is written out as the union of its releases, because a type checker cannot compute
    one from a version number. Each bound is a release's document type or its number as a string
    literal; the overloads are tried in order, and a release's own type selects its own overload.
    A bound the checker cannot read as one release (a ``str`` variable, an optional, a version
    tuple, or a literal no supported release has) falls through to the last two overloads, typed
    ``AnyIDFDocument``, and is checked only at run time. ``as_version(doc)`` matches none.
    """
    latest = versions[-1]

    def cls(ver: Version) -> str:
        return "IDFDocument" if ver == latest else _document_class_name(ver)

    def union(members: list[Version]) -> str:
        return " | ".join(cls(ver) for ver in members)

    def bound(ver: Version) -> str:
        return f'type[{cls(ver)}] | Literal["{ver[0]}.{ver[1]}", "{version_string(ver)}"]'

    aliases: list[str] = [
        "# Ranges of releases: a type to annotate with, and the as_version overloads that narrow to one.",
        "# Each lists the releases this idfkit supports, so a range from a release on grows when one is added.",
        "",
        *(f"{_range_alias('Since', ver)}: TypeAlias = {union(versions[i:])}" for i, ver in enumerate(versions)),
        *(
            f"{_range_alias('Before', ver)}: TypeAlias = {union(versions[:i])}"
            for i, ver in enumerate(versions[1:], start=1)
        ),
        "",
    ]
    overloads: list[str] = []
    for ver in versions:
        overloads.append("@overload")
        overloads.append(
            f"def as_version(doc: AnyIDFDocument, *, since: {bound(ver)}) -> {_range_alias('Since', ver)}: ..."
        )
    for ver in versions[1:]:
        overloads.append("@overload")
        overloads.append(
            f"def as_version(doc: AnyIDFDocument, *, before: {bound(ver)}) -> {_range_alias('Before', ver)}: ..."
        )
    for i, low in enumerate(versions):
        for j in range(i + 1, len(versions)):
            overloads.append("@overload")
            overloads.append(
                f"def as_version(doc: AnyIDFDocument, *, since: {bound(low)}, before: {bound(versions[j])})"
                f" -> {union(versions[i:j])}: ..."
            )
    # The fallbacks: since= required in one and before= in the other, so a call with neither stays an error.
    overloads.extend([
        "@overload",
        f"def as_version(doc: AnyIDFDocument, *, since: {_ANY_BOUND} | None, before: {_ANY_BOUND} | None = None)"
        " -> AnyIDFDocument: ...",
        "@overload",
        f"def as_version(doc: AnyIDFDocument, *, before: {_ANY_BOUND} | None) -> AnyIDFDocument: ...",
        "",
    ])
    return aliases, overloads


_ANY_BOUND = "type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int]"


def generate_versioned_py() -> str:
    """Generate ``versioned.py``, the run-time half of ``versioned.pyi``.

    At run time a per-version type is a stand-in: ``isinstance`` holds for a document of that
    version, and :func:`idfkit.versioned.as_version` checks against it. The classes with fields
    exist only for type checkers.

    It describes every release idfkit bundles, whatever ``SUPPORTED`` says: the stand-ins are
    checked against the run time's releases, and ``as_version`` takes ``IDFDocument`` to mean
    ``LATEST_VERSION``. Generated for a list cut short at 24.1 (``generate_stubs 24.1.0``), it would
    bind ``IDFDocumentV24_1`` to ``IDFDocument``, which rejects a 24.1 document and accepts a 26.2
    one, and drop the later releases' types from the running package.
    """
    versions = ENERGYPLUS_VERSIONS
    _check_version_tags(versions)
    names = [_document_class_name(ver) for ver in versions]
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
        "from ._document_types import as_version, document_type, release_type_var, release_union",
        "from .document import AnyIDFDocument, IDFDocument",
        "",
        "__all__ = [",
        '    "AnyIDFDocument",',
        # In the order ruff's RUF022 sorts them: Before, Since, then the release types.
        *(f'    "{_range_alias("Before", ver)}",' for ver in versions[1:]),
        *(f'    "{_range_alias("Since", ver)}",' for ver in versions),
        *(f'    "{name}",' for name in names),
        '    "ReleaseDocumentT",',
        '    "as_version",',
        "]",
        "",
    ]
    for ver in versions:
        if ver == versions[-1]:
            lines.append(f"{_document_class_name(ver)} = IDFDocument")
        else:
            lines.append(f'{_document_class_name(ver)} = document_type("{_document_class_name(ver)}", {ver!r})')
    lines.append("")
    lines.extend([
        "ReleaseDocumentT = release_type_var(",
        '    "ReleaseDocumentT",',
        *(f"    {name}," for name in names),
        ")",
    ])
    lines.extend(_RELEASE_DOCUMENT_T_DOC)
    lines.append("")
    lines.append("# Ranges of releases, typed in versioned.pyi. At run time each is the union of its releases.")
    # One member per line, with a trailing comma, so the output is already as ruff formats it.
    for i, ver in enumerate(versions):
        lines.extend([f"{_range_alias('Since', ver)} = release_union(", *(f"    {n}," for n in names[i:]), ")"])
    for i, ver in enumerate(versions[1:], start=1):
        lines.extend([f"{_range_alias('Before', ver)} = release_union(", *(f"    {n}," for n in names[:i]), ")"])
    lines.append("")
    return "\n".join(lines)


# The docstring of ReleaseDocumentT, written into both halves of the module.
_RELEASE_DOCUMENT_T_DOC = (
    '"""A type variable that is exactly one release\'s document type.',
    "",
    "Constrained to ``IDFDocumentV8_9`` ... ``IDFDocument``, so ``type[ReleaseDocumentT]`` accepts one",
    "release's type and refuses ``AnyIDFDocument``, which names no single release. A union of release",
    "types names none either: mypy refuses it, but pyright tries each member against the constraints",
    "and accepts it, so check at run time too. :func:`idfkit.migration.migrate` takes its target this",
    "way, and raises ``TypeError`` for a union.",
    '"""',
)


_AS_VERSION_DOC = """Type *doc* as a document of the EnergyPlus version *document_type* stands for.

Returns *doc* itself. A document's version is read from its file, so a type checker cannot
know it; this states it, and checks it at run time. Given a tuple of document types, as
``isinstance`` takes one, it accepts a document of any of them and types it as their union.

For a range of releases, such as those that have ``Space``, give ``since=`` and/or ``before=``
instead of *document_type*: it accepts a document of any release idfkit supports from *since* on
and before *before*, and types it as their union. Each bound is a release's document type, its
number or its version tuple: ``since=IDFDocumentV9_6``, ``since="9.6"`` or ``since=(9, 6, 0)``.
The range is computed from the releases idfkit supports, so it grows when idfkit adds one, and no
list of releases needs maintaining. ``IDFDocumentSince9_6`` and ``IDFDocumentBefore9_6`` are the
same ranges as types, to annotate with; pass ``since=``, not the alias, to this function.

A type checker reads a range only from a release's type or a string literal. A bound held in a
variable, an optional bound or a version tuple types the document as ``AnyIDFDocument``, and so
does a literal no supported release has (``since="27.1"``) or a range with no release in it;
those raise ``ValueError`` when the call runs.

Name a bound by its release, ``"{latest_number}"`` or ``{latest}``, not ``IDFDocument``: as a bound,
``IDFDocument`` stands for the latest release when the code runs, so ``since=IDFDocument`` stops
accepting a model of today's latest release once idfkit adopts the next one.

Check a release with this function, not ``isinstance``: at run time ``{latest}`` is
``IDFDocument`` itself, which every document is an instance of, so
``isinstance(doc, IDFDocument)`` holds for a document of any release while a type checker then
types it as the latest one. Nothing needs passing to reach ``AnyIDFDocument``: a document of any
release already is one.

In a tuple, name every release by its own type, the latest included: ``{latest}``, not
``IDFDocument``. ``IDFDocument`` stands for whichever release is latest when the code runs, so
once idfkit supports a newer release, a model of the release that was latest when the tuple was
written matches nothing in it, and this raises ``TypeError``. A range given by ``since=`` has
neither problem.

Args:
    doc: A document of any supported version.
    document_type: ``IDFDocument`` for the latest release, or one of the
        ``IDFDocumentV<major>_<minor>`` types of this module, or a tuple of them.
    since: The first release of a range: its document type, ``"major.minor"`` or a version tuple.
    before: The release a range stops before, the same way.

Returns:
    *doc*, typed as *document_type*, or as the union of the releases in the tuple or range.

Raises:
    TypeError: If *doc* is not a document of that version, or of any version in the tuple or
        range; or if both *document_type* and a range are given, or neither.
    ValueError: If *since* or *before* names no supported release, or the range holds none.

Examples:
    ```python
    from idfkit import load_idf
    from idfkit.versioned import IDFDocumentV9_4, as_version

    model = as_version(load_idf("legacy.idf"), IDFDocumentV9_4)
    model["Zone"].first()  # typed as Zone was declared in 9.4

    recent = as_version(load_idf("model.idf"), since="9.6")  # 9.6, 22.1, ... and the latest
    recent["Space"].first()  # typed in each of those releases
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


def generate_stubs(version: tuple[int, int, int] | None = None, sink: _CreationModules | None = None) -> str:
    """Generate the full ``_generated_types.pyi`` content.

    Args:
        version: The release to type ``IDFDocument`` for, as if it were the newest supported;
            defaults to the latest release.
        sink: Where the classes' creation signatures are filed (:class:`_CreationModules`); they
            are dropped when ``None``.

    Returns:
        Complete Python source for the generated types module.
    """
    with _as_latest(version):
        return _generate_types_module(sink)


def _generate_types_module(sink: _CreationModules | None = None) -> str:
    """``_generated_types.pyi``, filing its classes' creation signatures in *sink* (see :class:`_CreationModules`)."""
    sink = sink if sink is not None else _CreationModules()
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
    parts.append("from collections.abc import Mapping, Sequence")
    parts.append("from typing import Any, Literal, TypeAlias, TypedDict")
    parts.append("")
    parts.append("from typing_extensions import Never, Unpack")
    parts.append("")
    parts.extend(sink.imports())
    parts.append("from .objects import ExtensibleGroup, ExtensibleList, IDFCollection, IDFObject")
    parts.append("")
    parts.extend(_generate_typed_bases())
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
            parts.extend(_generate_base_class(schema, obj_type, layout[obj_type], type_since, field_since, sink))
            parts.append("")
            class_lines = _generate_object_class(
                schema,
                obj_type,
                type_since=type_since,
                field_since=field_since,
                base=_shared_class_name(obj_type),
                group_base=_group_base_for(obj_type),
                skip_fields=layout[obj_type].identical,
                omit_group=layout[obj_type].group,
                fields_base=_common_fields_name(obj_type),
                inherited=_common_entries(schema, obj_type, layout[obj_type]),
                sink=sink,
                creation=_class_creation(obj_type, [ver]),
            )
        else:
            class_lines = _generate_object_class(
                schema,
                obj_type,
                type_since=type_since,
                field_since=field_since,
                sink=sink,
                creation=_class_creation(obj_type, [ver]),
            )
        parts.extend(class_lines)
        parts.append("")

    parts.append("# =========================================================================")
    parts.append("# Any<Class> for the types every version that has them declares alike")
    parts.append("# =========================================================================")
    parts.append("")
    parts.extend(_generate_any_aliases(schema))
    parts.append("")

    return "\n".join(sink.drop_unused_imports(parts))


_ANY_DOCUMENT_DOC = """A document of any supported EnergyPlus version.

:class:`IDFDocument`, typed for the latest release, and every older release's type in
:mod:`idfkit.versioned` derive from it, so annotate with it to accept a document whatever its
version. Through it, a document offers what every supported version has: the object types
present in all of them, each typed as all of them declare it, so a field whose choices changed
between releases reads as the union of them, accepts only their intersection, and a field some
release lacks is not offered.

``"Space" in doc`` does not change this type: it is true when the document holds a ``Space``, and
false for a release without the type and for one that has it but holds none, so it says nothing
about the release. Narrow with ``idfkit.versioned.as_version`` to reach what only some releases
have.
"""

_ANY_VERSION_DOCUMENT_DOC = """A document as every supported EnergyPlus version has it.

Indexing it, or reaching an accessor, with an object type that some supported version lacks is a
type error, as is a field some version lacks through ``update``. ``AnyIDFDocument`` is this class;
annotate with that name. :class:`IDFDocument` and every document type in :mod:`idfkit.versioned`
derive from it. Narrow a document to its release with ``idfkit.versioned.as_version`` to reach what
only that release has.
"""


def _any_accessor_types() -> dict[str, str]:
    """Each ``AnyIDFDocument`` accessor, a name that reaches the same type in every version, and its class."""
    per_version = [_accessors(ver) for ver in SUPPORTED.versions]
    common = set(_common_object_types())
    return {
        name: _shared_class_name(obj_type)
        for name, obj_type in per_version[-1].items()
        if obj_type in common and all(accessors.get(name) == obj_type for accessors in per_version)
    }


def _generate_any_accessors() -> list[str]:
    """Typed accessors of ``AnyIDFDocument``: names that reach the same type in every version."""
    lines: list[str] = []
    for name, cls in _any_accessor_types().items():
        lines.append("    @property")
        lines.append(f"    def {name}(self) -> IDFCollection[{cls}]: ...")
    return lines


def generate_document_pyi(version: tuple[int, int, int] | None = None) -> str:
    """Generate ``document.pyi`` — a type stub for ``document.py``.

    The stub types ``doc["Zone"]`` with one ``__getitem__`` overload per object type
    (:func:`_generate_getitem`), on ``IDFDocument`` and on ``IDFDocumentAllVersions``,
    which every document type derives from.

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
    lines.append("from typing import Any, Generic, Literal, TypeAlias, TypeVar, overload")
    lines.append("")
    lines.append("from typing_extensions import Never, Self")
    lines.append("")
    lines.append("from ._accessors import AccessorResolver")
    lines.append("from ._compat import EppyDocumentMixin")
    lines.append("from ._generated_types import *  # noqa: F403")
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

    # The methods live on a plain mixin, the base of IDFDocumentAllVersions, from which every document
    # type -- the latest one and each older version's -- derives, each with its own __getitem__.
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
    emit("def __contains__(self, obj_type: str) -> bool", "IDFDocument.__contains__")
    emit("def __iter__(self) -> Iterator[str]", "IDFDocument.__iter__")
    emit("def __len__(self) -> int", "IDFDocument.__len__")
    emit("def keys(self) -> list[str]", "IDFDocument.keys")
    emit("def values(self) -> list[IDFCollection[IDFObject]]", "IDFDocument.values")
    emit("def items(self) -> list[tuple[str, IDFCollection[IDFObject]]]", "IDFDocument.items")
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

    # Its name is what a type checker prints when code reaches for an object type or an accessor some
    # supported version lacks, so it says what the type is rather than being private. Every document
    # type derives from it, so a document of any release is an AnyIDFDocument by name: a check that
    # costs nothing, where comparing ~800 keys structurally, as TypedDicts were, cost every call.
    lines.extend(_generate_not_an_object_type("EveryRelease", "every supported EnergyPlus release has"))
    lines.append("")
    lines.append(f"class IDFDocumentAllVersions({_METHODS_BASE}):")
    lines.extend(_format_docstring_for_stub(_ANY_VERSION_DOCUMENT_DOC, "    "))
    lines.append("")
    getitem_doc = docs.get("IDFDocument.__getitem__")
    common = [(t, _shared_class_name(t)) for t in _common_object_types()]
    lines.extend(_generate_getitem(common, "EveryRelease", getitem_doc))
    lines.append("")
    lines.extend(_generate_any_accessors())
    lines.append("")
    lines.append("AnyIDFDocument: TypeAlias = IDFDocumentAllVersions[Strict]")
    lines.extend(_format_docstring_for_stub(_ANY_DOCUMENT_DOC, ""))
    lines.append("")
    latest_label = f"EnergyPlus{_version_tag(ver)}"
    lines.extend(_generate_not_an_object_type(latest_label, f"EnergyPlus {version_str} has"))
    lines.append("")

    lines.append(f"class IDFDocument({_ALL_VERSIONS_BASE}):")
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

    lines.extend(_generate_getitem([(t, _to_class_name(t)) for t in schema.object_types], latest_label, getitem_doc))
    lines.append("")

    # Attribute accessor properties, one per object type plus the shorthands, with memo docstrings
    lines.extend(_generate_attr_properties(_build_resolver(schema).accessors(), schema, indent="    "))
    lines.append("")

    return "\n".join(lines)


_CREATION_PACKAGE_DOC = '''"""The creation signatures of the generated classes, one module per bucket of classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs

Each generated class declares ``_creation_signature`` as an instance of a class defined here, whose
``__call__`` is the signature ``IDFCollection.add`` takes: the name, the required fields, the others
with their defaults. Kept apart from the classes so that a type checker reads a module only when it
checks an ``add()`` call on one of its classes.
"""
'''


def generate_read_required_py() -> str:
    """The run-time table of :func:`read_required`: ``_read_required.py``."""
    lines = [
        '"""The fields reading gives a value for, by object type. GENERATED by idfkit.codegen.generate_stubs.',
        "",
        "A field is listed when every supported release that has it requires it with no default. Its",
        "read type is not optional, and reading it from an object that lacks it raises",
        "``MissingRequiredFieldError`` rather than returning ``None``.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "# Tuples of string literals are constants of the compiled module: importing it builds no set.",
        "READ_REQUIRED: dict[str, tuple[str, ...]] = {",
    ]
    for obj_type, fields in read_required().items():
        lines.append(f"    {obj_type!r}: {tuple(sorted(fields))!r},")
    lines += ["}", ""]
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
    creation = _CreationModules()
    versioned_creation = _CreationModules("_v", "_cv")
    content = _generate_types_module(creation)
    doc_pyi = _generate_document_module()

    types_path = base_path / "_generated_types.pyi"
    types_path.write_text(content, encoding="utf-8")

    pyi_path = base_path / "document.pyi"
    pyi_path.write_text(doc_pyi, encoding="utf-8")

    versioned_path = base_path / "versioned.pyi"
    versioned_path.write_text(generate_versioned_pyi(versioned_creation), encoding="utf-8")

    versioned_runtime_path = base_path / "versioned.py"
    versioned_runtime_path.write_text(generate_versioned_py(), encoding="utf-8")

    required_path = base_path / "_read_required.py"
    required_path.write_text(generate_read_required_py(), encoding="utf-8")

    # One stub per older release. A module left from a release that has since become the latest (or
    # stopped being supported) is removed, or it would still define a type versioned.pyi no longer has.
    documents_dir = base_path / "_versioned"
    documents_dir.mkdir(exist_ok=True)
    documents = generate_versioned_documents()
    for stale in documents_dir.glob("*.pyi"):
        if stale.name not in documents:
            stale.unlink()
    document_paths = [documents_dir / name for name in documents]
    for path in document_paths:
        path.write_text(documents[path.name], encoding="utf-8")

    creation_dir = base_path / "_creation"
    creation_dir.mkdir(exist_ok=True)
    creation_sources = {"__init__.pyi": _CREATION_PACKAGE_DOC, **creation.sources(), **versioned_creation.sources()}
    for stale in creation_dir.glob("*.pyi"):
        if stale.name not in creation_sources:
            stale.unlink()
    creation_paths = [creation_dir / name for name in creation_sources]
    for path in creation_paths:
        path.write_text(creation_sources[path.name], encoding="utf-8")

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
            str(required_path),
            *(str(path) for path in document_paths),
            *(str(path) for path in creation_paths),
        ],
        check=False,
    )
    from idfkit.codegen.verify_stubs import verify

    problems = verify(
        types_path.read_text(encoding="utf-8"),
        pyi_path.read_text(encoding="utf-8"),
        [versioned_path.read_text(encoding="utf-8"), *(path.read_text(encoding="utf-8") for path in document_paths)],
        SUPPORTED.versions,
        {path.stem: path.read_text(encoding="utf-8") for path in creation_paths},
    )
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"The generated stubs misdescribe {len(problems)} version-specific declarations.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Generated {types_path} ({types_path.stat().st_size:,} bytes)")
    print(f"Generated {pyi_path} ({pyi_path.stat().st_size:,} bytes)")
    print(f"Generated {versioned_path} ({versioned_path.stat().st_size:,} bytes)")
    print(f"Generated {documents_dir} ({len(document_paths)} modules)")


if __name__ == "__main__":
    main()
