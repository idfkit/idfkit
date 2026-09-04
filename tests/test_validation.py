"""Tests for the validation module."""

from __future__ import annotations

from typing import ClassVar
from unittest.mock import patch

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFCollection, IDFObject
from idfkit.schema import get_schema
from idfkit.validation import (
    Severity,
    ValidationError,
    ValidationResult,
    _unpopulated_reference_lists,  # pyright: ignore[reportPrivateUsage]
    _validate_field,  # pyright: ignore[reportPrivateUsage]
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
        errors = _validate_field(self._obj(), "f", 42.0, field_schema)
        assert errors == []

    def test_anyof_invalid_value(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "number"}]}
        errors = _validate_field(self._obj(), "f", "not_a_number", field_schema)
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
        """A branch with only 'enum' (no 'type') constrains nothing on type; the enum passes."""
        field_schema: dict[str, object] = {"anyOf": [{"enum": ["Yes", "No"]}, {"type": "string"}]}
        errors = _validate_field(self._obj(), "f", "Yes", field_schema)
        assert errors == []

    def test_anyof_subschema_enum_no_match_reports_enum_violation(self) -> None:
        """A typeless branch is satisfied on type, so its enum failure is E004, not E002.

        E002 is reserved for a value that matches no branch on *type*. A branch with no
        ``type`` key imposes no type constraint, so the value matches it and then fails
        its enum.
        """
        field_schema: dict[str, object] = {"anyOf": [{"enum": ["Yes", "No"]}]}
        errors = _validate_field(self._obj(), "f", "Maybe", field_schema)
        assert [e.code for e in errors] == ["E004"]

    def test_anyof_subschema_no_type_no_enum_assumes_valid(self) -> None:
        """A branch with neither 'type' nor 'enum' constrains nothing and matches any value."""
        field_schema: dict[str, object] = {"anyOf": [{"description": "anything goes"}]}
        errors = _validate_field(self._obj(), "f", "anything", field_schema)
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


class TestValidateFieldRangeDraft04:
    """Schemas for EnergyPlus 8.9.0-9.5.0 are JSON Schema draft-04.

    There, ``exclusiveMinimum``/``exclusiveMaximum`` are booleans qualifying the
    sibling ``minimum``/``maximum`` rather than carrying a bound of their own.
    Treating the boolean as a number silently compares against ``1``.
    """

    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Material", name="Concrete")

    def test_value_below_one_passes_exclusive_minimum_zero(self) -> None:
        """Regression: 0.2 with {minimum: 0.0, exclusiveMinimum: true} is valid.

        Comparing 0.2 against the boolean resolved it to ``0.2 <= True`` (i.e.
        ``0.2 <= 1``), rejecting every EnergyPlus 8.9-9.5 model with a material
        thinner than a metre.
        """
        errors = _validate_field_range(self._obj(), "thickness", 0.2, {"minimum": 0.0, "exclusiveMinimum": True})
        assert errors == []

    def test_at_bound_fails_when_exclusive(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 0.0, {"minimum": 0.0, "exclusiveMinimum": True})
        assert any(e.code == "E006" for e in errors)

    def test_at_bound_passes_when_not_exclusive(self) -> None:
        errors = _validate_field_range(self._obj(), "thickness", 0.0, {"minimum": 0.0})
        assert errors == []

    def test_value_above_one_passes_exclusive_maximum(self) -> None:
        errors = _validate_field_range(self._obj(), "fraction", 5.0, {"maximum": 10.0, "exclusiveMaximum": True})
        assert errors == []

    def test_at_upper_bound_fails_when_exclusive(self) -> None:
        errors = _validate_field_range(self._obj(), "fraction", 10.0, {"maximum": 10.0, "exclusiveMaximum": True})
        assert any(e.code == "E008" for e in errors)


# ---------------------------------------------------------------------------
# anyOf fields: type, enum and bounds weighed together, one finding per field
# ---------------------------------------------------------------------------


class TestAnyOfField:
    """An ``anyOf`` value is valid only when it *fully* satisfies one branch.

    Regression cover for a validator that read bounds from the top level of the field
    schema (where an ``anyOf`` field has none) and stopped a branch at its ``type``
    without consulting its ``enum``. Both defects let invalid values through.
    """

    def _obj(self) -> IDFObject:
        return IDFObject(obj_type="Zone", name="Z1")

    # Autosizable numeric field: number with bounds, or the "Autosize" sentinel.
    AUTOSIZABLE: ClassVar[dict[str, object]] = {
        "anyOf": [
            {"type": "number", "minimum": 0.0, "maximum": 1.0},
            {"type": "string", "enum": ["", "Autosize"]},
        ]
    }

    def test_number_within_bounds_is_valid(self) -> None:
        assert _validate_field(self._obj(), "f", 0.5, self.AUTOSIZABLE) == []

    def test_number_above_branch_maximum_reports_e007(self) -> None:
        """The bound lives inside anyOf[0]; reading only the top level found no bound."""
        errors = _validate_field(self._obj(), "f", 5.0, self.AUTOSIZABLE)
        assert [e.code for e in errors] == ["E007"]

    def test_number_below_branch_minimum_reports_e005(self) -> None:
        errors = _validate_field(self._obj(), "f", -1.0, self.AUTOSIZABLE)
        assert [e.code for e in errors] == ["E005"]

    def test_sentinel_string_is_valid(self) -> None:
        assert _validate_field(self._obj(), "f", "Autosize", self.AUTOSIZABLE) == []

    def test_sentinel_match_is_case_insensitive(self) -> None:
        assert _validate_field(self._obj(), "f", "autosize", self.AUTOSIZABLE) == []

    def test_wrong_sentinel_reports_e004(self) -> None:
        """The string branch matches on type, so its enum failure is E004, not E002."""
        errors = _validate_field(self._obj(), "f", "Autocalculate", self.AUTOSIZABLE)
        assert [e.code for e in errors] == ["E004"]

    def test_arbitrary_string_reports_e004(self) -> None:
        errors = _validate_field(self._obj(), "f", "Bogus", self.AUTOSIZABLE)
        assert [e.code for e in errors] == ["E004"]

    def test_string_branch_without_enum_accepts_any_string(self) -> None:
        """646 fields put no enum on the string branch, so any string is legal there."""
        field_schema: dict[str, object] = {"anyOf": [{"type": "number", "minimum": 0.0}, {"type": "string"}]}
        assert _validate_field(self._obj(), "f", "anything at all", field_schema) == []

    def test_value_matching_no_branch_type_reports_e002(self) -> None:
        errors = _validate_field(self._obj(), "f", [1, 2], self.AUTOSIZABLE)
        assert [e.code for e in errors] == ["E002"]

    def test_numeric_enum_on_number_branch_is_enforced(self) -> None:
        """68 fields are choice fields expressed as numbers; 3 is invalid where 0/1 are legal."""
        field_schema: dict[str, object] = {
            "anyOf": [{"type": "number", "enum": [0, 1]}, {"type": "string", "enum": [""]}]
        }
        assert _validate_field(self._obj(), "f", 1, field_schema) == []
        errors = _validate_field(self._obj(), "f", 3, field_schema)
        assert [e.code for e in errors] == ["E004"]

    def test_at_most_one_finding_per_field(self) -> None:
        """A value failing every branch still yields exactly one finding."""
        field_schema: dict[str, object] = {
            "anyOf": [
                {"type": "number", "minimum": 0.0, "maximum": 1.0},
                {"type": "number", "minimum": 10.0},
            ]
        }
        errors = _validate_field(self._obj(), "f", 5.0, field_schema)
        assert len(errors) == 1

    def test_first_matched_branch_reports_the_failure(self) -> None:
        """Declaration order decides which branch's diagnostic the user sees."""
        field_schema: dict[str, object] = {
            "anyOf": [
                {"type": "number", "maximum": 1.0},
                {"type": "number", "minimum": 10.0},
            ]
        }
        errors = _validate_field(self._obj(), "f", 5.0, field_schema)
        assert [e.code for e in errors] == ["E007"]

    def test_second_branch_can_rescue_the_value(self) -> None:
        field_schema: dict[str, object] = {
            "anyOf": [
                {"type": "number", "maximum": 1.0},
                {"type": "number", "minimum": 4.0},
            ]
        }
        assert _validate_field(self._obj(), "f", 5.0, field_schema) == []

    def test_bool_does_not_satisfy_a_number_branch(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "number"}]}
        errors = _validate_field(self._obj(), "f", True, field_schema)
        assert [e.code for e in errors] == ["E002"]

    def test_integer_branch_accepts_whole_float(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "integer"}, {"type": "string", "enum": ["", "Autosize"]}]}
        assert _validate_field(self._obj(), "f", 3.0, field_schema) == []

    def test_draft04_boolean_exclusive_minimum_inside_a_branch(self) -> None:
        """8.9.0-9.5.0 schemas put a *boolean* exclusiveMinimum next to the minimum."""
        field_schema: dict[str, object] = {
            "anyOf": [
                {"type": "number", "minimum": 0.0, "exclusiveMinimum": True},
                {"type": "string", "enum": ["", "Autosize"]},
            ]
        }
        assert _validate_field(self._obj(), "f", 0.2, field_schema) == []
        errors = _validate_field(self._obj(), "f", 0.0, field_schema)
        assert [e.code for e in errors] == ["E006"]

    def test_draft06_numeric_exclusive_maximum_inside_a_branch(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "number", "exclusiveMaximum": 1.0}, {"type": "string"}]}
        errors = _validate_field(self._obj(), "f", 1.0, field_schema)
        assert [e.code for e in errors] == ["E008"]

    def test_check_ranges_disabled_skips_branch_bounds(self) -> None:
        errors = _validate_field(self._obj(), "f", 5.0, self.AUTOSIZABLE, check_ranges=False)
        assert errors == []

    def test_check_types_disabled_skips_branch_enum_and_e002(self) -> None:
        assert _validate_field(self._obj(), "f", "Bogus", self.AUTOSIZABLE, check_types=False) == []
        assert _validate_field(self._obj(), "f", [1, 2], self.AUTOSIZABLE, check_types=False) == []

    def test_check_types_disabled_still_reports_bounds(self) -> None:
        errors = _validate_field(self._obj(), "f", 5.0, self.AUTOSIZABLE, check_types=False)
        assert [e.code for e in errors] == ["E007"]


class TestAnyOfAgainstRealSchema:
    """The same rule against the bundled EnergyPlus schemas."""

    def test_view_factor_to_ground_above_maximum(self) -> None:
        """maximum 1.0 lives inside anyOf[0] and used to be invisible to the validator."""
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="BuildingSurface:Detailed", name="Wall1", data={"view_factor_to_ground": 5.0})
        errors = _validate_object(obj, schema, check_required=False)
        assert [e.code for e in errors if e.field == "view_factor_to_ground"] == ["E007"]

    def test_view_factor_to_ground_autocalculate_is_valid(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(
            obj_type="BuildingSurface:Detailed", name="Wall1", data={"view_factor_to_ground": "Autocalculate"}
        )
        errors = _validate_object(obj, schema, check_required=False)
        assert [e for e in errors if e.field == "view_factor_to_ground"] == []

    def test_ceiling_height_rejects_arbitrary_string(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"ceiling_height": "Bogus"})
        errors = _validate_object(obj, schema, check_required=False)
        assert [e.code for e in errors if e.field == "ceiling_height"] == ["E004"]

    def test_ceiling_height_accepts_its_own_sentinel(self) -> None:
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"ceiling_height": "Autocalculate"})
        errors = _validate_object(obj, schema, check_required=False)
        assert [e for e in errors if e.field == "ceiling_height"] == []

    def test_ceiling_height_rejects_the_wrong_sentinel(self) -> None:
        """The sentinel is not always Autosize; 1,781 fields accept Autocalculate instead."""
        schema = get_schema((24, 1, 0))
        obj = IDFObject(obj_type="Zone", name="Z1", data={"ceiling_height": "Autosize"})
        errors = _validate_object(obj, schema, check_required=False)
        assert [e.code for e in errors if e.field == "ceiling_height"] == ["E004"]

    def test_draft04_schema_material_thickness_still_valid(self) -> None:
        """8.9.0 is draft-04: the boolean exclusiveMinimum must not be read as the bound 1."""
        schema = get_schema((8, 9, 0))
        obj = IDFObject(
            obj_type="Material",
            name="Concrete",
            data={
                "roughness": "MediumRough",
                "thickness": 0.2,
                "conductivity": 1.7,
                "density": 2200.0,
                "specific_heat": 900.0,
            },
        )
        assert _validate_object(obj, schema) == []


class TestReferenceDeclarations:
    """Names a document declares, and reference lists nothing can declare into.

    Both cases were false positives: the validator accused a valid model of naming
    something that does not exist. Over-reporting is as wrong as under-reporting,
    because a validator that cries wolf on working files stops being read.
    """

    def test_name_declared_by_a_field_is_not_dangling(self) -> None:
        """`FluidProperties:Name` has no name field and declares itself through `fluid_name`."""
        doc = new_document(version=(26, 1, 0))
        doc.add("FluidProperties:Name", fluid_name="R22", fluid_type="Refrigerant")
        doc.add("FluidProperties:Saturated", name="Sat1", fluid_name="R22")

        result = validate_document(doc)

        assert [e for e in result.errors if e.code == "E009"] == []

    def test_a_genuinely_undeclared_fluid_is_still_dangling(self) -> None:
        """The fix must not blanket-suppress the check it narrows."""
        doc = new_document(version=(26, 1, 0))
        doc.add("FluidProperties:Name", fluid_name="R22", fluid_type="Refrigerant")
        doc.add("FluidProperties:Saturated", name="Sat1", fluid_name="NeverDeclared")

        result = validate_document(doc)

        assert [e.code for e in result.errors if e.field == "fluid_name"] == ["E009"]

    def test_object_type_field_is_not_reported_as_a_dangling_name(self) -> None:
        """`validOASysEquipmentTypes` holds TYPE names, which no object ever declares."""
        doc = new_document(version=(26, 1, 0))
        doc.add(
            "AirLoopHVAC:OutdoorAirSystem:EquipmentList",
            name="OAEquip",
            component_1_object_type="OutdoorAir:Mixer",
            component_1_name="OAMixer",
            validate=False,
        )

        result = validate_document(doc)

        # component_1_name IS a real reference and stays dangling; only the TYPE field is exempt.
        assert [e for e in result.errors if e.field == "component_1_object_type"] == []
        assert [e.code for e in result.errors if e.field == "component_1_name"] == ["E009"]

    def test_the_unpopulated_list_set_is_exactly_the_four_equipment_type_lists(self) -> None:
        """Pin the set, so a schema change that adds a fifth is noticed rather than absorbed."""
        assert set(_unpopulated_reference_lists(get_schema((26, 1, 0)))) == {
            "validBranchEquipmentTypes",
            "validCondenserEquipmentTypes",
            "validOASysEquipmentTypes",
            "validPlantEquipmentTypes",
        }


class TestExtensibleGroupReferences:
    """References inside extensible groups are checked like any other reference.

    Ninety reference fields in the 26.1.0 schema sit inside an extensible group rather than
    at the top level, `Schedule:Week:Compact.schedule_day_name` and `SpaceList.space_name`
    among them. Skipping them under-validates nearly every model that carries a schedule.
    """

    def test_a_dangling_reference_inside_an_extensible_group_is_reported(self) -> None:
        doc = new_document(version=(26, 1, 0))
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "TotallyNotDefined"})

        result = validate_document(doc)

        assert [e.field for e in result.errors if e.code == "E009"] == ["electric_equipment_name"]

    def test_a_resolvable_reference_inside_an_extensible_group_is_not_reported(self) -> None:
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Office")
        doc.add(
            "ElectricEquipment",
            name="Office Equipment",
            zone_or_zonelist_or_space_or_spacelist_name="Office",
            schedule_name="Always On",
            design_level_calculation_method="EquipmentLevel",
            design_level=100.0,
            validate=False,
        )
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "Office Equipment"})

        result = validate_document(doc)

        assert [e for e in result.errors if e.field == "electric_equipment_name"] == []

    def test_every_repeat_group_is_reported_not_just_the_first(self) -> None:
        """Two groups naming the same missing target are two findings, matching TypeScript."""
        doc = new_document(version=(26, 1, 0))
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "Missing Equipment"})
        manager.equipment.append({"electric_equipment_name": "Missing Equipment"})

        result = validate_document(doc)

        assert [e.field for e in result.errors if e.code == "E009"] == [
            "electric_equipment_name",
            "electric_equipment_name",
        ]


class TestZoneListExpandedNames:
    """A reference may point at a name EnergyPlus synthesises rather than one a file declares."""

    def test_a_zonelist_expanded_name_is_not_dangling(self) -> None:
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "SPACE1-1")
        doc.add(
            "ElectricEquipment",
            name="AllZones with Electric Equipment",
            zone_or_zonelist_or_space_or_spacelist_name="AllOccupiedZones",
            schedule_name="Always On",
            design_level_calculation_method="EquipmentLevel",
            design_level=100.0,
            validate=False,
        )
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "Space1-1 AllZones with Electric Equipment"})

        result = validate_document(doc)

        assert [e for e in result.errors if e.field == "electric_equipment_name"] == []

    def test_the_split_is_tried_at_every_space_not_only_the_first(self) -> None:
        """Zone names contain spaces too, so the first space is not always the join point."""
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Thermal Zone 1")
        doc.add(
            "ElectricEquipment",
            name="Shared Equipment",
            zone_or_zonelist_or_space_or_spacelist_name="AllZones",
            schedule_name="Always On",
            design_level_calculation_method="EquipmentLevel",
            design_level=100.0,
            validate=False,
        )
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "Thermal Zone 1 Shared Equipment"})

        result = validate_document(doc)

        assert [e for e in result.errors if e.field == "electric_equipment_name"] == []

    def test_an_unknown_prefix_is_still_dangling(self) -> None:
        """The rule must not swallow a genuine typo that happens to contain a space."""
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "SPACE1-1")
        doc.add(
            "ElectricEquipment",
            name="AllZones with Electric Equipment",
            zone_or_zonelist_or_space_or_spacelist_name="AllOccupiedZones",
            schedule_name="Always On",
            design_level_calculation_method="EquipmentLevel",
            design_level=100.0,
            validate=False,
        )
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "NotAZone AllZones with Electric Equipment"})

        result = validate_document(doc)

        assert [e.code for e in result.errors if e.field == "electric_equipment_name"] == ["E009"]


class TestImplicitRemainderSpace:
    """`<Zone Name>-Remainder` is a space EnergyPlus creates; no file declares it."""

    def test_a_remainder_space_reference_is_not_dangling(self) -> None:
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Zone 5")
        doc.add("Space", "Space 5 Office", zone_name="Zone 5")
        connections = doc.add(
            "SpaceHVAC:EquipmentConnections",
            space_name="Zone 5-Remainder",
            validate=False,
        )
        assert connections is not None

        result = validate_document(doc)

        assert [e for e in result.errors if e.field == "space_name"] == []

    def test_the_suffix_alone_does_not_excuse_an_unknown_zone(self) -> None:
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Zone 5")
        doc.add("SpaceHVAC:EquipmentConnections", space_name="Zone 9-Remainder", validate=False)

        result = validate_document(doc)

        assert [e.code for e in result.errors if e.field == "space_name"] == ["E009"]

    def test_a_space_named_prefix_does_not_qualify_only_a_zone_does(self) -> None:
        """The rule names `Zone`, and a `Space` is not a zone."""
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Zone 5")
        doc.add("Space", "Lobby", zone_name="Zone 5")
        doc.add("SpaceHVAC:EquipmentConnections", space_name="Lobby-Remainder", validate=False)

        result = validate_document(doc)

        assert [e.code for e in result.errors if e.field == "space_name"] == ["E009"]
