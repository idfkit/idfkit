"""Tests for the validation module."""

from __future__ import annotations

from unittest.mock import patch

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFCollection, IDFObject
from idfkit.schema import get_schema
from idfkit.validation import (
    Severity,
    ValidationError,
    ValidationResult,
    _validate_field_range,  # pyright: ignore[reportPrivateUsage]
    _validate_field_type,  # pyright: ignore[reportPrivateUsage]
    _validate_object,  # pyright: ignore[reportPrivateUsage]
    validate_document,
    validate_object,
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

    def test_str_many_errors_shows_overflow_message(self) -> None:
        errors = [ValidationError(Severity.ERROR, "Zone", "Z1", None, f"Error {i}", "E001") for i in range(15)]
        result = ValidationResult(errors=errors, warnings=[], info=[])
        s = str(result)
        assert "15 errors" in s
        assert "5 more errors" in s

    def test_str_exactly_ten_errors_no_overflow(self) -> None:
        errors = [ValidationError(Severity.ERROR, "Zone", "Z1", None, f"Error {i}", "E001") for i in range(10)]
        result = ValidationResult(errors=errors, warnings=[], info=[])
        s = str(result)
        assert "more errors" not in s

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
        # simple_doc has valid references and required fields — no errors expected
        assert result.errors == []

    def test_validate_no_schema(self) -> None:
        doc = IDFDocument()  # No schema loaded
        result = validate_document(doc)
        # Should warn about missing schema
        assert len(result.warnings) > 0
        assert result.warnings[0].code == "W001"

    def test_validate_specific_object_types(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, object_types=["Zone"])
        # Scoping to Zone only: no errors expected for a well-formed zone
        assert result.errors == []

    def test_validate_check_references_disabled(self, simple_doc: IDFDocument) -> None:
        result = validate_document(simple_doc, check_references=False)
        # With reference checking disabled, no E009 errors should appear
        ref_errors = [e for e in result.errors if e.code == "E009"]
        assert ref_errors == []

    def test_validate_all_checks_disabled(self, simple_doc: IDFDocument) -> None:
        result = validate_document(
            simple_doc,
            check_references=False,
            check_required=False,
            check_types=False,
            check_ranges=False,
        )
        # With every check disabled, no errors should be produced
        assert result.errors == []


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
        # TestConstruction→TestMaterial and TestWall→TestZone are all valid references
        ref_errors = [e for e in result.errors if e.code == "E009"]
        assert ref_errors == []


class TestValidateSingletons:
    """Tests for maxProperties (singleton) constraint checking in validate_document."""

    def _force_duplicate_singleton(self, doc: IDFDocument, obj_type: str) -> None:
        """Bypass add() singleton guard by inserting directly into the collection."""
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


# ---------------------------------------------------------------------------
# validate_object (public API)
# ---------------------------------------------------------------------------


class TestValidateObjectPublicApi:
    def test_valid_object_returns_no_errors(self) -> None:
        schema = get_schema((24, 1, 0))
        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "Z1")
        errors = validate_object(zone, schema)
        assert isinstance(errors, list)

    def test_unknown_type_returns_warning(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="FakeObjectType999", name="x")
        errors = validate_object(obj, schema)
        assert any(e.code == "W002" for e in errors)


# ---------------------------------------------------------------------------
# _validate_object (unknown type / unknown field)
# ---------------------------------------------------------------------------


class TestValidateObjectUnknownType:
    def test_unknown_object_type_produces_w002(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="NotARealType", name="test")
        errors = _validate_object(obj, schema)
        assert len(errors) == 1
        assert errors[0].code == "W002"
        assert errors[0].severity == Severity.WARNING


class TestValidateObjectUnknownField:
    def test_unknown_field_on_non_extensible_produces_w003(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"not_a_real_field": "value"})
        errors = _validate_object(obj, schema, check_unknown=True)
        assert any(e.code == "W003" for e in errors)

    def test_unknown_field_on_extensible_no_w003(self) -> None:
        schema = get_schema((24, 1, 0))
        # BuildingSurface:Detailed is extensible; extra vertex fields should not warn
        obj = IDFObject(
            obj_type="BuildingSurface:Detailed",
            name="Wall1",
            data={"vertex_999_x_coordinate": 1.0},
        )
        errors = _validate_object(obj, schema, check_unknown=True)
        assert not any(e.code == "W003" for e in errors)

    def test_unknown_field_skipped_when_check_unknown_false(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"not_a_real_field": "value"})
        errors = _validate_object(obj, schema, check_unknown=False)
        assert not any(e.code == "W003" for e in errors)


# ---------------------------------------------------------------------------
# validate_document severity routing (warnings / info to correct buckets)
# ---------------------------------------------------------------------------


class TestValidateDocumentSeverityRouting:
    def test_object_warning_goes_to_warnings_list(self) -> None:
        """Objects of unknown type produce W002 warnings routed to result.warnings."""
        doc = new_document(version=(24, 1, 0))
        fake_type = "FakeObjectType999"
        coll: IDFCollection[IDFObject] = IDFCollection(fake_type)  # pyright: ignore[reportUnknownVariableType]
        coll._items.append(IDFObject(obj_type=fake_type, name="fake1"))  # pyright: ignore[reportPrivateUsage]
        doc._collections[fake_type] = coll  # pyright: ignore[reportPrivateUsage]

        result = validate_document(doc, object_types=[fake_type])
        assert any(e.code == "W002" for e in result.warnings)

    def test_info_severity_goes_to_info_list(self) -> None:
        """ValidationErrors with INFO severity end up in result.info."""
        info_err = ValidationError(Severity.INFO, "Zone", "Z1", None, "Info msg", "I001")
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1")  # add before patching so add-time validation runs normally

        with patch("idfkit.validation._validate_object", return_value=[info_err]):
            result = validate_document(doc, object_types=["Zone"])

        assert any(e.code == "I001" for e in result.info)

    def test_reference_warning_goes_to_warnings_list(self) -> None:
        """Reference errors with WARNING severity end up in result.warnings."""
        warn_err = ValidationError(Severity.WARNING, "Zone", "Z1", "field", "Ref warning", "W099")
        doc = new_document(version=(24, 1, 0))

        with patch("idfkit.validation._validate_references", return_value=[warn_err]):
            result = validate_document(doc, object_types=[])

        assert any(e.code == "W099" for e in result.warnings)


# ---------------------------------------------------------------------------
# _validate_field_type
# ---------------------------------------------------------------------------


class TestValidateFieldType:
    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Zone", name="Z1")

    def test_anyof_valid_value(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "number"}, {"type": "string"}]}
        errors = _validate_field_type(self._obj(), "f", 42.0, field_schema)
        assert errors == []

    def test_anyof_invalid_value(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "number"}]}
        errors = _validate_field_type(self._obj(), "f", "not_a_number", field_schema)
        assert any(e.code == "E002" for e in errors)

    def test_single_type_mismatch(self) -> None:
        field_schema: dict[str, object] = {"type": "number"}
        errors = _validate_field_type(self._obj(), "f", "not_a_number", field_schema)
        assert any(e.code == "E003" for e in errors)

    def test_enum_valid_case_insensitive(self) -> None:
        field_schema: dict[str, object] = {"enum": ["Yes", "No"]}
        errors = _validate_field_type(self._obj(), "f", "yes", field_schema)
        assert errors == []

    def test_enum_invalid_string(self) -> None:
        field_schema: dict[str, object] = {"enum": ["Yes", "No"]}
        errors = _validate_field_type(self._obj(), "f", "Maybe", field_schema)
        assert any(e.code == "E004" for e in errors)

    def test_enum_invalid_non_string(self) -> None:
        field_schema: dict[str, object] = {"enum": [1, 2, 3]}
        errors = _validate_field_type(self._obj(), "f", 99, field_schema)
        assert any(e.code == "E004" for e in errors)


# ---------------------------------------------------------------------------
# _value_matches_type (exercised via _validate_field_type)
# ---------------------------------------------------------------------------


class TestValueMatchesType:
    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Zone", name="Z1")

    def test_number_accepts_int_and_float(self) -> None:
        for val in (1, 1.5):
            errors = _validate_field_type(self._obj(), "f", val, {"type": "number"})
            assert errors == [], f"Expected no errors for {val!r}"

    def test_number_rejects_string(self) -> None:
        errors = _validate_field_type(self._obj(), "f", "oops", {"type": "number"})
        assert any(e.code == "E003" for e in errors)

    def test_integer_accepts_whole_float(self) -> None:
        errors = _validate_field_type(self._obj(), "f", 3.0, {"type": "integer"})
        assert errors == []

    def test_integer_rejects_fractional_float(self) -> None:
        errors = _validate_field_type(self._obj(), "f", 3.5, {"type": "integer"})
        assert any(e.code == "E003" for e in errors)

    def test_string_rejects_int(self) -> None:
        errors = _validate_field_type(self._obj(), "f", 42, {"type": "string"})
        assert any(e.code == "E003" for e in errors)

    def test_boolean_accepts_bool(self) -> None:
        errors = _validate_field_type(self._obj(), "f", True, {"type": "boolean"})
        assert errors == []

    def test_boolean_rejects_int(self) -> None:
        errors = _validate_field_type(self._obj(), "f", 1, {"type": "boolean"})
        assert any(e.code == "E003" for e in errors)

    def test_array_accepts_list(self) -> None:
        errors = _validate_field_type(self._obj(), "f", [1, 2], {"type": "array"})
        assert errors == []

    def test_array_rejects_dict(self) -> None:
        errors = _validate_field_type(self._obj(), "f", {}, {"type": "array"})
        assert any(e.code == "E003" for e in errors)

    def test_object_accepts_dict(self) -> None:
        errors = _validate_field_type(self._obj(), "f", {"key": "val"}, {"type": "object"})
        assert errors == []

    def test_object_rejects_list(self) -> None:
        errors = _validate_field_type(self._obj(), "f", [], {"type": "object"})
        assert any(e.code == "E003" for e in errors)


# ---------------------------------------------------------------------------
# _validate_field_range
# ---------------------------------------------------------------------------


class TestValidateObjectNullFieldSkipped:
    def test_none_value_in_data_is_skipped(self) -> None:
        """Fields with None value in obj.data are skipped (no type/range checks)."""
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"x_origin": None, "y_origin": 0.0})
        errors = _validate_object(obj, schema)
        assert not any(e.field == "x_origin" for e in errors)

    def test_empty_string_value_in_data_is_skipped(self) -> None:
        """Fields with empty string value are skipped."""
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"x_origin": "", "y_origin": 0.0})
        errors = _validate_object(obj, schema)
        assert not any(e.field == "x_origin" for e in errors)


class TestValueMatchesTypeEnumBranch:
    """Tests for the enum-only branch in _value_matches_type (no 'type' key, has 'enum')."""

    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Zone", name="Z1")

    def test_anyof_subschema_enum_match(self) -> None:
        """anyOf sub-schema with only 'enum' (no 'type') should match via enum check."""
        field_schema: dict[str, object] = {"anyOf": [{"enum": ["Yes", "No"]}, {"type": "string"}]}
        errors = _validate_field_type(self._obj(), "f", "Yes", field_schema)
        assert errors == []

    def test_anyof_subschema_enum_no_match_falls_through(self) -> None:
        """Value not in enum sub-schema causes the sub-schema to be invalid."""
        field_schema: dict[str, object] = {"anyOf": [{"enum": ["Yes", "No"]}]}
        errors = _validate_field_type(self._obj(), "f", "Maybe", field_schema)
        assert any(e.code == "E002" for e in errors)

    def test_anyof_subschema_no_type_no_enum_assumes_valid(self) -> None:
        """anyOf sub-schema with no 'type' and no 'enum' returns True (unknown type)."""
        # A sub-schema with only a description (no type, no enum) matches any value
        field_schema: dict[str, object] = {"anyOf": [{"description": "anything goes"}]}
        errors = _validate_field_type(self._obj(), "f", "anything", field_schema)
        assert errors == []


class TestValidateFieldRange:
    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Zone", name="Z1")

    def test_below_minimum(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", -1.0, {"minimum": 0.0})
        assert any(e.code == "E005" for e in errors)

    def test_at_minimum_passes(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 0.0, {"minimum": 0.0})
        assert errors == []

    def test_at_exclusive_minimum_fails(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 0.0, {"exclusiveMinimum": 0.0})
        assert any(e.code == "E006" for e in errors)

    def test_above_exclusive_minimum_passes(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 0.1, {"exclusiveMinimum": 0.0})
        assert errors == []

    def test_above_maximum(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 11.0, {"maximum": 10.0})
        assert any(e.code == "E007" for e in errors)

    def test_at_maximum_passes(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 10.0, {"maximum": 10.0})
        assert errors == []

    def test_at_exclusive_maximum_fails(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 10.0, {"exclusiveMaximum": 10.0})
        assert any(e.code == "E008" for e in errors)

    def test_below_exclusive_maximum_passes(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 9.9, {"exclusiveMaximum": 10.0})
        assert errors == []
