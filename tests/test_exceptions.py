"""Tests for custom exceptions."""

from __future__ import annotations

import pickle

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import (
    DanglingReferenceError,
    DuplicateObjectError,
    EnergyPlusNotFoundError,
    ExpandObjectsError,
    IdfKitError,
    IDFParseError,
    InvalidFieldError,
    NoDesignDaysError,
    ObjectNotFoundError,
    ParseDiagnostic,
    ParseError,
    RangeError,
    SchemaNotFoundError,
    SimulationError,
    UnknownObjectTypeError,
    UnsupportedVersionError,
    ValidationFailedError,
    VersionNotFoundError,
)
from idfkit.objects import IDFObject
from idfkit.versions import ENERGYPLUS_VERSIONS


class TestIdfKitError:
    def test_base_exception(self) -> None:
        err = IdfKitError("test error")
        assert str(err) == "test error"
        assert isinstance(err, Exception)

    def test_parse_error_alias(self) -> None:
        assert ParseError is IdfKitError


class TestIDFParseError:
    def test_no_diagnostics(self) -> None:
        err = IDFParseError("parse failed")
        assert "parse failed" in str(err)
        assert err.diagnostics == ()

    def test_with_diagnostic_full_location(self) -> None:
        diag = ParseDiagnostic(message="unexpected token", filepath="/a/b.idf", line=10, column=5)
        err = IDFParseError("parse failed", diagnostics=[diag])
        s = str(err)
        assert "/a/b.idf:10:5" in s
        assert "unexpected token" in s

    def test_with_diagnostic_filepath_and_line(self) -> None:
        diag = ParseDiagnostic(message="bad value", filepath="/a/b.idf", line=3)
        err = IDFParseError("parse failed", diagnostics=[diag])
        s = str(err)
        assert "/a/b.idf:3" in s
        assert "bad value" in s

    def test_with_diagnostic_filepath_only(self) -> None:
        diag = ParseDiagnostic(message="error", filepath="/a/b.idf")
        err = IDFParseError("parse failed", diagnostics=[diag])
        s = str(err)
        assert "/a/b.idf" in s

    def test_with_diagnostic_no_location(self) -> None:
        diag = ParseDiagnostic(message="mystery error")
        err = IDFParseError("parse failed", diagnostics=[diag])
        s = str(err)
        assert "unknown location" in s

    def test_with_diagnostic_obj_type_and_name(self) -> None:
        diag = ParseDiagnostic(message="err", filepath="/f.idf", line=1, column=1, obj_type="Zone", obj_name="Z1")
        err = IDFParseError("parse failed", diagnostics=[diag])
        s = str(err)
        assert "[object: Zone]" in s
        assert "[name: Z1]" in s

    def test_is_idfkit_error(self) -> None:
        assert isinstance(IDFParseError("x"), IdfKitError)


class TestSchemaNotFoundError:
    def test_basic(self) -> None:
        err = SchemaNotFoundError((24, 1, 0))
        assert err.version == (24, 1, 0)
        assert "24.1.0" in str(err)

    def test_with_searched_paths(self) -> None:
        err = SchemaNotFoundError((24, 1, 0), searched_paths=["/path/a", "/path/b"])
        assert err.searched_paths == ["/path/a", "/path/b"]
        assert "/path/a" in str(err)

    def test_is_idfkit_error(self) -> None:
        err = SchemaNotFoundError((1, 0, 0))
        assert isinstance(err, IdfKitError)


class TestDuplicateObjectError:
    def test_basic(self) -> None:
        err = DuplicateObjectError("Zone", "MyZone")
        assert err.obj_type == "Zone"
        assert err.name == "MyZone"
        assert "Zone" in str(err)
        assert "MyZone" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(DuplicateObjectError("Zone", "Z"), IdfKitError)


class TestUnknownObjectTypeError:
    def test_basic(self) -> None:
        err = UnknownObjectTypeError("FakeType")
        assert err.obj_type == "FakeType"
        assert "FakeType" in str(err)

    def test_with_version_known_type(self) -> None:
        """With a version, the error may append a docs URL for recognised types."""
        err = UnknownObjectTypeError("Zone", version=(24, 1, 0))
        assert "Zone" in str(err)

    def test_with_version_unknown_type(self) -> None:
        """With a version but unknown type, no URL is added but no crash either."""
        err = UnknownObjectTypeError("TotallyMadeUpType", version=(24, 1, 0))
        assert "TotallyMadeUpType" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(UnknownObjectTypeError("X"), IdfKitError)

    def test_is_key_error(self) -> None:
        assert isinstance(UnknownObjectTypeError("X"), KeyError)

    def test_str_is_the_message_not_its_repr(self) -> None:
        """KeyError.__str__ would quote the message and show its line break as a literal backslash-n."""
        err = UnknownObjectTypeError("Zoen", version=(24, 1, 0), suggestion="Zone")
        text = str(err)
        assert text.startswith("Unknown object type: 'Zoen'. Did you mean 'Zone'?")
        assert "\\n" not in text
        assert err.suggestion == "Zone"

    def test_pickles(self) -> None:
        import pickle

        err = pickle.loads(pickle.dumps(UnknownObjectTypeError("Zoen", (24, 1, 0), "Zone")))  # noqa: S301
        assert (err.obj_type, err.version, err.suggestion) == ("Zoen", (24, 1, 0), "Zone")

    def test_add_suggests_the_closest_type(self) -> None:
        from idfkit import new_document

        with pytest.raises(UnknownObjectTypeError, match="Did you mean 'Zone'") as exc_info:
            new_document().add("Zoen", "Z")
        assert exc_info.value.suggestion == "Zone"


class TestInvalidFieldError:
    def test_basic(self) -> None:
        err = InvalidFieldError("Zone", "bad_field")
        assert err.obj_type == "Zone"
        assert err.field_name == "bad_field"
        assert "Zone" in str(err)
        assert "bad_field" in str(err)

    def test_with_available_fields(self) -> None:
        err = InvalidFieldError("Zone", "bad", available_fields=["x_origin", "y_origin"])
        assert err.available_fields == ["x_origin", "y_origin"]
        assert "x_origin" in str(err)

    def test_with_many_available_fields(self) -> None:
        fields = [f"field_{i}" for i in range(15)]
        err = InvalidFieldError("Zone", "bad", available_fields=fields)
        assert "... and 5 more" in str(err)

    def test_with_extensible_fields(self) -> None:
        err = InvalidFieldError("Zone", "bad", extensible_fields=frozenset(["x_coord", "y_coord"]))
        s = str(err)
        assert "extensible" in s
        assert "x_coord" in s

    def test_with_version_known_type(self) -> None:
        """With a version for a recognised type, docs URL may be appended."""
        err = InvalidFieldError("Zone", "bad_field", version=(24, 1, 0))
        assert "bad_field" in str(err)

    def test_with_version_unknown_type(self) -> None:
        """With a version for an unknown type, no URL but no crash."""
        err = InvalidFieldError("MadeUpType", "bad_field", version=(24, 1, 0))
        assert "bad_field" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(InvalidFieldError("Z", "f"), IdfKitError)

    def test_is_attribute_error(self) -> None:
        assert isinstance(InvalidFieldError("Z", "f"), AttributeError)


class TestVersionNotFoundError:
    def test_basic(self) -> None:
        err = VersionNotFoundError("/path/to/file.idf")
        assert err.filepath == "/path/to/file.idf"
        assert "file.idf" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(VersionNotFoundError("x"), IdfKitError)


class TestDanglingReferenceError:
    def test_basic(self) -> None:
        obj = IDFObject(obj_type="People", name="P1")
        err = DanglingReferenceError(obj, "zone_name", "NonexistentZone")
        assert err.source is obj
        assert err.field == "zone_name"
        assert err.target == "NonexistentZone"
        assert "People" in str(err)
        assert "NonexistentZone" in str(err)

    def test_is_idfkit_error(self) -> None:
        obj = IDFObject(obj_type="X", name="Y")
        assert isinstance(DanglingReferenceError(obj, "f", "t"), IdfKitError)

    def test_suggestion(self) -> None:
        obj = IDFObject(obj_type="Construction", name="Wall")
        err = DanglingReferenceError(obj, "layer_2", "Insulx", suggestion="Insulation")
        assert err.suggestion == "Insulation"
        assert str(err).endswith(". Did you mean 'Insulation'?")


class TestObjectNotFoundError:
    def _doc(self) -> IDFDocument:
        doc = new_document()
        for name in ("SPACE1-1", "SPACE2-1", "PLENUM-1"):
            doc.add("Zone", name)
        return doc

    def test_lookup_by_name_suggests_the_closest_name(self) -> None:
        with pytest.raises(ObjectNotFoundError) as excinfo:
            _ = self._doc()["Zone"]["SPACE1_1"]
        err = excinfo.value
        assert isinstance(err, KeyError)
        assert isinstance(err, IdfKitError)
        assert (
            str(err) == "No Zone named 'SPACE1_1'. Did you mean 'SPACE1-1'?\n  Zone names: SPACE1-1, SPACE2-1, PLENUM-1"
        )
        assert (err.obj_type, err.name) == ("Zone", "SPACE1_1")
        assert err.suggestions[0] == "SPACE1-1"
        assert err.available == ("SPACE1-1", "SPACE2-1", "PLENUM-1")

    def test_rename_and_dotted_update_raise_it_too(self) -> None:
        doc = self._doc()
        with pytest.raises(ObjectNotFoundError, match="Did you mean 'SPACE1-1'"):
            doc.rename("Zone", "SPACE1_1", "X")
        with pytest.raises(ObjectNotFoundError, match="Did you mean 'SPACE1-1'"):
            doc.update({"Zone.SPACE1_1.x_origin": 1.0})

    def test_empty_collection_says_so(self) -> None:
        with pytest.raises(ObjectNotFoundError, match="The document has no Material objects"):
            _ = self._doc()["Material"]["Concrete"]

    def test_long_listing_is_truncated(self) -> None:
        err = ObjectNotFoundError("Zone", "Q", [f"Z{i}" for i in range(25)])
        assert "Z9, ... (15 more)" in str(err)
        assert "Z10" not in str(err)

    def test_nameless_type_does_not_claim_the_document_has_none(self) -> None:
        doc = new_document()
        assert len(doc["SimulationControl"]) == 1
        with pytest.raises(ObjectNotFoundError) as excinfo:
            _ = doc["SimulationControl"]["foo"]
        message = str(excinfo.value)
        assert "has no SimulationControl objects" not in message
        assert "1 SimulationControl object has no name" in message

    def test_names_are_not_computed_until_the_message_is_read(self) -> None:
        calls: list[int] = []

        def names() -> list[str]:
            calls.append(1)
            return ["SPACE1-1"]

        err = ObjectNotFoundError("Zone", "SPACE1_1", names)
        assert calls == []
        assert err.suggestions == ("SPACE1-1",)
        _ = str(err)
        assert calls == [1]

    def test_caught_miss_does_not_build_the_message(self) -> None:
        doc = self._doc()
        try:
            _ = doc["Zone"]["SPACE1_1"]
        except KeyError as exc:
            assert isinstance(exc, ObjectNotFoundError)
            assert exc._message is None  # pyright: ignore[reportPrivateUsage]
            assert exc._suggestions is None  # pyright: ignore[reportPrivateUsage]

    def test_pickle_round_trip(self) -> None:
        err = ObjectNotFoundError("Zone", "SPACE1_1", lambda: ["SPACE1-1"], object_count=1)
        clone = pickle.loads(pickle.dumps(err))  # noqa: S301
        assert str(clone) == str(err)
        assert clone.available == err.available


class TestRangeError:
    def test_basic(self) -> None:
        err = RangeError("Zone", "MyZone", "thickness", "Value out of range")
        assert err.obj_type == "Zone"
        assert err.obj_name == "MyZone"
        assert err.field_name == "thickness"
        assert "Value out of range" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(RangeError("Z", "N", "f", "msg"), IdfKitError)


class TestValidationFailedError:
    def test_basic(self) -> None:
        errors: list[object] = ["error 1", "error 2"]
        err = ValidationFailedError(errors)
        assert err.errors == errors
        assert "2 error(s)" in str(err)

    def test_truncation(self) -> None:
        errors: list[object] = [f"error {i}" for i in range(10)]
        err = ValidationFailedError(errors)
        assert "... and 5 more" in str(err)

    def test_header_counts_by_severity(self) -> None:
        """A warning is counted as a warning, not as an error."""
        from idfkit.validation import Severity, ValidationError

        def issue(severity: Severity) -> ValidationError:
            return ValidationError(severity=severity, obj_type="Zone", obj_name="Z", field=None, message="m", code="X")

        err = ValidationFailedError([issue(Severity.ERROR), issue(Severity.WARNING), issue(Severity.WARNING)])
        assert str(err).startswith("Validation failed with 1 error(s), 2 warning(s):")
        assert str(ValidationFailedError([issue(Severity.WARNING)])).startswith("Validation failed with 1 warning(s):")

    def test_is_idfkit_error(self) -> None:
        assert isinstance(ValidationFailedError([]), IdfKitError)


class TestExpandObjectsError:
    def test_basic(self) -> None:
        err = ExpandObjectsError("something failed")
        assert str(err) == "something failed"
        assert err.preprocessor is None
        assert err.exit_code is None
        assert err.stderr is None

    def test_with_preprocessor(self) -> None:
        err = ExpandObjectsError("failed", preprocessor="Slab")
        assert err.preprocessor == "Slab"
        assert str(err) == "failed"

    def test_with_exit_code(self) -> None:
        err = ExpandObjectsError("failed", exit_code=1)
        assert err.exit_code == 1
        assert "(exit code 1)" in str(err)

    def test_with_stderr(self) -> None:
        err = ExpandObjectsError("failed", stderr="  bad input  ")
        assert err.stderr == "  bad input  "
        assert "stderr: bad input" in str(err)

    def test_with_all_fields(self) -> None:
        err = ExpandObjectsError(
            "ExpandObjects did not produce expanded.idf",
            preprocessor="ExpandObjects",
            exit_code=1,
            stderr="some error",
        )
        assert err.preprocessor == "ExpandObjects"
        assert err.exit_code == 1
        assert err.stderr == "some error"
        assert "(exit code 1)" in str(err)
        assert "stderr: some error" in str(err)

    def test_stderr_truncated(self) -> None:
        long_stderr = "x" * 600
        err = ExpandObjectsError("failed", stderr=long_stderr)
        assert len(str(err)) < 700

    def test_is_idfkit_error(self) -> None:
        assert isinstance(ExpandObjectsError("x"), IdfKitError)

    def test_interface_matches_simulation_error(self) -> None:
        """ExpandObjectsError and SimulationError share the same exit_code/stderr interface."""
        expand_err = ExpandObjectsError("expand failed", exit_code=1, stderr="err1")
        sim_err = SimulationError("sim failed", exit_code=2, stderr="err2")
        assert expand_err.exit_code == 1
        assert sim_err.exit_code == 2
        assert expand_err.stderr == "err1"
        assert sim_err.stderr == "err2"


class TestSimulationError:
    def test_basic(self) -> None:
        err = SimulationError("sim failed")
        assert "sim failed" in str(err)
        assert err.exit_code is None
        assert err.stderr is None

    def test_with_exit_code(self) -> None:
        err = SimulationError("failed", exit_code=2)
        assert "(exit code 2)" in str(err)

    def test_with_stderr(self) -> None:
        err = SimulationError("failed", stderr="some error output")
        assert "stderr: some error output" in str(err)

    def test_is_idfkit_error(self) -> None:
        assert isinstance(SimulationError("x"), IdfKitError)


class TestEnergyPlusNotFoundError:
    def test_no_locations(self) -> None:
        err = EnergyPlusNotFoundError()
        s = str(err)
        assert "Could not find an EnergyPlus installation" in s
        assert "ENERGYPLUS_DIR" in s

    def test_with_searched_locations(self) -> None:
        err = EnergyPlusNotFoundError(searched_locations=["/usr/local/EnergyPlus", "/opt/EnergyPlus"])
        s = str(err)
        assert "/usr/local/EnergyPlus" in s
        assert "/opt/EnergyPlus" in s
        assert "Searched in:" in s

    def test_is_idfkit_error(self) -> None:
        assert isinstance(EnergyPlusNotFoundError(), IdfKitError)


class TestNoDesignDaysError:
    def test_with_station_name(self) -> None:
        err = NoDesignDaysError(station_name="Denver International Airport")
        s = str(err)
        assert "Denver International Airport" in s
        assert "SizingPeriod:DesignDay" in s

    def test_with_ddy_path(self) -> None:
        err = NoDesignDaysError(ddy_path="/path/to/station.ddy")
        s = str(err)
        assert "/path/to/station.ddy" in s

    def test_neither_name_nor_path(self) -> None:
        err = NoDesignDaysError()
        s = str(err)
        assert "DDY file contains no SizingPeriod:DesignDay objects." in s

    def test_with_nearby_suggestions(self) -> None:
        err = NoDesignDaysError(
            station_name="TestStation",
            nearby_suggestions=["StationA", "StationB", "StationC"],
        )
        s = str(err)
        assert "StationA" in s
        assert "Nearby stations" in s

    def test_is_idfkit_error(self) -> None:
        assert isinstance(NoDesignDaysError(), IdfKitError)


class TestUnsupportedVersionError:
    def test_basic(self) -> None:
        err = UnsupportedVersionError((9, 8, 0), ENERGYPLUS_VERSIONS)
        assert err.version == (9, 8, 0)
        assert "9.8.0" in str(err)
        assert "is not supported" in str(err)

    def test_lists_supported_versions(self) -> None:
        err = UnsupportedVersionError((99, 0, 0), ENERGYPLUS_VERSIONS)
        assert "8.9.0" in str(err)
        assert "25.2.0" in str(err)

    def test_stores_supported_versions(self) -> None:
        err = UnsupportedVersionError((9, 8, 0), ENERGYPLUS_VERSIONS)
        assert err.supported_versions == ENERGYPLUS_VERSIONS

    def test_is_idfkit_error(self) -> None:
        assert isinstance(UnsupportedVersionError((1, 0, 0), ()), IdfKitError)


class TestUnsupportedVersionIntegration:
    def test_new_document_rejects_unsupported_version(self) -> None:
        from idfkit import new_document

        with pytest.raises(UnsupportedVersionError, match=r"9\.8\.0"):
            new_document(version=(9, 8, 0))

    def test_new_document_rejects_nonexistent_version(self) -> None:
        from idfkit import new_document

        with pytest.raises(UnsupportedVersionError, match=r"99\.0\.0"):
            new_document(version=(99, 0, 0))

    def test_new_document_accepts_supported_version(self) -> None:
        from idfkit import new_document

        doc = new_document(version=(24, 1, 0))
        assert doc.version == (24, 1, 0)

    def test_load_idf_rejects_unsupported_version(self, tmp_path: object) -> None:
        import pathlib

        from idfkit import load_idf

        idf_path = pathlib.Path(str(tmp_path)) / "test.idf"
        idf_path.write_text("Version, 24.1;\n")
        with pytest.raises(UnsupportedVersionError, match=r"9\.8\.0"):
            load_idf(str(idf_path), version=(9, 8, 0))

    def test_load_idf_allows_none_version(self, tmp_path: object) -> None:
        """Auto-detected versions from files should still use closest-version fallback."""
        import pathlib

        from idfkit import load_idf

        idf_path = pathlib.Path(str(tmp_path)) / "test.idf"
        idf_path.write_text("Version, 24.1;\n")
        doc = load_idf(str(idf_path))
        assert doc.version == (24, 1, 0)
