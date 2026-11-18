"""The loaders' release targets: ``as_type=``, ``since=`` and ``before=``.

``load_idf``, ``load_epjson`` and ``load_idf_with_diagnostics`` check them as ``as_version`` does, once
the file is read; a malformed target is refused before it is. What a type checker reports for them
is checked by ``tests/type_checks/loaders_fixture.py``.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, get_origin

import pytest

import idfkit.versioned as versioned
from idfkit import load_epjson, load_idf, load_idf_with_diagnostics, new_document, save_epjson, save_idf
from idfkit.codegen import generate_stubs as gen
from idfkit.document import AnyIDFDocument, IDFDocument
from idfkit.idf_parser import ParseResult
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string

_V94 = (9, 4, 0)
_PACKAGE = Path(gen.__file__).resolve().parent.parent

_Loader = Callable[..., AnyIDFDocument]


def _load_idf(path: Path, *args: Any, **kwargs: Any) -> AnyIDFDocument:
    return load_idf(path, *args, **kwargs)


def _load_epjson(path: Path, *args: Any, **kwargs: Any) -> AnyIDFDocument:
    return load_epjson(path, *args, **kwargs)


def _load_with_diagnostics(path: Path, *args: Any, **kwargs: Any) -> AnyIDFDocument:
    result = load_idf_with_diagnostics(path, *args, **kwargs)
    assert isinstance(result, ParseResult)
    return result.document


_LOADERS: dict[str, tuple[_Loader, str]] = {
    "load_idf": (_load_idf, "idf"),
    "load_epjson": (_load_epjson, "epJSON"),
    "load_idf_with_diagnostics": (_load_with_diagnostics, "idf"),
}


@pytest.fixture(params=list(_LOADERS))
def loader(request: pytest.FixtureRequest) -> tuple[_Loader, str]:
    return _LOADERS[request.param]


def _model(tmp_path: Path, suffix: str, version: tuple[int, int, int] = _V94) -> Path:
    """A file of *version*, in the format *suffix* names."""
    doc = new_document(version=version)
    doc.add("Zone", "Office")
    path = tmp_path / f"model_{version_string(version)}.{suffix}"
    if suffix == "idf":
        save_idf(doc, path)
    else:
        save_epjson(doc, path)
    return path


class TestNoTarget:
    def test_loads_a_model_of_any_release(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        doc = load(_model(tmp_path, suffix))
        assert doc.version == _V94
        assert isinstance(doc, IDFDocument)


class TestAsType:
    def test_accepts_a_model_of_the_release(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        doc = load(_model(tmp_path, suffix), as_type=versioned.IDFDocumentV9_4)
        assert doc.version == _V94
        assert isinstance(doc, versioned.IDFDocumentV9_4)

    def test_refuses_a_model_of_another_release_naming_the_file(
        self, tmp_path: Path, loader: tuple[_Loader, str]
    ) -> None:
        load, suffix = loader
        path = _model(tmp_path, suffix)
        message = rf"^{re.escape(str(path))}: The document is EnergyPlus 9\.4\.0, not 26\.1\.0.*IDFDocumentV26_1$"
        with pytest.raises(TypeError, match=message):
            load(path, as_type=versioned.IDFDocumentV26_1)

    def test_idfdocument_means_the_latest_release(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        assert load(_model(tmp_path, suffix, LATEST_VERSION), as_type=IDFDocument).version == LATEST_VERSION
        with pytest.raises(TypeError, match=rf"not {re.escape(version_string(LATEST_VERSION))}"):
            load(_model(tmp_path, suffix), as_type=IDFDocument)

    def test_accepts_a_tuple_of_releases(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        doc = load(_model(tmp_path, suffix), as_type=(versioned.IDFDocumentV9_4, versioned.IDFDocumentV26_1))
        assert doc.version == _V94
        with pytest.raises(TypeError, match=r"not one of 9\.6\.0, 26\.1\.0"):
            load(_model(tmp_path, suffix), as_type=(versioned.IDFDocumentV9_6, versioned.IDFDocumentV26_1))

    def test_the_type_argument_does_not_change_strictness(self, tmp_path: Path) -> None:
        path = _model(tmp_path, "idf")
        assert load_idf(path, as_type=versioned.IDFDocumentV9_4[Literal[False]], strict=False).strict is False
        assert load_idf(path, as_type=versioned.IDFDocumentV9_4).strict is True

    def test_is_checked_against_the_version_override(self, tmp_path: Path) -> None:
        # A file with no Version object is read as the release the override names.
        path = tmp_path / "unversioned.idf"
        path.write_text("Zone,Office;\n", encoding="latin-1")
        assert load_idf(path, (9, 6, 0), as_type=versioned.IDFDocumentV9_6).version == (9, 6, 0)
        with pytest.raises(TypeError, match=r"EnergyPlus 9\.6\.0, not 9\.4\.0"):
            load_idf(path, (9, 6, 0), as_type=versioned.IDFDocumentV9_4)

    def test_any_idf_document_accepts_every_release(self, tmp_path: Path) -> None:
        assert load_idf(_model(tmp_path, "idf"), as_type=AnyIDFDocument).version == _V94


class TestRange:
    def test_since(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        path = _model(tmp_path, suffix)
        assert load(path, since="9.4").version == _V94
        assert load(path, since=versioned.IDFDocumentV9_0).version == _V94
        with pytest.raises(TypeError, match=r"not 9\.6\.0 or later"):
            load(path, since="9.6")

    def test_before(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        path = _model(tmp_path, suffix)
        assert load(path, before=(9, 6, 0)).version == _V94
        with pytest.raises(TypeError, match=re.escape(f"{path}: The document is EnergyPlus 9.4.0, not a release")):
            load(path, before="9.4")

    def test_since_and_before(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, suffix = loader
        path = _model(tmp_path, suffix)
        assert load(path, since="9.3", before="9.5").version == _V94
        with pytest.raises(TypeError, match=r"from 9\.5\.0 to before 22\.1\.0 \(9\.5\.0, 9\.6\.0\)"):
            load(path, since="9.5", before="22.1")


class TestRefusedBeforeReading:
    """A target no document could meet is refused before the file is read: the path need not exist."""

    def test_a_type_and_a_range_together(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(TypeError, match=r"as_type= or since=/before=, not both"):
            load(tmp_path / "missing", as_type=versioned.IDFDocumentV9_4, since="9.4")

    def test_a_type_that_is_not_a_document_type(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(TypeError, match="is not a document type"):
            load(tmp_path / "missing", as_type=int)

    def test_an_empty_tuple(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(TypeError, match="at least one document type"):
            load(tmp_path / "missing", as_type=())

    def test_a_release_idfkit_does_not_support(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(ValueError, match="supports no such EnergyPlus release"):
            load(tmp_path / "missing", since="27.1")

    def test_a_bound_that_is_not_a_release(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(ValueError, match="is not a release"):
            load(tmp_path / "missing", before="latest")

    def test_an_empty_range(self, tmp_path: Path, loader: tuple[_Loader, str]) -> None:
        load, _ = loader
        with pytest.raises(ValueError, match=r"No supported EnergyPlus release is from 9\.6\.0 to before 9\.4\.0"):
            load(tmp_path / "missing", since="9.6", before="9.4")


class TestDiagnostics:
    def test_a_narrowed_result_keeps_its_findings(self, tmp_path: Path) -> None:
        path = tmp_path / "hand_edited.idf"
        path.write_text("Version,9.4;\nNotAnObjectType,X;\nZone,Office;\n", encoding="latin-1")
        result = load_idf_with_diagnostics(path, as_type=versioned.IDFDocumentV9_4)
        assert len(result.document["Zone"]) == 1
        assert result.diagnostics

    def test_parse_result_takes_a_type_argument(self) -> None:
        # The stub declares it generic, so an annotation evaluated at run time must not raise.
        assert get_origin(ParseResult[IDFDocument]) is ParseResult


class TestStub:
    def test_names_a_range_from_and_before_every_release(self) -> None:
        stub = (_PACKAGE / "_loaders.pyi").read_text(encoding="utf-8")
        for name in ("load_idf", "load_epjson", "load_idf_with_diagnostics"):
            assert f"def {name}(" in stub
        for ver in ENERGYPLUS_VERSIONS:
            tag = f"{ver[0]}_{ver[1]}"
            assert f"-> IDFDocumentSince{tag}" in stub
            if ver != ENERGYPLUS_VERSIONS[0]:
                assert f"-> IDFDocumentBefore{tag}" in stub

    def test_carries_the_run_time_docstrings(self) -> None:
        stub = (_PACKAGE / "_loaders.pyi").read_text(encoding="utf-8")
        assert '"""Load an IDF file and return its document.' in stub
        assert '"""Load an IDF file, keeping the findings that did not stop the parse.' in stub
        assert '"""Load an epJSON file and return its document.' in stub

    def test_refuses_a_loader_without_a_docstring(self) -> None:
        with pytest.raises(ValueError, match="no docstring for load_epjson"):
            gen.generate_loaders_pyi({"load_idf": "x", "load_idf_with_diagnostics": "y"})
