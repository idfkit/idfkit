"""Tests for custom exceptions."""

from __future__ import annotations

import pytest

from idfkit.exceptions import (
    DanglingReferenceError,
    DuplicateObjectError,
    ExpandObjectsError,
    IdfKitError,
    InvalidFieldError,
    ParseError,
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

    def test_is_idfkit_error(self) -> None:
        assert isinstance(UnknownObjectTypeError("X"), IdfKitError)


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

    def test_is_idfkit_error(self) -> None:
        assert isinstance(InvalidFieldError("Z", "f"), IdfKitError)


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


class TestValidationFailedError:
    def test_basic(self) -> None:
        errors: list[object] = ["error 1", "error 2"]
        err = ValidationFailedError(errors)
        assert err.errors == errors
        assert "2 error(s)" in str(err)

    def test_truncation(self) -> None:
        errors: list[object] = [f"error {i}" for i in range(10)]
        err = ValidationFailedError(errors)
        assert "5 more errors" in str(err)

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
