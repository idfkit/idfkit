"""Check the generated stubs against the bundled schemas, version by version.

The per-version typing in ``versioned.pyi`` and ``_versioned/`` is assembled from pieces: classes
shared between versions, classes of one version range, and accessors filed under the range of
versions they hold over. This module does not trust that assembly. It reads the generated sources back,
resolves what a type checker would see for each object type in each supported version, and
compares it with that version's schema. What a field may hold is read from the schema here, not
taken from the generator, so a fault in how the generator maps a schema type is reported rather
than repeated:

* the object types a version's document can be indexed with are exactly the version's types,
  each overloaded once on the document class itself, the last overload matching no name, and every
  document type derives from ``IDFDocumentAllVersions``;
* every type's class has exactly the version's fields, each with the version's value type, and
  its extensible group exactly the version's inner fields;
* every class's ``update`` keywords are exactly its fields;
* a version's document has exactly the version's attribute accessors, each typed with the class
  of its object type in that version;
* ``AnyIDFDocument`` offers exactly the types every version has, each with exactly the fields
  every version has, and each field's type admits every version's values;
* every ``IDFDocumentSince``/``IDFDocumentBefore`` alias is exactly its range's releases, and every
  ``as_version`` overload for ``since=``/``before=`` is typed with exactly the releases its bounds
  name, one overload for each non-empty range.

``generate_stubs`` runs this after writing and fails if anything is reported, so adopting an
EnergyPlus release cannot regenerate stubs that misdescribe a version. The tests run it too,
including against a version list cut short, which is what adopting the next release looks like.
"""

from __future__ import annotations

import ast
import dataclasses
import functools
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from idfkit.schema import EpJSONSchema

Version = tuple[int, int, int]


@dataclasses.dataclass
class _Class:
    """What a generated class declares itself."""

    bases: list[str]
    fields: dict[str, str]
    properties: dict[str, str]
    # A property with a setter is a field: its getter's type is what reading it gives, and is in
    # ``fields``; its setter's value type, what assigning to it accepts, is here.
    setters: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
    # ``__getitem__`` overloads in order: the literal object type each takes (``None`` for one that
    # takes anything else), the type it returns, and its parameter's annotation.
    getitem: list[tuple[str | None, str, str]] = dataclasses.field(default_factory=list[tuple[str | None, str, str]])


@dataclasses.dataclass
class _Module:
    """The classes and type aliases of the generated sources."""

    classes: dict[str, _Class] = dataclasses.field(default_factory=dict[str, _Class])
    # Module-level ``Name: TypeAlias = Target``: the alias and the class it names.
    aliases: dict[str, str] = dataclasses.field(default_factory=dict[str, str])


@functools.cache
def _norm(annotation: str) -> str:
    """Normalise an annotation's spelling, so line wrapping and the ``_g.`` and ``_v.`` prefixes do not count."""
    return ast.unparse(ast.parse(annotation.replace("_g.", "").replace("_v.", ""), mode="eval"))


def _base_name(node: ast.expr) -> str:
    """A base class's name, without its module prefix or type arguments: ``IDFDocumentAllVersions``."""
    if isinstance(node, ast.Subscript):
        node = node.value
    return ast.unparse(node).replace("_g.", "").replace("_v.", "")


def _getitem_overload(item: ast.FunctionDef) -> tuple[str | None, str, str] | None:
    """``("Zone", "IDFCollection[Zone]", ...)`` for a ``__getitem__`` overload on ``Literal["Zone"]``."""
    if item.name != "__getitem__" or item.returns is None or len(item.args.posonlyargs) != 2:
        return None
    annotation = item.args.posonlyargs[1].annotation
    if annotation is None:
        return None
    key: str | None = None
    if (
        isinstance(annotation, ast.Subscript)
        and ast.unparse(annotation.value) == "Literal"
        and isinstance(annotation.slice, ast.Constant)
        and isinstance(annotation.slice.value, str)
    ):
        key = annotation.slice.value
    return key, _norm(ast.unparse(item.returns)), ast.unparse(annotation)


def _read_class(node: ast.ClassDef) -> _Class:
    """What one generated class declares: its bases, fields, properties, and setters."""
    cls = _Class([_base_name(b) for b in node.bases], {}, {})
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            cls.fields[item.target.id] = _norm(ast.unparse(item.annotation))
        elif not isinstance(item, ast.FunctionDef):
            continue
        elif (overload := _getitem_overload(item)) is not None:
            cls.getitem.append(overload)
        elif item.returns is not None and any(ast.unparse(d) == "property" for d in item.decorator_list):
            cls.properties[item.name] = _norm(ast.unparse(item.returns))
        elif (
            any(ast.unparse(d) == f"{item.name}.setter" for d in item.decorator_list)
            and len(item.args.args) == 2
            and item.args.args[1].annotation is not None
        ):
            cls.setters[item.name] = _norm(ast.unparse(item.args.args[1].annotation))
    for name in cls.setters:
        cls.fields[name] = cls.properties.pop(name)
    return cls


def _read(source: str, module: _Module | None = None) -> _Module:
    module = module if module is not None else _Module()
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            module.classes[node.name] = _read_class(node)
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.value is not None
            and ast.unparse(node.annotation) == "TypeAlias"
        ):
            module.aliases[node.target.id] = ast.unparse(node.value)
    return module


def _linearise(module: _Module, name: str) -> list[str]:
    """*name* and the generated classes it derives from, each overriding those before it.

    Bases are taken last first, so that where two declare the same attribute the first base wins,
    as it does in Python's method resolution order.
    """
    order: list[str] = []
    for base in reversed(module.classes[name].bases):
        if base in module.classes:
            for item in _linearise(module, base):
                if item not in order:
                    order.append(item)
    order.append(name)
    return order


def _fields(module: _Module, name: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in _linearise(module, name):
        if item in module.classes:
            out.update(module.classes[item].fields)
    return out


def _properties(module: _Module, name: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in _linearise(module, name):
        if item in module.classes:
            out.update(module.classes[item].properties)
    return out


def _getitem_entries(module: _Module, name: str, problems: list[str]) -> dict[str, str]:
    """What *name* is indexed with: object type -> collection type, from its own ``__getitem__`` overloads.

    Overloads do not merge across base classes, so only the class's own count. A type overloaded
    twice, and a class whose last overload takes an object type name (so that a name it lacks would
    match it, rather than be an error), are reported.
    """
    overloads = module.classes[name].getitem
    out: dict[str, str] = {}
    for key, value, _ in overloads:
        if key is None:
            continue
        if key in out:
            problems.append(f"{name}: {key!r} is overloaded twice")
        out[key] = value
    # The last takes a class no string is: one taking str, or none at all, would let a name the
    # release lacks type-check.
    last = overloads[-1][2] if overloads else ""
    if (
        not last.startswith("_NotAnObjectTypeOf")
        or last not in module.classes
        or any(key is None for key, _, _ in overloads[:-1])
    ):
        problems.append(f"{name}: __getitem__ does not end with the one overload that matches no object type")
    return out


def _collection_class(annotation: str) -> str:
    """``IDFCollection[Zone]`` -> ``Zone``.

    ``""`` for an annotation that is not subscripted, which names no class, so a caller reports it
    as an undefined class rather than this module stopping on an assertion.
    """
    node = ast.parse(annotation, mode="eval").body
    return ast.unparse(node.slice) if isinstance(node, ast.Subscript) else ""


@functools.cache
def _union_members(annotation: str) -> frozenset[str]:
    """The members of a union, with every ``Literal`` member counted on its own."""
    members: set[str] = set()

    def walk(node: ast.expr) -> None:
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            walk(node.left)
            walk(node.right)
        elif isinstance(node, ast.Subscript) and ast.unparse(node.value) == "Literal":
            elts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            members.update(f"Literal[{ast.unparse(e)}]" for e in elts)
        else:
            members.add(ast.unparse(node))

    walk(ast.parse(annotation, mode="eval").body)
    return frozenset(members)


_SCALARS = {"number": "float", "integer": "int", "string": "str", "array": "list[Any]"}


def _literal(value: object) -> str:
    return f"Literal[{value!r}]"


def _value_members(field_schema: dict[str, Any] | None, field_type: str | None) -> frozenset[str]:
    """What a field may hold, as union members with ``None``, read from its schema.

    Derived here rather than taken from the generator, so a fault in how the generator maps a schema
    to a value type is a disagreement this module reports, not one it repeats. A field restricted to
    an ``enum`` holds those values; an ``anyOf`` holds each branch's values, an ``enum`` branch's
    listed and any other branch's by its type; and a field with no usable type holds a string or a
    number, as EnergyPlus reads it.
    """
    members: set[str] = {"None"}
    if field_schema is not None and "enum" in field_schema:
        return frozenset(members | {_literal(v) for v in field_schema["enum"]})
    if field_schema is not None and "anyOf" in field_schema:
        for branch in field_schema["anyOf"]:
            kind = branch.get("type")
            if kind not in ("number", "integer", "string"):
                continue
            if "enum" in branch:
                members.update(_literal(v) for v in branch["enum"])
            else:
                members.add(_SCALARS[kind])
        return frozenset(members if len(members) > 1 else {"None", "str", "float"})
    scalar = _SCALARS.get(field_type) if field_type is not None else None
    return frozenset(members | ({scalar} if scalar else {"str", "float"}))


def _schema_fields(schema: EpJSONSchema, obj_type: str) -> dict[str, frozenset[str]]:
    """Each attribute a typed object of *obj_type* has, with the values it may hold.

    The schema's identifier fields, then the spelling without the trailing underscore of each that
    has one, as :class:`~idfkit.objects.IDFObject` resolves it at run time.
    """
    from idfkit.schema import trailing_underscore_aliases

    inner = schema.get_inner_schema(obj_type)
    properties: dict[str, Any] = inner.get("properties", {}) if inner else {}
    names = schema.get_field_names(obj_type)
    fields = {
        name: _value_members(properties.get(name), schema.get_field_type(obj_type, name))
        for name in names
        if name.isidentifier()
    }
    for alias, key in trailing_underscore_aliases(names).items():
        if alias != key and alias.isidentifier() and alias not in fields and key in fields:
            fields[alias] = fields[key]
    return fields


def _schema_group(schema: EpJSONSchema, obj_type: str) -> tuple[str, dict[str, frozenset[str]]] | None:
    """The extensible wrapper key of *obj_type* and the values each inner field may hold, or ``None``."""
    pc = schema.get_parsing_cache(obj_type)
    if pc is None or not pc.ext_wrapper_key or not pc.ext_inner_props:
        return None
    inner = {
        name: _value_members(sub, sub.get("type") if isinstance(sub.get("type"), str) else None)
        for name, sub in pc.ext_inner_props.items()
        if name.isidentifier()
    }
    return pc.ext_wrapper_key, inner


def _members_of(fields: dict[str, str]) -> dict[str, frozenset[str]]:
    return {name: _union_members(annotation) for name, annotation in fields.items()}


def _expected_fields(
    ver: Version, obj_type: str
) -> tuple[dict[str, frozenset[str]], tuple[str, dict[str, frozenset[str]]] | None]:
    """The fields of *obj_type* in *ver* as the stubs must declare them, and its group if any."""
    from idfkit.schema import get_schema

    schema = get_schema(ver)
    return _schema_fields(schema, obj_type), _schema_group(schema, obj_type)


def _check_class(module: _Module, cls: str, ver: Version, obj_type: str, problems: list[str]) -> None:
    where = f"{obj_type} in {'.'.join(map(str, ver))} ({cls})"
    if cls not in module.classes:
        problems.append(f"{where}: class not defined")
        return
    expected, group = _expected_fields(ver, obj_type)
    actual = _members_of(_fields(module, cls))
    keywords = dict(expected)
    if group is not None:
        wrapper, inner = group
        annotation = _fields(module, cls).get(wrapper)
        actual.pop(wrapper, None)
        if annotation is None:
            problems.append(f"{where}: no {wrapper} attribute")
        else:
            group_cls = _collection_class(annotation)
            if group_cls not in module.classes or _members_of(_fields(module, group_cls)) != inner:
                problems.append(f"{where}: group {group_cls} does not hold the version's inner fields")
        keywords[wrapper] = frozenset({"list[Any]"})
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        retyped = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        problems.append(f"{where}: missing {missing}, extra {extra}, mistyped {retyped}")
    _check_update(module, cls, keywords, where, problems)


def _check_update(
    module: _Module, cls: str, keywords: dict[str, frozenset[str]], where: str, problems: list[str]
) -> None:
    """The ``update`` keywords of *cls*: those of the nearest class in its line that types them.

    A class with no keyword to type keeps ``IDFObject.update``, as the latest classes always have.
    """
    if not any(k != "name" for k in keywords):
        return
    for item in reversed(_linearise(module, cls)):
        fields_cls = f"_{item}Fields"
        if fields_cls in module.classes:
            expected = {k: v for k, v in keywords.items() if k != "name"}
            if _members_of(_fields(module, fields_cls)) != expected:
                problems.append(f"{where}: update keywords ({fields_cls}) differ from its fields")
            return
    problems.append(f"{where}: update is not typed")


def verify(
    types_source: str, document_source: str, versioned_sources: Iterable[str], versions: tuple[Version, ...]
) -> list[str]:
    """Report every way the generated stubs misdescribe a supported version; empty when none.

    Args:
        types_source: The generated ``_generated_types.pyi``.
        document_source: The generated ``document.pyi``.
        versioned_sources: The generated ``versioned.pyi`` and the modules of ``_versioned/``, which
            define the older releases' document types.
        versions: The releases the stubs were generated to describe, oldest first; the last is the
            one ``IDFDocument`` is typed for. Passed rather than read from the generator, which may
            be running as ``__main__``, a second copy of its module.
    """
    sources = list(versioned_sources)
    module = _read(document_source, _read(types_source))
    for source in sources:
        module = _read(source, module)
    problems: list[str] = []
    for ver in versions:
        _check_version(module, ver, ver == versions[-1], problems)
    _check_any_document(module, versions, problems)
    _check_any_names(module, versions[-1], problems)
    _check_ranges(module, sources, versions, problems)
    return problems


@dataclasses.dataclass(frozen=True)
class _Ranges:
    """The supported releases, as the range aliases and overloads of ``versioned.pyi`` name them."""

    module: _Module
    versions: tuple[Version, ...]

    def name(self, ver: Version) -> str:
        return "IDFDocument" if ver == self.versions[-1] else f"IDFDocumentV{ver[0]}_{ver[1]}"

    def release(self, name: str) -> Version | None:
        return next((ver for ver in self.versions if self.name(ver) == name), None)

    def members(self, low: Version | None, high: Version | None) -> frozenset[str]:
        """The class names of the releases from *low* (inclusive) to *high* (exclusive)."""
        return frozenset(
            self.name(v) for v in self.versions if (low is None or v >= low) and (high is None or v < high)
        )

    def union(self, annotation: str) -> frozenset[str]:
        """The classes an annotation names, with range aliases resolved."""
        resolved: set[str] = set()
        for part in annotation.split("|"):
            name = part.strip()
            alias = self.module.aliases.get(name)
            resolved |= self.union(alias) if alias is not None and name.startswith("IDFDocument") else {name}
        return frozenset(resolved)


def _check_ranges(
    module: _Module, versioned_sources: list[str], versions: tuple[Version, ...], problems: list[str]
) -> None:
    """The range aliases and the ``since=``/``before=`` overloads of ``as_version`` name the right releases."""
    ranges = _Ranges(module, versions)
    for i, ver in enumerate(versions):
        _check_range_alias(ranges, f"IDFDocumentSince{ver[0]}_{ver[1]}", ranges.members(ver, None), problems)
        if i:
            _check_range_alias(ranges, f"IDFDocumentBefore{ver[0]}_{ver[1]}", ranges.members(None, ver), problems)
    seen: set[tuple[Version | None, Version | None]] = set()
    nodes = [node for source in versioned_sources for node in ast.parse(source).body]
    for node in nodes:
        if isinstance(node, ast.FunctionDef) and node.name == "as_version" and node.args.kwonlyargs:
            key = _check_range_overload(ranges, node, problems)
            if key is None:
                continue
            if key in seen:
                problems.append(f"as_version(since={key[0]}, before={key[1]}): more than one overload")
            seen.add(key)
    bounds = (None, *versions)
    wanted = {(low, high) for low in bounds for high in bounds if (low, high) != (None, None)}
    for low, high in sorted(wanted - seen, key=str):
        if ranges.members(low, high):
            problems.append(f"as_version(since={low}, before={high}): no overload")


def _check_range_alias(ranges: _Ranges, alias: str, expected: frozenset[str], problems: list[str]) -> None:
    value = ranges.module.aliases.get(alias)
    if value is None:
        problems.append(f"{alias}: missing")
    elif ranges.union(value) != expected:
        problems.append(f"{alias}: names {sorted(ranges.union(value))}, not {sorted(expected)}")


def _check_range_overload(
    ranges: _Ranges, node: ast.FunctionDef, problems: list[str]
) -> tuple[Version | None, Version | None] | None:
    """Check one keyword-only overload; its ``(since, before)``, or ``None`` for a fallback overload."""
    bounds: dict[str, Version | None] = {"since": None, "before": None}
    for arg in node.args.kwonlyargs:
        parts = [part.strip() for part in ast.unparse(arg.annotation).split("|")] if arg.annotation else []
        classes = [part[len("type[") : -1] for part in parts if part.startswith("type[")]
        literals = [part for part in parts if part.startswith("Literal[")]
        ver = ranges.release(classes[0]) if len(classes) == 1 else None
        if ver is None or len(literals) != 1:
            return None  # a fallback: any document type, any string, a tuple
        expected = f"Literal['{ver[0]}.{ver[1]}', '{ver[0]}.{ver[1]}.{ver[2]}']"
        if literals[0] != expected:
            problems.append(f"as_version({arg.arg}={classes[0]}): typed {literals[0]}, not {expected}")
        bounds[arg.arg] = ver
    key = (bounds["since"], bounds["before"])
    where = f"as_version(since={key[0]}, before={key[1]})"
    expected_members = ranges.members(*key)
    returned = ranges.union(ast.unparse(node.returns)) if node.returns is not None else frozenset[str]()
    if not expected_members:
        problems.append(f"{where}: an overload for an empty range")
    elif returned != expected_members:
        problems.append(f"{where}: returns {sorted(returned)}, not {sorted(expected_members)}")
    return key


def _check_any_names(module: _Module, latest: Version, problems: list[str]) -> None:
    """Every object type of the latest release has a public ``Any<Class>`` to annotate code for any release.

    It is the class ``AnyIDFDocument`` types the collection with when the type changed between
    versions, and otherwise an alias of the latest class, which is then that collection's class.
    """
    from idfkit.codegen.generate_stubs import _to_class_name  # pyright: ignore[reportPrivateUsage]
    from idfkit.schema import get_schema

    common = (
        _getitem_entries(module, "IDFDocumentAllVersions", []) if "IDFDocumentAllVersions" in module.classes else {}
    )
    for obj_type in get_schema(latest).object_types:
        cls = _to_class_name(obj_type)
        name = f"Any{cls}"
        if name in module.classes:
            if cls in module.classes and name not in _linearise(module, cls):
                problems.append(f"{name}: {cls} does not derive from it")
        elif module.aliases.get(name) != cls:
            problems.append(f"{obj_type}: no {name}, as a class or as an alias of {cls}")
            continue
        if obj_type in common and _collection_class(common[obj_type]) not in (name, cls):
            problems.append(f"AnyIDFDocument[{obj_type!r}]: typed with neither {name} nor {cls}")


def _admitted(member: str, members: frozenset[str]) -> bool:
    """Whether a value type, given as its union members, admits one member of another."""
    if member in members:
        return True
    if member == "int" and "float" in members:
        return True
    if member.startswith("Literal["):
        value = member[len("Literal[") : -1]
        if value.startswith(("'", '"')):
            return "str" in members
        return "float" in members or ("int" in members and "." not in value)
    return False


def _check_writable(
    module: _Module, cls: str, obj_type: str, decls: list[dict[str, frozenset[str]]], problems: list[str]
) -> None:
    """A shared base's assignable values are ones every version accepts, and ``update`` takes them.

    Each field that is a property is written through its setter: every member of the setter's value
    type must be admitted by every version's declaration of the field, or writing it into a document
    of some version would be accepted by the type checker and rejected by the version.
    """
    klass = module.classes[cls]
    for name, setter in klass.setters.items():
        if not all(name in decl for decl in decls):
            problems.append(f"AnyIDFDocument[{obj_type!r}].{name}: writable, but not a field of every version")
            continue
        members = _union_members(setter) - {"Never"}  # Never admits nothing: only clearing is safe
        for decl in decls:
            admitted = decl[name]
            if not all(_admitted(m, admitted) for m in members):
                problems.append(f"AnyIDFDocument[{obj_type!r}].{name}: writable values some version rejects")
                break
    if not klass.setters:
        return
    groups = set(_group_names(module, cls))
    keywords = {
        k: "list[Any]" if k in groups else klass.setters.get(k, v)
        for k, v in _fields(module, cls).items()
        if k != "name"
    }
    fields_cls = f"_{cls}Fields"
    if fields_cls not in module.classes:
        problems.append(f"AnyIDFDocument[{obj_type!r}] ({cls}): update is not typed")
    elif _fields(module, fields_cls) != keywords:
        problems.append(
            f"AnyIDFDocument[{obj_type!r}] ({cls}): update keywords ({fields_cls}) differ from its writable fields"
        )


def _check_any_group(
    module: _Module, cls: str, obj_type: str, schemas: list[EpJSONSchema], problems: list[str]
) -> None:
    """``Any<Class>`` declares the type's extensible group when every version has it under one key.

    Its fields must be ones every version's group has; reading one admits every version's values,
    and assigning one accepts only values every version accepts.
    """
    decls = [_schema_group(s, obj_type) for s in schemas]
    shared = [d for d in decls if d is not None]
    if len(shared) != len(decls) or len({d[0] for d in shared}) != 1:
        return
    wrapper = shared[0][0]
    annotation = _fields(module, cls).get(wrapper)
    if annotation is None or not annotation.startswith("ExtensibleList["):
        problems.append(f"{cls}: no {wrapper} group, though every version has one")
        return
    group_cls = _collection_class(annotation)
    if group_cls not in module.classes:
        problems.append(f"{cls}.{wrapper}: group class {group_cls} not defined")
        return
    inner = [d[1] for d in shared]
    setters = module.classes[group_cls].setters
    for name, read in _fields(module, group_cls).items():
        if not all(name in i for i in inner):
            problems.append(f"{group_cls}.{name}: not a field of every version's {wrapper} group")
            continue
        admitted = _union_members(read)
        if not all(i[name] <= admitted for i in inner):
            problems.append(f"{group_cls}.{name}: does not admit every version's values")
        writable = _union_members(setters.get(name, read)) - {"Never"}
        if not all(all(_admitted(m, i[name]) for m in writable) for i in inner):
            problems.append(f"{group_cls}.{name}: writable values some version rejects")


def _check_version(module: _Module, ver: Version, is_latest: bool, problems: list[str]) -> None:
    """Check the document type of one release: its map, every class it maps to, and its accessors."""
    from idfkit.document import _build_resolver  # pyright: ignore[reportPrivateUsage]
    from idfkit.schema import get_schema

    tag = f"{ver[0]}_{ver[1]}"
    schema = get_schema(ver)
    doc_name = "IDFDocument" if is_latest else f"IDFDocumentV{tag}"
    if doc_name not in module.classes:
        problems.append(f"{'.'.join(map(str, ver))}: no {doc_name}")
        return
    if "IDFDocumentAllVersions" not in _linearise(module, doc_name):
        problems.append(f"{doc_name}: does not derive from IDFDocumentAllVersions, so is not an AnyIDFDocument")
    entries = _getitem_entries(module, doc_name, problems)
    if set(entries) != set(schema.object_types):
        missing = sorted(set(schema.object_types) - set(entries))
        extra = sorted(set(entries) - set(schema.object_types))
        problems.append(f"{doc_name}: missing types {missing}, extra types {extra}")
    classes = {obj_type: _collection_class(annotation) for obj_type, annotation in entries.items()}
    for obj_type in schema.object_types:
        if obj_type in classes:
            _check_class(module, classes[obj_type], ver, obj_type, problems)
    if not is_latest:
        # A type missing from the overloads is reported above; its accessor is then expected untyped.
        expected_accessors = {
            name: f"IDFCollection[{classes.get(obj_type, '?')}]"
            for name, obj_type in _build_resolver(schema).accessors().items()
        }
        # Through IDFDocumentAllVersions it also has the shared document methods' properties (version, ...).
        shared = _properties(module, "_IDFDocumentMethods") if "_IDFDocumentMethods" in module.classes else {}
        accessors = {k: v for k, v in _properties(module, doc_name).items() if k not in shared}
        if accessors != expected_accessors:
            problems.append(f"{doc_name}: attribute accessors differ from the version's")


def _check_any_document(module: _Module, versions: tuple[Version, ...], problems: list[str]) -> None:
    from idfkit.schema import get_schema

    schemas = [get_schema(ver) for ver in versions]
    # Built once: object_types makes a new list on every read, and every entry below asks each version.
    type_sets = [set(s.object_types) for s in schemas]
    common = _intersection(type_sets)
    if "IDFDocumentAllVersions" not in module.classes:
        problems.append("AnyIDFDocument: no IDFDocumentAllVersions")
        return
    entries = _getitem_entries(module, "IDFDocumentAllVersions", problems)
    if set(entries) != common:
        # A type some version lacks is left out, so that indexing with it is a type error through
        # AnyIDFDocument; as_version reaches it.
        missing = sorted(common - set(entries))
        extra = sorted(set(entries) - common)
        problems.append(f"AnyIDFDocument: types are not those every version has: missing {missing}, extra {extra}")
    for obj_type, annotation in entries.items():
        _check_any_entry(module, obj_type, annotation, schemas, type_sets, problems)


def _check_any_entry(
    module: _Module,
    obj_type: str,
    annotation: str,
    schemas: list[EpJSONSchema],
    type_sets: list[set[str]],
    problems: list[str],
) -> None:
    """Check what ``AnyIDFDocument[obj_type]`` is typed with against every version that has the type."""
    if not annotation.startswith("IDFCollection["):
        problems.append(f"AnyIDFDocument[{obj_type!r}]: not IDFCollection[...]: {annotation}")
        return
    cls = _collection_class(annotation)
    cls = module.aliases.get(cls, cls)  # an alias of a class is that class to a type checker
    if cls not in module.classes:
        problems.append(f"AnyIDFDocument[{obj_type!r}]: class {cls or annotation} not defined")
        return
    having = [s for s, types in zip(schemas, type_sets, strict=True) if obj_type in types]
    if not having:
        return  # a type no version has, reported above as extra
    decls = [_schema_fields(s, obj_type) for s in having]
    shared = _intersection([set(d) for d in decls])
    _check_writable(module, cls, obj_type, decls, problems)
    _check_any_group(module, cls, obj_type, having, problems)
    groups = set(_group_names(module, cls))
    actual = {k: v for k, v in _fields(module, cls).items() if k not in groups}
    if set(actual) != shared:
        problems.append(f"AnyIDFDocument[{obj_type!r}] ({cls}): fields are not those every version has")
        return
    for name in shared:
        admitted = _union_members(actual[name])
        for decl in decls:
            if not decl[name] <= admitted:
                problems.append(f"AnyIDFDocument[{obj_type!r}].{name}: does not admit every version's values")
                break


def _intersection(sets: list[set[str]]) -> set[str]:
    out = set(sets[0])
    for other in sets[1:]:
        out &= other
    return out


def _group_names(module: _Module, cls: str) -> Iterable[str]:
    """Attributes of *cls* typed as an extensible list, which the field comparison leaves aside."""
    return [k for k, v in _fields(module, cls).items() if v.startswith("ExtensibleList[")]
