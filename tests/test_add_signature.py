"""The creation signature ``IDFCollection.add`` takes agrees with what ``add`` does at run time.

A type checker reads the parameters of ``doc["Material"].add(...)`` from the generated creation
signatures (``idfkit/_creation``): the name for a type with a Name field, the required fields with no
default, the others with their schema defaults. What a type checker reports is checked by
``tests/type_checks/add_signature_fixture.py``. These tests check that it never contradicts the run
time: every field a signature requires is one the validator refuses an object without, and the
other way round, for every object type of every supported release; through ``AnyIDFDocument``, no
release refuses a call for a field the signature does not require; and the name and the deprecated
``add(obj)`` form behave as before.
"""

from __future__ import annotations

import ast
import functools
import inspect
from pathlib import Path

import pytest

import idfkit
from idfkit import new_document
from idfkit.codegen.verify_stubs import (
    _collection_class,  # pyright: ignore[reportPrivateUsage]
    _creation_of,  # pyright: ignore[reportPrivateUsage]
    _getitem_entries,  # pyright: ignore[reportPrivateUsage]
    _Module,  # pyright: ignore[reportPrivateUsage]
    _read,  # pyright: ignore[reportPrivateUsage]
    _read_creation,  # pyright: ignore[reportPrivateUsage]
)
from idfkit.exceptions import DuplicateObjectError, InvalidFieldError, ValidationFailedError
from idfkit.objects import IDFCollection, IDFObject
from idfkit.schema import get_schema
from idfkit.validation import ValidationError
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION

_PACKAGE = Path(idfkit.__file__).resolve().parent
_NARROW_FIRST = "narrow_with_as_version_first"


@functools.cache
def _stubs() -> _Module:
    """The committed stubs, read as ``verify_stubs`` reads them."""
    module = _read((_PACKAGE / "_generated_types.pyi").read_text(encoding="utf-8"))
    module = _read((_PACKAGE / "document.pyi").read_text(encoding="utf-8"), module)
    module = _read((_PACKAGE / "versioned.pyi").read_text(encoding="utf-8"), module)
    for path in sorted((_PACKAGE / "_versioned").glob("v*.pyi")):
        module = _read(path.read_text(encoding="utf-8"), module)
    creation = {path.stem: path.read_text(encoding="utf-8") for path in (_PACKAGE / "_creation").glob("_*.pyi")}
    return _read_creation(creation, module)


def _stub_required(version: tuple[int, int, int] | None) -> dict[str, frozenset[str]]:
    """Each object type of *version*'s document (``AnyIDFDocument`` for ``None``) with the fields its
    creation signature requires (no default)."""
    module = _stubs()
    if version is None:
        doc_name = "IDFDocumentAllVersions"
    elif version == LATEST_VERSION:
        doc_name = "IDFDocument"
    else:
        doc_name = f"IDFDocumentV{version[0]}_{version[1]}"
    problems: list[str] = []
    out: dict[str, frozenset[str]] = {}
    for obj_type, annotation in _getitem_entries(module, doc_name, problems).items():
        found = _creation_of(module, _collection_class(annotation))
        assert found is not None, obj_type
        signature = found[1]
        assert signature is not None, obj_type
        out[obj_type] = frozenset(name for name, (_, default) in signature.params.items() if default is None)
    assert not problems
    return out


def _runtime_missing(version: tuple[int, int, int], obj_type: str) -> frozenset[str] | None:
    """The fields the validator reports missing (E001) when *obj_type* is added with none; ``None`` if it cannot tell."""
    doc = new_document(version=version)
    for existing in list(doc[obj_type]) if obj_type in doc else []:
        doc.removeidfobject(existing)
    name = "Probe" if get_schema(version).has_name(obj_type) else ""
    try:
        doc.add(obj_type, name)
    except ValidationFailedError as error:
        return frozenset(
            e.field for e in error.errors if isinstance(e, ValidationError) and e.code == "E001" and e.field
        )
    except DuplicateObjectError:
        return None
    return frozenset()


@pytest.mark.parametrize("version", ENERGYPLUS_VERSIONS, ids=lambda v: ".".join(map(str, v)))
def test_every_field_a_signature_requires_is_refused_when_missing(version: tuple[int, int, int]) -> None:
    """A type error for a missing field is never a contradiction of the run time, nor the other way round."""
    disagreements: list[str] = []
    for obj_type, required in _stub_required(version).items():
        missing = _runtime_missing(version, obj_type)
        if missing is not None and missing != required:
            disagreements.append(f"{obj_type}: stub requires {sorted(required)}, run time {sorted(missing)}")
    assert disagreements == []


def test_no_release_refuses_an_any_document_call_for_a_field_it_does_not_require() -> None:
    """Through AnyIDFDocument a field is required where any release requires it.

    So a call that type-checks is refused for a missing field by no release; where no call can
    give every release what it requires, the signature requires ``narrow_with_as_version_first``.
    """
    disagreements: list[str] = []
    for obj_type, required in _stub_required(None).items():
        if _NARROW_FIRST in required:
            continue
        for version in ENERGYPLUS_VERSIONS:
            missing = _runtime_missing(version, obj_type)
            if missing and not missing <= required:
                disagreements.append(f"{obj_type} in {version}: refuses {sorted(missing - required)}")
    assert disagreements == []


def test_a_missing_required_field_is_refused() -> None:
    doc = new_document()
    with pytest.raises(ValidationFailedError, match="roughness"):
        doc.materials.add("XPS", thickness=0.05, conductivity=0.034, density=35.0, specific_heat=1400.0)  # pyright: ignore[reportCallIssue]
    assert "XPS" not in doc.materials
    xps = doc.materials.add(
        "XPS", roughness="MediumSmooth", thickness=0.05, conductivity=0.034, density=35.0, specific_heat=1400.0
    )
    assert xps.name == "XPS"


def test_a_name_is_refused_for_a_type_without_one() -> None:
    doc = new_document()
    with pytest.raises(InvalidFieldError):
        doc["Output:SQLite"].add("Out", option_type="Simple")  # pyright: ignore[reportCallIssue]
    assert doc["Output:SQLite"].add(option_type="Simple").option_type == "Simple"


def test_the_name_is_the_only_positional_argument() -> None:
    doc = new_document()
    with pytest.raises(TypeError, match="takes 1 positional argument"):
        doc.zones.add("Office", 2)  # pyright: ignore[reportCallIssue]
    # The name is positional-only.
    with pytest.raises(TypeError, match=r"not add\(name=\.\.\.\)"):
        doc.zones.add(name="Office")  # pyright: ignore[reportCallIssue]
    assert doc.zones.add("Office").name == "Office"


def test_an_untyped_collection_takes_an_empty_name() -> None:
    doc = new_document()
    zone = doc.get_collection("Zone").add()
    assert zone.name == ""


def test_adding_an_existing_object_still_warns_and_files_it() -> None:
    doc = new_document()
    source = new_document()
    zone = source.zones.add("Office")
    target = doc.zones
    with pytest.warns(DeprecationWarning, match="deprecated"):
        filed = target.add(zone)  # pyright: ignore[reportArgumentType, reportCallIssue]
    assert filed is zone
    other = source.zones.add("Lab")
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert target.add(obj=other) is other  # pyright: ignore[reportCallIssue]
    assert isinstance(filed, IDFObject)
    assert zone in list(target)


def test_the_deprecated_form_refuses_fields_it_would_drop() -> None:
    # add(obj) files an existing object as it is; fields beside it would be silently dropped.
    doc = new_document()
    zone = new_document().zones.add("Office")
    with pytest.raises(TypeError, match="takes the object alone"):
        doc.zones.add(zone, multiplier=3)  # pyright: ignore[reportArgumentType, reportCallIssue]
    with pytest.raises(TypeError, match="takes the object alone"):
        doc.zones.add(zone, "extra")  # pyright: ignore[reportArgumentType, reportCallIssue]
    assert "Office" not in doc.zones


def _collection_add_definitions() -> tuple[ast.FunctionDef, ast.FunctionDef]:
    """``IDFCollection.add`` as type checkers read it, and as it runs: ``if TYPE_CHECKING`` / ``else``."""
    tree = ast.parse((_PACKAGE / "objects.py").read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "IDFCollection")
    for node in cls.body:
        if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
            checked = [n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "add"]
            run = [n for n in node.orelse if isinstance(n, ast.FunctionDef) and n.name == "add"]
            if checked and run:
                return checked[0], run[0]
    pytest.fail("IDFCollection.add is not declared for type checkers apart from its run-time definition")


def test_type_checkers_read_add_without_a_docstring() -> None:
    # pyright shows the creation signature's docstring (the object type's own) only when add has
    # none, so the declaration type checkers read must have none; the run-time one keeps it.
    checked, run = _collection_add_definitions()
    assert ast.get_docstring(checked) is None
    assert ast.unparse(checked.args) == ast.unparse(run.args)
    assert checked.returns is not None and run.returns is not None
    assert ast.unparse(checked.returns) == ast.unparse(run.returns)
    assert ast.get_docstring(run) == inspect.getdoc(IDFCollection.add)
    assert (IDFCollection.add.__doc__ or "").startswith("Create an object of this collection's type")
    # Every creation signature documents itself for the editor (see verify_stubs).
    assert all(signature.doc for signature in _stubs().signatures.values())
