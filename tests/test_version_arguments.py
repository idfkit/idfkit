"""A version given as a string to an API that takes a tuple raises a TypeError that names the tuple."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import idfkit
from idfkit import find_closest_version, get_schema, is_supported_version, load_epjson, load_idf, new_document
from idfkit.schema import SchemaManager
from idfkit.versions import find_release, reject_version_string


class TestRejectVersionString:
    def test_tuple_passes(self) -> None:
        reject_version_string((24, 1, 0))

    @pytest.mark.parametrize(
        ("value", "example"),
        [
            ("26.1", "(26, 1, 0)"),
            ("26.1.0", "(26, 1, 0)"),
            ("v24.2", "(24, 2, 0)"),
            ("24-1-0", "(24, 1, 0)"),
        ],
    )
    def test_string_names_its_tuple(self, value: str, example: str) -> None:
        with pytest.raises(TypeError) as info:
            reject_version_string(value)
        assert str(info.value) == f"version must be a (major, minor, patch) tuple, e.g. {example}; got {value!r}"

    def test_unparsable_string_names_the_latest_release(self) -> None:
        latest = idfkit.LATEST_VERSION
        with pytest.raises(TypeError) as info:
            reject_version_string("latest")
        assert f"e.g. ({latest[0]}, {latest[1]}, {latest[2]}); got 'latest'" in str(info.value)


_CALLS: dict[str, Callable[[Any], object]] = {
    "new_document": lambda v: new_document(version=v),
    "get_schema": get_schema,
    "SchemaManager.get_schema": lambda v: SchemaManager().get_schema(v),
    "is_supported_version": is_supported_version,
    "find_closest_version": find_closest_version,
    "find_release": find_release,
}


@pytest.mark.parametrize("name", sorted(_CALLS))
def test_public_functions_refuse_a_string(name: str) -> None:
    """Each of these read a string as a sequence of characters, or compared it with a tuple."""
    with pytest.raises(
        TypeError, match=r"version must be a \(major, minor, patch\) tuple, e\.g\. \(26, 1, 0\); got '26\.1'"
    ):
        _CALLS[name]("26.1")


@pytest.mark.parametrize("loader", [load_idf, load_epjson])
def test_loader_version_override_refuses_a_string(loader: Callable[..., object], tmp_path: Path) -> None:
    # Refused before the file is read, so the file need not exist.
    with pytest.raises(TypeError, match=r"e\.g\. \(24, 1, 0\); got '24\.1'"):
        loader(tmp_path / "model.idf", version="24.1")


def test_tuple_versions_still_work() -> None:
    assert is_supported_version((24, 1, 0))
    assert not is_supported_version((99, 0, 0))
    assert find_closest_version((9, 0, 0)) == (9, 0, 1)
    assert new_document(version=(24, 1, 0)).version == (24, 1, 0)
