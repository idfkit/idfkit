"""Tests for the validation module."""

from __future__ import annotations

from idfkit import IDFDocument
from idfkit.validation import (
    Severity,
    ValidationError,
    ValidationResult,
    validate_document,
)

# ---------------------------------------------------------------------------
# ValidationError
# ---------------------------------------------------------------------------


class TestValidationError:
    def test_str_with_field(self) -> None:
        err = ValidationError(
            severity=Severity.ERROR,
            obj_type="Zone",
            obj_name="Z1",
            field="x_origin",
            message="Something wrong",
            code="E001",
        )
        s = str(err)
        assert "[ERROR]" in s
        assert "Zone:'Z1'" in s
        assert ".x_origin" in s
        assert "Something wrong" in s

    def test_str_without_field(self) -> None:
        err = ValidationError(
            severity=Severity.WARNING,
            obj_type="Zone",
            obj_name="Z1",
            field=None,
            message="Warning",
            code="W001",
        )
        s = str(err)
        assert "[WARNING]" in s
        assert ".x_origin" not in s


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------


class TestValidationResult:
    def test_is_valid_no_errors(self) -> None:
        result = ValidationResult(errors=[], warnings=[], info=[])
        assert result.is_valid is True

    def test_is_valid_with_errors(self) -> None:
        err = ValidationError(Severity.ERROR, "Zone", "Z1", None, "Error", "E001")
        result = ValidationResult(errors=[err], warnings=[], info=[])
        assert result.is_valid is False

    def test_is_valid_warnings_only(self) -> None:
        warn = ValidationError(Severity.WARNING, "Zone", "Z1", None, "Warning", "W001")
        result = ValidationResult(errors=[], warnings=[warn], info=[])
        assert result.is_valid is True

    def test_total_issues(self) -> None:
        err = ValidationError(Severity.ERROR, "Zone", "Z1", None, "Error", "E001")
        warn = ValidationError(Severity.WARNING, "Zone", "Z1", None, "Warning", "W001")
        info = ValidationError(Severity.INFO, "Zone", "Z1", None, "Info", "I001")
        result = ValidationResult(errors=[err], warnings=[warn], info=[info])
        assert result.total_issues == 3

    def test_str(self) -> None:
        result = ValidationResult(errors=[], warnings=[], info=[])
        s = str(result)
        assert "0 errors" in s

    def test_bool_valid(self) -> None:
        result = ValidationResult(errors=[], warnings=[], info=[])
        assert bool(result) is True

    def test_bool_invalid(self) -> None:
        err = ValidationError(Severity.ERROR, "Zone", "Z1", None, "Error", "E001")
        result = ValidationResult(errors=[err], warnings=[], info=[])
        assert bool(result) is False


# ---------------------------------------------------------------------------
# validate_document
# ---------------------------------------------------------------------------


class TestValidateDocument:
    def test_validate_empty_doc(self, empty_doc: IDFDocument) -> None:
        result = validate_document(empty_doc)
        assert result.is_valid

    def test_validate_simple_doc(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc)
        # May have warnings but should not crash
        assert isinstance(result, ValidationResult)

    def test_validate_no_schema(self) -> None:
        doc = IDFDocument()  # No schema loaded
        result = validate_document(doc)
        # Should warn about missing schema
        assert len(result.warnings) > 0
        assert result.warnings[0].code == "W001"

    def test_validate_specific_object_types(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, object_types=["Zone"])
        assert isinstance(result, ValidationResult)

    def test_validate_check_references_disabled(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, check_references=False)
        assert isinstance(result, ValidationResult)

    def test_validate_all_checks_disabled(self, simple_doc: IDFDocument) -> None:
        result = validate_document(
            simple_doc,
            check_references=False,
            check_required=False,
            check_types=False,
            check_ranges=False,
        )
        assert isinstance(result, ValidationResult)


class TestValidateReferences:
    def test_dangling_reference_detected(self, empty_doc: IDFDocument) -> None:
        """Add a People object that references a non-existent zone."""
        empty_doc.add(
            "People",
            "TestPeople",
            {
                "zone_or_zonelist_or_space_or_spacelist_name": "NonexistentZone",
                "number_of_people_schedule_name": "NonexistentSchedule",
            },
        )
        result = validate_document(empty_doc, check_references=True)
        # Should find dangling references
        ref_errors = [e for e in result.errors if e.code == "E009"]
        assert len(ref_errors) > 0

    def test_valid_references_pass(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, check_references=True)
        # TestConstruction -> TestMaterial is valid, TestWall -> TestZone is valid
        assert isinstance(result, ValidationResult)


class TestSeverityEnum:
    def test_values(self) -> None:
        assert Severity.ERROR.value == "error"
        assert Severity.WARNING.value == "warning"
        assert Severity.INFO.value == "info"
