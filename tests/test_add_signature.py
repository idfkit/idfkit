"""The creation signature ``IDFCollection.add`` takes agrees with what ``add`` does at run time.

A type checker reads the parameters of ``doc["Material"].add(...)`` from the generated creation
signatures (``idfkit/_creation``): the name for a type with a Name field, the required fields with no
default, the others with their schema defaults. What a type checker reports is checked by
``tests/type_checks/add_signature_fixture.py``. These tests check that it never contradicts the run
time: every field a signature requires is one the validator refuses an object without, and the
other way round, for every object type of the latest release and of an older one; and the name and
the deprecated ``add(obj)`` form behave as before.
"""

from __future__ import annotations

import functools
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
from idfkit.objects import IDFObject
from idfkit.schema import get_schema
from idfkit.versions import LATEST_VERSION

_PACKAGE = Path(idfkit.__file__).resolve().parent
_OLDER = (9, 4, 0)


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


def _stub_required(version: tuple[int, int, int]) -> dict[str, frozenset[str]]:
    """Each object type of *version* with the fields its creation signature requires (no default)."""
    module = _stubs()
    doc_name = "IDFDocument" if version == LATEST_VERSION else f"IDFDocumentV{version[0]}_{version[1]}"
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
        return frozenset(e.field for e in error.errors if getattr(e, "code", None) == "E001" and e.field)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportUnknownArgumentType]
    except DuplicateObjectError:
        return None
    return frozenset()


@pytest.mark.parametrize("version", [LATEST_VERSION, _OLDER], ids=lambda v: ".".join(map(str, v)))
def test_every_field_a_signature_requires_is_refused_when_missing(version: tuple[int, int, int]) -> None:
    """A type error for a missing field is never a contradiction of the run time, nor the other way round."""
    disagreements: list[str] = []
    for obj_type, required in _stub_required(version).items():
        missing = _runtime_missing(version, obj_type)
        if missing is not None and missing != required:
            disagreements.append(f"{obj_type}: stub requires {sorted(required)}, run time {sorted(missing)}")
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
    # The name is positional-only: by keyword it is a field, which no type has (as before 1.3).
    with pytest.raises(ValidationFailedError, match="Unknown field 'name'"):
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
    assert isinstance(filed, IDFObject)
    assert zone in list(target)
