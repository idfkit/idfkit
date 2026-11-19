"""How an IDF file's text is read: which ``Version`` object picks the schema, and which encoding.

A ``Version`` object inside a ``!`` comment must not choose the schema, and a UTF-8 file (with or
without a byte-order mark) must read as the text it holds, and be written back in its encoding.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import pytest

from idfkit import load_idf, load_idf_with_diagnostics, new_document, save_epjson, save_idf, write_idf
from idfkit._idf_encoding import source_encoding
from idfkit.idf_parser import get_idf_version, iter_idf_objects, parse_idf
from idfkit.writers import IDFWriter

BOM = b"\xef\xbb\xbf"


class TestCommentedVersion:
    """A ``Version,x;`` in a comment is text, not the file's version."""

    BODY = "! Upgraded from Version,9.0; by hand\nVersion,24.2;\nZone,A;\nSpace,S1,A;\n"

    def test_load_reads_the_real_version(self, tmp_path: Path) -> None:
        path = tmp_path / "commented.idf"
        path.write_text(self.BODY)

        doc = load_idf(path)

        assert doc.version == (24, 2, 0)
        assert doc.schema is not None
        assert doc.schema.version == (24, 2, 0)
        assert "S1" in doc.get_collection("Space")

    def test_get_idf_version_skips_the_comment(self, tmp_path: Path) -> None:
        path = tmp_path / "commented.idf"
        path.write_text(self.BODY)

        assert get_idf_version(path) == (24, 2, 0)

    def test_trailing_comment_on_a_line(self, tmp_path: Path) -> None:
        path = tmp_path / "trailing.idf"
        path.write_text("Zone,A;  ! was Version,9.0;\nVersion,23.1;\n")

        assert get_idf_version(path) == (23, 1, 0)
        assert load_idf(path).version == (23, 1, 0)

    def test_commented_version_past_the_scan_window(self, tmp_path: Path) -> None:
        # Only a commented-out Version in the first 10 KB: the real one is further down.
        path = tmp_path / "late.idf"
        path.write_text("! Version,9.0;\n" + "! padding\n" * 2000 + "Version,24.1;\n")

        assert get_idf_version(path) == (24, 1, 0)

    def test_only_a_commented_version_is_no_version(self, tmp_path: Path) -> None:
        from idfkit.exceptions import VersionNotFoundError

        path = tmp_path / "none.idf"
        path.write_text("! Version,24.1;\nZone,A;\n")

        with pytest.raises(VersionNotFoundError):
            get_idf_version(path)
        with pytest.raises(VersionNotFoundError):
            load_idf(path)


class TestEncoding:
    """UTF-8 is detected; latin-1 stays the fallback; the document writes back what it read."""

    def test_utf8_names_read_as_written(self, tmp_path: Path) -> None:
        path = tmp_path / "utf8.idf"
        path.write_text("Version,24.1;\nZone,Büro Süd;\n", encoding="utf-8")

        doc = load_idf(path)

        assert [z.name for z in doc["Zone"]] == ["Büro Süd"]
        assert doc["Zone"]["Büro Süd"].name == "Büro Süd"

    def test_utf8_names_reach_epjson_intact(self, tmp_path: Path) -> None:
        path = tmp_path / "utf8.idf"
        path.write_text("Version,24.1;\nZone,Büro Süd;\n", encoding="utf-8")
        out = tmp_path / "out.epJSON"

        save_epjson(load_idf(path), out)

        assert "Büro Süd" in json.loads(out.read_text(encoding="utf-8"))["Zone"]

    def test_latin1_still_reads_as_latin1(self, tmp_path: Path) -> None:
        path = tmp_path / "latin1.idf"
        path.write_bytes("Version,24.1;\nZone,Büro;\n".encode("latin-1"))

        doc = load_idf(path)

        assert [z.name for z in doc["Zone"]] == ["Büro"]
        out = tmp_path / "out.idf"
        save_idf(doc, out)
        assert "Büro".encode("latin-1") in out.read_bytes()

    def test_explicit_encoding_wins(self, tmp_path: Path) -> None:
        path = tmp_path / "utf8.idf"
        path.write_text("Version,24.1;\nZone,Büro;\n", encoding="utf-8")

        doc = load_idf(path, encoding="latin-1")

        assert [z.name for z in doc["Zone"]] == ["BÃ¼ro"]

    def test_load_idf_with_diagnostics_takes_encoding(self, tmp_path: Path) -> None:
        path = tmp_path / "utf8.idf"
        path.write_text("Version,24.1;\nZone,Büro;\n", encoding="utf-8")

        assert [z.name for z in load_idf_with_diagnostics(path).document["Zone"]] == ["Büro"]
        assert [z.name for z in load_idf_with_diagnostics(path, encoding="latin-1").document["Zone"]] == ["BÃ¼ro"]

    def test_bom_is_dropped(self, tmp_path: Path) -> None:
        path = tmp_path / "bom.idf"
        path.write_bytes(BOM + "Version,24.1;\nZone,Büro;\n".encode())

        doc = load_idf(path, preserve_formatting=True)

        assert [z.name for z in doc["Zone"]] == ["Büro"]
        assert write_idf(doc).startswith("Version")
        assert get_idf_version(path) == (24, 1, 0)

    def test_bom_with_explicit_utf8(self, tmp_path: Path) -> None:
        path = tmp_path / "bom.idf"
        path.write_bytes(BOM + b"Version,24.1;\nZone,A;\n")

        doc = load_idf(path, encoding="utf-8", preserve_formatting=True)

        assert write_idf(doc).startswith("Version")

    @pytest.mark.parametrize(
        "raw",
        [
            "Version,24.1;\nZone,Büro;\n".encode(),
            BOM + "Version,24.1;\nZone,Büro;\n".encode(),
            "Version,24.1;\nZone,Büro;\n".encode("latin-1"),
            "Version,24.1;\nZone,办公室;\n".encode(),
        ],
        ids=["utf8", "utf8-bom", "latin1", "utf8-cjk"],
    )
    def test_lossless_round_trip_is_byte_identical(self, tmp_path: Path, raw: bytes) -> None:
        path = tmp_path / "in.idf"
        path.write_bytes(raw)
        out = tmp_path / "out.idf"

        save_idf(load_idf(path, preserve_formatting=True), out)

        assert out.read_bytes() == raw

    def test_save_writes_the_source_encoding(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_text("Version,24.1;\nZone,办公室;\n", encoding="utf-8")
        out = tmp_path / "out.idf"

        doc = load_idf(path)
        doc.add("Zone", "Küche")
        save_idf(doc, out)

        text = out.read_text(encoding="utf-8")
        assert "办公室" in text
        assert "Küche" in text

    def test_copy_and_pickle_keep_the_source_encoding(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_text("Version,24.1;\nZone,办公室;\n", encoding="utf-8")
        doc = load_idf(path)

        for twin in (doc.copy(), pickle.loads(pickle.dumps(doc))):  # noqa: S301
            out = tmp_path / "twin.idf"
            save_idf(twin, out)
            assert "办公室" in out.read_text(encoding="utf-8")

    def test_explicit_save_encoding_wins(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_text("Version,24.1;\nZone,Büro;\n", encoding="utf-8")
        out = tmp_path / "out.idf"

        save_idf(load_idf(path), out, encoding="latin-1")

        assert "Büro".encode("latin-1") in out.read_bytes()

    def test_idf_writer_writes_the_source_encoding(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_text("Version,24.1;\nZone,办公室;\n", encoding="utf-8")
        out = tmp_path / "out.idf"

        IDFWriter(load_idf(path)).write_to_file(out)

        assert "办公室" in out.read_text(encoding="utf-8")

    def test_idf_writer_never_writes_a_bom(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_bytes(BOM + "Version,24.1;\nZone,Büro;\n".encode())
        out = tmp_path / "out.idf"

        IDFWriter(load_idf(path, preserve_formatting=True)).write_to_file(out)

        assert not out.read_bytes().startswith(BOM)
        assert "Büro" in out.read_text(encoding="utf-8")

    def test_regenerated_output_drops_the_bom(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_bytes(BOM + "Version,24.1;\nZone,Büro;\n".encode())
        plain = tmp_path / "plain.idf"
        lossless = tmp_path / "lossless.idf"

        save_idf(load_idf(path), plain)
        save_idf(load_idf(path, preserve_formatting=True), lossless)

        assert not plain.read_bytes().startswith(BOM)
        assert "Büro" in plain.read_text(encoding="utf-8")
        assert lossless.read_bytes().startswith(BOM)

    def test_engine_input_never_has_a_bom(self, tmp_path: Path) -> None:
        path = tmp_path / "in.idf"
        path.write_bytes(BOM + "Version,24.1;\nZone,Büro;\n".encode())
        doc = load_idf(path, preserve_formatting=True)

        assert source_encoding(doc, bom=False) == "utf-8"
        assert source_encoding(doc, bom=True) == "utf-8-sig"
        assert source_encoding(new_document(), bom=False) == "latin-1"

    @pytest.mark.parametrize("requested", ["utf-8", "utf-8-sig", "UTF8"])
    def test_requested_utf8_adds_no_bom(self, tmp_path: Path, requested: str) -> None:
        raw = "Version,24.1;\nZone,Büro;\n".encode()
        path = tmp_path / "in.idf"
        path.write_bytes(raw)
        out = tmp_path / "out.idf"

        save_idf(load_idf(path, encoding=requested, preserve_formatting=True), out)

        assert out.read_bytes() == raw

    def test_parse_idf_and_iter_idf_objects_detect_too(self, tmp_path: Path) -> None:
        path = tmp_path / "utf8.idf"
        path.write_bytes(BOM + "Version,24.1;\nZone,Büro;\n".encode())

        assert [z.name for z in parse_idf(path)["Zone"]] == ["Büro"]
        assert [(t, n) for t, n, _ in iter_idf_objects(path)] == [("Version", "24.1"), ("Zone", "Büro")]


def test_comment_inside_the_version_object(tmp_path: Path) -> None:
    path = tmp_path / "split.idf"
    path.write_text("Version,  !- Version Identifier\n  24.1;\nZone,A;\n")

    assert get_idf_version(path) == (24, 1, 0)
    assert load_idf(path).version == (24, 1, 0)
