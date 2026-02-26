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
        # Using validate=False since we're testing document-level reference validation,
        # not add-time validation
        empty_doc.add(
            "People",
            "TestPeople",
            {
                "zone_or_zonelist_or_space_or_spacelist_name": "NonexistentZone",
                "number_of_people_schedule_name": "NonexistentSchedule",
            },
            validate=False,
        )
        result = validate_document(empty_doc, check_references=True)
        # Should find dangling references
        ref_errors = [e for e in result.errors if e.code == "E009"]
        assert len(ref_errors) > 0

    def test_valid_references_pass(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, check_references=True)
        # TestConstruction -> TestMaterial is valid, TestWall -> TestZone is valid
        assert isinstance(result, ValidationResult)


class TestValidateSingletons:
    """Tests for maxProperties (singleton) constraint checking in validate_document."""

    def _force_duplicate_singleton(self, doc: IDFDocument, obj_type: str) -> None:
        """Bypass add() singleton guard by inserting directly into the collection."""
        from idfkit.objects import IDFCollection, IDFObject

        key = obj_type.upper()
        if key not in {k.upper(): k for k in doc.collections}:
            collection = IDFCollection(obj_type)
            doc._collections[obj_type] = collection  # pyright: ignore[reportPrivateUsage]
        collection = doc[obj_type]
        obj = IDFObject(obj_type, "")
        collection._items.append(obj)  # pyright: ignore[reportPrivateUsage]

    def test_singleton_violation_detected(self, empty_doc: IDFDocument) -> None:
        """A singleton type with >1 instance should produce an E010 error."""
        empty_doc.add("Timestep", number_of_timesteps_per_hour=4)
        self._force_duplicate_singleton(empty_doc, "Timestep")

        result = validate_document(empty_doc)
        singleton_errors = [e for e in result.errors if e.code == "E010"]
        assert len(singleton_errors) == 1
        assert "Timestep" in singleton_errors[0].message
        assert "2 instances" in singleton_errors[0].message

    def test_singleton_valid_passes(self, empty_doc: IDFDocument) -> None:
        """A singleton type with exactly 1 instance should pass."""
        empty_doc.add("Timestep", number_of_timesteps_per_hour=4)
        result = validate_document(empty_doc)
        singleton_errors = [e for e in result.errors if e.code == "E010"]
        assert len(singleton_errors) == 0

    def test_singleton_check_disabled(self, empty_doc: IDFDocument) -> None:
        """check_singletons=False should skip singleton validation."""
        empty_doc.add("Timestep", number_of_timesteps_per_hour=4)
        self._force_duplicate_singleton(empty_doc, "Timestep")

        result = validate_document(empty_doc, check_singletons=False)
        singleton_errors = [e for e in result.errors if e.code == "E010"]
        assert len(singleton_errors) == 0

    def test_singleton_check_respects_object_types_filter(self, empty_doc: IDFDocument) -> None:
        """Singleton check should only apply to filtered object types."""
        empty_doc.add("Timestep", number_of_timesteps_per_hour=4)
        self._force_duplicate_singleton(empty_doc, "Timestep")

        # Filter to Zone only — Timestep singleton violation should not appear
        result = validate_document(empty_doc, object_types=["Zone"])
        singleton_errors = [e for e in result.errors if e.code == "E010"]
        assert len(singleton_errors) == 0


class TestSeverityEnum:
    def test_values(self) -> None:
        assert Severity.ERROR.value == "error"
        assert Severity.WARNING.value == "warning"
        assert Severity.INFO.value == "info"
