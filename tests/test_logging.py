"""Tests for logging integration across idfkit modules."""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Generator
from pathlib import Path

import pytest

import idfkit
from idfkit import new_document, validate_document, write_idf


class TestNullHandler:
    """The library root logger must have a NullHandler by default."""

    def test_null_handler_attached(self) -> None:
        root_logger = logging.getLogger("idfkit")
        handler_types = [type(h) for h in root_logger.handlers]
        assert logging.NullHandler in handler_types

    def test_no_output_by_default(self, capfd: pytest.CaptureFixture[str]) -> None:
        """Without user configuration, idfkit should produce no output."""
        doc = new_document()
        doc.add("Zone", "SilentZone")
        captured = capfd.readouterr()
        assert captured.out == ""
        assert captured.err == ""


class TestParserLogging:
    """IDF and epJSON parsers emit log records."""

    def test_idf_parse_logs(self, idf_file: Path) -> None:
        with _capture_logs("idfkit.idf_parser") as records:
            idfkit.load_idf(idf_file)
        messages = [r.message for r in records]
        # Should contain an INFO message about parse completion
        assert any("Parsed" in m and "objects" in m for m in messages)

    def test_epjson_parse_logs(self, epjson_file: Path) -> None:
        with _capture_logs("idfkit.epjson_parser") as records:
            idfkit.load_epjson(epjson_file)
        messages = [r.message for r in records]
        assert any("Parsed" in m and "objects" in m for m in messages)


class TestSchemaLogging:
    """Schema loading emits cache-related log records."""

    def test_schema_load_logs(self) -> None:
        # Clear the schema cache to force a fresh load
        from idfkit.schema import SchemaManager

        mgr = SchemaManager()

        with _capture_logs("idfkit.schema") as records:
            mgr.get_schema((24, 1, 0))
        messages = [r.message for r in records]
        assert any("Loaded schema" in m for m in messages)


class TestDocumentLogging:
    """Document mutations emit DEBUG log records."""

    def test_add_logs(self) -> None:
        doc = new_document()
        with _capture_logs("idfkit.document", level=logging.DEBUG) as records:
            doc.add("Zone", "LogZone")
        messages = [r.message for r in records]
        assert any("Added" in m and "LogZone" in m for m in messages)

    def test_remove_logs(self) -> None:
        doc = new_document()
        zone = doc.add("Zone", "RemoveMe")
        with _capture_logs("idfkit.document", level=logging.DEBUG) as records:
            doc.removeidfobject(zone)
        messages = [r.message for r in records]
        assert any("Removed" in m and "RemoveMe" in m for m in messages)

    def test_rename_logs(self, simple_doc: idfkit.IDFDocument) -> None:
        with _capture_logs("idfkit.document", level=logging.DEBUG) as records:
            simple_doc.rename("Zone", "TestZone", "RenamedZone")
        messages = [r.message for r in records]
        assert any("Renamed" in m and "RenamedZone" in m for m in messages)


class TestValidationLogging:
    """Validation emits summary log records."""

    def test_validate_logs(self) -> None:
        doc = new_document()
        doc.add("Zone", "ValidZone")
        with _capture_logs("idfkit.validation") as records:
            validate_document(doc)
        messages = [r.message for r in records]
        assert any("Validation complete" in m for m in messages)


class TestWriterLogging:
    """Writers emit log records."""

    def test_write_idf_to_string_logs(self) -> None:
        doc = new_document()
        doc.add("Zone", "WriterZone")
        with _capture_logs("idfkit.writers", level=logging.DEBUG) as records:
            write_idf(doc)
        messages = [r.message for r in records]
        assert any("Serialized IDF" in m for m in messages)

    def test_write_idf_to_file_logs(self, tmp_path: Path) -> None:
        doc = new_document()
        doc.add("Zone", "WriterZone")
        out = tmp_path / "out.idf"
        with _capture_logs("idfkit.writers") as records:
            write_idf(doc, out)
        messages = [r.message for r in records]
        assert any("Wrote IDF" in m for m in messages)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def _capture_logs(
    logger_name: str,
    level: int = logging.DEBUG,
) -> Generator[list[logging.LogRecord], None, None]:
    """Context manager that captures log records from a named logger."""
    records: list[logging.LogRecord] = []
    handler = logging.Handler()
    handler.emit = lambda record: records.append(record)  # type: ignore[assignment]
    handler.setLevel(level)
    target_logger = logging.getLogger(logger_name)
    target_logger.setLevel(level)
    target_logger.addHandler(handler)
    try:
        yield records
    finally:
        target_logger.removeHandler(handler)
        target_logger.setLevel(logging.WARNING)
