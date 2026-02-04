"""Tests for custom exceptions."""

from __future__ import annotations

from idfkit.exceptions import (
    DanglingReferenceError,
    DuplicateObjectError,
    IdfKitError,
    InvalidFieldError,
    ParseError,
    SchemaNotFoundError,
    UnknownObjectTypeError,
    ValidationFailedError,
    VersionNotFoundError,
)
from idfkit.objects import IDFObject


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
