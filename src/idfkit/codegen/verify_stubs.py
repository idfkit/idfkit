"""Check the generated stubs against the bundled schemas, version by version.

The per-version typing in ``versioned.pyi`` is assembled from pieces: classes shared between
versions, classes of one version range, and maps and accessors filed under the range of versions
they hold over. This module does not trust that assembly. It reads the generated sources back,
resolves what a type checker would see for each object type in each supported version, and
compares it with that version's schema:

* the object types a version's document can be indexed with are exactly the version's types;
* every type's class has exactly the version's fields, each with the version's value type, and
  its extensible group exactly the version's inner fields;
* every class's ``update`` keywords are exactly its fields;
* a version's document has exactly the version's attribute accessors, each typed with the class
  of its object type in that version;
* ``AnyIDFDocument`` offers exactly the types every version has, each with exactly the fields
  every version has, and each field's type admits every version's values.

``generate_stubs`` runs this after writing and fails if anything is reported, so adopting an
EnergyPlus release cannot regenerate stubs that misdescribe a version. The tests run it too,
including against a version list cut short, which is what adopting the next release looks like.
"""

from __future__ import annotations

import ast
import dataclasses
import functools
from collections.abc import Iterable

Version = tuple[int, int, int]


@dataclasses.dataclass
class _Class:
    """What a generated class declares itself."""

    bases: list[str]
    fields: dict[str, str]
    properties: dict[str, str]


@dataclasses.dataclass
class _Module:
    """The classes and functional ``TypedDict`` assignments of one generated source."""

    classes: dict[str, _Class] = dataclasses.field(default_factory=dict[str, _Class])
    typed_dicts: dict[str, dict[str, str]] = dataclasses.field(default_factory=dict[str, dict[str, str]])


@functools.cache
def _norm(annotation: str) -> str:
    """Normalise an annotation's spelling, so line wrapping and the ``_g.`` prefix do not count."""
    return ast.unparse(ast.parse(annotation.replace("_g.", ""), mode="eval"))


def _read(source: str, module: _Module | None = None) -> _Module:
    module = module if module is not None else _Module()
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            cls = _Class([ast.unparse(b).replace("_g.", "") for b in node.bases], {}, {})
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    cls.fields[item.target.id] = _norm(ast.unparse(item.annotation))
                elif (
                    isinstance(item, ast.FunctionDef)
                    and item.returns is not None
                    and any(ast.unparse(d) == "property" for d in item.decorator_list)
                ):
                    cls.properties[item.name] = _norm(ast.unparse(item.returns))
            module.classes[node.name] = cls
        elif (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and ast.unparse(node.value.func) == "TypedDict"
            and len(node.value.args) == 2
            and isinstance(node.value.args[1], ast.Dict)
        ):
            name = ast.unparse(node.targets[0])
            entries: dict[str, str] = {}
            for key, value in zip(node.value.args[1].keys, node.value.args[1].values, strict=True):
                assert isinstance(key, ast.Constant)  # noqa: S101 - generated maps have string keys
                entries[str(key.value)] = _norm(ast.unparse(value))
            module.typed_dicts[name] = entries
    return module


def _linearise(module: _Module, name: str) -> list[str]:
    """*name* and the generated classes it derives from, each overriding those before it.

    Bases are taken last first, so that where two declare the same attribute the first base wins,
    as it does in Python's method resolution order.
    """
    order: list[str] = []
    for base in reversed(module.classes[name].bases):
        if base in module.classes or base in module.typed_dicts:
            for item in _linearise(module, base) if base in module.classes else [base]:
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


def _map_entries(module: _Module, name: str, problems: list[str]) -> dict[str, str]:
    """The entries of a ``TypedDict`` map, assembled from its pieces; a key filed twice is reported."""
    if name in module.typed_dicts:
        return dict(module.typed_dicts[name])
    out: dict[str, str] = {}
    for item in _linearise(module, name):
        # A piece is a functional TypedDict, or a class one when all its keys are identifiers.
        piece = module.typed_dicts.get(item) or (module.classes[item].fields if item in module.classes else {})
        for key, value in piece.items():
            if key in out and out[key] != value:
                problems.append(f"{name}: {key!r} is filed as both {out[key]} and {value}")
            out[key] = value
    return out


def _collection_class(annotation: str) -> str:
    """``IDFCollection[Zone]`` -> ``Zone``."""
    node = ast.parse(annotation, mode="eval").body
    assert isinstance(node, ast.Subscript)  # noqa: S101 - generated maps hold IDFCollection[...]
    return ast.unparse(node.slice)


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


def _expected_fields(ver: Version, obj_type: str) -> tuple[dict[str, str], tuple[str, dict[str, str]] | None]:
    """The fields of *obj_type* in *ver* as the stubs must declare them, and its group if any."""
    from idfkit.codegen.generate_stubs import _field_decls, _group_decl  # pyright: ignore[reportPrivateUsage]
    from idfkit.schema import get_schema

    schema = get_schema(ver)
    fields = {name: _norm(f"{py_type} | None") for name, py_type in _field_decls(schema, obj_type).items()}
    group = _group_decl(schema, obj_type)
    if group is None:
        return fields, None
    return fields, (group[0], {name: _norm(f"{py_type} | None") for name, py_type in group[1]})


def _check_class(module: _Module, cls: str, ver: Version, obj_type: str, problems: list[str]) -> None:
    where = f"{obj_type} in {'.'.join(map(str, ver))} ({cls})"
    if cls not in module.classes:
        problems.append(f"{where}: class not defined")
        return
    expected, group = _expected_fields(ver, obj_type)
    actual = _fields(module, cls)
    keywords = dict(expected)
    if group is not None:
        wrapper, inner = group
        annotation = actual.pop(wrapper, None)
        if annotation is None:
            problems.append(f"{where}: no {wrapper} attribute")
        else:
            group_cls = _collection_class(annotation)
            if group_cls not in module.classes or _fields(module, group_cls) != inner:
                problems.append(f"{where}: group {group_cls} does not hold the version's inner fields")
        keywords[wrapper] = "list[Any]"
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        retyped = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        problems.append(f"{where}: missing {missing}, extra {extra}, mistyped {retyped}")
    _check_update(module, cls, keywords, where, problems)


def _check_update(module: _Module, cls: str, keywords: dict[str, str], where: str, problems: list[str]) -> None:
    """The ``update`` keywords of *cls*: those of the nearest class in its line that types them.

    A class with no keyword to type keeps ``IDFObject.update``, as the latest classes always have.
    """
    if not any(k != "name" for k in keywords):
        return
    for item in reversed(_linearise(module, cls)):
        fields_cls = f"_{item}Fields"
        if fields_cls in module.classes:
            expected = {k: v for k, v in keywords.items() if k != "name"}
            if _fields(module, fields_cls) != expected:
                problems.append(f"{where}: update keywords ({fields_cls}) differ from its fields")
            return
    problems.append(f"{where}: update is not typed")


def verify(types_source: str, document_source: str, versioned_source: str, versions: tuple[Version, ...]) -> list[str]:
    """Report every way the generated stubs misdescribe a supported version; empty when none.

    Args:
        types_source: The generated ``_generated_types.pyi``.
        document_source: The generated ``document.pyi``.
        versioned_source: The generated ``versioned.pyi``.
        versions: The releases the stubs were generated to describe, oldest first; the last is the
            one ``IDFDocument`` is typed for. Passed rather than read from the generator, which may
            be running as ``__main__``, a second copy of its module.
    """
    latest = versions[-1]
    from idfkit.document import _build_resolver  # pyright: ignore[reportPrivateUsage]
    from idfkit.schema import get_schema

    module = _read(versioned_source, _read(document_source, _read(types_source)))
    problems: list[str] = []
    for ver in versions:
        tag = f"{ver[0]}_{ver[1]}"
        schema = get_schema(ver)
        if ver == latest:
            map_name, doc_name = "_ObjectTypeMap", "IDFDocument"
        else:
            map_name, doc_name = f"_ObjectTypeMapV{tag}", f"IDFDocumentV{tag}"
        if map_name not in module.classes and map_name not in module.typed_dicts:
            problems.append(f"{'.'.join(map(str, ver))}: no {map_name}")
            continue
        entries = _map_entries(module, map_name, problems)
        if set(entries) != set(schema.object_types):
            missing = sorted(set(schema.object_types) - set(entries))
            extra = sorted(set(entries) - set(schema.object_types))
            problems.append(f"{map_name}: missing types {missing}, extra types {extra}")
        classes = {obj_type: _collection_class(annotation) for obj_type, annotation in entries.items()}
        for obj_type in schema.object_types:
            if obj_type in classes:
                _check_class(module, classes[obj_type], ver, obj_type, problems)
        if doc_name not in module.classes:
            problems.append(f"{'.'.join(map(str, ver))}: no {doc_name}")
            continue
        if ver != latest:
            expected_accessors = {
                name: f"IDFCollection[{classes[obj_type]}]"
                for name, obj_type in _build_resolver(schema).accessors().items()
            }
            if _properties(module, doc_name) != expected_accessors:
                problems.append(f"{doc_name}: attribute accessors differ from the version's")
    _check_any_document(module, versions, problems)
    return problems


def _check_any_document(module: _Module, versions: tuple[Version, ...], problems: list[str]) -> None:
    from idfkit.codegen.generate_stubs import _field_decls  # pyright: ignore[reportPrivateUsage]
    from idfkit.schema import get_schema

    schemas = [get_schema(ver) for ver in versions]
    common = _intersection([set(s.object_types) for s in schemas])
    entries = _map_entries(module, "_CommonTypeMap", problems)
    if set(entries) != common:
        problems.append("AnyIDFDocument: its types are not exactly those every version has")
    for obj_type, annotation in entries.items():
        # ReadOnly[IDFCollection[X]]
        cls = _collection_class(_collection_class(annotation))
        decls = [_field_decls(s, obj_type) for s in schemas if obj_type in s.object_types]
        shared = _intersection([set(d) for d in decls])
        actual = {k: v for k, v in _fields(module, cls).items() if k not in _group_names(module, cls)}
        if set(actual) != shared:
            problems.append(f"AnyIDFDocument[{obj_type!r}] ({cls}): fields are not those every version has")
            continue
        for name in shared:
            admitted = _union_members(actual[name])
            for decl in decls:
                if not _union_members(_norm(f"{decl[name]} | None")) <= admitted:
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
