"""A file of the other format, or a swapped argument, names the function to use instead."""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any, cast

import pytest

from idfkit import IDFDocument, load_epjson, load_idf, new_document, save_epjson, save_idf
from idfkit.exceptions import FileFormatError, IDFParseError


@pytest.fixture
def doc() -> IDFDocument:
    return new_document(version=(24, 1, 0))


class TestLoadWrongFormat:
    def test_load_idf_on_epjson_names_load_epjson(self, doc: IDFDocument, tmp_path: Path) -> None:
        path = tmp_path / "model.epJSON"
        save_epjson(doc, path)
        with pytest.raises(FileFormatError, match=r"looks like an epJSON file.*use load_epjson\(\)") as info:
            load_idf(path)
        assert info.value.detected_format == "epjson"
        assert info.value.filepath == str(path)

    def test_content_decides_not_the_suffix(self, doc: IDFDocument, tmp_path: Path) -> None:
        """epJSON content under an .idf name is still refused, and with version= given."""
        path = tmp_path / "model.idf"
        path.write_text("﻿\n  " + json.dumps({"Version": {"Version 1": {"version_identifier": "24.1"}}}))
        with pytest.raises(FileFormatError, match="use load_epjson"):
            load_idf(path, version=(24, 1, 0))

    def test_load_epjson_on_idf_names_load_idf(self, doc: IDFDocument, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        save_idf(doc, path)
        with pytest.raises(FileFormatError, match=r"looks like an IDF file.*use load_idf\(\)") as info:
            load_epjson(path)
        assert info.value.detected_format == "idf"
        assert isinstance(info.value.__cause__, json.JSONDecodeError)

    def test_load_epjson_on_latin1_idf_names_load_idf(self, doc: IDFDocument, tmp_path: Path) -> None:
        """A non-ASCII IDF (save_idf writes latin-1) is not UTF-8; it is still recognised as IDF."""
        doc.add("Zone", "Caf\u00e9")
        path = tmp_path / "cafe.idf"
        save_idf(doc, path)
        with pytest.raises(FileFormatError, match=r"use load_idf\(\)") as info:
            load_epjson(path)
        assert isinstance(info.value.__cause__, UnicodeDecodeError)

    def test_non_utf8_json_still_raises_decode_error(self, tmp_path: Path) -> None:
        path = tmp_path / "broken.epJSON"
        path.write_bytes(b'{"Zone": {"Caf\xe9": {}}}')
        with pytest.raises(UnicodeDecodeError):
            load_epjson(path)

    def test_format_error_survives_pickling(self) -> None:
        err = pickle.loads(pickle.dumps(FileFormatError("in.idf", "idf")))  # noqa: S301
        assert isinstance(err, FileFormatError)
        assert (err.filepath, err.detected_format) == ("in.idf", "idf")
        assert str(err) == str(FileFormatError("in.idf", "idf"))

    def test_format_error_is_a_parse_error_and_a_value_error(self) -> None:
        """Code that caught json.JSONDecodeError (a ValueError) or IDFParseError still catches it."""
        err = FileFormatError("in.idf", "idf")
        assert isinstance(err, IDFParseError)
        assert isinstance(err, ValueError)

    def test_malformed_json_still_raises_json_error(self, tmp_path: Path) -> None:
        path = tmp_path / "broken.epJSON"
        path.write_text('{"Version": ')
        with pytest.raises(json.JSONDecodeError):
            load_epjson(path)

    def test_matching_formats_still_load(self, doc: IDFDocument, tmp_path: Path) -> None:
        save_idf(doc, tmp_path / "a.idf")
        save_epjson(doc, tmp_path / "a.epJSON")
        assert load_idf(tmp_path / "a.idf").version == (24, 1, 0)
        assert load_epjson(tmp_path / "a.epJSON").version == (24, 1, 0)


class TestSaveWrongSuffix:
    @pytest.mark.parametrize("name", ["out.epJSON", "out.epjson", "out.json"])
    def test_save_idf_refuses_an_epjson_suffix(self, doc: IDFDocument, tmp_path: Path, name: str) -> None:
        path = tmp_path / name
        with pytest.raises(ValueError, match=r"save_idf\(\) writes IDF text.*use save_epjson\("):
            save_idf(doc, path)
        assert not path.exists()

    @pytest.mark.parametrize("name", ["out.idf", "out.IDF", "out.imf"])
    def test_save_epjson_refuses_an_idf_suffix(self, doc: IDFDocument, tmp_path: Path, name: str) -> None:
        path = tmp_path / name
        with pytest.raises(ValueError, match=r"save_epjson\(\) writes epJSON text.*use save_idf\("):
            save_epjson(doc, path)
        assert not path.exists()

    def test_other_suffixes_are_written(self, doc: IDFDocument, tmp_path: Path) -> None:
        save_idf(doc, tmp_path / "out.txt")
        save_epjson(doc, tmp_path / "out.txt.bak")
        assert (tmp_path / "out.txt").read_text(encoding="latin-1").lstrip().startswith("!")

    def test_document_save_of_an_epjson_model_does_not_write_idf_into_it(
        self, doc: IDFDocument, tmp_path: Path
    ) -> None:
        """doc.save() writes IDF; on a model loaded from epJSON it used to overwrite the .epJSON with IDF text."""
        path = tmp_path / "model.epJSON"
        save_epjson(doc, path)
        before = path.read_text(encoding="utf-8")
        loaded = load_epjson(path)
        with pytest.raises(ValueError, match="use save_epjson"):
            loaded.save()
        assert path.read_text(encoding="utf-8") == before


class TestSaveSwappedArguments:
    @pytest.mark.parametrize("path", ["o.idf", Path("o.idf")])
    def test_save_idf_with_path_first(self, doc: IDFDocument, path: str | Path) -> None:
        with pytest.raises(TypeError, match=r"save_idf\(doc, \.\.\.\): first argument must be a document.*path second"):
            save_idf(cast(Any, path), doc)

    def test_save_epjson_with_path_first(self, doc: IDFDocument) -> None:
        with pytest.raises(TypeError, match=r"save_epjson\(doc, \.\.\.\): first argument must be a document"):
            save_epjson(cast(Any, "o.epJSON"), doc)

    def test_non_path_non_document(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError, match="got dict") as info:
            save_idf(cast(Any, {}), tmp_path / "o.idf")
        assert "path second" not in str(info.value)
